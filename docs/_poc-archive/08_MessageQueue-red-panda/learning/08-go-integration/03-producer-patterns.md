# 03. Producer Patterns

> **이론**: `02-fundamentals/04-producer-deep-dive.md`
> **Spring 대응**: `03-spring-boot-integration/03-producer-consumer.md` (전반부)
> **이 문서**: Go franz-go Producer 구현 패턴에 집중.

## 목표

- 동기/비동기 Producer 구현
- 파티셔닝 전략 이해 및 커스텀 파티셔너
- 레코드 헤더 활용
- 배치 최적화

## 동기 vs 비동기 Produce

Spring Boot에서 `KafkaTemplate.send()`는 `CompletableFuture`를 반환한다. franz-go는 두 가지 방식을 제공하며, 선택 기준은 처리량과 지연 허용도다.

### 동기 Produce (ProduceSync)

```go
func syncProduce(client *kgo.Client, topic, key string, value []byte) error {
    record := &kgo.Record{
        Topic: topic,
        Key:   []byte(key),
        Value: value,
    }

    // ProduceSync: 브로커 응답까지 블로킹
    results := client.ProduceSync(context.Background(), record)
    for _, r := range results {
        if r.Err != nil {
            return fmt.Errorf("produce 실패: %w", r.Err)
        }
        fmt.Printf("produced to %s[%d]@%d\n",
            r.Record.Topic, r.Record.Partition, r.Record.Offset)
    }
    return nil
}
```

`ProduceSync`는 여러 레코드를 한 번에 전달할 수도 있다. 내부적으로 배치로 묶어 전송하지만, 모든 레코드의 응답을 받을 때까지 블로킹한다.

```go
// 여러 레코드 동기 전송
records := []*kgo.Record{
    {Topic: "orders", Key: []byte("k1"), Value: []byte("v1")},
    {Topic: "orders", Key: []byte("k2"), Value: []byte("v2")},
}
results := client.ProduceSync(ctx, records...)
if err := results.FirstErr(); err != nil {
    log.Printf("일부 실패: %v", err)
}
```

### 비동기 Produce (Produce + 콜백)

```go
func asyncProduce(client *kgo.Client, topic, key string, value []byte) {
    record := &kgo.Record{
        Topic: topic,
        Key:   []byte(key),
        Value: value,
    }

    // Produce: 콜백으로 결과 수신 (non-blocking)
    client.Produce(context.Background(), record, func(r *kgo.Record, err error) {
        if err != nil {
            log.Printf("produce 실패: %v", err)
            return
        }
        fmt.Printf("produced to %s[%d]@%d\n", r.Topic, r.Partition, r.Offset)
    })
}
```

Spring의 `ListenableFuture.addCallback()`에 해당하는 패턴이다. 콜백은 브로커 응답을 받은 시점에 별도 goroutine에서 호출된다.

### 완료 대기 (Flush)

비동기 produce 후 모든 레코드가 전송될 때까지 대기하려면 `Flush()`를 사용한다. 애플리케이션 종료 직전이나 배치 처리 완료 시점에 활용한다.

```go
// 여러 레코드 비동기 전송
for i := 0; i < 100; i++ {
    client.Produce(ctx, &kgo.Record{
        Topic: "batch-topic",
        Value: []byte(fmt.Sprintf("msg-%d", i)),
    }, nil) // 콜백 nil = 결과 무시
}

// 모든 버퍼링된 레코드 전송 완료 대기
if err := client.Flush(ctx); err != nil {
    log.Fatalf("flush 실패: %v", err)
}
fmt.Println("모든 메시지 전송 완료")
```

## 파티셔닝

### 기본 파티셔너

franz-go는 `StickyKeyPartitioner`를 기본 사용한다. 키가 있으면 해시 기반으로 파티션을 결정하고, 키가 없으면 sticky(같은 배치에서 동일 파티션)를 사용하여 배치 효율을 높인다.

```go
// 기본 (키 해시 → 파티션, 키 없으면 sticky)
kgo.RecordPartitioner(kgo.StickyKeyPartitioner(nil))

// 라운드 로빈 (파티션 고른 분산, 배치 효율 낮음)
kgo.RecordPartitioner(kgo.RoundRobinPartitioner())

// 수동 파티션 지정 (레코드 단위)
record := &kgo.Record{
    Topic:     "my-topic",
    Partition: 2, // 직접 지정
    Value:     []byte("targeted"),
}
```

### 커스텀 파티셔너

비즈니스 로직 기반 파티셔닝이 필요한 경우 `kgo.Partitioner` 인터페이스를 구현한다.

