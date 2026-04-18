# Chapter 1. LangChain으로 배우는 LLM 기초 (LLM Fundamentals with LangChain)

---

### 📌 핵심 요약
> LLM 애플리케이션 개발의 핵심 과제는 모델에 보낼 프롬프트를 효과적으로 구성하고, 모델의 예측 결과를 정확한 출력으로 처리하는 것이다. LangChain은 이를 위해 **교체 가능한 빌딩 블록**(LLM, Chat Model, Output Parser 등)과 **사전 구축된 공통 패턴**을 제공한다. 모든 컴포넌트는 `invoke`, `batch`, `stream` 메서드를 공유하는 **Runnable Interface**를 따르며, **명령형(Imperative)** 또는 **선언형(LCEL)** 방식으로 조합할 수 있다.

---

### 🎯 학습 목표
- LangChain을 사용하는 이유와 장점을 이해한다
- LLM과 Chat Model의 차이점을 설명할 수 있다
- PromptTemplate을 활용해 재사용 가능한 프롬프트를 만들 수 있다
- 구조화된 출력(JSON 등)을 생성하는 방법을 안다
- Runnable Interface와 조합 방식(명령형/선언형)을 이해한다

---

### 📖 본문 정리

#### 1. 왜 LangChain인가? (Why LangChain?)

LLM 제공업체의 SDK를 직접 사용할 수도 있지만, LangChain을 배우면 다음과 같은 이점이 있다:

| 장점 | 설명 |
|------|------|
| **사전 구축된 패턴** | Chain-of-Thought, Tool Calling 등 일반적인 LLM 패턴의 레퍼런스 구현 제공 |
| **교체 가능한 빌딩 블록** | 모든 컴포넌트가 공유 스펙을 따르므로, 필요시 쉽게 교체 가능 |
| **벤더 독립성** | OpenAI, Anthropic 등 다른 제공업체의 미묘한 차이를 추상화 |
| **관찰 가능성** | Callbacks 시스템으로 모든 주요 컴포넌트 계측 |
| **인터럽트/재개** | 장시간 실행되는 애플리케이션을 중단, 재개, 재시도 가능 |

##### 주요 컴포넌트 대안

```
LLM/Chat Model:
├─ 상용: OpenAI (기본), Anthropic
└─ 오픈소스: Ollama

Embeddings:
├─ 상용: OpenAI (기본), Cohere
└─ 오픈소스: Ollama

Vector Store:
├─ 오픈소스: PGVector (기본)
├─ 전용 벡터 DB: Weaviate
└─ 검색 DB: OpenSearch
```

---

#### 2. LangChain에서 LLM 사용하기

LangChain은 두 가지 인터페이스를 제공한다:

##### LLM Interface
단순히 문자열 프롬프트를 입력받아 모델 예측을 반환:

```python
from langchain_openai.llms import OpenAI

model = OpenAI(model="gpt-3.5-turbo")
model.invoke("The sky is")
# 출력: "Blue!"
```

##### Chat Model Interface
역할(Role) 기반의 대화형 메시지 처리:

```python
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

model = ChatOpenAI()
prompt = [HumanMessage("What is the capital of France?")]
model.invoke(prompt)
# 출력: AIMessage(content='The capital of France is Paris.')
```

##### 메시지 타입

| 메시지 타입 | 역할 | 설명 |
|-------------|------|------|
| `SystemMessage` | system | 모델이 따라야 할 지시사항 |
| `HumanMessage` | user | 사용자의 질문/입력 |
| `AIMessage` | assistant | 모델이 생성한 응답 |
| `ChatMessage` | 임의 | 역할을 자유롭게 설정 |

```python
from langchain_core.messages import HumanMessage, SystemMessage

system_msg = SystemMessage("You are a helpful assistant that responds with three exclamation marks.")
human_msg = HumanMessage("What is the capital of France?")

model.invoke([system_msg, human_msg])
# 출력: AIMessage('Paris!!!')
```

