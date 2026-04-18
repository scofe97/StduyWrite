# Chapter 3. RAG Part II: 데이터와 대화하기 (Chatting with Your Data)

---

### 📌 핵심 요약
> RAG(Retrieval-Augmented Generation)는 외부 소스에서 관련 문서를 검색하여 LLM의 정확도를 높이는 기법이다. RAG는 3단계로 구성된다: ① **Indexing** (전처리/저장) → ② **Retrieval** (유사 문서 검색) → ③ **Generation** (컨텍스트와 함께 답변 생성). 프로덕션 RAG 시스템 구축을 위해 **Query Transformation** (쿼리 품질 개선), **Query Routing** (적절한 데이터소스 선택), **Query Construction** (자연어→쿼리 언어 변환) 전략이 필요하다.

---

### 🎯 학습 목표
- RAG의 3단계(Indexing → Retrieval → Generation)를 이해한다
- Query Transformation 전략(Rewrite, Multi-Query, RAG-Fusion, HyDE)을 설명할 수 있다
- Query Routing(Logical, Semantic)의 차이를 안다
- Query Construction(Text-to-Metadata, Text-to-SQL)을 이해한다

---

### 📖 본문 정리

#### 1. RAG 소개

**RAG가 필요한 이유**:

| 질문 | RAG 없는 LLM | RAG 적용 LLM |
|------|--------------|--------------|
| "최신 월드컵 우승국은?" | ❌ "프랑스 (2018)" | ✅ "아르헨티나 (2022)" |

- LLM은 학습 데이터에 없는 최신/비공개 정보를 모름
- 관련 컨텍스트를 프롬프트에 포함시켜 정확도 향상

##### RAG 3단계

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RAG Pipeline                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ① Indexing          ② Retrieval           ③ Generation            │
│  ┌──────────┐        ┌──────────┐          ┌──────────┐            │
│  │  문서    │   →    │  쿼리    │    →     │ 프롬프트  │   →  답변  │
│  │ 전처리   │        │  유사도  │          │ + 컨텍스트│            │
│  │ & 저장   │        │  검색    │          │ → LLM    │            │
│  └──────────┘        └──────────┘          └──────────┘            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

| 단계 | 역할 | 주요 도구 |
|------|------|-----------|
| **Indexing** | 문서 전처리 및 벡터 저장소에 저장 | Document Loader, Text Splitter, Embeddings, Vector Store |
| **Retrieval** | 쿼리와 유사한 문서 검색 | Retriever, Similarity Search |
| **Generation** | 검색된 문서를 컨텍스트로 답변 생성 | ChatPromptTemplate, LLM |

---

#### 2. Retrieval 단계

##### as_retriever 사용

```python
# Vector Store → Retriever 변환
retriever = db.as_retriever()

# 유사 문서 검색
docs = retriever.invoke("Who are key figures in Greek philosophy?")
```

##### k 파라미터

```python
# 상위 2개 문서만 검색
retriever = db.as_retriever(search_kwargs={"k": 2})
```

| k 값 | 장점 | 단점 |
|------|------|------|
| 낮음 (1-3) | 빠름, 비용 절감, 노이즈 감소 | 관련 정보 누락 가능 |
| 높음 (5-10) | 포괄적인 컨텍스트 | 느림, 비용 증가, 환각 위험 |

**주의**: 더 많은 문서 ≠ 더 좋은 결과 (무관한 정보가 환각 유발)

---

#### 3. Generation 단계

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain

prompt = ChatPromptTemplate.from_template("""Answer based only on this context:
{context}

Question: {question}
""")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

@chain
def qa(input):
    # 1. 관련 문서 검색
    docs = retriever.invoke(input)
    # 2. 프롬프트 포맷팅
    formatted = prompt.invoke({"context": docs, "question": input})
    # 3. 답변 생성
    answer = llm.invoke(formatted)
    return answer

# 실행
qa.invoke("Who are key figures in Greek philosophy?")
```

**핵심 패턴**: 여러 단계를 하나의 함수로 캡슐화 (`@chain` 데코레이터)

---

#### 4. Query Transformation 전략

사용자 쿼리 품질 문제를 해결하는 전략들:

```
추상화 수준별 Query Transformation 전략:

