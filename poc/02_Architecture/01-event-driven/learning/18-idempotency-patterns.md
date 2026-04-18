# 18. 멱등성 패턴 (Idempotent Reader/Writer)

분산 시스템에서 메시지 중복 수신은 피할 수 없으므로, 같은 연산을 여러 번 실행해도 결과가 동일하도록 설계하는 패턴

## 학습 목표

- at-least-once 환경에서 멱등성이 필수인 이유를 이해한다
- Idempotent Writer(Producer)와 Idempotent Reader(Consumer)의 차이를 파악한다
- 3가지 멱등성 구현 전략(DB Upsert, Dedup Table, Idempotency Key)의 트레이드오프를 비교한다
- Schema-on-Read와 Schema-on-Write의 트레이드오프를 이해한다

---

## 1. 왜 멱등성이 중요한가

### 분산 시스템의 전달 보장 3단계

분산 시스템에서 메시지 전달은 세 가지 수준으로 보장할 수 있습니다.

```
at-most-once   : 메시지가 최대 1번 전달됨 (유실 가능, 중복 없음)
at-least-once  : 메시지가 최소 1번 전달됨 (유실 없음, 중복 가능)
exactly-once   : 메시지가 정확히 1번 전달됨 (유실 없음, 중복 없음)
```

`at-most-once`는 메시지가 유실될 수 있어 결제, 주문 등 중요한 도메인에서는 사용할 수 없습니다. `exactly-once`는 이상적으로 들리지만, 구현 비용이 매우 높습니다. 분산 트랜잭션(2PC)이 필요하고, 처리량이 크게 감소합니다.

그래서 실무 기본값은 **at-least-once**입니다. "적어도 한 번은 전달한다"는 보장은 ACK 기반 재전송으로 상대적으로 저렴하게 구현할 수 있습니다. 네트워크 단절, Consumer 재시작, 리밸런싱 등이 발생해도 메시지가 유실되지 않습니다.

**문제는 중복입니다.** Consumer가 메시지를 처리하고 ACK를 보내기 전에 장애가 나면, 브로커는 해당 메시지를 다시 보냅니다. Consumer는 같은 메시지를 두 번 처리하게 됩니다.

```
정상 흐름:
  Producer → Broker → Consumer → 처리 완료 → ACK → Offset Commit

장애 시:
  Producer → Broker → Consumer → 처리 완료 → [장애!]
                              ↑
                     재시작 후 같은 메시지 재수신 → 중복 처리!
```

### 멱등성이란 무엇인가

수학적 정의: f(f(x)) = f(x). 같은 함수를 여러 번 적용해도 결과가 동일합니다.

이벤트 처리에서의 정의: "같은 이벤트를 여러 번 처리해도 시스템 상태가 동일하다."

HTTP 메서드와 비교하면 직관적으로 이해할 수 있습니다. `GET /users/1`은 몇 번 호출해도 서버 상태를 바꾸지 않습니다. `PUT /users/1`은 같은 데이터로 여러 번 호출해도 결과가 동일합니다. 반면 `POST /orders`는 호출할 때마다 새 주문이 생성됩니다. 이벤트 처리도 마찬가지입니다.

```
자연적 멱등 연산:
  setStatus("COMPLETED")     → 몇 번이든 결과 동일
  updateAmount(1000)         → 몇 번이든 결과 동일
  PUT (upsert)               → 몇 번이든 결과 동일

비멱등 연산:
  addBalance(100)            → 호출마다 잔액 증가!
  insertOrder(order)         → 호출마다 새 주문 생성!
  sendEmail("확인 메일")     → 호출마다 이메일 발송!
```

비멱등 연산을 at-least-once 환경에서 그대로 사용하면 데이터 오염이 발생합니다. **멱등성은 at-least-once 전달 보장과 함께, effectively-once를 달성하는 핵심 전략입니다.**

---

## 2. Idempotent Writer (Producer 측)

### Kafka enable.idempotence=true 동작 원리

Producer 측 멱등성은 Kafka가 브로커 레벨에서 중복 메시지를 감지하고 제거하는 기능입니다. `enable.idempotence=true`를 설정하면 활성화됩니다.

동작 메커니즘은 두 가지 식별자를 사용합니다.

**Producer ID (PID)**: Producer가 처음 시작할 때 브로커가 할당하는 고유 ID입니다. 브로커는 이 ID로 메시지를 보낸 Producer를 추적합니다.

**Sequence Number**: Producer가 각 파티션별로 메시지마다 증가시키는 번호입니다. 0부터 시작하여 메시지를 보낼 때마다 1씩 증가합니다.

```
Producer (PID=42)  →  Broker
  seq=0, msg="주문생성"  →  수신, 저장
  seq=1, msg="결제요청"  →  수신, 저장
  seq=1, msg="결제요청"  →  seq=1 이미 처리됨 → 무시 (중복 제거!)
  seq=2, msg="배송시작"  →  수신, 저장
```

브로커는 파티션별로 마지막으로 수신한 시퀀스 번호를 기억합니다. 동일한 PID에서 동일한 시퀀스 번호가 오면 중복으로 판단하고 ACK는 보내되 실제로는 저장하지 않습니다.

### Epoch 펜싱: 좀비 Producer 처리

Producer가 재시작하면 새로운 PID를 받습니다. 이전 PID를 가진 "좀비 Producer"가 네트워크 지연으로 늦게 도착하는 메시지를 보낼 수 있습니다. Epoch(세대 번호)를 통해 이를 방지합니다.

```
Producer 재시작 전   : PID=42, Epoch=1  →  seq=5 전송 중 네트워크 지연
Producer 재시작 후   : PID=42, Epoch=2  →  브로커가 새 Epoch 등록
좀비 Producer 도착  : PID=42, Epoch=1  →  브로커가 거부 (낮은 Epoch)
```

### enable.idempotence 설정과 제약

```java
// application.yml
spring:
  kafka:
    producer:
      # 멱등성 활성화 (Kafka 3.0+에서 기본값 true)
      properties:
        enable.idempotence: true
        # 멱등성 활성화 시 자동으로 강제되는 설정들:
        acks: all                                    # 모든 ISR에서 확인
        max.in.flight.requests.per.connection: 5    # 최대 5 (순서 보장)
        retries: 2147483647                         # Integer.MAX_VALUE
```

**중요한 한계**: Producer 멱등성은 단일 Producer 세션 내에서만 보장됩니다. Producer가 완전히 재시작되면 새 PID를 받으므로, 재시작 전 마지막 메시지와 재시작 후 첫 메시지 사이의 중복은 감지하지 못합니다.

```java
@Configuration
public class KafkaProducerConfig {

    @Bean
    public ProducerFactory<String, Object> producerFactory() {
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        config.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);

        // 멱등성 활성화
        config.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        // acks=all, max.in.flight=5, retries=MAX_VALUE 자동 설정

        return new DefaultKafkaProducerFactory<>(config);
    }
}
```

