# Chapter 5: Postgres and JSON - 면접정리

## 핵심 개념 상세 설명

### 1. PostgreSQL의 JSON 지원

```
PostgreSQL JSON 데이터 저장 옵션
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  【 TEXT 】                                                  │
│  • 단순 문자열 저장                                         │
│  • JSON 유효성 검사 없음                                    │
│  • JSON 연산자 사용 불가                                    │
│                                                             │
│  【 JSON 】                                                  │
│  • JSON 유효성 검사                                         │
│  • 원본 그대로 저장 (공백, 키 순서 보존)                    │
│  • 매 접근마다 파싱 필요                                    │
│  • 인덱싱 불가                                              │
│                                                             │
│  【 JSONB 】 ⭐ 권장                                         │
│  • 바이너리 형식으로 저장                                   │
│  • 사전 파싱으로 빠른 접근                                  │
│  • GIN 인덱스 지원                                          │
│  • 공백 제거, 키 순서 변경될 수 있음                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. JSON vs JSONB 비교

```
저장 및 처리 비교
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  입력: {"b": 1, "a": 2}                                     │
│                                                             │
│  JSON 저장: {"b": 1, "a": 2}   ← 원본 그대로                │
│  JSONB 저장: {"a": 2, "b": 1}  ← 키 정렬, 바이너리          │
│                                                             │
│  처리 흐름:                                                  │
│                                                             │
│  JSON:                                                       │
│  INSERT → 유효성 검사 → 문자열 저장                         │
│  SELECT → 문자열 읽기 → 파싱 → 결과                         │
│                                                             │
│  JSONB:                                                      │
│  INSERT → 유효성 검사 → 파싱 → 바이너리 저장                │
│  SELECT → 바이너리 읽기 → 결과 (파싱 불필요!)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. JSONB 연산자

```
JSONB 접근 연산자
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  샘플 데이터:                                                │
│  {"name": "John", "address": {"city": "Seoul"}, "age": 30}  │
│                                                             │
│  【 -> 】 JSONB 반환                                        │
│  data->'name'           → "John" (JSONB 타입)               │
│  data->'address'->'city'→ "Seoul" (JSONB 타입)              │
│                                                             │
│  【 ->> 】 TEXT 반환                                        │
│  data->>'name'          → John (TEXT 타입, 따옴표 없음)     │
│  data->'address'->>'city'→ Seoul (TEXT 타입)                │
│                                                             │
│  【 #> 】 경로로 JSONB 반환                                 │
│  data#>'{address,city}' → "Seoul" (JSONB)                   │
│                                                             │
│  【 #>> 】 경로로 TEXT 반환                                 │
│  data#>>'{address,city}'→ Seoul (TEXT)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- 실제 사용 예시
SELECT
    order_data->>'customer_name' AS customer,     -- TEXT
    (order_data->>'amount')::numeric AS amount,   -- 형변환 필요
    order_data->'items'->0->>'name' AS first_item -- 배열 접근
FROM orders;

-- WHERE 절에서 사용
SELECT * FROM products
WHERE specs->>'color' = 'blue'
  AND (specs->>'price')::numeric < 100;
```

### 4. JSONB 검색 연산자

```
포함/존재 연산자
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  【 ? 】 키 존재 확인                                       │
│  data ? 'email'          키 'email'이 존재하는가?           │
│                                                             │
│  【 ?| 】 키 중 하나라도 존재 (OR)                          │
│  data ?| array['a','b']  'a' 또는 'b' 존재하는가?           │
│                                                             │
│  【 ?& 】 모든 키 존재 (AND)                                │
│  data ?& array['a','b']  'a' 와 'b' 모두 존재하는가?        │
│                                                             │
│  【 @> 】 포함 (왼쪽이 오른쪽을 포함)                       │
│  data @> '{"status":"active"}'                              │
│  data가 {"status":"active"}를 포함하는가?                   │
│                                                             │
│  【 <@ 】 포함됨 (오른쪽이 왼쪽을 포함)                     │
│  '{"a":1}' <@ data                                          │
│  {"a":1}이 data에 포함되는가?                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- 실제 쿼리 예시
-- 특정 태그를 가진 문서 찾기
SELECT * FROM documents
WHERE metadata @> '{"tags": ["important"]}';

-- 필수 필드가 모두 있는 레코드
SELECT * FROM profiles
WHERE data ?& array['email', 'phone', 'address'];

-- 특정 상태의 문서
SELECT * FROM orders
WHERE data @> '{"status": "pending"}';
```

