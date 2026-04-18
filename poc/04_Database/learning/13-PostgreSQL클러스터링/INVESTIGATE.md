# Ch.13 - PostgreSQL 클러스터링: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Patroni Failover는 구체적으로 어떤 단계를 거치며, 데이터 손실 가능성은 어떻게 제어하는가?

### 왜 이 질문이 중요한가

Patroni를 도입하면 자동 Failover가 동작하지만, "자동"이라는 단어 뒤에 숨겨진 복잡성을 이해하지 못하면 프로덕션 장애 시 대응이 불가능해진다. Failover 시간, 데이터 손실 범위, Split Brain 방지 메커니즘을 구체적으로 알아야 SLA를 설계할 수 있다.

### 답변

**Failover 상세 단계:**

1. **장애 감지**: Patroni는 각 노드에서 `loop_wait` 간격(기본 10초)으로 PostgreSQL 상태를 확인한다. 동시에 etcd에 리더 키를 `ttl` 간격(기본 30초)으로 갱신한다. Primary의 Patroni 프로세스가 죽거나 네트워크가 단절되면 리더 키가 만료된다.

2. **리더 경쟁**: 리더 키가 만료되면 모든 Standby의 Patroni가 etcd에 CAS(Compare-and-Set)로 새 리더 키 생성을 시도한다. etcd의 Raft 합의 덕분에 하나만 성공한다.

3. **승격 자격 검증**: 리더 키를 획득한 Standby가 승격 전에 자신의 WAL 위치(LSN)를 확인한다. `maximum_lag_on_failover` 설정(기본 1MB)보다 뒤처져 있으면 승격을 포기한다. 이 설정이 데이터 손실의 상한선을 제어한다.

4. **pg_ctl promote**: 자격 검증을 통과하면 PostgreSQL을 Primary로 승격한다. 이 시점에서 새 타임라인(timeline)이 시작된다.

5. **나머지 노드 재설정**: 다른 Standby 노드들은 `pg_rewind`로 새 Primary의 타임라인에 맞춰 자신의 데이터를 되돌린다. pg_rewind가 실패하면 `pg_basebackup`으로 전체 데이터를 다시 받는다.

**데이터 손실 제어:**

| 설정 | 역할 | 트레이드오프 |
|------|------|-------------|
| `synchronous_mode: true` | 동기 복제 강제, 최소 1개 Standby 확인 후 커밋 | Standby 전부 죽으면 쓰기 차단 |
| `synchronous_mode_strict: true` | 동기 Standby 없으면 쓰기 거부 | 가용성 저하 가능 |
| `maximum_lag_on_failover` | 이 이상 뒤처진 Standby는 승격 불가 | 너무 작으면 승격 가능 노드 없음 |

비동기 복제에서는 Primary가 죽기 직전 커밋된 트랜잭션이 Standby에 도달하지 못했을 수 있다. `synchronous_mode: true`로 설정하면 Patroni가 자동으로 가장 빠른 Standby 하나를 동기 대상으로 지정하여 데이터 손실을 방지한다.

**Split Brain 방지:**

Patroni의 핵심 안전장치는 etcd의 리더 키이다. Primary는 주기적으로 리더 키를 갱신해야 하며, 갱신에 실패하면 스스로를 Standby로 강등(demote)한다. 이 메커니즘 덕분에 네트워크 파티션이 발생해도 두 개의 Primary가 동시에 존재할 수 없다.

### 실무 적용

프로덕션에서는 `synchronous_mode: true`와 `maximum_lag_on_failover: 1048576` (1MB)을 기본으로 설정하고, Failover 후 반드시 `patronictl list`로 클러스터 상태를 확인하는 운영 프로세스가 필요하다. Failover 시간은 일반적으로 `ttl + loop_wait` = 약 30~40초이다.

---

## Q2. Citus 분산 테이블과 PostgreSQL 네이티브 파티셔닝의 차이는 무엇인가?

### 왜 이 질문이 중요한가

PostgreSQL 10부터 네이티브 파티셔닝(Declarative Partitioning)이 지원된다. Citus도 테이블을 나누는 기술이다. 둘 다 "큰 테이블을 작은 조각으로 나눈다"는 점에서 비슷해 보이지만, 해결하는 문제가 근본적으로 다르다. 잘못 선택하면 불필요한 복잡성을 도입하거나 확장 한계에 부딪힌다.

