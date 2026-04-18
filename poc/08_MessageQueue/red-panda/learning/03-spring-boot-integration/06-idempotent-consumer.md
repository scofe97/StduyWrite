# 06. 멱등 소비자 구현 (Idempotent Consumer)

> **이론 배경**: `01-event-driven/learning/17-idempotency-patterns.md` 참고
> **실습 기반**: ch03 SAGA Choreography 실제 구현 코드

---

## 학습 목표

- Spring Boot `@KafkaListener`에서 멱등성을 보장하는 3가지 구현 전략 습득
- Preemptive acquire 패턴의 원리와 구현 방법 이해
- `@Transactional`과 멱등성 로직의 상호작용 파악
- 기존 ch03 SAGA 실습 코드를 재활용한 범용 멱등성 컴포넌트 설계

---

## 1. Spring Boot에서 멱등 소비자가 필요한 이유

`@KafkaListener`는 기본적으로 **at-least-once** 전달을 보장한다. 즉, Kafka는 메시지가 **최소 한 번** 전달되도록 보장하지만, 동일한 메시지가 **두 번 이상** 전달될 수 있다. 이것이 기본값인 이유는 정확히 한 번 전달(exactly-once)보다 성능과 구현 단순성이 우월하기 때문이다.

### 중복 소비가 발생하는 세 가지 시나리오

```
시나리오 1: Consumer Rebalance
─────────────────────────────
Consumer A가 offset 100번 메시지를 처리 중
→ A가 죽거나 GC pause 발생
→ Consumer Rebalance 시작
→ Consumer B가 offset 100번부터 재소비
→ 동일 메시지 두 번 처리

시나리오 2: Spring Kafka DefaultErrorHandler 재시도
───────────────────────────────────────────────────
@KafkaListener가 예외를 던짐
→ DefaultErrorHandler가 2초 후 재시도
→ 외부 API 호출이 이미 성공했지만 응답 중 예외 발생
→ 재시도에서 동일 외부 API 재호출 → 중복 처리

시나리오 3: @RetryableTopic 재시도
────────────────────────────────
처리 실패 → Retry Topic으로 전송
→ 원래 토픽에서는 offset commit
→ Retry Topic에서 동일 이벤트 재소비
→ 실패 이유가 일시적이면 두 번 성공할 수도 있음
```

### 비즈니스 영향: 중복이 허용되지 않는 사례

중복 소비가 단순 로그 중복이라면 무시해도 된다. 그러나 다음 경우는 비즈니스에 직접 손해를 끼친다.

- **중복 결제**: `PaymentService.onInventoryReserved()`가 두 번 실행되면 고객에게 두 번 청구
- **중복 재고 차감**: `InventoryService.onOrderCreated()`가 두 번 실행되면 재고가 실제보다 적게 남음
- **중복 알림**: 이메일, SMS가 동일 내용으로 두 번 발송
- **SAGA 보상 중복**: `PaymentRefunded` 이벤트가 두 번 처리되면 이미 환불된 금액을 다시 환불 시도

### build.gradle 의존성 확인

이 챕터는 기존 ch03 설정을 그대로 활용한다. 별도 의존성 추가는 필요 없다.

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.kafka:spring-kafka'
    runtimeOnly 'org.postgresql:postgresql'

    // 테스트: Redpanda + PostgreSQL Testcontainers
    testImplementation 'org.testcontainers:redpanda'
    testImplementation 'org.testcontainers:postgresql'
    testImplementation 'org.testcontainers:junit-jupiter'
    testImplementation 'org.awaitility:awaitility'
}
```

---

## 2. 전략 1: DB Upsert (자연적 멱등성)

가장 단순한 전략이다. 이벤트가 나타내는 **최종 상태**를 그냥 덮어쓰면 몇 번을 실행해도 결과가 같아진다. 이것을 "자연적 멱등성(natural idempotency)"이라고 한다.

### 언제 적합한가

- 마지막 값만 중요한 경우: 상품 가격 업데이트, 사용자 프로필 동기화
- 누산이 없는 상태 전이: `PENDING → COMPLETED` (같은 전이를 두 번 해도 결과 동일)
- 이벤트 자체가 전체 상태를 포함하는 경우

### 언제 부적합한가

- 재고 차감처럼 **누산 연산**이 있는 경우 (10개 차감을 두 번 하면 20개 차감)
- 결제처럼 **외부 시스템 호출**이 포함된 경우 (DB Upsert로는 외부 중복 호출 방지 불가)

### JPA 구현 예시: ProductStateConsumer

```java
@Entity
@Table(name = "product_states")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ProductState {

    @Id
    private String productId;           // 자연 키 = 이벤트 키

    private String name;
    private BigDecimal price;
    private Instant updatedAt;
}
```

```java
@Service
@Slf4j
@RequiredArgsConstructor
public class ProductStateConsumer {

    private final ProductStateRepository repository;

