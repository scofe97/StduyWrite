# 20. EIP 메시지 구조 & 채널 패턴

메시지의 "무엇(구조)"과 "어디로(채널)" — EIP의 기반 어휘를 Kafka 매핑과 함께 정리한다

## 학습 목표

- EIP 메시지 유형(Command/Document/Event)의 의도 차이를 이해한다
- Kafka 토픽과 EIP 채널 패턴의 매핑 관계를 파악한다
- 기존 학습 문서에서 이미 다루는 패턴을 EIP 이름으로 재연결한다
- 채널 어댑터, 브리지, 버스 패턴의 현대적 구현을 이해한다

---

## 1. Kafka ↔ EIP 매핑 테이블

EIP 책(Gregor Hohpe & Bobby Woolf, 2003)에 수록된 65개 패턴 중 상당수는 이미 Kafka 생태계에서 특정 개념이나 기능으로 구현되어 있습니다. 문제는 두 세계가 서로 다른 용어를 사용한다는 점입니다. "Consumer Group"이라는 Kafka 용어를 알아도, 그것이 EIP의 "Competing Consumers" 패턴과 동일한 문제를 해결한다는 사실을 모르면 두 세계의 지식이 연결되지 않습니다. 아래 매핑 테이블은 이미 습득한 Kafka 개념에 EIP 이름표를 붙여 어휘를 통일하려는 목적으로 작성했습니다.

| EIP 패턴 이름 | Kafka 구현체 / 개념 | 참조 문서 |
|---------------|---------------------|-----------|
| **Point-to-Point Channel** | 단일 Consumer Group이 토픽 소비 | `02-fundamentals/06-consumer-groups` |
| **Publish-Subscribe Channel** | 여러 Consumer Group이 동일 토픽 소비 | `02-fundamentals/06-consumer-groups` |
| **Competing Consumers** | Consumer Group 내 여러 인스턴스가 파티션 분할 처리 | `02-fundamentals/06-consumer-groups` |
| **Datatype Channel** | 1 토픽 = 1 스키마 원칙 | `02-fundamentals/07-schema-registry` |
| **Invalid Message Channel** | `DeserializationExceptionHandler` → 별도 토픽 | `03-spring-boot-integration/05-error-dlq` |
| **Dead Letter Channel** | `SeekToCurrentErrorHandler` + DLQ 토픽 | `03-spring-boot-integration/05-error-dlq` |
| **Guaranteed Delivery** | `acks=all` + `min.insync.replicas` + `enable.idempotence` | `02-fundamentals/16-transactions` |
| **Message Sequence** | 파티션 키 기반 순서 보장 | `02-fundamentals/06-consumer-groups` |
| **Event Message** | `events.*` 네이밍 토픽 (사실 통보) | 본 문서 §2.1 |
| **Command Message** | `commands.*` 네이밍 토픽 (행동 요청) | 본 문서 §2.1 |
| **Format Indicator** | Schema Registry subject + content-type 헤더 | `02-fundamentals/07-schema-registry` |
| **Channel Adapter** | Kafka Connect Source/Sink Connector | `07-connectors` (8문서 시리즈) |
| **Messaging Bridge** | MirrorMaker2 (Kafka↔Kafka), Kafka Connect (Kafka↔외부) | `02-fundamentals/19-geo-replication` |
| **Message Bus** | Kafka 전체 클러스터 + Schema Registry | 본 문서 §3.7 |
| **Content-Based Router** | Kafka Streams `split().branch()` | `17-messaging-patterns §3 Event Router` |
| **Event Envelope** | CloudEvents 표준 / Avro 래퍼 스키마 | `17-messaging-patterns §2 Event Envelope` |

이 테이블에서 주목할 점은 대부분의 EIP 패턴이 이미 다른 문서에서 다뤄졌다는 것입니다. 이 문서는 그 위에 새로운 개념 두 가지를 추가합니다. 첫째, **아직 명시적으로 다루지 않은 패턴들** — Message Construct(명령/문서/이벤트 유형 구분), Message Expiration, Messaging Bridge 등을 채웁니다. 둘째, **기존에 다룬 패턴들을 EIP 이름으로 재조명**하여 두 어휘 체계를 하나로 연결합니다.

매핑 테이블을 읽는 방법은 두 가지입니다. "Kafka를 먼저 배운 사람"이라면 왼쪽 EIP 이름을 보면서 "아, Consumer Group의 Competing Consumers적 역할이 이 이름이었구나"를 확인합니다. "EIP를 먼저 배운 사람"이라면 오른쪽 Kafka 구현체를 보면서 "Dead Letter Channel이 Kafka에서는 이렇게 구현되는구나"를 확인합니다. 두 방향 모두에서 유용한 참조표가 되도록 작성했습니다.

한 가지 더 짚어둘 점은, 이 매핑이 **1:1 대응이 아닌 경우**도 있다는 것입니다. 예를 들어 Point-to-Point Channel과 Pub/Sub Channel은 Kafka에서 동일한 토픽을 가리키며, 차이는 Consumer Group 수에 있습니다. 또한 Channel Adapter는 Kafka Connect 전체를 의미하지만, Kafka Connect 자체가 Source Connector(Inbound)와 Sink Connector(Outbound)로 나뉘므로 하나의 EIP 패턴이 두 방향의 구현체를 포함합니다. 패턴은 개념을 가리키고, 구현은 맥락에 따라 달라집니다.

---

## 2. Message Construct 패턴

### 2.1 Command Message vs Document Message vs Event Message

메시지를 보낼 때 우리는 암묵적으로 의도를 가집니다. 그 의도가 명시되지 않으면 수신자는 메시지를 보고 "이걸 어떻게 처리해야 하지?"를 스스로 해석해야 합니다. EIP는 이 의도를 세 가지 유형으로 분류합니다.

**Command Message**는 "X를 해줘"라는 행동 요청입니다. 발신자는 수신자가 특정 작업을 수행하기를 기대합니다. 중요한 특징은 수신자가 **정확히 하나**여야 한다는 점입니다. 두 명이 동시에 같은 명령을 처리하면 중복 실행이 발생합니다. Kafka에서 Command Message는 단일 Consumer Group(Point-to-Point Channel)과 결합해야 의미가 완성됩니다.

**Document Message**는 "이 데이터를 전달할게"입니다. 수신자가 그 데이터로 무엇을 할지는 수신자의 결정입니다. 발신자는 수신자의 반응에 관심이 없습니다. 주기적 보고서, 설정 파일 배포, 마스터 데이터 동기화가 여기 해당합니다. Document Message는 여러 수신자가 동시에 받아도 문제없는 경우가 많습니다.

