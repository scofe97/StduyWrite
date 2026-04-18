# Chapter 8: Postgres for Generative AI - 면접정리

## 핵심 개념 상세 설명

### 1. 벡터 임베딩 개념

```
벡터 임베딩 (Vector Embedding)
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  【 개념 】                                                  │
│  텍스트, 이미지 등을 의미적 특성을 담은 숫자 배열로 변환    │
│                                                             │
│  "The cat sat on the mat"                                   │
│  ↓ Embedding Model (OpenAI, Cohere 등)                      │
│  [0.2, -0.5, 0.8, ..., 0.1]  (1536차원 벡터)               │
│                                                             │
│  【 특성 】                                                  │
│  • 의미가 유사한 텍스트는 벡터 공간에서 가까움              │
│  • 차원 수는 모델에 따라 다름 (256 ~ 4096)                  │
│  • 거리/유사도 계산으로 의미적 유사성 측정                  │
│                                                             │
│  【 활용 】                                                  │
│  • 시맨틱 검색 (의미 기반 검색)                             │
│  • 추천 시스템                                              │
│  • RAG (Retrieval-Augmented Generation)                    │
│  • 클러스터링                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. pgvector 확장

```sql
-- pgvector 설치
CREATE EXTENSION vector;

-- 벡터 컬럼이 있는 테이블 생성
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536)  -- OpenAI ada-002 차원
);

-- 벡터 데이터 삽입
INSERT INTO documents (content, embedding)
VALUES (
    'PostgreSQL is a powerful database',
    '[0.1, 0.2, -0.3, ...]'::vector
);
```

```
pgvector 데이터 타입
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  vector(n): n차원 벡터                                      │
│                                                             │
│  • vector(3): [1.0, 2.0, 3.0]                              │
│  • vector(1536): OpenAI text-embedding-ada-002             │
│  • vector(384): sentence-transformers/all-MiniLM-L6-v2     │
│                                                             │
│  최대 차원: 16,000 (기본)                                   │
│                                                             │
│  저장 크기: 4 bytes × 차원 수 + 8 bytes 오버헤드            │
│  예: 1536차원 = 6,152 bytes ≈ 6KB per row                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. 거리 함수

```
거리/유사도 연산자
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  【 L2 Distance (유클리드 거리) 】 <->                       │
│  √Σ(ai - bi)²                                              │
│  • 값이 작을수록 유사                                       │
│  • 범위: 0 ~ ∞                                              │
│                                                             │
│  【 Inner Product (내적) 】 <#>                              │
│  -Σ(ai × bi)  (음수로 반환)                                 │
│  • 값이 작을수록(음수가 클수록) 유사                        │
│  • 정규화된 벡터에서 코사인 유사도와 동일                   │
│                                                             │
│  【 Cosine Distance 】 <=>                                   │
│  1 - (Σ(ai × bi) / (|a| × |b|))                            │
│  • 값이 작을수록 유사                                       │
│  • 범위: 0 ~ 2                                              │
│  • 방향만 고려 (크기 무관)                                  │
│                                                             │
│  권장: 대부분의 경우 Cosine Distance (<=>)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- 유사 문서 검색
SELECT
    content,
    embedding <=> query_embedding AS distance
FROM documents
ORDER BY embedding <=> query_embedding
LIMIT 5;

-- 특정 거리 이내 검색
SELECT * FROM documents
WHERE embedding <=> query_embedding < 0.5;
```

### 4. 벡터 인덱스

