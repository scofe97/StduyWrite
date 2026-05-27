# operator k8s outbox 폴러 log4jdbc.log4j2 콘솔 폭주

- **발생일**: 2026-05-21
- **영향 범위**: TPS `operator-api` 서비스 dev/k8s 환경. operator local·sbh-local 및 executor 전 환경은 영향 없음.
- **심각도**: 운영 가시성 저하 (장애는 아니나 로그가 outbox 폴링 잡음으로 가득 차 다른 문제 신호가 묻힘).
- **상태**: dev 배포 완료 (`operator-api` repo `756bef5a`, 회차 3 최종). 운영 적용은 dev 관찰 후 결정.
- **관련 티켓**: IGMU-1040 (Outbox 모니터링 정책 설계)
- **fix 회차**: 3회차 (회차 1 잔여 라인 → 회차 2 부팅 실패 revert → 회차 3 thread name 식 + properties 정정 최종)

---

## 1. 증상

operator k8s pod 의 stdout/파일 로그에 다음 패턴이 0.5초 주기로 무한 반복.

```
2026-05-21 15:51:57.913 INFO  [] [operator-scheduler-2] log4jdbc.log4j2 - 2. Connection.prepareStatement(SELECT OE.OX_ID
FROM TB_TRB_OX_001 OE
WHERE OE.STTS_CD = 'PENDING' ...
FOR UPDATE SKIP LOCKED
) returned net.sf.log4jdbc.sql.jdbcapi.PreparedStatementSpy@...
2026-05-21 15:51:57.913 INFO  log4jdbc.log4j2 - 2. SELECT ... {executed in 1 ms}
2026-05-21 15:51:57.913 INFO  log4jdbc.log4j2 - 2. ResultSet.new ResultSet returned
2026-05-21 15:51:57.913 INFO  log4jdbc.log4j2 - 2. PreparedStatement.executeQuery() returned ...
2026-05-21 15:51:57.913 INFO  log4jdbc.log4j2 - |------|
|ox_id |
|------|
|------|
2026-05-21 15:51:57.913 INFO  log4jdbc.log4j2 - 2. ResultSet.next() returned false
... (Connection.commit, setAutoCommit, clearWarnings, ...)
```

폴링 1 사이클당 약 20+ 줄. 0.5초 주기 → 분당 약 2,400줄. PENDING 0건 정상 상태에서도 폭주.

---

## 2. 근본 원인

**세 가지 조건의 우연한 합**:

### (a) Outbox 폴러는 0건이어도 매 주기 SELECT 발행
`message-lib/src/main/java/org/okestro/tps/messaging/application/outbox/OutboxPoller.java:70-73`
```java
@Scheduled(
    fixedDelayString = "${outbox.poll-interval-ms:500}",
    initialDelayString = "${outbox.poll-initial-delay-ms:0}"
)
public void pollAndPublish() { ... }
```
0건이면 backoff 없이 그대로 500ms 후 재폴링. 이는 발행 지연을 낮추려는 의도된 설계.

### (b) operator k8s 의 JDBC driver 가 `DriverSpy` (log4jdbc-log4j2)
`operator/app/src/main/resources/application-k8s.yml:37`
```yaml
driver-class-name: net.sf.log4jdbc.sql.jdbcapi.DriverSpy
```
이 driver 는 PreparedStatement / ResultSet / Connection 의 거의 모든 호출을 wrap 해서 **logger 이름 `log4jdbc.log4j2`** 로 INFO 한 줄씩 남긴다. 로컬은 순정 `org.mariadb.jdbc.Driver` 라 채널 자체가 안 생긴다 (= 로컬은 멀쩡한 이유).

### (c) operator logback 의 root level 이 INFO 기본, EvaluatorFilter 식이 hibernate.SQL 한정
`operator/app/src/main/resources/logback-spring.xml:78,84`
```xml
<root level="${ROOT_LOG_LEVEL}">
```
`ROOT_LOG_LEVEL` 미설정 시 기본 `INFO`. 따라서 `log4jdbc.log4j2` INFO 메시지는 별도 logger 명시 없어도 root INFO 가 통과시킨다.

