# 5. Normalized vs Denormalized — 정규화와 비정규화

이벤트 스트림에서 정규화/비정규화 선택 기준, Transactional Outbox, CDC + Redpanda Connect 파이프라인. 선행: [04-event-schema-design.md](./04-event-schema-design.md).

---

## 1. 관계형 DB에서의 정규화, 그리고 이벤트 스트림으로의 확장

관계형 데이터베이스에서 정규화(Normalization)는 중복을 제거하고 데이터 일관성을 보장하기 위한 설계 원칙이다. 예를 들어 주문 테이블에 고객 이름을 직접 저장하지 않고, 고객 ID만 저장한 뒤 고객 테이블과 JOIN으로 연결하는 방식이다. 이렇게 하면 고객 이름이 바뀌더라도 고객 테이블 한 곳만 수정하면 모든 주문 조회에서 최신 이름이 반영된다.

이벤트 스트림 설계에서도 동일한 개념이 적용된다. 이벤트를 정규화한다는 것은 각 엔티티(Entity)를 별도의 토픽에 저장하고, 하나의 이벤트에는 관련 엔티티의 ID만 참조로 포함하는 방식을 의미한다. 반대로 비정규화(Denormalization)는 소비자(Consumer)가 필요한 모든 정보를 하나의 이벤트에 미리 합쳐서 넣는 방식이다.

이 선택은 단순한 저장 방식의 차이가 아니다. 시스템의 결합도, 소비자의 복잡도, 데이터 일관성 보장 방식, 심지어 장애 시 복구 방식까지 영향을 미친다. 어떤 것이 "옳다"는 답은 없지만, 상황에 따라 더 적합한 선택이 분명히 존재한다.

---

## 2. 정규화된 이벤트 (Normalized Events)

### 2.1 구조

정규화된 이벤트 설계에서는 도메인 엔티티마다 별도 토픽을 둔다. 주문 시스템을 예로 들면 아래와 같은 구조가 된다.

```
토픽: orders
{
  "orderId": "ORD-9871",
  "customerId": "CUST-42",   ← 고객 정보는 ID만 포함
  "productId": "PROD-007",
  "amount": 59000,
  "createdAt": "2026-02-27T09:00:00Z"
}

토픽: customers
{
  "customerId": "CUST-42",
  "name": "김민준",
  "tier": "GOLD",
  "address": "서울시 강남구"
}
```

주문 이벤트는 고객에 대해 `customerId`만 알고 있다. 고객의 이름, 등급, 주소는 `customers` 토픽에 별도로 존재한다. 이벤트 소비자가 주문과 고객 정보를 함께 필요로 한다면, 두 스트림을 JOIN해야 한다.

### 2.2 장점

**데이터 일관성이 자연스럽게 보장된다.** 고객의 등급이 SILVER에서 GOLD로 바뀌면 `customers` 토픽에 새로운 이벤트를 발행하면 끝이다. `orders` 토픽에 있는 수백만 개의 주문 이벤트를 건드릴 필요가 없다. 고객 정보는 단 한 곳에서 관리된다.

**스토리지 효율이 높다.** 같은 정보가 여러 이벤트에 반복 저장되지 않기 때문에 토픽 크기가 작게 유지된다. 특히 고객 정보처럼 크고 잘 변하지 않는 데이터일수록 이 차이가 커진다.

**발행 측(Producer)이 단순해진다.** 주문 서비스는 주문에 관련된 필드만 채워서 발행하면 된다. 고객 정보를 별도로 조회해 합쳐야 하는 부담이 없다.

### 2.3 단점

**소비자가 JOIN을 직접 수행해야 한다.** Kafka Streams나 ksqlDB 같은 스트림 처리 레이어 없이는 두 토픽의 데이터를 결합하기가 어렵다. 단순 Consumer로는 구현이 복잡해진다.