**Event Message**는 "이런 일이 일어났어"입니다. 과거 사실의 통보입니다. 발신자는 이 사실에 누가 관심을 갖는지 알 필요가 없습니다. `OrderCreated`, `PaymentProcessed`, `InventoryReserved`가 전형적인 예입니다. Event Message는 Pub/Sub 채널과 자연스럽게 결합합니다. 여러 컨슈머 그룹(주문 서비스, 알림 서비스, 분석 서비스)이 각자 독립적으로 처리할 수 있습니다.

CQRS 아키텍처와의 관계도 이 분류에서 명확해집니다. Command Message는 Write Model로 들어가고, 처리 결과로 발생한 Event Message는 Read Model을 갱신하는 데 사용됩니다. Document Message는 두 모델 중 어느 쪽과도 독립적으로 존재할 수 있습니다.

세 유형을 구분하는 실용적인 판단 기준은 "메시지가 실패했을 때 누가 책임지는가"를 물어보는 것입니다. Command Message가 실패하면 **발신자가 재시도를 책임**집니다. 주문 생성 명령이 실패하면 사용자 화면에 오류가 표시되고, 다시 시도해야 합니다. Event Message가 실패(컨슈머 처리 실패)하면 **컨슈머가 재처리를 책임**집니다. 발신자는 이미 사실을 기록했고, 해당 사실에 어떤 서비스가 반응했는지 관리하지 않습니다. Document Message가 실패하면 **다음 발행 주기를 기다리거나** 별도의 보상 메커니즘이 필요합니다. 이 책임 구분이 재시도 정책, 멱등성 요구사항, DLQ 운영 방식을 결정하는 데 영향을 미칩니다.

토픽 네이밍 컨벤션은 의도를 코드 외부에서도 읽을 수 있게 만듭니다.

```
# Command Message 토픽 — 행동 요청
commands.order.create
commands.payment.process
commands.inventory.reserve

# Document Message 토픽 — 데이터 전달
documents.product.catalog
documents.config.feature-flags

# Event Message 토픽 — 사실 통보
events.order.created
events.payment.processed
events.inventory.reserved
```

Avro 스키마 수준에서도 의도를 명시할 수 있습니다. namespace를 `com.example.commands.order`(커맨드)와 `com.example.events.order`(이벤트)로 분리하면, 스키마만 보고도 메시지 유형을 구분할 수 있습니다.

```json
// Command Message 스키마 예시
{
  "type": "record",
  "name": "CreateOrderCommand",
  "namespace": "com.example.commands.order",
  "fields": [
    {"name": "commandId",   "type": "string", "doc": "멱등성을 위한 커맨드 식별자"},
    {"name": "issuedAt",    "type": "long",   "doc": "epoch millis"},
    {"name": "issuedBy",    "type": "string", "doc": "커맨드 발행 주체"},
    {"name": "customerId",  "type": "string"},
    {"name": "items",       "type": {"type": "array", "items": "OrderItem"}}
  ]
}

// Event Message 스키마 예시
{
  "type": "record",
  "name": "OrderCreatedEvent",
  "namespace": "com.example.events.order",
  "fields": [
    {"name": "eventId",     "type": "string", "doc": "이벤트 식별자 (재처리 감지용)"},
    {"name": "occurredAt",  "type": "long",   "doc": "사건 발생 시각 (epoch millis)"},
    {"name": "orderId",     "type": "string"},
    {"name": "customerId",  "type": "string"},
    {"name": "totalAmount", "type": "long"}
  ]
}
```

두 스키마를 비교하면 의도의 차이가 드러납니다. Command에는 `issuedBy`(누가 요청했는가)와 `commandId`(중복 요청 방지)가 있고, Event에는 `occurredAt`(언제 일어났는가)과 `eventId`(재처리 감지)가 있습니다. Command는 미래를 지시하고, Event는 과거를 기록합니다.

실무에서 흔한 실수는 Command와 Event를 같은 토픽에 섞는 것입니다. "주문 토픽이니까 주문 관련 메시지는 다 여기"라는 생각인데, 이렇게 하면 수신자가 메시지를 꺼낼 때마다 타입을 확인해야 하고, Command는 단일 소비자여야 한다는 제약과 Event는 다중 소비자가 가능하다는 특성이 충돌합니다. 의도별로 토픽을 분리하는 것이 Datatype Channel 원칙(§3.2)과도 일치합니다.

---

### 2.2 Format Indicator

시스템이 진화하면 메시지 형식도 변합니다. 문제는 변경이 일어날 때 발신자와 수신자가 항상 동시에 배포되지 않는다는 것입니다. 발신자가 v2 형식으로 메시지를 보내는데 수신자는 아직 v1만 이해한다면 어떻게 될까요? 이 문제를 해결하려면 메시지 자체에 "나는 어떤 형식이야"라고 표시해야 합니다. EIP는 이를 **Format Indicator** 패턴이라고 부릅니다.

Kafka에서 Format Indicator는 두 계층에서 동작합니다.

첫 번째는 **Kafka Record Header**입니다. 헤더는 페이로드와 별도로 키-값 쌍을 저장할 수 있는 공간입니다. `content-type` 헤더를 사용하면 역직렬화 전에 형식을 판단할 수 있습니다.

```java
// Producer: 형식 정보를 헤더에 포함
ProducerRecord<String, byte[]> record = new ProducerRecord<>(
    "events.order.created",
    orderId,
    avroBytes
);
record.headers()
    .add("content-type", "application/avro".getBytes())
    .add("schema-version", "2".getBytes())
    .add("ce-specversion", "1.0".getBytes());  // CloudEvents 호환 헤더

// Consumer: 헤더로 형식 판별 후 분기 처리
ConsumerRecord<String, byte[]> record = ...;
Header contentType = record.headers().lastHeader("content-type");
String format = new String(contentType.value());

if ("application/avro".equals(format)) {
    processAvro(record.value());
} else if ("application/json".equals(format)) {
    processJson(record.value());
}
```

두 번째는 **Schema Registry**입니다. Avro/Protobuf를 Schema Registry와 함께 사용할 때, 모든 직렬화된 바이트의 앞 5바이트는 `[magic byte][schema id]` 형태를 가집니다. 이 schema id로 Schema Registry에서 스키마를 조회하면 정확한 형식을 알 수 있습니다. Schema Registry의 subject 네이밍 전략은 그 자체로 암묵적인 Format Indicator입니다.

