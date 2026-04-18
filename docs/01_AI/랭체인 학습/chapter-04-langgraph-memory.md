# Chapter 4. LangGraph로 챗봇에 메모리 추가하기 (Using LangGraph to Add Memory)

---

### 📌 핵심 요약
> LLM은 **Stateless**(무상태)하여 이전 대화를 기억하지 못한다. 프로덕션 수준의 챗봇을 만들려면 대화 히스토리를 저장하고 프롬프트에 포함시키는 **메모리 시스템**이 필수다. **LangGraph**는 멀티 액터, 멀티 스텝, 상태 기반 인지 아키텍처를 구현하기 위한 오픈소스 라이브러리로, **StateGraph**와 **Checkpointer**를 통해 대화 상태를 자동으로 관리한다. 메모리가 커질수록 **trim_messages**, **filter_messages**, **merge_message_runs**로 채팅 히스토리를 최적화해야 한다.

---

### 🎯 학습 목표
- LLM이 Stateless한 이유와 메모리 시스템의 필요성을 이해한다
- LangGraph의 핵심 개념(State, Nodes, Edges)을 설명할 수 있다
- StateGraph와 Checkpointer로 메모리를 구현할 수 있다
- Thread를 활용한 다중 사용자 대화 관리 방법을 안다
- 채팅 히스토리 수정 전략(Trim, Filter, Merge)을 적용할 수 있다

---

### 📖 본문 정리

#### 1. 왜 메모리 시스템이 필요한가?

##### LLM의 Stateless 특성

```
LLM 호출 1: "안녕, 나는 Jack이야"
    ↓
LLM 응답: "안녕하세요 Jack님!"

LLM 호출 2: "내 이름이 뭐지?" (이전 컨텍스트 없음)
    ↓
LLM 응답: "죄송합니다, 이름을 알 수 없습니다" ❌
```

**문제점**: LLM은 매 호출마다 이전 프롬프트나 응답을 기억하지 못함

##### 메모리 시스템의 역할

```
┌─────────────────────────────────────────────────────┐
│                    Memory System                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ Chat History:                                │   │
│  │ - Human: "안녕, 나는 Jack이야"              │   │
│  │ - AI: "안녕하세요 Jack님!"                  │   │
│  │ - Human: "내 이름이 뭐지?"                  │   │
│  └─────────────────────────────────────────────┘   │
│                        ↓                            │
│              프롬프트에 히스토리 포함                │
│                        ↓                            │
│              LLM: "당신의 이름은 Jack입니다" ✅     │
└─────────────────────────────────────────────────────┘
```

##### 메모리 시스템의 두 가지 핵심 설계 결정

| 결정 사항 | 설명 |
|-----------|------|
| **State 저장 방식** | 어디에, 어떤 형태로 대화 내용을 저장할 것인가 |
| **State 조회 방식** | 언제, 어떻게 저장된 대화를 가져올 것인가 |

---

#### 2. 간단한 메모리 시스템 구현

##### Placeholder를 활용한 Chat History 주입

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("placeholder", "{messages}"),  # 여기에 히스토리 주입
])

model = ChatOpenAI()
chain = prompt | model

# 수동으로 히스토리 전달
chain.invoke({
    "messages": [
        ("human", "Translate to French: I love programming."),
        ("ai", "J'adore programmer."),
        ("human", "What did you just say?"),
    ],
})
# 출력: "I said 'J'adore programmer,' which means 'I love programming' in French."
```

##### 프로덕션 환경의 과제

| 과제 | 설명 |
|------|------|
| **원자적 업데이트** | 질문/답변 중 하나만 기록되는 실패 방지 |
| **영구 저장소** | 관계형 DB 등 내구성 있는 저장소 필요 |
| **메시지 제어** | 저장할 메시지 수, 사용할 메시지 수 관리 |
| **상태 검사/수정** | LLM 호출 외부에서 상태 조회 및 변경 |

---

#### 3. LangGraph 소개

##### LangGraph란?

LangChain이 만든 오픈소스 라이브러리로, **멀티 액터**, **멀티 스텝**, **상태 기반** 인지 아키텍처를 구현

```
LangGraph의 세 가지 특성:
├─ Multi-Actor: 여러 전문가(LLM, 검색엔진 등)가 협력
├─ Multi-Step: 액터 간 작업 전달이 시간 순서대로 진행
└─ Stateful: 중앙 상태를 통해 스텝 간 통신
```

##### Multi-Actor (다중 액터)

```
단일 액터                    다중 액터
┌───────┐                ┌───────┐   ┌───────┐
│  LLM  │       →        │  LLM  │ ↔ │Search │
└───────┘                └───────┘   └───────┘
                              ↓
                         더 강력한 결과
