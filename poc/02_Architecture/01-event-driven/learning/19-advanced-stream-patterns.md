# 19. 고급 스트림 처리 패턴 (Advanced Stream Processing)

Confluent 공식 패턴 8가지: Event Time, Suppressed Aggregation, Stream Merger, Wait-for-N, Logical AND, Projection Table, State Table을 Kafka Streams DSL로 구현한다.

03장(무상태)과 04장(기본 상태)을 마쳤다면 이 장이 마지막 퍼즐 조각이다. 실무에서 마주치는 "복잡한 스트림 문제"는 대부분 여기서 다루는 패턴 중 하나로 해결된다.

---

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- Event Time vs Wall Clock Time의 차이와 워터마크 개념을 이해하고 TimestampExtractor를 직접 구현할 수 있다
- Suppressed Aggregation으로 중간 결과를 억제하여 다운스트림 부하를 줄이는 기법을 설명할 수 있다
- Event Stream Merger로 여러 소스를 통합할 때 고려해야 할 스키마 통일·순서 보장 문제를 파악한다
- Wait-for-N-Events와 Logical AND 패턴의 차이를 구분하고, 각각 어떤 상황에 적용해야 하는지 판단할 수 있다
- Projection Table과 State Table의 차이를 설명하고, CQRS 아키텍처에서의 역할을 연결할 수 있다

---

## 1. Event Time vs Wall Clock Time

### 1.1 세 가지 시간의 정의

스트림 처리에서 "이 이벤트는 언제 발생했는가?"라는 질문에 대한 답이 세 가지다. 왜 하나가 아닌가? 네트워크 지연, 시스템 장애, 배치 업로드가 존재하기 때문이다. 실제로 모바일 앱은 오프라인 상태에서도 이벤트를 기록하고, 네트워크가 복구된 후 한꺼번에 전송한다. 이때 이벤트가 처리된 시간(Processing Time)을 기준으로 집계하면 사용자의 실제 행동 패턴을 왜곡하게 된다.

```
Event Time     : 이벤트가 실제로 발생한 시점 (레코드에 담긴 타임스탬프)
                 예) 사용자가 오후 3시에 클릭한 이벤트 → timestamp=15:00:00

Ingestion Time : 이벤트가 Kafka 브로커에 도착한 시점
                 예) 네트워크 지연으로 오후 3시 5분에 브로커에 도착 → 15:05:00

Processing Time: 스트림 애플리케이션이 이벤트를 실제 처리한 시점
                 예) 컨슈머가 처리한 시점 → 15:06:00
```

시간 불일치가 발생하는 원인:
```
이벤트 발생 (15:00)
    │
    ├── 모바일 오프라인 → 로컬 큐 저장 (30분 후 전송)
    │
    ├── 네트워크 지연 → 브로커 도착 지연 (수 초 ~ 수 분)
    │
    └── 컨슈머 처리 지연 → 큐 쌓임 (장애 복구 후 재처리)
```

### 1.2 Kafka의 타임스탬프 추출

Kafka Streams는 `TimestampExtractor` 인터페이스를 통해 레코드의 타임스탬프를 결정한다. 기본 구현체는 두 가지다.

```java
// 기본값: 레코드 헤더의 CreateTime 사용 (Event Time에 가장 가까움)
// Kafka Producer가 메시지 생성 시 자동으로 기록
props.put(StreamsConfig.DEFAULT_TIMESTAMP_EXTRACTOR_CLASS_CONFIG,
          FailOnInvalidTimestamp.class);

// Wall Clock Time 사용 (Processing Time)
// 이벤트 발생 시점보다 처리 시점이 중요한 경우
props.put(StreamsConfig.DEFAULT_TIMESTAMP_EXTRACTOR_CLASS_CONFIG,
          WallclockTimestampExtractor.class);
```

실무에서는 이벤트 페이로드 안에 있는 타임스탬프를 사용해야 하는 경우가 많다. 예를 들어, 모바일 앱이 이벤트 발생 시각을 JSON 필드에 넣어 전송한다면 커스텀 추출기를 구현해야 한다.

```java
// 커스텀 TimestampExtractor: JSON 페이로드의 eventTime 필드 추출
public class EventTimeExtractor implements TimestampExtractor {

    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    public long extract(ConsumerRecord<Object, Object> record, long partitionTime) {
        if (record.value() instanceof String json) {
            try {
                JsonNode node = mapper.readTree(json);
                if (node.has("eventTime")) {
                    // ISO-8601 형식 → epoch milliseconds 변환
                    return Instant.parse(node.get("eventTime").asText())
                                  .toEpochMilli();
                }
            } catch (Exception e) {
                // 파싱 실패 시 파티션 타임으로 폴백
                return partitionTime;
            }
        }
        return partitionTime;  // 폴백: 파티션 내 마지막 유효 타임스탬프
    }
}

// 설정 적용
props.put(StreamsConfig.DEFAULT_TIMESTAMP_EXTRACTOR_CLASS_CONFIG,
          EventTimeExtractor.class);
```

