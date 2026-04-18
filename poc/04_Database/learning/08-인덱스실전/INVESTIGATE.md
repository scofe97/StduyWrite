# Ch.08 - 인덱스 실전: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. 인덱스 선택 전략: 실무에서 어떤 인덱스를 언제 만들어야 하는가?

### 왜 이 질문이 중요한가

인덱스는 "추가하면 좋은 것"이 아니라 "비용이 있는 트레이드오프"다. 면접에서도 "인덱스를 추가했는데 오히려 느려진 경험"을 물어보는 경우가 있다. 인덱스 추가/삭제의 판단 기준을 체계적으로 설명할 수 있어야 한다.

### 답변

**인덱스 필요 여부 판단 프로세스**:

```
1. EXPLAIN ANALYZE로 현재 쿼리 분석
   |
   +--> Seq Scan + Rows Removed by Filter 높음?
   |    --> 인덱스 후보
   |
   +--> 이미 Index Scan인데 느림?
   |    --> Covering Index, 복합 인덱스 재설계 검토
   |
   +--> Sort 비용이 큼?
        --> ORDER BY에 맞는 인덱스 추가
```

**인덱스 타입 선택 기준**:

```sql
-- 등호 + 범위 검색 -> B-tree (기본)
WHERE status = 'active' AND created_at > '2025-01-01'
CREATE INDEX idx ON orders(status, created_at);

-- JSONB 포함 검색 -> GIN
WHERE data @> '{"tags": ["urgent"]}'
CREATE INDEX idx ON tickets USING GIN(data);

-- 전문 검색 -> GIN (tsvector)
WHERE search_vector @@ to_tsquery('english', 'postgres')
CREATE INDEX idx ON articles USING GIN(search_vector);

-- 지리공간 근접 검색 -> GiST
WHERE ST_DWithin(location, point, 1000)
CREATE INDEX idx ON stores USING GiST(location);

-- 대용량 시계열 범위 검색 -> BRIN
WHERE created_at BETWEEN '2025-01-01' AND '2025-01-31'
CREATE INDEX idx ON logs USING BRIN(created_at);
```

**BRIN 인덱스의 숨은 강점**: 시계열 데이터처럼 물리적 삽입 순서와 컬럼 값 순서가 일치하는 테이블에서 BRIN은 B-tree 대비 인덱스 크기가 1/100 수준이다. 10억 행 테이블에서 B-tree 인덱스가 20GB라면 BRIN은 200MB 수준일 수 있다.

```sql
-- 1억 행 로그 테이블
CREATE INDEX idx_logs_brin ON logs USING BRIN(created_at)
    WITH (pages_per_range = 128);  -- 블록 범위 크기 조정
```

단, BRIN은 데이터가 물리적으로 정렬되어 있을 때만 효과적이다. 무작위 INSERT/UPDATE가 많으면 효과가 급감한다.

### 실무 적용

- 새 인덱스 추가 전 EXPLAIN ANALYZE로 현재 상태 확인
- 인덱스 추가 후 EXPLAIN ANALYZE로 효과 검증
- 쓰기 워크로드가 높은 테이블은 인덱스 수를 최소화
- 시계열 데이터는 BRIN을 먼저 검토 (B-tree보다 크기와 쓰기 비용이 월등히 작음)

---

## Q2. GIN과 GiST 인덱스는 내부적으로 어떻게 다르며, 전문 검색에서 어떤 것을 선택해야 하는가?

### 왜 이 질문이 중요한가

JSONB와 전문 검색에서 GIN/GiST 선택은 검색 속도, 인덱스 빌드 시간, 업데이트 성능에 직접 영향을 준다. 단순히 "GIN이 빠르다"가 아니라 내부 구조를 이해하면 워크로드에 맞는 선택을 할 수 있다.

### 답변

**GIN (Generalized Inverted Index)**:

역인덱스 구조로, 각 키(렉셈, JSON 키)가 해당 키를 포함하는 모든 행의 목록을 가리킨다.

