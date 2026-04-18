# Ch.11 - 쿼리 최적화와 모니터링

> **이론 매핑**: `docs/04_Database/04_PostgreSQL/A_최적화_팁.md` + `B_PostgreSQL_적합성.md` + `C_성능_모니터링.md`

---

## 핵심 요약

PostgreSQL 성능 최적화는 세 가지 축으로 구성된다. 첫째, EXPLAIN ANALYZE와 pg_stat_statements로 병목 지점을 정확히 식별하는 것. 둘째, shared_buffers, work_mem 등 설정 파라미터를 워크로드에 맞게 튜닝하는 것. 셋째, VACUUM과 autovacuum을 적절히 관리하여 dead tuple 누적을 방지하는 것. 여기에 PgBouncer 같은 커넥션 풀링으로 연결 오버헤드까지 줄이면, PostgreSQL 하나로 상당한 규모의 워크로드를 처리할 수 있다.

---

## 학습 목표

1. EXPLAIN (ANALYZE, BUFFERS) 출력을 해석하여 쿼리 병목을 진단할 수 있다
2. pg_stat_user_tables, pg_stat_activity로 테이블/쿼리 상태를 모니터링할 수 있다
3. pg_stat_statements로 가장 비용이 큰 쿼리를 식별할 수 있다
4. shared_buffers, work_mem의 역할과 튜닝 기준을 설명할 수 있다
5. VACUUM과 autovacuum의 동작 원리와 튜닝 포인트를 이해할 수 있다
6. PgBouncer의 풀링 모드를 이해하고 적절한 모드를 선택할 수 있다

---

## 본문

### 1. EXPLAIN ANALYZE 심화

EXPLAIN은 쿼리 실행 계획을 보여주고, ANALYZE를 추가하면 실제로 쿼리를 실행하여 런타임 통계를 수집한다. BUFFERS 옵션까지 켜면 I/O 패턴을 분석할 수 있다.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.order_date > '2024-01-01';
```

출력 해석의 핵심 요소:

```
Hash Join  (cost=1.05..24.10 rows=100 width=200)
           (actual time=0.050..0.120 rows=85 loops=1)
  ->  Seq Scan on orders o
           (cost=0.00..22.00 rows=100 width=100)
           (actual time=0.010..0.050 rows=100 loops=1)
        Filter: (order_date > '2024-01-01')
        Rows Removed by Filter: 400
  ->  Hash (cost=1.03..1.03 rows=50 width=100)
        Buckets: 1024  Memory Usage: 9kB
Planning Time: 0.150 ms
Execution Time: 0.200 ms
```

| 항목 | 의미 | 주의 사항 |
|------|------|----------|
| cost=시작..총 | 예상 비용 (임의 단위) | 절대값보다 비교에 사용 |
| rows (예상 vs 실제) | 예상 행 수 vs 실제 행 수 | 큰 차이 -> ANALYZE 필요 |
| Buffers: shared hit | 메모리 캐시에서 읽음 | 높을수록 좋음 |
| Buffers: shared read | 디스크에서 읽음 | 높으면 메모리 부족 의심 |
| Rows Removed by Filter | 필터에서 제거된 행 | 높으면 인덱스 필요 의심 |

**예상 rows와 실제 rows 차이가 크면** 통계가 부정확한 것이다. `ANALYZE tablename;`을 실행해서 통계를 갱신해야 한다. 대량 데이터 변경(마이그레이션, 벌크 INSERT) 후에는 반드시 ANALYZE를 실행하는 것이 좋다.

스캔 유형별 효율 순서:

```
Index Only Scan > Index Scan > Bitmap Index Scan > Seq Scan
```

Seq Scan이 항상 나쁜 것은 아니다. 작은 테이블이나 대부분의 행을 반환하는 쿼리에서는 Seq Scan이 오히려 효율적이다. 문제가 되는 것은 **대형 테이블에서 소수의 행을 찾는데 Seq Scan이 발생하는 경우**다.

### 2. pg_stat 시스템 뷰로 모니터링

PostgreSQL은 내부 통계를 수집하는 시스템 뷰를 제공한다. 핵심 세 가지를 다룬다.

**pg_stat_activity**: 현재 실행 중인 쿼리 확인

```sql
-- 현재 활성 쿼리 (오래 실행 중인 순)
SELECT pid,
       now() - query_start AS duration,
       query,
       state,
       wait_event_type