**JOIN 타이밍 문제가 발생할 수 있다.** 주문 이벤트가 도착했을 때 `customers` 토픽에서 해당 고객 정보가 아직 도착하지 않았다면 어떻게 할까? 대기(wait)할 것인가, 불완전한 이벤트를 내보낼 것인가? 이 문제는 생각보다 자주 발생하며 별도의 처리 전략이 필요하다.

---

## 3. 비정규화된 이벤트 (Denormalized Events)

### 3.1 구조

비정규화된 이벤트에서는 소비자가 필요한 모든 데이터를 하나의 이벤트에 담는다.

```
토픽: enriched-orders
{
  "orderId": "ORD-9871",
  "customerId": "CUST-42",
  "customerName": "김민준",      ← 고객 이름 직접 포함
  "customerTier": "GOLD",       ← 고객 등급 직접 포함
  "customerAddress": "서울시 강남구",
  "productId": "PROD-007",
  "amount": 59000,
  "createdAt": "2026-02-27T09:00:00Z"
}
```

이 이벤트를 수신한 소비자는 다른 토픽을 조회할 필요 없이 즉시 처리를 시작할 수 있다.

### 3.2 장점

**소비자 구현이 단순해진다.** 하나의 토픽만 구독하고, 이벤트 하나를 받으면 바로 처리 가능하다. 스트림 JOIN 같은 복잡한 로직이 필요 없다. 이는 소비자 팀이 많거나 다양한 기술 스택을 사용하는 경우에 특히 유리하다.

**조회 성능이 높다.** 외부 시스템 호출이나 추가 조회 없이 이벤트 하나에서 모든 정보를 얻을 수 있다. 처리 지연(latency)이 낮다.

**소비자-생산자 간 결합도를 낮출 수 있다.** 소비자는 이벤트만 보면 되기 때문에, 내부 서비스 구조나 다른 토픽의 존재를 알 필요가 없다.

### 3.3 단점

**데이터 불일치(Staleness) 문제가 핵심 약점이다.** 주문 이벤트에 고객 등급이 "SILVER"로 포함된 상태에서, 이후 고객 등급이 "GOLD"로 바뀌면 어떻게 될까? 이미 발행된 주문 이벤트의 등급 정보는 틀린 값이 되어버린다. 이벤트 로그는 불변(immutable)이기 때문에 수정할 수 없다. 이 문제를 해결하려면 보상 이벤트(compensating event)를 발행하거나, 소비자 측에서 최신 고객 정보를 별도로 조회하는 로직이 필요하다.

**페이로드 크기가 증가한다.** 같은 정보가 수백만 개의 이벤트에 반복 저장되면 스토리지와 네트워크 비용이 늘어난다. 고객 정보가 크다면 이 비용은 무시하기 어렵다.

**발행 측이 더 많은 일을 해야 한다.** 주문 이벤트를 발행하기 전에 고객 정보를 조회해야 하고, 이 조회가 실패하면 발행 자체가 실패한다. 생산자의 가용성(availability)이 다른 서비스에 의존하게 된다.

---

## 4. 트레이드오프 비교

```
측면              | 정규화                  | 비정규화
----------------|------------------------|------------------------
데이터 일관성    | 자연스럽게 보장         | 발행 시점 스냅샷만 보장
저장 효율        | 높음 (중복 없음)        | 낮음 (데이터 중복)
소비자 복잡도    | 높음 (JOIN 필요)        | 낮음 (이벤트 하나로 완결)
발행 복잡도      | 낮음 (자기 도메인만)    | 높음 (타 도메인 조회 필요)
스키마 진화      | 토픽별 독립 진화        | 여러 도메인 변경이 영향
소비자 수        | 적을수록 유리           | 많을수록 유리
```

어떤 방식을 선택할지는 다음 질문에 답하면서 결정하면 된다. "이 이벤트를 소비하는 팀이 몇 곳인가?" 소비자가 많다면 비정규화가 소비자 부담을 덜어준다. "포함될 데이터의 변경 빈도는 어떤가?" 고객 이름처럼 거의 변하지 않는 데이터라면 비정규화로 인한 데이터 불일치 위험이 낮다. "실시간 정확성이 얼마나 중요한가?" 재무나 결제처럼 정확성이 절대적이라면 비정규화는 위험하다.