### 1.3 워터마크와 Grace Period

워터마크(Watermark)란 "이 시간 이전의 모든 이벤트가 도착했다"는 선언이다. 왜 필요한가? 스트림은 무한하기 때문에 "언제 윈도우를 닫을지"를 알 수 없다. 이벤트가 항상 순서대로 도착한다면 문제가 없지만, 늦게 도착하는 이벤트(Late Event)가 존재하면 이미 닫힌 윈도우에 데이터를 추가해야 할지 결정해야 한다.

Kafka Streams에서는 Grace Period가 워터마크 역할을 한다. 윈도우 종료 후 Grace Period 동안은 늦게 도착한 이벤트를 허용하고, 그 이후는 무시한다.

```
타임라인 (Event Time 기준):
──────────────────────────────────────────────────────────────►

│←─── 5분 Tumbling Window ───→│  Grace: 1분  │  이후 무시
                                              │
14:00                        14:05          14:06
  │                            │              │
  │  이벤트 A (14:02)          │              │
  │  이벤트 B (14:04)          │              │
  │                            │  윈도우 닫힘  │
  │                       이벤트 C (14:05:30) │ → 허용 (Grace 내)
  │                                     이벤트 D (14:06:30) → 무시
```

```java
// Grace Period 적용 예시
KStream<String, OrderEvent> orders = builder.stream("orders",
    Consumed.with(Serdes.String(), orderSerde)
            .withTimestampExtractor(new EventTimeExtractor()));

KTable<Windowed<String>, Long> windowedCounts = orders
    .groupByKey()
    .windowedBy(
        TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5))
                   .grace(Duration.ofMinutes(1))  // 1분간 늦은 이벤트 허용
    )
    .count(Materialized.as("order-counts"));
```

늦게 도착하는 이벤트 처리 전략은 세 가지다. 첫째, Grace Period로 일정 시간 기다린다(기본 전략). 둘째, 늦은 이벤트를 별도 토픽으로 라우팅하여 배치로 재처리한다. 셋째, 늦은 이벤트를 무시하고 SLA를 허용 오차로 정의한다. 실무에서는 첫 번째와 두 번째를 조합하는 경우가 많다.

---

## 2. Event Stream Merger

### 2.1 왜 필요한가

같은 도메인 개념이 여러 소스에서 이벤트로 발생하는 경우가 있다. 예를 들어, 주문(Order)은 웹 채널, 모바일 앱, 오프라인 POS에서 각각 생성될 수 있다. 다운스트림 처리 로직은 소스를 구분하지 않고 "주문 이벤트"를 하나의 스트림으로 다루고 싶어한다. 이때 Event Stream Merger 패턴을 사용한다.

또 다른 사례는 레거시 마이그레이션이다. 구 시스템과 신 시스템이 동시에 이벤트를 발행하는 전환 기간에, 두 스트림을 합쳐서 단일 소비자가 처리하도록 구성할 수 있다.

### 2.2 Kafka Streams 구현

```java
@Configuration
public class OrderEventMergerTopology {

    @Bean
    public Topology buildTopology(StreamsBuilder builder) {
        // 세 개의 소스 토픽
        KStream<String, OrderEvent> webOrders =
            builder.stream("orders-web",
                Consumed.with(Serdes.String(), orderEventSerde));

        KStream<String, OrderEvent> mobileOrders =
            builder.stream("orders-mobile",
                Consumed.with(Serdes.String(), orderEventSerde));

        KStream<String, OrderEvent> posOrders =
            builder.stream("orders-pos",
                Consumed.with(Serdes.String(), orderEventSerde));

        // 방법 1: merge() 체이닝 (2개씩 병합)
        KStream<String, OrderEvent> allOrders =
            webOrders.merge(mobileOrders).merge(posOrders);

        // 방법 2: StreamsBuilder.stream(List) - 다중 토픽 동시 구독
        // 스키마가 동일한 경우 더 간결
        KStream<String, OrderEvent> allOrdersV2 = builder.stream(
            List.of("orders-web", "orders-mobile", "orders-pos"),
            Consumed.with(Serdes.String(), orderEventSerde)
        );

        // 머지된 스트림을 단일 토픽으로 출력
        allOrders.to("orders-unified",
            Produced.with(Serdes.String(), orderEventSerde));

        return builder.build();
    }
}
```

### 2.3 머지 시 핵심 고려사항

**스키마 통일**: 서로 다른 소스가 같은 필드를 다른 이름으로 부를 수 있다. 머지 전에 각 소스별 변환(map)을 통해 공통 스키마로 정규화해야 한다.

