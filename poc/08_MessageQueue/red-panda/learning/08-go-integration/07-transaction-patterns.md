# 07. Transaction Patterns

> **이론**: `02-fundamentals/09-exactly-once.md`
> **Spring 대응**: `03-spring-boot-integration/07-transaction-patterns.md`
> **이 문서**: Go franz-go 트랜잭션 API 구현에 집중.

## 목표

- Kafka 트랜잭션 개념 복습 (Consume-Transform-Produce)
- franz-go 트랜잭션 API 사용법
- DB + Kafka 원자성 패턴 (Outbox)
- GroupTransactSession 활용

## Kafka 트랜잭션 기본

Kafka 트랜잭션은 여러 토픽/파티션에 대한 produce와 consumer offset 커밋을 원자적으로 수행한다. Spring에서 `@Transactional` + `KafkaTransactionManager`가 자동으로 처리하는 것을, franz-go에서는 명시적으로 제어한다.

트랜잭션이 제공하는 보장은 두 가지다. 첫째, 트랜잭션 내 모든 produce가 커밋되거나 전부 롤백된다(원자성). 둘째, `isolation.level=read_committed`로 설정한 Consumer는 커밋된 메시지만 읽는다(격리성).

### 트랜잭셔널 Producer

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/twmb/franz-go/pkg/kgo"
)

func main() {
    client, err := kgo.NewClient(
        kgo.SeedBrokers("localhost:19092"),
        // TransactionalID: 동일 ID로 재시작 시 이전 미완료 트랜잭션을 fence한다
        kgo.TransactionalID("my-txn-producer-001"),
        kgo.RequiredAcks(kgo.AllISRAcks()), // 트랜잭션에 필수
    )
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    ctx := context.Background()

    // 트랜잭션 시작
    if err := client.BeginTransaction(); err != nil {
        log.Fatal(err)
    }

    // 여러 토픽에 원자적으로 produce
    client.Produce(ctx, &kgo.Record{
        Topic: "order-events",
        Key:   []byte("order-123"),
        Value: []byte(`{"status":"created"}`),
    }, nil)
    client.Produce(ctx, &kgo.Record{
        Topic: "inventory-events",
        Key:   []byte("order-123"),
        Value: []byte(`{"action":"reserve"}`),
    }, nil)

    // 버퍼 플러시 (모든 레코드를 브로커로 전송)
    if err := client.Flush(ctx); err != nil {
        client.AbortBufferedRecords(ctx)
        if abortErr := client.EndTransaction(ctx, kgo.TryAbort); abortErr != nil {
            log.Printf("abort 실패: %v", abortErr)
        }
        log.Fatalf("flush 실패: %v", err)
    }

    // 트랜잭션 커밋
    if err := client.EndTransaction(ctx, kgo.TryCommit); err != nil {
        log.Fatalf("커밋 실패: %v", err)
    }
    fmt.Println("트랜잭션 커밋 완료")
}
```

### 트랜잭션 중단 (Abort)

```go
// 처리 중 에러 발생 시 abort
if err := processStep(); err != nil {
    client.AbortBufferedRecords(ctx) // 버퍼에 남은 레코드 제거
    if abortErr := client.EndTransaction(ctx, kgo.TryAbort); abortErr != nil {
        log.Printf("abort 실패 (브로커 재연결 필요): %v", abortErr)
    }
    return err
}
```

## Consume-Transform-Produce (CTP)

CTP는 가장 일반적인 트랜잭션 패턴이다. 메시지를 소비하고, 변환한 후, 다른 토픽에 produce하면서 consumer offset까지 원자적으로 커밋한다. Spring의 `@Transactional` + `KafkaTransactionManager` + `@SendTo` 조합이 이 패턴에 해당한다.

### GroupTransactSession

franz-go는 `GroupTransactSession`으로 CTP 패턴을 단순화한다. 내부적으로 트랜잭션 시작, offset 커밋, 트랜잭션 커밋을 조율한다.

```go
package main

import (
    "context"
    "log"
    "os/signal"
    "syscall"

    "github.com/twmb/franz-go/pkg/kgo"
)

