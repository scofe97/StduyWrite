# Chapter 8. LLM 활용 극대화 패턴 (Patterns to Make the Most of LLMs)

---

### 📌 핵심 요약
> LLM 애플리케이션의 성공은 **Agency(자율성)**와 **Reliability(신뢰성)** 사이의 균형에 달려 있다. 이 장에서는 LangGraph를 활용하여 **Structured Output**, **Streaming**, **Human-in-the-Loop**, **Multitasking** 등 실무에서 필수적인 패턴들을 다룬다. 특히 Human-in-the-Loop의 6가지 모달리티(Interrupt, Authorize, Resume, Restart, Edit State, Fork)를 통해 LLM의 자율성을 적절히 제어하고 신뢰성을 확보하는 방법을 학습한다.

---

### 🎯 학습 목표
- Agency-Reliability Frontier의 개념과 트레이드오프를 이해한다
- Structured Output으로 LLM 응답을 구조화하는 방법을 안다
- LangGraph의 Streaming 기능과 다양한 stream_mode를 활용할 수 있다
- Human-in-the-Loop의 6가지 모달리티를 구현할 수 있다
- Double Texting과 Multitasking 처리 전략을 이해한다

---

### 📖 본문 정리

#### 1. Agency-Reliability Frontier

##### 트레이드오프 개념

```
Agency vs Reliability 트레이드오프:

     Reliability (신뢰성)
          ↑
     높음 │  ┌────────────┐
          │  │ LLM Call   │ ← 가장 신뢰성 높음
          │  └────────────┘
          │      ┌────────────┐
          │      │  Chain     │
          │      └────────────┘
          │          ┌────────────┐
          │          │  Router    │
          │          └────────────┘
          │              ┌────────────┐
          │              │  Agent     │
          │              └────────────┘
          │                  ┌────────────┐
     낮음 │                  │Multi-Agent │ ← 가장 자율성 높음
          └──────────────────────────────────→ Agency (자율성)
                                           높음
```

| 아키텍처 | Agency | Reliability | 적합한 상황 |
|----------|--------|-------------|-------------|
| LLM Call | 낮음 | 높음 | 단순 변환, 분류 |
| Chain | 낮음 | 높음 | 순차적 처리 |
| Router | 중간 | 중간 | 조건부 분기 |
| Agent | 높음 | 낮음 | 복잡한 태스크 |
| Multi-Agent | 매우 높음 | 낮음 | 대규모 복합 태스크 |

##### 핵심 인사이트

```
설계 원칙:
├─ "적절한 Agency 수준 선택이 성공의 열쇠"
├─ 높은 Agency = 더 많은 Human-in-the-Loop 필요
├─ 낮은 Agency = 예측 가능하지만 유연성 제한
└─ 작업 복잡도에 맞는 아키텍처 선택 필수
```

---

#### 2. Structured Output (구조화된 출력)

##### with_structured_output 활용

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Literal

# 스키마 정의
class RouteDecision(BaseModel):
    """라우팅 결정을 위한 구조화된 출력"""
    next_step: Literal["search", "generate", "end"] = Field(
        description="다음에 실행할 단계"
    )
    reasoning: str = Field(
        description="결정 이유"
    )

# 모델에 스키마 바인딩
llm = ChatOpenAI(model="gpt-4o", temperature=0)
structured_llm = llm.with_structured_output(RouteDecision)

# 사용
result = structured_llm.invoke("사용자가 날씨를 물어봤습니다")
print(result.next_step)    # "search"
print(result.reasoning)    # "날씨 정보는 실시간 검색이 필요합니다"
```

##### 언어별 스키마 정의

| 언어 | 스키마 도구 | 예시 |
|------|-------------|------|
| Python | Pydantic | `class Output(BaseModel): ...` |
| JavaScript | Zod | `z.object({ field: z.string() })` |
| TypeScript | Zod | 타입 추론 지원 |

##### Structured Output 장점

```
구조화된 출력의 이점:
├─ 타입 안전성: IDE 자동완성, 컴파일 타임 검증
├─ 검증: Pydantic/Zod의 자동 검증
├─ 일관성: 항상 동일한 형식의 응답
├─ 후처리 용이: JSON 파싱 불필요
└─ 디버깅: 명확한 출력 구조로 오류 추적 용이
```

---

#### 3. Intermediate Output / Streaming

##### LangGraph Stream Modes

```python
# 기본 스트리밍 사용
for event in graph.stream(inputs, config={"configurable": {"thread_id": "1"}}):
    print(event)
```

##### Stream Mode 비교

| Mode | 출력 내용 | 사용 시점 |
|------|----------|----------|
| `"updates"` | 노드별 상태 변경사항 | 기본값, 일반적 사용 |
| `"values"` | 전체 상태 스냅샷 | 전체 상태 필요 시 |
| `"debug"` | 상세 디버깅 정보 | 개발/디버깅 |
| `"messages"` | 메시지 스트리밍 | 채팅 UI |

##### updates vs values 비교

```python
# stream_mode="updates" (기본값)
# 각 노드에서 변경된 부분만 출력
{'agent': {'messages': [AIMessage(content="검색 중...")]}}
{'tool': {'messages': [ToolMessage(content="결과: ...")]}}

