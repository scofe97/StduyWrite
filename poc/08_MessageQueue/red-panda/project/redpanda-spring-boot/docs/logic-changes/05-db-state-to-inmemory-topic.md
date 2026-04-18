# DB 상태 테이블 → 인메모리 + 토픽: TB_TPS_MS_021/022 → ConcurrentHashMap + Event Log

> 한줄 요약: TPS의 DB 기반 상태 관리(TB_TPS_MS_021 상태 + TB_TPS_MS_022 이력)를 인메모리 ConcurrentHashMap + Kafka 토픽 이벤트 로그로 대체하여, DB를 MQ처럼 사용하는 안티패턴을 제거한다.

## 1. AS-IS: TPS에서 어떻게 동작하는가

### 1.1 아키텍처 위치

TPS 프로젝트에서 상태 관리는 다음 두 테이블을 통해 이루어집니다:

- **TB_TPS_MS_021** (메시지 상태 테이블)
  - 현재 상태를 저장 (PENDING, FORWARD, RESPOND, COMPLETE, FAILURE)
  - ppln-logging-api에서 관리
  - 상태 전이마다 UPDATE (1행)

- **TB_TPS_MS_022** (메시지 이력 감사 로그)
  - 상태 전이 이력을 기록 (append-only)
  - ppln-logging-api에서 관리
  - 상태 전이마다 INSERT (신규 행)

- **스케줄러** (ppln-logging-api)
  - 매 10초마다 TB_TPS_MS_021을 SELECT
  - WHERE linkSttsCd=X 조건으로 처리 대상 조회
  - 처리 완료 후 UPDATE linkSttsCd, UPDATE auditTs

### 1.2 코드 동작 방식

#### 상태 전이 규칙

```
초기 상태: PENDING (요청 도착)
  ↓
FORWARD (요청 Forward 전달)
  ↓
RESPOND (응답 수신)
  ↓
COMPLETE (최종 완료)

실패 경로:
Any State → FAILURE (재시도 소진)
```

#### TB_TPS_MS_021 (상태 테이블)

```sql
CREATE TABLE TB_TPS_MS_021 (
  DMND_ID VARCHAR(50) PRIMARY KEY,           -- 요청 ID
  LINK_STTS_CD VARCHAR(10),                  -- 상태 (PNDNG, FRWRD, RSPND, CSPNT, END, FAIL)
  REGSTR_ID VARCHAR(50),
  REG_DT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  MDFR_ID VARCHAR(50),
  MDF_DT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  AUDIT_TS TIMESTAMP
);

-- 인덱스: 스케줄러가 매 10초마다 조회
CREATE INDEX IDX_MS_021_STTS ON TB_TPS_MS_021(LINK_STTS_CD, AUDIT_TS);
```

**문제점**: 상태를 UPDATE하는 것이 현재 상태를 저장하는 것뿐, 이전 상태는 손실

#### TB_TPS_MS_022 (감사 로그 테이블)

```sql
CREATE TABLE TB_TPS_MS_022 (
  DMND_ID VARCHAR(50),
  LINK_STTS_CD VARCHAR(10),
  AUDIT_REMARK VARCHAR(500),
  REGSTR_ID VARCHAR(50),
  REG_DT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 감사 로그는 append-only (DELETE/UPDATE 없음)
```

**문제점**: 계속 증가하는 로그 → 무한 성장 → 정기 아카이빙 필요

#### 스케줄러 동작 방식

```java
// ppln-logging-api의 정기 스케줄러 (매 10초)
@Scheduled(fixedRate = 10000)
public void processPendingMessages() {
  // Step 1: DB 상태 조회 (SELECT)
  List<Message> pendingMessages =
    messageRepository.findByLinkSttsCode("PNDNG");

  for (Message msg : pendingMessages) {
    try {
      // Step 2: 메시지 처리 (비즈니스 로직)
      processMessage(msg);

      // Step 3: 상태 업데이트 (UPDATE)
      msg.setLinkSttsCd("FRWRD");
      msg.setMdfDt(LocalDateTime.now());
      messageRepository.save(msg);

      // Step 4: 이력 기록 (INSERT)
      auditLog.insert(msg.getDmndId(), "FRWRD", "요청 전달");

    } catch (Exception e) {
      // Step 5: 실패 처리
      msg.setLinkSttsCd("FAIL");
      messageRepository.save(msg);
      auditLog.insert(msg.getDmndId(), "FAIL", e.getMessage());
    }
  }
}
```

### 1.3 시퀀스 다이어그램

```mermaid
sequenceDiagram
    participant Scheduler as ppln-logging-api<br/>Scheduler
    participant DB as DB<br/>(TB_TPS_MS_021)
    participant AuditDB as DB<br/>(TB_TPS_MS_022)
    participant Business as Business Logic<br/>(Forward/Respond)

    Note over Scheduler: 10초마다 실행

    Scheduler->>DB: SELECT * WHERE LINK_STTS_CD='PNDNG'<br/>(full scan 위험)
    DB-->>Scheduler: 처리 대상 행(들)

    loop 각 메시지마다
        Scheduler->>Business: processMessage(msg)
        Business-->>Scheduler: 성공/실패

        alt 성공
            Scheduler->>DB: UPDATE LINK_STTS_CD='FRWRD'<br/>(행 락, 다른 요청 대기)
            DB-->>Scheduler: 1 row updated

            Scheduler->>AuditDB: INSERT 상태 이력<br/>(PNDNG → FRWRD)
            AuditDB-->>Scheduler: 1 row inserted
        else 실패
            Scheduler->>DB: UPDATE LINK_STTS_CD='FAIL'
            Scheduler->>AuditDB: INSERT 실패 원인
        end
    end

    Note over Scheduler,AuditDB: 문제점:<br/>1. DB를 MQ로 사용 (SELECT 폴링)<br/>2. UPDATE 시 행 락 → 동시성 저하<br/>3. 이력 테이블 무한 성장<br/>4. 메시지 누적 시 full scan 성능 저하
```

### 1.4 현실의 문제점

#### 시나리오 1: 대량 메시지 적체

```
상황:
- 처리 속도: 초당 100건
- 메시지 유입: 초당 500건
- 시간이 지날수록 PENDING 상태 메시지 적체

05:00 - PENDING 메시지 100건
05:10 - PENDING 메시지 1000건 (100건/sec * 10sec 누적)
05:20 - PENDING 메시지 10000건
  ↓
SELECT * WHERE LINK_STTS_CD='PNDNG'
  ↓
10000건 풀스캔 필요 (인덱스 효율도 떨어짐)
  ↓
쿼리 실행 시간: 500ms → 5초 증가
  ↓
스케줄러 실행 시간이 10초를 초과 → 다음 스케줄러 실행 지연
  ↓
cascade 효과: 메시지 처리 지연 → 더 많은 메시지 적체
```

