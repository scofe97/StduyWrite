# Document-Driven Development 개념 정리

## 핵심 한 줄 요약

> **CLAUDE.md와 규칙 파일은 AI의 "운영 매뉴얼"이다. 문서가 명확할수록 AI는 프로젝트에 맞게 동작하고, 실수를 줄이며, 신뢰할 수 있게 된다.**

---

## 1. Document-Driven Development란?

AI Agent의 행동을 **문서**로 제어하는 개발 방식입니다. 프롬프트만으로 지시하는 것이 아니라, 프로젝트 컨텍스트, 규칙, 패턴을 문서화하여 AI가 일관되고 예측 가능하게 동작하도록 합니다.

### 왜 필요한가?

| 프롬프트만 사용 | 문서 기반 접근 |
|----------------|---------------|
| 매번 컨텍스트 설명 필요 | 컨텍스트 자동 로드 |
| 일관성 없는 결과 | 일관된 스타일/패턴 |
| 규칙 위반 가능 | 규칙 자동 적용 |
| 반복적인 수정 | 처음부터 올바른 결과 |

---

## 2. 문서 계층 구조

### 파일 구조

```
project/
├── CLAUDE.md           # 프로젝트 전체 컨텍스트
├── .claude/
│   ├── rules/          # 세부 규칙
│   │   ├── git-workflow.md
│   │   ├── testing.md
│   │   └── security.md
│   ├── skills/         # 자동화 스킬
│   │   └── commit/
│   │       └── SKILL.md
│   └── agents/         # 전문 에이전트
│       └── reviewer.md
└── ~/.claude/
    └── CLAUDE.md       # 사용자 전역 설정
```

### 문서별 역할

| 문서 | 범위 | 역할 |
|------|------|------|
| `~/.claude/CLAUDE.md` | 전역 | 모든 프로젝트 공통 설정 |
| `CLAUDE.md` | 프로젝트 | 프로젝트 특화 컨텍스트 |
| `.claude/rules/*.md` | 도메인별 | 세부 규칙 (커밋, 테스트 등) |
| `.claude/skills/*.md` | 작업별 | 자동화 워크플로우 |

---

## 3. CLAUDE.md 작성법

### 필수 섹션

```markdown
# Project Name

## Overview
프로젝트 목적과 핵심 기능 설명

## Tech Stack
사용하는 기술 스택 목록

## Project Structure
디렉토리 구조와 각 역할

## Code Style
코딩 컨벤션과 스타일 규칙

## Rules
반드시 지켜야 할 규칙과 금지 사항

## Domain
비즈니스 용어와 도메인 지식
```

### 효과적인 규칙 작성

```markdown
## Rules

### 필수 (MUST)
- 모든 함수에 타입 정의
- 테스트 커버리지 80% 이상
- 커밋 전 린트 통과

### 금지 (MUST NOT)
- 직접 DOM 조작
- any 타입 사용
- console.log 남기기

### 권장 (SHOULD)
- 함수형 컴포넌트 선호
- 작은 함수로 분리
- 명확한 변수명
```

### 예시 포함하기

```markdown
## Commit Convention

### 형식
<type>: <subject>

### 예시
✅ 좋은 예:
- feat: 사용자 인증 기능 추가
- fix: 로그인 페이지 버그 수정

❌ 나쁜 예:
- update
- fix bug
- 수정
```

---

## 4. Progressive Delegation

### Human 역할의 진화

```
Executor → Reviewer → Collaborator → Governor
(실행자)   (검토자)   (협력자)      (통치자)
```

| 역할 | Human 책임 | Agent 자율성 |
|-----|-----------|-------------|
| **Executor** | 모든 출력 검토 | 최소 (감독 하) |
| **Reviewer** | 예외만 검토 | 중간 (루틴 처리) |
| **Collaborator** | 우선순위 가이드 | 높음 (초안/실행) |
| **Governor** | 정책 설정, 감사 | 거버넌스 규칙 내 자율 |

### Trust Lifecycle

```
Build (구축) → Calibrate (보정) → Maintain (유지) → Repair (복구)
     ↑                                                    ↓
     └────────────────────────────────────────────────────┘
```

### Trust Signal

