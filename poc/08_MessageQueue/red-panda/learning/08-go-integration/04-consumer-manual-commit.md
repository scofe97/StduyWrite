# 04. Consumer & Manual Commit

> **이론**: `02-fundamentals/05-consumer-deep-dive.md`
> **Spring 대응**: `03-spring-boot-integration/03-producer-consumer.md` (후반부) + `04-manual-commit-deep-dive.md`
> **이 문서**: Go franz-go Consumer 구현 및 수동 커밋 전략에 집중.

## 목표

- PollFetches 기반 Consumer 루프 구현
- Consumer Group과 리밸런스 이해
- 수동 커밋 전략 (per-record, per-partition, per-poll)
- Graceful Shutdown

## 기본 Consumer 루프

Spring의 `@KafkaListener`는 프레임워크가 폴링, 역직렬화, 커밋을 자동 처리한다. franz-go는 이 모든 것을 개발자가 직접 제어한다. 더 많은 코드를 요구하지만, 완전한 제어권을 갖는다.

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os/signal"
    "syscall"

    "github.com/twmb/franz-go/pkg/kgo"
)

func main() {
    client, err := kgo.NewClient(
        kgo.SeedBrokers("localhost:19092"),
        kgo.ConsumerGroup("my-go-group"),
        kgo.ConsumeTopics("order-events"),
    )
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    ctx, cancel := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer cancel()

    for {
        fetches := client.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }

        fetches.EachError(func(t string, p int32, err error) {
            log.Printf("fetch error topic=%s partition=%d: %v", t, p, err)
        })

        fetches.EachRecord(func(r *kgo.Record) {
            fmt.Printf("[%s][p%d][o%d] key=%s value=%s\n",
                r.Topic, r.Partition, r.Offset,
                string(r.Key), string(r.Value))
        })
    }
}
```

`PollFetches(ctx)`는 Spring의 `KafkaMessageListenerContainer` 내부 폴링 루프에 해당한다. 차이점은 Go에서는 이 루프가 코드에 노출되어 있다는 것이다. `ctx.Err() != nil` 체크는 SIGINT/SIGTERM 수신 시 루프를 종료하는 graceful shutdown 처리다.

## Consumer Group 설정

```go
client, err := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.ConsumerGroup("my-go-group"),
    kgo.ConsumeTopics("order-events"),
    // 처음 그룹 조인 시 오프셋 위치
    // AtStart(): 처음부터, AtEnd(): 최신부터
    kgo.ConsumeResetOffset(kgo.NewOffset().AtStart()),
)
```

### 리밸런스 콜백

Spring의 `ConsumerRebalanceListener`에 대응한다. 파티션이 재할당될 때 정리 작업이나 상태 초기화에 사용한다.

```go
client, err := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.ConsumerGroup("my-go-group"),
    kgo.ConsumeTopics("order-events"),
    kgo.OnPartitionsAssigned(func(ctx context.Context, cl *kgo.Client, assigned map[string][]int32) {
        for topic, partitions := range assigned {
            log.Printf("assigned: topic=%s partitions=%v", topic, partitions)
        }
    }),
    kgo.OnPartitionsRevoked(func(ctx context.Context, cl *kgo.Client, revoked map[string][]int32) {
        // 중요: revoke 전에 처리 완료된 오프셋을 커밋해야 데이터 손실을 막는다
        if err := cl.CommitUncommittedOffsets(ctx); err != nil {
            log.Printf("revoke 전 커밋 실패: %v", err)
        }
        for topic, partitions := range revoked {
            log.Printf("revoked: topic=%s partitions=%v", topic, partitions)
        }
    }),
)
```

`OnPartitionsRevoked` 콜백에서 커밋을 수행하는 이유는, 리밸런스 후 다른 Consumer가 같은 파티션을 할당받았을 때 중복 처리를 방지하기 위해서다.

## 수동 커밋 전략

franz-go의 기본 동작은 자동 커밋이다(내부적으로 `AutoCommitInterval` 5초). 수동 커밋을 위해 자동 커밋을 비활성화한다.

```go
client, err := kgo.NewClient(
    kgo.SeedBrokers("localhost:19092"),
    kgo.ConsumerGroup("manual-commit-group"),
    kgo.ConsumeTopics("order-events"),
    kgo.DisableAutoCommit(), // 수동 커밋 모드
)
```

### per-poll 커밋 (가장 일반적)

폴링 단위로 처리 후 커밋한다. 장애 시 최대 1 poll 분량의 메시지가 재처리될 수 있다.

```go
for {
    fetches := client.PollFetches(ctx)
    if ctx.Err() != nil {
        break
    }

    // 모든 레코드 처리
    fetches.EachRecord(func(r *kgo.Record) {
        processRecord(r)
    })

    // 폴링 단위로 커밋
    if err := client.CommitUncommittedOffsets(ctx); err != nil {
        log.Printf("커밋 실패: %v", err)
    }
}
```

### per-record 커밋 (최대 안전, 낮은 처리량)

레코드 단위로 커밋하므로 재처리 범위가 최소화된다. 단, 네트워크 왕복이 많아 처리량이 낮다.

```go
fetches.EachRecord(func(r *kgo.Record) {
    processRecord(r)
    // 레코드 단위 커밋 (동기)
    if err := client.CommitRecords(ctx, r); err != nil {
        log.Printf("레코드 커밋 실패: %v", err)
    }
})
```

### per-partition 배치 커밋

파티션의 마지막 레코드를 기준으로 커밋한다. 파티션별로 처리 완료를 보장하면서 커밋 횟수를 줄인다.

```go
fetches.EachPartition(func(p kgo.FetchTopicPartition) {
    for _, r := range p.Records {
        processRecord(r)
    }
    // 파티션의 마지막 레코드로 커밋
    if len(p.Records) > 0 {
        last := p.Records[len(p.Records)-1]
        if err := client.CommitRecords(ctx, last); err != nil {
            log.Printf("파티션 커밋 실패: %v", err)
        }
    }
})
```

### 커밋 전략 비교

| 전략 | 재처리 범위 | 처리량 | 사용 시점 |
|------|:---------:|:------:|----------|
| per-poll | 1 poll 분량 | 높음 | 일반적 상황 |
| per-partition | 1 파티션 poll 분량 | 중간 | 파티션별 독립 처리 |
| per-record | 최대 1개 | 낮음 | 정확히 한 번이 중요한 경우 |

## Graceful Shutdown

```go
func main() {
    client, err := kgo.NewClient(
        kgo.SeedBrokers("localhost:19092"),
        kgo.ConsumerGroup("graceful-group"),
        kgo.ConsumeTopics("order-events"),
        kgo.DisableAutoCommit(),
    )
    if err != nil {
        log.Fatal(err)
    }
    defer func() {
        // 미커밋 오프셋 최종 커밋
        commitCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
        defer cancel()
        client.CommitUncommittedOffsets(commitCtx)
        client.Close()
        log.Println("Consumer 정상 종료")
    }()

    ctx, cancel := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer cancel()

    for {
        fetches := client.PollFetches(ctx)
        if ctx.Err() != nil {
            log.Println("shutdown signal received, flushing...")
            break
        }
        fetches.EachRecord(func(r *kgo.Record) {
            processRecord(r)
        })
        client.CommitUncommittedOffsets(ctx)
    }
}
```

## Spring Boot vs Go 매핑

| Spring Boot | Go (franz-go) | 비고 |
|-------------|---------------|------|
| `@KafkaListener` | `client.PollFetches()` 루프 | 명시적 폴링 |
| `spring.kafka.consumer.group-id` | `kgo.ConsumerGroup(...)` | 그룹 설정 |
| `auto-offset-reset=earliest` | `kgo.ConsumeResetOffset(kgo.NewOffset().AtStart())` | 초기 오프셋 |
| `enable-auto-commit=false` | `kgo.DisableAutoCommit()` | 수동 커밋 |
| `Acknowledgment.acknowledge()` | `client.CommitRecords(ctx, r)` | per-record |
| `AckMode.BATCH` | `client.CommitUncommittedOffsets(ctx)` | per-poll |
| `ConsumerRebalanceListener` | `kgo.OnPartitionsAssigned/Revoked` | 리밸런스 |
| `@KafkaListener(concurrency=3)` | 3개 goroutine 각각 클라이언트 | 동시 소비 |

## 실습 TODO

```
TODO 1: PollFetches 기본 Consumer 루프 구현 (자동 커밋)
TODO 2: DisableAutoCommit + per-poll 수동 커밋 구현
TODO 3: 리밸런스 콜백에서 파티션 할당/해제 로깅
TODO 4: Graceful Shutdown 구현 (SIGINT → 커밋 → 종료)
TODO 5: 2개 Consumer 인스턴스 동시 실행 → 리밸런스 관찰
```

## 체크포인트

- [ ] Consumer Group으로 메시지 소비 확인
- [ ] 수동 커밋 후 Consumer 재시작 → 중복 없이 이어서 소비
- [ ] 리밸런스 시 파티션 재할당 로그 출력
- [ ] SIGINT로 graceful shutdown 확인 (미커밋 오프셋 커밋 후 종료)
- [ ] 2개 인스턴스: 파티션이 나뉘어 할당됨 확인