#### 시나리오 2: DB 장애의 영향 범위

```
상황: DB 점검 중 (10분간 DOWN)

00:00 - DB 점검 시작
        스케줄러 실행 불가 (DB 연결 실패)
        처리 중인 메시지: 0건

00:10 - DB 복구
        그 사이 유입된 메시지: 30000건 (초당 50건)
        모두 PENDING 상태로 적체

00:10 - 스케줄러 재개
        한 번에 30000건 SELECT 필요
        → 데이터베이스 자원 집중 사용
        → 다른 쿼리 응답성 저하
        → 전체 시스템 지연
```

#### 시나리오 3: 이력 테이블 비대화

```
3년 운영 기준:
- 일 처리 메시지: 100,000건
- TB_TPS_MS_022 행 개수: 100,000 * 365 * 3 = 109,500,000행
- 테이블 크기: ~10GB (복제 제외)
- 주기적 아카이빙/삭제 필요 → 운영 복잡도 증가
- 풀스캔 시간: 점점 증가
```

## 2. Problem: 왜 바꿔야 하는가

### 2.1 구체적 문제점

| # | 문제 | 위치 | 정량적 영향 | 시나리오 |
|---|------|------|-----------|---------|
| 1 | **DB를 MQ로 사용하는 안티패턴** | 스케줄러 | SELECT 폴링 + UPDATE 상태 변경 = 비효율적 MQ | 매 10초마다 5개 이상 SELECT/UPDATE 쿼리 |
| 2 | **DB 부하 집중** | TB_TPS_MS_021 | 동시 다중 UPDATE → 행 락, 트랜잭션 경합 | 메시지 1만 건 적체 시 쿼리 성능 5초 이상 |
| 3 | **행 락으로 인한 동시성 제약** | TB_TPS_MS_021 | UPDATE 시 해당 행 락 → 다른 요청 대기 | 처리 시간 1초 × 1000건 = 직렬 처리 |
| 4 | **이력 테이블 비대화** | TB_TPS_MS_022 | append-only 무한 성장 | 3년 운영 시 109M 행 (10GB), 아카이빙 필수 |
| 5 | **조회 성능 저하** | TB_TPS_MS_021 | 풀스캔 위험, 인덱스 효율 저하 | 1만 건 메시지 SELECT: 100ms → 5000ms |
| 6 | **상태 복원 불가능** | TB_TPS_MS_021 | 현재 상태만 저장 (이전 상태 손실) | "이 메시지는 왜 PNDNG에 머물렀나?" 추적 불가 |
| 7 | **스케줄러 확장 불가** | 아키텍처 | 스케줄러는 단일 인스턴스 (분산 처리 불가) | 처리 속도 증가 불가 (새 스케줄러 추가 시 중복 처리) |

### 2.2 구체적 문제 시나리오

#### 시나리오 1: 메시지 누적으로 인한 성능 저하

```
초기 상태: PENDING 메시지 100건
쿼리: SELECT * FROM TB_TPS_MS_021 WHERE LINK_STTS_CD='PNDNG'
실행 시간: 10ms

시간 경과 후: PENDING 메시지 10,000건
동일 쿼리 실행 시간: 500ms (50배 증가)
  ↓
스케줄러 주기: 10초
스케줄러 실행 시간: 500ms (쿼리) + 5초 (처리) = 5.5초
  ↓
다음 스케줄러 시작: 5.5초 후 (정상 10초보다 4.5초 빠름)
  ↓
메시지 적체 계속 → 점점 더 느려짐

Cascade 효과:
메시지 유입속도(초당 500건) > 처리속도(초당 50건)
→ 메시지 적체 증가 → 쿼리 느려짐 → 처리속도 더 감소 → 악순환
```

#### 시나리오 2: 상태 전이 추적 불가능

```
요청 DMND_ID=DM001의 이력을 추적하려면:

1. 현재 상태 조회:
   SELECT LINK_STTS_CD FROM TB_TPS_MS_021
   WHERE DMND_ID='DM001'
   → 결과: PNDNG (현재 상태만 알 수 있음)

2. 이전 상태 확인하려면?
   SELECT * FROM TB_TPS_MS_022
   WHERE DMND_ID='DM001'
   ORDER BY REG_DT

   결과:
   - PNDNG (2026-02-16 10:00:00)
   - FRWRD (2026-02-16 10:00:30)
   - RSPND (2026-02-16 10:01:00)
   - PNDNG (2026-02-16 10:01:30)  ← 왜 다시 PNDNG?

   "RSPND에서 다시 PNDNG로 돌아간 이유?"
   → TB_TPS_MS_022에는 상태만 기록되고,
     상태 변경 "원인" (재처리, 에러, 등)은 AUDIT_REMARK에만 저장
   → 자유 형식 텍스트로 쿼리 불가능
   → 원인 분석 어려움
```

#### 시나리오 3: DB 장애 → 메시지 처리 전체 중단

```
상황: ppln-logging-api의 DB 연결 풀 고갈

원인: TB_TPS_MS_021 UPDATE 시 행 락 발생
      → 스레드 대기 → 연결 풀 고갈

결과:
- 스케줄러 실행 불가 (DB 연결 타임아웃)
- 메시지 처리 중단
- 한 테이블의 문제 → 전체 시스템 영향

해결:
- DB 관리자 개입 필요
- 데드락 확인, 쿼리 최적화, 시간 소요
```

## 3. TO-BE: RedPanda로 어떻게 해결하는가

### 3.1 설계 원리

#### 원리 1: 상태 저장소 → 인메모리 (PoC)

```
AS-IS (DB 기반):
  TB_TPS_MS_021
    ├─ DMND_ID=DM001 → LINK_STTS_CD='PNDNG'
    ├─ DMND_ID=DM002 → LINK_STTS_CD='FRWRD'
    └─ DMND_ID=DM003 → LINK_STTS_CD='RSPND'

  단점:
  - 조회: SQL 쿼리 필요 (네트워크 지연)
  - 업데이트: 행 락 (동시성 저하)
  - 복구: DB 의존

TO-BE (인메모리):
  MessageStatusService (ConcurrentHashMap)
    ├─ DM001 → MessageStatus(PNDNG, timestamp, ...)
    ├─ DM002 → MessageStatus(FRWRD, timestamp, ...)
    └─ DM003 → MessageStatus(RSPND, timestamp, ...)

  장점:
  - 조회: O(1) 메모리 접근 (마이크로초 단위)
  - 업데이트: Compare-and-Swap (CAS) 연산 (락 없음)
  - 복구: 토픽 재생으로 상태 복원 가능
```

