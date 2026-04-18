# OMC 자동화 모드 가이드

## 개요

oh-my-claudecode는 복잡한 작업을 자동으로 처리하는 여러 모드를 제공합니다. 명시적인 명령어 없이 자연어로 활성화할 수 있습니다.

## 자동 활성화 (권장)

OMC는 특별한 명령어 없이 자연어로 동작합니다:

| 말하면 | 동작 |
|--------|------|
| "완료될 때까지 멈추지 마" | 지속 실행 모드 |
| "plan this" / "계획해줘" | 계획 수립 인터뷰 |
| "fast" / "parallel" | 병렬 처리 모드 |
| "stop" / "cancel" | 현재 작업 중단 |

---

## 모드 상세 가이드

### 1. Ralph - 지속 실행 모드

**"자기 참조적 개발 루프"** - 작업이 완전히 검증될 때까지 반복 실행

```
ralph: 인증 버그 수정해줘
```

#### 핵심 흐름

```
1. .ralph/PROMPT.md에서 요구사항 읽기
2. 현재 컨텍스트로 Claude Code 실행
3. 작업 목록(task list)으로 진행 추적
4. 완료 신호 평가
5. 조건 만족까지 반복
```

#### 종료 조건 (이중 조건 게이트)

Ralph는 두 조건이 **모두** 충족되어야 종료됩니다:

```
종료 = (완료 신호 ≥ 2) AND (EXIT_SIGNAL: true)
```

- **완료 신호**: 자연어 패턴에서 "작업 완료" 의도 감지
- **EXIT_SIGNAL**: Claude가 명시적으로 `EXIT_SIGNAL: true` 응답

#### 안전 메커니즘 (Circuit Breaker)

| 조건 | 설명 |
|------|------|
| 3회 연속 무진전 | 동일 오류 3번 연속 발생 시 중단 |
| 5회 반복 동일 오류 | 같은 에러 5번 이상 시 중단 |
| 진행도 없음 | 루프에서 진전 미감지 시 중단 |
| API 한도 초과 | 5시간 사용량 제한 도달 시 60분 대기 안내 |

#### 검증 체크리스트

```
□ BUILD: 빌드 성공
□ TEST: 테스트 통과
□ LINT: 린트 통과
□ FUNCTIONALITY: 기능 동작 확인
□ ARCHITECT REVIEW: 아키텍처 검증
□ TODO 완료: 모든 할일 항목 완료
□ ERROR_FREE: 에러 없음 상태
```

> **중요**: 증거는 5분 이내의 최신 데이터여야 하며, 실제 명령어 출력이 포함되어야 합니다.

#### 설정 파일 구조

```
.ralph/
├── PROMPT.md      # 프로젝트 목표 및 요구사항
├── fix_plan.md    # 작업 우선순위 계획
├── AGENT.md       # 빌드 명령어 (자동 유지보수)
└── .ralphrc       # Ralph 설정 파일
```

#### 사용 시나리오

- 복잡한 버그 수정
- 여러 파일에 걸친 리팩토링
- 테스트 통과까지 반복 작업

---

### 2. Ultrawork (ulw) - 최대 병렬화

**"최대 병렬 성능 모드"** - 파일 소유권 분할로 충돌 없는 병렬 작업

```
ulw API 전체 리팩토링해줘
```

#### 파일 소유권 분할 방식

```
원리:
1. 작업을 원자적(atomic) 단위로 분할
2. 각 에이전트에 배타적 파일 소유권 할당
3. 에이전트는 할당받은 파일만 수정 가능
4. 공유 영역은 원자적 커밋으로 보호
```

#### 에이전트 관리

- **병렬 워커**: 최대 **5개** 동시 에이전트
- 각 에이전트는 공유 작업 풀(Task Pool)에서 **원자적으로** 작업 청구