FROM pg_stat_activity
WHERE state != 'idle'
  AND query NOT LIKE '%pg_stat_activity%'
ORDER BY duration DESC;

-- 5분 이상 실행 중인 쿼리 강제 종료
SELECT pg_cancel_backend(pid);     -- 쿼리만 취소
SELECT pg_terminate_backend(pid);  -- 연결 종료
```

**pg_stat_user_tables**: 테이블별 읽기/쓰기 통계

```sql
-- 순차 스캔이 많은 테이블 (인덱스 후보)
SELECT
    schemaname || '.' || relname AS table_name,
    seq_scan,
    seq_tup_read,
    idx_scan,
    n_live_tup,
    n_dead_tup,
    last_autovacuum
FROM pg_stat_user_tables
WHERE seq_scan > 100
ORDER BY seq_tup_read DESC LIMIT 10;
```

`seq_scan`이 높고 `idx_scan`이 낮은 테이블은 인덱스가 필요할 가능성이 높다. `n_dead_tup`이 `n_live_tup` 대비 높으면 VACUUM이 필요하다.

**pg_stat_user_indexes**: 인덱스 사용 현황

```sql
-- 사용되지 않는 인덱스 (디스크 낭비)
SELECT
    schemaname || '.' || relname AS table_name,
    indexrelname AS index_name,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### 3. pg_stat_statements로 느린 쿼리 식별

pg_stat_statements는 쿼리별 누적 통계를 수집하는 확장이다. 프로덕션 환경에서 성능 분석의 첫 단계로 사용한다.

```sql
-- 총 실행 시간 기준 상위 쿼리
SELECT
    query,
    calls,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    round(mean_exec_time::numeric, 2) AS avg_time_ms,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- 캐시 히트율이 낮은 쿼리 (I/O 병목)
SELECT
    query,
    calls,
    shared_blks_hit,
    shared_blks_read,
    round(100.0 * shared_blks_hit /
          nullif(shared_blks_hit + shared_blks_read, 0), 2) AS hit_ratio
FROM pg_stat_statements
WHERE shared_blks_hit + shared_blks_read > 100
ORDER BY hit_ratio ASC
LIMIT 10;
```

캐시 히트율이 95% 이하인 쿼리는 shared_buffers 부족 또는 인덱스 전략 재검토가 필요하다.

### 4. 설정 파라미터 튜닝

PostgreSQL의 기본 설정은 보수적이다. 워크로드에 맞게 핵심 파라미터를 조정해야 한다.

| 파라미터 | 기본값 | 권장 설정 | 역할 |
|---------|-------|----------|------|
| shared_buffers | 128MB | RAM의 25% | 공유 메모리 캐시 |
| work_mem | 4MB | 64-256MB | 정렬, 해시 작업용 |
| effective_cache_size | 4GB | RAM의 75% | 플래너 힌트 (실제 할당 아님) |
| maintenance_work_mem | 64MB | 512MB-1GB | VACUUM, CREATE INDEX용 |
| max_connections | 100 | 워크로드 기반 | 최대 동시 연결 수 |

**shared_buffers**: PostgreSQL이 데이터를 캐시하는 공유 메모리 영역이다. RAM의 25%가 일반적 시작점이다. OS 캐시도 활용하므로 50% 이상은 오히려 역효과가 날 수 있다.

**work_mem**: ORDER BY, GROUP BY, Hash Join 등에서 사용하는 작업 메모리다. 이 값을 초과하면 디스크에 임시 파일을 쓴다. 주의할 점은 **쿼리 하나가 여러 정렬 작업을 수행하면 각각 work_mem을 할당**받는다는 것이다. 연결 수가 많으면 전체 메모리 사용량이 급증할 수 있으므로, `max_connections * work_mem * 예상 정렬 수`가 가용 RAM을 초과하지 않는지 확인해야 한다.

