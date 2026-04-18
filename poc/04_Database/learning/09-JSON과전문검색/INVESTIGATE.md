# Ch.09 - JSON과 전문 검색: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. JSONB와 정규화된 테이블의 성능 차이는 어느 정도이며, 어떤 기준으로 선택하는가?

### 왜 이 질문이 중요한가

"JSONB를 쓰면 NoSQL처럼 유연하게 쓸 수 있다"는 것은 사실이지만, 언제 JSONB가 적절하고 언제 정규화가 필요한지 판단하는 것이 실무에서 중요하다. 잘못된 선택은 쿼리 성능 저하, 데이터 무결성 문제, 유지보수 어려움으로 이어진다.

### 답변

**성능 비교**:

```sql
-- 시나리오: 100만 건 주문에서 특정 상품을 구매한 고객 찾기

-- 정규화된 구조
SELECT DISTINCT c.name
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
WHERE oi.product_id = 42;
-- 인덱스 활용: order_items(product_id), orders(customer_id)
-- 실행 시간: ~5ms

-- JSONB 구조 (items가 JSONB 배열)
SELECT DISTINCT data->>'customer_name'
FROM orders
WHERE data @> '{"items": [{"product_id": 42}]}';
-- GIN 인덱스 활용 가능하지만, 배열 내부 검색은 효율이 떨어짐
-- 실행 시간: ~50ms (10배 느림)
```

핵심 차이는 **JOIN 효율**이다. 정규화된 구조는 FK 인덱스를 타고 정확한 행만 읽지만, JSONB의 `@>` 연산은 문서 전체를 비교해야 한다.

**하이브리드 접근법이 실무 최적해**:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,          -- 자주 검색/JOIN -> 정규화
    price NUMERIC NOT NULL,      -- 집계 필요 -> 정규화
    category_id INT REFERENCES,  -- 관계 -> 정규화
    attributes JSONB             -- 유동적 속성 -> JSONB
);
```

**판단 기준 매트릭스**:

| 기준 | JSONB 적합 | 정규화 적합 |
|------|-----------|-----------|
| 스키마 | 유동적, 사전 정의 어려움 | 고정, 명확한 구조 |
| 쿼리 패턴 | 문서 단위 CRUD | JOIN, GROUP BY, 집계 |
| 무결성 | 느슨한 검증 허용 | 엄격한 제약조건 필요 |
| 인덱싱 | GIN으로 포함 검색 | B-tree로 정밀 검색 |
| 업데이트 | 전체 문서 재작성 | 특정 컬럼만 수정 |

### 실무 적용

- 사용자 정의 필드, 외부 API 응답, 설정/메타데이터 -> JSONB
- PK/FK 관계, 금액 집계, 리포팅 대상 데이터 -> 정규화
- 하이브리드: 핵심 속성은 컬럼, 부가 속성은 JSONB

---

## Q2. Elasticsearch vs PostgreSQL 전문 검색: 어디서 경계가 갈리는가?

### 왜 이 질문이 중요한가

"전문 검색이 필요하면 Elasticsearch를 도입해야 하는가?" 아키텍처 결정에서 자주 나오는 질문이다. PostgreSQL FTS로 충분한 범위와 Elasticsearch가 필요한 시점을 구분할 수 있어야 한다.

### 답변

**PostgreSQL FTS가 충분한 경우**:

- 문서 수 수백만 건 이하
- 검색 요구사항이 "키워드 매칭 + 랭킹" 수준
- 데이터가 이미 PostgreSQL에 있고 동기화 부담을 피하고 싶음
- 트랜잭션 일관성이 중요 (검색 결과와 최신 데이터 일치)

**Elasticsearch가 필요한 경우**:

- 문서 수 수천만~수억 건 이상
- 실시간 집계(Aggregation)가 복잡 (faceted search, nested aggregation)
- 다국어 분석기, 형태소 분석 등 고급 텍스트 처리 필요
- 검색 전용 인프라로 DB 부하 분리 필요

**벤치마크 비교** (일반적인 수치):

| 지표 | PostgreSQL FTS | Elasticsearch |
|------|---------------|---------------|
| 100만 문서 검색 | 5-50ms | 1-10ms |
| 인덱싱 속도 | 느림 (GIN 업데이트) | 빠름 (inverted index 최적화) |
| 집계/Facet | 기본 GROUP BY | 전용 Aggregation 엔진 |
| 한국어 지원 | 제한적 (사전 설정 필요) | nori 분석기 내장 |
| 운영 복잡도 | 낮음 (PostgreSQL 내장) | 높음 (별도 클러스터) |
| 일관성 | 강한 일관성 (ACID) | 최종 일관성 (near-realtime) |

**아키텍처 패턴**:

```
패턴 1: PostgreSQL만 사용 (단순)
App -> PostgreSQL (CRUD + FTS)

패턴 2: PostgreSQL + Elasticsearch (분리)
App -> PostgreSQL (CRUD, Source of Truth)
  └-> CDC/Sync -> Elasticsearch (검색 전용)

