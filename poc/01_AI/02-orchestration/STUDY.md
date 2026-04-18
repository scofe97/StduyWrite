# Orchestration 소크라테스 학습

## 학습 목표
- ReAct(Reasoning+Action) 패턴 이해
- OMC 모드(autopilot, ulw, pipeline)의 차이와 선택 기준
- Tool 선택 전략(Greedy, Routing, Planning) 비교

---

## 소크라테스 질문

### Q1: ReAct(Reasoning+Action) 패턴이란?

**탐구 시작**: AI Agent는 어떻게 "생각"과 "행동"을 조합하는가?

**나의 생각 기록**:
```
[여기에 자신의 생각 작성]
```

**AI Agents Ch5 핵심 개념**:

```
ReAct Loop:
┌─────────────────────────────────────────────┐
│ 1. Thought (생각) → 2. Action (행동)        │
│         ↑                    ↓              │
│ 4. Repeat (반복) ← 3. Observation (관찰)    │
└─────────────────────────────────────────────┘
```

**ReAct vs 단순 실행**:
| 방식 | 동작 | 장점 | 단점 |
|------|------|------|------|
| Reflex | 입력→행동 직접 매핑 | 빠름 (밀리초) | 다단계 추론 불가 |
| ReAct | 추론↔행동 인터리브 | 유연한 적응, 디버깅 용이 | 추가 지연/비용 |

**탐구 질문**:
1. 언제 Reflex가 ReAct보다 나은가?
2. ReAct 루프가 무한히 돌지 않으려면?
3. Observation이 예상과 다르면 어떻게 처리하는가?

---

### Q2: autopilot vs ulw vs pipeline 언제 사용?

**OMC 5가지 실행 모드와 Agent 패턴 매핑**:

| OMC 키워드 | Agent 패턴 | 사용 시나리오 | 특징 |
|-----------|-----------|-------------|------|
| `autopilot` | Planner-Executor | 자율 실행, 복잡한 작업 | 계획→실행 분리 |
| `ulw` | Parallel Execution | 3-5배 빠른 병렬 처리 | 독립 작업 동시 실행 |
| `pipeline` | Chains | review→implement→test | 순차 의존성 |
| `swarm` | Multi-Agent Pool | N개 에이전트 협력 | 태스크 풀 공유 |
| `eco` | Token-Efficient | 비용 30-50% 절감 | 작은 모델 활용 |
| `ralph` | Persistent Execution | 완료까지 지속 | 실패 복구 |

**선택 가이드**:

```
작업 분석
    ↓
독립적 병렬 가능? ─Yes→ ulw (3-5배 속도)
    ↓ No
순차적 의존성? ─Yes→ pipeline (A→B→C)
    ↓ No
완전 자율 필요? ─Yes→ autopilot (계획+실행)
    ↓ No
비용 민감? ─Yes→ eco (30-50% 절감)
    ↓ No
        → 기본 실행
```

**실험 아이디어**:
```
# 같은 작업, 다른 모드로 비교
"fix all lint errors in project"

1. 일반: fix all lint errors
2. autopilot: autopilot: fix all lint errors
3. ulw: ulw fix all lint errors
4. ralph ulw: ralph ulw fix all lint errors
```

---

### Q3: Greedy vs Routing vs Planning 도구 선택 전략의 차이?

**AI Agents 핵심 개념**:

#### Standard (Greedy) Tool Selection
- **방식**: 모든 Tool 정의를 FM에 제공, FM이 선택
- **장점**: 구현 간단
- **단점**: 도구 많으면 정확도 저하
- **적합**: 10개 미만 도구

#### Semantic (Routing) Tool Selection
- **방식**: 임베딩으로 Tool 인덱싱, 유사도 검색 후 FM 선택
- **장점**: 대규모 확장성
- **단점**: 의미적 충돌 시 정확도 저하
- **적합**: 10-50개 도구

#### Hierarchical (Planning) Tool Selection
- **방식**: 2단계 선택 (그룹 → 도구)
- **장점**: 높은 정확도, 대규모 확장성
- **단점**: 다중 FM 호출로 느림
- **적합**: 50개 이상 도구, 의미적 유사 도구 많음

**비교 매트릭스**:

```
High Accuracy
    ↑
    │   Hierarchical
    │       ▲
    │   Standard (소규모)
    │       ▲
    │   Semantic
    │       ▲
    │   Standard (대규모)
    │
    └────────────────────→ High Scalability
```

