# Go Integration: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

---

## Q1. franz-go vs confluent-kafka-go — 어떤 기준으로 선택하는가?

### 왜 이 질문이 중요한가

Go 신규 서비스에서 Kafka 클라이언트를 선택할 때 이 두 라이브러리가 가장 먼저 비교 대상에 오른다. "왜 franz-go를 썼나요?"라고 물어볼 때 "순수 Go니까요"로 끝내면 약하다. CGO가 빌드와 배포에 미치는 실질적 영향까지 설명할 수 있어야 한다.

### 답변

confluent-kafka-go는 librdkafka C 라이브러리를 CGO로 감싼 래퍼다. 이를 Go에서 사용하는 비용이 있다. alpine 기반 Docker 이미지에서 `CGO_ENABLED=1` + `musl libc` 조합이 링크 오류를 내고, scratch 이미지는 사용이 불가하며, 크로스 컴파일도 CGO 툴체인 없이는 동작하지 않는다.

```dockerfile
# confluent-kafka-go: gcc 의존
FROM golang:1.22-alpine AS builder
RUN apk add --no-cache gcc musl-dev
RUN CGO_ENABLED=1 go build ./...

# franz-go: scratch도 가능
FROM golang:1.22-alpine AS builder
RUN CGO_ENABLED=0 go build ./...
FROM scratch
COPY --from=builder /app/server /server
```

선택 기준은 명확하다. 순수 Go와 컨테이너 배포, 크로스 컴파일이 필요하면 franz-go를 선택한다. Confluent 공식 지원 SLA나 librdkafka 성숙도가 더 중요한 환경이라면 confluent-kafka-go가 맞다.

---

## Q2. Go 컨슈머 동시성 모델 — goroutine per partition vs worker pool

### 왜 이 질문이 중요한가

"처리량을 높이려면 어떻게 했나요?"라는 실무 질문에서 패턴명과 순서 보장 트레이드오프를 함께 답할 수 있어야 한다. 잘못 선택하면 파티션 내 순서가 깨지거나 goroutine 누수가 발생한다.

### 답변

franz-go의 `PollFetches`는 여러 파티션의 레코드를 한 번에 반환한다. 처리 방식에 따라 두 패턴으로 나뉜다.

**goroutine per partition**: 파티션별 전용 goroutine이 순서를 보장한다. 결제처럼 동일 키의 순서가 중요한 도메인에 적합하다.

```go
fetches.EachPartition(func(p kgo.FetchTopicPartition) {
    ch := getOrCreateWorker(p.Partition) // 파티션별 채널
    p.EachRecord(func(r *kgo.Record) { ch <- r })
})
```

**worker pool**: N개 goroutine이 파티션 무관하게 레코드를 처리한다. 순서가 깨지지만 처리량이 높다. 로그 집계나 통계처럼 순서가 무의미한 도메인에 적합하다.

핵심 원칙은 "파티션 순서 보장과 처리량은 trade-off"라는 것이다. 비즈니스 이벤트 대부분은 goroutine per partition이 안전하다.

---

## Q3. Go에서 Avro 직렬화 — hamba/avro의 한계와 Schema Registry 통합 주의점

### 왜 이 질문이 중요한가

Java Avro는 `.avsc`에서 코드를 자동 생성하는 방식이 일반적이다. Go에는 성숙한 코드 생성 도구가 없어 hamba/avro의 struct 태그 방식을 주로 쓴다. 이 방식의 한계를 모르면 Schema Registry 연동 시 런타임 에러가 발생한다.

### 답변

가장 흔한 실수는 `avro.Marshal`만 호출하고 Schema Registry wire format의 5바이트 magic header를 빠뜨리는 것이다.

