# 6. Normalized vs Denormalized — 실습 (Kafka Streams)

KStream-KTable JOIN, `selectKey()` 리파티셔닝, Foreign Key Join, TopologyTestDriver 실습. 선행: [05-normalized-vs-denormalized.md](./05-normalized-vs-denormalized.md).

---

## 1. 실습 시나리오

주문 처리 시스템에서 주문 이벤트와 고객 정보를 결합(Enrich)하는 파이프라인을 구성한다. 이 실습은 05 문서에서 이론으로 다룬 "Adapter 패턴"을 직접 구현하는 과정이다.

**입력 토픽 두 개:**

```
토픽: orders          (키: orderId)
토픽: customers       (키: customerId)
```

**출력 토픽 하나:**

```
토픽: enriched-orders (키: orderId)
```

주문 이벤트에는 `customerId`만 있고, 고객 이름과 등급은 `customers` 토픽에 있다. `orders`와 `customers`를 JOIN해서 소비자가 한 곳에서 모든 정보를 볼 수 있는 `enriched-orders`를 만드는 것이 목표다.

---

## 2. ksqlDB 원본 코드 (참고용)

Confluent 코스 원본은 ksqlDB SQL로 작성되어 있다. 이 코드가 어떤 의미인지 이해한 뒤 Kafka Streams로 변환하는 것이 이 문서의 핵심이다.

```sql
-- customers 스트림을 KTable로 구체화
CREATE TABLE customers_table (
  customerId VARCHAR PRIMARY KEY,
  name       VARCHAR,
  tier       VARCHAR
) WITH (
  KAFKA_TOPIC = 'customers',
  VALUE_FORMAT = 'JSON'
);

-- orders 스트림 정의
CREATE STREAM orders_stream (
  orderId    VARCHAR KEY,
  customerId VARCHAR,
  product    VARCHAR,
  amount     DOUBLE
) WITH (
  KAFKA_TOPIC = 'orders',
  VALUE_FORMAT = 'JSON'
);

-- JOIN으로 비정규화된 스트림 생성
CREATE STREAM enriched_orders AS
  SELECT
    o.orderId     AS orderId,
    o.product     AS product,
    o.amount      AS amount,
    c.name        AS customerName,
    c.tier        AS customerTier
  FROM orders_stream o
  LEFT JOIN customers_table c
    ON o.customerId = c.customerId
EMIT CHANGES;
```

ksqlDB는 이 SQL 한 조각으로 JOIN 스트림을 생성하고, 내부적으로 리파티셔닝, 상태 저장소 관리, 토픽 발행까지 처리한다. Kafka Streams에서는 이 과정을 직접 작성한다.

---

## 3. 프로젝트 구조

기존 `redpanda-spring-boot` 프로젝트에 새 패키지를 추가하거나, 독립 모듈로 구성한다.

```
src/main/java/com/example/streams/
├── model/
│   ├── Order.java
│   ├── Customer.java
│   └── EnrichedOrder.java
├── serde/
│   ├── JsonSerde.java
│   └── SerdeFactory.java
├── topology/
│   └── EnrichOrderTopology.java
└── EnrichOrderApp.java

src/test/java/com/example/streams/
└── topology/
    └── EnrichOrderTopologyTest.java
```

---

## 4. POJO 모델 클래스

### 4.1 Order

```java
package com.example.streams.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Order {

    @JsonProperty("orderId")
    private String orderId;

    @JsonProperty("customerId")
    private String customerId;

    @JsonProperty("product")
    private String product;

    @JsonProperty("amount")
    private double amount;
}
```

### 4.2 Customer

```java
package com.example.streams.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Customer {

    @JsonProperty("customerId")
    private String customerId;

    @JsonProperty("name")
    private String name;

    @JsonProperty("tier")
    private String tier;
}
```

### 4.3 EnrichedOrder

