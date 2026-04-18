# 03. Source/Sink 커넥터와 Event Gateway — Spring Boot 구현

> **시리즈**: `learning/07-connectors/` — Redpanda 커넥터 통합 학습
> | **[01-이론](01-source-sink-patterns.md)** | [02-Redpanda Connect](02-redpanda-connect.md) | **03-Spring Boot** | [04-운영](04-operations.md) |

Spring Boot에서 외부 시스템과 Redpanda를 연결하는 Source/Sink 패턴을 실전 코드로 구현한다. KafkaTemplate 기본 사용법과 Consumer 설정은 [03-spring-boot-integration/](../03-spring-boot-integration/) 참조.

---

## 1. Source/Sink 패턴과 Spring Boot

> **Source/Sink 패턴 이론**: [01-source-sink-patterns.md §1](./01-source-sink-patterns.md) 참조.

Spring Boot가 Source/Sink 역할을 맡는 방식과 구현 경로 선택 기준은 아래와 같다.

| 역할 | 대표 패턴 | 특징 |
|------|----------|------|
| Source | Write-Aside (Dual Write) | DB 저장 + Kafka 전송 동시 수행. 구현 단순하나 원자성 미보장 |
| Source | Outbox 패턴 | DB 트랜잭션에 이벤트 포함 → CDC 발행. effectively-once에 가장 가까움 |
| Source | Event Gateway | 외부 HTTP/Webhook → Kafka 변환. 외부 시스템이 Kafka를 직접 알 필요 없음 |
| Sink | `@KafkaListener` | Kafka 이벤트 수신 → DB/S3/Elasticsearch 저장 |

Spring Boot에서 Source/Sink 구현 경로는 직접 Producer/Consumer(유연성 최대, 에러 처리 직접), Kafka Connect(설정 기반, 별도 프로세스), Spring Cloud Stream(미들웨어 추상화) 세 가지다. 이 문서는 가장 실전적인 **직접 Producer/Consumer**와 **Redpanda Connect 통합**에 집중한다.

> **선택 의사결정 흐름도**: [01-source-sink-patterns.md §3](./01-source-sink-patterns.md) 참조.

---

## 2. Database Write-Aside 구현 (Dual Write)

> **TransactionSynchronization 심화 및 트랜잭션 Producer 설정**: [07-transaction-patterns.md](../03-spring-boot-integration/07-transaction-patterns.md) 참조.

### 가장 단순한 선택, 그리고 그 함정

`@Transactional` 메서드 안에서 DB 저장 후 `kafkaTemplate.send()`를 호출하는 것이 가장 직관적이다. 그러나 Kafka 전송은 DB 트랜잭션과 무관하게 즉시 브로커에 전달되므로, DB 커밋 실패 시에도 메시지는 이미 발행된 상태가 된다.

> KafkaTemplate 비동기/동기 전송 패턴은 [03-producer-consumer.md](../03-spring-boot-integration/03-producer-consumer.md) 참조.

### TransactionSynchronization으로 개선

`afterCommit()` 콜백을 등록하면 DB 커밋 성공 후에만 Kafka 전송이 실행되어 "DB 실패 + 이벤트 발행" 상황을 막을 수 있다. 단, `afterCommit()` 안에서 Kafka 전송이 실패하면 이벤트는 유실된다.

> 구체적인 구현 코드와 트레이드오프 분석은 [07-transaction-patterns.md §DB+Kafka 원자성](../03-spring-boot-integration/07-transaction-patterns.md) 참조.

### 언제 Dual Write를 선택하는가

이벤트 유실이 가끔 발생해도 비즈니스적으로 허용되거나, 재처리 메커니즘(배치 보정 등)이 이미 갖춰진 경우에 적합하다. 분석용 이벤트나 수동 재발행이 가능한 내부 시스템이 그 예다.

---

## 3. Outbox 패턴 구현 (Write-Through + CDC)

> **Outbox 패턴 개념과 Redpanda Connect Relay 구현**: [02-redpanda-connect.md §6 "Transactional Outbox/Inbox"](./02-redpanda-connect.md) 참조.
> **Outbox/CDC 이론**: [08-outbox-cdc.md](../02-fundamentals/08-outbox-cdc.md) 참조.