```
Agent_1: Task_Pool에서 Task_A 청구 (원자적)
Agent_2: Task_Pool에서 Task_B 청구 (원자적)
Agent_3: Task_Pool에서 Task_C 청구 (원자적)
→ 중복 청구 불가능 (원자성 보장)
```

#### 충돌 방지 메커니즘

| 메커니즘 | 설명 |
|---------|------|
| 원자적 작업 청구 | 한 번에 한 에이전트만 작업 클레임 가능 |
| 5분 타임아웃 | 작업 미완료 시 자동으로 풀에 반환 |
| 배타적 파일 소유권 | 각 에이전트는 할당받은 파일만 접근 |
| 원자적 커밋 | 변경사항은 자동으로 원자적 커밋 생성 |

#### 예시 시나리오

```
상황: 5개 에이전트, 작업 10개

Agent_A: backend/api.ts 소유 + 3개 작업 처리
Agent_B: frontend/component.tsx 소유 + 3개 작업 처리
Agent_C: database/schema.sql 소유 + 2개 작업 처리
Agent_D: config/ 소유 + 2개 작업 처리

결과: 동시 병렬 처리로 3-5배 가속
```

#### 사용 시나리오

- 대규모 코드베이스 수정
- 여러 컴포넌트 동시 작업
- 시간이 오래 걸리는 작업

---

### 3. Plan - 계획 수립 인터뷰

**"실행 전 연구 단계"** - 5단계 인터뷰 워크플로우

```
plan 새로운 결제 시스템
```

#### 인터뷰 워크플로우

```
Step 1: 초기 요청
사용자: "REST API 빌드해줘"

Step 2: 요구사항 명확화 (Claude 인터뷰)
- API 엔드포인트 구조는?
- 인증 방식은?
- 데이터베이스는?
- 에러 처리 전략은?
- 성능 요구사항은?

Step 3: 사용자 응답 수집

Step 4: 계획 문서 생성 (plan.md)

Step 5: 승인 → 실행 (Sonnet 4.5)
```

#### 도구 제한사항

| 사용 가능 | 제한됨 |
|-----------|--------|
| Read, LS, Glob, Grep | Edit, Write |
| Task, TodoRead/TodoWrite | Bash |
| WebFetch, WebSearch | NotebookEdit |
| NotebookRead | 상태 변경 MCP |

#### 토큰 효율성

- **76% 토큰 감소** (Opus 대비)
- Plan 단계: Opus 4.5
- 실행 단계: Sonnet 4.5 (저비용)

#### 사용 시나리오

- 새 기능 설계
- 아키텍처 결정
- 복잡한 변경 전 검토

---

### 4. Ralplan - 반복적 계획 수립

**"3명의 전문가가 협력하는 계획 검증 루프"**

```
ralplan 마이크로서비스 분리
```

#### 역할 분담 (모두 Opus 모델)

| 역할 | 책임 | 입출력 |
|------|------|--------|
| **Planner** | 전략적 계획 + 인터뷰 | 요구사항 → 초안 계획 |
| **Architect** | 아키텍처 + 디버깅 + 근본 원인 분석 | 계획 → 설계 검증 |
| **Critic** | 비판적 검토 | 계획 → 실현 가능성 평가 |

#### 상호작용 흐름

```
Planner ──→ 초안 계획 생성
    ↓
Architect ──→ 아키텍처 검증 + 기술적 검토
    ↓
Critic ──→ 비판적 평가 + 개선 제안
    ↓
합의 도달?
├─ NO ──→ Planner로 돌아가 개선
└─ YES ──→ 실행 단계 진행
```

#### 합의 도달 조건

```
합의 = Architect 검증 + Critic 승인 + Planner 확인

탈출 조건:
- 3명 모두가 계획에 동의
- 기술적 실현 가능성 확인
- 위험 요소 모두 식별 및 완화 계획 수립
- 최대 반복: 3-5회 (복잡도에 따라)
```

#### 사용 시나리오

- 중요한 아키텍처 결정
- 리스크가 큰 변경
- 팀 리뷰가 필요한 설계