```
# TopicNameStrategy (기본): 토픽 이름 = 형식 계약
events.order.created-value → OrderCreatedEvent v1~vN

# TopicRecordNameStrategy: 토픽 내 다중 형식 허용
events.order.all-value:com.example.events.OrderCreatedEvent
events.order.all-value:com.example.events.OrderCancelledEvent
```

CloudEvents 표준(`17-messaging-patterns §2 Event Envelope` 참조)은 이벤트를 표준화된 봉투(envelope)로 감싸는 CNCF 스펙입니다. 이 봉투에는 `datacontenttype`이라는 필수 필드가 있어 페이로드의 형식을 명시합니다. `"datacontenttype": "application/avro"` 또는 `"datacontenttype": "application/json"` 형태입니다. 핵심 차이는 **형식 정보가 존재하는 위치**입니다. Kafka 헤더 방식은 메시지 본문과 별개인 메타데이터 영역에 형식 정보를 넣지만, CloudEvents는 메시지 본문(JSON 객체) 안에 `datacontenttype`을 포함시킵니다. 즉 봉투를 열면 형식 정보가 데이터와 함께 하나의 구조체 안에 있으므로, 헤더를 따로 관리하거나 읽어야 하는 부담이 없습니다.

```json
// CloudEvents 봉투 예시 — datacontenttype이 본문 안에 내장됨
{
  "specversion": "1.0",
  "type": "com.example.OrderCreated",
  "source": "/order-service",
  "id": "evt-001",
  "datacontenttype": "application/avro",
  "dataschema": "https://registry.example.com/schemas/ids/10",
  "data": "<Avro 바이너리 또는 Base64>"
}
```

Format Indicator가 없는 시스템에서는 형식 변경이 두려운 작업이 됩니다. "v2로 바꾸면 아직 v1만 처리하는 컨슈머가 깨지지 않을까?"라는 불안이 변경을 막습니다. 형식 정보가 메시지에 명시되면, 컨슈머가 모르는 형식을 만났을 때 우아하게 건너뛰거나 DLQ로 보낼 수 있습니다. 변경에 대한 두려움이 줄어드는 것입니다.

Schema Registry를 사용할 때 Format Indicator는 사실상 자동으로 구현됩니다. Avro 직렬화 시 앞 5바이트에 포함된 schema id가 역직렬화 시 정확한 스키마 버전을 가리키기 때문입니다. 이 메커니즘 덕분에 발신자가 v2 스키마로 보내고 수신자가 v1 스키마로 역직렬화해도, Schema Registry가 호환성을 보장하는 한 두 버전이 공존할 수 있습니다. `02-fundamentals/07-schema-registry`에서 다룬 Backward/Forward 호환성 전략이 Format Indicator와 결합하여 무중단 스키마 진화를 가능하게 합니다.

Format Indicator를 헤더로 직접 구현할 때 주의할 점은 헤더 값의 신뢰성입니다. 헤더는 프로듀서가 임의로 설정할 수 있어 조작 가능성이 있습니다. Schema Registry의 schema id는 브로커와 Registry가 협력하여 부여하므로 신뢰도가 높습니다. 보안이 중요한 시스템에서는 헤더만 믿지 말고 Schema Registry를 통한 검증을 병행하는 것이 안전합니다.

---

### 2.3 Message Expiration

일부 메시지는 시간이 지나면 의미를 잃습니다. "지금 당장 재고를 확인해"라는 요청은 5분 뒤에는 무의미합니다. "오늘 오전 9시 현재 상품 가격 목록"은 내일이 되면 사용할 수 없습니다. 이처럼 메시지가 유효한 시간 창이 있을 때, 그 창을 넘긴 메시지를 처리하면 오히려 해가 됩니다. JMS는 메시지별 TTL(Time-To-Live)을 지원합니다. 프로듀서가 TTL을 설정하면 브로커가 만료된 메시지를 자동으로 삭제합니다.

Kafka는 **토픽 단위**의 보존 정책을 지원하며, 각 토픽마다 다른 `retention.ms`를 설정할 수 있습니다(`kafka-topics --alter --topic <name> --config retention.ms=300000`). 그러나 같은 토픽 안에서 **메시지별로 다른 만료 시각**을 지정하는 기능은 네이티브로 제공하지 않습니다. 토픽 A는 5분, 토픽 B는 7일로 설정할 수 있지만, 토픽 A 안의 메시지 1은 5분, 메시지 2는 1시간처럼 개별 TTL을 부여할 수는 없습니다(`02-fundamentals/13-retention-compaction-strategies` 참조). 따라서 메시지별 만료가 필요하다면 애플리케이션 레이어에서 시뮬레이션해야 합니다.

구현 방법은 두 단계입니다. 프로듀서가 만료 시각을 헤더 또는 페이로드에 포함시키고, 컨슈머가 처리 전 만료 여부를 확인합니다.

```java
// Producer: 만료 시각을 헤더에 포함 (5분 유효)
long expiresAt = System.currentTimeMillis() + Duration.ofMinutes(5).toMillis();
ProducerRecord<String, InventoryCheckCommand> record = new ProducerRecord<>(
    "commands.inventory.check",
    inventoryCheckCommand
);
record.headers().add(
    "expires-at",
    String.valueOf(expiresAt).getBytes()
);
producer.send(record);

// Consumer: 처리 전 만료 확인
ConsumerRecord<String, InventoryCheckCommand> record = ...;
Header expiresAtHeader = record.headers().lastHeader("expires-at");

if (expiresAtHeader != null) {
    long expiresAt = Long.parseLong(new String(expiresAtHeader.value()));
    if (System.currentTimeMillis() > expiresAt) {
        log.warn("만료된 메시지 건너뜀: key={}, expiresAt={}", record.key(), expiresAt);
        expiredMessageCounter.increment();
        return; // 처리 건너뜀
    }
}

// 만료되지 않은 경우에만 처리
processInventoryCheck(record.value());
```

이 접근법에는 중요한 주의사항이 있습니다. **만료된 메시지는 토픽에서 즉시 삭제되지 않습니다.** 토픽 보존 정책(`retention.ms`)이 만료될 때까지 물리적으로 남아 있습니다. 따라서 토픽을 replay하면 만료된 메시지도 다시 읽힙니다. 컨슈머의 만료 체크 로직이 replay 시에도 동일하게 동작해야 합니다. 만약 이벤트 소싱 시나리오처럼 정확한 과거 재현이 필요하다면, 만료 체크를 현재 시각 기준이 아닌 처리 시각 기준으로 작성해야 할 수도 있습니다.