# stream_mode="values"
# 매번 전체 상태 출력
{'messages': [HumanMessage(...), AIMessage(...), ToolMessage(...)]}
```

##### 실시간 토큰 스트리밍

```python
# LLM 토큰 단위 스트리밍
async for event in graph.astream_events(inputs, version="v2"):
    if event["event"] == "on_chat_model_stream":
        token = event["data"]["chunk"].content
        print(token, end="", flush=True)
```

---

#### 4. Human-in-the-Loop (HITL)

##### 6가지 HITL 모달리티

```
Human-in-the-Loop 모달리티:

┌─────────────────────────────────────────────────────┐
│                                                     │
│  1. Interrupt   - 실행 중단 및 대기                │
│  2. Authorize   - 액션 승인/거부                   │
│  3. Resume      - 중단된 실행 재개                 │
│  4. Restart     - 처음부터 다시 시작               │
│  5. Edit State  - 중간 상태 수정                   │
│  6. Fork        - 분기점에서 새 경로 생성          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

##### 4.1 Interrupt (인터럽트)

```python
from langgraph.graph import StateGraph

# 노드 실행 전 인터럽트 설정
graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["sensitive_tool"]  # 이 노드 전에 중단
)

# 또는 노드 실행 후 인터럽트
graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_after=["planning_node"]  # 이 노드 후에 중단
)
```

##### 4.2 Authorize (승인)

```python
# 실행 → 인터럽트 → 사용자 승인 확인 → 계속/취소
for event in graph.stream(inputs, config):
    if "sensitive_tool" in event:
        # 사용자에게 승인 요청
        action = event["sensitive_tool"]["pending_action"]
        approved = get_user_approval(action)  # UI에서 승인 받기

        if approved:
            # 승인됨 - 계속 실행
            graph.stream(None, config)  # None으로 재개
        else:
            # 거부됨 - 취소 처리
            cancel_action(config)
```

##### 4.3 Resume (재개)

```python
# 중단된 그래프 재개
# None을 입력으로 전달하면 마지막 체크포인트에서 재개
for event in graph.stream(None, config):
    print(event)
```

##### 4.4 Restart (재시작)

```python
# 특정 체크포인트로 롤백 후 재시작
checkpoints = list(graph.get_state_history(config))
target_checkpoint = checkpoints[2]  # 원하는 시점 선택

# 해당 시점의 config로 재시작
for event in graph.stream(new_input, target_checkpoint.config):
    print(event)
```

##### 4.5 Edit State (상태 수정)

```python
# 현재 상태 가져오기
state = graph.get_state(config)
print(state.values)

# 상태 수정
graph.update_state(
    config,
    values={"messages": corrected_messages},  # 수정된 값
    as_node="agent"  # 어떤 노드에서 수정된 것처럼 처리할지
)

# 수정된 상태에서 계속
for event in graph.stream(None, config):
    print(event)
```

##### 4.6 Fork (분기)

```python
# 기존 실행에서 분기하여 새 경로 생성
state = graph.get_state(config)

# 새 thread_id로 분기
forked_config = {"configurable": {"thread_id": "fork-1"}}
graph.update_state(
    forked_config,
    values=state.values  # 기존 상태 복사
)

# 분기된 경로에서 다른 입력으로 실행
for event in graph.stream(alternative_input, forked_config):
    print(event)
```

##### HITL 흐름 다이어그램

```
Human-in-the-Loop 워크플로우:

사용자 입력
     │
     ▼
┌─────────────┐
│   Agent     │
└─────────────┘
     │
     ▼
┌─────────────┐     ┌─────────────┐
│ Sensitive   │────▶│  INTERRUPT  │
│   Tool      │     │   (대기)    │
└─────────────┘     └─────────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
         [Approve]   [Edit State]  [Restart]
              │           │           │
              ▼           ▼           │
         [Resume]    [Resume]        │
              │           │           │
              └───────────┼───────────┘
                          ▼
                    계속 실행...
```

---

#### 5. Double Texting / Multitasking

##### 문제 상황

```
Double Texting 시나리오:

사용자 A: "날씨 알려줘"     ─────────────▶ [처리 중...]
사용자 A: "아니, 뉴스로!"   ─────────────▶ [???]

동일 사용자가 첫 번째 요청 처리 중에
두 번째 요청을 보내는 상황
```

##### 처리 전략

| 전략 | 설명 | 사용 시점 |
|------|------|----------|
| **Reject** | 진행 중 요청 거부 | 작업 완료가 중요할 때 |
| **Enqueue** | 대기열에 추가 | 순서대로 처리 필요 시 |
| **Interrupt** | 현재 작업 중단 | 새 요청 우선 시 |
| **Rollback** | 현재 작업 취소 후 새 작업 | 최신 요청만 유효 시 |

