# Tool Use & MCP 개념 정리

## 핵심 한 줄 요약

> **Tool은 AI Agent가 "생각"에서 "행동"으로 전환하는 다리다. MCP는 이 다리를 표준화하여 재사용 가능하게 만든다.**

---

## 1. Tool이란?

AI Agent가 외부 세계와 상호작용하기 위한 인터페이스입니다. 의사가 청진기, 주사기 등 다양한 도구를 사용하듯이, AI도 작업 유형에 맞는 도구가 필요합니다.

### Tool 없이 AI가 할 수 있는 것
- 텍스트 생성 및 분석
- 질문 응답 (학습된 지식 범위 내)
- 패턴 인식 및 추론

### Tool로 확장되는 영역
- 외부 데이터 조회 (API, 데이터베이스)
- 파일 시스템 조작 (읽기, 쓰기, 삭제)
- 코드 실행 및 테스트
- 외부 서비스 호출 (이메일, 슬랙, 결제)

---

## 2. 4가지 Tool 유형

### 2.1 Local Tools
- **특징**: 로컬에서 실행, 규칙 기반, 예측 가능
- **적합한 작업**: 수학 계산, 시간대 변환, 단위 변환
- **장점**: 정밀성, FM 약점 보완
- **단점**: 확장성 제한, 재배포 필요

### 2.2 API-Based Tools
- **특징**: 외부 서비스와 통신
- **적합한 작업**: 날씨 조회, 주가 확인, 검색 API
- **장점**: 실시간 데이터, 리소스 효율
- **단점**: 네트워크 의존, Rate Limit

### 2.3 Plug-In Tools
- **특징**: 플랫폼이 제공하는 모듈형 도구
- **적합한 작업**: 기존 플랫폼 기능 활용
- **장점**: 빠른 통합, 최소 개발
- **단점**: 커스터마이징 제한, 플랫폼 종속성

### 2.4 MCP Tools
- **특징**: 표준화된 프로토콜 (JSON-RPC 2.0)
- **적합한 작업**: 여러 Agent가 공유하는 서비스
- **장점**: 재사용성, 상호운용성, 발견 가능성
- **단점**: 보안 표준화 미완료

---

## 3. MCP (Model Context Protocol)

### 핵심 개념
MCP는 **"AI를 위한 USB-C 포트"**입니다. 다양한 서비스를 하나의 표준 프로토콜로 연결합니다.

### 아키텍처
```
MCP Client (Agent/LLM App)
    ↓
JSON-RPC 2.0 over HTTPS/WebSocket
    ↓
MCP Server (Data/Services)
    ↓
Cloud Storage, SQL DB, CRM, Business Logic
```

### MCP Server 구성요소
1. **Method Catalog**: 제공하는 기능 목록과 스키마
2. **Endpoint**: 접근 URL
3. **Transport**: stdio, HTTP, WebSocket

### MCP Client 역할
1. Server 발견 및 연결
2. Method Catalog 조회
3. JSON-RPC 요청 전송
4. 응답 처리

---

## 4. Tool Description의 중요성

### 원칙
> **모델은 Tool의 메타데이터(이름, 설명, 스키마)를 보고 어떤 Tool을 호출할지 결정한다.**

### 좋은 Tool Description 작성법

| 요소 | 권장 | 피해야 할 것 |
|------|------|-------------|
| 이름 | 구체적, 동사 시작 | 일반적, 모호함 |
| 설명 | 명확한 목적, 제약조건 | "does stuff" |
| 파라미터 | 타입, 범위, 예시 | 미정의, any |
| 반환값 | 구조, 예시 | 미정의 |

### 예시

```python
# 좋은 예
@tool
def get_stock_price(ticker: str) -> float:
    """Get the current stock price for a given ticker symbol.

    Args:
        ticker: Stock exchange ticker (e.g., 'AAPL', 'GOOGL')

    Returns:
        Current price in USD

    Example:
        get_stock_price('AAPL') -> 178.25
    """
    pass

# 나쁜 예
@tool
def get_data(x):
    """Gets some data."""
    pass
```

---

## 5. 보안 고려사항

### Stateful Tools의 위험
> **실제 사례**: AI Agent가 데이터베이스 성능을 "최적화"하려다 프로덕션 테이블의 절반을 삭제

### 보안 전략

| 전략 | 설명 |
|------|------|
| **Least Privilege** | 필요한 최소 권한만 부여 |
| **좁은 범위 Tool** | 임의 SQL 대신 특정 쿼리만 노출 |
| **입력 검증** | DROP, ALTER 등 위험 패턴 거부 |
| **Prepared Statements** | SQL Injection 방지 |
| **로깅** | 모든 Tool 호출 기록 |

---

## 6. OMC와의 연결

### OMC의 MCP 통합
- 32개 전문 에이전트가 MCP 서버와 상호작용
- Tool 선택은 자동화 (작업 복잡도 기반)
- 3-Tier Memory System으로 컨텍스트 보존

### OMC 키워드와 Tool 관계
| 키워드 | Tool 사용 패턴 |
|--------|---------------|
| `autopilot` | 자동 Tool 선택 및 실행 |
| `ulw` | 병렬 Tool 호출 |
| `swarm` | 분산 Tool 처리 |

---

## 7. Tool 선택 가이드

```
새 기능 필요
    ↓
로컬 실행 가능? ─Yes→ FM 약점 보완? ─Yes→ Local Tool
    ↓ No                    ↓ No
실시간 데이터 필요? ─Yes→ API-Based Tool
    ↓ No
플랫폼 제공? ─Yes→ Plug-In Tool
    ↓ No
여러 Agent 공유? ─Yes→ MCP Tool
    ↓ No
        → API-Based Tool
```

---

## 핵심 체크리스트

- [ ] Tool의 4가지 유형 구분 가능
- [ ] MCP의 아키텍처 설명 가능
- [ ] 좋은 Tool Description 작성 가능
- [ ] 보안 고려사항 적용 가능
- [ ] 상황에 맞는 Tool 유형 선택 가능