Command Message와 Message Expiration을 결합하면 시간 민감 작업의 안전한 처리가 가능합니다. 컨슈머 지연이 발생해 큐가 쌓였을 때, 이미 의미 없어진 명령들을 자동으로 건너뛰어 빠르게 현재 상태를 따라잡을 수 있습니다.

---

### 2.4 Message Sequence

하나의 논리적 메시지가 너무 커서 단일 Kafka Record에 담기 어려울 때, 또는 분산 처리를 위해 여러 파티션에 나눠야 할 때 Message Sequence 패턴이 필요합니다. EIP에서 Message Sequence는 "N개의 연속된 메시지가 모여 하나의 완전한 메시지를 구성한다"는 개념입니다. 각 메시지는 전체 시퀀스 내 자신의 위치(sequence number)와 전체 길이(total count)를 알아야 합니다.

`17-messaging-patterns §8 Event Chunking`에서 이미 대용량 이벤트를 분할하는 방법을 다뤘습니다. Message Sequence와 Event Chunking은 문제를 다른 관점에서 봅니다. **Event Chunking**은 대용량 페이로드를 분할하는 기술적 문제를 해결합니다. Kafka의 1MB 기본 메시지 크기 제한을 우회하거나, 네트워크 효율성을 높이기 위해 큰 페이로드를 조각냅니다. **Message Sequence**는 순서 보장이 핵심입니다. 여러 메시지가 특정 순서로 처리되어야 할 때, 그 순서를 명시적으로 지정합니다.

두 패턴의 공통점은 `correlationId`를 파티션 키로 사용한다는 것입니다. 같은 `correlationId`를 가진 메시지는 같은 파티션에 할당되어 순서가 보장됩니다.

```java
// Message Sequence: 순서 정보 포함 스키마
{
  "type": "record",
  "name": "OrderLineItemEvent",
  "fields": [
    {"name": "correlationId",   "type": "string", "doc": "전체 시퀀스 식별자"},
    {"name": "sequenceNumber",  "type": "int",    "doc": "현재 순서 (1-based)"},
    {"name": "totalInSequence", "type": "int",    "doc": "전체 메시지 수"},
    {"name": "isLast",          "type": "boolean","doc": "마지막 메시지 여부"},
    {"name": "payload",         "type": "OrderLineItem"}
  ]
}

// 파티션 키를 correlationId로 설정하여 순서 보장
for (int i = 0; i < lineItems.size(); i++) {
    OrderLineItemEvent event = OrderLineItemEvent.newBuilder()
        .setCorrelationId(orderId)
        .setSequenceNumber(i + 1)
        .setTotalInSequence(lineItems.size())
        .setIsLast(i == lineItems.size() - 1)
        .setPayload(lineItems.get(i))
        .build();

    producer.send(new ProducerRecord<>(
        "events.order.line-items",
        orderId,           // 파티션 키 = correlationId
        event
    ));
}
```

컨슈머 측에서는 Kafka Streams State Store를 활용해 시퀀스를 조립합니다. `correlationId`를 키로 부분 메시지를 상태 저장소에 누적하다가, `isLast == true`인 메시지가 도착하면 완전한 메시지를 조립해 다운스트림으로 내보냅니다. 이 패턴은 `17-messaging-patterns §8 Event Chunking`의 `aggregate()` 구현 예시와 동일한 구조를 가집니다.

Message Sequence를 사용할 때 주의해야 할 엣지 케이스는 **부분 실패**입니다. 시퀀스 중 하나의 메시지가 유실되면 전체 시퀀스가 영원히 불완전한 상태로 State Store를 점유합니다. 타임아웃 메커니즘을 함께 구현하거나, Claim Check 패턴(`17-messaging-patterns §7`)으로 시퀀스 전체를 외부 저장소에 저장하고 참조만 전달하는 방식이 더 안정적일 수 있습니다.

---

## 3. Messaging Channel 패턴

### 3.1 Point-to-Point vs Publish-Subscribe Channel

전통적인 메시징 시스템에서 Point-to-Point와 Publish-Subscribe는 **물리적으로 다른 구조**였습니다. JMS에서 P2P는 Queue, Pub/Sub은 Topic이라는 별도의 엔티티를 사용합니다. RabbitMQ에서 P2P는 Queue에 직접 바인딩, Pub/Sub은 Exchange를 통한 팬아웃입니다. 이 두 패턴 중 어느 것을 선택할지는 아키텍처 초기 단계에서 결정해야 했고, 한 번 선택하면 바꾸기 어려웠습니다.

Kafka는 이 이분법을 무너뜨립니다. **같은 토픽이 P2P이기도 하고 Pub/Sub이기도 합니다.** 관건은 Consumer Group의 수입니다.

```
# P2P: 하나의 Consumer Group이 토픽 전체를 소비
토픽: commands.order.create
  └── Consumer Group "order-processor" (3 인스턴스)
       파티션 0 → 인스턴스 A
       파티션 1 → 인스턴스 B
       파티션 2 → 인스턴스 C
  (각 메시지는 정확히 하나의 인스턴스만 처리)

# Pub/Sub: 여러 Consumer Group이 동일 토픽 소비
토픽: events.order.created
  ├── Consumer Group "notification-service"  (알림 발송)
  ├── Consumer Group "analytics-service"     (지표 집계)
  └── Consumer Group "inventory-service"     (재고 차감)
  (각 메시지를 세 그룹 모두가 독립적으로 처리)
```

이 이중성(duality)이 왜 강력한지는 설계 결정을 늦출 수 있다는 점에서 드러납니다. 처음에는 단일 Consumer Group으로 시작해도, 나중에 새로운 관심사가 생기면 Consumer Group만 추가하면 됩니다. 토픽 구조나 프로듀서 코드를 변경할 필요가 없습니다. RabbitMQ에서 Queue를 Exchange 기반 구조로 바꾸려면 상당한 리팩토링이 필요한 것과 대조됩니다.