```
IVFFlat vs HNSW 비교
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  【 IVFFlat (Inverted File with Flat) 】                    │
│                                                             │
│  구조:                                                       │
│  ┌───────────────────────────────────────┐                  │
│  │  Cluster 1: [v1, v5, v12, ...]        │                  │
│  │  Cluster 2: [v2, v8, v15, ...]        │                  │
│  │  Cluster 3: [v3, v7, v20, ...]        │                  │
│  │  ...                                  │                  │
│  └───────────────────────────────────────┘                  │
│                                                             │
│  • K-means로 클러스터링                                     │
│  • 검색 시 가까운 클러스터만 탐색                           │
│  • 빌드 빠름, 메모리 적음                                   │
│  • 정확도는 probes 수에 의존                                │
│                                                             │
│  파라미터:                                                   │
│  • lists: 클러스터 수 (√rows 권장)                          │
│  • probes: 검색할 클러스터 수 (√lists 권장)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  【 HNSW (Hierarchical Navigable Small World) 】            │
│                                                             │
│  구조:                                                       │
│  Layer 2: [v1] -------- [v50]                              │
│              \          /                                   │
│  Layer 1: [v1] -- [v20] -- [v50] -- [v80]                  │
│              \    /    \    /    \                          │
│  Layer 0: 모든 벡터가 연결됨 (밀집)                         │
│                                                             │
│  • 그래프 기반 탐색                                         │
│  • 빌드 느림, 메모리 많음                                   │
│  • 검색 빠름, 정확도 높음                                   │
│                                                             │
│  파라미터:                                                   │
│  • m: 연결 수 (16 기본)                                     │
│  • ef_construction: 빌드 시 탐색 범위 (64 기본)             │
│  • ef_search: 검색 시 탐색 범위 (40 기본)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- IVFFlat 인덱스 생성
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 검색 시 probes 설정
SET ivfflat.probes = 10;

-- HNSW 인덱스 생성
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 검색 시 ef_search 설정
SET hnsw.ef_search = 40;
```

### 5. 인덱스 선택 가이드

```
인덱스 선택 기준
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  데이터 크기?                                               │
│  ├─ < 10만 행: 인덱스 없이도 가능                          │
│  └─ > 10만 행: 인덱스 필요                                 │
│                                                             │
│  업데이트 빈도?                                             │
│  ├─ 자주 업데이트: IVFFlat (빌드 빠름)                     │
│  └─ 거의 안 함: HNSW (검색 성능 우선)                      │
│                                                             │
│  정확도 vs 속도?                                            │
│  ├─ 정확도 중요: HNSW + 높은 ef_search                     │
│  └─ 속도 중요: IVFFlat + 낮은 probes                       │
│                                                             │
│  메모리 제약?                                               │
│  ├─ 제약 있음: IVFFlat (메모리 효율적)                     │
│  └─ 여유 있음: HNSW (성능 우선)                            │
│                                                             │
│  일반적 권장:                                               │
│  • 대부분의 경우 HNSW 권장                                  │
│  • 자주 재빌드 필요하면 IVFFlat                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6. RAG 파이프라인

```
RAG (Retrieval-Augmented Generation) 흐름
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. 문서 준비 (Indexing)                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  문서들 → 청킹 → 임베딩 생성 → pgvector 저장        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  2. 검색 (Retrieval)                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  사용자 질문                                         │   │
│  │       ↓                                              │   │
│  │  질문 임베딩 생성                                    │   │
│  │       ↓                                              │   │
│  │  pgvector에서 유사 문서 검색 (<=> 연산)             │   │
│  │       ↓                                              │   │
│  │  관련 문서 조각들 반환                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  3. 생성 (Generation)                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  프롬프트 = 시스템 지시 + 관련 문서들 + 사용자 질문 │   │
│  │       ↓                                              │   │
│  │  LLM (GPT, Claude 등)                                │   │
│  │       ↓                                              │   │
│  │  컨텍스트 기반 응답 생성                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- RAG 검색 쿼리 예시
WITH query_embedding AS (
    SELECT embedding FROM embed_query('What is PostgreSQL?')
)
SELECT
    d.id,
    d.content,
    d.embedding <=> q.embedding AS distance
