# 17. 메시징 패턴 (Enterprise Integration Patterns)

다양한 시스템 간의 메시지 교환 문제를 해결하는 검증된 패턴들을 이벤트 스트리밍 컨텍스트에서 이해하고 적용한다

## 학습 목표

- Enterprise Integration Patterns(EIP)이 이벤트 스트리밍에서 어떻게 진화했는지 이해한다
- 메시지 변환/라우팅/분할 패턴을 실무에 적용하는 방법을 파악한다
- Claim Check 패턴으로 대용량 페이로드를 효율적으로 처리하는 전략을 이해한다
- Event Envelope과 CloudEvents 표준의 관계를 파악한다

---

## 1. Enterprise Integration Patterns과 이벤트 스트리밍

### 패턴의 기원

2003년 Gregor Hohpe와 Bobby Woolf가 출간한 "Enterprise Integration Patterns"은 서로 다른 시스템을 메시지로 연결할 때 반복해서 등장하는 문제들을 65개의 패턴으로 정리했습니다. 당시의 기술적 배경은 JMS(Java Message Service), AMQP, MSMQ 같은 전통적인 메시지 브로커였습니다. 메시지는 큐(Queue)에 쌓이고, 컨슈머가 꺼내 처리한 뒤 삭제하는 방식이었습니다.

이후 Apache Kafka가 등장하면서 메시징의 패러다임이 바뀌었습니다. 핵심 차이는 **영구 저장(Persistent Storage)**입니다. 전통적인 브로커는 메시지를 소비하면 사라지지만, Kafka는 설정된 보존 기간 동안 메시지를 유지합니다. 이로 인해 세 가지 새로운 능력이 생겼습니다.

1. **재처리(Replayability)**: 오프셋을 되감아 과거 이벤트를 다시 처리할 수 있습니다
2. **다중 소비자(Multiple Consumers)**: 같은 이벤트를 여러 컨슈머 그룹이 독립적으로 소비할 수 있습니다
3. **순서 보장(Ordering)**: 파티션 키가 같은 이벤트는 파티션 내에서 순서가 보장됩니다

### EIP 패턴이 여전히 유효한 이유

기술이 바뀌어도 문제의 본질은 변하지 않습니다. 레거시 시스템의 XML 이벤트를 JSON으로 변환하는 문제, 주문 이벤트에서 배송 정보만 추출하는 문제, 1MB를 넘는 이미지를 이벤트에 포함시키는 문제는 Kafka 시대에도 동일하게 발생합니다. EIP 패턴은 이러한 보편적 문제에 대한 이름과 해결책을 제공합니다. 패턴에 이름을 붙이는 것 자체가 팀 내 소통 비용을 줄여 주기 때문입니다. "이건 Claim Check 패턴으로 풀면 돼"라는 한 마디가 수십 줄의 설명을 대신합니다.

### 이 문서에서 다루는 8가지 패턴

원래 EIP 책에는 65개의 패턴이 있습니다. 이 문서는 Confluent가 이벤트 스트리밍 컨텍스트에서 특히 중요하다고 정리한 8가지 패턴에 집중합니다.

| 카테고리 | 패턴 | 핵심 질문 | Kafka Streams 연산자 |
|----------|------|-----------|---------------------|
| **메시지 구조** | Event Envelope | 메타데이터와 페이로드를 어떻게 분리하는가? | Record Headers |
| **메시지 구조** | Event Standardizer | 다양한 소스를 공통 형식으로 어떻게 통일하는가? | `mapValues()` |
| **라우팅** | Event Router | 이벤트를 속성에 따라 어떻게 분기하는가? | `split().branch()` |
| **구조 변환** | Event Splitter | 복합 이벤트를 어떻게 단일 이벤트로 분리하는가? | `flatMap()` |
| **형식 변환** | Event Translator | 스키마/형식을 어떻게 변환하는가? | `mapValues()` |
| **필터링** | Content Filter | 불필요한 필드를 어떻게 제거하는가? | `mapValues()` |
| **대용량 처리** | Claim Check | 대용량 페이로드를 어떻게 외부화하는가? | 외부 저장소(S3) |
| **대용량 처리** | Event Chunking | 대용량 이벤트를 어떻게 분할 전송하는가? | `aggregate()` + State Store |

### 이벤트 스트리밍에서의 패턴 구현 위치

```
Producer --> [Kafka Topic A] --> Processor --> [Kafka Topic B] --> Consumer
                                     ^
                                  여기서 패턴 적용:
                                  - Event Router   : split().branch() → 여러 토픽으로 분기
                                  - Event Translator: mapValues()     → 스키마 변환
                                  - Content Filter : mapValues()     → 필드 제거
                                  - Event Splitter : flatMap()       → 1:N 분리
```

Kafka Streams는 이 "Processor" 역할을 스트림 처리 로직으로 구현하는 가장 자연스러운 방법입니다. 아래 섹션들은 각 패턴이 Kafka Streams에서 어떤 연산자로 구현되는지를 중심으로 설명합니다.

### 전통적 메시징 vs 이벤트 스트리밍 패턴 적용 비교

전통적인 메시지 브로커(JMS/AMQP)에서 EIP 패턴을 적용할 때와 Kafka에서 적용할 때는 몇 가지 근본적인 차이가 있습니다.

**소비 모델**: JMS는 큐에서 메시지를 꺼내면 사라지므로 하나의 컨슈머만 처리할 수 있습니다. Kafka는 컨슈머 그룹마다 독립적인 오프셋을 가지므로, 동일한 이벤트에 Event Router, Content Filter, Claim Check를 각각 다른 컨슈머 그룹이 독립적으로 적용할 수 있습니다. 이는 패턴 조합의 유연성을 크게 높입니다.

**재처리**: JMS에서 Event Translator를 잘못 구현하면 원본 메시지를 잃습니다. Kafka에서는 소스 토픽의 이벤트가 보존 기간 내에 남아 있으므로, 번역기를 수정한 뒤 오프셋을 되감아 재처리할 수 있습니다. 패턴 구현 오류를 안전하게 복구할 수 있는 것입니다.

**스케일**: JMS 브로커는 패턴 적용 로직을 브로커 내부(필터, 라우터)에서 실행합니다. Kafka에서는 패턴 로직이 Kafka Streams 애플리케이션(외부 프로세스)에서 실행됩니다. 처리 용량이 부족하면 Streams 애플리케이션 인스턴스만 늘리면 됩니다.

---

## 2. Event Envelope

### 패턴 개요

Event Envelope은 이벤트를 **메타데이터(헤더) + 페이로드**의 두 층으로 감싸는 패턴입니다. 편지(Letter)를 봉투(Envelope)에 넣는 것과 동일한 개념입니다. 봉투에는 수신자 주소, 발신자 주소, 우편번호가 적혀 있어 우체국은 봉투만 보고 배달 경로를 결정합니다. 편지 내용을 열어보지 않아도 됩니다.

이 비유는 이벤트 스트리밍에서도 그대로 적용됩니다. 라우터나 필터 같은 중간 처리 노드가 라우팅 결정을 내릴 때 무거운 페이로드를 역직렬화할 필요가 없습니다. 헤더만 검사하면 됩니다. 이는 특히 Avro나 Protobuf처럼 역직렬화 비용이 있는 포맷에서 성능 차이를 만들어 냅니다.

### CloudEvents 표준

CloudEvents는 CNCF(Cloud Native Computing Foundation)가 정의한 이벤트 메타데이터 표준입니다. 벤더 종속성 없이 이벤트 메타데이터를 표현하는 공통 언어를 제공하는 것이 목적입니다.

```json
{
  "specversion": "1.0",
  "type": "com.example.order.created",
  "source": "https://order-service/orders",
  "id": "A234-1234-1234",
  "time": "2024-01-15T10:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "ORD-9001",
    "customerId": "CUST-123",
    "totalAmount": 49900
  }
}
```

핵심 필드의 역할:
- `specversion`: CloudEvents 스펙 버전 (현재 1.0)
- `type`: 이벤트 유형. 역방향 DNS 표기법을 사용하여 유일성 보장
- `source`: 이벤트 발생 시스템의 URI
- `id`: 소스 내에서 유일한 이벤트 ID (`source` + `id` 조합이 전역 유일)
- `time`: 이벤트 발생 시각 (ISO 8601 형식)

### 메타데이터 위치 선택: Kafka 헤더 vs Avro 페이로드

Avro를 사용하는 환경에서 가장 먼저 부딪히는 질문이 "메타데이터를 어디에 넣는가?"입니다. Avro 스키마 안에 메타데이터 필드를 포함시킬 수도 있고, Kafka Record Headers에만 넣을 수도 있습니다. 선택지는 세 가지이며, 각각 트레이드오프가 다릅니다.

**방식 A — Kafka Record Headers만 사용**

메타데이터 전부를 Kafka 헤더에 넣고, Avro 페이로드에는 순수 비즈니스 데이터만 담는 방식입니다.

```java
// 헤더: ce-type, ce-source, ce-id, trace-id
record.headers()
    .add("ce-type", "com.example.order.created".getBytes(UTF_8))
    .add("ce-source", "/order-service".getBytes(UTF_8));

// Avro 페이로드: OrderCreated — orderId, customerId, totalAmount만 포함
```

Avro 스키마가 비즈니스 필드에만 집중하므로 깔끔하고, 라우터가 역직렬화 없이 헤더만으로 판단할 수 있습니다. 단점은 헤더가 `byte[]` 타입이라 타입 안전성이 없고, Schema Registry의 호환성 검사 대상에서 제외된다는 점입니다. 헤더 키 이름 규약은 팀 간 문서로만 공유해야 하므로 규모가 커지면 관리가 어려워집니다.

**방식 B — Avro 스키마에 Envelope 필드 포함**

메타데이터를 Avro 스키마 자체에 포함시키는 방식입니다.

```json
{
  "type": "record",
  "name": "OrderEnvelope",
  "fields": [
    {"name": "eventId",   "type": "string"},
    {"name": "eventType", "type": "string"},
    {"name": "source",    "type": "string"},
    {"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "payload",   "type": "OrderCreated"}
  ]
}
```

