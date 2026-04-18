# 테스트 전략 비교: 수동 테스트 vs Testcontainers + RedPanda

> 한줄 요약: TPS의 수동 테스트(Postman + 로그 확인)를 Testcontainers + RedPanda 컨테이너 기반 자동화 통합 테스트로 대체하여, 테스트 재현성과 CI/CD 통합을 확보한다.

---

## 1. AS-IS: TPS 수동 테스트 방식

### 1.1 현황: 수동 테스트의 한계

TPS 프로젝트에서는 주로 수동 테스트로 비동기 흐름을 검증합니다.

```
1. Postman으로 REST API 호출
   ↓
2. 10초 대기 (스케줄러 주기)
   ↓
3. DB 또는 로그에서 상태 확인
   ↓
4. 수동으로 결과 검증
```

**구체적 예시: Ch07 파이프라인 테스트**

```
Step 1: POST /api/ch07/pipeline/start
  → Request Body: {"orderId": "ORD-001", "destination": "http://..."}

Step 2: 10초 대기 (MessageTaskScheduler.executeMessageTasks() 주기)

Step 3: DB 확인
  → SELECT * FROM TB_TPS_MS_021 WHERE order_id = 'ORD-001'
  → status = 'FRWRD' 확인 (Forward 완료)

Step 4: 20초 대기 (Destination 응답까지 추가 시간)

Step 5: 다시 DB 확인
  → status = 'RSPND' 확인 (응답 도착)

Step 6: 로그 검색
  → "Pipeline execution completed" 메시지 찾기
```

### 1.2 문제점 분석

| # | 문제 | 근본 원인 | 영향 |
|---|------|---------|------|
| 1 | 회귀 테스트 불가 | 수동 절차이므로 자동화 불가능 | 배포 전마다 30분 수동 검증 필요 |
| 2 | 비동기 흐름 검증 어려움 | Thread.sleep() 기반 대기 필요 | 스케줄러 → FeignClient → 응답 전체 흐름 자동 테스트 불가 |
| 3 | 환경 의존성 | 실제 Jenkins, DB, 네트워크 필요 | 로컬 개발 환경에서 테스트 불가, CI/CD 파이프라인 자동화 불가 |
| 4 | 플래키 테스트 위험 | 고정된 대기 시간 (10, 20초) | 간헐적 실패, 재현 어려움 |
| 5 | 상태 검증의 한계 | 각 단계별 상태를 개별적으로 확인 | 전체 워크플로우의 동시성 문제 감지 불가 |

**예시: 고장난 시나리오**

```
✗ Destination 응답이 10초 지연되는 경우
  → 20초 대기로도 'RSPND' 상태 못 찾음
  → "테스트 실패"라고 판단하지만, 사실은 시간 초과

✗ 동시 요청 처리 시
  → 수동으로 여러 orderId를 추적 불가능
  → 상태 전이 순서 검증 불가능
  → Race condition 감지 불가능
```

---

## 2. TO-BE: Testcontainers + RedPanda 자동화 전략

### 2.1 테스트 피라미드 구조

```
                    ▲
                   /E2E\
                  /     \  (통합 테스트)
                 /-------\
                /Integration\
               /             \ (컨테이너 기반)
              /-------────────\
            /    Unit Tests    \ (순수 로직)
           /─────────────────────\
          실행 시간: 빠름           많음
          복잡도:   낮음     →      높음
          안정성:   높음     →      낮음
```

**각 레벨의 테스트:**

| 레벨 | 대상 | 기술 | 예시 |
|------|------|------|------|
| **Unit** | 순수 로직 | JUnit | `MessageStatusRule.canTransitionTo()` |
| **Integration** | Producer/Consumer 흐름 | Testcontainers + RedPanda | `MessageStatusServiceTest`, `TransactionalProducerTest` |
| **E2E** | 전체 파이프라인 | Spring Boot Test + MockMvc | `HealthCheckControllerTest` |

### 2.2 Testcontainers의 장점

**1. 환경 독립성**

```java
// ❌ AS-IS: 실제 Kafka 브로커 필요
@EmbeddedKafka(partitions = 1, topics = {"orders"})
class OrderConsumerTest { }

// ✅ TO-BE: Docker 컨테이너 자동 시작
@Testcontainers
class OrderConsumerTest extends AbstractKafkaTest {
    // RedPanda 컨테이너가 테스트 시작 시 자동 실행
}
```

