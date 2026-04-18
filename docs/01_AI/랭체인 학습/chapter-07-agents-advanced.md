# Chapter 7. Agent 아키텍처 확장 (Agents II)

---

### 📌 핵심 요약
> Agent 아키텍처의 두 가지 강력한 확장: **Reflection**과 **Multi-Agent**. **Reflection**은 생성(Generate)과 비평(Reflect) 루프를 통해 출력 품질을 개선하며, 인간의 **System 2 사고**(숙고적 사고)를 모방한다. **Multi-Agent**는 복잡한 문제를 여러 전문 에이전트로 분할하여 해결하며, **Supervisor 아키텍처**가 가장 균형 잡힌 접근법이다. LangGraph의 **Subgraph** 기능이 이러한 확장을 가능하게 한다.

---

### 🎯 학습 목표
- Reflection 패턴의 원리와 구현 방법을 이해한다
- System 1과 System 2 사고의 차이를 설명할 수 있다
- LangGraph Subgraph의 두 가지 사용 방식을 안다
- Multi-Agent 아키텍처의 네 가지 유형을 구분할 수 있다
- Supervisor 아키텍처를 LangGraph로 구현할 수 있다

---

### 📖 본문 정리

#### 1. Reflection (Self-Critique)

##### 개념

> **Reflection**: 생성자(Creator) 프롬프트와 비평자(Reviser) 프롬프트 간의 **반복 루프**

```
┌─────────────────────────────────────────────────────────────┐
│                    Reflection Loop                           │
│                                                             │
│   ┌──────────┐        비평        ┌──────────┐             │
│   │ Generate │ ←─────────────── │  Reflect  │             │
│   │ (생성)   │                    │  (비평)   │             │
│   └────┬─────┘                    └────┬─────┘             │
│        │                               ↑                    │
│        └───────────────────────────────┘                    │
│                  초안 → 피드백 → 수정 → 피드백 → ...         │
└─────────────────────────────────────────────────────────────┘
```

##### System 1 vs System 2 사고

> *Daniel Kahneman, "Thinking, Fast and Slow" (2011)*

| 특성 | System 1 | System 2 |
|------|----------|----------|
| **특징** | 반응적, 본능적 | 체계적, 숙고적 |
| **속도** | 빠름 | 느림 |
| **노력** | 적음 | 많음 |
| **LLM 대응** | 단일 응답 | Reflection 루프 |

```
System 1: 질문 → 즉각적 답변 (직관)
System 2: 질문 → 초안 → 검토 → 수정 → 검토 → ... → 최종 답변 (숙고)
```

##### LangGraph 구현

```python
from typing import Annotated, TypedDict
from langchain_core.messages import (
    AIMessage, BaseMessage, HumanMessage, SystemMessage
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

model = ChatOpenAI()

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 생성 노드: 에세이 작성/수정
generate_prompt = SystemMessage(
    """You are an essay assistant tasked with writing excellent 3-paragraph essays.
    Generate the best essay possible for the user's request.
    If the user provides critique, respond with a revised version."""
)

def generate(state: State) -> State:
    answer = model.invoke([generate_prompt] + state["messages"])
    return {"messages": [answer]}

# 비평 노드: 에세이 평가
reflection_prompt = SystemMessage(
    """You are a teacher grading an essay submission.
    Generate critique and recommendations for the user's submission.
    Provide detailed recommendations, including length, depth, style, etc."""
)

def reflect(state: State) -> State:
    # 메시지 역할 교환: AI ↔ Human
    cls_map = {AIMessage: HumanMessage, HumanMessage: AIMessage}

    # 첫 메시지(원본 요청)는 유지, 나머지는 역할 교환
    translated = [reflection_prompt, state["messages"][0]] + [
        cls_map[msg.__class__](content=msg.content)
        for msg in state["messages"][1:]
    ]

    answer = model.invoke(translated)
    # 비평을 Human 피드백으로 변환하여 생성자에게 전달
    return {"messages": [HumanMessage(content=answer.content)]}

# 종료 조건: 3회 반복 후 종료
def should_continue(state: State):
    if len(state["messages"]) > 6:  # 3 iterations × 2 messages
        return END
    else:
        return "reflect"

# 그래프 구성
builder = StateGraph(State)
builder.add_node("generate", generate)
builder.add_node("reflect", reflect)
builder.add_edge(START, "generate")
builder.add_conditional_edges("generate", should_continue)
builder.add_edge("reflect", "generate")

graph = builder.compile()
```

##### 그래프 구조

