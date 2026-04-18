# Chapter 10. Testing: 평가, 모니터링, 지속적 개선

---

### 📌 핵심 요약
> LLM 애플리케이션은 비결정적 특성과 환각(Hallucination) 경향으로 인해 체계적인 테스트가 필수다. **Design → Preproduction → Production** 3단계에 걸쳐 테스트를 적용하며, 이는 **지속적 개선 사이클**을 형성한다. Design 단계에서는 **Self-Corrective RAG**로 런타임 오류를 자가 수정하고, Preproduction 단계에서는 **데이터셋 기반 오프라인 평가**와 **회귀 테스트**를 수행한다. Production 단계에서는 **트레이싱**, **온라인 평가**, **사용자 피드백 수집**으로 실시간 모니터링한다.

---

### 🎯 학습 목표
- LLM 앱 개발 주기의 3단계 테스트 기법을 이해한다
- Self-Corrective RAG의 제어 흐름을 구현할 수 있다
- LangSmith에서 데이터셋을 생성하고 평가 기준을 정의할 수 있다
- Human, Heuristic, LLM-as-a-Judge 세 가지 평가자 유형을 구분할 수 있다
- 에이전트의 Response, Single Step, Trajectory 평가 방법을 안다
- Production 트레이싱과 온라인 평가를 설정할 수 있다

---

### 📖 본문 정리

#### 1. LLM 앱 개발 주기와 테스트

```
┌─────────────────────────────────────────────────────────────┐
│              LLM App Development Cycle                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│      ┌──────────┐                                           │
│      │  Design  │◄────────────────────────────┐             │
│      │ (설계)   │                             │             │
│      └────┬─────┘                             │             │
│           │ Self-Corrective                   │             │
│           │ Error Handling                    │             │
│           ▼                                   │             │
│      ┌──────────────┐                         │             │
│      │Preproduction │                         │ Fix &       │
│      │ (사전 배포)   │                         │ Redesign    │
│      └────┬─────────┘                         │             │
│           │ Offline Evaluation                │             │
│           │ Regression Testing                │             │
│           ▼                                   │             │
│      ┌──────────────┐                         │             │
│      │  Production  │─────────────────────────┘             │
│      │   (운영)     │                                       │
│      └──────────────┘                                       │
│           │ Online Evaluation                               │
│           │ Monitoring                                      │
│           ▼                                                 │
│      [Continuous Improvement Cycle]                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### 3단계 테스트 목적

| 단계 | 목적 | 테스트 대상 |
|------|------|------------|
| **Design** | 사용자에게 도달하기 전 오류 처리 | 런타임 어설션, 자가 수정 |
| **Preproduction** | 배포 전 회귀 방지 | 데이터셋 기반 오프라인 평가 |
| **Production** | 실시간 이슈 감지 및 피드백 | 트레이싱, 온라인 평가 |

---

#### 2. Design 단계: Self-Corrective RAG

기본 RAG는 부정확한 검색으로 환각이 발생할 수 있다. **Self-Corrective RAG**는 LLM이 검색 관련성을 평가하고 스스로 수정한다.

##### 제어 흐름 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│                 Self-Corrective RAG Flow                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [Question]                                                │
│       │                                                     │
│       ▼                                                     │
│   ┌─────────┐                                               │
│   │ Router  │─────────────────┐                             │
│   └────┬────┘                 │                             │
│        │                      │                             │
│   Vector Store            Web Search                        │
│        │                      │                             │
│        ▼                      │                             │
│   ┌──────────┐                │                             │
│   │ Retrieve │                │                             │
│   └────┬─────┘                │                             │
│        │                      │                             │
│        ▼                      │                             │
│   ┌────────────┐              │                             │
│   │Grade Docs  │              │                             │
│   │(관련성 평가)│              │                             │
│   └────┬───────┘              │                             │
│        │                      │                             │
│   Relevant?                   │                             │
│   ├─ Yes ──▶ Generate         │                             │
│   │              │            │                             │
│   │              ▼            │                             │
│   │         ┌────────────┐    │                             │
│   │         │Check Answer│    │                             │
│   │         │(환각 검사)  │    │                             │
│   │         └─────┬──────┘    │                             │
│   │               │           │                             │
│   │          Accurate?        │                             │
│   │          ├─ Yes ──▶ [Output]                            │
│   │          └─ No ───────────┤                             │
│   │                           │                             │
│   └─ No ──────────────────────┴──▶ Web Search (Fallback)    │
│                                          │                  │
│                                          ▼                  │
│                                    [Generate Answer]        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### 검색 관련성 평가 구현

```python
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 이진 점수 데이터 모델
class GradeDocuments(BaseModel):
    """검색된 문서의 관련성 이진 점수"""
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )

