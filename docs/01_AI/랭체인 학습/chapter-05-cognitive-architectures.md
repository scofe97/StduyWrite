# Chapter 5. LangGraph로 인지 아키텍처 구현하기 (Cognitive Architectures with LangGraph)

---

### 📌 핵심 요약
> LLM 애플리케이션 설계의 핵심은 **인지 아키텍처(Cognitive Architecture)** 선택이다. 같은 재료(RAG, 프롬프팅, 메모리)로도 구조에 따라 전혀 다른 애플리케이션이 만들어진다. 아키텍처 선택의 핵심 트레이드오프는 **자율성(Agency) vs 신뢰성(Reliability)**이다. LangGraph로 구현 가능한 주요 아키텍처는 **LLM Call**(단일 호출), **Chain**(순차적 다중 호출), **Router**(조건부 분기)가 있으며, 각각 자율성 수준이 다르다.

---

### 🎯 학습 목표
- 인지 아키텍처의 개념과 필요성을 이해한다
- Agency vs Reliability 트레이드오프를 설명할 수 있다
- LLM 자율성의 세 가지 수준을 구분할 수 있다
- LLM Call, Chain, Router 아키텍처의 차이점을 안다
- LangGraph로 각 아키텍처를 구현할 수 있다
- 조건부 Edge(conditional_edges)를 활용할 수 있다

---

### 📖 본문 정리

#### 1. 인지 아키텍처란?

##### 왜 아키텍처가 중요한가?

```
같은 재료, 다른 결과:

벽돌 + 시멘트 + 철근
    ↓
┌─────────────┐     ┌─────────────┐
│   수영장    │  vs │   1층 집    │
└─────────────┘     └─────────────┘

RAG + 프롬프팅 + 메모리
    ↓
┌─────────────┐     ┌─────────────┐
│ 이메일 비서 │  vs │  SQL 생성기 │
└─────────────┘     └─────────────┘
```

**핵심**: 재료(컴포넌트)보다 **조합 방식(아키텍처)**이 더 중요

##### 인지 아키텍처 정의

> **Cognitive Architecture**: LLM 애플리케이션이 취해야 할 단계(steps)를 정의하는 레시피
>
> *출처: "Cognitive Architectures for Language Agents" (Sumers et al., 2023)*

**단계(Step) 예시**:
- RAG: 관련 문서 검색
- LLM 호출: Chain-of-Thought 프롬프트로 추론
- 도구 호출: 검색 엔진, 계산기 등

---

#### 2. Agency vs Reliability 트레이드오프

##### 이메일 비서 예시

**목표**: 이메일을 읽고 분류/응답하는 AI 비서

**제약 조건**:
- 사용자 방해 최소화 (시간 절약이 목적)
- 사용자가 보내지 않았을 답변 방지

##### 핵심 트레이드오프

```
← 낮은 자율성                높은 자율성 →
┌─────────────────────────────────────────┐
│                                         │
│  신뢰성 ↑              자율성 ↑         │
│  유용성 ↓              위험성 ↑         │
│                                         │
└─────────────────────────────────────────┘
```

| 속성 | 설명 | 예시 |
|------|------|------|
| **Agency (자율성)** | 자율적으로 행동할 수 있는 능력 | 이메일 자동 응답 |
| **Reliability (신뢰성)** | 출력을 신뢰할 수 있는 정도 | 검토 후 응답 |

##### LLM 자율성의 세 가지 수준

| 수준 | LLM이 결정하는 것 | 예시 |
|------|-------------------|------|
| **1단계** | 스텝의 **출력** | 이메일 답장 초안 작성 |
| **2단계** | **다음 스텝** 선택 | 보관/답장/검토 중 선택 |
| **3단계** | **가능한 스텝** 정의 | 새로운 동작 코드 작성 |

```
자율성 수준:
Level 1: LLM이 출력만 결정 (개발자가 흐름 제어)
    ↓
Level 2: LLM이 다음 스텝 선택 (개발자가 옵션 제공)
    ↓
Level 3: LLM이 스텝 자체를 정의 (최대 자율성)
```

