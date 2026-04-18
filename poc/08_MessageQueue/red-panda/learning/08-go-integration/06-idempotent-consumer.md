# 06. Idempotent Consumer

> **이론**: `02-fundamentals/09-exactly-once.md`, `01-event-driven/17-idempotency-patterns.md`
> **Spring 대응**: `03-spring-boot-integration/06-idempotent-consumer.md`
> **이 문서**: Go에서 Preemptive Acquire 패턴 구현에 집중.

## 목표

- 멱등성 Consumer의 필요성 이해
- Preemptive Acquire 패턴 Go 구현
- DB 기반 중복 제거 (SQLite)
- at-least-once + 멱등성 = effectively-once

## 왜 멱등성이 필요한가

Kafka의 at-least-once 전달 보장은 Consumer 장애 시 동일 메시지를 재전달할 수 있다. 네트워크 장애, Consumer 크래시, 리밸런스 모두 중복 전달의 원인이 된다. 따라서 Consumer는 동일 메시지를 여러 번 받아도 결과가 동일하도록 설계해야 한다. 이것이 멱등성이다.

## Check-Then-Act의 문제

직관적으로는 "처리 여부를 먼저 확인하고, 미처리면 실행" 방식을 생각하기 쉽다. 하지만 이 check-then-act 패턴은 동시성 문제가 있다.

```go
// 나쁜 패턴: check-then-act
if !store.IsDuplicate(correlationID, eventType) {  // 체크
    processEvent(r)                                  // 처리
    store.MarkProcessed(correlationID, eventType)   // 기록
}
// 체크와 기록 사이에 다른 Consumer가 같은 메시지를 처리할 수 있다
```

## Preemptive Acquire 패턴

먼저 처리 권한을 선점(`tryAcquire`)하고, 성공한 경우에만 비즈니스 로직을 실행한다. 선점 자체가 원자적이므로 동시성 문제가 없다. 이 패턴은 Spring Boot 챕터에서 `INSERT...WHERE NOT EXISTS` 네이티브 쿼리로 구현한 것과 동일한 원리다.

### DB 스키마

```sql
CREATE TABLE IF NOT EXISTS processed_events (
    correlation_id TEXT NOT NULL,
    event_type     TEXT NOT NULL,
    processed_at   TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (correlation_id, event_type)
);
```

복합 기본 키 `(correlation_id, event_type)`을 사용하는 이유는 SAGA 단계를 구분하기 위해서다. 하나의 주문(`order-123`)이 여러 이벤트(`OrderCreated`, `PaymentCompleted`, `InventoryReserved`)를 생성하므로, `correlationId`만으로는 단계를 구분할 수 없다.

### Go 구현

```go
package idempotency

import (
    "context"
    "database/sql"
    "fmt"

    _ "modernc.org/sqlite" // CGO-free SQLite driver
)

type Store struct {
    db *sql.DB
}

func NewStore(dbPath string) (*Store, error) {
    db, err := sql.Open("sqlite", dbPath)
    if err != nil {
        return nil, fmt.Errorf("DB 오픈 실패: %w", err)
    }

    if _, err := db.Exec(`
        CREATE TABLE IF NOT EXISTS processed_events (
            correlation_id TEXT NOT NULL,
            event_type     TEXT NOT NULL,
            processed_at   TEXT NOT NULL DEFAULT (datetime('now')),
            PRIMARY KEY (correlation_id, event_type)
        )
    `); err != nil {
        return nil, fmt.Errorf("스키마 생성 실패: %w", err)
    }

    return &Store{db: db}, nil
}

func (s *Store) Close() error { return s.db.Close() }

// TryAcquire attempts an atomic insert.
// Returns true if acquired (first time), false if duplicate.
func (s *Store) TryAcquire(ctx context.Context, correlationID, eventType string) (bool, error) {
    result, err := s.db.ExecContext(ctx, `
        INSERT INTO processed_events (correlation_id, event_type)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM processed_events
            WHERE correlation_id = ? AND event_type = ?
        )
    `, correlationID, eventType, correlationID, eventType)
    if err != nil {
        return false, fmt.Errorf("TryAcquire 실패: %w", err)
    }

    rows, err := result.RowsAffected()
    if err != nil {
        return false, err
    }
    // rows=1 이면 선점 성공 (처음 처리), rows=0 이면 중복
    return rows > 0, nil
}

// IsProcessed checks without acquiring. Use only for read-only queries.
func (s *Store) IsProcessed(ctx context.Context, correlationID, eventType string) (bool, error) {
    var count int
    err := s.db.QueryRowContext(ctx, `
        SELECT COUNT(1) FROM processed_events
        WHERE correlation_id = ? AND event_type = ?
    `, correlationID, eventType).Scan(&count)
    return count > 0, err
}
```

### Consumer 통합

