**AI Agentization 실무 역량 강화 객관식 문제 세트 (약 100문제)**

아래는 요청하신 주제(주요 LLM 모델 특성/활용, Harness Engineering, Token Optimization, MCP 설계, AI Agentization 등)를 바탕으로 회사 시험 수준으로 구성한 객관식 문제들입니다. 총 100문제를 섹션별로 나누어 출제했습니다. 각 문제는 4지 선다형이며, 실무 적용 중심으로 난이도를 조정했습니다.

> 실제 출제된 30문항(1–10, 21–25, 36–40, 56–60, 71–75)에는 **정답과 해설**을 각 문항 아래 달았습니다. `(문제 X-Y: …)`로 표기된 구간은 원본에 실제 문항이 없는 출제 방향 요약이므로 정답이 없습니다.

### **섹션 1: 주요 LLM 모델의 특성과 활용 방식 (문제 1-20)**

1. GPT 시리즈(예: GPT-5.x)의 가장 큰 강점으로 볼 수 있는 것은?  
   a) 오픈소스 가중치 공개  
   b) 강력한 tool calling과 reasoning 능력  
   c) 가장 저렴한 비용  
   d) 이미지 생성 전용  
   **정답: b** — GPT 계열은 함수/도구 호출과 추론에 강하다. 가중치는 비공개(a 오답)이고, 최저가도 아니며(c), 텍스트·추론 범용 모델이라 이미지 생성 전용(d)도 아니다.

2. Claude 모델(Anthropic)의 특징 중 맞는 것은?  
   a) Constitutional AI로 안전성과 긴 컨텍스트 처리 우수  
   b) 가장 빠른 inference 속도  
   c) 오픈소스 모델  
   d) 멀티모달에 weakest  
   **정답: a** — Claude는 Constitutional AI 기반 안전성과 긴 컨텍스트가 강점이다. 속도가 항상 최고인 것은 아니고(b), 가중치 비공개(c)이며, 멀티모달도 지원하므로 "가장 약함"(d)은 틀리다.

3. Llama 3/4 시리즈의 활용 시 주의점은?  
   a) 상용화 제한 없음  
   b) fine-tuning이 용이하나, inference 비용이 proprietary 모델보다 높음  
   c) context window가 8k로 제한적  
   d) Anthropic에서만 사용 가능  
   **정답: b** — 오픈웨이트라 파인튜닝은 자유롭지만, 직접 GPU를 운영하면 관리형 API보다 오히려 총비용이 높아질 수 있다. 라이선스에 상용 제약이 있고(a), 컨텍스트는 8k보다 크며(c), Meta 모델이라 d도 틀리다.

4. Gemini 모델의 강점은?  
   a) Google 생태계 통합과 멀티모달(비디오/오디오) 처리  
   b) 코드 생성에 최적화  
   c) 가장 긴 context window 독점  
   d) 완전 오픈소스  
   **정답: a** — Gemini는 Google 생태계 통합과 비디오·오디오 포함 멀티모달이 강점이다. 코드 전용(b)·컨텍스트 독점(c)·오픈소스(d)는 모두 사실이 아니다.

5. Grok 모델(xAI)의 차별점은?  
   a) 실시간 정보 접근과 유머러스한 응답 스타일  
   b) 가장 엄격한 safety filter  
   c) 오직 이미지 생성만 지원  
   d) enterprise 전용  
   **정답: a** — Grok은 X(트위터) 실시간 데이터 접근과 특유의 응답 톤이 차별점이다. 오히려 필터가 느슨한 편이고(b), 텍스트 모델이며(c), 일반 사용자도 쓸 수 있다(d).

6. LLM 선택 시 context window 크기가 중요한 이유는?  
   a) 긴 문서 요약이나 RAG에서 필수  
   b) inference 속도 향상  
   c) token 비용 절감  
   d) fine-tuning 용이성  
   **정답: a** — 컨텍스트가 클수록 긴 문서·다중 청크를 한 번에 넣어 요약/RAG가 유리하다. 컨텍스트가 크면 오히려 속도·비용은 늘고(b·c), 파인튜닝(d)과는 무관하다.

7. Proprietary LLM vs Open-source LLM 비교에서 proprietary의 장점은?  
   a) 최신 성능과 managed service  
   b) 완전 커스터마이징 자유  
   c) 비용 무료  
   d) 데이터 프라이버시 완벽 보장  
   **정답: a** — 상용 모델은 최신 성능과 운영을 대신 해주는 관리형 서비스가 강점이다. 자유로운 커스터마이징(b)은 오픈모델 쪽 장점이고, 무료(c)·프라이버시 완벽(d)은 성립하지 않는다.