더 추상적 ←────────────────────────────→ 더 구체적

    HyDE          Multi-Query       Rewrite-Retrieve-Read
(가상 문서 생성)   (다중 쿼리 생성)     (쿼리 재작성)
```

##### 4.1 Rewrite-Retrieve-Read

**문제**: 사용자 쿼리에 불필요한 정보가 포함됨

```
원본: "오늘 아침에 양치하고, 뉴스 읽다가, 음식을 태웠어.
       그리스 철학의 주요 인물은 누구야?"
      ↓ LLM이 재작성
재작성: "ancient greek philosophy key figures"
```

```python
rewrite_prompt = ChatPromptTemplate.from_template(
    """Provide a better search query for: {x}. End with '**'. Answer:"""
)

def parse_output(message):
    return message.content.strip('"').strip("**")

rewriter = rewrite_prompt | llm | parse_output

@chain
def qa_rrr(input):
    new_query = rewriter.invoke(input)  # 쿼리 재작성
    docs = retriever.invoke(new_query)   # 재작성된 쿼리로 검색
    formatted = prompt.invoke({"context": docs, "question": input})
    return llm.invoke(formatted)
```

**단점**: LLM 호출 2회 → 지연 시간 증가

##### 4.2 Multi-Query Retrieval

**문제**: 단일 쿼리로는 필요한 모든 관점을 포착하지 못함

```
원본 쿼리: "그리스 철학의 주요 인물은?"
    ↓ LLM이 5개 변형 생성
1. "ancient greek philosophers"
2. "founders of western philosophy"
3. "socrates plato aristotle contributions"
4. "pre-socratic philosophers"
5. "hellenistic philosophy leaders"
    ↓ 각각 검색 후 합집합
[고유 문서들]
```

```python
perspectives_prompt = ChatPromptTemplate.from_template(
    """Generate 5 different versions of this question for vector search:
    Original: {question}"""
)

query_gen = perspectives_prompt | llm | (lambda m: m.content.split('\n'))

def get_unique_union(doc_lists):
    # 중복 제거
    deduped = {doc.page_content: doc for docs in doc_lists for doc in docs}
    return list(deduped.values())

retrieval_chain = query_gen | retriever.batch | get_unique_union
```

**핵심**: `retriever.batch`로 병렬 검색 → 중복 제거

##### 4.3 RAG-Fusion (RRF 알고리즘)

Multi-Query + **재순위화(Reranking)**:

```
각 쿼리별 검색 결과:
Query1: [Doc_A(1위), Doc_B(2위), Doc_C(3위)]
Query2: [Doc_B(1위), Doc_A(2위), Doc_D(3위)]
Query3: [Doc_A(1위), Doc_C(2위), Doc_B(3위)]

RRF 점수 계산: score = Σ 1/(rank + k)

Doc_A: 1/(1+60) + 1/(2+60) + 1/(1+60) = 0.049
Doc_B: 1/(2+60) + 1/(1+60) + 1/(3+60) = 0.048
...
    ↓ 점수순 정렬
최종: [Doc_A, Doc_B, Doc_C, Doc_D]
```

```python
def reciprocal_rank_fusion(results, k=60):
    fused_scores = {}
    documents = {}

    for docs in results:
        for rank, doc in enumerate(docs):
            key = doc.page_content
            if key not in fused_scores:
                fused_scores[key] = 0
                documents[key] = doc
            # RRF 공식
            fused_scores[key] += 1 / (rank + k)

    # 점수순 정렬
    sorted_keys = sorted(fused_scores, key=lambda d: fused_scores[d], reverse=True)
    return [documents[k] for k in sorted_keys]

retrieval_chain = query_gen | retriever.batch | reciprocal_rank_fusion
```

**k 파라미터**: 높을수록 낮은 순위 문서의 영향력 증가

##### 4.4 HyDE (Hypothetical Document Embeddings)

**아이디어**: 쿼리보다 **가상 문서**가 실제 문서와 더 유사함

```
쿼리: "그리스 철학의 주요 인물은?"
    ↓ LLM이 가상 문서 생성
