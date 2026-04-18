# Ch.14 - MariaDB 클러스터링: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Galera의 Certification 기반 복제는 내부적으로 어떻게 동작하며, 어떤 워크로드에서 문제가 발생하는가?

### 왜 이 질문이 중요한가

Galera를 도입하면 "모든 노드에서 쓰기 가능"이라는 장점에 집중하기 쉽지만, Certification 메커니즘의 한계를 모르면 프로덕션에서 예상치 못한 트랜잭션 롤백과 성능 저하를 겪게 된다. 어떤 워크로드가 Galera에 적합하고 어떤 것이 부적합한지 판단하려면 내부 동작을 깊이 이해해야 한다.

### 답변

**Certification 내부 동작:**

Galera의 Certification은 낙관적 동시성 제어(Optimistic Concurrency Control)를 분산 환경에 적용한 것이다. 각 노드는 로컬에서 트랜잭션을 자유롭게 실행하되, 커밋 시점에만 전체 클러스터와 조율한다.

1. **로컬 실행**: 트랜잭션이 노드 A에서 실행된다. 이 시점에는 다른 노드와 통신하지 않는다. 변경된 행의 Primary Key와 데이터를 Write Set으로 수집한다.

2. **브로드캐스트**: COMMIT 요청 시 Write Set이 Group Communication System(GCS)을 통해 모든 노드에 전송된다. GCS는 Total Order(전체 순서)를 보장하므로, 모든 노드가 동일한 순서로 Write Set을 수신한다.

3. **Certification 검사**: 각 노드는 수신한 Write Set의 Primary Key가 자신의 로컬 인증 인덱스(certification index)와 충돌하는지 검사한다. 인증 인덱스는 최근 커밋된 트랜잭션들의 PK를 보관한다.

4. **결정**: 모든 노드가 동일한 순서로 동일한 검사를 수행하므로, PASS/FAIL 결정이 모든 노드에서 동일하다. 분산 투표가 필요 없다는 점이 핵심이다.

**충돌 발생 시나리오:**

```
Node A: BEGIN; UPDATE users SET name='Alice' WHERE id=1; COMMIT;
Node B: BEGIN; UPDATE users SET name='Bob'   WHERE id=1; COMMIT;

GCS 도착 순서: Node A의 Write Set → Node B의 Write Set

모든 노드에서:
- Node A의 Write Set: id=1 검사 → 충돌 없음 → PASS
- Node B의 Write Set: id=1 검사 → Node A와 충돌 → FAIL

결과:
- Node A: 커밋 성공
- Node B: 트랜잭션 롤백 (deadlock error 반환)
```

**문제가 되는 워크로드:**

| 워크로드 | 문제 | 이유 |
|---------|------|------|
| 핫 로우 업데이트 | 높은 롤백률 | 같은 PK에 여러 노드가 동시 쓰기 |
| 대규모 트랜잭션 | Write Set 전송 지연 | 수천 행 변경 시 Write Set이 커짐 |
| 긴 트랜잭션 | Flow Control 유발 | 적용 큐가 쌓이면서 전체 노드 제한 |
| DDL (ALTER TABLE) | 전체 클러스터 잠금 | TOI(Total Order Isolation) 방식 |

**핫 로우 문제의 실전 예시:**

카운터 테이블(`UPDATE counters SET value = value + 1 WHERE id = 1`)을 여러 노드에서 동시에 실행하면 대부분의 트랜잭션이 Certification에서 실패한다. 이런 패턴은 **하나의 노드에서만 처리**하거나, 카운터를 노드별로 분리한 후 합산하는 방식으로 우회해야 한다.

### 실무 적용

Galera는 "모든 노드에서 아무 데이터나 쓸 수 있다"는 의미가 아니다. 최적의 패턴은 **각 노드가 서로 다른 데이터를 쓰는 것**이다. 멀티테넌트 애플리케이션에서 tenant_id 기반으로 노드를 분리하거나, 지역별로 노드를 할당하면 충돌을 최소화할 수 있다. 같은 행을 여러 노드에서 동시에 쓰는 워크로드라면 Galera보다 Single-Leader(Patroni) 구성이 더 적합하다.