### build.gradle

```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.kafka:spring-kafka'
    implementation 'org.apache.avro:avro:1.11.3'
    implementation 'io.confluent:kafka-avro-serializer:7.6.0'
    runtimeOnly 'org.postgresql:postgresql'
    testImplementation 'org.testcontainers:kafka'
    testImplementation 'org.testcontainers:postgresql'
}
```

### Outbox 엔티티 설계

`aggregateType`은 Debezium Outbox Router가 Kafka 토픽 이름으로 변환하고, `aggregateId`는 Kafka 메시지 키(파티셔닝 기준)로 쓰이며, `type`은 이벤트 타입 헤더로 설정된다.

```java
@Entity
@Table(name = "outbox_events")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class OutboxEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private String aggregateType;  // Debezium이 Kafka 토픽 이름으로 사용 (예: "order")

    @Column(nullable = false)
    private String aggregateId;    // Kafka 메시지 키 (파티셔닝 기준)

    @Column(nullable = false)
    private String type;           // 이벤트 타입 헤더 (예: "OrderCreated")

    @Column(nullable = false, columnDefinition = "TEXT")
    private String payload;        // JSON 또는 Avro 직렬화 페이로드

    @Column(nullable = false)
    private Instant createdAt;

    public static OutboxEvent of(String aggregateType, String aggregateId,
                                  String type, String payload) {
        OutboxEvent event = new OutboxEvent();
        event.aggregateType = aggregateType;
        event.aggregateId = aggregateId;
        event.type = type;
        event.payload = payload;
        event.createdAt = Instant.now();
        return event;
    }
}
```

### @TransactionalEventListener 활용

`OrderService`가 Outbox 저장소에 직접 의존하면 도메인 서비스가 인프라 관심사를 알게 된다. `@TransactionalEventListener(phase = BEFORE_COMMIT)`을 사용하면 서비스는 도메인 이벤트만 발행하고, Outbox 저장은 별도 핸들러가 담당한다. `BEFORE_COMMIT` 단계에서 실행된 Outbox 저장은 원래 트랜잭션에 참여하므로 롤백 시 함께 취소된다.

```mermaid
sequenceDiagram
    participant C as "Client"
    participant SVC as "OrderService"
    participant EP as "ApplicationEventPublisher"
    participant OBH as "OrderOutboxHandler<br>(BEFORE_COMMIT)"
    participant DB as "PostgreSQL"

    C->>SVC: createOrder()
    activate SVC
    Note over SVC: @Transactional 시작
    SVC->>DB: orders INSERT
    SVC->>EP: publishEvent(OrderCreatedDomainEvent)
    EP->>OBH: handle(event) — 커밋 직전 실행
    OBH->>DB: outbox_events INSERT ← 같은 트랜잭션
    Note over SVC,DB: 트랜잭션 커밋 (둘 다 성공)<br>or 롤백 (둘 다 취소)
    SVC-->>C: order
    deactivate SVC
```

```java
public record OrderCreatedDomainEvent(Order order) {}

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        Order order = Order.from(request);
        orderRepository.save(order);
        eventPublisher.publishEvent(new OrderCreatedDomainEvent(order));
        return order;
    }
}

@Component
@RequiredArgsConstructor
public class OrderOutboxHandler {

    private final OutboxEventRepository outboxEventRepository;
    private final ObjectMapper objectMapper;

    @TransactionalEventListener(phase = TransactionPhase.BEFORE_COMMIT)
    public void handle(OrderCreatedDomainEvent domainEvent) throws JsonProcessingException {
        Order order = domainEvent.order();
        String payload = objectMapper.writeValueAsString(OrderCreatedPayload.from(order));
        outboxEventRepository.save(
            OutboxEvent.of("order", order.getId().toString(), "OrderCreated", payload)
        );
    }
}
```

### Debezium 설정 (application.yml)

`transforms.outbox.route.by.field`가 `aggregate_type` 값을 읽어 Kafka 토픽 이름을 동적으로 결정한다. `order`가 들어오면 `order.events` 토픽으로 라우팅된다.