---

#### 3. 인지 아키텍처 분류

```
┌─────────────────────────────────────────────────────────────┐
│                  Cognitive Architectures                     │
│                                                             │
│  #0 Code   #1 LLM Call   #2 Chain   #3 Router   #4+ Agent  │
│     │          │            │           │            │      │
│     └──────────┴────────────┴───────────┴────────────┘      │
│                                                             │
│  ← 낮은 자율성                          높은 자율성 →        │
└─────────────────────────────────────────────────────────────┘
```

| 아키텍처 | 설명 | LLM 역할 |
|----------|------|----------|
| **#0 Code** | LLM 미사용, 일반 소프트웨어 | 없음 |
| **#1 LLM Call** | 단일 LLM 호출 | 출력 생성 |
| **#2 Chain** | 순차적 다중 LLM 호출 | 각 스텝 출력 생성 |
| **#3 Router** | LLM이 다음 스텝 선택 | 스텝 선택 + 출력 생성 |
| **#4+ Agent** | LLM이 반복적으로 결정 | (Chapter 6에서 다룸) |

---

#### 4. Architecture #1: LLM Call

##### 특징

- **가장 단순한 아키텍처**: 단일 LLM 호출
- **용도**: 더 큰 애플리케이션의 일부로 특정 작업 수행

##### 실제 사용 예

| 제품 | 기능 | 아키텍처 |
|------|------|----------|
| Notion | 요약, 번역 | 단일 LLM Call |
| 간단한 SQL 생성기 | 쿼리 생성 | 단일 LLM Call |

##### LangGraph 구현

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

model = ChatOpenAI()

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    answer = model.invoke(state["messages"])
    return {"messages": [answer]}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()
```

##### 그래프 구조

```
┌───────┐     ┌─────────┐     ┌─────┐
│ START │ ──→ │ chatbot │ ──→ │ END │
└───────┘     └─────────┘     └─────┘
```

##### 실행

```python
from langchain_core.messages import HumanMessage

input = {"messages": [HumanMessage("hi!")]}
for chunk in graph.stream(input):
    print(chunk)

# 출력: {"chatbot": {"messages": [AIMessage("How can I help you?")]}}
```

---

#### 5. Architecture #2: Chain

##### 특징

- **다중 LLM 호출**: 미리 정의된 순서대로 실행
- **Flow Engineering**이라고도 불림
- **모든 호출이 같은 순서**로 실행 (입력/출력만 다름)

##### Text-to-SQL 예시

```
┌──────────────────────────────────────────────────────────┐
│                   Text-to-SQL Chain                       │
│                                                          │
│  Step 1: SQL 생성                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 입력: 사용자 질문 + DB 스키마 설명               │    │
│  │ 출력: SQL 쿼리                                   │    │
│  └─────────────────────────────────────────────────┘    │
│                         ↓                                │
│  Step 2: SQL 설명                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 입력: 생성된 SQL 쿼리                            │    │
│  │ 출력: 비전문가용 설명                            │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  (선택적 확장)                                            │
│  Step 3: SQL 실행 → Step 4: 결과 요약                     │
└──────────────────────────────────────────────────────────┘
```

##### LangGraph 구현

```python
from typing import Annotated, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

# Temperature에 따른 모델 분리
model_low_temp = ChatOpenAI(temperature=0.1)   # SQL 생성용 (정확성)
model_high_temp = ChatOpenAI(temperature=0.7)  # 자연어 출력용 (유창성)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str       # 입력
    sql_query: str        # 출력
    sql_explanation: str  # 출력

class Input(TypedDict):
    user_query: str

class Output(TypedDict):
    sql_query: str
    sql_explanation: str

generate_prompt = SystemMessage(
    "You are a helpful data analyst who generates SQL queries..."
)