```

**예시**: Perplexity, Arc Search - LLM + 검색 엔진 조합

##### Multi-Step (다중 스텝)

```
Step 1: LLM → "최신 뉴스 검색해줘"
    ↓
Step 2: Search Tool → 검색 결과 반환
    ↓
Step 3: LLM → 결과 요약 및 응답 생성
    ↓
Step 4: END (더 이상 작업 없음)
```

##### Stateful (상태 기반)

```
┌─────────────────────────────────────┐
│         Central State               │
│  ┌─────────────────────────────┐   │
│  │ messages: [...]              │   │
│  │ context: {...}               │   │
│  └─────────────────────────────┘   │
│       ↑         ↑         ↑        │
│    Node A    Node B    Node C      │
│   (읽기/쓰기) (읽기/쓰기) (읽기/쓰기) │
└─────────────────────────────────────┘
```

**장점**:
- 각 스텝에서 상태 스냅샷 저장 가능
- 실행 일시 정지/재개, 에러 복구 용이
- Human-in-the-loop 제어 구현 가능

---

#### 4. LangGraph 핵심 구성 요소

##### Graph의 세 가지 구성 요소

| 구성 요소 | 설명 | 예시 |
|-----------|------|------|
| **State** | 애플리케이션이 받고/수정/생성하는 데이터 | `{messages: [...]}` |
| **Nodes** | 실행할 각 스텝 (Python/JS 함수) | `chatbot`, `search_tool` |
| **Edges** | 노드 간 연결 (고정/조건부) | `START → chatbot → END` |

##### 설치

```bash
# Python
pip install langgraph

# JavaScript
npm i @langchain/langgraph
```

---

#### 5. StateGraph 생성하기

##### Step 1: State 정의

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    # add_messages: 기존 리스트에 새 메시지 추가 (덮어쓰기 X)
    messages: Annotated[list, add_messages]

builder = StateGraph(State)
```

```javascript
import { StateGraph, Annotation, messagesStateReducer, START, END }
  from '@langchain/langgraph'

const State = {
  messages: Annotation({
    reducer: messagesStateReducer,  // 메시지 추가 리듀서
    default: () => []
  }),
}

const builder = new StateGraph(State)
```

##### Reducer 함수 이해

```
Reducer 동작:
├─ 입력: (현재 상태, 새 값)
├─ 출력: 병합된 다음 상태
└─ add_messages: 새 메시지를 기존 리스트에 추가

기존 상태: [msg1, msg2]
새 값: [msg3]
결과: [msg1, msg2, msg3]  (덮어쓰기가 아닌 추가)
```

##### Step 2: Node 추가

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI()

def chatbot(state: State):
    answer = model.invoke(state["messages"])
    return {"messages": [answer]}  # 상태 업데이트 반환

builder.add_node("chatbot", chatbot)
```

##### Step 3: Edge 추가 및 컴파일

```python
builder.add_edge(START, 'chatbot')  # 시작점 연결
builder.add_edge('chatbot', END)    # 종료점 연결

graph = builder.compile()  # 실행 가능한 객체로 컴파일
```

##### 그래프 시각화

```python
graph.get_graph().draw_mermaid_png()
```

```
┌───────┐     ┌─────────┐     ┌─────┐
│ START │ ──→ │ chatbot │ ──→ │ END │
└───────┘     └─────────┘     └─────┘
```

##### 실행하기

```python
from langchain_core.messages import HumanMessage

input = {"messages": [HumanMessage("hi!")]}
for chunk in graph.stream(input):
    print(chunk)

# 출력: {"chatbot": {"messages": [AIMessage("How can I help you?")]}}
```

---

#### 6. StateGraph에 메모리 추가하기

##### Checkpointer 적용

```python
from langgraph.checkpoint.memory import MemorySaver

# Checkpointer와 함께 컴파일
graph = builder.compile(checkpointer=MemorySaver())
```

```javascript
import { MemorySaver } from '@langchain/langgraph'

const graph = builder.compile({ checkpointer: new MemorySaver() })
```

##### LangGraph 제공 어댑터

| 어댑터 | 용도 | 적합한 환경 |
|--------|------|-------------|
| **MemorySaver** | 인메모리 저장 | 개발/테스트 |
| **SQLite** | 로컬 파일 DB | 로컬 앱, 테스트 |
| **Postgres** | 관계형 DB | 대규모 프로덕션 |
| (커뮤니티) | Redis, MySQL 등 | 특수 요구사항 |

##### Thread를 활용한 대화 관리

```python
# 스레드 식별자 정의 (보통 UUID 사용)
thread1 = {"configurable": {"thread_id": "1"}}