**2. RedPanda의 빠른 시작**

```
RedPanda: ~7초 시작   ← 가볍고 효율적
Kafka:   ~15초 시작   ← 무겁고 느림
```

**3. Schema Registry 내장**

```java
// ❌ 별도 컨테이너 필요 X
// ✅ RedPanda에 Schema Registry가 이미 포함됨
registry.add("spring.kafka.consumer.properties.schema.registry.url",
    () -> REDPANDA.getSchemaRegistryAddress());
```

**4. 격리된 테스트 환경**

```
각 테스트 클래스마다 독립된 RedPanda 인스턴스
→ 테스트 간 간섭 없음
→ 병렬 실행 가능
→ 재현성 100%
```

### 2.3 공통 테스트 기반: AbstractKafkaTest

프로젝트의 모든 통합 테스트는 이 기반 클래스를 상속합니다.

```java
@Testcontainers
public abstract class AbstractKafkaTest {

    @Container
    static final RedpandaContainer REDPANDA = new RedpandaContainer(
            "docker.redpanda.com/redpandadata/redpanda:v25.3.6"
    );

    @DynamicPropertySource
    static void overrideProperties(DynamicPropertyRegistry registry) {
        // 1. Kafka Bootstrap Servers
        registry.add("spring.kafka.bootstrap-servers",
            REDPANDA::getBootstrapServers);

        // 2. Schema Registry 주소
        registry.add("spring.kafka.consumer.properties.schema.registry.url",
            () -> REDPANDA.getSchemaRegistryAddress());
        registry.add("spring.kafka.producer.properties.schema.registry.url",
            () -> REDPANDA.getSchemaRegistryAddress());
    }
}
```

**작동 원리:**

```
테스트 시작
  ↓
@Testcontainers 어노테이션
  ↓
@Container 필드로 RedPanda 이미지 다운로드 및 컨테이너 시작
  ↓
@DynamicPropertySource로 Spring 설정 오버라이드
  ↓
테스트 코드 실행
  ↓
테스트 종료 후 컨테이너 자동 정리
```

### 2.4 PoC 테스트 코드 구조

#### 2.4.1 HealthCheckControllerTest (Ch01)

**목표:** RedPanda 클러스터 연결 확인

```java
@SpringBootTest
@AutoConfigureMockMvc
class HealthCheckControllerTest extends AbstractKafkaTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void Redpanda_클러스터에_정상_연결되어야_한다() throws Exception {
        mockMvc.perform(get("/api/ch01/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"))
                .andExpect(jsonPath("$.nodes").value(1));
    }
}
```

**검증 항목:**
- RedPanda 컨테이너가 정상 시작됨
- AdminClient로 클러스터 정보 조회 가능
- 응답 형식 정확함

#### 2.4.2 MessageStatusServiceTest (Ch07)

**목표:** 상태 전이 규칙 검증 (단위 테스트)

```java
@SpringBootTest
class MessageStatusServiceTest extends AbstractKafkaTest {

    @Test
    @DisplayName("MessageStatusRule은 유효한 전이만 허용해야 한다")
    void 상태_전이_유효성_검증() {
        // PENDING -> FORWARD (유효)
        assertTrue(MessageStatusRule.canTransitionTo(
            MessageStatus.PENDING, MessageStatus.FORWARD));

        // PENDING -> COMPLETE (무효 - 중간 단계 건너뜀)
        assertFalse(MessageStatusRule.canTransitionTo(
            MessageStatus.PENDING, MessageStatus.COMPLETE));

        // COMPLETE -> 어떤 상태든 (무효 - 최종 상태)
        assertFalse(MessageStatusRule.canTransitionTo(
            MessageStatus.COMPLETE, MessageStatus.PENDING));
    }
}
```

**검증 항목:**
- 정상 상태 전이 경로: PENDING → FORWARD → RESPOND → COMPLETE
- 실패 경로: 모든 상태에서 FAILURE 가능 (최종 상태 제외)
- 불가능한 전이: COMPLETE/FAILURE에서 다른 상태로 전이 불가

#### 2.4.3 TransactionalProducerTest (Ch08)

**목표:** 트랜잭션 Producer 자동화 테스트 (구현 필요)