```go
import "hash/crc32"

type regionPartitioner struct{}

func (r *regionPartitioner) ForTopic(topic string) kgo.TopicPartitioner {
    return &regionTopicPartitioner{}
}

type regionTopicPartitioner struct{}

func (r *regionTopicPartitioner) RequiresConsistency(_ *kgo.Record) bool {
    // true: 파티션 수 변경 시에도 같은 키 → 같은 파티션 보장
    return true
}

func (r *regionTopicPartitioner) Partition(rec *kgo.Record, n int) int {
    region := string(rec.Key)
    switch region {
    case "KR":
        return 0 % n
    case "US":
        return 1 % n
    case "EU":
        return 2 % n
    default:
        // 알 수 없는 지역: 키 해시로 분산
        return int(crc32.ChecksumIEEE(rec.Key)) % n
    }
}

// 클라이언트에 등록
client, err := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.RecordPartitioner(&regionPartitioner{}),
)
```

## 레코드 헤더

Kafka 헤더는 메타데이터를 메시지 본문과 분리하여 전달하는 표준 방법이다. Spring의 `ProducerRecord.headers()`에 대응하며, 이벤트 타입, 추적 ID, 소스 정보 등을 담는다.

```go
import "github.com/google/uuid"

record := &kgo.Record{
    Topic: "order-events",
    Key:   []byte("order-123"),
    Value: orderJSON,
    Headers: []kgo.RecordHeader{
        {Key: "event-type", Value: []byte("OrderCreated")},
        {Key: "correlation-id", Value: []byte(uuid.New().String())},
        {Key: "source", Value: []byte("order-service")},
        {Key: "timestamp", Value: []byte(time.Now().Format(time.RFC3339))},
    },
}
```

### 헤더 읽기 (Consumer 측)

```go
func getHeader(r *kgo.Record, key string) string {
    for _, h := range r.Headers {
        if h.Key == key {
            return string(h.Value)
        }
    }
    return ""
}

// 사용
eventType := getHeader(r, "event-type")
correlationID := getHeader(r, "correlation-id")
```

## 배치 최적화

처리량을 높이려면 배치 크기와 대기 시간을 조정한다. 이 설정은 Spring의 `spring.kafka.producer.batch-size`, `spring.kafka.producer.linger-ms`에 해당한다.

```go
client, err := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    // 배치 최대 크기 (바이트) - 기본 1MB
    kgo.ProducerBatchMaxBytes(1_000_000),
    // 배치 대기 시간 - 기본 0 (즉시 전송)
    // 높일수록 배치 효율 상승, 지연 증가
    kgo.ProducerLinger(10*time.Millisecond),
    // 버퍼링 최대 레코드 수
    kgo.MaxBufferedRecords(10_000),
    // 압축 (CPU 사용 증가, 네트워크 절약)
    kgo.ProducerBatchCompression(kgo.SnappyCompression()),
)
```

### 처리량 vs 지연 트레이드오프

| 설정 | 높은 처리량 | 낮은 지연 |
|------|:---------:|:--------:|
| `ProducerLinger` | 10~50ms | 0ms |
| `ProducerBatchMaxBytes` | 1MB+ | 64KB |
| `MaxBufferedRecords` | 50,000+ | 1,000 |
| Compression | Snappy/LZ4 | None |

## Spring Boot vs Go 매핑

| Spring Boot | Go (franz-go) | 비고 |
|-------------|---------------|------|
| `KafkaTemplate.send()` | `client.Produce(ctx, rec, callback)` | 비동기 |
| `template.send().get()` | `client.ProduceSync(ctx, rec)` | 동기 |
| `ProducerConfig.PARTITIONER_CLASS` | `kgo.RecordPartitioner(...)` | 파티셔너 |
| `ProducerRecord.headers()` | `kgo.Record.Headers` | 헤더 |
| `spring.kafka.producer.batch-size` | `kgo.ProducerBatchMaxBytes(...)` | 배치 크기 |
| `spring.kafka.producer.linger-ms` | `kgo.ProducerLinger(...)` | 배치 대기 |
| `spring.kafka.producer.compression-type` | `kgo.ProducerBatchCompression(...)` | 압축 |

## 실습 TODO

```
TODO 1: 동기 Producer로 10개 메시지 전송 후 partition/offset 출력
TODO 2: 비동기 Producer + 콜백으로 100개 메시지 전송, Flush로 완료 대기
TODO 3: 커스텀 파티셔너 구현 (region 기반: KR→0, US→1, EU→2)
TODO 4: 헤더 포함 레코드 전송 후 Consumer에서 헤더 읽기
TODO 5: ProducerLinger 0ms vs 10ms 처리량 비교 (1000개 메시지 기준)
```

## 체크포인트

- [ ] 동기/비동기 produce 결과에서 partition, offset 확인
- [ ] 같은 키 → 같은 파티션 할당 검증 (10회 반복)
- [ ] 커스텀 파티셔너로 region별 파티션 분리 확인
- [ ] 헤더 값 produce → consume 라운드트립 성공
- [ ] Linger 설정 변경 시 처리량 차이 로그로 확인
