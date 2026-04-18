# Kafka Streams 적용 후보 분석

## 개요

TPS 프로젝트에서 단순 Kafka Producer/Consumer가 아닌 **Kafka Streams(상태 기반 스트림 처리)**가 적합한 영역을 분석한 결과다. Kafka Streams는 실시간 집계, 윈도우 카운팅, 스트림 조인, CEP(복합 이벤트 처리) 등 **상태를 유지하면서 이벤트를 처리**해야 하는 경우에 적합하다. 단순히 이벤트를 받아서 처리하는 것은 Consumer로 충분하지만, 집계 결과를 메모리에 유지하면서 새 이벤트마다 갱신해야 하는 경우에는 Kafka Streams의 KTable과 StateStore가 필요하다.

### 전제 조건

현재 TPS에는 Kafka Producer/Consumer가 직접 구현되어 있지 않다. 14개 서비스에서 `ApplicationEventPublisher` 기반 인-프로세스 이벤트를 사용하고 있으며, 이를 Kafka 토픽으로 전환하는 것이 모든 Kafka Streams 후보의 선행 작업이다. 다만 `core-lib`에 `AsyncMessageRequest.avsc` Avro 스키마가 이미 존재하므로 메시지 포맷 설계 부담은 줄어든다.

### 기존 Avro 인프라

**파일**: `core-lib/src/main/avro/async/message/request/AsyncMessageRequest.avsc`

```json
{
  "type": "record",
  "name": "AsyncMessageRequest",
  "namespace": "org.okestro.tps.core.message",
  "fields": [
    {"name": "srcModuleNm", "type": "string", "doc": "원천 모듈명"},
    {"name": "prpsModuleNm", "type": "string", "doc": "목적 모듈명"},
    {"name": "dmndThmSe", "type": "string", "doc": "요청 주제 분류"},
    {"name": "dmndActnSe", "type": "string", "doc": "요청 행위 분류"},
    {"name": "dmndPath", "type": "string", "doc": "요청 경로"},
    {"name": "rspnsPath", "type": "string", "doc": "응답 수신 경로"},
    {"name": "mxmmRspnsWaitTerm", "type": "long", "doc": "최대 응답 대기 기한(초)"},
    {"name": "dmndMxmmNmtm", "type": "int", "doc": "최대 재시도 횟수"},
    {"name": "spclKey", "type": "string", "doc": "원천 모듈 식별용 특수키"},
    {"name": "dmndData", "type": "string", "doc": "요청 데이터(JSON)"}
  ]
}
```

현재 이 스키마는 Feign HTTP 호출(`TicketEventPublisher` L66: `feignClient.publishEvent(request)`)을 통해 `ppln-logging-api`로 전달되고 있다. Kafka로 전환하면 동일 스키마를 Producer 직렬화에 재활용할 수 있다.

---

## HIGH 우선순위 (3건)

세 건 모두 대시보드 집계 관련이다. 현재 Quartz 배치(1회/일) 또는 매 요청 풀스캔 SQL로 동작하는 패턴을 KTable materialized view로 전환하면 실시간성과 쿼리 성능 모두 개선된다.

### S1. 일일 티켓 상태 집계 — KTable Materialized View

**현재 구현**

| 파일 | 경로 | 핵심 라인 |
|------|------|----------|
| Quartz Job | `scheduler/.../quartz/job/DailyTicketSttsInsertJob.java` | L19 |
| MyBatis SQL | `scheduler/src/main/resources/mapper/TbTpsSt001PCommandMapper.xml` | L4-85 |
| 대시보드 SQL | `workflow-api/src/main/resources/sql/1.개발진행현황.sql` | L19-46 |

Quartz 배치가 하루 1회 실행되어 `TB_TPS_ST_001_P` 테이블에 통계를 INSERT한다. SQL은 4개 CTE(`REG_TICKT`, `CLOSE_TICKT`, `PRGRS_TICKT`, `DELAY_INFO`)를 사용하며, `ROW_NUMBER()` 윈도우 함수와 `COUNT(DISTINCT)` + `GROUP BY TASK_CD`로 집계한다. 대시보드의 "개발 진행 현황" 패널은 별도 SQL(`PRCS_COMPONENTS` CTE)로 컴포넌트별(개발/테스트/배포/결재) 카운트를 계산한다.