```java
package com.example.streams.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EnrichedOrder {

    @JsonProperty("orderId")
    private String orderId;

    @JsonProperty("customerId")
    private String customerId;

    @JsonProperty("customerName")
    private String customerName;

    @JsonProperty("customerTier")
    private String customerTier;

    @JsonProperty("product")
    private String product;

    @JsonProperty("amount")
    private double amount;

    public static EnrichedOrder from(Order order, Customer customer) {
        String name = (customer != null) ? customer.getName() : "Unknown";
        String tier = (customer != null) ? customer.getTier() : "STANDARD";
        return EnrichedOrder.builder()
                .orderId(order.getOrderId())
                .customerId(order.getCustomerId())
                .customerName(name)
                .customerTier(tier)
                .product(order.getProduct())
                .amount(order.getAmount())
                .build();
    }
}
```

`from()` 팩토리 메서드에서 `customer`가 `null`인 경우를 처리하는 것이 중요하다. `leftJoin`은 매칭되는 고객이 없을 때 `null`을 전달한다. 이를 무시하고 `customer.getName()`을 호출하면 `NullPointerException`이 발생한다.

---

## 5. JSON Serde 구성

Kafka Streams는 키와 값의 직렬화/역직렬화 방식을 `Serde`로 지정한다. Jackson 기반 JSON Serde를 직접 구현한다.

```java
package com.example.streams.serde;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serializer;

public class JsonSerde<T> implements Serde<T> {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final Class<T> targetType;

    public JsonSerde(Class<T> targetType) {
        this.targetType = targetType;
    }

    @Override
    public Serializer<T> serializer() {
        return (topic, data) -> {
            if (data == null) return null;
            try {
                return objectMapper.writeValueAsBytes(data);
            } catch (Exception e) {
                throw new SerializationException("직렬화 실패: " + topic, e);
            }
        };
    }

    @Override
    public Deserializer<T> deserializer() {
        return (topic, data) -> {
            if (data == null) return null;
            try {
                return objectMapper.readValue(data, targetType);
            } catch (Exception e) {
                throw new SerializationException("역직렬화 실패: " + topic, e);
            }
        };
    }
}
```

```java
package com.example.streams.serde;

import com.example.streams.model.Customer;
import com.example.streams.model.EnrichedOrder;
import com.example.streams.model.Order;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;

public class SerdeFactory {

    public static Serde<Order> orderSerde() {
        return new JsonSerde<>(Order.class);
    }

    public static Serde<Customer> customerSerde() {
        return new JsonSerde<>(Customer.class);
    }

    public static Serde<EnrichedOrder> enrichedOrderSerde() {
        return new JsonSerde<>(EnrichedOrder.class);
    }

    public static Serde<String> stringSerde() {
        return Serdes.String();
    }
}
```

---

## 6. 핵심 토폴로지 구현

### 6.1 키 불일치 문제 이해

`orders` 토픽의 키는 `orderId`이고, `customers` 토픽의 키는 `customerId`다. KStream-KTable JOIN은 **같은 키**를 기준으로 동작한다. 따라서 `orders`의 키를 `customerId`로 바꿔서 `customers`와 같은 키 공간에 놓아야 한다.

이 과정을 **리파티셔닝(repartitioning)**이라고 한다. 키가 바뀌면 파티션 배치도 바뀌어야 하기 때문에, 내부적으로 중간 토픽이 생성된다.

```
orders (키: orderId)
    │
    │ selectKey: orderId → customerId
    ▼
orders-repartitioned (키: customerId)  ← 내부 토픽 자동 생성
    │
    │ leftJoin with customers (키: customerId)
    ▼
enriched (키: customerId)
    │
    │ selectKey: customerId → orderId (원래 키 복원)
    ▼
enriched-orders (키: orderId)
```

### 6.2 토폴로지 코드

