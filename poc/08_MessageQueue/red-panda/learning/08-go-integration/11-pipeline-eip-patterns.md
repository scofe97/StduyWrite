# 11. Pipeline & EIP Patterns

> **이론**: `01-event-driven/16-messaging-patterns-eip.md`
> **Spring 대응**: `03-spring-boot-integration/11-topic-pipeline-architecture.md` + `13-messaging-patterns-impl.md`
> **이 문서**: Go 채널과 goroutine을 활용한 메시징 파이프라인 구현에 집중.

## 목표

- Go 채널 기반 파이프라인 구성
- EIP 패턴 Go 구현 (Router, Splitter, Aggregator)
- Fan-out/Fan-in 패턴
- Kafka Streams 없이 스트림 처리 구현

## Go 채널 파이프라인

Kafka Streams는 JVM 전용이므로 Go에서는 사용할 수 없다. 대신 Go의 goroutine과 channel을 활용하여 유사한 스트림 처리 파이프라인을 구축한다. 각 스테이지는 입력 채널을 받아 출력 채널을 반환하는 함수로 표현된다. Unix 파이프(`cat file | grep pattern | wc -l`)와 개념적으로 동일하다.

### 기본 파이프라인

```go
type Stage func(ctx context.Context, in <-chan *kgo.Record) <-chan *kgo.Record

func pipeline(ctx context.Context, source <-chan *kgo.Record, stages ...Stage) <-chan *kgo.Record {
    current := source
    for _, stage := range stages {
        current = stage(ctx, current)
    }
    return current
}

// Filter 스테이지
func filter(predicate func(*kgo.Record) bool) Stage {
    return func(ctx context.Context, in <-chan *kgo.Record) <-chan *kgo.Record {
        out := make(chan *kgo.Record)
        go func() {
            defer close(out)
            for r := range in {
                if predicate(r) {
                    select {
                    case out <- r:
                    case <-ctx.Done():
                        return
                    }
                }
            }
        }()
        return out
    }
}

// Transform 스테이지
func transform(fn func(*kgo.Record) *kgo.Record) Stage {
    return func(ctx context.Context, in <-chan *kgo.Record) <-chan *kgo.Record {
        out := make(chan *kgo.Record)
        go func() {
            defer close(out)
            for r := range in {
                select {
                case out <- fn(r):
                case <-ctx.Done():
                    return
                }
            }
        }()
        return out
    }
}
```

### Kafka 소스/싱크 연결

```go
func kafkaSource(ctx context.Context, client *kgo.Client) <-chan *kgo.Record {
    out := make(chan *kgo.Record, 100)
    go func() {
        defer close(out)
        for {
            fetches := client.PollFetches(ctx)
            if ctx.Err() != nil {
                return
            }
            fetches.EachRecord(func(r *kgo.Record) {
                select {
                case out <- r:
                case <-ctx.Done():
                    return
                }
            })
        }
    }()
    return out
}

func kafkaSink(ctx context.Context, client *kgo.Client, topic string, in <-chan *kgo.Record) {
    for r := range in {
        r.Topic = topic
        client.Produce(ctx, r, nil)
    }
    client.Flush(ctx)
}
```

### 파이프라인 조합 예시

```go
func runOrderPipeline(ctx context.Context, consumer, producer *kgo.Client) {
    source := kafkaSource(ctx, consumer)

    output := pipeline(ctx, source,
        filter(func(r *kgo.Record) bool {
            return headerValue(r, "event-type") == "OrderCreated"
        }),
        transform(func(r *kgo.Record) *kgo.Record {
            // 금액 필드 마스킹 등 변환
            return enrichRecord(r)
        }),
    )

    kafkaSink(ctx, producer, "processed-orders", output)
}
```

## EIP 패턴

### Content-Based Router

메시지 내용에 따라 다른 토픽으로 라우팅한다. Spring의 `KStream.branch()`와 동일한 역할이다.

```go
func router(routes map[string]string, classify func(*kgo.Record) string) Stage {
    return func(ctx context.Context, in <-chan *kgo.Record) <-chan *kgo.Record {
        out := make(chan *kgo.Record)
        go func() {
            defer close(out)
            for r := range in {
                category := classify(r)
                if topic, ok := routes[category]; ok {
                    r.Topic = topic
                }
                select {
                case out <- r:
                case <-ctx.Done():
                    return
                }
            }
        }()
        return out
    }
}

// 사용 예: 주문 등급별 라우팅
routes := map[string]string{
    "VIP":     "orders-vip",
    "REGULAR": "orders-regular",
    "BULK":    "orders-bulk",
}
classify := func(r *kgo.Record) string {
    return headerValue(r, "customer-tier")
}
```

### Fan-out

하나의 메시지를 여러 채널에 복제하여 전달한다. Spring의 `KStream`을 여러 번 subscribe하는 것과 동일하다.

