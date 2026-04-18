# 13. Production Patterns

> **이론**: `02-fundamentals/12-operations.md`
> **Spring 대응**: `03-spring-boot-integration/17-design-and-tuning.md` + `18-anti-patterns-troubleshooting.md`
> **이 문서**: Go 특화 프로덕션 패턴, goroutine 모델, 튜닝에 집중.

## 목표

- Go 특화 Kafka 안티패턴 식별
- goroutine 기반 동시 소비 모델
- 성능 튜닝 (배치, 압축, 메모리)
- 모니터링 및 메트릭

## Go 특화 안티패턴

### 1. goroutine 누수

context 없이 goroutine을 시작하면 프로세스가 종료될 때까지 종료되지 않는다. `PollFetches`는 context가 취소될 때까지 블로킹하므로 context 전달이 필수다.

```go
// ❌ 안티패턴: context 없는 goroutine
go func() {
    for {
        fetches := client.PollFetches(context.Background()) // 영원히 블로킹
        // ...
    }
}()

// ✅ 올바른 패턴: context로 종료 제어
go func(ctx context.Context) {
    for {
        fetches := client.PollFetches(ctx)
        if ctx.Err() != nil {
            return // context 취소 시 종료
        }
        // ...
    }
}(ctx)
```

### 2. 채널 데드락

버퍼 없는 채널에 goroutine이 쓰려면 반드시 읽는 쪽이 준비되어 있어야 한다. Consumer가 처리 속도가 느리면 Producer goroutine이 영구 블로킹된다.

```go
// ❌ 안티패턴: 버퍼 없는 채널 + 느린 Consumer
ch := make(chan *kgo.Record)

// ✅ 올바른 패턴: 적절한 버퍼
ch := make(chan *kgo.Record, 1000)
```

### 3. Client 역할 혼용

franz-go의 `kgo.Client`는 Producer와 Consumer 역할을 동시에 수행할 수 있지만, Consumer Group과 트랜잭션을 함께 사용하는 CTP(Consume-Transform-Produce) 패턴 외에는 역할별로 분리하는 것이 안전하다.

```go
// ❌ 안티패턴: 하나의 Client로 produce + consume (CTP 아닐 때)
client, _ := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.ConsumerGroup("my-group"),
    kgo.ConsumeTopics("input"),
    kgo.TransactionalID("my-txn"),
)

// ✅ 올바른 패턴: 역할별 Client 분리
producer, _ := kgo.NewClient(kgo.SeedBrokers("localhost:19092"))
consumer, _ := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.ConsumerGroup("my-group"),
    kgo.ConsumeTopics("input"),
)
```

### 4. CommitUncommittedOffsets 누락

`PollFetches` 후 오프셋을 커밋하지 않으면 재시작 시 모든 메시지를 재처리한다. `AutoCommit`을 쓰면 간단하지만, 처리 실패 후 커밋되는 문제가 생긴다. 수동 커밋이 정확하다.

```go
// ❌ 안티패턴: 커밋 없는 루프
for {
    fetches := client.PollFetches(ctx)
    fetches.EachRecord(processRecord)
    // 커밋 없음 → 재시작 시 중복 처리
}

// ✅ 올바른 패턴: 처리 후 커밋
for {
    fetches := client.PollFetches(ctx)
    fetches.EachRecord(processRecord)
    client.CommitUncommittedOffsets(ctx) // 처리 완료 후 커밋
}
```

## goroutine 동시 소비 모델

Spring의 `concurrency=N`은 N개 스레드로 파티션을 병렬 소비한다. Go에서는 goroutine으로 동일한 효과를 달성하되, 파티션 순서를 보장하려면 파티션별로 goroutine을 분리해야 한다.

### 파티션별 goroutine

```go
func consumeConcurrent(ctx context.Context, client *kgo.Client) {
    partitionCh := make(map[int32]chan *kgo.Record)
    var mu sync.Mutex

    getOrCreate := func(partition int32) chan *kgo.Record {
        mu.Lock()
        defer mu.Unlock()
        if ch, ok := partitionCh[partition]; ok {
            return ch
        }
        ch := make(chan *kgo.Record, 100)
        partitionCh[partition] = ch
        go func() {
            for r := range ch {
                processRecord(r)
            }
        }()
        return ch
    }

    for {
        fetches := client.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }
        fetches.EachRecord(func(r *kgo.Record) {
            ch := getOrCreate(r.Partition)
            ch <- r
        })
        client.CommitUncommittedOffsets(ctx)
    }
}
```

### Worker Pool

순서 보장이 불필요하고 처리량이 중요할 때 Worker Pool을 사용한다. 파티션 순서와 무관하게 N개 goroutine이 병렬로 처리한다.

```go
func workerPool(ctx context.Context, client *kgo.Client, poolSize int) {
    jobs := make(chan *kgo.Record, poolSize*10)

    var wg sync.WaitGroup
    for i := 0; i < poolSize; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            for r := range jobs {
                processRecord(r)
            }
        }(i)
    }

    go func() {
        defer close(jobs)
        for {
            fetches := client.PollFetches(ctx)
            if ctx.Err() != nil {
                return
            }
            fetches.EachRecord(func(r *kgo.Record) {
                jobs <- r
            })
            client.CommitUncommittedOffsets(ctx)
        }
    }()

    wg.Wait()
}
```

