# 21. EIP 고급 라우팅 & 엔드포인트 패턴

메시지를 "어떻게 흘려보내고(라우팅)" "누가 처리하는가(엔드포인트)" — 중급 이상 EIP 패턴을 Kafka 생태계에서 이해한다. `17-messaging-patterns.md`가 메시지 구조와 채널 기초를 다뤘다면, 이 문서는 그 위에서 메시지가 복잡한 토폴로지를 따라 이동하는 방식과, 그 이동의 양 끝에서 시스템과 메시지를 연결하는 엔드포인트 패턴을 다룬다. 패턴을 단순히 이름으로 외우는 것이 아니라, "왜 이 패턴이 필요한가"와 "Kafka에서는 이미 어떤 형태로 구현되어 있는가"를 중심으로 살펴본다.

## 학습 목표

- Recipient List, Routing Slip 등 고급 라우팅 패턴을 Kafka로 구현하는 방법을 이해한다
- Kafka SDK에 내장된 엔드포인트 패턴(Gateway, Activator, Mapper)을 식별한다
- Polling Consumer와 Event-Driven Consumer의 차이와 선택 기준을 파악한다
- Process Manager와 Saga Orchestrator의 관계를 이해한다

---

## 1. 고급 라우팅 패턴

라우팅 패턴이란 메시지가 소스에서 목적지로 가는 경로를 결정하는 메커니즘이다. `17-messaging-patterns.md`의 §12에서 Content-Based Router와 Filter 같은 기초 라우팅을 다뤘는데, 여기서는 그보다 복잡한 상황 — 다수의 수신자, 순서가 뒤섞인 메시지, 메시지 스스로가 경로를 알고 있는 경우 — 을 처리하는 패턴들을 살펴본다.

### 1.1 Pipes-and-Filters

Pipes-and-Filters는 EIP 전체 구조를 관통하는 가장 기초적인 아키텍처 스타일이다. 이름처럼 파이프(채널)로 연결된 독립적인 필터(처리 단계)들이 메시지를 순차적으로 변환한다. 각 필터는 이전 단계와 다음 단계에 대해 아무것도 모른다 — 단지 자신에게 들어오는 입력을 처리하고 출력을 내보낼 뿐이다. 이 단순한 원칙이 강력한 이유는 필터를 독립적으로 테스트하고, 교체하고, 병렬화할 수 있기 때문이다.

Kafka Streams DSL은 그 자체가 Pipes-and-Filters의 직접 구현이다. `stream.filter().map().to()`라는 체인이 곧 필터들을 파이프로 연결하는 선언적 표현이다. 각 연산자가 독립적인 필터이고, Kafka 토픽이 이들을 연결하는 파이프다. Unix 파이프(`cat access.log | grep ERROR | awk '{print $4}'`)와 유사하지만 결정적 차이가 있다 — Kafka는 비동기적이고 분산되어 있으며, 파이프(토픽)가 내구성을 갖는다. Unix 파이프는 프로세스가 죽으면 데이터가 사라지지만, Kafka 토픽은 메시지를 보존하므로 필터 하나가 잠시 멈춰도 파이프가 버퍼 역할을 한다.

```java
// Kafka Streams DSL = Pipes-and-Filters 의 선언적 표현
StreamsBuilder builder = new StreamsBuilder();

KStream<String, OrderEvent> orders = builder.stream("orders-raw");

// Filter 1: 유효성 검증
KStream<String, OrderEvent> validated = orders
    .filter((key, order) -> order.getAmount() > 0 && order.getCustomerId() != null);

// Filter 2: 정규화 (도메인 표준 포맷으로 변환)
KStream<String, OrderEvent> normalized = validated
    .mapValues(order -> OrderNormalizer.normalize(order));

// Filter 3: 위험 주문 분류 (branch = 파이프 분기)
KStream<String, OrderEvent>[] branches = normalized.branch(
    (key, order) -> order.getAmount() > 1_000_000,  // 고위험
    (key, order) -> true                              // 일반
);

KStream<String, OrderEvent> highRisk = branches[0];
KStream<String, OrderEvent> normal   = branches[1];

// 각 브랜치를 다른 파이프(토픽)로
highRisk.to("orders-high-risk");
normal.to("orders-standard");
```

이 토폴로지에서 `orders-raw`, `orders-high-risk`, `orders-standard`가 파이프이고, `filter`, `mapValues`, `branch`가 필터다. 각 필터는 Kafka Streams 내부에서 독립적인 처리 노드로 실행된다. 관련 내용은 `17-messaging-patterns.md` §12를 참조한다.

### 1.2 Recipient List

Content-Based Router가 메시지를 하나의 목적지로 라우팅한다면, Recipient List는 하나의 메시지를 여러 수신자에게 동시에 전달한다. 주문이 생성되었을 때 재고 서비스, 결제 서비스, 배송 서비스 모두에게 동시에 알려야 한다면 Recipient List가 필요하다. Router는 "이 메시지는 A에게"라고 결정하지만, Recipient List는 "이 메시지는 A에게도, B에게도, C에게도"라고 결정한다.

