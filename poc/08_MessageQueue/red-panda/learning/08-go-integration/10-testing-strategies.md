# 10. Testing Strategies

> **이론**: `02-fundamentals/10-testing.md`
> **Spring 대응**: `03-spring-boot-integration/10-testing.md`
> **이 문서**: Go 테스트 패턴과 testcontainers-go 활용에 집중.

## 목표

- Go 테이블 드리븐 테스트 패턴
- testcontainers-go로 Redpanda 통합 테스트
- Producer/Consumer 테스트 전략
- 테스트 격리 및 병렬 실행

## Go 테스트 기본

Go는 `testing` 패키지와 `go test` 명령어로 테스트를 실행한다. Spring의 `@SpringBootTest` 같은 프레임워크 지원 없이, 필요한 의존성을 직접 구성한다. 테스트 함수명은 반드시 `Test`로 시작해야 한다.

### 테이블 드리븐 테스트

JUnit의 `@ParameterizedTest`와 동일한 역할을 Go 관용구로 표현한다. 케이스를 슬라이스로 나열하고 `t.Run()`으로 각각 실행하면 실패 시 어느 케이스인지 이름으로 명확히 식별된다.

```go
func TestClassifyError(t *testing.T) {
    tests := []struct {
        name string
        err  error
        want ErrorKind
    }{
        {"timeout", context.DeadlineExceeded, Retryable},
        {"json syntax", &json.SyntaxError{}, NonRetryable},
        {"nil error", nil, NonRetryable},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := classifyError(tt.err)
            if got != tt.want {
                t.Errorf("classifyError(%v) = %v, want %v", tt.err, got, tt.want)
            }
        })
    }
}
```

## testcontainers-go

Spring Boot 프로젝트에서는 `@ActiveProfiles("local")` + docker-compose로 로컬 인프라를 사용했다. Go에서는 testcontainers-go로 테스트 내에서 Redpanda를 자동 시작/종료하여 외부 의존성 없이 실행할 수 있다. Redpanda는 testcontainers-go 전용 모듈을 제공하므로 설정이 간단하다.

```go
import (
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/redpanda"
)

func setupRedpanda(t *testing.T) (string, func()) {
    t.Helper()
    ctx := context.Background()

    container, err := redpanda.Run(ctx,
        "docker.redpanda.com/redpandadata/redpanda:v24.3.1",
        redpanda.WithAutoCreateTopics(),
    )
    if err != nil {
        t.Fatalf("redpanda 시작 실패: %v", err)
    }

    brokers, err := container.KafkaSeedBroker(ctx)
    if err != nil {
        t.Fatalf("broker 주소 조회 실패: %v", err)
    }

    cleanup := func() {
        container.Terminate(ctx)
    }

    return brokers, cleanup
}
```

### Schema Registry 주소도 함께 얻기

```go
func setupRedpandaFull(t *testing.T) (brokers string, schemaURL string, cleanup func()) {
    t.Helper()
    ctx := context.Background()

    container, err := redpanda.Run(ctx,
        "docker.redpanda.com/redpandadata/redpanda:v24.3.1",
        redpanda.WithAutoCreateTopics(),
    )
    if err != nil {
        t.Fatalf("redpanda 시작 실패: %v", err)
    }

    brokers, err = container.KafkaSeedBroker(ctx)
    if err != nil {
        t.Fatalf("broker 주소 조회 실패: %v", err)
    }

    schemaURL, err = container.SchemaRegistryAddress(ctx)
    if err != nil {
        t.Fatalf("schema registry 주소 조회 실패: %v", err)
    }

    cleanup = func() { container.Terminate(ctx) }
    return
}
```

## Producer/Consumer 통합 테스트

### 라운드트립 테스트

```go
func TestProduceAndConsume(t *testing.T) {
    brokers, cleanup := setupRedpanda(t)
    defer cleanup()

    topic := uniqueTopic(t)

    // Producer
    producer, err := kgo.NewClient(kgo.SeedBrokers(brokers))
    if err != nil {
        t.Fatal(err)
    }
    defer producer.Close()

    results := producer.ProduceSync(context.Background(), &kgo.Record{
        Topic: topic,
        Key:   []byte("key-1"),
        Value: []byte("value-1"),
    })
    if err := results.FirstErr(); err != nil {
        t.Fatalf("produce 실패: %v", err)
    }

    // Consumer
    consumer, err := kgo.NewClient(
        kgo.SeedBrokers(brokers),
        kgo.ConsumerGroup(uniqueGroup(t)),
        kgo.ConsumeTopics(topic),
        kgo.ConsumeResetOffset(kgo.NewOffset().AtStart()),
    )
    if err != nil {
        t.Fatal(err)
    }
    defer consumer.Close()

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    fetches := consumer.PollFetches(ctx)
    if errs := fetches.Errors(); len(errs) > 0 {
        t.Fatalf("fetch errors: %v", errs)
    }

    records := fetches.Records()
    if len(records) != 1 {
        t.Fatalf("expected 1 record, got %d", len(records))
    }
    if string(records[0].Value) != "value-1" {
        t.Errorf("expected value-1, got %s", string(records[0].Value))
    }
}
```

### 멱등성 Consumer 테스트

같은 메시지를 두 번 전송해도 처리가 한 번만 발생하는지 검증한다.

