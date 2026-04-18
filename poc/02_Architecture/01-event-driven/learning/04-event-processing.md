# 04. Stateless Topology (무상태 스트림 처리)

Kafka Streams DSL, filter, map, flatMap, branch, peek을 활용한 변환 파이프라인

모든 스트림 처리의 기초는 Stateless 연산이다. 상태 없이 이벤트를 필터링/변환/라우팅하는 능력이 있어야 Stateful 처리로 나아갈 수 있다.

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- Stateless 토폴로지의 핵심 연산(filter, map, branch, merge)을 이해한다
- 이벤트 라우팅과 변환 파이프라인을 설계할 수 있다
- Stateless vs Stateful 처리의 차이와 선택 기준을 설명할 수 있다

---

## 구성:

### 1. Kafka Streams란?

#### 핵심 개념
```
Kafka Streams:
├── 라이브러리 방식 (별도 클러스터 불필요, 애플리케이션에 내장)
├── 실시간 스트림 처리 (마이크로배치 아님, 진짜 스트리밍)
├── Exactly-Once Semantics 지원 (processing.guarantee=exactly_once_v2)
├── 자동 파티션 분산 (파티션 수만큼 병렬 처리)
└── 상태 관리 (RocksDB 기반 로컬 State Store)
```

#### Stateless vs Stateful
```
Stateless:
├── 메시지 하나만 보고 결정 (이전 메시지 기억 안 함)
├── filter, map, flatMap, branch
├── 수평 확장 쉬움 (인스턴스 추가만 하면 됨)
└── 예: 주문 금액 10만원 이상 필터링, 화폐 변환

Stateful:
├── 여러 메시지를 모아서 처리 (상태 저장 필요)
├── aggregate, count, join, windowing
├── State Store 관리 필요 (복구, 리밸런싱)
└── 예: 사용자별 총 구매액, 최근 5분간 주문 수
```

### 2. Docker Compose 설정

```yaml
version: '3.8'
services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:v24.2.4
    command:
      - redpanda start
      - --smp 1
      - --overprovisioned
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092
    ports:
      - 19092:19092
      - 9644:9644
    healthcheck:
      test: ["CMD-SHELL", "rpk cluster health | grep -E 'Healthy:.+true' || exit 1"]

  console:
    image: docker.redpanda.com/redpandadata/console:latest
    entrypoint: /bin/sh
    command: -c "echo \"$$CONSOLE_CONFIG_FILE\" > /tmp/config.yml; /app/console"
    environment:
      CONFIG_FILEPATH: /tmp/config.yml
      CONSOLE_CONFIG_FILE: |
        kafka:
          brokers: ["redpanda:9092"]
    ports:
      - 8080:8080
    depends_on:
      - redpanda
```

### 3. Spring Boot Kafka Streams 설정

#### build.gradle
```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.apache.kafka:kafka-streams'
    implementation 'org.springframework.kafka:spring-kafka'
}
```

#### application.yml
```yaml
spring:
  application:
    name: order-processor
  kafka:
    bootstrap-servers: localhost:19092
    streams:
      application-id: order-processor-app
      properties:
        default.key.serde: org.apache.kafka.common.serialization.Serdes$StringSerde
        default.value.serde: org.apache.kafka.common.serialization.Serdes$StringSerde
        commit.interval.ms: 1000
```

**핵심 설정**:
- `application-id`: Consumer Group ID와 유사 (스트림 애플리케이션 식별자)
- `default.key.serde`: 키 직렬화/역직렬화 방식 (StringSerde = String 타입)
- `default.value.serde`: 값 직렬화/역직렬화 방식
- `commit.interval.ms`: 오프셋 커밋 주기

### 4. Stateless Topology 패턴

#### 패턴 1: filter (조건 필터링)
```java
@Configuration
@EnableKafkaStreams
@Slf4j
public class OrderFilterTopology {
    @Bean
    public KStream<String, String> filterHighValueOrders(StreamsBuilder builder) {
        KStream<String, String> orders = builder.stream("orders");

        orders
            .filter((key, value) -> {
                JsonNode order = parseJson(value);
                double amount = order.get("amount").asDouble();
                return amount >= 100000;  // 10만원 이상만 통과
            })
            .peek((key, value) -> log.info("High-value order: {}", value))
            .to("high-value-orders");

        return orders;
    }

    private JsonNode parseJson(String json) {
        try {
            return new ObjectMapper().readTree(json);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
```