```java
package com.example.streams.topology;

import com.example.streams.model.Customer;
import com.example.streams.model.EnrichedOrder;
import com.example.streams.model.Order;
import com.example.streams.serde.SerdeFactory;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.*;

public class EnrichOrderTopology {

    public static final String ORDERS_TOPIC         = "orders";
    public static final String CUSTOMERS_TOPIC      = "customers";
    public static final String ENRICHED_ORDERS_TOPIC = "enriched-orders";

    public static void build(StreamsBuilder builder) {

        // 1. orders 토픽을 KStream으로 읽기 (키: orderId)
        KStream<String, Order> orders = builder.stream(
                ORDERS_TOPIC,
                Consumed.with(SerdeFactory.stringSerde(), SerdeFactory.orderSerde())
        );

        // 2. customers 토픽을 KTable로 읽기 (키: customerId)
        //    KTable은 각 키의 최신 값을 상태 저장소에 유지한다
        KTable<String, Customer> customers = builder.table(
                CUSTOMERS_TOPIC,
                Consumed.with(SerdeFactory.stringSerde(), SerdeFactory.customerSerde()),
                Materialized.as("customers-store")  // 상태 저장소 이름 명시
        );

        // 3. orders의 키를 customerId로 변환 (리파티셔닝 발생)
        //    이 시점에 내부 리파티셔닝 토픽이 자동 생성된다
        KStream<String, Order> reKeyedOrders = orders
                .selectKey((orderId, order) -> order.getCustomerId());

        // 4. LEFT JOIN: customerId 기준으로 orders와 customers를 결합
        //    leftJoin이므로 매칭 고객이 없어도 주문 이벤트는 통과한다 (customer = null)
        KStream<String, EnrichedOrder> enriched = reKeyedOrders.leftJoin(
                customers,
                EnrichedOrder::from,
                Joined.with(
                        SerdeFactory.stringSerde(),
                        SerdeFactory.orderSerde(),
                        SerdeFactory.customerSerde()
                )
        );

        // 5. 키를 orderId로 복원하고 결과 토픽에 발행
        enriched
                .selectKey((customerId, enrichedOrder) -> enrichedOrder.getOrderId())
                .to(
                        ENRICHED_ORDERS_TOPIC,
                        Produced.with(SerdeFactory.stringSerde(), SerdeFactory.enrichedOrderSerde())
                );
    }
}
```

`leftJoin` 대신 `join`(inner join)을 쓰면 고객 정보가 없는 주문은 결과에서 제외된다. 어떤 것을 쓸지는 비즈니스 요구사항에 따라 결정한다. 고객이 반드시 존재해야 처리 가능한 흐름이라면 inner join이 더 적합하고, 고객 미등록 주문도 처리해야 한다면 left join이 필요하다.

---

## 7. 애플리케이션 진입점

```java
package com.example.streams;

import com.example.streams.topology.EnrichOrderTopology;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;

import java.util.Properties;
import java.util.concurrent.CountDownLatch;

public class EnrichOrderApp {

    public static void main(String[] args) throws InterruptedException {
        Properties props = buildProps();

        StreamsBuilder builder = new StreamsBuilder();
        EnrichOrderTopology.build(builder);
        Topology topology = builder.build();

        System.out.println(topology.describe());  // 토폴로지 구조 출력 (디버그용)

        KafkaStreams streams = new KafkaStreams(topology, props);
        CountDownLatch latch = new CountDownLatch(1);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            streams.close();
            latch.countDown();
        }));

        streams.start();
        latch.await();
    }

    private static Properties buildProps() {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "enrich-order-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:19092");
        // Redpanda 브로커 주소. docker-compose 기준 포트
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG,
                org.apache.kafka.common.serialization.Serdes.StringSerde.class);
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG,
                org.apache.kafka.common.serialization.Serdes.StringSerde.class);
        // 내부 리파티셔닝 토픽 자동 생성 허용 (Redpanda 기본값: true)
        props.put("auto.create.topics.enable", "true");
        return props;
    }
}
```

---

## 8. docker-compose 설정

기존 Redpanda 프로젝트의 `docker-compose.yml`을 재사용한다. 새로 필요한 것은 없다.

```yaml
# 기존 docker-compose.yml (발췌)
services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:v25.3.6
    command:
      - redpanda
      - start
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092
      - --mode dev-container
      - --smp 1
      - --default-log-level=info
    ports:
      - "19092:19092"
      - "9644:9644"
    environment:
      REDPANDA_AUTO_CREATE_TOPICS_ENABLED: "true"
```

`REDPANDA_AUTO_CREATE_TOPICS_ENABLED: "true"`는 Kafka Streams가 내부 리파티셔닝 토픽과 changelog 토픽을 자동 생성할 수 있도록 허용한다. 프로덕션에서는 보안 정책상 이 옵션을 끄고 토픽을 사전에 수동으로 생성하는 경우가 많다.

**테스트용 토픽 생성 명령어:**