**effective_cache_size**: 실제 메모리를 할당하지 않고, 쿼리 플래너에게 "OS 캐시를 포함해 이만큼의 캐시가 가용하다"는 힌트를 준다. 이 값이 크면 플래너가 인덱스 스캔을 더 선호하게 된다.

### 5. VACUUM과 autovacuum

MVCC에서 UPDATE는 새 버전을 생성하고 기존 버전을 dead tuple로 남긴다. VACUUM은 이 dead tuple을 정리하여 공간을 재활용한다.

```sql
-- Dead tuple이 많은 테이블 확인
SELECT
    schemaname || '.' || relname AS table_name,
    n_live_tup,
    n_dead_tup,
    round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2)
        AS dead_ratio,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- 수동 VACUUM + 통계 갱신
VACUUM ANALYZE table_name;

-- 전체 재구성 (주의: 테이블 락 발생)
VACUUM FULL table_name;
```

VACUUM과 VACUUM FULL의 차이:

| 구분 | VACUUM | VACUUM FULL |
|------|--------|-------------|
| 락 | 읽기/쓰기 가능 | 테이블 배타적 락 |
| 공간 반환 | OS에 반환 안 함 (재활용만) | OS에 반환 |
| 시간 | 빠름 | 느림 (테이블 재작성) |
| 용도 | 일상적 정리 | 대량 삭제 후 디스크 회수 |

autovacuum은 PostgreSQL이 자동으로 VACUUM을 실행하는 데몬이다. 기본 설정은 대부분의 워크로드에서 적절하지만, 대량 쓰기가 발생하는 테이블은 테이블별로 튜닝할 수 있다.

```sql
-- 특정 테이블의 autovacuum 설정 조정
ALTER TABLE high_write_table SET (
    autovacuum_vacuum_threshold = 50,         -- 기본 50
    autovacuum_vacuum_scale_factor = 0.05,    -- 기본 0.2 (20% -> 5%)
    autovacuum_analyze_threshold = 50,
    autovacuum_analyze_scale_factor = 0.05
);
```

`autovacuum_vacuum_scale_factor`를 낮추면 VACUUM이 더 자주 실행된다. 대형 테이블(수천만 행)에서는 기본값 0.2(20%)가 너무 크므로, 0.01-0.05로 낮추는 것이 일반적이다.

### 6. 커넥션 풀링: PgBouncer

PostgreSQL은 연결 하나당 하나의 OS 프로세스를 생성한다. 연결 수가 많으면 프로세스 생성/종료 오버헤드와 메모리 소비가 문제가 된다. PgBouncer는 이 문제를 해결하는 경량 커넥션 풀러다.

```
커넥션 풀링 아키텍처
┌─────────┐  ┌─────────┐  ┌─────────┐
│  App 1  │  │  App 2  │  │  App 3  │
└────┬────┘  └────┬────┘  └────┬────┘
     └────────────┼────────────┘
                  v
     ┌────────────────────────┐
     │       PgBouncer        │
     │  Pool: 20 connections  │  <-- 실제 DB 연결은 20개
     └───────────┬────────────┘
                 v
     ┌───────────────────────┐
     │     PostgreSQL        │
     │  max_connections=100  │
     └───────────────────────┘
```

PgBouncer의 세 가지 풀링 모드:

| 모드 | 연결 반환 시점 | Prepared Statement | 세션 변수 | 적합 환경 |
|------|-------------|-------------------|----------|----------|
| Session | 세션 종료 시 | 가능 | 가능 | Prepared Statement 필수 |
| **Transaction** | 트랜잭션 완료 시 | 불가 | 불가 | 웹 앱 (권장) |
| Statement | 각 쿼리 완료 시 | 불가 | 불가 | 단순 읽기 |