**흐름**:
```
orders (모든 주문)
  ↓ filter (amount >= 100000)
high-value-orders (고액 주문만)
```

#### 패턴 2: map (1:1 변환)
```java
@Bean
public KStream<String, String> enrichOrders(StreamsBuilder builder) {
    KStream<String, String> orders = builder.stream("orders");

    orders
        .mapValues(value -> {
            JsonNode order = parseJson(value);
            ObjectNode enriched = ((ObjectNode) order);

            // 환율 적용 (USD → KRW)
            double amount = order.get("amount").asDouble();
            enriched.put("amountUSD", amount / 1300.0);
            enriched.put("enrichedAt", System.currentTimeMillis());

            return enriched.toString();
        })
        .to("enriched-orders");

    return orders;
}
```

**흐름**:
```
orders ({"orderId": "1", "amount": 130000})
  ↓ mapValues (USD 변환 추가)
enriched-orders ({"orderId": "1", "amount": 130000, "amountUSD": 100, "enrichedAt": 1234567890})
```

#### 패턴 3: flatMap (1:N 변환)
```java
@Bean
public KStream<String, String> splitOrderItems(StreamsBuilder builder) {
    KStream<String, String> orders = builder.stream("orders");

    orders
        .flatMapValues(value -> {
            JsonNode order = parseJson(value);
            List<String> items = new ArrayList<>();

            // items 배열을 개별 메시지로 분할
            JsonNode itemsNode = order.get("items");
            for (JsonNode item : itemsNode) {
                ObjectNode itemWithOrderId = mapper.createObjectNode();
                itemWithOrderId.put("orderId", order.get("orderId").asText());
                itemWithOrderId.set("item", item);
                items.add(itemWithOrderId.toString());
            }

            return items;
        })
        .to("order-items");

    return orders;
}
```

**흐름**:
```
orders (1개 주문, 3개 아이템)
{"orderId": "1", "items": [{"name": "A"}, {"name": "B"}, {"name": "C"}]}
  ↓ flatMapValues (아이템별 분리)
order-items (3개 메시지)
{"orderId": "1", "item": {"name": "A"}}
{"orderId": "1", "item": {"name": "B"}}
{"orderId": "1", "item": {"name": "C"}}
```

#### 패턴 4: branch (조건별 분기)
```java
@Bean
public KStream<String, String> routeOrders(StreamsBuilder builder) {
    KStream<String, String> orders = builder.stream("orders");

    Map<String, KStream<String, String>> branches = orders.split(Named.as("order-"))
        .branch((key, value) -> {
            double amount = parseJson(value).get("amount").asDouble();
            return amount >= 1000000;  // 100만원 이상
        }, Branched.as("vip"))
        .branch((key, value) -> {
            double amount = parseJson(value).get("amount").asDouble();
            return amount >= 100000;  // 10만원 이상
        }, Branched.as("premium"))
        .defaultBranch(Branched.as("standard"));

    branches.get("order-vip").to("vip-orders");
    branches.get("order-premium").to("premium-orders");
    branches.get("order-standard").to("standard-orders");

    return orders;
}
```

**흐름**:
```
orders (모든 주문)
  ↓ split + branch
  ├─ vip-orders (amount >= 100만원)
  ├─ premium-orders (10만원 <= amount < 100만원)
  └─ standard-orders (amount < 10만원)
```

#### 패턴 5: peek (디버깅, 로깅)
```java
@Bean
public KStream<String, String> monitorOrders(StreamsBuilder builder) {
    KStream<String, String> orders = builder.stream("orders");

    orders
        .peek((key, value) -> log.info("Received: key={}, value={}", key, value))
        .filter((key, value) -> parseJson(value).get("amount").asDouble() >= 100000)
        .peek((key, value) -> log.info("Filtered: key={}, value={}", key, value))
        .mapValues(value -> {
            JsonNode order = parseJson(value);
            return ((ObjectNode) order).put("processed", true).toString();
        })
        .peek((key, value) -> log.info("Processed: key={}, value={}", key, value))
        .to("processed-orders");

    return orders;
}
```