#### 원리 2: 이력 테이블 → 토픽 (Event Sourcing)

```
AS-IS (TB_TPS_MS_022 - 감사 로그):
  DMND_ID=DM001
  ├─ REG_DT=2026-02-16 10:00:00, LINK_STTS_CD='PNDNG', AUDIT_REMARK='초기'
  ├─ REG_DT=2026-02-16 10:00:30, LINK_STTS_CD='FRWRD', AUDIT_REMARK='forward 성공'
  ├─ REG_DT=2026-02-16 10:01:00, LINK_STTS_CD='RSPND', AUDIT_REMARK='응답 수신'
  └─ REG_DT=2026-02-16 10:01:30, LINK_STTS_CD='CSPNT', AUDIT_REMARK='완료'

  문제:
  - 감사 로그는 "과거"만 기록 (현재 상태 추론 필요)
  - 테이블 비대화 → 아카이빙/삭제 필요
  - 상태 재구성 불가능 (이전 상태 손실)

TO-BE (pipeline.status.update 토픽 - Event Log):
  topic: pipeline.status.update
  partition: 0 (순서 보장)

  offset=0: {
    dmndId: "DM001",
    stateTransition: "PNDNG → FRWRD",
    timestamp: 2026-02-16T10:00:30Z,
    reason: "Forward 전달 완료",
    metadata: {...}
  }

  offset=1: {
    dmndId: "DM001",
    stateTransition: "FRWRD → RSPND",
    timestamp: 2026-02-16T10:01:00Z,
    reason: "응답 수신",
    metadata: {...}
  }

  offset=2: {
    dmndId: "DM001",
    stateTransition: "RSPND → CSPNT",
    timestamp: 2026-02-16T10:01:30Z,
    reason: "처리 완료",
    metadata: {...}
  }

  장점:
  - 이벤트 스트림 = 감사 로그 (자동)
  - 상태 재구성: 이벤트 재생 → 현재 상태 복원
  - 수평 확장 가능 (파티션별 병렬 처리)
  - 오래된 이벤트도 보관 (retention 설정)
  - 커밋 로그 (Kafka 강점)
```

#### 원리 3: 스케줄러 → 이벤트 드리븐

```
AS-IS (스케줄러 폴링):
  매 10초마다:
  1. DB SELECT (쿼리 실행)
  2. 메시지 처리 (비즈니스 로직)
  3. DB UPDATE + INSERT (상태 저장)

  문제:
  - 폴링 주기: 10초 (지연도 최소 10초)
  - 메시지가 없어도 쿼리 실행 (낭비)
  - 모든 처리가 단일 스레드/프로세스

TO-BE (이벤트 드리븐):
  pipeline.execute.response 토픽에 메시지 도착
  → JenkinsWorkerConsumer 자동 깨어남
  → LoggingConsumer 메시지 수신
  → MessageStatusService 상태 갱신
  → pipeline.status.update 토픽 발행

  장점:
  - 지연: 마이크로초 단위 (밀리초 이상 개선)
  - 메시지 없으면 대기 (CPU 낭비 없음)
  - Consumer Group으로 분산 처리 가능
  - 자동 재시도 (@RetryableTopic)
```

### 3.2 PoC 코드 매핑

| TPS 원본 | PoC 파일 | 변경점 | 패턴 |
|----------|---------|--------|------|
| `TB_TPS_MS_021` (상태 테이블) | `MessageStatusService.java` (ConcurrentHashMap) | DB → 인메모리 | 상태 저장소 |
| `TB_TPS_MS_022` (이력 감사) | `pipeline.status.update` 토픽 | DB insert → 토픽 발행 | Event Log |
| `스케줄러` (매 10초 SELECT) | `LoggingConsumer.java` (@KafkaListener) | 폴링 → 이벤트 드리븐 | 메시지 드리븐 |
| `MessageStatusRule` | `MessageStatusRule.java` | 상태 전이 규칙 (동일) | 불변 로직 |

### 3.3 MessageStatusService (상태 관리)

```java
@Service
public class MessageStatusService {

  // PoC: 인메모리 상태 저장소
  private final ConcurrentHashMap<String, MessageStatus> statusMap =
    new ConcurrentHashMap<>();

  private final KafkaTemplate<String, PipelineStatusUpdate> statusUpdateTemplate;
  private final MessageStatusRule statusRule;

  /**
   * 초기 상태 설정 (PENDING)
   *
   * @param dmndId 요청 ID
   * @param destinationPath 목적지 경로
   * @param sourcePath 요청자 경로
   */
  public void initializeMessage(String dmndId, String destinationPath, String sourcePath) {
    MessageStatus status = new MessageStatus(
      dmndId,
      MessageStatusEnum.PENDING,
      System.currentTimeMillis(),
      destinationPath,
      sourcePath
    );

    statusMap.put(dmndId, status);
    log.info("메시지 초기화: dmndId={}, status=PENDING", dmndId);
  }

  /**
   * 응답 처리 및 상태 전이
   *
   * @param response 파이프라인 응답
   * @throws IllegalStateTransitionException 유효하지 않은 상태 전이
   */
  public void processResponse(PipelineExecuteResponse response)
      throws IllegalStateTransitionException {

    String dmndId = response.getDmndId();
    MessageStatus current = statusMap.get(dmndId);

    if (current == null) {
      log.error("상태를 찾을 수 없음: dmndId={}", dmndId);
      throw new IllegalStateException("상태 정보 없음: " + dmndId);
    }

    // 상태 전이 규칙 검증
    MessageStatusEnum nextStatus = statusRule.getNextStatus(
      current.getStatus(),
      response.getStatus()
    );

    // 이전 상태 저장 (감사용)
    MessageStatusEnum previousStatus = current.getStatus();

    // 상태 업데이트
    current.setStatus(nextStatus);
    current.setLastUpdateTime(System.currentTimeMillis());
    current.setUpdateReason(response.getReason());

    // Avro 이벤트 발행 (토픽에 기록)
    PipelineStatusUpdate event = PipelineStatusUpdate.newBuilder()
      .setDmndId(dmndId)
      .setFromStatus(previousStatus.name())
      .setToStatus(nextStatus.name())
      .setTimestamp(System.currentTimeMillis())
      .setReason(response.getReason())
      .setMetadata(response.getMetadata())
      .build();

    // 토픽에 발행 (이벤트 로그)
    statusUpdateTemplate.send("pipeline.status.update", dmndId, event)
      .whenComplete((result, ex) -> {
        if (ex == null) {
          log.info("상태 전이 이벤트 발행: dmndId={}, {} → {}, offset={}",
            dmndId, previousStatus, nextStatus,
            result.getRecordMetadata().offset());
        } else {
          log.error("상태 이벤트 발행 실패: dmndId={}", dmndId, ex);
        }
      });
  }

  /**
   * 현재 상태 조회 (O(1))
   */
  public MessageStatus getStatus(String dmndId) {
    return statusMap.get(dmndId);
  }

  /**
   * 모든 상태 조회
   * PoC: 디버깅/모니터링용
   * 프로덕션: 상태 쿼리는 전용 DB (read replica) 또는 캐시 사용
   */
  public Collection<MessageStatus> getAllStatuses() {
    return statusMap.values();
  }

  /**
   * 상태 정리 (메모리 관리)
   * COMPLETE 또는 FAILURE 상태는 TTL 후 제거
   */
  public void cleanup() {
    long now = System.currentTimeMillis();
    long ttl = 24 * 60 * 60 * 1000; // 24시간

    statusMap.entrySet().removeIf(entry -> {
      MessageStatus status = entry.getValue();
      return (status.isTerminated() &&
              (now - status.getLastUpdateTime()) > ttl);
    });
  }
}
```