    /**
     * 상품 상태를 덮어쓴다.
     * JPA save()는 ID가 존재하면 UPDATE, 없으면 INSERT를 수행한다.
     * 따라서 동일 이벤트를 N번 처리해도 결과는 항상 동일 — 자연적 멱등성.
     */
    @Transactional
    @KafkaListener(topics = "product-state-updated", groupId = "product-state-consumer")
    public void onProductStateUpdated(ProductStateUpdatedEvent event, Acknowledgment ack) {
        ProductState state = ProductState.builder()
                .productId(event.getProductId())
                .name(event.getName())
                .price(event.getPrice())
                .updatedAt(Instant.now())
                .build();

        repository.save(state);  // merge semantics: 있으면 UPDATE, 없으면 INSERT
        ack.acknowledge();

        log.info("[UPSERT] Product state updated: productId={}", event.getProductId());
    }
}
```

```sql
-- PostgreSQL: 더 명시적인 Upsert (네이티브 쿼리 활용 시)
INSERT INTO product_states (product_id, name, price, updated_at)
VALUES (:productId, :name, :price, :updatedAt)
ON CONFLICT (product_id)
DO UPDATE SET
    name       = EXCLUDED.name,
    price      = EXCLUDED.price,
    updated_at = EXCLUDED.updated_at;
```

> **주의**: JPA `save()`의 merge 동작은 `@Version` 필드가 없으면 낙관적 잠금이 적용되지 않는다. 동시에 두 Consumer가 같은 productId를 처리하면 마지막 write가 이긴다(last-write-wins). 이것이 "최신 값만 중요"한 경우에만 적합한 이유다.

---

## 3. 전략 2: Dedup Table (ProcessedEvent)

재고 차감, 결제처럼 누산 연산이 포함된 경우에는 DB Upsert로는 멱등성을 보장할 수 없다. 이때는 별도의 **중복 제거 테이블(Dedup Table)**을 사용한다. "이 이벤트를 이미 처리했는가?"를 DB에 기록해두고, 이미 처리했다면 건너뛰는 방식이다.

ch03 SAGA 실습이 정확히 이 방식을 사용한다.

### 3.1 테이블 설계

```sql
-- PostgreSQL DDL
CREATE TABLE ch03_processed_events (
    id             VARCHAR(36)  NOT NULL,
    correlation_id VARCHAR(36)  NOT NULL,
    event_type     VARCHAR(100) NOT NULL,
    processed_at   TIMESTAMPTZ  NOT NULL,

    PRIMARY KEY (id),

    -- 핵심: (correlationId, eventType) 복합 유니크 제약
    -- "같은 SAGA 흐름(correlationId)에서 같은 단계(eventType)는 한 번만"을 보장
    CONSTRAINT uk_correlation_event_type
        UNIQUE (correlation_id, event_type)
);

-- 조회 성능을 위한 인덱스 (UNIQUE 제약이 이미 인덱스를 생성하지만, 명시적으로)
CREATE INDEX idx_processed_events_correlation ON ch03_processed_events(correlation_id);
```

복합 키 `(correlationId, eventType)`이 핵심이다. `correlationId`만으로는 SAGA 단계를 구분할 수 없다. 예를 들어, 같은 주문(correlationId)에 대해 재고 예약(`INVENTORY_RESERVE`)과 결제 처리(`PAYMENT_PROCESS`)는 서로 다른 이벤트 타입이므로 각각 한 번씩 처리되어야 한다. `correlationId` 단독 유니크 제약이었다면 두 번째 단계부터 모두 중복으로 판단하는 버그가 생긴다.

```java
// SagaStepType: 모든 SAGA 단계를 열거
public enum SagaStepType {
    INVENTORY_RESERVE,
    INVENTORY_RELEASE_PAYMENT_FAILED,
    INVENTORY_RELEASE_PAYMENT_REFUNDED,
    PAYMENT_PROCESS,
    PAYMENT_REFUND,
    SHIPPING_REQUEST,
    ORDER_COMPLETE,
    ORDER_CANCEL
}
```

```java
@Entity
@Table(name = "ch03_processed_events",
       uniqueConstraints = @UniqueConstraint(
               name = "uk_correlation_event_type",
               columnNames = {"correlationId", "eventType"}))
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProcessedEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;

    @Column(nullable = false)
    private String correlationId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private SagaStepType eventType;

    @Column(nullable = false)
    private Instant processedAt;
}
```

### 3.2 check-then-act의 함정 (안티패턴)

직관적으로 떠오르는 구현은 "먼저 중복인지 확인하고, 아니면 처리한 후, 처리 완료를 기록"하는 순서다. 이것이 **check-then-act** 패턴이며, 두 가지 심각한 문제를 가진다.

**문제 1: 동시성 레이스 컨디션**

```
Consumer A                          Consumer B
────────────────────────────────    ────────────────────────────────
isDuplicate() → false               isDuplicate() → false
비즈니스 로직 실행 중...              비즈니스 로직 실행 중...
markProcessed() → 성공              markProcessed() → 성공(또는 예외)
                                    ↑ 둘 다 처리 완료!