수신자 목록을 관리하는 방식에 따라 두 종류로 나뉜다. **정적 Recipient List**는 대상 토픽 목록이 설정 파일이나 코드에 고정되어 있다. 비즈니스 로직이 바뀌지 않는 한 수신자가 바뀌지 않으므로 단순하고 예측 가능하다. **동적 Recipient List**는 메시지 헤더에 수신자 목록이 포함되어 있어 메시지마다 다른 수신자에게 전달할 수 있다. 구독 기반 알림 시스템처럼 런타임에 수신자가 결정되어야 할 때 유용하다.

```java
// 동적 Recipient List: 헤더에서 수신 토픽 목록을 읽어 각각에 생산
@Component
public class DynamicRecipientListRouter {

    private final KafkaTemplate<String, byte[]> kafkaTemplate;

    public DynamicRecipientListRouter(KafkaTemplate<String, byte[]> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @KafkaListener(topics = "order-created")
    public void route(ConsumerRecord<String, OrderEvent> record) {
        // 헤더에서 수신자 목록 파싱
        Header recipientHeader = record.headers().lastHeader("X-Recipients");
        if (recipientHeader == null) {
            return;
        }

        String[] recipients = new String(recipientHeader.value()).split(",");
        OrderEvent order = record.value();

        // 각 수신자 토픽에 메시지 전달
        for (String topic : recipients) {
            ProducerRecord<String, byte[]> outRecord =
                new ProducerRecord<>(topic.trim(), record.key(), serialize(order));

            // 원본 헤더를 그대로 전파 (traceability)
            record.headers().forEach(h -> outRecord.headers().add(h));
            kafkaTemplate.send(outRecord);
        }
    }
}
```

정적 Recipient List는 더 단순하다 — `KafkaTemplate.send()`를 여러 토픽에 반복 호출하면 된다. 동적 방식은 헤더 파싱 로직이 추가되지만 유연성을 얻는다. 실제 주문 시스템에서 `order-created` 이벤트를 `inventory-service-topic`, `billing-service-topic`, `shipping-notification-topic`에 동시에 배포하는 것이 전형적인 Recipient List 사용 사례다.

### 1.3 Resequencer

분산 시스템에서 메시지는 전송된 순서대로 도착하지 않을 수 있다. 특히 여러 파티션이나 여러 외부 시스템에서 이벤트가 합류하는 경우다. Resequencer는 순서가 뒤섞인 메시지를 받아 원래 순서대로 재정렬한 후 내보내는 패턴이다.

Kafka를 단일 토픽 단일 파티션에서만 사용한다면 Resequencer는 불필요하다 — Kafka는 파티션 단위로 순서를 보장하기 때문이다. 그러나 복수의 파티션에서 이벤트가 합류하거나, 외부 시스템(REST API, 레거시 큐)에서 이벤트를 수집할 때는 순서 보장이 깨질 수 있다. 예를 들어, 센서 데이터를 수집할 때 네트워크 지연으로 시퀀스 번호 5가 6보다 늦게 도착하는 상황이다.

```java
// Kafka Streams로 구현하는 Resequencer
// 시퀀스 번호 기반, 윈도우 버퍼링 방식
StreamsBuilder builder = new StreamsBuilder();
KStream<String, SensorEvent> raw = builder.stream("sensor-raw");

// 상태 저장소 정의 (버퍼)
StoreBuilder<KeyValueStore<Long, SensorEvent>> storeBuilder =
    Stores.keyValueStoreBuilder(
        Stores.persistentKeyValueStore("resequence-buffer"),
        Serdes.Long(),
        sensorEventSerde
    );
builder.addStateStore(storeBuilder);

// Transformer에서 시퀀스 번호 기반 재정렬
KStream<String, SensorEvent> resequenced = raw.transform(
    () -> new ResequencerTransformer("resequence-buffer"),
    "resequence-buffer"
);

resequenced.to("sensor-ordered");
```

```java
public class ResequencerTransformer implements Transformer<String, SensorEvent, KeyValue<String, SensorEvent>> {

    private static final long WINDOW_SIZE_MS = 5_000; // 5초 대기
    private KeyValueStore<Long, SensorEvent> buffer;
    private long expectedSeq = 0;

    @Override
    public void init(ProcessorContext context) {
        this.buffer = context.getStateStore("resequence-buffer");
        // 주기적으로 버퍼 플러시 (punctuate)
        context.schedule(Duration.ofSeconds(1), PunctuationType.WALL_CLOCK_TIME, timestamp -> flush(context));
    }

    @Override
    public KeyValue<String, SensorEvent> transform(String key, SensorEvent event) {
        buffer.put(event.getSequenceNumber(), event);
        return null; // 즉시 방출하지 않음
    }

    private void flush(ProcessorContext context) {
        // 연속된 시퀀스 번호가 있으면 순서대로 방출
        SensorEvent next;
        while ((next = buffer.get(expectedSeq)) != null) {
            context.forward(next.getSensorId(), next);
            buffer.delete(expectedSeq);
            expectedSeq++;
        }
    }
}
```

Resequencer의 핵심 트레이드오프는 지연(latency) 대 정확성이다. 순서를 보장하려면 다음 시퀀스가 올 때까지 기다려야 하는데, 그 메시지가 영영 오지 않을 수도 있다. 실무에서는 타임아웃을 설정하고, 타임아웃 초과 시 순서를 포기하고 방출하거나 데드레터 큐로 보내는 전략을 함께 사용한다.

### 1.4 Composed Message Processor

