# PostgreSQL 성능 모니터링

---

## 📌 핵심 요약

PostgreSQL의 성능 모니터링을 위한 시스템 뷰(pg_stat_*), EXPLAIN ANALYZE를 활용한 쿼리 분석, 그리고 일반적인 성능 병목 지점 해결 방법을 다룬다.

---

## 🎯 학습 목표

- [ ] pg_stat_* 시스템 뷰를 활용한 모니터링 방법을 알 수 있다
- [ ] EXPLAIN ANALYZE로 쿼리 실행 계획을 분석할 수 있다
- [ ] 일반적인 성능 병목 지점을 식별하고 해결할 수 있다
- [ ] 인덱스 사용 현황을 분석할 수 있다

---

## 📖 본문

### 1. 시스템 통계 뷰 (pg_stat_*)

#### 1.1 주요 통계 뷰

| 뷰 | 설명 |
|-----|------|
| `pg_stat_activity` | 현재 실행 중인 쿼리 |
| `pg_stat_user_tables` | 테이블별 통계 |
| `pg_stat_user_indexes` | 인덱스별 통계 |
| `pg_stat_statements` | 쿼리별 통계 (확장 필요) |
| `pg_stat_bgwriter` | 백그라운드 writer 통계 |

#### 1.2 pg_stat_activity - 현재 쿼리 확인

```sql
-- 현재 실행 중인 쿼리
SELECT
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state,
    wait_event_type,
    wait_event
FROM pg_stat_activity
WHERE state != 'idle'
  AND query NOT LIKE '%pg_stat_activity%'
ORDER BY duration DESC;

-- 5분 이상 실행 중인 쿼리
SELECT pid, query, state, query_start
FROM pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > interval '5 minutes';

-- 장시간 쿼리 강제 종료
SELECT pg_cancel_backend(pid);  -- 쿼리만 취소
SELECT pg_terminate_backend(pid);  -- 연결 종료
```

#### 1.3 pg_stat_user_tables - 테이블 통계

```sql
-- 테이블별 읽기/쓰기 통계
SELECT
    schemaname,
    relname AS table_name,
    seq_scan,        -- 순차 스캔 횟수
    seq_tup_read,    -- 순차 스캔으로 읽은 행 수
    idx_scan,        -- 인덱스 스캔 횟수
    idx_tup_fetch,   -- 인덱스로 가져온 행 수
    n_tup_ins,       -- 삽입된 행 수
    n_tup_upd,       -- 업데이트된 행 수
    n_tup_del,       -- 삭제된 행 수
    n_live_tup,      -- 현재 행 수
    n_dead_tup,      -- Dead tuple 수 (VACUUM 필요)
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- 순차 스캔이 많은 테이블 (인덱스 필요 가능성)
SELECT
    schemaname || '.' || relname AS table,
    seq_scan,
    seq_tup_read,
    CASE WHEN seq_scan > 0
         THEN seq_tup_read / seq_scan
         ELSE 0
    END AS avg_seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 100
ORDER BY seq_tup_read DESC
LIMIT 10;
```

#### 1.4 pg_stat_user_indexes - 인덱스 사용 현황

```sql
-- 사용되지 않는 인덱스 찾기
SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'  -- PK 제외
ORDER BY pg_relation_size(indexrelid) DESC;

-- 인덱스 효율성 분석
SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    CASE WHEN idx_tup_read > 0
         THEN round(100.0 * idx_tup_fetch / idx_tup_read, 2)
         ELSE 0
    END AS fetch_ratio
FROM pg_stat_user_indexes
WHERE idx_scan > 0
ORDER BY idx_scan DESC;
```

---

### 2. EXPLAIN ANALYZE 심화

#### 2.1 기본 사용법

```sql
EXPLAIN ANALYZE
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.order_date > '2024-01-01';
```

#### 2.2 출력 해석

```
Hash Join  (cost=1.05..24.10 rows=100 width=200) (actual time=0.050..0.120 rows=85 loops=1)
  Hash Cond: (o.customer_id = c.id)
  ->  Seq Scan on orders o  (cost=0.00..22.00 rows=100 width=100) (actual time=0.010..0.050 rows=100 loops=1)
        Filter: (order_date > '2024-01-01'::date)
        Rows Removed by Filter: 400
  ->  Hash  (cost=1.03..1.03 rows=50 width=100) (actual time=0.020..0.020 rows=50 loops=1)
        Buckets: 1024  Batches: 1  Memory Usage: 9kB
        ->  Seq Scan on customers c  (cost=0.00..1.03 rows=50 width=100)
Planning Time: 0.150 ms
Execution Time: 0.200 ms
```

| 항목 | 설명 |
|------|------|
| `cost=0.00..22.00` | 예상 비용 (시작..총) |
| `rows=100` | 예상 행 수 |
| `actual time=0.010..0.050` | 실제 시간 (ms) |
| `rows=100` (actual) | 실제 행 수 |
| `loops=1` | 실행 횟수 |
| `Rows Removed by Filter` | 필터에서 제외된 행 |

#### 2.3 주요 노드 유형

