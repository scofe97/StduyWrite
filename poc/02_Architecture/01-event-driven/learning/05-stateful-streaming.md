# 05. Stateful Streaming (상태 기반 스트림 처리)

KTable, State Store, Windowing, Stream-Table Join, Aggregate

이벤트 스트림에서 집계, 조인, 윈도우 연산을 하려면 상태(State)가 필요하다. Kafka Streams의 State Store는 이를 로컬에서 처리하면서도 장애 복구를 지원한다.

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- KTable과 KStream의 차이를 이해하고 적절히 선택할 수 있다
- 윈도우 연산(Tumbling, Hopping, Session)을 실무에 적용할 수 있다
- State Store의 동작 원리와 Interactive Query를 이해한다

---

## 구성:

### 1. Stateful vs Stateless

#### Stateless (03장)
```
특징:
├── 메시지 하나만 보고 처리
├── 이전 메시지 기억 안 함
├── State Store 불필요
└── 예: filter, map, flatMap

장점: 단순, 빠름, 스케일링 쉬움
단점: 집계, 조인 불가
```

#### Stateful (이번 장)
```
특징:
├── 여러 메시지를 모아서 처리
├── State Store에 상태 저장 (RocksDB)
├── 복구 가능 (Changelog 토픽)
└── 예: aggregate, count, join, windowing

장점: 집계, 조인, 윈도우 연산 가능
단점: 복잡, 느림, State Store 관리 필요
```

### 2. State Store 아키텍처

```
┌──────────────┐
│ Application  │
│   Instance   │
└──────┬───────┘
       │
       ↓
┌─────────────────────┐
│   State Store       │ ← 로컬 디스크 (RocksDB)
│ (orderId → count)   │
└─────────┬───────────┘
          │ 변경사항 기록
          ↓
┌─────────────────────┐
│ Changelog Topic     │ ← Redpanda 토픽
│ (복구용 로그)        │
└─────────────────────┘

리밸런싱 시:
1. 새 인스턴스가 파티션 할당받음
2. Changelog 토픽에서 상태 복구
3. 처리 재개
```

**핵심**: State Store는 로컬 캐시 + Changelog 토픽 조합 (복구 가능, 내결함성)

### 3. KTable vs KStream

| 구분 | KStream | KTable |
|------|---------|--------|
| 의미 | 이벤트 스트림 (Append-Only) | 변경 로그 (Update) |
| 메시지 | 각 메시지가 독립적 이벤트 | 각 메시지가 상태 업데이트 |
| 키 중복 | 모두 독립적 처리 | 최신 값으로 덮어씀 |
| 예시 | 주문 생성 이벤트 | 사용자 프로필 (최신 상태) |

#### 예제 비교
```
입력 메시지 (키 → 값):
user1 → {"name": "Alice", "age": 25}
user2 → {"name": "Bob", "age": 30}
user1 → {"name": "Alice", "age": 26}

KStream 처리 (3개 메시지 모두 독립):
user1: Alice, 25
user2: Bob, 30
user1: Alice, 26

KTable 처리 (키별 최신 값만):
user1: Alice, 26
user2: Bob, 30
```

### 4. 기본 Aggregate 예제

#### 요구사항: 고객별 총 주문 금액 계산

```java
@Configuration
@EnableKafkaStreams
@Slf4j
public class CustomerAggregateTopology {
    private final ObjectMapper mapper = new ObjectMapper();

    @Bean
    public KStream<String, String> aggregateOrders(StreamsBuilder builder) {
        // KStream (주문 이벤트)
        KStream<String, String> orders = builder.stream("orders");

        // customerId를 키로 재배치 (원래 키는 orderId)
        KStream<String, String> ordersByCustomer = orders
            .selectKey((orderId, orderJson) -> {
                JsonNode order = parseJson(orderJson);
                return order.get("customerId").asText();
            });

        // KTable (고객별 총 금액)
        KTable<String, Double> totalByCustomer = ordersByCustomer
            .groupByKey()
            .aggregate(
                () -> 0.0,  // 초기값
                (customerId, orderJson, currentTotal) -> {
                    JsonNode order = parseJson(orderJson);
                    double amount = order.get("amount").asDouble();
                    double newTotal = currentTotal + amount;
                    log.info("Customer {}: {} + {} = {}", customerId, currentTotal, amount, newTotal);
                    return newTotal;
                },
                Materialized.<String, Double, KeyValueStore<Bytes, byte[]>>as("customer-totals")
                    .withKeySerde(Serdes.String())
                    .withValueSerde(Serdes.Double())
            );

        // KTable을 KStream으로 변환하여 출력 토픽에 전송
        totalByCustomer.toStream().to("customer-totals",
            Produced.with(Serdes.String(), Serdes.Double()));

        return orders;
    }

    private JsonNode parseJson(String json) {
        try {
            return mapper.readTree(json);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
```

