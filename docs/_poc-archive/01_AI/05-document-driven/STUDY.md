# Document-Driven Development 소크라테스 학습

## 학습 목표
- CLAUDE.md가 AI 행동에 미치는 영향 이해
- 규칙 파일로 AI 실수를 방지하는 방법 학습
- Progressive Delegation의 개념과 적용

---

## 소크라테스 질문

### Q1: CLAUDE.md가 AI 행동에 어떻게 영향을 주는가?

**탐구 시작**: 같은 AI인데 프로젝트마다 왜 다르게 동작하는가?

**나의 생각 기록**:
```
[여기에 자신의 생각 작성]
```

**AI Agents Ch13 핵심 개념**:

> **Human-Agent 협업의 성공은 기술적 역량만큼이나 인터페이스 설계, 신뢰 보정, 거버넌스 구조에 달려 있다.**

**CLAUDE.md의 역할**:
1. **Context 제공**: 프로젝트 특성, 기술 스택, 규칙
2. **행동 제어**: 허용/금지 행동 정의
3. **품질 기준**: 코드 스타일, 테스트 요구사항
4. **도메인 지식**: 비즈니스 로직, 용어 정의

**CLAUDE.md 구성 요소**:
```markdown
# Project Name

## Overview
- 프로젝트 목적
- 기술 스택
- 주요 특성

## Rules
- 코딩 컨벤션
- 금지 사항
- 필수 요구사항

## Architecture
- 디렉토리 구조
- 핵심 패턴
- 의존성 규칙

## Domain
- 비즈니스 용어
- 핵심 개념
- 워크플로우
```

**탐구 질문**:
1. CLAUDE.md 없이 AI가 프로젝트를 이해할 수 있는가?
2. 어떤 정보가 가장 영향력이 큰가?
3. 너무 많은 규칙은 오히려 해가 되는가?

---

### Q2: 규칙 파일로 AI의 실수를 어떻게 방지하는가?

**AI Agents 핵심 개념**:

#### Accountability Framework
```
Ethical Audits → Behavioral Assessments → Logging & Traceability
```

| 구성요소 | 역할 |
|----------|------|
| **출력 평가** | Agent 행동이 목표/지침과 일치하는지 |
| **편향/공정성** | 출력의 편향 패턴 식별 |
| **결정 경로** | 권장/결정에 도달하는 방법 |
| **이해관계자 영향** | 다양한 그룹에 미치는 영향 |

**규칙 파일 유형**:

| 파일 | 역할 | 예시 |
|------|------|------|
| `CLAUDE.md` | 전체 컨텍스트 | 프로젝트 개요, 규칙 |
| `.claude/rules/*.md` | 세부 규칙 | 커밋 규칙, 테스트 규칙 |
| `.claude/skills/*.md` | 스킬 정의 | 자동화 워크플로우 |
| `.claude/agents/*.md` | 에이전트 정의 | 전문 에이전트 역할 |

**규칙 작성 원칙**:

```
1. 명확성: 모호함 없이 정확하게
2. 예시 포함: 좋은 예/나쁜 예 함께
3. 이유 설명: 왜 이 규칙이 필요한지
4. 검증 가능: 규칙 준수 확인 방법
```

**실패 방지 패턴**:

```markdown
## Git 규칙

### 금지 사항
- `git push --force` to main/master
- 시크릿 포함 커밋

### 필수 사항
- 커밋 전 빌드/테스트 통과
- 의미 있는 커밋 메시지

### 검증
- [ ] `git diff` 확인
- [ ] 민감 정보 없음
```

**탐구 질문**:
1. 어떤 규칙이 가장 자주 위반되는가?
2. 규칙 위반 시 AI는 어떻게 반응하는가?
3. 규칙 간 충돌은 어떻게 처리하는가?

---

### Q3: Progressive Delegation이란?

**AI Agents Ch13 핵심 개념**:

```
Trust Lifecycle:
Build → Calibrate → Maintain → Repair → Build ...
```

#### Human 역할의 진화

```
Executor → Reviewer → Collaborator → Governor
```

| 역할 | Human 책임 | Agent 자율성 |
|-----|-----------|-------------|
| **Executor** | 모든 출력 검토 | 최소 |
| **Reviewer** | 예외만 검토 | 중간 |
| **Collaborator** | 우선순위 가이드 | 높음 |
| **Governor** | 정책 설정, 감사 | 거버넌스 규칙 내 자율 |

#### Progressive Delegation 패턴