##### LangGraph에서의 Multitasking

```python
# 방법 1: Reject (기본)
try:
    result = graph.stream(input, config)
except ConcurrentExecutionError:
    print("이전 요청 처리 중입니다. 잠시 후 시도해주세요.")

# 방법 2: Thread별 분리
# 각 대화를 별도 thread로 관리
config_1 = {"configurable": {"thread_id": "user-1-conv-1"}}
config_2 = {"configurable": {"thread_id": "user-1-conv-2"}}

# 방법 3: Interrupt and Restart
# interrupt_before로 중단점 설정 후 새 입력으로 재시작
```

##### 실무 권장 패턴

```python
# 권장: Thread ID + Timestamp 조합
import time

def create_config(user_id: str) -> dict:
    return {
        "configurable": {
            "thread_id": f"{user_id}-{int(time.time())}"
        }
    }

# 또는 대화별 고유 ID 관리
from uuid import uuid4

def create_conversation_config(user_id: str) -> dict:
    return {
        "configurable": {
            "thread_id": str(uuid4()),
            "user_id": user_id
        }
    }
```

---

### 🔍 심화 학습

#### Agency 수준 선택 가이드

```
작업 유형별 권장 아키텍처:

┌────────────────────────────────────────────────────┐
│ 작업 복잡도           │ 권장 아키텍처              │
├────────────────────────────────────────────────────┤
│ 텍스트 분류/요약      │ LLM Call                  │
│ 단계별 처리           │ Chain                      │
│ 조건부 분기           │ Router                     │
│ 도구 활용 필요        │ Agent                      │
│ 복합 전문가 협업      │ Multi-Agent               │
└────────────────────────────────────────────────────┘

선택 기준:
├─ 예측 가능성 중요 → 낮은 Agency (Chain/Router)
├─ 유연성 중요 → 높은 Agency (Agent)
├─ 안전성 중요 → HITL 필수
└─ 성능 중요 → Streaming 활용
```

#### Checkpointer 선택 가이드

| Checkpointer | 특징 | 사용 시점 |
|--------------|------|----------|
| `MemorySaver` | 인메모리, 휘발성 | 개발/테스트 |
| `SqliteSaver` | SQLite 기반 | 단일 서버 프로덕션 |
| `PostgresSaver` | PostgreSQL 기반 | 분산 프로덕션 |
| `RedisSaver` | Redis 기반 | 고성능 분산 시스템 |

#### Streaming 최적화

```python
# 효율적인 스트리밍 패턴
async def stream_with_ui(graph, inputs, config):
    """UI 업데이트를 위한 스트리밍"""

    async for event in graph.astream(inputs, config, stream_mode="updates"):
        # 노드별 처리
        for node_name, node_output in event.items():
            if node_name == "agent":
                yield {"type": "thinking", "content": "분석 중..."}
            elif node_name == "tool":
                yield {"type": "tool_result", "content": node_output}
            elif node_name == "final":
                yield {"type": "answer", "content": node_output}
```

---

### 💡 실무 적용 포인트

1. **Agency 수준 결정**: 작업 복잡도와 안전 요구사항을 기준으로 적절한 아키텍처 선택
2. **Structured Output 활용**: 후속 처리가 필요한 모든 LLM 출력에 적용
3. **Streaming 기본 적용**: UX 향상을 위해 모든 대화형 애플리케이션에 필수
4. **HITL 단계적 적용**: 민감한 액션부터 Interrupt → Authorize 패턴 적용
5. **Checkpointer 선택**: 개발은 MemorySaver, 프로덕션은 PostgresSaver 또는 RedisSaver
6. **Double Texting 대응**: 서비스 특성에 맞는 전략 선택 (Reject/Enqueue/Interrupt)

---

### ✅ 정리 체크리스트

- [ ] Agency-Reliability Frontier 개념과 트레이드오프를 설명할 수 있다
- [ ] with_structured_output으로 Pydantic 스키마 기반 출력을 구현할 수 있다
- [ ] LangGraph의 4가지 stream_mode (updates, values, debug, messages) 차이를 안다
- [ ] interrupt_before/interrupt_after로 HITL 인터럽트를 설정할 수 있다
- [ ] get_state, update_state로 그래프 상태를 조회/수정할 수 있다
- [ ] HITL 6가지 모달리티 (Interrupt, Authorize, Resume, Restart, Edit State, Fork)를 안다
- [ ] Double Texting 4가지 처리 전략 (Reject, Enqueue, Interrupt, Rollback)을 안다
- [ ] 작업 복잡도에 맞는 적절한 아키텍처를 선택할 수 있다

---

### 🔗 참고 자료

- *LangChain for LLM Application Development* (책 제목 가정)
- [LangGraph Human-in-the-Loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)
- [LangGraph Streaming](https://langchain-ai.github.io/langgraph/concepts/streaming/)
- [LangChain Structured Output](https://python.langchain.com/docs/concepts/structured_outputs/)
- [LangGraph Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/)
