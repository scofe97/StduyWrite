# M1~M5 중간 우선순위 EDA 전환 후보

## 개요

HIGH 우선순위 4개(결재, 티켓↔파이프라인, 파이프라인 실행, LDAP 동기화) 이후 단계적으로 전환할 수 있는 5개 후보를 정리한다. 각 후보는 "현재 패턴 → EDA 전환 방식 → 고려사항" 3단 구조로 설명한다.

MEDIUM 우선순위 후보들은 HIGH 후보와 달리 당장 전환하지 않아도 시스템이 동작하는 영역이다. 그러나 현재 구조를 그대로 두면 확장성 한계, 데이터 불일치, 장애 전파 문제가 점진적으로 심화된다. 이 문서는 각 후보의 현재 문제를 구체적으로 드러내고, EDA 전환으로 무엇이 달라지는지 설명한다.

---

## M1. 알림 파이프라인 (Notification Pipeline)

### 현재 패턴

**코드 경로**:
- `workflow-api/.../event/notification/ApvrNotificationEventListener.java`
- `scheduler/.../delegate/event/DelegateNotificationEventListener.java`

현재 구조를 보면 workflow-api는 `@TransactionalEventListener`로 인-프로세스 알림 이벤트를 처리한다. 핸들러는 4개로 나뉜다. 결재 요청(L57-98), 진행(L105-152), 완료(L159-190), 실패(L197-227) 각각의 상황에서 `NotificatorFeignClient`를 통해 SSE를 전달한다. scheduler 모듈도 같은 방식이다. `DelegateNotificationEventListener`가 위임 알림을 처리하고, 역시 `NotificatorFeignClient.sendSSEToSpecificClients()`를 호출한다. react-app 쪽의 `UserNotifications.tsx`(L50-103)는 `useNotificatorQuery().useGetAlarmListByUserByQuery(userId)`로 알림 목록을 폴링하고, 수동으로 읽음 처리한다.

이 구조의 문제는 세 가지다. 첫째, 알림 처리가 비즈니스 로직과 같은 프로세스에 있기 때문에 서비스 장애 시 알림도 함께 중단된다. 둘째, `NotificatorFeignClient` 호출이 실패하면 알림이 유실된다. 재시도 로직이 없으므로 사용자는 결재가 완료됐는지 알 방법이 없다. 셋째, 알림 서비스를 독립적으로 확장하거나 채널을 추가(이메일, 슬랙 등)하려면 workflow-api 코드를 직접 수정해야 한다.

### EDA 전환 방식

핵심 아이디어는 알림 요청 자체를 이벤트로 분리하는 것이다. workflow-api와 scheduler가 `NotificationRequestedEvent`를 `tps.notification` 토픽으로 발행하면, 독립 Notification Consumer가 채널별로 전달을 처리한다. SSE Consumer, 이메일 Consumer, 슬랙 Consumer를 별도로 운영할 수 있고, 각각 독립적으로 확장된다.

이벤트 스키마:
```json
{
  "eventType": "NOTIFICATION_REQUESTED",
  "correlationId": "tckt-12345",
  "payload": {
    "targetUserIds": ["user-001", "user-002"],
    "notificationType": "APPROVAL_REQUESTED",
    "channel": "SSE",
    "title": "결재 요청",
    "body": "TCKT-12345에 대한 결재가 요청되었습니다.",
    "linkUrl": "/workflow/ticket/TCKT-12345"
  }
}
```

### 고려사항

전환 난이도가 낮은 편이다. `@TransactionalEventListener` 내부에서 `NotificatorFeignClient`를 직접 호출하는 부분을 Kafka produce로 교체하면 되기 때문에 코드 변경 범위가 좁다. 알림은 at-least-once 정책이 적합하다. 중복 알림이 알림 누락보다 사용자 경험 측면에서 낫기 때문이다. react-app의 `UserNotifications.tsx`는 폴링 방식을 SSE 수신으로 전환하면 서버 부하도 줄어든다.

---

## M2. 위임 상태 변경 (Delegate Status Change)