### 브로커 레벨 MessageId 중복 제거

Kafka 외의 메시지 브로커는 브로커 자체에서 MessageId 기반 중복 제거를 지원하는 경우가 있습니다. Amazon SQS FIFO 큐는 `MessageDeduplicationId`를 기반으로 5분 윈도우 내 동일 메시지를 자동으로 버립니다. Azure Service Bus도 `MessageId` 기반 중복 감지 윈도우를 설정할 수 있습니다.

Kafka에서는 이 역할을 `enable.idempotence`가 대체합니다. 다만 Kafka의 멱등성은 단일 Producer 세션 내에서만 유효하므로, 브로커 레벨 중복 제거만으로는 Consumer 측 멱등성을 보장할 수 없다는 점은 동일합니다. SQS의 5분 윈도우도 마찬가지로, 윈도우를 넘긴 재전송에는 무력합니다. 결국 **Consumer 측 멱등성은 브로커와 무관하게 별도 구현이 필요합니다.**

### Idempotent Writer의 역할과 한계 정리

```
Producer 멱등성이 막는 것:
  ✓ 네트워크 재전송으로 인한 단일 세션 내 중복

Producer 멱등성이 막지 못하는 것:
  ✗ Producer 재시작 후 중복
  ✗ Consumer 측 중복 처리
  ✗ 애플리케이션 레벨 중복 (같은 이벤트를 다른 경로로 두 번 발행)
```

따라서 **Consumer 측 멱등성은 반드시 별도로 구현해야 합니다.** Producer 멱등성만 믿고 Consumer를 설계하면 프로덕션에서 데이터 오염이 발생합니다.

---

## 3. Idempotent Reader (Consumer 측)

### Consumer의 멱등성이 더 중요한 이유

Consumer 재시작, 리밸런싱, 네트워크 장애 등 다양한 원인으로 메시지가 중복 소비됩니다. 이는 Kafka 설계상 자연스러운 현상입니다.

```
Consumer 그룹 리밸런싱 시나리오:
  Consumer A: 파티션 0 처리 중 → offset 100 처리, 아직 commit 안 됨
  Consumer A: 리밸런싱 감지 → 파티션 0을 Consumer B에게 양도
  Consumer B: 파티션 0 인수 → committed offset = 99 → 100부터 재처리!
```

### isolation.level의 역할과 한계

Kafka Transactions 사용 시 `isolation.level=read_committed`를 설정하면 커밋된 트랜잭션의 메시지만 읽습니다. 트랜잭션이 중단(abort)된 메시지는 보이지 않습니다.

```java
spring:
  kafka:
    consumer:
      properties:
        isolation.level: read_committed
```

그러나 이것만으로는 충분하지 않습니다. Consumer 자체의 처리 로직이 멱등하지 않으면 커밋된 메시지를 두 번 처리할 때 여전히 문제가 발생합니다.

### 비즈니스 로직 자체를 멱등하게 만들어야 하는 이유

결국 핵심은 비즈니스 로직입니다. 아무리 브로커가 멱등성을 보장하더라도, Consumer의 처리 로직이 중복을 견디지 못하면 시스템은 안전하지 않습니다.

```
이상적인 Consumer 처리 흐름:

  메시지 수신
    ↓
  이미 처리한 메시지인가? → Yes → 무시하고 ACK
    ↓ No
  비즈니스 로직 실행
    ↓
  처리 완료 기록
    ↓
  ACK (Offset Commit)
```

---

## 4. 멱등성 구현 전략 3가지

### 4.1 DB Upsert (Natural Idempotency)

자연적 멱등성을 활용하는 가장 단순한 방법입니다. 이벤트의 고유 식별자를 DB의 Primary Key 또는 Unique Key로 활용하고, INSERT 시 중복이면 UPDATE하는 방식입니다.

```sql
-- PostgreSQL: INSERT ON CONFLICT (Upsert)
INSERT INTO orders (order_id, user_id, status, amount, updated_at)
VALUES (:orderId, :userId, :status, :amount, NOW())
ON CONFLICT (order_id)
DO UPDATE SET
    status = EXCLUDED.status,
    amount = EXCLUDED.amount,
    updated_at = EXCLUDED.updated_at;
```

```java
// Spring Data JPA: save()는 이미 upsert 의미 (PK 있으면 update)
@Transactional
public void handleOrderCreated(OrderCreatedEvent event) {
    Order order = Order.builder()
        .orderId(event.getOrderId())   // PK로 사용
        .userId(event.getUserId())
        .status(OrderStatus.CREATED)
        .amount(event.getAmount())
        .build();

    orderRepository.save(order);  // 동일 orderId 있으면 UPDATE
}
```

**언제 적합한가**: 이벤트가 엔티티의 전체 상태를 나타낼 때, 즉 "주문 상태가 이렇게 변경되었다"는 SET 의미일 때 자연스럽게 멱등합니다.

**한계**: 잔액 증가처럼 누적(accumulation) 연산에는 적용할 수 없습니다. `addBalance(100)`을 upsert로 만들면 의미가 왜곡됩니다.

```
Upsert가 적합한 경우:        Upsert가 부적합한 경우:
  setStatus(COMPLETED)         addBalance(100)
  updateShippingAddress(...)   appendToList(item)
  setLastLoginTime(now)        incrementViewCount()
```

### 4.2 Dedup Table (Processed Events Pattern)

처리한 이벤트 ID를 별도 테이블에 기록하는 방법입니다. 비즈니스 로직을 변경하지 않고 멱등성을 추가할 수 있어 범용적입니다.

#### check-then-act의 함정

직관적인 첫 번째 시도는 "처리 전에 확인하고, 처리 후에 기록"하는 방식입니다.

```java
// 위험한 구현: check-then-act 패턴
@Transactional
public void handlePaymentCompleted(PaymentCompletedEvent event) {
    // Step 1: 이미 처리했는가?
    if (processedEventRepository.existsById(event.getEventId())) {
        return; // 중복이면 스킵
    }

    // Step 2: 비즈니스 로직 실행
    balanceService.addBalance(event.getUserId(), event.getAmount());

    // Step 3: 처리 완료 기록
    processedEventRepository.save(new ProcessedEvent(event.getEventId()));
}
// 문제: Step 1과 Step 3 사이에 다른 스레드/인스턴스가 같은 이벤트를 처리하면?
// → 동시에 두 인스턴스가 existsById=false → 동시에 addBalance 실행!
```

Step 1(확인)과 Step 3(기록) 사이에 타임 윈도우가 존재합니다. 여기서 다른 Consumer 인스턴스가 동일 메시지를 처리하면 중복이 발생합니다.

#### preemptive acquire 패턴