```java
@SpringBootTest
public class TransactionalProducerTest extends AbstractKafkaTest {

    @Autowired
    private TransactionalProducer transactionalProducer;

    /**
     * TODO 1: 트랜잭션 커밋 시나리오
     *
     * 절차:
     * 1. TransactionEvent 생성
     * 2. transactionalProducer.sendTransactional(event) 호출
     * 3. tx-orders, tx-analytics, tx-audit 토픽에 메시지 도착 확인
     * 4. Awaitility로 비동기 대기
     */
    @Test
    void 트랜잭션_커밋_시_3개_토픽_모두_메시지_보임() {
        // TODO: 구현
    }

    /**
     * TODO 2: 트랜잭션 abort 시나리오
     *
     * 절차:
     * 1. TransactionEvent 생성
     * 2. transactionalProducer.sendWithAbort(event) 호출
     * 3. read_committed Consumer로 메시지 없음 확인
     * 4. read_uncommitted Consumer로 메시지 존재 확인 (abort 과정 가시화)
     */
    @Test
    void 트랜잭션_abort_시_메시지_안_보임() {
        // TODO: 구현
    }

    /**
     * TODO 3: 배치 원자성
     *
     * 절차:
     * 1. 5개의 TransactionEvent 리스트 생성
     * 2. transactionalProducer.sendBatch(events) 호출
     * 3. tx-orders 토픽에 정확히 5개 메시지 도착 확인
     */
    @Test
    void 배치_트랜잭션_원자성_검증() {
        // TODO: 구현
    }
}
```

### 2.5 Awaitility: 비동기 대기 패턴

#### 2.5.1 Thread.sleep()의 문제점

```java
// ❌ 안티패턴: 고정 대기
@Test
void 주문_처리_완료() {
    orderProducer.send(order);
    Thread.sleep(5000);  // 5초 고정 대기
    assertEquals("COMPLETED", getOrderStatus(orderId));
}
```

**문제:**
- 5초에 처리되면? → 불필요한 5초 대기
- 6초에 처리되면? → 테스트 실패 (플래키 테스트)
- CI 환경에서 느림 → 전체 테스트 시간 배 이상 증가

#### 2.5.2 Awaitility 패턴

```java
// ✅ 조건 기반 대기
@Test
void 주문_처리_완료() {
    orderProducer.send(order);

    // "조건이 만족될 때까지" 최대 5초 대기
    await()
        .atMost(Duration.ofSeconds(5))
        .pollInterval(Duration.ofMillis(100))
        .untilAsserted(() -> {
            assertEquals("COMPLETED", getOrderStatus(orderId));
        });
}
```

**장점:**
- 조건 만족 시 즉시 다음 단계로 진행
- 최대 대기 시간만 설정하면 됨
- 폴링 간격 조정으로 성능 튜닝 가능

#### 2.5.3 Awaitility 실제 사용 예시

```java
// 1. Consumer에서 메시지 도착까지 대기
@Test
void Producer_메시지_Consumer가_수신() {
    String orderId = "ORD-123";
    orderProducer.send(new OrderEvent(orderId, "PENDING"));

    await()
        .atMost(Duration.ofSeconds(10))
        .pollInterval(Duration.ofMillis(50))
        .untilAsserted(() -> {
            assertTrue(testConsumer.hasMessageWithId(orderId));
        });
}

// 2. DB 상태 변경까지 대기
@Test
void 스케줄러_실행_후_DB_상태_변경() {
    messageRepository.save(new Message("MSG-001", "PENDING"));

    await()
        .atMost(Duration.ofSeconds(15))
        .pollInterval(Duration.ofMillis(100))
        .untilAsserted(() -> {
            Message msg = messageRepository.findById("MSG-001");
            assertEquals("FORWARDED", msg.getStatus());
        });
}

// 3. 복수 조건 검증
@Test
void 파이프라인_전체_흐름() {
    pipelineService.start(pipeline);

    await()
        .atMost(Duration.ofSeconds(20))
        .untilAsserted(() -> {
            Pipeline result = pipelineRepository.findById(pipeline.getId());
            assertEquals("COMPLETED", result.getStatus());
            assertEquals(5, result.getStepCount());
            assertTrue(result.isSuccessful());
        });
}
```

---