```
┌───────┐     ┌──────────┐
│ START │ ──→ │ generate │ ←───────┐
└───────┘     └────┬─────┘         │
                   │               │
                   ↓               │
           ┌──────────────┐        │
           │should_continue│        │
           └──────────────┘        │
              │         │          │
              ↓         ↓          │
           ┌─────┐  ┌─────────┐    │
           │ END │  │ reflect │ ───┘
           └─────┘  └─────────┘
```

##### 메시지 역할 교환의 이유

```
문제: 대화형 LLM은 Human-AI 메시지 쌍으로 학습됨
      → 같은 역할의 연속 메시지는 성능 저하

해결: 역할 교환으로 자연스러운 대화 구조 유지

Generate 관점:
  Human(원본 요청) → AI(초안) → Human(비평) → AI(수정) → ...

Reflect 관점:
  Human(원본 요청) → Human(에세이) → AI(비평)
  (AI가 쓴 에세이를 학생이 쓴 것처럼 위장)
```

##### 비평 출력 예시

```
"Your essay on 'The Little Prince' is well-written and insightful.
However, there are areas for improvement:

1. **Depth**: Delve deeper into each theme with specific examples.
2. **Analysis**: Apply the book's messages to current societal issues.
3. **Length**: Expand with more examples and counterarguments.
4. **Style**: Incorporate quotes and anecdotes for engagement.
5. **Conclusion**: Summarize the enduring significance."
```

##### Reflection 변형 패턴

| 변형 | 설명 | 장점 |
|------|------|------|
| **고정 반복** | N회 후 종료 | 예측 가능한 비용/지연 |
| **비평자 결정** | Reflect가 종료 판단 | 품질 기반 종료 |
| **Agent 결합** | 최종 출력 전 Reflection | 자동 품질 개선 |
| **외부 검증** | 린터/컴파일러 결과로 비평 | 객관적 피드백 |

##### 외부 검증과 결합 (권장)

```
코드 생성 Agent의 경우:
generate → 코드 실행/린터 → reflect → generate → ...

┌──────────┐     ┌────────────┐     ┌─────────┐
│ generate │ ──→ │ 린터/테스트 │ ──→ │ reflect │
└──────────┘     └────────────┘     └─────────┘
                    에러 정보를
                   비평에 포함
```

---

#### 2. LangGraph Subgraph

##### Subgraph란?

> 다른 그래프의 **일부로 사용되는 그래프**

##### 사용 사례

| 사례 | 설명 |
|------|------|
| **Multi-Agent** | 각 Agent를 독립 그래프로 구성 |
| **재사용** | 공통 노드 집합을 여러 그래프에서 재사용 |
| **팀 협업** | 팀별로 독립적인 서브그래프 개발 |

##### 방식 1: 직접 호출 (공유 상태 키)

```python
from langgraph.graph import START, StateGraph
from typing import TypedDict

# 부모 그래프 상태
class State(TypedDict):
    foo: str  # 공유 키

# 서브그래프 상태
class SubgraphState(TypedDict):
    foo: str  # 공유 키 (같은 이름!)
    bar: str  # 서브그래프 내부 키

# 서브그래프 정의
def subgraph_node(state: SubgraphState):
    return {"foo": state["foo"] + "bar"}  # 공유 키 수정

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node)
# ... 추가 설정
subgraph = subgraph_builder.compile()

# 부모 그래프에 직접 추가
builder = StateGraph(State)
builder.add_node("subgraph", subgraph)  # 컴파일된 그래프를 노드로!
# ... 추가 설정
graph = builder.compile()
```

##### 직접 호출의 규칙

```
부모: {foo, baz}
서브: {foo, bar}

전달: foo (공유 키만)
무시: baz (부모 전용), bar (서브 전용)

통신은 공유 키를 통해서만!
```

##### 방식 2: 함수로 감싸서 호출 (다른 상태 스키마)

```python
# 부모 그래프 상태
class State(TypedDict):
    foo: str

# 서브그래프 상태 (완전히 다른 키!)
class SubgraphState(TypedDict):
    bar: str
    baz: str

# 서브그래프 정의
def subgraph_node(state: SubgraphState):
    return {"bar": state["bar"] + "baz"}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node)
subgraph = subgraph_builder.compile()

# 래퍼 함수로 상태 변환
def node(state: State):
    # 부모 → 서브그래프 상태 변환
    response = subgraph.invoke({"bar": state["foo"]})
    # 서브그래프 → 부모 상태 변환
    return {"foo": response["bar"]}

# 래퍼 함수를 노드로 추가
builder = StateGraph(State)
builder.add_node(node)  # 함수를 노드로!
graph = builder.compile()
```

##### 두 방식 비교