**특징**: `peek`은 스트림을 변경하지 않고 중간 단계를 관찰 (디버깅/로깅 용도)

### 5. 실전 예제: 주문 처리 파이프라인

#### 요구사항
```
1. 주문 수신 (orders 토픽)
2. 금액 10만원 이상 필터링
3. VIP 고객 여부 확인 (외부 API 호출 시뮬레이션)
4. 환율 적용 (USD 추가)
5. 지역별 라우팅 (domestic/international)
```

#### 전체 코드
```java
@Configuration
@EnableKafkaStreams
@Slf4j
public class OrderProcessingTopology {
    private final ObjectMapper mapper = new ObjectMapper();

    @Bean
    public KStream<String, String> processOrders(StreamsBuilder builder) {
        KStream<String, String> orders = builder.stream("orders");

        // 1. 고액 주문만 필터링
        KStream<String, String> highValueOrders = orders
            .filter((key, value) -> {
                double amount = parseJson(value).get("amount").asDouble();
                return amount >= 100000;
            })
            .peek((key, value) -> log.info("High-value order: {}", value));

        // 2. VIP 확인 및 enrichment
        KStream<String, String> enrichedOrders = highValueOrders
            .mapValues(value -> {
                JsonNode order = parseJson(value);
                ObjectNode enriched = (ObjectNode) order;

                String customerId = order.get("customerId").asText();
                boolean isVip = checkVipStatus(customerId);

                enriched.put("isVip", isVip);
                enriched.put("amountUSD", order.get("amount").asDouble() / 1300.0);
                enriched.put("processedAt", System.currentTimeMillis());

                return enriched.toString();
            })
            .peek((key, value) -> log.info("Enriched: {}", value));

        // 3. 지역별 라우팅
        Map<String, KStream<String, String>> regionBranches = enrichedOrders
            .split(Named.as("region-"))
            .branch((key, value) -> {
                String country = parseJson(value).get("country").asText();
                return "KR".equals(country);
            }, Branched.as("domestic"))
            .defaultBranch(Branched.as("international"));

        regionBranches.get("region-domestic").to("domestic-orders");
        regionBranches.get("region-international").to("international-orders");

        return orders;
    }

    private JsonNode parseJson(String json) {
        try {
            return mapper.readTree(json);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private boolean checkVipStatus(String customerId) {
        // 실제로는 외부 API 호출 또는 캐시 조회
        return customerId.startsWith("VIP");
    }
}
```

#### 테스트 Producer
```java
@RestController
@RequiredArgsConstructor
public class OrderController {
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper mapper = new ObjectMapper();

    @PostMapping("/orders")
    public String createOrder(@RequestBody OrderRequest request) throws Exception {
        ObjectNode order = mapper.createObjectNode();
        order.put("orderId", UUID.randomUUID().toString());
        order.put("customerId", request.customerId());
        order.put("amount", request.amount());
        order.put("country", request.country());

        kafkaTemplate.send("orders", order.get("orderId").asText(), order.toString());
        return "Order sent: " + order;
    }
}

record OrderRequest(String customerId, double amount, String country) {}
```

### 6. 토폴로지 시각화

```
orders
  ↓
filter (amount >= 100000)
  ↓
mapValues (VIP 확인 + USD 변환)
  ↓
split + branch (country)
  ├─ domestic-orders (country == "KR")
  └─ international-orders (country != "KR")
```

**Kafka Streams 내부 표현**:
```
Topology:
   Sub-topology: 0
    Source: KSTREAM-SOURCE-0000000000 (topics: [orders])
      --> KSTREAM-FILTER-0000000001
    Processor: KSTREAM-FILTER-0000000001 (stores: [])
      --> KSTREAM-MAPVALUES-0000000002
      <-- KSTREAM-SOURCE-0000000000
    Processor: KSTREAM-MAPVALUES-0000000002 (stores: [])
      --> KSTREAM-BRANCH-0000000003
      <-- KSTREAM-FILTER-0000000001
    Processor: KSTREAM-BRANCH-0000000003 (stores: [])
      --> KSTREAM-BRANCHCHILD-0000000004, KSTREAM-BRANCHCHILD-0000000005
      <-- KSTREAM-MAPVALUES-0000000002
    Sink: KSTREAM-SINK-0000000006 (topic: domestic-orders)
      <-- KSTREAM-BRANCHCHILD-0000000004
    Sink: KSTREAM-SINK-0000000007 (topic: international-orders)
      <-- KSTREAM-BRANCHCHILD-0000000005
```