### 현재 패턴

**코드 경로**:
- `scheduler/.../quartz/job/DelegateStatusUpdateJob.java`
- `scheduler/.../delegate/service/DelegateStatusService.java`
- `scheduler/.../delegate/event/DelegateNotificationEventListener.java`

매일 실행되는 Quartz job이 `TbTpsCm004`를 조회한다. 오늘 시작하는 위임은 WAIT → PROGRESS로, 오늘 종료하는 위임은 PROGRESS → DONE으로 상태를 업데이트한다. 상태 변경 후에는 `DelegateNotificationEvent`를 Spring 인-프로세스로 발행하고, Listener가 `NotificatorFeignClient.sendSSEToSpecificClients()`를 호출한다.

이 구조는 두 가지 문제를 안고 있다. Daily batch 주기로 인해 위임 상태 변경 감지에 최대 24시간 지연이 발생한다. 위임이 오전 9시에 시작해야 하는데 Quartz job이 자정에 실행된다면, 당일 오전에는 WAIT 상태가 유지된다. 그리고 SSE 전달 실패 시 재시도가 없어 사용자가 위임 시작을 알 수 없는 상황이 생긴다.

### EDA 전환 방식

완전한 이벤트 전환 대신 점진적 접근이 현실적이다. Quartz job은 유지하되, 상태 변경 시 Kafka로 이벤트를 발행하도록 수정한다. `DelegationStartedEvent`와 `DelegationEndedEvent`로 나뉘며, 이를 consume하는 알림 Consumer, 대시보드 Consumer, 감사 Consumer가 독립적으로 처리한다.

이벤트 스키마:
```json
{
  "eventType": "DELEGATION_STARTED",
  "payload": {
    "undtakeSn": "DLG-001",
    "delegatorId": "user-001",
    "delegateeId": "user-002",
    "startDate": "2026-02-25",
    "endDate": "2026-03-01",
    "scope": "APPROVAL"
  }
}
```

### 고려사항

시간 기반 이벤트라는 특성 때문에 Kafka delayed message 방식보다 Quartz 유지가 더 안정적이다. Kafka delayed message는 아직 표준화된 방식이 없어 운영 복잡도가 높다. 위임 시작/종료 알림은 M1(알림 파이프라인)과 동일한 토픽을 재활용할 수 있다. 파티션 키는 delegatorId로 설정하면 같은 위임자의 이벤트 순서가 보장된다.

---

## M3. 감사 로그 중앙화 (Audit Log Centralization)

### 현재 패턴

**코드 경로**: 각 모듈의 `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)`

각 모듈이 각자의 방식으로 감사 로그를 기록한다. workflow-api는 `AuditCaptureEvent`를 발행하고 인-프로세스에서 처리한다. pipeline-api는 `TcktHstryEventListener`에서 이력 이벤트를 처리한다. scheduler는 에러 발생 시 `TbTpsCm047`에 직접 기록한다. 감사 로직이 모듈마다 분산되어 있다.

이로 인해 생기는 문제는 명확하다. 모듈별로 감사 로그 형식이 다르기 때문에 중앙에서 통합 조회가 불가능하다. 특정 티켓의 전체 처리 이력을 보려면 workflow-api DB, pipeline-api DB, scheduler DB를 각각 조회해서 수동으로 합쳐야 한다. 또한 감사 처리 실패가 비즈니스 트랜잭션에 영향을 줄 수 있는 구조다.

### EDA 전환 방식

모든 감사 이벤트를 `tps.audit` 단일 토픽으로 통합한다. 각 모듈의 `@TransactionalEventListener`를 Kafka produce로 교체하고, 중앙 Audit Consumer가 통합 감사 저장소에 기록한다. 감사 저장소는 읽기 전용 전용 DB로 분리하면 비즈니스 DB 부하도 줄어든다.

