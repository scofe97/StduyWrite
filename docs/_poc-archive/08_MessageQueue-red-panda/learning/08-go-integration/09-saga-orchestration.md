# 09. SAGA Orchestration

> **이론**: `01-event-driven/04-saga-pattern.md`
> **Spring 대응**: `03-spring-boot-integration/09-saga-orchestration.md`
> **이 문서**: Go에서 중앙 조정자 기반 SAGA Orchestration 구현에 집중.

## 목표

- Orchestrator 패턴의 Go 구현
- 상태 머신 기반 SAGA 관리
- Choreography vs Orchestration 트레이드오프

## Orchestrator vs Choreography

Choreography(Ch08)는 각 서비스가 이벤트를 직접 주고받는다. 흐름이 단순할 때 적합하지만, 서비스 수가 늘면 이벤트 체인 추적이 어려워진다. Orchestrator는 중앙 조정자가 전체 흐름을 관리하여 가시성이 높다. 복잡도는 서비스 수에 비례하지 않고 선형으로만 증가한다.

## 상태 머신

```go
type SagaState int

const (
    StateCreated SagaState = iota
    StatePaymentPending
    StatePaymentCompleted
    StateInventoryPending
    StateInventoryReserved
    StateConfirmed
    // 보상 상태
    StatePaymentRefunding
    StatePaymentRefunded
    StateCancelled
    StateFailed
)

type SagaInstance struct {
    ID            string
    CorrelationID string
    CurrentState  SagaState
    CreatedAt     time.Time
    UpdatedAt     time.Time
    FailReason    string
}
```

### 상태 전이 테이블

상태 전이를 switch-case 대신 테이블로 관리하면 새로운 상태/이벤트 추가 시 기존 코드를 수정하지 않고 확장할 수 있다.

```go
type Transition struct {
    From   SagaState
    Event  EventType
    To     SagaState
    Action func(ctx context.Context, saga *SagaInstance) error
}

var transitions = []Transition{
    {StateCreated, OrderCreated, StatePaymentPending, requestPayment},
    {StatePaymentPending, PaymentCompleted, StateInventoryPending, requestInventory},
    {StatePaymentPending, PaymentFailed, StateCancelled, cancelOrder},
    {StateInventoryPending, InventoryReserved, StateConfirmed, confirmOrder},
    {StateInventoryPending, InventoryFailed, StatePaymentRefunding, requestRefund},
    {StatePaymentRefunding, PaymentRefunded, StateCancelled, cancelOrder},
}

func (o *Orchestrator) processEvent(ctx context.Context, saga *SagaInstance, event SagaEvent) error {
    for _, t := range transitions {
        if t.From == saga.CurrentState && t.Event == event.EventType {
            saga.CurrentState = t.To
            saga.UpdatedAt = time.Now()
            if err := o.saveSaga(ctx, saga); err != nil {
                return err
            }
            return t.Action(ctx, saga)
        }
    }
    return fmt.Errorf("invalid transition: state=%d event=%s", saga.CurrentState, event.EventType)
}
```

## Orchestrator 구현

```go
type Orchestrator struct {
    client *kgo.Client
    db     *sql.DB
    store  *IdempotencyStore
}

func (o *Orchestrator) StartSaga(ctx context.Context, order Order) error {
    saga := &SagaInstance{
        ID:            uuid.New().String(),
        CorrelationID: order.ID,
        CurrentState:  StateCreated,
        CreatedAt:     time.Now(),
        UpdatedAt:     time.Now(),
    }
    if err := o.saveSaga(ctx, saga); err != nil {
        return err
    }

    // 첫 번째 커맨드 발행
    return o.publishCommand(ctx, "payment-commands", Command{
        Type:          "ProcessPayment",
        CorrelationID: order.ID,
        Payload:       mustMarshal(order),
    })
}

func (o *Orchestrator) Listen(ctx context.Context) {
    for {
        fetches := o.client.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }

        fetches.EachRecord(func(r *kgo.Record) {
            var event SagaEvent
            json.Unmarshal(r.Value, &event)

            acquired, _ := o.store.TryAcquire(ctx, event.CorrelationID, string(event.EventType))
            if !acquired {
                return
            }

            saga, err := o.loadSaga(ctx, event.CorrelationID)
            if err != nil {
                log.Printf("SAGA 로드 실패: %v", err)
                return
            }

            if err := o.processEvent(ctx, saga, event); err != nil {
                log.Printf("상태 전이 실패: %v", err)
            }
        })
        o.client.CommitUncommittedOffsets(ctx)
    }
}
```