**문제점**: 대시보드 데이터가 최대 24시간 지연된다. 오전에 티켓 10건을 완료해도 다음 날 배치가 돌기 전까지 통계에 반영되지 않는다.

**왜 Kafka Streams인가**: 단순 Consumer는 이벤트를 받아서 DB에 쓸 수 있지만, taskCd별 카운트를 메모리에 유지하면서 새 이벤트마다 즉시 갱신하려면 KTable의 상태 저장소가 필요하다. Interactive Query로 O(1) 조회가 가능하여 DB 풀스캔을 대체할 수 있다.

**Kafka Streams 토폴로지**

```
Source: tps.ticket.events (TicketCreated, TicketStatusChanged, TicketCompleted)
    │
    ├── Branch[0]: status-count-stream
    │   └── GroupBy(taskCd)
    │       └── Aggregate(
    │             regNocs:   count where event=CREATED && date=today
    │             prgrsNocs: count where status NOT IN (DEL,CMPTN,RGRJT)
    │             cmptnNocs: count where event=COMPLETED && date=today
    │             delayNocs: count where delayYn=Y
    │           )
    │           └── Materialized KTable: "ticket-stats-by-task-store"
    │               └── Interactive Query: GET /stats/{taskCd} → O(1)
    │
    └── Branch[1]: component-progress-stream
        └── Filter(status=EXCN)
            └── FlatMap(ticket → components)
                └── GroupBy(componentType: dev/test/deploy/approval)
                    └── Count()
                        └── Materialized KTable: "dev-progress-store"
```

**효과**: Quartz 배치 제거. 대시보드가 초 단위 실시간 데이터를 Interactive Query로 직접 조회한다.

---

### S2. 티켓 발행 빈도 히트맵 (30일) — Windowed KTable

**현재 구현**

| 파일 | 경로 | 핵심 라인 |
|------|------|----------|
| SQL | `workflow-api/src/main/resources/sql/4. 티켓 발행 빈도.sql` | L18-29 |

```sql
SELECT DATE_FORMAT(E.REG_DT, '%Y-%m-%d') AS TRGT_YMD,
       COUNT(*) AS REG_NOCS
  FROM TPS.TB_TPS_TK_201 E
 WHERE E.REG_DT BETWEEN DATE_SUB(NOW(), INTERVAL 29 DAY) AND NOW()
   AND EXISTS(SELECT 1 FROM TASK_AUTH F WHERE F.TASK_CD = E.TASK_CD AND F.USER_ID = ?)
 GROUP BY DATE_FORMAT(E.REG_DT, '%Y-%m-%d')
```

대시보드 로드마다 30일 범위 COUNT/GROUP BY 풀스캔이 실행된다. 사용자 수가 늘면 DB 부하가 선형 증가하는 구조다.

**왜 Kafka Streams인가**: 30일 윈도우를 유지하면서 일별 카운트를 사전 계산해야 한다. `TimeWindows.ofSizeWithNoGrace(Duration.ofDays(1))`로 일별 카운트를 자동 유지하면, 히트맵 조회는 WindowStore에서 30개 포인트 룩업(O(30))으로 끝난다.

**Kafka Streams 토폴로지**

```
Source: tps.ticket.events (TicketCreated)
    │
    └── SelectKey(YYYY-MM-DD from REG_DT)
        └── GroupByKey()
            └── WindowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofDays(1)))
                └── Count()
                    └── Materialized WindowStore: "ticket-frequency-store"
                        └── Interactive Query: store.fetch(key, from, to)
                            → 30개 일별 카운트 반환
```

**효과**: DB 풀스캔 제거. 새 티켓 등록 시 초 단위로 히트맵이 갱신된다. 가장 단순한 토폴로지(단일 윈도우 카운트)이므로 Kafka Streams 패턴 검증에 최적이다.

---

### S3. 등록/완료 추이 — Dual Windowed KTable Join

**현재 구현**

| 파일 | 경로 | 핵심 라인 |
|------|------|----------|
| SQL | `workflow-api/src/main/resources/sql/2-2.등록 및 완료 날짜별 건수.sql` | L25-59 |

