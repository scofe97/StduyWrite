# Chapter 11. Building with LLMs: LLM 애플리케이션 UX 패턴

---

### 📌 핵심 요약
> LLM은 기존 컴퓨팅과 달리 **비결정적**이고 **유연한** 인터페이스를 제공한다. 기존 생산성 소프트웨어의 "도구 팔레트 + 캔버스" 패러다임은 LLM 시대에 재고가 필요하다. 본 챕터에서는 LLM 네이티브 애플리케이션 구축을 위한 **3가지 UX 패턴**을 제시한다: **(1) Interactive Chatbots** - AI 사이드킥을 기존 앱에 추가, **(2) Collaborative Editing** - LLM을 협업 편집자로 활용, **(3) Ambient Computing** - 백그라운드에서 지속적으로 작동하는 LLM 에이전트.

---

### 🎯 학습 목표
- 기존 소프트웨어 인터페이스와 LLM 네이티브 인터페이스의 차이를 이해한다
- Interactive Chatbot 패턴의 구성 요소와 확장 방법을 안다
- Collaborative Editing 패턴의 기술적 요구사항을 설명할 수 있다
- Ambient Computing 패턴의 개념과 필요 구성 요소를 안다
- 각 패턴의 적합한 사용 사례를 판단할 수 있다

---

### 📖 본문 정리

#### 1. LLM과 기존 컴퓨팅의 차이

##### 기존 컴퓨터의 특성
- **결정적**: 같은 입력 → 항상 같은 출력
- **정밀함 요구**: 오타, 불명확한 입력 → 오류
- **신뢰성 기반 UI**: 모든 기능이 미리 정의됨

##### LLM의 특성
- **비결정적**: 같은 입력 → 다양한 출력 가능
- **유연함**: 오타, 모호한 입력도 처리 가능
- **"살짝 벗어난" 결과 가능성**: 유연함의 대가