# 구조화된 출력을 가진 LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
structured_llm_grader = llm.with_structured_output(GradeDocuments)

# 평가 프롬프트
system = """You are a grader assessing relevance of a retrieved document
to a user question. If the document contains keyword(s) or semantic meaning
related to the question, grade it as relevant.
Give a binary score 'yes' or 'no'."""

grade_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
])

retrieval_grader = grade_prompt | structured_llm_grader

# 실행
result = retrieval_grader.invoke({
    "question": "agent memory",
    "document": doc_txt
})
# 출력: binary_score='yes'
```

---

#### 3. Preproduction 단계: 오프라인 평가

##### 3.1 데이터셋 생성

데이터셋은 입력과 기대 출력의 모음으로, LLM 앱을 평가하는 데 사용된다.

**데이터셋 구축 방법:**

| 방법 | 설명 | 권장 크기 |
|------|------|----------|
| **수동 큐레이션** | 예상 입력과 이상적 출력 직접 작성 | 10-50개 |
| **애플리케이션 로그** | 실제 사용자 입력 수집 | 지속 추가 |
| **합성 데이터** | 기존 입력 샘플링으로 인공 생성 | 데이터 부족 시 |

**LangSmith 데이터셋 유형:**

| 유형 | 설명 | 적합한 사용 사례 |
|------|------|----------------|
| **kv** (key-value) | 임의의 키-값 쌍 | 다중 입출력 체인/에이전트 |
| **llm** | 단일 프롬프트 → 단일 응답 | 완성형 LLM 평가 |
| **chat** | 직렬화된 채팅 메시지 | 대화형 AI/챗봇 |

##### 3.2 평가자 유형

```
┌─────────────────────────────────────────────────────────────┐
│                    Evaluator Types                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │    Human     │  │  Heuristic   │  │ LLM-as-a-Judge   │  │
│  │   Evaluator  │  │  Evaluator   │  │    Evaluator     │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                    │            │
│    주관적 품질        코드 기반 검증        LLM 기반 채점      │
│    피드백 수집        정확도, JSON 검증     답변 비교 평가      │
│                                                             │
│  권장 순서: Human → Heuristic → LLM-as-a-Judge             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 평가자 유형 | 설명 | 장점 | 단점 |
|------------|------|------|------|
| **Human** | 사람이 직접 점수 부여 | 주관적 품질 평가 가능 | 시간/비용 소모 |
| **Heuristic** | 하드코딩된 함수/어설션 | 빠르고 일관됨 | 유연성 부족 |
| **LLM-as-a-Judge** | LLM이 출력 평가 | 확장 가능, 자연어 평가 | 신뢰성 검증 필요 |

##### 3.3 LLM-as-a-Judge 평가자

```
┌─────────────────────────────────────────────────────────────┐
│               LLM-as-a-Judge (RAG 사례)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [User Question]                                           │
│         │                                                   │
│         ▼                                                   │
│   ┌─────────────┐                                           │
│   │  RAG Chain  │──────────▶ [Generated Answer]             │
│   └─────────────┘                     │                     │
│                                       │                     │
│   [Reference Answer]                  │                     │
│   (Ground Truth)                      │                     │
│         │                             │                     │
│         └──────────┬──────────────────┘                     │
│                    │                                        │
│                    ▼                                        │
│              ┌───────────┐                                  │
│              │   Judge   │                                  │
│              │   (LLM)   │                                  │
│              └─────┬─────┘                                  │
│                    │                                        │
│                    ▼                                        │
│              [Score: 0 or 1]                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Few-Shot 학습으로 정확도 향상:**

1. LLM 평가자가 피드백 제공
2. 인간이 피드백 수정 (LangSmith)
3. 수정 사항이 Few-Shot 예시로 저장
4. 향후 평가에 예시 반영
5. 점진적으로 인간 선호도에 정렬

##### 3.4 Pairwise 평가

두 버전의 출력을 **동시에 비교**하여 어느 것이 더 나은지 판단:

```
Version A Output  ──┐
                    ├──▶ [Pairwise Evaluator] ──▶ Preference Score