```

두 Consumer가 동시에 `isDuplicate() = false`를 받으면 둘 다 비즈니스 로직을 실행한다. Kafka Consumer Group에서는 같은 파티션을 동시에 소비하지 않으므로 이 경우가 드물지만, 서비스 재시작이나 Rebalance 직후에는 발생한다.

**문제 2: Hibernate 세션 rollback-only 오염**

```java
// 안티패턴: saveAndFlush + DataIntegrityViolationException catch
@Transactional
@KafkaListener(...)
public void onEvent(Event event, Acknowledgment ack) {
    // 1차 SELECT: 중복 확인
    if (processedEventRepository.existsByCorrelationId(event.correlationId())) {
        ack.acknowledge();
        return;
    }

    // 비즈니스 로직
    doBusinessLogic(event);

    // 2차 INSERT: 처리 완료 기록
    try {
        ProcessedEvent pe = ProcessedEvent.builder()
                .correlationId(event.correlationId())
                .eventType(SagaStepType.PAYMENT_PROCESS)
                .processedAt(Instant.now())
                .build();
        processedEventRepository.saveAndFlush(pe); // ← 문제 발생 지점
    } catch (DataIntegrityViolationException e) {
        // 동시에 다른 Consumer가 먼저 INSERT함 → UNIQUE 제약 위반
        // DataIntegrityViolationException을 catch하면...
        // Hibernate 세션이 이미 rollback-only 상태로 마킹됨!
        log.warn("Concurrent duplicate detected, ignoring: {}", event.correlationId());
        ack.acknowledge();
        return;
        // ↑ 여기서 return해도 @Transactional이 커밋을 시도하면
        //   UnexpectedRollbackException 발생 → 비즈니스 로직도 롤백
    }

    ack.acknowledge();
}
```

`saveAndFlush()`가 `DataIntegrityViolationException`을 던지는 순간, Spring의 트랜잭션 인터셉터가 해당 예외를 감지하고 현재 트랜잭션을 **rollback-only**로 마킹한다. 이 상태에서는 나중에 `catch`로 예외를 삼켜도 이미 늦었다. 트랜잭션이 커밋을 시도하면 `UnexpectedRollbackException`이 발생하고, 비즈니스 로직이 성공했음에도 모든 변경이 롤백된다.

결론: **예외를 던지지 않는 방법으로 중복을 처리해야 한다.**

### 3.3 preemptive acquire 패턴 (권장)

ch03에서 실제로 사용하는 패턴이다. 핵심 아이디어는 **"비즈니스 로직 실행 전에 처리 권한을 원자적으로 선점"**하는 것이다.

```
check-then-act (문제)          preemptive acquire (해결)
──────────────────────         ────────────────────────────
SELECT → 없음                  INSERT ... WHERE NOT EXISTS
비즈니스 로직                  ↓ 반환값 확인
INSERT → 성공 or 예외          0 = 이미 처리됨 → 스킵
                               1 = 선점 성공 → 비즈니스 로직
```

`INSERT ... WHERE NOT EXISTS`는 **원자적(atomic)**이다. DB 레벨에서 SELECT와 INSERT가 한 문장으로 실행되므로 두 Consumer가 동시에 실행해도 정확히 하나만 성공한다. 그리고 예외를 던지지 않고 **반환값(0 또는 1)**으로 결과를 알려주므로 Hibernate 세션이 오염되지 않는다.

```java
// ProcessedEventRepository
public interface ProcessedEventRepository extends JpaRepository<ProcessedEvent, String> {

    boolean existsByCorrelationIdAndEventType(String correlationId, SagaStepType eventType);

    /**
     * 트랜잭션 오염 없는 조건부 INSERT.
     *
     * 레코드가 이미 존재하면 0 반환 (예외 없음).
     * 신규면 INSERT 후 1 반환.
     *
     * DataIntegrityViolationException을 발생시키지 않으므로
     * 호출자의 @Transactional이 오염되지 않는다.
     */
    @Modifying
    @Query(nativeQuery = true, value =
            "INSERT INTO ch03_processed_events (id, correlation_id, event_type, processed_at) " +
            "SELECT :id, :correlationId, :eventType, :processedAt " +
            "WHERE NOT EXISTS (" +
            "  SELECT 1 FROM ch03_processed_events " +
            "  WHERE correlation_id = :correlationId AND event_type = :eventType)")
    int insertIfAbsent(@Param("id") String id,
                       @Param("correlationId") String correlationId,
                       @Param("eventType") String eventType,
                       @Param("processedAt") Instant processedAt);
}
```

```java
// EventIdempotencyChecker: 선점 방식 멱등성 체커
@Component
@RequiredArgsConstructor
@Slf4j
public class EventIdempotencyChecker {

    private final ProcessedEventRepository processedEventRepository;