---

### 5. Ultrapilot - 병렬 Autopilot

**"Autopilot의 병렬 처리 버전"** - 3-5배 속도 향상

```
ultrapilot: React 앱 구축
```

#### Autopilot vs Ultrapilot

| 측면 | Autopilot | Ultrapilot |
|------|-----------|-----------|
| 실행 방식 | 순차 처리 | 3-5배 병렬 처리 |
| 동시 워커 | 1개 | 최대 5개 |
| 사용 케이스 | 단순 작업 | 대규모 멀티 컴포넌트 |
| 속도 | 기준선 | 3-5배 빠름 |
| 메모리 | 낮음 | 중간~높음 |

#### 파일 파티셔닝 예시

```
프로젝트 구조:
src/
├── components/     → Agent_B 소유
├── styles/         → Agent_C 소유
├── tests/          → Agent_D 소유
├── config/         → Agent_E 소유
└── utils/          → 공유 (원자적 커밋으로 보호)
```

---

### 6. 추가 모드

#### Swarm - 좌표 제어 병렬 실행

```
N개 조정된 에이전트 + 공유 작업 풀

특징:
- 작업 풀에서 원자적으로 작업 청구
- 완료하면 마크
- 5분 타임아웃으로 미완료 작업 반환

예: 100개 파일 리팩토링
→ 5개 에이전트가 20개씩 분산 처리
→ 타임아웃으로 병목 작업 재할당
```

#### Ecomode - 토큰 효율성

```
비용 최적화 조합:
- Haiku: 빠른 작업, 간단한 로직
- Sonnet: 중간 복잡도 구현
- Opus: 아키텍처 결정만

결과: 30-50% 비용 절감
```

---

## 모드 비교 요약

| 모드 | 병렬화 | 지속성 | 계획 | 속도 | 비용 | 사용 사례 |
|------|--------|--------|------|------|------|-----------|
| autopilot | X | X | X | 1x | 중간 | 기본/단순 작업 |
| ralph | O (자동) | O | X | ~1x | 중간 | 복잡한 버그 수정 |
| ultrawork | O | X | X | 3-5x | 높음 | 대규모 리팩토링 |
| ultrapilot | O | X | X | 3-5x | 높음 | 대규모 멀티 컴포넌트 |
| plan | X | X | O | 느림 | 낮음 | 새 기능 설계 |
| ralplan | X | O | O | 느림 | 높음 | 아키텍처 결정 |
| swarm | O | X | X | 3-5x | 중간 | 많은 작업 분산 |
| ecomode | O | X | X | 2-3x | 낮음 | 비용 최적화 |

---

## 실전 예시

### 예시 1: 버그 수정 (Ralph)
```
ralph: 로그인 시 세션이 유지되지 않는 버그 수정해줘.
테스트도 추가하고 모든 테스트가 통과할 때까지 계속해.
```

### 예시 2: 대규모 리팩토링 (Ultrawork)
```
ulw 모든 API 엔드포인트에 에러 핸들링 추가해줘.
각 컨트롤러별로 병렬로 처리해.
```

### 예시 3: 신기능 계획 (Plan)
```
plan 사용자 알림 시스템 추가하고 싶어.
이메일, 푸시, 인앱 알림 모두 지원해야 해.
```

### 예시 4: 아키텍처 결정 (Ralplan)
```
ralplan 모놀리스를 마이크로서비스로 분리하고 싶어.
사용자, 주문, 결제 도메인으로 나누려고 해.
```

### 예시 5: 대규모 앱 구축 (Ultrapilot)
```
ultrapilot: 풀스택 e-commerce 앱 구축해줘.
React 프론트엔드, Node.js 백엔드, PostgreSQL 사용.
```

---

## 모드 선택 의사결정 트리