---

## 5. Transactional Outbox 패턴

### 5.1 왜 필요한가

정규화 방식에서 자주 맞닥뜨리는 문제가 있다. 서비스가 DB에 주문 레코드를 저장하면서 동시에 `orders` 토픽에 이벤트를 발행하려 한다고 가정하자. DB 저장은 성공했는데 카프카 발행이 실패하면? 반대로 카프카 발행은 성공했는데 DB 저장이 실패하면? 두 작업을 하나의 트랜잭션으로 묶을 수 없기 때문에 데이터 불일치가 발생한다.

Transactional Outbox 패턴은 이 문제를 해결한다. **DB 변경과 이벤트 발행을 하나의 DB 트랜잭션으로 원자적으로 처리**하는 것이 핵심이다.

### 5.2 동작 방식

```
┌─────────────────┐         ┌──────────────────┐
│  Order Service  │         │   PostgreSQL DB   │
│                 │─txn──►  │  orders 테이블    │
│  주문 처리 로직  │         │  outbox 테이블    │ ← 같은 트랜잭션에 함께 저장
└─────────────────┘         └────────┬─────────┘
                                     │ CDC (변경 감지)
                                     ▼
                            ┌──────────────────┐
                            │  Debezium /      │
                            │  Redpanda Connect│
                            └────────┬─────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  Kafka/Redpanda  │
                            │  orders 토픽      │
                            └──────────────────┘
```

1. 주문 서비스가 `orders` 테이블과 `outbox` 테이블에 동시에 쓴다. 두 쓰기가 하나의 DB 트랜잭션 안에 있기 때문에 둘 다 성공하거나 둘 다 실패한다.
2. CDC(Change Data Capture) 컴포넌트가 `outbox` 테이블의 변경을 감지한다.
3. 감지된 변경을 카프카/Redpanda 토픽에 발행한다.

`outbox` 테이블은 이벤트의 임시 대기소 역할을 한다. 카프카가 잠시 다운되더라도 이벤트는 DB에 안전하게 저장되어 있고, 복구 후 CDC가 발행을 재시도한다.

### 5.3 Outbox 테이블 구조 예시

```sql
CREATE TABLE outbox (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50)  NOT NULL,  -- 'Order', 'Customer' 등
    aggregate_id   VARCHAR(50)  NOT NULL,  -- orderId, customerId 등
    event_type     VARCHAR(100) NOT NULL,  -- 'OrderCreated', 'OrderShipped' 등
    payload        JSONB        NOT NULL,  -- 실제 이벤트 내용
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    processed      BOOLEAN      NOT NULL DEFAULT FALSE
);
```

`aggregate_type`과 `aggregate_id`를 별도 컬럼으로 관리하면 CDC 컴포넌트가 토픽 라우팅을 정교하게 할 수 있다. 예를 들어 `aggregate_type = 'Order'`이면 `orders` 토픽으로, `aggregate_type = 'Customer'`이면 `customers` 토픽으로 보내는 식이다.

---

## 6. CDC와 Debezium / Redpanda Connect

### 6.1 CDC란

CDC(Change Data Capture)는 DB의 변경 이력(redo log, WAL 등)을 실시간으로 읽어서 변경 이벤트를 생성하는 기술이다. 애플리케이션 코드를 수정하지 않고도 DB의 모든 INSERT/UPDATE/DELETE를 이벤트 스트림으로 변환할 수 있다.

정규화된 DB 설계를 그대로 유지하면서, CDC를 통해 이벤트 스트림을 자동 생성하는 방식은 기존 시스템을 이벤트 기반 아키텍처로 점진적으로 전환할 때 특히 유용하다. DB 스키마를 바꾸거나 애플리케이션 코드를 대대적으로 수정하지 않아도 된다.

### 6.2 Debezium 구성 예시