---

## Q2. MaxScale의 라우팅 알고리즘은 어떻게 동작하며, readwritesplit의 세부 동작은?

### 왜 이 질문이 중요한가

MaxScale의 readwritesplit 라우터는 "SELECT는 Replica, 나머지는 Primary"라는 단순한 규칙 이상의 복잡한 동작을 한다. 트랜잭션 경계, 세션 변수, 임시 테이블 등 다양한 상황에서 라우팅 결정이 달라진다. 이를 이해하지 못하면 예상치 못한 곳에서 데이터 불일치나 오류가 발생할 수 있다.

### 답변

**readwritesplit의 라우팅 규칙:**

MaxScale은 SQL을 파싱하는 대신 **연결 상태를 추적**하여 라우팅을 결정한다. 핵심 규칙은 다음과 같다.

1. **트랜잭션 내부**: `BEGIN`~`COMMIT` 사이의 모든 쿼리(SELECT 포함)는 Primary로 전송된다. 트랜잭션 내에서 읽기 일관성을 보장하기 위한 것이다.

2. **트랜잭션 외부 SELECT**: 명시적 트랜잭션 밖의 SELECT는 Replica로 분산된다.

3. **쓰기 쿼리**: INSERT, UPDATE, DELETE, DDL은 항상 Primary로 전송된다.

4. **세션 변수**: `SET @var = 1` 같은 세션 변수 설정은 모든 백엔드에 전파되어야 한다. MaxScale은 이를 추적하여 세션 일관성을 유지한다.

5. **임시 테이블**: `CREATE TEMPORARY TABLE`이 감지되면 이후 해당 세션의 모든 쿼리가 같은 서버로 고정된다.

6. **LAST_INSERT_ID()**: 이 함수를 사용하는 SELECT는 Primary로 전송된다(가장 최근 INSERT가 Primary에서 실행되었으므로).

**transaction_replay 기능:**

MaxScale 2.3부터 도입된 `transaction_replay`는 Failover 시 진행 중인 트랜잭션을 자동으로 새 Primary에서 재실행하는 기능이다. Primary가 죽었을 때 클라이언트가 에러를 받는 대신, MaxScale이 트랜잭션 내의 모든 쿼리를 기록해두었다가 새 Primary에서 재실행한다.

```
[1] Client → MaxScale: BEGIN
[2] Client → MaxScale: INSERT INTO orders VALUES(...)
[3] Primary 장애 발생!
    MaxScale이 [1], [2]를 기록해둔 상태
[4] MaxScale → 새 Primary: BEGIN
[5] MaxScale → 새 Primary: INSERT INTO orders VALUES(...)
[6] Client → MaxScale: COMMIT
[7] MaxScale → 새 Primary: COMMIT → 성공
    Client는 장애를 인지하지 못함
```

제한 사항: `transaction_replay_max_size`(기본 1MB)를 초과하는 대규모 트랜잭션은 재실행되지 않는다.

**Galera 환경에서의 특수 동작:**

Galera의 galeramon은 각 노드의 `wsrep_local_state` 값을 확인하여 상태를 판별한다.

| wsrep_local_state | 의미 | MaxScale 동작 |
|-------------------|------|---------------|
| 4 (Synced) | 정상 | 읽기/쓰기 라우팅 가능 |
| 2 (Donor/Desynced) | SST 제공 중 | `available_when_donor=true`면 읽기 가능 |
| 1 (Joining) | 합류 중 | 라우팅 제외 |

### 실무 적용

readwritesplit을 사용할 때 가장 흔한 실수는 **트랜잭션 밖에서 읽기 직후 쓰기를 하는 패턴**이다. `SELECT ... FOR UPDATE` 같은 잠금 읽기는 반드시 트랜잭션 내에서 실행해야 Primary로 라우팅된다. `transaction_replay`는 프로덕션에서 Failover 영향을 크게 줄이는 기능이므로 반드시 활성화할 것을 권장한다.

---

## Q3. MariaDB와 PostgreSQL 중 HA 시나리오에서 어떤 것을 선택해야 하는가?

### 왜 이 질문이 중요한가