# 첫 번째 대화
result_1 = graph.invoke(
    {"messages": [HumanMessage("hi, my name is Jack!")]},
    thread1
)
# → {"messages": [AIMessage("How can I help you, Jack?")]}

# 두 번째 대화 (같은 스레드)
result_2 = graph.invoke(
    {"messages": [HumanMessage("what is my name?")]},
    thread1
)
# → {"messages": [AIMessage("Your name is Jack")]} ✅ 기억함!
```

##### Thread의 역할

```
Thread 1 (User A)              Thread 2 (User B)
┌─────────────────┐           ┌─────────────────┐
│ "나는 Jack이야"  │           │ "나는 Alice야"  │
│ "Jack님 안녕!"   │           │ "Alice님 안녕!" │
│ "내 이름은?"     │           │ "내 이름은?"    │
│ "Jack입니다"     │           │ "Alice입니다"   │
└─────────────────┘           └─────────────────┘
       ↓                              ↓
   독립적인 대화 히스토리 유지 (서로 섞이지 않음)
```

##### 상태 조회 및 수정

```python
# 현재 상태 조회
graph.get_state(thread1)

# 상태 업데이트 (메시지 추가)
graph.update_state(thread1, [HumanMessage("I like LLMs!")])
```

---

#### 7. 채팅 히스토리 수정하기

히스토리가 커질수록 최적화가 필요한 세 가지 전략:

```
Chat History 최적화:
├─ Trimming: 토큰 제한에 맞게 메시지 수 줄이기
├─ Filtering: 특정 조건의 메시지만 선택
└─ Merging: 연속된 같은 타입 메시지 합치기
```

##### 7.1 trim_messages (트리밍)

**문제**: LLM 컨텍스트 윈도우 제한 + 과도한 정보는 환각 유발

```python
from langchain_core.messages import SystemMessage, trim_messages
from langchain_openai import ChatOpenAI

trimmer = trim_messages(
    max_tokens=65,              # 최대 토큰 수
    strategy="last",            # 최신 메시지 우선 ("first"도 가능)
    token_counter=ChatOpenAI(model="gpt-4o"),  # 토큰 계산용 모델
    include_system=True,        # 시스템 메시지 유지
    allow_partial=False,        # 메시지 부분 잘림 허용 여부
    start_on="human",           # Human 메시지부터 시작 보장
)

messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="what's 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]

trimmed = trimmer.invoke(messages)
```

**결과**: 11개 → 7개 메시지로 축소 (시스템 메시지 유지)

```
[SystemMessage("you're a good assistant"),
 HumanMessage("what's 2 + 2"),
 AIMessage("4"),
 HumanMessage("thanks"),
 AIMessage("no problem!"),
 HumanMessage("having fun?"),
 AIMessage("yes!")]
```

##### trim_messages 파라미터

| 파라미터 | 설명 | 값 |
|----------|------|-----|
| `strategy` | 시작 방향 | `"last"` (최신 우선), `"first"` (오래된 우선) |
| `token_counter` | 토큰 계산용 모델 | ChatOpenAI 인스턴스 |
| `include_system` | 시스템 메시지 유지 | `True` / `False` |
| `allow_partial` | 부분 메시지 허용 | `True` / `False` |
| `start_on` | 시작 메시지 타입 | `"human"` (AI 없이 Human 삭제 방지) |

##### 7.2 filter_messages (필터링)

**용도**: 타입, ID, 이름으로 메시지 선택적 필터링

```python
from langchain_core.messages import filter_messages

messages = [
    SystemMessage("you are a good assistant", id="1"),
    HumanMessage("example input", id="2", name="example_user"),
    AIMessage("example output", id="3", name="example_assistant"),
    HumanMessage("real input", id="4", name="bob"),
    AIMessage("real output", id="5", name="alice"),
]

# Human 메시지만 필터링
filter_messages(messages, include_types="human")
# → [HumanMessage("example input"), HumanMessage("real input")]

# 특정 이름 제외
filter_messages(messages, exclude_names=["example_user", "example_assistant"])
# → [SystemMessage, HumanMessage("real input"), AIMessage("real output")]