설계 결정의 핵심 질문은 **"이 메시지에 관심 있는 소비자가 지금 하나인가, 또는 미래에 늘어날 가능성이 있는가?"**입니다. 명확히 하나이고 앞으로도 하나일 것이 확실하다면(예: 특정 마이크로서비스로만 보내는 Command) 단일 CG P2P로 충분합니다. 여러 팀이 관심 가질 수 있는 비즈니스 이벤트라면(예: 주문 생성됨) 처음부터 Pub/Sub 토픽으로 설계하는 것이 나중의 CG 추가를 자연스럽게 만듭니다.

RabbitMQ와 비교하면 Kafka의 이 이중성이 얼마나 독특한지 더 명확해집니다. RabbitMQ에서 P2P(Queue)로 설계된 시스템에 두 번째 소비자를 추가하려면 Exchange를 도입하고 Queue를 바인딩하는 구조로 전환해야 합니다. 이미 구독 중인 프로듀서와 컨슈머의 연결 방식이 달라지기 때문에 코드 변경이 불가피합니다. Kafka에서는 새로운 Consumer Group id 하나를 정의하고 연결하기만 하면 됩니다. 기존 프로듀서나 다른 Consumer Group은 전혀 영향을 받지 않습니다. 이것이 Kafka 기반 시스템이 사후 확장(Retroactive Extension)에 유리한 이유입니다.

---

### 3.2 Datatype Channel

Datatype Channel은 "하나의 채널(토픽)에는 하나의 데이터 타입만 담아야 한다"는 원칙입니다. 이 원칙이 중요한 이유는 수신자 관점에서 생각해보면 명확합니다. 수신자는 채널에서 메시지를 꺼낼 때 무엇이 들어있는지 알고 싶어합니다. 타입이 보장된다면 역직렬화 코드가 단순해지고, 스키마 진화도 단일 타입에 대해서만 고려하면 됩니다.

Kafka에서 이 원칙은 Schema Registry의 기본 전략인 `TopicNameStrategy`로 구현됩니다. 이 전략에서 subject 이름은 `{토픽명}-value` 형태이므로, 토픽당 하나의 스키마 계보(schema lineage)만 허용됩니다. 즉 토픽 이름이 곧 타입 계약입니다.

Datatype Channel을 위반하는 흔한 패턴은 하나의 토픽에 여러 이벤트 타입을 넣는 것입니다.

```
# 안티패턴: 여러 타입이 혼재
토픽: events.order.all
  메시지 1: OrderCreatedEvent
  메시지 2: OrderCancelledEvent
  메시지 3: OrderShippedEvent
```

이렇게 하면 컨슈머는 모든 타입을 역직렬화할 준비를 해야 하고, 새로운 이벤트 타입이 추가될 때마다 컨슈머 코드도 변경해야 합니다. 또한 `TopicNameStrategy` 하에서는 모든 타입이 동일한 subject에 등록되어 스키마 호환성 검사가 의미를 잃습니다.

만약 성능상의 이유로 여러 타입을 하나의 토픽에 담아야 한다면(파티션 수 절약, 관련 이벤트의 순서 보장 등), Schema Registry의 `TopicRecordNameStrategy`를 사용할 수 있습니다.

```java
// TopicRecordNameStrategy: 토픽 내 다중 타입 허용
props.put(KafkaAvroSerializerConfig.VALUE_SUBJECT_NAME_STRATEGY,
    TopicRecordNameStrategy.class.getName());
// subject: events.order.all-com.example.events.OrderCreatedEvent
// subject: events.order.all-com.example.events.OrderCancelledEvent
```

그러나 이 전략을 사용하면 Datatype Channel 원칙을 포기한 것이며, Event Router 패턴(`17-messaging-patterns §3`)이 반드시 필요해집니다. 타입 혼재 토픽에서 컨슈머가 원하는 타입만 선택적으로 처리해야 하기 때문입니다. 편의를 위한 타협이 다른 복잡성을 불러오는 전형적인 예입니다. 일반적으로는 Datatype Channel을 지키는 것이 장기적으로 시스템을 단순하게 유지합니다.

---

### 3.3 Invalid Message Channel & Dead Letter Channel

두 패턴은 이름이 비슷하지만 실패 지점이 다릅니다. **Invalid Message Channel**은 메시지를 처리조차 할 수 없는 경우, 즉 **역직렬화 실패**를 처리합니다. **Dead Letter Channel**은 역직렬화는 성공했지만 **비즈니스 로직 처리가 실패**한 경우를 처리합니다.

역직렬화 실패는 보통 스키마 비호환이나 데이터 손상에서 발생합니다. 이 메시지는 애플리케이션 코드까지 도달하지 못합니다. Kafka Streams에서는 `DeserializationExceptionHandler`로 이를 처리합니다.

```java
// Kafka Streams: Invalid Message Channel 구현
StreamsConfig config = new StreamsConfig(props);
// 역직렬화 실패 시 로그만 남기고 건너뜀 (LogAndContinueExceptionHandler)
props.put(StreamsConfig.DEFAULT_DESERIALIZATION_EXCEPTION_HANDLER_CLASS_CONFIG,
    LogAndContinueExceptionHandler.class);

// 또는 실패한 레코드를 별도 토픽으로 보내는 커스텀 핸들러
public class InvalidMessageChannelHandler implements DeserializationExceptionHandler {
    @Override
    public DeserializationHandlerResponse handle(
            ProcessorContext context,
            ConsumerRecord<byte[], byte[]> record,
            Exception exception) {
        // Raw bytes를 invalid-messages 토픽으로 전송
        Producer<String, byte[]> dlqProducer = ...;
        dlqProducer.send(new ProducerRecord<>(
            "invalid-messages",
            record.key() != null ? new String(record.key()) : null,
            record.value()  // 원본 바이트 보존
        ));
        return DeserializationHandlerResponse.CONTINUE;
    }
}
```

Dead Letter Channel은 비즈니스 로직 예외를 처리합니다. Spring Kafka에서는 `SeekToCurrentErrorHandler`(구버전) 또는 `DefaultErrorHandler`(신버전)와 `DeadLetterPublishingRecoverer`를 조합합니다. 이 구조는 `03-spring-boot-integration` 시리즈에서 자세히 다뤘으므로, 여기서는 두 채널의 의미론적 차이에 집중합니다.

Invalid Message Channel의 메시지는 **원인이 메시지 자체**에 있습니다. 메시지를 다시 시도해도 성공할 가능성이 낮습니다(스키마가 바뀌거나 데이터가 복구되지 않는 한). 반면 Dead Letter Channel의 메시지는 **원인이 일시적인 외부 상태**에 있을 수 있습니다. 데이터베이스가 일시적으로 응답 불가였거나, 외부 API가 순간적으로 에러를 반환한 경우입니다. 이런 메시지는 나중에 재처리 가능성이 있습니다.