def generate_sql(state: State) -> State:
    user_message = HumanMessage(state["user_query"])
    messages = [generate_prompt, *state["messages"], user_message]
    res = model_low_temp.invoke(messages)
    return {
        "sql_query": res.content,
        "messages": [user_message, res],
    }

explain_prompt = SystemMessage(
    "You are a helpful data analyst who explains SQL queries..."
)

def explain_sql(state: State) -> State:
    messages = [explain_prompt, *state["messages"]]
    res = model_high_temp.invoke(messages)
    return {
        "sql_explanation": res.content,
        "messages": res,
    }

# 그래프 구성
builder = StateGraph(State, input=Input, output=Output)
builder.add_node("generate_sql", generate_sql)
builder.add_node("explain_sql", explain_sql)
builder.add_edge(START, "generate_sql")
builder.add_edge("generate_sql", "explain_sql")
builder.add_edge("explain_sql", END)

graph = builder.compile()
```

##### 그래프 구조

```
┌───────┐     ┌──────────────┐     ┌─────────────┐     ┌─────┐
│ START │ ──→ │ generate_sql │ ──→ │ explain_sql │ ──→ │ END │
└───────┘     └──────────────┘     └─────────────┘     └─────┘
```

##### 실행 결과

```python
graph.invoke({"user_query": "What is the total sales for each product?"})
```

```python
{
    "sql_query": """SELECT product_name, SUM(sales_amount) AS total_sales
                    FROM sales
                    GROUP BY product_name;""",
    "sql_explanation": "This query retrieves the total sales for each product..."
}
```

##### Input/Output 스키마 분리

```python
builder = StateGraph(State, input=Input, output=Output)
```

| 스키마 | 역할 |
|--------|------|
| `State` | 전체 상태 (내부 포함) |
| `Input` | 사용자로부터 받는 입력만 |
| `Output` | 사용자에게 반환하는 출력만 |

---

#### 6. Architecture #3: Router

##### 특징

- **LLM이 다음 스텝 선택**: 자율성 한 단계 상승
- **조건부 분기**: 입력에 따라 다른 경로 실행
- **Conditional Edge** 사용

##### Router vs Chain 비교

| 특성 | Chain | Router |
|------|-------|--------|
| **실행 순서** | 고정 | 동적 |
| **분기** | 없음 | 조건부 분기 |
| **LLM 역할** | 출력만 생성 | 경로 선택 + 출력 |

##### Multi-Index RAG 예시

**문제**: 여러 도메인의 문서 인덱스가 있을 때 어떤 인덱스를 사용할지?

**기존 방식 (ML Classifier)**:
- 수동으로 데이터셋 구축 필요
- 쿼리에서 특성(feature) 추출 필요
- 분류기 학습 필요

**LLM Router 방식**:
- Zero-shot 또는 Few-shot으로 분류 가능
- 추가 학습 불필요

##### 흐름 설명

```
┌──────────────────────────────────────────────────────────────┐
│                   Multi-Index RAG Router                      │
│                                                              │
│  Step 1: Router (LLM)                                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 입력: 사용자 쿼리 + 인덱스 설명                     │     │
│  │ 출력: 사용할 인덱스 선택 (records | insurance)     │     │
│  └────────────────────────────────────────────────────┘     │
│                         ↓                                    │
│  Step 2: Retrieval (조건부)                                   │
│  ┌────────────────┐         ┌─────────────────────┐         │
│  │ Medical Records│   OR    │ Insurance FAQs      │         │
│  │ Retriever      │         │ Retriever           │         │
│  └────────────────┘         └─────────────────────┘         │
│                         ↓                                    │
│  Step 3: Answer Generation                                   │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 입력: 검색된 문서 + 사용자 쿼리                    │     │
│  │ 출력: 최종 답변                                    │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

##### LangGraph 구현