**탐구 질문**:
1. 도구가 20개일 때 어떤 전략이 최적인가?
2. Semantic 선택에서 의미적 충돌이란?
3. Hierarchical의 그룹을 어떻게 정의하는가?

---

## Tool Topology 이해

### 4가지 실행 패턴

```
복잡도 스펙트럼:
Single → Parallel → Chains → Graphs
```

| 토폴로지 | 설명 | FM 호출 | 지연 | 적용 사례 |
|----------|------|---------|------|----------|
| **Single** | 하나의 도구 | 2 | 최저 | 단일 작업 (날씨 조회) |
| **Parallel** | 여러 도구 병렬 | 2+N | 낮음 | 다중 소스 수집 |
| **Chains** | 순차 실행 | 2×Steps | 중간 | A→B→C 워크플로우 |
| **Graphs** | 조건부 분기/통합 | 높음 | 높음 | 복잡한 비즈니스 로직 |

### OMC 모드와 Topology 매핑

| OMC 모드 | Tool Topology | 특징 |
|----------|--------------|------|
| `autopilot` | Graphs | 자동 계획, 동적 분기 |
| `ulw` | Parallel | 독립 작업 동시 실행 |
| `pipeline` | Chains | 순차 의존성 |
| `swarm` | Parallel + Chains | 분산 처리 |

---

## 실험 설계

### 실험 1: 모드별 성능 비교

**목적**: 같은 작업을 다른 OMC 모드로 실행, 시간/토큰 비교

**설정**:
```bash
# 테스트 작업: 프로젝트의 모든 린트 오류 수정

# 일반 실행
fix all lint errors

# autopilot 모드
autopilot: fix all lint errors

# ulw 모드
ulw fix all lint errors

# ralph ulw 모드
ralph ulw: fix all lint errors
```

**측정 항목**:
- [ ] 완료 시간
- [ ] 토큰 사용량
- [ ] 수정된 파일 수
- [ ] 품질 (잔여 오류)

**결과 기록**:
```
[실험 후 작성]
```

---

### 실험 2: Tool Selection 전략 비교

**목적**: 도구 수에 따른 선택 정확도 비교

**설정**:
1. 5개 도구 → Standard
2. 20개 도구 → Semantic
3. 50개 도구 → Hierarchical

**결과 기록**:
```
[실험 후 작성]
```

---

## Agent 유형 요약

### 6가지 Agent 유형

| Agent 유형 | 강점 | 약점 | 최적 사용 사례 |
|------------|------|------|----------------|
| **Reflex** | 밀리초 응답 | 다단계 추론 불가 | 키워드 라우팅, 단순 조회 |
| **ReAct** | 유연한 적응 | 높은 지연/비용 | 탐색적 워크플로우, 문제 해결 |
| **Plan-Execute** | 명확한 작업 분해 | 계획 오버헤드 | 복잡한 다단계 프로세스 |
| **Query-Decomposition** | 근거 있는 검색 | 다중 도구 호출 | 연구, 사실 기반 Q&A |
| **Reflection** | 조기 오류 감지 | 추가 연산/지연 | 고위험, 안전 중요 작업 |
| **Deep Research** | 다단계 적응적 조사 | 매우 높은 비용/지연 | 장기 문헌 검토 |

---

## 핵심 체크리스트

### Agent Types
- [ ] Reflex vs ReAct 차이 설명 가능
- [ ] Planner-Executor 패턴 이해
- [ ] Reflection의 자기 수정 메커니즘 이해

### Tool Selection
- [ ] Standard, Semantic, Hierarchical 비교 가능
- [ ] 도구 수에 따른 전략 선택 가능
- [ ] Tool Description 품질 최적화 가능

### Tool Topologies
- [ ] Single, Parallel, Chains, Graphs 구분
- [ ] 상황에 맞는 토폴로지 선택 가능
- [ ] OMC 모드와 토폴로지 매핑 이해

---

## 다음 단계

- [ ] SUMMARY.md 작성 (개념 정리)
- [ ] experiments/ 폴더에 실험 결과 저장
- [ ] OMC 키워드 조합 패턴 정리

---

## 참고 자료

- AI Agents Chapter 5: Orchestration
- OMC 가이드: 5가지 실행 모드
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