프로젝트 초기에 데이터베이스를 선택할 때 "HA를 어떻게 구성할 것인가"는 핵심 결정 요소이다. PostgreSQL과 MariaDB는 HA 철학이 근본적으로 다르고, 이 차이가 운영 복잡성, Failover 시간, 데이터 일관성에 직접적인 영향을 준다.

### 답변

**Failover 시간 비교:**

PostgreSQL(Patroni)의 Failover는 etcd 리더 키 TTL 만료(기본 30초) + 승격 시간으로, 총 **30~40초**가 소요된다. 이 시간 동안 쓰기가 불가능하다. TTL을 줄이면 Failover는 빨라지지만, 네트워크 지터로 인한 불필요한 Failover(false positive) 위험이 증가한다.

Galera Cluster의 Failover는 노드 탈퇴를 GCS가 감지하는 즉시 발생한다. 나머지 노드가 과반수를 유지하면 **수초 이내**에 자동으로 새 Primary View가 형성된다. 모든 노드가 쓰기 가능하므로, 단일 노드 장애 시 애플리케이션은 다른 노드로 즉시 요청을 전환할 수 있다.

**데이터 일관성 비교:**

| 시나리오 | PostgreSQL (Patroni, sync) | Galera |
|---------|---------------------------|--------|
| 정상 운영 | 강한 일관성 (동기 복제) | 가상 동기 (Certification) |
| 단일 노드 장애 | 커밋된 데이터 보존 (sync mode) | 커밋된 데이터 보존 |
| 네트워크 파티션 | 소수 측 쓰기 불가 (etcd 합의) | 소수 측 쓰기 불가 (Quorum) |
| 동시 쓰기 충돌 | 불가능 (Single-Leader) | 한쪽 트랜잭션 롤백 |

**운영 복잡성 비교:**

PostgreSQL + Patroni는 etcd 클러스터를 별도로 운영해야 한다. etcd 자체도 3~5노드 클러스터가 필요하므로, PostgreSQL HA를 위해 총 6~8개 프로세스를 관리해야 한다. 하지만 Single-Leader 모델이 단순하므로 디버깅이 상대적으로 쉽다.

Galera는 외부 의존성 없이 MariaDB 노드 자체가 클러스터를 구성한다. 운영할 프로세스가 적지만, Multi-Master 특유의 문제(Certification 실패, Flow Control, DDL 잠금)를 이해하고 대응해야 한다. 특히 전체 클러스터가 다운된 후 복구(Bootstrap)하는 과정이 까다롭다.

**결정 프레임워크:**

```
Q1: 모든 노드에서 쓰기가 필요한가?
├─ YES → Galera (MariaDB)
└─ NO → Q2

Q2: Failover 시간이 10초 미만이어야 하는가?
├─ YES → Galera (MariaDB) 또는 PG + Patroni(TTL 최소화)
└─ NO → Q3

Q3: 복잡한 SQL 기능(CTE, Window Function, JSONB, GIS)이 핵심인가?
├─ YES → PostgreSQL (Patroni)
└─ NO → Q4

Q4: MySQL 호환성이 필요한가?
├─ YES → MariaDB
└─ NO → PostgreSQL (생태계가 더 풍부)
```

### 실무 적용

대부분의 웹 애플리케이션은 읽기가 쓰기보다 훨씬 많고, 모든 노드에서 쓰기가 필요한 경우는 드물다. 이런 환경에서는 PostgreSQL + Patroni가 더 단순하고 안전한 선택이다. Multi-DC 배포에서 각 DC가 독립적으로 쓰기를 처리해야 하거나, 30초의 Failover 시간이 허용되지 않는 환경에서 Galera가 장점을 발휘한다.

---

## Q4. SST와 IST 메커니즘은 어떻게 동작하며, 클러스터 복구 시 어떤 전략을 써야 하는가?

### 왜 이 질문이 중요한가

Galera 운영에서 가장 스트레스받는 순간은 노드 복구와 전체 클러스터 재시작이다. SST는 대규모 데이터 전송이 필요해 시간이 오래 걸리고, Donor 노드에 부하를 준다. IST는 빠르지만 GCache가 부족하면 동작하지 않는다. 복구 전략을 사전에 수립하지 않으면 장애가 장기화된다.