## 3. AS-IS vs TO-BE 비교 테이블

| 항목 | AS-IS (수동 테스트) | TO-BE (Testcontainers) |
|------|------------------|----------------------|
| **테스트 방식** | Postman + 수동 로그 확인 | 자동화 JUnit 테스트 |
| **자동화 가능** | 불가능 | 가능 (CI/CD 파이프라인 통합) |
| **재현성** | 낮음 (환경 의존적) | 높음 (100% 일관성) |
| **대기 메커니즘** | Thread.sleep(고정값) | Awaitility (조건 기반) |
| **테스트 속도** | 느림 (최소 30분) | 빠름 (챕터당 ~2분) |
| **환경 의존성** | 높음 (실제 DB, 네트워크) | 낮음 (Docker 컨테이너) |
| **비동기 검증** | 어려움 (단계별 수동 확인) | 쉬움 (wait/until 패턴) |
| **회귀 테스트** | 불가능 | 가능 (배포 전 자동 실행) |
| **개발 속도** | 느림 (변경→대기→확인 반복) | 빠름 (즉시 피드백) |
| **CI/CD 통합** | 불가능 | 가능 (Jenkins/GitHub Actions) |
| **비용** | 높음 (수동 인력) | 낮음 (자동화) |

---

## 4. 테스트 안티패턴과 해결책

### 4.1 고정 대기 시간

```java
// ❌ 안티패턴
@Test
void 메시지_처리() {
    producer.send(message);
    Thread.sleep(3000);  // 3초 고정 대기
    assertMessageProcessed(message);
}
```

**문제:**
- 처리가 빠르면? → 불필요한 대기
- 처리가 느리면? → 테스트 실패
- 환경마다 다르면? → 플래키 테스트

**해결:**

```java
// ✅ Awaitility 사용
@Test
void 메시지_처리() {
    producer.send(message);
    await()
        .atMost(Duration.ofSeconds(5))
        .pollInterval(Duration.ofMillis(100))
        .untilAsserted(() -> {
            assertMessageProcessed(message);
        });
}
```

### 4.2 하드코딩 포트 번호

```java
// ❌ 안티패턴
@Test
void 포트_고정() {
    KafkaConsumer<String, String> consumer =
        new KafkaConsumer<>(Map.of(
            "bootstrap.servers", "localhost:9092",  // 고정 포트
            "group.id", "test-group"
        ));
}
```

**문제:**
- 포트 충돌 (다른 테스트와 동시 실행 불가)
- 로컬에서는 성공, CI에서는 실패
- 병렬 테스트 불가능

**해결:**

```java
// ✅ 동적 포트 할당 (AbstractKafkaTest)
@Testcontainers
public abstract class AbstractKafkaTest {
    @Container
    static final RedpandaContainer REDPANDA = new RedpandaContainer(...);

    @DynamicPropertySource
    static void overrideProperties(DynamicPropertyRegistry registry) {
        // 동적으로 포트 할당 (각 테스트마다 다름)
        registry.add("spring.kafka.bootstrap-servers",
            REDPANDA::getBootstrapServers);
    }
}
```

### 4.3 토픽/그룹 공유로 인한 테스트 오염

```java
// ❌ 안티패턴
@Test
void 테스트1_주문() {
    producer.send("orders", order1);  // 공유 토픽
    // ...
}

@Test
void 테스트2_주문() {
    producer.send("orders", order2);  // 테스트1의 메시지도 남아있음!
    // ...
}
```

**문제:**
- 테스트 순서에 따라 결과가 달라짐
- 테스트 간 간섭
- 병렬 실행 불가능

**해결:**

```java
// ✅ UUID로 고유한 토픽/그룹 생성
@Test
void 테스트1_주문() {
    String topicId = UUID.randomUUID().toString();
    String groupId = "test-group-" + UUID.randomUUID();

    producer.send("orders-" + topicId, order1);
    // 격리된 환경에서 테스트
}
```

### 4.4 @DirtiesContext 남용

```java
// ❌ 안티패턴
@SpringBootTest
@DirtiesContext(classMode = ClassMode.AFTER_EACH_TEST_METHOD)
class SlowTestWithDirtiesContext {
    // 각 테스트마다 Spring 컨텍스트 재로드 → 매우 느림!
}
```