**흐름**:
```
orders (orderId → order)
  ↓ selectKey (customerId로 재배치)
ordersByCustomer (customerId → order)
  ↓ groupByKey + aggregate
customer-totals (customerId → totalAmount)

예:
C001 → 100000
C001 → 50000  → C001: 150000
C002 → 200000 → C002: 200000
C001 → 30000  → C001: 180000
```

### 5. Interactive Queries (State Store 조회)

```java
@RestController
@RequiredArgsConstructor
public class CustomerStatsController {
    private final StreamsBuilderFactoryBean factoryBean;

    @GetMapping("/customers/{customerId}/total")
    public ResponseEntity<Double> getCustomerTotal(@PathVariable String customerId) {
        KafkaStreams streams = factoryBean.getKafkaStreams();
        if (streams == null) {
            return ResponseEntity.status(503).build();
        }

        ReadOnlyKeyValueStore<String, Double> store =
            streams.store(StoreQueryParameters.fromNameAndType(
                "customer-totals",
                QueryableStoreTypes.keyValueStore()
            ));

        Double total = store.get(customerId);
        if (total == null) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(total);
    }

    @GetMapping("/customers")
    public Map<String, Double> getAllCustomers() {
        KafkaStreams streams = factoryBean.getKafkaStreams();
        ReadOnlyKeyValueStore<String, Double> store =
            streams.store(StoreQueryParameters.fromNameAndType(
                "customer-totals",
                QueryableStoreTypes.keyValueStore()
            ));

        Map<String, Double> result = new HashMap<>();
        store.all().forEachRemaining(kv -> result.put(kv.key, kv.value));
        return result;
    }
}
```

**테스트**:
```bash
# 주문 전송
curl -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId": "C001", "amount": 100000}'

# 총액 조회
curl http://localhost:8080/customers/C001/total
# 응답: 100000.0
```

### 6. Windowing (시간 기반 집계)

#### Tumbling Window (고정 윈도우)
```java
@Bean
public KStream<String, String> tumblingWindowAggregate(StreamsBuilder builder) {
    KStream<String, String> orders = builder.stream("orders");

    KTable<Windowed<String>, Long> orderCountsPer5Min = orders
        .selectKey((orderId, orderJson) -> parseJson(orderJson).get("customerId").asText())
        .groupByKey()
        .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
        .count(Materialized.as("order-counts-5min"));

    orderCountsPer5Min.toStream()
        .map((windowedKey, count) -> {
            String key = windowedKey.key();
            long start = windowedKey.window().start();
            long end = windowedKey.window().end();
            String value = String.format("{\"customerId\":\"%s\",\"count\":%d,\"windowStart\":%d,\"windowEnd\":%d}",
                key, count, start, end);
            return KeyValue.pair(key, value);
        })
        .to("order-counts-5min");

    return orders;
}
```

**Tumbling Window 특징**:
```
시간: 00:00 ~ 00:05 ~ 00:10 ~ 00:15
      [----W1----][----W2----][----W3----]

특징:
- 윈도우 크기 고정 (5분)
- 윈도우 간 겹침 없음
- 각 메시지는 하나의 윈도우에만 속함
```

#### Hopping Window (겹침 있는 고정 윈도우)
```java
@Bean
public KStream<String, String> hoppingWindowAggregate(StreamsBuilder builder) {
    KStream<String, String> orders = builder.stream("orders");

    KTable<Windowed<String>, Long> orderCountsHopping = orders
        .selectKey((orderId, orderJson) -> parseJson(orderJson).get("customerId").asText())
        .groupByKey()
        .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(10))
                               .advanceBy(Duration.ofMinutes(5)))
        .count(Materialized.as("order-counts-hopping"));

    // ... (toStream 생략)
    return orders;
}
```

**Hopping Window 특징**:
```
시간: 00:00 ~ 00:05 ~ 00:10 ~ 00:15
      [------W1------]
            [------W2------]
                  [------W3------]

특징:
- 윈도우 크기: 10분
- Advance: 5분 (윈도우가 5분마다 시작)
- 각 메시지는 여러 윈도우에 속함 (겹침)
```

#### Session Window (이벤트 기반 윈도우)
```java
@Bean
public KStream<String, String> sessionWindowAggregate(StreamsBuilder builder) {
    KStream<String, String> orders = builder.stream("orders");

    KTable<Windowed<String>, Long> sessions = orders
        .selectKey((orderId, orderJson) -> parseJson(orderJson).get("customerId").asText())
        .groupByKey()
        .windowedBy(SessionWindows.ofInactivityGapWithNoGrace(Duration.ofMinutes(30)))
        .count(Materialized.as("order-sessions"));

    // ... (toStream 생략)
    return orders;
}
```

