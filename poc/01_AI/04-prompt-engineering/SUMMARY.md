# Prompt Engineering 개념 정리

## 핵심 한 줄 요약

> **OMC에서 프롬프트는 "키워드 + 작업 + 세부사항"의 조합이다. 키워드는 AI의 동작 모드를 활성화하고, 세부사항은 품질을 결정한다.**

---

## 1. OMC 키워드 체계

### 키워드 구조

```
[실행 스킬] + [향상 스킬] + [보장 옵션]: 작업 내용

예시:
ralph ulw: migrate database
└─────┘└──┘  └────────────┘
보장   향상     작업 내용
```

### 키워드 카테고리

#### 실행 스킬 (무엇을 할 것인가)
| 키워드 | 동작 | 사용 시나리오 |
|--------|------|--------------|
| `autopilot` / `ap` | 완전 자율 실행 | 복잡한 작업 자동화 |
| `swarm` | N개 에이전트 협력 | 대규모 병렬 처리 |
| `pipeline` | 순차 체이닝 | 단계별 워크플로우 |
| `plan` | 계획 인터뷰 | 요구사항 명확화 |

#### 향상 스킬 (어떻게 더 잘할 것인가)
| 키워드 | 동작 | 효과 |
|--------|------|------|
| `ulw` (Ultrawork) | 병렬 실행 | 3-5배 속도 향상 |
| `eco` (Ecomode) | 토큰 효율 | 30-50% 비용 절감 |

#### 보장 옵션 (어떻게 완료를 보장할 것인가)
| 키워드 | 동작 | 효과 |
|--------|------|------|
| `ralph` | 완료까지 지속 | 실패 시 재시도 |
| `ralplan` | 반복적 계획 | 계획 품질 개선 |

---

## 2. 효과적인 키워드 조합

### 추천 조합

| 조합 | 효과 | 사용 사례 |
|------|------|----------|
| `ralph autopilot` | 자율 + 완료 보장 | 복잡한 기능 구현 |
| `ralph ulw` | 병렬 + 완료 보장 | 다수 파일 수정 |
| `eco swarm` | 효율 + 분산 | 대규모 처리, 비용 민감 |
| `plan pipeline` | 계획 + 순차 | 명확한 단계별 작업 |

### 조합 시 주의사항

```
✅ 호환 가능:
- ralph + 모든 실행 스킬
- ulw + autopilot/swarm
- eco + swarm

⚠️ 주의 필요:
- eco + ulw: 리소스 충돌 가능
- swarm + pipeline: 동시 사용 권장 안함
```

---

## 3. 프롬프트 작성 원칙

### 좋은 프롬프트의 특징

| 원칙 | 설명 | 예시 |
|------|------|------|
| **명확성** | 모호함 없는 요청 | "REST API" vs "API" |
| **범위 한정** | 과도하지 않은 범위 | 하나의 모듈 vs 전체 시스템 |
| **구체성** | 세부 요구사항 포함 | 기술 스택, 제약사항 명시 |
| **검증 가능** | 완료 기준 명확 | 테스트 통과, 빌드 성공 |

### 프롬프트 템플릿

```
autopilot: [작업 설명] with:
- [요구사항 1]
- [요구사항 2]
- [제약사항]
- [완료 기준]
```

---

## 4. 작업 분해 패턴

### 패턴 1: 명시적 단계

```
autopilot:
1. Create project structure
2. Implement core logic
3. Add tests
4. Document API
```

**장점**: 명확한 순서, 진행 상황 추적 용이
**단점**: 유연성 부족

### 패턴 2: Pipeline 사용

```
pipeline: architect -> developer -> tester -> documenter
```

**장점**: 역할 분리, 전문화
**단점**: 순차 처리로 시간 소요

### 패턴 3: Plan 인터뷰

```
plan: build an e-commerce platform
```

**장점**: 요구사항 발굴, 누락 방지
**단점**: 인터랙션 필요

### 패턴 4: Swarm 분산

```
swarm:
- Agent 1: Frontend
- Agent 2: Backend
- Agent 3: Tests
```

**장점**: 병렬 처리, 속도
**단점**: 통합 복잡성

---

## 5. 성공/실패 패턴 분석

### 성공 패턴

#### 1. 명확한 범위 + 키워드
```
autopilot: create user authentication with:
- Email/password login
- JWT tokens
- Password reset
```

#### 2. 병렬 + 완료 보장
```
ralph ulw: refactor all services to use DI
```

#### 3. 순차 체이닝
```
pipeline: review -> implement -> test -> document
```

### 실패 패턴

#### 1. 모호한 요청
```
❌ make it better
✅ improve performance by adding caching
```

#### 2. 과도한 범위
```
❌ build complete e-commerce platform
✅ create product catalog module
```

#### 3. 세부사항 부재
```
❌ create API
✅ create REST API with Express.js, CRUD for users, JWT auth
```

---

## 6. 프롬프트 예시 컬렉션

### 개발 작업

```bash
# 새 기능 개발
autopilot: create a user notification system with:
- Email notifications
- Push notifications
- Notification preferences
- Notification history

# 리팩토링
ralph ulw: refactor all controllers to use async/await

# 버그 수정
autopilot: fix memory leak in WebSocket connections

# 테스트 추가
ralph ulw: add unit tests for all service classes
```

### 코드 품질

```bash
# 린트 수정
ulw: fix all ESLint errors in src/

# 타입 추가
ralph ulw: add TypeScript types to all API responses

# 문서화
swarm: document all public APIs with JSDoc
```

### 프로젝트 설정

```bash
# 프로젝트 초기화
autopilot: create a new React project with:
- TypeScript
- TailwindCSS
- React Query
- React Router

# CI/CD 설정
autopilot: set up GitHub Actions for:
- Lint on PR
- Test on push
- Deploy on main merge
```

---

## 7. 핵심 체크리스트

### 프롬프트 작성 전
- [ ] 작업 범위 명확화
- [ ] 적절한 키워드 선택
- [ ] 세부 요구사항 정리
- [ ] 완료 기준 정의

### 키워드 선택
- [ ] 자율 실행 필요? → autopilot
- [ ] 병렬 처리 가능? → ulw
- [ ] 순차 단계 필요? → pipeline
- [ ] 분산 처리 필요? → swarm
- [ ] 비용 민감? → eco
- [ ] 완료 보장 필요? → ralph

### 작업 분해
- [ ] 독립적으로 완료 가능한 단계
- [ ] 명확한 순서/의존성
- [ ] 각 단계의 검증 기준

---

## 8. 빠른 참조표

### 상황별 추천 프롬프트

| 상황 | 프롬프트 패턴 |
|------|-------------|
| 새 기능 개발 | `autopilot: create [기능] with: [요구사항]` |
| 대규모 리팩토링 | `ralph ulw: refactor [대상] to [목표]` |
| 버그 수정 | `autopilot: fix [버그 설명]` |
| 테스트 추가 | `ralph ulw: add tests for [대상]` |
| 문서화 | `swarm: document [대상]` |
| 코드 정리 | `ulw: fix all [문제] in [범위]` |
| 요구사항 불명확 | `plan: [프로젝트 설명]` |

### 키워드 조합 빠른 선택

| 우선순위 | 조합 |
|----------|------|
| 속도 | `ulw` |
| 완료 보장 | `ralph` |
| 속도 + 완료 | `ralph ulw` |
| 비용 절감 | `eco` |
| 복잡한 작업 | `autopilot` |
| 대규모 병렬 | `swarm` |