### 5. JSONB 수정 함수

```sql
-- jsonb_set: 값 설정/수정
UPDATE products SET
    specs = jsonb_set(specs, '{price}', '99.99')
WHERE id = 1;

-- 중첩 경로 설정
UPDATE products SET
    specs = jsonb_set(specs, '{dimensions,height}', '10')
WHERE id = 1;

-- || 연산자: 병합
UPDATE products SET
    specs = specs || '{"new_field": "value"}'
WHERE id = 1;

-- - 연산자: 키 제거
UPDATE products SET
    specs = specs - 'old_field'
WHERE id = 1;

-- #- 연산자: 경로로 제거
UPDATE products SET
    specs = specs #- '{dimensions,depth}'
WHERE id = 1;
```

```
JSONB 수정 패턴
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  원본: {"a": 1, "b": {"c": 2}}                              │
│                                                             │
│  jsonb_set(data, '{b,c}', '3')                              │
│  결과: {"a": 1, "b": {"c": 3}}                              │
│                                                             │
│  data || '{"d": 4}'                                         │
│  결과: {"a": 1, "b": {"c": 2}, "d": 4}                      │
│                                                             │
│  data - 'a'                                                 │
│  결과: {"b": {"c": 2}}                                      │
│                                                             │
│  create_if_missing 파라미터:                                │
│  jsonb_set(data, '{new,path}', '"value"', true)             │
│  → 경로가 없어도 생성                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6. JSONB 인덱싱

```
GIN 인덱스 옵션
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  【 jsonb_ops 】 기본값                                     │
│  CREATE INDEX idx ON table USING GIN(data);                 │
│                                                             │
│  지원 연산자: ?, ?|, ?&, @>, <@                             │
│  특징:                                                       │
│  • 모든 키와 값 인덱싱                                      │
│  • 키 존재 검사 (?) 지원                                    │
│  • 인덱스 크기 더 큼                                        │
│                                                             │
│  【 jsonb_path_ops 】                                       │
│  CREATE INDEX idx ON table USING GIN(data jsonb_path_ops);  │
│                                                             │
│  지원 연산자: @> (포함 연산만!)                             │
│  특징:                                                       │
│  • 경로-값 쌍만 인덱싱                                      │
│  • 인덱스 크기 더 작음 (2-3배)                              │
│  • @> 연산에 더 빠름                                        │
│  • ? 연산자 지원 안 함!                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- jsonb_ops (기본)
CREATE INDEX idx_data_gin ON products USING GIN(data);

-- 이 쿼리들 모두 인덱스 사용 가능
SELECT * FROM products WHERE data ? 'color';
SELECT * FROM products WHERE data @> '{"status": "active"}';

-- jsonb_path_ops
CREATE INDEX idx_data_path ON products USING GIN(data jsonb_path_ops);

-- 이 쿼리만 인덱스 사용 가능
SELECT * FROM products WHERE data @> '{"status": "active"}';

-- 이 쿼리는 인덱스 사용 불가!
SELECT * FROM products WHERE data ? 'color';  -- Seq Scan
```

### 7. JSON Path

```sql
-- JSON Path 기본 문법
-- $: 루트
-- .: 객체 멤버 접근
-- []: 배열 인덱스

SELECT jsonb_path_query(
    '{"store": {"book": [{"title": "A"}, {"title": "B"}]}}',
    '$.store.book[*].title'
);
-- 결과: "A", "B"

-- 조건부 필터링
SELECT jsonb_path_query(
    '[{"name": "A", "price": 10}, {"name": "B", "price": 20}]',
    '$[*] ? (@.price > 15)'
);
-- 결과: {"name": "B", "price": 20}