## 성능 튜닝

### Producer 튜닝

`ProducerLinger`는 배치가 가득 차지 않아도 일정 시간 대기하여 더 큰 배치를 만든다. 처리량 향상과 레이턴시 증가의 트레이드오프다.

```go
producer, _ := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.ProducerBatchMaxBytes(1_048_576),        // 1MB 배치
    kgo.ProducerLinger(5*time.Millisecond),       // 배치 대기
    kgo.MaxBufferedRecords(100_000),              // 버퍼 크기
    kgo.ProducerBatchCompression(
        kgo.ZstdCompression(),                    // zstd (최고 압축률)
    ),
    kgo.RecordDeliveryTimeout(30*time.Second),
)
```

### Consumer 튜닝

```go
consumer, _ := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.FetchMaxBytes(52_428_800),               // 50MB 페치
    kgo.FetchMaxPartitionBytes(10_485_760),       // 10MB/파티션
    kgo.FetchMaxWait(500*time.Millisecond),       // 최대 대기
    kgo.MaxConcurrentFetches(3),                  // 동시 페치 수
)
```

## 메트릭 수집

franz-go는 `kgo.WithHooks()`로 내부 이벤트를 후킹할 수 있다. Spring의 Micrometer 자동 계측과 달리 직접 구현해야 하지만, Prometheus 등 외부 시스템과 자유롭게 연동할 수 있다.

```go
type metrics struct {
    produceCount  atomic.Int64
    consumeCount  atomic.Int64
    produceErrors atomic.Int64
}

func (m *metrics) OnProduceRecordBuffered(r *kgo.Record) {
    m.produceCount.Add(1)
}

func (m *metrics) OnFetchRecordBuffered(r *kgo.Record) {
    m.consumeCount.Add(1)
}

func (m *metrics) OnProduceRecordUnbuffered(r *kgo.Record, err error) {
    if err != nil {
        m.produceErrors.Add(1)
    }
}

func (m *metrics) print() {
    log.Printf("produce=%d consume=%d errors=%d",
        m.produceCount.Load(),
        m.consumeCount.Load(),
        m.produceErrors.Load(),
    )
}

// 사용
m := &metrics{}
client, _ := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.WithHooks(m),
)
```

## Graceful Shutdown 패턴

프로세스 종료 시 처리 중인 레코드를 잃지 않으려면 순서대로 종료해야 한다. context 취소 → 미처리 레코드 flush → 오프셋 커밋 → 클라이언트 종료.

```go
func main() {
    ctx, cancel := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer cancel()

    client, _ := kgo.NewClient(/* opts */)

    defer func() {
        shutdownCtx, shutdownCancel := context.WithTimeout(
            context.Background(), 10*time.Second)
        defer shutdownCancel()

        client.Flush(shutdownCtx)                    // 1. 미처리 produce 완료
        client.CommitUncommittedOffsets(shutdownCtx) // 2. 오프셋 커밋
        client.Close()                               // 3. 연결 종료
        log.Println("graceful shutdown 완료")
    }()

    consume(ctx, client)
}
```

## pprof 프로파일링

goroutine 누수 확인은 `net/http/pprof`를 활용한다. 프로덕션 배포 전 반드시 확인해야 할 항목이다.

```go
import _ "net/http/pprof"

// 별도 goroutine에서 pprof 서버 시작
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()

// 확인 방법
// curl http://localhost:6060/debug/pprof/goroutine?debug=1
// go tool pprof http://localhost:6060/debug/pprof/goroutine
```

## Spring Boot vs Go 매핑

| Spring Boot | Go | 비고 |
|-------------|-----|------|
| `concurrency=N` | goroutine 풀 | 동시 소비 |
| `spring.kafka.producer.batch-size` | `kgo.ProducerBatchMaxBytes` | 배치 |
| `spring.kafka.producer.compression-type` | `kgo.ProducerBatchCompression` | 압축 |
| Micrometer 메트릭 | `kgo.WithHooks()` | 메트릭 |
| `@PreDestroy` | `defer` + `signal.NotifyContext` | Shutdown |
| 스레드 풀 | goroutine + channel | 동시성 모델 |
| JVM heap dump | `go tool pprof` | 메모리 프로파일 |

## 실습 TODO

```
TODO 1: goroutine 누수 탐지 → pprof goroutine 프로파일
TODO 2: 파티션별 goroutine 동시 소비 구현
TODO 3: Worker Pool 패턴 구현 + 처리량 측정
TODO 4: Producer 튜닝 (배치 크기/linger/압축 변경 후 벤치마크)
TODO 5: kgo.WithHooks 메트릭 수집 → 콘솔 출력
TODO 6: Graceful Shutdown 구현 + SIGINT 테스트
```

## 체크포인트

- [ ] goroutine 프로파일에서 누수 없음 확인
- [ ] Worker Pool N=1 vs N=10 처리량 차이 측정
- [ ] 배치/압축 튜닝 후 처리량 향상 확인
- [ ] 메트릭 (produce/consume count, error rate) 실시간 출력
- [ ] SIGINT → 10초 내 graceful shutdown 완료