Composed Message Processor는 하나의 메타-패턴이다 — Splitter, Router, Aggregator를 하나의 파이프라인으로 조합하여 복잡한 분할-처리-병합 워크플로우를 구현한다. `17-messaging-patterns.md`에서 각각을 독립 패턴으로 다뤘는데, 실무에서는 이 세 패턴이 항상 함께 등장한다. 그래서 EIP는 이 조합에 별도 이름을 붙였다.

전형적인 시나리오는 이렇다. 고객이 장바구니에 5개 상품을 담아 주문했을 때, 주문을 개별 상품 단위로 분할하고(Splitter), 각 상품을 해당 창고로 라우팅하고(Router), 모든 창고 처리 결과를 수집하여 최종 배송 정보로 병합한다(Aggregator). 각 단계는 독립적으로 병렬 실행되므로 5개 창고를 순차 처리하는 것보다 훨씬 빠르다.

```
┌─────────────────────────────────────────────────────┐
│           Composed Message Processor                 │
│                                                      │
│  OrderEvent(5 items)                                 │
│       │                                              │
│       ▼                                              │
│  [Splitter]  → item-1, item-2, item-3, item-4, item-5│
│       │                                              │
│       ▼                                              │
│  [Router]    → warehouse-A, warehouse-B, warehouse-C │
│                    │           │           │         │
│               [Worker]    [Worker]    [Worker]       │
│                    │           │           │         │
│       ▼                                              │
│  [Aggregator] ← shipment-result-A, B, C             │
│       │                                              │
│       ▼                                              │
│  FinalShipmentPlan                                   │
└─────────────────────────────────────────────────────┘
```

Kafka Streams로 구현할 때 Splitter는 `flatMapValues`, Router는 `branch`, Aggregator는 `groupByKey().aggregate()`가 된다. 세 단계를 이어주는 파이프가 `item-split`, `warehouse-results` 토픽이다. 각 단계 사이에 Kafka 토픽이 있으므로 각 단계를 독립적으로 스케일아웃할 수 있다는 것이 큰 장점이다.

### 1.5 Routing Slip

Routing Slip은 메시지가 자신의 처리 경로를 헤더에 직접 담아 이동하는 패턴이다. 각 처리 단계는 헤더를 읽어 다음 목적지를 확인하고, 자신이 처리를 완료한 후 남은 경로대로 메시지를 전달한다. 경로 결정이 중앙 라우터에 집중되지 않고 메시지 자체에 분산되어 있다는 것이 핵심이다.

Content-Based Router와의 차이가 중요하다. Router는 라우팅 로직이 중앙화된 컴포넌트에 있어서 경로가 변경되면 Router를 수정해야 한다. Routing Slip은 각 메시지가 자신만의 경로를 가지므로, 메시지 생성 시점에 경로를 동적으로 결정할 수 있고 라우팅 컴포넌트를 수정할 필요가 없다. "보험 청구 처리"처럼 케이스마다 필요한 심사 단계가 달라지는 워크플로우에 적합하다.

```java
// 생산자: 처리 경로를 헤더에 포함
public void publishWithRoutingSlip(ClaimEvent claim, List<String> processingSteps) {
    ProducerRecord<String, ClaimEvent> record =
        new ProducerRecord<>("claims-inbox", claim.getId(), claim);

    // 라우팅 슬립을 JSON 배열로 직렬화하여 헤더에 추가
    String slip = objectMapper.writeValueAsString(processingSteps);
    // 예: ["fraud-check", "medical-review", "approval", "payment"]
    record.headers().add("X-Routing-Slip", slip.getBytes(StandardCharsets.UTF_8));

    kafkaTemplate.send(record);
}

// 각 처리 단계의 소비자: 슬립을 읽고 다음 단계로 전달
@KafkaListener(topics = "fraud-check")
public void handleFraudCheck(ConsumerRecord<String, ClaimEvent> record) {
    ClaimEvent claim = record.value();

    // 1. 이 단계의 처리 수행
    FraudCheckResult result = fraudService.check(claim);
    claim.setFraudCheckPassed(result.isPassed());

    // 2. 헤더에서 라우팅 슬립 읽기
    Header slipHeader = record.headers().lastHeader("X-Routing-Slip");
    List<String> remainingSteps = parseSlip(slipHeader);

    // 3. 현재 단계(fraud-check)는 처리 완료 → 슬립에서 제거
    remainingSteps.remove(0); // 첫 번째 항목이 현재 단계

    if (remainingSteps.isEmpty()) {
        // 모든 단계 완료 → 최종 결과 토픽으로
        kafkaTemplate.send("claims-completed", claim.getId(), claim);
    } else {
        // 다음 단계로 전달
        String nextTopic = remainingSteps.get(0);
        ProducerRecord<String, ClaimEvent> next =
            new ProducerRecord<>(nextTopic, claim.getId(), claim);

        // 갱신된 슬립(남은 단계)을 헤더에 재설정
        String updatedSlip = objectMapper.writeValueAsString(remainingSteps);
        next.headers().add("X-Routing-Slip", updatedSlip.getBytes(StandardCharsets.UTF_8));

        // 원본의 다른 헤더(traceId 등)도 전파
        record.headers().forEach(h -> {
            if (!h.key().equals("X-Routing-Slip")) {
                next.headers().add(h);
            }
        });
        kafkaTemplate.send(next);
    }
}
```

