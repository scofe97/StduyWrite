# Chapter 6. Agent 아키텍처 (Agent Architecture)

---

### 📌 핵심 요약
> **Agent**는 "행동하는 무언가"로, LLM이 여러 가능한 행동 중 하나를 **선택**하고 **실행**하는 아키텍처다. 핵심은 **Tool Calling**(외부 함수 호출)과 **Chain-of-Thought**(단계적 추론)의 조합, 그리고 **LLM이 제어하는 루프(Plan-Do Loop)**다. 이 아키텍처는 **ReAct**라 불리며, LLM이 스스로 언제 멈출지 결정한다. LangGraph는 `ToolNode`와 `tools_condition`으로 이를 쉽게 구현하며, **특정 도구 우선 호출**이나 **RAG 기반 도구 선택**으로 확장할 수 있다.

---

### 🎯 학습 목표
- Agent의 정의와 특성을 이해한다
- Tool Calling과 Chain-of-Thought의 조합을 설명할 수 있다
- Plan-Do Loop(ReAct)의 동작 원리를 안다
- LangGraph로 기본 Agent를 구현할 수 있다
- ToolNode와 tools_condition의 역할을 안다
- Agent 확장 패턴(도구 우선 호출, 다중 도구 처리)을 적용할 수 있다

---

### 📖 본문 정리

#### 1. Agent란 무엇인가?

##### 정의 (Stuart Russell & Peter Norvig)

> **Agent**: "Something that acts" (행동하는 무언가)
>
> *— Artificial Intelligence: A Modern Approach (Pearson, 2020)*

##### "Acts"의 의미

```
행동(Acts)의 세 가지 조건:
├─ 1. 결정 능력: 무엇을 할지 결정할 수 있어야 함
├─ 2. 선택지: 둘 이상의 가능한 행동이 있어야 함
└─ 3. 정보 접근: 외부 환경에 대한 정보에 접근 가능해야 함
```

##### Agentic LLM 애플리케이션

```
┌─────────────────────────────────────────────────────────┐
│                  Agentic LLM Application                │
│                                                         │
│  ┌─────────┐    컨텍스트     ┌──────────────────────┐  │
│  │  LLM    │ ←───────────── │ 외부 환경 정보        │  │
│  │         │                │ (검색 결과, DB 등)    │  │
│  └────┬────┘                └──────────────────────┘  │
│       │                                               │
│       ↓ 선택                                           │
│  ┌────────────────────────────────────────────────┐   │
│  │  Action A  |  Action B  |  Action C  |  ...    │   │
│  │  (검색)    |  (계산)    |  (종료)    |         │   │
│  └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

#### 2. Agent의 핵심 기술

##### 두 가지 프롬프팅 기법의 조합

| 기법 | 역할 | 구현 |
|------|------|------|
| **Tool Calling** | 외부 함수 목록 제공, 선택 형식 지정 | 도구 설명 + 출력 형식 지시 |
| **Chain-of-Thought** | 복잡한 문제를 단계별로 분해 | "Think step by step" 지시 |

##### 예시 프롬프트

```
Tools:
search: this tool accepts a web search query and returns top results.
calculator: this tool accepts math expressions and returns their result.

If you want to use tools, output in CSV format: tool,input

Think step by step; if you need multiple tool calls, return only the first one.

How old was the 30th president of the United States when he died?

tool,input
```

**LLM 출력** (temperature=0):
```
search,30th president of the United States
```

---

#### 3. Plan-Do Loop (ReAct 아키텍처)

##### LLM이 제어하는 루프

```
┌─────────────────────────────────────────────────────────────┐
│                     Plan-Do Loop (ReAct)                     │
│                                                             │
│   ┌──────────────────────────────────────────────────────┐ │
│   │                                                       │ │
│   │  ┌──────────┐     ┌──────────┐     ┌────────────┐   │ │
│   │  │  Plan    │ ──→ │   Do     │ ──→ │  Observe   │   │ │
│   │  │ (LLM)    │     │ (Tool)   │     │ (결과확인) │   │ │
│   │  └──────────┘     └──────────┘     └─────┬──────┘   │ │
│   │       ↑                                   │          │ │
│   │       └───────────────────────────────────┘          │ │
│   │                                                       │ │
│   │             LLM이 "output" 선택 시 루프 종료          │ │
│   └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

##### ReAct의 핵심

> **ReAct** (Reasoning + Acting): Shunyu Yao et al.이 제안
>
> LLM이 **다음 행동**을 결정하고, **언제 멈출지**도 결정