Schema Registry가 메타데이터 필드까지 관리하므로 타입 안전성이 보장되고, 스키마 진화(호환성 검사)도 적용됩니다. 하지만 라우터가 메타데이터를 읽으려면 반드시 Avro 역직렬화를 거쳐야 합니다. Avro는 부분 역직렬화를 지원하지 않으므로 전체 메시지를 파싱하는 비용이 발생합니다. 이벤트 타입 하나만 확인하려고 수백 바이트의 페이로드를 전부 디코딩하는 것은 비효율적입니다.

**방식 C — 하이브리드 (실무 표준)**

대부분의 실무 환경에서 채택하는 방식입니다. **라우팅·인프라 메타데이터는 Kafka 헤더에, 비즈니스 메타데이터는 Avro 페이로드에** 분리합니다.

```
Kafka Record
├── Headers (라우팅/인프라 — 역직렬화 없이 접근 가능)
│   ├── ce-type: "com.example.order.created"     ← 라우터가 사용
│   ├── ce-source: "/order-service"              ← 모니터링이 사용
│   ├── ce-id: "550e8400-e29b-..."               ← 멱등성 검사
│   └── trace-id: "abc-def-ghi"                  ← 분산 추적
│
└── Value (Avro — Schema Registry 관리, 타입 안전)
    ├── orderId: "ORD-9001"
    ├── customerId: "CUST-123"
    ├── totalAmount: 49900
    └── createdAt: 1705312800000
```

하이브리드 방식의 판단 기준은 단순합니다: **"이 필드를 역직렬화 없이 읽어야 하는 컴포넌트가 있는가?"** 라우터, 모니터링 도구, 분산 추적 시스템처럼 이벤트 내용을 이해할 필요 없이 메타데이터만으로 동작하는 컴포넌트가 사용하는 정보는 헤더에 넣습니다. 주문 금액, 고객 ID처럼 비즈니스 로직이 소비하는 정보는 Avro 페이로드에 넣어 Schema Registry의 보호를 받게 합니다.

| 필드 유형 | 위치 | 예시 | 이유 |
|-----------|------|------|------|
| 이벤트 타입 | 헤더 | `ce-type` | 라우터가 역직렬화 없이 분기 |
| 이벤트 소스 | 헤더 | `ce-source` | 모니터링/로깅에서 원본 추적 |
| 트레이스 ID | 헤더 | `trace-id` | 분산 추적 시스템이 사용 |
| 멱등성 키 | 헤더 | `ce-id` | 컨슈머가 중복 체크 시 빠른 접근 |
| 비즈니스 ID | Avro | `orderId` | 비즈니스 로직에서만 사용 |
| 금액/수량 | Avro | `totalAmount` | 비즈니스 로직에서만 사용 |
| 비즈니스 타임스탬프 | Avro | `createdAt` | 비즈니스 의미가 있는 시각 |

### Kafka에서의 구현: Record Headers 활용

Kafka는 메시지마다 헤더(Headers)를 첨부할 수 있습니다. CloudEvents 메타데이터를 헤더에 넣으면 페이로드와 분리하여 검사할 수 있습니다.

```java
// Producer: CloudEvents 헤더 추가
ProducerRecord<String, OrderCreated> record = new ProducerRecord<>(
    "orders", orderId, orderCreatedEvent
);

record.headers()
    .add("ce-specversion", "1.0".getBytes())
    .add("ce-type", "com.example.order.created".getBytes())
    .add("ce-source", "https://order-service/orders".getBytes())
    .add("ce-id", UUID.randomUUID().toString().getBytes())
    .add("ce-time", Instant.now().toString().getBytes());

producer.send(record);
```

```java
// Consumer: 헤더만 검사하여 처리 여부 결정
ConsumerRecord<String, byte[]> record = ...; // 역직렬화 전

String eventType = new String(
    record.headers().lastHeader("ce-type").value()
);

if ("com.example.order.created".equals(eventType)) {
    // 페이로드를 이제 역직렬화하여 처리
    OrderCreated event = deserialize(record.value());
    processOrder(event);
} else {
    // 관심 없는 이벤트 타입은 역직렬화 비용 없이 스킵
    log.debug("Skipping event type: {}", eventType);
}
```

### 공통 헤더 자동 부착

프로듀서마다 수동으로 헤더를 추가하면 누락이 발생합니다. 자동 부착 방법은 세 가지가 있으며, 실무에서는 Spring 빈으로 관리할 수 있는 방식이 선호됩니다.

#### 방법 1: KafkaTemplate 래퍼 빈 (권장)

가장 Spring-idiomatic한 방법입니다. `KafkaTemplate`을 감싸는 전용 빈을 만들어 모든 발행에 공통 헤더를 부착합니다. Spring DI를 자유롭게 활용할 수 있고, 테스트에서 목킹이 쉽습니다.

```java
@Component
@RequiredArgsConstructor
public class EnvelopedKafkaTemplate<V> {

    private final KafkaTemplate<String, V> delegate;

    @Value("${spring.application.name}")
    private String serviceName;

    public CompletableFuture<SendResult<String, V>> send(String topic, String key, V value) {
        return send(topic, key, value, null);
    }

    public CompletableFuture<SendResult<String, V>> send(
            String topic, String key, V value, @Nullable String eventType) {

        ProducerRecord<String, V> record = new ProducerRecord<>(topic, key, value);
        Headers headers = record.headers();

        // 공통 헤더 자동 부착
        headers.add("ce-id", UUID.randomUUID().toString().getBytes(UTF_8));
        headers.add("ce-source", serviceName.getBytes(UTF_8));
        headers.add("ce-time", Instant.now().toString().getBytes(UTF_8));

        // 이벤트별 헤더 (호출자가 지정)
        if (eventType != null) {
            headers.add("ce-type", eventType.getBytes(UTF_8));
        }

        // 분산 추적: MDC에서 trace-id 전파
        String traceId = MDC.get("traceId");
        if (traceId != null) {
            headers.add("trace-id", traceId.getBytes(UTF_8));
        }

        return delegate.send(record);
    }
}
```

```java
// 사용측: 래퍼만 주입받아 사용
@Service
@RequiredArgsConstructor
public class OrderProducer {

    private final EnvelopedKafkaTemplate<OrderCreated> kafkaTemplate;

    public void publish(OrderCreated event) {
        kafkaTemplate.send(
            "orders",
            event.getOrderId(),
            event,
            "com.example.order.created"  // ce-type만 이벤트별로 지정
        );
        // ce-id, ce-source, ce-time, trace-id는 자동 부착
    }
}
```

#### 방법 2: KafkaTemplate.setProducerInterceptor() (Spring 빈 주입 가능)

Spring Kafka 2.8+에서 `KafkaTemplate`에 직접 `ProducerInterceptor`를 설정할 수 있습니다. `interceptor.classes` 프로퍼티와 달리 **Kafka가 아닌 Spring이 인스턴스를 관리**하므로, `@Value`, `@Autowired` 등 Spring DI를 자유롭게 활용할 수 있습니다.

```java
@Configuration
public class KafkaProducerConfig {

    @Bean
    public KafkaTemplate<String, Object> kafkaTemplate(
            ProducerFactory<String, Object> pf,
            CommonHeaderInterceptor interceptor) {

        KafkaTemplate<String, Object> template = new KafkaTemplate<>(pf);
        template.setProducerInterceptor(interceptor);  // Spring 빈으로 등록된 인터셉터
        return template;
    }
}

@Component
public class CommonHeaderInterceptor implements ProducerInterceptor<String, Object> {

    @Value("${spring.application.name}")
    private String serviceName;

    /**
     * 메시지가 브로커로 전송되기 직전에 호출된다.
     * ProducerRecord를 수정하거나 새로 만들어 반환할 수 있다.
     * 여기서 공통 헤더를 부착한다.
     */
    @Override
    public ProducerRecord<String, Object> onSend(ProducerRecord<String, Object> record) {
        Headers headers = record.headers();
        addIfAbsent(headers, "ce-source", serviceName);
        addIfAbsent(headers, "ce-id", UUID.randomUUID().toString());
        addIfAbsent(headers, "ce-time", Instant.now().toString());

        String traceId = MDC.get("traceId");
        if (traceId != null) {
            addIfAbsent(headers, "trace-id", traceId);
        }
        return record;
    }

    /** 이미 같은 키가 있으면 덮어쓰지 않는다. Producer가 명시 설정한 헤더가 우선. */
    private void addIfAbsent(Headers headers, String key, String value) {
        if (headers.lastHeader(key) == null) {
            headers.add(key, value.getBytes(StandardCharsets.UTF_8));
        }
    }

    /**
     * 브로커가 ack를 반환하거나 전송이 실패했을 때 호출된다.
     * 전송 결과 메트릭 수집 등에 사용할 수 있다.
     */
    @Override public void onAcknowledgement(RecordMetadata m, Exception e) {}

    /**
     * Producer가 close()될 때 호출된다.
     * 인터셉터가 보유한 리소스를 정리하는 용도.
     */
    @Override public void close() {}

    /**
     * interceptor.classes로 등록 시 Kafka가 호출하는 초기화 메서드.
     * Producer 설정값(Map)을 받는다.
     * setProducerInterceptor()로 등록하면 Spring DI가 대신하므로 비워둬도 된다.
     */
    @Override public void configure(Map<String, ?> configs) {}
}
```

#### 방법 3: interceptor.classes 프로퍼티 (Kafka 네이티브)

Kafka가 직접 인스턴스를 생성하므로 Spring DI를 사용할 수 없습니다. `configure(Map)` 메서드로 전달되는 Producer 설정값만 접근 가능합니다. Spring 빈이 필요 없는 단순한 헤더 부착에는 사용할 수 있지만, 실무에서는 방법 1이나 2를 선호합니다.

```yaml
spring:
  kafka:
    producer:
      properties:
        interceptor.classes: com.example.kafka.SimpleHeaderInterceptor
        app.service.name: order-service  # configure()에서 접근 가능
```

#### 세 방법 비교

