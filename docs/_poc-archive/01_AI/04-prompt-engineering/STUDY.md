# Prompt Engineering 소크라테스 학습

## 학습 목표
- OMC 매직 키워드의 효과적인 사용법 이해
- 프롬프트 조합 패턴 학습
- 성공/실패 프롬프트 패턴 분석

---

## 소크라테스 질문

### Q1: 왜 어떤 프롬프트는 잘 작동하고 어떤 건 실패하는가?

**탐구 시작**: 같은 작업인데 왜 결과가 다른가?

**나의 생각 기록**:
```
[여기에 자신의 생각 작성]
```

**실험 비교**:

| 프롬프트 | 예상 결과 | 실제 결과 | 분석 |
|----------|----------|----------|------|
| "build a todo app" | ? | | |
| "autopilot: build a todo app" | ? | | |
| "ralph ulw: build a todo app with tests" | ? | | |

**가설**:
1. 키워드가 AI의 "모드"를 활성화한다
2. 더 구체적인 요구사항이 더 나은 결과를 낳는다
3. 키워드 조합이 기능을 레이어링한다

**탐구 질문**:
1. 키워드 없이도 AI가 복잡한 작업을 수행하는가?
2. 어떤 키워드 조합이 가장 효과적인가?
3. 프롬프트 길이와 품질의 관계는?

---

### Q2: 키워드 조합(`ralph ulw`)의 효과는?

**OMC 키워드 체계**:

```
[실행 스킬] + [향상 스킬] + [보장 옵션]

예시:
ralph ulw: migrate database
└─────┘└──┘  └────────────┘
지속성  병렬     작업 내용
```

**키워드 카테고리**:

#### 실행 스킬
| 키워드 | 기능 | 효과 |
|--------|------|------|
| `autopilot` / `ap` | 자율 실행 | 완전 자동화 |
| `swarm` | 에이전트 협력 | N개 병렬 처리 |
| `pipeline` | 순차 체이닝 | A→B→C 흐름 |
| `plan` | 계획 인터뷰 | 요구사항 명확화 |

#### 향상 스킬
| 키워드 | 기능 | 효과 |
|--------|------|------|
| `ulw` | 병렬 실행 | 3-5배 속도 |
| `eco` | 토큰 효율 | 30-50% 비용 절감 |

#### 보장 옵션
| 키워드 | 기능 | 효과 |
|--------|------|------|
| `ralph` | 완료까지 지속 | 실패 복구 |
| `ralplan` | 반복적 계획 | 계획 개선 |

**조합 패턴 예시**:

| 조합 | 효과 |
|------|------|
| `ralph autopilot` | 자율 실행 + 완료 보장 |
| `ralph ulw` | 병렬 처리 + 완료 보장 |
| `eco swarm` | 비용 효율 + 분산 처리 |
| `plan pipeline` | 계획 후 순차 실행 |

**탐구 질문**:
1. 어떤 조합이 상충하는가?
2. 조합 순서가 중요한가?
3. 모든 조합이 가능한가?

---

### Q3: 복잡한 작업을 어떻게 분해해서 전달하는가?

**작업 분해 패턴**:

#### 패턴 1: 명시적 단계
```
autopilot:
1. Create project structure
2. Implement REST API
3. Add authentication
4. Write tests
5. Document API
```

#### 패턴 2: Pipeline 사용
```
pipeline: architect -> developer -> tester -> documenter
```

#### 패턴 3: Plan 인터뷰
```
plan: build an e-commerce platform

# AI가 질문하며 요구사항 명확화
- 결제 시스템은?
- 상품 카테고리는?
- 사용자 인증 방식은?
```

#### 패턴 4: Swarm 분산
```
swarm:
- Agent 1: Frontend
- Agent 2: Backend
- Agent 3: Database
- Agent 4: Tests
```

**효과적인 분해 원칙**:
1. **원자성**: 각 단계가 독립적으로 완료 가능
2. **순서성**: 의존성 관계 명시
3. **검증성**: 각 단계 완료 기준 명확

---

## 프롬프트 비교 실험

### 실험 1: 키워드 유무 비교

