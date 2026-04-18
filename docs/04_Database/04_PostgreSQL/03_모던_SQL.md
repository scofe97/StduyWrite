# Chapter 3: Modern SQL - 면접정리

## 핵심 개념 상세 설명

### 1. CTE (Common Table Expression)

```
CTE 구조와 장점
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  WITH cte_name AS (                                         │
│      -- 재사용 가능한 서브쿼리                               │
│      SELECT ...                                             │
│  )                                                          │
│  SELECT * FROM cte_name;                                    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                      CTE 장점                               │
│                                                             │
│  1. 가독성 향상                                              │
│     └─ 복잡한 쿼리를 논리적 단위로 분리                      │
│                                                             │
│  2. 재사용성                                                 │
│     └─ 같은 CTE를 메인 쿼리에서 여러 번 참조                 │
│                                                             │
│  3. 재귀 쿼리 지원                                           │
│     └─ WITH RECURSIVE로 계층 구조 탐색                      │
│                                                             │
│  4. 디버깅 용이                                              │
│     └─ 각 CTE를 독립적으로 테스트 가능                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- 다중 CTE 예시
WITH
  monthly_orders AS (
    SELECT
      DATE_TRUNC('month', order_date) AS month,
      customer_id,
      SUM(amount) AS total
    FROM orders
    GROUP BY 1, 2
  ),
  customer_ranking AS (
    SELECT
      customer_id,
      SUM(total) AS yearly_total,
      RANK() OVER (ORDER BY SUM(total) DESC) AS rank
    FROM monthly_orders
    GROUP BY customer_id
  )
SELECT c.name, cr.yearly_total, cr.rank
FROM customer_ranking cr
JOIN customers c ON cr.customer_id = c.id
WHERE cr.rank <= 10;
```

### 2. 재귀 CTE (Recursive CTE)

```
재귀 CTE 구조
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  WITH RECURSIVE cte_name AS (                               │
│      -- Base Case (Anchor Member)                           │
│      SELECT ... WHERE parent_id IS NULL                     │
│                                                             │
│      UNION ALL                                              │
│                                                             │
│      -- Recursive Case (Recursive Member)                   │
│      SELECT ... FROM cte_name                               │
│      JOIN table ON table.parent_id = cte_name.id            │
│  )                                                          │
│  SELECT * FROM cte_name;                                    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    실행 흐름                                │
│                                                             │
│  Iteration 0: Base Case 실행 → 루트 노드들                  │
│       ↓                                                     │
│  Iteration 1: Recursive Case (루트의 자식들)                │
│       ↓                                                     │
│  Iteration 2: Recursive Case (손자들)                       │
│       ↓                                                     │
│  ...                                                        │
│       ↓                                                     │
│  종료: 더 이상 새로운 행이 없을 때                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- 조직도 탐색 예시
WITH RECURSIVE org_tree AS (
    -- Base Case: 최상위 관리자
    SELECT id, name, manager_id, 1 AS depth,
           ARRAY[name] AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive Case: 부하 직원들
    SELECT e.id, e.name, e.manager_id, t.depth + 1,
           t.path || e.name
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT depth, name, array_to_string(path, ' → ') AS hierarchy
FROM org_tree
ORDER BY path;

-- 결과:
-- depth | name    | hierarchy
--   1   | CEO     | CEO
--   2   | CTO     | CEO → CTO
--   3   | Dev Lead| CEO → CTO → Dev Lead
```

### 3. 윈도우 함수 (Window Functions)

```
윈도우 함수 구조
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  function_name(args) OVER (                                 │
│      PARTITION BY column     -- 그룹 분할 (선택)            │
│      ORDER BY column         -- 정렬 (선택)                 │
│      ROWS/RANGE frame        -- 프레임 (선택)               │
│  )                                                          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                   GROUP BY vs OVER                          │
│                                                             │
│  GROUP BY                    │  WINDOW OVER                 │
│  ┌─────────────────────┐     │  ┌─────────────────────┐    │
│  │ A: 100, 200, 300    │     │  │ A: 100 (sum: 600)   │    │
│  │ → A: 600 (1행)      │     │  │ A: 200 (sum: 600)   │    │
│  └─────────────────────┘     │  │ A: 300 (sum: 600)   │    │
│  행이 집계됨                  │  └─────────────────────┘    │
│                              │  원본 행 유지 + 집계값       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- 윈도우 함수 활용 예시
SELECT
    department,
    employee_name,
    salary,

    -- 집계 함수
    SUM(salary) OVER (PARTITION BY department) AS dept_total,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg,

    -- 순위 함수
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,

    -- 비율 함수
    PERCENT_RANK() OVER (ORDER BY salary) AS pct_rank,
    NTILE(4) OVER (ORDER BY salary) AS quartile

FROM employees;
```

