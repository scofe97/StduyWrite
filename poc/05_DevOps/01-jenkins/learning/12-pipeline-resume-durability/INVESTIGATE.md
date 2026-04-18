# Ch12. Pipeline Resume과 Durability — 점검 질문

> 답을 외우지 말고, 핵심 포인트를 중심으로 자신만의 문장으로 설명할 수 있는지 확인한다.

---

## Q1. CPS(Continuation-Passing Style)란 무엇이며, Pipeline resume에서 어떤 역할을 하는가?

**핵심 포인트**
- CPS의 정의와 일반 함수 호출 방식과의 차이
- Jenkins가 Groovy 코드를 CPS 변환하는 이유
- FlowNode 단위로 실행 상태를 직렬화하는 방식
- controller 재시작 후 FlowNode를 역직렬화하여 실행을 재개하는 흐름

**심화 질문**
- CPS가 아닌 일반 Groovy 스크립트는 왜 resume이 안 되는가?
- `@NonCPS` 어노테이션을 붙인 메서드가 resume에 미치는 영향은?

---

## Q2. Resumable step과 nonresumable step의 차이를 예시와 함께 설명하라

**핵심 포인트**
- `sh`, `input`이 resumable로 설계된 이유와 동작 방식
- `checkout`, `junit`이 nonresumable인 이유와 재시작 시 동작
- controller 재시작을 견디는 step과 그렇지 않은 step의 설계 의도 차이
- nonresumable step 실행 중 controller가 죽었을 때 발생하는 상황

**심화 질문**
- 커스텀 step을 만든다면 resumable하게 만들기 위해 무엇이 필요한가?
- step이 resumable인지 여부를 코드나 문서에서 어떻게 확인할 수 있는가?

---

## Q3. sh step 실행 중 Jenkins controller가 죽으면 실제로 어떤 일이 벌어지는가?

**핵심 포인트**
- durable-task 플러그인이 sh 프로세스를 추적하는 방식
- controller가 죽어도 agent 프로세스가 생존하는 이유
- controller 복구 후 agent 재연결(reconnection) 과정
- workspace 파일과 `.jenkins` 추적 파일의 역할

**심화 질문**
- agent도 controller와 함께 죽은 경우는 어떻게 다른가?
- durable-task 플러그인이 없다면 sh step은 어떻게 동작하는가?

---

## Q4. disableResume()은 어떤 상황에서 사용하며, 사용하지 않으면 어떤 위험이 있는가?

**핵심 포인트**
- `options { disableResume() }` 선언 위치와 효과
- 멱등성을 보장할 수 없는 파이프라인에서 resume이 위험한 이유
- 외부 시스템(결제, 배포, API 호출)에 부작용을 남기는 작업의 특성
- resume 금지를 정책으로 강제해야 하는 팀/조직 시나리오

**심화 질문**
- `disableResume()`과 `disableRestartFromStage()`의 차이는?
- resume을 허용하면서도 외부 부작용을 방지하는 설계 방법이 있는가?

---

## Q5. Durability 설정의 레벨별 차이와 각각의 트레이드오프를 설명하라

**핵심 포인트**
- `MAX_SURVIVABILITY`, `SURVIVABLE_NONATOMIC`, `PERFORMANCE_OPTIMIZED` 세 레벨의 의미
- 디스크 쓰기 빈도와 복구 안정성 사이의 트레이드오프
- 레벨별로 복구 가능한 상황과 불가능한 상황
- 기본값이 무엇이며 왜 그렇게 설정되어 있는지

**심화 질문**
- 대규모 Jenkins 환경에서 durability를 낮추는 것이 합리적인 경우는?
- `PERFORMANCE_OPTIMIZED`로 설정한 파이프라인이 crash 후 어떤 상태가 되는가?

---

## Q6. "Restart from Stage"와 자동 resume의 근본적 차이는 무엇인가?

**핵심 포인트**
- Restart from Stage 실행 시 새 build number가 생성되는 이유
- 재시작 가능한 top-level stage 선택 방식과 제약
- Declarative Pipeline 전용 기능인 이유
- 이전 단계가 skip되는 동작과 환경 변수/아티팩트 재사용 여부

**심화 질문**
- Scripted Pipeline에서 유사한 기능을 구현하려면 어떻게 해야 하는가?
- Restart from Stage 사용 시 이전 build의 상태를 어떻게 참조하는가?

---

## Q7. Pipeline resume 설계에서 멱등성(idempotency)이 왜 핵심적으로 중요한가?

**핵심 포인트**
- "resume될 수 있다"는 전제가 step 설계에 미치는 영향
- 동일 step이 두 번 실행되었을 때 안전한 경우와 위험한 경우의 구분
- 외부 API 호출, 배포, 데이터 변경 작업의 중복 실행 위험
- 멱등성을 전제로 한 파이프라인 설계 원칙

**심화 질문**
- 멱등성을 보장하기 어려운 step은 어떻게 설계하는가?
- 이미 배포된 서비스에 resume이 발생했을 때 롤백 전략은?

---

## Q8. Agent, container, pod의 생명주기가 Pipeline resume에 어떤 영향을 미치는가?

**핵심 포인트**
- controller와 agent의 역할 분리가 resume 가능성에 미치는 영향
- Kubernetes 환경에서 pod 재생성 시 workspace 유실 문제
- durable-task 추적 파일이 ephemeral 스토리지에 있을 때의 위험
- agent 재연결 타임아웃과 resume 성공 여부의 관계

**심화 질문**
- Kubernetes 환경에서 Pipeline resume의 근본적 한계는 무엇인가?
- PVC를 활용해 workspace를 영속화하면 resume 안정성이 달라지는가?

---

## Q9. 운영 환경에서 특정 Pipeline이 resume 가능한지 어떻게 판별할 수 있는가?

**핵심 포인트**
- 파이프라인의 durability 설정 확인 방법
- 실행 중이던 step이 resumable인지 여부 판단 기준
- controller 재시작 전후 agent 상태 및 연결 확인 방법
- FlowNode 로그에서 resume 시도 흔적을 찾는 방법

**심화 질문**
- resume 실패 시 어떤 로그/이벤트를 먼저 확인해야 하는가?
- resume 가능성을 사전에 테스트하는 방법이 있는가?

---

## Q10. retry 블록을 활용한 nonresumable step 보호 패턴을 설명하라

**핵심 포인트**
- `retry(N) { checkout scm }` 패턴이 nonresumable step 실패를 보호하는 방식
- retry와 멱등성의 관계 — retry가 안전하려면 step이 멱등해야 하는 이유
- retry 범위를 넓게/좁게 잡을 때의 트레이드오프
- 실패 알림과 retry를 조합하는 실무 패턴

**심화 질문**
- `retry`와 `catchError`의 조합은 언제 사용하는가?
- retry 횟수를 소진한 후 파이프라인 전체를 실패시키지 않고 특정 분기로 유도하려면?
