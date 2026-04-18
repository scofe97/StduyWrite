# Multi-Agent Patterns 소크라테스 학습

## 학습 목표
- 단일 vs 멀티 에이전트 선택 기준 이해
- 4가지 조율 패턴(Democratic, Manager, Hierarchical, Actor-Critic) 비교
- 에이전트 간 정보 공유 방법 학습

---

## 소크라테스 질문

### Q1: 단일 에이전트 vs 멀티 에이전트 언제 선택?

**탐구 시작**: 왜 여러 에이전트가 필요한가? 하나로 충분하지 않은가?

**나의 생각 기록**:
```
[여기에 자신의 생각 작성]
```

**AI Agents Ch8 핵심 개념**:

```
원칙: 단순하게 시작하고, 성능 향상이 필요할 때만 복잡성 추가
```

**Single-Agent 적합 상황**:
| 조건 | 설명 |
|------|------|
| 중간 난이도 태스크 | 복잡하지 않은 단일 도메인 작업 |
| 제한된 도구 수 | 10개 미만의 도구 집합 |
| 낮은 환경 복잡도 | 단순한 상호작용 패턴 |
| 지연 시간 중요 | 빠른 응답이 필수인 경우 |

**Multi-Agent 적합 상황**:
- 복잡한 태스크와 다양한 도구셋 필요
- 병렬 처리 요구
- 동적 환경 적응 필요
- 전문화된 도메인 지식 필요

**탐구 질문**:
1. 도구가 몇 개일 때 멀티 에이전트를 고려해야 하는가?
2. 멀티 에이전트의 통신 오버헤드는 얼마나 되는가?
3. 어떤 작업이 병렬화 불가능한가?

---

### Q2: Democratic vs Manager vs Hierarchical 조율 패턴의 차이?

**AI Agents 핵심 개념**:

#### Democratic Coordination
```
Agent 1 ←→ Agent 2 ←→ Agent 3
      \       |       /
        → Consensus ←
```
- **특징**: 모든 에이전트에 동등한 의사결정 권한
- **장점**: 견고성 (단일 실패점 없음), 공정성
- **단점**: 통신 오버헤드, 느린 의사결정
- **적합**: 분산 센서 네트워크, 협력 로봇

#### Manager Coordination
```
        Manager
       /   |   \
  Agent 1  2   3
```
- **특징**: 중앙화된 관리자 에이전트
- **장점**: 효율적 의사결정, 명확한 책임 할당
- **단점**: 단일 실패 지점, 확장성 제한
- **적합**: 제조 시스템, 고객 지원 센터

#### Hierarchical Coordination
```
     Strategic Level
       /         \
   Tactical A   Tactical B
    /    \       /    \
 Op1   Op2   Op3   Op4
```
- **특징**: 다중 계층 조직
- **장점**: 확장성, 중복성, 명확한 권한
- **단점**: 설계 복잡성, 통신 지연
- **적합**: 공급망 관리, 군사 작전

#### Actor-Critic Approaches
```
Actor → [Candidate 1, 2, 3] → Critic
                               ↓
                        Score ≥ 8? → Output
                               ↓ No
                            → Actor (재생성)
```
- **특징**: Actor가 후보 생성, Critic이 품질 평가
- **장점**: 반복적 품질 개선
- **단점**: 추가 생성 비용
- **적합**: 명확한 평가 루브릭이 있는 생성 태스크

**탐구 질문**:
1. 우리 팀 구조와 가장 유사한 패턴은?
2. 패턴을 혼합해서 사용할 수 있는가?
3. 장애 발생 시 각 패턴의 복구 방식은?

---

### Q3: 에이전트 간 정보 공유 방법은?

**AI Agents 핵심 개념**:

#### Communication Techniques

| 방식 | 특징 | 적합 상황 |
|------|------|----------|
| **A2A Protocol** | JSON-RPC 2.0, Agent Card | 동적 에코시스템 협업 |
| **Message Brokers** | Pub/Sub, 비동기 | 분산 태스크 라우팅 |
| **Actor Frameworks** | 상태 있는 액터 | 세션별 격리 에이전트 |
| **Workflow Engines** | 자동 복구, 체크포인트 | 장기 실행 워크플로우 |

#### A2A Protocol (Google)
```python
agent_card = {
    "identity": "SummarizerAgent",
    "capabilities": ["summarizeText"],
    "schemas": {
        "summarizeText": {
            "input": {"text": "string"},
            "output": {"summary": "string"}
        }
    },
    "endpoint": "http://localhost:8000/api"
}
```