| 노드 | 설명 | 성능 영향 |
|------|------|----------|
| Seq Scan | 전체 테이블 스캔 | 대용량 시 느림 |
| Index Scan | 인덱스 → 테이블 | 선택적 조회에 효율 |
| Index Only Scan | 인덱스만으로 완료 | 가장 효율적 |
| Bitmap Index Scan | 비트맵으로 여러 인덱스 결합 | 중간 선택도에 효율 |
| Hash Join | 해시 테이블 기반 조인 | 동등 조인에 효율 |
| Nested Loop | 중첩 루프 조인 | 소규모에 적합 |
| Sort | 정렬 | 메모리 사용, 느릴 수 있음 |

#### 2.4 EXPLAIN 옵션

```sql
-- 버퍼 사용량 포함
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE id = 100;

-- 포맷 지정
EXPLAIN (ANALYZE, FORMAT JSON)
SELECT * FROM orders WHERE id = 100;

-- 상세 출력
EXPLAIN (ANALYZE, VERBOSE, BUFFERS, TIMING)
SELECT * FROM orders WHERE id = 100;
```

---

### 3. pg_stat_statements

#### 3.1 설정 및 활성화

```sql
-- postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

-- 확장 생성
CREATE EXTENSION pg_stat_statements;
```

#### 3.2 느린 쿼리 분석

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

-- 평균 실행 시간이 긴 쿼리
SELECT
    query,
    calls,
    round(mean_exec_time::numeric, 2) AS avg_time_ms,
    round(stddev_exec_time::numeric, 2) AS stddev_ms
FROM pg_stat_statements
WHERE calls > 10
ORDER BY mean_exec_time DESC
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

---

### 4. 성능 병목 해결

#### 4.1 인덱스 누락

```sql
-- 문제: Seq Scan on large table
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 100;

-- 해결: 인덱스 생성
CREATE INDEX idx_orders_customer ON orders (customer_id);

-- 확인: Index Scan 사용
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 100;
```

#### 4.2 비효율적인 인덱스

```sql
-- 문제: 선택도가 낮은 인덱스 (많은 행 반환)
-- 해결: 복합 인덱스 또는 Covering Index

-- Before
CREATE INDEX idx_status ON orders (status);  -- 선택도 낮음

-- After (더 선택적인 복합 인덱스)
CREATE INDEX idx_status_date ON orders (status, order_date DESC);
```

#### 4.3 락 경합

```sql
-- 현재 락 확인
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity
    ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity
    ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

#### 4.4 VACUUM 필요

```sql
-- Dead tuple이 많은 테이블 확인
SELECT
    schemaname || '.' || relname AS table,
    n_live_tup,
    n_dead_tup,
    round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- 수동 VACUUM
VACUUM ANALYZE table_name;

-- 전체 재구성 (락 발생 주의)
VACUUM FULL table_name;
```

---

### 5. 연결 풀 모니터링

```sql
-- 연결 상태별 수
SELECT
    state,
    count(*) AS connections
FROM pg_stat_activity
GROUP BY state;

-- 데이터베이스별 연결 수
SELECT
    datname,
    count(*) AS connections
FROM pg_stat_activity
GROUP BY datname;

-- 최대 연결 수 확인
SHOW max_connections;

-- 현재 연결 수
SELECT count(*) FROM pg_stat_activity;
```

---

### 6. 디스크 사용량 모니터링

```sql
-- 테이블별 크기
SELECT
    schemaname || '.' || relname AS table,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
    pg_size_pretty(pg_relation_size(relid)) AS table_size,
    pg_size_pretty(pg_indexes_size(relid)) AS indexes_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;

-- 데이터베이스 크기
SELECT
    datname,
    pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

-- 테이블스페이스 크기
SELECT
    spcname,
    pg_size_pretty(pg_tablespace_size(spcname)) AS size
FROM pg_tablespace;
```

---

## 💡 실무 적용

### 모니터링 체크리스트

```
□ 느린 쿼리 식별 (pg_stat_statements)
□ 사용되지 않는 인덱스 정리
□ Dead tuple 비율 확인 (VACUUM 필요성)
□ 연결 풀 사용률 확인
□ 디스크 사용량 추세 확인
□ 캐시 히트율 확인
```

### 외부 모니터링 도구

| 도구 | 설명 |
|------|------|
| pgAdmin | GUI 기반 관리/모니터링 |
| pg_top | top과 유사한 실시간 모니터링 |
| pgBadger | 로그 분석 및 리포트 |
| Prometheus + Grafana | 메트릭 수집 및 시각화 |

---

## ✅ 체크리스트

- [ ] pg_stat_activity로 현재 쿼리를 확인할 수 있다
- [ ] pg_stat_user_tables로 테이블 통계를 분석할 수 있다
- [ ] EXPLAIN ANALYZE 출력을 해석할 수 있다
- [ ] pg_stat_statements로 느린 쿼리를 찾을 수 있다
- [ ] 사용되지 않는 인덱스를 식별할 수 있다
- [ ] VACUUM 필요성을 판단할 수 있다

---

## 🔗 참고 자료

- 📄 PostgreSQL Statistics Collector: https://www.postgresql.org/docs/current/monitoring-stats.html
- 📄 EXPLAIN Documentation: https://www.postgresql.org/docs/current/using-explain.html
- 📄 pg_stat_statements: https://www.postgresql.org/docs/current/pgstatstatements.html