```sql
SELECT DATE_FORMAT(A.YMD, '%Y-%m-%d') AS TRGT_YMD,
       COALESCE(SUM(B.REG_NOCS), 0)   AS REG_NOCS,
       COALESCE(SUM(B.CMPTN_NOCS), 0) AS CMPTN_NOCS
  FROM TPS.TB_TPS_CM_091 A  -- 캘린더 테이블
  LEFT JOIN (...subquery with CASE-WHEN...) B ON A.YMD = B.YMD
 WHERE A.YMD BETWEEN DATE_SUB(NOW(), INTERVAL 6 DAY) AND NOW()
```

캘린더 테이블 LEFT JOIN + CASE-WHEN 집계로 동작한다. 기간 전환(일/주/월)마다 전체 재계산이 필요하다. 프론트엔드 `RegistrationCompletionSummary.tsx`(L146-152)에서는 이전 기간 대비 비교(`previousPeriodRegCompareCount`)까지 클라이언트 측에서 계산하고 있다.

**왜 Kafka Streams인가**: 등록 스트림과 완료 스트림을 날짜 키로 조인해야 한다. 두 개의 독립 Windowed KTable을 만든 후 `join()`으로 합치면, 기간 전환은 같은 스토어에서 범위만 바꿔 조회하면 되고, 이전 기간 대비 비교도 서버 측에서 처리할 수 있다.

**Kafka Streams 토폴로지**

```
Source: tps.ticket.events
    │
    ├── Branch[0]: registration-stream
    │   └── Filter(event=CREATED)
    │       └── SelectKey(YYYY-MM-DD)
    │           └── WindowedBy(Duration.ofDays(1))
    │               └── Count() → KTable "reg-daily-store"
    │
    ├── Branch[1]: completion-stream
    │   └── Filter(event=COMPLETED, status=CMPTN)
    │       └── SelectKey(YYYY-MM-DD)
    │           └── WindowedBy(Duration.ofDays(1))
    │               └── Count() → KTable "cmptn-daily-store"
    │
    └── Join: reg-daily-store ⋈ cmptn-daily-store (by date key)
        └── Materialized KTable: "reg-cmptn-trend-store"
            └── Interactive Query: GET /trend?from=...&to=...
```

**효과**: 캘린더 테이블 JOIN 제거. `previousPeriodRegCompareCount` 클라이언트 계산도 서버 측 Interactive Query로 이동 가능.

---

## MEDIUM 우선순위 (4건)

### S4. 티켓 지연 감지 — punctuate() CEP

**현재 구현**

| 파일 | 경로 |
|------|------|
| Quartz Job | `scheduler/.../quartz/job/TicketDelaySttsUpdtJob.java` (L25) |
| MyBatis SQL | `scheduler/src/main/resources/mapper/TpTpsTk202CommandMapper.xml` (L4-28) |

```sql
UPDATE TB_TPS_TK_202 A
   SET A.DELAY_YN = CASE
     WHEN B.STTS_CD IN ('DEL','CMPTN','RGRJT','IMPRC')
       THEN CASE WHEN A.TCKT_CMPTN_PRNMNT_DT < DATE_FORMAT(B.MDFCN_DT, '%Y%m%d')
                 THEN 'Y' ELSE 'N' END
     ELSE CASE WHEN A.TCKT_CMPTN_PRNMNT_DT < DATE_FORMAT(NOW(), '%Y%m%d')
               THEN 'Y' ELSE 'N' END
   END
```

Quartz 배치가 주기적으로 지연 여부를 UPDATE한다. 배치 사이에 발생한 지연은 다음 실행까지 감지되지 않는다.

**Kafka Streams 방식**: Processor API의 `punctuate(WALL_CLOCK_TIME)`로 매 1분마다 상태 저장소를 순회한다. 각 티켓의 `TCKT_CMPTN_PRNMNT_DT`를 StateStore에 보관하고, 완료예정일 < 현재시각인 티켓 발견 시 `TicketDelayedEvent`를 발행한다. 배치 주기(수 시간) → 1분 간격으로 감지 정밀도가 향상된다.

**고려사항**: 현재 Quartz로 충분히 동작하는 영역이다. 실시간 SLA 알림이 비즈니스 요구사항으로 확정되면 전환 가치가 있다.

---