```yaml
debezium:
  connector:
    name: outbox-connector
    config:
      connector.class: io.debezium.connector.postgresql.PostgresConnector
      database.hostname: localhost
      database.port: 5432
      database.user: postgres
      database.password: ${DB_PASSWORD}
      database.dbname: mydb
      database.server.name: mydb-server
      table.include.list: public.outbox_events
      plugin.name: pgoutput

      transforms: outbox
      transforms.outbox.type: io.debezium.transforms.outbox.EventRouter
      transforms.outbox.table.field.event.id: id
      transforms.outbox.table.field.event.key: aggregate_id
      transforms.outbox.table.field.event.type: type
      transforms.outbox.table.field.event.payload: payload
      transforms.outbox.route.by.field: aggregate_type
      transforms.outbox.route.topic.replacement: ${routedByValue}.events
      # 결과: aggregate_type=order → Kafka 토픽 = order.events
```

---

## 4. Event Gateway 구현 (REST → Kafka Bridge)

> **Event Gateway 역할과 책임**: [01-source-sink-patterns.md §2](./01-source-sink-patterns.md) 참조.

외부 시스템이 Kafka에 직접 접근할 수 없을 때, Gateway가 인증·인가, Rate Limiting, 스키마 검증, 프로토콜 변환을 담당한다.

### EventGatewayController 구현

핵심은 두 가지다. 첫째, `{eventType}` 경로 변수를 `eventValidator`가 Kafka 토픽으로 변환하여 외부 이름과 내부 토픽 이름을 분리한다. 둘째, `Idempotency-Key` 헤더를 Kafka 메시지 키로 활용해 클라이언트 재시도 시 중복 처리 방지 기반을 마련한다.

```java
@RestController
@RequestMapping("/api/v1/events")
@RequiredArgsConstructor
@Slf4j
public class EventGatewayController {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final EventValidator eventValidator;
    private final EventMetricsRecorder metricsRecorder;
    private final WebhookVerifier webhookVerifier;

    @PostMapping("/{eventType}")
    public CompletableFuture<ResponseEntity<EventPublishedResponse>> publish(
            @PathVariable String eventType,
            @RequestBody @Valid EventRequest request,
            @RequestHeader(value = "X-Source-System", required = false) String sourceSystem,
            @RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey) {

        String targetTopic = eventValidator.resolveTopicOrThrow(eventType);
        String eventKey = idempotencyKey != null ? idempotencyKey : UUID.randomUUID().toString();

        GatewayEvent gatewayEvent = GatewayEvent.builder()
            .eventId(eventKey)
            .eventType(eventType)
            .sourceSystem(sourceSystem)
            .payload(request.payload())
            .occurredAt(Instant.now())
            .build();

        return kafkaTemplate.send(targetTopic, eventKey, gatewayEvent)
            .thenApply(result -> {
                metricsRecorder.recordSuccess(eventType);
                log.info("Event published via gateway. type={}, topic={}, offset={}",
                    eventType, targetTopic, result.getRecordMetadata().offset());
                return ResponseEntity.accepted()
                    .body(new EventPublishedResponse(eventKey, targetTopic));
            })
            .exceptionally(ex -> {
                metricsRecorder.recordFailure(eventType);
                log.error("Failed to publish event via gateway. type={}", eventType, ex);
                return ResponseEntity.internalServerError()
                    .body(new EventPublishedResponse(eventKey, null));
            })
            .toCompletableFuture();
    }

    /**
     * Webhook 수신 엔드포인트.
     * 외부 시스템(GitHub, Stripe 등)이 보낸 Webhook을 내부 Kafka 이벤트로 변환한다.
     */
    @PostMapping("/webhook/{provider}")
    public ResponseEntity<Void> receiveWebhook(
            @PathVariable String provider,
            @RequestBody String rawPayload,
            @RequestHeader Map<String, String> headers) {

        webhookVerifier.verify(provider, rawPayload, headers);

        WebhookReceivedEvent event = WebhookReceivedEvent.builder()
            .provider(provider)
            .rawPayload(rawPayload)
            .receivedAt(Instant.now())
            .build();

        // 비동기 발행, 202 즉시 응답 (Webhook은 빠른 응답이 필수)
        kafkaTemplate.send("webhook.received." + provider, UUID.randomUUID().toString(), event);
        return ResponseEntity.accepted().build();
    }
}
```