```java
// 소스별 스키마 차이 처리: POS 시스템은 'amount' 대신 'total' 필드를 사용
KStream<String, OrderEvent> normalizedPosOrders = posOrders
    .mapValues(posEvent -> OrderEvent.builder()
        .orderId(posEvent.getReceiptId())      // 필드명 다름
        .amount(posEvent.getTotal())            // 필드명 다름
        .channel("POS")
        .eventTime(posEvent.getCreatedAt())
        .build());
```

**순서 보장의 한계**: 머지 후에는 파티션 내 순서만 보장된다. 토픽 A의 이벤트와 토픽 B의 이벤트 사이의 순서는 보장되지 않는다. 따라서 머지된 스트림에서 이벤트 순서에 의존하는 로직(예: "첫 번째 주문 감지")은 Event Time 정렬이나 별도의 상태 관리가 필요하다.

**중복 제거**: 동일 이벤트가 여러 토픽에 동시 발행되는 경우, 머지 후 중복이 발생할 수 있다. 이때는 State Store에 이벤트 ID를 저장하고 중복을 걸러내는 Deduplication 로직이 필요하다(17장 멱등성 패턴 참고).

---

## 3. Suppressed Event Aggregator

### 3.1 문제: 중간 결과의 폭발

Kafka Streams의 윈도우 집계는 기본적으로 이벤트가 도착할 때마다 중간 결과를 출력한다. 5분 윈도우 동안 이벤트가 1,000개 들어오면 결과 토픽에 1,000개의 중간 집계 결과가 쌓인다. 왜 이게 문제인가? 다운스트림 컨슈머는 "최종 집계 결과" 하나만 필요한데, 999개의 불필요한 메시지를 처리해야 하기 때문이다. 이는 불필요한 CPU 사용, 네트워크 트래픽, 다운스트림 시스템 부하를 유발한다.

```
suppress 없음:
이벤트 도착 → 중간 결과 출력 → 이벤트 도착 → 중간 결과 출력 → ... → 윈도우 닫힘 → 최종 결과

suppress 있음:
이벤트 도착 → (내부 상태만 업데이트) → ... → 윈도우 닫힘 → 최종 결과만 출력
```

### 3.2 Suppressed 구현

```java
@Bean
public Topology salesAggregationTopology(StreamsBuilder builder) {

    KStream<String, SaleEvent> sales = builder.stream("sales-events",
        Consumed.with(Serdes.String(), saleSerde));

    KTable<Windowed<String>, Double> windowedSales = sales
        .groupBy((key, sale) -> sale.getProductCategory(),
                 Grouped.with(Serdes.String(), saleSerde))
        .windowedBy(
            TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5))
                       .grace(Duration.ofSeconds(30))
        )
        .aggregate(
            () -> 0.0,
            (category, sale, total) -> total + sale.getAmount(),
            Materialized.<String, Double, WindowStore<Bytes, byte[]>>as("sales-store")
                        .withValueSerde(Serdes.Double())
        )
        // 핵심: 윈도우가 완전히 닫힐 때까지 중간 결과 억제
        .suppress(
            Suppressed.untilWindowCloses(
                // 메모리 버퍼 설정: 100만 레코드 또는 50MB 초과 시 조기 방출
                Suppressed.BufferConfig
                          .maxRecords(1_000_000)
                          .withMaxBytes(50 * 1024 * 1024)
                          .emitEarlyWhenFull()  // 버퍼 초과 시 억제 해제, 조기 방출
            )
        );

    // 억제 후에는 윈도우 닫힐 때 한 번만 출력
    windowedSales
        .toStream()
        .map((windowedKey, total) -> KeyValue.pair(
            windowedKey.key() + "@" + windowedKey.window().startTime(),
            total
        ))
        .to("sales-aggregated-final",
            Produced.with(Serdes.String(), Serdes.Double()));

    return builder.build();
}
```

### 3.3 suppress 없을 때 vs 있을 때 출력 비교

```
입력 이벤트 (5분 윈도우, 카테고리: "electronics"):
  14:01:00 - sale(100)
  14:02:00 - sale(200)
  14:03:00 - sale(150)
  14:05:30 - 윈도우 닫힘 (Grace 30초 포함)

suppress 없음 → 출력 토픽:
  {key="electronics@14:00", value=100.0}   ← 중간
  {key="electronics@14:00", value=300.0}   ← 중간
  {key="electronics@14:00", value=450.0}   ← 최종 (3개 메시지)

suppress 있음 → 출력 토픽:
  {key="electronics@14:00", value=450.0}   ← 최종만 (1개 메시지)
```

**트레이드오프**: suppress는 출력 지연(윈도우 종료까지 기다림)과 메모리 사용(버퍼)을 발생시킨다. 실시간 대시보드처럼 중간 결과가 필요한 경우에는 suppress를 사용하지 않는 것이 맞다. 알림 발송, 정산, 리포트 생성처럼 최종 결과만 필요한 경우에 적합하다.

