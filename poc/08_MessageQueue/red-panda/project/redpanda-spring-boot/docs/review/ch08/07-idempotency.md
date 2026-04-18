# #7 멱등성 보장

같은 이벤트가 여러 번 도착해도 비즈니스 로직은 **딱 한 번만** 실행된다.

---

## 구현 요약

| 항목 | 내용 |
|------|------|
| 신규 파일 | `ProcessedEvent` (엔티티), `ProcessedEventRepository`, `EventIdempotencyChecker` |
| 변경 파일 | `InventoryService`, `PaymentService`, `ShippingService`, `OrderService` (4개) |
| 핵심 전략 | **선점 방식(preemptive acquire)** — 비즈니스 로직 전에 처리 권한을 확보 |
| 동시성 안전 | `INSERT ... WHERE NOT EXISTS` 네이티브 쿼리 (트랜잭션 오염 없음) |
| 빌드 결과 | compileJava + compileTestJava 성공 |

---

## 1. 왜 멱등성이 필요한가

Kafka는 **at-least-once** 전달을 보장한다. "최소 한 번"은 곧 "여러 번 올 수 있다"는 뜻이다.

### 중복 발생 시나리오

```
sequenceDiagram
    Consumer ->> Broker: poll() → 메시지 수신
    Consumer ->> DB: 비즈니스 로직 실행
    Note over Consumer: 여기서 크래시 발생!
    Consumer --x Broker: ack 전송 실패
    Note over Broker: 오프셋 미커밋 → 같은 메시지 재전달
    Consumer ->> Broker: poll() → 동일 메시지 다시 수신
```

| 원인 | 설명 |
|------|------|
| Consumer 크래시 | 오프셋 커밋 전 장애 → 같은 메시지 재전달 |
| 리밸런싱 | Consumer Group 변경 시 파티션 재할당 → 오프셋 중복 구간 |
| Producer 재전송 | ACK 미수신 → 같은 메시지를 브로커에 중복 전송 |
| 보상 재시도 | DefaultErrorHandler가 실패한 보상을 재시도 |

멱등성 없이 재처리하면 **재고 이중 차감**, **결제 이중 발생**, **환불 이중 실행** 같은 데이터 불일치가 발생한다.

---

## 2. 전체 진행 흐름

### 한눈에 보는 멱등성 흐름

```
sequenceDiagram
    participant Kafka
    participant Listener
    participant IdempotencyChecker
    participant DB
    participant BusinessLogic

    Kafka ->> Listener: 이벤트 수신
    Listener ->> IdempotencyChecker: tryAcquire(correlationId, eventType)
    IdempotencyChecker ->> DB: SELECT EXISTS (빠른 중복 조회)

    alt 이미 처리됨
        DB -->> IdempotencyChecker: true
        IdempotencyChecker -->> Listener: false (스킵)
        Listener ->> Kafka: ack
        Note over Listener: 비즈니스 로직 실행 안 함
    else 미처리
        DB -->> IdempotencyChecker: false
        IdempotencyChecker ->> DB: INSERT ... WHERE NOT EXISTS (선점)
        DB -->> IdempotencyChecker: 1 (삽입 성공)
        IdempotencyChecker -->> Listener: true (진행)
        Listener ->> BusinessLogic: 비즈니스 로직 실행
        alt 성공
            BusinessLogic -->> Listener: OK
            Listener ->> Kafka: send(다음 이벤트)
            Listener ->> Kafka: ack
            Note over DB: TX 커밋 - ProcessedEvent 확정
        else 실패 (보상 리스너)
            BusinessLogic -->> Listener: throw
            Note over DB: TX 롤백 - ProcessedEvent도 롤백
            Note over Listener: 재시도 시 tryAcquire 다시 성공
        end
    end
```

### 핵심 포인트

1. `tryAcquire()`는 비즈니스 로직 **전에** 호출한다 (선점)
2. 같은 JPA `@Transactional`에 참여하므로 비즈니스 로직 실패 시 **함께 롤백**
3. 롤백되면 ProcessedEvent도 사라지므로 **재시도 시 다시 처리 가능**

---

## 3. 구현 상세

### 3-1. ProcessedEvent 엔티티 — "누가 뭘 처리했는지" 기록

