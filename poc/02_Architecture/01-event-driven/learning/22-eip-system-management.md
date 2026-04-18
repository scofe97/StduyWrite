# 22. EIP 시스템 관리 패턴

메시징 시스템의 "관측, 테스트, 운영" — 프로덕션 환경에서 메시지 흐름을 제어하고 모니터링하는 EIP 패턴을 Kafka 생태계에서 이해한다.

## 학습 목표

- Wire Tap, Message History 등 관측성 패턴으로 메시지 흐름을 모니터링하는 방법을 이해한다
- Test Message, Channel Purger 등 테스트/디버깅 패턴의 프로덕션 활용법을 파악한다
- Control Bus 패턴으로 메시징 시스템을 런타임에 제어하는 전략을 이해한다
- 8개 Systems Management 패턴 전체를 Kafka 매핑과 함께 습득한다

---

## 1. 관측성 패턴

EIP의 Systems Management 패턴 범주는 메시징 시스템을 운영하면서 필연적으로 마주치는 질문들에 답합니다. "이 메시지가 실제로 처리되고 있는가?", "처리 과정에서 어디가 병목인가?", "장애가 발생했을 때 이 메시지는 어느 단계에서 실패했는가?" 이런 질문들은 기능 개발보다 훨씬 어렵고, 메시지가 비동기로 흐르는 환경에서는 더욱 그렇습니다. Kafka의 경우 메시지가 여러 토픽과 컨슈머 그룹을 거치며 변환되기 때문에, 전통적인 동기 호출의 스택 트레이스 방식으로는 추적이 불가능합니다. EIP는 이 문제를 해결하기 위한 세 가지 관측성 패턴을 제시합니다.

### 1.1 Wire Tap

Wire Tap은 메시지가 흐르는 채널에 "분기점"을 만들어, 원래 흐름을 전혀 방해하지 않으면서 메시지 사본을 별도의 관측 채널로 보내는 패턴입니다. 이름이 직관적입니다. 전화 도청처럼, 주 회선을 끊지 않고 옆에서 흐름을 들여다보는 방식입니다.

Kafka에서 Wire Tap을 구현하는 방법은 두 가지입니다. 첫 번째는 `KStream.peek()`입니다. `peek()`은 스트림의 각 레코드를 소비하면서 부수 효과(side effect)를 실행하지만, 레코드 자체는 수정하지 않고 그대로 통과시킵니다. 로깅이나 메트릭 카운터 증가 같은 간단한 관측에 적합합니다. 두 번째는 별도의 감사(audit) 토픽으로 프로듀싱하는 방식입니다. `peek()` 내부에서 별도 프로듀서를 통해 `payments.audit` 같은 토픽에 비동기로 메시지 사본을 전송합니다. 이 방식은 감사 레코드를 장기 보존하거나, 다른 팀이 독립적으로 구독할 수 있다는 장점이 있습니다.

Wire Tap의 핵심 원칙은 **주 흐름에 제로 영향(zero-impact)**이어야 한다는 것입니다. 만약 Wire Tap 처리가 실패하거나 느려져서 주 메시지 처리를 지연시킨다면, 관측하려다 시스템을 망가뜨리는 역설이 됩니다. 따라서 감사 토픽 프로듀싱은 항상 `acks=0` 또는 비동기(fire-and-forget)로 구성하고, Wire Tap 처리 실패가 주 흐름의 예외로 전파되지 않도록 `try-catch`로 격리해야 합니다.

실제 활용 사례로는 결제 이벤트의 실시간 부정 거래 감지가 있습니다. `payments.processed` 토픽의 메시지를 Wire Tap으로 `fraud.detection.input` 토픽에 복사해, 부정 거래 감지 서비스가 비동기로 분석합니다. 결제 처리 서비스는 부정 거래 감지와 완전히 독립적으로 동작하며, 부정 거래 감지 서비스의 장애가 결제 흐름에 영향을 주지 않습니다.

MirrorMaker 2도 거시적 관점에서 Wire Tap의 한 형태입니다. 운영 클러스터의 토픽을 분석 클러스터로 미러링하여, 분석 워크로드가 운영 클러스터에 부하를 주지 않도록 분리합니다.

```java
// Wire Tap: peek()으로 감사 로그 + 별도 토픽으로 비동기 복사
KStream<String, PaymentEvent> payments = builder.stream("payments.processed");

KafkaProducer<String, PaymentEvent> auditProducer = createAuditProducer();

payments
    .peek((key, value) -> {
        // 1. 동기 로깅 (매우 빠른 부수 효과만 허용)
        log.info("Wire tap: payment {} amount={}", key, value.getAmount());
        metricsRegistry.counter("payments.processed").increment();

        // 2. 비동기 감사 토픽 프로듀싱 (fire-and-forget, 실패 격리)
        try {
            ProducerRecord<String, PaymentEvent> auditRecord =
                new ProducerRecord<>("payments.audit", key, value);
            auditRecord.headers().add("wire-tap-time",
                Instant.now().toString().getBytes());
            auditProducer.send(auditRecord); // 콜백 없음 = fire-and-forget
        } catch (Exception e) {
            // Wire Tap 실패가 주 흐름을 중단시키지 않음
            log.warn("Wire tap to audit topic failed, ignoring: {}", e.getMessage());
        }
    })
    .filter((key, value) -> value.getStatus() == PaymentStatus.APPROVED)
    .to("payments.approved");
```

