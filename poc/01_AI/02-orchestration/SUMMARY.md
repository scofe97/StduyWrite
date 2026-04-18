# Orchestration 개념 정리

## 핵심 한 줄 요약

> **Orchestration은 Agent가 Tool들을 조율하여 실제 작업을 수행하는 두뇌다. "무엇을 언제 어떻게 호출할지" 결정하는 핵심 로직이다.**

---

## 1. Orchestration이란?

단순히 어떤 Tool을 호출할지 결정하는 것을 넘어, 각 모델 호출에 적절한 Context를 구성하여 효과적이고 근거 있는 행동을 보장하는 것입니다.

### Orchestration의 역할
```
User Query → Orchestration Layer → Foundation Model
                    ↓                    ↑
            External/Local Tools ←───────┘
                    ↓
            Final Response
```

---

## 2. Agent 유형 스펙트럼

### 복잡도 순서
```
Reflex → ReAct → Planner-Executor → Query-Decomposition → Reflection → Deep Research
(단순)                                                                    (복잡)
```

### 유형별 특성

| 유형 | 핵심 패턴 | 응답 시간 | 적합한 작업 |
|------|----------|----------|------------|
| **Reflex** | if-then 규칙 | 밀리초 | 키워드 라우팅 |
| **ReAct** | 추론↔행동 반복 | 초~분 | 탐색적 문제 해결 |
| **Planner-Executor** | 계획→실행 분리 | 분 | 다단계 프로세스 |
| **Query-Decomposition** | 질문 분해 | 분 | 사실 기반 Q&A |
| **Reflection** | 자기 검토 | 분~시간 | 고위험 작업 |
| **Deep Research** | 다단계 조사 | 시간 | 문헌 검토 |

### ReAct 패턴

```
┌─────────────────────────────────────────────┐
│ 1. Thought (생각) → 2. Action (행동)        │
│         ↑                    ↓              │
│ 4. Repeat (반복) ← 3. Observation (관찰)    │
└─────────────────────────────────────────────┘
```

**장점**: 유연한 적응, 디버깅 용이 (chain of thought 노출)
**단점**: 추가 지연 및 API 비용

---

## 3. Tool Selection 전략

### 3가지 전략 비교

| 전략 | 방식 | 장점 | 단점 | 적합 상황 |
|------|------|------|------|----------|
| **Standard** | 전체 Tool 목록 제공 | 구현 간단 | 도구 많으면 정확도↓ | <10개 도구 |
| **Semantic** | 임베딩 기반 검색 | 확장성 우수 | 의미적 충돌 | 10-50개 도구 |
| **Hierarchical** | 2단계 선택 (그룹→도구) | 높은 정확도 | 느림 | >50개 도구 |

### Semantic Tool Selection 흐름

```
[사전 준비]
Tool Descriptions → Embedding Model → Vector Database

[런타임]
User Query → Embedding → Vector Search → Top-K Tools → FM 선택 → 실행
```

### Hierarchical Tool Selection 흐름

```
User Query → 그룹 선택 (FM) → 해당 그룹 내 도구 선택 (FM) → 실행
```

---

## 4. Tool Topology

### 4가지 실행 패턴

| 토폴로지 | 설명 | 예시 |
|----------|------|------|
| **Single** | 하나의 도구 실행 | 날씨 조회 |
| **Parallel** | 여러 도구 병렬 실행 | 고객 정보 + 주문 이력 + 서비스 로그 동시 조회 |
| **Chains** | 순차적 실행, 이전 결과 의존 | 데이터 수집 → 분석 → 보고서 생성 |
| **Graphs** | 조건부 분기 및 통합 | 이슈 분류 → 유형별 처리 → 요약 |

### 토폴로지 선택 가이드

```
선형 흐름? ─Yes→ 단일 도구? ─Yes→ Single
    │              │ No
    │              └→ 의존성? ─Yes→ Chain
    │                         │ No
    │                         └→ Parallel
    │ No
    └→ 분기 후 통합? ─Yes→ Graph
                    │ No
                    └→ Tree/Parallel
```

---

## 5. OMC 모드와 Agent 패턴

### OMC 5가지 실행 모드