```
GIN 내부 구조 (전문 검색 예시):
'database' -> [row_1, row_5, row_12, row_89]
'postgres' -> [row_2, row_5, row_7, row_45]
'index'    -> [row_3, row_12, row_67]

검색: 'database & postgres'
-> 'database' 목록과 'postgres' 목록의 교집합
-> [row_5]
```

**GiST (Generalized Search Tree)**:

트리 기반 구조로, 각 내부 노드가 하위 노드의 "요약"(bounding box, signature)을 저장한다. 손실 압축을 사용하므로 False Positive이 발생할 수 있다.

```
GiST 내부 구조:
      [Root: signature covering all]
      /                \
[Sig: pages 1-50]  [Sig: pages 51-100]
  /        \           /        \
[p1-25]  [p26-50]  [p51-75]  [p76-100]

검색: 쿼리와 매칭되는 signature를 따라 내려감
-> False Positive 가능 -> Recheck 단계 필요
```

**전문 검색에서의 선택**:

| 워크로드 | GIN | GiST |
|---------|-----|------|
| 읽기 90% 쓰기 10% | 적합 (빠른 검색) | 과잉 |
| 읽기 50% 쓰기 50% | 빌드/업데이트 부담 | 적합 (빠른 업데이트) |
| 정확도 중요 | 정확 (False Positive 없음) | Recheck 필요 |
| 디스크 제약 | 크기 큼 | 크기 작음 |

**GIN의 Pending List 최적화**: GIN은 업데이트 시 모든 키의 포스팅 리스트를 갱신해야 하므로 느리다. 이를 완화하기 위해 pending list에 변경사항을 모아두었다가 일괄 적용하는 fastupdate 옵션이 있다. 단, pending list가 커지면 검색 시 추가 비용이 발생한다.

```sql
-- fastupdate 비활성화 (검색 성능 우선)
CREATE INDEX idx ON articles USING GIN(search_vector)
    WITH (fastupdate = off);
```

### 실무 적용

- 전문 검색: GIN이 기본 (읽기 위주 워크로드가 대부분)
- 실시간 로그 인덱싱 등 쓰기가 빈번한 경우: GiST 검토
- GIN fastupdate는 bulk insert 후 `GIN_CLEAN_PENDING_LIST` 실행

---

## Q3. 인덱스 블로트(Bloat)란 무엇이며, 어떻게 관리하는가?

### 왜 이 질문이 중요한가

운영 환경에서 인덱스는 시간이 지남에 따라 비대해진다(bloat). 인덱스 크기가 실제 데이터 대비 비정상적으로 크면 캐시 효율이 떨어지고 검색 성능이 저하된다. DBA 관점에서 인덱스 블로트 모니터링과 해결 방법을 아는 것이 중요하다.

### 답변

**블로트 발생 원인**:

B-tree 인덱스에서 행이 삭제되면 해당 인덱스 엔트리는 "사용 안 함" 표시만 되고 물리적으로 제거되지 않는다. VACUUM이 이 엔트리를 재활용 가능 상태로 만들지만, 페이지 자체를 OS에 반환하지는 않는다. 대량 DELETE 후에 인덱스 크기가 줄지 않는 이유가 이것이다.

```sql
-- 인덱스 블로트 추정 쿼리
SELECT
    schemaname || '.' || relname AS table_name,
    indexrelname AS index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- pgstattuple 확장으로 정확한 블로트 측정
CREATE EXTENSION pgstattuple;
SELECT * FROM pgstatindex('idx_orders_customer');
-- avg_leaf_density: 낮으면 블로트 심함 (90% 이상이 정상)
```

**블로트 해결 방법**:

| 방법 | 장점 | 단점 | 다운타임 |
|------|------|------|---------|
| REINDEX | 간단 | 테이블 락 발생 | 있음 |
| REINDEX CONCURRENTLY | 락 없음 | 임시 디스크 2배 | 없음 |
| CREATE INDEX CONCURRENTLY + DROP | 유연 | 수동 작업 | 없음 |

