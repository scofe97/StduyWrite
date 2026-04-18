# Ch.07 - 모던 SQL

> **이론 매핑**: `docs/04_Database/04_PostgreSQL/03_모던_SQL.md`

---

## 핵심 요약

모던 SQL은 단순한 CRUD를 넘어 복잡한 분석 쿼리를 선언적으로 작성할 수 있게 해주는 기능들이다. CTE로 쿼리를 논리적 단위로 분리하고, 윈도우 함수로 원본 행을 유지하면서 집계 계산을 수행하며, 재귀 CTE로 계층 구조를 탐색할 수 있다. 이 기능들을 활용하면 애플리케이션 코드에서 처리하던 복잡한 로직을 SQL 한 문장으로 해결할 수 있다.

---

## 학습 목표

1. CTE(WITH 절)를 사용해 복잡한 쿼리를 논리적 단위로 분리하고 재사용할 수 있다
2. 재귀 CTE로 조직도, 카테고리 트리 등 계층 구조를 탐색할 수 있다
3. ROW_NUMBER, RANK, DENSE_RANK의 차이를 이해하고 상황에 맞게 선택할 수 있다
4. LAG/LEAD로 이전/다음 행을 참조하여 변화량을 계산할 수 있다
5. 윈도우 프레임(ROWS BETWEEN)을 지정하여 이동 평균 등을 구현할 수 있다
6. GROUP BY 집계와 윈도우 함수의 차이를 설명하고 적절히 선택할 수 있다

---

## 본문

### 1. CTE (Common Table Expression)

CTE는 WITH 절로 정의하는 이름 있는 임시 결과 집합이다. 서브쿼리와 비교했을 때 핵심 차이는 **재사용성**과 **가독성**에 있다.

```sql
-- 서브쿼리: monthly_sales를 두 번 사용하려면 두 번 작성해야 한다
SELECT * FROM (
    SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS total
    FROM orders GROUP BY 1
) sub
WHERE total > (
    SELECT AVG(total) FROM (
        SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS total
        FROM orders GROUP BY 1
    ) sub2
);

-- CTE: 한 번 정의하고 여러 번 참조한다
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS total
    FROM orders GROUP BY 1
)
SELECT * FROM monthly_sales
WHERE total > (SELECT AVG(total) FROM monthly_sales);
```

CTE의 장점을 정리하면 다음과 같다.

| 특성 | CTE | 서브쿼리 |
|------|-----|---------|
| 재사용 | 같은 쿼리에서 여러 번 참조 | 매번 재작성 |
| 가독성 | 쿼리 상단에 정의, 위에서 아래로 읽힘 | 중첩되어 안에서 바깥으로 읽힘 |
| 재귀 | WITH RECURSIVE 지원 | 불가능 |
| 디버깅 | 각 CTE를 독립적으로 실행 가능 | 전체 쿼리 필요 |

다중 CTE를 연결하면 복잡한 분석 파이프라인을 구성할 수 있다.

```sql
WITH
  monthly_orders AS (
    SELECT DATE_TRUNC('month', order_date) AS month,
           customer_id, SUM(amount) AS total
    FROM orders GROUP BY 1, 2
  ),
  customer_ranking AS (
    SELECT customer_id,
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

### 2. 재귀 CTE

재귀 CTE는 `WITH RECURSIVE`로 선언하며, Base Case와 Recursive Case로 구성된다. 계층 구조를 탐색할 때 필수적이다.

```
재귀 CTE 실행 흐름
┌─────────────────────────────────────────────────┐
│  WITH RECURSIVE cte AS (                         │
│      Base Case       -- Iteration 0: 시작 지점   │
│      UNION ALL                                   │
│      Recursive Case  -- Iteration 1, 2, 3...     │
│  )                                               │
│                                                  │
│  실행:                                           │
│  Iter 0: Base Case 실행 -> 루트 노드들           │
│  Iter 1: 루트의 자식들                           │
│  Iter 2: 자식의 자식들                           │
│  ...                                             │
│  종료: 새로운 행이 없으면 멈춤                    │
└─────────────────────────────────────────────────┘
```

조직도 탐색 예시를 보자.

```sql
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
SELECT depth, name, array_to_string(path, ' -> ') AS hierarchy
FROM org_tree
ORDER BY path;