### S5. 결재 만료 자동 반려 — punctuate() 타임아웃

**현재 구현**

| 파일 | 경로 |
|------|------|
| Service | `scheduler/.../approval/service/ApprovalCancelService.java` (L33, L45-79) |

```java
List<...> expiredList = az006QueryMapper.selectExpiredApprovals();
for (var item : expiredList) {
    workflowApiFeignClient.tcktAprvEnd("sysadmin", request);
}
// L71-79: catch — 실패 로그 후 계속 (재시도 없음)
```

매 1분 Quartz 실행 → 만료 조회 → 건별 Feign 호출. 실패 시 재시도 없이 다음 스케줄까지 방치된다.

**Kafka Streams 방식**: 결재 생성 이벤트가 토픽에 들어오면 StateStore에 만료 시각을 저장한다. `punctuate()`로 주기 체크하여 만료 감지 시 `ApprovalExpiredEvent`를 출력 토픽에 발행한다. workflow-api Consumer가 반려 처리를 수행하며, Kafka의 at-least-once 전달 보장 + 멱등성 컨슈머로 누락을 방지한다.

**고려사항**: S4(지연 감지)와 동일한 `punctuate()` 패턴이므로 함께 구현하면 패턴을 재활용할 수 있다.

---

### S6. 파이프라인 실행 상태 추적 — KTable + SSE

**현재 구현**

| 파일 | 경로 |
|------|------|
| MyBatis | `pipeline-api/src/main/resources/mapper/TbTpsPl205QueryMapperV3.xml` (L6-126) |
| 프론트 폴링 | `react-app/.../pplnLogging/v3/usePplnLoggingQuery.ts` (L45: 5초, L59: 5초) |

`TB_TPS_PL_205` 테이블에서 페이지네이션 조회(L6-27), MAX() 서브쿼리로 최신 실행 조회(L38-56), TASK_INFO/INT_INFO CTE + ArgoCD 조인(L58-126) 등 복잡한 SQL이 매 5초마다 실행된다.

**Kafka Streams 방식**: 파이프라인 상태 변경 이벤트(RUNNING/SUCCESS/FAIL)를 `(pplnNo, pplnVsrn)` 키로 KTable에 materialized view로 유지한다. SSE 엔드포인트가 KTable 변경을 감지하여 프론트엔드에 실시간 푸시하면, 5초 폴링을 완전히 제거할 수 있다.

**고려사항**: 프론트엔드 SSE 전환이 수반되어 범위가 넓다. `04-pipeline-execution-eda.md`의 SSE 전환과 동시 진행을 권장한다.

---

### S7. 업무코드별 티켓 사용 현황 — Count KTable

**현재 구현**

| 파일 | 경로 |
|------|------|
| 전체 SQL | `workflow-api/src/main/resources/sql/3-1.티켓별 업무코드 사용 현황(전체 업무코드).sql` (L19-37) |
| 상위5개 SQL | `workflow-api/src/main/resources/sql/3-2.티켓별 업무코드 사용 현황(상위 5개).sql` (L19-40) |

```sql
SELECT CONCAT(CAST(A.TASK_CD AS CHAR), ' ', B.TASK_NM) AS DISPLAY_TASK_NM,
       COUNT(1) AS TCKT_NOCS
  FROM TPS.TB_TPS_TK_201 A
  JOIN TPS.TB_TPS_CM_038 B ON A.TASK_CD = B.TASK_CD
 WHERE A.STTS_CD NOT IN ('DEL','CMPTN','RGRJT','IMPRC')
 GROUP BY A.TASK_CD, B.TASK_NM
 ORDER BY COUNT(1) DESC
```

대시보드 로드마다 전체 테이블 COUNT/GROUP BY 풀스캔이 실행된다.

**Kafka Streams 방식**: `GroupBy(taskCd) → Count()` KTable로 업무코드별 카운트를 유지한다. "상위 5개"는 Interactive Query 시 정렬하거나, 커스텀 프로세서로 Top-N을 유지할 수 있다.

**고려사항**: S1(일일 티켓 통계)과 동일 소스 토픽(`tps.ticket.events`)을 사용한다. S1 구현 시 함께 추가하면 증분 비용이 낮다.

---

## LOW 우선순위 (3건)