# 타입 포함 + ID 제외 조합
filter_messages(messages, include_types=[HumanMessage, AIMessage], exclude_ids=["3"])
# → [HumanMessage("example input"), HumanMessage("real input"), AIMessage("real output")]
```

##### 체인에서 사용

```python
model = ChatOpenAI()
filter_ = filter_messages(exclude_names=["example_user", "example_assistant"])
chain = filter_ | model  # 선언형 조합
```

##### 7.3 merge_message_runs (병합)

**문제**: 일부 모델(Anthropic 등)은 연속된 같은 타입 메시지를 지원하지 않음

```python
from langchain_core.messages import merge_message_runs

messages = [
    SystemMessage("you're a good assistant."),
    SystemMessage("you always respond with a joke."),  # 연속 System
    HumanMessage([{"type": "text", "text": "why langchain?"}]),
    HumanMessage("and who is harrison?"),              # 연속 Human
    AIMessage("WordRope didn't have the same ring!"),
    AIMessage("He's chasing coffee!"),                 # 연속 AI
]

merged = merge_message_runs(messages)
```

**결과**: 6개 → 3개 메시지로 병합

```
[SystemMessage("you're a good assistant.\nyou always respond with a joke."),
 HumanMessage([{'type': 'text', 'text': "why langchain?"}, 'and who is harrison?']),
 AIMessage("WordRope didn't have the same ring!\nHe's chasing coffee!")]
```

##### 병합 규칙

| 콘텐츠 타입 | 병합 결과 |
|-------------|-----------|
| 둘 다 문자열 | `\n`으로 연결 |
| 하나가 리스트 | 리스트에 추가 |

##### 체인에서 사용

```python
model = ChatOpenAI()
merger = merge_message_runs()
chain = merger | model
```

---

### 🔍 심화 학습

#### LangGraph vs LangChain Expression Language (LCEL)

| 특성 | LCEL | LangGraph |
|------|------|-----------|
| **복잡도** | 단순 체인 | 복잡한 그래프 |
| **상태 관리** | 수동 | 자동 (Checkpointer) |
| **분기/반복** | 제한적 | 조건부 Edge로 유연 |
| **영속성** | 없음 | 내장 (Thread) |
| **Human-in-the-loop** | 어려움 | 쉬움 |

#### Checkpointer 선택 가이드

```
환경별 Checkpointer 선택:
├─ 개발/테스트: MemorySaver (인메모리)
├─ 로컬 앱: SQLite (파일 기반)
├─ 프로덕션: Postgres (확장성, 내구성)
└─ 특수 요구: Redis (캐시), MySQL (기존 인프라)
```

#### 토큰 최적화 전략

```
메모리 최적화 우선순위:
1. trim_messages: 토큰 제한 준수 (필수)
2. filter_messages: 불필요한 메시지 제거
3. merge_message_runs: 모델 호환성 보장

조합 예시:
messages → trim → filter → merge → model
```

---

### 💡 실무 적용 포인트

1. **Thread 기반 설계**: 다중 사용자 환경에서 `thread_id`로 대화 분리
2. **Checkpointer 선택**: 개발은 MemorySaver, 프로덕션은 Postgres
3. **토큰 관리**: `trim_messages`로 컨텍스트 윈도우 초과 방지
4. **시스템 메시지 보존**: `include_system=True`로 일관된 봇 성격 유지
5. **Human-AI 쌍 유지**: `start_on="human"`으로 대화 맥락 보존
6. **모델 호환성**: Anthropic 사용 시 `merge_message_runs` 적용
7. **상태 디버깅**: `get_state()`로 현재 상태 확인, `update_state()`로 수정

---

### ✅ 정리 체크리스트

- [ ] LLM이 Stateless한 이유와 메모리의 필요성을 안다
- [ ] LangGraph의 세 가지 특성(Multi-Actor, Multi-Step, Stateful)을 설명할 수 있다
- [ ] State, Nodes, Edges의 역할을 안다
- [ ] StateGraph를 생성하고 컴파일할 수 있다
- [ ] Checkpointer로 메모리를 추가하는 방법을 안다
- [ ] Thread를 활용해 다중 사용자 대화를 관리할 수 있다
- [ ] `get_state()`, `update_state()`로 상태를 조회/수정할 수 있다
- [ ] `trim_messages`의 파라미터(strategy, include_system, start_on)를 안다
- [ ] `filter_messages`로 타입/이름/ID 기반 필터링을 할 수 있다
- [ ] `merge_message_runs`로 연속 메시지를 병합할 수 있다
- [ ] 세 가지 히스토리 수정 전략을 체인에서 조합할 수 있다

---

### 🔗 참고 자료

- *LangChain for LLM Application Development* (책 제목 가정)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangChain Message Utilities](https://python.langchain.com/docs/how_to/#messages)
- [Checkpointer Adapters](https://langchain-ai.github.io/langgraph/concepts/persistence/)