#### Message Brokers

| 브로커 | 특징 | 적합 용도 |
|--------|------|----------|
| **Apache Kafka** | 고처리량, 내구성 | 이벤트 재생 가능 |
| **Redis Stream** | 저지연, 메모리 기반 | 프로토타이핑 |
| **NATS** | 경량, 실시간 | 엣지 환경 |
| **RabbitMQ** | 단순 배포 | 간단한 비동기 |

#### Actor Frameworks

| 프레임워크 | 언어 | 특징 |
|------------|------|------|
| **Ray** | Python | `@ray.remote` 데코레이터 |
| **Orleans** | .NET | Virtual Actor |
| **Akka** | JVM | 클러스터링, 샤딩 |

**탐구 질문**:
1. 어떤 통신 방식이 디버깅하기 쉬운가?
2. 메시지 유실 시 복구 방법은?
3. 상태를 어디에 저장해야 하는가?

---

## OMC Swarm 모드 이해

### Swarm의 특성

| 특징 | 설명 |
|------|------|
| **Decentralization** | 중앙 제어 없이 자기 조직화 |
| **Local Interactions** | 간단한 로컬 규칙으로 복잡한 행동 창발 |
| **Scalability** | 수백~수천 에이전트로 확장 가능 |
| **Robustness** | 단일 실패 지점 없음 |

### OMC Swarm 사용법

```bash
# N개 에이전트가 태스크 풀 공유
swarm: process all test files
```

**특징**:
- 각 에이전트는 5분 타임아웃
- 원자적 태스크 claim 및 처리
- 태스크 풀 공유

---

## 실험 설계

### 실험 1: Single vs Multi-Agent 비교

**목적**: 같은 작업을 단일/다중 에이전트로 실행, 품질 비교

**설정**:
```bash
# 단일 에이전트
autopilot: build a REST API

# 멀티 에이전트 (Swarm)
swarm: build a REST API with architect, developer, tester
```

**측정 항목**:
- [ ] 완료 시간
- [ ] 토큰 사용량
- [ ] 코드 품질 (린트, 테스트 통과율)
- [ ] 아키텍처 일관성

**결과 기록**:
```
[실험 후 작성]
```

---

### 실험 2: Pipeline 패턴 관찰

**목적**: 순차 에이전트 체이닝의 정보 전달 관찰

**설정**:
```bash
# Pipeline: review → implement → test
pipeline: architect -> developer -> tester
```

**관찰 포인트**:
- [ ] 각 단계의 산출물은?
- [ ] 다음 단계로 어떤 정보가 전달되는가?
- [ ] 이전 단계의 결정이 다음 단계에 어떻게 영향?

**결과 기록**:
```
[실험 후 작성]
```

---

## OMC 32개 에이전트 매핑

### 도메인별 에이전트

| 도메인 | 에이전트 | 역할 |
|--------|---------|------|
| **아키텍처** | architect | 시스템 설계 |
| **리서치** | researcher | 정보 수집 |
| **디자인** | designer | UI/UX 설계 |
| **테스팅** | QA-tester | 품질 검증 |
| **문서화** | writer | 문서 작성 |
| **검토** | critic | 코드 리뷰 |
| **계획** | planner | 작업 분해 |

### 자동 모델 선택

| 작업 복잡도 | 모델 | 특징 |
|------------|------|------|
| 간단 | Haiku | 빠름, 저비용 |
| 복잡 | Opus | 높은 추론력 |

---

## 핵심 체크리스트

### Agent 수 결정
- [ ] Single Agent의 장단점 이해
- [ ] Multi-Agent 전환 기준 (도구 수, 복잡도, 병렬 처리)
- [ ] Swarm의 특성과 적용 시나리오

### Coordination 전략
- [ ] Democratic, Manager, Hierarchical, Actor-Critic 비교
- [ ] 각 전략의 장단점과 적합한 시나리오
- [ ] Supervisor-Specialist 패턴 구현

### Communication
- [ ] A2A Protocol (Agent Card, JSON-RPC)
- [ ] Message Broker 종류와 선택 기준
- [ ] Actor Framework (Ray, Orleans, Akka)

---

## 다음 단계

- [ ] SUMMARY.md 작성 (개념 정리)
- [ ] experiments/ 폴더에 실험 결과 저장
- [ ] OMC swarm/pipeline 사용법 정리

---

## 참고 자료

- AI Agents Chapter 8: From One Agent to Many
- OMC 가이드: Swarm, Pipeline 모드
- [A2A Protocol - Google Cloud AI](https://cloud.google.com/ai)