| 기준 | 래퍼 빈 (방법 1) | setProducerInterceptor (방법 2) | interceptor.classes (방법 3) |
|------|:---:|:---:|:---:|
| Spring DI | O | O | X |
| 테스트 목킹 | 쉬움 | 보통 | 어려움 |
| 적용 범위 | 래퍼 사용 코드만 | 해당 KafkaTemplate 전체 | 해당 Producer 전체 |
| 누락 방지 | 래퍼만 사용하도록 강제 필요 | 자동 (투명) | 자동 (투명) |
| 헤더 커스터마이징 | 호출별 유연 | onSend 내에서만 | onSend 내에서만 |

**실무 권장**: 이벤트별로 `ce-type`을 다르게 지정해야 하는 경우 **방법 1(래퍼 빈)**이 가장 유연합니다. 모든 헤더를 동일하게 부착하는 단순한 경우에는 **방법 2**가 투명하게 동작하므로 누락 위험이 적습니다.

#### 다중 인터셉터 순서 제어

`interceptor.classes`는 YAML에 나열한 순서대로 실행됩니다. 그런데 `setProducerInterceptor()`는 **인터셉터 하나만** 받으므로 여러 인터셉터의 순서를 직접 제어해야 합니다. 방법은 두 가지입니다.

**방법 A — 단일 인터셉터 내부에서 순차 호출**

가장 간단합니다. 한 인터셉터의 `onSend()` 안에서 모든 로직을 순서대로 실행합니다. 헤더 부착과 메트릭 수집처럼 관심사가 명확히 다른 경우에도, 인터셉터 수가 2~3개 이하라면 이 방법이 코드 복잡도 대비 효율적입니다.

**방법 B — CompositeProducerInterceptor로 체이닝**

관심사를 별도 클래스로 분리하고 싶다면 Composite 패턴을 사용합니다. 리스트 순서가 곧 실행 순서입니다.

```java
@Configuration
public class KafkaProducerConfig {

    @Bean
    public KafkaTemplate<String, Object> kafkaTemplate(
            ProducerFactory<String, Object> pf,
            CommonHeaderInterceptor headerInterceptor,
            MetricsInterceptor metricsInterceptor) {

        // 리스트 순서 = onSend() 실행 순서
        CompositeProducerInterceptor<String, Object> composite =
            new CompositeProducerInterceptor<>(
                headerInterceptor,    // 1번: 헤더 부착
                metricsInterceptor    // 2번: 메트릭 수집
            );

        KafkaTemplate<String, Object> template = new KafkaTemplate<>(pf);
        template.setProducerInterceptor(composite);
        return template;
    }
}
```

`CompositeProducerInterceptor`는 Spring Kafka 3.x에서 제공하는 클래스로, 내부적으로 `List<ProducerInterceptor>`를 순회하며 `onSend()`를 체이닝합니다. 이전 인터셉터가 반환한 `ProducerRecord`가 다음 인터셉터의 입력이 됩니다.

**주의 — `setProducerInterceptor()`와 `interceptor.classes`를 함께 사용하면 안 됩니다.** 둘 다 설정하면 인터셉터가 이중 실행되어 헤더가 중복 추가됩니다. 하나만 선택해야 합니다.

### 헤더 설계 시 주의사항

**1. 헤더 값은 `byte[]`**: Kafka 헤더는 항상 `byte[]`이므로 직렬화/역직렬화를 직접 처리해야 합니다. 팀 전체에서 `UTF-8` 인코딩을 일관되게 사용하는 것이 기본 규약입니다.

**2. 동일 키 중복 가능**: Kafka 헤더는 `Map`이 아니라 `List`처럼 동작합니다. 같은 키를 여러 번 `add()`하면 값이 누적됩니다. 읽을 때는 `lastHeader(key)`로 마지막 값을 가져오거나, `headers(key)`로 전체를 순회해야 합니다. ProducerInterceptor 체인에서 여러 인터셉터가 같은 키를 추가하는 실수가 빈번하므로 `addIfAbsent` 패턴을 권장합니다.

**3. 크기 제한**: 헤더도 메시지 크기(`message.max.bytes`)에 포함됩니다. 헤더에는 짧은 문자열(타입명, UUID, ISO 타임스탬프)만 넣고, 구조화된 데이터나 바이너리는 페이로드에 담아야 합니다.

**4. Schema Registry 미적용**: 헤더는 Schema Registry가 관리하지 않습니다. 따라서 헤더 규약(키 이름, 값 형식, 필수/선택 여부)을 별도로 문서화해야 합니다. CloudEvents 표준을 채택하면 `ce-` 접두사가 붙은 필수 헤더(`specversion`, `type`, `source`, `id`)가 이미 정의되어 있어 규약 수립 비용을 줄일 수 있습니다.

---

## 3. Event Standardizer

### 패턴 개요

실무에서 이벤트를 발행하는 시스템은 단일하지 않습니다. 사내 레거시 시스템, 외부 결제 API, 파트너사 연동, SaaS 서비스 등 각각이 자신만의 이벤트 형식을 가지고 있습니다. 주문 이벤트 하나를 예로 들면, 자사 시스템은 `orderId`를, 레거시 시스템은 `order_no`를, 외부 API는 `transactionRef`를 사용합니다.

Event Standardizer는 이러한 다양한 형식의 이벤트를 **Canonical Data Model(정규 데이터 모델)**로 변환하는 패턴입니다. 정규 데이터 모델은 조직 내 공통 언어 역할을 합니다. 모든 소비자가 이 공통 형식만 알면 되므로, N개의 소스 × M개의 소비자 = N×M개의 변환기가 아니라, N개의 소스→정규화 + M개의 정규화→소비자로 N+M개의 변환기만 필요합니다.

Canonical Data Model이 없을 때와 있을 때의 복잡도 차이는 N과 M이 커질수록 극적으로 벌어집니다.

```
[Canonical Data Model 없이: N×M 변환기 필요]

레거시시스템 ---> 배송서비스 (변환기 1)
레거시시스템 ---> 통계서비스 (변환기 2)
레거시시스템 ---> 알림서비스 (변환기 3)
외부결제API  ---> 배송서비스 (변환기 4)
외부결제API  ---> 통계서비스 (변환기 5)
외부결제API  ---> 알림서비스 (변환기 6)
파트너사API  ---> 배송서비스 (변환기 7)
파트너사API  ---> 통계서비스 (변환기 8)
파트너사API  ---> 알림서비스 (변환기 9)
                              ↑ 3소스 × 3소비자 = 9개 변환기

[Canonical Data Model 사용: N+M 변환기만 필요]

레거시시스템 ---> [Standardizer] --+
외부결제API  ---> [Standardizer] --+--> [canonical.orders] ---> 배송서비스
파트너사API  ---> [Standardizer] --+                       ---> 통계서비스
                                                           ---> 알림서비스
                              ↑ 3개 표준화기 + 0개 소비자측 변환 = 3개
```

소스 3개, 소비자 3개인 지금은 9개 vs 3개의 차이지만, 소스 10개 소비자 20개가 되면 200개 vs 30개의 차이가 됩니다. 정규 데이터 모델은 시스템 확장에 비례하여 가치가 커집니다.

### 구현 전략: 진입점 표준화 vs 소비자별 변환

두 가지 전략이 있습니다.

**전략 1 - 진입점(Gateway)에서 표준화**: 이벤트가 시스템에 진입하는 순간 정규 형식으로 변환합니다. Kafka의 경우 소스 토픽을 별도로 두고, Standardizer가 소비하여 정규화 토픽으로 발행합니다.

**전략 2 - 소비자별 변환**: 소비자가 각자 원하는 형식으로 변환합니다. 이 방식은 단기적으로 쉽지만, 같은 변환 로직이 여러 소비자에 중복 구현되어 유지보수 비용이 증가합니다.

실무에서는 **전략 1**이 권장됩니다. 변환 로직이 한 곳에 집중되어 있어 소스 시스템의 형식이 바뀌어도 Standardizer 하나만 수정하면 됩니다.

한 가지 주의점은 Canonical Data Model이 지나치게 범용적으로 설계되면 오히려 모든 시스템의 특수한 요구사항을 수용하려다 거대하고 복잡한 공통 스키마가 만들어질 수 있습니다. 이를 "God Object" 안티패턴이라고 합니다. 정규 모델은 **도메인 내에서 공통으로 쓰이는 핵심 필드**만 포함하고, 특수 필드는 각 서비스의 확장 필드로 분리하는 것이 바람직합니다.

```java
// Kafka Streams: 다양한 소스 이벤트를 정규 형식으로 변환
KStream<String, LegacyOrderEvent> legacyStream = builder.stream("legacy.orders");

KStream<String, CanonicalOrderEvent> canonicalStream = legacyStream.mapValues(legacy -> {
    return CanonicalOrderEvent.newBuilder()
        .setOrderId(legacy.getOrderNo())          // order_no → orderId
        .setCustomerId(legacy.getCustId())         // cust_id → customerId
        .setTotalAmount(legacy.getAmt())           // amt → totalAmount
        .setCreatedAt(parseDate(legacy.getDate())) // 날짜 형식 통일
        .build();
});

canonicalStream.to("canonical.orders");
```

---

## 4. Event Router

### 패턴 개요

Event Router는 이벤트의 속성(타입, 소스, 우선순위, 대상 지역 등)을 기반으로 서로 다른 토픽이나 처리 경로로 분기하는 패턴입니다. 라우터는 이벤트 내용을 변경하지 않습니다. 단지 **어디로 보낼지**만 결정합니다.

왜 라우팅이 필요한가? 단일 이벤트 스트림에 모든 이벤트가 섞여 있으면 각 소비자가 자신과 무관한 이벤트를 필터링하는 비용을 부담해야 합니다. 라우터를 두면 소비자는 자신이 관심 있는 토픽만 구독하면 됩니다.

### Kafka Streams: branch()와 split()