**설정**:
```
# 버전 1: 기본
build a REST API

# 버전 2: autopilot
autopilot: build a REST API

# 버전 3: 상세
autopilot: build a REST API with:
- Express.js
- CRUD operations for users
- JWT authentication
- Swagger documentation
```

**관찰 항목**:
- [ ] 생성된 파일 수
- [ ] 코드 품질
- [ ] 문서화 수준
- [ ] 테스트 포함 여부

**결과 기록**:
```
버전 1:
- 파일 수:
- 품질:
- 문서화:
- 테스트:

버전 2:
...

버전 3:
...
```

---

### 실험 2: 키워드 조합 효과

**설정**:
```
# 조합 1: autopilot만
autopilot: fix all lint errors

# 조합 2: ulw만
ulw: fix all lint errors

# 조합 3: ralph + ulw
ralph ulw: fix all lint errors

# 조합 4: eco + ulw
eco ulw: fix all lint errors
```

**측정 항목**:
- [ ] 완료 시간
- [ ] 토큰 사용량
- [ ] 수정된 파일 수
- [ ] 잔여 오류 수

**결과 기록**:
```
[실험 후 작성]
```

---

### 실험 3: 작업 분해 방식 비교

**설정**:
```
# 방식 1: 한 번에 요청
autopilot: build a todo app with React frontend, Node backend, MongoDB

# 방식 2: Pipeline
pipeline: architect -> frontend-dev -> backend-dev -> tester

# 방식 3: 명시적 단계
autopilot:
1. Design architecture
2. Create React frontend
3. Create Node backend
4. Connect to MongoDB
5. Add tests
```

**관찰 항목**:
- [ ] 아키텍처 일관성
- [ ] 컴포넌트 통합 품질
- [ ] 전체 완료 시간

**결과 기록**:
```
[실험 후 작성]
```

---

## 프롬프트 패턴 컬렉션

### 성공 패턴

#### 1. 명확한 범위 + autopilot
```
autopilot: create a user authentication system with:
- Email/password login
- JWT tokens
- Password reset via email
- Rate limiting
```

#### 2. 병렬 처리 + 완료 보장
```
ralph ulw: refactor all service classes to use dependency injection
```

#### 3. 순차 체이닝
```
pipeline: code-review -> implement-fixes -> run-tests -> update-docs
```

#### 4. 분산 처리
```
swarm: process all markdown files in docs/ folder
- Agent 1: Grammar check
- Agent 2: Format standardization
- Agent 3: Link validation
```

### 실패 패턴

#### 1. 모호한 요청
```
# 나쁨
make it better

# 좋음
autopilot: improve performance by:
- Adding caching layer
- Optimizing database queries
- Implementing lazy loading
```

#### 2. 과도한 범위
```
# 나쁨
build a complete e-commerce platform

# 좋음
autopilot: create the product catalog module with:
- CRUD operations
- Category hierarchy
- Search functionality
```

#### 3. 충돌하는 키워드
```
# 주의 필요
eco ulw: complex multi-agent task
# eco는 비용 절감, ulw는 병렬 처리 → 리소스 충돌 가능
```

---

## 핵심 체크리스트

### 키워드 이해
- [ ] 실행 스킬: autopilot, swarm, pipeline, plan
- [ ] 향상 스킬: ulw, eco
- [ ] 보장 옵션: ralph, ralplan

### 조합 패턴
- [ ] 기본 조합: ralph + 실행스킬
- [ ] 성능 조합: ulw + 실행스킬
- [ ] 효율 조합: eco + 실행스킬

### 작업 분해
- [ ] 명시적 단계 나열
- [ ] Pipeline 사용
- [ ] Swarm 분산
- [ ] Plan 인터뷰

---

## 다음 단계

- [ ] SUMMARY.md 작성 (패턴 정리)
- [ ] experiments/ 폴더에 실험 결과 저장
- [ ] 효과적인 프롬프트 템플릿 수집

---

## 참고 자료

- OMC 가이드: 매직 키워드 섹션
- OMC GitHub: 예시 프롬프트
- [ROBOCO OMC 분석글](https://roboco.io/posts/oh-my-claudecode-distilled/)