### 3.4 BufferConfig 전략

```java
// 전략 1: 메모리 무제한 - OOM 위험, 작은 규모에서만 사용
Suppressed.BufferConfig.unbounded()

// 전략 2: 레코드 수 제한 - 초과 시 조기 방출 (suppress 부분 해제)
Suppressed.BufferConfig.maxRecords(500_000).emitEarlyWhenFull()

// 전략 3: 메모리 크기 제한 - 초과 시 예외 발생 (애플리케이션 중단)
// 완전한 억제가 비즈니스 요구사항인 경우
Suppressed.BufferConfig.maxBytes(100 * 1024 * 1024)  // emitEarlyWhenFull 없음
```

---

## 4. Wait-for-N-Events / Logical AND

### 4.1 Wait-for-N-Events

**패턴 정의**: 동일한 키에 대해 N개의 이벤트가 모두 도착했을 때 처리를 트리거한다. 왜 필요한가? 분산 시스템에서 "N개의 확인"을 모아야 의미 있는 처리가 가능한 경우가 있다. 예를 들어, 배치 주문 시스템은 100개의 개별 주문이 모두 확인된 후 배차를 요청한다.

```
구현 전략:
1. State Store에 키별 카운트 저장
2. 이벤트 도착 시 카운트 증가
3. 카운트 == N → 결과 출력 + 상태 초기화
4. 타임아웃(Punctuator) → N 미달 시 불완전 처리

State Store 구조:
  키: "batch-001"
  값: {count: 3, events: [...], firstSeen: 14:00:00}
```

```java
public class WaitForNEventsTransformer
    implements Transformer<String, OrderEvent, KeyValue<String, BatchResult>> {

    private static final int REQUIRED_COUNT = 5;
    private static final long TIMEOUT_MS = 5 * 60 * 1000L; // 5분

    private KeyValueStore<String, BatchState> stateStore;
    private ProcessorContext context;

    @Override
    public void init(ProcessorContext context) {
        this.context = context;
        this.stateStore = context.getStateStore("batch-state-store");

        // 타임아웃 체크: 30초마다 실행
        context.schedule(
            Duration.ofSeconds(30),
            PunctuationType.WALL_CLOCK_TIME,
            this::handleTimeout
        );
    }

    @Override
    public KeyValue<String, BatchResult> transform(String batchId, OrderEvent event) {
        BatchState state = stateStore.get(batchId);

        if (state == null) {
            state = new BatchState(context.currentSystemTimeMs());
        }

        state.addEvent(event);
        stateStore.put(batchId, state);

        // N개 도달 시 처리
        if (state.getCount() >= REQUIRED_COUNT) {
            stateStore.delete(batchId);
            return KeyValue.pair(batchId,
                BatchResult.complete(batchId, state.getEvents()));
        }

        return null; // 아직 N개 미달 → 출력 없음
    }

    private void handleTimeout(long currentTime) {
        // 전체 State Store 순회하여 타임아웃된 배치 처리
        try (KeyValueIterator<String, BatchState> iter = stateStore.all()) {
            while (iter.hasNext()) {
                KeyValue<String, BatchState> entry = iter.next();
                BatchState state = entry.value;

                if (currentTime - state.getFirstSeenMs() > TIMEOUT_MS) {
                    stateStore.delete(entry.key);
                    // 불완전하지만 타임아웃된 배치를 불완전 결과로 방출
                    context.forward(entry.key,
                        BatchResult.incomplete(entry.key, state.getEvents()));
                }
            }
        }
    }

    @Override
    public void close() {}
}

// 토폴로지에 적용
KStream<String, BatchResult> batchResults = orders
    .transform(
        () -> new WaitForNEventsTransformer(),
        "batch-state-store"  // State Store 이름 (별도로 addStateStore 필요)
    )
    .filter((key, value) -> value != null); // null 필터링
```

### 4.2 Logical AND

**패턴 정의**: 서로 다른 종류의 이벤트가 모두 도착했을 때 처리를 트리거한다. Wait-for-N과의 차이는 "동일 타입 N개" vs "다른 타입 N종"이다.

```
Wait-for-N:  order-event × 5개 → 처리
Logical AND: credit-check-event AND income-check-event AND asset-check-event → 처리
```

실제 사례: 대출 심사 시스템은 신용 조회, 소득 확인, 자산 평가 세 가지 이벤트가 모두 도착해야 최종 승인 여부를 결정할 수 있다. 각 이벤트는 서로 다른 외부 시스템에서 비동기로 발행된다.

