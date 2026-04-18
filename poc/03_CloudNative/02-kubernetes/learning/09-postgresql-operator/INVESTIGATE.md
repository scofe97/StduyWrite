# Ch09. CloudNativePG 점검 질문

## Q1. CloudNativePG vs Zalando Postgres Operator 선택 기준

**질문:** 새 프로젝트를 시작할 때 CloudNativePG와 Zalando Postgres Operator 중 무엇을 선택해야 하며, 각각의 강점과 약점은 무엇인가?

**핵심 포인트:**

- **CloudNativePG의 강점**: 설치가 단순하다(kubectl apply 한 번). 외부 의존성이 없다(Patroni, etcd 불필요). CNCF Sandbox 프로젝트라서 벤더 중립적이고, 커뮤니티가 빠르게 성장하고 있다. Barman 통합으로 백업과 PITR이 간단하다. 최신 PostgreSQL 버전을 빠르게 지원한다(15, 16 등).

- **Zalando의 강점**: 수년간 프로덕션에서 검증되었다. Zalando가 내부적으로 수백 개 클러스터를 운영하면서 다듬었다. Patroni 기반이라서 복잡한 페일오버 시나리오(네트워크 파티션, 스플릿 브레인)에 강하다. Postgres Operator UI가 제공되어 웹에서 클러스터를 관리할 수 있다. 대규모 멀티 테넌트 환경에서의 사례가 많다.

- **CNPG의 약점**: 비교적 신생 프로젝트다(2021년 시작). 대규모 프로덕션 사례가 Zalando보다 적다. Patroni만큼 복잡한 HA 시나리오를 다루지 못할 수 있다(하지만 대부분의 경우 충분하다).

- **Zalando의 약점**: 아키텍처가 복잡하다. Patroni를 이해해야 하고, etcd/Consul 같은 분산 키-값 저장소가 필요하다(K8s 자체가 etcd를 쓰지만, Patroni는 별도로 접근). 설정이 많아서 학습 곡선이 가파르다. CNCF 프로젝트가 아니라서 Zalando의 우선순위에 의존한다.

- **선택 기준**: 새 프로젝트이고 간결함을 원한다면 CNPG. 이미 Patroni를 사용 중이거나, 대규모 검증된 솔루션이 필요하면 Zalando. 엔터프라이즈 기능(감사, 암호화)이 필요하면 CrunchyData PGO.

- **마이그레이션 가능성**: 두 Operator 모두 표준 PostgreSQL을 사용하므로, 나중에 다른 Operator로 마이그레이션하는 것도 가능하다. pg_dump/pg_restore로 데이터를 옮기면 된다. 하지만 HA 설정, 백업 정책 등은 다시 구성해야 한다.

**심화 질문:**

- Patroni의 DCS(Distributed Configuration Store)가 K8s ConfigMap/Endpoints API를 사용할 수 있는데, 왜 Zalando Operator는 여전히 etcd를 권장하는가? (힌트: 성능과 안정성)
- CNPG가 CNCF에 들어간 것이 기술적으로 어떤 의미를 갖는가? (힌트: 중립성, 장기 유지보수 보장)

---

## Q2. Streaming Replication과 Logical Replication 차이

**질문:** PostgreSQL의 Streaming Replication(CNPG가 사용)과 Logical Replication은 어떻게 다르며, 각각 언제 사용해야 하는가?

**핵심 포인트:**

- **Streaming Replication (물리적 복제)**: WAL(Write-Ahead Log) 파일을 바이트 단위로 Primary에서 Replica로 전송한다. Replica는 Primary의 완전한 복사본이다. 모든 데이터베이스, 모든 테이블이 복제된다. 트랜잭션 단위가 아니라 블록 단위로 복제되므로 빠르다. 하지만 PostgreSQL 버전이 다르면 호환되지 않는다(메이저 버전 업그레이드 시 문제).