기존 EvaluatorFilter 식:
```xml
<expression>
    return logger.equals("org.hibernate.SQL")
           &amp;&amp; formattedMessage.contains("TB_TRB_OX_001");
</expression>
```
`org.hibernate.SQL` 만 잡고 `log4jdbc.log4j2` 는 안 잡음 → outbox SELECT 통과.

### (d) executor 는 왜 멀쩡한가 — 비교 대조
executor 도 (b) 조건은 동일 (`DriverSpy`). 그러나:
- `executor/engine/src/main/resources/logback-spring.xml:60,111` → **`<root level="OFF">`**.
- root OFF 라 명시되지 않은 모든 로거가 차단됨. evaluator 가 hibernate.SQL 만 잡든 말든 `log4jdbc.log4j2` 는 출력 경로에 도달조차 못 함.

→ **단일 안전망 (root OFF) 에 의존하는 executor 와, evaluator 식 + root INFO 조합에 의존하는 operator 의 정책 차이가 동일 driver 환경에서 다른 결과를 만들었다.**

---

## 3. 환경별 매트릭스

| 환경 | 서비스 | driver | root level | evaluator 식 커버리지 | 결과 |
|------|--------|--------|------------|----------------------|------|
| local | operator | mariadb (순정) | INFO | hibernate.SQL only | 안 뜸 (채널 자체 없음) |
| sbh-local | operator | mariadb | INFO | hibernate.SQL only | 안 뜸 |
| **k8s** | **operator** | **DriverSpy** | **INFO** | **hibernate.SQL only** | **폭주** |
| local | executor | DriverSpy | OFF | hibernate.SQL only | 안 뜸 (root OFF) |
| sbh-local | executor | mariadb | OFF | hibernate.SQL only | 안 뜸 |
| k8s | executor | DriverSpy | OFF | hibernate.SQL only | 안 뜸 (root OFF) |

---

## 4. 적용 조치 (operator 선 배포) — 3회차 시퀀스

대상 파일: `operator/app/src/main/resources/logback-spring.xml` EvaluatorFilter 식 2군데 (CONSOLE 17~26, FILE 41~52) + 회차 3 에서 `operator/app/src/main/resources/log4jdbc.log4j2.properties` 정정 추가.

### 회차 요약

| 회차 | commit | 식/변경 | 결과 | 잔여 문제 |
|------|--------|---------|------|----------|
| 1 | `850b7df8` | 키워드 OR: `formattedMessage.contains("TB_TRB_OX_001") && (hibernate.SQL \|\| log4jdbc.* \|\| jdbc.*)` | SQL 본문 라인은 차단 | wrap 라인 (audit/resultset/connection) 통과 → 절반 잔존 |
| 2 | `92fd87b1` → revert `7eb759b5` | thread 변수: `thread.startsWith("operator-scheduler-") && (...)` | **Pod 부팅 실패** | Janino 컴파일 에러 — `thread` 변수는 evaluator 가 자동 주입하지 않는 식별자 |
| 3 | `756bef5a` | `event.getThreadName().startsWith("operator-scheduler-") && (...)` + properties `log4jdbc.drivers` 를 mysql → mariadb 로 정정 | 최종 적용 | wrap 라인 포함 사실상 0 (cleanup cron 시점만 짧게) |

### 회차 1 — 키워드 식 (부분 완화)

```xml
<expression>
    return formattedMessage != null
           &amp;&amp; formattedMessage.contains("TB_TRB_OX_001")
           &amp;&amp; (logger.equals("org.hibernate.SQL")
               || logger.startsWith("log4jdbc.")
               || logger.startsWith("jdbc."));
</expression>
```