### 답변

**IST(Incremental State Transfer)의 동작:**

IST는 Galera의 GCache(Group Cache)에 저장된 Write Set을 활용한다. 각 노드는 최근 Write Set을 링 버퍼 형태의 GCache에 보관한다. 노드가 일시적으로 분리되었다가 재합류할 때, 누락된 Write Set이 GCache에 남아있으면 IST로 빠르게 동기화된다.

```
Node B가 5분간 분리 후 재합류:

GCache 상태 (Node A):
[WS #1000] [WS #1001] ... [WS #1500]

Node B의 마지막 적용: WS #1200

#1200 ~ #1500이 GCache에 존재
→ IST로 300개 Write Set만 전송 (수초 소요)
```

GCache 크기(`gcache.size`)가 작거나 분리 기간이 길면 누락된 Write Set이 이미 GCache에서 밀려나 IST를 사용할 수 없다. 이때 SST로 전환된다.

**SST(State Snapshot Transfer)의 동작:**

SST는 Donor 노드의 전체 데이터를 Joiner 노드로 전송한다.

| SST 방식 | Donor 영향 | 속도 | 권장도 |
|---------|-----------|------|--------|
| mariabackup | 읽기/쓰기 가능 (non-blocking) | 빠름 | 권장 |
| rsync | 읽기 전용 (FTWRL 잠금) | 빠름 | 비추천 |
| mysqldump | 읽기/쓰기 가능 | 느림 | 특수 경우만 |

mariabackup을 사용하면 Donor가 정상 서비스를 계속하면서 백업을 생성한다. 하지만 데이터가 수백 GB인 경우 SST에 수십 분~수 시간이 걸릴 수 있다.

**전체 클러스터 다운 후 복구(Bootstrap):**

가장 위험한 시나리오이다. 모든 노드가 동시에 다운된 경우, 가장 최신 데이터를 가진 노드를 찾아 그 노드로 클러스터를 부트스트랩해야 한다.

```bash
# 1. 각 노드에서 마지막 커밋 위치 확인
cat /var/lib/mysql/grastate.dat
# seqno 값이 가장 큰 노드를 부트스트랩 노드로 선택

# 2. 부트스트랩 노드에서 클러스터 시작
galera_new_cluster
# 또는
mysqld --wsrep-new-cluster

# 3. 나머지 노드를 순차적으로 시작
systemctl start mariadb  # 자동으로 IST/SST 진행
```

`seqno: -1`인 노드는 비정상 종료된 것이므로 `--wsrep-recover`로 복구 후 seqno를 확인한다.

**GCache 크기 설계:**

```
필요 GCache 크기 = 쓰기 처리량(MB/초) x 최대 허용 분리 시간(초)

예: 초당 2MB 쓰기, 최대 30분 분리 허용
    = 2 x 1800 = 3600MB ≈ 4GB
```

### 실무 적용

프로덕션에서는 GCache를 충분히 크게 설정(최소 수 GB)하여 IST 성공률을 높이고, SST 방식은 반드시 mariabackup을 사용한다. 전체 클러스터 다운은 반드시 피해야 하므로, **롤링 재시작**(한 노드씩 순차 재시작)을 운영 절차로 확립해야 한다. 부트스트랩 절차는 문서화하여 팀 전원이 숙지하고, 정기적으로 모의 훈련을 실시하는 것이 좋다.

---

## Q5. Galera의 Flow Control은 어떻게 동작하며, 성능 문제를 어떻게 진단하는가?

### 왜 이 질문이 중요한가

Flow Control은 Galera 성능 문제의 가장 흔한 원인이다. "클러스터 속도가 갑자기 느려졌다"는 증상의 대부분이 Flow Control과 관련된다. Flow Control의 동작 원리와 모니터링 방법을 모르면, 느린 노드 하나가 전체 클러스터를 끌어내리는 상황을 방치하게 된다.

### 답변

**Flow Control 동작 원리:**