| 신호 | 측정 방법 | 임계값 |
|------|----------|--------|
| **정확도** | 출력 정확성 | >95% |
| **일관성** | 동일 입력 동일 출력 | >90% |
| **투명성** | 설명 제공 | 중요 결정마다 |
| **회복력** | 오류 복구 시간 | <1시간 |
| **수용률** | 제안 수락률 | >70% |

### Progressive Delegation 적용

```
단계 1: 신중한 시작
- Agent: 모든 중요 결정에 확인 요청
- Human: 모든 출력 검토

단계 2: 신뢰 구축
- Agent: 루틴 작업 자율 처리
- Human: 예외 케이스만 검토

단계 3: 자율 운영
- Agent: 정의된 범위 내 자율 실행
- Human: 정책 설정 및 감사
```

---

## 5. OMC와 Document-Driven

### OMC의 3-Tier Memory System

| 계층 | 역할 | 지속성 |
|------|------|--------|
| **Short-term** | 현재 세션 컨텍스트 | 세션 내 |
| **Mid-term** | 작업 관련 정보 | 작업 완료까지 |
| **Long-term** | 프로젝트 지식 | 영구 |

### CLAUDE.md와 OMC 통합

```markdown
# Project CLAUDE.md

## OMC Settings

### Default Mode
autopilot: 기본 자율 실행 모드

### Agent Preferences
- architect: 시스템 설계 담당
- QA-tester: 테스트 담당

### Memory Rules
- 모든 아키텍처 결정 Long-term 저장
- API 변경사항 팀과 공유
```

---

## 6. Accountability Framework

### 구성요소

```
Ethical Audits → Behavioral Assessments → Logging → Third-party Audits
```

### 로깅 시스템

| 로그 유형 | 내용 |
|----------|------|
| **결정 로그** | 특정 결정 이유 (입력, 추론, 출력) |
| **상호작용 로그** | 입력/응답 + 타임스탬프 |
| **오류 로그** | 실패 시점과 이유 |

### 추적 가능성

- **Explainability**: 왜 이 결정을 했는가?
- **Traceability**: 어디서 비롯된 결정인가?
- **Reversibility**: 되돌릴 수 있는가?
- **Monitorable**: 모니터링 가능한가?

---

## 7. 실무 적용 체크리스트

### CLAUDE.md 작성

```
□ 프로젝트 개요 명확
□ 기술 스택 정의
□ 디렉토리 구조 설명
□ 코드 스타일 규칙
□ 필수/금지 사항
□ 도메인 지식
□ 좋은 예/나쁜 예 포함
```

### 규칙 파일 작성

```
□ 각 도메인별 분리 (git, test, security)
□ 명확하고 구체적
□ 예시 포함
□ 이유 설명
□ 검증 방법 정의
```

### Progressive Delegation

```
□ 현재 역할 인식 (Executor/Reviewer/Collaborator/Governor)
□ Trust Signal 정의
□ 자율성 확대 기준 설정
□ 신뢰 위반 시 복구 절차
□ 정기적인 신뢰 평가
```

---

## 8. 템플릿

### 기본 CLAUDE.md

```markdown
# Project Name

## Overview
[프로젝트 한 줄 설명]

## Tech Stack
- Language: [언어]
- Framework: [프레임워크]
- Database: [데이터베이스]

## Structure
[주요 디렉토리 설명]

## Rules
### MUST
- [필수 규칙 1]
- [필수 규칙 2]

### MUST NOT
- [금지 사항 1]
- [금지 사항 2]

## Commit Convention
[커밋 메시지 규칙]
```

### 규칙 파일 템플릿

```markdown
# [도메인] 규칙

## 목적
[이 규칙의 목적]

## 규칙

### 필수
- [규칙 1]
- [규칙 2]

### 금지
- [금지 사항 1]
- [금지 사항 2]

## 예시

### 좋은 예
[좋은 예시]

### 나쁜 예
[나쁜 예시]

## 검증
- [ ] [검증 항목 1]
- [ ] [검증 항목 2]
```

---

## 핵심 원칙 요약

1. **명확한 문서화**: 모호함 없이 정확하게
2. **예시 포함**: 좋은 예/나쁜 예 함께
3. **이유 설명**: 왜 이 규칙이 필요한지
4. **검증 가능**: 규칙 준수 확인 방법
5. **점진적 위임**: 신뢰 구축에 따라 자율성 확대
6. **지속적 개선**: 피드백 반영하여 문서 업데이트