func runCTP() error {
    client, err := kgo.NewClient(
        kgo.SeedBrokers("localhost:19092"),
        kgo.TransactionalID("ctp-processor-001"),
        kgo.ConsumerGroup("ctp-group"),
        kgo.ConsumeTopics("input-topic"),
        kgo.DisableAutoCommit(),
        kgo.RequiredAcks(kgo.AllISRAcks()),
        // read_committed: 커밋된 메시지만 소비 (트랜잭션 격리)
        kgo.FetchIsolationLevel(kgo.ReadCommitted()),
    )
    if err != nil {
        return err
    }
    defer client.Close()

    // GroupTransactSession이 CTP 흐름을 관리한다
    sess, err := kgo.NewGroupTransactSession(client)
    if err != nil {
        return err
    }

    ctx, cancel := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer cancel()

    for {
        // 트랜잭션 시작 + 폴링
        fetches := sess.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }

        fetches.EachError(func(t string, p int32, err error) {
            log.Printf("fetch error: %s[%d] %v", t, p, err)
        })

        // 변환 후 output 토픽으로 produce
        fetches.EachRecord(func(r *kgo.Record) {
            transformed := transform(r.Value)
            client.Produce(ctx, &kgo.Record{
                Topic: "output-topic",
                Key:   r.Key,
                Value: transformed,
            }, nil)
        })

        // 트랜잭션 커밋: produce + consumer offset 원자적 커밋
        committed, err := sess.End(ctx, kgo.TryCommit)
        if err != nil {
            log.Printf("트랜잭션 실패 (committed=%v): %v", committed, err)
        }
    }
    return nil
}

func transform(input []byte) []byte {
    // 실제 변환 로직
    return append([]byte("transformed:"), input...)
}
```

`sess.End(ctx, kgo.TryCommit)`은 내부적으로 다음을 수행한다.
1. `client.Flush(ctx)` — 버퍼 전송
2. `client.EndTransaction(ctx, kgo.TryCommit)` — 트랜잭션 커밋 (produce + offset 원자적)

## DB + Kafka 원자성: Outbox 패턴

외부 DB 작업과 Kafka produce를 진정한 의미에서 원자적으로 수행하는 것은 분산 트랜잭션 문제다. Kafka 트랜잭션만으로는 DB 변경과의 원자성을 보장할 수 없다. Outbox 패턴으로 이를 근사한다.

### 핵심 아이디어

비즈니스 로직과 Kafka 이벤트 발행을 같은 DB 트랜잭션으로 묶는다. Kafka에 직접 produce하는 대신, 같은 DB의 outbox 테이블에 이벤트를 저장한다. 별도 poller가 outbox를 읽어 Kafka로 발행한다.

```go
package outbox

import (
    "context"
    "database/sql"
    "encoding/json"
    "fmt"
    "time"

    "github.com/twmb/franz-go/pkg/kgo"
)

// DB 스키마
const createOutboxTable = `
CREATE TABLE IF NOT EXISTS outbox (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    aggregate_id TEXT    NOT NULL,
    event_type   TEXT    NOT NULL,
    topic        TEXT    NOT NULL,
    payload      BLOB    NOT NULL,
    published    BOOLEAN NOT NULL DEFAULT false,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);
`

// SaveEvent는 비즈니스 트랜잭션 내에서 outbox에 이벤트를 저장한다.
func SaveEvent(ctx context.Context, tx *sql.Tx, aggregateID, eventType, topic string, payload any) error {
    data, err := json.Marshal(payload)
    if err != nil {
        return fmt.Errorf("payload 직렬화 실패: %w", err)
    }
    _, err = tx.ExecContext(ctx, `
        INSERT INTO outbox (aggregate_id, event_type, topic, payload)
        VALUES (?, ?, ?, ?)
    `, aggregateID, eventType, topic, data)
    return err
}

// Poller는 outbox 테이블을 주기적으로 폴링하여 미발행 이벤트를 Kafka로 전송한다.
type Poller struct {
    db       *sql.DB
    client   *kgo.Client
    interval time.Duration
}

func NewPoller(db *sql.DB, client *kgo.Client, interval time.Duration) *Poller {
    return &Poller{db: db, client: client, interval: interval}
}

func (p *Poller) Run(ctx context.Context) {
    ticker := time.NewTicker(p.interval)
    defer ticker.Stop()
    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            if err := p.publish(ctx); err != nil {
                fmt.Printf("outbox poll 실패: %v\n", err)
            }
        }
    }
}