### 1.2 Message History

Message History 패턴은 메시지가 처리 파이프라인을 거치면서 각 단계의 처리 정보를 메시지 자체에 누적하는 패턴입니다. 메시지를 받은 각 노드는 자신의 식별자와 타임스탬프를 헤더에 추가하고 전달합니다. 최종 소비자 또는 디버거는 헤더를 읽어 메시지의 전체 여정을 역추적할 수 있습니다.

Kafka에서 구현하는 방법은 Record Headers를 활용하는 것입니다. `ProducerRecord`의 `Headers` 객체에 각 처리 단계의 식별자를 JSON 배열로 누적합니다. 헤더는 메시지 페이로드와 분리되어 있기 때문에, 비즈니스 로직을 건드리지 않고 인프라 레벨에서 추가할 수 있습니다.

Message History와 분산 추적(Distributed Tracing)은 비슷해 보이지만 목적이 다릅니다. OpenTelemetry 기반의 분산 추적은 인프라 레벨에서 HTTP 요청, DB 쿼리, Kafka produce/consume 연산의 지연 시간을 측정합니다. 반면 Message History는 애플리케이션 레벨에서 "어떤 비즈니스 컴포넌트가 이 메시지를 처리했는가"를 기록합니다. 두 접근이 상호 보완적입니다. 분산 추적으로 어느 구간에서 지연이 발생했는지 찾고, Message History로 해당 구간의 비즈니스 처리 맥락을 파악합니다.

Message History가 표준 분산 추적보다 유리한 상황은 멀티 브로커 또는 조직 간 메시지 흐름입니다. 외부 파트너 시스템과 메시지를 교환할 때, 상대방 시스템이 OpenTelemetry를 지원하지 않을 수 있습니다. 이 경우 메시지 헤더에 포함된 Message History는 추적 인프라에 관계없이 동작합니다.

```java
// 각 처리 단계에서 Message History 헤더를 누적하는 유틸리티
public class MessageHistoryUtil {

    private static final String HISTORY_HEADER = "X-Message-History";
    private static final ObjectMapper MAPPER = new ObjectMapper();

    public static void appendHistory(Headers headers, String nodeId) {
        try {
            List<Map<String, String>> history = readHistory(headers);
            history.add(Map.of(
                "node", nodeId,
                "timestamp", Instant.now().toString(),
                "host", InetAddress.getLocalHost().getHostName()
            ));
            headers.remove(HISTORY_HEADER);
            headers.add(HISTORY_HEADER, MAPPER.writeValueAsBytes(history));
        } catch (Exception e) {
            log.warn("Failed to append message history", e);
        }
    }

    public static List<Map<String, String>> readHistory(Headers headers) {
        Header header = headers.lastHeader(HISTORY_HEADER);
        if (header == null) return new ArrayList<>();
        try {
            return MAPPER.readValue(header.value(), new TypeReference<>() {});
        } catch (Exception e) {
            return new ArrayList<>();
        }
    }
}

// Kafka Streams Transformer에서 각 단계마다 호출
public class OrderValidationTransformer
        implements ValueTransformerWithKey<String, OrderEvent, OrderEvent> {

    @Override
    public OrderEvent transform(String key, OrderEvent value) {
        // 처리 로직 수행
        OrderEvent validated = validateOrder(value);
        // 처리 완료 후 Message History에 이 노드 기록
        MessageHistoryUtil.appendHistory(context.headers(), "order-validation-service");
        return validated;
    }
}
```

### 1.3 Message Store

Message Store 패턴은 메시지 사본을 영구 저장소에 보존하여 감사, 재처리, 장애 분석에 활용하는 패턴입니다. 흥미롭게도 Kafka 토픽 자체가 Message Store의 가장 자연스러운 구현입니다. Kafka는 메시지를 디스크에 영구 저장하며, 보존 기간(retention.ms) 또는 압축(log compaction) 정책으로 저장 방식을 제어합니다. 소비자가 메시지를 읽어도 삭제되지 않기 때문에, 오프셋을 되감아 과거 메시지를 재처리할 수 있습니다.

이와 관련된 설정은 `14-operations-deployment.md`와 `02-fundamentals/13-retention-compaction`에서 상세히 다룹니다.

