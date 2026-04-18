# Chapter 2. RAG Part I: 데이터 인덱싱 (Indexing Your Data)

---

### 📌 핵심 요약
> LLM은 **비공개 데이터**와 **최신 정보**를 알지 못한다는 한계가 있다. 이를 해결하기 위해 **RAG(Retrieval-Augmented Generation)** 기법을 사용한다. RAG의 첫 번째 단계인 **인덱싱**은 문서를 4단계로 전처리한다: ① 텍스트 추출(Document Loader) → ② 청크 분할(Text Splitter) → ③ 임베딩 생성(Embeddings Model) → ④ 벡터 저장소에 저장(Vector Store). 임베딩은 텍스트의 **의미(Semantic)**를 숫자로 표현한 것으로, **코사인 유사도**를 통해 유사한 문서를 찾을 수 있다.

---

### 🎯 학습 목표
- LLM의 지식 한계(Private data, Knowledge cutoff)를 이해한다
- RAG의 개념과 인덱싱 파이프라인을 설명할 수 있다
- Sparse vs Dense Embeddings의 차이를 안다
- Document Loader, Text Splitter, Embeddings Model, Vector Store 사용법을 안다
- 인덱싱 최적화 전략(MultiVector, RAPTOR, ColBERT)을 이해한다

---

### 📖 본문 정리

#### 1. LLM의 지식 한계

| 한계 | 설명 |
|------|------|
| **비공개 데이터 (Private Data)** | 공개되지 않은 정보는 LLM 학습 데이터에 포함되지 않음 |
| **지식 마감일 (Knowledge Cutoff)** | LLM 학습은 시간이 오래 걸려서, 특정 날짜 이후의 정보를 알지 못함 |

**문제점**: 모델이 모르는 정보에 대해 **환각(Hallucination)**을 일으켜 부정확한 정보를 생성함

**해결책**: 프롬프트에 관련 컨텍스트를 포함시키되, 모든 문서를 포함할 수 없으므로 **관련성 높은 부분만 선택**해야 함

---

#### 2. RAG 인덱싱 파이프라인

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAG Indexing Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📄 Document    →    📝 Text     →    🔢 Embeddings   →   🗄️ Vector  │
│     (PDF)           Chunks           (Numbers)           Store   │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │ Document │ → │  Text    │ → │Embeddings│ → │  Vector  │   │
│  │  Loader  │    │ Splitter │    │  Model   │    │  Store   │   │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 단계 | 도구 | 역할 |
|------|------|------|
| 1. 텍스트 추출 | Document Loader | 다양한 형식의 문서에서 텍스트 추출 |
| 2. 청크 분할 | Text Splitter | 큰 문서를 작은 청크로 분할 |
| 3. 임베딩 생성 | Embeddings Model | 텍스트를 숫자 벡터로 변환 |
| 4. 저장 | Vector Store | 벡터와 원본 텍스트를 저장 |

---

#### 3. 임베딩 (Embeddings): 텍스트를 숫자로

##### Sparse Embeddings (Bag-of-Words)

단어 존재 여부를 0/1로 표현:

```
문장: "What a sunny day"
     what  a  sunny  day  such  bright ...
       1   1    1     1    0      0    ...
```

**한계**: 의미(Semantic)를 이해하지 못함
- "sunny day"와 "bright skies"는 비슷한 의미지만, 단어가 달라 유사도 0

##### Dense Embeddings (LLM-based)

텍스트의 **의미**를 100~2,000개의 부동소수점 숫자로 표현:

```python
# 예시: 3차원 임베딩
lion = [0.2, 0.8, 0.1]
pet  = [0.9, 0.3, 0.7]
dog  = [0.8, 0.4, 0.6]

# pet과 dog가 lion보다 서로 더 가까움 (의미적으로 유사)
```

##### 코사인 유사도 (Cosine Similarity)

두 벡터 간의 유사도를 측정:

| 값 | 의미 |
|----|------|
| 1 | 완전히 유사 |
| 0 | 상관없음 |
| -1 | 완전히 반대 |