**문제:**
- 각 테스트 후 Spring 컨텍스트 재시작 (매우 느림)
- 테스트 5개 = 5번 컨텍스트 재로드
- CI 파이프라인 시간 배 증가

**해결:**

```java
// ✅ @BeforeEach로 테스트 격리
@SpringBootTest
class FastTestWithBeforeEach {

    @BeforeEach
    void setUp() {
        // 컨텍스트는 유지하되, 테스트 데이터만 초기화
        testRepository.deleteAll();
        testKafkaTopic.reset();
    }

    @Test
    void 테스트1() { }

    @Test
    void 테스트2() { }
}
```

---

## 5. 현직 사례와 모범 사례

### 5.1 Redpanda Official: TDD & CI Testing

**Redpanda 공식 예제에서 권장하는 패턴:**

```java
@Testcontainers
public class RedpandaBestPractice {

    @Container
    static RedpandaContainer container = new RedpandaContainer(
        "docker.redpanda.com/redpandadata/redpanda:latest"
    );

    // 1. 실제 브로커로 테스트 (Mock 아님)
    @Test
    void 실제_브로커_기반_테스트() {
        // RedPanda 실제 인스턴스
    }

    // 2. Container Reuse로 CI 시간 단축
    // testcontainers.reuse.enable=true (gradle.properties)
    // → 컨테이너 재사용으로 시작 시간 0s로 단축

    // 3. Schema Registry 통합 (내장)
    @Test
    void Avro_스키마_레지스트리_통합() {
        // REDPANDA.getSchemaRegistryAddress()로 접근
    }
}
```

**이점:**
- 개발 환경 = 테스트 환경 = 프로덕션 환경 일관성
- 스키마 호환성 사전 검증
- 프로덕션 배포 전 실제 동작 보증

### 5.2 Spring Kafka Testing: @EmbeddedKafka vs Testcontainers

| 항목 | @EmbeddedKafka | Testcontainers + RedPanda |
|------|----------------|--------------------------|
| **속도** | 빠름 (~1초 시작) | 중간 (~7초 시작) |
| **프로덕션 일관성** | 낮음 (경량화된 브로커) | 높음 (실제 브로커) |
| **Avro 지원** | 별도 설정 필요 | 내장 (Schema Registry) |
| **네트워크 테스트** | 불가능 | 가능 (실제 소켓) |
| **트랜잭션** | 기본 지원 | 전체 지원 |
| **추천 용도** | 빠른 단위 테스트 | 실제 같은 통합 테스트 |

**선택 기준:**

```
단위 테스트 (로직만 검증)
→ @EmbeddedKafka 사용 (빠름)

통합 테스트 (Producer/Consumer 흐름)
→ Testcontainers 사용 (정확함)
```

### 5.3 CI/CD 파이프라인 통합

**GitHub Actions 예시:**

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'

      - name: Run tests with Testcontainers
        run: |
          # Docker 설치됨 (GitHub Actions 기본 제공)
          ./gradlew test

      # Testcontainers가 Docker를 자동으로 관리
      # 테스트 완료 후 컨테이너 자동 정리
```

**Jenkins 예시:**

```groovy
pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                script {
                    sh './gradlew test'
                    // Testcontainers가 Docker 자동 관리
                }
            }
        }
    }

    post {
        always {
            junit 'build/test-results/**/*.xml'
            // 테스트 결과 수집
        }
    }
}
```

---

## 6. 트랜잭션 테스트 구현 가이드

### 6.1 read_committed vs read_uncommitted

**배경:** Kafka 트랜잭션 격리 수준

```
트랜잭션 commit 전:
  read_uncommitted: 메시지 보임 (dirty read)
  read_committed:   메시지 안 보임

트랜잭션 abort 후:
  read_uncommitted: 메시지 여전히 보임 (롤백 안 됨)
  read_committed:   메시지 사라짐 (롤백됨)
```

### 6.2 Testcontainers에서 트랜잭션 테스트

```java
@SpringBootTest
public class TransactionalProducerTest extends AbstractKafkaTest {

    @Autowired
    private TransactionalProducer producer;