```java
// Logical AND 상태 표현: 비트 플래그 사용
public class LoanCheckState {
    private static final int CREDIT_CHECK  = 0b001;
    private static final int INCOME_CHECK  = 0b010;
    private static final int ASSET_CHECK   = 0b100;
    private static final int ALL_COMPLETED = 0b111;

    private int flags = 0;
    private Map<String, CheckResult> results = new HashMap<>();

    public void setCreditCheck(CheckResult result) {
        this.flags |= CREDIT_CHECK;
        this.results.put("credit", result);
    }

    public void setIncomeCheck(CheckResult result) {
        this.flags |= INCOME_CHECK;
        this.results.put("income", result);
    }

    public void setAssetCheck(CheckResult result) {
        this.flags |= ASSET_CHECK;
        this.results.put("asset", result);
    }

    public boolean isAllCompleted() {
        return (flags & ALL_COMPLETED) == ALL_COMPLETED;
    }
}

// 각 이벤트 타입별 스트림 생성 후 State Store에서 상태 병합
public class LoanApprovalTransformer
    implements Transformer<String, LoanCheckEvent, KeyValue<String, LoanDecision>> {

    private KeyValueStore<String, LoanCheckState> stateStore;

    @Override
    public KeyValue<String, LoanDecision> transform(String loanId, LoanCheckEvent event) {
        LoanCheckState state = Optional.ofNullable(stateStore.get(loanId))
                                       .orElse(new LoanCheckState());

        // 이벤트 타입에 따라 해당 플래그 설정
        switch (event.getType()) {
            case "CREDIT_CHECK"  -> state.setCreditCheck(event.getResult());
            case "INCOME_CHECK"  -> state.setIncomeCheck(event.getResult());
            case "ASSET_CHECK"   -> state.setAssetCheck(event.getResult());
        }

        stateStore.put(loanId, state);

        if (state.isAllCompleted()) {
            stateStore.delete(loanId);
            // 세 가지 결과를 종합하여 최종 결정
            return KeyValue.pair(loanId, LoanDecision.from(state.getResults()));
        }

        return null; // 아직 일부 미도착
    }
}
```

**Logical AND 구현 시 중요 포인트**: 각 이벤트 타입이 서로 다른 토픽에 발행된다면 먼저 `merge()`로 통합하거나, 각 스트림을 동일한 Transformer에 라우팅해야 한다. 타임아웃 처리는 Wait-for-N과 동일하게 Punctuator를 사용한다.

---

## 5. Projection Table

### 5.1 개념: Materialized View의 스트림 버전

Projection Table은 이벤트 스트림으로부터 읽기 최적화된 뷰를 지속적으로 유지하는 패턴이다. 데이터베이스의 Materialized View가 쿼리 결과를 미리 계산하여 저장하는 것처럼, Projection Table은 이벤트를 처리하면서 "가장 최신 상태"를 Key-Value 형태로 유지한다.

왜 필요한가? 이벤트 소싱(15장) 시스템에서 현재 상태를 조회하려면 이벤트 히스토리를 처음부터 재생해야 하는데, 이는 조회 성능이 매우 나쁘다. Projection Table은 이 문제를 해결한다. 이벤트가 발생할 때마다 현재 상태를 업데이트하여, 조회 시에는 최신 스냅샷만 읽으면 된다.

```
이벤트 소싱 없이:
조회 요청 → 전체 이벤트 재생 → 현재 상태 계산 → 응답 (느림)

Projection Table 있음:
이벤트 발생 → Projection 업데이트 (비동기)
조회 요청 → Projection Table 조회 → 응답 (빠름)
```

### 5.2 CQRS에서의 역할

Projection Table은 CQRS(Command Query Responsibility Segregation)의 Query 측을 담당한다. 15장의 이벤트 소싱과 연계하면:

```
Command Side (쓰기):
  사용자 요청 → Command Handler → 이벤트 발행 → 이벤트 저장소

Query Side (읽기):
  이벤트 스트림 → Kafka Streams Topology → Projection Table (KTable)
  조회 요청 → Interactive Queries → Projection Table 조회 → 응답
```

### 5.3 KTable vs GlobalKTable

```
KTable:
├── 파티션별 상태 유지 (파티션 0 → 인스턴스 A, 파티션 1 → 인스턴스 B)
├── 스케일 아웃 가능 (파티션 수만큼 병렬)
├── 조인 시 동일 파티션끼리만 조인 (co-partitioning 필요)
└── 대규모 데이터에 적합

GlobalKTable:
├── 모든 인스턴스가 전체 데이터 보유 (복제)
├── 어떤 파티션의 KStream과도 조인 가능 (co-partitioning 불필요)
├── 메모리/디스크 사용량 N배 증가 (인스턴스 수만큼)
└── 소규모 참조 데이터 (lookup table)에 적합
```

### 5.4 구현: UserProfileProjection