Debezium은 MySQL, PostgreSQL, MongoDB 등 주요 DB의 CDC를 지원하는 오픈소스 커넥터다. Kafka Connect 위에서 동작하며, Redpanda와도 완전히 호환된다.

```json
{
  "name": "orders-outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.dbname": "shop",
    "table.include.list": "public.outbox",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.table.field.event.key": "aggregate_id",
    "transforms.outbox.route.by.field": "aggregate_type",
    "transforms.outbox.route.topic.replacement": "${routedByValue}s"
  }
}
```

`EventRouter` 트랜스폼이 핵심이다. `aggregate_type` 필드를 읽어서 어느 토픽으로 라우팅할지 결정하고, `payload` 필드의 JSON을 실제 카프카 메시지로 변환한다.

### 6.3 Redpanda Connect (구 Benthos 기반)

Redpanda Connect는 Redpanda에 내장된 데이터 파이프라인 도구다. Debezium을 별도로 설치하지 않아도 Redpanda Connect로 PostgreSQL WAL을 읽어 토픽에 쓸 수 있다.

```yaml
# redpanda-connect-cdc.yaml
input:
  postgres_cdc:
    dsn: "postgres://user:pass@postgres:5432/shop?sslmode=disable"
    schema: "public"
    tables: ["outbox"]
    slot_name: "redpanda_slot"

pipeline:
  processors:
    - mapping: |
        root = this.payload.parse_json()
        meta topic = "orders"

output:
  kafka_franz:
    seed_brokers: ["redpanda:9092"]
    topic: ${! meta("topic") }
```

Debezium보다 설정이 간결하고, Redpanda 생태계와 통합이 자연스럽다는 장점이 있다.

---

## 7. 추상화 레이어 (Adapter) 패턴

### 7.1 왜 내부와 외부 이벤트를 분리하는가

도메인 내부에서는 정규화된 이벤트를 사용해 일관성을 유지하고, 외부 소비자에게는 비정규화된 이벤트를 제공해 편의성을 높이는 방식이 있다. 이 두 세계 사이에 중간 서비스(Adapter)를 두어 변환을 담당하게 한다.

```
내부 이벤트 (정규화)          Adapter 서비스         외부 이벤트 (비정규화)
─────────────────────        ─────────────         ─────────────────────
orders 토픽       ──►        JOIN + 변환   ──►      enriched-orders 토픽
customers 토픽    ──►                               (외부 파트너, 다른 팀 소비)
```

이 패턴의 핵심 이점은 **내부 도메인 모델을 외부로부터 보호**한다는 점이다. 내부 스키마가 바뀌어도 외부 소비자에게 영향을 주지 않으려면 Adapter가 그 변환 책임을 지면 된다. 마이크로서비스 아키텍처에서 팀 간 계약(contract)을 명확히 하는 데도 유용하다.

### 7.2 구현 예시 (Kafka Streams)

```java
// Adapter: orders + customers → enriched-orders
StreamsBuilder builder = new StreamsBuilder();

KStream<String, Order> orders =
    builder.stream("orders", Consumed.with(Serdes.String(), orderSerde));

KTable<String, Customer> customers =
    builder.table("customers", Consumed.with(Serdes.String(), customerSerde));

// customerId를 키로 리파티셔닝
KStream<String, Order> reKeyedOrders = orders
    .selectKey((orderId, order) -> order.getCustomerId());

// JOIN: 주문과 고객 정보 합치기
KStream<String, EnrichedOrder> enriched = reKeyedOrders.leftJoin(
    customers,
    (order, customer) -> EnrichedOrder.builder()
        .orderId(order.getOrderId())
        .customerName(customer != null ? customer.getName() : "Unknown")
        .customerTier(customer != null ? customer.getTier() : "STANDARD")
        .product(order.getProduct())
        .amount(order.getAmount())
        .build(),
    Joined.with(Serdes.String(), orderSerde, customerSerde)
);

// 결과를 외부 소비자용 토픽에 발행
enriched
    .selectKey((customerId, enrichedOrder) -> enrichedOrder.getOrderId())
    .to("enriched-orders", Produced.with(Serdes.String(), enrichedOrderSerde));
```