    @Test
    void 트랜잭션_커밋_시_메시지_보임() {
        // 1. 메시지 발행 (트랜잭션)
        TransactionEvent event = new TransactionEvent("ORD-001", 100.0);
        producer.sendTransactional(event);

        // 2. read_committed Consumer로 확인 (메시지 보여야 함)
        KafkaConsumer<String, TransactionEvent> consumer =
            createReadCommittedConsumer();

        await()
            .atMost(Duration.ofSeconds(5))
            .untilAsserted(() -> {
                List<TransactionEvent> messages =
                    pollMessages(consumer, "tx-orders");
                assertEquals(1, messages.size());
                assertEquals("ORD-001", messages.get(0).getOrderId());
            });
    }

    @Test
    void 트랜잭션_abort_시_메시지_안_보임() {
        // 1. abort되는 트랜잭션 실행
        try {
            producer.sendWithAbort(new TransactionEvent("ORD-002", 200.0));
        } catch (RuntimeException e) {
            // 예상된 예외
        }

        // 2. read_committed Consumer (메시지 없어야 함)
        KafkaConsumer<String, TransactionEvent> consumer =
            createReadCommittedConsumer();

        List<TransactionEvent> messages = pollMessages(consumer, "tx-orders");
        assertEquals(0, messages.size(),
            "read_committed에서는 abort된 메시지 보이지 않아야 함");

        // 3. read_uncommitted Consumer (메시지 보여야 함 - 선택사항)
        KafkaConsumer<String, TransactionEvent> uncommittedConsumer =
            createReadUncommittedConsumer();

        List<TransactionEvent> uncommittedMessages =
            pollMessages(uncommittedConsumer, "tx-orders");
        assertEquals(1, uncommittedMessages.size(),
            "read_uncommitted에서는 abort된 메시지도 보임");
    }

    // Helper: read_committed Consumer 생성
    private KafkaConsumer<String, TransactionEvent>
            createReadCommittedConsumer() {
        Properties props = new Properties();
        props.put("bootstrap.servers", REDPANDA.getBootstrapServers());
        props.put("group.id", "test-group-" + UUID.randomUUID());
        props.put("auto.offset.reset", "earliest");
        props.put("isolation.level", "read_committed");
        props.put("key.deserializer",
            "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer",
            "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        props.put("schema.registry.url", REDPANDA.getSchemaRegistryAddress());

        return new KafkaConsumer<>(props);
    }

    // Helper: read_uncommitted Consumer 생성
    private KafkaConsumer<String, TransactionEvent>
            createReadUncommittedConsumer() {
        Properties props = new Properties();
        props.put("bootstrap.servers", REDPANDA.getBootstrapServers());
        props.put("group.id", "test-group-" + UUID.randomUUID());
        props.put("auto.offset.reset", "earliest");
        props.put("isolation.level", "read_uncommitted");  // 차이점
        props.put("key.deserializer",
            "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer",
            "io.confluent.kafka.serializers.KafkaAvroDeserializer");
        props.put("schema.registry.url", REDPANDA.getSchemaRegistryAddress());

        return new KafkaConsumer<>(props);
    }
}
```

### 6.3 DLQ (Dead Letter Queue) 테스트

```java
@Test
void 재시도_실패_시_DLQ로_전달() {
    // 1. 처리 실패하는 메시지 발행
    OrderEvent order = new OrderEvent("ORD-FAIL", "invalid-json");
    producer.send("orders", order);

    // 2. 메인 토픽 Consumer 재시도 -> 실패 -> DLQ로 라우팅
    await()
        .atMost(Duration.ofSeconds(10))
        .untilAsserted(() -> {
            // DLQ 토픽 확인
            List<OrderEvent> dlqMessages =
                pollMessages(dlqConsumer, "orders-dlq");
            assertEquals(1, dlqMessages.size());
            assertEquals("ORD-FAIL", dlqMessages.get(0).getOrderId());
        });
}
```

---

## 7. 면접 예상 질문 및 답변

### Q1: 비동기 메시징 시스템을 어떻게 테스트하나요?

**예상 답변:**

"두 가지 접근을 사용합니다.

1. **단위 테스트 (빠름)**
   - 순수 로직만 검증 (MessageStatusRule)
   - Mock/Stub 사용
   - 1초 이내 완료

2. **통합 테스트 (정확함)**
   - Testcontainers로 실제 Redpanda 컨테이너 실행
   - 실제 Producer/Consumer 상호작용 검증
   - Awaitility로 비동기 대기 (조건 기반)
   - 5-10초 완료

**구체적 예시:**

```
메시지 발행 → Consumer 수신 → 상태 변경
까지 전체 흐름을 자동화 테스트합니다.

고정 시간 대기 대신 Awaitility의 wait().until()
패턴으로 조건 만족 시 즉시 진행하므로,
플래키 테스트를 방지하고 테스트 속도를 높입니다.
```"

### Q2: Testcontainers의 장점과 사용 시 주의점은?

**예상 답변:**

**장점:**
- 환경 독립적 (Docker 컨테이너로 격리)
- 프로덕션과 동일한 환경에서 테스트
- Schema Registry 내장 (Redpanda의 경우)
- CI/CD 자동화 가능

**주의점:**

1. **포트 충돌 방지**
   ```java
   // ❌ 하드코딩 금지
   "bootstrap.servers", "localhost:9092"