-- 결과:
-- depth | name     | hierarchy
--   1   | CEO      | CEO
--   2   | CTO      | CEO -> CTO
--   3   | Dev Lead | CEO -> CTO -> Dev Lead
```

재귀 CTE의 주의점 두 가지가 있다.

첫째, **종료 조건이 없으면 무한 루프**에 빠진다. `WHERE n < 100` 같은 조건으로 깊이를 제한해야 한다.

둘째, 데이터에 **사이클**이 있으면 역시 무한 루프가 된다. 방문한 노드를 ARRAY로 추적하여 사이클을 감지할 수 있다.

```sql
-- 사이클 방지
WHERE NOT n.id = ANY(t.path_ids)  -- 이미 방문한 노드 제외
```

### 3. 윈도우 함수 기초

윈도우 함수는 GROUP BY와 달리 **원본 행을 유지하면서 집계 계산**을 수행한다. 이것이 핵심 차이다.

```
GROUP BY vs 윈도우 함수
┌────────────────────────────┬────────────────────────────┐
│ GROUP BY                   │ WINDOW OVER                │
│ 데이터: A: 100, 200, 300   │ 데이터: A: 100, 200, 300   │
│ 결과:   A: 600 (1행)       │ 결과:   A: 100 (sum: 600)  │
│                            │         A: 200 (sum: 600)  │
│ 행이 집약됨                │         A: 300 (sum: 600)  │
│                            │ 원본 행 유지 + 집계값 추가  │
└────────────────────────────┴────────────────────────────┘
```

윈도우 함수의 문법은 `function() OVER (PARTITION BY ... ORDER BY ...)` 형태다.

```sql
SELECT
    department,
    employee_name,
    salary,
    -- 부서별 합계 (원본 행 유지)
    SUM(salary) OVER (PARTITION BY department) AS dept_total,
    -- 부서별 평균
    AVG(salary) OVER (PARTITION BY department) AS dept_avg,
    -- 부서별 순위
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank_in_dept
FROM employees;
```

PARTITION BY는 데이터를 논리적 그룹으로 나누고, ORDER BY는 그 안에서의 처리 순서를 정한다.

| PARTITION BY | ORDER BY | 동작 |
|--------------|----------|------|
| 없음 | 없음 | 전체 테이블에 대해 계산 |
| 있음 | 없음 | 파티션별 전체 집계 |
| 없음 | 있음 | 전체에서 순서대로 누적 |
| 있음 | 있음 | 파티션별 순서대로 누적 |

### 4. 순위 함수: ROW_NUMBER vs RANK vs DENSE_RANK

세 함수 모두 순위를 매기지만 동일 값 처리 방식이 다르다. 데이터가 `[100, 100, 90, 80]`일 때:

```
ROW_NUMBER: 1, 2, 3, 4   -- 항상 연속 번호, 동일 값에도 다른 번호
RANK:       1, 1, 3, 4   -- 동일 값은 같은 순위, 다음 순위 건너뜀
DENSE_RANK: 1, 1, 2, 3   -- 동일 값은 같은 순위, 순위 연속
```

어떤 것을 선택할지는 비즈니스 요구사항에 달려 있다.

| 함수 | 사용 시나리오 | 예시 |
|------|-------------|------|
| ROW_NUMBER | 페이지네이션, 중복 제거 (동점 중 하나만 선택) | 검색 결과 10개씩 |
| RANK | 경쟁 순위 (공동 1등 2명이면 3등부터) | 시험 성적 순위 |
| DENSE_RANK | 등급 분류 (1등급 다음은 항상 2등급) | 급여 등급 분류 |

추가로 `NTILE(n)`은 데이터를 n개 그룹으로 균등 분할한다. 백분위 분석에 유용하다.

### 5. LAG/LEAD로 행 간 비교

LAG는 이전 행, LEAD는 다음 행의 값을 참조한다. 시계열 데이터에서 변화량 계산에 필수적이다.

```sql
SELECT
    order_date,
    amount,
    -- 전일 매출
    LAG(amount, 1) OVER (ORDER BY order_date) AS prev_amount,
    -- 전일 대비 증감
    amount - LAG(amount) OVER (ORDER BY order_date) AS diff,
    -- 전일 대비 증감률
    ROUND(
        (amount - LAG(amount) OVER (ORDER BY order_date))::numeric
        / NULLIF(LAG(amount) OVER (ORDER BY order_date), 0) * 100,
        2
    ) AS growth_pct
FROM daily_sales;
```

`LAG(column, offset, default)` 형태로, offset은 몇 행 이전인지(기본 1), default는 NULL일 때 대체값이다.

실무 활용 패턴은 다음과 같다.

- 전일/전월 대비 변화량 및 증감률
- 사용자 이벤트 간 시간 간격 (세션 분석)
- 상태 변경 감지 (주문 상태가 바뀐 시점 추적)
- 이상치 탐지 (급격한 값 변화 감지)

### 6. 윈도우 프레임

윈도우 프레임은 현재 행을 기준으로 함수가 참조하는 행의 범위를 지정한다. 이동 평균, 누적 합계 등에 쓰인다.

```sql
SELECT
    order_date,
    amount,
    -- 7일 이동 평균
    AVG(amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7,

    -- 누적 합계 (기본 프레임)
    SUM(amount) OVER (ORDER BY order_date) AS running_total,

    -- 전체 합계 (프레임을 전체로 확장)
    SUM(amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS total
FROM orders;
```

프레임 경계 옵션은 다음과 같다.

```
ROWS BETWEEN 경계 옵션:
  UNBOUNDED PRECEDING  -- 파티션 첫 행
  n PRECEDING          -- n행 전
  CURRENT ROW          -- 현재 행
  n FOLLOWING          -- n행 후
  UNBOUNDED FOLLOWING  -- 파티션 마지막 행
```

ROWS와 RANGE의 차이를 이해하는 것도 중요하다. ROWS는 물리적 행 수 기준이고, RANGE는 ORDER BY 컬럼 값 기준이다. 같은 날짜 데이터가 여러 행 있을 때 RANGE는 같은 값을 가진 행들을 모두 포함한다.

`LAST_VALUE`를 사용할 때 주의점이 있다. 기본 프레임은 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`이므로 LAST_VALUE가 현재 행을 반환한다. 파티션의 실제 마지막 값을 얻으려면 프레임을 명시적으로 `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`으로 지정해야 한다.

---

## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| CTE | WITH 절로 쿼리를 논리 단위로 분리, 같은 쿼리에서 여러 번 참조 가능 |
| 재귀 CTE | Base Case + Recursive Case로 계층 구조 탐색, 종료 조건 필수 |
| 윈도우 함수 | 원본 행 유지하면서 집계 계산, GROUP BY와 핵심 차이 |
| ROW_NUMBER | 항상 연속 번호, 페이지네이션에 적합 |
| RANK / DENSE_RANK | 동일 값 같은 순위, 건너뜀 여부가 차이 |
| LAG / LEAD | 이전/다음 행 값 참조, 시계열 변화량 계산에 필수 |
| 윈도우 프레임 | ROWS BETWEEN으로 참조 범위 지정, 이동 평균 구현 |