##### 주요 모델 파라미터

| 파라미터 | 설명 | 권장값 |
|----------|------|--------|
| `model` | 사용할 모델 (크기↑ = 성능↑, 비용↑, 속도↓) | 작업에 따라 선택 |
| `temperature` | 출력의 창의성 조절 (0.1: 예측 가능, 0.9: 창의적) | 구조화 출력 → 낮게, 창작 → 높게 |
| `max_tokens` | 출력 크기 제한 (비용 조절) | 너무 낮으면 출력이 잘림 |

---

#### 3. 재사용 가능한 프롬프트 만들기

##### PromptTemplate
동적 입력을 받는 프롬프트 템플릿:

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("""Answer the question based on the context below.
If the question cannot be answered, answer with "I don't know".

Context: {context}

Question: {question}

Answer: """)

# 템플릿 사용
prompt = template.invoke({
    "context": "LLMs are driving NLP advancements...",
    "question": "Which model providers offer LLMs?"
})
```

##### ChatPromptTemplate
역할 기반 채팅 프롬프트:

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ('system', 'Answer based on context. If unknown, say "I don\'t know".'),
    ('human', 'Context: {context}'),
    ('human', 'Question: {question}'),
])

prompt = template.invoke({
    "context": "...",
    "question": "Which model providers offer LLMs?"
})
```

---

#### 4. 구조화된 출력 얻기

##### JSON 출력 (with_structured_output)

스키마 정의 후 자동으로 JSON 구조화:

```python
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel

class AnswerWithJustification(BaseModel):
    '''An answer with justification'''
    answer: str
    justification: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
structured_llm = llm.with_structured_output(AnswerWithJustification)

structured_llm.invoke("What weighs more, a pound of bricks or a pound of feathers?")
# 출력: {'answer': 'They weigh the same', 'justification': 'Both weigh one pound...'}
```

##### Output Parsers
CSV, XML 등 다른 형식 처리:

```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
parser.invoke("apple, banana, cherry")
# 출력: ['apple', 'banana', 'cherry']
```

**Output Parser의 두 가지 기능**:
1. **Format Instructions**: 프롬프트에 형식 지시사항 주입
2. **Validate & Parse**: LLM 출력을 구조화된 형식으로 변환/검증

---

#### 5. Runnable Interface

모든 LangChain 컴포넌트는 동일한 인터페이스를 공유한다:

| 메서드 | 설명 | 예시 |
|--------|------|------|
| `invoke` | 단일 입력 → 단일 출력 | `model.invoke("Hi!")` |
| `batch` | 다중 입력 → 다중 출력 | `model.batch(["Hi!", "Bye!"])` |
| `stream` | 단일 입력 → 스트리밍 출력 | `for token in model.stream("Bye!")` |

```python
model = ChatOpenAI()

# invoke
completion = model.invoke('Hi there!')  # "Hi!"

# batch
completions = model.batch(['Hi!', 'Bye!'])  # ['Hi!', 'See you!']

# stream
for token in model.stream('Bye!'):
    print(token)  # Good / bye / !
```

---

#### 6. 컴포넌트 조합 방식

##### 비교표

| 항목 | 명령형 (Imperative) | 선언형 (Declarative/LCEL) |
|------|---------------------|---------------------------|
| **문법** | Python/JavaScript 전체 | LCEL (`\|` 또는 `.pipe()`) |
| **병렬 실행** | 스레드/코루틴 직접 구현 | 자동 |
| **스트리밍** | `yield` 키워드 사용 | 자동 |
| **비동기 실행** | `async` 함수 사용 | 자동 |

##### 명령형 조합 (Imperative)

```python
from langchain_core.runnables import chain

template = ChatPromptTemplate.from_messages([...])
model = ChatOpenAI()

@chain
def chatbot(values):
    prompt = template.invoke(values)
    return model.invoke(prompt)

# 사용
chatbot.invoke({"question": "Which providers offer LLMs?"})
```

