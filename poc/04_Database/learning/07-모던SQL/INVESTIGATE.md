# Ch.07 - 모던 SQL: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. 재귀 CTE는 실무에서 어떤 문제를 풀 수 있으며, 성능 한계는 어디인가?

### 왜 이 질문이 중요한가

재귀 CTE는 계층 구조 탐색의 표준 도구지만, 데이터 규모에 따라 성능 문제가 발생할 수 있다. 면접에서 "조직도를 SQL로 탐색하라"는 질문이 나오면 재귀 CTE로 답하되, 성능 한계까지 언급할 수 있어야 한다.

### 답변

**실무 활용 사례**:

1. **조직도/카테고리 트리**: 가장 일반적인 사용처다. 부모-자식 관계를 재귀적으로 탐색한다.

```sql
-- BOM(Bill of Materials): 제품의 부품 구성 탐색
WITH RECURSIVE bom AS (
    SELECT part_id, part_name, parent_id, quantity, 1 AS level
    FROM parts WHERE parent_id IS NULL AND part_id = 'PRODUCT-A'

    UNION ALL

    SELECT p.part_id, p.part_name, p.parent_id,
           p.quantity * b.quantity AS total_qty,
           b.level + 1
    FROM parts p
    JOIN bom b ON p.parent_id = b.part_id
)
SELECT * FROM bom ORDER BY level;
```

2. **경로 찾기**: 그래프에서 노드 간 경로를 탐색한다.

3. **날짜 생성**: generate_series의 대안으로 사용할 수 있다.

**성능 한계와 최적화**:

재귀 CTE의 성능은 **깊이 x 폭**에 비례하여 저하된다. PostgreSQL은 재귀 CTE의 중간 결과를 메모리에 유지하므로, 결과가 크면 디스크 스필이 발생한다.

```sql
-- 깊이 제한으로 성능 보호
WITH RECURSIVE tree AS (
    SELECT id, parent_id, 1 AS depth FROM nodes WHERE parent_id IS NULL
    UNION ALL
    SELECT n.id, n.parent_id, t.depth + 1
    FROM nodes n JOIN tree t ON n.parent_id = t.id
    WHERE t.depth < 20  -- 깊이 20 이상은 탐색하지 않음
)
SELECT * FROM tree;
```

**대안**: 만약 계층 데이터를 자주 조회하고 트리 구조가 자주 변경되지 않는다면, **ltree 확장**이나 **Materialized Path** 패턴이 더 효율적이다.

```sql
-- ltree 확장: 경로를 라벨로 저장
CREATE EXTENSION ltree;
-- path 컬럼: 'root.dept.team.member'
SELECT * FROM org WHERE path <@ 'root.engineering';
```

| 방식 | 조회 성능 | 수정 성능 | 적합 상황 |
|------|----------|----------|----------|
| 재귀 CTE | 느림 (재귀 실행) | 빠름 (행 하나 수정) | 트리가 자주 변경됨 |
| ltree | 빠름 (인덱스) | 보통 (경로 업데이트) | 읽기 위주, 경로 쿼리 |
| Materialized Path | 빠름 (LIKE) | 느림 (하위 경로 갱신) | 단순 계층, 읽기 위주 |
| Closure Table | 빠름 (JOIN) | 느림 (관계 테이블 갱신) | 복잡한 쿼리 필요 |

### 실무 적용

- 깊이 10 이하, 노드 수 만 단위 이하: 재귀 CTE로 충분
- 깊이 무제한, 노드 수 십만 이상: ltree 또는 Closure Table 검토
- 재귀 CTE 사용 시 반드시 깊이 제한과 사이클 방지를 포함

---

## Q2. 윈도우 함수의 성능 특성은 어떠하며, 대용량 데이터에서 주의점은 무엇인가?

### 왜 이 질문이 중요한가

윈도우 함수는 분석 쿼리에서 강력하지만, 전체 파티션 데이터를 메모리에 유지해야 하므로 대용량 데이터에서 성능 이슈가 발생할 수 있다. EXPLAIN 결과에서 Sort 노드의 비용을 해석하고, 인덱스로 정렬을 생략시키는 최적화를 이해해야 한다.

### 답변

**윈도우 함수의 실행 과정**:

```
1. FROM/WHERE 실행 -> 결과 집합 생성
2. PARTITION BY 기준으로 정렬 (Sort 노드)
3. 각 파티션 내에서 윈도우 함수 계산
4. SELECT 결과 반환
```

핵심 비용은 2단계의 **정렬**이다. PARTITION BY와 ORDER BY에 맞는 인덱스가 없으면 전체 데이터를 정렬해야 한다.

```sql
-- 정렬 비용이 큰 경우
EXPLAIN ANALYZE
SELECT department, employee, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC)
FROM employees;

-- Sort  (cost=100.00..120.00)  <-- 정렬 발생
--   Sort Key: department, salary DESC
```

**인덱스로 정렬 생략**:

```sql
-- 인덱스가 PARTITION BY + ORDER BY와 일치하면 Sort 생략
CREATE INDEX idx_emp_dept_salary
ON employees(department, salary DESC);

-- 실행 계획에서 Sort 노드 사라짐 -> Index Scan으로 대체
```

**NAMED WINDOW로 중복 제거**:

같은 OVER 절을 여러 번 반복하면 가독성이 떨어지고, PostgreSQL이 각각 독립적으로 정렬할 수 있다. WINDOW 절로 정의하면 한 번만 정렬한다.

```sql
SELECT
    department, salary,
    ROW_NUMBER() OVER w AS rn,
    SUM(salary) OVER w AS running_sum,
    AVG(salary) OVER w AS running_avg
FROM employees
WINDOW w AS (PARTITION BY department ORDER BY salary DESC);
```