```java
// Kafka Streams 3.x: split() + branch() 패턴
KStream<String, OrderEvent> orderStream = builder.stream("orders.all");

Map<String, KStream<String, OrderEvent>> branches = orderStream.split(Named.as("route-"))
    .branch(
        (key, event) -> event.getPriority() == Priority.HIGH,
        Branched.as("high-priority")
    )
    .branch(
        (key, event) -> "KR".equals(event.getRegion()),
        Branched.as("korea")
    )
    .branch(
        (key, event) -> "US".equals(event.getRegion()),
        Branched.as("us")
    )
    .defaultBranch(Branched.as("default"));

branches.get("route-high-priority").to("orders.high-priority");
branches.get("route-korea").to("orders.kr");
branches.get("route-us").to("orders.us");
branches.get("route-default").to("orders.standard");
```

**주의**: Kafka Streams 2.x의 `branch()` 메서드는 배열을 반환하며 3.x에서 deprecated되었습니다. 3.x에서는 `split()`을 사용하고, 하나의 이벤트가 여러 조건을 만족해도 **첫 번째 매칭 브랜치에만** 라우팅됩니다.

### TopicNameExtractor: 동적 라우팅

브랜치 수가 많거나 라우팅 규칙이 런타임에 변경될 수 있는 경우, `TopicNameExtractor`를 사용하여 동적으로 대상 토픽을 결정할 수 있습니다.

```java
// 이벤트 속성을 보고 런타임에 토픽 이름을 결정
TopicNameExtractor<String, OrderEvent> routingExtractor =
    (key, value, recordContext) -> {
        String region = value.getRegion();
        String tier = value.getCustomerTier();
        // 예: "orders.kr.premium", "orders.us.standard"
        return "orders." + region.toLowerCase() + "." + tier.toLowerCase();
    };

orderStream.to(routingExtractor);
```

동적 라우팅의 장점은 코드 변경 없이 라우팅 규칙을 외부 설정(데이터베이스, Config Server)에서 관리할 수 있다는 점입니다. 단, 대상 토픽이 존재하지 않으면 예외가 발생하므로 사전에 토픽 생성 여부를 검증하는 로직이 필요합니다.

이 패턴은 `13-topic-pipeline-architecture.md`의 **FilterBranch 패턴**과 동일한 문제를 다룹니다. 두 문서를 함께 참조하면 라우팅 패턴의 전체 그림을 볼 수 있습니다.

### 실무 시나리오: 이벤트 타입 기반 라우팅

단일 토픽에 여러 이벤트 타입이 혼재하는 상황은 흔합니다. 예를 들어 `user-events` 토픽에 `UserRegistered`, `UserUpdated`, `UserDeleted` 이벤트가 모두 들어오는 경우, 서비스마다 관심 있는 타입만 소비하고 싶습니다.

Event Envelope의 `ce-type` 헤더를 Router와 결합하면 역직렬화 없이 타입별로 분리할 수 있습니다. 단, Kafka Streams DSL의 `branch()` 조건 함수는 `(key, value)`만 받으므로 헤더에 직접 접근할 수 없습니다. 이를 해결하는 실전 패턴은 **2단계 접근**입니다: 먼저 Processor API로 헤더를 값에 포함시킨 뒤, DSL의 `split().branch()`로 분기합니다.

```java
// 헤더 정보를 값에 포함시키기 위한 래퍼
record TypedPayload(String eventType, byte[] payload) {}

// 1단계: Processor API로 헤더에서 이벤트 타입을 추출하여 값에 포함
KStream<String, byte[]> rawStream = builder.stream(
    "user-events",
    Consumed.with(Serdes.String(), Serdes.ByteArray())
);

KStream<String, TypedPayload> typed = rawStream.processValues(
    () -> new FixedKeyProcessor<String, byte[], TypedPayload>() {
        private FixedKeyProcessorContext<String, TypedPayload> context;

        @Override
        public void init(FixedKeyProcessorContext<String, TypedPayload> ctx) {
            this.context = ctx;
        }

        @Override
        public void process(FixedKeyRecord<String, byte[]> record) {
            Header h = record.headers().lastHeader("ce-type");
            String type = (h != null)
                ? new String(h.value(), StandardCharsets.UTF_8)
                : "unknown";
            context.forward(record.withValue(new TypedPayload(type, record.value())));
        }
    }
);

// 2단계: 추출된 타입으로 분기
Map<String, KStream<String, TypedPayload>> branches = typed
    .split(Named.as("type-"))
    .branch(
        (key, v) -> "com.example.user.registered".equals(v.eventType()),
        Branched.as("registered")
    )
    .branch(
        (key, v) -> "com.example.user.updated".equals(v.eventType()),
        Branched.as("updated")
    )
    .defaultBranch(Branched.as("other"));

// 3단계: 각 브랜치에서 원본 바이트를 역직렬화
branches.get("type-registered")
    .mapValues(v -> deserializeAs(v.payload(), UserRegisteredEvent.class))
    .to("user.registered");

branches.get("type-updated")
    .mapValues(v -> deserializeAs(v.payload(), UserUpdatedEvent.class))
    .to("user.updated");
```

이 패턴의 핵심은 **헤더 → 값 승격(promotion)**입니다. 인프라 계층(Processor API)에서 헤더 정보를 값으로 옮기면, 이후 비즈니스 계층(DSL)에서는 순수한 값 기반 로직만으로 라우팅할 수 있습니다. 이벤트 타입이 수십 가지로 늘어나도 `branch()` 조건만 추가하면 됩니다.

---

## 5. Event Splitter

### 패턴 개요

Event Splitter는 하나의 복합 이벤트(Composite Event)를 여러 개의 단일 이벤트로 분리하는 패턴입니다. 왜 복합 이벤트가 발생하는가? 두 가지 이유가 있습니다.

첫째, **배치 이벤트(Batch Event)**: 성능 최적화나 레거시 시스템 제약으로 인해 여러 이벤트가 하나의 메시지에 묶여 있는 경우입니다. 예를 들어 배치 시스템이 하루치 주문 1,000건을 하나의 이벤트로 발행하는 경우입니다.

둘째, **1:N 관계 이벤트**: 주문(Order)과 주문 상품(OrderItem)처럼 부모-자식 관계가 하나의 이벤트에 포함된 경우입니다. 주문 이벤트에 여러 아이템이 포함되어 있을 때, 아이템별로 처리가 필요한 소비자(예: 창고 시스템)는 이를 분리해야 합니다.

### Kafka Streams: flatMap()

```java
KStream<String, OrderCreatedEvent> orderStream = builder.stream("orders.created");

// 주문 이벤트를 아이템별 이벤트로 분리
KStream<String, OrderItemEvent> itemStream = orderStream.flatMap(
    (orderId, orderEvent) -> {
        List<KeyValue<String, OrderItemEvent>> items = new ArrayList<>();

        for (OrderItem item : orderEvent.getItems()) {
            OrderItemEvent itemEvent = OrderItemEvent.newBuilder()
                .setOrderId(orderEvent.getOrderId())
                .setItemId(item.getItemId())
                .setProductId(item.getProductId())
                .setQuantity(item.getQuantity())
                .setWarehouseId(item.getWarehouseId())
                .build();

            // 파티션 키를 warehouseId로 설정: 같은 창고의 이벤트는 같은 파티션으로
            items.add(KeyValue.pair(item.getWarehouseId(), itemEvent));
        }

        return items;
    }
);

itemStream.to("order-items.to-fulfill");
```

`flatMap()`은 키와 값을 모두 변경할 수 있어 **재파티셔닝이 발생**합니다. 위 예시에서 파티션 키를 `orderId`에서 `warehouseId`로 변경했기 때문입니다. 키를 변경할 필요가 없다면(분리된 아이템들이 원래 주문과 같은 파티션에 있어도 된다면) `flatMapValues()`를 사용하면 재파티셔닝 없이 처리할 수 있습니다.

**순서 보장 전략**: 분리된 이벤트들의 처리 순서가 중요하다면, 파티션 키를 어떻게 설정하느냐가 핵심입니다. 위 예시에서 `warehouseId`를 키로 사용하면 같은 창고로 가는 아이템들이 동일 파티션에 순서대로 들어갑니다. `orderId`를 키로 사용하면 같은 주문의 아이템들이 같은 파티션에 들어갑니다.

### 역패턴: Event Aggregator

Splitter의 반대 패턴은 **Event Aggregator(집계)**입니다. 여러 개의 단일 이벤트를 하나의 복합 이벤트로 합칩니다. Kafka Streams에서는 `groupBy()` + `aggregate()` 또는 `windowedBy()` + `reduce()`로 구현합니다. 예를 들어 분산된 아이템별 배송 완료 이벤트를 집계하여 "주문 전체 배송 완료" 이벤트를 생성하는 경우입니다.

```
[Splitter]                          [Aggregator]
주문이벤트(3개 아이템)              아이템배송완료 × 3개
    |                                    |
    +--> 아이템이벤트 #1                  +--> 주문배송완료이벤트
    +--> 아이템이벤트 #2         -->
    +--> 아이템이벤트 #3
```

Aggregator의 핵심 문제는 **완료 조건**입니다. 3개 아이템을 모두 받았을 때 집계를 완료하려면, 전체 아이템 수를 어디선가 알고 있어야 합니다. 일반적으로 두 가지 접근이 있습니다.

**접근 1 - 카운트 기반**: 주문 이벤트(부모)가 `totalItems: 3`을 포함하고, Aggregator State Store에 해당 수까지 누적되면 완료로 판단합니다.

**접근 2 - 타임아웃 기반**: 일정 시간(예: 24시간) 이내에 도착한 이벤트를 모두 집계합니다. 일부 이벤트가 유실되어도 타임아웃 후 강제로 완료 처리합니다. 완전한 집계보다 시간 내 처리가 중요한 경우에 적합합니다.