Routing Slip의 주의점은 헤더 크기다. 처리 단계가 많아질수록 헤더가 커지므로, 단계가 수십 개라면 헤더 대신 외부 상태 저장소에 슬립을 보관하고 헤더에는 ID만 담는 변형을 고려해야 한다. 또한 각 단계가 실패했을 때 보상 로직이 헤더 기반으로는 복잡해지므로, 복잡한 오류 처리가 필요하다면 Process Manager로 전환하는 것이 낫다.

### 1.6 Process Manager

Process Manager는 복잡한 다단계 워크플로우의 실행 상태를 중앙에서 관리하는 컴포넌트다. Routing Slip이 메시지에 경로를 담아 분산 결정을 내린다면, Process Manager는 워크플로우 전체 상태를 한 곳에서 추적하고 다음 단계를 능동적으로 결정한다. 이벤트 스트리밍에서는 `08-orchestration-saga.md`의 Saga Orchestrator가 곧 Process Manager다.

Process Manager가 필요한 이유는 상태 때문이다. "주문의 재고 확인은 완료되었고, 결제는 처리 중이며, 배송 준비는 아직 시작 안 됨"이라는 복합적인 상태를 메시지 헤더에 담기는 너무 복잡하다. Process Manager는 이 상태를 자신이 소유하고 관리하므로, 워크플로우의 임의 지점에서 상태를 조회하거나, 타임아웃을 처리하거나, 부분 실패 후 재시작하는 것이 가능하다.

```java
// Process Manager의 상태 머신 구현
@Component
public class OrderProcessManager {

    private final KeyValueStore<String, OrderWorkflowState> stateStore;
    private final KafkaTemplate<String, Object> kafkaTemplate;

    // 상태 전이 테이블
    private static final Map<WorkflowStep, WorkflowStep> TRANSITIONS = Map.of(
        WorkflowStep.CREATED,           WorkflowStep.INVENTORY_CHECK,
        WorkflowStep.INVENTORY_CHECK,   WorkflowStep.PAYMENT_PROCESSING,
        WorkflowStep.PAYMENT_PROCESSING, WorkflowStep.SHIPPING_PREPARATION,
        WorkflowStep.SHIPPING_PREPARATION, WorkflowStep.COMPLETED
    );

    @KafkaListener(topics = {
        "inventory-check-result",
        "payment-result",
        "shipping-prepared"
    })
    public void onStepCompleted(ConsumerRecord<String, StepResultEvent> record) {
        String orderId = record.key();
        StepResultEvent result = record.value();

        // 현재 워크플로우 상태 로드
        OrderWorkflowState state = stateStore.get(orderId);
        if (state == null) return;

        if (result.isSuccess()) {
            // 다음 단계로 전이
            WorkflowStep nextStep = TRANSITIONS.get(state.getCurrentStep());
            state.setCurrentStep(nextStep);
            stateStore.put(orderId, state);

            if (nextStep == WorkflowStep.COMPLETED) {
                kafkaTemplate.send("order-completed", orderId, new OrderCompletedEvent(orderId));
            } else {
                // 다음 단계 커맨드 발송
                kafkaTemplate.send(nextStep.getCommandTopic(), orderId, result.getPayload());
            }
        } else {
            // 보상 트랜잭션 시작 (Saga 보상 참조: 08-orchestration-saga.md)
            state.setCurrentStep(WorkflowStep.COMPENSATING);
            stateStore.put(orderId, state);
            kafkaTemplate.send("compensation-commands", orderId, new CompensationCommand(orderId, state));
        }
    }
}
```

Routing Slip과 Process Manager의 핵심 차이는 "상태가 어디에 있는가"이다. Routing Slip에서는 상태가 메시지에 있어 Process Manager가 없어도 되므로 단순하다. 반면 복잡한 오류 처리, 타임아웃, 병렬 단계 조율이 필요하다면 중앙화된 상태를 갖는 Process Manager가 훨씬 유지보수하기 쉽다. Saga Orchestrator 패턴의 상세한 구현은 `08-orchestration-saga.md`를 참조한다.

---

## 2. 엔드포인트 패턴

엔드포인트 패턴은 애플리케이션 코드와 메시징 인프라가 만나는 경계를 다룬다. 메시지를 보내는 쪽(생산자 엔드포인트)과 받는 쪽(소비자 엔드포인트) 모두에서 패턴이 등장한다. Kafka SDK와 Spring Kafka가 이미 대부분의 패턴을 구현해 제공하므로, 개발자는 그 패턴의 이름과 목적을 인식하는 것만으로도 설계 결정을 더 의식적으로 내릴 수 있다.

### 2.1 Messaging Gateway & Service Activator

Messaging Gateway는 애플리케이션 코드가 메시징 인프라를 직접 알지 못하도록 감싸는 추상화 레이어다. 도메인 서비스는 "주문 이벤트를 발행한다"는 비즈니스 의도만 표현하고, 그것이 Kafka로 가는지, SQS로 가는지, 심지어 동기 HTTP 호출인지 알 필요가 없다. 이 추상화가 Gateway 패턴이다.

Spring Kafka에서 `KafkaTemplate`이 바로 Messaging Gateway다. `kafkaTemplate.send("order-created", key, event)`를 호출하는 서비스 코드는 Kafka의 ProducerRecord 구조나 직렬화 방식을 신경 쓰지 않는다. `KafkaTemplate`이 이를 캡슐화한다.