"먼저 선점하고, 성공하면 처리한다"는 방식입니다. 처리 기록을 INSERT하는 것 자체를 락으로 사용합니다.

```sql
-- Unique Constraint로 선점 시도
CREATE TABLE processed_events (
    id          BIGSERIAL PRIMARY KEY,
    event_id    VARCHAR(255) NOT NULL,
    event_type  VARCHAR(100) NOT NULL,
    processed_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT uq_processed_events UNIQUE (event_id, event_type)
);
```

```java
// ProcessedEventRepository.java
public interface ProcessedEventRepository extends JpaRepository<ProcessedEvent, Long> {

    // INSERT ... WHERE NOT EXISTS: 네이티브 쿼리로 원자적 선점
    @Modifying
    @Query(value = """
        INSERT INTO processed_events (event_id, event_type, processed_at)
        SELECT :eventId, :eventType, NOW()
        WHERE NOT EXISTS (
            SELECT 1 FROM processed_events
            WHERE event_id = :eventId AND event_type = :eventType
        )
        """, nativeQuery = true)
    int tryAcquire(
        @Param("eventId") String eventId,
        @Param("eventType") String eventType
    );
}
```

```java
// PaymentEventConsumer.java
@Component
public class PaymentEventConsumer {

    private final ProcessedEventRepository processedEventRepo;
    private final BalanceService balanceService;

    @KafkaListener(topics = "payment-completed")
    @Transactional
    public void handlePaymentCompleted(PaymentCompletedEvent event) {
        // 1. 원자적 선점: 내가 먼저 INSERT에 성공해야만 처리
        int acquired = processedEventRepo.tryAcquire(
            event.getEventId(),
            "PAYMENT_COMPLETED"
        );

        if (acquired == 0) {
            // 다른 인스턴스가 이미 처리했거나 처리 중
            log.info("이미 처리된 이벤트 스킵: {}", event.getEventId());
            return;
        }

        // 2. 선점 성공 → 비즈니스 로직 실행
        balanceService.addBalance(event.getUserId(), event.getAmount());
        log.info("잔액 추가 완료: userId={}, amount={}", event.getUserId(), event.getAmount());
    }
}
```

**왜 INSERT...WHERE NOT EXISTS인가**: JPA의 `saveAndFlush()`를 try-catch로 감싸는 방식은 Hibernate 세션을 오염시킵니다. `DataIntegrityViolationException`이 발생하면 해당 세션은 rollback-only 상태로 전환되어 이후 모든 DB 작업이 실패합니다. 네이티브 쿼리는 예외 없이 삽입 성공/실패를 0/1로 반환하므로 세션 오염이 없습니다.

```
saveAndFlush + catch 방식 (위험):
  try {
    processedEventRepo.saveAndFlush(event)  // UNIQUE 위반 시 예외 발생
  } catch (DataIntegrityViolationException e) {
    // 예외 잡았지만...
    // Hibernate 세션이 이미 rollback-only!
    // 이후 balanceService.addBalance() → 트랜잭션 커밋 실패!
  }

INSERT...WHERE NOT EXISTS 방식 (안전):
  int result = repo.tryAcquire(eventId, type)  // 예외 없음, 0 또는 1 반환
  if (result == 0) return  // 깨끗하게 종료
  // 세션 상태 오염 없음, 이후 로직 안전하게 실행
```

#### (correlationId, eventType) 복합 키로 SAGA 멱등성 구현

SAGA 패턴에서는 하나의 트랜잭션 ID(correlationId)로 여러 단계(eventType)를 처리합니다. correlationId만으로는 단계를 구분할 수 없으므로 복합 키가 필수입니다.

```
주문 SAGA 흐름 (correlationId = "order-001"):
  Step 1: ORDER_CREATED      (correlationId=order-001, eventType=ORDER_CREATED)
  Step 2: PAYMENT_COMPLETED  (correlationId=order-001, eventType=PAYMENT_COMPLETED)
  Step 3: DELIVERY_STARTED   (correlationId=order-001, eventType=DELIVERY_STARTED)

correlationId만 사용하면:
  Step 2 처리 후 processed_events에 "order-001" 기록
  Step 3 처리 시 "order-001" 이미 있음 → 스킵! (잘못된 동작)

(correlationId, eventType) 복합 키 사용:
  Step 2 처리 후: ("order-001", "PAYMENT_COMPLETED") 기록
  Step 3 처리 시: ("order-001", "DELIVERY_STARTED") 없음 → 정상 처리
```

#### (messageId, consumerName) 복합 키로 다중 Consumer 멱등성 구현

SAGA에서는 하나의 correlationId에 대해 여러 단계(eventType)를 구분했습니다. 비슷하지만 다른 시나리오가 있습니다. **같은 메시지를 여러 Consumer가 독립적으로 처리해야 하는 경우**입니다.

예를 들어 `OrderCreated` 이벤트를 재고 서비스, 알림 서비스, 분석 서비스가 각각 구독한다고 가정합니다. `event_id`만으로 dedup하면, 재고 서비스가 먼저 처리 기록을 남긴 뒤 알림 서비스가 같은 `event_id`를 보고 스킵하는 문제가 발생합니다.

```
OrderCreated (event_id = "evt-001")

event_id만 사용하면:
  재고 서비스 처리 → processed_events에 "evt-001" 기록
  알림 서비스 처리 → "evt-001" 이미 있음 → 스킵! (잘못된 동작)

(messageId, consumerName) 복합 키 사용:
  재고 서비스 처리 → ("evt-001", "InventoryConsumer") 기록
  알림 서비스 처리 → ("evt-001", "NotificationConsumer") 없음 → 정상 처리
```

스키마는 기존 `processed_events` 테이블에 `consumer_name` 컬럼을 추가하면 됩니다.

```sql
CREATE TABLE processed_messages (
    id              BIGSERIAL       PRIMARY KEY,
    message_id      VARCHAR(255)    NOT NULL,
    consumer_name   VARCHAR(100)    NOT NULL,
    processed_at    TIMESTAMP       NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_message_consumer UNIQUE (message_id, consumer_name)
);

CREATE INDEX idx_processed_messages_ttl ON processed_messages (processed_at);
```

```java
@Repository
public interface ProcessedMessageRepository extends JpaRepository<ProcessedMessage, Long> {

    @Modifying
    @Query(value = "INSERT INTO processed_messages (message_id, consumer_name, processed_at) "
            + "VALUES (:messageId, :consumerName, NOW()) "
            + "ON CONFLICT (message_id, consumer_name) DO NOTHING"
            , nativeQuery = true)
    int tryAcquire(
            @Param("messageId") String messageId
            , @Param("consumerName") String consumerName
    );
}
```

**사용 시점 비교:**

| 복합 키 | 시나리오 | 예시 |
|---------|---------|------|
| `(correlationId, eventType)` | 하나의 SAGA에서 여러 단계를 구분 | 주문 생성 → 결제 → 배송 |
| `(messageId, consumerName)` | 하나의 메시지를 여러 서비스가 독립 처리 | 주문 이벤트 → 재고, 알림, 분석 |