**스트리밍 지원 추가**:
```python
@chain
def chatbot(values):
    prompt = template.invoke(values)
    for token in model.stream(prompt):
        yield token

for part in chatbot.stream({"question": "..."}):
    print(part)
```

##### 선언형 조합 (LCEL)

```python
# Python: | 연산자 사용
chatbot = template | model

# JavaScript: .pipe() 메서드 사용
# const chatbot = template.pipe(model)

# 사용 - 스트리밍/비동기 자동 지원
chatbot.invoke({"question": "..."})

for part in chatbot.stream({"question": "..."}):
    print(part)
```

---

### 🔍 심화 학습

#### LLM vs Chat Model 선택 기준

```
사용 시나리오:
├─ 단순 텍스트 완성 → LLM Interface
├─ 대화형 애플리케이션 → Chat Model Interface
├─ 시스템 지시사항 필요 → Chat Model (SystemMessage)
└─ 멀티턴 대화 → Chat Model (메시지 히스토리 관리)
```

#### 명령형 vs 선언형 선택 기준

```
선택 가이드:
├─ 커스텀 로직이 많음 → 명령형
├─ 기존 컴포넌트 단순 조합 → 선언형 (LCEL)
├─ 스트리밍/비동기 필요 → 선언형 (자동 지원)
└─ 디버깅/세밀한 제어 → 명령형
```

#### Temperature 설정 가이드

| 작업 유형 | 권장 Temperature | 이유 |
|-----------|------------------|------|
| JSON/코드 생성 | 0.0 ~ 0.3 | 예측 가능하고 정확한 출력 필요 |
| 일반 Q&A | 0.3 ~ 0.7 | 균형 잡힌 응답 |
| 창작/브레인스토밍 | 0.7 ~ 1.0 | 다양하고 창의적인 출력 |

---

### 💡 실무 적용 포인트

1. **벤더 독립성 확보**: LangChain 추상화를 활용해 특정 제공업체에 종속되지 않는 코드 작성
2. **프롬프트 템플릿화**: 하드코딩된 프롬프트 대신 PromptTemplate으로 재사용성 확보
3. **구조화된 출력**: API 응답이나 DB 저장 시 `with_structured_output` 활용
4. **LCEL 우선 사용**: 단순 조합은 LCEL로, 복잡한 로직은 명령형으로
5. **스트리밍 고려**: UX 향상을 위해 `stream()` 메서드 활용
6. **Temperature 조정**: 작업 특성에 맞게 temperature 값 설정

---

### ✅ 정리 체크리스트

- [ ] LangChain의 두 가지 핵심 장점(사전 구축 패턴, 교체 가능 빌딩 블록)을 안다
- [ ] LLM Interface와 Chat Model Interface의 차이를 설명할 수 있다
- [ ] SystemMessage, HumanMessage, AIMessage의 역할을 안다
- [ ] PromptTemplate과 ChatPromptTemplate 사용법을 안다
- [ ] with_structured_output으로 JSON 출력을 생성할 수 있다
- [ ] Output Parser의 두 가지 기능을 안다
- [ ] Runnable Interface의 세 가지 메서드(invoke, batch, stream)를 안다
- [ ] 명령형과 선언형(LCEL) 조합 방식의 차이를 이해한다
- [ ] `|` (Python) 또는 `.pipe()` (JS)로 컴포넌트를 조합할 수 있다

---

### 🔗 참고 자료

- *LangChain for LLM Application Development* (책 제목 가정)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangChain Chat Models](https://python.langchain.com/docs/integrations/chat/)
- [LangChain Embeddings](https://python.langchain.com/docs/integrations/text_embedding/)
- [LangChain Vector Stores](https://python.langchain.com/docs/integrations/vectorstores/)
- [OpenAI Models Overview](https://platform.openai.com/docs/models)