   // ✅ 동적 할당
   @DynamicPropertySource로 오버라이드
   ```

2. **테스트 격리**
   ```java
   // UUID로 고유한 토픽/그룹 사용
   String groupId = "test-" + UUID.randomUUID();
   ```

3. **컨테이너 정리**
   ```java
   // @Testcontainers가 자동으로 정리
   // 하지만 정상 종료 확인 필수
   ```

4. **Docker 의존성**
   - 로컬에서는 Docker Desktop 필요
   - CI 환경에서는 Docker 실행 권한 필요

### Q3: 플래키 테스트를 방지하는 방법은?

**예상 답변:**

"플래키 테스트는 비결정적 동작으로 인한 간헐적 실패입니다.

**원인:**

1. 고정 대기 시간
   ```java
   Thread.sleep(3000);  // 3초 고정
   // → 3.5초에 완료되면 실패
   ```

2. 하드코딩 포트
   ```java
   // → 다른 테스트와 포트 충돌 가능
   ```

3. 테스트 간 간섭
   ```java
   // 공유 토픽/그룹 사용 → 순서 의존성
   ```

**해결책:**

1. **Awaitility 사용**
   ```java
   await()
       .atMost(Duration.ofSeconds(5))
       .untilAsserted(() -> { /* 조건 검증 */ });
   ```

2. **동적 포트 할당**
   ```java
   @DynamicPropertySource로 자동 할당
   ```

3. **테스트 격리**
   ```java
   UUID로 고유한 토픽/그룹
   @BeforeEach로 데이터 초기화
   ```

4. **병렬 실행**
   ```java
   // 각 테스트가 독립적이면 병렬 실행 가능
   // → 속도 개선
   ```"

### Q4: DLQ (Dead Letter Queue) 테스트는 어떻게 작성하나요?

**예상 답변:**

"DLQ는 처리 실패한 메시지를 따로 저장하는 토픽입니다.

```
메인 토픽 → Consumer
  ↓ (재시도 3회 실패)
  ↓
DLQ 토픽 → 모니터링/수동 처리
```

**테스트 구조:**

1. **에러 유발 메시지 발행**
   ```java
   OrderEvent invalid = new OrderEvent(null, "invalid-json");
   producer.send("orders", invalid);
   ```

2. **메인 토픽 Consumer 실패**
   ```java
   // 역직렬화 실패 또는 비즈니스 로직 실패
   ```

3. **DLQ로 라우팅**
   ```java
   // Spring Cloud Stream이나 Kafka Stream 라우팅
   ```

4. **DLQ 토픽 검증**
   ```java
   await()
       .atMost(Duration.ofSeconds(10))
       .untilAsserted(() -> {
           List<OrderEvent> dlqMessages =
               pollMessages(dlqConsumer, "orders-dlq");
           assertEquals(1, dlqMessages.size());
       });
   ```

**주의점:**
- 재시도 정책 명확 (몇 회? 어떤 간격?)
- DLQ 토픽도 모니터링 필요
- 실패 이유 로깅 필수
"

---

## 8. 체크리스트: 테스트 품질 검증

작성한 테스트가 다음 항목을 만족하는지 확인하세요.

### 8.1 통합 테스트 체크리스트

```
□ AbstractKafkaTest를 상속했는가?
□ @SpringBootTest 어노테이션이 있는가?
□ 테스트 이름이 명확한가? (한국어 displayName)
□ 실제 Redpanda 브로커로 테스트하는가? (Mock 아님)
□ 동적 포트 할당을 사용하는가?
□ UUID로 고유한 토픽/그룹을 사용하는가?
□ Thread.sleep() 대신 Awaitility를 사용하는가?
□ @BeforeEach로 테스트 데이터를 초기화하는가?
□ 비동기 조건을 명확히 정의했는가?
□ 성공 경로와 실패 경로를 모두 테스트하는가?
□ 타임아웃 설정이 적절한가? (너무 짧거나 길지 않은가)
```

### 8.2 단위 테스트 체크리스트

```
□ 외부 의존성을 Mock했는가?
□ 테스트당 하나의 논리만 검증하는가?
□ Edge case를 포함했는가?
□ 테스트 이름이 Given-When-Then 구조인가?
□ 1초 이내에 완료되는가?
```

### 8.3 E2E 테스트 체크리스트

```
□ REST API 엔드포인트를 호출하는가?
□ MockMvc를 사용하는가?
□ HTTP 상태 코드를 검증하는가?
□ 응답 바디의 JSON 구조를 검증하는가?
□ 예상 실패 케이스를 포함하는가?
```

---

## 9. CI/CD 통합 설정

### 9.1 gradle.properties (Testcontainers Reuse)

```properties
# Testcontainers 컨테이너 재사용 (CI 속도 개선)
testcontainers.reuse.enable=true

# DockerCompose 사용 시
testcontainers.docker.compose.version=1.29.2
```

### 9.2 GitHub Actions Workflow

```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      docker:
        image: docker:dind
        options: >-
          --privileged
          --health-cmd="docker ps"
          --health-interval=10s

    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Run Tests
        run: ./gradlew test --info

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: build/test-results/
```

---

## 10. 성능 튜닝 팁

### 10.1 테스트 실행 속도 개선

```bash
# 1. 병렬 테스트 실행
./gradlew test --max-workers=4

# 2. Testcontainers 컨테이너 재사용
# gradle.properties에서 testcontainers.reuse.enable=true

# 3. 폴링 간격 최적화
await()
    .atMost(Duration.ofSeconds(5))
    .pollInterval(Duration.ofMillis(50))  // 50ms로 조정
    .untilAsserted(() -> { });

# 4. 불필요한 @DirtiesContext 제거
```

### 10.2 RedPanda 컨테이너 크기 제한

```java
// 메모리 제한 설정
@Container
static final RedpandaContainer REDPANDA =
    new RedpandaContainer("docker.redpanda.com/redpandadata/redpanda:v25.3.6")
        .withCreateContainerCmdModifier(cmd ->
            cmd.getHostConfig()
                .withMemory(512 * 1024 * 1024)  // 512MB
                .withMemorySwap(512 * 1024 * 1024));
```

---

## 11. 관련 문서

- [08. 에러 핸들링 비교](./08-error-handling-comparison.md)
- [06. JSON → Avro](../logic-changes/06-json-manual-to-avro-schema-registry.md)
- [13. 성능 기대치](./13-performance-expectations.md)
- [Spring Kafka Testing 공식 문서](https://spring.io/projects/spring-kafka)
- [Testcontainers 공식 문서](https://www.testcontainers.org/)
- [Apache Kafka 트랜잭션](https://kafka.apache.org/documentation/#semantics)

---

## 12. 학습 로드맵

```
Week 1: 기초
├─ AbstractKafkaTest 이해
├─ @Testcontainers 어노테이션
└─ 첫 번째 통합 테스트 작성

Week 2: 심화
├─ Awaitility 패턴 마스터
├─ 복수 Consumer 테스트
└─ 에러 시나리오 테스트

Week 3: 고급
├─ 트랜잭션 테스트
├─ DLQ 처리
└─ CI/CD 통합

Week 4: 실무
├─ 성능 튜닝
├─ 플래키 테스트 해결
└─ 팀 표준화
```

---

**다음 단계:**

1. `AbstractKafkaTest` 기반으로 첫 번째 통합 테스트 작성
2. `MessageStatusServiceTest` 예시 코드 실행 및 수정
3. `TransactionalProducerTest`의 TODO 항목 구현
4. 로컬에서 `./gradlew test` 실행 및 검증
5. CI/CD 파이프라인에 테스트 추가