```java
// Aggregator: orderId별로 아이템 배송 완료 이벤트를 집계
KStream<String, ItemDeliveredEvent> itemStream = builder.stream("item-delivery.completed");

// orderId를 키로 그룹화
KGroupedStream<String, ItemDeliveredEvent> grouped =
    itemStream.groupBy((itemId, event) -> event.getOrderId());

// State Store에 누적
KTable<String, OrderDeliveryAggregator> aggregated = grouped.aggregate(
    OrderDeliveryAggregator::new,
    (orderId, itemEvent, agg) -> {
        agg.addDeliveredItem(itemEvent.getItemId());
        return agg;
    },
    Materialized.as("order-delivery-store")
);

// 완료된 주문만 다운스트림으로 전송
aggregated.toStream()
    .filter((orderId, agg) -> agg.isAllItemsDelivered())
    .mapValues(agg -> agg.toOrderFullyDeliveredEvent())
    .to("orders.fully-delivered");
```

Splitter와 Aggregator를 함께 사용할 때는 **파티션 키 일관성**이 중요합니다. Splitter가 `orderId`를 키로 아이템 이벤트를 발행했다면, Aggregator도 `orderId`로 그룹화해야 같은 Kafka Streams 태스크에서 같은 State Store를 사용하여 집계할 수 있습니다.

---

## 6. Event Translator

### 패턴 개요

Event Translator는 이벤트의 스키마나 형식을 변환하는 패턴입니다. Event Standardizer와 유사해 보이지만 목적이 다릅니다. Standardizer는 **다양한 소스**를 하나의 표준으로 통일하는 것이 목적이고, Translator는 **동일한 의미를 가진 이벤트의 표현 방식**을 변환하는 것이 목적입니다.

실무에서 Translator가 필요한 대표적인 상황은 스키마 마이그레이션입니다. v1 스키마를 사용하는 기존 컨슈머가 있는 상태에서 v2 스키마로 전환해야 할 때, 모든 컨슈머를 동시에 업그레이드할 수 없습니다. 이 경우 Translator가 v2 이벤트를 소비하여 v1 형식으로 변환한 뒤 v1 토픽에 발행하면, 기존 컨슈머들은 변경 없이 계속 동작할 수 있습니다.

```
producers (v2) --> [orders.v2 topic] --> [Translator] --> [orders.v1 topic] --> legacy consumers
                                                     \--> [orders.v2 topic] --> new consumers
```

### Schema Registry와의 연계

`10-message-schema-design.md`에서 다룬 Schema Registry의 호환성 모드와 Translator는 상호보완적입니다. Schema Registry의 `BACKWARD` 호환성은 새 스키마가 이전 스키마로 작성된 이벤트를 읽을 수 있게 보장합니다. 그러나 이것만으로는 **이전 버전 컨슈머**가 새 스키마 이벤트를 읽는 상황을 커버하지 못합니다. Translator는 이 간극을 메웁니다.

```java
// Kafka Streams: v2 스키마 이벤트를 v1 형식으로 변환
KStream<String, OrderEventV2> v2Stream = builder.stream(
    "orders.v2",
    Consumed.with(Serdes.String(), orderV2Serde)
);

KStream<String, OrderEventV1> v1Stream = v2Stream.mapValues(v2 -> {
    return OrderEventV1.newBuilder()
        .setOrderId(v2.getOrderId())
        .setUserId(v2.getCustomerId())          // customerId → userId (이름 변경)
        .setAmount(v2.getTotalAmount().longValue()) // BigDecimal → long (타입 변경)
        .setStatus(v2.getStatus().name())        // Enum → String (타입 변경)
        // v2에 추가된 필드들은 v1에 없으므로 무시
        .build();
});

v1Stream.to("orders.v1", Produced.with(Serdes.String(), orderV1Serde));
```

### Schema Registry 호환성과의 역할 분담

Translator를 도입하기 전에 먼저 Schema Registry의 호환성 모드로 해결할 수 있는지 확인해야 합니다.

- **BACKWARD 호환**(기본): 새 스키마의 컨슈머가 이전 스키마 데이터를 읽을 수 있습니다. 컨슈머를 먼저 업그레이드하는 시나리오에서는 Translator 없이도 마이그레이션이 가능합니다.
- **FORWARD 호환**: 이전 스키마의 컨슈머가 새 스키마 데이터를 읽을 수 있습니다. 프로듀서를 먼저 업그레이드하는 시나리오에서 Translator를 대체할 수 있습니다.
- **FULL 호환**: 양방향 모두 가능합니다. 대부분의 단순 스키마 변경에서 Translator가 불필요합니다.

**Translator가 반드시 필요한 경우**: 필드 이름 변경(`userId` → `customerId`), 타입 변경(`long` → `BigDecimal`), 구조 변경(flat → nested)처럼 Schema Registry의 호환성 규칙으로 커버되지 않는 **breaking change**가 포함된 마이그레이션에서만 Translator를 사용합니다. 호환 가능한 변경(필드 추가/제거 + default 값)이라면 Schema Registry만으로 충분합니다.

---

## 7. Content Filter

### 패턴 개요

Content Filter는 이벤트에서 불필요한 필드를 제거하고 필요한 데이터만 다운스트림으로 전달하는 패턴입니다. 세 가지 이유로 필요합니다.

**보안(Security)**: 개인정보(PII, Personally Identifiable Information)가 포함된 이벤트를 개인정보 처리가 불필요한 서비스(예: 통계 집계 서비스)로 그대로 전달해서는 안 됩니다. GDPR, 개인정보보호법 준수를 위해 불필요한 PII는 필터링해야 합니다.

**대역폭(Bandwidth)**: 이벤트에 분석에 불필요한 대용량 필드(예: HTML 본문, 바이너리 데이터)가 포함된 경우, 이를 제거하면 네트워크 트래픽과 저장 비용을 줄일 수 있습니다.

**관심사 분리(Separation of Concerns)**: 결제 서비스는 주문 이벤트에서 결제 관련 필드만, 배송 서비스는 배송지 필드만 필요합니다. 관심 없는 필드까지 처리하면 코드 복잡도가 증가합니다.

```
[주문 이벤트]                      [필터 후]
{                                  {
  orderId: "ORD-001",                orderId: "ORD-001",
  customerId: "CUST-123",            customerId: "CUST-123",  ← 집계에 필요
  name: "홍길동",       --> 제거      totalAmount: 49900       ← 집계에 필요
  email: "hong@ex.com" --> 제거    }
  phone: "010-...",    --> 제거    (이름, 이메일, 전화번호 제거)
  totalAmount: 49900,
  deliveryAddress: "..." --> 제거
}
```

### Kafka Streams 구현

```java
KStream<String, OrderCreatedEvent> orderStream = builder.stream("orders.created");

// 통계 집계용: PII 제거, 필요한 필드만 남김
KStream<String, OrderAnalyticsEvent> analyticsStream = orderStream.mapValues(order -> {
    return OrderAnalyticsEvent.newBuilder()
        .setOrderId(order.getOrderId())
        .setCustomerSegment(order.getCustomerTier()) // ID 대신 세그먼트만
        .setTotalAmount(order.getTotalAmount())
        .setItemCount(order.getItems().size())
        .setRegion(order.getRegion())
        .setCreatedAt(order.getCreatedAt())
        // name, email, phone, deliveryAddress 필드 의도적으로 제외
        .build();
});

analyticsStream.to("orders.analytics");
```

### GDPR과의 관계: Crypto-Shredding 패턴

GDPR(일반 개인정보보호규정)은 개인정보를 **목적에 필요한 최소한으로만** 처리하도록 요구합니다(데이터 최소화 원칙). Content Filter를 통해 개인정보가 불필요한 토픽에는 PII가 포함되지 않도록 아키텍처 수준에서 보장할 수 있습니다.

그러나 Content Filter만으로는 해결하기 어려운 시나리오가 있습니다. Kafka 이벤트는 보존 기간 동안 변경할 수 없습니다. 사용자가 "잊혀질 권리(Right to Erasure)"를 행사하면 해당 사용자의 개인정보를 Kafka 토픽에서 삭제해야 하는데, 이미 발행된 이벤트는 수정할 수 없습니다.

이 문제를 해결하는 기법이 **Crypto-Shredding(암호화 파쇄)**입니다. PII를 이벤트에 직접 저장하는 대신, 사용자별 암호화 키로 PII를 암호화하여 저장합니다. 사용자가 삭제를 요청하면 암호화 키만 삭제합니다. 키가 없으면 암호화된 PII는 해독 불가능한 쓰레기 데이터가 되어, 사실상 삭제된 것과 같은 효과를 냅니다.

```
[일반 방식: PII 직접 저장]                [Crypto-Shredding]
이벤트: {                                이벤트: {
  userId: "U-123",                         userId: "U-123",
  name: "홍길동",        ← 삭제 불가        name: "a3Fx9mP2...",  ← 암호화된 값
  email: "hong@ex.com"  ← 삭제 불가        email: "k8Yn3qR1..." ← 암호화된 값
}                                        }
                                         암호화 키 저장소: { "U-123": "key-abc" }
                                         삭제 요청 시: 키 저장소에서 "key-abc" 삭제
                                         → 암호화된 값은 복호화 불가
```

```java
// Crypto-Shredding을 적용한 Content Filter
@Component
public class PiiEncryptingFilter {

    private final KeyManagementService kms; // AWS KMS, Vault 등

    public OrderAnalyticsEvent filter(OrderCreatedEvent order) {
        // 사용자별 암호화 키 가져오기 (없으면 새로 생성)
        SecretKey userKey = kms.getOrCreateKey("user:" + order.getCustomerId());

        return OrderAnalyticsEvent.newBuilder()
            .setOrderId(order.getOrderId())
            // PII 필드는 암호화하여 저장
            .setEncryptedCustomerName(encrypt(order.getCustomerName(), userKey))
            .setEncryptedEmail(encrypt(order.getEmail(), userKey))
            // 비-PII 필드는 그대로 포함
            .setTotalAmount(order.getTotalAmount())
            .setRegion(order.getRegion())
            .setCreatedAt(order.getCreatedAt())
            .build();
    }

    // 삭제 요청 처리: 키만 삭제하면 암호화된 데이터는 사실상 삭제됨
    public void handleErasureRequest(String customerId) {
        kms.deleteKey("user:" + customerId);
        log.info("Crypto-shredded PII for customer: {}", customerId);
    }
}
```

