# Ch05. 배포 전략 심화 — 탐구 질문

이 파일은 LEARN.md를 읽은 뒤 스스로 답을 찾아야 할 질문들이다.
정답을 바로 찾기보다, 먼저 자신의 언어로 답을 써보고 나서 검증하라.
각 질문에 2-3문장으로 자신의 생각을 먼저 적고, 공식 문서나 코드로 확인하는 순서를 권장한다.

---

## Q1. Feature Toggle 4가지 유형과 수명주기 관리

Pete Hodgson의 분류에 따르면 Feature Toggle은 Release, Experiment, Ops, Permission 4가지로 나뉜다. 각 유형은 수명(lifetime)과 역동성(dynamism)에서 본질적으로 다르다.

- 각 유형의 **전형적인 수명**(며칠, 몇 주, 영구)은 어떻게 다른가? 수명이 짧을수록 더 자주 변경되는가, 아니면 반대인가?
- "결제 기능 점검 중에 결제 버튼을 비활성화한다"는 어느 유형인가? 이 토글을 담당 팀이 실시간으로 제어할 수 있어야 하는 이유는?
- "베타 사용자에게만 새 대시보드를 보여준다"는 어느 유형인가? 이 토글의 판단 기준(사용자 속성)이 코드에 하드코딩되면 안 되는 이유는?
- Release Toggle을 6개월 동안 유지하면 코드베이스에 어떤 일이 벌어지는가? `if (isEnabled("old-flag")) { ... } else { ... }` 형태의 분기가 10개 중첩되면 테스트해야 할 경로는 최대 몇 가지인가?
- 수명주기 자동화의 핵심은 "만료일 강제"다. CI에서 만료된 토글을 감지해 빌드를 실패시키면, 개발팀이 토글 삭제를 미룰 때 어떤 압박이 생기는가? 이것이 기술 부채 관리에서 "자동화된 강제"가 중요한 이유다.
- 토글 결정(ON/OFF)이 비즈니스팀 권한인 경우(예: Permission Toggle)와 개발팀 권한인 경우(Release Toggle)를 어떻게 구분하는가? Unleash의 "환경별 설정"이 이 문제를 어떻게 해결하는가?

---

## Q2. A/B Testing의 통계적 유의성 판단

A/B Testing에서 "결과가 통계적으로 유의하다"는 말은 직관과 다르게 동작한다. 잘못 이해하면 잘못된 제품 결정으로 이어진다.

- p-value 0.05의 정확한 의미는 무엇인가? "95% 확률로 B가 낫다"는 해석이 왜 틀렸는가? p-value는 B의 우월성 확률이 아니라 무엇의 확률인가?
- **Peeking Problem**이란 무엇인가? 실험 도중 데이터를 보고 "오, 이미 유의하다" 싶을 때 종료하면 왜 False Positive 비율이 5%를 크게 초과하는가? Sequential Testing이나 Bayesian 접근이 이를 어떻게 완화하는가?
- 실험 시작 전에 표본 크기를 미리 계산해야 하는 이유는? 표본이 부족하면 실제 차이가 있어도 "유의하지 않다"는 결론이 나올 수 있다(검정력 부족). 표본 크기에 영향을 주는 변수 3가지(기준선 전환율, 최소 탐지 효과 크기, 유의수준 α)를 각각 설명하라.
- nginx의 `split_clients`가 IP 해시를 기본으로 쓰는 이유는 일관성 때문이다. 같은 사용자가 매 요청마다 A/B를 오가면 실험 결과가 오염된다. 그렇다면 NAT 뒤에 수천 명이 같은 IP를 공유하는 환경에서 IP 해시는 어떤 문제를 일으키는가?
- A/B 테스트 결과가 통계적으로 유의하지 않을 때, 파이프라인은 자동으로 기존 버전(A)을 유지해야 하는가, 아니면 사람이 결정해야 하는가? 자동화의 한계는 어디인가?
- LEARN.md에서 nginx `split_clients`의 해시 키로 `$remote_addr`을 썼다. 로그인한 사용자에게 더 일관된 경험을 보장하려면 어떤 값을 해시 키로 쓰는 것이 좋은가? 쿠키 기반 그룹 배정의 장단점은?

---

## Q3. SLSA Level 1-4 각 단계의 요구사항

SLSA는 "이 바이너리가 정말 이 소스코드에서 빌드됐는가"를 증명하는 신뢰 체계다. 각 단계가 어떤 공격 벡터를 방어하는지 이해해야 각 단계의 가치를 판단할 수 있다.