### 4. 순위 함수 비교

```
ROW_NUMBER vs RANK vs DENSE_RANK
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  데이터: [100, 100, 90, 80]                                 │
│                                                             │
│  ROW_NUMBER: 1, 2, 3, 4                                     │
│  ├─ 항상 연속된 번호                                        │
│  └─ 동일 값이어도 다른 번호                                 │
│                                                             │
│  RANK:       1, 1, 3, 4                                     │
│  ├─ 동일 값은 같은 순위                                     │
│  └─ 다음 순위는 건너뜀 (2 건너뜀)                           │
│                                                             │
│  DENSE_RANK: 1, 1, 2, 3                                     │
│  ├─ 동일 값은 같은 순위                                     │
│  └─ 다음 순위는 연속 (건너뛰지 않음)                        │
│                                                             │
│  선택 기준:                                                  │
│  • 페이지네이션 → ROW_NUMBER                                │
│  • 경쟁 순위 (1등이 2명이면 3등부터) → RANK                 │
│  • 등급 분류 (1등급, 2등급...) → DENSE_RANK                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5. 윈도우 프레임

```sql
-- 윈도우 프레임 지정
SELECT
    order_date,
    amount,

    -- 기본 프레임: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    SUM(amount) OVER (ORDER BY order_date) AS running_total,

    -- 이동 평균 (최근 3일)
    AVG(amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3,

    -- 전체 평균과 비교
    AVG(amount) OVER () AS overall_avg

FROM orders;
```

```
윈도우 프레임 옵션
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ROWS BETWEEN:                                              │
│  ├─ UNBOUNDED PRECEDING  ─ 파티션 첫 행                     │
│  ├─ n PRECEDING          ─ n행 전                          │
│  ├─ CURRENT ROW          ─ 현재 행                          │
│  ├─ n FOLLOWING          ─ n행 후                          │
│  └─ UNBOUNDED FOLLOWING  ─ 파티션 마지막 행                 │
│                                                             │
│  예시:                                                       │
│  ROWS BETWEEN 2 PRECEDING AND 1 FOLLOWING                   │
│  [이전2] [이전1] [현재] [다음1]                              │
│  ←───────── 프레임 범위 ──────────→                         │
│                                                             │
│  ROWS vs RANGE:                                              │
│  • ROWS: 물리적 행 기준                                     │
│  • RANGE: 값 기준 (ORDER BY 컬럼 값이 같으면 같이 포함)     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6. LAG/LEAD 함수

```sql
-- 이전/다음 행 값 참조
SELECT
    order_date,
    amount,
    LAG(amount, 1) OVER (ORDER BY order_date) AS prev_amount,
    LEAD(amount, 1) OVER (ORDER BY order_date) AS next_amount,

    -- 전일 대비 증감
    amount - LAG(amount) OVER (ORDER BY order_date) AS diff,

    -- 전일 대비 증감률
    ROUND(
        (amount - LAG(amount) OVER (ORDER BY order_date))::numeric
        / LAG(amount) OVER (ORDER BY order_date) * 100,
        2
    ) AS growth_pct

FROM daily_sales;
```

```
LAG/LEAD 사용 패턴
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  LAG(column, offset, default)                               │
│  ├─ offset: 몇 행 이전 (기본 1)                             │
│  └─ default: NULL일 때 대체값                               │
│                                                             │
│  활용 사례:                                                  │
│  ├─ 전일/전월 대비 변화량                                   │
│  ├─ 연속 이벤트 간 시간 간격                                │
│  ├─ 상태 변경 감지                                          │
│  └─ 이상치 탐지 (급격한 변화)                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7. FIRST_VALUE/LAST_VALUE

```sql
SELECT
    department,
    employee_name,
    salary,

    -- 부서 내 최고 연봉자
    FIRST_VALUE(employee_name) OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS top_earner,

    -- 부서 내 최저 연봉자 (프레임 주의!)
    LAST_VALUE(employee_name) OVER (
        PARTITION BY department
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_earner

FROM employees;
```

---

## 비교표

### 집계 함수 vs 윈도우 함수

| 구분 | 집계 함수 (GROUP BY) | 윈도우 함수 (OVER) |
|------|---------------------|-------------------|
| 결과 행 수 | 그룹당 1행 | 원본 행 유지 |
| 원본 데이터 | 접근 불가 | 접근 가능 |
| 사용 위치 | SELECT, HAVING | SELECT, ORDER BY |
| 그룹화 | GROUP BY 필수 | PARTITION BY 선택 |

### 순위 함수 비교

| 함수 | 동일 값 처리 | 순위 건너뜀 | 용도 |
|------|------------|------------|------|
| ROW_NUMBER | 다른 번호 부여 | 해당 없음 | 페이지네이션, 중복 제거 |
| RANK | 같은 순위 | 건너뜀 | 경쟁 순위 |
| DENSE_RANK | 같은 순위 | 안 건너뜀 | 등급 분류 |
| NTILE(n) | N개 그룹 분할 | 해당 없음 | 백분위, 분위수 |

---

## 면접 예상 질문 및 모범 답안

### Q1. CTE(Common Table Expression)란 무엇이고, 서브쿼리와의 차이점은?

**모범 답안:**

CTE는 WITH 절을 사용해 이름 있는 임시 결과 집합을 정의하는 기능입니다.

**서브쿼리와의 차이점:**

| 구분 | CTE | 서브쿼리 |
|------|-----|---------|
| 재사용 | 같은 쿼리에서 여러 번 참조 가능 | 매번 재작성 필요 |
| 가독성 | 쿼리 상단에 정의, 논리 흐름 명확 | 중첩되어 가독성 저하 |
| 재귀 | WITH RECURSIVE 지원 | 불가능 |
| 디버깅 | 독립 실행으로 테스트 용이 | 전체 쿼리 필요 |

```sql
-- CTE 활용
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', date) AS month, SUM(amount) AS total
    FROM orders GROUP BY 1
)
SELECT * FROM monthly_sales
WHERE total > (SELECT AVG(total) FROM monthly_sales);
-- monthly_sales를 두 번 사용
```

CTE는 복잡한 분석 쿼리에서 특히 유용하며, 쿼리 계획에서 인라인되거나 Materialized될 수 있습니다.

---

### Q2. 재귀 CTE를 사용하는 상황과 주의점을 설명해주세요.

**모범 답안:**

**사용 상황:**
1. **계층 구조 탐색**: 조직도, 카테고리 트리, BOM(자재 명세서)
2. **그래프 탐색**: 경로 찾기, 연결 관계 분석
3. **시퀀스 생성**: generate_series 대용

**주의점:**

1. **무한 루프 방지:**
```sql
WITH RECURSIVE cte AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM cte WHERE n < 100  -- 종료 조건 필수!
)
```

2. **사이클 감지:**
```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, ARRAY[id] AS path
    FROM nodes WHERE parent_id IS NULL
    UNION ALL
    SELECT n.id, n.parent_id, t.path || n.id
    FROM nodes n
    JOIN tree t ON n.parent_id = t.id
    WHERE NOT n.id = ANY(t.path)  -- 사이클 방지
)
```

3. **성능**: 대용량 데이터에서는 인덱스 활용과 깊이 제한 고려

---

### Q3. ROW_NUMBER, RANK, DENSE_RANK의 차이점을 설명해주세요.

**모범 답안:**

세 함수 모두 순위를 매기지만 동일 값 처리 방식이 다릅니다.

```sql
SELECT
    name, score,
    ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num,
    RANK() OVER (ORDER BY score DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM students;

-- score: 100, 100, 90, 80
-- row_num:  1,   2,  3,  4  (항상 연속)
-- rank:     1,   1,  3,  4  (동점은 같은 순위, 다음 건너뜀)
-- dense_rank: 1, 1,  2,  3  (동점은 같은 순위, 연속)
```

**사용 시나리오:**
- **ROW_NUMBER**: 페이지네이션, 중복 제거 (동점 중 하나만 선택)
- **RANK**: 경쟁 순위 (공동 1등 2명이면 3등부터)
- **DENSE_RANK**: 등급 분류 (1등급 다음은 항상 2등급)

---

### Q4. 윈도우 함수에서 PARTITION BY와 ORDER BY의 역할을 설명해주세요.

**모범 답안:**

**PARTITION BY:**
- 데이터를 논리적 그룹으로 분할
- 각 파티션 내에서 독립적으로 함수 계산
- GROUP BY와 유사하지만 행을 유지

**ORDER BY:**
- 파티션 내 행의 처리 순서 결정
- 순위 함수, 누적 계산에 영향
- 윈도우 프레임의 기준

```sql
SELECT
    department,
    employee,
    salary,
    -- 부서별 누적 합계
    SUM(salary) OVER (
        PARTITION BY department    -- 부서별로 분리
        ORDER BY hire_date         -- 입사일 순으로 누적
    ) AS running_total
FROM employees;
```

**조합에 따른 동작:**

| PARTITION BY | ORDER BY | 결과 |
|--------------|----------|------|
| 없음 | 없음 | 전체 테이블에 대해 계산 |
| 있음 | 없음 | 파티션별 전체 집계 |
| 없음 | 있음 | 전체에서 순서대로 누적 |
| 있음 | 있음 | 파티션별 순서대로 누적 |

---

### Q5. LAG와 LEAD 함수의 활용 사례를 설명해주세요.

**모범 답안:**

LAG는 이전 행, LEAD는 다음 행의 값을 참조합니다.

**활용 사례:**

1. **전일 대비 변화:**
```sql
SELECT
    date, sales,
    sales - LAG(sales) OVER (ORDER BY date) AS daily_change,
    ROUND((sales - LAG(sales) OVER (ORDER BY date))::numeric
          / LAG(sales) OVER (ORDER BY date) * 100, 2) AS growth_pct
FROM daily_sales;
```

2. **세션 분석 (이벤트 간 시간):**
```sql
SELECT
    user_id, event_time,
    event_time - LAG(event_time) OVER (
        PARTITION BY user_id ORDER BY event_time
    ) AS time_since_last
FROM user_events;
```

3. **상태 변경 감지:**
```sql
SELECT *
FROM (
    SELECT id, status,
           LAG(status) OVER (ORDER BY updated_at) AS prev_status
    FROM orders
) sub
WHERE status != prev_status;
```

---

### Q6. 윈도우 프레임(ROWS BETWEEN)은 어떤 상황에서 사용하나요?

**모범 답안:**

윈도우 프레임은 현재 행을 기준으로 함수가 참조하는 행의 범위를 지정합니다.

**주요 사용 사례:**

1. **이동 평균:**
```sql
AVG(value) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW  -- 7일 이동평균
)
```

2. **누적 합계와 전체 합계:**
```sql
-- 누적 합계 (기본)
SUM(amount) OVER (ORDER BY date)

-- 전체 합계
SUM(amount) OVER (
    ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

3. **LAST_VALUE 정확한 사용:**
```sql
-- 기본 프레임은 CURRENT ROW까지라 LAST_VALUE가 제대로 안 됨
LAST_VALUE(name) OVER (
    ORDER BY salary
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

**ROWS vs RANGE:**
- ROWS: 물리적 행 수 기준
- RANGE: ORDER BY 값 기준 (같은 값은 같은 그룹)

---

## 실무 체크리스트

```
□ 복잡한 서브쿼리는 CTE로 리팩토링 고려
□ 재귀 CTE 사용 시 종료 조건과 사이클 방지 확인
□ 윈도우 함수 vs GROUP BY 선택 기준 이해
□ 순위 함수 선택 (ROW_NUMBER/RANK/DENSE_RANK)
□ LAG/LEAD로 이전/다음 행 비교
□ 윈도우 프레임으로 이동 평균, 누적 계산
□ EXPLAIN으로 윈도우 함수 성능 확인
```

---

## 참고 자료

- [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL WITH Queries (CTE)](https://www.postgresql.org/docs/current/queries-with.html)
- 책 GitHub: https://github.com/dmagda/just-use-postgres-book