### S8. Feign 호출 체인 대체

`TicketEventPublisher`(L66)가 Feign으로 `ppln-logging-api`를 경유하여 비동기 메시지를 전달한다. `AsyncMessageRequest.avsc` 스키마가 이미 있으므로 Feign → Kafka Producer로 전환하면 되지만, 이것은 Kafka Streams가 아닌 단순 Producer/Consumer 영역이다.

### S9. 티켓 상태 머신 중앙화

`SttsCdType.java`(11개 상태), `TestRqstStatusEnums.java`(L67: `canTransitionFrom()`), `TicketEventProcessState.java`에 상태 전이 로직이 분산되어 있다. Kafka Streams 상태 머신으로 중앙화하면 감사 추적이 자동화되지만, 현재 인-프로세스 검증이 정상 동작하므로 기능적 갭은 없다.

### S10. 알림 디스패치

`NotificatorFeignClient` 동기 호출을 Kafka 토픽으로 대체하는 것인데, 단순 fire-and-forget이므로 Kafka Streams보다 일반 Consumer가 적합하다.

---

## 프론트엔드 분석

### 대시보드 패널 (수동 refetch 패턴)

모든 대시보드 패널이 `enabled: false` + 사용자 인터랙션 시 `refetch()` 호출 패턴을 사용한다. 기간이나 뷰를 전환할 때마다 DB 풀스캔 SQL이 실행되는 구조다.

| 패널 | 컴포넌트 | 쿼리 훅 |
|------|---------|---------|
| 개발 진행 현황 | `dashboard/v4/panel/DevelopmentProgressStatus.tsx` (L76-82) | `useDevelopmentProgressStatusQuery.ts` (L22) |
| 티켓 발행 빈도 | `dashboard/v4/panel/TicketFrequency.tsx` (L18-21) | `useTicketFrequencyStatusQuery.ts` (L16) |
| 등록/완료 추이 | `dashboard/v4/panel/RegistrationCompletionSummary.tsx` (L93-105) | `useRegistrationCompletionQuery.ts` (L37) |
| 프로젝트 진행 | `dashboard/v4/panel/ProjectProgressStatus.tsx` (L27-34) | 2개 병렬 쿼리 (multi-query cascade) |

**Kafka Streams 적용 시 프론트 변화**:
- S1~S3의 Interactive Query API를 호출하면 DB 풀스캔 대신 O(1)~O(30) 조회로 변경
- `RegistrationCompletionSummary`의 이전 기간 비교 로직(L146-152: `previousPeriodRegCompareCount`, `previousPeriodCmptnCompareCount`)도 서버에서 처리하여 클라이언트 계산을 제거할 수 있음
- `ProjectProgressStatus`의 multi-query cascade(2개 독립 쿼리) → 단일 Interactive Query 호출로 통합 가능

### 폴링 기반 컴포넌트 (활성 refetchInterval)

| 컴포넌트 | 쿼리 훅 | 간격 |
|---------|---------|------|
| 파이프라인 스테이지 정보 | `pplnLogging/v3/usePplnLoggingQuery.ts` | 5초 (L45) |
| 파이프라인 스테이지 로그 | `pplnLogging/v3/usePplnLoggingQuery.ts` | 5초 (L59) |
| 워크플로우 실행 | `workflow/wrkflwExcn/v2/useWrkflwExcnQuery.ts` | 30초 (L25) |
| APM 모니터링 | `common/monitoring/v1/useMonitoringQuery.ts` | 5초 (L228) |
| SonarQube 분석 | `pipeline/sonarqube/v3/useAnalysisMngQuery.ts` | 10초/5초 (L50, L119) |
| 워크플로우 상태 | `workflow/workflow/v1/useWorkflowQuery.ts` | 30초 (L23) |
| 칸반 보드 | `pms/.../kanbanBoard/v1/useKanbanBoardQuery.ts` | 10초 (L37) |
| ArgoCD 앱 | `pipeline/argocd/application/v3/useApplicationQuery.ts` | 조건부 (L101) |

파이프라인 로깅(5초)과 APM 모니터링(5초)이 가장 고빈도 폴러다. S6(파이프라인 상태 KTable) + SSE 푸시로 이 폴링을 제거하면 서버 부하가 가장 크게 감소한다. 워크플로우 30초 폴링도 KTable + SSE로 대체 가능하다.