```go
// 잘못된 방식: 헤더 없이 직렬화 → Consumer에서 "unknown magic byte" 에러
b, _ := avro.Marshal(schema, &event)

// 올바른 방식: sr.Serde가 [0x00][schemaID 4bytes][payload] 헤더 자동 처리
var serde sr.Serde
serde.Register(schemaID, OrderEvent{},
    sr.EncodeFn(func(v any) ([]byte, error) { return avro.Marshal(schema, v) }),
    sr.DecodeFn(func(b []byte, v any) error { return avro.Unmarshal(schema, b, v) }),
)
b, _ := serde.Encode(&event)
```

hamba/avro의 추가 한계: Avro enum을 Go `string`으로 매핑하므로 잘못된 값이 컴파일 타임에 잡히지 않는다. Union 타입은 `map[string]interface{}`로 표현해야 해서 타입 안전성이 떨어진다. 스키마 진화 시 태그 없는 필드는 조용히 누락된다.

---

## Q4. Go Kafka 클라이언트 에러 핸들링 — context 취소, 재시도, graceful shutdown

### 왜 이 질문이 중요한가

"서비스 종료 시 메시지 손실 없이 어떻게 보장했나요?"는 실무 면접 단골 질문이다. context, signal, WaitGroup이 어떻게 맞물려 graceful shutdown을 구현하는지 코드 수준으로 설명할 수 있어야 한다.

### 답변

```go
func main() {
    ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
    defer stop()

    var wg sync.WaitGroup
    wg.Add(1)
    go func() {
        defer wg.Done()
        consumeLoop(ctx, client) // ctx 취소 시 PollFetches 반환
    }()

    <-ctx.Done()
    client.CloseAllowingRebalance() // 파티션 반납 먼저
    wg.Wait()                       // in-flight 처리 완료 대기
    client.Close()                  // 연결 종료
}
```

`CloseAllowingRebalance()`를 `Close()` 전에 호출하는 순서가 중요하다. 이 순서를 바꾸면 리밸런스 타임아웃까지 파티션이 잠겨 다른 Consumer의 처리 지연이 발생한다.

재시도 시에는 `ctx.Done()` 채널을 반드시 확인해야 한다. context가 취소된 상황에서도 backoff sleep을 기다리면 종료가 지연된다.

```go
select {
case <-ctx.Done():
    return ctx.Err() // 종료 신호면 즉시 중단
case <-time.After(backoff):
    backoff = min(backoff*2, 30*time.Second)
}
```

---

## Q5. testcontainers-go로 통합 테스트 — Redpanda 컨테이너 구성과 테스트 격리

### 왜 이 질문이 중요한가

"Kafka 의존 코드를 어떻게 테스트했나요?"에 mock만 답하면 통합 테스트 경험이 없다는 인상을 준다. testcontainers-go로 실제 Redpanda를 띄우는 패턴과 테스트 간 격리 전략을 설명할 수 있어야 한다.

### 답변

컨테이너는 `TestMain`에서 패키지 전체가 한 번 공유하고, 각 테스트는 UUID 접미사로 고유 토픽을 만드는 방식이 속도와 격리의 균형점이다.

```go
func startRedpanda(t *testing.T) string {
    req := testcontainers.ContainerRequest{
        Image:        "redpandadata/redpanda:v25.1.1",
        ExposedPorts: []string{"19092/tcp"},
        Cmd: []string{
            "redpanda", "start",
            "--overprovisioned", "--smp", "1", "--memory", "200M",
        },
        WaitingFor: wait.ForLog("Started Redpanda!"),
    }
    c, _ := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: req, Started: true,
    })
    host, _ := c.Host(ctx)
    port, _ := c.MappedPort(ctx, "19092")
    return fmt.Sprintf("%s:%s", host, port.Port())
}

// 테스트별 고유 토픽으로 격리
func TestProducer(t *testing.T) {
    topic := "orders-" + uuid.New().String()[:8]
    // ...
}
```

`--overprovisioned --smp 1 --memory 200M` 플래그는 CI 환경의 제한된 리소스에서 Redpanda가 안정적으로 동작하도록 리소스 사용량을 제한한다. 이 플래그 없이 CI에서 실행하면 OOM으로 컨테이너가 죽는 경우가 있다.