##### 실행 예시

**Iteration 1:**
```
입력: "How old was the 30th president when he died?"
LLM 출력: search,30th president of the United States
→ 검색 실행
```

**Iteration 2:**
```
입력: [이전 대화 + 검색 결과]
검색 결과: "Calvin Coolidge (July 4, 1872 – January 5, 1933)..."
LLM 출력: calculator,1933-1872
→ 계산 실행
```

**Iteration 3:**
```
입력: [이전 대화 + 계산 결과]
계산 결과: 61
LLM 출력: output,61
→ 루프 종료!
```

##### "output" 도구의 역할

```python
# 프롬프트에 추가
"""
output: this tool ends the interaction. Use it when you have the final answer.
"""
```

**핵심**: LLM이 `output` 도구를 선택하면 루프 종료

---

#### 4. LangGraph로 Agent 구현

##### 설치

```bash
# Python
pip install duckduckgo-search

# JavaScript
npm i duck-duck-scrape expr-eval
```

##### 기본 Agent 구현

```python
import ast
from typing import Annotated, TypedDict

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Custom Tool 정의
@tool
def calculator(query: str) -> str:
    """A simple calculator tool. Input should be a mathematical expression."""
    return ast.literal_eval(query)

# 도구 설정
search = DuckDuckGoSearchRun()
tools = [search, calculator]
model = ChatOpenAI(temperature=0.1).bind_tools(tools)  # 도구 바인딩!

class State(TypedDict):
    messages: Annotated[list, add_messages]

def model_node(state: State) -> State:
    res = model.invoke(state["messages"])
    return {"messages": res}

# 그래프 구성
builder = StateGraph(State)
builder.add_node("model", model_node)
builder.add_node("tools", ToolNode(tools))      # 도구 실행 노드
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)  # 조건부 분기
builder.add_edge("tools", "model")              # 루프!

graph = builder.compile()
```

##### 그래프 구조

```
                    ┌──────────────────────┐
                    │                      │
                    ↓                      │
┌───────┐     ┌─────────┐            ┌─────────┐
│ START │ ──→ │  model  │ ─ ─ ─ ─ ─→ │  tools  │
└───────┘     └────┬────┘            └─────────┘
                   │
                   ↓ (tool_calls 없으면)
               ┌───────┐
               │  END  │
               └───────┘

(점선: Conditional Edge - tools_condition)
```

##### LangGraph 핵심 컴포넌트

| 컴포넌트 | 역할 |
|----------|------|
| **ToolNode** | AI 메시지의 tool_calls 실행, ToolMessage 반환, 예외 처리 포함 |
| **tools_condition** | 최신 AI 메시지에 tool_calls가 있으면 tools 노드로, 없으면 END |
| **bind_tools()** | 모델에 사용 가능한 도구 목록 바인딩 |

##### 실행 및 출력

```python
from langchain_core.messages import HumanMessage

input = {
    "messages": [
        HumanMessage("How old was the 30th president when he died?")
    ]
}
for c in graph.stream(input):
    print(c)
```

**출력:**
```python
# 1. model 노드: 검색 도구 호출 결정
{"model": {
    "messages": AIMessage(
        content="",
        tool_calls=[{
            "name": "duckduckgo_search",
            "args": {"query": "30th president of the United States age at death"},
            "id": "call_ZWRb...",
            "type": "tool_call"
        }]
    )
}}

# 2. tools 노드: 검색 실행
{"tools": {
    "messages": [
        ToolMessage(
            content="Calvin Coolidge (born July 4, 1872...died January 5, 1933)...",
            name="duckduckgo_search",
            tool_call_id="call_ZWRb..."
        )
    ]
}}

# 3. model 노드: 최종 답변 (tool_calls 없음 → 종료)
{"model": {
    "messages": AIMessage(
        content="Calvin Coolidge...died at the age of 60."
    )
}}
```

##### 루프의 핵심

```
model ──→ tools ──→ model ──→ tools ──→ ... ──→ model ──→ END
  │         │         │         │               │
  └─────────┴─────────┴─────────┴───────────────┘
           LLM이 tool_calls를 반환하는 동안 계속

           tool_calls가 없으면 → END
```

---

#### 5. 확장 패턴 #1: 특정 도구 우선 호출

##### 왜 필요한가?

| 장점 | 설명 |
|------|------|
| **지연 시간 감소** | 첫 LLM 호출 생략 |
| **일관성 보장** | 항상 특정 도구로 시작 |
| **오류 방지** | LLM이 잘못 판단하는 경우 방지 |