- **Logical Replication (논리적 복제)**: 트랜잭션의 논리적 변경(INSERT, UPDATE, DELETE)을 전송한다. 특정 테이블, 특정 데이터베이스만 선택적으로 복제할 수 있다. 서로 다른 PostgreSQL 버전 간에도 가능하다(10 → 15). 양방향 복제, 부분 복제, 데이터 변환 등이 가능하다. 하지만 느리고, DDL(테이블 스키마 변경)은 자동 복제되지 않는다.

- **CNPG가 Streaming을 사용하는 이유**: HA(High Availability)에는 Streaming이 적합하다. Replica가 Primary의 완전한 복사본이므로, 페일오버 시 즉시 Primary 역할을 할 수 있다. Logical Replication은 부분 복제이므로 페일오버에 사용할 수 없다.

- **Logical Replication의 사용 사례**: 서로 다른 버전 간 마이그레이션(10 → 16 업그레이드 중 Zero Downtime), 멀티 클라우드 복제(AWS RDS → GCP CloudSQL), 특정 테이블만 분석 환경으로 복제(OLTP → OLAP), 데이터 필터링(민감한 컬럼 제외).

- **동기 vs 비동기**: Streaming Replication은 동기와 비동기 모두 가능하다. 동기 모드에서는 Primary가 Replica의 확인을 기다려야 커밋된다(`synchronous_standby_names` 설정). Logical Replication은 기본적으로 비동기다.

**심화 질문:**

- Streaming Replication에서 Replica는 읽기 전용인데, Logical Replication에서는 Subscriber(대상)에 쓰기가 가능한가? (힌트: 가능하지만 충돌 해결 필요)
- WAL 파일이 커지면 Streaming Replication 성능이 떨어지는가? 어떻게 최적화하는가? (힌트: wal_compression, wal_level 설정)

---

## Q3. CNPG의 자동 페일오버 메커니즘 (리더 선출 과정)

**질문:** Primary Pod가 죽으면 CNPG Operator는 어떤 기준으로 새 Primary를 선출하며, 이 과정에서 데이터 손실을 방지하는 메커니즘은 무엇인가?

**핵심 포인트:**

- **Liveness Probe로 장애 감지**: Operator는 각 Pod의 Liveness Probe를 주기적으로 체크한다. Primary Pod가 응답하지 않거나, 프로세스가 죽으면 Operator는 "장애"로 판단한다. 일반적으로 3~5회 연속 실패 후 장애로 확정한다.

- **LSN(Log Sequence Number) 기반 선출**: PostgreSQL은 WAL에 LSN을 부여한다. LSN은 트랜잭션의 순서를 나타낸다. Operator는 모든 Replica의 LSN을 확인하고, 가장 앞선(가장 최신 데이터를 가진) Replica를 새 Primary로 선출한다. 이렇게 하면 데이터 손실을 최소화할 수 있다.

- **pg_ctl promote 실행**: 선택된 Replica에서 `pg_ctl promote` 명령을 실행한다. 이 명령은 Replica를 Recovery 모드에서 빠져나와 Normal 모드(쓰기 가능)로 전환한다. 이 과정은 1~5초 정도 걸린다.

- **다른 Replica 재설정**: 새 Primary가 선출되면, 나머지 Replica들은 이 새 Primary를 따라가도록 재설정된다. `primary_conninfo`를 업데이트하고, Replication Slot을 재생성한다.

- **Service 엔드포인트 업데이트**: Operator는 `-rw` Service의 Selector를 업데이트해서 새 Primary로 트래픽을 보낸다. K8s Service는 즉시 엔드포인트를 갱신한다(보통 1~2초).

- **타임라인(Timeline) 개념**: PostgreSQL은 페일오버마다 새로운 Timeline을 시작한다. Timeline은 "이 Primary의 역사"를 나타낸다. 이전 Primary가 복구되어 돌아오면, 자신의 Timeline이 구버전임을 알고 새 Primary의 Timeline을 따라간다. 이렇게 스플릿 브레인을 방지한다.

**심화 질문:**