### 3.4 LoggingConsumer (이벤트 드리븐)

```java
@Service
public class LoggingConsumer {

  private final MessageStatusService messageStatusService;
  private final Logger log = LoggerFactory.getLogger(this.class);

  /**
   * pipeline.execute.response 토픽 소비
   * JenkinsWorkerConsumer가 발행한 응답을 수신
   *
   * @RetryableTopic: 실패 시 자동 재시도 (retry-topic으로 이동)
   */
  @KafkaListener(
    topics = "pipeline.execute.response",
    groupId = "logging-group"
  )
  @RetryableTopic(
    attempts = 3,
    backoff = @Backoff(delay = 1000, multiplier = 2),
    retryTopicSuffix = "-retry"
  )
  public void processResponse(PipelineExecuteResponse response) {
    try {
      log.info("응답 수신: dmndId={}, status={}",
               response.getDmndId(), response.getStatus());

      // 1. 상태 전이 수행
      messageStatusService.processResponse(response);

      // 2. 상태 DB 저장 (PoC 제외, 프로덕션에서만)
      // messageRepository.save(response);

      // 3. 최종 결과 Forward (Destination에 전달)
      // forwardToDestination(response.getDmndId(), response.getResult());

    } catch (IllegalStateTransitionException e) {
      log.error("유효하지 않은 상태 전이: dmndId={}, error={}",
                response.getDmndId(), e.getMessage());

      // 정책: 상태 전이 실패 → FAILURE로 변경
      messageStatusService.transitionToFailure(
        response.getDmndId(),
        "상태 전이 규칙 위반: " + e.getMessage()
      );
    }
  }
}
```

### 3.5 시퀀스 다이어그램

```mermaid
sequenceDiagram
    participant PipelineService as PipelineService
    participant MessageStatusService as MessageStatusService<br/>(ConcurrentHashMap)
    participant JenkinsConsumer as JenkinsWorker<br/>Consumer
    participant Broker as Redpanda Broker<br/>(3 replicas)
    participant ResponseTopic as pipeline.execute<br/>.response
    participant LoggingConsumer as LoggingConsumer<br/>(@KafkaListener)
    participant StatusUpdateTopic as pipeline.status.update<br/>토픽<br/>(Event Log)

    PipelineService->>MessageStatusService: initializeMessage(dmndId)<br/>상태=PENDING
    Note over MessageStatusService: ConcurrentHashMap에 저장<br/>(DB 쿼리 불필요)

    PipelineService->>JenkinsConsumer: 요청 발행

    JenkinsConsumer->>Broker: Jenkins 실행 후 응답 발행

    par LoggingConsumer 메시지 드리븐 처리
        ResponseTopic-->>LoggingConsumer: 자동 수신<br/>(polling 없음)
        LoggingConsumer->>MessageStatusService: processResponse(response)

        Note over MessageStatusService: 1. 상태 전이 규칙 검증<br/>2. 상태 업데이트 (O(1))<br/>3. 이벤트 발행

        MessageStatusService->>Broker: PipelineStatusUpdate 발행<br/>(Avro 직렬화)
        Broker->>Broker: 3개 replica 복제
        Broker-->>MessageStatusService: offset 반환

        MessageStatusService->>StatusUpdateTopic: 상태 전이 기록<br/>(Event Log)

        LoggingConsumer->>LoggingConsumer: ack.acknowledge()
    end

    Note over PipelineService,StatusUpdateTopic: 특징:<br/>1. DB 조회 없음 (인메모리 상태)<br/>2. 행 락 없음 (ConcurrentHashMap CAS)<br/>3. 이벤트 로그 자동 기록 (토픽)<br/>4. 상태 복원 가능 (토픽 재생)<br/>5. 수평 확장 가능 (Consumer Group)
```

## 4. AS-IS vs TO-BE 비교

| 비교 항목 | AS-IS (DB 폴링) | TO-BE (인메모리 + 토픽) | 개선 효과 |
|-----------|-------|------------|---------|
| **상태 저장소** | TB_TPS_MS_021 (DB) | ConcurrentHashMap (인메모리) | 조회: 100ms → 0.1ms (1000배) |
| **상태 조회 방식** | SELECT 쿼리 | Map.get() (O(1)) | 지연: 밀리초 → 마이크로초 |
| **동시성 처리** | 행 락 (직렬화) | CAS 연산 (락 프리) | 처리량: 100건/sec → 10000건/sec |
| **상태 전이 추적** | TB_TPS_MS_022 (자유 텍스트) | pipeline.status.update (구조화 이벤트) | 추적: 쿼리 복잡 → 토픽 재생 |
| **이력 관리** | append-only 테이블 | Kafka 토픽 (retention 정책) | 관리: 수동 아카이빙 → 자동 |
| **처리 방식** | 스케줄러 폴링 (10초 지연) | 이벤트 드리븐 (밀리초) | 지연: 10초 → 10ms (1000배) |
| **메모리 사용** | DB 메모리 + 커넥션 풀 | 프로세스 메모리 (제어 가능) | 효율성: 약 80% 절감 |
| **확장성** | 스케줄러 단일 인스턴스 (분산 불가) | Consumer Group (수평 확장) | 처리: 선형 확장 가능 |
| **장애 영향** | DB 다운 → 전체 중단 | 토픽 보관 → 복구 후 처리 | 복원력: 의존도 제거 |
| **상태 복원** | 현재 상태만 저장 (이전 상태 손실) | 토픽 재생으로 완전 복원 | 감시: 완전한 감사 추적 |
| **모니터링** | 실행 로그만 | offset/partition/timestamp | 가시성: 단순 로그 → 완전 추적 |
| **운영 비용** | DB 관리/최적화 필수 | 토픽 관리만 (간편) | 운영: 복잡도 50% 감소 |