```
pet ↔ dog  : 0.75 (유사)
pet ↔ lion : 0.10 (비유사)
```

##### 임베딩의 다양한 활용

| 활용 | 설명 |
|------|------|
| **검색 (Search)** | 쿼리와 가장 유사한 문서 찾기 |
| **클러스터링** | 문서들을 주제별로 그룹화 |
| **분류** | 새 문서를 기존 라벨에 할당 |
| **추천** | 유사한 문서 추천 |
| **이상 탐지** | 기존 문서와 매우 다른 문서 식별 |
| **벡터 연산** | king - man + woman ≈ queen |

---

#### 4. Document Loaders

다양한 소스에서 텍스트를 추출하여 `Document` 객체로 변환:

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("./test.txt")
docs = loader.load()
# [Document(page_content='...', metadata={'source': './test.txt'})]
```

##### 주요 Document Loaders

| Loader | 용도 |
|--------|------|
| `TextLoader` | .txt 파일 |
| `PyPDFLoader` | PDF 파일 |
| `WebBaseLoader` | 웹 페이지 HTML |
| `CSVLoader` | CSV 파일 |
| `JSONLoader` | JSON 파일 |

```python
# PDF 로딩
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("./report.pdf")
pages = loader.load()

# 웹 페이지 로딩
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://www.example.com/")
docs = loader.load()
```

---

#### 5. Text Splitters

큰 문서를 작은 청크로 분할 (LLM/임베딩 모델의 컨텍스트 윈도우 제한 때문):

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 최대 청크 크기
    chunk_overlap=200,    # 청크 간 중복 (컨텍스트 유지)
)
chunks = splitter.split_documents(docs)
```

##### RecursiveCharacterTextSplitter 동작 원리

```
분할 순서 (중요도 순):
1. 단락 구분자: \n\n
2. 줄 구분자: \n
3. 단어 구분자: 공백
```

**의미 단위로 분할**: 단락 → 줄 → 단어 순으로 시도하여 의미가 유지되는 최대한 큰 단위로 분할

##### 코드/마크다운 분할

```python
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

# Python 코드 분할
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=50,
    chunk_overlap=0
)
python_docs = python_splitter.create_documents([python_code])

# Markdown 분할
md_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,
    chunk_size=60,
    chunk_overlap=0
)
md_docs = md_splitter.create_documents(
    [markdown_text],
    [{"source": "https://example.com"}]  # 메타데이터
)
```

---

#### 6. Embeddings Models

텍스트를 벡터로 변환:

```python
from langchain_openai import OpenAIEmbeddings

model = OpenAIEmbeddings()

# 여러 문서 임베딩 (배치 처리 권장)
embeddings = model.embed_documents([
    "Hi there!",
    "What's your name?",
    "Hello World!"
])
# [[0.004845, 0.004899, ...], [...], ...]
```

**주의**: 다른 모델의 임베딩은 비교 불가 (모델별로 다른 숫자/차원 생성)

---

#### 7. Vector Stores

벡터와 원본 텍스트를 저장하고 유사도 검색을 수행하는 특수 데이터베이스:

```
┌──────────────────────────────────────────────────────┐
│                    Vector Store                       │
├──────────────────────────────────────────────────────┤
│  Query → Embed → Similarity Search → Top-K Docs     │
│                                                       │
│  [0.1, 0.8, ...] ←→ Cosine Similarity ←→ [0.2, 0.7]  │
└──────────────────────────────────────────────────────┘
```

##### PGVector 설정

```bash
# Docker로 Postgres + PGVector 실행
docker run \
    --name pgvector-container \
    -e POSTGRES_USER=langchain \
    -e POSTGRES_PASSWORD=langchain \
    -e POSTGRES_DB=langchain \
    -p 6024:5432 \
    -d pgvector/pgvector:pg16
```

##### Vector Store 사용

