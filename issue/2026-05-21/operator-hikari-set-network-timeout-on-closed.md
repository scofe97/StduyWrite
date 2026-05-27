# operator k8s HikariCP `setNetworkTimeout` on closed connection — 풀 회수 race 로그

- **발생일**: 2026-05-21 21:40:02.185~.186 (KST)
- **영향 범위**: TPS `operator-api` dev/k8s. 동일 timestamp 1초 구간에 `CP connection closer` 스레드가 5+회 연속 실패. 비즈니스 트랜잭션 실패 동반 흔적 없음. local·sbh-local·executor 환경 영향 없음.
- **심각도**: 운영 가시성 저하 (장애 아님). Hikari 가 release 시점에 죽은 connection 정리하는 *설계된 동작* 의 잡음이지만, 동일 패턴이 2026-05-19 에 이어 두 번째 관측 → 영구 조치 권고. 분당 N회 (예: 5회) 이상 재발 또는 비즈니스 트랜잭션 실패 동반 시 격상.
- **상태**: 진단 완료, 조치 미적용. `keepalive-time` 추가 + `max-lifetime` 단축 결합 권고. 실제 매니페스트 변경은 별도 PR.
- **관련 티켓**: 미연결 (dev 로그 잡음 트래킹 티켓 존재 시 추가)
- **fix 회차**: 0 (수정 전 진단 보고서)
- **선행 관찰**: 2026-05-19 동일 dev 환경 `operator-scheduler-3` 에서 `conn=29761` 1건으로 한 차례 기록됨 — `~/okestro/tps-gitlab2/operator/.sbh/issues.md` "2026-05-19 HikariCP - setNetworkTimeout on closed connection" 항목

---

## 1. 증상

`operator` Pod stdout 에 2026-05-21 21:40:02.185 ~ 21:40:02.186 1초 구간에 다음 패턴이 conn id 만 바꾸며 5+회 반복.

```
2026-05-21 21:40:02.186 ERROR [] [CP connection closer] jdbc.sqlonly - 54. Connection.setNetworkTimeout(java.util.concurrent.ThreadPoolExecutor@46e05384[Running, pool size = 0, active threads = 0, queued tasks = 0, completed tasks = 0], 15000;
java.sql.SQLSyntaxErrorException: (conn=41018) Connection.setNetworkTimeout cannot be called on a closed connection
    at org.mariadb.jdbc.export.ExceptionFactory.createException(ExceptionFactory.java:289)
    at org.mariadb.jdbc.export.ExceptionFactory.create(ExceptionFactory.java:343)
    at org.mariadb.jdbc.Connection.setNetworkTimeout(Connection.java:766)
    at net.sf.log4jdbc.sql.jdbcapi.ConnectionSpy.setNetworkTimeout(ConnectionSpy.java:1120)
    at com.zaxxer.hikari.pool.PoolBase.setNetworkTimeout(PoolBase.java:561)
    at com.zaxxer.hikari.pool.PoolBase.quietlyCloseConnection(PoolBase.java:136)
    at com.zaxxer.hikari.pool.HikariPool.lambda$closeConnection$1(HikariPool.java:444)
    at scouter.agent.wrapper.async.WrTask.run(WrTask.java:35)
    at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
    at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
    at java.base/java.lang.Thread.run(Thread.java:833)

2026-05-21 21:40:02.186 WARN  [] [operator-scheduler-3] com.zaxxer.hikari.pool.PoolBase - CP - Failed to validate connection net.sf.log4jdbc.sql.jdbcapi.ConnectionSpy@60b9137f ((conn=41018) Connection.setNetworkTimeout cannot be called on a closed connection). Possibly consider using a shorter maxLifetime value.
```

같은 timestamp 구간에서 잡힌 conn id 표본: `conn=41003`, `conn=41008`, `conn=41018` (최소 3건, 동일 시각에 한꺼번에 회수 중). 모두 동일 호출 경로 `HikariPool.closeConnection → PoolBase.quietlyCloseConnection → PoolBase.setNetworkTimeout` 에서 실패.

요점 세 가지:

| 단서 | 의미 |
|------|------|
| 스레드 `CP connection closer` | Hikari 가 *풀에 들고 있던* connection 을 **닫는 중** (idle/lifetime 만료 회수). 사용자 트랜잭션 경로 아님. |
| 메서드 `setNetworkTimeout(...)` | HikariCP `PoolBase.quietlyCloseConnection` 이 close 직전에 timeout 을 짧게 설정해 hang 방지 — 이 호출이 실패. 즉 *close 도중* 에러. |
| 동반 WARN `Failed to validate connection ... Possibly consider using a shorter maxLifetime value.` | Hikari 가 다른 스레드 (`operator-scheduler-3`) 에서 같은 conn 을 *빌리려고 검증* 하다 invalid 판정. Hikari 가 명시적으로 `maxLifetime` 단축을 권고. |

conn id 가 `41xxx` 대역 → 짧은 시간에 connection 이 다수 새로 생성/회수되어 ID 가 빠르게 증가한 상태. 풀이 정상 안정화 상태가 아니라 *재생성 사이클* 중.

---

## 2. 근본 원인

두 가지 race 가설의 조합이다. Hikari WARN 메시지 자체가 (b) 를 직접 가리킨다.

### (a) 서버/네트워크 측 idle 끊김 → 풀 회수 race

MariaDB `wait_timeout` / K8s Service idle timeout (기본 15분 추정) / conntrack idle 만료 중 어느 하나가 *Hikari max-lifetime 보다 짧으면*, 서버가 socket 을 먼저 끊은 상태에서 Hikari `CP connection closer` 가 `max-lifetime` 만료 회수를 시도. close 경로의 첫 호출 `setNetworkTimeout` 이 이미 닫힌 socket 위에서 실패 → 예외 발생. Hikari 는 이 예외를 *예상 동작* 으로 받아들이고 다음 borrow 에는 정상 connection 을 새로 만든다.

`isClosed()` returned `true` 확인 + `Connection closed` INFO 로그가 직전에 함께 찍히는 점이 이 경로를 가리킨다.

### (b) max-lifetime 과 서버 timeout 안전 마진 부족

현재 `HIKARI_MAX_LIFETIME = 1,770,000 ms = 29분 30초`. HikariCP 공식 권고는 *DB connection timeout 보다 최소 30초 짧게* 설정이다. 측정 안 된 dev 환경 서버 측 timeout 의 어느 하나가 30분 미만이면 race window 가 매번 열린다. WARN 메시지가 *`Possibly consider using a shorter maxLifetime value.`* 라고 못박는 이유다.

`keepalive-time` 이 *미설정* (Hikari 기본 = disabled) 이라 idle 동안 stale 사전 검출 경로가 없는 것도 race 확률을 키운다. idle ping 이 있었다면 conn 이 끊긴 즉시 풀에서 *조용히* 제거되고 borrow 시점에 invalid 판정 자체가 안 일어난다.

### 보강 — 같은 회수 사이클에서 5+회 동시 발생한 이유

`CP connection closer` 스레드 1개가 *동일 시각에* 여러 connection 을 순차 close 한다. 풀 내 idle connection 들이 *같은 시점에 생성* 됐다면 `max-lifetime` 도 같은 시점에 만료. 한 회수 사이클에서 5+회 실패가 연속 찍힌 것은 *풀 초기 워밍업 직후의 한 묶음* 이 일제히 만료에 도달한 표시.

---

## 3. 현재 설정 매트릭스

| 항목 | 값 | 출처 |
|------|-----|------|
| `spring.datasource.hikari.max-lifetime` | 1,770,000 ms (29분 30초) | `tps-manifest/values/global-values.yaml:31` (`HIKARI_MAX_LIFETIME`) |
| `spring.datasource.hikari.idle-timeout` | 600,000 ms (10분) | `tps-manifest/values/global-values.yaml:32` (`HIKARI_IDLE_TIMEOUT`) |
| `spring.datasource.hikari.connection-timeout` | 30,000 ms (30초) | `tps-manifest/values/global-values.yaml:30` (`HIKARI_CONNECTION_TIMEOUT`) |
| `spring.datasource.hikari.keepalive-time` | **미설정** (Hikari 기본 = disabled) | (코드/매니페스트 부재) |
| `pool-name` | `CP` | `operator/app/src/main/resources/application.yml:36` |
| `driver-class-name` | `net.sf.log4jdbc.sql.jdbcapi.DriverSpy` | `operator/app/src/main/resources/application.yml:34` |
| MariaDB `wait_timeout` | **미측정** | `SHOW GLOBAL VARIABLES LIKE 'wait_timeout';` 명령 필요 |
| MariaDB `interactive_timeout` | **미측정** | `SHOW GLOBAL VARIABLES LIKE 'interactive_timeout';` 명령 필요 |
| K8s Service / LB idle timeout | **미측정** | 클러스터 네트워크 정책 확인 필요 |

