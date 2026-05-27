# 21. Outbox Pattern + Retry Topic 자가 치유 아키텍처

컬리 3PL팀의 Transactional Outbox 패턴과 @RetryableTopic 조합 사례 분석

---

> 출처: [컬리 3PL팀의 Outbox Pattern과 Retry Topic](https://helloworld.kurly.com/blog/2026-outbox-pattern-and-retry-topic/)

> **사전 지식**: [07-transaction-patterns.md](./07-transaction-patterns.md), [05-dlq-strategy.md](./05-dlq-strategy.md) 참조

## 1. 배경과 요구사항

컬리 3PL(Third-Party Logistics) 서비스는 외부 채널(파트너사)로부터 입고예정 데이터를 수신하여 내부 시스템에 동기화한다. 이 과정에서 두 가지 근본적인 신뢰성 문제가 존재한다.

1. **발행 원자성**: DB 저장은 성공했지만 Kafka 발행이 실패하면 데이터 불일치 발생
2. **수신 일시 장애**: 파트너 정보 미등록 등 일시적 사유로 Consumer 처리가 실패하면 수동 개입 필요

목표는 이 두 실패 지점을 **자동으로 복구**하여 운영자 개입을 최소화하는 것이다.

---

## 2. 두 가지 실패 지점

### 2.1 발행 단계 (Producer) — 원자성 문제

```java
@Transactional
void process(Request request) {
    interfaceDB.save(request);      // ← DB 저장 성공
    kafkaProducer.send(message);    // ← Kafka 발행 실패!
    // 트랜잭션 커밋 → DB에는 있지만 이벤트는 발행 안 됨
}
```

DB와 Kafka는 서로 다른 트랜잭션 시스템이다. `@Transactional`은 DB 트랜잭션만 관리하므로, Kafka 발행 실패 시 DB는 이미 커밋된 상태로 남는다. 반대로 Kafka 발행 후 DB 커밋이 실패하면 이벤트는 발행됐지만 DB에는 데이터가 없는 역전 상태가 된다.

### 2.2 수신 단계 (Consumer) — 의존성 문제

- 파트너 정보가 아직 미등록 → 처리 실패
- 외부 API 일시 장애 → 타임아웃
- 일시적 실패지만 기본 Consumer에는 자동 재시도 메커니즘이 없음 → 수동 개입 필요

이 두 문제를 동시에 해결하기 위해 **Outbox 패턴**(발행 원자성)과 **@RetryableTopic**(수신 재시도)을 조합했다.

---

## 3. Outbox 패턴 이론

Transactional Outbox 패턴의 핵심 아이디어는 단순하다:

1. 비즈니스 데이터와 **발행할 메시지를 같은 DB 트랜잭션**에 저장
2. 별도 프로세스(폴러)가 Outbox 테이블을 주기적으로 조회하여 Kafka에 발행
3. 발행 성공 시 완료 마킹

DB 트랜잭션이 비즈니스 데이터와 메시지의 원자성을 보장하므로, "DB에는 있지만 이벤트는 없는" 불일치가 구조적으로 불가능해진다.

```
[비즈니스 로직]
    ├─ interfaceDB.save()     ┐ 같은 DB 트랜잭션
    └─ outboxRecord.save()    ┘ → 원자성 보장
            ↓
[Outbox Poller] → outbox_record 테이블 폴링 (2초마다)
            ↓
[Kafka Producer] → 토픽에 발행
            ↓
[완료 마킹] → status = COMPLETED
```

폴링 방식은 CDC(Change Data Capture) 방식보다 인프라 요구사항이 낮다. DB의 WAL/binlog 접근 권한이 필요 없고, 별도의 Debezium 같은 외부 프로세스도 필요 없다. 대신 폴링 간격만큼의 지연과 DB 부하가 트레이드오프다.

---

## 4. Namastack Outbox 라이브러리 상세

**Namastack Outbox**는 Spring Boot용 Transactional Outbox 구현 라이브러리로, 폴링 기반으로 동작한다. 별도 인프라 없이 애플리케이션 내장형으로 동작하며, 멀티 인스턴스 환경을 기본 지원한다.

### 4.1 테이블 구조 + 인덱스

**outbox_record 테이블:**

```sql
CREATE TABLE outbox_record (
    id VARCHAR(255) PRIMARY KEY,
    status VARCHAR(20) NOT NULL,          -- PENDING / PROCESSING / COMPLETED / FAILED
    aggregate_id VARCHAR(255) NOT NULL,   -- 비즈니스 엔티티 ID (Kafka 키로 사용)
    event_type VARCHAR(255) NOT NULL,     -- 이벤트 타입 (라우팅에 사용)
    payload TEXT NOT NULL,                -- JSON 직렬화된 메시지
    created_at DATETIME(6) NOT NULL,
    completed_at DATETIME(6) NULL,
    retry_count INT NOT NULL DEFAULT 0,   -- 현재 재시도 횟수
    next_retry_at DATETIME(6) NOT NULL,   -- 다음 재시도 예정 시간
    partition_no INT NOT NULL             -- 멀티 인스턴스 파티션 분배용
);

-- 성능 최적화 인덱스
CREATE INDEX idx_outbox_record_partition_status_retry
    ON outbox_record (partition_no, status, next_retry_at);
CREATE INDEX idx_outbox_record_status_retry
    ON outbox_record (status, next_retry_at);
```

첫 번째 인덱스(`partition_no, status, next_retry_at`)는 폴러의 핵심 쿼리를 커버한다. 각 인스턴스는 자신의 `partition_no`에 해당하는 `PENDING`/`FAILED` 상태 레코드만 조회하므로, 이 복합 인덱스가 풀 테이블 스캔을 방지한다.

**outbox_instance 테이블:**

```sql
CREATE TABLE outbox_instance (
    instance_id VARCHAR(255) PRIMARY KEY,
    hostname VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    started_at DATETIME(6) NOT NULL,
    last_heartbeat DATETIME(6) NOT NULL,  -- 30초 무응답 → 비정상 감지
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL
);

CREATE INDEX idx_outbox_instance_status_heartbeat
    ON outbox_instance (status, last_heartbeat);
```

### 4.2 YAML 설정 전문

```yaml
outbox:
  poll-interval: 2000                          # 폴링 주기 (ms) — 2초마다 outbox_record 조회
  batch-size: 10                               # 한 번에 처리할 최대 aggregate ID 수

  processing:
    publish-after-save: true                   # 저장 직후 리스너에 즉시 알림 (지연 최소화)
    stop-on-first-failure: true                # 첫 실패 시 나머지 이벤트 중단 (순서 보장)
    delete-completed-records: false            # 완료 레코드 삭제 안 함 (감사 추적용)
    executor-core-pool-size: 4                 # 기본 스레드 풀 크기
    executor-max-pool-size: 8                  # 최대 스레드 풀 크기

  instance:
    heartbeat-interval-seconds: 5              # 하트비트 전송 주기
    stale-instance-timeout-seconds: 30         # 이 시간 동안 하트비트 없으면 비정상 판정
    new-instance-detection-interval-seconds: 10 # 새 인스턴스 감지 주기
    graceful-shutdown-timeout-seconds: 15       # 종료 시 드레인 대기 시간

  retry:
    max-retries: 3                             # 최대 재시도 횟수
    policy: "exponential"                      # 재시도 정책 (exponential/linear/fixed)
    exponential:
      initial-delay: 2000                      # 첫 재시도 대기 (ms)
      max-delay: 60000                         # 최대 대기 (ms) — 1분 캡
      multiplier: 2.0                          # 대기 시간 배수
```

각 설정의 의미를 짚어보면:

- **`publish-after-save: true`**: DB 트랜잭션 커밋 직후 폴러에게 즉시 알림을 보낸다. `false`이면 다음 폴링 주기(2초)까지 대기한다. 지연에 민감한 서비스라면 `true`가 적합하다.
- **`stop-on-first-failure: true`**: 같은 aggregate 내 이벤트 순서가 중요할 때 사용한다. 첫 이벤트 발행이 실패하면 후속 이벤트도 중단하여 순서 역전을 방지한다.
- **`delete-completed-records: false`**: 완료된 레코드를 삭제하지 않고 보존한다. 감사(audit) 추적이나 디버깅에 유용하지만, 테이블 크기가 지속 증가하므로 별도 배치로 보존 기간 후 삭제해야 한다.
- **Exponential backoff**: 첫 재시도 2초 → 4초 → 8초 → ... → 최대 60초. max-retries(3)를 초과하면 `FAILED` 상태로 전환된다.

### 4.3 JPA 의존성과 MyBatis 환경 대응

Namastack Outbox는 두 가지 persistence 모듈을 제공한다.

| 모듈 | 의존성 | 스키마 관리 | 적합 환경 |
|------|--------|-----------|----------|
| `namastack-outbox-starter-jpa` | Spring Data JPA + Hibernate | Flyway/Liquibase 수동 관리 필요 | JPA 기반 프로젝트 |
| `namastack-outbox-starter-jdbc` | Spring JDBC (Hibernate 불필요) | 애플리케이션 시작 시 자동 생성 | MyBatis, JdbcTemplate, jOOQ 등 |

**MyBatis 프로젝트라면 `starter-jdbc`를 사용하면 된다.** 이 모듈은 Hibernate/JPA 의존성 없이 순수 JDBC로 동작하므로, MyBatis의 `SqlSession`과 같은 DB 트랜잭션 컨텍스트 안에서 outbox 레코드를 저장할 수 있다. 핵심은 Outbox 라이브러리가 사용하는 `DataSource`와 비즈니스 로직이 사용하는 `DataSource`가 동일해야 한다는 점이다. 같은 `DataSource`를 공유하면 Spring의 `@Transactional`이 하나의 DB 트랜잭션으로 묶어준다.

```xml
<!-- Maven: MyBatis 프로젝트용 -->
<dependency>
    <groupId>io.namastack</groupId>
    <artifactId>namastack-outbox-starter-jdbc</artifactId>
</dependency>
<!-- JPA/Hibernate 의존성 불필요 -->
```

JDBC 모듈의 자동 스키마 생성은 H2, MySQL/MariaDB, PostgreSQL, SQL Server를 지원한다. 프로덕션에서는 자동 생성을 끄고 Flyway/Liquibase로 관리하는 것이 권장된다.

**Namastack 외 대안 — Gruelbox TransactionOutbox:**

Namastack이 Spring Boot에 특화되어 있다면, [Gruelbox TransactionOutbox](https://github.com/gruelbox/transaction-outbox)는 더 범용적인 선택지다. 이 라이브러리는 JDBC 레벨에서 직접 동작하며 특정 ORM에 의존하지 않는다. Spring, Guice, jOOQ 등 다양한 DI/트랜잭션 프레임워크를 지원하고, MyBatis와도 `TransactionManager.fromDataSource()`를 통해 통합할 수 있다. 단, 멀티 인스턴스 파티션 분산은 직접 구현해야 한다는 점에서 Namastack보다 설정 부담이 크다.

**직접 구현 — MyBatis Mapper 활용:**

라이브러리 도입이 부담스럽다면 MyBatis Mapper로 직접 구현하는 것도 가능하다. outbox_record 테이블에 대한 INSERT/SELECT/UPDATE Mapper를 작성하고, `@Scheduled`로 폴러를 구현하면 된다. 이 방식은 라이브러리 의존성이 없고 기존 MyBatis 인프라를 그대로 활용하지만, 멀티 인스턴스 중복 처리 방지, 재시도 정책, 하트비트 같은 기능을 직접 구현해야 한다.

```java
// MyBatis Mapper 직접 구현 예시
@Mapper
public interface OutboxRecordMapper {
    @Insert("INSERT INTO outbox_record (id, status, aggregate_id, event_type, payload, " +
            "created_at, next_retry_at, partition_no) " +
            "VALUES (#{id}, 'PENDING', #{aggregateId}, #{eventType}, #{payload}, " +
            "#{createdAt}, #{nextRetryAt}, #{partitionNo})")
    void insert(OutboxRecord record);

    @Select("SELECT * FROM outbox_record WHERE status IN ('PENDING', 'FAILED') " +
            "AND next_retry_at <= NOW() ORDER BY created_at LIMIT #{batchSize}")
    List<OutboxRecord> findPendingRecords(@Param("batchSize") int batchSize);

    @Update("UPDATE outbox_record SET status = 'COMPLETED', completed_at = NOW() " +
            "WHERE id = #{id}")
    void markCompleted(@Param("id") String id);
}
```

### 4.4 Spring Boot 통합

```java
@SpringBootApplication
@EnableOutbox          // Outbox 자동 폴링 활성화
@EnableScheduling      // 스케줄러 기반 폴러 동작에 필요
public class InboundBatchApplication {
    public static void main(String[] args) {
        SpringApplication.run(InboundBatchApplication.class, args);
    }
}
```

**Clock 빈 등록:**

```java
@Configuration
public class OutboxConfiguration {
    @Bean
    public Clock clock() {
        return Clock.systemUTC();
    }
}
```

`Clock` 빈은 Outbox 라이브러리가 `created_at`, `next_retry_at` 등 시간 관련 필드를 설정할 때 사용한다. 테스트 시 `Clock.fixed()`로 교체하면 시간을 고정하여 결정론적 테스트가 가능하다.

**Producer Service (Outbox 적재):**

```java
@Service
public class ExternalInboundExpectationSaveService {
    private final OutboxRecordRepository outboxRecordRepository;
    private final ObjectMapper objectMapper;
    private final Clock clock;

    @Transactional
    public void process(Request request) {
        // 1. 비즈니스 데이터 저장
        inboundExpectationInterfaceMasterPort.save(request.toMaster());
        inboundExpectationInterfaceDetailPort.saveAll(request.toDetail());

        // 2. Outbox에 메시지 저장 (같은 DB 트랜잭션)
        OutboxRecord outboxRecord = new OutboxRecord.Builder()
                .aggregateId(message.inboundId())
                .eventType("INBOUND_EXPECTATION_SAVE")
                .payload(objectMapper.writeValueAsString(message))
                .build(clock);
        outboxRecordRepository.save(outboxRecord);
        // 트랜잭션 커밋 시 비즈니스 데이터 + outbox가 원자적으로 저장됨
    }
}
```

핵심은 **Kafka에 직접 보내지 않는다**는 점이다. Kafka 발행은 폴러의 책임이다.

**Outbox Processor (폴러가 호출):**

```java
@Component
public class KafkaProduceOutboxProcessor implements OutboxRecordProcessor {
    private final ObjectMapper objectMapper;
    private final KafkaProducePort kafkaProducePort;

    @Override
    public void process(@NonNull OutboxRecord outboxRecord) {
        switch (outboxRecord.getEventType()) {
            case "INBOUND_EXPECTATION_SAVE":
                InboundExpectationMessage message = objectMapper.readValue(
                    outboxRecord.getPayload(),
                    InboundExpectationMessage.class);
                kafkaProducePort.send(message);
                break;
        }
        // 성공 시 라이브러리가 자동으로 completed_at 마킹
        // 실패 시 retry_count++, next_retry_at 갱신 (exponential backoff)
    }
}
```

라이브러리는 폴링 → process() 호출 → 성공/실패 처리를 자동으로 관리한다. 개발자는 `OutboxRecordProcessor`만 구현하면 된다.

### 4.5 멀티 인스턴스 파티션 분산

프로덕션 환경에서는 여러 인스턴스가 동시에 Outbox를 처리한다. Namastack은 consistent hashing 기반 파티션 분산으로 중복 처리를 방지한다.

```
인스턴스 A (partition 0, 1)  ←──┐
인스턴스 B (partition 2, 3)  ←──┤ Consistent Hashing
인스턴스 C (partition 4, 5)  ←──┘

outbox_record.partition_no = hash(aggregate_id) % total_partitions
```

**동작 메커니즘:**

1. **하트비트**: 각 인스턴스는 5초마다 `outbox_instance.last_heartbeat`를 갱신
2. **비정상 감지**: 30초 동안 하트비트가 없으면 해당 인스턴스를 stale로 판정
3. **자동 재할당**: stale 인스턴스의 파티션을 정상 인스턴스들에 재분배
4. **새 인스턴스 감지**: 10초 주기로 새 인스턴스 등록을 확인하고 파티션 재분배
5. **Graceful Shutdown**: 종료 시 15초 동안 진행 중인 작업을 마무리한 후 파티션 반납

이 설계 덕분에 인스턴스 수를 늘리면 처리량이 선형적으로 증가하고, 인스턴스 장애 시 자동으로 다른 인스턴스가 작업을 인수한다.

---

## 5. @RetryableTopic Non-Blocking 재시도

Outbox가 발행 원자성을 해결했다면, `@RetryableTopic`은 수신 단계의 일시적 장애를 자동 복구한다.

### 5.1 설정 상세

```java
@RetryableTopic(
    attempts = "145",                            // 메인 1회 + 재시도 144회
    backoff = @Backoff(delay = 600000L),         // 10분 간격
    sameIntervalTopicReuseStrategy =
        SameIntervalTopicReuseStrategy.SINGLE_TOPIC,  // 재시도 토픽 1개로 통합
    kafkaTemplate = "retryKafkaTemplate"         // 재시도용 별도 템플릿
)
@KafkaListener(topics = "${spring.kafka.topics.main-topic-name}")
public void onMessage(SomethingRequestDTO dto, Acknowledgment ack,
        @Header(KafkaHeaders.RECEIVED_TOPIC) String currentTopicName) {
    TopicNameSet topicNameSet = TopicNameSet.of(mainTopicName, currentTopicName);
    somethingConvertUseCase.convert(dto.toDomain(), topicNameSet);
    ack.acknowledge();
}

@DltHandler
public void handleDeadLetter(SomethingRequestDTO dto,
        @Header(KafkaHeaders.RECEIVED_TOPIC) String dltTopicName) {
    alarmUtils.alarm("[최종 실패]", "id: " + dto.id() + "\nDLT: " + dltTopicName);
}
```

**각 설정의 의미:**

| 설정 | 값 | 설명 |
|------|-----|------|
| `attempts` | `"145"` | 원본 시도(1) + 재시도(144) = 총 145회. 144 × 10분 = 1,440분 = **24시간** |
| `backoff.delay` | `600000L` | 재시도 간격 600,000ms = 10분. `multiplier` 미설정이므로 고정 간격 |
| `sameIntervalTopicReuseStrategy` | `SINGLE_TOPIC` | 동일 간격 재시도를 하나의 토픽으로 통합. 없으면 144개 토픽 생성 |
| `kafkaTemplate` | `"retryKafkaTemplate"` | 이중 직렬화 방지를 위한 별도 템플릿 |

**토픽 생성 결과:**

```
my-topic                    ← 메인 토픽
my-topic-retry              ← 재시도 토픽 (SINGLE_TOPIC이므로 1개)
my-topic-dlt                ← Dead Letter Topic
```

`SINGLE_TOPIC` 전략은 Spring Kafka 3.2+의 기본값이다. 이 전략이 없으면 attempts 수만큼 `-retry-0`, `-retry-1`, ... 개별 토픽이 생성되어 토픽 관리가 복잡해진다.

### 5.2 retryKafkaTemplate 이중 직렬화 방지

```java
@Configuration
public class KafkaConfig {

    @Bean
    public KafkaTemplate<String, Object> kafkaTemplate() {
        Map<String, Object> configs = new HashMap<>();
        configs.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
            JsonSerializer.class);  // 메인 토픽: 객체 → JSON 직렬화
        return new KafkaTemplate<>(new DefaultKafkaProducerFactory<>(configs));
    }

    @Bean
    public KafkaTemplate<String, String> retryKafkaTemplate() {
        Map<String, Object> configs = new HashMap<>();
        configs.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
            StringSerializer.class);  // 재시도 토픽: 이미 JSON 문자열 → 그대로 전송
        return new KafkaTemplate<>(new DefaultKafkaProducerFactory<>(configs));
    }
}
```

왜 별도 템플릿이 필요한가? `@RetryableTopic`이 실패한 메시지를 재시도 토픽으로 보낼 때, 메시지는 이미 JSON 문자열 상태다. 메인 `kafkaTemplate`의 `JsonSerializer`를 그대로 사용하면 **JSON 문자열을 다시 JSON으로 직렬화**하여 이스케이프 문자가 추가된 깨진 메시지가 된다.

```
원본:     {"id": "123", "name": "item"}
이중직렬화: "{\"id\": \"123\", \"name\": \"item\"}"   ← 깨짐!
```

`StringSerializer`를 사용하는 `retryKafkaTemplate`은 이미 직렬화된 문자열을 그대로 전송하므로 이 문제를 방지한다.

### 5.3 TopicNameSet 토픽별 알림 정책

```java
public record TopicNameSet(
    String mainTopicName,
    String currentTopicName
) {
    public static TopicNameSet of(String mainTopicName, String currentTopicName) {
        return new TopicNameSet(mainTopicName, currentTopicName);
    }

    public boolean isMainTopic() {
        return Objects.equals(this.mainTopicName, this.currentTopicName);
    }

    public boolean isRetryTopic() {
        return this.currentTopicName.endsWith("-retry");
    }

    public boolean isDltTopic() {
        return this.currentTopicName.endsWith("-dlt");
    }
}
```

`TopicNameSet`은 현재 메시지가 어느 토픽에서 왔는지를 suffix로 판별한다. 이를 활용하여 토픽별로 다른 알림 정책을 적용한다:

```java
public void convert(SomethingDomain domain, TopicNameSet topicNameSet) {
    try {
        repository.create(domain);
        if (topicNameSet.isRetryTopic()) {
            alarm("[복구됨]", domain.id());  // 재시도에서 성공 → 복구 알림
        }
    } catch (Exception e) {
        if (topicNameSet.isMainTopic()) {
            alarm("[처리 실패]", domain.id());  // 최초 실패만 알림
        }
        // 재시도 토픽에서의 실패는 조용히 다시 재시도 (알림 폭탄 방지)
        throw e;  // 예외 전파 → @RetryableTopic이 다음 재시도 스케줄링
    }
}
```

**알림 정책 매트릭스:**

| 시점 | 메인 토픽 | 재시도 토픽 | DLT |
|------|---------|----------|-----|
| 최초 실패 | 슬랙 알림 발송 | - | - |
| 재시도 중 실패 | - | 조용히 재시도 | - |
| 재시도 성공 | - | "복구됨" 알림 | - |
| 144회 모두 실패 | - | - | "최종 실패" 알림 |

이 설계의 핵심은 **알림 폭탄을 방지**하면서 운영자에게 의미 있는 정보만 전달하는 것이다. 144회 재시도 동안 매번 알림이 가면 아무도 알림을 확인하지 않게 된다.

### 5.4 @DltHandler

```java
@DltHandler
public void handleDeadLetter(SomethingRequestDTO dto,
        @Header(KafkaHeaders.RECEIVED_TOPIC) String dltTopicName) {
    alarmUtils.alarm("[최종 실패 - Dead Letter]",
        "id: " + dto.id() + "\nDLT: " + dltTopicName);
}
```

145회(24시간) 재시도를 모두 소진한 메시지는 DLT(Dead Letter Topic)로 이동하고, 운영자에게 최종 실패 알림이 발송된다. DLT의 메시지는 원인을 파악하고 코드를 수정한 후 수동으로 재처리한다.

---

## 6. 전체 아키텍처 흐름

```
[외부 채널] → [Producer Service]
                ├─ interfaceDB.save()     ┐ 같은 DB 트랜잭션
                └─ outboxRecord.save()    ┘ → 원자성 보장
                        ↓
              [Outbox Poller] (배치 인스턴스, 2초마다)
                        ↓ (Kafka Producer)
              [Kafka Main Topic]
                        ↓
              [Consumer] → 성공 → 끝
                        ↓ 실패
              [Kafka Retry Topic] → 10분 대기 → 재처리
                        ↓ 144회 실패 (24시간)
              [Kafka DLT] → 운영자 알림 → 수동 재처리
```

각 구간의 자가 치유 동작:

1. **DB ↔ Kafka 원자성** (Outbox): DB 트랜잭션이 보장하므로 구조적 불일치 불가
2. **Outbox 발행 실패** (Exponential Backoff): 3회 재시도 (2초 → 4초 → 8초), 이후 FAILED
3. **Consumer 일시 장애** (@RetryableTopic): 10분 간격 144회 = 24시간 자동 재시도
4. **복구 불가 장애** (DLT): 운영자 알림 → 코드 수정 후 DLT 재처리

---

## 7. Polling vs CDC: Outbox 메시지 릴레이 방식 비교

Outbox 테이블에 적재된 메시지를 Kafka로 발행하는 방식은 크게 **Polling**(폴링)과 **CDC**(Change Data Capture) 두 가지가 있다. Namastack Outbox는 Polling만 지원하며, CDC를 사용하려면 Debezium 같은 별도 인프라가 필요하다.

### 7.1 Polling 방식 (Namastack 기본)

애플리케이션 내부의 스케줄러가 주기적으로 outbox 테이블을 조회하여 미발행 레코드를 Kafka에 발행한다.

```
[App 내부 Poller] → SELECT * FROM outbox_record WHERE status = 'PENDING'
                  → Kafka.send()
                  → UPDATE status = 'COMPLETED'
```

**장점:**
- 별도 인프라 불필요 (애플리케이션 내장)
- 설정이 간단하고 디버깅이 쉬움
- DB의 WAL/binlog 접근 권한 불필요

**단점:**
- 폴링 간격만큼 지연 발생 (기본 2초)
- DB에 주기적 쿼리 부하
- 레코드 수가 많아지면 폴링 쿼리 성능 저하

**Namastack v1.1.0+ Adaptive Polling:**

v1.1.0부터 도입된 adaptive polling은 워크로드에 따라 폴링 간격을 동적으로 조절한다. 처리할 레코드가 많으면 간격을 줄이고, 없으면 간격을 늘려 불필요한 DB 쿼리를 줄인다. 고정 `poll-interval` 대비 DB 부하를 줄이면서도 지연을 최소화하는 트레이드오프를 자동으로 관리한다.

### 7.2 CDC 방식 (Debezium)

DB의 WAL(Write-Ahead Log) 또는 binlog를 실시간으로 스트리밍하여, outbox 테이블에 INSERT가 발생하면 즉시 Kafka에 발행한다.

```
[DB binlog/WAL] → [Debezium Connector] → [Kafka Connect] → [Kafka Topic]
                                          (Outbox Event Router SMT)
```

**장점:**
- 밀리초 단위 지연 (거의 실시간)
- DB에 추가 쿼리 부하 없음 (binlog 스트리밍)
- 완료 레코드 자동 삭제 가능 (SMT 설정)
- 애플리케이션 코드 변경 최소화

**단점:**
- Kafka Connect + Debezium 인프라 운영 필요
- DB의 binlog/WAL 접근 권한 필요 (DBA 협조)
- Connector 장애 시 복구 복잡성
- 초기 설정과 운영 학습 곡선이 높음

### 7.3 선택 기준

| 기준 | Polling (Namastack) | CDC (Debezium) |
|------|---------------------|----------------|
| **지연** | 초 단위 (2초~, adaptive로 개선 가능) | 밀리초 단위 |
| **인프라** | 없음 (앱 내장) | Kafka Connect + Debezium |
| **DB 부하** | 폴링 쿼리 (인덱스로 최적화) | 없음 (binlog 스트리밍) |
| **설정 난이도** | YAML 몇 줄 | Connector JSON + SMT 설정 |
| **운영 복잡도** | 낮음 | 높음 (Connector 모니터링) |
| **Outbox 정리** | 별도 배치 필요 | SMT로 자동 삭제 가능 |
| **적합 상황** | 초 단위 지연 허용, 인프라 최소화 | 실시간 필수, Debezium 이미 도입 |

컬리 사례처럼 입고예정 데이터 동기화는 초 단위 지연이 허용되므로 Polling이 적합했다. 반면 결제나 재고 차감처럼 밀리초 지연이 중요한 도메인이라면 CDC를 고려해야 한다.

**Debezium Outbox Event Router 설정 예시:**

```json
{
  "name": "outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "db-host",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "${DB_PASSWORD}",
    "database.server.id": "1",
    "table.include.list": "mydb.outbox_record",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.table.fields.additional.placement": "event_type:header",
    "transforms.outbox.route.by.field": "aggregate_id",
    "transforms.outbox.route.topic.replacement": "outbox.events.${routedByValue}",
    "transforms.outbox.table.expand.json.payload": "true"
  }
}
```

이 설정에서 `EventRouter` SMT(Single Message Transform)는 outbox_record 테이블의 INSERT를 감지하여 `aggregate_id` 기반으로 토픽을 라우팅하고, payload를 JSON으로 펼쳐서 Kafka에 발행한다. Debezium이 발행을 완료하면 outbox 레코드를 자동 삭제하도록 설정할 수도 있다.

---

## 8. Outbox 라이브러리 대안 비교

| 라이브러리 | 방식 | 특징 | 적합 상황 |
|-----------|------|------|----------|
| **Namastack Outbox** | 폴링 기반 (앱 내장) | Spring Boot 네이티브, 멀티 인스턴스 파티션, 자동 재시도 | 별도 인프라 없이 빠르게 도입 |
| **Debezium Outbox Event Router** | CDC 기반 (외부 프로세스) | DB WAL 스트리밍, SMT로 라우팅, outbox 테이블 자동 정리 | Debezium 인프라가 이미 있는 경우 |
| **Spring Modulith** | 이벤트 퍼블리케이션 레지스트리 | `@ApplicationModuleListener` + JPA/JDBC 이벤트 로그 | 모듈러 모놀리스 아키텍처 |
| **Gruelbox TransactionOutbox** | 폴링 기반 (앱 내장) | 다양한 DB/DI 프레임워크 지원, 경량 | Spring 외 환경 (Guice 등) |
| **직접 구현** | 폴링/CDC | 완전 제어 가능 | 특수 요구사항 (비권장) |

**Namastack vs Debezium 핵심 차이:**

폴링 방식(Namastack)은 애플리케이션 내부에서 동작하므로 별도 인프라가 필요 없고 설정이 간단하다. 반면 CDC 방식(Debezium)은 DB의 WAL/binlog를 스트리밍하므로 지연이 밀리초 단위로 짧고, 완료된 outbox 레코드를 자동 정리할 수 있다. 폴링은 간격(2초)만큼 지연이 발생하고 DB에 주기적 쿼리 부하를 준다.

---

## 9. 대안 접근법 비교

| 접근법 | 발행 원자성 | 수신 재시도 | 복잡도 |
|--------|-----------|-----------|--------|
| **Outbox + @RetryableTopic** (컬리 선택) | ✅ | ✅ 자동 (24시간) | 중간 |
| Kafka 트랜잭션 + DefaultErrorHandler | △ (Kafka 내부만) | △ 블로킹 | 낮음 |
| @TransactionalEventListener + 수동 재발행 | △ (발행 실패 시 유실) | ❌ 수동 | 높음 |
| Debezium CDC + Custom DLQ 컨슈머 | ✅ | △ 커스텀 필요 | 높음 |

**Kafka 트랜잭션** (`spring.kafka.producer.transaction-id-prefix`)은 Kafka 내부의 원자성만 보장한다. Producer → Kafka → Consumer가 하나의 트랜잭션으로 묶이지만, DB와 Kafka 간의 원자성은 보장하지 못한다. "DB 저장 + 이벤트 발행"이 원자적이어야 하는 Outbox 시나리오와는 해결하는 문제가 다르다.

**@TransactionalEventListener**는 DB 트랜잭션 커밋 후 이벤트를 발행하지만, 발행 자체가 실패하면 이벤트가 유실된다. 이벤트 발행이 DB 트랜잭션 밖에서 일어나기 때문이다.

---

## 10. 운영 인사이트

### 10.1 Poison Pill 문제

"Poison Pill이면 어떡하나?" — 구조적 오류(잘못된 스키마, 필수 필드 누락 등)로 인해 아무리 재시도해도 절대 성공할 수 없는 메시지가 있을 수 있다. 이 경우 145회 재시도를 모두 소진한 후 DLT에 도달한다.

DLT 메시지의 처리 프로세스:
1. DLT 알림을 받은 운영자가 메시지 내용 확인
2. 원인 분석 (스키마 불일치, 비즈니스 규칙 위반 등)
3. 코드 수정 배포
4. DLT 메시지를 메인 토픽으로 재발행하여 재처리

Poison Pill을 조기에 식별하고 싶다면, 특정 예외 타입(예: `SchemaValidationException`)에 대해서는 재시도 없이 즉시 DLT로 보내는 `@ExceptionTypeRouterCustomizer`를 설정할 수 있다. 다만 컬리의 경우 대부분의 실패가 일시적 의존성 문제이므로, 모든 예외에 대해 재시도를 적용하는 것이 더 적합했다.

### 10.2 Outbox 테이블 정리 전략

`delete-completed-records: false` 설정은 완료 레코드를 삭제하지 않으므로, 테이블이 지속적으로 증가한다. 정리 전략:

1. **보존 기간 설정**: 예를 들어 7일 이후 COMPLETED 레코드 삭제
2. **별도 배치 작업**: Spring `@Scheduled` 또는 DB 이벤트 스케줄러로 주기적 정리
3. **아카이브**: 삭제 전 별도 아카이브 테이블로 이동 (장기 감사 추적 필요 시)

```sql
-- 7일 이상 된 완료 레코드 정리 예시
DELETE FROM outbox_record
WHERE status = 'COMPLETED'
  AND completed_at < DATE_SUB(NOW(), INTERVAL 7 DAY)
LIMIT 10000;  -- 대량 삭제 시 배치 처리
```

### 10.3 모니터링

효과적인 Outbox + Retry 모니터링을 위한 핵심 지표:

**Outbox 지표:**

```sql
-- 상태별 레코드 수 (대시보드 패널)
SELECT status, COUNT(*) FROM outbox_record GROUP BY status;

-- retry_count 분포 (재시도 패턴 분석)
SELECT retry_count, COUNT(*) FROM outbox_record
WHERE status = 'FAILED' GROUP BY retry_count;

-- 평균 발행 지연 (created_at → completed_at)
SELECT AVG(TIMESTAMPDIFF(SECOND, created_at, completed_at))
FROM outbox_record WHERE status = 'COMPLETED';
```

**@RetryableTopic 지표:**

- `spring_kafka_listener_seconds_sum` / `spring_kafka_listener_seconds_count` — Consumer 처리 시간
- 재시도 토픽과 DLT의 Consumer lag — 재시도 적체량
- DLT 메시지 인입률 — 복구 불가 장애 빈도

### 10.4 멱등성 고려

Outbox 폴러가 Kafka 발행에 성공한 후 `outbox_record` 상태를 COMPLETED로 갱신하기 전에 인스턴스가 크래시하면, 재시작 시 같은 메시지를 다시 발행한다. 따라서 **Consumer는 반드시 멱등하게 설계**해야 한다.

멱등성 구현 방법:
- DB `UPSERT` (INSERT ... ON DUPLICATE KEY UPDATE)
- `aggregate_id` + `event_type` 기반 중복 체크 테이블
- 상세: [06-idempotent-consumer.md](./06-idempotent-consumer.md) 참조

---

## 11. 실전 교훈

1. **DB와 메시지 브로커는 다른 트랜잭션 시스템이다.** `@Transactional`이 Kafka 발행까지 보장한다는 착각이 가장 흔한 실수다. Outbox 패턴으로 이 간극을 메워야 한다.

2. **재시도의 시간 설계가 비즈니스를 결정한다.** 10분 × 144회 = 24시간은 "파트너 정보 등록에 최대 하루가 걸릴 수 있다"는 비즈니스 SLA를 반영한 것이다. 재시도 횟수와 간격은 기술이 아닌 비즈니스 요구사항에서 도출해야 한다.

3. **알림 정책은 토픽별로 차등 적용하라.** 모든 실패에 알림을 보내면 알림 피로(alert fatigue)로 정작 중요한 알림을 놓친다. 최초 실패, 복구, 최종 실패 세 지점만 알림하는 것이 운영에 효과적이다.

4. **이중 직렬화는 @RetryableTopic의 가장 흔한 함정이다.** `retryKafkaTemplate`을 `StringSerializer`로 구성하지 않으면 재시도 메시지가 깨진다. 메인 토픽과 재시도 토픽의 직렬화 전략이 다르다는 점을 기억해야 한다.

5. **Outbox 테이블은 무한 증가한다.** `delete-completed-records: false`는 감사 추적에 유용하지만, 별도 정리 배치 없이는 디스크 문제를 유발한다. 보존 기간과 아카이브 전략을 미리 설계하라.

6. **Consumer 멱등성은 Outbox와 @RetryableTopic 모두에서 필수다.** Outbox는 발행 중복, @RetryableTopic은 수신 중복이 발생할 수 있다. 양쪽 모두 멱등성으로 방어해야 한다.