```java
@Configuration
public class UserProfileProjectionTopology {

    @Bean
    public Topology buildTopology(StreamsBuilder builder) {

        // 사용자 이벤트 스트림 (생성, 수정, 이메일 변경 등)
        KStream<String, UserEvent> userEvents = builder.stream("user-events",
            Consumed.with(Serdes.String(), userEventSerde));

        // Projection Table: 최신 사용자 프로필 유지
        KTable<String, UserProfile> userProfiles = userEvents
            .groupByKey()
            .aggregate(
                UserProfile::empty,  // 초기값
                (userId, event, currentProfile) -> {
                    // 이벤트 타입에 따라 프로필 업데이트
                    return switch (event.getType()) {
                        case "USER_CREATED" -> UserProfile.from(event);
                        case "EMAIL_CHANGED" -> currentProfile.withEmail(event.getEmail());
                        case "NAME_CHANGED"  -> currentProfile.withName(event.getName());
                        case "USER_DELETED"  -> null; // null → KTable에서 삭제 (tombstone)
                        default -> currentProfile;
                    };
                },
                // Materialized: State Store 이름 지정 → Interactive Queries 가능
                Materialized.<String, UserProfile, KeyValueStore<Bytes, byte[]>>
                    as("user-profile-store")
                    .withKeySerde(Serdes.String())
                    .withValueSerde(userProfileSerde)
            );

        // 읽기 모델 토픽으로도 출력 (다른 서비스 소비용)
        userProfiles.toStream()
                    .to("user-profiles-readonly",
                        Produced.with(Serdes.String(), userProfileSerde));

        return builder.build();
    }
}

// Interactive Queries: 외부 REST API로 State Store 조회
@RestController
@RequestMapping("/users")
public class UserProfileQueryController {

    private final KafkaStreams kafkaStreams;

    @GetMapping("/{userId}")
    public ResponseEntity<UserProfile> getUser(@PathVariable String userId) {
        // State Store에서 직접 조회 (토픽 경유 없이 로컬 RocksDB 조회)
        ReadOnlyKeyValueStore<String, UserProfile> store =
            kafkaStreams.store(
                StoreQueryParameters.fromNameAndType(
                    "user-profile-store",
                    QueryableStoreTypes.keyValueStore()
                )
            );

        UserProfile profile = store.get(userId);
        if (profile == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(profile);
    }
}
```

---

## 6. State Table

### 6.1 State Store의 내부 구조

State Table은 Kafka Streams 내부에서 상태를 관리하는 저장소다. Projection Table(외부 조회 최적화 목적)과 달리, State Table은 스트림 처리 로직 내에서 필요한 중간 상태를 유지하기 위한 것이다. 왜 이 둘을 구분하는가? 목적이 다르기 때문이다.

```
State Table:
├── 목적: 처리 로직 내부 상태 유지 (집계 중간값, 조인 상태)
├── 소비자: 스트림 처리 로직 자체
├── 수명: 처리가 진행되면서 업데이트/삭제
└── 예: 윈도우 집계 카운트, Logical AND 완료 상태

Projection Table:
├── 목적: 외부 조회를 위한 읽기 모델
├── 소비자: 외부 서비스 (REST API 등)
├── 수명: 최신 상태 계속 유지 (삭제 이벤트 처리 전까지)
└── 예: 사용자 프로필 현재 상태, 주문 현재 상태
```

### 6.2 State Store 유형

```java
// 1. KeyValueStore: 키-값 조회 (가장 일반적)
//    Kafka Streams의 KTable, aggregate, count 등이 내부적으로 사용
KeyValueStore<String, Long> kvStore = context.getStateStore("my-kv-store");
kvStore.put("key", 42L);
Long value = kvStore.get("key");

// 2. WindowStore: 시간 윈도우별 저장
//    windowed aggregate가 내부적으로 사용
WindowStore<String, Long> windowStore = context.getStateStore("my-window-store");
// 특정 시간 범위의 값 조회
WindowStoreIterator<Long> iter =
    windowStore.fetch("key",
        Instant.parse("2024-01-01T14:00:00Z"),
        Instant.parse("2024-01-01T14:05:00Z"));

// 3. SessionStore: 세션 윈도우 저장
//    사용자 세션 분석에 사용 (비활성 기간으로 세션 구분)
SessionStore<String, Long> sessionStore = context.getStateStore("my-session-store");
```

### 6.3 Changelog Topic과 내구성

State Store는 로컬 디스크(RocksDB)에 저장되어 빠르지만, 장애 발생 시 데이터가 손실될 수 있다. Kafka Streams는 이를 Changelog Topic으로 해결한다.

```
State Store 쓰기:
  애플리케이션 → RocksDB (로컬, 빠름)
             ↘
              Changelog Topic (브로커, 내구성)

장애 복구:
  새 인스턴스 시작 → Changelog Topic 읽기 → RocksDB 복원 → 처리 재개

복구 시간 최적화: Standby Replicas
  다른 인스턴스가 동일한 Changelog를 미리 구독하여 핫 스탠바이 유지
  주 인스턴스 장애 시 즉시 전환 (복구 시간 거의 0)
```