```java
@Entity
@Table(name = "ch03_processed_events",
       uniqueConstraints = @UniqueConstraint(
               name = "uk_correlation_event_type",
               columnNames = {"correlationId", "eventType"}))
public class ProcessedEvent {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    private String correlationId;  // 어떤 SAGA인지 (주문 단위)
    private String eventType;     // 어떤 단계인지 (서비스 단위)
    private Instant processedAt;  // 언제 처리했는지
}
```

**왜 두 개의 키가 필요한가?**

하나의 SAGA(correlationId=`abc-123`)는 여러 단계를 거친다:

```
abc-123 + InventoryReserve   → 재고 예약 완료
abc-123 + PaymentProcess     → 결제 완료
abc-123 + ShippingProcess    → 배송 요청 완료
abc-123 + OrderComplete      → 주문 완료
```

correlationId만으로는 "재고 예약은 했는데 결제는 아직"을 구분할 수 없다. eventType을 추가하면 **SAGA 내 각 단계를 독립적으로** 중복 체크할 수 있다.

### 3-2. EventIdempotencyChecker — 선점 방식 멱등성 체커

```java
public boolean tryAcquire(String correlationId, String eventType) {
    // 1차: 빠른 SELECT (대부분의 중복을 여기서 차단 → DB 부하 최소화)
    if (processedEventRepository.existsByCorrelationIdAndEventType(correlationId, eventType)) {
        return false;
    }

    // 2차: INSERT ... WHERE NOT EXISTS (동시성 안전, 트랜잭션 오염 없음)
    int inserted = processedEventRepository.insertIfAbsent(
            UUID.randomUUID().toString(), correlationId, eventType, Instant.now());

    return inserted > 0;  // 1=선점 성공, 0=다른 스레드가 먼저 선점
}
```

**왜 2단계인가?**

| 단계 | 역할 | 이유 |
|------|------|------|
| 1차 SELECT | 빠른 필터 | 99%의 중복은 여기서 걸림. INSERT보다 가볍다 |
| 2차 INSERT | 동시성 안전망 | 두 스레드가 동시에 1차를 통과해도 하나만 성공 |

**왜 `INSERT ... WHERE NOT EXISTS`인가?**

이전 구현에서는 `saveAndFlush()` + `DataIntegrityViolationException` catch 방식을 사용했다. 이 방식의 문제:

```
[문제] saveAndFlush() 예외 → Hibernate가 트랜잭션을 rollback-only로 마킹
      → catch에서 삼켜도 @Transactional 커밋 시 UnexpectedRollbackException
      → 이미 실행된 비즈니스 로직까지 전부 롤백
```

`INSERT ... WHERE NOT EXISTS`는 **레코드가 이미 있으면 0을 반환**하고 예외를 던지지 않는다. 트랜잭션이 오염되지 않으므로 호출자의 `@Transactional`이 정상 동작한다.

### 3-3. Repository 네이티브 쿼리

```java
@Modifying
@Query(nativeQuery = true, value =
    "INSERT INTO ch03_processed_events (id, correlation_id, event_type, processed_at) " +
    "SELECT :id, :correlationId, :eventType, :processedAt " +
    "WHERE NOT EXISTS (" +
    "  SELECT 1 FROM ch03_processed_events " +
    "  WHERE correlation_id = :correlationId AND event_type = :eventType)")
int insertIfAbsent(...);
```

표준 SQL로 H2, PostgreSQL 모두 호환된다. 유니크 인덱스가 `WHERE NOT EXISTS` 서브쿼리를 최적화한다.

---

## 4. eventType 전체 맵

10개 리스너에 10개 고유 eventType — 중복이나 충돌 없음.

### 정방향 (forward-flow)

| 서비스 | 리스너 | eventType | 의미 |
|--------|--------|-----------|------|
| InventoryService | onOrderCreated | `InventoryReserve` | 재고 예약 |
| PaymentService | onInventoryReserved | `PaymentProcess` | 결제 처리 |
| ShippingService | onPaymentCompleted | `ShippingProcess` | 배송 요청 |
| OrderService | onShippingRequested | `OrderComplete` | 주문 완료 |

### 실패 (failure)