---

## 4. 영향 평가

- **사용자 영향**: 0. 비즈니스 트랜잭션 실패 동반 흔적 없음. Hikari 가 다음 borrow 에서 새 connection 으로 자동 회복.
- **운영 영향**: 로그 잡음. ERROR + 스택트레이스가 한 사이클에 5+회 찍히므로 다른 ERROR 신호가 묻힘. `operator-outbox-log-flood.md` (`log4jdbc.log4j2` 잡음) 와 합쳐지면 가시성 추가 저하.
- **재발 패턴**: 2026-05-19 1회 → 2026-05-21 5+회. 빈도 증가 추세 가능. 한 달 모니터링 후 격상 검토.
- **격상 조건**: (i) 분당 5회 이상 반복 OR (ii) 비즈니스 트랜잭션 실패 (`CannotCreateTransactionException`, `JpaSystemException` 등) 동반 OR (iii) Outbox 발행 지연 동반.

---

## 5. 권고 조치 — B + C 결합

`keepalive-time` 추가로 race window 자체를 줄이고, `max-lifetime` 단축으로 서버 timeout 안쪽에 안전 마진 확보. 두 개 모두 매니페스트 환경변수 변경만으로 적용되며 코드 수정 불필요.

| 항목 | 변경 종류 | 값 | 위치 | 근거 |
|------|----------|----|----- |------|
| **B. `keepalive-time` 추가** | env 신규 + yml 라인 추가 | `HIKARI_KEEPALIVE_TIME=300000` (5분) | (1) `tps-manifest/values/global-values.yaml` 의 `HIKARI_*` 블록에 한 줄 추가 (2) `operator/app/src/main/resources/application-k8s.yml:46` 아래에 `keepalive-time: ${HIKARI_KEEPALIVE_TIME}` 라인 추가 | idle 5분마다 ping → stale 사전 검출 → release race 자체 감소. Hikari `> 30000ms` 권고 안. |
| **C. `max-lifetime` 단축** | env 값 변경 | `HIKARI_MAX_LIFETIME=840000` (14분) | `tps-manifest/values/global-values.yaml:31` 값 교체 | 1,800s (30분) 미만으로 잡아 K8s Service idle 정책 안쪽. dev MariaDB `wait_timeout` 디폴트 28,800s 대비 충분히 짧음. wait_timeout 실측 후 더 단축 여지. |

### 적용 전 필수 진단 — D

```bash
# MariaDB 측 timeout 값
kubectl -n <mariadb-ns> exec <mariadb-pod> -- \
  mysql -uroot -p<password> -e "SHOW GLOBAL VARIABLES LIKE 'wait_timeout';"
kubectl -n <mariadb-ns> exec <mariadb-pod> -- \
  mysql -uroot -p<password> -e "SHOW GLOBAL VARIABLES LIKE 'interactive_timeout';"

# 현재 풀에서 사용 중인 connection 수 (재발 빈도 추정용)
kubectl -n <mariadb-ns> exec <mariadb-pod> -- \
  mysql -uroot -p<password> -e "SHOW STATUS LIKE 'Threads_connected';"

# 21:40 전후 K8s 이벤트 (선행 이벤트 확인)
kubectl -n <op-ns> get events --sort-by='.lastTimestamp' \
  | grep -E '21:3[5-9]|21:4[0-5]'
```

D 결과가 `wait_timeout < 1,800` 이면 C 의 14분도 부족. 더 짧게 (예: `wait_timeout - 60s`) 잡거나 서버 측을 늘려야 한다. *D 결과를 본 문서 §3 매트릭스에 채워 넣은 뒤에 B+C 의 영구 PR 을 작성*.

### 대안 (참고만)