---

## Spring ApplicationEventPublisher 사용 현황 (14개 서비스)

Kafka Streams의 **입력 토픽**을 만드는 데 필요한 이벤트 발행 지점이다. 이 위치에서 Kafka Producer를 추가하면 Kafka Streams 토폴로지의 소스가 만들어진다.

| 서비스 | 위치 |
|--------|------|
| AprvMngCommandServiceImpl | L47 |
| AprvPrcsCommandServiceImpl | L71 |
| TestRqstCommandServiceImpl | L37 |
| TcktMngCommandServiceImpl / V2 | L57 / L53 |
| WrkflwExcnCommandServiceImpl / V2 | L52 / L52 |
| TcktExcnCommandServiceImpl / V2 | L69 / L99 |
| DefaultChangeManagementExternalServiceV2 | L45 |
| TcktIntegrationServiceImpl / V2 | L65 / L55 |
| DefaultBranchControlExternalService / V2 | L35 / L35 |

모두 `workflow-api` 모듈에 위치한다.

**마이그레이션 경로**: `applicationEventPublisher.publishEvent(event)` 호출 위치에서 추가로 Kafka Producer를 호출하거나, Transactional Outbox 패턴으로 Outbox 테이블에 INSERT한다.

---

## 구현 순서 권장

| 순서 | 후보 | 근거 |
|------|------|------|
| 1 | **S2 (티켓 빈도 히트맵)** | 가장 단순한 토폴로지(단일 윈도우 카운트). 패턴 검증에 적합하다 |
| 2 | **S1 (일일 티켓 통계)** | Quartz 배치 제거 효과가 크다. S2 패턴을 멀티 집계로 확장하면 된다 |
| 3 | **S7 (업무코드 사용 현황)** | S1과 동일 소스 토픽을 사용하므로 증분 비용이 낮다 |
| 4 | **S3 (등록/완료 추이)** | 듀얼 스트림 조인으로 가장 복잡하지만 비즈니스 가치가 높다 |
| 5 | **S4 (지연 감지)** | `punctuate()` 패턴을 도입하며, 또 다른 Quartz 배치를 제거한다 |
| 6 | **S5 (결재 만료)** | S4와 동일 `punctuate()` 패턴을 재활용할 수 있다 |
| 7 | **S6 (파이프라인 상태)** | 프론트엔드 SSE 전환이 수반되어 범위가 넓다 |

---

## EDA(01~06) vs Kafka Streams(07) 관계

| 구분 | EDA (Producer/Consumer) | Kafka Streams |
|------|------------------------|--------------|
| 목적 | 모듈 간 비동기 디커플링 | 실시간 상태 기반 처리 |
| 선행 | 없음 (독립 적용 가능) | EDA 토픽이 소스 데이터 |
| 예시 | TicketCreatedEvent → pipeline-api consume | TicketCreatedEvent → 일별 카운트 집계 |
| 관계 | Kafka Streams의 **입력 토픽**을 만드는 역할 | EDA 토픽을 **소비하여 파생 데이터** 생성 |

EDA 전환(01~06)이 먼저 완료되어야 Kafka Streams(07)의 소스 토픽이 확보된다. 다만 S1~S3의 대시보드 집계는 기존 DB 변경 이벤트(CDC)를 소스로 사용하면 EDA 전환과 독립적으로 시작할 수도 있다. Debezium으로 `TB_TPS_TK_201` 테이블의 CDC 이벤트를 캡처하여 Kafka 토픽에 넣으면, EDA 마이그레이션 완료를 기다리지 않고 Kafka Streams 토폴로지를 구축할 수 있다는 뜻이다.

---

## 요약

| 우선순위 | 건수 | 핵심 패턴 | 대체 대상 |
|---------|------|----------|----------|
| HIGH | 3 | KTable 집계, Windowed Count, Stream Join | 대시보드 풀스캔 SQL + Quartz 배치 |
| MEDIUM | 4 | punctuate() CEP, KTable + SSE | Quartz 지연감지, 5초 폴링 |
| LOW | 3 | 단순 Producer/Consumer | Feign 체인, 상태 머신, 알림 |
