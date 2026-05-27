# PPP operator-api JDBC connection 로그 반복 및 DB 세션 점검

- **발생일**: 2026-05-26 13:16 KST (로그 확인 시점)
- **영향 범위**: PPP 클러스터 (`trb-ppp`, 3.0.5.1P / 3.0.5.2 계열) / `trb-app` 네임스페이스 / `Deployment/trb-app-operator-api`. 관련 DB: `Deployment/mariadb-deploy`, `Service/mariadb-deploy`. 서비스 중단 미관측. `jdbc.*` 로그가 주기 출력 + 종료된 이전 Pod IP (`10.233.66.211`) 의 `Sleep` 세션 10개가 MariaDB processlist 에 잔존.
- **심각도**: 운영 가시성 저하 (장애 아님). MariaDB `Threads_connected = 56` / `max_connections = 500` 으로 여유 충분. 격상 조건: (i) `Threads_connected` 가 `max_connections` 의 50% 초과 도달 OR (ii) 비즈니스 트랜잭션 실패 (`CannotCreateTransactionException` 등) 동반 OR (iii) 잔여 Pod IP 세션이 롤아웃 후 감소하지 않고 누적.
- **상태**: 진단 완료, 즉시 조치 불필요. 영구 조치 (운영 프로파일 `jdbc.*` 로그 레벨 하향 / `/actuator/prometheus` DB 조회 경로 재검토 / MariaDB `wait_timeout` 28,800s 운영 정책 검토 / `preStop` + Hikari graceful shutdown 충분성 확인) 미적용.
- **관련 티켓**: 미연결.
- **fix 회차**: 0 (수정 전 진단 보고서)
- **작성자**: Codex (원본 표기 보존)
- **선행 관찰**: `issue/2026-05-21/operator-hikari-set-network-timeout-on-closed.md` — dev/sbh-local 환경에서 같은 `setNetworkTimeout on closed connection` 증상을 *Hikari 풀 회수 race* 각도로 1차 진단한 자료. 본 보고서는 동일 증상의 **PPP 환경 재관측 + Prometheus scrape DB 조회 경로 + 종료 Pod 잔여 세션 각도** 보강.

---

## 1. 장애 현상 (Symptom)

### 1-1. 사용자 관점

`trb-app` 네임스페이스의 `operator-api` 로그에 아래와 같은 JDBC 로그가 주기적으로 출력되었다.

```text
2026-05-26 13:16:00.138 ERROR [] [CP connection closer] jdbc.sqlonly - 5. Connection.setNetworkTimeout(..., 15000;
2026-05-26 13:16:00.137 ERROR [] [CP connection closer] jdbc.audit - 4. Connection.setNetworkTimeout(..., 15000;
2026-05-26 13:16:00.137 ERROR [] [CP connection closer] jdbc.sqltiming - 3. Connection.setNetworkTimeout(..., 15000;
```

같은 네임스페이스의 MariaDB와 연결하는 구조이므로 다음 가능성을 확인했다.

- `operator-api` 내부 좀비 프로세스 존재 여부
- HikariCP 커넥션 풀 누수 여부
- 종료된 Pod의 DB 세션이 MariaDB에 남아 있는지 여부
- DB `max_connections` 한계 접근 여부

### 1-2. 시스템 관점

확인 시점의 `operator-api`는 정상 기동 상태였다.

```text
trb-app-operator-api-6f7bff9d65-6rtvn   2/2   Running   0   26m   10.233.64.233
```

Deployment 상태도 정상 수렴 상태였다.

```text
Deployment/trb-app-operator-api
image: harbor.dev.trombone-v2.okestro.cloud/trb/operator-api:20260526-131313
readyReplicas: 1
updatedReplicas: 1
```

---

## 2. 환경/상태 스냅샷 (Evidence)

### 2-1. 서비스 및 엔드포인트

```bash
kubectl get svc -n trb-app
kubectl get endpoints -n trb-app
```

확인 결과:

| 리소스 | 값 |
|--------|----|
| `Service/mariadb-deploy` | `ClusterIP 10.233.58.16`, `NodePort 30006`, `3306/TCP` |
| `Endpoints/mariadb-deploy` | `10.233.71.17:3306` |
| `Service/trb-app-operator-api` | `ClusterIP 10.233.43.235`, `80/TCP` |
| `Endpoints/trb-app-operator-api` | `10.233.64.233:8091` |

`backend-common-cm`의 JDBC URL은 `mariadb-deploy.trb-app.svc.cluster.local:3306`를 사용한다. 문서에는 DB 계정/비밀번호 값은 기록하지 않는다.