    /**
     * 멱등성 선점 시도.
     * 비즈니스 로직 실행 전에 호출하여 처리 권한을 "선점"한다.
     *
     * 2단계 전략:
     * 1차) existsByCorrelationIdAndEventType() — 빠른 SELECT (대부분의 중복을 저렴하게 차단)
     * 2차) insertIfAbsent() — 원자적 INSERT (동시성 안전, 예외 없음)
     *
     * @return true = 선점 성공 (비즈니스 로직 진행), false = 이미 처리됨 (스킵)
     */
    public boolean tryAcquire(String correlationId, SagaStepType stepType) {
        // 1차: 빠른 SELECT 조회 (대부분의 중복을 여기서 차단 — DB 부하 최소화)
        if (processedEventRepository.existsByCorrelationIdAndEventType(correlationId, stepType)) {
            log.debug("[IDEMPOTENCY] Already processed: correlationId={}, stepType={}",
                    correlationId, stepType);
            return false;
        }

        // 2차: INSERT ... WHERE NOT EXISTS (동시성 안전, 트랜잭션 오염 없음)
        // 네이티브 쿼리는 enum을 직접 처리할 수 없으므로 .name()으로 문자열 전달
        int inserted = processedEventRepository.insertIfAbsent(
                UUID.randomUUID().toString(),
                correlationId,
                stepType.name(),
                Instant.now());

        if (inserted == 0) {
            log.warn("[IDEMPOTENCY] Concurrent duplicate detected: correlationId={}, stepType={}",
                    correlationId, stepType);
        }

        return inserted > 0;
    }
}
```

**2단계 전략인 이유**: 1차 SELECT는 빠르고 저렴하다. 대부분의 재시도(중복)는 1차에서 차단된다. 2차 `insertIfAbsent()`는 네이티브 쿼리 실행 비용이 있으므로, 실제로 동시 충돌이 있을 때만 실행된다. 운영 환경에서 중복 이벤트의 99%는 1차에서 처리된다.

### 3.4 Forward 리스너 vs Compensation 리스너의 차이

같은 preemptive acquire 패턴을 사용하지만, 비즈니스 로직 실패 시 처리 방식이 **의도적으로 다르다**. 이 차이를 이해하는 것이 핵심이다.

```
Forward 리스너 실패 처리 흐름:
──────────────────────────────────────────────────────────────
tryAcquire() → 성공 (ProcessedEvent INSERT됨, 트랜잭션 안)
비즈니스 로직 실행
예외 발생
catch 블록:
  실패 이벤트 발행 (예: PaymentFailed 토픽으로)
  ack.acknowledge()  ← 정상 return
  return             ← @Transactional은 커밋됨
결과: ProcessedEvent가 커밋 → 재시도 시 중복으로 스킵
왜 이래야 하는가: 실패 이벤트를 발행했으므로 처리는 완료됨.
                  재시도하면 또 실패 이벤트를 발행 → SAGA 흐름 오염.

Compensation 리스너 실패 처리 흐름:
──────────────────────────────────────────────────────────────
tryAcquire() → 성공 (ProcessedEvent INSERT됨, 트랜잭션 안)
보상 비즈니스 로직 실행
예외 발생
catch 블록:
  throw e  ← 예외를 다시 던짐
결과: @Transactional이 롤백 → ProcessedEvent도 함께 롤백
     → 재시도 시 tryAcquire() 다시 성공 → 보상 로직 재실행 가능
왜 이래야 하는가: 보상 트랜잭션이 실패하면 데이터가 불일치 상태.
                  반드시 다시 시도해야 하므로 ProcessedEvent도 롤백해야 함.
```

```
Forward 리스너 (예: InventoryService.onOrderCreated)
┌────────────────────────────────────────────────────────────────┐
│  @Transactional                                                │
│  tryAcquire() ──→ ProcessedEvent INSERT (트랜잭션 참여)         │
│  비즈니스 로직                                                  │
│      성공 ──→ InventoryReserved 발행 → ack → 커밋              │
│              ProcessedEvent 커밋 ✓                             │
│      실패 ──→ [catch] InventoryReservationFailed 발행          │
│              ack → return → 커밋                               │
│              ProcessedEvent 커밋 ✓ (재시도 시 스킵됨)           │
└────────────────────────────────────────────────────────────────┘

Compensation 리스너 (예: InventoryService.onPaymentFailed)
┌────────────────────────────────────────────────────────────────┐
│  @Transactional                                                │
│  tryAcquire() ──→ ProcessedEvent INSERT (트랜잭션 참여)         │
│  보상 비즈니스 로직                                              │
│      성공 ──→ InventoryReleased 발행 → ack → 커밋              │
│              ProcessedEvent 커밋 ✓                             │
│      실패 ──→ [catch] throw e                                  │
│              @Transactional 롤백                               │
│              ProcessedEvent도 롤백 ✓ (재시도 가능)              │
└────────────────────────────────────────────────────────────────┘
```

실제 ch03 코드를 보면 이 차이가 명확하다.

```java
// Forward 리스너: InventoryService.onOrderCreated (핵심만 발췌)
@Transactional
@KafkaListener(topics = "chapter3.order-created", groupId = "ch03-inventory-service",
               containerFactory = "ch03KafkaListenerContainerFactory")
public void onOrderCreated(SagaOrderCreated avroEvent, Acknowledgment ack) {
    OrderCreated event = SagaEventMapper.toDomain(avroEvent);

    if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.INVENTORY_RESERVE)) {
        ack.acknowledge();
        return;  // 중복 → 스킵
    }

    try {
        // 재고 차감 및 예약 생성 ...
        kafkaTemplate.send("chapter3.inventory-reserved", ...);
        ack.acknowledge();

    } catch (Exception e) {
        // 실패 → 실패 이벤트 발행 후 정상 return
        // ProcessedEvent는 커밋됨 → 재시도 시 중복으로 스킵
        kafkaTemplate.send("chapter3.inventory-reservation-failed", ...);
        ack.acknowledge();  // ← ack 후 return (예외 throw 아님)
    }
}

// Compensation 리스너: InventoryService.onPaymentFailed (핵심만 발췌)
@Transactional
@KafkaListener(topics = "chapter3.payment-failed", groupId = "ch03-inventory-service",
               containerFactory = "ch03KafkaListenerContainerFactory")