배포 후 실제 로그를 보니 SQL 본문이 박힌 라인 (`Connection.prepareStatement(...)`, `... {executed in N ms}`) 만 사라지고, `ResultSet.next() returned false`, `Connection.commit() returned`, `PreparedStatement.setInt(1, 50)`, 표 헤더 `|------|` 같이 `TB_TRB_OX_001` 키워드 없는 라인은 여전히 통과. 폴링 한 사이클당 약 20+ 줄 중 18 줄이 그대로 남음. 운영 가시성은 미미하게 개선.

### 회차 2 — thread 변수 식 (부팅 실패 → 즉시 revert)

회차 1 의 한계를 메우려고 **호출 컨텍스트 기반** 으로 전환. operator 가 자체 `@Scheduled` 가 없고 `operator-scheduler-*` 풀은 message-lib OutboxPoller 의 2개 메서드 전용임을 grep 으로 확인 후 시도.

```xml
<expression>
    return thread != null
           &amp;&amp; thread.startsWith("operator-scheduler-")
           &amp;&amp; (logger.startsWith("log4jdbc.")
               || logger.startsWith("jdbc.")
               || logger.equals("org.hibernate.SQL"));
</expression>
```

push 후 Pod 가 즉시 부팅 실패. 에러:

```
ERROR in ch.qos.logback.classic.boolex.JaninoEventEvaluator
  - Could not start evaluator with expression [...]
  org.codehaus.commons.compiler.CompileException: Line 2, Column 8:
    Expression "thread" is not an rvalue
```

원인: `JaninoEventEvaluator` 가 자동 주입하는 변수는 `event` / `level` / `logger` / `message` / `formattedMessage` / `throwable` / `marker` / `mdc` / `timeStamp` 만. `thread`, `threadName` 모두 미주입. thread 이름이 필요하면 `event.getThreadName()` 으로 ILoggingEvent 에서 직접 꺼내야 한다.

즉시 `git revert 92fd87b1 && git push origin dev` 로 `7eb759b5` 적용 → 회차 1 식으로 복귀.

### 회차 3 — event.getThreadName() 식 + properties 정정 (최종)

```xml
<!-- operator-scheduler-* 스레드 풀은 message-lib OutboxPoller 의 @Scheduled 메서드 전용이므로
     (operator 자체 @Scheduled 없음), 해당 스레드에서 발생하는 JDBC/Hibernate 로그를 통째로 차단해
     0건 폴링 wrap 라인까지 제거한다. JaninoEventEvaluator 는 thread 변수를 자동 주입하지 않아
     event.getThreadName() 으로 접근한다. -->
<expression>
    return event.getThreadName() != null
           &amp;&amp; event.getThreadName().startsWith("operator-scheduler-")
           &amp;&amp; (logger.startsWith("log4jdbc.")
               || logger.startsWith("jdbc.")
               || logger.equals("org.hibernate.SQL"));
</expression>
```

같은 커밋에서 `log4jdbc.log4j2.properties` 정정:

```properties
# Before
log4jdbc.drivers=com.mysql.cj.jdbc.Driver
# After
log4jdbc.drivers=org.mariadb.jdbc.Driver
log4jdbc.auto.load.popular.drivers=false
log4jdbc.dump.sql.maxlinelength=0
```

부수 발견 — log4jdbc properties 가 기존부터 운영에 박혀 있었는데 `drivers` 값이 MySQL 로 잘못 박혀 있었다. `auto.load.popular.drivers` 가 기본 `true` 라서 log4jdbc 가 우연히 mariadb driver 를 자동 로드해 동작은 했지만, 부팅 시 없는 driver 로드 시도로 잡음 로그가 났을 가능성. mariadb 명시 + auto-load 끄기로 정리.

push 후 정상 부팅 + 폴링 스레드 로그 사실상 0. cleanupSentEvents cron (매일 03:00) 의 짧은 DELETE 만 같이 차단 — SQL 디버깅 손실 무시 가능.

커밋: `[IGMU-1040][operator-api] #time 0.3h fix: outbox 폴러 wrap 라인 차단 (스레드 이름 기반) + log4jdbc 드라이버 mariadb 로 정정` (`756bef5a`)