Crypto-Shredding은 Content Filter와 함께 사용하여 이중 보호를 구성할 수 있습니다. 불필요한 PII는 Content Filter로 완전히 제거하고, 일부 필요한 PII는 Crypto-Shredding으로 암호화하여 보존하는 전략입니다.

---

## 8. Claim Check

### 패턴 개요

Claim Check 패턴은 수하물 보관소(Baggage Claim)에서 이름을 따왔습니다. 공항에서 큰 짐을 맡기면 보관 번호가 적힌 영수증(Claim Check)을 받고, 나중에 그 번호로 짐을 찾습니다. 이벤트 스트리밍에서도 동일한 개념입니다. 대용량 페이로드(이미지, 비디오, 대형 JSON, PDF)를 이벤트 메시지에 직접 포함하는 대신, 외부 저장소(S3, GCS, Azure Blob)에 저장하고 **참조 URI(Claim Check)**만 이벤트에 담아 전송합니다.

### 왜 필요한가?

Kafka의 기본 메시지 크기 제한은 **1MB**입니다(`message.max.bytes` 설정). 물론 이 값을 늘릴 수 있지만, 그렇게 해서는 안 되는 이유가 있습니다. 첫째, 메시지가 크면 브로커의 페이지 캐시 효율이 떨어집니다. 큰 메시지 몇 개가 캐시를 차지하면 작은 메시지 수천 개가 캐시 미스를 경험합니다. 둘째, 컨슈머 처리 지연이 발생합니다. 100MB 이미지가 담긴 이벤트를 처리하는 동안 다른 이벤트들이 대기해야 합니다. 셋째, 네트워크 대역폭 낭비입니다. 대용량 페이로드는 모든 컨슈머 그룹이 각각 다운로드하지만, 실제로 페이로드를 필요로 하는 컨슈머는 소수일 수 있습니다.

### 아키텍처

```
Producer                  S3/GCS              Kafka Topic            Consumer
   |                         |                     |                     |
   |-- 1. 페이로드 업로드 -->  |                     |                     |
   |<-- 2. URI 반환 ------   |                     |                     |
   |                         |                     |                     |
   |-- 3. URI만 포함된 이벤트 발행 ------------->   |                     |
   |                         |                     |-- 4. 이벤트 소비 --> |
   |                         |                     |                     |
   |                         |<--- 5. URI로 페이로드 다운로드 ------------|
   |                         |--- 6. 페이로드 반환 ---------------------->|
```

### 구현 예시: S3 + Kafka 조합

```java
// Producer: S3에 업로드 후 URI만 이벤트에 포함
@Service
public class OrderDocumentProducer {

    private final S3Client s3Client;
    private final KafkaTemplate<String, OrderDocumentEvent> kafkaTemplate;
    private static final long INLINE_THRESHOLD_BYTES = 10_000; // 10KB 이하는 인라인

    public void publishOrderDocument(String orderId, byte[] pdfBytes) {
        String payloadRef;

        if (pdfBytes.length <= INLINE_THRESHOLD_BYTES) {
            // 작은 페이로드: 인라인으로 포함
            payloadRef = "data:application/pdf;base64," +
                Base64.getEncoder().encodeToString(pdfBytes);
        } else {
            // 큰 페이로드: S3에 업로드하고 URI만 포함 (Claim Check)
            String s3Key = "orders/" + orderId + "/document.pdf";
            s3Client.putObject(
                PutObjectRequest.builder()
                    .bucket("order-documents")
                    .key(s3Key)
                    .contentType("application/pdf")
                    .build(),
                RequestBody.fromBytes(pdfBytes)
            );
            payloadRef = "s3://order-documents/" + s3Key;
        }

        OrderDocumentEvent event = OrderDocumentEvent.newBuilder()
            .setOrderId(orderId)
            .setPayloadRef(payloadRef)        // URI 또는 인라인 데이터
            .setPayloadSize(pdfBytes.length)
            .setCreatedAt(Instant.now())
            .build();

        kafkaTemplate.send("orders.documents", orderId, event);
    }
}
```

```java
// Consumer: URI를 확인하고 S3에서 실제 페이로드 가져오기
@KafkaListener(topics = "orders.documents")
public void processDocument(OrderDocumentEvent event) {
    byte[] pdfBytes;
    String payloadRef = event.getPayloadRef();

    if (payloadRef.startsWith("s3://")) {
        // Claim Check: S3에서 페이로드 다운로드
        String[] parts = payloadRef.substring(5).split("/", 2);
        String bucket = parts[0];
        String key = parts[1];

        ResponseBytes<GetObjectResponse> response = s3Client.getObjectAsBytes(
            GetObjectRequest.builder().bucket(bucket).key(key).build()
        );
        pdfBytes = response.asByteArray();
    } else {
        // 인라인 데이터 디코딩
        String base64Data = payloadRef.split(",")[1];
        pdfBytes = Base64.getDecoder().decode(base64Data);
    }

    processOrderDocument(event.getOrderId(), pdfBytes);
}
```

### Claim Check vs 인라인 페이로드 판단 기준

| 기준 | 인라인 | Claim Check |
|------|--------|------------|
| 페이로드 크기 | < 10KB | > 10KB |
| 소비자 수 | 다수 (모두 필요) | 소수 (일부만 필요) |
| 페이로드 수명 | 이벤트 보존 기간과 동일 | 별도 라이프사이클 관리 필요 |
| 네트워크 비용 | 낮음 | S3 API 호출 비용 추가 |
| 복잡도 | 낮음 | 높음 (외부 저장소 관리) |

---

## 9. Event Chunking

### 패턴 개요

Event Chunking은 Claim Check과 같은 문제(대용량 페이로드)를 다른 방식으로 해결합니다. Claim Check은 페이로드를 외부 저장소로 **오프로드**하지만, Event Chunking은 페이로드를 **분할(Chunk)**하여 여러 이벤트로 쪼개어 전송합니다. 소비자는 청크들을 받아 **재조립(Reassembly)**합니다.

```
[Producer]          [Kafka]                        [Consumer]
    |                  |                                |
    |-- chunk #1/3 --> |                                |
    |-- chunk #2/3 --> |  ---- chunk #1/3 -->          |
    |-- chunk #3/3 --> |  ---- chunk #2/3 -->   [State Store에 누적]
                       |  ---- chunk #3/3 -->   [3/3 도착: 재조립 완료]
```

### 청크 헤더 설계

청크 이벤트에는 재조립에 필요한 메타데이터가 포함되어야 합니다.

```java
// 청크 이벤트 스키마
{
  "correlationId": "upload-2024-001",  // 전체 이벤트의 고유 ID
  "chunkIndex": 0,                     // 현재 청크의 순서 (0-based)
  "totalChunks": 3,                    // 전체 청크 수
  "chunkData": "...",                  // 이 청크의 실제 데이터
  "checksum": "sha256:abc123"          // 데이터 무결성 검증
}
```

### Kafka Streams: State Store를 이용한 재조립

```java
// Kafka Streams: 청크 수집 후 재조립
KStream<String, ChunkEvent> chunkStream = builder.stream("events.chunks");

// correlationId를 키로 사용하여 같은 파티션에 모으기
KGroupedStream<String, ChunkEvent> grouped = chunkStream
    .groupBy((key, chunk) -> chunk.getCorrelationId());

// Aggregator로 청크 수집
KTable<String, ChunkAggregator> aggregated = grouped.aggregate(
    ChunkAggregator::new,
    (correlationId, chunk, aggregator) -> {
        aggregator.addChunk(chunk.getChunkIndex(), chunk.getChunkData());

        if (aggregator.isComplete(chunk.getTotalChunks())) {
            // 모든 청크 수집 완료: 재조립
            aggregator.reassemble();
        }
        return aggregator;
    },
    Materialized.<String, ChunkAggregator, KeyValueStore<Bytes, byte[]>>as("chunk-store")
        .withValueSerde(chunkAggregatorSerde)
);

// 재조립 완료된 이벤트만 다운스트림으로 전송
KStream<String, CompleteEvent> completeStream = aggregated.toStream()
    .filter((correlationId, agg) -> agg.isComplete())
    .mapValues(agg -> agg.toCompleteEvent());

completeStream.to("events.complete");
```

**중요한 설계 포인트**: 모든 청크가 같은 `correlationId`를 파티션 키로 사용해야 동일한 Kafka 파티션에 할당되고, 동일한 Kafka Streams 태스크에서 처리됩니다. 다른 파티션에 청크가 분산되면 재조립이 불가능합니다.

### Claim Check vs Event Chunking 선택 기준

| 기준 | Claim Check | Event Chunking |
|------|------------|----------------|
| 외부 저장소 의존성 | 필요 (S3 등) | 불필요 |
| 소비자 측 복잡도 | S3 API 호출 | 재조립 로직 구현 |
| 대용량 처리 | 크기 제한 없음 | Kafka 파티션 처리 용량 내 |
| 전송 원자성 | 단일 이벤트 | 청크 순서 보장 필요 |
| 추천 상황 | 이미지/비디오처럼 독립적인 바이너리 | 구조화된 데이터를 분할 전송할 때 |

실무에서는 **Claim Check이 더 일반적**으로 사용됩니다. S3 같은 오브젝트 스토리지는 이미 대부분의 인프라에 갖추어져 있고, 소비자 측에서 재조립 State Store를 관리하는 복잡도를 피할 수 있기 때문입니다. Chunking은 외부 저장소를 추가하기 어려운 제약 환경이나, 이미 분할이 자연스러운 스트리밍 데이터(비디오 세그먼트 등)에 적합합니다.

---

## 10. 패턴 조합 예시

### 실무 시나리오: 주문 이벤트 처리 파이프라인

전자상거래 플랫폼에서 주문 이벤트가 발생하면 여러 시스템이 협력해야 합니다. 이 시나리오에서 여러 EIP 패턴이 어떻게 조합되는지 살펴보겠습니다.