-- 실제 테이블에서 사용
SELECT * FROM orders
WHERE jsonb_path_exists(
    data,
    '$.items[*] ? (@.quantity > 5)'
);
```

---

## 비교표

### JSON vs JSONB

| 구분 | JSON | JSONB |
|------|------|-------|
| 저장 형식 | 텍스트 | 바이너리 |
| 입력 속도 | 빠름 | 느림 (파싱) |
| 처리 속도 | 느림 (매번 파싱) | 빠름 |
| 인덱싱 | 불가 | GIN 지원 |
| 원본 보존 | 공백, 키 순서 유지 | 변경될 수 있음 |
| 중복 키 | 모두 유지 | 마지막 값만 |
| 권장 용도 | 로그, 감사 | 일반적인 사용 |

### GIN 인덱스 옵션 비교

| 옵션 | jsonb_ops | jsonb_path_ops |
|------|-----------|----------------|
| 인덱스 크기 | 큼 | 작음 (2-3배) |
| ?, ?|, ?& | 지원 | 미지원 |
| @>, <@ | 지원 | 지원 |
| 사용 시점 | 키 존재 검사 필요 | 포함 검사만 필요 |

---

## 면접 예상 질문 및 모범 답안

### Q1. JSON과 JSONB의 차이점과 각각의 사용 시나리오를 설명해주세요.

**모범 답안:**

**저장 방식:**
- JSON: 텍스트 그대로 저장 (공백, 키 순서 보존)
- JSONB: 바이너리로 변환하여 저장

**성능 특성:**
- JSON: 입력 빠름, 조회 느림 (매번 파싱)
- JSONB: 입력 느림, 조회 빠름 (사전 파싱됨)

**기능 차이:**
- JSON: 인덱싱 불가, 원본 보존 필요 시
- JSONB: GIN 인덱스 지원, 연산자 최적화

**사용 시나리오:**

```sql
-- JSONB (일반적인 권장)
-- 검색, 필터링, 인덱싱이 필요한 경우
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    data JSONB
);

-- JSON (특수 케이스)
-- 원본 보존이 중요한 감사 로그
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    raw_request JSON  -- API 요청 원본 보존
);
```

대부분의 경우 JSONB를 사용하며, 원본 형식 보존이 필수인 경우에만 JSON을 사용합니다.

---

### Q2. JSONB의 -> 연산자와 ->> 연산자의 차이점은?

**모범 답안:**

두 연산자 모두 JSONB에서 값을 추출하지만, 반환 타입이 다릅니다.

**-> 연산자: JSONB 반환**
```sql
SELECT data->'name' FROM users;
-- 결과: "John" (JSONB, 따옴표 포함)

-- JSONB 타입이므로 추가 JSONB 연산 가능
SELECT data->'address'->'city' FROM users;
```

**->> 연산자: TEXT 반환**
```sql
SELECT data->>'name' FROM users;
-- 결과: John (TEXT, 따옴표 없음)

-- 문자열 함수 직접 사용 가능
SELECT UPPER(data->>'name') FROM users;
```

**실무 팁:**
```sql
-- 숫자 비교 시 형변환 필요
WHERE (data->>'price')::numeric > 100

-- 마지막 추출은 보통 ->>
WHERE data->'address'->>'city' = 'Seoul'
```

체이닝 시 중간은 ->, 마지막은 ->>를 사용하는 것이 일반적입니다.

---

### Q3. JSONB @> 연산자는 어떻게 동작하고, 언제 사용하나요?

**모범 답안:**

@>는 "포함(contains)" 연산자로, 왼쪽 JSONB가 오른쪽 JSONB를 포함하는지 확인합니다.

**동작 원리:**
```sql
-- 단순 키-값 매칭
'{"a": 1, "b": 2}' @> '{"a": 1}'  -- true

-- 중첩 구조도 매칭
'{"user": {"role": "admin"}}' @> '{"user": {"role": "admin"}}'  -- true

-- 배열은 순서 무관, 포함 여부만 확인
'{"tags": ["a", "b", "c"]}' @> '{"tags": ["a", "c"]}'  -- true
```

**GIN 인덱스와 함께 사용:**
```sql
CREATE INDEX idx_data ON products USING GIN(data);

