# Ch.08 - 인덱스 실전

> **이론 매핑**: `docs/04_Database/04_PostgreSQL/04_인덱스.md`

---

## 핵심 요약

인덱스는 데이터 검색 속도를 O(N)에서 O(log N) 이하로 줄이는 자료 구조다. 하지만 공짜가 아니다. 인덱스가 추가될 때마다 INSERT/UPDATE/DELETE의 비용이 증가하고 디스크 공간을 소비한다. PostgreSQL은 B-tree, Hash, GIN, GiST, BRIN 등 다양한 인덱스 타입을 제공하며, Partial Index, Covering Index 같은 고급 전략으로 인덱스 효율을 극대화할 수 있다.

---

## 학습 목표

1. B-tree 인덱스의 구조와 지원 연산자를 설명할 수 있다
2. 복합 인덱스에서 컬럼 순서의 중요성(Leading Column 규칙)을 이해하고 적용할 수 있다
3. Covering Index(INCLUDE)와 Partial Index를 적절한 상황에서 활용할 수 있다
4. EXPLAIN ANALYZE 결과를 해석하여 인덱스 사용 여부와 성능을 판단할 수 있다
5. GIN, GiST, BRIN 인덱스의 용도를 구분하고 선택할 수 있다
6. 불필요한 인덱스를 식별하고 제거하는 방법을 알 수 있다

---

## 본문

### 1. B-tree 인덱스: PostgreSQL의 기본

B-tree(Balanced Tree)는 PostgreSQL에서 `CREATE INDEX`를 실행하면 기본으로 생성되는 인덱스 타입이다. 왜 기본값인가? 대부분의 쿼리 패턴(등호, 범위, 정렬)에 범용적으로 대응하기 때문이다.

```
B-tree 구조
         [Root: 50 | 100]
         /        |        \
   [10,20,30,40] [60,70,80,90] [110,120,130]
        |             |             |
   [Heap Tuples - 실제 데이터 위치 포인터]

특징:
- 시간복잡도: O(log N)
- 모든 Leaf 노드가 같은 깊이 (균형 유지)
- Leaf 노드 간 연결로 범위 검색 효율적
```

B-tree가 지원하는 연산자: `<`, `<=`, `=`, `>=`, `>`, `BETWEEN`, `IN`, `LIKE 'prefix%'`

`LIKE '%suffix'`는 B-tree로 최적화할 수 없다. 왜냐하면 B-tree는 값의 앞부분부터 정렬하므로 뒷부분 패턴 매칭은 인덱스를 활용할 수 없기 때문이다. 이런 경우 pg_trgm 확장의 GIN 인덱스를 검토해야 한다.

```sql
-- B-tree 인덱스 생성
CREATE INDEX idx_users_email ON users(email);

-- 정렬 방향 지정 (DESC 쿼리가 많을 때)
CREATE INDEX idx_orders_date_desc ON orders(order_date DESC);
```

### 2. Hash 인덱스

Hash 인덱스는 등호(`=`) 연산만 지원하는 대신 O(1) 시간복잡도를 가진다. UUID나 해시값처럼 등호 검색만 필요한 컬럼에 적합하다.

```sql
CREATE INDEX idx_users_uuid ON users USING hash(uuid);

-- Hash 인덱스 활용 가능
SELECT * FROM users WHERE uuid = 'abc-123';

-- Hash 인덱스 활용 불가 (범위 검색)
SELECT * FROM users WHERE created_at > '2025-01-01';  -- B-tree 필요
```

실무에서 Hash 인덱스를 선택하는 경우는 드물다. B-tree도 등호 연산에 충분히 빠르고, 범위 검색까지 커버하기 때문이다. Hash를 고려하는 시점은 인덱스 크기를 최소화해야 하면서 등호 검색만 사용하는 경우다.

### 3. 복합 인덱스와 Leading Column 규칙

복합 인덱스는 여러 컬럼을 하나의 인덱스로 묶는다. 여기서 **컬럼 순서가 성능을 결정**한다.

```
CREATE INDEX idx ON orders(customer_id, order_date);

인덱스 내부 정렬:
(customer_id=1, date=2025-01-01)
(customer_id=1, date=2025-01-02)
(customer_id=1, date=2025-01-03)
(customer_id=2, date=2025-01-01)  <-- customer_id 우선 정렬
(customer_id=2, date=2025-01-02)
```