##### 단점

- 규칙이 명확하지 않은 경우 오히려 성능 저하

##### 구현

```python
from uuid import uuid4
from langchain_core.messages import AIMessage, ToolCall

def first_model(state: State) -> State:
    """LLM 호출 없이 직접 검색 도구 호출 생성"""
    query = state["messages"][-1].content
    search_tool_call = ToolCall(
        name="duckduckgo_search",
        args={"query": query},
        id=uuid4().hex
    )
    return {"messages": AIMessage(content="", tool_calls=[search_tool_call])}

# 그래프 구성
builder = StateGraph(State)
builder.add_node("first_model", first_model)  # LLM 없이 도구 호출
builder.add_node("model", model_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "first_model")         # 시작 → first_model
builder.add_edge("first_model", "tools")       # first_model → tools
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools", "model")

graph = builder.compile()
```

##### 그래프 구조

```
┌───────┐     ┌─────────────┐     ┌─────────┐     ┌─────────┐
│ START │ ──→ │ first_model │ ──→ │  tools  │ ──→ │  model  │
└───────┘     └─────────────┘     └─────────┘     └────┬────┘
                  (LLM 없음)                           │
                                                       ↓
                                               ┌───────────────┐
                                               │ tools_condition│
                                               └───────────────┘
                                                  │         │
                                                  ↓         ↓
                                               tools       END
```

##### 차이점

| 기본 Agent | 도구 우선 호출 |
|------------|----------------|
| START → model → tools → model → ... | START → first_model → tools → model → ... |
| 첫 LLM 호출로 도구 선택 | 직접 도구 호출 생성 (LLM 없음) |

---

#### 6. 확장 패턴 #2: 다중 도구 처리 (RAG 기반)

##### 문제: 도구가 많으면 성능 저하

```
도구 수 증가 → LLM의 도구 선택 정확도 ↓ (특히 10개 이상)
```

##### 해결책: RAG로 관련 도구 사전 선택

```
┌─────────────────────────────────────────────────────────────┐
│                   Tool Selection via RAG                     │
│                                                             │
│  사용자 쿼리 → 벡터 검색 → 관련 도구 k개 선택 → LLM에 전달  │
│                                                             │
│  전체 도구: [A, B, C, D, E, F, G, H, I, J] (10개)           │
│                      ↓                                      │
│  선택된 도구: [B, E] (2개)  ← 쿼리와 가장 관련있는 도구     │
│                      ↓                                      │
│  LLM은 2개 도구 중에서만 선택                               │
└─────────────────────────────────────────────────────────────┘
```

##### 장점

| 항목 | 설명 |
|------|------|
| **성능 향상** | 선택지 감소로 정확도 증가 |
| **비용 절감** | 프롬프트 길이 감소 |

##### 단점

| 항목 | 설명 |
|------|------|
| **지연 시간 증가** | RAG 단계 추가 |
| **적용 시점** | 도구 추가 후 성능 저하가 관찰될 때만 |

##### 구현

```python
from langchain_core.documents import Document
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

# 도구 설명을 벡터 저장소에 인덱싱
embeddings = OpenAIEmbeddings()
tools_retriever = InMemoryVectorStore.from_documents(
    [Document(tool.description, metadata={"name": tool.name}) for tool in tools],
    embeddings,
).as_retriever()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    selected_tools: list[str]  # 선택된 도구 이름

def select_tools(state: State) -> State:
    """쿼리와 가장 관련있는 도구 선택"""
    query = state["messages"][-1].content
    tool_docs = tools_retriever.invoke(query)
    return {"selected_tools": [doc.metadata["name"] for doc in tool_docs]}

def model_node(state: State) -> State:
    """선택된 도구만 바인딩"""
    selected_tools = [
        tool for tool in tools if tool.name in state["selected_tools"]
    ]
    res = model.bind_tools(selected_tools).invoke(state["messages"])
    return {"messages": res}

# 그래프 구성
builder = StateGraph(State)
builder.add_node("select_tools", select_tools)
builder.add_node("model", model_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "select_tools")        # 시작 → 도구 선택
builder.add_edge("select_tools", "model")      # 도구 선택 → model
builder.add_conditional_edges("model", tools_condition)
builder.add_edge("tools", "model")

graph = builder.compile()
```

##### 그래프 구조