FROM documents d, query_embedding q
WHERE d.embedding <=> q.embedding < 0.5
ORDER BY distance
LIMIT 5;
```

---

## 비교표

### 거리 함수 비교

| 연산자 | 이름 | 범위 | 특징 |
|--------|------|------|------|
| `<->` | L2 Distance | 0 ~ ∞ | 크기와 방향 모두 고려 |
| `<#>` | Inner Product | -∞ ~ ∞ | 음수 반환, 정규화 필요 |
| `<=>` | Cosine Distance | 0 ~ 2 | 방향만 고려, 가장 일반적 |

### IVFFlat vs HNSW 비교

| 특성 | IVFFlat | HNSW |
|------|---------|------|
| 빌드 속도 | 빠름 | 느림 |
| 검색 속도 | 보통 | 빠름 |
| 메모리 사용 | 적음 | 많음 |
| 정확도 | 파라미터 의존 | 높음 |
| 업데이트 | 재빌드 필요 | 점진적 가능 |
| 권장 용도 | 빈번한 변경 | 읽기 위주 |

---

## 면접 예상 질문 및 모범 답안

### Q1. 벡터 임베딩이란 무엇이고, 왜 사용하나요?

**모범 답안:**

벡터 임베딩은 텍스트, 이미지 등 비정형 데이터를 고차원 숫자 배열로 변환한 것입니다.

**특징:**
- 의미적으로 유사한 데이터는 벡터 공간에서 가까움
- 차원 수는 모델에 따라 다름 (OpenAI ada-002: 1536차원)
- 거리 계산으로 유사도 측정 가능

**사용 이유:**
1. **시맨틱 검색**: "강아지"로 검색해도 "puppy" 문서 찾음
2. **RAG**: LLM에 관련 컨텍스트 제공
3. **추천 시스템**: 유사 아이템 추천
4. **이상 탐지**: 정상 패턴과 거리 측정

```sql
-- PostgreSQL에서 유사 문서 검색
SELECT content
FROM documents
ORDER BY embedding <=> query_embedding
LIMIT 5;
```

---

### Q2. pgvector의 거리 연산자 차이점을 설명해주세요.

**모범 답안:**

pgvector는 세 가지 거리/유사도 연산자를 제공합니다.

**1. L2 Distance (`<->`):**
- 유클리드 거리
- 벡터의 크기와 방향 모두 고려
- 범위: 0 ~ ∞

**2. Inner Product (`<#>`):**
- 내적의 음수값 반환
- 정규화된 벡터에서만 의미 있음
- 고성능 (단순 곱셈과 덧셈)

**3. Cosine Distance (`<=>`):**
- 1 - 코사인 유사도
- 방향만 고려 (크기 무관)
- 범위: 0 ~ 2
- 텍스트 임베딩에 가장 일반적

**권장:**
대부분의 텍스트 임베딩에서 **Cosine Distance**를 사용합니다. 벡터 크기보다 방향(의미)이 중요하기 때문입니다.

---

### Q3. IVFFlat과 HNSW 인덱스의 차이점과 선택 기준은?

**모범 답안:**

**IVFFlat:**
- K-means 클러스터링 기반
- 검색 시 가까운 클러스터만 탐색
- 빌드 빠름, 메모리 적음
- 데이터 변경 시 재빌드 권장

**HNSW:**
- 계층적 그래프 구조
- 상위 레이어에서 하위로 탐색
- 빌드 느림, 메모리 많음
- 검색 빠름, 정확도 높음

**선택 기준:**

| 상황 | 권장 인덱스 |
|------|------------|
| 읽기 위주 | HNSW |
| 빈번한 업데이트 | IVFFlat |
| 메모리 제약 | IVFFlat |
| 최고 정확도 | HNSW |

일반적으로 **HNSW**를 권장하며, 자주 재빌드해야 하면 IVFFlat을 고려합니다.

---

### Q4. RAG(Retrieval-Augmented Generation)에서 pgvector의 역할은?

**모범 답안:**