8. 2026년 기준 최고 reasoning 벤치마크(GPQA, AIME 등)에서 강세를 보이는 모델군은?  
   a) Claude Opus 시리즈  
   b) Llama 소형 모델  
   c) 모든 Gemini 모델  
   d) Grok-1  
   **정답: a** — 최상위 추론 벤치마크는 대형 프런티어 모델(Claude Opus 등)이 주도한다. 소형 Llama(b)·구형 Grok-1(d)은 상위권이 아니고, "모든" Gemini(c)로 뭉뚱그리는 것도 부정확하다.

9. LLM 활용 시 temperature parameter의 역할은?  
   a) 창의성 vs 결정성 조절  
   b) token 수 제한  
   c) context window 확장  
   d) safety filter 강화  
   **정답: a** — temperature는 샘플링 무작위성을 조절해 창의성(높음)과 일관성/결정성(낮음)의 균형을 잡는다. 토큰 수 제한(b)·컨텍스트 확장(c)·안전 필터(d)와는 무관하다.

10. Multi-modal LLM의 실무 활용 예시로 적합하지 않은 것은?  
    a) 이미지 기반 코드 생성  
    b) 텍스트-only RAG  
    c) 비디오 분석 에이전트  
    d) 오디오 트랜스크립션 후 요약  
    **정답: b** — 텍스트만 다루는 RAG는 굳이 멀티모달 모델이 필요 없다. 나머지 a·c·d는 이미지·비디오·오디오가 개입하므로 멀티모달의 대표 활용처다.

(문제 11-20: 비슷한 패턴으로 모델 비교, 벤치마크(MMLU, SWE-bench, Agentic), 비용/속도 trade-off, cutoff date 영향, fine-tuning vs prompting 등 다룸)

### **섹션 2: Token Optimization (문제 21-35)**

21. Token Optimization의 주요 목적은?  
    a) 비용 절감, latency 감소, context window 효율화  
    b) 모델 accuracy 향상만  
    c) safety 강화  
    d) UI 디자인 개선  
    **정답: a** — 토큰 최적화는 비용·지연·컨텍스트 효율을 함께 노린다. 정확도(b)는 부수 효과일 뿐 "향상만"이 목적은 아니고, 안전(c)·UI(d)는 다른 관심사다.

22. Prompt에서 token 수를 줄이는 효과적인 방법은?  
    a) 불필요한 설명 제거, abbreviation 사용, structured format  
    b) 더 긴 문장 추가  
    c) 모든 예시 포함  
    d) temperature 높임  
    **정답: a** — 군더더기 제거·구조화로 같은 의미를 더 적은 토큰에 담는다. 문장 늘리기(b)·예시 전부 넣기(c)는 토큰을 늘리고, temperature(d)는 토큰 수와 무관하다.

23. Prefix Caching(또는 Prompt Caching)의 이점은?  
    a) 반복되는 system prompt에 대한 token 비용 절감  
    b) output token만 감소  
    c) context window 확장  
    d) hallucination 방지  
    **정답: a** — 매 요청 반복되는 긴 프리픽스(시스템 프롬프트·도구 정의)를 캐싱해 입력 토큰 비용·지연을 줄인다. 출력 토큰(b)·컨텍스트 크기(c)·환각(d)에는 영향이 없다.

24. RAG 파이프라인에서 token optimization 기법으로 적합한 것은?  
    a) Chunking + Reranking + Summarization  
    b) 모든 문서 full context 입력  
    c) embedding dimension 증가  
    d) vector DB 없이 검색  
    **정답: a** — 청킹·재순위·요약으로 관련 부분만 골라 넣어야 토큰이 절약된다. 전체 문서 투입(b)은 정반대이고, 임베딩 차원 증가(c)나 벡터DB 미사용(d)은 최적화가 아니다.

25. LLM Agent에서 chat history 압축 방법으로 효과적인 것은?  
    a) Summarizer agent 또는 key event extraction  
    b) 전체 history 항상 유지  
    c) temperature 0 고정  
    d) tool calling 비활성화  
    **정답: a** — 대화가 길어지면 요약·핵심 이벤트 추출로 압축해 컨텍스트를 관리한다. 전체 유지(b)는 곧 한도 초과·context rot로 이어지고, temperature(c)·tool calling(d)은 압축과 무관하다.