Service Activator는 반대 방향의 패턴이다 — 메시지가 도착했을 때 해당 서비스 메서드를 호출하는 연결 고리다. Spring Kafka의 `@KafkaListener`가 Service Activator 역할을 한다. 메시지를 받아 역직렬화하고, 적절한 서비스 메서드에 전달한다. 이 두 패턴이 한 쌍을 이루어 "메시지를 보내는 Gateway"와 "메시지를 받아 서비스에 연결하는 Activator"가 된다.

```java
// KafkaTemplate = Messaging Gateway
// 서비스 코드는 Kafka 세부 사항을 모른다
@Service
public class OrderService {

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;  // Gateway

    public void placeOrder(Order order) {
        // 비즈니스 로직
        Order savedOrder = orderRepository.save(order);

        // Gateway를 통해 이벤트 발행 — Kafka 구조를 직접 다루지 않음
        kafkaTemplate.send("order-created", savedOrder.getId(), OrderEvent.from(savedOrder));
    }
}

// @KafkaListener = Service Activator
// 메시지가 도착하면 서비스 메서드를 활성화
@Component
public class InventoryServiceActivator {

    private final InventoryService inventoryService;  // 실제 비즈니스 서비스

    @KafkaListener(topics = "order-created", groupId = "inventory-group")
    public void onOrderCreated(OrderEvent event) {
        // Service Activator가 메시지를 받아 서비스 메서드 호출
        inventoryService.reserveItems(event.getOrderId(), event.getItems());
    }
}
```

Anti-pattern은 `ProducerRecord`를 서비스 코드에서 직접 생성하고 직렬화를 직접 수행하는 것이다. 이렇게 하면 비즈니스 로직이 메시징 인프라 세부 사항에 의존하게 되어, 나중에 메시징 시스템을 교체하거나 테스트하기 어려워진다. Gateway를 통하면 테스트에서 `KafkaTemplate`을 Mock으로 교체하여 Kafka 없이도 서비스 로직을 단위 테스트할 수 있다.

### 2.2 Messaging Mapper

Messaging Mapper는 도메인 객체와 메시지 포맷 사이의 변환을 담당한다. 도메인 모델은 JPA 엔티티나 도메인 클래스로 표현되지만, 메시지로 전송할 때는 Avro, JSON, Protobuf 같은 직렬화 포맷으로 변환해야 한다. 이 변환 책임이 Messaging Mapper에 있다.

Kafka에서는 Serializer/Deserializer 쌍이 Messaging Mapper를 구현한다. Avro를 사용하면 `KafkaAvroSerializer`/`KafkaAvroDeserializer`가, JSON이면 `JsonSerializer`/`JsonDeserializer`가 Mapper 역할을 한다. SpecificRecord 기반 Avro 매핑은 컴파일 타임에 스키마를 강제하므로 타입 안전성이 높다. 반면 `GenericRecord` 방식은 런타임까지 타입 오류가 드러나지 않는다.

```java
// 커스텀 Messaging Mapper 구현 (특수한 변환 로직이 필요한 경우)
public class OrderEventMapper implements Serializer<OrderEvent>, Deserializer<OrderEvent> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public byte[] serialize(String topic, OrderEvent data) {
        if (data == null) return null;
        try {
            // 도메인 객체 → 메시지 포맷 변환
            OrderEventDto dto = OrderEventDto.fromDomain(data);  // 구조 변환
            return objectMapper.writeValueAsBytes(dto);
        } catch (JsonProcessingException e) {
            throw new SerializationException("OrderEvent 직렬화 실패", e);
        }
    }

    @Override
    public OrderEvent deserialize(String topic, byte[] data) {
        if (data == null) return null;
        try {
            // 메시지 포맷 → 도메인 객체 변환
            OrderEventDto dto = objectMapper.readValue(data, OrderEventDto.class);
            return dto.toDomain();  // 역구조 변환
        } catch (IOException e) {
            throw new SerializationException("OrderEvent 역직렬화 실패", e);
        }
    }
}
```

Avro SpecificRecord와의 관계는 `02-fundamentals/08-avro-deep-dive.md`에 상세히 다루어져 있다. 핵심은 `.avsc` 스키마 파일에서 Java 클래스를 생성하면(`avro-tools`, Gradle 플러그인), 생성된 클래스가 이미 Mapper 역할의 `toByteBuffer()`/`fromByteBuffer()` 메서드를 포함한다는 점이다. 즉, Avro SpecificRecord 자체가 Messaging Mapper를 구현하고 있다.

### 2.3 Transactional Client

Transactional Client는 메시지 송수신을 트랜잭션 경계 안에 묶는 패턴이다. "데이터베이스를 업데이트하고 이벤트를 발행하는" 두 작업이 둘 다 성공하거나 둘 다 실패하도록 원자성을 보장해야 할 때 필요하다. 트랜잭션 없이는 DB 업데이트는 성공했는데 Kafka 발행이 실패하거나, 그 반대 상황이 생겨 시스템이 불일치 상태에 빠질 수 있다.