그러나 Kafka 토픽만으로는 부족한 경우가 있습니다. 금융 규제(예: 7년 보존), 크로스 시스템 쿼리(SQL로 메시지 내용을 분석해야 하는 경우), 또는 Kafka 클러스터 장애 시 메시지 복구 등의 요구사항이 있을 때 외부 Message Store가 필요합니다. 이 때 Kafka Connect의 JDBC Sink Connector를 활용하여 Kafka 메시지를 PostgreSQL이나 S3에 자동으로 미러링할 수 있습니다.

`16-event-sourcing.md`에서 다루는 Event Store 패턴은 Message Store의 특수화된 형태입니다. Event Store는 메시지를 단순히 보존하는 것에 더해, 집합체(Aggregate)의 상태를 재구성하는 데 최적화된 구조를 가집니다. 두 패턴을 혼동하지 않는 것이 중요합니다.

```json
// Kafka Connect - JDBC Sink로 PostgreSQL Message Store 구성
{
  "name": "payments-message-store",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "3",
    "topics": "payments.processed",
    "connection.url": "jdbc:postgresql://postgres:5432/message_store",
    "connection.user": "${env:DB_USER}",
    "connection.password": "${env:DB_PASS}",
    "auto.create": "true",
    "auto.evolve": "true",
    "insert.mode": "insert",
    "pk.mode": "record_key",
    "pk.fields": "payment_id",
    "fields.whitelist": "payment_id,amount,status,created_at",
    "transforms": "insertTimestamp",
    "transforms.insertTimestamp.type":
      "org.apache.kafka.connect.transforms.InsertField$Value",
    "transforms.insertTimestamp.timestamp.field": "stored_at"
  }
}
```

세 가지 보존 전략의 트레이드오프를 이해하는 것이 중요합니다. **시간 기반(time-based)** 보존(`retention.ms`)은 설정이 단순하지만 오래된 데이터가 예고 없이 사라집니다. **크기 기반(size-based)** 보존(`retention.bytes`)은 디스크 사용량을 예측 가능하게 유지하지만 트래픽 급증 시 최신 메시지가 의도치 않게 삭제될 수 있습니다. **압축(log compaction)**은 키별 최신 상태만 유지하여 컴팩트한 스냅샷을 제공하지만, 히스토리 재처리가 불가능합니다.

---

## 2. 테스트 & 디버깅 패턴

메시징 시스템의 테스트와 디버깅은 동기 시스템보다 훨씬 어렵습니다. 메시지가 여러 토픽과 컨슈머를 거쳐 비동기로 흐르기 때문에, "시스템이 살아있는가?"라는 단순한 질문에 답하는 것조차 HTTP 헬스체크만으로는 불충분합니다. EIP는 이 문제를 위한 세 가지 패턴을 제시합니다.

### 2.1 Test Message

Test Message 패턴은 시스템이 제대로 동작하는지 확인하기 위해 진단용 메시지를 주기적으로 발행하는 패턴입니다. 실제 비즈니스 이벤트가 아닌, 시스템 건강 상태를 측정하기 위한 "합성(synthetic)" 이벤트를 의도적으로 주입합니다. 프로듀서에서 테스트 메시지를 발행하고, 컨슈머가 해당 메시지를 수신한 시점을 기록하여 왕복 지연(round-trip latency)을 측정합니다. 지연이 임계값을 초과하거나 메시지가 지정된 시간 내에 수신되지 않으면 알람을 발생시킵니다.

이 접근법의 핵심 가치는 **능동적 모니터링(active/synthetic monitoring)**에 있습니다. 수동적 모니터링(passive monitoring)은 실제 비즈니스 이벤트가 발생해야만 시스템 상태를 알 수 있습니다. 밤 12시에 트래픽이 거의 없는 시간대에 Kafka 브로커가 교착 상태에 빠져도, 실제 트래픽이 없으면 감지가 늦어집니다. 반면 Test Message를 30초마다 발행하면, 트래픽이 없는 시간에도 시스템이 살아있다는 것을 지속적으로 검증할 수 있습니다.

`13-testing-strategy.md`에서 다루는 토폴로지 테스트와 통합 테스트는 코드 품질을 보장합니다. Test Message 패턴은 이와 상호 보완적으로, 프로덕션 환경의 런타임 상태를 지속적으로 검증합니다.