func (p *Poller) publish(ctx context.Context) error {
    rows, err := p.db.QueryContext(ctx, `
        SELECT id, aggregate_id, event_type, topic, payload
        FROM outbox
        WHERE published = false
        ORDER BY id
        LIMIT 100
    `)
    if err != nil {
        return err
    }
    defer rows.Close()

    var records []*kgo.Record
    var ids []int64

    for rows.Next() {
        var id int64
        var aggID, eventType, topic string
        var payload []byte
        if err := rows.Scan(&id, &aggID, &eventType, &topic, &payload); err != nil {
            return err
        }
        records = append(records, &kgo.Record{
            Topic: topic,
            Key:   []byte(aggID),
            Value: payload,
            Headers: []kgo.RecordHeader{
                {Key: "event-type", Value: []byte(eventType)},
            },
        })
        ids = append(ids, id)
    }
    if len(records) == 0 {
        return nil
    }

    // Kafka로 전송
    results := p.client.ProduceSync(ctx, records...)
    if err := results.FirstErr(); err != nil {
        return fmt.Errorf("kafka publish 실패: %w", err)
    }

    // 발행 완료 표시
    for _, id := range ids {
        p.db.ExecContext(ctx, `UPDATE outbox SET published = true WHERE id = ?`, id)
    }
    fmt.Printf("outbox: %d 이벤트 발행 완료\n", len(records))
    return nil
}
```

### 서비스 레이어 통합

```go
func createOrder(ctx context.Context, db *sql.DB, req OrderRequest) error {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    // 1. 비즈니스 로직: 주문 저장
    orderID, err := saveOrderTx(ctx, tx, req)
    if err != nil {
        return err
    }

    // 2. Outbox에 이벤트 저장 (같은 DB 트랜잭션)
    event := map[string]any{
        "order_id":   orderID,
        "user_id":    req.UserID,
        "total":      req.Total,
        "created_at": time.Now().UTC(),
    }
    if err := outbox.SaveEvent(ctx, tx, orderID, "OrderCreated", "order-events", event); err != nil {
        return err
    }

    // 3. DB 커밋 (비즈니스 로직 + outbox 이벤트 원자적)
    return tx.Commit()
    // Poller가 비동기로 Kafka publish 처리
}
```

## Spring Boot vs Go 매핑

| Spring Boot | Go (franz-go) | 비고 |
|-------------|---------------|------|
| `@Transactional` + KTM | `client.BeginTransaction()` / `EndTransaction()` | 트랜잭션 경계 |
| 자동 커밋/롤백 | `TryCommit` / `TryAbort` 명시적 | 직접 제어 |
| `KafkaTransactionManager` + `@SendTo` | `GroupTransactSession` | CTP 패턴 |
| `ChainedKafkaTransactionManager` | Outbox 패턴 직접 구현 | DB+Kafka |
| `spring.kafka.producer.transaction-id-prefix` | `kgo.TransactionalID(...)` | 트랜잭션 ID |
| `isolation.level=read_committed` | `kgo.FetchIsolationLevel(kgo.ReadCommitted())` | 격리 수준 |
| Spring `@Transactional` rollback | `tx.Rollback()` defer | DB 롤백 |

## 실습 TODO

```
TODO 1: 트랜잭셔널 Producer로 2개 토픽에 원자적 produce
TODO 2: isolation.level=read_committed Consumer로 abort 메시지 미노출 확인
TODO 3: GroupTransactSession으로 CTP 구현 (input → transform → output)
TODO 4: Outbox 패턴 구현 (DB 저장 + outbox 삽입 + Poller 발행)
TODO 5: DB 저장 성공 + Poller 재시작 후 미발행 이벤트 재발행 확인
```

## 체크포인트

- [ ] 트랜잭션 커밋 → 두 토픽 모두에 메시지 노출
- [ ] 트랜잭션 abort → 어떤 토픽에도 메시지 미노출 (read_committed Consumer 기준)
- [ ] CTP: input 소비 → output produce + offset 커밋이 원자적으로 수행
- [ ] Outbox: DB 커밋 후 Poller가 Kafka publish, published=true 업데이트
- [ ] Outbox Poller 재시작 후 published=false 이벤트 재발행 확인