(문제 26-35: Context compression, LoRA fine-tuning 영향, cost per successful task metric, embedding optimization, hybrid search 등)

### **섹션 3: Harness Engineering (문제 36-55)**

36. Harness Engineering의 핵심 정의는?  
    a) LLM 주변의 scaffolding(tools, verification, memory, observability) 설계  
    b) 모델 fine-tuning만  
    c) prompt 작성 기술  
    d) UI/UX 디자인  
    **정답: a** — 하네스는 모델을 감싸는 실행·검증·메모리·관측 등의 스캐폴딩 전체를 설계하는 일이다. 파인튜닝(b)은 모델 내부, 프롬프트 작성(c)은 하네스의 한 조각일 뿐이며 UI(d)는 별개다.

37. Coding Agent를 위한 Outer Harness의 목적은?  
    a) Agent output 검증, self-correction loop 구축  
    b) input token만 최적화  
    c) 모델 교체  
    d) 비용 청구  
    **정답: a** — 아우터 하네스는 에이전트 산출물(예: 코드)을 빌드·테스트로 검증하고 실패를 되먹여 자가 수정 루프를 만든다. 토큰 최적화(b)·모델 교체(c)·과금(d)은 목적이 아니다.

38. Effective Harness의 구성 요소로 필수적인 것은?  
    a) Planning artifacts, verification loops, sandbox  
    b) 오직 system prompt  
    c) 단일 tool  
    d) human oversight 제거  
    **정답: a** — 계획 산출물·검증 루프·격리 실행 환경(sandbox)이 신뢰성 있는 하네스의 뼈대다. 시스템 프롬프트만(b)·도구 하나만(c)으로는 부족하고, 사람 감독 제거(d)는 오히려 위험하다.

39. Harness Engineering이 Context Engineering의 subset인 이유는?  
    a) Context delivery와 configuration points 관리  
    b) 모델 내부만 변경  
    c) token counting만  
    d) 벤치마크 점수 향상  
    **정답: a** — 하네스는 결국 모델에 무엇을 어떻게 전달할지(컨텍스트 전달·설정 지점)를 다루므로 컨텍스트 엔지니어링의 한 갈래다. 모델 내부(b)·토큰 카운팅(c)·벤치마크(d)는 초점이 아니다.

40. AI Agent Harness에서 Observability의 중요성은?  
    a) Trace every LLM call, tool call, retrieval for debugging  
    b) output만 logging  
    c) input 무시  
    d) latency 측정 불필요  
    **정답: a** — 모든 LLM 호출·도구 호출·검색을 추적해야 비결정적 에이전트를 디버깅·개선할 수 있다. 출력만 기록(b)·입력 무시(c)·지연 측정 생략(d)은 관측성을 반쪽으로 만든다.

(문제 41-55: Feedback loops, permission boundaries, guardrails, retries/state machines, human-in-the-loop 등)

### **섹션 4: MCP (Model Context Protocol) 설계 (문제 56-70)**

56. MCP(Model Context Protocol)의 주요 목적은?  
    a) LLM이 외부 tools, DB, API와 표준화된 방식으로 상호작용  
    b) 모델 내부 training  
    c) token 생성만  
    d) UI 렌더링  
    **정답: a** — MCP는 LLM 애플리케이션과 외부 도구·데이터·워크플로우 연결을 표준화하는 개방형 프로토콜이다. 학습(b)·토큰 생성(c)·UI(d)와는 무관하다.

57. MCP의 클라이언트-서버 아키텍처에서 LLM 역할은?  
    a) MCP Client (요청 측)  
    b) MCP Server (tool 제공)  
    c) Database만  
    d) Human operator  
    **정답: a** — LLM을 품은 호스트 애플리케이션이 클라이언트가 되어 서버에 도구·리소스를 요청한다. 도구를 노출하는 쪽이 서버(b)이고, DB(c)·사람(d)은 이 역할 구분에 해당하지 않는다.

58. MCP 도입의 장점은?  
    a) Agent Framework와 Tool 간 vendor lock-in 감소, interoperability 향상  
    b) context window 감소  
    c) 비용 증가  
    d) safety 저하  
    **정답: a** — 표준 프로토콜이라 특정 프레임워크·벤더에 묶이지 않고 도구를 재사용·상호운용할 수 있다. 컨텍스트 축소(b)·비용 증가(c)·안전 저하(d)는 장점이 아니다.