```bash
# Redpanda 컨테이너에 접속해서 토픽 생성
docker exec -it redpanda rpk topic create orders --partitions 3
docker exec -it redpanda rpk topic create customers --partitions 3
docker exec -it redpanda rpk topic create enriched-orders --partitions 3

# 토픽 목록 확인
docker exec -it redpanda rpk topic list
```

`orders`와 `customers` 토픽의 파티션 수를 맞추면 리파티셔닝 이후 JOIN이 더 균등하게 분산된다.

---

## 9. KTable Foreign Key Join 패턴

### 9.1 언제 필요한가

위 실습에서 `selectKey()`로 키를 바꿔서 JOIN하는 방식은 잘 동작하지만 한 가지 제약이 있다. `orders` 스트림의 원래 키(`orderId`)를 잃어버리고 중간에 `customerId`를 키로 쓰는 과정이 필요하다. Kafka Streams 2.4부터는 **KTable-KTable Foreign Key Join**으로 이 과정을 더 자연스럽게 표현할 수 있다.

FK Join은 KStream이 아닌 KTable 두 개를 JOIN하는 패턴이다. `orders`를 KTable로 구체화하면 각 `orderId`의 최신 주문만 유지되며, 고객 정보가 업데이트될 때 자동으로 재조인(re-join)이 일어난다.

### 9.2 코드

```java
// orders도 KTable로 구성
KTable<String, Order> ordersTable = builder.table(
        "orders",
        Consumed.with(SerdeFactory.stringSerde(), SerdeFactory.orderSerde()),
        Materialized.as("orders-store")
);

KTable<String, Customer> customersTable = builder.table(
        "customers",
        Consumed.with(SerdeFactory.stringSerde(), SerdeFactory.customerSerde()),
        Materialized.as("customers-store")
);

// FK Join: ordersTable의 각 레코드에서 customerId(FK)를 추출
// → customersTable의 PK(customerId)와 매칭
KTable<String, EnrichedOrder> enrichedTable = ordersTable.join(
        customersTable,
        Order::getCustomerId,               // FK 추출 함수
        EnrichedOrder::from,                // ValueJoiner
        TableJoined.with(
                SerdeFactory.stringSerde(),
                SerdeFactory.customerSerde()
        ),
        Materialized.with(SerdeFactory.stringSerde(), SerdeFactory.enrichedOrderSerde())
);

enrichedTable.toStream().to(
        "enriched-orders",
        Produced.with(SerdeFactory.stringSerde(), SerdeFactory.enrichedOrderSerde())
);
```

FK Join의 강점은 **고객 정보가 바뀔 때 자동으로 관련 주문들이 재계산된다**는 점이다. CUST-42의 등급이 SILVER에서 GOLD로 바뀌면, CUST-42의 모든 주문에 대해 재조인이 실행되고 `enriched-orders`에 업데이트된 이벤트가 자동으로 발행된다. KStream-KTable JOIN에서는 이런 자동 재계산이 일어나지 않는다.

---

## 10. TopologyTestDriver로 단위 테스트

`TopologyTestDriver`는 실제 카프카 클러스터 없이 토폴로지를 인메모리로 실행하는 테스트 도구다. CI 환경에서 빠르게 JOIN 로직을 검증하기에 적합하다.