```python
from typing import Annotated, Literal, TypedDict
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

embeddings = OpenAIEmbeddings()
model_low_temp = ChatOpenAI(temperature=0.1)
model_high_temp = ChatOpenAI(temperature=0.7)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str
    domain: Literal["records", "insurance"]  # LLM이 선택
    documents: list[Document]
    answer: str

# Vector Store 및 Retriever 설정
medical_records_store = InMemoryVectorStore.from_documents([], embeddings)
medical_records_retriever = medical_records_store.as_retriever()

insurance_faqs_store = InMemoryVectorStore.from_documents([], embeddings)
insurance_faqs_retriever = insurance_faqs_store.as_retriever()

# Router Node: LLM이 도메인 선택
router_prompt = SystemMessage("""
You need to decide which domain to route the user query to:
- records: medical records (diagnosis, treatment, prescriptions)
- insurance: insurance FAQs (policies, claims, coverage)

Output only the domain name.
""")

def router_node(state: State) -> State:
    user_message = HumanMessage(state["user_query"])
    messages = [router_prompt, *state["messages"], user_message]
    res = model_low_temp.invoke(messages)
    return {
        "domain": res.content,
        "messages": [user_message, res],
    }

# Conditional Edge 함수: 다음 노드 결정
def pick_retriever(state: State) -> Literal[
    "retrieve_medical_records",
    "retrieve_insurance_faqs"
]:
    if state["domain"] == "records":
        return "retrieve_medical_records"
    else:
        return "retrieve_insurance_faqs"

# Retriever Nodes
def retrieve_medical_records(state: State) -> State:
    documents = medical_records_retriever.invoke(state["user_query"])
    return {"documents": documents}

def retrieve_insurance_faqs(state: State) -> State:
    documents = insurance_faqs_retriever.invoke(state["user_query"])
    return {"documents": documents}

# Answer Generation Node
def generate_answer(state: State) -> State:
    if state["domain"] == "records":
        prompt = SystemMessage("You are a medical chatbot...")
    else:
        prompt = SystemMessage("You are an insurance chatbot...")

    messages = [prompt, *state["messages"],
                HumanMessage(f"Documents: {state['documents']}")]
    res = model_high_temp.invoke(messages)
    return {"answer": res.content, "messages": res}

# 그래프 구성
builder = StateGraph(State, input=Input, output=Output)
builder.add_node("router", router_node)
builder.add_node("retrieve_medical_records", retrieve_medical_records)
builder.add_node("retrieve_insurance_faqs", retrieve_insurance_faqs)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "router")
builder.add_conditional_edges("router", pick_retriever)  # 조건부 Edge!
builder.add_edge("retrieve_medical_records", "generate_answer")
builder.add_edge("retrieve_insurance_faqs", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()
```

##### 그래프 구조

```
                          ┌───────────────────────────┐
                          │ retrieve_medical_records  │
                     ┌───→│                           │───┐
                     │    └───────────────────────────┘   │
┌───────┐  ┌────────┐│                                    ↓  ┌─────────────────┐  ┌─────┐
│ START │─→│ router │┤                                    ├─→│ generate_answer │─→│ END │
└───────┘  └────────┘│                                    ↑  └─────────────────┘  └─────┘
                     │    ┌───────────────────────────┐   │
                     └───→│ retrieve_insurance_faqs   │───┘
                          └───────────────────────────┘

                  (점선: Conditional Edge)
```

##### Conditional Edge 핵심

```python
# 일반 Edge: 항상 같은 다음 노드
builder.add_edge("A", "B")  # A → B (항상)

# Conditional Edge: 함수가 다음 노드 결정
builder.add_conditional_edges("router", pick_retriever)
# router → pick_retriever() 결과에 따라 분기
```

##### 스트리밍 출력 예시

```python
input = {"user_query": "Am I covered for COVID-19 treatment?"}
for c in graph.stream(input):
    print(c)
```

```python
# 1. Router가 도메인 선택
{"router": {
    "messages": [HumanMessage("Am I covered..."), AIMessage("insurance")],
    "domain": "insurance"
}}

# 2. 선택된 Retriever 실행 (insurance 경로)
{"retrieve_insurance_faqs": {
    "documents": [...]
}}

# 3. 답변 생성
{"generate_answer": {
    "messages": AIMessage("..."),
    "answer": "..."
}}
```