이벤트 스키마:
```json
{
  "eventType": "AUDIT_TRAIL",
  "payload": {
    "module": "workflow-api",
    "action": "APPROVAL_COMPLETED",
    "actor": "user-001",
    "target": "TCKT-12345",
    "details": {"result": "APPROVED", "duration": 3600},
    "timestamp": "2026-02-25T10:00:00Z"
  }
}
```

### 고려사항

감사 로그는 at-least-once 정책이 적합하다. 중복 기록이 누락보다 훨씬 낫기 때문이다. 보존 기간은 규정 준수 요건에 따라 결정한다. 일반적으로 감사 로그는 수년간 보존해야 하므로, Kafka topic compaction 대신 별도 저장소(RDBMS 또는 시계열 DB)로 내보내는 구조가 현실적이다. 기존 `TbTpsCm047` 에러 테이블도 같은 토픽으로 통합하면 에러 이력과 감사 이력을 한 곳에서 볼 수 있다. 이벤트 순서가 중요하지 않은 영역이므로 파티션을 많이 분산해 처리량을 높일 수 있다.

---

## M4. 티켓 지연 상태 / 일일 스냅샷 (Ticket Delay & Daily Snapshot)

### 현재 패턴

**코드 경로**:
- `scheduler/.../quartz/job/TicketDelaySttsUpdtJob.java`
- `scheduler/.../quartz/job/DailyTicketSttsInsertJob.java`
- `scheduler/.../ticket/service/impl/TicketServiceImpl.java`

두 Quartz job이 각각 다른 역할을 한다. `TicketDelaySttsUpdtJob`은 주기적으로 `TbTpsTk202.DELAY_YN` 컬럼을 업데이트한다. 완료예정일을 현재 날짜와 비교해서 지연 여부를 판단한다. `DailyTicketSttsInsertJob`은 매일 `TbTpsSt001P`에 그날의 티켓 상태 스냅샷을 INSERT한다. 이 스냅샷은 대시보드나 통계 조회에 사용된다.

이 구조의 핵심 문제는 실시간성이 없다는 점이다. 티켓이 완료예정일을 넘겼더라도 다음 배치 실행까지 `DELAY_YN = 'N'`으로 남아 있다. 배치 주기가 1시간이라면 최대 1시간 동안 잘못된 상태를 보여준다. 또한 대량 UPDATE 쿼리가 DB 부하로 이어질 수 있다.

### EDA 전환 방식

지연 감지와 일일 스냅샷을 분리해서 접근하는 것이 합리적이다. 일일 스냅샷은 시점 기반 집계라는 특성 때문에 Quartz를 유지하는 것이 적합하다. 반면 지연 감지는 이벤트 기반으로 전환할 수 있다. 티켓 상태 변경 이벤트(`TicketStatusChangedEvent`)를 consume하는 지연 감지 Consumer가 완료예정일을 실시간으로 체크하고, 지연이 감지되면 `TicketDelayDetectedEvent`를 발행한다.

이벤트 스키마:
```json
{
  "eventType": "TICKET_DELAY_DETECTED",
  "payload": {
    "tcktNo": "TCKT-12345",
    "completionDueDate": "2026-02-20",
    "currentDate": "2026-02-25",
    "delayDays": 5,
    "assigneeId": "user-001"
  }
}
```

### 고려사항

지연 이벤트는 M1(알림 파이프라인)과 연동하면 담당자에게 실시간 SLA 알림을 보낼 수 있다. react-app의 Gantt Chart나 대시보드도 SSE를 통해 지연 발생 즉시 갱신된다. 다만 `TICKET_DELAY_DETECTED` 이벤트는 중복 발생 가능성이 있다. 같은 티켓이 이미 지연 상태인데 또 지연 이벤트가 발행되는 경우다. 중복 방지를 위해 Consumer에서 현재 `DELAY_YN` 상태를 확인하고 이미 지연 처리된 경우 스킵하는 멱등성 로직이 필요하다.

---

## M5. 공통코드 캐시 무효화 (Common Code Cache Invalidation)

### 현재 패턴

**코드 경로**:
- `scheduler/.../quartz/job/CommonCodeUpdateJob.java`
- `TbTpsCm037CommandMapper.replace()`

