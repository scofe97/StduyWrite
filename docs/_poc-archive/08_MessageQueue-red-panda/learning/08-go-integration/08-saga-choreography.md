# 08. SAGA Choreography

> **이론**: `02-fundamentals/08-distributed-transactions.md`, `01-event-driven/04-saga-pattern.md`
> **Spring 대응**: `03-spring-boot-integration/08-saga-choreography.md`
> **이 문서**: Go로 이벤트 기반 SAGA Choreography 구현에 집중.

## 목표

- Choreography SAGA 패턴의 Go 구현
- 보상 트랜잭션(Compensation) 처리
- 이벤트 흐름 설계 (Order → Payment → Inventory)
- 멱등성 통합 (Ch06 재활용)

## SAGA Choreography 복습

Choreography는 중앙 조정자 없이 각 서비스가 이벤트를 발행하고 구독하여 분산 트랜잭션을 완성한다. 성공 흐름과 보상 흐름을 각 서비스가 독립적으로 처리한다.

```
정상: OrderCreated → PaymentCompleted → InventoryReserved → OrderConfirmed
보상: InventoryFailed → PaymentRefunded → OrderCancelled
```

## 이벤트 정의

```go
type EventType string

const (
    OrderCreated      EventType = "OrderCreated"
    PaymentCompleted  EventType = "PaymentCompleted"
    PaymentFailed     EventType = "PaymentFailed"
    InventoryReserved EventType = "InventoryReserved"
    InventoryFailed   EventType = "InventoryFailed"
    PaymentRefunded   EventType = "PaymentRefunded"
    OrderConfirmed    EventType = "OrderConfirmed"
    OrderCancelled    EventType = "OrderCancelled"
)

type SagaEvent struct {
    CorrelationID string    `json:"correlationId"`
    EventType     EventType `json:"eventType"`
    Payload       []byte    `json:"payload"`
    Timestamp     time.Time `json:"timestamp"`
}

func newSagaRecord(topic string, event SagaEvent) *kgo.Record {
    value, _ := json.Marshal(event)
    return &kgo.Record{
        Topic: topic,
        Key:   []byte(event.CorrelationID),
        Value: value,
        Headers: []kgo.RecordHeader{
            {Key: "correlation-id", Value: []byte(event.CorrelationID)},
            {Key: "event-type", Value: []byte(string(event.EventType))},
        },
    }
}
```

## Order Service

```go
type OrderService struct {
    client *kgo.Client
    store  *IdempotencyStore
}

func (s *OrderService) CreateOrder(ctx context.Context, order Order) error {
    // DB에 주문 저장 (상태: PENDING)
    if err := s.saveOrder(order); err != nil {
        return err
    }

    // OrderCreated 이벤트 발행
    event := SagaEvent{
        CorrelationID: order.ID,
        EventType:     OrderCreated,
        Payload:       mustMarshal(order),
        Timestamp:     time.Now(),
    }
    results := s.client.ProduceSync(ctx, newSagaRecord("order-events", event))
    return results.FirstErr()
}

func (s *OrderService) Listen(ctx context.Context) {
    for {
        fetches := s.client.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }
        fetches.EachRecord(func(r *kgo.Record) {
            var event SagaEvent
            json.Unmarshal(r.Value, &event)

            acquired, _ := s.store.TryAcquire(ctx, event.CorrelationID, string(event.EventType))
            if !acquired {
                return // 중복 스킵
            }

            switch event.EventType {
            case InventoryReserved:
                s.confirmOrder(ctx, event.CorrelationID)
            case PaymentFailed, InventoryFailed:
                s.cancelOrder(ctx, event.CorrelationID)
            }
        })
        s.client.CommitUncommittedOffsets(ctx)
    }
}
```

## Payment Service

```go
type PaymentService struct {
    client *kgo.Client
    store  *IdempotencyStore
}

func (s *PaymentService) Listen(ctx context.Context) {
    for {
        fetches := s.client.PollFetches(ctx)
        if ctx.Err() != nil {
            break
        }
        fetches.EachRecord(func(r *kgo.Record) {
            var event SagaEvent
            json.Unmarshal(r.Value, &event)

            acquired, _ := s.store.TryAcquire(ctx, event.CorrelationID, string(event.EventType))
            if !acquired {
                return
            }

            switch event.EventType {
            case OrderCreated:
                s.processPayment(ctx, event)
            case InventoryFailed:
                s.refundPayment(ctx, event) // 보상 트랜잭션
            }
        })
        s.client.CommitUncommittedOffsets(ctx)
    }
}

func (s *PaymentService) processPayment(ctx context.Context, event SagaEvent) {
    // 결제 처리 (성공/실패 분기)
    if err := s.chargePayment(event.Payload); err != nil {
        s.publishEvent(ctx, "payment-events", SagaEvent{
            CorrelationID: event.CorrelationID,
            EventType:     PaymentFailed,
            Timestamp:     time.Now(),
        })
        return
    }
    s.publishEvent(ctx, "payment-events", SagaEvent{
        CorrelationID: event.CorrelationID,
        EventType:     PaymentCompleted,
        Timestamp:     time.Now(),
    })
}

func (s *PaymentService) refundPayment(ctx context.Context, event SagaEvent) {
    // 보상: 결제 취소
    s.doRefund(event.CorrelationID)
    s.publishEvent(ctx, "payment-events", SagaEvent{
        CorrelationID: event.CorrelationID,
        EventType:     PaymentRefunded,
        Timestamp:     time.Now(),
    })
}
```