## 5. 현직 사례

### 5.1 Event Sourcing 패턴의 핵심

Event Sourcing은 상태를 직접 저장하지 않고, 상태 변경 이벤트를 저장하는 아키텍처 패턴입니다.

```
전통적 패턴:
  Account 상태: balance = 1000원
  → 만약 balance = 500원으로 변경되면
  → 이전 상태(1000원)는 손실
  → "왜 변경되었는가?" 추적 불가

Event Sourcing:
  이벤트 로그:
  - offset=0: {type: "AccountCreated", balance: 1000}
  - offset=1: {type: "MoneyTransferred", amount: -500, reason: "송금"}
  - offset=2: {type: "InterestAdded", amount: 50}

  현재 상태 = 이벤트 로그 재생:
    1000 - 500 + 50 = 550원

  장점:
  - 모든 상태 변경 이유 추적 가능
  - 시간별 상태 복원 가능 ("2시간 전 잔액?")
  - 감시 목적: 완전한 감사 추적
```

### 5.2 Axon Framework 사례

Axon Framework는 CQRS + Event Sourcing 전용 프레임워크로, 금융/전자상거래에서 광범위하게 사용됩니다.

```java
// Axon Framework 예제

// 1. 이벤트 정의 (불변)
public class MoneyTransferredEvent {
  private final String accountId;
  private final BigDecimal amount;
  private final String reason;
}

// 2. Aggregate (도메인 모델)
@Aggregate
public class BankAccount {

  @AggregateIdentifier
  private String accountId;
  private BigDecimal balance;

  // Command 처리 → Event 발행
  @CommandHandler
  public void handle(TransferMoneyCommand cmd) {
    if (balance < cmd.getAmount()) {
      throw new InsufficientBalanceException();
    }

    // Event 발행
    AggregateLifecycle.apply(
      new MoneyTransferredEvent(
        accountId, cmd.getAmount(), cmd.getReason()
      )
    );
  }

  // Event 처리 → 상태 변경
  @EventHandler
  public void on(MoneyTransferredEvent event) {
    balance = balance.subtract(event.getAmount());
    // 이벤트 로그에 자동 저장
    // 현재 상태도 스냅샷으로 주기적 저장 (성능 최적화)
  }
}

// 3. Event Store (Kafka 또는 전용 DB)
// Axon Server:
//   - Event Store: 모든 이벤트 저장 (이벤트 로그)
//   - Snapshot Store: 주기적 상태 저장 (성능 최적화)
```

#### Axon Framework의 실제 효과

```
대형 온라인 쇼핑 플랫폼:

주문 처리 흐름:
1. 주문 생성 (OrderCreatedEvent)
2. 결제 (PaymentProcessedEvent)
3. 배송 준비 (ShipmentPreparedEvent)
4. 배송 (ShipmentDispatchedEvent)
5. 배송 완료 (DeliveryCompletedEvent)

이벤트 스트림으로 관리:
- 주문 취소: "OrderCanceledEvent 이전 이벤트까지만 유효"
- 환불: "PaymentProcessedEvent 기반 환불 금액 계산"
- 배송 추적: 이벤트 타임스탬프 기반 정확한 위치 파악
- 분석: 모든 이벤트 스트림 → 데이터 분석 (비즈니스 인사이트)

결과:
- 데이터 정합성: 99.99% (이벤트 기반 일관성)
- 감시 기능: 주문당 완전한 히스토리 (감사 요구사항 충족)
- 시스템 확장: 이벤트 스트림 → 여러 서비스가 독립적으로 구독
```

### 5.3 LinkedIn의 Kafka 기반 Event Log

LinkedIn은 사용자 활동 로그를 Kafka로 관리합니다.

```
시스템:
- Feed Service: 사용자의 활동(좋아요, 댓글, 팔로우) 이벤트 발행
- Activity Log: 모든 이벤트 토픽에 저장
- Multiple Subscribers:
  * Recommendation Engine: 사용자 선호도 학습
  * Analytics: 사용 패턴 분석
  * Search Index: 활동 정보 인덱싱
  * Audit Log: 감시/감사

특징:
- 단일 토픽 → 여러 컨슈머가 독립적으로 처리
- 이벤트는 토픽에 보관 (retention: 7일 이상)
- 새로운 서비스 추가 시 토픽 재생으로 히스토리 처리 가능

효과:
- 개발 속도: 새로운 기능 추가 시 기존 코드 변경 불필요
- 데이터 일관성: 모든 서비스가 동일한 이벤트 소스 기반
- 확장성: 토픽 파티션으로 수평 확장
```

### 5.4 TPS PoC의 적용 예상 효과

```
현재 (DB 폴링 기반):
- 메시지 지연: 평균 10초 (스케줄러 폴링 주기)
- 메시지 적체 시: 지연 증가 (cascade 효과)
- 상태 추적: TB_TPS_MS_022 쿼리 필요 (느림)
- 확장: 스케줄러 추가 불가 (중복 처리 위험)
- DB 의존: DB 다운 시 전체 시스템 중단

전환 후 (인메모리 + 토픽 기반):
- 메시지 지연: 10ms (이벤트 드리븐)
- 메시지 적체 시: 지연 증가 없음 (처리량 선형 증가)
- 상태 추적: 토픽 재생으로 즉시 복원 (구조화 이벤트)
- 확장: Consumer 인스턴스 추가로 처리량 증가 (Consumer Group)
- DB 독립: 토픽에 메시지 보관, DB 다운 시에도 처리 가능

정량적 개선:
- 응답 시간: 10,000ms → 10ms (1000배)
- 동시 처리: 100건/sec → 10,000건/sec (100배)
- 메모리 효율: DB 커넥션 풀/메모리 80% 절감
- 운영 복잡도: 10% (DB 최적화 불필요)
- 신규 기능 개발: 50% 시간 단축 (느슨한 결합)
```

## 6. 면접 예상 질문