```
[외부 주문 시스템]                      [자체 시스템]
POS, 앱, 웹, 파트너사 API
       |
       v
[Event Standardizer]  ← 다양한 형식 → 정규 형식으로 통일
       |
       v
[orders.canonical 토픽]
       |
       +--[Content Filter]--> [orders.analytics 토픽]  → 통계 서비스 (PII 제거)
       |
       +--[Event Router]----> [orders.high-priority]   → VIP 주문 처리 서비스
       |                 +--> [orders.standard]         → 일반 주문 처리 서비스
       |
       +--[Event Splitter]--> [order-items.fulfill]    → 창고 시스템 (아이템별 분리)
       |
       +--[Claim Check]-----> [orders.with-docs]        → 계약서 첨부 주문 (S3 참조)
```

### Envelope + Claim Check 조합

대용량 첨부 파일이 있는 이벤트를 처리할 때, Envelope 패턴으로 헤더에 파일 크기 정보를 포함시키면 라우터가 페이로드를 열지 않고도 Claim Check가 필요한 이벤트를 식별할 수 있습니다.

```java
// Producer: Envelope 헤더에 페이로드 크기 정보 포함
ProducerRecord<String, OrderEvent> record = new ProducerRecord<>("orders.all", orderId, event);

// 헤더에 첨부 파일 크기 기록 (라우터가 역직렬화 없이 판단 가능)
record.headers()
    .add("ce-type", "com.example.order.created".getBytes())
    .add("attachment-size", String.valueOf(attachmentSize).getBytes())
    .add("has-attachment", "true".getBytes());

producer.send(record);
```

```java
// Router: 헤더만 보고 Claim Check 처리 경로로 분기
@KafkaListener(topics = "orders.all")
public void routeOrder(ConsumerRecord<String, byte[]> record) {
    Header attachmentHeader = record.headers().lastHeader("has-attachment");
    boolean hasAttachment = attachmentHeader != null &&
        "true".equals(new String(attachmentHeader.value()));

    if (hasAttachment) {
        // 역직렬화 후 Claim Check 처리 경로로 발행
        OrderEvent event = deserialize(record.value());
        claimCheckProducer.publishWithClaimCheck("orders.with-docs", event);
    } else {
        // 일반 처리 경로
        OrderEvent event = deserialize(record.value());
        standardTemplate.send("orders.standard", record.key(), event);
    }
}
```

### Router + Translator + Filter 파이프라인

레거시 ERP 시스템이 v1 XML 이벤트를 발행하고, 현대 서비스들은 v2 Avro 이벤트를 기대하는 상황에서 세 패턴을 조합합니다.

```
[레거시 ERP] --> XML 이벤트
                    |
            [Event Translator]  XML → Avro v2 변환
                    |
            [Event Router]  서비스 타입에 따라 분기
                    |
        +-----------+------------+
        |                        |
[Content Filter]          [Claim Check]
PII 제거 후 → 분석 서비스    첨부문서 → 계약 서비스
```

이 파이프라인에서 각 패턴은 **단일 책임(Single Responsibility)**을 가집니다. Translator는 형식 변환만, Router는 분기 결정만, Filter는 필드 제거만 담당합니다. 이렇게 책임을 분리하면 각 단계를 독립적으로 테스트하고, 교체하거나, 스케일아웃할 수 있습니다.

---

## 11. 패턴 선택 가이드

실무에서 어떤 패턴을 언제 적용할지 결정하는 것은 쉽지 않습니다. 아래는 문제 상황별로 적절한 패턴을 빠르게 찾을 수 있는 가이드입니다.

### 문제 상황별 패턴 매핑

| 문제 상황 | 적용 패턴 | 이유 |
|----------|-----------|------|
| 이벤트 타입에 따라 다른 서비스로 보내야 한다 | Event Router | 라우팅 조건이 이벤트 내용 기반 |
| 레거시 XML을 현대 서비스가 읽어야 한다 | Event Translator | 형식 변환, 의미는 동일 |
| 다양한 소스의 이벤트를 통일해야 한다 | Event Standardizer | 다수 소스 → 정규 모델 |
| 이벤트에서 개인정보를 제거해야 한다 | Content Filter | PII 필드 제거, GDPR 준수 |
| 주문 1개에서 아이템 N개를 처리해야 한다 | Event Splitter | 1:N 관계 분리 |
| 이벤트에 1MB 초과 파일이 첨부된다 | Claim Check | 대용량 외부화, Kafka 크기 제한 우회 |
| 이벤트를 분할 전송 후 소비자가 재조립해야 한다 | Event Chunking | 외부 저장소 없이 분할 처리 |
| 중간 노드가 페이로드 파싱 없이 라우팅해야 한다 | Event Envelope | 헤더에 라우팅 메타데이터 포함 |

### 패턴 조합 시 권장 순서

여러 패턴을 조합할 때는 처리 순서가 중요합니다. 일반적으로 권장하는 파이프라인 순서는 다음과 같습니다.

```
입력 이벤트
    |
    v
[1] Event Translator / Standardizer   -- 형식을 먼저 통일 (이후 단계가 단일 형식을 전제)
    |
    v
[2] Content Filter                    -- 불필요한 필드 제거 (이후 처리 대상 데이터 축소)
    |
    v
[3] Event Router                      -- 내용 기반 분기 (정제된 데이터로 라우팅 결정)
    |
    v
[4] Event Splitter                    -- 복합 이벤트 분리 (라우팅 후 개별 처리)
    |
    v
[5] Claim Check / Event Chunking      -- 대용량 처리 (마지막에 적용, 소비자 근처에서)
```

**왜 이 순서인가?** Translator를 먼저 적용하면 이후 모든 패턴이 단일 스키마를 전제로 동작할 수 있습니다. Content Filter를 Translator 바로 다음에 두면, 이후 Router와 Splitter가 처리해야 하는 데이터 크기를 줄입니다. Router를 필터링 후에 적용하면 분기 조건 검사 시 이미 정제된 이벤트를 다룰 수 있습니다.

### 패턴 도입 시 흔한 실수

**실수 1 - 너무 많은 패턴을 한꺼번에 도입**: 처음부터 8개 패턴을 모두 적용하면 파이프라인이 복잡해져 디버깅이 어렵습니다. 가장 명확한 문제(예: 대용량 페이로드)부터 하나씩 적용하고, 측정 후 다음 패턴을 추가하는 점진적 접근을 권장합니다.

**실수 2 - Splitter 후 파티션 키 변경 누락**: Splitter로 이벤트를 분리할 때 파티션 키를 원래 이벤트의 키(orderId)와 다르게 설정하면, 동일 주문의 아이템들이 서로 다른 파티션으로 흩어져 처리 순서가 보장되지 않습니다.

**실수 3 - Claim Check URI 만료**: S3 Presigned URL처럼 만료 시간이 있는 URI를 Claim Check으로 사용하면, Kafka의 이벤트 보존 기간(예: 7일)보다 URI 만료 시간(예: 1시간)이 짧을 경우 재처리 시 URI를 따라가도 오브젝트를 가져올 수 없습니다. 영구 URI 또는 충분히 긴 만료 시간을 설정해야 합니다.

**실수 4 - Event Standardizer를 Translator와 혼동**: Standardizer는 여러 소스를 하나로 통일하는 패턴이고, Translator는 같은 데이터를 다른 형식으로 변환하는 패턴입니다. 레거시 시스템 연동에는 Standardizer, 스키마 버전 마이그레이션에는 Translator가 더 적합합니다.

---

## 12. 보충: 이 문서에서 다루지 않은 EIP 패턴

앞선 8가지 패턴 외에도 실무에서 자주 마주치지만 이 문서에서 명시적으로 다루지 않은 두 가지 패턴이 있습니다. 하나는 데이터를 풍부하게 만드는 Content Enricher, 다른 하나는 이 문서 전체의 근간이 되는 Pipes-and-Filters 아키텍처입니다.

### Content Enricher

Content Filter가 이벤트에서 불필요한 필드를 **제거**하는 패턴이라면, Content Enricher는 정반대로 이벤트에 부족한 정보를 외부 소스에서 가져와 **추가**하는 패턴입니다.

실무에서 이런 상황은 흔합니다. 주문 이벤트에 `customerId`만 있고 고객의 이름, 등급, 배송 주소는 없는 경우, 추천 서비스가 상품 이벤트를 받았는데 카테고리 정보가 빠져 있는 경우가 그렇습니다. 이때 이벤트 자체를 수정하는 것이 아니라, 스트림 처리 단계에서 참조 데이터를 조인하여 풍부하게 만드는 것이 Content Enricher의 핵심입니다.

Kafka Streams에서는 **KStream-KTable Join**이 Content Enricher의 가장 자연스러운 구현체입니다.

```
KStream<String, Order> orders = builder.stream("orders");
KTable<String, Customer> customers = builder.table("customers");

// orders 스트림에 customer 정보를 조인하여 풍부하게 만듦
KStream<String, EnrichedOrder> enriched = orders.join(
    customers,
    (order, customer) -> new EnrichedOrder(
        order.getOrderId(),
        order.getItems(),
        customer.getName(),     // 추가된 정보
        customer.getTier(),     // 추가된 정보
        customer.getAddress()   // 추가된 정보
    )
);
enriched.to("enriched-orders");
```

이 방식이 REST API 호출로 고객 정보를 가져오는 것보다 나은 이유는 **로컬 상태 저장소(State Store)** 덕분입니다. KTable은 customers 토픽의 최신 상태를 로컬에 캐싱하므로, 매 이벤트마다 네트워크 호출 없이 조인할 수 있습니다. 초당 수만 건의 이벤트를 처리해야 하는 상황에서 외부 API 호출과 로컬 조인의 성능 차이는 수십 배에 달합니다.

**주의할 점**: KStream-KTable Join은 키가 같은 경우에만 동작합니다. 주문 이벤트의 키가 `orderId`이고 고객 테이블의 키가 `customerId`라면, 주문 이벤트를 `customerId` 기준으로 리키(re-key)한 뒤 조인해야 합니다. 리키 과정에서 내부적으로 리파티셔닝이 발생하므로 네트워크 비용이 추가됩니다.

> 교차참조: `05-stateful-streaming.md` — KTable과 State Store의 상세 동작, `19-advanced-stream-patterns.md` — 고급 조인 패턴