Version B Output  ──┘
```

- 인간/LLM 평가자에게 인지 부담 감소
- "더 정보성 있는", "더 안전한" 등 기준으로 비교

##### 3.5 회귀 테스트

AI 모델은 **모델 드리프트**로 성능이 변동될 수 있어 100% 통과를 기대하기 어렵다.

**LangSmith 회귀 테스트 기능:**
- 여러 실험 및 실행 비교
- 베이스라인 대비 회귀/개선 감지
- 성능 변화가 있는 데이터 포인트 드릴다운

---

#### 4. 에이전트 평가 (3단계 세분화)

에이전트는 LLM이 제어 흐름을 결정하므로 테스트가 복잡하다.

```
┌─────────────────────────────────────────────────────────────┐
│                Agent Evaluation Levels                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Level 1: Response (최종 응답)                              │
│   ├─ Input: 프롬프트, (선택) 도구 목록                        │
│   ├─ Output: 에이전트 최종 응답                              │
│   └─ Evaluator: LLM-as-a-Judge                              │
│                                                             │
│   Level 2: Single Step (단일 단계)                           │
│   ├─ Input: 단일 단계 입력 (이전 단계 포함 가능)              │
│   ├─ Output: 도구 호출                                       │
│   └─ Evaluator: 이진 점수 (도구 선택 정확도)                  │
│                                                             │
│   Level 3: Trajectory (전체 궤적)                            │
│   ├─ Input: 사용자 입력, (선택) 도구                         │
│   ├─ Output: 도구 호출 시퀀스                                │
│   └─ Evaluator: 순서/개수 일치 검사                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### 4.1 최종 응답 테스트

```python
from langsmith import Client

client = Client()

# 데이터셋 생성
examples = [
    ("Which country's customers spent the most?",
     "The country is the USA, with $523.06"),
    ("What was the most purchased track of 2013?",
     "The most purchased track of 2013 was Hot Girl."),
]

dataset_name = "SQL Agent Response"
dataset = client.create_dataset(dataset_name=dataset_name)
inputs, outputs = zip(
    *[({"input": text}, {"output": label}) for text, label in examples]
)
client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)

# 평가 함수
def answer_evaluator(run, example) -> dict:
    input_question = example.inputs["input"]
    reference = example.outputs["output"]
    prediction = run.outputs["response"]

    # LLM-as-a-Judge로 비교
    score = answer_grader.invoke({
        "question": input_question,
        "correct_answer": reference,
        "student_answer": prediction
    })

    return {"key": "answer_v_reference_score", "score": score["Score"]}
```

##### 4.2 단일 단계 테스트

```python
def check_specific_tool_call(root_run: Run, example: Example) -> dict:
    """첫 번째 도구 호출이 예상과 일치하는지 확인"""
    expected_tool_call = 'sql_db_list_tables'

    response = root_run.outputs["response"]

    try:
        tool_call = getattr(response, 'tool_calls', [])[0]['name']
    except (IndexError, KeyError):
        tool_call = None

    score = 1 if tool_call == expected_tool_call else 0
    return {"score": score, "key": "single_tool_call"}
```

##### 4.3 궤적 테스트 (3가지 변형)

```python
def find_tool_calls(messages):
    """메시지에서 모든 도구 호출 추출"""
    return [
        tc['name']
        for m in messages['messages']
        for tc in getattr(m, 'tool_calls', [])
    ]

# 1. 순서 무관, 모든 도구 호출 확인
def contains_all_tool_calls_any_order(root_run, example) -> dict:
    expected = ['sql_db_list_tables', 'sql_db_schema',
                'sql_db_query_checker', 'sql_db_query', 'check_result']
    tool_calls = find_tool_calls(root_run.outputs["response"])
    score = 1 if set(expected) <= set(tool_calls) else 0
    return {"score": score, "key": "multi_tool_call_any_order"}

# 2. 순서대로 모든 도구 호출 확인
def contains_all_tool_calls_in_order(root_run, example) -> dict:
    expected = ['sql_db_list_tables', 'sql_db_schema',
                'sql_db_query_checker', 'sql_db_query', 'check_result']
    tool_calls = find_tool_calls(root_run.outputs["response"])
    it = iter(tool_calls)
    score = 1 if all(elem in it for elem in expected) else 0
    return {"score": score, "key": "multi_tool_call_in_order"}

# 3. 정확히 일치 (순서 + 추가 호출 없음)
def contains_all_tool_calls_in_order_exact_match(root_run, example) -> dict:
    expected = ['sql_db_list_tables', 'sql_db_schema',
                'sql_db_query_checker', 'sql_db_query', 'check_result']
    tool_calls = find_tool_calls(root_run.outputs["response"])
    score = 1 if tool_calls == expected else 0
    return {"score": score, "key": "multi_tool_call_in_exact_order"}
```

---

#### 5. Production 단계: 온라인 평가