### Rate Limiting 적용

Event Gateway는 인터넷에 노출되는 진입점이므로 Rate Limiting이 필수다. Bucket4j는 토큰 버킷 알고리즘을 구현한 라이브러리로, IP별 버킷을 만들어 초과 요청을 429로 차단한다. 분산 환경이라면 `bucket4j-redis`를 추가해 Redis 기반으로 전환한다.

```gradle
dependencies {
    implementation 'com.bucket4j:bucket4j-core:8.10.1'
    // 분산 Rate Limiting: implementation 'com.bucket4j:bucket4j-redis:8.10.1'
}
```

```java
@Component
public class RateLimitInterceptor implements HandlerInterceptor {

    // IP당 분당 100건 제한
    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

    @Override
    public boolean preHandle(HttpServletRequest request,
                              HttpServletResponse response,
                              Object handler) throws IOException {
        String clientIp = request.getRemoteAddr();
        Bucket bucket = buckets.computeIfAbsent(clientIp, this::newBucket);

        if (bucket.tryConsume(1)) {
            return true;
        }

        response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
        response.getWriter().write("Rate limit exceeded");
        return false;
    }

    private Bucket newBucket(String ip) {
        return Bucket.builder()
            .addLimit(Bandwidth.classic(100, Refill.greedy(100, Duration.ofMinutes(1))))
            .build();
    }
}
```

---

## 5. Sink Connector: 이벤트 → 외부 시스템

> **DLQ 전략과 DefaultErrorHandler 설정**: [05-dlq-strategy.md](../03-spring-boot-integration/05-dlq-strategy.md) 참조.

Sink 컴포넌트는 Kafka 이벤트를 수신해서 외부 시스템(DB, S3, Elasticsearch 등)에 저장하거나 전달한다. 두 가지 과제를 동시에 다뤄야 한다. 첫째는 실패 처리(재시도 횟수, DLQ 이동), 둘째는 처리 효율(이벤트 하나마다 외부 시스템을 호출하면 성능이 나오지 않으므로 배치 API 활용).

```mermaid
flowchart TD
    RP["Redpanda<br>order.events Topic"]

    subgraph SINK["Sink Consumer (Spring Boot)"]
        KL["@KafkaListener<br>(배치 모드)"]
        EH["ErrorHandler<br>(DefaultErrorHandler)"]
        BO["BackOff<br>(FixedBackOff: 1s × 3회)"]
        DLQ["DeadLetterPublishingRecoverer<br>(DLQ 발행)"]
    end

    subgraph STORE["외부 저장소"]
        S3["S3<br>(NDJSON 업로드)"]
        ES["Elasticsearch<br>(Bulk 인덱싱)"]
        DB2["Database<br>(UPSERT)"]
    end

    RP -->|"consume (batch)"| KL
    KL -->|"성공 → ack"| STORE
    KL -->|"실패 → throw"| EH
    EH --> BO
    BO -->|"재시도 소진"| DLQ
    DLQ -->|"produce"| DLQT["order.events.DLT<br>(DLQ Topic)"]

    style KL fill:#dbeafe,color:#333
    style EH fill:#fef9c3,color:#333
    style DLQ fill:#fee2e2,color:#333
    style DLQT fill:#fee2e2,color:#333
```

### 배치 ContainerFactory 설정

배치 리스너를 쓰려면 `setBatchListener(true)`를 설정한 전용 `ContainerFactory`가 필요하다. `FixedBackOff(1000L, 3L)`은 1초 간격 3회 재시도 후 DLQ로 이동시킨다.

```java
@Configuration
public class KafkaBatchConfig {

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Object>
    batchKafkaListenerContainerFactory(ConsumerFactory<String, Object> consumerFactory,
                                       KafkaTemplate<String, Object> kafkaTemplate) {

        ConcurrentKafkaListenerContainerFactory<String, Object> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        factory.setBatchListener(true);
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL);

        factory.setCommonErrorHandler(new DefaultErrorHandler(
            new DeadLetterPublishingRecoverer(kafkaTemplate),
            new FixedBackOff(1000L, 3L)
        ));

        return factory;
    }
}
```