```java
// Test Message 프로듀서: 30초마다 heartbeat 이벤트 발행
@Component
public class HeartbeatProducer {

    private final KafkaTemplate<String, HeartbeatEvent> kafkaTemplate;
    private final MeterRegistry meterRegistry;

    @Scheduled(fixedDelay = 30_000)
    public void sendHeartbeat() {
        String heartbeatId = UUID.randomUUID().toString();
        HeartbeatEvent event = HeartbeatEvent.builder()
            .heartbeatId(heartbeatId)
            .sentAt(Instant.now())
            .source("payment-service")
            .build();

        kafkaTemplate.send("__heartbeat.payment", heartbeatId, event)
            .whenComplete((result, ex) -> {
                if (ex != null) {
                    log.error("Heartbeat send failed: {}", ex.getMessage());
                    meterRegistry.counter("heartbeat.send.failure").increment();
                } else {
                    log.debug("Heartbeat sent: {}", heartbeatId);
                }
            });
    }
}

// Test Message 컨슈머: 수신 시 왕복 지연 측정 및 알람
@Component
public class HeartbeatConsumer {

    private final MeterRegistry meterRegistry;
    private final AlertService alertService;
    private static final Duration ALERT_THRESHOLD = Duration.ofSeconds(10);

    @KafkaListener(topics = "__heartbeat.payment", groupId = "heartbeat-monitor")
    public void onHeartbeat(ConsumerRecord<String, HeartbeatEvent> record) {
        HeartbeatEvent event = record.value();
        Duration roundTrip = Duration.between(event.getSentAt(), Instant.now());

        meterRegistry.timer("heartbeat.roundtrip").record(roundTrip);
        log.info("Heartbeat received: id={} roundTrip={}ms",
            event.getHeartbeatId(), roundTrip.toMillis());

        if (roundTrip.compareTo(ALERT_THRESHOLD) > 0) {
            alertService.fire(Alert.builder()
                .severity(Severity.WARNING)
                .message("Kafka roundtrip exceeded threshold: " + roundTrip.toMillis() + "ms")
                .build());
        }
    }

    // 30초 내 heartbeat 미수신 감지 (별도 스케줄러)
    @Scheduled(fixedDelay = 35_000)
    public void checkHeartbeatTimeout() {
        // lastHeartbeatAt이 35초 이상 전이면 알람
        if (Duration.between(lastHeartbeatAt, Instant.now()).getSeconds() > 35) {
            alertService.fire(Alert.builder()
                .severity(Severity.CRITICAL)
                .message("Heartbeat timeout: no message received in 35s")
                .build());
        }
    }
}
```

### 2.2 Channel Purger

Channel Purger는 채널(토픽)에 쌓인 메시지를 운영 목적으로 제거하는 패턴입니다. 이 패턴을 "패턴"이라고 부르기 어색할 만큼 단순하지만, 잘못 사용하면 치명적인 결과를 초래하기 때문에 명확한 이해가 필요합니다.

Kafka에서 토픽 메시지를 제거하는 방법은 세 가지입니다. 첫째, 토픽 삭제 후 재생성입니다. 가장 확실하지만 컨슈머 그룹의 오프셋이 무효화됩니다. 둘째, `retention.ms=0`으로 임시 설정하는 방법입니다. Kafka가 자동으로 메시지를 삭제한 후 원래 값으로 복원합니다. 단, 삭제가 즉시 이루어지지 않고 로그 클리너 주기에 따라 지연될 수 있습니다. 셋째, `kafka-delete-records.sh`를 활용하여 특정 오프셋 이전의 메시지를 삭제하는 방법입니다. 가장 정밀하지만 파티션별 오프셋을 수동으로 지정해야 합니다.

Channel Purger를 프로덕션 환경에서 사용하는 가장 흔한 시나리오는 **Poison Pill 복구**입니다. 처리 불가능한 메시지가 특정 파티션에 걸려 해당 컨슈머가 무한 재시도에 빠진 경우, Dead Letter Queue(DLQ)로 이동시키거나 해당 오프셋을 건너뛰는 방법이 Purger보다 안전합니다. 토픽 전체를 Purge하는 것은 진짜 "핵 옵션(nuclear option)"으로, 대부분의 경우 컨슈머 측 필터링이나 DLQ 패턴으로 대체 가능합니다.

```bash
# 방법 1: kafka-delete-records로 파티션별 최고 오프셋까지 삭제
# delete-records.json 작성
cat > /tmp/delete-records.json << 'EOF'
{
  "partitions": [
    {"topic": "payments.processed", "partition": 0, "offset": -1},
    {"topic": "payments.processed", "partition": 1, "offset": -1},
    {"topic": "payments.processed", "partition": 2, "offset": -1}
  ],
  "version": 1
}
EOF

kafka-delete-records.sh \
  --bootstrap-server localhost:9092 \
  --offset-json-file /tmp/delete-records.json

# 방법 2: retention.ms 임시 0으로 설정 후 복원
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --entity-type topics \
  --entity-name payments.processed \
  --add-config retention.ms=0

# 삭제 완료 확인 후 원래 값으로 복원
sleep 60  # 로그 클리너 실행 대기
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --entity-type topics \
  --entity-name payments.processed \
  --add-config retention.ms=604800000  # 7일
```