| 항목 | 설명 | 비고 |
|------|------|------|
| **A. 무시/관찰** | 분당 빈도 < 1회 + 비즈니스 실패 동반 없음이 한 달 유지되면 잡음으로 둠 | 운영자 판단. 본 보고서 §4 의 격상 조건을 모니터링 알람으로 박을 것. |
| **E. operator rollout restart** | `kubectl -n <op-ns> rollout restart deployment/operator-api` 로 풀 전체 재생성 | 임시 회복용. 영구 조치 아님. B+C 적용 후에는 거의 불필요. |

---

## 6. 모니터링 · 회수 후속

- **Grafana 패널 점검**: `hikari_connections_active`, `hikari_connections_idle`, `hikari_connections_pending`, `hikari_connections_acquire_seconds`, `mysql_global_status_aborted_clients`. 누락 패널은 추가. (참고 — 같은 폴더의 `outbox-prometheus-not-collected.md` 처럼 operator-api 의 `/actuator/prometheus` 가 노출되는지도 함께 점검 필요.)
- **알람 조건**: `rate(hikari_connections_acquire_seconds_count{pool="CP"}[5m]) > N` 또는 로그 측에서 `Failed to validate connection` 분당 5회 초과.
- **재발 추적**: 2026-06-21 자로 캘린더 등록. B+C 적용 후 4주간 같은 ERROR 발생 0건이면 안정화로 판정.
- **횡전개 검토**: 동일 매니페스트 (`tps-manifest/values/global-values.yaml`) 를 공유하는 다른 모듈 (`executor`, `pipeline-api`, `auth-api`, `notificator`, `scheduler`, `ppln-logging-api`, `pms-api`, `workflow-api`, `common-api`) 도 동일 race 가능. B+C 가 모듈별이 아니라 *global-values* 레벨이라면 한 PR 로 횡전개 가능.

---

## 7. 미해결 잔여

- MariaDB `wait_timeout` / `interactive_timeout` 실측치 — 본 보고서 작성 시점 미확보. §5 D 명령으로 채워야 함.
- 같은 노드/네트워크 이벤트 (Pod 재배치, NodePort conntrack 만료, MariaDB Pod 흔들림) 가 21:40:02 직전에 있었는지 미확인. `kubectl -n <op-ns> get events`, `kubectl -n <mariadb-ns> describe pod <mariadb>` 로 확인 권장.
- 21:40:02 직전 후 5분 구간의 비즈니스 트랜잭션 실패율 — 어플리케이션 메트릭 (`http_server_requests_seconds_count{status="5xx"}`) 으로 확인하면 P3 / P2 판정에 결정적 증거.
- `setNetworkTimeout` 호출 자체가 `quietlyCloseConnection` 안에서 *quietly* 처리되도록 설계됐는데도 ERROR 레벨 로그가 찍히는 이유 — `log4jdbc.log4j2` 의 `DriverSpy` 가 *모든 JDBC 호출* 의 예외를 logger 로 흘리는 부작용 가능 (`operator-outbox-log-flood.md` 와 같은 driver 영향 가능성).

---

## 8. 참고

- `~/okestro/tps-gitlab2/operator/.sbh/issues.md` 2026-05-19 항목 — 동일 증상 1차 관측, 짧은 메모 형태. 본 보고서가 그 항목의 *상세본 + 후속 조치 권고*.
- `~/okestro/tps-gitlab2/executor/.sbh/2026-05-19/error-log/00-outbox-poller-db-socket-closed.md` — executor 측 `EOFException: socket was closed by server` 사례. 끊김 시점 (사용 직전) 은 다르지만 *원인 가설 (HikariCP race)* 동일.
- `~/okestro/tps-gitlab2/operator/.sbh/kafka-broker-not-available-troubleshooting.md` — 같은 dev 환경 네트워크 흔들림 사례.
- 같은 폴더 `operator-outbox-log-flood.md` (2026-05-21) — `DriverSpy` 가 logger 잡음을 만든 별건. 본 건의 ERROR 로그 레벨도 driver 영향 가능성 §7 참조.
- HikariCP 공식 — *"maxLifetime should be set to a value at least 30 seconds less than any database or infrastructure imposed connection time limit."* (`https://github.com/brettwooldridge/HikariCP` README)