### S3 Sink 구현

파티션별로 레코드를 그룹핑한 뒤 NDJSON 파일로 직렬화해서 업로드한다. 파일명에 파티션 번호와 오프셋 범위를 포함하면 특정 이벤트 추적이 편해진다.

```gradle
dependencies {
    implementation 'software.amazon.awssdk:s3:2.25.0'
    implementation 'software.amazon.awssdk:auth:2.25.0'
}
```

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class S3SinkConsumer {

    private final S3Client s3Client;

    @Value("${sink.s3.bucket-name}")
    private String bucketName;

    @KafkaListener(
        topics = "order.events",
        groupId = "s3-sink-group",
        containerFactory = "batchKafkaListenerContainerFactory"
    )
    public void consumeBatch(List<ConsumerRecord<String, OrderEvent>> records,
                              Acknowledgment ack) {
        if (records.isEmpty()) {
            ack.acknowledge();
            return;
        }

        try {
            Map<Integer, List<ConsumerRecord<String, OrderEvent>>> byPartition =
                records.stream().collect(Collectors.groupingBy(ConsumerRecord::partition));

            byPartition.forEach((partition, partitionRecords) -> {
                String s3Key = buildS3Key(partition, partitionRecords);
                String content = serializeToNdjson(partitionRecords);
                uploadToS3(s3Key, content);
            });

            ack.acknowledge();
            log.info("S3 sink: uploaded {} records to bucket={}", records.size(), bucketName);

        } catch (Exception ex) {
            log.error("S3 sink upload failed. count={}", records.size(), ex);
            throw new S3SinkException("Failed to upload batch to S3", ex);
        }
    }

    // S3 키 형식: events/year=YYYY/month=MM/day=DD/partition=N/offset-MIN-MAX.ndjson
    // 레코드 직렬화: ObjectMapper로 NDJSON (줄바꿈 구분 JSON) 생성
    // S3 업로드: PutObjectRequest.builder().bucket(bucketName).key(key) 사용
}
```

### Elasticsearch Sink 구현

Bulk API는 개별 문서 단위로 성공/실패가 갈릴 수 있다. `response.errors()`로 전체 실패를 확인한 뒤 실패한 항목만 추려서 로깅한다.

```gradle
dependencies {
    implementation 'co.elastic.clients:elasticsearch-java:8.13.0'
    implementation 'com.fasterxml.jackson.core:jackson-databind'
}
```

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class ElasticsearchSinkConsumer {

    private final ElasticsearchClient esClient;

    @KafkaListener(
        topics = "product.search.events",
        groupId = "es-sink-group",
        containerFactory = "batchKafkaListenerContainerFactory"
    )
    public void consumeBatch(List<ConsumerRecord<String, ProductEvent>> records,
                              Acknowledgment ack) {
        if (records.isEmpty()) {
            ack.acknowledge();
            return;
        }

        try {
            BulkRequest.Builder bulkBuilder = new BulkRequest.Builder();

            for (ConsumerRecord<String, ProductEvent> record : records) {
                ProductEvent event = record.value();
                bulkBuilder.operations(op -> op
                    .index(idx -> idx
                        .index("products")
                        .id(event.getProductId())
                        .document(ProductSearchDoc.from(event))
                    )
                );
            }

            BulkResponse response = esClient.bulk(bulkBuilder.build());

            if (response.errors()) {
                // 부분 실패: 실패한 문서만 로깅 (전체 재시도 대신 선택적 처리)
                response.items().stream()
                    .filter(item -> item.error() != null)
                    .forEach(item -> log.error("ES indexing failed. id={}, error={}",
                        item.id(), item.error().reason()));
            }

            ack.acknowledge();
            log.info("ES sink: indexed {} documents", records.size());

        } catch (IOException ex) {
            log.error("ES sink failed. count={}", records.size(), ex);
            throw new ElasticsearchSinkException("Bulk indexing failed", ex);
        }
    }
}
```

---

## 6. Redpanda Connect(rpk connect) 통합