두 채널을 별도로 운영하는 것은 이 재처리 가능성의 차이 때문입니다. Dead Letter Channel은 수동 또는 자동 재처리를 위한 대기소이고, Invalid Message Channel은 조사와 수동 복구를 위한 격리 공간입니다.

운영 관점에서 두 채널의 토픽 네이밍을 구분해두면 모니터링 알림을 분리할 수 있습니다. `invalid-messages.*` 토픽에 메시지가 쌓이면 스키마 배포 오류나 데이터 손상 가능성을 의심해야 하고, 담당자는 스키마 관리자나 데이터 엔지니어입니다. `dead-letter.*` 토픽에 메시지가 쌓이면 외부 의존성 장애나 비즈니스 로직 버그를 의심해야 하고, 담당자는 해당 도메인 개발자입니다. 같은 토픽에 두 종류를 섞으면 이 구분이 사라져 장애 대응이 느려집니다.

```
# 토픽 네이밍 권장 구조
invalid-messages.events.order.created   ← 역직렬화 실패 (Invalid Message Channel)
dead-letter.events.order.created        ← 처리 실패 (Dead Letter Channel)
```

Go 기반 컨슈머에서의 구현은 `08-go-integration/05-error-handling-dlq`에서 다룹니다. Spring Kafka와 달리 Go의 `franz-go`는 에러 핸들러 추상화를 제공하지 않으므로 컨슈머 루프 내에서 직접 분기 처리해야 합니다. 원칙은 동일하지만 구현 방식이 다른 대표적인 예입니다.

---

### 3.4 Guaranteed Delivery

메시지가 브로커에 도달했다가 브로커 장애로 유실되는 상황, 또는 네트워크 오류로 프로듀서가 전송 성공을 알지 못하는 상황에서 Guaranteed Delivery 패턴이 필요합니다. EIP에서 Guaranteed Delivery는 "메시지가 언젠가는 반드시 수신자에게 도달함을 보장한다"는 약속입니다. 전통적인 JMS 구현에서는 메시지 영속성(persistence)과 트랜잭션으로 이를 달성했습니다.

Kafka에서 Guaranteed Delivery는 세 가지 설정의 조합으로 구현됩니다. 이 세 가지가 모두 갖춰져야 진정한 Guaranteed Delivery입니다.

```properties
# Guaranteed Delivery를 위한 필수 프로듀서 설정

# 1. acks=all: 리더와 모든 ISR(In-Sync Replica)이 메시지를 수신해야 확인
acks=all

# 2. min.insync.replicas=2: 최소 2개 이상의 ISR이 쓰기를 확인해야 성공
# (브로커 설정 또는 토픽 설정)
min.insync.replicas=2

# 3. enable.idempotence=true: 네트워크 재시도 시 중복 쓰기 방지
enable.idempotence=true

# 4. retries: 충분히 높게 설정 (idempotence 활성화 시 자동으로 Integer.MAX_VALUE)
retries=2147483647

# 5. max.in.flight.requests.per.connection: idempotence와 함께 최대 5
max.in.flight.requests.per.connection=5
```

Kafka의 기본 설정인 `acks=1`은 **Guaranteed Delivery가 아닙니다.** 리더 브로커만 메시지를 받으면 성공 응답을 보내기 때문에, 리더가 팔로워에게 복제하기 전에 장애가 나면 메시지가 유실됩니다. 많은 서비스가 성능을 위해 기본값을 그대로 사용하는데, 이는 중요한 비즈니스 이벤트에 대해 묵시적으로 "유실 가능"을 허용하는 것입니다.

`enable.idempotence=true`가 왜 필요한지도 이해해야 합니다. `acks=all`에서 리더가 메시지를 쓰고 ACK를 보내기 전에 네트워크가 끊기면, 프로듀서는 실패로 판단해 재전송합니다. 하지만 브로커 입장에서는 이미 메시지를 받았으므로 두 번 저장됩니다. 멱등성 프로듀서는 PID(Producer ID)와 시퀀스 번호를 함께 보내 브로커가 중복을 감지하고 버릴 수 있게 합니다. `02-fundamentals/16-transactions`에서 이 메커니즘을 상세히 다뤘습니다.

Guaranteed Delivery가 보장하는 범위를 명확히 이해해야 오해가 없습니다. 이 설정이 보장하는 것은 **"브로커에 도달한 메시지가 지정된 복제본 수에 저장된다"**는 것입니다. 컨슈머가 메시지를 실제로 처리했는지는 Guaranteed Delivery 범위 밖입니다. 컨슈머가 메시지를 꺼내 처리하다가 실패해도, Kafka에는 메시지가 남아 있습니다. 이때 오프셋을 커밋하지 않으면 메시지를 재처리할 수 있습니다. 즉 Kafka에서 완전한 end-to-end 보장은 **프로듀서 Guaranteed Delivery + 컨슈머 at-least-once 처리 + 컨슈머 멱등성**의 세 가지 조합으로 달성됩니다. 세 가지 중 하나라도 빠지면 "언젠가 정확히 한 번 처리"(effectively-once)가 깨집니다.

Redpanda 같은 Kafka 호환 브로커를 사용할 때도 동일한 설정이 적용됩니다. Redpanda는 Kafka API를 완전히 구현하므로, 프로듀서 설정은 바꿀 필요가 없습니다. 단, Redpanda는 Raft 기반 복제를 사용하므로 `min.insync.replicas`의 내부 동작 원리가 다릅니다. 효과는 동일하지만 장애 내성 수준이 약간 달라질 수 있으므로, 프로덕션 배포 전 브로커 문서를 확인하는 것이 좋습니다.

---

### 3.5 Channel Adapter

Channel Adapter는 메시징 인프라를 이해하지 못하는 외부 시스템을 메시지 채널에 연결하는 컴포넌트입니다. 레거시 데이터베이스, REST API, 파일 시스템 같은 시스템은 Kafka 프로토콜을 모릅니다. Channel Adapter가 이 시스템들과 Kafka 사이의 변환과 통신을 담당합니다.

Kafka Connect가 바로 이 Channel Adapter 패턴의 현대적 구현입니다. Source Connector는 외부 시스템에서 Kafka로 데이터를 가져오고(Inbound Channel Adapter), Sink Connector는 Kafka에서 외부 시스템으로 데이터를 내보냅니다(Outbound Channel Adapter).