---

## 8. 선택 기준 플로우차트

```
주문 이벤트에 고객 정보를 포함해야 하는가?
         │
         ├─ No → 정규화 유지 (ID 참조만)
         │
         └─ Yes
              │
              ├─ 고객 정보가 자주 바뀌는가?
              │         │
              │         ├─ Yes (빈번한 변경)
              │         │       → 정규화 유지 + Adapter(KStream JOIN)
              │         │
              │         └─ No (드문 변경)
              │                 │
              │                 ├─ 소비자가 여러 팀/서비스인가?
              │                 │         │
              │                 │         ├─ Yes → 비정규화 (소비자 편의)
              │                 │         └─ No  → 정규화 유지
              │
              └─ 데이터 정확성이 절대적인가? (금융/결제)
                         │
                         └─ Yes → 정규화 필수 (불일치 위험 제거)
```

---

## 9. Outbox 패턴의 장애 시나리오와 대응

Outbox 패턴이 DB 저장과 이벤트 발행의 원자성을 보장한다고 해서 모든 장애가 사라지는 것은 아니다. 실제로 어떤 장애가 발생할 수 있고 어떻게 대응하는지 이해해야 패턴을 올바르게 운영할 수 있다.

**장애 1: CDC 컴포넌트(Debezium/Redpanda Connect)가 다운된 경우.**

DB의 `outbox` 테이블에는 이벤트가 계속 쌓인다. CDC가 복구되면 쌓인 이벤트를 순서대로 처리한다. PostgreSQL의 WAL 슬롯(replication slot)이 CDC의 마지막 읽기 위치를 기억하기 때문이다. 다만 WAL 슬롯이 지나치게 오래 미처리 상태로 남으면 디스크 공간을 점유하므로, CDC 다운 시간에 상한선을 두는 모니터링이 필요하다.

**장애 2: 카프카/Redpanda가 다운된 경우.**

CDC 컴포넌트는 브로커에 발행을 시도하다 실패한다. 재시도 정책(retry policy)에 따라 일정 횟수 재시도하며 대기한다. 브로커가 복구되면 발행을 재개한다. 이 과정에서 `outbox` 테이블의 `processed` 컬럼을 활용하면 이미 성공한 이벤트를 재발행하는 것을 방지할 수 있다.

**장애 3: 같은 이벤트가 두 번 발행되는 경우(at-least-once).**

CDC는 at-least-once 보장을 제공한다. 즉 장애 복구 과정에서 동일 이벤트가 중복 발행될 수 있다. 소비자 측에서 멱등성(idempotency) 처리를 구현해야 한다. `outbox.id`(UUID)를 이벤트 헤더에 포함시키고, 소비자가 이 ID를 기준으로 중복 처리를 감지하는 방식이 일반적이다.

```sql
-- 처리된 이벤트 추적 (소비자 측 DB)
CREATE TABLE processed_events (
    event_id   UUID PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 이벤트 처리 전 중복 확인
INSERT INTO processed_events (event_id)
VALUES (:eventId)
ON CONFLICT (event_id) DO NOTHING;
-- 영향받은 행이 0이면 이미 처리된 이벤트 → 스킵
```

### 9.1 CDC 흐름 Mermaid 다이어그램

```mermaid
sequenceDiagram
    participant App as Order Service
    participant DB as PostgreSQL
    participant CDC as Debezium / Redpanda Connect
    participant Broker as Kafka / Redpanda
    participant Consumer as 소비자

    App->>DB: BEGIN TRANSACTION
    App->>DB: INSERT INTO orders (...)
    App->>DB: INSERT INTO outbox (aggregate_type, payload, ...)
    App->>DB: COMMIT

    loop WAL Polling
        CDC->>DB: Read WAL (outbox 변경 감지)
        DB-->>CDC: outbox row (aggregate_type=Order, payload=...)
    end

    CDC->>Broker: Produce → orders 토픽
    Broker-->>CDC: ACK

    Consumer->>Broker: Poll orders 토픽
    Broker-->>Consumer: OrderCreated 이벤트
    Consumer->>Consumer: 멱등성 확인 (event_id 중복 체크)
    Consumer->>Consumer: 비즈니스 로직 처리
```