**Session Window 특징**:
```
이벤트:  E1   E2        E3        E4   E5
시간:    10:00 10:05    10:40     11:00 11:10
                ↑ 35분 gap (세션 종료)

결과:
Session 1: [E1, E2] (10:00 ~ 10:05, count=2)
Session 2: [E3] (10:40, count=1)
Session 3: [E4, E5] (11:00 ~ 11:10, count=2)

특징:
- 고정된 크기 없음
- Inactivity Gap (비활성 기간)으로 세션 종료
- 사용자 세션 분석에 적합
```

### 7. Stream-Table Join

#### Inner Join (사용자 정보 enrichment)
```java
@Bean
public KStream<String, String> enrichOrdersWithUserInfo(StreamsBuilder builder) {
    // KStream: 주문 이벤트
    KStream<String, String> orders = builder.stream("orders");

    // KTable: 사용자 프로필 (최신 상태)
    KTable<String, String> users = builder.table("users");

    // Join: customerId로 조인
    KStream<String, String> enrichedOrders = orders
        .selectKey((orderId, orderJson) -> parseJson(orderJson).get("customerId").asText())
        .join(users,
            (orderJson, userJson) -> {
                JsonNode order = parseJson(orderJson);
                JsonNode user = parseJson(userJson);

                ObjectNode enriched = mapper.createObjectNode();
                enriched.set("order", order);
                enriched.set("user", user);
                enriched.put("enrichedAt", System.currentTimeMillis());

                return enriched.toString();
            });

    enrichedOrders.to("enriched-orders");
    return orders;
}
```

**흐름**:
```
orders (orderId → {customerId: C001, amount: 100000})
  ↓ selectKey (customerId로 재배치)
orders (C001 → {customerId: C001, amount: 100000})
  ↓ join with users (C001 → {name: "Alice", email: "alice@example.com"})
enriched-orders ({order: {...}, user: {...}})
```

#### Left Join (사용자 정보 없어도 처리)
```java
KStream<String, String> enrichedOrders = orders
    .selectKey((orderId, orderJson) -> parseJson(orderJson).get("customerId").asText())
    .leftJoin(users,
        (orderJson, userJson) -> {
            JsonNode order = parseJson(orderJson);
            ObjectNode enriched = mapper.createObjectNode();
            enriched.set("order", order);

            if (userJson != null) {
                enriched.set("user", parseJson(userJson));
            } else {
                enriched.putNull("user");
            }

            return enriched.toString();
        });
```

### 8. GlobalKTable (모든 파티션 데이터 복제)

```java
@Bean
public KStream<String, String> enrichWithProduct(StreamsBuilder builder) {
    KStream<String, String> orders = builder.stream("orders");

    // GlobalKTable: 모든 인스턴스가 전체 products 데이터 보유
    GlobalKTable<String, String> products = builder.globalTable("products");

    KStream<String, String> enrichedOrders = orders
        .join(products,
            (orderId, orderJson) -> parseJson(orderJson).get("productId").asText(),  // Foreign Key
            (orderJson, productJson) -> {
                JsonNode order = parseJson(orderJson);
                JsonNode product = parseJson(productJson);

                ObjectNode enriched = mapper.createObjectNode();
                enriched.set("order", order);
                enriched.set("product", product);

                return enriched.toString();
            });

    enrichedOrders.to("enriched-orders");
    return orders;
}
```

**GlobalKTable vs KTable**:
```
KTable:
- 파티션별 분산 (각 인스턴스가 일부 데이터만 보유)
- Join 시 키가 같은 파티션에 있어야 함 (Co-partitioning 필요)
- 메모리 효율적

GlobalKTable:
- 모든 인스턴스가 전체 데이터 보유 (복제)
- Join 시 키가 달라도 됨 (Foreign Key Join 가능)
- 메모리 사용량 높음 (작은 테이블만 사용)
```

### 9. Co-partitioning (파티션 정렬)

#### 문제 상황
```
orders (파티션 3개, 키: orderId)
  ├─ P0: order1, order4
  ├─ P1: order2, order5
  └─ P2: order3, order6

users (파티션 3개, 키: userId)
  ├─ P0: user1, user3
  ├─ P1: user2
  └─ P2: user4, user5

❌ 조인 불가: orderId와 userId가 다른 파티션에 있음
```