- 만약 모든 Replica의 LSN이 동일하면 어떤 기준으로 선출하는가? (힌트: Pod 이름 순서, 네트워크 레이턴시 등 추가 기준)
- 동기 복제(`synchronous_standby_names`)를 사용하면 데이터 손실이 완전히 방지되는가? 트레이드오프는 무엇인가? (힌트: 레이턴시 증가, Replica 장애 시 쓰기 중단)

---

## Q4. PostgreSQL 설정을 CR로 관리하는 방법 (postgresql.parameters)

**질문:** Cluster CR의 `postgresql.parameters` 필드로 postgresql.conf를 관리할 때, 어떤 설정을 우선 조정해야 하며, 설정 변경 시 PostgreSQL 재시작이 필요한 경우는 어떻게 처리되는가?

**핵심 포인트:**

- **우선 조정해야 할 설정**: `shared_buffers`(메모리의 25% 권장), `effective_cache_size`(메모리의 50~75%), `work_mem`(정렬/조인 작업 메모리), `maintenance_work_mem`(인덱스 생성 등), `max_connections`(동시 연결 수 제한), `log_min_duration_statement`(느린 쿼리 로깅).

- **설정 우선순위**: postgresql.conf는 여러 방법으로 설정할 수 있다. 우선순위는 `ALTER SYSTEM` > `postgresql.conf` > 기본값이다. CNPG의 `postgresql.parameters`는 postgresql.conf에 반영된다. 사용자가 Pod에 접속해서 `ALTER SYSTEM`을 실행하면 그게 우선된다. 하지만 이는 권장하지 않는다. 모든 설정을 CR로 관리해야 GitOps가 가능하다.

- **재시작 필요 여부**: PostgreSQL 설정은 세 가지로 분류된다.
  - **SIGHUP**: 설정 파일을 리로드하면 즉시 적용된다. `pg_ctl reload` 또는 `SELECT pg_reload_conf()`. 대부분의 설정이 이 범주다.
  - **재시작 필요**: `shared_buffers`, `max_connections` 같은 메모리 관련 설정은 PostgreSQL을 재시작해야 적용된다.
  - **즉시 적용**: 일부 설정은 세션마다 다르게 적용할 수 있다(예: `work_mem`은 `SET work_mem='16MB'`로 세션마다 변경 가능).

- **CNPG의 Rolling Update**: CR에서 설정을 변경하면 Operator는 Pod를 하나씩 재시작한다(Rolling Update). Replica부터 먼저 재시작하고, 마지막에 Primary를 재시작한다. Primary 재시작 시 Replica 중 하나를 임시로 Primary로 승격시키고, 기존 Primary를 재시작한 후 다시 Primary로 승격시킨다. 이 과정은 무중단으로 진행되지만, 10~30초의 쓰기 중단이 발생할 수 있다.

- **주의할 설정**: `max_connections`를 너무 크게 설정하면 메모리 부족이 발생할 수 있다. 각 연결은 약 10MB의 메모리를 소비한다. 200 연결 = 2GB 메모리. 연결 풀링(PgBouncer)을 사용하면 연결 수를 줄일 수 있다.

**심화 질문:**

- `shared_buffers`를 메모리의 50%로 설정하면 안 되는 이유는 무엇인가? (힌트: OS 페이지 캐시와 이중 캐싱 문제)
- `postgresql.parameters`에서 설정한 값이 적용되지 않는 경우는 언제인가? (힌트: ConfigMap 우선순위, 잘못된 값)

---

## Q5. WAL 아카이빙과 PITR(Point-in-Time Recovery) 개념

**질문:** WAL 아카이빙이 왜 중요하며, PITR은 어떻게 동작하는가? Base Backup과 WAL의 관계는 무엇인가?

**핵심 포인트:**

- **WAL의 역할**: WAL(Write-Ahead Log)은 트랜잭션의 모든 변경 사항을 기록한다. 데이터 파일보다 WAL이 먼저 쓰인다. 시스템이 크래시되면 WAL을 재생해서 복구한다. WAL이 없으면 데이터 손실이 발생한다.