```go
package main

import (
    "context"
    "log"
    "os/signal"
    "syscall"

    "github.com/twmb/franz-go/pkg/kgo"
)

func consumeIdempotent(client *kgo.Client, store *idempotency.Store) {
    ctx, cancel := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer cancel()

    for {
        fetches := client.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }

        fetches.EachRecord(func(r *kgo.Record) {
            correlationID := getHeader(r, "correlation-id")
            eventType := getHeader(r, "event-type")

            if correlationID == "" || eventType == "" {
                log.Printf("헤더 누락 — 처리 스킵: key=%s", string(r.Key))
                return
            }

            // Preemptive Acquire: 선점 먼저
            acquired, err := store.TryAcquire(ctx, correlationID, eventType)
            if err != nil {
                log.Printf("멱등성 체크 실패 (재시도 예정): %v", err)
                return // 커밋하지 않으면 재처리됨
            }
            if !acquired {
                log.Printf("중복 스킵: correlationId=%s eventType=%s", correlationID, eventType)
                return // 이미 처리됨 — 정상적으로 skip
            }

            // 비즈니스 로직 실행
            if err := processEvent(ctx, r); err != nil {
                // 처리 실패해도 processed_events는 롤백하지 않는다.
                // 이유: DB 트랜잭션과 Kafka 커밋이 분리되어 있어,
                //       processed_events를 삭제하면 재처리 시 다시 시도하지만
                //       그 사이 부분 효과(side effect)가 이미 발생했을 수 있다.
                log.Printf("처리 실패 (DLQ 고려): %v", err)
            }
        })

        if err := client.CommitUncommittedOffsets(ctx); err != nil {
            log.Printf("커밋 실패: %v", err)
        }
    }
}
```

## 트랜잭션 연동 (DB 작업과 함께)

비즈니스 로직이 DB를 수정하는 경우, processed_events 삽입과 비즈니스 DB 변경을 같은 트랜잭션으로 묶을 수 있다.

```go
func processWithTx(ctx context.Context, db *sql.DB, r *kgo.Record) error {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    correlationID := getHeader(r, "correlation-id")
    eventType := getHeader(r, "event-type")

    // 1. Preemptive Acquire (트랜잭션 내)
    result, err := tx.ExecContext(ctx, `
        INSERT INTO processed_events (correlation_id, event_type)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM processed_events
            WHERE correlation_id = ? AND event_type = ?
        )
    `, correlationID, eventType, correlationID, eventType)
    if err != nil {
        return fmt.Errorf("acquire 실패: %w", err)
    }
    rows, _ := result.RowsAffected()
    if rows == 0 {
        return nil // 중복, 트랜잭션 롤백 (processed_events 변경 없음)
    }

    // 2. 비즈니스 로직 (같은 트랜잭션)
    if err := saveOrder(ctx, tx, r.Value); err != nil {
        return err // 롤백 → processed_events도 롤백 → 재시도 가능
    }

    return tx.Commit()
}
```

이 방식은 processed_events 삽입과 비즈니스 로직이 원자적으로 처리된다. 비즈니스 로직 실패 시 processed_events도 함께 롤백되므로 재처리가 가능하다.

## Spring Boot vs Go 매핑

| Spring Boot | Go | 비고 |
|-------------|-----|------|
| `ProcessedEvent` JPA Entity | `processed_events` 테이블 + `database/sql` | DB 접근 |
| `@Transactional` + JPA saveAndFlush | `INSERT...WHERE NOT EXISTS` | 원자적 삽입 |
| `DataIntegrityViolationException` catch | `RowsAffected() == 0` 체크 | 중복 감지 |
| Spring Data Repository | `*sql.DB` 직접 사용 | ORM 없음 |
| `(correlationId, eventType)` 복합 키 | PRIMARY KEY (correlation_id, event_type) | 동일 |
| `@Transactional` rollback | `tx.Rollback()` defer | 트랜잭션 관리 |

## 실습 TODO

```
TODO 1: modernc.org/sqlite 드라이버 추가 후 IdempotencyStore 구현
TODO 2: TryAcquire() 단위 테스트 (동시 goroutine 10개로 중복 삽입 시도)
TODO 3: Consumer에 멱등성 통합 → 같은 메시지 2번 전송 → 1번만 처리 확인
TODO 4: 복합 키 (correlationId + eventType) 동작 확인
TODO 5: (선택) 비즈니스 DB 작업과 트랜잭션 연동
```

## 체크포인트

- [ ] 동일 메시지 재전송 시 "중복 스킵" 로그 출력
- [ ] DB에 동일 (correlationId, eventType) 레코드 1개만 존재
- [ ] 다른 eventType은 별도로 처리됨 확인
- [ ] 동시 goroutine 10개가 같은 키로 TryAcquire → 정확히 1개만 true 반환