```
┌───────┐     ┌──────────────┐     ┌─────────┐
│ START │ ──→ │ select_tools │ ──→ │  model  │
└───────┘     └──────────────┘     └────┬────┘
                   (RAG)                 │
                                         ↓
                                 ┌───────────────┐
                                 │ tools_condition│
                                 └───────────────┘
                                    │         │
                                    ↓         ↓
                                 tools       END
                                    │
                                    └──→ model
```

##### 출력 예시

```python
# 1. 도구 선택
{"select_tools": {
    "selected_tools": ["duckduckgo_search", "calculator"]
}}

# 2. model (선택된 도구만 사용)
{"model": {
    "messages": AIMessage(
        tool_calls=[{"name": "duckduckgo_search", ...}]
    )
}}

# 3. tools
{"tools": {"messages": [ToolMessage(...)]}}

# 4. model (최종 답변)
{"model": {"messages": AIMessage(content="...")}}
```

---

### 🔍 심화 학습

#### Agent vs Router 비교

| 특성 | Router | Agent |
|------|--------|-------|
| **루프** | 없음 (단일 분기) | 있음 (반복 실행) |
| **종료 조건** | 개발자 정의 | LLM 결정 |
| **도구 호출 수** | 최대 1회 | 다회 가능 |
| **자율성** | 낮음 | 높음 |

#### Custom Tool 작성 패턴

```python
from langchain_core.tools import tool

# 패턴 1: 데코레이터 사용
@tool
def my_tool(query: str) -> str:
    """Tool description for LLM."""  # docstring이 설명이 됨
    return process(query)

# 패턴 2: StructuredTool (복잡한 입력)
from langchain_core.tools import StructuredTool
from pydantic import BaseModel

class MyInput(BaseModel):
    query: str
    limit: int = 10

def my_func(query: str, limit: int) -> str:
    return process(query, limit)

my_tool = StructuredTool.from_function(
    func=my_func,
    name="my_tool",
    description="...",
    args_schema=MyInput
)
```

#### ToolNode 예외 처리

```
도구 실행 중 예외 발생 시:
├─ ToolNode가 예외 메시지를 ToolMessage로 변환
├─ LLM에게 전달
└─ LLM이 다음 행동 결정 (재시도, 다른 도구, 포기 등)
```

#### 도구 선택 전략 비교

| 전략 | 장점 | 단점 | 적합한 상황 |
|------|------|------|-------------|
| **전체 전달** | 구현 간단 | 성능 저하 (10개+) | 도구 수 적을 때 |
| **RAG 선택** | 성능 유지 | 지연 시간 | 도구 수 많을 때 |
| **카테고리 분류** | 체계적 | 복잡 | 도메인이 명확할 때 |

---

### 💡 실무 적용 포인트

1. **시작은 단순하게**: 기본 Agent로 시작, 필요시 확장
2. **Temperature 0.1**: 도구 선택은 일관성이 중요
3. **도구 설명 중요**: LLM이 도구 설명을 보고 선택함
4. **예외 처리 확인**: ToolNode의 기본 예외 처리 활용
5. **도구 수 모니터링**: 10개 이상 시 RAG 선택 고려
6. **우선 호출 패턴**: 명확한 규칙 있을 때만 적용
7. **스트리밍 디버깅**: 각 노드 출력으로 흐름 파악

---

### ✅ 정리 체크리스트

- [ ] Agent의 정의("행동하는 무언가")와 세 가지 조건을 안다
- [ ] Tool Calling과 Chain-of-Thought의 역할을 설명할 수 있다
- [ ] Plan-Do Loop(ReAct)의 동작 원리를 안다
- [ ] LLM이 루프 종료를 결정하는 방식을 이해한다
- [ ] LangGraph로 기본 Agent를 구현할 수 있다
- [ ] `bind_tools()`, `ToolNode`, `tools_condition`의 역할을 안다
- [ ] @tool 데코레이터로 커스텀 도구를 만들 수 있다
- [ ] 특정 도구 우선 호출 패턴을 구현할 수 있다
- [ ] RAG 기반 도구 선택 패턴을 구현할 수 있다
- [ ] 각 확장 패턴의 장단점과 적용 시점을 안다

---

### 🔗 참고 자료

- *LangChain for LLM Application Development* (책 제목 가정)
- Stuart Russell & Peter Norvig, *Artificial Intelligence: A Modern Approach* (Pearson, 2020)
- Shunyu Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", arXiv, 2022
- [LangGraph Agent Documentation](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/)
- [LangChain Tools](https://python.langchain.com/docs/how_to/#tools)
- [DuckDuckGo Search Tool](https://python.langchain.com/docs/integrations/tools/ddg/)