```java
// 방법 3: AdminClient API로 프로그래밍 방식 Purge (테스트 환경 자동화)
@Component
public class ChannelPurger {

    private final AdminClient adminClient;

    public void purgeToLatest(String topicName) throws Exception {
        // 현재 최고 오프셋(최신 메시지 다음) 조회
        Map<TopicPartition, Long> endOffsets = adminClient
            .listOffsets(getTopicPartitions(topicName).stream()
                .collect(Collectors.toMap(tp -> tp,
                    tp -> OffsetSpec.latest())))
            .all().get().entrySet().stream()
            .collect(Collectors.toMap(
                Map.Entry::getKey,
                e -> e.getValue().offset()));

        // 해당 오프셋까지 삭제
        Map<TopicPartition, RecordsToDelete> recordsToDelete = endOffsets.entrySet().stream()
            .collect(Collectors.toMap(
                Map.Entry::getKey,
                e -> RecordsToDelete.beforeOffset(e.getValue())));

        adminClient.deleteRecords(recordsToDelete).all().get();
        log.info("Channel purged: topic={} partitions={}", topicName, endOffsets.size());
    }
}
```

### 2.3 Detour

Detour 패턴은 정상 처리 경로와 진단 처리 경로를 동적으로 전환하는 패턴입니다. 일반적으로 메시지는 `A → B` 경로를 따르지만, 디버깅이나 특정 조건 검사가 필요할 때 `A → (validation) → B` 경로로 임시 우회(detour)시킵니다.

Kafka에서 Detour를 구현하는 가장 실용적인 방법은 **설정 토픽(config topic)**과 결합한 동적 라우터입니다. 별도의 설정 토픽(`config.routing`)을 구독하는 컨슈머가 있고, 이 컨슈머가 라우팅 플래그를 메모리에 유지합니다. 운영자가 설정 토픽에 "detour=ON" 메시지를 발행하면, 다음 메시지부터 Detour 경로로 라우팅됩니다.

이 패턴의 대표적인 활용은 **점진적 롤아웃(gradual rollout)** 시나리오입니다. 새로운 결제 처리 로직을 배포할 때, 처음에는 전체 메시지의 1%만 새 경로로 Detour하여 검증하고, 문제가 없으면 점진적으로 비율을 늘립니다. A/B 테스트와 유사하지만, Detour는 주로 검증을 위한 임시 경로 전환이라는 점에서 다릅니다.

Detour는 반드시 빠른 롤백 메커니즘과 함께 사용해야 합니다. Detour 경로 자체에 버그가 있거나 지연이 발생하면, 설정 토픽에 "detour=OFF" 메시지를 즉시 발행하여 정상 경로로 복귀할 수 있어야 합니다.

```java
// Detour 구현: 설정 토픽으로 라우팅 동적 제어
@Component
public class DetourRouter {

    // 설정 토픽에서 실시간으로 업데이트되는 라우팅 플래그
    private volatile boolean detourEnabled = false;
    private volatile double detourRatio = 0.0; // 0.0 ~ 1.0

    @KafkaListener(topics = "config.routing", groupId = "routing-config")
    public void onConfigChange(ConsumerRecord<String, RoutingConfig> record) {
        RoutingConfig config = record.value();
        this.detourEnabled = config.isDetourEnabled();
        this.detourRatio = config.getDetourRatio();
        log.info("Routing config updated: detourEnabled={} ratio={}", detourEnabled, detourRatio);
    }

    // 메인 처리 흐름에서 호출
    public String resolveTargetTopic(String key, Object value) {
        if (!detourEnabled) {
            return "payments.processed"; // 정상 경로
        }
        // detourRatio 비율만큼만 Detour 경로로 전송
        double hash = Math.abs(key.hashCode() % 100) / 100.0;
        if (hash < detourRatio) {
            return "payments.validation-detour"; // Detour 경로
        }
        return "payments.processed";
    }
}

// Kafka Streams에서 Detour 적용
KStream<String, PaymentEvent> payments = builder.stream("payments.input");
payments.split()
    .branch(
        (key, value) -> detourRouter.isDetour(key),
        Branched.withConsumer(s -> s
            .peek((k, v) -> log.info("Detour: key={}", k))
            .mapValues(validationPipeline::validate) // 추가 검증 단계
            .to("payments.processed"))
    )
    .defaultBranch(Branched.withConsumer(s -> s.to("payments.processed")));
```

---

## 3. 제어 패턴

관측성이 "시스템을 들여다보는" 능력이라면, 제어 패턴은 "시스템에 명령을 내리는" 능력입니다. 이상적인 메시징 시스템은 재배포 없이 런타임에 동작을 변경할 수 있어야 합니다. EIP는 이를 위한 두 가지 제어 패턴을 제시합니다.

### 3.1 Control Bus