두 패턴은 배타적이지 않습니다. SAGA 오케스트레이터 내부에서는 `(correlationId, eventType)`을 사용하고, 이벤트를 구독하는 독립 서비스 간에는 `(messageId, consumerName)`을 사용할 수 있습니다.

### 4.3 Idempotency Key 헤더

Producer가 각 이벤트에 고유 키를 Kafka Record Header에 삽입하고, Consumer가 이 헤더를 기반으로 중복을 판단합니다. 비즈니스 로직과 중복 제거 로직을 명확히 분리할 수 있습니다.

```java
// Producer 측: 헤더에 Idempotency Key 삽입
@Service
public class OrderEventProducer {

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public void publishOrderCreated(Order order) {
        String idempotencyKey = UUID.randomUUID().toString();

        ProducerRecord<String, OrderEvent> record = new ProducerRecord<>(
            "order-events",
            order.getOrderId(),
            OrderCreatedEvent.from(order)
        );

        // Idempotency Key를 헤더에 추가
        record.headers().add(
            "idempotency-key",
            idempotencyKey.getBytes(StandardCharsets.UTF_8)
        );

        kafkaTemplate.send(record);
    }
}
```

```java
// Consumer 측: 헤더에서 키 추출 → Dedup 확인
@Component
public class OrderEventConsumer {

    private final ProcessedEventRepository processedEventRepo;

    @KafkaListener(topics = "order-events")
    @Transactional
    public void handleOrderCreated(
        OrderCreatedEvent event,
        @Header(KafkaHeaders.RECEIVED_TOPIC) String topic,
        ConsumerRecord<String, OrderCreatedEvent> record
    ) {
        // 헤더에서 Idempotency Key 추출
        Header idempotencyHeader = record.headers().lastHeader("idempotency-key");
        if (idempotencyHeader == null) {
            // 키 없음 → fallback으로 이벤트 내 ID 사용
            processWithDedup(event.getEventId(), "ORDER_CREATED", event);
            return;
        }

        String idempotencyKey = new String(idempotencyHeader.value(), StandardCharsets.UTF_8);
        processWithDedup(idempotencyKey, "ORDER_CREATED", event);
    }

    private void processWithDedup(String key, String type, OrderCreatedEvent event) {
        int acquired = processedEventRepo.tryAcquire(key, type);
        if (acquired == 0) return;

        // 비즈니스 로직
        orderService.createOrder(event);
    }
}
```

**장점**: 비즈니스 이벤트 스키마를 변경하지 않고 멱등성 키를 외부화할 수 있습니다. AOP나 인터셉터로 범용 중복 제거 레이어를 구현할 수도 있습니다.

**단점**: Producer와 Consumer가 헤더 규약을 공유해야 합니다. 헤더가 없는 외부 Producer 이벤트에는 적용하기 어렵습니다.

#### 비결정적 사이드이펙트: 외부 API 호출의 멱등성

지금까지의 전략은 모두 **DB 트랜잭션 경계 안에서** 처리 기록과 비즈니스 로직을 원자적으로 묶는 방식이었습니다. 그런데 이메일 발송, 결제 API 호출, SMS 전송처럼 **DB 트랜잭션 밖의 외부 호출**이 포함되면 상황이 달라집니다. 외부 API 호출은 롤백할 수 없기 때문입니다.

```
문제 시나리오:
  1. tryAcquire 성공 (DB에 처리 기록)
  2. 비즈니스 로직 실행
  3. 이메일 API 호출 → 성공 (이메일 발송됨)
  4. DB 커밋 전 장애 발생 → 트랜잭션 롤백
  5. 재시도 → tryAcquire 성공 (롤백되어 기록 없음)
  6. 이메일 API 호출 → 또 성공 → 이메일 2통 발송!
```

이 문제에 대한 두 가지 전략이 있습니다.

**전략 1: 외부 API의 Idempotency-Key 활용**

Stripe, SendGrid, PayPal 등 주요 외부 API는 요청 헤더에 `Idempotency-Key`를 받아 동일 키의 재요청을 무시합니다. 이벤트의 고유 ID를 그대로 전달하면 외부 API 측에서 중복을 차단합니다.

```java
// 결제 API 호출 시 이벤트 ID를 Idempotency-Key로 전달
public void processPayment(String eventId, PaymentRequest request) {
    int acquired = processedEventRepo.tryAcquire(eventId, "PAYMENT_REQUESTED");
    if (acquired == 0) return;

    paymentClient.charge(
            request
            , Map.of("Idempotency-Key", eventId)  // 외부 API에 키 전달
    );
}
```

이 방식은 외부 API가 멱등성 키를 지원해야만 사용할 수 있습니다. 지원하지 않는 API라면 전략 2를 사용합니다.

**전략 2: 로컬 의도 저장 (Pending Actions 패턴)**

외부 호출을 즉시 실행하지 않고, **"이 작업을 해야 한다"는 의도**를 DB에 먼저 저장합니다. 별도의 발송 프로세스가 주기적으로 pending 레코드를 읽어 외부 API를 호출하고, 성공하면 상태를 업데이트합니다.

```
개선된 흐름:
  1. tryAcquire 성공
  2. 비즈니스 로직 + pending_actions에 INSERT (같은 트랜잭션)
  3. DB 커밋 → 원자적으로 완료
  4. [별도 프로세스] pending_actions 폴링 → 이메일 발송 → status = SENT
```

이 패턴은 Transactional Outbox와 동일한 원리입니다. 외부 호출의 신뢰성을 DB 트랜잭션의 원자성으로 보장하는 것입니다.

**판단 기준: "반복 실행의 실제 피해가 있는가?"**

모든 외부 호출에 이런 복잡한 전략이 필요한 것은 아닙니다. 캐시 무효화 API 호출은 두 번 해도 피해가 없습니다. 반면 결제 API는 두 번 호출하면 이중 과금이 발생합니다. 실제 피해의 크기에 따라 전략의 복잡도를 선택합니다.

---

## 5. Exactly-Once Semantics (EOS)

### Kafka Transactions 메커니즘

Kafka Transactions는 Producer의 메시지 발행과 Consumer의 Offset Commit을 하나의 원자적 단위로 묶습니다.

```java
@Configuration
public class KafkaTransactionConfig {

    @Bean
    public ProducerFactory<String, Object> transactionalProducerFactory() {
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        config.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);

        // Transactional ID: 재시작 후에도 동일 ID 사용 → EOS 보장
        config.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "order-service-producer-1");

        DefaultKafkaProducerFactory<String, Object> factory =
            new DefaultKafkaProducerFactory<>(config);
        factory.setTransactionIdPrefix("order-svc-");
        return factory;
    }
}
```