- SLSA Level 1은 provenance를 생성하지만 서명하지 않는다. 서명 없는 provenance를 공격자가 어떻게 위조할 수 있는가? Level 2에서 서명이 추가되면 이 공격이 왜 어려워지는가?
- SLSA Level 3에서 "빌드 환경이 격리된다"는 것은 빌드 워커가 소스코드나 빌드 스크립트를 변조할 수 없어야 한다는 의미다. 이를 보장하려면 빌드 워커가 빌드 중에 어떤 권한을 가져서는 안 되는가?
- SLSA Level 4의 **재현 가능한 빌드**가 어려운 이유는 비결정적 요소 때문이다. 타임스탬프, 파일 정렬 순서, 컴파일러 버전 차이를 제거하는 구체적인 방법(`SOURCE_DATE_EPOCH`, `--remap-path-prefix`)을 조사하라.
- `slsa-verifier verify-artifact` 명령이 검증하는 항목 중 "예상 소스 저장소"와 "예상 태그"가 포함된다. 이 두 항목을 검증하지 않으면 어떤 공격이 가능한가? (다른 저장소의 합법적인 빌드 provenance를 재사용하는 시나리오)
- 대부분의 조직이 SLSA Level 2-3에서 멈추는 이유는 재현 가능한 빌드 달성이 현실적으로 난이도가 높기 때문이다. 조직에서 SLSA Level 선택 시 "위협 모델"과 "구현 비용"을 어떻게 균형 잡을 것인가?
- SLSA provenance를 생성한 후 배포 전에 검증하지 않으면 provenance가 있어도 의미가 없다. 검증 단계를 어느 파이프라인 단계에 배치해야 하는가? (빌드 직후 vs 프로덕션 배포 직전)

---

## Q4. OPA/Rego 정책으로 배포 게이트 구현

OPA는 "정책을 API로 평가"하는 범용 엔진이다. 배포 파이프라인에 통합하면 정책 변경이 파이프라인 코드 변경과 완전히 분리된다. 정책팀이 Rego를 수정하면, 다음 배포부터 즉시 새 정책이 적용된다.

- LEARN.md의 Rego 정책에서 `default allow = false`(Fail Closed)인 이유는? 시스템이 OPA 서버에 연결하지 못할 때 `default allow = true`(Fail Open)를 쓰면 어떤 일이 벌어지는가?
- `deny[reason]` 배열로 거부 이유를 반환하는 이유는? 단순히 `deny = true`보다 디버깅이 왜 쉬워지는가? CI 로그에서 "Policy check failed" 한 줄만 보이는 것과 구체적인 이유 목록이 보이는 것의 차이를 생각해보라.
- OPA를 사이드카(Pod 안에 함께 배포)로 쓸 때와 중앙 서버로 쓸 때의 트레이드오프는? 사이드카는 네트워크 장애에 강하지만 정책 배포가 복잡해진다. 중앙 서버는 관리가 쉽지만 단일 장애점이 된다. 각각 언제 선택하는가?
- Kubernetes Admission Webhook에서 OPA(또는 OPA Gatekeeper)를 쓰면 `kubectl apply` 시점에 정책을 강제할 수 있다. 이것이 파이프라인 게이트와 중복처럼 보이는데, 왜 두 레이어를 모두 유지하는 것이 Defense in Depth 관점에서 올바른가?
- `opa test` 명령으로 Rego 정책을 단위 테스트하는 방법을 조사하라. `test_allow_when_all_conditions_met`와 `test_deny_when_critical_vulnerability_found` 두 테스트를 어떻게 작성하는가?
- LEARN.md의 OPA 정책에서 `deployment_frozen` 조건이 `hotfix-` 태그를 예외로 두었다. 이 예외 로직이 악용되면 어떤 보안 문제가 생기는가? 예외 처리를 더 안전하게 만들려면 어떻게 해야 하는가?

---

## Q5. Dark Launch의 구현 방법과 리스크

Dark Launch는 사용자에게 영향을 주지 않으면서 프로덕션 트래픽으로 신규 버전을 검증한다. 구현은 단순해 보이지만, 부수 효과(side effect) 처리가 까다롭다.

- LEARN.md의 `shadowMiddleware`에서 왜 `await`를 쓰지 않는가? Shadow 요청이 500ms 걸릴 때 `await`를 쓰면 사용자 응답 시간에 어떤 영향을 주는가?
- Shadow 서비스가 DB에 쓰기 작업을 수행하면 데이터가 오염된다. 이를 방지하는 방법 두 가지는 (1) Shadow 서비스에 별도 테스트 DB를 연결하는 것과 (2) Shadow 서비스를 읽기 전용으로만 구현하는 것이다. 각각의 한계는 무엇인가?
- 응답 비교에서 타임스탬프(`created_at`), UUID, 랜덤 요소처럼 **의도적으로 달라야 하는 필드**를 비교에서 제외하지 않으면 divergence 비율이 100%에 가까워진다. 이런 필드를 체계적으로 제외하는 방법은?
- Dark Launch와 Canary 배포의 근본적인 차이는 "사용자가 새 버전의 응답을 받는가"다. 어떤 상황에서 Canary 대신 Dark Launch를 선택해야 하는가? (예: 응답 형식이 하위 호환되지 않는 대규모 리팩토링)
- Shadow 트래픽이 외부 결제 API나 SMS 발송 API를 호출하면 실제 요금이 청구되거나 사용자에게 문자가 발송된다. 이를 방지하기 위해 Shadow 환경에서 외부 API 호출을 가로채는 방법은? (Mock 서버, WireMock, 환경변수 기반 분기)
- Dark Launch 운영 중 divergence 비율이 2%에서 갑자기 15%로 올라갔다. 어떤 순서로 원인을 조사하겠는가? 타임스탬프 변경과 비즈니스 로직 버그를 어떻게 구분하는가?

