# 05. 에러 처리 및 특수 케이스 대응

Redpanda 환경에서의 에러 유형 분류, DLQ 고급 패턴, Redpanda Connect 에러 처리, 특수 케이스 대응 전략

> DLQ/DLT 전략의 기초(재시도 설정, DefaultErrorHandler, DLT 라우팅)는 [03/06-dlq-strategy.md](../03-spring-boot-integration/06-dlq-strategy.md) 참조. 이 문서는 **고급 에러 처리 패턴과 DLT 재처리 자동화**에 집중한다.

## 구성:

### 1. 에러 유형 분류 (심화)

#### Non-Transient Errors (Poison Pills)
```
특징: 결정론적 실패, 재시도해도 항상 실패
원인:
├── 역직렬화 오류 (잘못된 JSON, Avro 스키마 불일치)
├── 필수 필드 누락 / null 값
├── 비즈니스 검증 실패 (음수 금액, 존재하지 않는 상품 ID)
├── 메시지 크기 초과 (max.message.bytes)
└── Consumer 코드 버그 (NullPointerException 등)

대응: 즉시 DLT로 이동, 재시도 낭비 방지
```

#### Transient Errors
```
특징: 비결정론적, 시간이 지나면 자가 치유
원인:
├── 일시적 네트워크 단절
├── 다운스트림 서비스 일시 불가 (503)
├── 타임아웃 (서비스 과부하)
├── DB 커넥션 풀 고갈
└── Rate Limiting (429 Too Many Requests)

대응: 재시도 + Exponential Backoff → 재시도 소진 후 DLT
```

#### 특수 케이스
```
├── Rebalancing 중 메시지 유실
│   → session.timeout.ms, max.poll.interval.ms 조정
├── Offset Commit 실패
│   → enable.auto.commit=false, 수동 커밋
├── 순서 보장 실패 (재시도 시)
│   → max.in.flight.requests.per.connection=1
├── 스키마 진화 실패
│   → Schema Registry 호환성 모드 설정
└── Backpressure (Consumer가 Producer 속도를 못따라감)
    → Consumer 인스턴스 추가, 파티션 수 증가
```

### 2. Redpanda Connect 에러 처리 패턴

Redpanda Connect(구 Benthos)는 YAML 기반 스트리밍 파이프라인 도구로, 자체적인 에러 처리 메커니즘을 제공합니다.

#### try 프로세서 - 순차 실행, 실패 시 건너뜀
```yaml
pipeline:
  processors:
    - try:
        - mapping: |
            root = this
            root.validated = true
        - http:
            url: http://enrichment-service/api/enrich
            verb: POST
        - mapping: |
            root.enriched = true
```
설명: processor가 실패하면 해당 메시지는 남은 프로세서를 건너뜁니다. 의존 관계가 있는 프로세서 체인에서 유용합니다.

#### catch 프로세서 - 실패한 메시지 복구
```yaml
pipeline:
  processors:
    - mapping: |
        root = this.parse_json()
    - catch:
        - log:
            level: ERROR
            message: "파싱 실패: ${! error() }"
        - mapping: |
            root = {"error": error(), "raw": content()}
```
설명: catch 블록은 에러가 발생한 메시지만 처리하며, 처리 후 에러 플래그를 제거합니다.

#### switch로 에러 유형별 라우팅
```yaml
output:
  switch:
    cases:
      - check: 'errored() && error().contains("schema")'
        output:
          redpanda_common:
            topic: schema-errors.DLT
      - check: 'errored() && error().contains("timeout")'
        output:
          retry:
            max_retries: 5
            output:
              redpanda_common:
                topic: original-topic
      - check: errored()
        output:
          redpanda_common:
            topic: general-errors.DLT
      - output:
          redpanda_common:
            topic: processed-output
```
설명: error() 함수로 에러 메시지를 검사하여 스키마 에러, 타임아웃, 기타 에러를 각각 다른 토픽으로 라우팅합니다.

#### fallback 출력 - DLQ 패턴
```yaml
output:
  fallback:
    - redpanda_common:
        topic: orders-processed
    - retry:
        output:
          redpanda_common:
            topic: orders.DLT
```
설명: 주 출력(orders-processed)에 실패하면 DLT(orders.DLT)로 전송합니다. retry로 감싸면 DLT 전송도 재시도합니다.

