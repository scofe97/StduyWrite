# Multi-Agent Patterns 개념 정리

## 핵심 한 줄 요약

> **소프트웨어 아키텍처의 원칙(모놀리스 분해, 관심사 분리)이 AI 에이전트 시스템에도 동일하게 적용된다. 시스템이 확장됨에 따라 독립적으로 검증, 테스트, 통합, 재사용할 수 있는 작은 에이전트로 분해해야 한다.**

---

## 1. Single vs Multi-Agent

### 원칙
```
단순하게 시작하고, 성능 향상이 필요할 때만 복잡성 추가
```

### Single-Agent 적합 상황

| 조건 | 이유 |
|------|------|
| 도구 10개 미만 | 도구 선택 정확도 유지 |
| 중간 난이도 태스크 | 오버헤드 없이 처리 |
| 빠른 응답 필요 | 통신 지연 최소화 |
| 낮은 환경 복잡도 | 단순 상호작용 |

### Multi-Agent 적합 상황

| 조건 | 이점 |
|------|------|
| 도구 10개 이상 | 전문화된 선택 |
| 복잡한 태스크 | 역할 분담 |
| 병렬 처리 가능 | 속도 향상 |
| 동적 환경 적응 | 유연성 |

### Multi-Agent 핵심 장점

```
Specialization: 도메인별 전문화
Parallelism: 동시 처리
Adaptability: 동적 역할 재할당
Redundancy: 장애 허용
```

---

## 2. 에이전트 추가 원칙

| 원칙 | 설명 |
|------|------|
| **Task Decomposition** | 복잡한 태스크를 관리 가능한 하위 태스크로 분해 |
| **Specialization** | 각 에이전트에 강점에 맞는 역할 할당 |
| **Parsimony** | 필요한 최소 에이전트만 추가 (복잡성 최소화) |
| **Coordination** | 효율적 정보 공유와 충돌 해결 메커니즘 |
| **Robustness** | 장애 허용을 위한 중복성 내장 |
| **Efficiency** | 에이전트 추가의 비용-편익 분석 |

---

## 3. 4가지 Coordination 전략

### Democratic Coordination

```
Agent 1 ←→ Agent 2 ←→ Agent 3
      \       |       /
        → Consensus ←
```

| 특성 | 내용 |
|------|------|
| **동작** | 모든 에이전트에 동등한 의사결정 권한 |
| **장점** | 견고성, 유연성, 공정성 |
| **단점** | 통신 오버헤드, 느린 의사결정 |
| **적합** | 분산 센서 네트워크, 협력 로봇 |

### Manager Coordination

```
        Manager
       /   |   \
  Agent 1  2   3
```

| 특성 | 내용 |
|------|------|
| **동작** | 중앙화된 관리자가 태스크 분배 |
| **장점** | 효율적 의사결정, 명확한 책임 |
| **단점** | 단일 실패점, 확장성 제한 |
| **적합** | 제조 시스템, 고객 지원 센터 |

### Hierarchical Coordination

```
     Strategic Level
       /         \
   Tactical A   Tactical B
    /    \       /    \
 Op1   Op2   Op3   Op4
```

| 특성 | 내용 |
|------|------|
| **동작** | 다중 계층, 상위→전략, 하위→실행 |
| **장점** | 확장성, 중복성, 명확한 권한 |
| **단점** | 설계 복잡성, 통신 지연 |
| **적합** | 공급망 관리, 군사 작전 |

### Actor-Critic Approaches

```
Actor → [Candidate 1, 2, 3] → Critic → Score ≥ 8? → Output
                                  ↓ No
                               → Actor (재생성)
```

| 특성 | 내용 |
|------|------|
| **동작** | Actor 생성, Critic 평가, 반복 개선 |
| **장점** | 품질 개선 (test-time compute) |
| **단점** | 추가 생성 비용 |
| **적합** | 명확한 평가 루브릭이 있는 태스크 |

---

## 4. 통신 기법

### 통신 방식 비교