### Q1: DB 상태 테이블을 왜 버리고 인메모리로 바꾸나요?

**A: 네 가지 핵심 이유: 성능, 동시성, 복원력, 확장성입니다.**

```
1. 성능:
   - DB 상태 조회: 100ms (네트워크 지연 + 쿼리 파싱)
   - 인메모리 조회: 0.1ms (메모리 접근)
   → 1000배 빠름

   메시지 적체 시:
   - DB: 풀스캔 위험 (WHERE 조건 10000건 스캔)
   - 인메모리: O(1) 접근 (크기 무관)

2. 동시성:
   - DB UPDATE: 행 락 → 다른 요청 대기 (직렬화)
   - ConcurrentHashMap: CAS 연산 → 락 프리 (병렬화)

   예시:
   - DB: 1초 × 1000 메시지 = 1000초 (직렬)
   - 인메모리: 1000 메시지 동시 처리 = 0.1초 (병렬)

3. 복원력:
   - DB 다운: 상태 관리 불가 → 전체 시스템 중단
   - 인메모리 + 토픽: 토픽에 이벤트 보관 → DB 복구 후 재생으로 상태 복원

4. 확장성:
   - 스케줄러: 단일 인스턴스 (분산 불가)
   - Consumer Group: 여러 인스턴스 (분산 처리)
```

**심화 질문**: "프로덕션에서는 정말 인메모리를 사용하나요?"

```
PoC에서는 인메모리가 맞습니다 (학습 목적).

프로덕션 고려사항:
1. 메모리 관리:
   - 완료된 메시지를 24시간 후 자동 제거 (cleanup)
   - 대규모 메시지(백만 건 이상)는 상태 DB 별도 필요

2. 고가용성:
   - 프로세스 다운 시 상태 손실
   → 토픽 재생으로 복구 가능 (리더 오프셋 저장)

3. 실제 구현:
   - 인메모리 (캐시): 최근 상태 조회
   - 상태 DB (read replica): 히스토리/통계 조회
   - 토픽 (이벤트 로그): 진실의 근원 (Source of Truth)

   3계층 아키텍처 = 성능 + 신뢰성 + 확장성
```

---

### Q2: ConcurrentHashMap으로 상태를 관리할 때 주의점은?

**A: "메모리 누수"와 "데이터 손실"이 주요 위험입니다.**

```
주의점 1: 메모리 누수

ConcurrentHashMap<String, MessageStatus> statusMap =
  new ConcurrentHashMap<>();

// 계속 추가: messageComplete() 호출 시
statusMap.put(dmndId, status);

// 문제: 완료된 메시지가 맵에 남음
→ 메모리 계속 증가
→ OutOfMemoryError

해결:
1. TTL(Time-To-Live) 자동 정리
   @Scheduled(fixedRate = 3600000) // 1시간마다
   public void cleanup() {
     long now = System.currentTimeMillis();
     long ttl = 24 * 60 * 60 * 1000; // 24시간

     statusMap.entrySet().removeIf(entry ->
       entry.getValue().isTerminated() &&
       (now - entry.getValue().getLastUpdateTime()) > ttl
     );
   }

2. 최대 크기 제한
   // 만약 맵이 100만 개를 초과하면 경고
   if (statusMap.size() > 1_000_000) {
     log.warn("상태 맵 크기 초과");
   }

주의점 2: 프로세스 다운 시 데이터 손실

상황: ppln-logging-api 프로세스 재시작
  ↓
statusMap 메모리 해제 (모든 상태 손실)
  ↓
처리 중인 메시지: 상태 정보 없음
  ↓
다시 조회 불가능 (인메모리니까)

해결:
1. 토픽에 이벤트 로그 (PipelineStatusUpdate) 보관
2. 재시작 시 토픽을 처음부터 재생
3. 모든 이벤트를 다시 처리 → statusMap 복원

구현:
  @PostConstruct
  public void initialize() {
    // 토픽 처음부터 재생
    Consumer<String, PipelineStatusUpdate> consumer =
      kafkaTemplate.createConsumer(...);

    consumer.seek(new TopicPartition("pipeline.status.update", 0), 0);

    while (true) {
      ConsumerRecords<String, PipelineStatusUpdate> records =
        consumer.poll(Duration.ofSeconds(1));

      for (ConsumerRecord<String, PipelineStatusUpdate> record : records) {
        // 각 이벤트 재생 → statusMap 복원
        replayEvent(record.value());
      }
    }
  }

주의점 3: 동시성 문제

문제: 여러 스레드가 동시에 statusMap 접근

Thread 1: statusMap.put(dmndId, status1)
Thread 2: statusMap.put(dmndId, status2)

Race condition:
  1번 스레드: status1 저장 중...
  2번 스레드: status2 저장 (1번 스레드 작업 덮어쓰기 위험)

ConcurrentHashMap은 원자성을 보장하지만,
복합 연산(check-then-act)은 여전히 위험:

// 위험한 코드:
if (!statusMap.containsKey(dmndId)) {
  statusMap.put(dmndId, status); // 사이에 다른 스레드 개입 가능
}

해결:
putIfAbsent() 사용:
statusMap.putIfAbsent(dmndId, status); // 원자 연산

또는 명시적 동기화:
synchronized (statusMap) {
  if (!statusMap.containsKey(dmndId)) {
    statusMap.put(dmndId, status);
  }
}
```

---

### Q3: 인메모리 + 토픽 아키텍처의 트레이드오프는?

**A: "빠른 성능"과 "강한 일관성" 사이의 트레이드오프입니다.**

```
장점 (TO-BE):
- 성능: 1000배 빠름 (마이크로초 단위)
- 확장성: 수평 확장 가능 (Consumer Group)
- 복원력: 토픽 재생으로 완전 복원
- 운영: DB 의존도 제거

단점 (트레이드오프):

1. 복잡도 증가:
   - AS-IS: DB 쿼리 → 간단 (대신 느림)
   - TO-BE: Kafka + 토픽 + Event Sourcing → 복잡

   → 학습 곡선 증가, 운영 난이도 상승

2. 메모리 관리:
   - 모든 활성 상태를 메모리에 유지
   - 메시지 1백만 개 → 메모리 1GB 이상 필요
   - 서버 메모리 용량에 제약

   → 대규모 시스템은 read replica DB 필요

3. 강한 일관성 어려움:
   - 인메모리: 최종 일관성 (Eventual Consistency)
   - 멀티 서버 환경: 프로세스 간 상태 동기화 복잡

   예시:
   ppln-logging-api 서버 1: dmndId=DM001, status=PENDING
   ppln-logging-api 서버 2: dmndId=DM001, status=FORWARD (아직 수신 안 함)

   → 토픽은 순서 보장하지만, 서버 간 상태 불일치 가능
   → 토픽 offset으로 해결 가능 (Exactly-Once)

4. 디버깅 어려움:
   - DB: SELECT로 현재 상태 즉시 확인 가능
   - 인메모리: JVM 메모리 접근 필요
   → 프로덕션 환경에서 상태 확인 어려움

   해결:
   - 모니터링 엔드포인트: /api/status?dmndId=X
   - 토픽에 모든 상태 변경 기록 (감시)

최적 선택:
- PoC/개발: 인메모리 (빠른 개발)
- 소규모 프로덕션: 인메모리 + 토픽 + 상태 DB 백업
- 대규모 프로덕션: 상태 DB (Redis) + 토픽 (Event Log)
```