```
프로젝트 규모?
├─ 작음 (< 2시간) → Autopilot
├─ 중간 (2-8시간) → Plan + Autopilot
├─ 큼 (> 8시간) → Ultrapilot + Ralph
└─ 매우 복잡 → Ralplan + Ralph + Ultrapilot

비용 민감?
├─ YES → Ecomode
└─ NO → Ultrawork/Ultrapilot
```

---

## Best Practices

### Ralph 모드

**DO:**
- 명확한 요구사항을 `.ralph/PROMPT.md`에 작성
- 최대 반복을 합리적으로 설정 (보통 10-30회)
- 검증 체크리스트를 구체적으로 정의
- 진행 상황을 HUD에서 주기적으로 모니터링

**DON'T:**
- 모호한 목표로 시작
- 무한 루프 방지 장치 없이 실행
- 실패 조건 정의 없이 운영
- 프로덕션 환경에 무분별 사용

### 병렬 모드 (Ultrawork/Ultrapilot)

**파일 구조 설계:**
```
✅ Good - 병렬화 용이:
src/
├── modules/user/      → Agent_A
├── modules/product/   → Agent_B
├── modules/order/     → Agent_C
└── shared/utils.ts    → 원자적 커밋

❌ Bad - 병렬화 어려움:
src/
├── index.ts           (모든 에이전트가 필요)
├── shared/            (높은 의존도)
└── legacy/            (강한 결합)
```

**작업 분해 전략:**
- 의존도 최소화
- 각 작업을 2-4시간 범위로 조정
- 공유 인터페이스 미리 정의
- 병합 전략 사전 계획

### 토큰 효율성 최적화

| 상황 | 추천 조합 | 효과 |
|------|-----------|------|
| 단순 구현 | Ecomode + Autopilot | 토큰 30-50% 절감 |
| 복잡한 설계 | Plan + Ralplan | 사전 검증으로 재작업 감소 |
| 대규모 병렬 | Ultrapilot + Ecomode | 속도 + 비용 동시 최적화 |
| 장기 작업 | Ralph + Ultrawork | 지속성 + 병렬 처리 |

---

## 중단 방법

작업 중 언제든 중단할 수 있습니다:

- **키보드**: `Ctrl+C`
- **자연어**: "stop", "cancel", "멈춰"
- **명령어**: `/oh-my-claudecode:cancel`

---

## 주의사항

1. **ralph 사용 시**: 컨텍스트 사용량 모니터링 필요 (HUD에서 확인)
2. **ultrawork 사용 시**: 파일 충돌 가능성 있는 작업은 피하기
3. **ralplan 사용 시**: 시간이 오래 걸릴 수 있음
4. **ultrapilot 사용 시**: 메모리 사용량 높음

---

## 아키텍처 개요

### 3단계 Skill 조합 시스템

oh-my-claudecode는 **행동 주입(behavior injection)** 아키텍처를 사용합니다:

```
기본 공식: [Execution Skill] + [0-N Enhancement] + [Optional Guarantee]

예시:
default + ultrawork + ralph
= 기본 실행 + 병렬 처리 + 지속 검증
```

### 에이전트 복잡도 티어링

| Tier | 모델 | 용도 |
|------|------|------|
| LOW | Haiku | 빠른 조회, 단순 작업 |
| MEDIUM | Sonnet | 표준 구현, 중간 복잡도 |
| HIGH | Opus | 복잡한 추론, 아키텍처 결정 |

### 상태 저장

```
.omc/state/{name}.json
```

---

## 관련 문서

- [44_oh-my-claudecode_설치_및_개요.md](./44_oh-my-claudecode_설치_및_개요.md)
- [46_OMC_HUD_상태표시줄_가이드.md](./46_OMC_HUD_상태표시줄_가이드.md)

---

## 참고 자료

- [oh-my-claudecode GitHub](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [oh-my-claudecode 공식 사이트](https://ohmyclaudecode.com/)
- [Ralph Claude Code](https://github.com/frankbria/ralph-claude-code)