| OMC 모드 | Agent 패턴 | Tool Topology | 사용 시나리오 |
|----------|-----------|--------------|--------------|
| `autopilot` | Planner-Executor | Graphs | 완전 자율 실행 |
| `ulw` | Parallel Execution | Parallel | 3-5배 빠른 병렬 처리 |
| `pipeline` | Chains | Chains | review→implement→test |
| `swarm` | Multi-Agent Pool | Parallel+Chains | N개 에이전트 협력 |
| `eco` | Token-Efficient | - | 비용 30-50% 절감 |
| `ralph` | Persistent Execution | - | 완료까지 지속 |

### 키워드 조합

```
[실행 스킬] + [향상 스킬] + [보장 옵션]

예시:
ralph ulw: migrate database
└─────┘└──┘  └────────────┘
지속성  병렬     작업 내용
```

### 모드 선택 가이드

```
작업 분석
    ↓
독립적 병렬 가능? ─Yes→ ulw
    ↓ No
순차적 의존성? ─Yes→ pipeline
    ↓ No
완전 자율 필요? ─Yes→ autopilot
    ↓ No
비용 민감? ─Yes→ eco
    ↓ No
완료 보장 필요? ─Yes→ ralph
```

---

## 6. Context Engineering

### Prompt Engineering vs Context Engineering

| 측면 | Prompt Engineering | Context Engineering |
|------|-------------------|---------------------|
| **초점** | 효과적인 지침 작성 | 동적 입력 조립 |
| **범위** | 단일 프롬프트 | 전체 워크플로우 |
| **구성요소** | 지침, 예시 | 사용자 입력, 검색된 지식, 상태, 시스템 프롬프트 |

### Context 구성 요소

```
Context
├── User Input
│   ├── Current message
│   └── Conversation history
├── Retrieved Knowledge
│   ├── Memory snippets
│   └── External KB
├── Workflow State
│   ├── Current step
│   └── Previous results
└── System Instructions
    ├── Agent role
    └── Allowed actions
```

### Context Engineering 원칙

1. **관련성 우선**: 관련 정보만 검색
2. **명확성 유지**: 구조화된 포맷 사용
3. **요약 기법**: 긴 이력을 핵심 보존하며 압축
4. **동적 조립**: 각 단계에서 목표/단계/입력 반영

---

## 7. 실무 적용 가이드

### Orchestration 설계 Best Practices

1. **요구사항 분석**: 지연, 정확도 요구사항 파악
2. **작업 복잡도 평가**: 필요한 행동 수 결정
3. **적응성 평가**: 계획 변경 필요 여부
4. **테스트 설계**: 대표적인 테스트 케이스
5. **단순성 원칙**: 요구사항 충족하는 가장 단순한 접근법

### Latency vs Accuracy 트레이드오프

```
High Accuracy
    ↑
    │   Deep Research
    │       ▲
    │   Reflection
    │       ▲
    │   Planner-Executor
    │       ▲
    │   ReAct
    │       ▲
    │   Reflex
    └────────────────────→ High Latency
```

---

## 핵심 체크리스트

### Agent Types
- [ ] Reflex: 직접 입력→행동 매핑, 밀리초 응답
- [ ] ReAct: Reasoning + Action 인터리브
- [ ] Planner-Executor: Planning과 Execution 분리
- [ ] Reflection: 자기 검토 및 오류 수정

### Tool Selection
- [ ] Standard: 간단, 소규모 도구셋
- [ ] Semantic: 임베딩 기반 검색, 확장성
- [ ] Hierarchical: 그룹화, 높은 정확도

### Tool Topologies
- [ ] Single: 하나의 도구, 최소 지연
- [ ] Parallel: 여러 도구 병렬 실행
- [ ] Chains: 순차적 의존성 있는 실행
- [ ] Graphs: 조건부 분기 및 통합

### OMC 모드
- [ ] autopilot: 완전 자율 실행
- [ ] ulw: 병렬 처리 (3-5배 속도)
- [ ] pipeline: 순차 체이닝
- [ ] swarm: 에이전트 협력
- [ ] eco: 토큰 효율
- [ ] ralph: 완료 보장