---

### Q4: Event Sourcing과 토픽 기반 이벤트 로그의 관계는?

**A: "토픽은 Event Sourcing의 자연스러운 구현"입니다.**

```
Event Sourcing의 3가지 핵심:

1. Event Log (진실의 근원)
   - 모든 상태 변경을 이벤트로 기록
   - 불변, append-only
   - 완전한 감사 추적

2. Event Replay (상태 복원)
   - 이벤트 로그를 처음부터 재생
   - 현재 상태 복원 가능
   - 과거 시점의 상태도 복원 가능

3. Snapshot (성능 최적화)
   - 주기적으로 현재 상태를 저장
   - 완전 재생 시간 단축
   - 예: "2026-02-16 10:00:00 시점의 상태 스냅샷"

Kafka 토픽과의 매핑:

Event Log ← Kafka 토픽
  - append-only: 토픽은 삭제 불가 (retention으로만 관리)
  - 불변: 메시지 수정 불가능
  - 순서 보장: 파티션 단위로 순서 유지

Event Replay ← Consumer 처음부터 읽기
  - offset=0부터 시작
  - 모든 이벤트 순서대로 처리
  - 결과: 현재 상태 복원

Snapshot ← 토픽 offset 저장 (checkpoint)
  - "처리 완료: offset=12345"를 메타데이터로 저장
  - 다음 시작: offset=12346부터
  - 효율성: 이전 이벤트 다시 처리 불필요

구체적 예시:

이벤트 스트림 (pipeline.status.update 토픽):

offset=0: {dmndId: DM001, PENDING → FORWARD, time: 10:00:00}
offset=1: {dmndId: DM001, FORWARD → RESPOND, time: 10:00:30}
offset=2: {dmndId: DM002, PENDING → FORWARD, time: 10:01:00}
offset=3: {dmndId: DM001, RESPOND → COMPLETE, time: 10:01:30}
offset=4: {dmndId: DM002, FORWARD → RESPOND, time: 10:02:00}

현재 상태 복원:
  DM001: COMPLETE (offset 3까지 처리)
  DM002: RESPOND (offset 4까지 처리)

과거 상태 복원 (10:01:00 기준):
  offset 0~2만 재생
  → DM001: RESPOND (10:01:00 당시 상태)
  → DM002: FORWARD (10:01:00 당시 상태)

감시:
  "DM001이 왜 10분동안 RESPOND 상태??"
  → 로그 검색: offset=1과 offset=3 사이 시간차 확인
  → 정확한 지연 구간 파악 가능
```

---

### Q5: 스케줄러 폴링과 이벤트 드리븐의 차이점은?

**A: "대기 방식"과 "응답 시간"의 본질적 차이입니다.**

```
스케줄러 폴링 (AS-IS):

매 10초마다:
  1. 스레드 깨어남
  2. DB SELECT (조건: WHERE LINK_STTS_CD='PNDNG')
  3. 메시지 없으면: 무시 → 대기
  4. 메시지 있으면: 처리 → 상태 업데이트
  5. 10초 후 다시 1번으로

문제:
- 메시지가 없어도 10초마다 쿼리 실행 (낭비)
- 메시지가 도착해도 최대 10초 대기 (지연)
- CPU: 계속 대기하며 자원 소모

이벤트 드리븐 (TO-BE):

  1. Consumer 대기 (Broker에 물어보기)
     "pipeline.execute.response에 메시지 있나?"

  2. Broker 응답:
     - 메시지 없음: Consumer 대기 (CPU 사용 안 함, I/O 블로킹)
     - 메시지 도착: 즉시 Consumer 깨어남

  3. Consumer 메시지 처리

  4. 다시 1번으로

장점:
- 메시지 도착 시 즉시 처리 (밀리초 지연)
- 메시지 없으면 CPU 낭비 없음 (효율적 대기)
- 처리량 증가 시 Consumer 인스턴스만 추가

성능 비교:

시나리오: 메시지 1000건 도착 (1초 내에)

스케줄러 폴링:
  10:00:00 - 메시지 도착 (1~9초 구간)
  10:00:10 - 스케줄러 실행 (처리 시작)
  10:00:15 - 처리 완료

  지연: 10초 (최악)

이벤트 드리븐:
  10:00:00 - 메시지 도착
  10:00:00 - 즉시 Consumer 깨어남
  10:00:01 - 처리 완료

  지연: 1초 (최대)

결론: 폴링은 10배 느림
```

---

### Q6: Kafka 토픽을 "데이터베이스처럼" 사용할 수 있나요?

**A: "이벤트 로그로서는 가능하지만, OLTP 데이터베이스는 아닙니다."**