| 서비스 | 리스너 | eventType | 의미 |
|--------|--------|-----------|------|
| OrderService | onInventoryReservationFailed | `OrderFail-Inventory` | 재고 부족으로 주문 실패 |
| OrderService | onPaymentFailed | `OrderFail-Payment` | 결제 실패로 주문 실패 |
| OrderService | onShippingFailed | `OrderFail-Shipping` | 배송 실패로 주문 실패 |

### 보상 (compensation)

| 서비스 | 리스너 | eventType | 의미 |
|--------|--------|-----------|------|
| InventoryService | onPaymentFailed | `InventoryRelease-PaymentFailed` | 결제 실패 → 재고 복구 |
| InventoryService | onPaymentRefunded | `InventoryRelease-PaymentRefunded` | 환불 완료 → 재고 복구 |
| PaymentService | onShippingFailed | `PaymentRefund` | 배송 실패 → 환불 |

**네이밍 규칙**: `{동작}-{트리거}`. 보상 리스너는 트리거가 다르면 별도 추적한다. 예를 들어 재고 복구는 "결제 실패" 경로와 "환불 완료" 경로 두 가지가 있으므로 eventType을 분리한다.

---

## 5. 리스너 유형별 적용 패턴

### 5-1. 정방향 리스너 (성공/실패 분기)

InventoryService, PaymentService, ShippingService의 메인 리스너가 이 패턴을 사용한다.

```java
@Transactional
public void onOrderCreated(SagaOrderCreated avroEvent, Acknowledgment ack) {
    OrderCreated event = SagaEventMapper.toDomain(avroEvent);
    SagaMdc.set(event.correlationId(), event.orderId());
    try {
        // (1) 선점: 비즈니스 로직 전에 처리 권한 확보
        if (!idempotencyChecker.tryAcquire(event.correlationId(), "InventoryReserve")) {
            log.warn("[SAGA] Duplicate InventoryReserve ignored");
            ack.acknowledge();
            return;
        }

        try {
            // (2) 비즈니스 로직
            reserve(items);

            // (3) 성공 이벤트 발행
            kafkaTemplate.send("chapter3.inventory-reserved", ...);
            ack.acknowledge();
            // TX 커밋 → ProcessedEvent 확정

        } catch (Exception e) {
            // (4) 실패 이벤트 발행
            kafkaTemplate.send("chapter3.inventory-reservation-failed", ...);
            ack.acknowledge();
            // TX 커밋 → ProcessedEvent 확정 (실패도 "처리 완료"로 기록)
            // → 재전달 시 tryAcquire=false → 실패 이벤트 중복 발행 방지
        }
    } finally {
        SagaMdc.clear();
    }
}
```

**왜 실패 경로에서도 ProcessedEvent가 커밋되는가?**

`catch` 블록이 예외를 삼키므로 `@Transactional`은 정상 완료로 간주한다. 따라서 `tryAcquire()`의 INSERT도 커밋된다. 이것이 의도된 동작이다 — 실패 이벤트를 이미 발행했으므로, 재전달 시 다시 처리하면 **실패 이벤트가 중복 발행**되어 보상 트랜잭션을 다중 트리거할 수 있다.

### 5-2. 보상 리스너 (실패 시 재시도)

InventoryService의 `onPaymentFailed`, `onPaymentRefunded`와 PaymentService의 `onShippingFailed`가 이 패턴을 사용한다.

```java
@Transactional
public void onPaymentFailed(SagaPaymentFailed avroEvent, Acknowledgment ack) {
    PaymentFailed event = SagaEventMapper.toDomain(avroEvent);
    SagaMdc.set(event.correlationId(), event.orderId());
    try {
        // (1) 선점
        if (!idempotencyChecker.tryAcquire(event.correlationId(), "InventoryRelease-PaymentFailed")) {
            ack.acknowledge();
            return;
        }

        try {
            // (2) 보상 로직
            releaseInventory(event.orderId(), event.correlationId());
            ack.acknowledge();
            // TX 커밋 → ProcessedEvent 확정

        } catch (Exception e) {
            // (3) 보상 실패 → 재시도 필요
            throw e;
            // TX 롤백 → ProcessedEvent도 롤백 → 재시도 시 tryAcquire 다시 성공
        }
    } finally {
        SagaMdc.clear();
    }
}
```

**정방향과 보상의 차이:**