```java
package com.example.streams.topology;

import com.example.streams.model.Customer;
import com.example.streams.model.EnrichedOrder;
import com.example.streams.model.Order;
import com.example.streams.serde.SerdeFactory;
import org.apache.kafka.streams.*;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Properties;

import static org.assertj.core.api.Assertions.assertThat;

class EnrichOrderTopologyTest {

    private TopologyTestDriver driver;
    private TestInputTopic<String, Order> ordersTopic;
    private TestInputTopic<String, Customer> customersTopic;
    private TestOutputTopic<String, EnrichedOrder> enrichedOrdersTopic;

    @BeforeEach
    void setUp() {
        StreamsBuilder builder = new StreamsBuilder();
        EnrichOrderTopology.build(builder);
        Topology topology = builder.build();

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "test-enrich-order");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "dummy:9092");

        driver = new TopologyTestDriver(topology, props);

        ordersTopic = driver.createInputTopic(
                EnrichOrderTopology.ORDERS_TOPIC,
                SerdeFactory.stringSerde().serializer(),
                SerdeFactory.orderSerde().serializer()
        );

        customersTopic = driver.createInputTopic(
                EnrichOrderTopology.CUSTOMERS_TOPIC,
                SerdeFactory.stringSerde().serializer(),
                SerdeFactory.customerSerde().serializer()
        );

        enrichedOrdersTopic = driver.createOutputTopic(
                EnrichOrderTopology.ENRICHED_ORDERS_TOPIC,
                SerdeFactory.stringSerde().deserializer(),
                SerdeFactory.enrichedOrderSerde().deserializer()
        );
    }

    @AfterEach
    void tearDown() {
        driver.close();
    }

    @Test
    @DisplayName("고객 정보가 먼저 있을 때 주문과 JOIN되어 enriched 이벤트가 발행된다")
    void shouldEnrichOrderWithCustomerInfo() {
        // Given: customers 토픽에 고객 정보를 먼저 적재 (KTable 초기화)
        Customer customer = Customer.builder()
                .customerId("CUST-42")
                .name("김민준")
                .tier("GOLD")
                .build();
        customersTopic.pipeInput("CUST-42", customer);

        // When: 주문 이벤트 발행
        Order order = Order.builder()
                .orderId("ORD-9871")
                .customerId("CUST-42")
                .product("무선 이어폰")
                .amount(59000.0)
                .build();
        ordersTopic.pipeInput("ORD-9871", order);

        // Then: enriched-orders 토픽에 결합된 이벤트가 나와야 한다
        EnrichedOrder result = enrichedOrdersTopic.readValue();
        assertThat(result.getOrderId()).isEqualTo("ORD-9871");
        assertThat(result.getCustomerName()).isEqualTo("김민준");
        assertThat(result.getCustomerTier()).isEqualTo("GOLD");
        assertThat(result.getProduct()).isEqualTo("무선 이어폰");
        assertThat(result.getAmount()).isEqualTo(59000.0);
    }

    @Test
    @DisplayName("매칭 고객이 없을 때 leftJoin은 Unknown으로 채운 이벤트를 발행한다")
    void shouldHandleMissingCustomerWithLeftJoin() {
        // Given: customers 토픽에 CUST-99는 없음

        // When: 알 수 없는 customerId로 주문 발행
        Order order = Order.builder()
                .orderId("ORD-0001")
                .customerId("CUST-99")
                .product("키보드")
                .amount(120000.0)
                .build();
        ordersTopic.pipeInput("ORD-0001", order);

        // Then: 결과가 나오며 고객 정보는 Unknown/STANDARD 기본값
        EnrichedOrder result = enrichedOrdersTopic.readValue();
        assertThat(result.getOrderId()).isEqualTo("ORD-0001");
        assertThat(result.getCustomerName()).isEqualTo("Unknown");
        assertThat(result.getCustomerTier()).isEqualTo("STANDARD");
    }

    @Test
    @DisplayName("고객 등급이 변경된 후 들어온 주문은 새 등급으로 JOIN된다")
    void shouldUseLatestCustomerInfoForNewOrders() {
        // Given: 초기 고객 정보
        customersTopic.pipeInput("CUST-42",
                Customer.builder().customerId("CUST-42").name("김민준").tier("SILVER").build());

        // 첫 번째 주문 (SILVER)
        ordersTopic.pipeInput("ORD-0001",
                Order.builder().orderId("ORD-0001").customerId("CUST-42")
                        .product("마우스").amount(30000.0).build());

        // 고객 등급 업데이트
        customersTopic.pipeInput("CUST-42",
                Customer.builder().customerId("CUST-42").name("김민준").tier("GOLD").build());

        // 두 번째 주문 (GOLD 등급 업데이트 이후)
        ordersTopic.pipeInput("ORD-0002",
                Order.builder().orderId("ORD-0002").customerId("CUST-42")
                        .product("모니터").amount(350000.0).build());

        // Then: 첫 번째 주문은 SILVER로, 두 번째 주문은 GOLD로 JOIN
        EnrichedOrder first = enrichedOrdersTopic.readValue();
        EnrichedOrder second = enrichedOrdersTopic.readValue();

        assertThat(first.getCustomerTier()).isEqualTo("SILVER");
        assertThat(second.getCustomerTier()).isEqualTo("GOLD");
    }
}
```