### 답변

**네이티브 파티셔닝**: 단일 노드 내에서 테이블을 물리적으로 분할한다. 파티션 프루닝(pruning)으로 쿼리 시 불필요한 파티션을 건너뛰어 성능을 향상시킨다. 하지만 모든 파티션이 같은 노드의 디스크에 존재하므로, 단일 노드의 스토리지와 CPU 한계를 넘을 수 없다.

```sql
-- 네이티브 파티셔닝: 단일 노드
CREATE TABLE events (
    id bigserial,
    created_at timestamptz,
    payload jsonb
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_01 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

**Citus 분산 테이블**: 여러 물리 노드에 걸쳐 테이블을 분산한다. 해시 샤딩으로 데이터를 Worker 노드들에 분배하고, Coordinator가 쿼리를 병렬로 실행한다. 단일 노드의 한계를 넘어 수평 확장이 가능하다.

```sql
-- Citus: 여러 노드에 분산
CREATE TABLE events (
    tenant_id int,
    id bigserial,
    payload jsonb
);
SELECT create_distributed_table('events', 'tenant_id');
```

| 비교 항목 | 네이티브 파티셔닝 | Citus 분산 테이블 |
|----------|-----------------|-----------------|
| 데이터 위치 | 단일 노드 | 여러 노드 |
| 확장 방식 | 수직 (Scale-up) | 수평 (Scale-out) |
| 파티션 키 | Range, List, Hash | Hash (분산 컬럼) |
| 크로스 파티션 조인 | 효율적 (같은 노드) | 네트워크 비용 발생 |
| DDL 관리 | 수동 (파티션 생성/삭제) | 자동 (Citus가 샤드 관리) |
| 적합 규모 | TB 단위까지 | TB~PB 단위 |
| 복잡성 | 낮음 | 높음 (분산 트랜잭션, 네트워크) |

**둘을 함께 사용하는 패턴도 존재한다.** Citus 분산 테이블의 각 샤드를 네이티브 파티셔닝으로 시간 기반 분할하면, 오래된 파티션을 효율적으로 삭제(DROP PARTITION)할 수 있다.

### 실무 적용

데이터가 수백 GB 이하이고 단일 노드로 충분하다면 네이티브 파티셔닝으로 시작한다. 단일 노드의 CPU/스토리지 한계에 도달했거나 멀티테넌트 SaaS에서 테넌트별 격리가 필요하면 Citus를 검토한다. "미래에 필요할 수도 있으니" Citus를 미리 도입하는 것은 과잉 설계이다.

---

## Q3. Streaming Replication과 Logical Replication, 어떤 상황에서 어떤 것을 선택해야 하는가?

### 왜 이 질문이 중요한가

두 복제 방식은 이름이 비슷하지만 사용 목적이 다르다. HA를 위해 Logical Replication을 선택하거나, 무중단 마이그레이션을 위해 Streaming Replication을 선택하면 목표를 달성할 수 없다. 각 방식의 강점과 제약을 정확히 이해해야 올바른 아키텍처를 설계한다.

### 답변

**Streaming Replication을 선택해야 하는 경우:**

1. **고가용성(HA)**: Primary 장애 시 Standby를 즉시 승격해야 할 때. Streaming Replication은 전체 클러스터의 물리적 복사본을 유지하므로, Standby를 Primary로 승격하면 모든 데이터(테이블, 인덱스, 시퀀스, 함수 등)가 그대로 사용 가능하다.

2. **읽기 분산**: 읽기 쿼리를 여러 Standby에 분산할 때. Hot Standby 모드를 활성화하면 Standby에서 SELECT 쿼리를 실행할 수 있다.

3. **재해 복구(DR)**: 다른 데이터센터에 전체 데이터 복사본을 유지할 때.

**Logical Replication을 선택해야 하는 경우:**

1. **무중단 메이저 버전 업그레이드**: PostgreSQL 14에서 16으로 업그레이드할 때, Logical Replication으로 데이터를 새 버전에 실시간 동기화한 후 컷오버한다. Streaming Replication은 동일 메이저 버전에서만 동작한다.

2. **선택적 테이블 복제**: 전체가 아닌 특정 테이블만 다른 데이터베이스로 복제할 때. 분석 DB에 주문 테이블만 실시간 전송하는 경우가 대표적이다.

3. **CDC(Change Data Capture)**: 데이터 변경 이벤트를 다른 시스템(Kafka, Elasticsearch)에 전달할 때. Debezium이 PostgreSQL의 Logical Decoding을 사용한다.

4. **양방향 복제 (주의 필요)**: Subscriber에서도 쓰기가 가능하므로 Multi-Leader 패턴을 구현할 수 있다. 그러나 충돌 해결 메커니즘이 내장되어 있지 않아 애플리케이션에서 처리해야 한다.

**제약 사항 비교:**

| 제약 | Streaming | Logical |
|------|-----------|---------|
| DDL 복제 | 자동 | 불가 (수동 적용) |
| SEQUENCE 복제 | 자동 | 불가 |
| TRUNCATE 복제 | 자동 | PG 11+ 지원 |
| Large Object 복제 | 자동 | 불가 |
| 초기 데이터 동기화 | pg_basebackup (전체) | Subscription 생성 시 자동 (테이블 단위) |

### 실무 적용

가장 일반적인 패턴은 **Streaming Replication으로 HA를 구성하고, Logical Replication으로 분석/마이그레이션을 처리**하는 조합이다. 하나의 Primary에서 두 방식을 동시에 사용할 수 있다. Patroni + Streaming Replication으로 자동 Failover를 보장하면서, 별도의 Logical Subscription으로 분석 DB에 특정 테이블을 실시간 전송하는 구성이 대표적이다.

---

## Q4. CloudNativePG와 Zalando Postgres Operator 중 어떤 것을 선택해야 하는가?

### 왜 이 질문이 중요한가

Kubernetes에서 PostgreSQL을 운영할 때 두 Operator가 가장 많이 사용된다. 둘 다 HA 클러스터를 선언적으로 관리하지만, 아키텍처 철학이 다르다. 잘못된 선택은 운영 부담 증가나 기능 부족으로 이어질 수 있으므로, 팀의 상황에 맞는 선택이 중요하다.

### 답변

**아키텍처 철학의 차이:**

CloudNativePG는 "Kubernetes-native" 접근법을 취한다. Patroni나 etcd 없이 Kubernetes API 자체를 통해 리더 선출과 페일오버를 관리한다. PostgreSQL 인스턴스가 Kubernetes의 일급 시민(first-class citizen)으로 동작하며, PVC(PersistentVolumeClaim)와 Pod의 생명주기를 Operator가 직접 관리한다.

Zalando Operator는 "Patroni 위에 Kubernetes를 얹는" 접근법이다. 검증된 Patroni의 HA 메커니즘을 그대로 활용하고, Kubernetes는 배포/스케일링의 편의를 위해 사용한다. Patroni가 etcd 대신 Kubernetes API의 Endpoints 리소스를 DCS(Distributed Configuration Store)로 사용한다.

**기능 비교:**

| 기능 | CloudNativePG | Zalando Operator |
|------|---------------|------------------|
| Failover 메커니즘 | 자체 구현 | Patroni |
| 외부 의존성 | 없음 | Patroni (내장) |
| PgBouncer | 내장 사이드카 | 별도 배포 필요 |
| 백업 도구 | Barman (S3/GCS/Azure) | WAL-G (S3/GCS/Azure) |
| PITR | 지원 | 지원 |
| 모니터링 | 내장 메트릭 엔드포인트 | Prometheus 사이드카 |
| 커스텀 TLS | 자동 인증서 관리 | cert-manager 연동 |
| CNCF 인정 | Sandbox 프로젝트 | 비공식 |
| 프로덕션 실적 | EDB 고객사 | Zalando 내부 (수천 클러스터) |

**선택 가이드:**

- Kubernetes에 익숙하고, 외부 의존성을 최소화하고 싶다면 → **CloudNativePG**
- Patroni에 이미 익숙하거나, 대규모 프로덕션 실적이 중요하다면 → **Zalando Operator**
- PgBouncer 통합이 핵심 요구사항이면 → **CloudNativePG** (내장 지원)
- 복잡한 팀 기반 멀티테넌시가 필요하면 → **Zalando Operator** (teamId 기반 관리)

### 실무 적용

신규 프로젝트에서 Kubernetes 경험이 풍부한 팀이라면 CloudNativePG가 더 깔끔한 선택이다. CNCF Sandbox에 편입되어 커뮤니티 성장이 빠르고, 외부 컴포넌트 없이 순수 Kubernetes 리소스만으로 운영할 수 있다. 반면 이미 Patroni 기반 운영 경험이 있거나, Docker Compose → Kubernetes 마이그레이션 경로가 필요하다면 Zalando Operator가 전환 비용이 적다.

---

## Q5. PostgreSQL 클러스터에서 읽기/쓰기 분리(Read-Write Splitting)를 구현하는 가장 좋은 방법은?

### 왜 이 질문이 중요한가

읽기 트래픽이 쓰기의 10배 이상인 서비스에서는 읽기를 Standby로 분산하는 것이 성능 확장의 핵심이다. 하지만 구현 방법에 따라 복잡성, 복제 지연 처리, 장애 대응이 크게 달라진다. 애플리케이션 레벨, 미들웨어 레벨, 인프라 레벨 각각의 장단점을 비교해야 올바른 결정을 내릴 수 있다.

### 답변

**방법 1: 애플리케이션 레벨 분리**

애플리케이션 코드에서 읽기/쓰기 커넥션을 명시적으로 구분한다.

```python
# Python/SQLAlchemy 예시
write_engine = create_engine("postgresql://primary:5432/mydb")
read_engine = create_engine("postgresql://standby:5432/mydb")