Kafka는 트랜잭셔널 프로듀서를 통해 Exactly-once semantics를 지원한다. 소비자 쪽에서는 `isolation.level=read_committed`로 설정하면 커밋된 트랜잭션의 메시지만 읽는다. Transactional Outbox 패턴(`09-transactional-messaging.md`)은 DB 트랜잭션과 Kafka 발행 사이의 이중 쓰기 문제를 해결하는 보완적 접근이다.

```java
// Kafka 트랜잭셔널 프로듀서 설정
@Bean
public ProducerFactory<String, Object> transactionalProducerFactory() {
    Map<String, Object> props = new HashMap<>();
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "order-service-tx-1");
    props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
    props.put(ProducerConfig.ACKS_CONFIG, "all");
    props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);
    return new DefaultKafkaProducerFactory<>(props);
}

// 트랜잭션 내에서 여러 토픽에 원자적으로 발행
@Service
public class OrderEventPublisher {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishOrderEvents(Order order) {
        kafkaTemplate.executeInTransaction(operations -> {
            // 두 발행이 트랜잭션으로 묶임: 둘 다 성공 or 둘 다 실패
            operations.send("order-created", order.getId(), OrderCreatedEvent.from(order));
            operations.send("audit-log", order.getId(), AuditEvent.orderCreated(order));
            return null;
        });
    }
}

// 소비자: 커밋된 메시지만 읽기
props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
```

Kafka 트랜잭션의 범위는 Kafka 토픽들 사이에서만 원자성을 보장한다. DB 업데이트와 Kafka 발행의 원자성은 Kafka 트랜잭션만으로는 해결할 수 없고, Transactional Outbox 패턴이나 Saga 패턴을 사용해야 한다. 관련 상세 내용은 `18-idempotency-patterns.md`의 Outbox 섹션을 참조한다.

### 2.4 Polling Consumer vs Event-Driven Consumer

Polling Consumer와 Event-Driven Consumer는 소비자가 메시지를 받는 방식에서 근본적으로 다르다. Polling Consumer는 소비자가 능동적으로 "메시지가 있나요?"를 주기적으로 물어보는 방식이다. Event-Driven Consumer는 메시지가 도착하면 시스템이 소비자를 깨우는 방식이다.

Kafka의 근본 모델은 Polling이다. `KafkaConsumer.poll(Duration timeout)`이 핵심 API다. 소비자 스레드가 루프를 돌며 poll을 호출하고, 결과가 있으면 처리하고, 없으면 `timeout`만큼 기다렸다가 다시 poll한다. 이 방식이 Push 방식보다 Kafka에서 선택된 이유가 있다 — 소비자가 처리 속도를 직접 제어할 수 있기 때문이다. Push 방식에서는 브로커가 결정하는 속도로 메시지가 밀려오므로 소비자가 압도(overwhelm)될 수 있다.

Spring Kafka의 `@KafkaListener`는 이 Polling 루프를 프레임워크가 대신 실행하고, 메시지가 오면 어노테이션이 달린 메서드를 호출하는 방식으로 Event-Driven Consumer처럼 보이게 감싼다. 내부적으로는 여전히 polling이지만, 개발자 관점에서는 이벤트가 "도달"하는 것처럼 보인다.

```java
// Polling Consumer: 원시 Kafka API 직접 사용
// 배치 처리, backpressure 세밀 제어가 필요할 때
@Component
public class BatchPollingConsumer implements Runnable {

    private final KafkaConsumer<String, OrderEvent> consumer;

    @Override
    public void run() {
        consumer.subscribe(List.of("orders-to-process"));

        while (!Thread.currentThread().isInterrupted()) {
            // poll: 최대 1초 대기 후 레코드 반환
            ConsumerRecords<String, OrderEvent> records = consumer.poll(Duration.ofSeconds(1));

            if (!records.isEmpty()) {
                // 배치 단위로 처리
                processBatch(records);

                // 처리 완료 후 명시적 오프셋 커밋
                consumer.commitSync();
            }
        }
    }

    private void processBatch(ConsumerRecords<String, OrderEvent> records) {
        // 배치 처리 로직 — DB 벌크 인서트 등
        List<OrderEvent> batch = new ArrayList<>();
        for (ConsumerRecord<String, OrderEvent> record : records) {
            batch.add(record.value());
        }
        orderRepository.saveAll(batch);  // 한 번에 삽입
    }
}

// Event-Driven Consumer: @KafkaListener
// 실시간 처리, 개별 이벤트 응답이 중요할 때
@Component
public class OrderEventConsumer {

    @KafkaListener(topics = "order-created", groupId = "order-processor")
    public void onOrderCreated(OrderEvent event) {
        // 프레임워크가 poll 루프를 관리 — 메서드만 구현
        orderProcessingService.process(event);
    }
}
```

| 구분 | Polling Consumer | Event-Driven Consumer (@KafkaListener) |
|------|-----------------|---------------------------------------|
| 처리 단위 | 배치(ConsumerRecords) | 개별 메시지 |
| backpressure | 직접 제어 | 프레임워크가 관리 |
| 오프셋 커밋 | 명시적 commitSync/Async | 자동 또는 수동 ack |
| 코드 복잡도 | 높음 | 낮음 |
| 적합 상황 | 배치 ETL, 세밀한 흐름 제어 | 실시간 이벤트 처리, 대부분의 경우 |

실무에서는 대부분 `@KafkaListener`가 충분하다. 원시 poll을 직접 사용해야 하는 경우는 배치 크기를 동적으로 조절해야 하거나, 오프셋 관리를 완전히 직접 통제해야 하는 특수한 상황이다.