RAG는 LLM의 지식을 외부 데이터로 보강하는 기법입니다.

**pgvector의 역할: Retrieval 단계**

1. **문서 저장:**
```sql
INSERT INTO documents (content, embedding)
VALUES ('PostgreSQL guide...', '[0.1, 0.2, ...]');
```

2. **유사 문서 검색:**
```sql
SELECT content
FROM documents
ORDER BY embedding <=> query_embedding
LIMIT 5;
```

3. **LLM에 컨텍스트 제공:**
검색된 문서를 프롬프트에 포함하여 LLM이 관련 정보 기반으로 응답

**장점:**
- 최신 정보 반영 (LLM 학습 이후 데이터)
- 환각(Hallucination) 감소
- 도메인 특화 지식 활용
- SQL로 메타데이터 필터링 가능

---

### Q5. 벡터 인덱스 파라미터 튜닝 방법을 설명해주세요.

**모범 답안:**

**IVFFlat 파라미터:**

```sql
-- lists: 클러스터 수
CREATE INDEX ON docs USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- √rows 권장

-- probes: 검색할 클러스터 수
SET ivfflat.probes = 10;  -- √lists 권장
```

- lists 증가 → 빌드 느림, 검색 빠름
- probes 증가 → 정확도 높음, 속도 느림

**HNSW 파라미터:**

```sql
-- m: 연결 수, ef_construction: 빌드 시 탐색 범위
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- ef_search: 검색 시 탐색 범위
SET hnsw.ef_search = 40;
```

- m 증가 → 정확도 높음, 메모리 많음
- ef_construction 증가 → 빌드 느림, 그래프 품질 좋음
- ef_search 증가 → 정확도 높음, 속도 느림

**튜닝 전략:**
1. 기본값으로 시작
2. 정확도 확인 (Recall 측정)
3. 속도와 정확도 트레이드오프 조정

---

### Q6. 전문 벡터 DB(Pinecone, Weaviate) 대신 pgvector를 선택하는 이유는?

**모범 답안:**

**pgvector 선택 이유:**

1. **운영 단순화:**
   - 이미 PostgreSQL 사용 중이면 추가 인프라 불필요
   - 단일 DB로 관계형 데이터와 벡터 모두 관리

2. **트랜잭션 일관성:**
   ```sql
   BEGIN;
   INSERT INTO documents (...) VALUES (...);
   INSERT INTO embeddings (...) VALUES (...);
   COMMIT;
   ```
   - 문서와 임베딩의 원자적 업데이트

3. **SQL 통합:**
   ```sql
   SELECT d.content, m.category
   FROM documents d
   JOIN metadata m ON d.id = m.doc_id
   WHERE m.date > '2024-01-01'
   ORDER BY d.embedding <=> query_vec
   LIMIT 5;
   ```
   - 메타데이터 필터링 + 벡터 검색 결합

4. **비용:**
   - 오픈소스, 추가 라이선스 없음

**전문 벡터 DB 필요한 경우:**
- 수십억 벡터 규모
- 극한의 검색 성능 필요
- 분산 시스템 요구

중소 규모에서는 pgvector가 충분하며, 아키텍처 복잡도를 줄일 수 있습니다.

---

## 실무 체크리스트

```
□ 적절한 임베딩 모델 선택 (차원 수, 품질)
□ Cosine Distance (<=>)를 기본으로 사용
□ 10만 행 이상이면 인덱스 생성
□ HNSW 기본 권장, 빈번한 변경 시 IVFFlat
□ 인덱스 파라미터 튜닝 (Recall 측정)
□ 청킹 전략 설계 (문서 분할 크기)
□ 메타데이터 필터링과 벡터 검색 결합
□ 정기적인 인덱스 REINDEX 고려
```

---

## 참고 자료

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [pgvector 문서](https://github.com/pgvector/pgvector#readme)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- 책 GitHub: https://github.com/dmagda/just-use-postgres-book