---

## 5. 교훈

### (1) logback 식은 변경 즉시 부팅 1회 검증
회차 2 가 부팅을 막은 건 사용자가 dev 에 바로 push 한 게 화근. logback evaluator 컴파일 에러는 application 기동 자체를 막아 외관상 "배포 실패" 와 동일하게 보인다. 다음부터 logback 식 변경은 **반드시 로컬 부팅 1회 (`bootRun`) 후 push**. 5초 비용으로 운영 사고 막을 수 있다.

### (2) JaninoEventEvaluator 의 자동 주입 변수는 한정적
직관적으로 "thread name 도 식별자로 노출돼 있겠지" 라고 추측한 게 회차 2 의 원인. 실제로는 다음만 자동 변수:

| 변수 | 타입 | 비고 |
|------|------|------|
| `event` | `ILoggingEvent` | 전체 이벤트, 다른 모든 정보의 fallback 경로 |
| `level` | `Level` | enum |
| `logger` | `String` | logger 이름 |
| `message` | `String` | parameter substitution 전 |
| `formattedMessage` | `String` | 치환된 메시지 |
| `throwable` | `Throwable` | null 가능 |
| `marker` | `Marker` | null 가능 |
| `mdc` | `Map<String,String>` | MDC 전체 |
| `timeStamp` | `long` | epoch ms |

이 목록에 없는 식별자 (`thread`, `threadName`, `host`, `pid` 등) 는 모두 `event.getThreadName()` 같은 메서드 호출로 접근. evaluator 식이 길어지면 차라리 `event` 만 잡고 `event.getXxx()` 일관 호출 스타일이 안전.

### (3) wrap 라이브러리의 underlying driver 는 명시
`log4jdbc.drivers=com.mysql.cj.jdbc.Driver` 가 mariadb 운영에 박혀 있어도 `auto.load.popular.drivers=true` 가 우연히 가려준다. 의존이 정상 동작과 우연 동작 사이의 회색 지대에 박힌다. wrapper driver (`DriverSpy`) 와 underlying driver (`mariadb.jdbc.Driver`) 를 명확히 분리해서 명시할 것.

### (4) 식 확장보다 컨텍스트 매칭이 외과적
회차 1 (`formattedMessage.contains(...)`) 는 키워드 의존이라 다른 코드 경로가 같은 테이블을 SELECT 하면 같이 막힌다. 회차 3 (`event.getThreadName().startsWith(...)`) 는 "outbox 폴러 스레드 안의 모든 JDBC 로그" 라는 호출 컨텍스트로 끊는다. 의미가 더 정확하고 잔여 wrap 라인까지 같이 사라진다. 비슷한 차단이 필요할 때는 **메시지 매칭 < thread/MDC 매칭 < logger 레벨** 순으로 정확도가 올라간다는 점을 기억.

---

## 5-1. 알려진 한계 (회차 3 기준)

cleanupSentEvents (매일 03:00 cron) 도 같은 `operator-scheduler-*` 풀에서 돌므로 그 시점 DELETE SQL 디버깅이 같이 사라진다. operator 가 자체 `@Scheduled` 를 추가하면 같은 풀에 들어가 SQL 디버깅이 같이 차단될 위험. 향후 `@Scheduled` 가 늘면 outbox 전용 `TaskScheduler` 빈을 별 thread name prefix (`outbox-poll-`) 로 분리하는 게 정석.

---

## 6. 후속 조치 (회차 3 기준)

### 단기 (워킹 트리 대기 중)
- executor 동일 변경 — logback 3군데 evaluator 식 + `application-sbh-local.yml` driver 통일. 워킹 트리에 dirty 로 남아 있으나 미커밋. executor 는 root OFF 가 일차 안전망이라 시급성 낮음. 별 PR 로 분리하거나 폐기 결정 대기.
- operator 의 `@Scheduled` 가 늘어날 경우 outbox 전용 `TaskScheduler` 빈 분리 (thread name prefix `outbox-poll-` 로). 현재는 OutboxPoller 2개 메서드 뿐이라 미시급.