```java
// Standby Replicas 설정
props.put(StreamsConfig.NUM_STANDBY_REPLICAS_CONFIG, 1);
// 1개의 스탠바이 → 인스턴스 최소 2개 필요

// State Store 직접 정의 (Transformer에서 사용)
StoreBuilder<KeyValueStore<String, MyState>> storeBuilder =
    Stores.keyValueStoreBuilder(
        Stores.persistentKeyValueStore("my-state-store"),
        Serdes.String(),
        myStateSerde
    );
builder.addStateStore(storeBuilder);
```

### 6.4 EOS와 State Store 일관성

Exactly-Once Semantics(EOS)를 활성화하면 State Store 업데이트와 출력 메시지 발행이 하나의 트랜잭션으로 묶인다. 이는 "상태와 출력이 원자적으로 일관성 있게 유지된다"는 것을 의미한다.

```java
// EOS 활성화
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
          StreamsConfig.EXACTLY_ONCE_V2);
// v2: KIP-447, 한 트랜잭션에 여러 파티션 쓰기 가능 (성능 개선)
```

### 6.5 Interactive Queries: State Store 외부 노출

```java
// 집계 State Store를 REST API로 노출
@RestController
public class SalesQueryController {

    private final KafkaStreams streams;

    // 특정 카테고리의 최근 5분 매출 조회
    @GetMapping("/sales/{category}/recent")
    public Double getRecentSales(@PathVariable String category) {
        ReadOnlyWindowStore<String, Double> windowStore =
            streams.store(
                StoreQueryParameters.fromNameAndType(
                    "sales-store",
                    QueryableStoreTypes.windowStore()
                )
            );

        // 현재 시각 기준 5분 이내 윈도우 조회
        Instant now = Instant.now();
        Instant from = now.minus(Duration.ofMinutes(5));

        WindowStoreIterator<Double> iter =
            windowStore.fetch(category, from, now);

        double total = 0.0;
        while (iter.hasNext()) {
            KeyValue<Long, Double> next = iter.next();
            total += next.value;
        }
        iter.close();

        return total;
    }
}
```

### 6.6 Projection Table vs State Table 비교

| 구분 | Projection Table | State Table |
|------|-----------------|-------------|
| **목적** | 외부 조회 최적화 (읽기 모델) | 처리 로직 내부 상태 유지 |
| **소비자** | REST API, 외부 서비스 | 스트림 처리 로직 |
| **데이터 수명** | 최신 상태 영속 유지 | 처리 완료 후 삭제 가능 |
| **Kafka Streams 구성** | KTable + Materialized Store | StateStore (addStateStore) |
| **조회 방식** | Interactive Queries (외부) | context.getStateStore() (내부) |
| **예시** | 사용자 현재 프로필 | Logical AND 완료 상태 |
| **Changelog** | 자동 생성 (KTable) | 자동 생성 (영속 Store) |

---

## 7. 기존 문서와 연계 및 학습 경로

### 7.1 세 장의 관계

```
03-event-processing.md (무상태 처리)
├── filter: 조건에 맞지 않는 이벤트 제거
├── map / mapValues: 이벤트 변환
├── flatMap: 1개 이벤트 → N개 이벤트
├── branch: 조건별 라우팅
└── merge: 스트림 단순 병합 ← Stream Merger의 기초

04-stateful-streaming.md (기본 상태)
├── groupByKey + count: 기본 집계
├── aggregate: 커스텀 집계
├── join / leftJoin: 스트림-스트림, 스트림-테이블 조인
├── windowing: Tumbling / Hopping / Session 윈도우
└── KTable 기초

18-advanced-stream-patterns.md (고급 패턴) ← 지금 이 문서
├── Event Time 처리: TimestampExtractor + Grace Period
├── Stream Merger: 다중 소스 통합 + 스키마 정규화
├── Suppressed Aggregation: 중간 결과 억제 + 최종만 출력
├── Wait-for-N: N개 동일 이벤트 집합
├── Logical AND: N종 다른 이벤트 집합
├── Projection Table: 읽기 모델 (CQRS Query Side)
└── State Table: 처리 내부 상태 + Interactive Queries
```

### 7.2 패턴 범위 비교표

| 패턴 | 03장 | 04장 | 18장 |
|------|:----:|:----:|:----:|
| filter / map | ✓ | | |
| merge (단순) | ✓ | | |
| groupBy + count | | ✓ | |
| join (기본) | | ✓ | |
| windowing (기본) | | ✓ | |
| Event Time 추출 | | | ✓ |
| Grace Period | | | ✓ |
| Suppressed Aggregation | | | ✓ |
| Stream Merger (다중 소스) | | | ✓ |
| Wait-for-N | | | ✓ |
| Logical AND | | | ✓ |
| Projection Table | | | ✓ |
| State Table + IQ | | | ✓ |