Control Bus 패턴은 메시지 데이터가 흐르는 데이터 채널과 분리된, 시스템 제어를 위한 전용 채널입니다. 운영자는 Control Bus를 통해 메시징 시스템의 동작을 런타임에 변경할 수 있습니다. 비유하자면, 도로(데이터 채널)와 교통 신호 시스템(Control Bus)을 분리하는 것과 같습니다.

Kafka는 내장 Control Bus를 이미 가지고 있습니다. `__consumer_offsets` 토픽은 컨슈머 그룹의 오프셋 커밋을 저장하여 컨슈머를 제어합니다. `__transaction_state` 토픽은 트랜잭션 코디네이터가 분산 트랜잭션 상태를 관리하는 데 사용합니다. 이들은 Kafka 인프라 레벨의 내장 Control Bus입니다.

애플리케이션 레벨에서는 `config.*` 패턴의 토픽을 Control Bus로 활용합니다. 각 마이크로서비스가 `config.{service-name}` 토픽을 구독하고, 운영자가 런타임 설정 변경을 이 토픽에 발행합니다. 재배포 없이 처리 스레드 수, 배치 크기, 타임아웃 등을 동적으로 조정할 수 있습니다.

제어의 세 가지 수준을 구분하는 것이 중요합니다. **인프라 수준**은 Kafka 브로커가 내부적으로 관리하며 애플리케이션이 직접 개입하지 않습니다. **플랫폼 수준**은 AdminClient API로 컨슈머 그룹 재조정, 파티션 재할당 등을 수행합니다. **애플리케이션 수준**은 비즈니스 설정(배치 크기, 임계값, 기능 플래그)을 런타임에 변경합니다. Control Bus 패턴은 주로 플랫폼과 애플리케이션 수준에서 사용합니다.

```java
// Control Bus: 런타임 설정 변경을 config 토픽으로 수신
@Component
public class ApplicationControlBus {

    // Control Bus가 제어하는 런타임 파라미터
    private volatile int concurrency = 3;
    private volatile int batchSize = 100;
    private volatile boolean featureXEnabled = false;

    @KafkaListener(topics = "config.payment-service", groupId = "control-bus")
    public void onControlMessage(ConsumerRecord<String, ControlCommand> record) {
        ControlCommand cmd = record.value();
        switch (cmd.getType()) {
            case "SET_CONCURRENCY":
                int newConcurrency = cmd.getIntParam("value");
                log.info("Control Bus: changing concurrency {} -> {}", concurrency, newConcurrency);
                this.concurrency = newConcurrency;
                // 실제로 KafkaListenerEndpointRegistry로 concurrency 조정 가능
                adjustListenerConcurrency(newConcurrency);
                break;
            case "SET_BATCH_SIZE":
                this.batchSize = cmd.getIntParam("value");
                log.info("Control Bus: batch size changed to {}", batchSize);
                break;
            case "TOGGLE_FEATURE":
                this.featureXEnabled = cmd.getBoolParam("enabled");
                log.info("Control Bus: feature X {}", featureXEnabled ? "enabled" : "disabled");
                break;
            default:
                log.warn("Unknown control command type: {}", cmd.getType());
        }
    }

    private void adjustListenerConcurrency(int newConcurrency) {
        KafkaListenerEndpointRegistry registry = applicationContext
            .getBean(KafkaListenerEndpointRegistry.class);
        MessageListenerContainer container = registry.getListenerContainer("paymentListener");
        if (container instanceof ConcurrentMessageListenerContainer) {
            ((ConcurrentMessageListenerContainer<?, ?>) container).setConcurrency(newConcurrency);
        }
    }
}

// Control Bus로 명령 전송 (운영자 API 또는 관리 도구)
@RestController
@RequestMapping("/admin/control")
public class ControlBusController {

    private final KafkaTemplate<String, ControlCommand> kafkaTemplate;

    @PostMapping("/concurrency")
    public ResponseEntity<Void> setConcurrency(@RequestParam int value) {
        ControlCommand cmd = ControlCommand.builder()
            .type("SET_CONCURRENCY")
            .param("value", value)
            .issuedAt(Instant.now())
            .issuedBy(SecurityContextHolder.getContext().getAuthentication().getName())
            .build();
        kafkaTemplate.send("config.payment-service", "control", cmd);
        return ResponseEntity.accepted().build();
    }
}
```

### 3.2 Smart Proxy

Smart Proxy 패턴은 Request-Reply 시나리오에서 요청자가 직접 응답 채널을 관리하지 않아도 되도록, 프록시가 응답 라우팅을 자동으로 처리하는 패턴입니다. "Smart"라는 이름이 붙은 이유는 프록시가 응답을 보낼 주소(return address)를 기억하고 알아서 라우팅하기 때문입니다.