---

### 🔍 심화 학습

#### 아키텍처 선택 가이드

```
사용 사례별 권장 아키텍처:
├─ 단순 변환 (번역, 요약) → #1 LLM Call
├─ 순차적 처리 (Text-to-SQL + 설명) → #2 Chain
├─ 다중 데이터 소스 → #3 Router
├─ 복잡한 의사결정 → #4+ Agent (Chapter 6)
└─ 최대 자율성 필요 → #4+ Agent
```

#### Temperature 전략

| 작업 유형 | Temperature | 이유 |
|-----------|-------------|------|
| SQL 생성, 라우팅 | 0.1 ~ 0.3 | 정확성, 일관성 필요 |
| 설명, 답변 생성 | 0.5 ~ 0.7 | 자연스러운 표현 |
| 창작, 브레인스토밍 | 0.7 ~ 1.0 | 다양성 필요 |

#### Conditional Edge 패턴

```python
# 패턴 1: 단순 매핑
def pick_node(state):
    return "node_a" if state["condition"] else "node_b"

# 패턴 2: 다중 분기
def pick_node(state) -> Literal["node_a", "node_b", "node_c"]:
    mapping = {
        "type_a": "node_a",
        "type_b": "node_b",
        "type_c": "node_c",
    }
    return mapping[state["type"]]

# 패턴 3: LLM 출력 기반
def pick_node(state):
    llm_decision = state["llm_choice"]  # LLM이 선택한 값
    return f"handle_{llm_decision}"
```

#### LLM을 Classifier로 사용하는 장점

| 기존 ML 방식 | LLM Router 방식 |
|-------------|-----------------|
| 데이터셋 수집 필요 | Zero-shot 가능 |
| Feature Engineering 필요 | 자연어 설명으로 충분 |
| 모델 학습 필요 | 즉시 사용 가능 |
| 새 카테고리 추가 시 재학습 | 프롬프트 수정만으로 가능 |

---

### 💡 실무 적용 포인트

1. **단순 시작**: #1 LLM Call로 시작 → 필요시 복잡한 아키텍처로 확장
2. **Temperature 분리**: 작업 특성에 맞게 모델 인스턴스 분리
3. **Input/Output 스키마**: 내부 상태와 외부 인터페이스 분리
4. **Router 활용**: 다중 데이터 소스나 전문화된 처리 필요 시
5. **스트리밍 디버깅**: `graph.stream()`으로 각 노드 출력 확인
6. **점진적 자율성**: 신뢰성 확보 후 자율성 증가
7. **Flow Engineering**: Chain 아키텍처로 복잡한 작업을 단계별로 분해

---

### ✅ 정리 체크리스트

- [ ] 인지 아키텍처가 무엇인지 설명할 수 있다
- [ ] Agency vs Reliability 트레이드오프를 이해한다
- [ ] LLM 자율성의 세 가지 수준을 구분할 수 있다
- [ ] #0~#3 아키텍처의 특징과 차이점을 안다
- [ ] LLM Call 아키텍처를 LangGraph로 구현할 수 있다
- [ ] Chain 아키텍처를 구현하고 Temperature를 전략적으로 설정할 수 있다
- [ ] Input/Output 스키마 분리의 목적을 안다
- [ ] Router 아키텍처에서 `add_conditional_edges`를 사용할 수 있다
- [ ] LLM을 Classifier로 활용하는 장점을 안다
- [ ] 스트리밍 출력으로 그래프 실행을 디버깅할 수 있다

---

### 🔗 참고 자료

- *LangChain for LLM Application Development* (책 제목 가정)
- Theodore R. Sumers et al., "Cognitive Architectures for Language Agents", arXiv, 2023
- Tal Ridnik et al., "Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering", arXiv, 2024
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Conditional Edges](https://langchain-ai.github.io/langgraph/concepts/low_level/#conditional-edges)