### 2-2. operator-api 런타임 상태

```bash
kubectl describe pod -n trb-app -l app.kubernetes.io/name=operator-api
```

확인 결과:

| 항목 | 값 |
|------|----|
| Pod | `trb-app-operator-api-6f7bff9d65-6rtvn` |
| Pod IP | `10.233.64.233` |
| Node | `pd-pppv2-trb-worker-5` |
| Container restart | `operator-api=0`, `istio-proxy=0` |
| 시작 시각 | 2026-05-26 13:15:16 KST |
| 특이 이벤트 | 초기 startup probe `500` 3회 후 정상 Ready |

컨테이너 내부 프로세스 확인:

```bash
kubectl exec -n trb-app deploy/trb-app-operator-api -c operator-api -- sh -c \
  'ps -ef; find /proc -maxdepth 2 -name status 2>/dev/null | xargs grep -H "^State:" 2>/dev/null | grep zombie || true'
```

결과:

```text
UID   PID  PPID  CMD
root    1     0  java -cp @/app/jib-classpath-file org.okestro.tps.OperatorApplication

zombie 프로세스 없음
```

### 2-3. operator-api DB 소켓 상태

```bash
kubectl exec -n trb-app deploy/trb-app-operator-api -c operator-api -- sh -c \
  '(ss -tanp || netstat -tanp) 2>/dev/null | grep 3306 || true'
```

확인 결과, `operator-api` Java 프로세스가 DB로 유지 중인 established socket은 5개였다.

```text
10.233.64.233:<port> -> 10.233.58.16:3306 users:(("java",pid=1,...))
```

이는 `backend-common-cm`에 설정된 Hikari 최소 idle 값과 일치한다.

```text
HIKARI_MIN_IDLE=5
HIKARI_MAX_POOL_SIZE=10
HIKARI_IDLE_TIMEOUT=600000
HIKARI_MAX_LIFETIME=1770000
HIKARI_CONNECTION_TIMEOUT=30000
HIKARI_LEAK_DETECTION_THRESHOLD=60000
```

### 2-4. MariaDB processlist 요약

```bash
kubectl exec -n trb-app deploy/mariadb-deploy -c mariadb -- sh -c '
  MYSQL_PWD="$TRB_DB_PASSWORD" mariadb -u"$TRB_DB_USERNAME" -e "
    SHOW GLOBAL STATUS LIKE '\''Threads_connected'\'';
    SHOW GLOBAL STATUS LIKE '\''Max_used_connections'\'';
    SHOW FULL PROCESSLIST;
  "
'
```

실제 실행 시에는 컨테이너 환경변수 또는 Secret에서 계정 정보를 사용한다. 문서에는 평문 비밀번호를 남기지 않는다.

확인 결과:

| 항목 | 값 |
|------|----|
| `Threads_connected` | `56` |
| `Max_used_connections` | `108` |
| `max_connections` | `500` |
| `wait_timeout` | `28800`초 |
| `interactive_timeout` | `28800`초 |

클라이언트 IP별 DB 세션 요약:

| Client IP | 매핑 | DB | Command | Count | 해석 |
|-----------|------|----|---------|-------|------|
| `10.233.64.233` | 현재 `operator-api` Pod | `TPS` | `Sleep` | `5` | Hikari `minIdle=5`와 일치 |
| `10.233.69.166` | `executor` Pod | `TPS` | `Sleep` | `5` | 앱 풀 idle 세션 |
| `10.233.71.116` | `transfer` Pod | `TPS` | `Sleep` | `5` | 앱 풀 idle 세션 |
| `10.233.70.115` | `auth-api` Pod | `TPS` | `Sleep` | `5` | 앱 풀 idle 세션 |
| `10.233.69.58` | `common-api` Pod | `TPS` | `Sleep` | `5` | 앱 풀 idle 세션 |
| `10.233.64.40` | `scheduler` Pod | `TPS/config` | `Sleep` | `15` | 복수 datasource 사용 가능 |
| `10.233.68.58` | `notificator` Pod | `TPS` | `Sleep` | `5` | 앱 풀 idle 세션 |
| `10.233.66.211` | 현재 Pod 미매핑 | `TPS` | `Sleep` | `10` | 종료된 이전 Pod의 잔여 세션 가능성 |

`10.233.66.211`은 아래 명령으로 현재 Pod에 매핑되지 않음을 확인했다.

```bash
kubectl get pods -A -o wide | rg '10.233.66.211'
```

결과:

```text
현재 실행 중인 Pod 없음
```

### 2-5. 로그 패턴