이 다이어그램에서 핵심은 App과 DB 사이의 트랜잭션이다. `orders`와 `outbox`를 같은 트랜잭션으로 묶기 때문에 "주문은 저장됐는데 이벤트는 유실"되는 상황이 원천적으로 불가능하다. CDC는 DB 내부의 WAL을 직접 읽기 때문에 App이 CDC를 직접 호출하지 않아도 된다. App은 DB에만 집중하면 된다.

---

## 10. 실무 권장 사항

대부분의 프로덕션 시스템에서는 정규화와 비정규화를 혼용한다. 도메인 내부는 정규화로 유지하고, 외부 인터페이스(API Gateway 이벤트, 파트너 연동, 분석 시스템)는 비정규화된 이벤트를 제공하는 식이다.

핵심은 **이벤트의 소비자가 누구인가**를 중심으로 설계하는 것이다. 도메인 전문가로 구성된 내부 팀이 소비자라면 JOIN 비용을 감수하더라도 정규화가 유리하다. 외부 파트너나 다른 기술 스택을 쓰는 팀이 소비자라면 비정규화로 진입 장벽을 낮추는 것이 협업 효율을 높인다.

Transactional Outbox 패턴은 정규화 방식에서 이벤트 발행의 신뢰성을 보장하는 사실상의 표준이다. DB 트랜잭션과 이벤트 발행의 원자성을 보장하지 않으면, 분산 시스템에서 데이터 불일치는 시간의 문제일 뿐이다.

---

## Redpanda 호환성 노트

- **CDC 커넥터**: Redpanda는 Kafka API와 완전히 호환되기 때문에 Debezium이 그대로 동작한다. Debezium의 `bootstrap.servers`를 Redpanda 브로커 주소로 설정하면 된다.
- **Redpanda Connect**: Debezium 대신 Redpanda Connect(구 Benthos)를 사용하면 별도 Kafka Connect 클러스터 없이 CDC 파이프라인을 구성할 수 있다. 운영 복잡도가 낮아진다.
- **Outbox 패턴**: Redpanda의 높은 쓰기 처리량과 낮은 지연 덕분에 Outbox 패턴의 CDC 경로가 더욱 효율적으로 동작한다. Outbox 테이블이 대기열로 쌓이는 현상이 최소화된다.
- **Schema Registry**: Redpanda 내장 Schema Registry를 사용하면 정규화 방식에서 각 토픽의 스키마를 독립적으로 관리할 수 있다. Adapter 서비스는 입력 스키마와 출력 스키마를 각각 별도로 등록한다.
- **KTable 상태 저장소**: Adapter 패턴에서 Kafka Streams의 KTable은 내부적으로 RocksDB에 상태를 저장한다. Redpanda에서도 동일하게 동작하며, 토픽 기반 changelog를 통해 복구된다.

---

## 체크포인트

- [ ] 정규화된 이벤트와 비정규화된 이벤트의 구조 차이를 직접 그려볼 수 있다
- [ ] "고객 등급이 변경되었을 때 정규화/비정규화 방식에서 각각 어떤 일이 발생하는가?"를 설명할 수 있다
- [ ] Transactional Outbox 패턴의 3단계(DB 저장 → CDC 감지 → 토픽 발행)를 순서대로 설명할 수 있다
- [ ] CDC와 Debezium의 역할 차이를 한 문장으로 설명할 수 있다
- [ ] 주어진 시나리오에서 정규화와 비정규화 중 어떤 것을 선택할지 근거를 들어 설명할 수 있다
- [ ] Adapter 패턴이 내부 도메인을 어떻게 보호하는지 이해했다
- [ ] Redpanda Connect로 Outbox 테이블을 토픽에 연결하는 설정 구조를 읽고 이해할 수 있다