```
┌─────────────────────────────────────────────────────────────┐
│           Traditional Software vs LLM-Native Software        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Traditional (Figma, Word 등)                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  ┌──────────────┐      ┌──────────────────────┐    │   │
│   │  │ Tool Palette │      │       Canvas         │    │   │
│   │  │              │      │                      │    │   │
│   │  │ • Shapes     │      │   [User's Creation]  │    │   │
│   │  │ • Lines      │      │                      │    │   │
│   │  │ • Text       │      │                      │    │   │
│   │  └──────────────┘      └──────────────────────┘    │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   → 모든 기능이 미리 코딩됨                                   │
│   → 인터페이스 설계 시 모든 기능 파악 가능                     │
│                                                             │
│   LLM-Native                                                │
│   ┌─────────────────────────────────────────────────────┐   │
│   │           ???                                       │   │
│   │                                                     │   │
│   │   • 기능이 미리 정의되지 않음                         │   │
│   │   • 새로운 인터페이스 패러다임 필요                   │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

#### 2. Pattern 1: Interactive Chatbots

기존 애플리케이션에 **AI 사이드킥**을 추가하는 가장 쉬운 방법.

##### 개념

```
┌─────────────────────────────────────────────────────────────┐
│                    Interactive Chatbot Pattern               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────┐  ┌──────────────────┐    │
│   │                             │  │   AI Sidekick    │    │
│   │      Main Application       │  │     (Chat)       │    │
│   │         (Canvas)            │◀─┼─▶               │    │
│   │                             │  │  💬 "How can I   │    │
│   │   [User's Work Area]        │  │     help you?"   │    │
│   │                             │  │                  │    │
│   │                             │  │  [User Input]    │    │
│   │                             │  │                  │    │
│   └─────────────────────────────┘  └──────────────────┘    │
│                                                             │
│   예시: VSCode + GitHub Copilot Chat                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### 기본 구성 요소

| 구성 요소 | 설명 | 필수 여부 |
|----------|------|----------|
| **Chat Model** | 대화 튜닝된 모델 (멀티턴 상호작용) | 필수 |
| **Conversation History** | 이전 메시지 기억 | 필수 |

##### 확장 구성 요소

| 구성 요소 | 설명 | 용도 |
|----------|------|------|
| **Streaming Output** | 토큰/문장 단위 스트리밍 | 지연 시간 체감 완화 |
| **Tool Calling** | 캔버스/도구 조작 기능 노출 | 애플리케이션 상호작용 |
| **Human-in-the-Loop** | 사용자 확인/편집 후 실행 | 제어권 반환 |

##### 도구 호출 예시

```python
# 예시: 워드 프로세서용 도구
tools = [
    {
        "name": "get_selected_text",
        "description": "현재 선택된 텍스트를 가져옴"
    },
    {
        "name": "insert_text_at_cursor",
        "description": "커서 위치에 텍스트 삽입",
        "parameters": {"text": "삽입할 텍스트"}
    },
    {
        "name": "replace_selected_text",
        "description": "선택된 텍스트를 새 텍스트로 교체",
        "parameters": {"new_text": "새 텍스트"}
    }
]
```

> **Note**: 스트리밍 채팅은 현재 LLM의 원형적 애플리케이션이다. 하지만 미래에는 **LLM 시대의 커맨드 라인**이 될 수도 있다—즉, 직접적인 프로그래밍 접근에 가장 가까운, 틈새 인터페이스로.

---

#### 3. Pattern 2: Collaborative Editing with LLMs

LLM 에이전트를 **협업 편집자 중 한 명**으로 활용.

##### 협업 편집의 진화

```
┌─────────────────────────────────────────────────────────────┐
│              Evolution of Collaborative Editing              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Level 1: Save and Send                                    │
│   ┌─────┐    ┌─────┐    ┌─────┐                            │
│   │User1│───▶│File │───▶│User2│   (한 번에 한 명만 편집)     │
│   └─────┘    └─────┘    └─────┘                            │
│   예: 이메일로 파일 전송, MS Office                          │
│                                                             │
│   Level 2: Version Control                                  │
│   ┌─────┐              ┌─────┐                             │
│   │User1│──┐        ┌──│User2│   (동시 편집 → 나중에 병합)   │
│   └─────┘  │  Merge │  └─────┘                             │
│            ▼        ▼                                       │
│         ┌────────────┐                                      │
│         │   Merged   │                                      │
│         └────────────┘                                      │
│   예: Git/GitHub                                            │
│                                                             │
│   Level 3: Real-Time Collaboration                          │
│   ┌─────┐                                                  │
│   │User1│──┐                                               │
│   └─────┘  │  ┌────────────┐                               │
│            ├──│  Shared    │   (동시 편집, 실시간 동기화)    │
│   ┌─────┐  │  │  Document  │                               │
│   │User2│──┘  └────────────┘                               │
│   └─────┘                                                  │
│   예: Google Docs, Google Sheets                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### LLM 협업 형태

| 형태 | 설명 | 예시 |
|------|------|------|
| **Always-on Copilot** | 다음 문장 완성 제안 | GitHub Copilot |
| **Asynchronous Drafter** | 리서치 후 초안 작성 | 백그라운드 문서 생성 |

##### 필수 구성 요소

```
┌─────────────────────────────────────────────────────────────┐
│           Collaborative Editing Requirements                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Shared State (공유 상태)                                 │
│     └─ LLM과 사용자가 동일한 문서 상태 접근/이해              │
│                                                             │
│  2. Task Manager (작업 관리자)                               │
│     └─ 장시간 작업 스케줄링, 오류 복구, 큐잉                  │
│                                                             │
│  3. Merging Forks (포크 병합)                                │
│     ├─ 수동: Git 스타일                                     │
│     └─ 자동: CRDT, OT (Google Docs 방식)                    │
│                                                             │
│  4. Concurrency (동시성)                                     │
│     └─ 중단, 취소, 재라우팅, 큐잉 처리                        │
│                                                             │
│  5. Undo/Redo Stack                                         │
│     └─ 이전 상태로 되돌리기                                  │
│                                                             │
│  6. Intermediate Output (중간 출력)                          │
│     └─ 점진적 출력으로 병합 용이화                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### 병합 알고리즘 비교

| 알고리즘 | 설명 | 사용처 |
|----------|------|--------|
| **CRDT** | Conflict-free Replicated Data Type | 분산 시스템 |
| **OT** | Operational Transformation | Google Docs |
| **Manual Merge** | 사용자가 충돌 해결 | Git |

---

#### 4. Pattern 3: Ambient Computing

**백그라운드에서 지속적으로 작동**하며 "흥미로운" 이벤트 발생 시 알림.

##### 기존 Ambient Computing 예시

- 주식 가격 알림 (특정 가격 이하 시 알림)
- Google Alerts (새 검색 결과 발견 시 알림)
- 인프라 모니터링 (비정상 패턴 감지 시 알림)

##### 기존 방식의 한계

```
"흥미로운" 정의의 딜레마:

┌───────────────┐
│   Useful      │ ◀─ 원하는 시점에 알림
├───────────────┤
│      vs       │
├───────────────┤
│   Practical   │ ◀─ 규칙 설정에 시간 소모 최소화
└───────────────┘

기존: 사용자가 미리 규칙 정의 필요 (시간 소모)
LLM:  추론으로 규칙 대체 (유용성 + 실용성)
```

##### Collaborative vs Ambient 차이

| 구분 | Collaborative | Ambient |
|------|---------------|---------|
| **동시성** | 사용자와 LLM이 동시에 작업 | LLM만 백그라운드 작업 |
| **상호작용** | 서로의 작업 참조 | 사용자는 다른 일 수행 |
| **출력 시점** | 즉각적 협업 | 이벤트 발생 시 알림 |

##### 필수 구성 요소

```
┌─────────────────────────────────────────────────────────────┐
│              Ambient Computing Requirements                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Triggers (트리거)                                        │
│     └─ 환경에서 새 정보 수신/폴링                            │
│                                                             │
│  2. Long-term Memory (장기 기억)                             │
│     └─ 이전 정보 DB로 새 이벤트 감지                         │
│                                                             │
│  3. Reflection / Learning (반영/학습)                        │
│     └─ 이벤트 발생 후 규칙 업데이트                          │
│     └─ "흥미로운" 기준 학습                                  │
│                                                             │
│  4. Summarize Output (출력 요약)                             │
│     └─ 방대한 출력을 핵심만 요약                             │
│                                                             │
│  5. Task Manager (작업 관리자)                               │
│     └─ 지속적 백그라운드 작업 관리, 큐잉, 오류 복구          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### Reflection (학습) 흐름

```
┌─────────────────────────────────────────────────────────────┐
│                    Reflection Loop                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [New Event] ──▶ [Detect Interesting?]                     │
│                          │                                  │
│                    ┌─────┴─────┐                            │
│                    ▼           ▼                            │
│                  Yes          No                            │
│                    │           │                            │
│                    ▼           │                            │
│             [Notify User]      │                            │
│                    │           │                            │
│                    ▼           │                            │
│             [User Feedback]    │                            │
│                    │           │                            │
│                    ▼           ▼                            │
│              [Update Rules in Long-term Memory]             │
│                    │                                        │
│                    ▼                                        │
│            [Improved Detection]                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

#### 5. 세 가지 패턴 비교

```
┌─────────────────────────────────────────────────────────────┐
│                   Pattern Comparison                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    복잡도 증가 ───────────────────▶          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Interactive │  │Collaborative │  │   Ambient    │      │
│  │   Chatbot    │  │   Editing    │  │  Computing   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  • 사이드바 채팅    • 공유 문서 편집   • 백그라운드 모니터링  │
│  • 기존 앱에 추가   • 실시간 협업     • 이벤트 기반 알림     │
│  • 가장 쉬운 구현   • 병합/동시성     • 장기 기억/학습       │
│                                                             │
│  예: Copilot Chat   예: Google Docs   예: 스마트 알림       │
│                      + LLM 에이전트     인프라 모니터링      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 패턴 | 구현 난이도 | 핵심 요구사항 | 적합한 사용 사례 |
|------|------------|--------------|-----------------|
| **Interactive Chatbot** | 낮음 | Chat Model, History | 기존 앱 확장 |
| **Collaborative Editing** | 중간 | Shared State, Merging | 문서 협업 |
| **Ambient Computing** | 높음 | Triggers, Memory, Learning | 모니터링, 알림 |

---

### 🔍 심화 학습

#### 패턴 선택 가이드

```
어떤 패턴을 사용할까?

사용자가 LLM과 동시에 작업하는가?
├─ No ──▶ 사용자가 다른 일 하는 동안 LLM 작동?
│              ├─ Yes ──▶ Ambient Computing
│              └─ No ───▶ Interactive Chatbot
│
└─ Yes ─▶ 같은 문서/아티팩트를 수정하는가?
              ├─ Yes ──▶ Collaborative Editing
              └─ No ───▶ Interactive Chatbot
```

#### 스트리밍의 미래

```
현재: 스트리밍 채팅 = LLM의 원형적 애플리케이션
      (개발자가 처음 배우는 것)

미래 가능성:
├─ 계속 주류로 유지
└─ "LLM 시대의 커맨드 라인"이 됨
   └─ 직접적 프로그래밍 접근
   └─ 틈새 인터페이스화
```

#### CRDT vs OT

| 특성 | CRDT | OT |
|------|------|-----|
| **원리** | 충돌 없는 자료 구조 | 연산 변환 |
| **복잡도** | 구현 복잡 | 알고리즘 복잡 |
| **확장성** | P2P 친화적 | 서버 중심 |
| **사용처** | Figma, Yjs | Google Docs |

---

### 💡 실무 적용 포인트

1. **점진적 도입**: Interactive Chatbot → Collaborative Editing → Ambient Computing 순서로 복잡도 증가
2. **기존 앱 확장**: 가장 빠른 ROI는 Interactive Chatbot 패턴
3. **Human-in-the-Loop 필수**: 도구 호출 시 사용자 확인 단계 추가
4. **스트리밍 활용**: 모든 패턴에서 지연 시간 체감 완화
5. **병합 전략 선택**: 실시간 협업은 CRDT/OT, 비동기 협업은 Git 스타일
6. **Ambient 패턴의 학습**: Reflection 루프로 "흥미로운" 기준 지속 개선
7. **Task Manager 필수**: Collaborative/Ambient 패턴에서 장시간 작업 관리
8. **빌드 → 피드백 → 반복**: "무언가 구리더라도 만들고, 사용자와 대화하고, 반복"

---

### ✅ 정리 체크리스트

- [ ] 기존 소프트웨어와 LLM 네이티브 소프트웨어의 인터페이스 차이를 설명할 수 있다
- [ ] Interactive Chatbot 패턴의 기본 구성 요소(Chat Model, History)를 안다
- [ ] Chatbot 확장 요소(Streaming, Tool Calling, Human-in-the-Loop)를 안다
- [ ] 협업 편집의 세 단계(Save&Send, Version Control, Real-time)를 구분할 수 있다
- [ ] Collaborative Editing에 필요한 6가지 요소를 나열할 수 있다
- [ ] CRDT와 OT의 차이를 안다
- [ ] Ambient Computing의 개념과 기존 예시를 안다
- [ ] Collaborative와 Ambient 패턴의 동시성 차이를 설명할 수 있다
- [ ] Ambient Computing에 필요한 5가지 요소를 나열할 수 있다
- [ ] Reflection(학습) 루프의 역할을 설명할 수 있다
- [ ] 세 패턴의 적합한 사용 사례를 판단할 수 있다

---

### 🔗 참고 자료

- [GitHub Copilot Chat Documentation](https://docs.github.com/en/copilot)
- [Google Docs OT Algorithm](https://developers.google.com/docs/api/concepts/operational-transform)
- [CRDT.tech](https://crdt.tech/)
- [Yjs - CRDT Framework](https://yjs.dev/)
- [LangChain Streaming Guide](https://python.langchain.com/docs/concepts/streaming/)
- [LangGraph Human-in-the-Loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)