| | 정방향 (forward) | 보상 (compensation) |
|---|---|---|
| 실패 시 | catch → 실패 이벤트 발행 → TX 커밋 | throw → TX 롤백 → 재시도 |
| ProcessedEvent | 성공/실패 모두 커밋됨 | 성공만 커밋, 실패 시 롤백 |
| 이유 | 실패 이벤트가 "결과"이므로 완료로 간주 | 보상은 반드시 성공해야 하므로 재시도 필요 |

### 5-3. 상태 업데이트 리스너 (OrderService)

OrderService의 4개 리스너가 이 패턴을 사용한다. 후속 이벤트를 발행하지 않으므로 가장 단순하다.

```java
@Transactional
public void onShippingRequested(SagaShippingRequested avroEvent, Acknowledgment ack) {
    ShippingRequested event = SagaEventMapper.toDomain(avroEvent);
    SagaMdc.set(event.correlationId(), event.orderId());
    try {
        // (1) 선점
        if (!idempotencyChecker.tryAcquire(event.correlationId(), "OrderComplete")) {
            ack.acknowledge();
            return;
        }

        // (2) 상태 업데이트만 (이벤트 발행 없음)
        Order order = orderRepository.findById(event.orderId()).orElseThrow();
        order.setStatus(OrderStatus.COMPLETED);
        order.setTrackingNumber(event.trackingNumber());
        orderRepository.save(order);

        ack.acknowledge();
    } finally {
        SagaMdc.clear();
    }
}
```

---

## 6. 동시성 시나리오 분석

### 정상 케이스: 단일 스레드

```
Thread A: tryAcquire() → SELECT: 없음 → INSERT: 1 → true
Thread A: 비즈니스 로직 실행 → 성공
Thread A: TX 커밋 → ProcessedEvent 확정
```

### 경합 케이스: 두 스레드 동시 처리

```
Thread A: tryAcquire() → SELECT: 없음
Thread B: tryAcquire() → SELECT: 없음  (A의 INSERT가 아직 미커밋)
Thread A: INSERT ... WHERE NOT EXISTS → 1 (성공)
Thread B: INSERT ... WHERE NOT EXISTS → 0 (A가 먼저 삽입)
Thread A: 비즈니스 로직 실행 → 성공
Thread B: tryAcquire() = false → ack → return (스킵)
```

**이전 방식과의 차이:**

| | 이전 (check-then-act) | 현재 (preemptive acquire) |
|---|---|---|
| 경합 시 | 두 스레드 모두 비즈니스 로직 실행 | 한 스레드만 비즈니스 로직 실행 |
| 동시성 해결 | `DataIntegrityViolationException` catch | `INSERT ... WHERE NOT EXISTS` 반환값 |
| 트랜잭션 오염 | 있음 (rollback-only) | 없음 |
| 비즈니스 로직 이중 실행 | 가능 | 불가능 |

---

## 7. 기존 멱등성 메커니즘과의 관계

PaymentService에는 이미 상태 기반 멱등성이 있었다:

```java
// 도메인 수준 멱등성 (PaymentService.onShippingFailed)
if (payment.getStatus() == PaymentStatus.REFUNDED) {
    log.warn("Payment already refunded, skipping");
    return;
}
```

이것은 **도메인 수준 멱등성**으로, 비즈니스 로직에 의존한다. `tryAcquire()`는 **인프라 수준 멱등성**으로, 비즈니스 로직과 독립적이다. 두 가지를 함께 사용하면 **이중 보호**가 된다:

| 레이어 | 메커니즘 | 장점 | 한계 |
|--------|----------|------|------|
| 인프라 | `tryAcquire(correlationId, eventType)` | 범용, 비즈니스 로직 무관, 동시성 안전 | DB 테이블 필요, 정리 필요 |
| 도메인 | 상태 체크 (REFUNDED 등) | 추가 테이블 불필요, 직관적 | 비즈니스 로직마다 다르게 구현 |

---

## 8. 코드 리뷰 반영 사항

초기 구현 후 코드 리뷰에서 CRITICAL 2건, HIGH 3건이 발견되어 수정했다.

### 수정 전 (check-then-act)