```bash
kubectl logs -n trb-app deploy/trb-app-operator-api -c operator-api --since=45m \
  | rg -n -C 6 '13:16:00|setNetworkTimeout|CP connection closer|Connection closed|Connection\.close\(\)|Connection\.isValid'
```

확인된 주요 패턴:

```text
2026-05-26 13:15:22.195 INFO  [main] com.zaxxer.hikari.HikariDataSource - CP - Starting...
2026-05-26 13:15:22.362 INFO  [main] com.zaxxer.hikari.pool.HikariPool - CP - Added connection ...
2026-05-26 13:15:22.363 INFO  [main] com.zaxxer.hikari.HikariDataSource - CP - Start completed.

2026-05-26 13:16:12.138 INFO  [http-nio-8091-exec-1] SERVER-INCOMING uri=/operator/api/actuator/prometheus
2026-05-26 13:16:12.149 INFO  [http-nio-8091-exec-1] jdbc.audit - Connection.isValid(5) returned true
2026-05-26 13:16:12.149 INFO  [http-nio-8091-exec-1] jdbc.sqlonly - select count(...) where STTS_CD='PENDING'
2026-05-26 13:16:12.150 INFO  [http-nio-8091-exec-1] jdbc.sqltiming - ... {executed in 1 msec}
2026-05-26 13:16:12.154 INFO  [http-nio-8091-exec-1] SERVER-OUTGOING uri=/operator/api/actuator/prometheus status=200
```

`/operator/api/actuator/prometheus`가 10초 주기로 호출되며 DB 조회와 `Connection.isValid()` 로그가 반복된다.

커넥션 교체 시점에는 HikariCP 내부 스레드가 커넥션을 닫고 새 커넥션을 보충한다.

```text
2026-05-26 13:44:09.920 INFO [CP connection closer] jdbc.connection - Connection closed
2026-05-26 13:44:09.920 INFO [CP connection closer] jdbc.audit - Connection.close() returned
2026-05-26 13:44:09.927 INFO [CP connection adder] jdbc.connection - Connection opened
```

---

## 3. 근본 원인 분석 (Root Cause)

### 3-1. 직접 원인: log4jdbc가 HikariCP 내부 커넥션 동작을 상세 출력

문제 로그의 thread name인 `CP connection closer`는 HikariCP가 커넥션을 정리하는 내부 스레드다.

`Connection.setNetworkTimeout(..., 15000)`은 HikariCP가 커넥션 close 또는 validation 과정에서 JDBC driver에 network timeout을 적용하는 호출로 보인다. 이 호출 자체는 DB 장애나 커넥션 누수를 의미하지 않는다.

이번 조사에서 `operator-api`의 현재 DB 연결 수는 5개였고, 설정값 `HIKARI_MIN_IDLE=5`와 정확히 일치했다.

```text
현재 operator-api DB 세션 수 = 5
HIKARI_MIN_IDLE = 5
HIKARI_MAX_POOL_SIZE = 10
```

따라서 현재 실행 중인 `operator-api`가 DB 커넥션을 계속 누적하고 있다는 증거는 없다.

### 3-2. 주기 로그의 원인: Prometheus scrape 경로가 DB 조회를 수행

`/operator/api/actuator/prometheus` 요청이 약 10초마다 들어오며, 이 요청 처리 중 아래 쿼리가 실행된다.

```sql
select count(oee1_0.OX_ID)
from TB_TRB_OX_001 oee1_0
where oee1_0.STTS_CD='PENDING'
```

이 쿼리는 짧게 실행되고, 로그상 실행 시간은 0~2ms 수준이다. DB 부하 징후보다는 메트릭 수집 경로에서 DB-backed gauge 또는 repository 조회가 수행되는 구조로 판단된다.

### 3-3. 잔여 세션 원인: 롤아웃 중 종료된 Pod의 Sleep 세션

MariaDB processlist에 `10.233.66.211`에서 온 `Sleep` 세션 10개가 있었지만, 현재 클러스터의 Pod IP 목록에는 해당 IP가 없었다.

같은 시간대에 `operator-api`는 여러 번 이미지 롤아웃됐다.

```text
trb-app-operator-api-5f8487fd6   image operator-api:20260526-095302
trb-app-operator-api-7ff7fd4bc6  image operator-api:20260526-102808
trb-app-operator-api-5df6c7c7f6  image operator-api:20260526-110836
trb-app-operator-api-bb54bd76d   image operator-api:20260526-130012
trb-app-operator-api-6f7bff9d65  image operator-api:20260526-131313
```