```java
// Consume-Transform-Produce 패턴 (EOS)
@KafkaListener(topics = "order-events")
public void processAndForward(OrderEvent event, Acknowledgment ack) {
    kafkaTemplate.executeInTransaction(operations -> {
        // 1. 비즈니스 로직 실행
        ProcessedResult result = orderService.process(event);

        // 2. 결과 이벤트 발행
        operations.send("processed-orders", result.toEvent());

        // 3. Offset Commit도 트랜잭션에 포함
        Map<TopicPartition, OffsetAndMetadata> offsets = /* 현재 offset */;
        operations.sendOffsetsToTransaction(offsets, "order-consumer-group");

        return null;
    });
}
```

Consumer는 `isolation.level=read_committed`로 커밋된 트랜잭션의 메시지만 읽습니다.

### EOS의 비용

EOS는 이론적으로 완벽하지만 실제 비용이 큽니다.

```
EOS 비용:
  - 트랜잭션 코디네이터 통신 오버헤드
  - 처리량(throughput) 20-40% 감소
  - 지연(latency) 증가
  - 브로커 리소스 추가 사용
  - 복잡한 에러 핸들링

실무에서 EOS가 필요한 경우:
  ✓ 금융 정산 (정확한 이체 금액 필수)
  ✓ 재고 차감 (oversell 절대 불가)
  ✓ 법적 컴플라이언스 (이중 처리 증거 남기면 안 됨)

at-least-once + 멱등성으로 충분한 경우:
  ✓ 이벤트 집계 (약간의 오차 허용)
  ✓ 알림 발송 (중복 발송이 치명적이지 않음)
  ✓ 로그/감사 이벤트 (중복보다 유실이 더 위험)
  ✓ 캐시 무효화 (멱등하므로 자연 해결)
```

기존 `12-transactions.md`에서 Kafka Transactions의 상세 구현을 참고하세요.

---

## 6. 기존 실습과 연계: ch03 SAGA의 preemptive acquire

### ch03에서 구현한 멱등성 패턴 복습

ch03 Choreography SAGA 실습에서 구현한 멱등성 패턴을 이론적으로 정리합니다.

```
ch03 SAGA 아키텍처:

  OrderService                PaymentService              DeliveryService
      │                           │                           │
      │──ORDER_CREATED──────────→ │                           │
      │                           │ tryAcquire(id, PAYMENT)   │
      │                           │ addBalance()              │
      │                           │──PAYMENT_COMPLETED──────→ │
      │                           │                           │ tryAcquire(id, DELIVERY)
      │                           │                           │ startDelivery()
      │                           │                           │──DELIVERY_STARTED────→
```

각 서비스는 이벤트를 받을 때 `(correlationId, eventType)` 복합 키로 선점을 시도합니다. 선점에 실패하면 이미 처리된 이벤트이므로 안전하게 스킵합니다.

### ProcessedEvent 테이블 이중 활용

ch03의 핵심 설계 아이디어는 `ProcessedEvent` 테이블 하나로 두 가지 역할을 수행하는 것입니다.

```
ProcessedEvent 테이블:
  ┌─────────────────┬──────────────────────┬──────────┬─────────────────────┐
  │ event_id        │ event_type           │ status   │ processed_at        │
  ├─────────────────┼──────────────────────┼──────────┼─────────────────────┤
  │ order-001       │ ORDER_CREATED        │ SUCCESS  │ 2026-01-01 10:00:00 │
  │ order-001       │ PAYMENT_COMPLETED    │ SUCCESS  │ 2026-01-01 10:00:05 │
  │ order-001       │ DELIVERY_FAILED      │ FAILED   │ 2026-01-01 10:00:10 │
  │ order-001       │ ORDER_CANCELLED      │ SUCCESS  │ 2026-01-01 10:00:15 │
  └─────────────────┴──────────────────────┴──────────┴─────────────────────┘

역할 1: 멱등성 체크
  → tryAcquire(eventId, eventType) 선점으로 중복 처리 방지

역할 2: SAGA 상태 추적
  → event_type 시퀀스로 현재 SAGA가 어느 단계에 있는지 파악
  → 장애 분석 시 전체 흐름을 이 테이블 하나로 재현 가능
```

별도의 SAGA 상태 테이블 없이도 ProcessedEvent의 이벤트 이력으로 SAGA 상태를 추적할 수 있습니다. 추가 테이블 없이 두 가지 기능을 얻는 효율적인 설계입니다.

### Forward 리스너 vs Compensation 리스너의 멱등성 차이

SAGA에서 Forward(정방향)과 Compensation(보상)의 멱등성 처리 방식이 다릅니다. 이 차이는 "재시도 가능성"의 차이입니다.

```
Forward 리스너 (정방향 처리):
  성공 시: 다음 단계 이벤트 발행 → 정상 완료
  실패 시: 실패 이벤트 발행 → Compensation 트리거
           → catch 블록에서 이벤트 발행 후 정상 return
           → ProcessedEvent는 커밋됨 (재시도 시 스킵)

  이유: 실패를 감지했으므로 보상 트랜잭션으로 처리한다.
        이 단계를 재시도하면 같은 실패가 반복될 뿐이다.
```

```java
// Forward 리스너: 실패 시 보상 이벤트 발행 후 return
@KafkaListener(topics = "payment-requested")
@Transactional
public void handlePaymentRequested(PaymentRequestedEvent event) {
    int acquired = processedEventRepo.tryAcquire(
        event.getCorrelationId(), "PAYMENT_REQUESTED");
    if (acquired == 0) return;  // 멱등: 이미 처리됨

    try {
        paymentService.processPayment(event);
        kafkaTemplate.send("payment-completed", new PaymentCompletedEvent(event));
    } catch (InsufficientBalanceException e) {
        // 실패 이벤트 발행 → 보상 트랜잭션 트리거
        kafkaTemplate.send("payment-failed", new PaymentFailedEvent(event, e.getMessage()));
        // 예외를 re-throw하지 않음 → ProcessedEvent 커밋됨 → 재시도 시 스킵
    }
}
```

```
Compensation 리스너 (보상 처리):
  성공 시: 이전 단계 롤백 완료
  실패 시: 예외 throw → @Transactional 롤백
           → ProcessedEvent도 롤백 → 재시도 가능!

  이유: 보상 트랜잭션은 반드시 성공해야 한다.
        실패하면 시스템이 불일치 상태에 빠진다.
        따라서 실패 시 재시도할 수 있도록 ProcessedEvent도 롤백해야 한다.
```