| 특성 | 직접 호출 | 함수 래핑 |
|------|-----------|-----------|
| **상태 스키마** | 공유 키 필요 | 완전히 다를 수 있음 |
| **변환** | 불필요 | 입출력 변환 필요 |
| **복잡도** | 낮음 | 높음 |
| **유연성** | 낮음 | 높음 |

---

#### 3. Multi-Agent 아키텍처

##### 왜 Multi-Agent인가?

| 문제 | 설명 |
|------|------|
| **도구 과다** | 선택지가 많으면 결정 품질 저하 |
| **컨텍스트 복잡성** | 단일 Agent가 추적하기 어려움 |
| **전문화 필요** | 계획, 연구, 수학 등 특화 영역 |

##### 네 가지 연결 방식

```
1. Network (네트워크)
   ┌───┐    ┌───┐
   │ A │ ↔ │ B │
   └─┬─┘    └─┬─┘
     │   ↘↗   │
     ↓        ↓
   ┌───┐    ┌───┐
   │ C │ ↔ │ D │
   └───┘    └───┘
   → 모든 Agent가 서로 통신

2. Supervisor (감독자)
        ┌────────────┐
        │ Supervisor │
        └─────┬──────┘
          ↙   │   ↘
       ┌───┐ ┌───┐ ┌───┐
       │ A │ │ B │ │ C │
       └───┘ └───┘ └───┘
   → 중앙 감독자가 라우팅

3. Hierarchical (계층적)
          ┌────────────┐
          │  Top Sup   │
          └─────┬──────┘
            ↙       ↘
    ┌─────────┐  ┌─────────┐
    │ Sub Sup │  │ Sub Sup │
    └────┬────┘  └────┬────┘
      ↙   ↘        ↙   ↘
    ┌──┐ ┌──┐    ┌──┐ ┌──┐
    │A │ │B │    │C │ │D │
    └──┘ └──┘    └──┘ └──┘
   → 감독자의 감독자

4. Custom Workflow (커스텀)
   ┌───┐ ──→ ┌───┐
   │ A │     │ B │ ─┐
   └───┘     └─┬─┘  │
               ↓    ↓
             ┌───┐ ┌───┐
             │ C │ │ D │
             └───┘ └───┘
   → 일부만 결정권, 나머지는 고정
```

##### 각 방식의 특징

| 방식 | 장점 | 단점 | 적합한 경우 |
|------|------|------|-------------|
| **Network** | 유연성 최대 | 복잡, 예측 어려움 | 동등한 Agent들 |
| **Supervisor** | 균형 잡힘 | 감독자 병목 | 일반적 추천 |
| **Hierarchical** | 대규모 확장 | 매우 복잡 | 복잡한 조직 |
| **Custom** | 맞춤 최적화 | 설계 어려움 | 특정 워크플로우 |

---

#### 4. Supervisor 아키텍처 구현

##### Supervisor 노드

```python
from typing import Literal
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# 구조화된 출력 스키마
class SupervisorDecision(BaseModel):
    next: Literal["researcher", "coder", "FINISH"]

model = ChatOpenAI(model="gpt-4o", temperature=0)
model = model.with_structured_output(SupervisorDecision)

agents = ["researcher", "coder"]

system_prompt_part_1 = f"""You are a supervisor managing these workers: {agents}.
Given the user request, respond with the worker to act next.
Each worker will perform a task and respond with results.
When finished, respond with FINISH."""

system_prompt_part_2 = f"""Who should act next? Or FINISH?
Select one of: {', '.join(agents)}, FINISH"""

def supervisor(state):
    messages = [
        ("system", system_prompt_part_1),
        *state["messages"],
        ("system", system_prompt_part_2)
    ]
    return model.invoke(messages)
```

##### 전체 그래프 구성

```python
from langgraph.graph import StateGraph, MessagesState, START

class AgentState(BaseModel):
    next: Literal["researcher", "coder", "FINISH"]

def researcher(state: AgentState):
    response = model.invoke(...)  # 연구 작업
    return {"messages": [response]}

def coder(state: AgentState):
    response = model.invoke(...)  # 코딩 작업
    return {"messages": [response]}

# 그래프 구성
builder = StateGraph(AgentState)
builder.add_node(supervisor)
builder.add_node(researcher)
builder.add_node(coder)

builder.add_edge(START, "supervisor")
# Supervisor 결정에 따라 라우팅
builder.add_conditional_edges("supervisor", lambda state: state["next"])
builder.add_edge("researcher", "supervisor")
builder.add_edge("coder", "supervisor")

supervisor_graph = builder.compile()
```

##### 그래프 구조