```java
// 문제 1: 비즈니스 로직 후에 markProcessed → 사이에 동시성 갭
// 문제 2: markProcessed()의 DataIntegrityViolationException → 트랜잭션 오염
// 문제 3: 실패 경로에서 markProcessed 누락 → 실패 이벤트 중복 발행
if (isDuplicate(correlationId, eventType)) { return; }
businessLogic();
kafkaTemplate.send(...);
markProcessed(correlationId, eventType);  // ← 여기서 트랜잭션 오염 가능
```

### 수정 후 (preemptive acquire)

```java
// 해결: 비즈니스 로직 전에 선점 + 네이티브 쿼리로 예외 없음
if (!tryAcquire(correlationId, eventType)) { return; }
businessLogic();
kafkaTemplate.send(...);
// markProcessed 불필요 — tryAcquire에서 이미 기록됨
```

| 이슈 | 심각도 | 원인 | 수정 |
|------|--------|------|------|
| 트랜잭션 오염 | CRITICAL | `saveAndFlush()` + `DataIntegrityViolationException` | `INSERT...WHERE NOT EXISTS` 네이티브 쿼리 |
| 실패 이벤트 중복 | CRITICAL | catch 경로에서 `markProcessed` 누락 | 선점 방식 — 비즈니스 로직 전에 기록 |
| Kafka send 후 markProcessed | HIGH | send 성공 + markProcessed 실패 → 중복 전송 | 선점 방식으로 순서 문제 해소 |
| SendTo 멱등성 누락 | HIGH | `InventoryServiceWithSendTo`에 체크 없음 | 학습용 경고 Javadoc 추가 |
| 반환값 무시 | HIGH | `markProcessed()` 반환값 미사용 | `tryAcquire()` 단일 반환값으로 통합 |

---

## 9. 프로덕션 고려사항

### ProcessedEvent 테이블 정리

```sql
-- 7일 이상 지난 레코드 삭제 (배치 작업)
DELETE FROM ch03_processed_events WHERE processed_at < NOW() - INTERVAL 7 DAY;
```

보존 기간은 최대 재시도 기간보다 길어야 한다. DefaultErrorHandler가 3회 재시도(3초)를 하므로 7일이면 충분하다.

### 인덱스

유니크 제약이 자동으로 `(correlation_id, event_type)` 복합 인덱스를 생성한다. `existsByCorrelationIdAndEventType`과 `INSERT ... WHERE NOT EXISTS` 모두 이 인덱스를 사용한다.

### 대안: Redis 기반

```java
String key = "processed:" + correlationId + ":" + eventType;
Boolean isNew = redisTemplate.opsForValue().setIfAbsent(key, "1", Duration.ofDays(7));
if (Boolean.FALSE.equals(isNew)) { return; }
```

Redis는 DB보다 빠르고 TTL로 자동 정리되지만, JPA 트랜잭션과 원자적이지 않다. 선점 방식의 "TX 롤백 시 함께 롤백" 보장이 불가능하다.

### 알려진 한계: DB-Kafka 원자성

JPA 커밋 성공 후 Kafka 커밋이 실패하면 불일치가 발생할 수 있다. 이것은 Transactional Outbox 패턴으로만 완전히 해결 가능하며, #5-1에서 별도로 다룬다.

---

## 10. 핵심 학습 포인트

1. **at-least-once + 멱등성 = effectively-once**: Kafka의 전달 보장과 애플리케이션 멱등성을 결합하면 사실상 정확히 한 번 처리를 구현할 수 있다.
2. **선점 방식 > check-then-act**: 비즈니스 로직 전에 기록하면 동시성 갭, 트랜잭션 오염, 실패 경로 누락이 한꺼번에 해결된다.
3. **네이티브 쿼리로 트랜잭션 보호**: `INSERT ... WHERE NOT EXISTS`는 예외 없이 0/1을 반환하므로 `@Transactional`을 오염시키지 않는다.
4. **correlationId + eventType = SAGA 단계별 독립 추적**: 하나의 SAGA에서 여러 단계와 여러 실패 경로를 구분한다.
5. **정방향 vs 보상의 실패 처리 차이**: 정방향은 실패도 "완료" (실패 이벤트 발행), 보상은 실패 시 롤백+재시도.
6. **인프라 멱등성 + 도메인 멱등성 = 이중 보호**: 두 레이어가 독립적으로 중복을 차단한다.