> **Redpanda Connect 개념과 컴포넌트 상세**: [02-redpanda-connect.md](./02-redpanda-connect.md) 참조.

Spring Boot 앱이 HTTP 엔드포인트를 노출하면 rpk connect가 그것을 입력 소스로 폴링할 수 있다. Spring Boot는 비즈니스 로직을, rpk connect는 파이프라인 라우팅을 담당하는 역할 분리가 자연스럽게 이루어진다.

```mermaid
flowchart LR
    subgraph SB["Spring Boot 앱"]
        API["GET /api/v1/events/pending<br>(HTTP 엔드포인트)"]
    end

    subgraph RPC["Redpanda Connect (rpk connect)"]
        IN["input:<br>http_client<br>(10req/s 제한)"]
        PROC["pipeline:<br>processors<br>(mapping/변환)"]
        OUT["output:<br>kafka_franz"]
    end

    subgraph RP["Redpanda"]
        TP["spring-events<br>Topic"]
    end

    SB -->|"HTTP GET (폴링)"| IN
    IN --> PROC
    PROC --> OUT
    OUT -->|"produce"| TP
```

```yaml
# rpk connect가 Spring Boot 앱의 REST API를 폴링하는 설정
input:
  http_client:
    url: http://spring-app:8080/api/v1/events/pending
    verb: GET
    rate_limit: my_rate_limit
    headers:
      Authorization: "Bearer ${API_TOKEN}"

rate_limit_resources:
  - label: my_rate_limit
    local:
      count: 10
      interval: 1s

output:
  kafka_franz:
    seed_brokers:
      - redpanda:19092
    topic: spring-events
```

### 파이프라인 예시: JDBC Source → Redpanda → S3 Sink

rpk connect의 `broker` 출력을 활용하면 같은 데이터를 여러 목적지로 동시에 보낼 수 있다. Spring Boot 코드 한 줄 없이 YAML만으로 DB 폴링 → Redpanda + S3 동시 저장 파이프라인이 동작한다.

```mermaid
flowchart LR
    subgraph DB["PostgreSQL"]
        OT2["orders 테이블<br>(status=PENDING)"]
    end

    subgraph RPC2["Redpanda Connect"]
        IN2["input:<br>sql_select<br>(30s 주기)"]
        PROC2["pipeline:<br>mapping 변환"]
        OUT2["output broker<br>(fan-out)"]
    end

    subgraph OUT_TARGETS["출력 대상"]
        RP2["Redpanda<br>order.events"]
        S3T["S3<br>events/orders/"]
    end

    OT2 -->|"WHERE status=PENDING"| IN2
    IN2 --> PROC2
    PROC2 --> OUT2
    OUT2 -->|"kafka_franz"| RP2
    OUT2 -->|"aws_s3"| S3T
```

```yaml
# redpanda-connect-pipeline.yaml
input:
  sql_select:
    driver: postgres
    dsn: "postgres://postgres:password@postgres:5432/mydb?sslmode=disable"
    table: orders
    columns: [id, customer_id, status, created_at]
    where: "status = 'PENDING' AND processed = false"
    period: 30s

pipeline:
  processors:
    - mapping: |
        root = {
          "event_type": "OrderPending",
          "order_id": this.id,
          "customer_id": this.customer_id,
          "occurred_at": this.created_at
        }

output:
  broker:
    - kafka_franz:
        seed_brokers: [localhost:19092]
        topic: order.events
        key: ${! json("order_id") }
    - aws_s3:
        bucket: my-events-bucket
        path: events/orders/${! timestamp_unix() }-${! uuid_v4() }.json
        credentials:
          id: ${AWS_ACCESS_KEY_ID}
          secret: ${AWS_SECRET_ACCESS_KEY}
```

### Docker Compose에서 rpk connect 실행

```yaml
services:
  redpanda-connect:
    image: docker.redpanda.com/redpandadata/connect:latest
    volumes:
      - ./redpanda-connect-pipeline.yaml:/connect.yaml
    command: run /connect.yaml
    environment:
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
      API_TOKEN: ${API_TOKEN}
    depends_on:
      - redpanda
      - postgres
    restart: unless-stopped
```

---