#### reject_errored + 메타데이터 추가
```yaml
output:
  fallback:
    - reject_errored:
        redpanda_common:
          topic: orders-processed
    - processors:
        - mapping: |
            meta error_message = error()
            meta error_timestamp = now()
            meta original_topic = meta("kafka_topic")
      redpanda_common:
        topic: orders.DLT
```
설명: 에러가 없는 메시지만 주 출력으로 보내고, 에러 메시지는 메타데이터(에러 내용, 시간, 원본 토픽)를 추가한 후 DLT로 보냅니다.

### 3. DLQ 고급 전략

#### 토픽별 DLT vs 공통 DLT
```
토픽별 DLT:
orders → orders.DLT
payments → payments.DLT

장점: 도메인별 분리, 독립적 재처리
단점: 토픽 수 증가, 관리 부담

공통 DLT:
모든 실패 → application.DLT

장점: 관리 단순, 모니터링 집중
단점: 재처리 시 원본 토픽 식별 필요
```
권장: 토픽별 DLT (원본 토픽 자동 식별, 재처리 단순화)

#### DLQ에 넣으면 안 되는 경우
```
❌ Backpressure 처리 목적
   → Consumer 스케일 아웃이 정답
❌ 연결 실패 (DB 다운, 서비스 불가)
   → 연결 문제를 해결해야 함, DLQ에 넣어도 다음 메시지도 같은 실패
❌ 전체 Consumer 장애
   → Kafka의 offset 기반 재소비가 더 적합
```

#### Schema Registry로 DLQ 감소
```
Schema Registry를 사용하면:
├── Producer 단에서 스키마 검증
├── 잘못된 메시지가 토픽에 들어가는 것 자체를 방지
├── Consumer의 역직렬화 실패 대폭 감소
└── Poison Pill 예방의 가장 효과적 방법
```

### 4. Spring Kafka DLQ 고급 패턴

#### Non-Blocking 재시도 + DLT 통합
```java
@RetryableTopic(
    attempts = "4",
    backoff = @Backoff(delay = 1000, multiplier = 2, maxDelay = 10000),
    dltTopicSuffix = ".DLT",
    retryTopicSuffix = ".retry",
    autoCreateTopics = "true",
    include = {RetryableException.class, TimeoutException.class},
    exclude = {DeserializationException.class, ValidationException.class}
)
@KafkaListener(topics = "orders", groupId = "order-service")
public void consume(OrderEvent event) {
    processOrder(event);
}

@DltHandler
public void handleDlt(OrderEvent event,
                      @Header(KafkaHeaders.RECEIVED_TOPIC) String topic,
                      @Header(KafkaHeaders.EXCEPTION_MESSAGE) String errorMessage,
                      @Header(KafkaHeaders.ORIGINAL_TOPIC) String originalTopic) {
    log.error("DLT: topic={}, orderId={}, error={}", topic, event.orderId(), errorMessage);
    dltRepository.save(DltMessage.from(event, errorMessage, originalTopic));
    alertService.notifyOps(event, errorMessage);
}
```

생성되는 토픽:
```
orders              (원본)
orders.retry-0      (1초 후 재시도)
orders.retry-1      (2초 후 재시도)
orders.retry-2      (4초 후 재시도)
orders.DLT          (최종 실패)
```

#### 커스텀 에러 분류기
```java
@Bean
public DefaultErrorHandler errorHandler(KafkaTemplate<String, Object> kafkaTemplate) {
    DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(kafkaTemplate,
        (record, ex) -> {
            if (ex.getCause() instanceof ValidationException) {
                return new TopicPartition(record.topic() + ".validation.DLT", -1);
            } else if (ex.getCause() instanceof ExternalServiceException) {
                return new TopicPartition(record.topic() + ".external.DLT", -1);
            }
            return new TopicPartition(record.topic() + ".DLT", -1);
        });

    ExponentialBackOffWithMaxRetries backOff = new ExponentialBackOffWithMaxRetries(4);
    backOff.setInitialInterval(1000L);
    backOff.setMultiplier(2.0);
    backOff.setMaxInterval(10000L);

    DefaultErrorHandler handler = new DefaultErrorHandler(recoverer, backOff);
    handler.addNotRetryableExceptions(
        DeserializationException.class,
        MessageConversionException.class,
        ValidationException.class
    );
    return handler;
}
```