가상 문서: "고대 그리스 철학의 주요 인물로는 소크라테스,
           플라톤, 아리스토텔레스가 있다. 소크라테스는..."
    ↓ 가상 문서를 임베딩하여 유사 문서 검색
[실제 관련 문서들]
```

```python
hyde_prompt = ChatPromptTemplate.from_template(
    """Write a passage to answer: {question}\nPassage:"""
)

generate_doc = hyde_prompt | ChatOpenAI(temperature=0) | StrOutputParser()

# 가상 문서로 검색
retrieval_chain = generate_doc | retriever
```

**장점**: 쿼리-문서 간 "의미적 갭" 해소

---

#### 5. Query Routing

여러 데이터소스 중 적절한 곳으로 쿼리 라우팅:

##### 5.1 Logical Routing (Function Calling)

LLM이 데이터소스를 **추론**하여 선택:

```python
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal

class RouteQuery(BaseModel):
    """Route to the most relevant datasource."""
    datasource: Literal["python_docs", "js_docs"] = Field(
        description="Choose datasource based on programming language"
    )

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
structured_llm = llm.with_structured_output(RouteQuery)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Route the question to the appropriate data source."),
    ("human", "{question}")
])

router = prompt | structured_llm

# 사용
result = router.invoke({"question": "from langchain_core.prompts import..."})
# → {"datasource": "python_docs"}

def choose_route(result):
    if "python_docs" in result.datasource.lower():
        return python_retriever
    else:
        return js_retriever

full_chain = router | RunnableLambda(choose_route)
```

**Tip**: 대소문자 변환 + 부분 문자열 매칭으로 LLM 출력의 불확실성 대응

##### 5.2 Semantic Routing (Cosine Similarity)

프롬프트 임베딩과 쿼리 임베딩의 **유사도**로 선택:

```python
from langchain.utils.math import cosine_similarity

physics_template = """You are a physics professor...\n{query}"""
math_template = """You are a mathematician...\n{query}"""

embeddings = OpenAIEmbeddings()
prompt_embeddings = embeddings.embed_documents([physics_template, math_template])

@chain
def prompt_router(query):
    query_embedding = embeddings.embed_query(query)
    similarity = cosine_similarity([query_embedding], prompt_embeddings)[0]
    most_similar = [physics_template, math_template][similarity.argmax()]
    return PromptTemplate.from_template(most_similar)

semantic_router = prompt_router | ChatOpenAI() | StrOutputParser()

# "블랙홀이란?" → physics_template 선택
semantic_router.invoke("What's a black hole")
```

| 방식 | 장점 | 적합한 경우 |
|------|------|-------------|
| Logical | 명확한 분류 기준 | 데이터소스가 명확히 구분됨 |
| Semantic | 유연한 매칭 | 주제가 모호하거나 겹침 |

---

#### 6. Query Construction

자연어 → 데이터소스 쿼리 언어 변환:

##### 6.1 Text-to-Metadata Filter (SelfQueryRetriever)

```
쿼리: "8.5점 이상의 SF 영화 추천해줘"
    ↓ 자동 분리
검색 쿼리: "science fiction"
메타데이터 필터: rating > 8.5
```

```python
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

fields = [
    AttributeInfo(name="genre", description="Movie genre", type="string"),
    AttributeInfo(name="year", description="Release year", type="integer"),
    AttributeInfo(name="rating", description="Rating 1-10", type="float"),
]

retriever = SelfQueryRetriever.from_llm(
    llm, db,
    document_contents="Brief summary of a movie",
    metadata_field_info=fields
)

# 자동으로 메타데이터 필터 + 시맨틱 검색 수행
retriever.invoke("highly rated (above 8.5) science fiction film")
```

##### 6.2 Text-to-SQL

```
쿼리: "직원이 몇 명이야?"
    ↓ LLM이 SQL 생성
SELECT COUNT(*) FROM employees;
    ↓ 실행
결과: 8
```

```python
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 질문 → SQL 변환
write_query = create_sql_query_chain(llm, db)

# SQL 실행
execute_query = QuerySQLDatabaseTool(db=db)