Leading Column(첫 번째 컬럼)을 포함하지 않은 검색은 인덱스를 활용할 수 없다.

```sql
-- 인덱스 사용 가능
WHERE customer_id = 1                          -- 첫 컬럼만
WHERE customer_id = 1 AND order_date > '2025'  -- 모두 사용

-- 인덱스 사용 불가 -> Full Scan
WHERE order_date > '2025'                      -- 두 번째만
```

복합 인덱스 설계 원칙 세 가지:

1. **등호 조건 컬럼을 범위 조건 앞에** 배치한다. `(status, order_date)`가 `(order_date, status)`보다 `WHERE status = 'active' AND order_date > X`에서 효율적이다.
2. **선택도가 높은 컬럼을 앞에** 배치한다. 선택도란 해당 조건이 걸러내는 비율이다.
3. **자주 단독으로 사용되는 컬럼을 앞에** 배치한다. Leading Column만으로도 인덱스를 활용할 수 있기 때문이다.

### 4. Covering Index (INCLUDE)

일반 인덱스는 인덱스에서 키를 찾은 후 실제 테이블(Heap)에 접근해서 데이터를 읽는다. Covering Index는 인덱스 자체에 필요한 모든 컬럼을 포함시켜 **테이블 접근을 생략**한다.

```
일반 인덱스:    Index Scan -> Heap Fetch (테이블 접근)
Covering Index: Index Scan -> 완료! (Index-Only Scan)
```

```sql
-- INCLUDE로 조회 전용 컬럼 추가
CREATE INDEX idx_orders_covering ON orders(customer_id)
    INCLUDE (order_date, amount);

-- 이 쿼리는 Index-Only Scan 가능 (테이블 접근 불필요)
SELECT customer_id, order_date, amount
FROM orders
WHERE customer_id = 123;
```

INCLUDE 컬럼은 검색 조건으로 사용되지 않고 조회만 가능하다. 복합 인덱스 키와의 차이는 이 점이다. INCLUDE는 인덱스 트리 구조에 영향을 주지 않으므로 인덱스 크기와 유지 비용이 복합 키보다 작다.

### 5. Partial Index (부분 인덱스)

테이블의 전체가 아닌 일부 행만 인덱싱한다. 활성 데이터가 전체의 일부분일 때 인덱스 크기를 대폭 줄일 수 있다.

```sql
-- active 상태인 주문만 인덱싱 (전체의 10%라면 인덱스 90% 축소)
CREATE INDEX idx_active_orders ON orders(order_date)
    WHERE status = 'active';

-- 이 쿼리에서 인덱스 사용됨
SELECT * FROM orders
WHERE status = 'active' AND order_date > '2025-01-01';

-- 이 쿼리에서는 인덱스 사용 안 됨 (조건 불일치)
SELECT * FROM orders
WHERE status = 'completed' AND order_date > '2025-01-01';
```

Partial Index가 효과적인 상황:

- 특정 상태의 행만 자주 조회 (active/pending 등)
- NULL이 아닌 값만 검색 (`WHERE email IS NOT NULL`)
- 최근 데이터만 조회 (`WHERE created_at > '2024-01-01'`)

### 6. 함수 기반 인덱스 (Expression Index)

WHERE 절에서 컬럼에 함수를 적용하면 일반 인덱스를 사용할 수 없다. Expression Index는 함수 결과를 인덱싱한다.

```sql
-- 대소문자 무시 검색
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- 날짜 추출
CREATE INDEX idx_orders_month ON orders(DATE_TRUNC('month', order_date));
SELECT * FROM orders
WHERE DATE_TRUNC('month', order_date) = '2025-01-01';

-- JSONB 필드
CREATE INDEX idx_profile_city ON users((profile->>'city'));
SELECT * FROM users WHERE profile->>'city' = 'Seoul';
```

주의: **쿼리의 표현식이 인덱스 정의와 정확히 일치해야** 인덱스가 사용된다. `LOWER(email)` 인덱스는 `UPPER(email)` 쿼리에 사용되지 않는다.

### 7. EXPLAIN ANALYZE로 인덱스 효과 확인