Spring Kafka의 `ReplyingKafkaTemplate`이 Smart Proxy의 완벽한 구현 예시입니다. 클라이언트는 요청 토픽에 메시지를 보내고 `sendAndReceive()`를 호출합니다. 내부적으로 `ReplyingKafkaTemplate`은 고유한 `correlationId`를 생성하고, 메시지 헤더에 `reply-topic`과 `correlation-id`를 자동으로 추가합니다. 서버 측 컨슈머는 헤더를 읽어 응답을 올바른 reply 토픽으로 전송합니다. `ReplyingKafkaTemplate`은 `correlationId`로 응답을 매핑하여 정확한 요청자에게 반환합니다. 이 모든 과정이 클라이언트 코드에서는 단순한 동기 호출처럼 보입니다.

Smart Proxy가 특히 중요한 상황은 **다단계 Request-Reply 체인**입니다. 게이트웨이가 여러 마이크로서비스에 요청을 보내고 응답을 집계해야 할 때, 각 서비스의 응답이 게이트웨이로 정확히 돌아오도록 Smart Proxy가 라우팅을 관리합니다. 관련 구현 상세는 `03-spring-boot-integration`의 ReplyingKafkaTemplate 챕터에서 다룹니다.

```java
// Smart Proxy 내부 동작 이해: ReplyingKafkaTemplate이 하는 일
@Service
public class PaymentRequestService {

    private final ReplyingKafkaTemplate<String, PaymentRequest, PaymentResponse> replyingTemplate;

    // 클라이언트 코드: 단순한 request-reply처럼 보임
    public PaymentResponse processPayment(PaymentRequest request) throws Exception {
        ProducerRecord<String, PaymentRequest> record =
            new ProducerRecord<>("payments.requests", request.getPaymentId(), request);

        // ReplyingKafkaTemplate이 자동으로:
        // 1. correlationId 생성 → 헤더에 추가
        // 2. replyTopic(예: payments.replies) → 헤더에 추가
        // 3. 응답 대기 (내부적으로 ConcurrentHashMap<correlationId, CompletableFuture>)
        RequestReplyFuture<String, PaymentRequest, PaymentResponse> future =
            replyingTemplate.sendAndReceive(record, Duration.ofSeconds(10));

        // 블로킹 대기 (또는 비동기 처리)
        ConsumerRecord<String, PaymentResponse> response = future.get(10, TimeUnit.SECONDS);
        return response.value();
    }
}

// 서버 측: Smart Proxy가 설정한 헤더를 읽어 응답 라우팅
@Component
public class PaymentRequestHandler {

    private final KafkaTemplate<String, PaymentResponse> kafkaTemplate;

    @KafkaListener(topics = "payments.requests", groupId = "payment-processor")
    @SendTo  // 응답을 요청 헤더의 replyTopic으로 자동 전송
    public PaymentResponse handleRequest(PaymentRequest request) {
        // @SendTo가 Smart Proxy 역할: 헤더에서 reply-topic을 읽어 응답 전송
        PaymentResponse response = processPayment(request);
        return response; // ReplyingKafkaTemplate의 @SendTo가 자동으로 reply-topic으로 라우팅
    }
}
```

Smart Proxy를 수동으로 구현할 때(ReplyingKafkaTemplate 없이)의 복잡성을 이해하면 이 패턴의 가치가 더욱 명확해집니다. 직접 구현하려면 correlationId 생성, 응답 대기 맵 관리, 타임아웃 처리, 컨슈머 그룹별 reply 토픽 관리 등을 모두 직접 처리해야 합니다. Smart Proxy가 이 복잡성을 추상화해 줍니다.

---

## 4. 패턴 선택 가이드

8개의 Systems Management 패턴을 모두 이해했다면, 실제 운영 상황에서 어떤 패턴을 선택해야 할지 판단하는 기준이 필요합니다.

### 문제 상황별 패턴 매핑

| 운영 문제 | 적합한 패턴 | 이유 |
|-----------|-------------|------|
| 메시지 흐름을 방해하지 않고 감사해야 한다 | Wire Tap | 주 흐름 무영향, 비동기 감사 |
| 메시지가 어느 단계에서 실패했는지 추적해야 한다 | Message History | 처리 경로를 메시지 자체에 누적 |
| 규제 요건으로 7년간 메시지를 보존해야 한다 | Message Store (외부 DB) | Kafka 보존 기간 초과, SQL 조회 필요 |
| 시스템이 살아있는지 항상 확인해야 한다 | Test Message | 트래픽 없는 시간대에도 능동적 검증 |
| 테스트 환경의 오염된 토픽을 초기화해야 한다 | Channel Purger | 테스트 환경 리셋, 프로덕션 위험 주의 |
| Poison Pill로 컨슈머가 무한 재시도에 빠졌다 | Channel Purger (surgical) | `delete-records`로 해당 오프셋만 제거 |
| 새 처리 로직을 일부 메시지에만 먼저 적용해보고 싶다 | Detour | 동적 비율 라우팅으로 점진적 검증 |
| 재배포 없이 컨슈머 처리 스레드 수를 늘려야 한다 | Control Bus | config 토픽으로 런타임 파라미터 변경 |
| Kafka Request-Reply를 구현해야 한다 | Smart Proxy (ReplyingKafkaTemplate) | correlationId/replyTopic 자동 관리 |

