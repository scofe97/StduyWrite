# Ch.11 - 쿼리 최적화와 모니터링: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. VACUUM과 autovacuum 튜닝은 어떻게 접근하는가?

### 왜 이 질문이 중요한가

VACUUM은 PostgreSQL 운영의 핵심이다. autovacuum이 제때 동작하지 않으면 테이블이 비대해지고 쿼리 성능이 저하되며, 최악의 경우 Transaction ID Wraparound로 DB가 셧다운될 수 있다. DBA가 아니더라도 백엔드 개발자가 autovacuum의 동작 원리와 튜닝 포인트를 이해하고 있어야 한다.

### 답변

**autovacuum 트리거 조건**:

autovacuum은 다음 공식으로 실행 여부를 결정한다.

```
VACUUM 실행 조건:
dead_tuples > autovacuum_vacuum_threshold
              + autovacuum_vacuum_scale_factor * n_live_tup

기본값: 50 + 0.2 * n_live_tup

예시: 100만 행 테이블
-> 50 + 0.2 * 1,000,000 = 200,050개 dead tuple이 쌓여야 VACUUM 실행
-> 20%나 쌓여야 실행된다는 의미
```

대형 테이블에서는 이 기본값이 너무 관대하다. 1000만 행 테이블이면 200만 dead tuple이 쌓여야 VACUUM이 동작한다.

**테이블별 튜닝**:

```sql
-- 쓰기 빈번한 대형 테이블: 5%마다 VACUUM
ALTER TABLE high_write_table SET (
    autovacuum_vacuum_scale_factor = 0.05,    -- 20% -> 5%
    autovacuum_vacuum_threshold = 1000,       -- 최소 임계값
    autovacuum_analyze_scale_factor = 0.02,   -- ANALYZE도 자주
    autovacuum_vacuum_cost_delay = 2          -- 기본 20ms -> 2ms (빠르게)
);

-- 거의 변경되지 않는 참조 테이블: 기본값 유지
-- (별도 설정 불필요)
```

**autovacuum이 지연되는 원인과 대응**:

| 원인 | 증상 | 대응 |
|------|------|------|
| 긴 트랜잭션 | dead tuple 정리 불가 | idle_in_transaction_session_timeout 설정 |
| autovacuum_max_workers 부족 | 대기 중인 테이블 누적 | workers 수 증가 (기본 3 -> 5) |
| cost_delay가 너무 큼 | VACUUM이 느리게 진행 | cost_delay 감소 |
| 대형 테이블 독점 | 다른 테이블 VACUUM 지연 | 테이블별 설정 분리 |

**Transaction ID Wraparound 방지**:

```sql
-- 현재 가장 오래된 미정리 xid 확인
SELECT datname, age(datfrozenxid) AS xid_age,
       current_setting('autovacuum_freeze_max_age') AS freeze_max
FROM pg_database;

-- xid_age가 autovacuum_freeze_max_age(기본 2억)에 접근하면 위험
-- 1.5억 이상이면 수동 VACUUM FREEZE 고려
VACUUM FREEZE table_name;
```

**VACUUM FULL은 언제 필요한가?**

일반 VACUUM은 dead tuple을 재활용 가능 상태로 만들지만, 디스크 공간을 OS에 반환하지 않는다. 대량 DELETE 후 실제 디스크를 회수하려면 VACUUM FULL이 필요하지만, 배타적 락이 걸리므로 프로덕션에서는 주의해야 한다.

```sql
-- 대안: pg_repack (락 없이 테이블 재구성)
-- 확장 설치 필요
CREATE EXTENSION pg_repack;
-- 터미널에서: pg_repack -t table_name dbname
```

### 실무 적용

- 기본 autovacuum 설정은 대부분 테이블에 충분
- 쓰기 빈번한 대형 테이블은 scale_factor를 0.01-0.05로 낮춤
- pg_stat_user_tables의 n_dead_tup과 last_autovacuum을 주기적 모니터링
- Transaction ID age가 10억에 접근하면 즉시 대응

---

## Q2. PgBouncer vs Pgpool-II: 커넥션 풀링 솔루션은 어떻게 선택하는가?

### 왜 이 질문이 중요한가

마이크로서비스 환경에서 커넥션 관리는 PostgreSQL 운영의 가장 흔한 병목이다. "max_connections에 도달했다"는 에러를 경험한 팀이 많다. PgBouncer와 Pgpool-II의 차이를 이해하고, 환경에 맞는 솔루션을 선택할 수 있어야 한다.

### 답변

**아키텍처 차이**:

```
PgBouncer:
┌──────────┐     ┌───────────┐     ┌────────────┐
│ 100 Clients│ --> │ PgBouncer │ --> │ PostgreSQL │
│           │     │ (단일 프로세스│     │ 20 conn    │
│           │     │  경량, 2-3MB)│     │            │
└──────────┘     └───────────┘     └────────────┘
역할: 순수 커넥션 풀링

Pgpool-II:
┌──────────┐     ┌────────────┐     ┌────────────┐
│ 100 Clients│ --> │  Pgpool-II │ --> │ Primary    │
│           │     │ (다기능)     │ --> │ Replica 1  │
│           │     │ 풀링+LB+복제│ --> │ Replica 2  │
└──────────┘     └────────────┘     └────────────┘
역할: 풀링 + 로드밸런싱 + 자동 페일오버 + 쿼리 캐싱
```

**상세 비교**:

| 항목 | PgBouncer | Pgpool-II |
|------|-----------|-----------|
| 메모리 사용 | 2-3MB | 수십~수백MB |
| 풀링 모드 | Session/Transaction/Statement | Session 기반 |
| 로드밸런싱 | 없음 | READ/WRITE 분리 |
| 자동 페일오버 | 없음 | 지원 |
| 쿼리 캐싱 | 없음 | 지원 (메모리 기반) |
| 설정 복잡도 | 낮음 | 높음 |
| 프로토콜 호환성 | 높음 | 일부 제한 |

**Transaction 모드의 함정과 해결**:

PgBouncer Transaction 모드에서 발생하는 대표적 문제:

```sql
-- 문제 1: Prepared Statement 사용 불가
-- Java/Spring에서 HikariCP + PgBouncer Transaction 모드 사용 시
-- prepareThreshold=0 설정 필요

-- 문제 2: SET 명령어 사용 불가
SET work_mem = '256MB';  -- 다음 쿼리에서 효과 없음
-- 해결: SET LOCAL 사용 (트랜잭션 내에서만 유효)
BEGIN;
SET LOCAL work_mem = '256MB';
-- 쿼리 실행
COMMIT;

-- 문제 3: LISTEN/NOTIFY 사용 불가
-- 해결: 별도 직접 연결 사용
```

**다중 서비스 환경 설계**:

```
추천 아키텍처 (마이크로서비스):

Service A ──┐
Service B ──┼──> PgBouncer (Transaction 모드)
Service C ──┘         |
                      v
            PostgreSQL Primary
                      |
                (Streaming Replication)
                      |
            PostgreSQL Replica
                      ^
                      |
Analytics ──> PgBouncer (Session 모드, 읽기 전용)
```

### 실무 적용

- 순수 풀링만 필요: PgBouncer (간단하고 가벼움)
- HA + 로드밸런싱 통합: Pgpool-II (단, 복잡도 증가)
- 일반적 권장: PgBouncer + HAProxy(또는 Patroni) 조합
- Transaction 모드에서 Prepared Statement 이슈는 사전 테스트 필수

---

## Q3. PostgreSQL vs 특정 워크로드 전용 DB: 어떤 기준으로 판단하는가?

### 왜 이 질문이 중요한가

"Just Use Postgres"는 강력한 원칙이지만, 모든 상황에서 최적인 것은 아니다. 면접에서 "PostgreSQL의 한계를 아는가?"라는 질문에 답할 수 있어야 하고, 실무에서도 아키텍처 결정 시 객관적인 판단 기준이 필요하다.

### 답변

**PostgreSQL로 커버 가능한 범위**:

```
PostgreSQL 확장 커버리지:
┌─────────────────────────────────────────────────┐
│  OLTP (기본)                                     │
│  JSON 문서 (JSONB)                               │
│  전문 검색 (tsvector)                            │
│  벡터 검색 (pgvector)         <-- ~1000만 벡터   │
│  지리공간 (PostGIS)                              │
│  시계열 (TimescaleDB)                            │
│  메시지 큐 (pgmq, LISTEN/NOTIFY)                 │
│  그래프 (재귀 CTE)            <-- 단순 그래프    │
└─────────────────────────────────────────────────┘
```

**전용 DB가 필요한 영역**:

| 워크로드 | PostgreSQL 한계 | 전용 DB | 전환 시그널 |
|---------|---------------|---------|-----------|
| 그래프 순회 | 재귀 CTE 깊이 제한, 성능 | Neo4j | 6+ hop 관계 탐색 빈번 |
| 페타바이트 분석 | 단일 노드 한계 | ClickHouse, DuckDB | 분석 쿼리가 분 단위 |
| 실시간 스트리밍 | 이벤트 처리 부적합 | Kafka + Flink | 초당 10만+ 이벤트 |
| 인메모리 캐시 | 디스크 기반 | Redis | 서브밀리초 응답 필수 |
| 글로벌 분산 | 단일 리전 | CockroachDB, Spanner | 다중 리전 강한 일관성 |

**의사결정 프레임워크**:

```
Step 1: PostgreSQL로 구현 가능한가?
├── 불가능 -> 전용 DB
└── 가능 -> Step 2

Step 2: 구현 복잡도 vs 가치
├── 복잡도 > 가치 -> 전용 DB
└── 복잡도 < 가치 -> Step 3

Step 3: 현재 규모에서 성능이 충분한가?
├── 충분 -> PostgreSQL 유지
└── 부족 -> Step 4

Step 4: 튜닝/확장으로 해결 가능한가?
├── 가능 (인덱스, 파티셔닝, 레플리카) -> PostgreSQL 유지
└── 불가능 -> 전용 DB 도입
```

**비용 관점**: 전용 DB 도입은 기술적 비용뿐 아니라 운영 비용(인프라, 모니터링, 온콜, 학습)이 크다. PostgreSQL 하나로 80%를 커버할 수 있다면, 나머지 20%를 위해 전체 아키텍처를 복잡하게 만들 필요가 없을 수 있다.

### 실무 적용

- 프로젝트 초기: PostgreSQL로 시작하고 병목이 발생하면 전문 DB 도입
- 병목 확인 방법: pg_stat_statements로 느린 쿼리 식별, EXPLAIN으로 분석
- 전용 DB 도입 시 데이터 동기화 전략(CDC, 이벤트)이 핵심 과제
- "멋져 보여서"가 아닌 "측정된 문제를 해결하기 위해" 도입해야 함

---

## Q4. 프로덕션 PostgreSQL 모니터링 체계는 어떻게 구축하는가?

### 왜 이 질문이 중요한가

"문제가 발생한 후 대응"이 아니라 "문제가 발생하기 전에 감지"하는 모니터링 체계가 프로덕션 운영의 핵심이다. 어떤 지표를 어떤 도구로 수집하고, 어떤 임계값에서 알람을 발생시킬지 체계적으로 설계할 수 있어야 한다.

### 답변

**모니터링 계층**:

```
Layer 1: 시스템 메트릭 (OS 레벨)
  - CPU, 메모리, 디스크 I/O, 네트워크
  - 도구: node_exporter + Prometheus

Layer 2: PostgreSQL 메트릭
  - 연결 수, 캐시 히트율, 트랜잭션 수, 복제 지연
  - 도구: postgres_exporter + Prometheus + Grafana

Layer 3: 쿼리 성능
  - 느린 쿼리, 실행 계획 변화
  - 도구: pg_stat_statements, auto_explain, pgBadger

Layer 4: 비즈니스 메트릭
  - 응답 시간 (P95, P99), 에러율
  - 도구: APM (Datadog, New Relic)
```

**핵심 알람 임계값**:

| 지표 | 경고 | 위험 | 확인 쿼리 |
|------|------|------|----------|
| 연결 사용률 | 70% | 90% | `SELECT count(*) FROM pg_stat_activity` |
| 캐시 히트율 | < 95% | < 90% | `pg_stat_bgwriter의 buffers_hit 비율` |
| Dead tuple 비율 | > 10% | > 20% | `pg_stat_user_tables.n_dead_tup` |
| 복제 지연 | > 1초 | > 10초 | `pg_stat_replication.replay_lag` |
| 장시간 쿼리 | > 30초 | > 5분 | `pg_stat_activity.query_start` |
| 디스크 사용률 | > 70% | > 85% | OS 메트릭 |
| xid age | > 5억 | > 10억 | `age(datfrozenxid)` |

**Prometheus + Grafana 설정 예시**:

```yaml
# postgres_exporter로 수집되는 주요 메트릭
pg_stat_activity_count              # 연결 수
pg_stat_database_blks_hit           # 캐시 히트
pg_stat_database_blks_read          # 디스크 읽기
pg_stat_user_tables_n_dead_tup      # Dead tuple
pg_stat_replication_pg_wal_lsn_diff # 복제 지연
```

**사고 대응 체크리스트**:

```
DB 느려짐 발생:
1. pg_stat_activity: 현재 활성 쿼리 확인, 장시간 쿼리 식별
2. pg_stat_statements: 최근 느려진 쿼리 확인
3. pg_locks: 락 경합 확인
4. pg_stat_user_tables: dead tuple 축적 확인
5. 시스템 메트릭: CPU/메모리/디스크 I/O 확인
6. 복제 지연: 레플리카 기반 읽기가 있다면 지연 확인
```

### 실무 적용

- 최소 구성: pg_stat_statements + Grafana 대시보드 + 연결 수/캐시 히트율 알람
- 권장 구성: Prometheus + postgres_exporter + Grafana + PagerDuty
- pg_stat_statements는 프로덕션에서 기본 활성화 (오버헤드 미미)
- auto_explain은 운영 중 느린 쿼리 자동 로깅에 유용 (log_min_duration 설정)