```
# Source Connector (Inbound Channel Adapter): 외부 → Kafka
MySQL CDC (Debezium) ──→ [Kafka Connect] ──→ events.db.orders
REST API             ──→ [Kafka Connect] ──→ events.weather.updates
파일 시스템           ──→ [Kafka Connect] ──→ events.file.uploads

# Sink Connector (Outbound Channel Adapter): Kafka → 외부
events.user.analytics ──→ [Kafka Connect] ──→ Elasticsearch
events.order.completed ──→ [Kafka Connect] ──→ PostgreSQL DW
events.notification    ──→ [Kafka Connect] ──→ SendGrid API
```

JDBC Source Connector의 설정 예시를 통해 Channel Adapter의 실제 모습을 보겠습니다.

```json
{
  "name": "orders-source-connector",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:mysql://legacy-db:3306/orders",
    "connection.user": "kafka_reader",
    "connection.password": "${file:/opt/kafka/secrets:db.password}",
    "table.whitelist": "orders,order_items",
    "mode": "timestamp+incrementing",
    "timestamp.column.name": "updated_at",
    "incrementing.column.name": "id",
    "topic.prefix": "events.legacy.",
    "poll.interval.ms": "1000"
  }
}
```

이 설정 하나로 `legacy-db`의 `orders` 테이블 변경사항이 `events.legacy.orders` 토픽으로 자동 발행됩니다. 레거시 MySQL 서버는 Kafka의 존재를 전혀 모르고, 변경도 필요 없습니다. Channel Adapter가 두 세계의 경계에서 통역사 역할을 합니다. Kafka Connect의 전체 생태계는 `07-connectors` 8문서 시리즈에서 상세히 다룹니다.

---

### 3.6 Messaging Bridge

Messaging Bridge는 두 개의 분리된 메시징 시스템을 연결합니다. Channel Adapter가 "메시징 시스템 + 비-메시징 시스템" 간의 연결이라면, Messaging Bridge는 "메시징 시스템 + 메시징 시스템" 간의 연결입니다. 두 Kafka 클러스터를 연결하거나, Kafka와 RabbitMQ를 연결하는 것이 여기에 해당합니다.

Bridge가 필요한 상황은 크게 세 가지입니다. 첫째, **지리적 분리** — 서울 데이터센터와 싱가포르 데이터센터의 Kafka 클러스터를 동기화해야 할 때. 둘째, **기술 이기종** — 기존 RabbitMQ 기반 시스템과 새로 도입한 Kafka를 단계적으로 통합할 때. 셋째, **조직 경계** — 다른 팀이 운영하는 Kafka 클러스터끼리 특정 토픽만 공유해야 할 때.

Kafka↔Kafka Bridge는 **MirrorMaker2(MM2)**로 구현합니다. MM2는 `02-fundamentals/19-geo-replication`에서 상세히 다뤘으며, 여기서는 Bridge 패턴 관점의 핵심만 짚습니다.

```
[서울 Kafka Cluster]                [싱가포르 Kafka Cluster]
  events.order.created  ──MM2──→  seoul.events.order.created
  events.payment.done   ──MM2──→  seoul.events.payment.done

# MM2가 source 클러스터 이름을 prefix로 추가 (토픽 충돌 방지)
# offset 매핑도 MM2가 관리하여 양방향 동기화 지원
```

Kafka↔RabbitMQ Bridge는 Kafka Connect의 RabbitMQ Source/Sink Connector로 구현합니다. 단방향이므로 방향을 명확히 결정해야 합니다. 전환 중인 시스템이라면 RabbitMQ → Kafka 방향(레거시에서 신규로)이 일반적입니다.

Bridge 도입 전 고려해야 할 질문이 있습니다. **"클러스터를 통합할 수 있는가?"** Bridge는 두 시스템 간 지연(latency)을 추가하고, Bridge 자체가 장애 지점이 됩니다. 단순히 관리 편의를 위해 분리된 클러스터라면, Bridge를 추가하는 대신 클러스터를 통합하는 것이 더 나을 수 있습니다. Bridge는 지리적 분리나 조직 경계처럼 통합이 불가능한 상황에서 의미가 있습니다.

---

### 3.7 Message Bus

Message Bus는 여러 시스템이 공유하는 메시지 교환 인프라입니다. 각 시스템은 Bus에 메시지를 발행하거나 구독함으로써, 서로를 직접 알지 않고도 통신합니다. 2000년대 ESB(Enterprise Service Bus)가 이 역할을 했습니다. ESB는 메시지 변환, 라우팅, 프로토콜 변환 등의 로직을 Bus 자체에 내장했습니다. 시스템들은 ESB에 연결만 하면 됐고, 통합 로직은 ESB가 담당했습니다.

"Kafka is the new ESB"라는 말이 있습니다. 이 말은 반은 맞고 반은 틀립니다. Kafka는 확실히 Message Bus 역할을 합니다. 수십 개의 서비스가 Kafka라는 공통 Bus를 통해 이벤트를 주고받고, 어떤 서비스가 Bus에 연결되어 있는지 서로 알 필요가 없습니다.

그러나 핵심적인 차이가 있습니다. **ESB는 로직이 Bus 안에 있고, Kafka는 로직이 엔드포인트에 있습니다.**

```
# ESB 모델: Bus가 지능을 가짐
[시스템 A] → [ESB: 변환+라우팅+오케스트레이션] → [시스템 B]
                        ^
                  Bus가 모든 것을 알고 결정

# Kafka 모델: Bus는 바보, 엔드포인트가 지능을 가짐
[서비스 A] → [Kafka: 단순 저장+전달] → [서비스 B의 Kafka Streams]
                                              ^
                                     서비스 B가 직접 변환+처리
```

ESB의 문제는 Bus가 너무 많은 것을 알게 된다는 점입니다. 새로운 통합이 필요할 때마다 ESB 설정을 변경해야 하고, ESB는 거대한 단일 장애점이 됩니다. Kafka 기반 Message Bus에서는 Bus(Kafka 클러스터)는 단순히 메시지를 저장하고 전달합니다. 변환, 필터링, 라우팅은 각 서비스가 자신의 Consumer에서 처리합니다.