### 2.5 Competing Consumers

Competing Consumers는 여러 소비자 인스턴스가 하나의 채널(큐/토픽)을 두고 경쟁하여 메시지를 나눠 처리하는 패턴이다. 처리량을 수평 확장하는 가장 직접적인 방법이며, Kafka의 Consumer Group이 이 패턴의 구현체다.

Consumer Group에서 각 파티션은 그룹 내 정확히 하나의 소비자에게 할당된다. 소비자가 3개이고 파티션이 9개라면, 각 소비자가 3개 파티션을 담당한다. 소비자가 5개로 늘어나면 각자가 담당하는 파티션 수가 줄어 처리량이 늘어난다. 소비자 인스턴스 수가 파티션 수를 초과하면 초과 인스턴스는 유휴 상태가 된다 — 이것이 **파티션 수가 최대 병렬도**를 결정하는 이유다.

```java
// 같은 groupId = Competing Consumers
// 3개 인스턴스가 동일 groupId로 실행되면 파티션을 나눠 처리
@KafkaListener(
    topics = "orders-to-fulfill",
    groupId = "fulfillment-workers",  // 그룹 ID로 경쟁 관계 형성
    concurrency = "3"                  // 인스턴스당 3개 스레드 (파티션 수에 맞게)
)
public void fulfillOrder(OrderEvent event) {
    // 여러 인스턴스가 동시에 다른 파티션의 메시지를 처리
    fulfillmentService.process(event);
}
```

리밸런싱은 Competing Consumers의 동적 재분배 메커니즘이다. 소비자가 추가되거나 제거되면 Kafka가 자동으로 파티션을 재분배한다. 리밸런싱 중에는 짧은 처리 중단이 발생하므로, 처리 시간이 `max.poll.interval.ms` 이내로 유지되어야 한다. Consumer Group의 상세한 동작은 `02-fundamentals/06-consumer-groups`를 참조한다.

### 2.6 Message Dispatcher

Message Dispatcher는 하나의 채널에서 다양한 메시지 타입을 받아 타입에 맞는 핸들러 메서드로 분배하는 패턴이다. 여러 이벤트 타입이 하나의 토픽에 혼재하는 "polyglot topic" 구조에서 유용하다. 예를 들어, `order-events` 토픽에 `OrderCreated`, `OrderUpdated`, `OrderCancelled` 이벤트가 함께 흐를 때 타입별로 다른 메서드에서 처리하고 싶다면 Message Dispatcher가 필요하다.

Spring Kafka는 클래스 레벨의 `@KafkaListener`와 메서드 레벨의 `@KafkaHandler`를 조합하여 Message Dispatcher를 구현한다. 프레임워크가 메시지 타입(실제로는 역직렬화된 Java 타입)을 보고 적합한 `@KafkaHandler` 메서드를 선택한다.

```java
// Message Dispatcher: 하나의 토픽, 타입별로 다른 핸들러
@Component
@KafkaListener(topics = "order-events", groupId = "order-dispatcher")
public class OrderEventDispatcher {

    // OrderCreatedEvent 타입 → 이 메서드로 분배
    @KafkaHandler
    public void handleCreated(OrderCreatedEvent event) {
        inventoryService.reserve(event.getOrderId(), event.getItems());
    }

    // OrderCancelledEvent 타입 → 이 메서드로 분배
    @KafkaHandler
    public void handleCancelled(OrderCancelledEvent event) {
        inventoryService.release(event.getOrderId());
        refundService.initiate(event.getOrderId());
    }

    // 알 수 없는 타입에 대한 fallback
    @KafkaHandler(isDefault = true)
    public void handleUnknown(Object payload) {
        log.warn("알 수 없는 이벤트 타입 수신: {}", payload.getClass().getSimpleName());
    }
}
```

Dispatcher 패턴의 전제 조건은 토픽의 메시지를 역직렬화할 때 타입 정보를 함께 포함해야 한다는 점이다. JSON의 경우 `spring.json.trusted.packages`와 `__TypeId__` 헤더가, Avro의 경우 Schema Registry의 스키마 ID가 타입 구분 역할을 한다. polyglot topic은 개념적으로 편리하지만, 한 토픽에 이질적인 이벤트가 섞이면 나중에 분리하기 어려워지므로 초기 설계에서 신중하게 결정해야 한다.

### 2.7 Selective Consumer

Selective Consumer는 채널에서 특정 조건을 만족하는 메시지만 선택적으로 소비하는 패턴이다. 모든 메시지를 받되, 관심 없는 메시지는 스킵한다. Content-Based Router와의 차이는 관점의 차이다 — Router는 생산자 측에서 메시지를 분기하고, Selective Consumer는 소비자 측에서 필터링한다.

Kafka에서는 두 가지 방법이 있다. `RecordFilterStrategy`를 사용하면 스프링 컨테이너가 메시지를 수신한 후 리스너 메서드 호출 전에 필터링한다. 단, 이 방식은 메시지를 이미 Kafka에서 읽은 후 필터링하므로 네트워크 비용은 절약되지 않는다.