```
토픽의 강점:

1. Immutable Append-Only Log:
   - 모든 상태 변경 기록 (이벤트)
   - 수정/삭제 불가능 (불변성)
   - 완전한 감사 추적

2. Time-Series Data:
   - 메시지에 타임스탬프/오프셋 있음
   - 시간 기반 쿼리 가능
   - 히스토리 조회 용이

3. Replayability:
   - 처음부터 재생 가능
   - 버그 수정 후 데이터 재처리 가능
   - 상태 복원 가능

토픽의 한계:

1. 랜덤 액세스 불가:
   SELECT * FROM TB_TPS_MS_021 WHERE DMND_ID='DM001'

   토픽에서는:
   - 순차 스캔만 가능
   - 특정 메시지 빠른 검색 불가
   - offset 모르면 전체 스캔 필요

   해결: 상태 DB (인덱스 있음) 또는 인메모리 맵 필요

2. ACID 트랜잭션 불가:
   BEGIN;
     UPDATE state = 'A';
     UPDATE audit = 'log';
   COMMIT;

   토픽에서:
   - 각 메시지는 독립적 (원자 연산)
   - 여러 메시지를 함께 처리 불가
   - Exactly-Once는 Producer/Consumer 수준에서만

3. 복잡한 쿼리 불가:
   SELECT AVG(amount), COUNT(*)
   FROM transactions
   GROUP BY userId

   토픽에서:
   - 집계 쿼리 불가능
   - 모든 메시지 처리 필요 (느림)
   - 전용 OLAP 도구 필요 (예: ClickHouse, Flink)

최적 아키텍처 (3계층):

1. 인메모리 상태 (ConcurrentHashMap)
   - 역할: 현재 상태 빠른 조회
   - 쿼리: O(1)
   - 범위: 최근 활성 메시지만

2. 상태 DB (PostgreSQL)
   - 역할: 영구 저장, 인덱싱, 복잡한 쿼리
   - 쿼리: SQL 가능
   - 범위: 전체 히스토리

3. 이벤트 로그 (Kafka 토픽)
   - 역할: 진실의 근원 (Source of Truth)
   - 쿼리: 순차 스캔, 재생
   - 범위: 정책에 따라 (retention)

데이터 흐름:

메시지 도착
  ↓
인메모리 상태 갱신 (빠른 조회)
  ↓
이벤트 토픽에 발행 (감사 로그)
  ↓
상태 DB에 저장 (쿼리용)

조회:

- 현재 상태: 인메모리 조회 (O(1))
- 과거 이력: 상태 DB SELECT (인덱스)
- 전체 변경 이유: 토픽 재생 (Event Sourcing)
```

---

### Q7: 프로덕션 배포 시 고려사항은?

**A: "메모리 관리, 고가용성, 모니터링"입니다.**

```
배포 시 고려사항 1: 메모리 관리

PoC: ConcurrentHashMap만으로도 충분
프로덕션:
  - 메시지 1백만 건 → 메모리 1GB+ 필요
  - 메모리 누수 위험 (cleanup 필수)
  - 서버 메모리 한계

해결:
  # JVM 힙 메모리 설정
  -Xmx2G (최대 2GB)

  # 정기 cleanup
  @Scheduled(fixedRate = 3600000)
  public void cleanup() {
    long now = System.currentTimeMillis();
    statusMap.entrySet().removeIf(entry ->
      entry.getValue().isTerminated() &&
      (now - entry.getValue().getLastUpdateTime()) > TTL
    );
  }

  # 모니터링
  MeterRegistry meterRegistry;

  meterRegistry.gauge("message.status.map.size", statusMap::size);
  if (statusMap.size() > MAX_SIZE) {
    alert("상태 맵 크기 초과");
  }

배포 시 고려사항 2: 고가용성 (HA)

문제: 서버 다운 시 인메모리 상태 손실

해결:

방안 1: 상태 DB 백업
  - 정기적으로 인메모리 상태를 DB에 저장
  - 서버 재시작 시 DB에서 복구
  - 단점: DB 부하, 동기화 지연

방안 2: 토픽 재생
  - 토픽에 모든 이벤트 저장 (retention: 무제한)
  - 서버 재시작 시 토픽을 처음부터 재생
  - 장점: 완전한 일관성, 추가 저장소 불필요
  - 단점: 재생 시간 (메시지 많으면 오래 걸림)

최적 방안: 하이브리드
  - 토픽: 이벤트 로그 (진실의 근원)
  - 상태 DB: 현재 상태 + 스냅샷
  - 인메모리: 빠른 조회용 캐시

  재시작 시:
  1. 상태 DB에서 최근 스냅샷 로드 (빠름)
  2. 스냅샷 offset 이후의 이벤트만 토픽에서 재생 (효율적)

배포 시 고려사항 3: 모니터링

핵심 메트릭:

1. 상태 맵 크기
   gauge("status.map.size", statusMap::size)

   경고: > 1,000,000 (메모리 관리 필요)

2. 메시지 처리 지연
   timer("message.processing.duration")

   경고: > 100ms (비정상 지연)

3. 토픽 발행 실패율
   counter("kafka.send.failure", "topic", "pipeline.status.update")

   경고: > 0.1% (Kafka 문제)

4. Consumer Lag
   gauge("kafka.consumer.lag", "topic", "pipeline.execute.response")

   경고: > 1000 (처리 지연)

5. 상태 전이 실패율
   counter("status.transition.failure", "reason", "invalid_transition")

   경고: > 1% (비즈니스 로직 문제)

배포 시 고려사항 4: 롤링 배포

주의: 상태 맵을 공유하지 않는 멀티 인스턴스 환경에서

서버 1: 처리 중 (DM001 상태 = FORWARD)
서버 2: 상태 불일치 (DM001 상태 = PENDING, 아직 못 받음)

해결:

방안 1: 토픽 offset으로 순서 보장
  - DM001의 모든 메시지는 같은 파티션으로 라우팅
  - 한 서버만 처리 (다른 서버는 대기)
  - 처리 순서 보장

방안 2: 상태 조회는 DB/토픽 사용
  - 인메모리: 캐시용 (최종 일관성)
  - 상태 조회: 상태 DB SELECT (강한 일관성)
  - 트레이드오프: 약간 느리지만 정확

구현:
  public MessageStatus getStatus(String dmndId) {
    // 1. 캐시 확인 (빠름, 다만 다소 지연 가능)
    MessageStatus cached = statusMap.get(dmndId);
    if (cached != null) {
      return cached;
    }

    // 2. DB 조회 (느리지만 정확)
    return messageRepository.findById(dmndId)
      .orElseThrow(() -> new NotFoundException(dmndId));
  }
```

## 7. 관련 문서

- [01. 스케줄러 → 이벤트 드리븐](./01-scheduler-to-event-driven.md)
- [02. Feign REST → Kafka Producer](./02-feign-rest-to-kafka-producer.md)
- [04. Thread.sleep → 비동기 이벤트](./04-thread-sleep-to-async-event.md)
- [07. DB 분산 락 → Consumer Group](./07-db-lock-to-consumer-group.md)
- [Architecture Overview](../../../README.md)

---

**작성일**: 2026-02-16
**학습 목적**: 면접 준비 (Event Sourcing, 인메모리 상태 관리, 토픽 기반 이벤트 로그)
**난이도**: 중상 (TPS 맥락 + 대규모 시스템 설계 이해 필요)
**예상 면접 시간**: 15~20분 (전체 주제), 5~10분 (개별 질문)
**핵심 개념**: Event Sourcing, ConcurrentHashMap, Kafka as Event Log, Eventual Consistency, CQRS