- **WAL 아카이빙**: PostgreSQL은 일정 크기(기본 16MB)마다 WAL 파일을 생성한다. 이 파일들을 외부 스토리지(S3, Azure Blob 등)로 복사하는 것이 WAL 아카이빙이다. Primary가 완전히 망가져도 WAL만 있으면 복구할 수 있다.

- **Base Backup**: 데이터 디렉토리 전체의 스냅샷이다. `pg_basebackup` 명령으로 생성한다. Base Backup은 특정 시점의 데이터베이스 상태를 담고 있다. 하지만 이 시점 이후의 변경 사항은 포함되지 않는다.

- **Base Backup + WAL = PITR**: Base Backup을 복원하고, 그 이후의 WAL을 순서대로 재생하면 원하는 시점으로 복구할 수 있다. 예를 들어 "2월 13일 오전 10시 Base Backup + 오전 10시~오후 2시 30분 WAL"을 재생하면 오후 2시 30분 상태로 복구된다.

- **PITR의 사용 사례**: 실수로 테이블을 DROP했을 때, "DROP 직전 시점"으로 복구한다. 악의적인 데이터 변조가 발견되었을 때, "변조 직전 시점"으로 복구한다. 프로덕션 데이터로 테스트 환경을 구성할 때, "어제 밤 12시 상태"를 복원한다.

- **WAL 압축과 보관 기간**: WAL 파일은 빠르게 쌓인다. 쓰기가 많으면 하루에 수십 GB가 될 수 있다. CNPG는 gzip으로 압축해서 저장한다(약 70~80% 절약). `retentionPolicy: "30d"`로 30일 이상 된 WAL과 백업을 자동 삭제한다.

**심화 질문:**

- WAL 파일이 아카이빙되기 전에 Primary가 죽으면 어떻게 되는가? (힌트: 마지막 WAL은 손실될 수 있다, `archive_mode = always` 옵션)
- PITR로 복원할 때 `recovery_target_action`을 `promote`/`pause`/`shutdown` 중 무엇으로 설정해야 하는가? (힌트: 복원 후 확인이 필요하면 pause)

---

## Q6. CNPG에서 Rolling Update가 동작하는 방식 (Primary 마지막)

**질문:** PostgreSQL 버전을 업그레이드하거나 설정을 변경할 때, CNPG는 어떻게 무중단으로 Rolling Update를 수행하며, Primary는 왜 마지막에 재시작되는가?

**핵심 포인트:**

- **Rolling Update 순서**: Replica들을 먼저 하나씩 재시작한다. 각 Replica가 정상 동작하는 것을 확인한 후 다음 Replica로 넘어간다. 모든 Replica가 업데이트되면 마지막으로 Primary를 재시작한다.

- **Primary를 마지막에 하는 이유**: Primary는 쓰기를 담당한다. Primary를 먼저 재시작하면 쓰기가 중단된다. Replica를 먼저 업데이트하면 새 버전의 Replica가 준비된 상태에서 Primary를 전환할 수 있다. 쓰기 중단 시간을 최소화하는 전략이다.

- **Primary 재시작 과정**: Primary를 재시작할 때, CNPG는 Switchover를 수행한다. Replica 중 하나를 새 Primary로 승격시키고(Failover와 동일), 기존 Primary를 재시작한다. 재시작된 Pod는 Replica로 합류한다. 이 상태로 잠시 운영하다가, 필요하면 다시 Switchback(원래 Primary로 되돌림)을 수행한다.

- **Switchback은 선택적**: 기본적으로 CNPG는 Switchback을 자동으로 하지 않는다. 새 Primary가 그대로 Primary로 남는다. 이는 추가 중단을 피하기 위해서다. 사용자가 원하면 `kubectl cnpg promote`로 수동 Switchback을 수행할 수 있다.

- **메이저 버전 업그레이드의 한계**: Streaming Replication은 같은 메이저 버전 간에만 동작한다(예: 15.1 ↔ 15.3 가능, 15.x ↔ 16.x 불가능). 메이저 버전 업그레이드(15 → 16)는 Rolling Update로 불가능하다. Blue-Green 방식(새 클러스터를 16으로 생성, Logical Replication으로 데이터 동기화, 트래픽 전환)을 사용해야 한다.