| 방식 | 핵심 개념 | 장점 | 적합 상황 |
|------|----------|------|----------|
| **A2A Protocol** | Agent Card, JSON-RPC | 상호운용성, 모듈성 | 동적 협업 |
| **Message Brokers** | Pub/Sub | 확장성, 재생 가능 | 분산 태스크 |
| **Actor Frameworks** | 상태 있는 액터 | 통합 상태/동작 | 세션별 격리 |
| **Workflow Engines** | 체크포인트 | 자동 복구 | 장기 실행 |

### A2A Protocol

```python
# Agent Card 예시
agent_card = {
    "identity": "SummarizerAgent",
    "capabilities": ["summarizeText"],
    "endpoint": "http://localhost:8000/api"
}

# JSON-RPC Request
rpc_request = {
    "jsonrpc": "2.0",
    "method": "summarizeText",
    "params": {"text": "Long text..."},
    "id": 123
}
```

### Message Broker 선택

| 요구사항 | 추천 브로커 |
|----------|-------------|
| 프로토타이핑, 저지연 | Redis Stream |
| 이벤트 재생, 내구성 | Kafka |
| 실시간, 엣지 | NATS |
| 단순 비동기 | RabbitMQ |

---

## 5. OMC의 Multi-Agent 구현

### OMC 모드별 패턴

| OMC 모드 | Coordination | 특징 |
|----------|-------------|------|
| `swarm` | Democratic + Pool | N개 에이전트 태스크 공유 |
| `pipeline` | Chains | 순차 전달 |
| `ulw` | Parallel Manager | 병렬 처리 |
| `autopilot` | Hierarchical | 자동 계획/실행 |

### 32개 전문 에이전트

| 도메인 | 에이전트 | 역할 |
|--------|---------|------|
| 아키텍처 | architect | 시스템 설계 |
| 리서치 | researcher | 정보 수집 |
| 디자인 | designer | UI/UX 설계 |
| 테스팅 | QA-tester | 품질 검증 |
| 문서화 | writer | 문서 작성 |
| 검토 | critic | 코드 리뷰 |
| 계획 | planner | 작업 분해 |

### Swarm 모드 특성

- **Decentralization**: 중앙 제어 없이 자기 조직화
- **Local Interactions**: 로컬 규칙으로 복잡한 행동 창발
- **Scalability**: 수백~수천 에이전트 확장
- **Robustness**: 단일 실패 지점 없음

---

## 6. 상태 관리

### Storage Options

| 접근법 | 장점 | 적합 용도 |
|--------|------|----------|
| Relational DB | 유연, 쿼리 가능 | 커스텀 시스템 |
| Vector Stores | 시맨틱 검색 | 지식 집약 |
| Object Storage | 저렴, 대용량 | 아카이브 |
| Workflow Frameworks | 자동 복구 | 장기 실행 |

### Memory 유형

| 유형 | 설명 | 저장 전략 |
|------|------|----------|
| **Episodic** | 단기, 태스크 특화 | 인메모리 |
| **Semantic** | 장기 지식 | 벡터 인덱싱 |
| **Workflow** | 실패 복원 | 체크포인트 |

---

## 7. 단계별 확장 전략

```
Phase 1: Single Agent Prototype
    ↓ (도구 > 10 또는 성능 저하)
Phase 2: Semantic Tool Selection
    ↓ (여전히 부족)
Phase 3: Multi-Agent Decomposition
    ↓ (규모 확장)
Phase 4: Distributed Communication
```

---

## 핵심 체크리스트

### Agent 수 결정
- [ ] Single Agent 한계 인식
- [ ] Multi-Agent 전환 기준 이해
- [ ] Swarm 적용 시나리오 파악

### Coordination 전략
- [ ] 4가지 패턴 비교 가능
- [ ] 상황에 맞는 전략 선택
- [ ] Supervisor-Specialist 패턴 이해

### Communication
- [ ] A2A Protocol 개념 이해
- [ ] Message Broker 선택 기준
- [ ] Actor Framework 활용

### OMC 적용
- [ ] swarm 모드 사용법
- [ ] pipeline 모드 사용법
- [ ] 32개 에이전트 역할 이해