```sql
-- 프로덕션에서 안전한 방법
-- 1. 새 인덱스를 CONCURRENTLY로 생성
CREATE INDEX CONCURRENTLY idx_orders_customer_new
ON orders(customer_id);

-- 2. 기존 인덱스 삭제
DROP INDEX idx_orders_customer;

-- 3. 새 인덱스 이름 변경
ALTER INDEX idx_orders_customer_new RENAME TO idx_orders_customer;
```

PostgreSQL 12+에서는 `REINDEX CONCURRENTLY`가 도입되어 한 번에 처리할 수 있다.

### 실무 적용

- 월 1회 인덱스 크기 대비 테이블 크기 비율 모니터링
- avg_leaf_density가 50% 이하면 REINDEX 검토
- 대량 DELETE 작업 후 REINDEX CONCURRENTLY 실행
- Partial Index 활용으로 인덱스 크기 자체를 줄이는 것도 방법

---

## Q4. EXPLAIN 결과에서 Bitmap Index Scan은 언제 나타나며, 왜 Index Scan과 다른가?

### 왜 이 질문이 중요한가

EXPLAIN 결과를 해석할 때 Bitmap Index Scan이 나타나면 "인덱스를 쓰고 있으니 괜찮다"고 넘기기 쉽다. 하지만 Bitmap Scan은 Index Scan과 동작 방식이 다르며, 특정 상황에서 발생하는 이유를 이해해야 성능을 정확히 판단할 수 있다.

### 답변

**세 가지 인덱스 스캔 방식의 차이**:

```
Index Scan:
  인덱스에서 행 찾기 -> 즉시 Heap 접근 -> 다음 행 -> 즉시 Heap 접근
  특징: 랜덤 I/O, 소수의 행에서 효율적

Bitmap Index Scan:
  1단계: 인덱스에서 매칭 행의 위치를 비트맵에 기록
  2단계: 비트맵을 페이지 순서로 정렬
  3단계: 정렬된 순서로 Heap 접근 (Bitmap Heap Scan)
  특징: 순차 I/O에 가까움, 중간 선택도에서 효율적

Index Only Scan:
  인덱스에서 행 찾기 -> 인덱스에 모든 컬럼 있음 -> Heap 접근 불필요
  특징: 가장 빠름, Covering Index 필요
```

**Bitmap Scan이 선택되는 조건**: 쿼리 플래너는 반환할 행이 "너무 적지도 않고 너무 많지도 않은" 중간 범위일 때 Bitmap Scan을 선택한다. 소수의 행이면 Index Scan이, 대부분의 행이면 Seq Scan이 효율적이다.

```
선택도(selectivity)에 따른 스캔 방식:
0.1% 이하  -> Index Scan (소수 행, 랜덤 I/O 감수)
0.1% ~ 20% -> Bitmap Index Scan (비트맵으로 순차 I/O 변환)
20% 이상   -> Seq Scan (전체 읽기가 오히려 빠름)
```

**Bitmap Scan의 추가 장점**: 여러 인덱스의 결과를 BitmapAnd/BitmapOr로 결합할 수 있다.

```sql
-- 두 인덱스의 비트맵을 AND로 결합
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE status = 'active' AND region = 'asia';

-- Bitmap Heap Scan on orders
--   Recheck Cond: (status = 'active') AND (region = 'asia')
--   ->  BitmapAnd
--         ->  Bitmap Index Scan on idx_status
--         ->  Bitmap Index Scan on idx_region
```

이 경우 복합 인덱스 `(status, region)` 하나가 더 효율적이지만, 각 컬럼이 단독으로도 자주 사용된다면 단일 인덱스 2개 + BitmapAnd 조합이 더 유연하다.

### 실무 적용

- Bitmap Scan이 나타나면 반환 행의 비율을 확인. 5% 이하인데 Bitmap이면 인덱스 통계 갱신(ANALYZE) 검토
- BitmapAnd가 빈번하면 복합 인덱스 도입으로 한 단계 최적화 가능
- Bitmap Heap Scan의 "Recheck Cond"에서 "lossy" 표시가 있으면 work_mem 부족