Quartz job이 주기적으로 공통코드 마스터 데이터를 갱신한다. `replace()` 메서드로 데이터를 교체하고, 다른 서비스는 자체 캐시 TTL이 만료될 때까지 이전 데이터를 사용한다. 예를 들어 티켓 상태 코드가 추가됐더라도 각 서비스의 캐시가 살아 있는 동안은 새 코드를 인식하지 못한다.

이 문제는 평소에는 드러나지 않는다. 공통코드 변경 빈도가 낮기 때문이다. 그러나 코드를 추가하자마자 즉시 반영되기를 기대하는 운영 상황에서는 캐시 불일치가 혼란을 만든다. 서비스를 재시작하거나 캐시 TTL을 짧게 설정해서 DB 조회를 늘리는 방식으로 임시 해결하는 경우가 생긴다.

### EDA 전환 방식

공통코드 갱신 시 `CommonCodeUpdatedEvent`를 `tps.system.config` 토픽으로 발행한다. 각 서비스는 이 이벤트를 consume하면 즉시 로컬 캐시를 무효화하고, 다음 조회 시 최신 데이터를 DB에서 가져온다.

이벤트 스키마:
```json
{
  "eventType": "COMMON_CODE_UPDATED",
  "payload": {
    "codeGroup": "TICKET_STATUS",
    "updatedCodes": ["TS001", "TS002"],
    "updatedAt": "2026-02-25T10:00:00Z"
  }
}
```

### 고려사항

캐시 무효화는 at-least-once에 안전하다. 중복 이벤트를 받아도 결과는 캐시 무효화이고, 이후 DB 조회가 한 번 더 발생할 뿐이다. 중요한 설계 포인트는 broadcast 패턴이다. 공통코드 캐시는 서비스의 모든 인스턴스가 갱신해야 한다. 그런데 Kafka의 Consumer Group은 그룹 내 한 인스턴스만 메시지를 받는다. 따라서 각 서비스 유형별로 Consumer Group ID를 다르게 설정해야 한다. 예를 들어 workflow-api 인스턴스가 3개라면 세 인스턴스 모두가 이벤트를 받을 수 있도록 인스턴스별 고유 Group ID를 사용하거나, 파티션 수와 인스턴스 수를 맞추는 방식이 필요하다.

공통코드 변경 빈도가 낮으므로 토픽 보존 기간은 짧게 설정해도 무방하다. react-app 쪽에서도 SSE로 갱신 이벤트를 수신하면 React Query 캐시를 즉시 무효화해서 화면 새로고침 없이 최신 코드가 반영되는 경험을 줄 수 있다.

---

## 전환 로드맵

| 단계 | 후보 | 선행 조건 | 예상 효과 |
|------|------|----------|----------|
| Phase 1 | M1 알림 파이프라인 | H1~H4 인프라 구축 완료 | 알림 독립 확장, 채널 분리 |
| Phase 2 | M3 감사 로그 | M1과 병행 가능 | 중앙 감사, 모듈 간 일관성 |
| Phase 3 | M2 위임 상태 | M1 알림 파이프라인 | 실시간 위임 알림 |
| Phase 4 | M5 공통코드 | Kafka 인프라 안정화 | 캐시 즉시 무효화 |
| Phase 5 | M4 티켓 지연 | M1 알림 + Kafka 안정화 | 실시간 SLA 추적 |

Phase 1과 Phase 2를 병행할 수 있는 이유는 두 후보가 서로 의존하지 않기 때문이다. M1(알림 파이프라인)은 운영 효과가 가장 즉각적이고, M3(감사 로그 중앙화)는 기존 모듈별 코드를 건드리지 않고 produce만 추가하면 되므로 변경 범위가 좁다. M2, M4, M5는 M1이 안정화된 이후 순차적으로 진행하는 것이 현실적이다. 특히 M2와 M4는 M1의 알림 토픽을 재활용하므로 M1이 먼저 검증되어 있어야 한다.