### 중장기
- **MDC 키 기반 외과적 필터** — `OutboxPoller.pollAndPublish()` 에 `MDC.put("outbox-poll", "true")` 박고 logback evaluator 가 `mdc.get("outbox-poll") != null && (log4jdbc/jdbc/hibernate.SQL)` 일 때 DENY. thread name 매칭보다 한 단계 더 명시적. message-lib 변경 + operator/executor 양쪽 의존성 동기화 필요라 영향 범위 큼.
- **outbox 폴링 0건 backoff** — N 사이클 연속 empty 시 polling interval 을 2배·4배로 늘리는 adaptive backoff. 발행 지연 SLA 와 트레이드오프 — 학습 글 `05_data/04-02.Outbox 폴러의 0건 SELECT 와 polling cadence.md` 에서 별도 풀이.
- **운영계 driver 재검토** — log4jdbc wrap 자체의 운영 가치 (요청 추적성 등) 가 운영 콘솔 노이즈/성능 비용을 정당화하는지 별 의사결정. 관찰가능성을 OpenTelemetry/APM 으로 옮겼다면 wrap 제거 가능 — 학습 글 `write/05_data/jdbc/04-01.JDBC 드라이버 wrap 로깅의 운영 비용.md` 에서 별도 풀이.

---

## 7. 재발 방지 / 모니터링

- 로그 카운트 SLO 도입 (예: `log4jdbc.log4j2` 채널 분당 N건 이상이면 알람). Loki/CloudWatch 알람으로 가시화.
- 새 서비스를 만들 때 logback 템플릿에 root level 정책 명시 (OFF 또는 INFO + evaluator 식). 합의된 한 가지로 통일.
- driver 선택을 환경별 yml 에 분산시키지 말고 별 표준 (`tps-defaults.yml` 류) 로 모은 뒤 환경 override 만 허용 — 차이 발견이 쉬워짐.

---

## 8. 학습 주제 (Runners-High 차후 글감)

이번 사건은 운영 환경 SRE/관찰가능성 글로 풀어낼 소재가 풍부합니다. 우선순위 순:

### A. (최우선, 작성 완료 → `write/05_data/jdbc/04-01.JDBC 드라이버 wrap 로깅의 운영 비용.md`) JDBC 드라이버 wrap 라이브러리의 운영 비용 모델
- **글감**: "log4jdbc-log4j2 vs p6spy vs datasource-proxy — 운영 콘솔이 감당할 수 있는 wrap 라이브러리는 어디까지인가"
- **본문 축**:
  1. 세 라이브러리가 각각 어떤 logger 이름·레벨로 어떤 호출을 캡처하는지 비교 표 (Connection / PreparedStatement / ResultSet 각 1사이클당 라인 수)
  2. wrap 의 진짜 가치 — SQL 평문 + 바인딩 파라미터 + 실행 시간. 이걸 OTel JDBC instrumentation 으로 대체할 수 있는가
  3. 운영 환경에서 wrap 를 켜둘 때 합리적 가드레일 (sampling, MDC 게이팅, level 조정)
- **왜 학습 가치 있음**: 한국 백엔드 팀 대부분이 log4jdbc·p6spy 를 "켜면 SQL 보임" 정도로만 쓰는데, 실제로는 ResultSet 호출당 1줄을 INFO 로 쏟는다는 것이 운영 환경에서 폭탄. 본인이 직접 사고로 경험한 이야기 + 라이브러리 내부 매커니즘을 풀면 차별화됨.