```python
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings

connection = 'postgresql+psycopg://langchain:langchain@localhost:6024/langchain'
embeddings_model = OpenAIEmbeddings()

# 문서 로드 → 분할 → 임베딩 → 저장 (한 번에)
db = PGVector.from_documents(documents, embeddings_model, connection=connection)

# 유사도 검색
results = db.similarity_search("query", k=4)

# 문서 추가
db.add_documents([
    Document(page_content="cats in the pond", metadata={"topic": "animals"})
], ids=[str(uuid.uuid4())])

# 문서 삭제
db.delete(ids=["document-id"])
```

---

#### 8. Indexing API (변경 추적)

문서 변경 시 중복 방지 및 효율적인 재인덱싱을 위한 API:

##### Cleanup 모드

| 모드 | 동작 |
|------|------|
| `None` | 자동 정리 없음 (수동 관리) |
| `incremental` | 변경된 문서만 업데이트/삭제 |
| `full` | 현재 인덱싱에 포함되지 않은 모든 문서 삭제 |

```python
from langchain.indexes import SQLRecordManager, index

# Record Manager 생성
record_manager = SQLRecordManager(
    "my_namespace",
    db_url="postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
)
record_manager.create_schema()

# 인덱싱 (중복 방지)
result = index(
    docs,
    record_manager,
    vectorstore,
    cleanup="incremental",
    source_id_key="source"
)
# {'num_added': 2, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 0}

# 동일 문서 재인덱싱 시 스킵됨
result2 = index(docs, record_manager, vectorstore, cleanup="incremental", source_id_key="source")
# {'num_added': 0, 'num_updated': 0, 'num_skipped': 2, 'num_deleted': 0}

# 문서 수정 시 자동 업데이트
docs[0].page_content = "Modified content!"
result3 = index(docs, record_manager, vectorstore, cleanup="incremental", source_id_key="source")
# {'num_added': 1, 'num_updated': 0, 'num_skipped': 1, 'num_deleted': 1}
```

---

#### 9. 인덱싱 최적화 전략

##### 9.1 MultiVectorRetriever

**문제**: 테이블이 포함된 문서는 단순 텍스트 분할 시 테이블이 손실됨

**해결**: 요약(Summary)을 임베딩하고, 검색 시 원본 전체를 반환

```
┌─────────────────────────────────────────────────────────┐
│                  MultiVectorRetriever                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  원본 문서 → LLM 요약 → 요약 임베딩 → Vector Store      │
│      ↓                                                   │
│  원본 저장 ─────────────────────────→ Doc Store         │
│                                                          │
│  검색: 요약으로 찾음 → 원본 전체 반환                    │
└─────────────────────────────────────────────────────────┘
```

```python
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore

# 요약용 Vector Store + 원본용 Doc Store
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=InMemoryStore(),
    id_key="doc_id"
)

# 요약은 Vector Store에, 원본은 Doc Store에 저장
retriever.vectorstore.add_documents(summary_docs)
retriever.docstore.mset(list(zip(doc_ids, original_chunks)))

# 검색 시 원본 전체 반환
retrieved_docs = retriever.invoke("chapter on philosophy")
```

##### 9.2 RAPTOR (Recursive Abstractive Processing)

**문제**: 단일 문서의 세부 사항과 여러 문서에 걸친 상위 개념 모두 처리 필요

**해결**: 재귀적으로 요약 → 클러스터링 → 재요약하여 계층적 트리 구성

```
Level 3:    [전체 요약]
              ↑
Level 2: [클러스터1 요약] [클러스터2 요약]
              ↑               ↑
Level 1: [청크 요약들...] [청크 요약들...]
              ↑               ↑
Level 0: [원본 청크들...] [원본 청크들...]
```

**효과**: 낮은 수준(세부 사항) ~ 높은 수준(개념) 질문 모두 대응 가능

##### 9.3 ColBERT (Late Interaction)

**문제**: 고정 길이 임베딩은 불필요한 내용도 포함하여 환각 유발 가능

**해결**: 토큰 단위로 임베딩 후, 쿼리-문서 토큰 간 유사도 합산