```java
// Compensation 리스너: 실패 시 예외 throw → ProcessedEvent 롤백
@KafkaListener(topics = "payment-failed")
@Transactional
public void handlePaymentFailed(PaymentFailedEvent event) {
    int acquired = processedEventRepo.tryAcquire(
        event.getCorrelationId(), "PAYMENT_FAILED");
    if (acquired == 0) return;  // 멱등: 이미 처리됨

    try {
        orderService.cancelOrder(event.getCorrelationId());
    } catch (Exception e) {
        // 예외 throw → 트랜잭션 롤백 → ProcessedEvent도 롤백
        // 다음 재시도 시 tryAcquire 다시 성공 → 보상 재시도 가능
        throw new CompensationFailedException("주문 취소 실패", e);
    }
}
```

```
Forward vs Compensation 멱등성 비교:

           │ 성공 시              │ 실패 시
──────────┼──────────────────────┼───────────────────────────
Forward   │ ProcessedEvent 커밋  │ 실패 이벤트 발행 후 return
          │ 재시도 시 스킵       │ → ProcessedEvent 커밋
          │                      │ → 재시도 시 스킵 (정상)
──────────┼──────────────────────┼───────────────────────────
Compensat │ ProcessedEvent 커밋  │ 예외 throw → 롤백
  -ion    │ 재시도 시 스킵       │ → ProcessedEvent 롤백
          │                      │ → 재시도 시 재처리 (필수)
```

---

## 7. Schema-on-Read

### Schema-on-Write와 Schema-on-Read의 개념

데이터를 어느 시점에 스키마를 강제하느냐에 따라 두 가지 방식이 나뉩니다.

**Schema-on-Write (쓰기 시점 강제)**: 데이터를 저장하기 전에 스키마 유효성을 검사합니다. Schema Registry가 대표적인 예입니다. 유효하지 않은 데이터는 처음부터 거부됩니다.

```
Schema-on-Write 흐름:
  Producer
    → Schema Registry에 스키마 검증 요청
    → 유효하면 직렬화(Avro) → Kafka
    → 유효하지 않으면 예외 발생 (데이터가 Kafka에 도달하지 않음)

Consumer
    → Kafka에서 수신
    → Schema Registry에서 스키마 조회
    → 역직렬화 → 타입 안전한 객체
```

**Schema-on-Read (읽기 시점 해석)**: 데이터를 그대로 저장하고, 읽을 때 스키마를 적용합니다. JSON이나 데이터 레이크 환경에서 많이 사용됩니다.

```
Schema-on-Read 흐름:
  Producer
    → 검증 없이 JSON/바이트로 Kafka에 저장

Consumer
    → Kafka에서 수신
    → 읽기 시점에 스키마 해석 시도
    → 스키마가 맞지 않으면 오류 (이때 발견)
```

### Schema Registry가 Schema-on-Write를 강제하는 이유

Schema Registry는 Avro, Protobuf, JSON Schema를 쓰기 시점에 검증합니다. 이 설계에는 중요한 이유가 있습니다.

분산 시스템에서 Producer와 Consumer는 독립적으로 배포됩니다. Schema-on-Read를 사용하면 스키마 불일치를 Consumer가 메시지를 읽는 시점에야 발견합니다. 이미 수천 개의 잘못된 메시지가 Kafka에 쌓인 후입니다. 롤백이 불가능하고, Consumer 장애로 이어집니다.

Schema-on-Write는 "나쁜 데이터를 처음부터 막는다"는 방어적 설계입니다. 잘못된 스키마는 Producer가 발행하는 순간 거부되므로 파이프라인 전체가 보호됩니다.

### specific.avro.reader 옵션

```java
// application.yml
spring:
  kafka:
    consumer:
      properties:
        # true: SpecificRecord (생성된 Java 클래스)
        # false: GenericRecord (Map 형태, 런타임에 필드 접근)
        specific.avro.reader: true
```

```java
// specific.avro.reader=true → 타입 안전한 클래스 사용
@KafkaListener(topics = "order-events")
public void handleWithSpecific(OrderCreatedEvent event) {
    // 컴파일 타임에 타입 체크
    String orderId = event.getOrderId();  // String, 타입 보장
    Long amount = event.getAmount();       // Long, 타입 보장
}

// specific.avro.reader=false → GenericRecord 사용
@KafkaListener(topics = "order-events")
public void handleWithGeneric(GenericRecord record) {
    // 런타임에 필드 접근, 타입 안전성 없음
    Object orderId = record.get("order_id");  // Object로 반환
    Object amount = record.get("amount");      // 타입 캐스팅 필요
}
```

### Schema-on-Read가 적합한 경우

Schema-on-Read가 무조건 나쁜 것은 아닙니다. 적합한 상황이 있습니다.

**데이터 레이크**: S3나 HDFS에 저장하는 raw 이벤트는 미래에 어떻게 쿼리할지 모릅니다. 쓰기 시점에 스키마를 강제하면 나중에 필요한 필드가 없을 수 있습니다. 파케이(Parquet)나 ORC 포맷으로 저장하고 읽을 때 스키마를 지정하는 방식이 유연합니다.

**탐색적 분석**: 데이터 사이언티스트가 raw 이벤트를 분석할 때, 스키마가 고정되어 있으면 새로운 패턴을 발견하기 어렵습니다.

**레거시 시스템 연동**: 스키마를 제어할 수 없는 외부 시스템의 이벤트를 수신할 때는 읽기 시점에 필요한 필드만 추출하는 Schema-on-Read가 더 현실적입니다.

### 트레이드오프 비교표

| 항목 | Schema-on-Write | Schema-on-Read |
|------|----------------|----------------|
| **오류 감지 시점** | 쓰기 시점 (즉시) | 읽기 시점 (지연) |
| **데이터 품질** | 높음 (나쁜 데이터 차단) | 낮음 (나쁜 데이터 누적) |
| **유연성** | 낮음 (스키마 변경 비용) | 높음 (사후 해석 가능) |
| **Consumer 복잡도** | 낮음 (타입 보장) | 높음 (방어적 파싱) |
| **적합한 환경** | MSA 이벤트 파이프라인 | 데이터 레이크, 분석 |
| **도구** | Schema Registry + Avro | Spark, Athena, Presto |

---

## 8. at-least-once + 멱등성 = effectively-once

### effectively-once란 무엇인가

`exactly-once`는 "메시지가 정확히 한 번 전달된다"는 보장입니다. 하지만 비용이 높습니다. `effectively-once`는 "메시지가 여러 번 전달될 수 있지만, 그 효과(effect)는 정확히 한 번만 발생한다"는 보장입니다.

```
exactly-once    : 메시지 중복 자체를 방지 (인프라 레벨)
effectively-once: 메시지는 중복될 수 있지만 처리 결과는 동일 (애플리케이션 레벨)

at-least-once (전달) + 멱등성 (처리) = effectively-once (결과)
```

이 조합이 실무에서 훨씬 자주 사용됩니다. 인프라는 at-least-once로 단순하게 유지하고, 애플리케이션 레벨에서 멱등성을 보장하는 것이 더 유연하고 성능도 좋습니다.