패턴 3: 점진적 전환
1단계: PostgreSQL FTS로 시작
2단계: 성능 한계에 도달하면 Elasticsearch 도입
3단계: PostgreSQL은 CRUD, Elasticsearch는 검색
```

### 실무 적용

- 프로젝트 초기에는 PostgreSQL FTS로 시작하고, 검색 요구사항이 복잡해지면 Elasticsearch를 도입하는 점진적 접근이 리스크가 작다
- Elasticsearch 도입 시 데이터 동기화 전략(CDC, 이벤트 기반)이 핵심 과제
- 한국어 전문 검색이 필수라면 Elasticsearch의 nori 분석기가 현실적 선택

---

## Q3. 한국어 전문 검색을 PostgreSQL에서 구현하려면 어떤 접근이 필요한가?

### 왜 이 질문이 중요한가

PostgreSQL의 내장 FTS는 영어 등 서양 언어에 최적화되어 있다. 한국어는 교착어로 형태소 분석이 필수인데, PostgreSQL에서 이를 어떻게 처리할 수 있는지, 한계는 무엇인지 알아야 한다.

### 답변

**한국어 FTS의 문제점**: 한국어는 공백으로 단어를 분리해도 조사가 붙어 있다. "데이터베이스를"에서 "데이터베이스"를 추출하려면 형태소 분석이 필요하다.

```sql
-- 영어: 어간 추출이 잘 동작
SELECT to_tsvector('english', 'The databases are running');
-- 'databas':2 'run':4

-- 한국어: simple 사전으로는 공백 분리만
SELECT to_tsvector('simple', '데이터베이스를 운영하는 방법');
-- '데이터베이스를':1 '운영하는':2 '방법':3
-- "데이터베이스"로 검색하면 매칭 안 됨!
```

**해결 방법 1: pg_bigm (2-gram 기반)**

```sql
CREATE EXTENSION pg_bigm;

-- 2글자 단위로 인덱싱
CREATE INDEX idx_content_bigm ON articles
    USING GIN(content gin_bigm_ops);

-- LIKE 검색이 인덱스를 활용
SELECT * FROM articles
WHERE content LIKE '%데이터베이스%';
```

pg_bigm은 형태소 분석 없이 부분 문자열 매칭을 지원한다. 설정이 간단하지만 "랭킹"이나 "어간 추출"은 불가능하다.

**해결 방법 2: 외부 형태소 분석기 연동**

mecab-ko 같은 한국어 형태소 분석기를 PostgreSQL과 연동하는 방법이 있다. textsearch_ko 같은 커뮤니티 확장을 사용하지만, 설치와 유지보수가 복잡하다.

**해결 방법 3: 애플리케이션 레벨 전처리**

```sql
-- 애플리케이션에서 형태소 분석 후 키워드를 별도 컬럼에 저장
-- Python: konlpy로 형태소 분석 -> 명사만 추출
-- 결과를 tsvector 컬럼에 저장
UPDATE articles SET search_vector =
    to_tsvector('simple', '데이터베이스 운영 방법');  -- 전처리된 키워드
```

| 방법 | 난이도 | 검색 품질 | 랭킹 | 유지보수 |
|------|-------|----------|------|---------|
| pg_bigm | 낮음 | 부분 매칭 | 불가 | 쉬움 |
| mecab-ko 연동 | 높음 | 형태소 기반 | 가능 | 어려움 |
| 앱 레벨 전처리 | 중간 | 선택적 | 가능 | 보통 |
| Elasticsearch nori | 중간 | 높음 | 가능 | 보통 |

### 실무 적용

- 단순 부분 매칭만 필요: pg_bigm으로 빠르게 해결
- 형태소 기반 검색 + 랭킹 필요: Elasticsearch nori가 현실적 선택
- PostgreSQL만 사용해야 하는 제약: 애플리케이션에서 형태소 분석 후 tsvector에 저장

---

## Q4. JSONB 데이터의 스키마 검증은 어떻게 하는가?

### 왜 이 질문이 중요한가

JSONB는 유연하지만 "아무 데이터나 들어갈 수 있다"는 것이 양날의 검이다. 프로덕션에서 JSONB 컬럼에 잘못된 구조의 데이터가 들어오면 애플리케이션 오류로 이어진다. DB 레벨에서 JSONB 스키마를 검증하는 방법을 알아야 한다.

### 답변

**방법 1: CHECK 제약조건**

```sql
-- 필수 키 존재 확인
ALTER TABLE products ADD CONSTRAINT valid_specs
CHECK (
    specs ? 'name'
    AND specs ? 'price'
    AND (specs->>'price')::numeric > 0
);

-- JSON Path 검증 (PostgreSQL 12+)
ALTER TABLE events ADD CONSTRAINT valid_event
CHECK (
    jsonb_path_exists(data, '$.type')
    AND jsonb_path_exists(data, '$.timestamp')
);
```

**방법 2: 트리거 기반 검증**

```sql
CREATE FUNCTION validate_product_specs() RETURNS trigger AS $$
BEGIN
    IF NOT (NEW.specs ? 'name') THEN
        RAISE EXCEPTION 'specs must contain "name" key';
    END IF;
    IF jsonb_typeof(NEW.specs->'tags') != 'array' THEN
        RAISE EXCEPTION 'specs.tags must be an array';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_specs
    BEFORE INSERT OR UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION validate_product_specs();
```

**방법 3: is_valid_json_schema (커뮤니티 확장)**

pg_jsonschema 확장을 사용하면 JSON Schema 표준으로 검증할 수 있다.

```sql
CREATE EXTENSION pg_jsonschema;

ALTER TABLE products ADD CONSTRAINT valid_specs
CHECK (
    json_matches_schema('{
        "type": "object",
        "required": ["name", "price"],
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number", "minimum": 0}
        }
    }', specs)
);
```

### 실무 적용

- 필수 키/타입 검증: CHECK 제약조건으로 간단히 구현
- 복잡한 스키마: pg_jsonschema 확장 또는 트리거 기반
- 클라우드 환경에서 확장 설치가 어려우면 애플리케이션 레벨 검증 + CHECK 최소 검증 조합