##### 5.1 트레이싱 설정

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export OPENAI_API_KEY=<your-openai-api-key>
```

환경 변수 설정만으로 자동 트레이싱 활성화. LangSmith에서 다음 지표 확인:
- 트레이스 볼륨
- 성공/실패율
- 지연 시간
- 토큰 수 및 비용

##### 5.2 피드백 수집

| 피드백 유형 | 설명 | 구현 방법 |
|------------|------|----------|
| **사용자 피드백** | 좋아요/싫어요, 상세 피드백 | UI 버튼, 주석 큐 |
| **LLM-as-a-Judge** | 실시간 환각/독성 탐지 | 트레이스에 직접 적용 |

##### 5.3 분류 및 태깅

- **참조 레이블 없음**: LLM-as-a-Judge로 기준 기반 분류
- **참조 레이블 있음**: 커스텀 휴리스틱 평가자로 정확도 측정

##### 5.4 오류 모니터링 및 수정

```
Production 오류 발견
        │
        ▼
테스트 데이터셋에 추가
        │
        ▼
오프라인 평가로 재현
        │
        ▼
수정 후 재배포
```

**베타 릴리스 전략**: 소규모 사용자에게 먼저 배포하여 버그 발견 및 평가 데이터셋 구축

---

### 🔍 심화 학습

#### 오프라인 vs 온라인 평가

| 구분 | 오프라인 평가 | 온라인 평가 |
|------|-------------|------------|
| **시점** | 배포 전 | 배포 후 |
| **데이터** | 사전 정의된 테스트 셋 | 실시간 사용자 입력 |
| **참조 응답** | Ground Truth 있음 | 없음 (Reference-free) |
| **목적** | 회귀 방지 | 실시간 품질 모니터링 |

#### 평가자 선택 가이드

```
평가 요구사항 결정 트리:

코드로 표현 가능한가?
├─ Yes → Heuristic Evaluator
│         (JSON 검증, 정확도 등)
│
└─ No → 주관적 품질 평가인가?
         ├─ Yes (초기) → Human Evaluator
         │                (주석 큐 활용)
         │
         └─ Yes (확장 필요) → LLM-as-a-Judge
                               (Few-Shot으로 정렬)
```

#### 에이전트 평가 전략

```
복잡도 증가 ──────────────────────────────────▶

┌──────────┐   ┌──────────────┐   ┌─────────────┐
│ Response │ → │ Single Step  │ → │ Trajectory  │
│  (결과)   │   │  (단일 단계)  │   │  (전체 경로) │
└──────────┘   └──────────────┘   └─────────────┘
     │                │                  │
  블랙박스         특정 결정          전체 흐름
  성공/실패        디버깅            최적화
```

---

### 💡 실무 적용 포인트

1. **단계별 테스트**: Design → Preproduction → Production 순서로 점진적 적용
2. **Self-Corrective RAG**: 검색 관련성 평가 + 환각 검사로 품질 향상
3. **데이터셋 점진적 확장**: 수동 큐레이션 → 로그 수집 → 합성 데이터
4. **평가자 진화**: Simple (Heuristic) → Human → LLM-as-a-Judge (Few-Shot)
5. **에이전트 3단계 테스트**: Response → Single Step → Trajectory
6. **회귀 테스트 필수**: 모델 업데이트 시 베이스라인 대비 성능 확인
7. **베타 릴리스**: 전체 배포 전 소규모 사용자로 검증
8. **피드백 루프**: Production 오류 → 테스트 데이터셋 → 오프라인 평가 → 수정

---

### ✅ 정리 체크리스트

- [ ] Design/Preproduction/Production 3단계 테스트의 목적을 안다
- [ ] Self-Corrective RAG의 제어 흐름(Router → Retrieve → Grade → Generate → Check)을 설명할 수 있다
- [ ] 데이터셋 구축 3가지 방법(수동, 로그, 합성)을 안다
- [ ] LangSmith 데이터셋 유형(kv, llm, chat)의 차이를 안다
- [ ] Human, Heuristic, LLM-as-a-Judge 평가자의 장단점을 비교할 수 있다
- [ ] Few-Shot 학습으로 LLM-as-a-Judge 정확도를 향상시키는 방법을 안다
- [ ] Pairwise 평가의 개념과 장점을 안다
- [ ] 회귀 테스트의 중요성과 LangSmith 지원 기능을 안다
- [ ] 에이전트 평가 3단계(Response, Single Step, Trajectory)를 구현할 수 있다
- [ ] Production 트레이싱 환경 변수를 설정할 수 있다
- [ ] 온라인 평가와 오프라인 평가의 차이를 설명할 수 있다

---

### 🔗 참고 자료

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Evaluation Guide](https://docs.smith.langchain.com/evaluation)
- [LangSmith Datasets & Testing](https://docs.smith.langchain.com/evaluation/datasets)
- [LangGraph Self-Corrective RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/)
- [LLM-as-a-Judge Best Practices](https://docs.smith.langchain.com/evaluation/llm-as-judge)
- [Agent Evaluation Strategies](https://docs.smith.langchain.com/evaluation/agent-evals)