| 단계 | Agent 행동 | Human 역할 |
|-----|-----------|-----------|
| 초기 | 신중하게 행동, 검토 요청 | 모든 출력 검토 |
| 성장 | 신뢰성 입증에 따라 자율성 확대 | 예외만 검토 |
| 성숙 | 정의된 범위 내 자율 운영 | 정책 설정 및 감사 |

**Trust Signal**:
| 신호 유형 | 측정 방법 | 임계값 예시 |
|----------|----------|-----------|
| 정확도 | 출력 정확성 비율 | >95% |
| 일관성 | 동일 입력 동일 출력 | >90% |
| 투명성 | 설명 제공 빈도 | 모든 중요 결정 |
| 회복력 | 오류 후 복구 시간 | <1시간 |

**탐구 질문**:
1. 현재 나는 AI와 어떤 역할 관계인가?
2. 어떤 기준으로 더 많은 자율성을 부여할 것인가?
3. 신뢰 위반 시 어떻게 복구할 것인가?

---

## 실험 설계

### 실험 1: CLAUDE.md 영향 관찰

**목적**: CLAUDE.md 유무에 따른 AI 행동 차이 관찰

**설정**:
1. CLAUDE.md 없이 작업 요청
2. 간단한 CLAUDE.md 추가 후 동일 요청
3. 상세한 CLAUDE.md로 동일 요청

**프롬프트**:
```
create a user service with CRUD operations
```

**관찰 항목**:
- [ ] 사용된 기술 스택
- [ ] 코드 스타일
- [ ] 테스트 포함 여부
- [ ] 문서화 수준

**결과 기록**:
```
[실험 후 작성]
```

---

### 실험 2: 규칙 준수 관찰

**목적**: 규칙 파일이 AI 행동을 얼마나 제어하는지 관찰

**설정**:
1. 규칙 없이 커밋 요청
2. 커밋 규칙 추가 후 동일 요청

**규칙 파일**:
```markdown
# Git 커밋 규칙

## 커밋 메시지 형식
<type>: <subject>

## 타입
- feat: 새 기능
- fix: 버그 수정
- refactor: 리팩토링

## 필수 검증
- [ ] 빌드 통과
- [ ] 테스트 통과
```

**관찰 항목**:
- [ ] 커밋 메시지 형식 준수
- [ ] 검증 단계 수행 여부

**결과 기록**:
```
[실험 후 작성]
```

---

## CLAUDE.md 템플릿

### 기본 템플릿

```markdown
# Project Name

## Overview
프로젝트 설명...

## Tech Stack
- Language: TypeScript
- Framework: React/Node.js
- Database: PostgreSQL

## Code Style
- ESLint + Prettier 사용
- 함수형 컴포넌트 선호
- 명확한 타입 정의

## Project Structure
```
src/
├── components/
├── services/
├── hooks/
└── utils/
```

## Rules
- 모든 함수에 타입 정의 필수
- 테스트 커버리지 80% 이상
- 직접 DOM 조작 금지

## Commit Convention
- feat: 새 기능
- fix: 버그 수정
- refactor: 리팩토링
- docs: 문서
- test: 테스트
```

### 고급 템플릿

```markdown
# Enterprise Project

## Overview
...

## Architecture Decisions
- [ ] ADR-001: REST vs GraphQL → REST
- [ ] ADR-002: State Management → Zustand

## Domain Model
- User: 사용자 정보
- Order: 주문 정보
- Product: 상품 정보

## Security Rules
- 모든 입력 검증 필수
- SQL Injection 방지
- XSS 방지

## Performance Guidelines
- 이미지 lazy loading
- 코드 스플리팅
- API 응답 캐싱

## Testing Strategy
- Unit: Jest + Testing Library
- Integration: Cypress
- Coverage: 80%

## Deployment
- CI/CD: GitHub Actions
- Staging → Production
- Rollback 절차 정의
```

---

## 핵심 체크리스트

### CLAUDE.md 작성
- [ ] 프로젝트 개요 명확
- [ ] 기술 스택 정의
- [ ] 코드 스타일 규칙
- [ ] 프로젝트 구조 설명
- [ ] 금지/필수 사항

### 규칙 파일
- [ ] 명확하고 구체적
- [ ] 예시 포함
- [ ] 이유 설명
- [ ] 검증 방법

### Progressive Delegation
- [ ] 현재 역할 인식
- [ ] Trust Signal 정의
- [ ] 자율성 확대 기준
- [ ] 신뢰 회복 절차

---

## 다음 단계

- [ ] templates/ 폴더에 CLAUDE.md 템플릿 저장
- [ ] 규칙 파일 예시 작성
- [ ] 실험 결과 문서화

---

## 참고 자료

- AI Agents Chapter 13: Human-Agent Collaboration
- OMC 가이드: 3-Tier Memory System
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