### 언제 EOS, 언제 멱등성만으로 충분한가

```
결정 트리 (Decision Tree)

시작: 이벤트 중복 처리 시 어떤 문제가 발생하는가?

  ┌─ 데이터 오류가 발생하는가?
  │
  │   ┌─ Yes ─→ 자연적 멱등 연산인가?
  │   │              │
  │   │              ├─ Yes ─→ DB Upsert만으로 충분
  │   │              │          (setStatus, updateAddress 등)
  │   │              │
  │   │              └─ No ─→ 누적/카운트 연산인가?
  │   │                          │
  │   │                          ├─ Yes ─→ Dedup Table 필요
  │   │                          │          (preemptive acquire)
  │   │                          │
  │   │                          └─ 금융/법적 정확성 필수?
  │   │                                  │
  │   │                                  ├─ Yes ─→ Kafka Transactions (EOS)
  │   │                                  │
  │   │                                  └─ No ─→ Dedup Table + 모니터링
  │   │
  │   └─ No ─→ 이미 자연적으로 멱등함
  │               (로그 기록, 캐시 무효화, 읽기 전용)
  │
  └─ 판단 기준: "같은 이벤트를 100번 처리해도 결과가 동일한가?"
```

### 실전 가이드라인

```
도메인별 권장 전략:

  결제/정산
    → Kafka Transactions (EOS) 또는 Dedup Table + DB 트랜잭션
    → 이유: 금융 오류는 법적 책임으로 이어짐

  주문 생성/취소
    → Dedup Table (preemptive acquire)
    → 이유: 중복 주문은 비즈니스 오류, 복구 비용 높음

  재고 차감
    → Dedup Table + 낙관적 락
    → 이유: 차감 연산은 비멱등, 과다 차감은 재고 오류

  알림 발송
    → DB Upsert (notification_id PK)
    → 이유: 중복 알림은 사용자 불편이지만 치명적이지 않음

  이벤트 집계/분석
    → at-least-once만으로 충분
    → 이유: 약간의 카운트 오차는 허용 가능

  캐시 무효화
    → 아무 전략 불필요
    → 이유: 자연적으로 멱등 (캐시 삭제를 두 번 해도 결과 동일)
```

### 멱등성 패턴이 불필요한 경우

모든 Consumer에 Dedup Table을 적용하는 것은 과잉 설계입니다. 다음 경우에는 별도의 멱등성 패턴 없이도 안전합니다.

**자연적 멱등 연산**: 프로젝션 업데이트(`UPDATE view SET total = 100`), 상태 플래그 설정(`UPDATE order SET status = 'SHIPPED'`), 캐시 갱신/무효화는 몇 번 실행해도 결과가 동일합니다. 이런 연산에 Dedup Table을 추가하면 불필요한 DB 쿼리만 늘어납니다.

**전제 조건 체크로 충분한 경우**: 비즈니스 로직 자체에 상태 검증이 포함되어 있으면 중복 처리가 자연스럽게 차단됩니다. 예를 들어 `if (order.getStatus() != PENDING) return;` 같은 가드 절은 이미 처리된 주문의 재처리를 막습니다. 이 경우 Dedup Table은 동일한 보호를 중복으로 제공할 뿐입니다.

**집계/분석 파이프라인**: 약간의 카운트 오차가 허용되는 분석 시스템에서는 at-least-once만으로 충분합니다. Dedup의 운영 비용(테이블 관리, TTL, 인덱스)이 중복 허용의 비용보다 클 수 있습니다.

핵심 판단 기준은 **"같은 이벤트를 두 번 처리했을 때 실제 피해가 무엇인가?"**입니다. 피해가 없거나 무시할 수 있는 수준이면 멱등성 패턴을 적용하지 않는 것이 올바른 설계입니다. 위의 도메인별 전략 선택 가이드에서 "아무 전략 불필요"로 분류한 캐시 무효화가 대표적인 예입니다.

### 체크리스트: 멱등성 설계 시 확인 사항

```
□ 1. 이 Consumer의 처리가 멱등한가?
      → "같은 이벤트를 두 번 처리하면?" 시나리오 작성

□ 2. 이벤트마다 고유 식별자가 있는가?
      → event_id, correlation_id, message_id 중 하나 필수

□ 3. Dedup 테이블의 키 설계가 올바른가?
      → SAGA면 (correlationId, eventType) 복합 키 필수
      → 단순 이벤트면 event_id 단일 키로 충분

□ 4. preemptive acquire를 사용하는가?
      → check-then-act 패턴 사용 시 동시성 위험 검토

□ 5. 트랜잭션 경계가 올바른가?
      → tryAcquire + 비즈니스 로직이 같은 트랜잭션 안에 있는가?
      → 트랜잭션 롤백 시 tryAcquire도 함께 롤백되는가?

□ 6. Forward/Compensation 패턴을 구분했는가?
      → Forward 실패: 보상 이벤트 발행 후 return (ProcessedEvent 커밋)
      → Compensation 실패: 예외 throw (ProcessedEvent 롤백 → 재시도)

□ 7. 테스트 시나리오에 중복 메시지가 포함되어 있는가?
      → "같은 이벤트를 두 번 publish했을 때" 테스트 케이스 필수

□ 8. Dedup 테이블 정리(TTL) 전략이 있는가?
      → processed_events가 무한 증가하지 않도록 주기적 삭제
      → 예: 90일 이상 지난 레코드 삭제 (SAGA 완료 시점 기준)
```

---

## 9. 멱등성 패턴 전체 비교 및 선택 가이드

### 전략별 핵심 특성 비교

| 전략 | 구현 난이도 | 성능 영향 | 동시성 안전 | 적합한 연산 |
|------|-----------|----------|------------|------------|
| **DB Upsert** | 낮음 | 없음 | 안전 (DB 락) | SET/UPDATE 계열 |
| **Dedup Table** | 중간 | 약간 (쿼리 1회 추가) | 안전 (preemptive acquire) | 모든 연산 |
| **Idempotency Key 헤더** | 중간 | 약간 | 안전 (Dedup Table 결합) | 비즈니스 로직 분리 필요 시 |
| **Kafka Transactions (EOS)** | 높음 | 20-40% 감소 | 안전 | 금융/법적 정확성 필수 |

### Dedup Table 스키마 설계 예시 (전체)

운영에서 사용할 수 있는 완전한 ProcessedEvent 테이블 설계입니다.