```python
from ragatouille import RAGPretrainedModel

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

# 인덱스 생성
RAG.index(
    collection=[full_document],
    index_name="my-index",
    max_document_length=180,
    split_documents=True
)

# 검색
results = RAG.search(query="What studio did Miyazaki found?", k=3)

# LangChain Retriever로 사용
retriever = RAG.as_langchain_retriever(k=3)
```

---

### 🔍 심화 학습

#### Chunk Size 선택 가이드

| Chunk Size | 장점 | 단점 | 적합한 경우 |
|------------|------|------|-------------|
| 작음 (200-500) | 정밀한 검색 | 컨텍스트 부족 | FAQ, 짧은 답변 |
| 중간 (500-1000) | 균형 잡힌 검색 | - | 일반적인 Q&A |
| 큼 (1000-2000) | 풍부한 컨텍스트 | 노이즈 포함 가능 | 복잡한 분석 |

#### Vector Store 선택 기준

| 기준 | 고려사항 |
|------|----------|
| **규모** | 소규모: 인메모리, 대규모: 전용 Vector DB |
| **기존 인프라** | PostgreSQL 사용 중 → PGVector |
| **검색 성능** | 전용 DB (Weaviate, Pinecone) > 확장 기능 |
| **비용** | 오픈소스 (PGVector, Weaviate) vs 상용 (Pinecone) |

#### 임베딩 모델 비교

| 모델 | 차원 | 특징 |
|------|------|------|
| OpenAI text-embedding-3-small | 1536 | 비용 효율적 |
| OpenAI text-embedding-3-large | 3072 | 고품질 |
| Cohere embed-v3 | 1024 | 다국어 지원 |
| Ollama (로컬) | 다양 | 무료, 프라이버시 |

---

### 💡 실무 적용 포인트

1. **적절한 Chunk Size 선택**: 너무 작으면 컨텍스트 손실, 너무 크면 노이즈 증가
2. **Chunk Overlap 사용**: 청크 경계에서 정보 손실 방지 (보통 10-20%)
3. **메타데이터 활용**: source, page_number 등을 저장하여 추적 가능하게
4. **Indexing API 사용**: 문서 변경 시 효율적인 재인덱싱
5. **테이블/이미지 포함 문서**: MultiVectorRetriever로 요약과 원본 분리
6. **다양한 질문 수준**: RAPTOR로 세부~개념 질문 모두 대응
7. **기존 DB 활용**: PostgreSQL 사용 중이면 PGVector로 복잡성 감소

---

### ✅ 정리 체크리스트

- [ ] LLM의 두 가지 지식 한계(Private data, Knowledge cutoff)를 안다
- [ ] RAG 인덱싱 4단계를 순서대로 설명할 수 있다
- [ ] Sparse vs Dense Embeddings의 차이를 안다
- [ ] 코사인 유사도의 개념과 값의 의미를 안다
- [ ] Document Loader 사용법을 안다
- [ ] RecursiveCharacterTextSplitter의 동작 원리를 이해한다
- [ ] chunk_size와 chunk_overlap의 역할을 안다
- [ ] Vector Store에서 similarity_search 사용법을 안다
- [ ] Indexing API의 cleanup 모드(None, incremental, full)를 안다
- [ ] MultiVectorRetriever의 목적과 동작을 이해한다
- [ ] RAPTOR의 계층적 요약 개념을 안다
- [ ] ColBERT의 토큰 단위 유사도 계산 방식을 안다

---

### 🔗 참고 자료

- *LangChain for LLM Application Development* - Chapter 2
- [LangChain Document Loaders](https://python.langchain.com/docs/integrations/document_loaders/)
- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [LangChain Vector Stores](https://python.langchain.com/docs/integrations/vectorstores/)
- [PGVector Extension](https://github.com/pgvector/pgvector)
- [RAPTOR Paper (ICLR 2024)](https://arxiv.org/abs/2401.18059)
- [ColBERTv2 Paper](https://arxiv.org/abs/2112.01488)
- [RAGatouille Library](https://github.com/bclavie/RAGatouille)