각 Galera 노드는 수신한 Write Set을 적용(apply)하는 큐를 가지고 있다. 이 큐의 크기가 `gcs.fc_limit`(기본 16개 트랜잭션)을 초과하면, 해당 노드가 Flow Control 메시지를 발송하여 전체 클러스터의 복제를 일시 중지시킨다. 큐가 `gcs.fc_factor`(기본 0.5) x `gcs.fc_limit` 이하로 줄어들면 복제가 재개된다.

```
wsrep_local_recv_queue (적용 대기 큐):

정상:  [TX] [TX] → 즉시 적용
경고:  [TX] [TX] [TX] ... [TX] (16개) → fc_limit 도달
조치:  Flow Control 발동 → 전체 클러스터 복제 중지
복구:  큐가 8개(16 x 0.5) 이하로 줄면 재개
```

**Flow Control이 발동하는 원인:**

1. **느린 디스크**: 한 노드의 I/O가 느리면 Write Set 적용이 지연된다
2. **대규모 트랜잭션**: 수천 행을 수정하는 트랜잭션은 적용 시간이 길다
3. **DDL**: `ALTER TABLE`은 TOI 방식으로 전체 클러스터를 잠그고 순차 실행한다
4. **느린 네트워크**: 노드 간 지연이 높으면 Write Set 수신이 지연된다
5. **불균형한 하드웨어**: CPU/메모리가 작은 노드가 병목이 된다

**모니터링 쿼리:**

```sql
-- Flow Control 상태 확인
SHOW STATUS LIKE 'wsrep_flow_control_%';

-- 핵심 지표
-- wsrep_flow_control_paused: Flow Control로 중지된 시간 비율 (0.0 ~ 1.0)
-- wsrep_flow_control_sent:   이 노드가 보낸 FC 메시지 수
-- wsrep_flow_control_recv:   이 노드가 받은 FC 메시지 수

-- 적용 큐 크기
SHOW STATUS LIKE 'wsrep_local_recv_queue%';
-- wsrep_local_recv_queue:     현재 큐 크기
-- wsrep_local_recv_queue_avg: 평균 큐 크기

-- 전체 클러스터 상태
SHOW STATUS LIKE 'wsrep_%';
```

**정상 상태 기준:**

| 지표 | 정상 | 경고 | 위험 |
|------|------|------|------|
| `wsrep_flow_control_paused` | < 0.01 | 0.01 ~ 0.1 | > 0.1 |
| `wsrep_local_recv_queue_avg` | < 1 | 1 ~ 5 | > 5 |
| `wsrep_flow_control_sent` | 0 | 간헐적 | 지속 증가 |
| `wsrep_cert_deps_distance` | > 10 | 5 ~ 10 | < 5 |

`wsrep_cert_deps_distance`는 병렬 적용 가능한 트랜잭션 수를 나타낸다. 이 값이 낮으면 트랜잭션 간 의존성이 높아 `wsrep_slave_threads`를 늘려도 병렬화 효과가 없다는 뜻이다.

**Flow Control 완화 전략:**

1. **wsrep_slave_threads 증가**: 병렬 적용 스레드를 늘린다. `wsrep_cert_deps_distance` 이하로 설정해야 효과가 있다.
2. **gcs.fc_limit 증가**: 큐 임계치를 올린다. 하지만 메모리 사용량이 증가하고, 노드 간 데이터 차이가 커질 수 있다.
3. **대규모 트랜잭션 분할**: 수천 행 UPDATE를 배치(1000행씩)로 나눈다.
4. **DDL 전략**: `ALTER TABLE`은 트래픽이 적은 시간에 실행하거나, pt-online-schema-change 같은 도구를 사용한다.
5. **하드웨어 균일화**: 가장 느린 노드가 전체 성능을 결정하므로, 클러스터 내 노드 스펙을 동일하게 맞춘다.

### 실무 적용

Prometheus + Grafana로 `wsrep_flow_control_paused`, `wsrep_local_recv_queue_avg`를 실시간 모니터링하고, `wsrep_flow_control_paused > 0.05`일 때 알림을 설정하는 것이 권장된다. Flow Control이 자주 발동하면 원인 노드를 식별(`wsrep_flow_control_sent`가 높은 노드)하고, 해당 노드의 디스크 I/O, 네트워크 지연, 쿼리 패턴을 점검해야 한다.