#### 해결: 재파티셔닝
```java
KStream<String, String> orders = builder.stream("orders");

// customerId로 재배치 (through = 중간 토픽 생성 + 재파티셔닝)
KStream<String, String> ordersByCustomer = orders
    .selectKey((orderId, orderJson) -> parseJson(orderJson).get("customerId").asText())
    .through("orders-by-customer",
        Produced.with(Serdes.String(), Serdes.String()));

KTable<String, String> users = builder.table("users");

// 이제 조인 가능 (같은 키, 같은 파티션 수)
KStream<String, String> enrichedOrders = ordersByCustomer.join(users, ...);
```

**Co-partitioning 요구사항**:
```
1. 같은 파티션 수
2. 같은 키
3. 같은 파티셔닝 전략 (기본: Murmur2)
```

### 10. 실전 예제: 실시간 대시보드

#### 요구사항
```
1. 최근 5분간 고객별 주문 수
2. 최근 5분간 총 주문 금액
3. VIP 고객 실시간 주문 모니터링
```

#### 전체 코드
```java
@Configuration
@EnableKafkaStreams
@Slf4j
public class DashboardTopology {
    private final ObjectMapper mapper = new ObjectMapper();

    @Bean
    public KStream<String, String> buildDashboard(StreamsBuilder builder) {
        KStream<String, String> orders = builder.stream("orders");
        KTable<String, String> users = builder.table("users");

        // 1. 최근 5분간 고객별 주문 수
        KTable<Windowed<String>, Long> orderCountsPer5Min = orders
            .selectKey((orderId, orderJson) -> parseJson(orderJson).get("customerId").asText())
            .groupByKey()
            .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
            .count(Materialized.as("order-counts-5min"));

        orderCountsPer5Min.toStream().to("dashboard-order-counts");

        // 2. 최근 5분간 총 주문 금액
        KTable<Windowed<String>, Double> totalAmountPer5Min = orders
            .groupBy((orderId, orderJson) -> "total",
                Grouped.with(Serdes.String(), Serdes.String()))
            .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
            .aggregate(
                () -> 0.0,
                (key, orderJson, total) -> {
                    double amount = parseJson(orderJson).get("amount").asDouble();
                    return total + amount;
                },
                Materialized.with(Serdes.String(), Serdes.Double())
            );

        totalAmountPer5Min.toStream().to("dashboard-total-amount");

        // 3. VIP 고객 실시간 주문 (Join)
        KStream<String, String> vipOrders = orders
            .selectKey((orderId, orderJson) -> parseJson(orderJson).get("customerId").asText())
            .join(users,
                (orderJson, userJson) -> {
                    JsonNode user = parseJson(userJson);
                    if ("VIP".equals(user.get("tier").asText())) {
                        ObjectNode alert = mapper.createObjectNode();
                        alert.set("order", parseJson(orderJson));
                        alert.set("user", user);
                        alert.put("alertType", "VIP_ORDER");
                        alert.put("timestamp", System.currentTimeMillis());
                        return alert.toString();
                    }
                    return null;
                })
            .filter((customerId, alert) -> alert != null);

        vipOrders.to("dashboard-vip-alerts");

        return orders;
    }

    private JsonNode parseJson(String json) {
        try {
            return mapper.readTree(json);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
```

### 11. 운영 체크리스트

```
□ State Store 디스크 공간 모니터링 (RocksDB 크기)
□ Changelog 토픽 보관 주기 설정 (log.retention.ms)
□ 리밸런싱 시간 측정 (State Store 복구 시간)
□ Interactive Query 응답 시간 모니터링
□ 윈도우 크기 최적화 (메모리 사용량 vs 정확도)
□ Co-partitioning 검증 (파티션 수, 키 일치)
□ Changelog 토픽 압축 설정 (cleanup.policy=compact)
```

### 12. 트러블슈팅

#### State Store 복구 느림
```
원인: Changelog 토픽이 너무 큼
해결:
1. standby.replicas 설정 (대기 복제본)
2. State Store 크기 줄이기 (retention 설정)
3. 파티션 수 증가 (병렬 복구)
```

#### 메모리 부족
```
원인: 너무 큰 윈도우, 너무 많은 키
해결:
1. 윈도우 크기 줄이기
2. 힙 메모리 증가 (-Xmx)
3. RocksDB 캐시 조정 (rocksdb.config.setter)
```

#### Co-partitioning 에러
```
Error: Partition counts for topics [orders, users] don't match
원인: 파티션 수 불일치
해결: rpk topic alter-config로 파티션 수 맞추기 (단, 기존 데이터 영향)
```

### 13. 참고 자료
- [Kafka Streams Stateful Operations](https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#stateful-transformations)
- [Kafka Streams Windowing](https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#windowing)
- [Interactive Queries](https://kafka.apache.org/documentation/streams/developer-guide/interactive-queries.html)