**work_mem과의 관계**: 정렬 데이터가 work_mem을 초과하면 디스크에 임시 파일을 쓴다. 분석 쿼리가 느리면 work_mem 증가를 검토한다.

### 실무 적용

- 윈도우 함수 쿼리에서 Sort 노드 비용이 크면 PARTITION BY + ORDER BY에 맞는 인덱스 생성
- 같은 OVER 절 반복 시 WINDOW 절 사용
- 대용량 분석 쿼리 전용 연결에서 `SET work_mem = '256MB'`로 세션별 조정

---

## Q3. LATERAL JOIN은 무엇이며, 서브쿼리와 어떻게 다른가?

### 왜 이 질문이 중요한가

LATERAL JOIN은 모던 SQL에서 "각 행마다 다른 서브쿼리를 실행"할 수 있게 해주는 기능이다. Top-N per group, 시계열 데이터 분석 등에서 윈도우 함수보다 효율적인 경우가 있다.

### 답변

일반 서브쿼리는 외부 쿼리의 현재 행을 참조할 수 없다. LATERAL은 이 제약을 해제한다.

```sql
-- 일반 JOIN: 서브쿼리가 독립적 (외부 행 참조 불가)
SELECT * FROM departments d
JOIN (SELECT * FROM employees LIMIT 3) e ON e.dept_id = d.id;
-- LIMIT 3은 전체에서 3개, 부서별 3개가 아님

-- LATERAL JOIN: 각 행마다 서브쿼리 실행
SELECT d.name, e.*
FROM departments d
CROSS JOIN LATERAL (
    SELECT * FROM employees
    WHERE dept_id = d.id
    ORDER BY salary DESC
    LIMIT 3
) e;
-- 부서별 상위 3명을 정확히 가져옴
```

**LATERAL vs 윈도우 함수 비교 (Top-N per group)**:

```sql
-- 방법 1: 윈도우 함수 (전체 정렬 후 필터)
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
    FROM employees
) sub WHERE rn <= 3;

-- 방법 2: LATERAL (인덱스 활용 가능)
SELECT d.name, e.*
FROM departments d
CROSS JOIN LATERAL (
    SELECT * FROM employees
    WHERE dept_id = d.id
    ORDER BY salary DESC LIMIT 3
) e;
```

LATERAL은 `employees(dept_id, salary DESC)` 인덱스가 있으면 각 부서별로 인덱스 스캔으로 3건만 읽는다. 윈도우 함수는 전체 employees를 정렬한 후 필터링하므로, 부서 수가 적고 직원이 많을 때 LATERAL이 효율적이다.

**LATERAL의 다른 활용**:

```sql
-- 시계열: 각 센서의 최근 5개 측정값
SELECT s.name, m.*
FROM sensors s
CROSS JOIN LATERAL (
    SELECT * FROM measurements
    WHERE sensor_id = s.id
    ORDER BY measured_at DESC LIMIT 5
) m;

-- JSON 배열 언래핑
SELECT o.id, item->>'name' AS item_name
FROM orders o
CROSS JOIN LATERAL jsonb_array_elements(o.items) AS item;
```

### 실무 적용

- Top-N per group: 그룹 수가 적고 데이터가 많으면 LATERAL + 인덱스가 유리
- JSON 배열 처리: `CROSS JOIN LATERAL jsonb_array_elements()`가 표준 패턴
- LATERAL은 인덱스 활용 여부가 성능을 결정하므로 EXPLAIN 확인 필수

---

## Q4. GROUPING SETS, CUBE, ROLLUP은 어떤 분석 시나리오에서 유용한가?

### 왜 이 질문이 중요한가

다차원 분석(OLAP) 쿼리에서 여러 수준의 집계를 한 번에 수행할 수 있다. 리포트나 대시보드를 구현할 때 여러 GROUP BY 쿼리를 UNION ALL로 합치는 대신 하나의 쿼리로 해결할 수 있다.

### 답변

```sql
-- UNION ALL로 3번 쿼리 (비효율)
SELECT department, NULL AS year, SUM(salary) FROM employees GROUP BY department
UNION ALL
SELECT NULL, EXTRACT(YEAR FROM hire_date), SUM(salary) FROM employees GROUP BY 2
UNION ALL
SELECT NULL, NULL, SUM(salary) FROM employees;

-- GROUPING SETS로 1번 쿼리 (효율)
SELECT department, EXTRACT(YEAR FROM hire_date) AS year, SUM(salary)
FROM employees
GROUP BY GROUPING SETS (
    (department),
    (EXTRACT(YEAR FROM hire_date)),
    ()  -- 전체 합계
);
```

**ROLLUP**: 계층적 집계 (소계 + 총계)

```sql
-- 지역 > 부서 > 팀 순서로 소계
SELECT region, department, team, SUM(revenue)
FROM sales
GROUP BY ROLLUP(region, department, team);
-- 결과: 팀별 + 부서별 소계 + 지역별 소계 + 총계
```

**CUBE**: 모든 조합의 집계

```sql
SELECT region, product, SUM(revenue)
FROM sales
GROUP BY CUBE(region, product);
-- 결과: (region, product), (region), (product), () 모든 조합
```

`GROUPING()` 함수로 NULL이 데이터의 NULL인지 집계 수준의 NULL인지 구분할 수 있다.

```sql
SELECT
    CASE WHEN GROUPING(department) = 1 THEN '전체' ELSE department END AS dept,
    SUM(salary)
FROM employees
GROUP BY ROLLUP(department);
```

### 실무 적용

- 대시보드의 소계/총계를 서버 사이드에서 한 번에 계산할 때
- 피벗 테이블 스타일 리포트 생성 시
- 여러 차원의 집계를 UNION ALL 대신 단일 쿼리로 처리