```go
func TestIdempotentConsumer(t *testing.T) {
    brokers, cleanup := setupRedpanda(t)
    defer cleanup()

    topic := uniqueTopic(t)
    db := setupTestDB(t)
    store := NewIdempotencyStore(db)

    // 동일 메시지 2회 produce
    producer, _ := kgo.NewClient(kgo.SeedBrokers(brokers))
    defer producer.Close()

    for i := 0; i < 2; i++ {
        producer.ProduceSync(context.Background(), &kgo.Record{
            Topic: topic,
            Key:   []byte("order-123"),
            Value: []byte(`{"orderId":"order-123"}`),
            Headers: []kgo.RecordHeader{
                {Key: "event-type", Value: []byte("OrderCreated")},
            },
        })
    }

    // Consumer에서 처리 횟수 카운트
    processCount := 0
    consumer, _ := kgo.NewClient(
        kgo.SeedBrokers(brokers),
        kgo.ConsumerGroup(uniqueGroup(t)),
        kgo.ConsumeTopics(topic),
        kgo.ConsumeResetOffset(kgo.NewOffset().AtStart()),
    )
    defer consumer.Close()

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    for processCount < 2 {
        fetches := consumer.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }
        fetches.EachRecord(func(r *kgo.Record) {
            acquired, _ := store.TryAcquire(ctx, "order-123", "OrderCreated")
            if acquired {
                processCount++
            }
        })
        consumer.CommitUncommittedOffsets(ctx)
    }

    if processCount != 1 {
        t.Errorf("expected 1 processing, got %d", processCount)
    }
}
```

## 테스트 격리

테스트 간 상태가 공유되면 순서 의존성이 생기고 플레이키(flaky) 테스트가 된다. 고유 토픽/그룹명으로 완전한 격리를 보장한다.

```go
func uniqueTopic(t *testing.T) string {
    t.Helper()
    // t.Name()은 슬래시 포함 가능 → 대체
    name := strings.ReplaceAll(t.Name(), "/", "-")
    return fmt.Sprintf("test-%s-%d", name, time.Now().UnixNano())
}

func uniqueGroup(t *testing.T) string {
    t.Helper()
    name := strings.ReplaceAll(t.Name(), "/", "-")
    return fmt.Sprintf("group-%s-%d", name, time.Now().UnixNano())
}
```

### 병렬 테스트

`t.Parallel()`을 추가하면 테스트가 병렬로 실행된다. 고유 토픽/그룹명을 사용하면 격리가 보장되므로 충돌이 없다.

```go
func TestParallelConsume(t *testing.T) {
    t.Parallel() // 이 줄만 추가하면 병렬 실행
    brokers, cleanup := setupRedpanda(t)
    defer cleanup()
    // ...
}
```

## DLQ 라우팅 통합 테스트

```go
func TestDLQRouting(t *testing.T) {
    brokers, cleanup := setupRedpanda(t)
    defer cleanup()

    inputTopic := uniqueTopic(t)
    dlqTopic := inputTopic + "-dlq"

    // invalid JSON 전송 → DLQ로 라우팅되어야 함
    producer, _ := kgo.NewClient(kgo.SeedBrokers(brokers))
    defer producer.Close()

    producer.ProduceSync(context.Background(), &kgo.Record{
        Topic: inputTopic,
        Value: []byte("not-valid-json"),
    })

    // DLQ Consumer
    dlqConsumer, _ := kgo.NewClient(
        kgo.SeedBrokers(brokers),
        kgo.ConsumerGroup(uniqueGroup(t)),
        kgo.ConsumeTopics(dlqTopic),
        kgo.ConsumeResetOffset(kgo.NewOffset().AtStart()),
    )
    defer dlqConsumer.Close()

    ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
    defer cancel()

    fetches := dlqConsumer.PollFetches(ctx)
    records := fetches.Records()

    if len(records) == 0 {
        t.Error("DLQ에 레코드가 없음: 라우팅 실패")
    }
}
```

## Spring Boot vs Go 매핑

| Spring Boot | Go | 비고 |
|-------------|-----|------|
| `@SpringBootTest` | `func TestXxx(t *testing.T)` | 테스트 진입점 |
| `@EmbeddedKafka` | `testcontainers-go/redpanda` | 임베디드 브로커 |
| `@ActiveProfiles("test")` | 환경변수 또는 테스트 설정 | 프로파일 |
| JUnit `@ParameterizedTest` | 테이블 드리븐 테스트 | 매개변수 테스트 |
| Mockito | 인터페이스 + 수동 mock | 목킹 |
| `Awaitility.await()` | `context.WithTimeout` + 폴링 | 비동기 대기 |

## 실습 TODO

```
TODO 1: testcontainers-go로 Redpanda 컨테이너 헬퍼 구현
TODO 2: Producer → Consumer 라운드트립 테스트
TODO 3: DLQ 라우팅 통합 테스트
TODO 4: 멱등성 Consumer 테스트 (같은 메시지 2회 전송)
TODO 5: 테스트 격리 (고유 토픽/그룹명)
TODO 6: t.Parallel() 추가 후 병렬 실행 확인
```

## 체크포인트

- [ ] `go test ./...` 전체 통과
- [ ] testcontainers가 Redpanda 자동 시작/종료
- [ ] 테스트 간 토픽 격리 확인
- [ ] 병렬 테스트 (`t.Parallel()`) 충돌 없음
- [ ] 멱등성 테스트: 2회 전송 → 1회 처리 확인