확인 방법:
```java
@Bean
public KStream<String, String> topology(StreamsBuilder builder) {
    // ... topology 정의 ...

    Topology topology = builder.build();
    log.info("Topology:\n{}", topology.describe());

    return stream;
}
```

### 7. 운영 명령어

#### 토픽 생성
```bash
docker exec -it redpanda rpk topic create orders high-value-orders \
  enriched-orders domestic-orders international-orders \
  -p 3
```

#### 메시지 전송 테스트
```bash
# 국내 고액 주문
curl -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId": "VIP001", "amount": 150000, "country": "KR"}'

# 해외 고액 주문
curl -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId": "NORMAL002", "amount": 200000, "country": "US"}'

# 저액 주문 (필터링됨)
curl -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId": "NORMAL003", "amount": 50000, "country": "KR"}'
```

#### 결과 확인
```bash
# domestic-orders 확인
docker exec -it redpanda rpk topic consume domestic-orders --format '%v\n'

# international-orders 확인
docker exec -it redpanda rpk topic consume international-orders --format '%v\n'
```

### 8. 에러 처리

#### 역직렬화 에러 처리
```yaml
spring:
  kafka:
    streams:
      properties:
        default.deserialization.exception.handler: org.apache.kafka.streams.errors.LogAndContinueExceptionHandler
```

옵션:
- `LogAndFailExceptionHandler` (기본): 에러 시 애플리케이션 종료
- `LogAndContinueExceptionHandler`: 에러 로깅 후 다음 메시지 처리
- Custom Handler: DLQ로 전송

#### Custom Exception Handler
```java
public class DlqDeserializationExceptionHandler implements DeserializationExceptionHandler {
    private KafkaTemplate<String, String> dlqTemplate;

    @Override
    public DeserializationHandlerResponse handle(ProcessorContext context,
                                                  ConsumerRecord<byte[], byte[]> record,
                                                  Exception exception) {
        log.error("Deserialization error: {}", exception.getMessage());

        String dlqTopic = context.topic() + ".DLT";
        dlqTemplate.send(dlqTopic, new String(record.key()), new String(record.value()));

        return DeserializationHandlerResponse.CONTINUE;
    }
}
```

### 9. 스케일링

#### 인스턴스 추가
```bash
# 애플리케이션을 여러 인스턴스로 실행 (같은 application-id)
java -jar order-processor.jar --server.port=8081
java -jar order-processor.jar --server.port=8082
java -jar order-processor.jar --server.port=8083
```

**자동 파티션 할당**:
```
orders (파티션 3개)
├── Instance 1 → 파티션 0
├── Instance 2 → 파티션 1
└── Instance 3 → 파티션 2
```

#### 리밸런싱 모니터링
```java
@Bean
public StreamsBuilderFactoryBeanConfigurer configurer() {
    return fb -> fb.setStateListener((newState, oldState) -> {
        log.info("Kafka Streams state change: {} -> {}", oldState, newState);
        if (newState == KafkaStreams.State.REBALANCING) {
            log.warn("Rebalancing in progress...");
        }
    });
}
```

### 10. 실습 체크리스트

```
□ docker-compose up -d
□ 토픽 생성 (orders, high-value-orders, enriched-orders, domestic-orders, international-orders)
□ Spring Boot 애플리케이션 실행
□ 로그에서 Topology 확인
□ 여러 주문 전송 (고액/저액, 국내/해외)
□ Console에서 각 토픽 메시지 확인
□ 저액 주문이 high-value-orders에 없는지 확인
□ domestic-orders에 country=KR만 있는지 확인
□ 애플리케이션 재시작 → 중단 없이 처리 재개 확인
```

### 11. 참고 자료
- [Kafka Streams DSL](https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html)
- [Spring Kafka Streams](https://docs.spring.io/spring-kafka/reference/streams.html)
- [Redpanda Kafka Streams](https://docs.redpanda.com/current/develop/kafka-clients/)