### B. Logback evaluator filter vs turbo filter vs logger 레벨 — 어떤 레이어로 차단할 것인가
- **글감**: "로그 한 줄을 끄는 4가지 위치 — logback 차단 레이어의 시멘틱과 비용"
- **본문 축**:
  1. **logger level** (가장 빠름, ASL 평가 전 단계 차단)
  2. **TurboFilter** (logger 평가 직후, ILoggingEvent 생성 전)
  3. **EvaluatorFilter on Appender** (이벤트 생성 후, appender 별 평가)
  4. **EvaluatorFilter on Logger** (logger 레벨 안에서)
  - 각 레이어의 평가 시점, 비용 (JaninoEventEvaluator 는 컴파일된 Java 식 매번 평가), MDC 접근 가능성, OnMismatch/OnMatch 의미
- **왜 학습 가치 있음**: 사용자가 이번에 "이 복잡한 식 말고 특정 경로만 끄는 방법" 을 질문한 그 답이 정확히 이 글의 결론. 본인 경험 → 학습 → 다음 결정의 흐름.

### C. "다른 환경에서 다르게 동작" 디버깅 체크리스트
- **글감**: "로컬은 멀쩡한데 운영만 터질 때 — 환경 매트릭스 사고법"
- **본문 축**:
  1. 환경별 다른 변수의 카테고리: (a) 외부 설정 (env, yml profile, k8s ConfigMap), (b) 의존 인스턴스 (driver, MQ broker, DB 버전), (c) 부하 패턴, (d) JVM/OS 자체
  2. 매트릭스를 그리는 습관 — 이번 사건의 6×3 표 (서비스 × 환경 × 결과) 가 한 번에 원인을 가시화한 사례
  3. 환경 격리도 SLO — "로컬에서 운영을 얼마나 똑같이 재현할 수 있는가" 를 점수화
- **왜 학습 가치 있음**: 본인이 sbh-local 이라는 "준 운영" 환경을 따로 만든 것 자체가 환경 격차를 줄이려는 시도였고, 이번 사건이 그 노력이 충분치 않았던 케이스. 진짜 경험에서 나오는 글.

### D. (작성 완료 → `write/05_data/04-02.Outbox 폴러의 0건 SELECT 와 polling cadence.md`) Transactional outbox 폴러의 polling cadence 설계
- **글감**: "500ms fixedDelay 가 정답인 경우, 아닌 경우 — outbox 폴러의 발행 지연 vs DB 부하 트레이드오프"
- **본문 축**:
  1. Transactional Outbox 패턴 자체 복습 (Chris Richardson 원전 + Debezium CDC 대안과 비교)
  2. polling interval 의 결정 변수: 발행 지연 SLA, DB 커넥션 풀 여유, OX 테이블 평균 PENDING 깊이, 동시에 폴러를 띄운 인스턴스 수
  3. adaptive backoff 의 알고리즘 (jitter, exponential, hybrid LISTEN/NOTIFY)
  4. CDC (Debezium) 가 같은 문제를 어떻게 풀어주는가
- **왜 학습 가치 있음**: 이번 사건의 "0건 SELECT 폭주" 가 polling cadence 의 부작용 중 하나. 한 줄짜리 운영 해결책 (log 차단) 으로 끝낼 수도 있지만, 본질은 폴링 모델의 설계 결정. 시리즈로 풀면 두꺼움.

### E. (보너스) Janino + Logback expression 의 보안/성능
- **글감**: "logback evaluator 식에 Janino 가 컴파일하는 그 Java 코드, 운영에서 안전한가"
- **본문 축**: Janino 컴파일 캐시, 식 내부에서 throw 시 동작, 식이 외부 입력을 참조할 때의 위험. 짧은 글.

---

우선순위 추천: **A → B → C** 순. A 는 이번 사건의 핵심 메커니즘, B 는 후속 조치(MDC + evaluator) 의 이론적 기반, C 는 메타-스킬. D 는 깊이 있지만 분량이 크니 시리즈물 한 편으로 별도 기획.

**2026-05-21 갱신**: A 와 D 는 05_data/04-NN 단편으로 동시 작성. B (logback 차단 레이어), C (환경 매트릭스 사고법), E (Janino 식 보안/성능) 는 후속 글감으로 보존 — 본 이슈를 다시 회수할 때 인용 가능.