-- 인덱스 활용 가능
SELECT * FROM products
WHERE data @> '{"category": "electronics", "in_stock": true}';
```

**사용 시나리오:**
1. 특정 속성을 가진 문서 필터링
2. 태그/카테고리 기반 검색
3. 중첩 조건 검색

---

### Q4. JSONB에 GIN 인덱스를 생성할 때 jsonb_ops와 jsonb_path_ops의 차이는?

**모범 답안:**

두 옵션은 인덱싱 방식과 지원 연산자가 다릅니다.

**jsonb_ops (기본값):**
```sql
CREATE INDEX idx ON table USING GIN(data);
```
- 모든 키와 값을 개별적으로 인덱싱
- ?, ?|, ?&, @>, <@ 모두 지원
- 인덱스 크기가 더 큼

**jsonb_path_ops:**
```sql
CREATE INDEX idx ON table USING GIN(data jsonb_path_ops);
```
- 경로-값 쌍을 해시하여 인덱싱
- @>만 지원 (포함 연산만)
- 인덱스 크기 2-3배 작음
- @> 연산 시 더 빠름

**선택 기준:**
```sql
-- 키 존재 확인이 필요하면 jsonb_ops
WHERE data ? 'email'  -- jsonb_ops 필요

-- 포함 검색만 하면 jsonb_path_ops
WHERE data @> '{"status": "active"}'  -- 둘 다 가능, path_ops가 효율적
```

---

### Q5. JSONB 데이터를 수정하는 방법들을 설명해주세요.

**모범 답안:**

JSONB는 불변(immutable)이므로 수정 시 새 값을 생성합니다.

**1. jsonb_set - 특정 경로 값 설정:**
```sql
UPDATE products SET
    data = jsonb_set(data, '{price}', '99.99')
WHERE id = 1;

-- 중첩 경로
data = jsonb_set(data, '{specs,weight}', '"10kg"')

-- 경로 없으면 생성 (create_if_missing=true)
data = jsonb_set(data, '{new_field}', '"value"', true)
```

**2. || 연산자 - 병합:**
```sql
UPDATE products SET
    data = data || '{"new_key": "value"}'
WHERE id = 1;
```

**3. - 연산자 - 키 제거:**
```sql
UPDATE products SET
    data = data - 'old_key'
WHERE id = 1;

-- 경로로 제거
data = data #- '{nested,key}'
```

**주의점:**
- 전체 JSONB를 다시 쓰므로 큰 문서는 비효율적
- 자주 수정되는 데이터는 정규화 고려

---

### Q6. 언제 JSONB를 사용하고, 언제 정규화된 테이블을 사용해야 하나요?

**모범 답안:**

**JSONB 적합한 경우:**

1. **스키마가 유동적:**
   - 사용자 정의 필드
   - 외부 API 응답 저장
   - 설정/메타데이터

2. **중첩 구조가 자연스러운 경우:**
   - 문서 기반 데이터
   - 계층적 속성

3. **조인이 거의 없는 경우:**
   - 독립적인 문서
   - 단일 쿼리로 완결

**정규화 테이블 적합한 경우:**

1. **관계가 중요:**
   - FK로 연결되는 데이터
   - 조인이 자주 필요

2. **집계/분석 쿼리:**
   - GROUP BY, SUM 등
   - 리포팅

3. **데이터 무결성 중요:**
   - 엄격한 스키마 필요
   - 제약조건 활용

**하이브리드 접근:**
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,           -- 정규화: 자주 검색
    price NUMERIC NOT NULL,       -- 정규화: 집계 필요
    category_id INT REFERENCES,   -- 정규화: 관계
    attributes JSONB              -- JSONB: 유동적 속성
);
```

---

## 실무 체크리스트

```
□ 일반적으로 JSON 대신 JSONB 사용
□ 자주 검색하는 JSONB 필드에 GIN 인덱스 추가
□ @> 연산만 사용하면 jsonb_path_ops 고려
□ ->> 사용 시 필요한 형변환 적용
□ 큰 JSONB 문서의 잦은 수정은 성능 고려
□ EXPLAIN으로 인덱스 사용 여부 확인
□ 관계형 모델과 JSONB의 적절한 조합 설계
```

---

## 참고 자료

- [PostgreSQL JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)
- [JSON Functions and Operators](https://www.postgresql.org/docs/current/functions-json.html)
- [GIN Indexes](https://www.postgresql.org/docs/current/gin.html)
- 책 GitHub: https://github.com/dmagda/just-use-postgres-book