```java
// RecordFilterStrategy: 소비자 측 필터링
@Bean
public ConcurrentKafkaListenerContainerFactory<String, OrderEvent> filteringFactory(
        ConsumerFactory<String, OrderEvent> consumerFactory) {

    ConcurrentKafkaListenerContainerFactory<String, OrderEvent> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConsumerFactory(consumerFactory);

    // VIP 주문만 처리하는 Selective Consumer
    factory.setRecordFilterStrategy(record -> {
        // true 반환 = 필터링(스킵), false = 처리
        OrderEvent event = record.value();
        return !event.isVip();  // VIP가 아닌 주문은 스킵
    });

    factory.setAckDiscarded(true);  // 필터링된 메시지도 오프셋 커밋
    return factory;
}

// 이 리스너는 VIP 주문만 수신
@KafkaListener(topics = "orders", containerFactory = "filteringFactory")
public void handleVipOrder(OrderEvent event) {
    vipOrderService.process(event);  // VIP 전용 처리 로직
}
```

Selective Consumer의 성능 함의를 이해해야 한다. 메시지는 이미 브로커에서 소비자로 전송되었고, 역직렬화도 완료된 상태에서 필터링이 일어난다. 즉 "읽었지만 처리하지 않는" 메시지에 대해 네트워크와 역직렬화 비용을 지불한 셈이다. 선택 비율이 낮다면(예: 전체의 1%만 처리) 별도의 "필터링 전용" 토픽을 두거나, 생산자 측에서 미리 분기하는 것이 효율적이다.

### 2.8 Durable Subscriber

Durable Subscriber는 일시적으로 오프라인 상태가 되어도 그동안 생성된 메시지를 재연결 시 모두 받을 수 있는 소비자다. "내가 없는 동안 발행된 메시지도 나중에 받고 싶다"는 요구사항이다. Non-Durable Subscriber는 연결이 끊긴 동안의 메시지를 영영 받지 못한다.

Kafka에서 `group.id`와 커밋된 오프셋이 Durable Subscriber를 구현한다. Consumer Group에 속한 소비자가 재시작하면, Kafka는 해당 그룹이 마지막으로 커밋한 오프셋부터 메시지를 다시 제공한다. 그 사이에 발행된 메시지들이 보존되어 있기 때문이다. 이것이 Kafka의 내구성(Durability)이 Durable Subscriber를 자연스럽게 지원하는 이유다.

```java
// Durable Subscriber: group.id + enable.auto.commit=false
Map<String, Object> durableProps = new HashMap<>();
durableProps.put(ConsumerConfig.GROUP_ID_CONFIG, "billing-service");  // 고정 group ID
durableProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest"); // 처음부터 읽기 (첫 실행시)
durableProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);     // 명시적 커밋으로 안전성 확보

// Non-Durable Subscriber: group.id 없음 또는 매번 다른 group.id
Map<String, Object> nonDurableProps = new HashMap<>();
// group.id를 UUID로 랜덤 생성 → 재시작 시 처음부터 읽거나 최신 오프셋부터 읽음
nonDurableProps.put(ConsumerConfig.GROUP_ID_CONFIG, "temp-" + UUID.randomUUID());
nonDurableProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest"); // 재연결 시 새 메시지만
```

`auto.offset.reset` 정책이 Durable Subscriber의 시작점을 결정한다. `earliest`는 처음부터, `latest`는 가장 최신 오프셋부터 읽기 시작한다. 신규 consumer group이 처음 연결될 때 적용되는 설정이므로, 기존 오프셋이 있으면 이 값과 무관하게 커밋된 오프셋부터 읽는다. 메시지 보존 기간(`retention.ms`) 이상 오프라인 상태였다면 그 사이 메시지는 이미 삭제되어 복구할 수 없으므로, 오프라인 허용 시간을 보존 기간보다 짧게 유지해야 한다.

---

## 참고 자료

- **Enterprise Integration Patterns** — Gregor Hohpe, Bobby Woolf (Addison-Wesley, 2003): 이 문서에서 다룬 모든 패턴의 원전. [eaipatterns.com](https://www.eaipatterns.com/) 에서 패턴 카탈로그를 웹으로도 확인 가능
- **Confluent: Event Streaming Patterns** — [developer.confluent.io/patterns](https://developer.confluent.io/patterns/): EIP 패턴을 Kafka 생태계에서 구체화한 공식 패턴 카탈로그
- **Spring Kafka Reference Documentation** — [docs.spring.io/spring-kafka](https://docs.spring.io/spring-kafka/docs/current/reference/html/): `@KafkaListener`, `@KafkaHandler`, `RecordFilterStrategy`, `KafkaTemplate` 등 엔드포인트 패턴 구현의 공식 레퍼런스
- **Kafka Streams Developer Guide** — [kafka.apache.org/documentation/streams](https://kafka.apache.org/documentation/streams/developer-guide/): Pipes-and-Filters, Resequencer 구현에 사용된 Streams DSL과 Transformer API 공식 문서
- `17-messaging-patterns.md` — 이 문서의 전제인 기초 메시징 패턴(Splitter, Aggregator, Content-Based Router, Filter)의 상세 설명
- `08-orchestration-saga.md` — Process Manager 패턴의 구체적 구현인 Saga Orchestrator 패턴의 전체 구현 가이드
- `18-idempotency-patterns.md` — Transactional Client 패턴과 연관된 Exactly-once semantics와 Outbox 패턴의 심화 내용