---

## Q6. Feature Toggle 기술 부채 관리

Feature Toggle은 단기적으로는 배포 유연성을 주지만, 장기적으로 방치하면 코드베이스의 이해와 테스트를 불가능하게 만든다. 이를 기술 부채로 인식하고 체계적으로 관리해야 한다.

- 토글이 N개 있을 때 이론적으로 가능한 코드 경로의 조합은 2^N이다. 토글이 10개면 1,024가지 경로가 존재한다. 이것이 실제로 QA에 어떤 영향을 주는가? 물론 모든 조합이 프로덕션에서 발생하지는 않지만, 어떤 조합이 발생할지 예측하기 어렵다는 것이 문제다.
- LEARN.md의 `checkExpiredFlags` 스크립트를 CI 파이프라인의 어느 단계에 넣어야 하는가? lint 단계(빠른 실패)가 test 단계(느리지만 전체 검증 후)보다 왜 더 나은가?
- Ops Toggle은 "언제 꺼야 할지 모른다"는 특성 때문에 만료일을 두기 어렵다. 대신 Ops Toggle을 관리하는 대안적 방법은? (분기 리뷰, 사용 메트릭 감시, 오너십 지정)
- "Feature Toggle 없이 같은 목표를 달성할 수 있는가?"를 먼저 묻는 것이 중요하다. 단순히 "이 기능은 일단 꺼두자"는 이유로 토글을 추가하는 것이 과도한 해결책인 상황의 예시를 들어라. 토글 대신 어떤 대안이 있는가?
- Strangler Fig 패턴으로 레거시 시스템을 교체할 때, Feature Toggle을 어떻게 활용하는가? 새 구현체를 토글 뒤에 숨기고 점진적으로 트래픽을 전환하는 과정이 Canary 배포와 어떻게 다른가?
- 토글 레지스트리(`FEATURE_FLAGS` 객체)를 코드베이스가 아닌 외부 설정 서비스(Unleash, LaunchDarkly)에서만 관리하면 만료일 강제(`checkExpiredFlags`)가 어떻게 달라지는가? 코드 레벨 레지스트리와 외부 서비스 관리의 장단점을 비교하라.

---

## 탐구 힌트

- Martin Fowler, "Feature Toggles (aka Feature Flags)": 4가지 유형 분류의 원전 — https://martinfowler.com/articles/feature-toggles.html
- Unleash 공식 문서, "Activation Strategies": 점진적 롤아웃(gradual rollout by userId) 구현 — https://docs.getunleash.io/reference/activation-strategies
- Evan Miller, "How Not To Run an A/B Test": Peeking Problem의 수학적 설명 — https://www.evanmiller.org/how-not-to-run-an-ab-test.html
- Evan Miller, "Sample Size Calculator": 표본 크기 계산 도구 — https://www.evanmiller.org/ab-testing/sample-size.html
- SLSA 공식 사이트, "Threats & Mitigations": 각 Level이 방어하는 공격 매핑 — https://slsa.dev/spec/v1.0/threats
- SLSA GitHub Generator: GitHub Actions에서 SLSA Level 3 provenance 생성 — https://github.com/slsa-framework/slsa-github-generator
- OPA 공식 문서, "Policy Testing": `opa test` 단위 테스트 작성법 — https://www.openpolicyagent.org/docs/latest/policy-testing/
- OPA Gatekeeper: Kubernetes Admission Webhook 통합 — https://open-policy-agent.github.io/gatekeeper/
- Netflix Tech Blog, "Diffy: Semantic Diffing for Services": Dark Launch 대규모 운영 사례
- Twitter Engineering, "Diffy": Shadow Traffic 비교 프레임워크 오픈소스 — https://github.com/opendiffy/diffy
- CDEvents 스펙: CI/CD 이벤트 표준 포맷 — https://cdevents.dev/docs/

---

## 자기 점검 체크리스트

탐구를 마친 후 아래 항목에 자신 있게 답할 수 있는지 확인하라.

- [ ] Feature Toggle 유형 4가지를 예시와 함께 구분해서 설명할 수 있다
- [ ] "이 토글은 언제 삭제해야 하는가"라는 질문에 유형별로 답할 수 있다
- [ ] p-value의 정확한 의미를 동료에게 설명할 수 있다 (오해 없이)
- [ ] SLSA Level 3이 Level 2보다 강력한 이유를 공격 시나리오로 설명할 수 있다
- [ ] OPA Rego 정책을 직접 수정하고 `opa test`로 검증할 수 있다
- [ ] Dark Launch 구현 시 외부 API 부수 효과를 방지하는 방법을 설계할 수 있다
- [ ] 현재 팀 코드베이스에서 만료된 Feature Toggle이 몇 개인지 파악할 수 있다