59. MCP를 활용한 Agentic RAG 설계 시 핵심은?  
    a) 모든 search/retrieval을 MCP Tool로 통일  
    b) direct DB query  
    c) prompt-only  
    d) static data  
    **정답: a** — 검색/조회를 MCP 도구로 표준화하면 에이전트가 일관된 인터페이스로 여러 소스를 다룰 수 있다. 직접 DB 쿼리(b)·프롬프트만(c)·정적 데이터(d)는 agentic RAG의 취지와 어긋난다.

60. MCP와 A2A(Agent-to-Agent) 프로토콜의 관계는?  
    a) MCP는 tool integration, A2A는 multi-agent 협업  
    b) 동일한 프로토콜  
    c) MCP가 multi-agent 전용  
    d) 둘 다 불필요  
    **정답: a** — MCP는 에이전트↔도구/데이터 연결, A2A는 에이전트↔에이전트 협업으로 계층이 다르다. 같은 프로토콜(b)도, MCP가 멀티에이전트 전용(c)도 아니며 둘 다 실무에서 쓰인다(d).

(문제 61-70: MCP 구현 예시, security, local LLM 연동, workflow design 등)

### **섹션 5: AI Agentization 및 종합 실무 (문제 71-100)**

71. LLM Agent의 핵심 구성 요소는?  
    a) Planning, Memory, Tools, LLM Core  
    b) Prompt만  
    c) Vector DB  
    d) Frontend  
    **정답: a** — 에이전트는 계획·메모리·도구·LLM 코어가 맞물려 동작한다. 프롬프트만(b)·벡터DB(c)·프런트엔드(d)는 그중 일부이거나 별개 요소다.

72. ReAct 패러다임의 흐름은?  
    a) Thought → Action → Observation 반복  
    b) Single shot answer  
    c) Tree of Thoughts만  
    d) No tool use  
    **정답: a** — ReAct는 추론(Thought)→행동(Action)→관찰(Observation)을 반복하며 도구를 쓰는 패턴이다. 단발 응답(b)·ToT 전용(c)·도구 미사용(d)은 ReAct가 아니다.

73. AI Agentization에서 Memory 유형으로 장기 기억 관리는?  
    a) Vector store + summarization  
    b) Session memory만  
    c) Prompt에 모두 포함  
    d) 무시  
    **정답: a** — 장기 기억은 벡터 스토어에 저장하고 요약으로 압축해 필요할 때 검색한다. 세션 메모리만(b)은 단기 한정이고, 전부 프롬프트에 넣기(c)는 한도 초과, 무시(d)는 기억 관리가 아니다.

74. Multi-Agent System의 활용 시 이점은?  
    a) Role specialization과 collaboration  
    b) 단일 모델 비용 절감  
    c) complexity 감소  
    d) latency 무관  
    **정답: a** — 여러 에이전트에 역할을 나눠 협업시키면 전문화된 처리가 가능하다. 다만 비용(b)·복잡도(c)·지연(d)은 오히려 늘어날 수 있어 이점이 아니다.

75. Production AI Agent에서 Guardrails와 Human Approval의 역할은?  
    a) Safety와 reliability 확보  
    b) 속도 향상  
    c) token 증가  
    d) autonomy 완전 제거  
    **정답: a** — 가드레일과 사람 승인은 위험한 행동을 막아 안전성·신뢰성을 확보한다. 속도(b)·토큰(c)과는 무관하고, 자율성을 "완전 제거"(d)하는 게 아니라 위험 구간에만 개입한다.

**활용 팁**:  
- 25문제 시험용으로는 각 섹션에서 5문제씩 균형 있게 추출 추천.  
- 난이도 조절: 기본 개념(1-50), 실무 적용/시나리오(51-100).  
- 필요 시 정답 키, 설명, 또는 추가 문제(변형) 생성 가능.  

이 문제들은 2026년 기준 최신 트렌드(Claude MCP, Harness, Token Opt 등)를 반영했습니다. 실제 시험에 맞게 수정해 사용하세요! 추가 조정이 필요하면 말씀해주세요.

---

## 문제에 나온 키워드 정리

문항과 각 섹션 출제 방향에 등장한 용어를 주제별로 묶어 한 줄 정의로 정리했습니다.

### 섹션 1) 주요 LLM 모델의 특성

