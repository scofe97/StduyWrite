# Ch.09 - JSON과 전문 검색

> **이론 매핑**: `docs/04_Database/04_PostgreSQL/05_JSON_처리.md` + `06_전문검색.md`

---

## 핵심 요약

PostgreSQL은 JSONB 타입으로 문서 데이터베이스의 유연성을, tsvector/tsquery 기반 전문 검색으로 검색 엔진의 기능을 하나의 DB 안에서 제공한다. JSONB는 바이너리 형식으로 저장되어 GIN 인덱스와 결합하면 빠른 검색이 가능하고, 전문 검색은 어간 추출, 불용어 제거, 가중치 기반 랭킹까지 지원한다. 별도의 MongoDB나 Elasticsearch를 도입하기 전에 PostgreSQL이 제공하는 기능으로 충분한지 검토할 가치가 있다.

---

## 학습 목표

1. JSON과 JSONB의 차이를 이해하고 JSONB를 기본으로 선택하는 이유를 설명할 수 있다
2. JSONB 접근 연산자(`->`, `->>`, `@>`, `?`)를 활용해 데이터를 조회하고 필터링할 수 있다
3. GIN 인덱스의 jsonb_ops와 jsonb_path_ops 차이를 이해하고 적절히 선택할 수 있다
4. tsvector/tsquery의 동작 원리(토큰화, 어간 추출, 불용어 제거)를 설명할 수 있다
5. setweight와 ts_rank로 가중치 기반 검색 랭킹을 구현할 수 있다
6. 저장된 tsvector 컬럼과 트리거를 활용한 검색 성능 최적화를 구현할 수 있다

---

## 본문

### 1. JSON vs JSONB: 왜 JSONB인가

PostgreSQL은 JSON과 JSONB 두 가지 JSON 타입을 제공한다. 결론부터 말하면, **대부분의 경우 JSONB를 사용해야 한다**.

```
저장/처리 비교
┌─────────────────────────────────────────────────┐
│  입력: {"b": 1, "a": 2}                         │
│                                                  │
│  JSON 저장:  {"b": 1, "a": 2}  <-- 원본 그대로  │
│  JSONB 저장: {"a": 2, "b": 1}  <-- 키 정렬됨    │
│                                                  │
│  JSON 조회:  문자열 읽기 -> 파싱 -> 결과         │
│  JSONB 조회: 바이너리 읽기 -> 결과 (파싱 불필요) │
└─────────────────────────────────────────────────┘
```

| 구분 | JSON | JSONB |
|------|------|-------|
| 저장 형식 | 텍스트 | 바이너리 |
| 입력 속도 | 빠름 | 느림 (파싱 후 저장) |
| 조회 속도 | 느림 (매번 파싱) | 빠름 |
| 인덱싱 | 불가 | GIN 인덱스 지원 |
| 원본 보존 | 공백, 키 순서 유지 | 변경될 수 있음 |
| 중복 키 | 모두 유지 | 마지막 값만 |

JSON을 선택하는 경우는 API 요청 원본을 그대로 보존해야 하는 감사 로그 정도다. 그 외에는 JSONB가 올바른 선택이다.

### 2. JSONB 연산자

JSONB에서 값을 추출하는 연산자는 반환 타입이 다르다. `->` 는 JSONB를, `->>`는 TEXT를 반환한다.

```sql
-- 샘플 데이터: {"name": "John", "address": {"city": "Seoul"}, "age": 30}

-- -> : JSONB 반환 (체이닝 가능)
data->'name'              -- "John" (JSONB, 따옴표 포함)
data->'address'->'city'   -- "Seoul" (JSONB)

-- ->> : TEXT 반환 (비교, 함수 사용 가능)
data->>'name'             -- John (TEXT, 따옴표 없음)
data->'address'->>'city'  -- Seoul (TEXT)
```

실무 패턴: **체이닝 중간은 `->`, 마지막 추출은 `->>`** 를 사용한다. 숫자 비교 시에는 형변환이 필요하다.

```sql
SELECT * FROM products
WHERE specs->>'color' = 'blue'
  AND (specs->>'price')::numeric < 100;

-- 배열 접근
SELECT order_data->'items'->0->>'name' AS first_item
FROM orders;
```

