# Tool Use & MCP 소크라테스 학습

## 학습 목표
- MCP가 없으면 AI는 무엇을 못하는지 이해
- Tool의 `description`이 AI 행동에 미치는 영향 파악
- 4가지 Tool 유형의 차이와 적용 사례 학습

---

## 소크라테스 질문

### Q1: MCP가 없으면 AI는 무엇을 못하는가?

**탐구 시작**: AI Agent는 Foundation Model(LLM)만으로는 무엇이 제한되는가?

**나의 생각 기록**:
```
[여기에 자신의 생각 작성]
```

**AI Agents Ch4 참조 포인트**:
- Tool은 AI Agent가 **정보를 검색**하고, **작업을 수행**하며, **환경과 상호작용**할 수 있게 하는 핵심 구성 요소
- MCP 없이는:
  - 외부 시스템 접근 불가 (데이터베이스, API, 파일 시스템)
  - 실시간 데이터 획득 불가 (날씨, 주가, 뉴스)
  - 행동 수행 불가 (이메일 전송, 파일 생성, 코드 실행)

**탐구 질문**:
1. LLM만으로 할 수 있는 것은?
2. LLM + Tool로 확장되는 영역은?
3. MCP가 기존 API 통합 방식보다 나은 점은?

---

### Q2: Tool의 `description`이 AI 행동에 어떤 영향을 주는가?

**핵심 인사이트**:
> **모델은 Tool의 메타데이터(이름, 설명, 스키마)를 보고 어떤 Tool을 호출할지 결정한다.**

**좋은 vs 나쁜 Tool 설명 비교**:

| 요소 | 좋은 예 | 나쁜 예 |
|------|---------|---------|
| 이름 | `multiply` (정확, 좁은 범위) | `calculate` (너무 일반적) |
| 설명 | "Multiply 'x' times 'y'." | "Performs calculations" |
| 스키마 | x: float, y: float -> float | 미정의 |

**실험 아이디어**:
```python
# 같은 기능, 다른 설명으로 AI 행동 변화 관찰
@tool
def vague_tool(data: str) -> str:
    """Process the data."""
    return process(data)

@tool
def specific_tool(customer_id: str) -> dict:
    """Retrieve customer profile including name, email, and order history."""
    return get_customer(customer_id)
```

**탐구 질문**:
1. 모호한 설명일 때 AI는 어떻게 행동하는가?
2. 여러 Tool이 비슷한 설명을 가지면 어떻게 되는가?
3. 설명에 예시를 포함하면 어떤 차이가 있는가?

---

### Q3: 4가지 Tool 유형의 차이는?

**AI Agents 핵심 개념**:
```
Tool Types:
├── Local Tools: 로컬 실행, 규칙 기반, 예측 가능
├── API Tools: 외부 서비스 연동, 실시간 데이터
├── Plugin Tools: 플랫폼 제공 모듈, 빠른 배포
└── MCP Tools: 표준화된 프로토콜, 상호운용성
```

**비교 매트릭스**:

| 유형 | 장점 | 단점 | 적합한 상황 |
|------|------|------|-------------|
| Local | 정밀성, 예측 가능 | 확장성 제한 | 수학, 시간대 변환 |
| API | 실시간 데이터, 외부 통합 | 네트워크 의존 | 날씨, 주가 조회 |
| Plugin | 빠른 통합, 최소 개발 | 커스터마이징 제한 | 기존 플랫폼 기능 활용 |
| MCP | 재사용성, 표준화 | 보안 미완성 | 여러 Agent 공유 |

**MCP의 핵심 가치** ("AI를 위한 USB-C 포트"):
```
Before MCP:
Agent A ──→ Custom Adapter 1 ──→ Service 1
Agent A ──→ Custom Adapter 2 ──→ Service 2
Agent B ──→ Custom Adapter 1 ──→ Service 1
→ 취약, 오류 발생 쉬움, 유지보수 어려움

After MCP:
Agent A ──┐
          ├──→ MCP Protocol ──→ Service 1, 2, 3
Agent B ──┘
→ 균일한 인터페이스, 재사용 가능, 확장 용이
```

---

## 실험 설계

### 실험 1: MCP 서버 생성 관찰

**목적**: AI에게 MCP 서버 생성을 요청하고 과정 관찰

**프롬프트**:
```
autopilot: create a simple MCP tool server with weather, calculator tools
```

**관찰 포인트**:
- [ ] AI가 어떤 구조로 서버를 설계하는가?
- [ ] Tool description을 어떻게 작성하는가?
- [ ] JSON-RPC 2.0 프로토콜을 어떻게 구현하는가?

**결과 기록**:
```
[실험 후 작성]
```

---

### 실험 2: Tool Description 품질 비교

**목적**: 설명 품질에 따른 AI 도구 선택 정확도 비교

**설정**:
1. 모호한 설명의 Tool 세트
2. 명확한 설명의 Tool 세트
3. 동일한 작업 요청

**결과 기록**:
```
[실험 후 작성]
```

---

## 핵심 체크리스트

### LangChain 기초
- [ ] `ChatOpenAI`, `HumanMessage`, `AIMessage` 역할 이해
- [ ] `@tool` 데코레이터로 함수 등록
- [ ] `.bind_tools()`로 Model에 Tool 바인딩
- [ ] `.invoke()`로 Model 호출 및 Tool 실행

### Tool Types
- [ ] Local Tools: 정밀성, FM 약점 보완
- [ ] API-Based Tools: 실시간 데이터, 외부 서비스 통합
- [ ] Plug-In Tools: 플랫폼 제공, 빠른 통합
- [ ] MCP Tools: 표준화된 프로토콜, 재사용성

### 보안
- [ ] Least Privilege 원칙
- [ ] 입력 검증 및 SQL Injection 방지
- [ ] 좁은 범위의 Tool 등록
- [ ] 로깅 및 실시간 모니터링

---

## 다음 단계

- [ ] SUMMARY.md 작성 (개념 정리)
- [ ] experiments/ 폴더에 AI 생성 코드 저장
- [ ] OMC와 연결점 정리

---

## 참고 자료

- AI Agents Chapter 4: Tool Use
- OMC 가이드: MCP 통합 섹션
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