```sql
-- processed_events: 멱등성 + SAGA 상태 추적 이중 역할
CREATE TABLE processed_events (
    id              BIGSERIAL       PRIMARY KEY,
    event_id        VARCHAR(255)    NOT NULL,       -- 이벤트 고유 ID
    event_type      VARCHAR(100)    NOT NULL,       -- 이벤트 타입 (SAGA 단계)
    correlation_id  VARCHAR(255),                   -- SAGA 트랜잭션 ID
    service_name    VARCHAR(100),                   -- 처리한 서비스
    status          VARCHAR(20)     NOT NULL        -- SUCCESS / FAILED
                    DEFAULT 'SUCCESS',
    error_message   TEXT,                           -- 실패 시 원인
    processed_at    TIMESTAMP       NOT NULL
                    DEFAULT NOW(),

    -- 멱등성 보장: (event_id, event_type) 중복 불허
    CONSTRAINT uq_processed_events UNIQUE (event_id, event_type)
);

-- 조회 성능: correlation_id로 SAGA 전체 이력 조회
CREATE INDEX idx_processed_events_correlation
    ON processed_events (correlation_id, processed_at);

-- TTL 지원: processed_at 기준 파티셔닝 또는 주기 삭제
CREATE INDEX idx_processed_events_processed_at
    ON processed_events (processed_at);
```

```java
// ProcessedEvent.java (JPA Entity)
@Entity
@Table(
    name = "processed_events",
    uniqueConstraints = @UniqueConstraint(
        name = "uq_processed_events",
        columnNames = {"event_id", "event_type"}
    )
)
public class ProcessedEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "event_id", nullable = false)
    private String eventId;

    @Column(name = "event_type", nullable = false)
    private String eventType;

    @Column(name = "correlation_id")
    private String correlationId;

    @Column(name = "service_name")
    private String serviceName;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ProcessingStatus status = ProcessingStatus.SUCCESS;

    @Column(name = "error_message")
    private String errorMessage;

    @Column(name = "processed_at")
    private LocalDateTime processedAt = LocalDateTime.now();

    // SAGA 상태 추적용: 특정 correlationId의 모든 이벤트 조회
    public static ProcessedEvent forSaga(
            String eventId, String eventType,
            String correlationId, String serviceName) {
        ProcessedEvent pe = new ProcessedEvent();
        pe.eventId = eventId;
        pe.eventType = eventType;
        pe.correlationId = correlationId;
        pe.serviceName = serviceName;
        return pe;
    }
}

public enum ProcessingStatus { SUCCESS, FAILED }
```

### TTL: Dedup 테이블 정리 전략

ProcessedEvent 테이블은 시간이 지나면서 계속 증가합니다. SAGA가 완료된 이후 오래된 레코드는 멱등성 체크에 더 이상 필요 없습니다. 주기적으로 정리해야 합니다.

```java
// ProcessedEventCleanupJob.java
@Component
public class ProcessedEventCleanupJob {

    private final ProcessedEventRepository repository;

    // 매일 새벽 2시 실행
    @Scheduled(cron = "0 0 2 * * *")
    @Transactional
    public void cleanupOldEvents() {
        // 90일 이상 지난 레코드 삭제
        LocalDateTime cutoff = LocalDateTime.now().minusDays(90);
        int deleted = repository.deleteByProcessedAtBefore(cutoff);
        log.info("ProcessedEvent 정리 완료: {} 건 삭제 (기준: {})", deleted, cutoff);
    }
}
```

```java
// ProcessedEventRepository.java 추가 메서드
public interface ProcessedEventRepository extends JpaRepository<ProcessedEvent, Long> {

    @Modifying
    @Query(value = """
        INSERT INTO processed_events (event_id, event_type, correlation_id, service_name, processed_at)
        SELECT :eventId, :eventType, :correlationId, :serviceName, NOW()
        WHERE NOT EXISTS (
            SELECT 1 FROM processed_events
            WHERE event_id = :eventId AND event_type = :eventType
        )
        """, nativeQuery = true)
    int tryAcquire(
        @Param("eventId") String eventId,
        @Param("eventType") String eventType,
        @Param("correlationId") String correlationId,
        @Param("serviceName") String serviceName
    );

    // SAGA 상태 추적용: correlationId로 전체 이벤트 이력 조회
    List<ProcessedEvent> findByCorrelationIdOrderByProcessedAtAsc(String correlationId);

    // TTL 정리
    @Modifying
    @Query("DELETE FROM ProcessedEvent pe WHERE pe.processedAt < :cutoff")
    int deleteByProcessedAtBefore(@Param("cutoff") LocalDateTime cutoff);
}
```

### 멱등성 테스트 패턴

멱등성이 실제로 동작하는지 검증하는 테스트는 "같은 이벤트를 두 번 보냈을 때 결과가 동일한가"를 확인합니다.

```java
// IdempotencyIntegrationTest.java
@SpringBootTest
@EmbeddedKafka(partitions = 1, topics = {"payment-completed"})
class IdempotencyIntegrationTest {

    @Autowired
    private KafkaTemplate<String, PaymentCompletedEvent> kafkaTemplate;

    @Autowired
    private BalanceRepository balanceRepository;

    @Autowired
    private ProcessedEventRepository processedEventRepository;

    @Test
    @DisplayName("같은 결제 이벤트를 두 번 처리해도 잔액은 한 번만 증가해야 한다")
    void givenDuplicatePaymentEvent_whenProcessedTwice_thenBalanceIncreasedOnce()
            throws Exception {

        // Given: 초기 잔액 1000
        String userId = "user-001";
        balanceRepository.save(new Balance(userId, 1000L));

        PaymentCompletedEvent event = PaymentCompletedEvent.builder()
            .eventId("evt-12345")       // 동일 eventId
            .userId(userId)
            .amount(500L)
            .build();

        // When: 같은 이벤트를 두 번 발행 (at-least-once 시뮬레이션)
        kafkaTemplate.send("payment-completed", event).get();
        kafkaTemplate.send("payment-completed", event).get();  // 중복!

        // Then: 잔액은 1번만 증가 → 1500
        await().atMost(Duration.ofSeconds(10)).untilAsserted(() -> {
            Balance balance = balanceRepository.findByUserId(userId).orElseThrow();
            assertThat(balance.getAmount()).isEqualTo(1500L);  // 1000 + 500, NOT 2000

            // ProcessedEvent는 1건만 존재
            long count = processedEventRepository.countByEventId("evt-12345");
            assertThat(count).isEqualTo(1);
        });
    }
}
```

---

## 참고 자료

- [Confluent: Idempotent Writer Pattern](https://developer.confluent.io/patterns/event-processing/idempotent-writer/)
- [Confluent: Idempotent Reader Pattern](https://developer.confluent.io/patterns/event-processing/idempotent-reader/)
- [Confluent: Schema-on-Read Pattern](https://developer.confluent.io/patterns/event-processing/schema-on-read/)
- [Kafka KIP-98: Exactly Once Delivery and Transactional Messaging](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
- 기존 문서: `12-transactions.md` (Kafka Transactions 상세 구현)
- 기존 문서: `06-choreography-saga.md` (Choreography SAGA 패턴)
- 기존 문서: `07-orchestration-saga.md` (Orchestration SAGA 패턴)