public void onPaymentFailed(SagaPaymentFailed avroEvent, Acknowledgment ack) {
    PaymentFailed event = SagaEventMapper.toDomain(avroEvent);

    if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.INVENTORY_RELEASE_PAYMENT_FAILED)) {
        ack.acknowledge();
        return;  // 중복 → 스킵
    }

    try {
        releaseInventory(event.orderId(), event.correlationId());
        ack.acknowledge();

    } catch (Exception e) {
        // 보상 실패 → 예외 throw
        // @Transactional 롤백 → ProcessedEvent도 롤백 → 재시도 가능
        throw e;  // ← 예외를 다시 던짐 (ack 없음)
    }
}
```

---

## 4. 전략 3: Idempotency Key 헤더

Producer가 Kafka Record Header에 고유 키를 삽입하고, Consumer가 이를 추출해 중복을 판단하는 방식이다. 이 전략은 **correlationId가 없는 독립적인 이벤트**에 적합하다. SAGA처럼 correlationId가 있는 경우에는 전략 2가 더 적합하다.

### Idempotency Key 자동 삽입: ProducerInterceptor

```java
// ProducerInterceptor 방식은 @Component만으로 등록되지 않음
// ProducerFactory에 직접 설정하거나, interceptor.classes 속성 사용 필요
@Component
public class IdempotencyKeyInterceptor implements ProducerInterceptor<String, Object> {

    public static final String IDEMPOTENCY_KEY_HEADER = "X-Idempotency-Key";

    @Override
    public ProducerRecord<String, Object> onSend(ProducerRecord<String, Object> record) {
        // 이미 키가 있으면 그대로 유지 (재시도 시 동일 키 보존)
        if (record.headers().lastHeader(IDEMPOTENCY_KEY_HEADER) != null) {
            return record;
        }

        // 없으면 새로 생성: UUID (단순) 또는 키+토픽+타임스탬프 조합 (추적 가능)
        String idempotencyKey = UUID.randomUUID().toString();
        record.headers().add(IDEMPOTENCY_KEY_HEADER, idempotencyKey.getBytes(StandardCharsets.UTF_8));
        return record;
    }

    @Override
    public void onAcknowledgement(RecordMetadata metadata, Exception exception) {}

    @Override
    public void close() {}

    @Override
    public void configure(Map<String, ?> configs) {}
}
```

```java
// ProducerFactory에 인터셉터 등록 (application.yml 방식도 가능)
@Bean
public ProducerFactory<String, Object> producerFactory() {
    Map<String, Object> configs = new HashMap<>();
    // ... 기본 설정 ...
    configs.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG,
            IdempotencyKeyInterceptor.class.getName());
    return new DefaultKafkaProducerFactory<>(configs);
}
```

### Consumer에서 헤더 기반 중복 제거

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class HeaderBasedDedupConsumer {

    private final HeaderDedupRepository dedupRepository;

    @Transactional
    @KafkaListener(topics = "notification-requested", groupId = "notification-consumer")
    public void onNotificationRequested(
            NotificationEvent event,
            @Header(name = "X-Idempotency-Key", required = false) String idempotencyKey,
            Acknowledgment ack) {

        // 헤더가 없으면 처리 (하위 호환성)
        if (idempotencyKey != null) {
            if (dedupRepository.existsById(idempotencyKey)) {
                log.warn("[DEDUP] Duplicate notification skipped: key={}", idempotencyKey);
                ack.acknowledge();
                return;
            }
            dedupRepository.save(new DedupRecord(idempotencyKey, Instant.now()));
        }

        // 알림 발송 로직
        sendNotification(event);
        ack.acknowledge();
    }
}
```

```java
@Entity
@Table(name = "dedup_records")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class DedupRecord {
    @Id
    private String idempotencyKey;    // X-Idempotency-Key 헤더값

    @Column(nullable = false)
    private Instant processedAt;
}
```

---

## 5. 범용 멱등성 컴포넌트 설계

ch03에서 검증된 `EventIdempotencyChecker`를 모든 Consumer에서 재사용할 수 있도록 범용화한다. AOP를 활용하면 멱등성 체크 코드를 비즈니스 로직에서 완전히 분리할 수 있다.

### @IdempotentListener 커스텀 어노테이션

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface IdempotentListener {

    /**
     * 이벤트 타입 식별자 (ProcessedEvent.eventType에 저장됨)
     */
    String eventType();

    /**
     * correlationId를 추출할 메서드 또는 필드 이름.
     * 이벤트 객체에서 getCorrelationId() 또는 correlationId()를 호출한다.
     */
    String correlationIdField() default "correlationId";
}
```

### IdempotencyAspect

```java
@Aspect
@Component
@RequiredArgsConstructor
@Slf4j
public class IdempotencyAspect {

    private final GenericIdempotencyChecker idempotencyChecker;

    @Around("@annotation(idempotentListener)")
    public Object checkIdempotency(ProceedingJoinPoint pjp,
                                   IdempotentListener idempotentListener) throws Throwable {
        // 첫 번째 파라미터에서 이벤트 객체 추출
        Object[] args = pjp.getArgs();
        if (args.length == 0) {
            return pjp.proceed();
        }

        Object event = args[0];
        String correlationId = extractCorrelationId(event, idempotentListener.correlationIdField());

        if (correlationId == null) {
            log.warn("[IDEMPOTENCY-AOP] correlationId not found, skipping idempotency check");
            return pjp.proceed();
        }

        String eventType = idempotentListener.eventType();

        if (!idempotencyChecker.tryAcquire(correlationId, eventType)) {
            log.warn("[IDEMPOTENCY-AOP] Duplicate skipped: correlationId={}, eventType={}",
                    correlationId, eventType);
            // Acknowledgment 파라미터를 찾아 ack 처리
            findAndAcknowledge(args);
            return null;
        }

        return pjp.proceed();
    }