세 번째 테스트가 중요한 동작을 검증한다. KStream-KTable JOIN에서 KTable은 항상 **현재 시점의 최신 값**을 참조한다. 주문 이벤트가 도착했을 때 KTable에 있는 값이 JOIN에 사용된다. 따라서 고객 등급이 바뀐 이후에 들어온 주문은 새 등급으로 JOIN된다. 이미 처리된 과거 주문 이벤트는 변경되지 않는다.

---

## 11. Gradle 의존성

```groovy
// build.gradle
dependencies {
    implementation 'org.apache.kafka:kafka-streams:3.7.0'
    implementation 'com.fasterxml.jackson.core:jackson-databind:2.17.0'
    compileOnly 'org.projectlombok:lombok:1.18.32'
    annotationProcessor 'org.projectlombok:lombok:1.18.32'

    testImplementation 'org.apache.kafka:kafka-streams-test-utils:3.7.0'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.2'
    testImplementation 'org.assertj:assertj-core:3.25.3'
}
```

---

## 12. 실행 및 검증

```bash
# 1. Redpanda 시작
docker-compose up -d

# 2. 토픽 생성
docker exec -it redpanda rpk topic create orders customers enriched-orders

# 3. 애플리케이션 실행
./gradlew run --args="com.example.streams.EnrichOrderApp"

# 4. 고객 데이터 발행 (customers 토픽)
docker exec -it redpanda rpk topic produce customers --key "CUST-42" <<EOF
{"customerId":"CUST-42","name":"김민준","tier":"GOLD"}
EOF

# 5. 주문 이벤트 발행 (orders 토픽)
docker exec -it redpanda rpk topic produce orders --key "ORD-9871" <<EOF
{"orderId":"ORD-9871","customerId":"CUST-42","product":"무선 이어폰","amount":59000}
EOF

# 6. 결과 확인 (enriched-orders 토픽)
docker exec -it redpanda rpk topic consume enriched-orders --num 1
```

정상 동작하면 다음과 같은 결과가 출력된다:

```json
{
  "orderId": "ORD-9871",
  "customerId": "CUST-42",
  "customerName": "김민준",
  "customerTier": "GOLD",
  "product": "무선 이어폰",
  "amount": 59000.0
}
```

---

## Redpanda 호환성 노트

- **KTable FK Join 내부 토픽**: `selectKey()` 사용 시 또는 FK Join 시 Kafka Streams는 내부 리파티셔닝 토픽을 자동 생성한다. Redpanda에서도 `auto.create.topics.enable=true`이면 정상 생성된다. 해당 토픽 이름은 `{application-id}-{uuid}-repartition` 형태다.
- **상태 저장소 changelog 토픽**: KTable은 상태를 RocksDB에 저장하고, 복구를 위해 changelog 토픽을 자동 생성한다. Redpanda에서도 그대로 동작한다.
- **rpk 토픽 조회**: `docker exec -it redpanda rpk topic list`로 자동 생성된 내부 토픽들을 확인할 수 있다. `enrich-order-app-*-repartition` 형태의 토픽이 보이면 정상이다.
- **TopologyTestDriver**: 실제 브로커와 무관하게 동작하므로 Redpanda/Kafka 구분 없이 동일한 테스트 코드를 사용할 수 있다.
- **포트**: 이 실습은 Redpanda 외부 리스너 포트 `19092`를 사용한다. 기존 프로젝트의 `docker-compose.yml` 설정과 일치시켜야 한다.

---

## 체크포인트

- [ ] `selectKey()`를 쓰지 않으면 KStream-KTable JOIN이 왜 동작하지 않는지 설명할 수 있다
- [ ] `leftJoin`과 `join`(inner)의 차이를 고객 없는 주문 처리 관점에서 설명할 수 있다
- [ ] KTable-KTable FK Join과 KStream-KTable JOIN의 차이(고객 변경 시 동작)를 설명할 수 있다
- [ ] `TopologyTestDriver`로 고객 등급 변경 이후의 JOIN 동작을 테스트할 수 있다
- [ ] `auto.create.topics.enable` 설정이 Kafka Streams 내부 토픽 생성에 왜 필요한지 이해했다
- [ ] 위 코드를 실제로 실행하고 `enriched-orders` 토픽에서 결과를 확인할 수 있다