Kafka를 Message Bus로 효과적으로 사용하기 위한 두 가지 인프라가 있습니다. 첫째, **Schema Registry**입니다. 모든 서비스가 공유하는 스키마 저장소로, "Bus에서 오는 메시지의 형식이 무엇인가"를 중앙에서 관리합니다. 이것이 없으면 서비스들이 서로 비공식 채널로 스키마를 공유해야 합니다. 둘째, **토픽 네이밍 컨벤션**입니다. `{메시지타입}.{도메인}.{이벤트명}` 형태의 일관된 이름이 Bus에서 관련 이벤트를 찾을 수 있게 합니다.

```
# Kafka as Message Bus: 토픽 네이밍으로 느슨한 결합 달성
events.order.created     → 주문 생성됨 (주문 도메인)
events.order.cancelled   → 주문 취소됨
events.payment.processed → 결제 완료됨 (결제 도메인)
events.inventory.updated → 재고 변경됨 (재고 도메인)

# 새 서비스가 Bus에 합류: Kafka 설정만 추가, 다른 서비스 변경 없음
new Consumer Group "loyalty-service"
  subscribes to: events.order.created, events.payment.processed
```

Message Bus의 진정한 가치는 느슨한 결합(Loose Coupling)입니다. 주문 서비스는 자신의 `events.order.created`를 누가 구독하는지 알 필요가 없습니다. 포인트 서비스, 분석 서비스, 알림 서비스가 독립적으로 구독합니다. 새로운 서비스가 생겨도 주문 서비스 코드는 변경되지 않습니다. 이것이 EDA(Event-Driven Architecture)와 Message Bus가 함께 강력한 이유입니다.

그러나 Message Bus가 만능 해결책이 아니라는 점도 기억해야 합니다. Bus를 통한 느슨한 결합은 **추적 가능성(Traceability) 저하**라는 대가를 요구합니다. "이 이벤트가 어디서 소비되는가"를 파악하려면 모든 Consumer Group을 조회해야 합니다. ESB는 중앙 설정 파일 하나를 보면 전체 데이터 흐름을 파악할 수 있었습니다. Kafka 기반 Bus에서는 Schema Registry의 subject 목록, Consumer Group 목록, 그리고 각 서비스의 코드를 종합해야 합니다. Confluent Control Center나 Redpanda Console 같은 관리 도구가 이 가시성 문제를 부분적으로 해결하지만, 완전한 답은 아닙니다.

두 번째 주의점은 **스키마 거버넌스**입니다. ESB에서는 메시지 스키마를 ESB 관리자가 중앙에서 통제했습니다. Kafka Bus에서는 각 팀이 자신의 토픽 스키마를 Schema Registry에 등록합니다. 명확한 거버넌스가 없으면 스키마가 빠르게 파편화됩니다. `02-fundamentals/11-topic-governance-gitops`에서 다루는 GitOps 기반 토픽/스키마 거버넌스가 이 문제를 조직적으로 해결하는 방법입니다.

---

## 4. 패턴 선택 가이드

이 문서에서 다룬 패턴들을 실제 설계 결정에 적용할 때 도움이 되는 의사결정 흐름을 정리합니다.

**메시지 유형 선택 (§2.1)**

메시지를 설계할 때 가장 먼저 "이 메시지의 의도가 무엇인가"를 묻습니다. 수신자에게 특정 행동을 요청한다면 Command Message이고, 단일 Consumer Group + P2P Channel 조합을 선택합니다. 비즈니스 사실을 여러 관심자에게 알린다면 Event Message이고, 여러 Consumer Group + Pub/Sub Channel 조합을 선택합니다. 데이터를 전달하되 수신자의 반응에 무관심하다면 Document Message입니다.

**채널 선택 (§3.1~3.2)**

- 처리자가 정확히 하나여야 한다 → Point-to-Point (단일 CG)
- 여러 처리자가 독립적으로 소비해야 한다 → Publish-Subscribe (다중 CG)
- 채널에 담기는 타입이 하나다 → Datatype Channel (TopicNameStrategy 기본값)
- 불가피하게 여러 타입을 한 채널에 담아야 한다 → TopicRecordNameStrategy + Event Router 필수

**신뢰성 요구사항 (§3.3~3.4)**

- 역직렬화 실패 메시지를 격리해야 한다 → Invalid Message Channel
- 처리 실패 메시지를 나중에 재처리해야 한다 → Dead Letter Channel
- 메시지 유실이 절대 허용되지 않는다 → Guaranteed Delivery (acks=all + min.insync.replicas + enable.idempotence)

**통합 패턴 (§3.5~3.7)**

- 외부 시스템(DB, REST API, 파일)을 Kafka에 연결해야 한다 → Channel Adapter (Kafka Connect)
- 두 Kafka 클러스터를 연결해야 한다 → Messaging Bridge (MirrorMaker2)
- 여러 서비스가 공통 이벤트 인프라를 공유해야 한다 → Message Bus (Kafka + Schema Registry + 토픽 네이밍 컨벤션)

이 가이드는 출발점입니다. 실제 결정에는 팀 규모, 기존 인프라, 성능 요구사항 등 맥락이 더해져야 합니다. 패턴은 답을 주는 것이 아니라, 올바른 질문을 하도록 돕습니다.

---

## 참고 자료

- **Enterprise Integration Patterns** — Gregor Hohpe & Bobby Woolf (2003). EIP 패턴의 원전. https://www.enterpriseintegrationpatterns.com/
- **Confluent EIP Series** — 65개 EIP 패턴의 Kafka 매핑 분석. https://www.confluent.io/blog/apache-kafka-vs-enterprise-service-bus-esb-friendsettle-debate/
- **CloudEvents Specification v1.0** — Format Indicator 표준화. https://cloudevents.io/
- **Apache Kafka Documentation: Producer Configs** — `acks`, `enable.idempotence` 상세 설명. https://kafka.apache.org/documentation/#producerconfigs
- `17-messaging-patterns.md` — Event Envelope, Event Router, Claim Check, Event Chunking 패턴 (본 문서의 선행 학습)
- `02-fundamentals/06-consumer-groups` — Consumer Group 메커니즘 (P2P/Pub-Sub 이중성 기반)
- `02-fundamentals/07-schema-registry` — Schema Registry, TopicNameStrategy vs TopicRecordNameStrategy
- `02-fundamentals/16-transactions` — 멱등성 프로듀서, Guaranteed Delivery 메커니즘
- `02-fundamentals/19-geo-replication` — MirrorMaker2 Messaging Bridge 상세
- `07-connectors` — Kafka Connect Channel Adapter 전체 8문서 시리즈