    private String extractCorrelationId(Object event, String fieldName) {
        try {
            // correlationId() 메서드 시도 (record)
            var method = event.getClass().getMethod(fieldName);
            return (String) method.invoke(event);
        } catch (NoSuchMethodException e) {
            try {
                // getCorrelationId() 메서드 시도 (일반 클래스)
                String getter = "get" + Character.toUpperCase(fieldName.charAt(0))
                        + fieldName.substring(1);
                var method = event.getClass().getMethod(getter);
                return (String) method.invoke(event);
            } catch (Exception ex) {
                return null;
            }
        } catch (Exception e) {
            return null;
        }
    }

    private void findAndAcknowledge(Object[] args) {
        for (Object arg : args) {
            if (arg instanceof Acknowledgment ack) {
                ack.acknowledge();
                return;
            }
        }
    }
}
```

```java
// GenericIdempotencyChecker: String eventType을 받는 범용 버전
@Component
@RequiredArgsConstructor
@Slf4j
public class GenericIdempotencyChecker {

    private final GenericProcessedEventRepository repository;

    public boolean tryAcquire(String correlationId, String eventType) {
        if (repository.existsByCorrelationIdAndEventType(correlationId, eventType)) {
            return false;
        }

        int inserted = repository.insertIfAbsent(
                UUID.randomUUID().toString(),
                correlationId,
                eventType,
                Instant.now());

        return inserted > 0;
    }
}
```

### AOP 어노테이션 적용 예시

```java
@Service
@Slf4j
@RequiredArgsConstructor
public class NotificationService {

    @Transactional
    @KafkaListener(topics = "order-completed", groupId = "notification-service")
    @IdempotentListener(eventType = "NOTIFICATION_SEND")   // ← 어노테이션 하나로 멱등성 적용
    public void onOrderCompleted(OrderCompletedEvent event, Acknowledgment ack) {
        // 멱등성 체크는 AOP가 처리 — 비즈니스 로직에 집중
        sendOrderCompletionEmail(event.customerId(), event.orderId());
        ack.acknowledge();
        log.info("[NOTIFICATION] Email sent: orderId={}", event.orderId());
    }
}
```

### application.yml 설정

```yaml
# application.yml
idempotency:
  strategy: dedup           # upsert | dedup | header
  dedup:
    table-name: processed_events
    ttl-days: 7             # 7일 후 자동 삭제
  header:
    key-name: X-Idempotency-Key
```

---

## 6. Kafka Transactions + 멱등성

**exactly-once semantics(EOS)**는 Kafka 자체 트랜잭션 기능으로 멱등성을 보장하는 방법이다. Spring Kafka에서는 `DefaultKafkaProducerFactory`에 `transactionIdPrefix`를 설정해서 활성화한다.

### EOS 설정

```java
// KafkaConfig: Transactional Producer 설정
@Bean
public ProducerFactory<String, Object> transactionalProducerFactory() {
    Map<String, Object> configs = new HashMap<>();
    configs.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
    configs.put(ProducerConfig.ACKS_CONFIG, "all");
    configs.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);  // Producer 멱등성
    // ...

    DefaultKafkaProducerFactory<String, Object> factory =
            new DefaultKafkaProducerFactory<>(configs);
    factory.setTransactionIdPrefix("tx-");  // ← 트랜잭션 활성화
    return factory;
}

// Consumer: isolation.level 설정 필수
@Bean
public ConsumerFactory<String, Object> transactionalConsumerFactory() {
    Map<String, Object> configs = new HashMap<>();
    // ...
    configs.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");  // ← 커밋된 메시지만 읽기
    return new DefaultKafkaConsumerFactory<>(configs);
}
```

### @Transactional + @KafkaListener: read-process-write 패턴

```java
@Service
@Slf4j
public class TransactionalConsumer {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final OrderRepository orderRepository;