### 7.3 실무 적용 가이드: 어떤 패턴을 선택할까?

```
문제: 이벤트가 제때 도착하지 않아 집계 결과가 틀림
→ 해결: Event Time 처리 + Grace Period (1장)

문제: 다운스트림이 중간 집계 결과를 너무 많이 받아 과부하
→ 해결: Suppressed Aggregation (3장)

문제: 여러 마이크로서비스/채널에서 같은 종류의 이벤트가 발행됨
→ 해결: Event Stream Merger (2장) + 스키마 정규화

문제: N개의 항목이 모두 수집된 후에만 처리해야 함 (배치)
→ 해결: Wait-for-N-Events (4장)

문제: A, B, C 조건이 모두 충족된 후에만 처리해야 함 (승인 프로세스)
→ 해결: Logical AND (4장)

문제: 이벤트 소싱 시스템에서 현재 상태를 빠르게 조회해야 함
→ 해결: Projection Table + Interactive Queries (5장)

문제: 스트림 처리 도중 중간 상태를 저장하고 외부에서 조회해야 함
→ 해결: State Table + Interactive Queries (6장)
```

### 7.4 다른 장과의 연계

- **15-event-sourcing.md**: Projection Table은 이벤트 소싱의 읽기 모델을 구현하는 핵심 도구다. "이벤트로 상태를 재구성"하는 15장의 개념이 "이벤트로 Projection을 지속 업데이트"하는 이 장의 5절로 이어진다.
- **17-idempotency-patterns.md**: Wait-for-N과 Logical AND에서 중복 이벤트 처리는 멱등성 패턴(17장)과 결합해야 정확히 N번 처리를 보장할 수 있다.
- **06-choreography-saga.md**: Logical AND 패턴은 SAGA 코레오그래피의 "모든 단계 완료 감지"를 구현하는 방법 중 하나다.

### 7.5 학습 체크리스트

- [ ] TimestampExtractor를 직접 구현하여 JSON 페이로드에서 Event Time을 추출할 수 있다
- [ ] Grace Period의 의미와 값 설정 기준을 설명할 수 있다
- [ ] `KStream.merge()`와 `StreamsBuilder.stream(List)`의 차이와 사용 시점을 구분한다
- [ ] suppress 없는 집계와 있는 집계의 출력 차이를 코드로 확인했다
- [ ] `BufferConfig.maxRecords().emitEarlyWhenFull()`의 의미를 설명할 수 있다
- [ ] Wait-for-N과 Logical AND를 서로 다른 비즈니스 문제에 적용할 수 있다
- [ ] KTable Materialized Store를 Interactive Queries로 외부에서 조회하는 코드를 작성했다
- [ ] Changelog Topic과 Standby Replicas의 역할을 장애 복구 관점에서 설명할 수 있다
- [ ] Projection Table과 State Table의 사용 목적 차이를 명확히 구분할 수 있다

---

## 참고 자료

- **Confluent Design Patterns**
  - [Event Stream Merger](https://developer.confluent.io/patterns/stream-processing/event-stream-merger/)
  - [Suppressed Event Aggregator](https://developer.confluent.io/patterns/stream-processing/suppressed-event-aggregator/)
  - [Wait-for-N-Events](https://developer.confluent.io/patterns/stream-processing/wait-for-n-events/)
  - [Logical AND](https://developer.confluent.io/patterns/stream-processing/logical-and/)
  - [Wallclock-Time Processing](https://developer.confluent.io/patterns/stream-processing/wallclock-time/)
  - [Event-Time Processing](https://developer.confluent.io/patterns/stream-processing/event-time-processing/)
  - [Projection Table](https://developer.confluent.io/patterns/stream-processing/projection-table/)
  - [State Table](https://developer.confluent.io/patterns/stream-processing/state-table/)
- **Kafka Streams in Action** (William P. Bejeck Jr.) — Chapter 6 (Advanced State), Chapter 7 (Windowing)
- **Kafka Streams 공식 문서**
  - [Suppressed Processing](https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#suppressing-changelog-updates)
  - [Interactive Queries](https://kafka.apache.org/documentation/streams/developer-guide/interactive-queries.html)
  - [TimestampExtractor](https://kafka.apache.org/documentation/streams/developer-guide/config-streams.html#timestamp-extractor)
- **관련 문서**
  - `03-event-processing.md` — 무상태 기초 (filter, map, branch, merge)
  - `04-stateful-streaming.md` — 기본 상태 (KTable, windowing, join)
  - `15-event-sourcing.md` — 이벤트 소싱과 CQRS (Projection Table의 배경)
  - `17-idempotency-patterns.md` — 멱등성 (Wait-for-N과 조합)