```go
func fanOut(ctx context.Context, in <-chan *kgo.Record, n int) []<-chan *kgo.Record {
    outs := make([]chan *kgo.Record, n)
    for i := range outs {
        outs[i] = make(chan *kgo.Record, 10)
    }
    go func() {
        defer func() {
            for _, ch := range outs {
                close(ch)
            }
        }()
        for r := range in {
            for _, ch := range outs {
                select {
                case ch <- r:
                case <-ctx.Done():
                    return
                }
            }
        }
    }()

    result := make([]<-chan *kgo.Record, n)
    for i, ch := range outs {
        result[i] = ch
    }
    return result
}
```

### Fan-in

여러 채널의 메시지를 하나로 합친다. Spring의 `StreamsBuilder.merge()`와 동일하다.

```go
func fanIn(ctx context.Context, channels ...<-chan *kgo.Record) <-chan *kgo.Record {
    out := make(chan *kgo.Record)
    var wg sync.WaitGroup
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan *kgo.Record) {
            defer wg.Done()
            for r := range c {
                select {
                case out <- r:
                case <-ctx.Done():
                    return
                }
            }
        }(ch)
    }
    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}
```

### Request-Reply (Spring의 ReplyingKafkaTemplate 대체)

Go에는 `ReplyingKafkaTemplate`이 없으므로 직접 구현한다. `correlation-id` 헤더로 요청과 응답을 매핑한다.

```go
func requestReply(ctx context.Context, client *kgo.Client, requestTopic, replyTopic string, request []byte) ([]byte, error) {
    correlationID := uuid.New().String()

    // Reply Consumer 준비 (AtEnd: 이후 메시지만 수신)
    replyClient, err := kgo.NewClient(
        kgo.SeedBrokers("localhost:19092"),
        kgo.ConsumeTopics(replyTopic),
        kgo.ConsumeResetOffset(kgo.NewOffset().AtEnd()),
    )
    if err != nil {
        return nil, err
    }
    defer replyClient.Close()

    // Request 전송
    client.ProduceSync(ctx, &kgo.Record{
        Topic: requestTopic,
        Value: request,
        Headers: []kgo.RecordHeader{
            {Key: "correlation-id", Value: []byte(correlationID)},
            {Key: "reply-topic", Value: []byte(replyTopic)},
        },
    })

    // Reply 대기
    timeout, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()

    for {
        fetches := replyClient.PollFetches(timeout)
        if timeout.Err() != nil {
            return nil, fmt.Errorf("reply timeout")
        }
        var reply []byte
        fetches.EachRecord(func(r *kgo.Record) {
            if headerValue(r, "correlation-id") == correlationID {
                reply = r.Value
            }
        })
        if reply != nil {
            return reply, nil
        }
    }
}

func headerValue(r *kgo.Record, key string) string {
    for _, h := range r.Headers {
        if h.Key == key {
            return string(h.Value)
        }
    }
    return ""
}
```

## Kafka Streams vs Go 파이프라인

| Kafka Streams | Go 파이프라인 | 한계 |
|---------------|-------------|------|
| KTable (상태 저장) | sync.Map 또는 DB | 분산 상태 없음 |
| Window 연산 | time.Ticker + 버퍼 | 수동 구현 필요 |
| 자동 리밸런스 | Consumer Group 의존 | 파티션별 파이프라인 |
| Exactly-once | 트랜잭션 + 멱등성 | 수동 보장 |

## Spring Boot vs Go 매핑

| Spring Boot | Go | 비고 |
|-------------|-----|------|
| `@SendTo("output")` | `kafkaSink(client, topic, ch)` | 출력 토픽 |
| `StreamsBuilder.stream()` | `kafkaSource(ctx, client)` | 입력 소스 |
| `KStream.filter()` | `filter(predicate)` 스테이지 | 필터 |
| `KStream.mapValues()` | `transform(fn)` 스테이지 | 변환 |
| `KStream.branch()` | `router(routes, classify)` | 라우팅 |
| `ReplyingKafkaTemplate` | `requestReply()` 직접 구현 | 요청-응답 |

## 실습 TODO

```
TODO 1: kafkaSource → filter → transform → kafkaSink 기본 파이프라인
TODO 2: Content-Based Router (주문 유형별 토픽 분기)
TODO 3: Fan-out (1 입력 → 3 출력 채널)
TODO 4: Fan-in (3 입력 → 1 출력 채널)
TODO 5: Request-Reply 패턴 구현
```

## 체크포인트

- [ ] 파이프라인 입력 → 필터 → 변환 → 출력 확인
- [ ] Router로 메시지 유형별 다른 토픽 전달
- [ ] Fan-out: 동일 메시지 3개 채널에 복제
- [ ] Fan-in: 3개 소스 → 1개 출력 머지
- [ ] Request-Reply: 30초 내 응답 수신