### Pipes-and-Filters 아키텍처

사실 이 문서 전체가 Pipes-and-Filters 아키텍처 위에 구성되어 있습니다. Pipes-and-Filters는 EIP의 근간이 되는 아키텍처 패턴으로, 독립적인 **필터(Filter)**들을 **파이프(Pipe)**로 연결하여 메시지 처리 파이프라인을 구성하는 방식입니다. Unix의 `cat file | grep error | sort | uniq -c`와 같은 파이프라인 사고방식이 메시징 시스템에 적용된 것입니다.

이 문서에서 다룬 각 패턴은 모두 하나의 "필터"에 해당합니다.

| EIP 역할 | Kafka 매핑 | 이 문서의 해당 패턴 |
|----------|-----------|------------------|
| **파이프(Pipe)** | Kafka 토픽 | 토픽 간 데이터 흐름 |
| **필터(Filter)** | Kafka Streams 앱 / Consumer | Router, Translator, Filter, Splitter 등 |
| **소스(Source)** | Producer | 이벤트 발행자 |
| **싱크(Sink)** | Consumer / 외부 시스템 | 최종 소비자 |

Kafka Streams DSL의 체이닝 구문이 Pipes-and-Filters를 자연스럽게 표현하는 이유도 여기에 있습니다.

```java
// Pipes-and-Filters의 직접적 표현
builder.stream("raw-events")              // Source
    .mapValues(EventTranslator::translate) // Filter 1: Translator
    .mapValues(ContentFilter::strip)       // Filter 2: Content Filter
    .split()                               // Filter 3: Router
        .branch(isPayment, Branched.withConsumer(s -> s.to("payments")))
        .branch(isRefund, Branched.withConsumer(s -> s.to("refunds")))
        .defaultBranch(Branched.withConsumer(s -> s.to("other")));
```

Go 채널을 이용한 구현도 Pipes-and-Filters 패턴의 직접적 구현입니다. Go의 채널(channel)이 파이프, 고루틴(goroutine)이 필터 역할을 합니다.

```go
// Go 채널 파이프라인 = Pipes-and-Filters
events := produce(ctx)                    // Source
translated := translate(ctx, events)      // Filter 1
filtered := filter(ctx, translated)       // Filter 2
routed := route(ctx, filtered)            // Filter 3
consume(ctx, routed)                      // Sink
```

> 교차참조: `08-go-integration/11-pipeline-eip` — Go 채널 파이프라인으로 EIP 패턴을 직접 구현한 실습

---

## 13. EIP 전체 패턴 맵 — 학습 문서 크로스레퍼런스

원전(Enterprise Integration Patterns, 2003)의 65개 패턴 중 이벤트 스트리밍에서 실질적으로 관련있는 61개 패턴이 학습 문서 어디에서 다뤄지는지를 정리합니다. 이 테이블은 "이 패턴이 뭐지?" 싶을 때 해당 문서를 바로 찾아가기 위한 인덱스입니다.

**범례**: ● 전용 섹션, ◐ 다른 맥락에서 설명, ○ 미커버

### Message Construct (10)

| 패턴 | 상태 | 참조 문서 |
|------|------|-----------|
| Message | ● | 전체 문서의 기본 전제 |
| Command Message | ● | `20-eip-message-channel.md` §2.1 |
| Document Message | ● | `20-eip-message-channel.md` §2.1 |
| Event Message | ● | `02-eda-foundations.md`, 이 문서 §1 |
| Request-Reply | ● | `10-request-response-bridge.md`, `03-spring/12-replying-kafka-template` |
| Return Address | ◐ | Request-Reply 구현 내 reply-topic 헤더 |
| Correlation Identifier | ◐ | `07-choreography-saga.md`, 이 문서 §8 Event Chunking |
| Message Sequence | ● | `20-eip-message-channel.md` §2.4, 이 문서 §8 Event Chunking |
| Message Expiration | ● | `20-eip-message-channel.md` §2.3 |
| Format Indicator | ● | `20-eip-message-channel.md` §2.2 |

### Message Routing (14)

| 패턴 | 상태 | 참조 문서 |
|------|------|-----------|
| Pipes-and-Filters | ● | 이 문서 §12, `08-go/11-pipeline-eip` |
| Message Router | ● | 이 문서 §4 Event Router |
| Content-Based Router | ● | 이 문서 §4, `08-go/11-pipeline-eip` |
| Message Filter | ● | 이 문서 §7 Content Filter |
| Dynamic Router | ◐ | 이 문서 §4 TopicNameExtractor |
| Recipient List | ● | `21-eip-routing-endpoint.md` §1.2 |
| Splitter | ● | 이 문서 §5, `03-spring/13-messaging-patterns-impl` |
| Aggregator | ● | 이 문서 §5, `03-spring/11-topic-pipeline-architecture` Fan-In |
| Resequencer | ● | `21-eip-routing-endpoint.md` §1.3 |
| Composed Msg. Processor | ● | `21-eip-routing-endpoint.md` §1.4 |
| Scatter-Gather | ◐ | `03-spring/12-replying-kafka-template` AggregatingReplyingKafkaTemplate |
| Routing Slip | ● | `21-eip-routing-endpoint.md` §1.5 |
| Process Manager | ● | `21-eip-routing-endpoint.md` §1.6, `08-orchestration-saga.md` |
| Message Broker | ◐ | Kafka 자체가 브로커 (명시적 EIP 설명은 `20-eip-message-channel.md` §3.7) |

### Message Transformation (7)

| 패턴 | 상태 | 참조 문서 |
|------|------|-----------|
| Message Translator | ● | 이 문서 §6 Event Translator |
| Envelope Wrapper | ● | 이 문서 §2 Event Envelope + CloudEvents |
| Content Enricher | ● | 이 문서 §12 |
| Content Filter | ● | 이 문서 §7 + GDPR Crypto-Shredding |
| Claim Check | ● | 이 문서 §8 (S3 + Kafka) |
| Normalizer | ● | 이 문서 §3 Event Standardizer |
| Canonical Data Model | ● | 이 문서 §3 Event Standardizer |

### Messaging Endpoints (12)

| 패턴 | 상태 | 참조 문서 |
|------|------|-----------|
| Message Endpoint | ◐ | 기본 전제로 암묵적 사용 |
| Messaging Gateway | ● | `21-eip-routing-endpoint.md` §2.1 |
| Messaging Mapper | ● | `21-eip-routing-endpoint.md` §2.2 |
| Transactional Client | ● | `21-eip-routing-endpoint.md` §2.3, `02-fund/16-transactions` |
| Polling Consumer | ● | `21-eip-routing-endpoint.md` §2.4 |
| Event-Driven Consumer | ● | `21-eip-routing-endpoint.md` §2.4 |
| Competing Consumers | ● | `21-eip-routing-endpoint.md` §2.5, `02-fund/06-consumer-groups` |
| Message Dispatcher | ● | `21-eip-routing-endpoint.md` §2.6 |
| Selective Consumer | ● | `21-eip-routing-endpoint.md` §2.7 |
| Durable Subscriber | ● | `21-eip-routing-endpoint.md` §2.8 |
| Idempotent Receiver | ● | `18-idempotency-patterns.md`, `03-spring/06-idempotent-consumer` |
| Service Activator | ● | `21-eip-routing-endpoint.md` §2.1 |

### Messaging Channels (10)

| 패턴 | 상태 | 참조 문서 |
|------|------|-----------|
| Message Channel | ◐ | Kafka Topic = Message Channel (암묵적) |
| Point-to-Point Channel | ● | `20-eip-message-channel.md` §3.1 |
| Publish-Subscribe Channel | ● | `20-eip-message-channel.md` §3.1 |
| Datatype Channel | ● | `20-eip-message-channel.md` §3.2 |
| Invalid Message Channel | ● | `20-eip-message-channel.md` §3.3 |
| Dead Letter Channel | ● | `03-spring/05-dlq-strategy`, `08-go/05-error-handling-dlq` |
| Guaranteed Delivery | ● | `20-eip-message-channel.md` §3.4 |
| Channel Adapter | ● | `20-eip-message-channel.md` §3.5, `07-connectors` |
| Messaging Bridge | ● | `20-eip-message-channel.md` §3.6 |
| Message Bus | ● | `20-eip-message-channel.md` §3.7 |

### Systems Management (8)

| 패턴 | 상태 | 참조 문서 |
|------|------|-----------|
| Control Bus | ● | `22-eip-system-management.md` §3.1 |
| Detour | ● | `22-eip-system-management.md` §2.3 |
| Wire Tap | ● | `22-eip-system-management.md` §1.1 |
| Message History | ● | `22-eip-system-management.md` §1.2 |
| Message Store | ● | `22-eip-system-management.md` §1.3 |
| Smart Proxy | ● | `22-eip-system-management.md` §3.2 |
| Test Message | ● | `22-eip-system-management.md` §2.1 |
| Channel Purger | ● | `22-eip-system-management.md` §2.2 |

---

## 참고 자료

- Gregor Hohpe, Bobby Woolf, "Enterprise Integration Patterns" (2003) — 패턴의 원전
- [Confluent Event Streaming Patterns](https://developer.confluent.io/patterns/) — Kafka 컨텍스트의 패턴 가이드
- [CloudEvents Specification](https://cloudevents.io/) — 이벤트 메타데이터 표준
- 기존 문서: `13-topic-pipeline-architecture.md` — FilterBranch, FanOut 등 토픽 파이프라인 패턴
- 기존 문서: `10-message-schema-design.md` — Schema Registry 호환성 모드, Avro 설계
- 기존 문서: `15-event-sourcing.md` — 이벤트 불변성, Event Store 개념
- 신규 문서: `20-eip-message-channel.md` — 메시지 구조 + 채널 패턴 (Message Construct, Messaging Channels)
- 신규 문서: `21-eip-routing-endpoint.md` — 고급 라우팅 + 엔드포인트 패턴 (Message Routing, Messaging Endpoints)
- 신규 문서: `22-eip-system-management.md` — 시스템 관리 패턴 (Systems Management)