## 7. 테스트 전략

> **Testcontainers 컨테이너 설정, @DynamicPropertySource, EmbeddedKafka vs Testcontainers 비교**: [10-testing.md](../03-spring-boot-integration/10-testing.md) 참조.

Source/Sink 테스트는 빠른 피드백이 필요한 부분과 실제 인프라 연동이 필요한 부분을 계층으로 나눈다.

| 계층 | 도구 | 대상 | 실행 주기 |
|------|------|------|----------|
| 단위 테스트 | JUnit + Mock | OrderService, EventGatewayController, S3SinkConsumer(Mock S3Client) | PR마다 |
| 슬라이스 테스트 | @DataJpaTest, EmbeddedKafka | OutboxEvent 저장, @KafkaListener 기동 확인 | PR마다 |
| 통합 테스트 | Testcontainers | Outbox→CDC→Topic 전체 흐름, 이벤트→S3 업로드 | 머지 전 |

### Source 통합 테스트: Outbox 레코드 저장 검증

`@Testcontainers` + `@DynamicPropertySource` 기본 구조는 [10-testing.md](../03-spring-boot-integration/10-testing.md)를 참조한다. 이 테스트의 핵심은 **Outbox 레코드가 같은 트랜잭션에서 저장됐는지** 검증하는 부분이다.

```java
// RedpandaContainer + PostgreSQLContainer + @DynamicPropertySource 설정은 10-testing.md 참조

@Test
void 주문_생성시_Outbox_레코드가_저장되어야_한다() {
    Order order = orderService.createOrder(new CreateOrderRequest("customer-1", List.of("item-1")));

    await().atMost(Duration.ofSeconds(5)).untilAsserted(() -> {
        List<OutboxEvent> events = outboxEventRepository.findByAggregateId(order.getId().toString());
        assertThat(events).hasSize(1);
        assertThat(events.get(0).getType()).isEqualTo("OrderCreated");
        assertThat(events.get(0).getAggregateType()).isEqualTo("order");
    });
}
```

### Sink 통합 테스트: 이벤트 수신 → S3 업로드 검증

Sink 테스트는 방향이 반대다. Kafka 토픽에 이벤트를 직접 발행한 뒤 LocalStack S3에 파일이 올라갔는지 비동기로 확인한다. `awaitility`가 Kafka Consumer의 처리 지연을 흡수한다.

```java
// RedpandaContainer + LocalStackContainer 설정은 10-testing.md 참조

@BeforeEach
void setUp() {
    s3Client.createBucket(b -> b.bucket(bucketName));
}

@Test
void 이벤트_수신시_S3에_파일이_업로드되어야_한다() throws Exception {
    kafkaTemplate.send("order.events", "order-001",
        OrderEvent.builder().orderId("order-001").customerId("customer-1").status("CREATED").build()
    ).get();

    await().atMost(Duration.ofSeconds(10)).untilAsserted(() -> {
        ListObjectsV2Response objects = s3Client.listObjectsV2(
            b -> b.bucket(bucketName).prefix("events/")
        );
        assertThat(objects.contents()).isNotEmpty();
    });
}
```

---

## 참고 자료

- [Spring for Apache Kafka 공식 문서](https://docs.spring.io/spring-kafka/docs/current/reference/html/)
- [Debezium Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
- [Redpanda Connect 공식 문서](https://docs.redpanda.com/redpanda-connect/about/)
- [Bucket4j Rate Limiter](https://github.com/bucket4j/bucket4j)
- [Testcontainers for Java](https://testcontainers.com/guides/getting-started-with-testcontainers-for-java/)
- 기존 문서: [02-producer-consumer.md](../03-spring-boot-integration/02-producer-consumer.md) — KafkaTemplate 기본 사용법
- 기존 문서: [07-transaction-patterns.md](../03-spring-boot-integration/07-transaction-patterns.md) — TransactionSynchronization 심화
- 기존 문서: [05-dlq-strategy.md](../03-spring-boot-integration/05-dlq-strategy.md) — Sink 에러 처리 및 DLQ 연계
- 운영/에러 처리: [04-operations.md](./04-operations.md) — 에러 핸들링, DLQ, 모니터링