### 5. 특수 케이스 대응

#### Rebalancing 중 메시지 중복/유실 방지
```yaml
spring:
  kafka:
    consumer:
      properties:
        session.timeout.ms: 30000
        max.poll.interval.ms: 300000
        max.poll.records: 100
    listener:
      ack-mode: MANUAL_IMMEDIATE
```
설명: max.poll.interval.ms를 넉넉하게 설정하여 처리 시간이 긴 메시지에서 리밸런싱이 발생하지 않도록 합니다. 수동 ACK으로 처리 완료 후에만 오프셋을 커밋합니다.

#### 순서 보장 + 재시도
```yaml
spring:
  kafka:
    producer:
      properties:
        max.in.flight.requests.per.connection: 1
        enable.idempotence: true
        retries: 3
```
설명: max.in.flight.requests.per.connection=1이면 한 번에 하나의 요청만 전송하므로 재시도 시에도 순서가 보장됩니다. 단, 처리량이 감소합니다.

#### Consumer 과부하 (Backpressure)
```
감지:
- Consumer Lag 증가 (rpk group describe)
- max.poll.interval.ms 초과 경고

대응 순서:
1. Consumer 인스턴스 추가 (파티션 수 이내)
2. 파티션 수 증가 (rpk topic alter-config)
3. 배치 크기 최적화 (max.poll.records)
4. Consumer 처리 로직 비동기화
5. 워크로드 분리 (무거운 처리를 별도 스레드풀로)
```

#### Offset Reset 사고 복구
```bash
# 특정 시점으로 오프셋 되돌리기
docker exec -it redpanda rpk group seek order-consumers \
  --to-timestamp 1704067200000 --topics orders

# 맨 처음부터 다시 처리
docker exec -it redpanda rpk group seek order-consumers \
  --to start --topics orders

# 최신으로 건너뛰기 (이미 처리된 것으로 간주)
docker exec -it redpanda rpk group seek order-consumers \
  --to end --topics orders
```

### 6. DLT 재처리 자동화

#### 스케줄러 기반 자동 재처리
```java
@Component
@RequiredArgsConstructor
public class DltReprocessScheduler {
    private final DltRepository dltRepository;
    private final KafkaTemplate<String, byte[]> kafkaTemplate;

    @Scheduled(fixedDelay = 300000)  // 5분마다
    public void reprocessPendingMessages() {
        List<DltMessage> messages = dltRepository
            .findByStatusAndRetryCountLessThan(DltStatus.PENDING, 3);

        for (DltMessage msg : messages) {
            try {
                kafkaTemplate.send(msg.getOriginalTopic(), msg.getKey(), msg.getValue()).get();
                msg.setStatus(DltStatus.REPROCESSED);
            } catch (Exception e) {
                msg.setRetryCount(msg.getRetryCount() + 1);
                if (msg.getRetryCount() >= 3) {
                    msg.setStatus(DltStatus.PERMANENTLY_FAILED);
                }
            }
            dltRepository.save(msg);
        }
    }
}
```

### 7. 운영 체크리스트
```
에러 처리 설계 시:
□ 에러 유형별 분류 (Transient vs Non-Transient)
□ Non-Transient → 즉시 DLT
□ Transient → Exponential Backoff 후 DLT
□ DLT 메시지에 메타데이터 추가 (원본 토픽, 에러 내용, 타임스탬프)
□ DLT 모니터링 알림 설정 (5분 내 N개 초과 시)
□ DLT 재처리 API 또는 스케줄러 구현
□ Schema Registry로 Poison Pill 예방
□ Consumer Lag 모니터링 설정
□ Rebalancing 안정화 설정 (timeout, poll 간격)
```

### 8. 참고 자료
- [Redpanda DLQ 가이드](https://www.redpanda.com/blog/reliable-message-processing-with-dead-letter-queue)
- [Redpanda Connect Error Handling](https://docs.redpanda.com/redpanda-connect/configuration/error_handling/)
- [Redpanda Connect Retry Output](https://docs.redpanda.com/redpanda-connect/components/outputs/retry/)
- [Spring Kafka Error Handling](https://docs.spring.io/spring-kafka/reference/#annotation-error-handling)