# 쓰기
with write_engine.begin() as conn:
    conn.execute(insert_stmt)

# 읽기
with read_engine.connect() as conn:
    result = conn.execute(select_stmt)
```

장점: 가장 세밀한 제어, 미들웨어 의존성 없음. 단점: 코드 복잡성 증가, 모든 쿼리에 대해 개발자가 판단해야 함.

**방법 2: pgpool-II**

SQL 파서가 쿼리 유형을 자동 판별해 라우팅한다. SELECT는 Standby로, INSERT/UPDATE/DELETE는 Primary로 보낸다.

장점: 애플리케이션 코드 변경 불필요. 단점: SQL 파싱 오버헤드, 복잡한 쿼리(CTE, 함수 내 쓰기)에서 오판 가능, 단일 장애점이 될 수 있음.

**방법 3: HAProxy + Patroni REST API**

HAProxy가 두 개의 포트를 열어 Primary와 Replica를 분리하고, Patroni의 `/primary`와 `/replica` 엔드포인트로 헬스체크한다.

장점: 단순하고 안정적, Patroni와 자연스럽게 통합. 단점: 애플리케이션이 두 개의 커넥션 문자열을 관리해야 함.

**방법 4: Kubernetes Service 분리**

CloudNativePG나 Zalando Operator는 자동으로 `<cluster>-rw`와 `<cluster>-ro` Service를 생성한다. 애플리케이션은 DNS 이름만 다르게 사용하면 된다.

```
my-cluster-rw.default.svc → Primary Pod
my-cluster-ro.default.svc → Replica Pods (라운드로빈)
```

**복제 지연 처리:**

어떤 방법을 선택하든 복제 지연 문제는 남는다. 사용자가 데이터를 수정한 직후 읽기 요청이 Standby로 가면 이전 데이터가 보일 수 있다. 실전 해결 패턴은 두 가지이다.

1. **쓰기 직후 일정 시간(예: 5초) 동안은 Primary에서 읽기**: 세션에 마지막 쓰기 시각을 저장하고, 일정 시간이 지나야 Standby로 라우팅한다.
2. **동기 복제 사용**: `synchronous_commit = remote_apply`로 설정하면 Standby에서 읽기 가능 상태가 보장된 후 커밋이 완료된다. 지연은 증가하지만 일관성이 보장된다.

### 실무 적용

가장 널리 사용되는 조합은 **HAProxy + Patroni**(Docker/VM 환경) 또는 **Operator 자동 Service 분리**(Kubernetes 환경)이다. 애플리케이션에서는 `DATABASE_URL_WRITE`와 `DATABASE_URL_READ` 환경변수로 두 엔드포인트를 구분하고, ORM 설정에서 읽기/쓰기 커넥션 풀을 분리하는 것이 표준 패턴이다.