### 관측성 성숙도 모델

메시징 시스템의 관측성 성숙도는 점진적으로 구축됩니다. 모든 패턴을 한 번에 도입하려 하면 오히려 운영 부담이 증가합니다. 조직의 현재 수준을 진단하고 다음 단계로 진화하는 접근이 현실적입니다.

**Level 1: 로깅만 존재** — 가장 기본적인 상태입니다. 각 서비스가 개별적으로 로그를 남기지만, 메시지 흐름 전체를 추적하는 도구가 없습니다. 장애 발생 시 여러 서비스의 로그를 수동으로 대조해야 합니다. 대부분의 초기 EDA 도입 조직이 여기에 해당합니다. 이 단계에서는 로그 집계 도구(ELK, Loki)를 먼저 갖추는 것이 우선입니다.

**Level 2: Wire Tap + Message Store** — 기본 관측성을 갖춘 단계입니다. Wire Tap으로 주요 토픽의 메시지를 감사 토픽에 복사하고, Message Store(Kafka 보존 정책 또는 외부 DB)로 히스토리를 유지합니다. 이제 과거 메시지를 재처리하거나 감사 기록을 조회할 수 있습니다. 메시지 흐름 전체를 "들여다볼 수 있는" 첫 번째 수준입니다.

**Level 3: Message History + Test Message** — 능동적 모니터링을 갖춘 단계입니다. Message History로 개별 메시지의 여정을 추적하고, Test Message로 트래픽이 없어도 시스템 건강 상태를 지속 검증합니다. 장애가 발생하기 전에 감지하는 능력이 생깁니다. 알람 임계값과 온콜 체계가 갖춰져야 이 단계를 온전히 활용할 수 있습니다.

**Level 4: Control Bus + Detour + Smart Proxy** — 완전한 운영 제어를 갖춘 단계입니다. Control Bus로 재배포 없이 런타임 파라미터를 변경하고, Detour로 새 기능을 점진적으로 검증하며, Smart Proxy로 복잡한 Request-Reply 패턴을 안전하게 처리합니다. 이 단계에 도달한 팀은 운영 중단 없이 시스템을 진화시킬 수 있습니다. 그러나 이 수준의 동적 제어는 팀의 운영 경험과 자동화 인프라가 성숙해야 안전하게 활용할 수 있습니다.

성숙도 레벨은 반드시 순서대로 올라가야 합니다. Level 1에서 곧바로 Level 4를 도입하면, Control Bus를 통한 잘못된 명령이 전파되어도 감지할 관측 도구가 없는 상황이 됩니다. 관측성(Levels 2-3)이 제어(Level 4)보다 먼저 갖춰져야 합니다.

---

## 참고 자료

- **Gregor Hohpe, Bobby Woolf** — "Enterprise Integration Patterns" (Addison-Wesley, 2003): Wire Tap(Chapter 12), Message History(Chapter 13), Message Store(Chapter 12), Test Message(Chapter 12), Channel Purger(Chapter 6), Detour(Chapter 12), Control Bus(Chapter 12), Smart Proxy(Chapter 9) 패턴 원전
- **Confluent Documentation** — "Event Streaming Patterns - Systems Management": EIP 패턴을 Kafka 생태계로 매핑한 공식 문서 (https://developer.confluent.io/patterns/)
- **Kafka AdminClient API** — Channel Purger 구현에 필요한 `deleteRecords()`, `deleteConsumerGroups()` 등의 프로그래밍 인터페이스 (https://kafka.apache.org/documentation/#adminapi)
- **OpenTelemetry for Kafka** — Message History 패턴과 분산 추적의 상호 보완 관계, Kafka 컨텍스트 전파 구현 (https://opentelemetry.io/docs/instrumentation/java/manual/)
- **Spring Kafka ReplyingKafkaTemplate** — Smart Proxy 패턴의 Spring 구현체, 설정 및 고급 사용법 (https://docs.spring.io/spring-kafka/reference/kafka/request-reply.html)
- `13-testing-strategy.md` — Test Message 패턴과 상호 보완하는 코드 품질 테스트 전략
- `16-event-sourcing.md` — Message Store 패턴의 특수화된 형태인 Event Store 패턴
- `17-messaging-patterns.md` — EIP의 메시지 변환/라우팅 패턴 (이 문서와 함께 EIP 전체를 구성)