### 3. JSONB 검색 연산자

포함(`@>`) 및 존재(`?`) 연산자는 GIN 인덱스와 함께 사용될 때 빠른 검색을 제공한다.

```sql
-- @> : 포함 연산 (왼쪽이 오른쪽을 포함하는가?)
SELECT * FROM products
WHERE data @> '{"status": "active"}';

-- ? : 키 존재 확인
SELECT * FROM profiles
WHERE data ? 'email';

-- ?& : 모든 키 존재 (AND)
SELECT * FROM profiles
WHERE data ?& array['email', 'phone', 'address'];

-- ?| : 키 중 하나라도 존재 (OR)
SELECT * FROM profiles
WHERE data ?| array['email', 'phone'];
```

`@>` 연산자는 중첩 구조와 배열도 매칭한다. 배열의 경우 순서와 무관하게 포함 여부만 확인한다.

```sql
-- 배열 포함 매칭 (순서 무관)
'{"tags": ["a", "b", "c"]}' @> '{"tags": ["a", "c"]}'  -- true
```

### 4. JSONB 수정과 인덱싱

JSONB는 불변(immutable)이므로 수정 시 새 값을 생성한다.

```sql
-- jsonb_set: 특정 경로 값 설정
UPDATE products SET
    specs = jsonb_set(specs, '{price}', '99.99')
WHERE id = 1;

-- || 연산자: 병합 (새 키 추가)
UPDATE products SET
    specs = specs || '{"new_field": "value"}'
WHERE id = 1;

-- - 연산자: 키 제거
UPDATE products SET specs = specs - 'old_field' WHERE id = 1;

-- #- 연산자: 중첩 경로 제거
UPDATE products SET specs = specs #- '{dimensions,depth}' WHERE id = 1;
```

JSONB에 GIN 인덱스를 생성할 때 두 가지 옵션이 있다.

| 옵션 | 지원 연산자 | 인덱스 크기 | 선택 기준 |
|------|-----------|-----------|----------|
| `jsonb_ops` (기본) | ?, ?|, ?&, @>, <@ | 큼 | 키 존재 검사가 필요할 때 |
| `jsonb_path_ops` | @> 만 | 2-3배 작음 | 포함 검색만 할 때 |

```sql
-- jsonb_ops (기본): 모든 연산자 지원
CREATE INDEX idx_data_gin ON products USING GIN(data);

-- jsonb_path_ops: @> 전용, 크기 작음, @>에서 더 빠름
CREATE INDEX idx_data_path ON products USING GIN(data jsonb_path_ops);
```

`jsonb_path_ops`는 `?` 연산자를 지원하지 않으므로, `WHERE data ? 'email'` 같은 쿼리는 Seq Scan이 된다.

### 5. 전문 검색(FTS) 기초: tsvector와 tsquery

LIKE 검색의 한계는 명확하다. `WHERE content LIKE '%postgres%'`는 Full Table Scan을 유발하고, 어간 추출이 없어 'running'으로 'run'을 찾을 수 없다.

PostgreSQL의 전문 검색은 tsvector와 tsquery라는 두 가지 타입으로 동작한다.

```
tsvector 처리 과정 (to_tsvector)
┌─────────────────────────────────────────────────┐
│  입력: "The quick brown foxes jumped over lazy" │
│                                                  │
│  1. 토큰화:   The, quick, brown, foxes, ...     │
│  2. 소문자화: the, quick, brown, foxes, ...     │
│  3. 불용어 제거: the, over 제거                  │
│  4. 어간 추출: foxes->fox, jumped->jump         │
│  5. 위치 저장: 각 렉셈의 원본 위치 기록         │
│                                                  │
│  결과: 'brown':3 'fox':4 'jump':5 'lazi':7      │
│        'quick':2                                 │
└─────────────────────────────────────────────────┘
```

tsquery는 검색 조건을 표현하며, 논리 연산자를 지원한다.

```sql
-- 기본 검색 (@@ 연산자: 매칭 확인)
SELECT * FROM articles
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'database');

-- AND 조건
WHERE ... @@ to_tsquery('english', 'postgres & performance');

-- 인접 검색 (단어가 바로 옆에)
WHERE ... @@ to_tsquery('english', 'new <-> york');

-- N 단어 이내
WHERE ... @@ to_tsquery('english', 'quick <2> fox');
```