- **설정 변경 vs 이미지 변경**: 설정 변경(postgresql.parameters)은 대부분 SIGHUP으로 처리되므로 재시작이 필요 없다. 하지만 `shared_buffers` 같은 일부 설정은 재시작이 필요하다. 이미지 변경(PostgreSQL 버전, 확장 설치 등)은 항상 재시작이 필요하다.

**심화 질문:**

- Rolling Update 중 한 Replica가 재시작에 실패하면 어떻게 되는가? 전체 업데이트가 중단되는가? (힌트: CNPG는 실패한 Pod를 건너뛰고 계속 진행, 사용자에게 알림)
- K8s의 PodDisruptionBudget(PDB)가 CNPG Rolling Update에 어떻게 영향을 미치는가? (힌트: PDB가 있으면 동시 재시작 수를 제한)

---

## Q7. 애플리케이션이 Primary/Replica 엔드포인트를 구분하는 방법

**질문:** 애플리케이션은 `-rw` Service(Primary)와 `-ro` Service(Replica)를 어떻게 사용해야 하며, Read-Write 분리의 이점과 주의사항은 무엇인가?

**핵심 포인트:**

- **기본 연결 방식**: 대부분의 애플리케이션은 `-rw` Service만 사용한다. 모든 쿼리(읽기+쓰기)를 Primary로 보낸다. 간단하지만 Primary에 부하가 집중된다.

- **Read-Write 분리**: 쓰기와 강한 일관성이 필요한 읽기는 `-rw`로, 최종 일관성이 허용되는 읽기는 `-ro`로 보낸다. 예를 들어 "사용자가 방금 작성한 게시글 조회"는 `-rw`(Primary)로, "대시보드 통계 조회"는 `-ro`(Replica)로 보낸다.

- **Replication Lag 문제**: Replica는 Primary보다 약간 뒤처진다. Replication Lag가 1초라면, Primary에 쓴 데이터가 1초 후 Replica에 나타난다. 사용자가 글을 쓰고 바로 조회하면 Replica에는 아직 없을 수 있다. 이를 "Read Your Writes Consistency" 문제라고 한다.

- **Session Stickiness로 해결**: 사용자가 쓰기를 했으면, 그 사용자의 다음 읽기는 Primary로 보낸다. 일정 시간(예: 5초) 후에는 다시 Replica로 보낸다. 이렇게 하면 사용자는 자신이 쓴 데이터를 즉시 볼 수 있다. 애플리케이션 레벨에서 구현해야 한다(세션 플래그 사용).

- **Connection Pooler (PgBouncer)**: `-rw`, `-ro` Service에 각각 PgBouncer를 배치하면 연결 풀링이 가능하다. 애플리케이션이 1000개 연결을 열어도 PostgreSQL에는 10~20개 연결만 유지된다. `max_connections` 제한을 완화할 수 있다.

- **Failover 시 동작**: Primary가 죽어서 Replica가 승격되면, `-rw` Service의 엔드포인트가 자동으로 새 Primary로 바뀐다. 애플리케이션은 연결 재시도 로직만 구현하면 된다. `-ro` Service는 남은 Replica들을 가리키므로 영향이 적다.

- **ORM 지원**: Hibernate, Django ORM, ActiveRecord 같은 ORM은 Read-Write 분리를 지원한다. 설정에서 Primary와 Replica 엔드포인트를 각각 지정하고, ORM이 쿼리 타입(SELECT vs INSERT/UPDATE/DELETE)에 따라 자동 라우팅한다.

**심화 질문:**

- Replica에서 SELECT FOR UPDATE를 실행하면 어떻게 되는가? (힌트: 읽기 전용이므로 에러 발생)
- PgBouncer의 Pool Mode(Session, Transaction, Statement) 중 무엇을 사용해야 하며, 각각의 트레이드오프는 무엇인가? (힌트: Session은 안전하지만 연결 재사용 낮음, Transaction은 재사용 높음)