Transaction 모드가 가장 효율적이지만, `SET` 명령어나 Prepared Statement를 사용하는 애플리케이션에서는 Session 모드가 필요하다. 대부분의 웹 애플리케이션은 Transaction 모드로 충분하다.

클라이언트 사이드(HikariCP, SQLAlchemy)와 서버 사이드(PgBouncer) 풀링의 차이:

| 구분 | Client-side | Server-side (PgBouncer) |
|------|-------------|-------------------------|
| 위치 | 애플리케이션 내부 | 데이터베이스 앞단 |
| 효과 | 단일 앱 내 연결 재사용 | 여러 앱의 연결 집계 |
| 적합 | 단일 앱 | 마이크로서비스, 다중 앱 |

마이크로서비스 환경에서는 각 서비스가 자체 풀을 가지므로, 서비스 수가 늘어나면 총 연결 수가 급증한다. PgBouncer를 중간에 배치하면 실제 DB 연결을 적은 수로 유지할 수 있다.

### 7. SELECT 최적화 원칙

쿼리 작성 습관이 성능에 미치는 영향은 생각보다 크다.

**SELECT * 피하기**: 불필요한 컬럼까지 읽으면 DB의 직렬화, 네트워크 전송, 애플리케이션의 역직렬화 비용이 모두 증가한다. JSONB나 TEXT 같은 가변 크기 컬럼이 포함되면 영향이 배가된다.

**count(*) vs count(column)**: `count(*)`는 행 존재 여부만 확인하므로 컬럼 값을 읽지 않는다(width=0). `count(column)`은 NULL 제외를 위해 컬럼 값을 실제로 읽는다. 행 수만 세려면 `count(*)`가 효율적이다.

**정렬/집계는 DB에서**: 100만 행을 애플리케이션으로 가져와 정렬하는 대신, `ORDER BY ... LIMIT`으로 DB에서 처리하면 인덱스를 활용할 수 있고 네트워크 전송량도 줄어든다.

### 8. PostgreSQL 적합성 판단

모든 워크로드에 PostgreSQL이 최적은 아니다. 적합하지 않은 경우를 아는 것도 중요하다.

| 워크로드 | PostgreSQL | 대안 | 선택 기준 |
|---------|-----------|------|----------|
| 일반 CRUD | 적합 | - | PostgreSQL |
| JSON 문서 | JSONB로 대응 | MongoDB | 규모와 스키마 유연성 요구에 따라 |
| 벡터 검색 | pgvector로 대응 | Pinecone, Milvus | 수억 벡터 이상이면 전문 DB |
| 순수 그래프 쿼리 | 부적합 | Neo4j | 그래프가 핵심이면 전문 DB |
| 페타바이트 분석 | 부적합 | ClickHouse, DuckDB | 대용량 분석 전문 DB |
| 실시간 스트리밍 | 부적합 | Kafka Streams | 스트리밍 처리 시스템 |

핵심 원칙: "Just Use Postgres"는 "항상 Postgres만 사용하라"가 아니라, "Postgres의 다양한 가능성을 먼저 검토하라"는 뜻이다. 기존 시스템이 잘 작동하고 있다면 굳이 교체할 필요가 없고, 팀이 다른 DB에 능숙하다면 그 전문성을 활용하는 것이 실용적이다.

---

## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| EXPLAIN (ANALYZE, BUFFERS) | 실행 계획 + 런타임 통계 + I/O 패턴 분석 |
| pg_stat_statements | 쿼리별 누적 통계, 느린 쿼리 식별의 시작점 |
| shared_buffers | RAM의 25%, 공유 메모리 캐시 |
| work_mem | 정렬/해시 작업용, 연결 수 대비 메모리 총량 주의 |
| VACUUM | dead tuple 정리, FULL은 락 발생하므로 일상적으로는 일반 VACUUM |
| autovacuum 튜닝 | 대형 테이블은 scale_factor를 0.01-0.05로 낮춤 |
| PgBouncer | Transaction 모드가 기본, 마이크로서비스 환경에서 필수 |
| 적합성 판단 | 그래프/페타바이트 분석/스트리밍은 전문 DB가 적합 |