## 보상 트랜잭션 에러 처리

Spring Boot 챕터에서 검증한 핵심 원칙을 Go에서도 동일하게 적용한다.

- **Forward 리스너 실패**: catch에서 실패 이벤트 발행 → 정상 return → 멱등성 레코드 커밋됨
- **Compensation 리스너 실패**: 예외(Go에서는 error return 후 커밋 생략) → 재시도 가능

```go
// Forward: 실패해도 이벤트 발행 후 정상 진행
func (s *PaymentService) processPayment(ctx context.Context, event SagaEvent) {
    if err := s.chargePayment(event.Payload); err != nil {
        // 실패 이벤트 발행 → 이 레코드는 처리 완료로 기록
        s.publishEvent(ctx, "payment-events", SagaEvent{
            CorrelationID: event.CorrelationID,
            EventType:     PaymentFailed,
        })
        return // 정상 return → 멱등성 커밋됨 → 재시도 시 스킵
    }
    // ...
}

// Compensation: 실패하면 panic/error → 재시도 필요
func (s *PaymentService) refundPayment(ctx context.Context, event SagaEvent) {
    if err := s.doRefund(event.CorrelationID); err != nil {
        // 보상 실패 → 에러 전파 → 커밋 안 됨 → 재시도 가능
        log.Printf("보상 실패 (재시도 예정): %v", err)
        panic(fmt.Sprintf("compensation failed: %v", err))
    }
    // ...
}
```

## SAGA 상태 추적

ProcessedEvent 테이블을 이중 활용하여 SAGA 진행 상태를 추적한다. 별도 상태 테이블을 추가하지 않고도 이벤트 시퀀스를 확인할 수 있다.

```go
func (s *OrderService) getSagaStatus(ctx context.Context, correlationID string) ([]string, error) {
    rows, err := s.db.QueryContext(ctx, `
        SELECT event_type, processed_at
        FROM processed_events
        WHERE correlation_id = ?
        ORDER BY processed_at
    `, correlationID)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var events []string
    for rows.Next() {
        var eventType, processedAt string
        rows.Scan(&eventType, &processedAt)
        events = append(events, fmt.Sprintf("%s @ %s", eventType, processedAt))
    }
    return events, nil
}
```

## Spring Boot vs Go 매핑

| Spring Boot | Go | 비고 |
|-------------|-----|------|
| `@KafkaListener` + `@SendTo` | `PollFetches` + `Produce` | 이벤트 체인 |
| `@Transactional` 롤백 | `panic` 또는 error return | 보상 재시도 |
| `ProcessedEvent` JPA | `processed_events` SQL | 멱등성 |
| `SagaStatusController` | HTTP 핸들러 + DB 조회 | 상태 추적 |
| MDC 분산 추적 | zerolog + correlationID | 로그 추적 |

## 실습 TODO

```
TODO 1: SagaEvent 타입 + 토픽 구조 정의
TODO 2: OrderService.CreateOrder() → OrderCreated 이벤트 발행
TODO 3: PaymentService 정상/보상 플로우 구현
TODO 4: InventoryService 정상/보상 플로우 구현
TODO 5: OrderService에서 최종 상태 (Confirmed/Cancelled) 처리
TODO 6: 멱등성 통합 (Ch06 IdempotencyStore 재활용)
TODO 7: 보상 실패 → 재시도 동작 확인
TODO 8: SAGA 상태 추적 API 구현
```

## 체크포인트

- [ ] 정상 흐름: OrderCreated → PaymentCompleted → InventoryReserved → OrderConfirmed
- [ ] 보상 흐름: PaymentFailed → OrderCancelled
- [ ] 동일 이벤트 재전송 → 중복 처리 없음
- [ ] 보상 리스너 실패 → 재시도 가능
- [ ] SAGA 상태 조회 시 이벤트 시퀀스 확인 가능