인덱스를 추가한 후 실제로 사용되는지 반드시 확인해야 한다.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 123;
```

출력 해석의 핵심 포인트:

```
-- 인덱스 미사용 (Seq Scan)
Seq Scan on orders  (cost=0.00..1520.00 rows=100 width=120)
                    (actual time=0.023..15.234 rows=98 loops=1)
  Filter: (customer_id = 123)
  Rows Removed by Filter: 49902      <-- 5만 행 읽고 100개만 남김
  Buffers: shared hit=520

-- 인덱스 사용 (Index Scan)
Index Scan using idx_customer on orders
                    (cost=0.42..8.44 rows=100 width=120)
                    (actual time=0.028..0.156 rows=98 loops=1)
  Index Cond: (customer_id = 123)
  Buffers: shared hit=5              <-- 5블록만 읽음 (104배 감소)
```

| 스캔 타입 | 설명 | 효율 |
|----------|------|------|
| Seq Scan | 전체 테이블 순차 스캔 | 대형 테이블에서 느림 |
| Index Scan | 인덱스로 검색 후 테이블 접근 | 선택적 조회에 효율 |
| Index Only Scan | 인덱스만으로 완료 (Covering) | 가장 효율적 |
| Bitmap Index Scan | 비트맵으로 여러 행 수집 후 접근 | 중간 선택도에 적합 |

예상 rows와 실제 rows가 크게 다르면 `ANALYZE tablename;`으로 통계를 갱신해야 한다. 통계가 부정확하면 쿼리 플래너가 잘못된 실행 계획을 선택한다.

### 8. 인덱스를 만들지 말아야 하는 경우

인덱스를 추가하면 항상 좋은 것은 아니다. 오버인덱싱의 비용을 인식해야 한다.

인덱스를 피해야 하는 상황:

- **작은 테이블**: Full Scan이 오히려 빠르다. 인덱스 탐색 오버헤드가 직접 읽기보다 클 수 있다.
- **낮은 카디널리티**: boolean이나 status처럼 값의 종류가 적은 컬럼은 인덱스 효과가 작다 (단, Partial Index는 예외).
- **자주 갱신되는 컬럼**: 매 UPDATE마다 인덱스도 갱신되므로 쓰기 성능이 저하된다.
- **거의 조회하지 않는 컬럼**: 쓰기 비용만 증가한다.

사용되지 않는 인덱스를 정기적으로 확인하고 제거하는 것이 중요하다.

```sql
-- idx_scan = 0인 인덱스 찾기
SELECT indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### 9. 인덱스 타입 종합 비교

| 타입 | 시간복잡도 | 지원 연산 | 대표 용도 |
|------|-----------|----------|----------|
| B-tree | O(log N) | <, <=, =, >=, >, BETWEEN, LIKE 'prefix%' | 범용, 기본값 |
| Hash | O(1) | = | UUID 등 등호 전용 |
| GIN | O(log N) | 포함, 존재 | JSONB, 배열, 전문 검색 |
| GiST | O(log N) | 범위, 근접 | 지리공간, 범위 타입 |
| BRIN | O(1) | 범위 | 대용량 순차 데이터 (시계열) |

BRIN(Block Range INdex)은 테이블의 물리적 블록 범위별 최소/최대값만 저장한다. 시계열 데이터처럼 물리적 순서와 논리적 순서가 일치하는 대용량 테이블에서 인덱스 크기를 수백 배 줄일 수 있다.

---

## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| B-tree | 기본 인덱스, 등호+범위+정렬 지원, O(log N) |
| 복합 인덱스 | Leading Column 포함해야 활용 가능, 등호 앞 범위 뒤 배치 |
| Covering Index | INCLUDE로 테이블 접근 생략, Index-Only Scan 가능 |
| Partial Index | WHERE 조건으로 일부만 인덱싱, 크기 대폭 감소 |
| Expression Index | 함수 결과를 인덱싱, 쿼리 표현식과 정확히 일치 필요 |
| EXPLAIN ANALYZE | 실행 계획 확인, Buffers로 I/O 분석, 통계 갱신(ANALYZE) 중요 |
| 오버인덱싱 | 쓰기 성능 저하+스토리지 낭비, idx_scan=0 인덱스 정기 정리 |