# 결합
chain = write_query | execute_query
chain.invoke("How many employees are there?")
```

**⚠️ 보안 주의사항**:
- 읽기 전용 DB 사용자 권한
- 허용된 테이블만 접근
- 쿼리 타임아웃 설정
- 프로덕션에서는 추가 보안 조치 필수

---

### 🔍 심화 학습

#### Query Transformation 전략 비교

| 전략 | 핵심 아이디어 | LLM 호출 | 적합한 경우 |
|------|--------------|----------|-------------|
| **Rewrite-Retrieve-Read** | 쿼리 정제 | 2회 | 잡음 많은 쿼리 |
| **Multi-Query** | 다중 관점 쿼리 | 1회 + 병렬 검색 | 복합적인 질문 |
| **RAG-Fusion** | Multi-Query + 재순위화 | 1회 + 병렬 검색 | 정밀한 순위 필요 |
| **HyDE** | 가상 문서 생성 | 2회 | 쿼리-문서 갭 큼 |

#### 프로덕션 RAG 체크리스트

```
Query Transformation:
├─ 사용자 쿼리가 불완전한가? → Rewrite-Retrieve-Read
├─ 다양한 관점이 필요한가? → Multi-Query / RAG-Fusion
└─ 쿼리와 문서 스타일이 다른가? → HyDE

Query Routing:
├─ 데이터소스가 명확히 구분되는가? → Logical Routing
└─ 주제 기반으로 라우팅해야 하는가? → Semantic Routing

Query Construction:
├─ 메타데이터 필터링이 필요한가? → SelfQueryRetriever
└─ SQL DB에서 조회해야 하는가? → Text-to-SQL
```

---

### 💡 실무 적용 포인트

1. **k 값 조절**: 너무 많은 문서 검색은 비용↑, 노이즈↑, 환각 위험↑
2. **Rewrite 적용**: 사용자 입력이 비정형적인 경우 쿼리 정제
3. **Multi-Query 활용**: 복잡한 질문은 여러 관점으로 분해
4. **RAG-Fusion**: 검색 결과의 정밀한 순위가 중요할 때
5. **Logical Routing**: 데이터소스가 명확히 분리된 경우 (Python docs vs JS docs)
6. **SelfQueryRetriever**: 메타데이터 필터링이 필요한 경우 (연도, 장르, 평점 등)
7. **Text-to-SQL 보안**: 프로덕션에서는 반드시 읽기 전용 권한 + 타임아웃 설정

---

### ✅ 정리 체크리스트

- [ ] RAG의 3단계(Indexing, Retrieval, Generation)를 순서대로 설명할 수 있다
- [ ] as_retriever()와 k 파라미터의 역할을 안다
- [ ] @chain 데코레이터로 여러 단계를 캡슐화할 수 있다
- [ ] Rewrite-Retrieve-Read 전략의 동작을 안다
- [ ] Multi-Query Retrieval과 중복 제거 로직을 이해한다
- [ ] RAG-Fusion의 RRF 알고리즘을 설명할 수 있다
- [ ] HyDE의 "가상 문서" 아이디어를 안다
- [ ] Logical Routing과 Semantic Routing의 차이를 안다
- [ ] with_structured_output으로 라우팅 스키마를 정의할 수 있다
- [ ] SelfQueryRetriever의 메타데이터 필터링을 안다
- [ ] Text-to-SQL의 보안 고려사항을 안다

---

### 🔗 참고 자료

- *LangChain for LLM Application Development* - Chapter 3
- [RAG Paper (Meta AI, 2021)](https://arxiv.org/abs/2005.11401)
- [Query Rewriting Paper (Microsoft Research, 2023)](https://arxiv.org/abs/2305.14283)
- [RAG-Fusion Paper (2024)](https://arxiv.org/abs/2402.03367)
- [HyDE Paper (2022)](https://arxiv.org/abs/2212.10496)
- [LangChain Retrievers Documentation](https://python.langchain.com/docs/modules/data_connection/retrievers/)
- [LangChain SQL Database](https://python.langchain.com/docs/integrations/tools/sql_database/)