    @Transactional("kafkaTransactionManager")  // Kafka 트랜잭션 매니저 지정
    @KafkaListener(topics = "order-created", groupId = "transactional-consumer")
    public void onOrderCreated(OrderCreatedEvent event, Acknowledgment ack) {
        // read (Kafka)
        // process (DB)
        orderRepository.save(Order.from(event));

        // write (Kafka) — 이 send()도 같은 트랜잭션 안에서 실행
        kafkaTemplate.send("order-processed", new OrderProcessedEvent(event.orderId()));

        // Kafka 트랜잭션이 커밋되어야 offset commit과 메시지 발행이 원자적으로 완료
        // @Transactional이 커밋하면 Kafka offset + 발행 메시지가 한꺼번에 커밋됨
    }
}
```

### EOS vs at-least-once + 멱등성: 성능 비교

```
┌─────────────────────┬──────────────────────────┬──────────────────────────┐
│ 항목                │ EOS (Kafka Transaction)   │ at-least-once + Dedup    │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ 처리량              │ 낮음 (트랜잭션 오버헤드)  │ 높음                     │
│ 레이턴시            │ 높음 (2PC 유사)           │ 낮음                     │
│ 구현 복잡도         │ 낮음 (설정만으로 가능)    │ 중간 (Dedup 테이블 필요) │
│ 적용 범위           │ Kafka → Kafka만           │ Kafka → 임의 DB/외부 API │
│ 외부 API 보호       │ 불가                      │ 가능                     │
│ 운영 비용           │ Transaction Log 관리      │ Dedup 테이블 TTL 관리    │
└─────────────────────┴──────────────────────────┴──────────────────────────┘
```

결제 API, 재고 차감처럼 **외부 시스템 호출**이 포함된 경우 EOS만으로는 부족하다. Kafka 트랜잭션은 Kafka 내부(토픽 간 메시지 발행 + offset commit)에만 원자성을 보장하기 때문이다. 외부 API 중복 호출 방지는 Dedup Table 전략이 필요하다.

---

## 7. 테스트 전략

멱등성 테스트의 핵심은 단순하다: **"같은 메시지를 N번 보내고, 비즈니스 효과가 1번만 발생했는지 검증"**한다.

### 통합 테스트: Testcontainers + Redpanda

```java
@SpringBootTest
@Testcontainers
@ActiveProfiles("test")
class IdempotentConsumerIntegrationTest {

    @Container
    static RedpandaContainer redpanda = new RedpandaContainer("docker.redpanda.com/redpandadata/redpanda:v25.1.1");

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.bootstrap-servers", redpanda::getBootstrapServers);
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private ProcessedEventRepository processedEventRepository;