```
                     ┌────────────┐
       ┌─────────────│ supervisor │←─────────────┐
       │             └─────┬──────┘              │
       │                   │                     │
       ↓                   ↓                     │
┌────────────┐      ┌────────────┐        ┌───────────┐
│ researcher │ ─────│ conditional│────────│   coder   │
└────────────┘      │   edges    │        └───────────┘
       │            └──────┬─────┘              │
       │                   │                    │
       └───────────────────┼────────────────────┘
                           ↓
                       ┌───────┐
                       │ FINISH │
                       └───────┘
```

##### 실행 흐름 예시

```
사용자: "Python으로 웹 스크래퍼 만들어줘"

1. supervisor → "coder" 선택
2. coder → 코드 작성 후 supervisor로 복귀
3. supervisor → "FINISH" 선택 (또는 추가 작업 필요시 다른 Agent)
4. 종료
```

##### 설계 고려사항

| 고려사항 | 설명 |
|----------|------|
| **Agent 이름** | 자기 설명적이어야 함 (`agent_1` ❌, `researcher` ✅) |
| **상태 공유** | 모든 Agent가 messages를 공유 |
| **독립 상태** | 내부 상태 유지 후 요약만 출력 가능 |
| **라우팅** | 감독자 복귀 또는 Agent가 직접 종료 결정 |

---

### 🔍 심화 학습

#### Reflection 적용 시점

```
권장 적용 시점:
├─ 창작물 생성 (에세이, 코드, 디자인)
├─ 복잡한 추론이 필요한 작업
├─ 품질이 중요한 최종 출력
└─ 외부 검증 도구가 있는 경우 (린터, 테스트)

주의 사항:
├─ 지연 시간 증가 (반복 횟수 × LLM 호출)
├─ 비용 증가
└─ 무한 루프 방지 필요 (고정 횟수 또는 품질 기준)
```

#### Multi-Agent vs Single Agent

| 특성 | Single Agent | Multi-Agent |
|------|-------------|-------------|
| **복잡도** | 낮음 | 높음 |
| **디버깅** | 쉬움 | 어려움 |
| **확장성** | 제한적 | 높음 |
| **적용** | 단순 작업 | 복잡한 도메인 |

**권장**: 단순 Agent로 시작 → 문제 발생 시 Multi-Agent 전환

#### Supervisor 프롬프트 최적화

```python
# Agent 설명 추가 (이름이 불명확할 때)
agents_with_desc = {
    "researcher": "Web search and information gathering",
    "coder": "Python code writing and debugging",
    "reviewer": "Code review and quality assurance"
}

system_prompt = f"""You are a supervisor managing these workers:
{chr(10).join(f'- {name}: {desc}' for name, desc in agents_with_desc.items())}

Given the user request, select the most appropriate worker."""
```

---

### 💡 실무 적용 포인트

1. **단순 시작**: Chapter 6의 기본 Agent로 시작
2. **Reflection 선택적 적용**: 품질이 중요한 최종 출력에만
3. **외부 검증 결합**: 가능하면 린터/테스트 결과를 Reflection에 활용
4. **고정 반복 권장**: 무한 루프 방지를 위해 최대 반복 횟수 설정
5. **Supervisor 우선**: Multi-Agent 필요시 Supervisor 아키텍처부터
6. **Agent 이름**: 자기 설명적인 이름 사용 (`data_analyst`, `code_reviewer` 등)
7. **상태 공유 범위**: messages 공유 vs 독립 상태 후 요약 중 선택

---

### ✅ 정리 체크리스트

- [ ] Reflection 패턴이 System 2 사고를 모방한다는 것을 안다
- [ ] Generate-Reflect 루프를 LangGraph로 구현할 수 있다
- [ ] 메시지 역할 교환(AI ↔ Human)의 이유를 설명할 수 있다
- [ ] 외부 검증과 Reflection을 결합하는 방법을 안다
- [ ] Subgraph의 두 가지 사용 방식(직접/함수 래핑)을 구분할 수 있다
- [ ] 공유 키를 통한 부모-서브그래프 통신을 이해한다
- [ ] Multi-Agent의 네 가지 연결 방식을 구분할 수 있다
- [ ] Supervisor 아키텍처를 LangGraph로 구현할 수 있다
- [ ] `with_structured_output`으로 Supervisor 결정을 구조화할 수 있다
- [ ] 각 확장 패턴의 적용 시점과 주의사항을 안다

---

### 🔗 참고 자료

- *LangChain for LLM Application Development* (책 제목 가정)
- Daniel Kahneman, *Thinking, Fast and Slow* (Farrar, Straus and Giroux, 2011)
- [LangGraph Subgraphs](https://langchain-ai.github.io/langgraph/concepts/low_level/#subgraphs)
- [LangGraph Multi-Agent](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- [LangGraph Reflection Example](https://langchain-ai.github.io/langgraph/tutorials/reflection/reflection/)