이력상 `10.233.66.211` 세션은 현재 Pod가 아니라 종료된 이전 Pod의 연결이 DB 서버에 `Sleep` 상태로 남은 것으로 판단된다.

DB의 `wait_timeout`은 28800초로 기본 8시간 수준이므로, 애플리케이션 종료 시 TCP close가 DB에 즉시 반영되지 않으면 잔여 세션이 오래 보일 수 있다.

### 3-4. 인과 체인

```text
operator-api 신규 이미지 롤아웃 반복
  → 기존 Pod 종료 및 신규 Pod 기동
    → 신규 Pod는 HikariCP minIdle=5에 맞춰 DB 연결 5개 유지
    → 이전 Pod의 일부 DB 세션이 MariaDB processlist에 Sleep 상태로 잔존
      → log4jdbc가 HikariCP close/add/validation 호출을 jdbc.* 카테고리로 상세 출력
        → Connection.setNetworkTimeout 로그가 DB 장애 또는 커넥션 누수처럼 보임
```

---

## 4. 해결 조치 (Resolution)

### 4-1. 즉시 조치 (Mitigation)

현재 시점에는 서비스 중단이나 DB 연결 한계 접근이 관측되지 않았으므로 즉시 Pod 재시작 또는 DB 재기동은 필요하지 않다.

잔여 세션을 즉시 정리해야 할 경우에는 현재 Pod에 매핑되지 않는 client IP만 선별해 `KILL`한다.

사전 확인:

```bash
kubectl get pods -A -o wide | rg '10.233.66.211'

kubectl exec -n trb-app deploy/mariadb-deploy -c mariadb -- sh -c '
  mariadb -u"$TRB_DB_USERNAME" -p"$TRB_DB_PASSWORD" -e "
    SELECT ID, USER, HOST, DB, COMMAND, TIME
    FROM information_schema.PROCESSLIST
    WHERE HOST LIKE '\''10.233.66.211:%'\'';
  "
'
```

정리 예시:

```sql
KILL <process_id>;
```

주의:

- 현재 실행 중인 Pod IP와 매핑되는 세션은 임의로 종료하지 않는다.
- `KILL` 전에는 반드시 `kubectl get pods -A -o wide`로 해당 IP가 live Pod인지 확인한다.

### 4-2. 영구 조치 (Fix)

권장 조치:

1. `jdbc.audit`, `jdbc.sqlonly`, `jdbc.sqltiming`, `jdbc.connection` 로그 레벨을 운영 환경에서 낮춘다.
2. `/actuator/prometheus`에서 DB 조회가 필요한 메트릭인지 확인하고, 필요하면 캐시 또는 lightweight indicator로 변경한다.
3. MariaDB `wait_timeout`을 운영 정책에 맞게 낮추는 방안을 검토한다.
4. 롤아웃 시 `preStop`/`terminationGracePeriodSeconds`와 Spring graceful shutdown이 Hikari pool close를 완료하기에 충분한지 확인한다.

현재 Deployment에는 `preStop: sleep 10`, `terminationGracePeriodSeconds: 30`, `SERVER_SHUTDOWN=graceful`, `SPRING_LIFECYCLE_TIMEOUT_PER_SHUTDOWN_PHASE=25s`가 설정되어 있다. 일반적으로 충분해 보이나, 잔여 세션이 반복적으로 누적되면 애플리케이션 종료 로그에서 Hikari shutdown 완료 여부를 확인해야 한다.

### 4-3. 검증

반복 점검 명령:

```bash
kubectl get pods -n trb-app -o wide | rg 'operator-api|mariadb'

kubectl exec -n trb-app deploy/trb-app-operator-api -c operator-api -- sh -c \
  '(ss -tanp || netstat -tanp) 2>/dev/null | grep 3306 || true'

kubectl exec -n trb-app deploy/mariadb-deploy -c mariadb -- sh -c '
  mariadb -u"$TRB_DB_USERNAME" -p"$TRB_DB_PASSWORD" -e "
    SELECT SUBSTRING_INDEX(HOST, '\'':'\'', 1) AS client_ip,
           DB, COMMAND, COUNT(*) AS cnt, MIN(TIME) AS min_sec, MAX(TIME) AS max_sec
    FROM information_schema.PROCESSLIST
    GROUP BY client_ip, DB, COMMAND
    ORDER BY cnt DESC, max_sec DESC;
  "
'
```

정상 기준:

| 항목 | 기준 |
|------|------|
| `operator-api` Pod | `2/2 Running`, restart 증가 없음 |
| `operator-api` DB 세션 | 기본 idle 5개 수준 유지 |
| MariaDB `Threads_connected` | `max_connections=500` 대비 여유 있음 |
| 잔여 Pod IP 세션 | 롤아웃 후 점진 감소 또는 운영자가 선별 정리 |
| 로그 | `Connection.setNetworkTimeout` 단독 반복은 장애로 보지 않음 |

---

## 5. 재발 방지 (Prevention)

| 항목 | 조치 | 담당 | 기한 |
|------|------|------|------|
| 로그 레벨 정리 | 운영 프로파일에서 `jdbc.audit`, `jdbc.sqlonly`, `jdbc.sqltiming`, `jdbc.connection` 로그 레벨 하향 | 애플리케이션 담당 | 다음 배포 전 |
| 메트릭 경로 점검 | `/actuator/prometheus`가 10초마다 DB 조회를 수행하는 구조가 필요한지 검토 | 애플리케이션 담당 | 다음 성능 점검 시 |
| DB 세션 Runbook | `PROCESSLIST`에서 live Pod IP와 미매핑 IP를 구분하는 절차 문서화 | 플랫폼 운영 | 즉시 |
| 롤아웃 후 점검 | 이미지 롤아웃 후 `Threads_connected`, client IP별 Sleep 세션 수 확인 | 플랫폼 운영 | operator-api 배포 시 |
| Timeout 정책 | MariaDB `wait_timeout` 28800초 유지 여부 검토 | DBA/플랫폼 운영 | 운영 정책 확정 시 |

---

## 6. 참고 명령

### 현재 Pod와 IP 확인

```bash
kubectl get pods -n trb-app -o wide
kubectl get rs -n trb-app -l app.kubernetes.io/name=operator-api -o wide
```

### operator-api 로그 필터

```bash
kubectl logs -n trb-app deploy/trb-app-operator-api -c operator-api --since=2h \
  | rg -n 'ERROR|setNetworkTimeout|CP connection closer|Connection\.close|Connection\.isValid|Hikari|Pool|Exception|Communications|timeout'
```

### DB 세션 확인

```bash
kubectl exec -n trb-app deploy/mariadb-deploy -c mariadb -- sh -c '
  mariadb -u"$TRB_DB_USERNAME" -p"$TRB_DB_PASSWORD" -e "
    SHOW GLOBAL STATUS LIKE '\''Threads_connected'\'';
    SHOW GLOBAL STATUS LIKE '\''Max_used_connections'\'';
    SHOW VARIABLES LIKE '\''max_connections'\'';
    SHOW VARIABLES LIKE '\''wait_timeout'\'';
    SHOW FULL PROCESSLIST;
  "
'
```

### 좀비 프로세스 확인

```bash
kubectl exec -n trb-app deploy/trb-app-operator-api -c operator-api -- sh -c \
  'find /proc -maxdepth 2 -name status 2>/dev/null | xargs grep -H "^State:" 2>/dev/null | grep zombie || true'
```

---

## 7. 최종 판단

이번 현상은 `operator-api`의 좀비 프로세스나 명확한 커넥션 누수 장애로 판단되지 않는다.

현재 실행 중인 `operator-api`는 HikariCP 설정에 맞는 5개 idle DB 세션만 유지하고 있으며, DB 전체 연결 수도 `max_connections=500` 대비 여유가 있다.

다만 현재 Pod에 매핑되지 않는 IP의 Sleep 세션이 관측되었으므로, 잦은 롤아웃 후에는 MariaDB processlist에서 종료된 Pod의 잔여 세션을 확인하고 필요 시 선별 정리한다. 로그 소음은 log4jdbc 운영 로그 레벨 조정으로 완화하는 것이 적절하다.

---

## 8. 참고

- `issue/2026-05-21/operator-hikari-set-network-timeout-on-closed.md` — dev/sbh-local 환경에서 같은 `Connection.setNetworkTimeout cannot be called on a closed connection` 증상을 관측한 1차 진단. 본 보고서가 *서버/네트워크 idle 끊김 race* (가설 a) 와 *max-lifetime 안전 마진 부족* (가설 b) 을 다룬다면, 본 (PPP) 보고서는 같은 driver/log4jdbc 가 만드는 *주기 로그 출력 자체* 와 *종료된 Pod 잔여 Sleep 세션* 각도로 보강. 두 보고서가 같은 증상 - 다른 환경 - 다른 단면의 한 쌍을 이룬다.
- 같은 디렉토리 `redpanda-schema-registry-schemas-topic-retention-corruption.md` — 동일 작업일(2026-05-26) 로컬 환경의 별건. 본 건과 인과 무관.