검색 편의 함수도 제공된다.

```sql
-- plainto_tsquery: 일반 텍스트 -> AND 조건
plainto_tsquery('english', 'fat cats')  -- 'fat' & 'cat'

-- phraseto_tsquery: 구문 검색
phraseto_tsquery('english', 'fat cats')  -- 'fat' <-> 'cat'

-- websearch_to_tsquery: 구글 스타일 검색 문법
websearch_to_tsquery('english', 'fat cats -dogs "new york"')
-- 'fat' & 'cat' & !'dog' & 'new' <-> 'york'
```

`websearch_to_tsquery`는 사용자 입력을 안전하게 처리하므로 SQL 인젝션 걱정이 없다. 검색 UI를 구현할 때 권장하는 함수다.

### 6. 검색 랭킹과 하이라이팅

검색 결과의 관련도 순위를 매기려면 ts_rank를 사용한다. setweight로 필드별 가중치를 적용하면 제목 매칭이 본문보다 높은 점수를 받도록 설정할 수 있다.

```sql
SELECT
    title,
    ts_rank(
        setweight(to_tsvector('english', title), 'A') ||
        setweight(to_tsvector('english', content), 'B'),
        to_tsquery('english', 'database')
    ) AS rank
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@
      to_tsquery('english', 'database')
ORDER BY rank DESC;
```

가중치 레벨: A(1.0) > B(0.4) > C(0.2) > D(0.1). 제목을 A, 본문을 D로 설정하면 제목 매칭이 10배 높은 점수를 받는다.

검색어 하이라이팅은 ts_headline으로 구현한다.

```sql
SELECT
    title,
    ts_headline('english', content,
        to_tsquery('english', 'postgres'),
        'StartSel=<b>, StopSel=</b>, MaxWords=35, MinWords=15'
    ) AS snippet
FROM articles
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'postgres');

-- 결과: "...using <b>Postgres</b> for full-text search provides..."
```

### 7. 검색 성능 최적화: 저장된 tsvector

매 쿼리마다 `to_tsvector()`를 호출하면 CPU 비용이 발생한다. 사전에 계산하여 별도 컬럼에 저장하면 성능이 크게 향상된다.

```sql
-- 1. tsvector 컬럼 추가
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- 2. 기존 데이터 채우기
UPDATE articles SET search_vector =
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(content, '')), 'B');

-- 3. 트리거로 자동 업데이트
CREATE FUNCTION update_search_vector() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.content, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_search_update
    BEFORE INSERT OR UPDATE ON articles
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- 4. GIN 인덱스 생성
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- 5. 검색 쿼리 (tsvector 계산 불필요)
SELECT * FROM articles
WHERE search_vector @@ to_tsquery('english', 'database');
```

GIN과 GiST 인덱스 선택:

| 구분 | GIN | GiST |
|------|-----|------|
| 검색 속도 | 빠름 | 상대적 느림 |
| 빌드/업데이트 | 느림 | 빠름 |
| 인덱스 크기 | 큼 | 작음 |
| 정확도 | 정확 | False Positive 가능 |
| 권장 | 읽기 위주 (기본) | 쓰기 많은 환경 |

대부분의 경우 GIN을 선택한다. 쓰기가 빈번한 환경에서만 GiST를 고려한다.

---

## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| JSONB | 바이너리 저장, GIN 인덱싱 가능, JSON 대신 기본 선택 |
| -> vs ->> | ->는 JSONB 반환 (체이닝), ->>는 TEXT 반환 (비교용) |
| @> 연산자 | 포함 검사, GIN 인덱스로 빠른 필터링 |
| jsonb_path_ops | @> 전용이지만 인덱스 크기 2-3배 작음 |
| tsvector | 문서를 검색 가능한 형태로 변환 (토큰화+어간추출+불용어 제거) |
| ts_rank + setweight | 필드별 가중치 적용한 관련도 순위 |
| 저장된 tsvector | 별도 컬럼에 사전 계산, 트리거로 자동 갱신, GIN 인덱스 필수 |