    @Test
    @DisplayName("동일 이벤트를 3번 발행해도 주문 생성은 1번만 발생해야 한다")
    void duplicateEvents_shouldProcessOnce() throws Exception {
        String correlationId = UUID.randomUUID().toString();
        String orderId = UUID.randomUUID().toString();

        OrderCreatedEvent event = OrderCreatedEvent.builder()
                .orderId(orderId)
                .correlationId(correlationId)
                .totalAmount(BigDecimal.valueOf(50000))
                .build();

        // 동일 이벤트를 3번 발행
        for (int i = 0; i < 3; i++) {
            kafkaTemplate.send("chapter3.order-created", event);
        }

        // 처리 완료 대기
        await().atMost(Duration.ofSeconds(10))
               .until(() -> processedEventRepository.existsByCorrelationIdAndEventType(
                       correlationId, SagaStepType.INVENTORY_RESERVE));

        // 잠시 더 대기 (중복 처리가 일어나지 않도록 충분한 시간)
        Thread.sleep(2000);

        // 비즈니스 효과 검증: 재고 예약은 정확히 1번
        List<Reservation> reservations = reservationRepository.findByOrderId(orderId);
        assertThat(reservations).hasSize(event.getItems().size());  // 아이템 수만큼만

        // ProcessedEvent도 1건만 존재
        List<ProcessedEvent> processedEvents = processedEventRepository.findByCorrelationId(correlationId);
        long inventoryReserveCount = processedEvents.stream()
                .filter(pe -> pe.getEventType() == SagaStepType.INVENTORY_RESERVE)
                .count();
        assertThat(inventoryReserveCount).isEqualTo(1);
    }
}
```

### 동시성 테스트: CountDownLatch + ExecutorService

```java
@Test
@DisplayName("동시에 5개의 Consumer가 같은 이벤트를 처리해도 1번만 처리되어야 한다")
void concurrentDuplicates_shouldProcessOnce() throws Exception {
    String correlationId = UUID.randomUUID().toString();
    int concurrency = 5;

    CountDownLatch startLatch = new CountDownLatch(1);
    CountDownLatch doneLatch = new CountDownLatch(concurrency);
    AtomicInteger successCount = new AtomicInteger(0);

    ExecutorService executor = Executors.newFixedThreadPool(concurrency);

    for (int i = 0; i < concurrency; i++) {
        executor.submit(() -> {
            try {
                startLatch.await();  // 동시 시작 대기
                boolean acquired = idempotencyChecker.tryAcquire(correlationId, SagaStepType.PAYMENT_PROCESS);
                if (acquired) {
                    successCount.incrementAndGet();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                doneLatch.countDown();
            }
        });
    }

    startLatch.countDown();  // 동시 시작
    doneLatch.await(5, TimeUnit.SECONDS);
    executor.shutdown();

    // 5개 중 정확히 1개만 선점 성공해야 함
    assertThat(successCount.get()).isEqualTo(1);

    // DB에도 1건만 존재
    assertThat(processedEventRepository.existsByCorrelationIdAndEventType(
            correlationId, SagaStepType.PAYMENT_PROCESS)).isTrue();
    assertThat(processedEventRepository.findByCorrelationId(correlationId)).hasSize(1);
}
```

---

## 8. 운영 고려사항

### ProcessedEvent 테이블 크기 관리 (TTL 기반 정리)

ProcessedEvent 테이블은 무한히 커질 수 있다. 이벤트가 처리되고 나면 이론적으로는 영구 보관이 필요 없다. Kafka의 기본 메시지 보존 기간(7일)에 맞춰 TTL을 7일로 설정하는 것이 일반적이다. 7일이 지난 이벤트는 Kafka에서도 삭제되어 재소비될 수 없으므로 ProcessedEvent 기록도 불필요하다.

```java
@Component
@Slf4j
@RequiredArgsConstructor
public class ProcessedEventCleanupScheduler {

    private final ProcessedEventRepository processedEventRepository;

    @Value("${idempotency.dedup.ttl-days:7}")
    private int ttlDays;

    /**
     * 매일 새벽 2시에 오래된 ProcessedEvent 삭제
     * Kafka 메시지 보존 기간(기본 7일)에 맞춰 설정
     */
    @Scheduled(cron = "0 0 2 * * *")
    @Transactional
    public void cleanupExpiredEvents() {
        Instant threshold = Instant.now().minus(Duration.ofDays(ttlDays));
        int deleted = processedEventRepository.deleteByProcessedAtBefore(threshold);
        log.info("[CLEANUP] Deleted {} expired ProcessedEvents (threshold={})", deleted, threshold);
    }
}
```

```java
// Repository에 삭제 메서드 추가
public interface ProcessedEventRepository extends JpaRepository<ProcessedEvent, String> {

    @Modifying
    @Query("DELETE FROM ProcessedEvent pe WHERE pe.processedAt < :threshold")
    int deleteByProcessedAtBefore(@Param("threshold") Instant threshold);
}
```

### 모니터링: 중복 감지 횟수 메트릭 (Micrometer)

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class EventIdempotencyChecker {

    private final ProcessedEventRepository processedEventRepository;
    private final MeterRegistry meterRegistry;

    public boolean tryAcquire(String correlationId, SagaStepType stepType) {
        if (processedEventRepository.existsByCorrelationIdAndEventType(correlationId, stepType)) {
            // 중복 감지 카운터 증가
            meterRegistry.counter("idempotency.duplicate.detected",
                    "eventType", stepType.name()).increment();
            log.debug("[IDEMPOTENCY] Duplicate: correlationId={}, stepType={}", correlationId, stepType);
            return false;
        }

        int inserted = processedEventRepository.insertIfAbsent(
                UUID.randomUUID().toString(), correlationId, stepType.name(), Instant.now());

        if (inserted == 0) {
            meterRegistry.counter("idempotency.concurrent.duplicate",
                    "eventType", stepType.name()).increment();
        } else {
            meterRegistry.counter("idempotency.acquired",
                    "eventType", stepType.name()).increment();
        }

        return inserted > 0;
    }
}
```

```yaml
# Prometheus 메트릭 노출 (application.yml)
management:
  endpoints:
    web:
      exposure:
        include: prometheus, health, info
  metrics:
    export:
      prometheus:
        enabled: true
```

Grafana 대시보드에서 `idempotency_duplicate_detected_total`이 급증하면 Consumer Rebalance나 네트워크 불안정으로 인한 중복 소비가 과도하게 발생하고 있다는 신호다.

### 장애 시나리오: ProcessedEvent DB 장애 시 동작

ProcessedEvent 테이블을 저장하는 DB가 장애가 나면 `tryAcquire()`가 예외를 던진다. 이때 `@Transactional`이 전체를 롤백하고, Spring Kafka의 `DefaultErrorHandler`가 재시도한다. DB가 복구되면 재시도가 성공한다. 이 경우 멱등성이 일시적으로 보장되지 않으므로, ProcessedEvent DB는 **주 데이터 DB와 동일한 HA 구성**을 사용해야 한다.

---

## 정리: 전략 선택 가이드

```
이벤트 성격에 따른 전략 선택
─────────────────────────────────────────────────────────────────
                    마지막 값만 중요?
                         │
              ┌──── Yes ─┘──── No ──────────────┐
              │                                   │
       DB Upsert 전략                    correlationId가 있는가?
    (상품 상태 동기화 등)                         │
                                   ┌──── Yes ────┘──── No ──────┐
                                   │                              │
                           Dedup Table 전략              Header 전략
                       (SAGA, 결제, 재고 차감)        (독립 이벤트, 알림)
                       EventIdempotencyChecker
                       preemptive acquire 패턴
```

**ch03 SAGA에서 배운 핵심 교훈**: 멱등성은 단순한 "중복 체크"가 아니라, **트랜잭션 경계와 비즈니스 의도를 함께 설계**해야 한다. Forward 리스너는 실패해도 ProcessedEvent를 커밋해야 하고, Compensation 리스너는 실패하면 ProcessedEvent도 롤백해야 한다. 이 차이를 이해하지 못하면 SAGA가 교착 상태(deadlock)에 빠지거나 보상이 무한 반복되는 버그가 생긴다.

---

## 참고 자료

- Spring for Apache Kafka Reference — Error Handling, Transactions
  - https://docs.spring.io/spring-kafka/reference/kafka/annotation-error-handling.html
- Apache Kafka Documentation — Exactly Once Semantics
  - https://kafka.apache.org/documentation/#semantics
- 기존 문서 (같은 프로젝트)
  - `03-saga-choreography.md` — ch03 SAGA 전체 구현 및 멱등성 실습
  - `08-transaction-patterns.md` — Kafka 트랜잭션, ChainedTransactionManager
  - `10-manual-commit-deep-dive.md` — ack.acknowledge() 타이밍과 offset commit 심화
- 이론 배경
  - `01-event-driven/learning/17-idempotency-patterns.md` — 멱등성 패턴 이론