### Command 패턴

Orchestrator는 이벤트(무슨 일이 일어났다) 대신 커맨드(무엇을 하라)를 발행한다. 이 구분이 Choreography와 Orchestration의 핵심 차이다.

```go
type Command struct {
    Type          string `json:"type"`
    CorrelationID string `json:"correlationId"`
    Payload       []byte `json:"payload"`
}

func (o *Orchestrator) publishCommand(ctx context.Context, topic string, cmd Command) error {
    value, _ := json.Marshal(cmd)
    results := o.client.ProduceSync(ctx, &kgo.Record{
        Topic: topic,
        Key:   []byte(cmd.CorrelationID),
        Value: value,
        Headers: []kgo.RecordHeader{
            {Key: "command-type", Value: []byte(cmd.Type)},
            {Key: "correlation-id", Value: []byte(cmd.CorrelationID)},
        },
    })
    return results.FirstErr()
}
```

## SAGA 영속화

SQLite의 `ON CONFLICT DO UPDATE`(upsert)를 사용하여 INSERT와 UPDATE를 하나의 쿼리로 처리한다. Spring의 `saveAndFlush()`와 동일한 역할이다.

```go
func (o *Orchestrator) saveSaga(ctx context.Context, saga *SagaInstance) error {
    _, err := o.db.ExecContext(ctx, `
        INSERT INTO saga_instances (id, correlation_id, current_state, created_at, updated_at, fail_reason)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            current_state = excluded.current_state,
            updated_at = excluded.updated_at,
            fail_reason = excluded.fail_reason
    `, saga.ID, saga.CorrelationID, saga.CurrentState, saga.CreatedAt, saga.UpdatedAt, saga.FailReason)
    return err
}

func (o *Orchestrator) loadSaga(ctx context.Context, correlationID string) (*SagaInstance, error) {
    row := o.db.QueryRowContext(ctx, `
        SELECT id, correlation_id, current_state, created_at, updated_at, fail_reason
        FROM saga_instances WHERE correlation_id = ?
    `, correlationID)

    saga := &SagaInstance{}
    err := row.Scan(&saga.ID, &saga.CorrelationID, &saga.CurrentState,
        &saga.CreatedAt, &saga.UpdatedAt, &saga.FailReason)
    return saga, err
}
```

## Choreography vs Orchestration

| 기준 | Choreography (Ch08) | Orchestration (Ch09) |
|------|:-------------------:|:-------------------:|
| 결합도 | 낮음 (이벤트만) | 중간 (조정자 의존) |
| 가시성 | 낮음 (추적 어려움) | 높음 (상태 머신) |
| 복잡도 | 서비스 수 증가 시 급증 | 선형 증가 |
| 단일 장애점 | 없음 | Orchestrator |
| 적합 | 3개 이하 서비스 | 4개 이상 서비스 |

## Spring Boot vs Go 매핑

| Spring Boot | Go | 비고 |
|-------------|-----|------|
| SagaOrchestrator Bean | `Orchestrator` 구조체 | 중앙 조정자 |
| JPA SagaInstance | SQLite saga_instances | 상태 영속화 |
| `@KafkaListener` 응답 수신 | `PollFetches` 루프 | 이벤트 수신 |
| `KafkaTemplate` 커맨드 발행 | `ProduceSync` | 커맨드 전송 |
| 상태 전이 switch-case | 전이 테이블 배열 | 상태 머신 |

## 실습 TODO

```
TODO 1: SagaState 상태 머신 + 전이 테이블 정의
TODO 2: Orchestrator.StartSaga() 구현
TODO 3: 상태 전이 처리 (processEvent)
TODO 4: Payment/Inventory 서비스의 커맨드 핸들러 구현
TODO 5: 정상/보상 흐름 E2E 테스트
TODO 6: SAGA 인스턴스 조회 API
```

## 체크포인트

- [ ] 정상: Created → PaymentPending → InventoryPending → Confirmed
- [ ] 보상: PaymentPending → PaymentFailed → Cancelled
- [ ] DB에 SAGA 상태 변경 이력 저장됨
- [ ] 동일 이벤트 재전송 → 상태 변경 없음 (멱등성)
- [ ] 잘못된 상태 전이 시 에러 로그 출력