| 키워드 | 정의 |
|--------|------|
| **GPT 시리즈** | 강력한 tool calling·reasoning이 강점인 상용 모델군(가중치 비공개). |
| **Claude (Anthropic)** | Constitutional AI 기반 안전성·긴 컨텍스트가 강점. |
| **Llama 3/4** | 오픈웨이트로 파인튜닝은 자유롭지만, 자체 운영 시 관리형 API보다 총비용이 높을 수 있음. |
| **Gemini (Google)** | Google 생태계 통합 + 비디오·오디오 포함 멀티모달. |
| **Grok (xAI)** | X 실시간 데이터 접근 + 특유의 응답 톤. |
| **context window** | 긴 문서 요약·RAG에서 중요. 크면 속도·비용은 늘어남. |
| **proprietary vs open-source** | 상용=최신 성능·관리형 서비스 / 오픈=커스터마이징·데이터 통제. |
| **reasoning 벤치마크** | GPQA·AIME 등. 대형 프런티어 모델(Claude Opus 등)이 강세. |
| **temperature** | 창의성 vs 결정성 조절 파라미터. |
| **multi-modal 활용** | 이미지 코드 생성·비디오 분석·오디오 요약 등(텍스트 전용 RAG는 불필요). |
| *(11–20 방향)* | 벤치마크(MMLU·SWE-bench·Agentic), 비용/속도 trade-off, cutoff date 영향, fine-tuning vs prompting. |

### 섹션 2) Token Optimization

| 키워드 | 정의 |
|--------|------|
| **토큰 최적화 목적** | 비용 절감·latency 감소·컨텍스트 효율화. |
| **프롬프트 토큰 절감** | 군더더기 제거·약어·구조화 포맷. |
| **Prefix/Prompt Caching** | 반복되는 system prompt 재사용으로 입력 토큰 비용 절감. |
| **RAG 토큰 최적화** | Chunking + Reranking + Summarization. |
| **chat history 압축** | Summarizer agent·key event extraction. |
| *(26–35 방향)* | Context compression, LoRA fine-tuning 영향, cost per successful task, embedding 최적화, hybrid search. |

### 섹션 3) Harness Engineering

| 키워드 | 정의 |
|--------|------|
| **Harness Engineering** | LLM 주변의 scaffolding(tools·verification·memory·observability) 설계. |
| **Outer Harness** | 에이전트 산출물을 빌드·테스트로 검증하고 실패를 되먹이는 self-correction 루프. |
| **Effective Harness 요소** | Planning artifacts·verification loops·sandbox. |
| **Context Engineering의 subset** | 하네스는 결국 컨텍스트 전달·설정 지점 관리. |
| **Observability** | 모든 LLM 호출·tool 호출·retrieval을 trace해 디버깅. |
| *(41–55 방향)* | Feedback loops, permission boundaries, guardrails, retries/state machines, human-in-the-loop. |

### 섹션 4) MCP 설계

| 키워드 | 정의 |
|--------|------|
| **MCP** | LLM이 외부 tools·DB·API와 표준화된 방식으로 상호작용하는 프로토콜. |
| **Client-Server 역할** | LLM 호스트 앱=Client(요청 측), 도구 제공=Server. |
| **MCP 장점** | 프레임워크·도구 간 vendor lock-in 감소, interoperability 향상. |
| **Agentic RAG** | search/retrieval을 MCP Tool로 통일해 일관된 인터페이스 제공. |
| **MCP vs A2A** | MCP=에이전트↔도구 통합, A2A=에이전트↔에이전트 협업(계층이 다름). |
| *(61–70 방향)* | MCP 구현 예시, security, local LLM 연동, workflow design. |

### 섹션 5) AI Agentization 및 종합 실무

| 키워드 | 정의 |
|--------|------|
| **Agent 핵심 구성** | Planning · Memory · Tools · LLM Core. |
| **ReAct** | Thought → Action → Observation 반복. |
| **장기 기억(Memory)** | Vector store + summarization으로 저장·검색. |
| **Multi-Agent System** | 역할 특화(role specialization)와 협업(비용·복잡도·지연은 늘 수 있음). |
| **Guardrails + Human Approval** | 위험 행동을 막아 safety·reliability 확보(자율성 완전 제거는 아님). |
| *(76–100 방향)* | Tool use vs direct prompting, LLM-as-Judge, RAG pitfalls, agent workflows(LangGraph 등), cost optimization, observability, scaling, ethics, 2026+ trends. |

> **참고:** 위 표에서 *(N–M 방향)* 항목은 원본에 실제 문항이 없는 출제 방향 요약입니다. 해당 구간을 실제 문제로 확장하려면 요청해 주세요.
