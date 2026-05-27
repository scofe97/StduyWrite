# Ch03. INVESTIGATE — 테스트 자동화 패턴과 브랜칭

탐구 질문 6개. 각 질문은 LEARN.md 개념을 더 깊이 파고들거나 실무 경험으로 연결하기 위한 것이다.

---

## Q1. Data-Driven Testing과 Property-Based Testing의 차이는 무엇인가?

**Data-Driven Testing**은 미리 정의된 구체적인 입력-출력 쌍으로 테스트한다. `amount=150, tier="premium" → 120.0`처럼 테스트 작성자가 케이스를 명시적으로 나열한다. 장점은 예측 가능성과 문서화 효과다. 단점은 작성자가 생각하지 못한 입력값은 검증되지 않는다는 것이다.

**Property-Based Testing**은 입력의 "속성(property)"을 기술하면 프레임워크가 무작위 입력을 수백 개 생성해서 테스트한다. Python의 `hypothesis`, Haskell의 `QuickCheck`가 대표적이다. "어떤 양수 금액이든 할인 후 금액은 원래보다 작거나 같아야 한다"는 속성을 기술하면, 프레임워크가 엣지 케이스(0, 최댓값, 소수점 등)를 자동으로 탐색한다.

```python
from hypothesis import given, strategies as st

@given(
    amount=st.floats(min_value=0.01, max_value=1_000_000),
    tier=st.sampled_from(["standard", "premium", "vip"])
)
def test_discount_never_increases_price(amount, tier):
    result = calculate_discount(tier, amount)
    assert result <= amount  # 속성: 할인은 가격을 올리지 않는다
```

두 방식은 경쟁 관계가 아니라 보완 관계다. Data-Driven으로 비즈니스 규칙을 문서화하고, Property-Based로 구현의 불변 조건을 검증하는 방식으로 함께 사용한다.

---

## Q2. Page Object Model의 설계 원칙은 무엇이며, 어디까지 추상화해야 하는가?

POM의 핵심 원칙은 **"한 페이지의 변경이 한 클래스만 수정한다"**는 단일 변경 지점이다. 이를 위해 세 가지 규칙을 지킨다.

첫째, 페이지 객체는 검증(assertion)을 포함하지 않는다. `login_page.assert_error_shown()`이 아니라 `login_page.get_error_message()`를 반환하고, 테스트 코드에서 검증한다. 검증 로직이 페이지 객체 안에 있으면 같은 페이지를 다른 기대값으로 테스트할 때 재사용할 수 없다.

둘째, 페이지 객체는 다른 페이지 객체를 반환할 수 있다. `login_page.login(email, password)`가 성공하면 `DashboardPage` 인스턴스를 반환하는 방식이다. 이 패턴은 메서드 체이닝을 가능하게 한다.

셋째, 추상화는 페이지 단위가 기본이지만, 복잡한 컴포넌트(데이터 테이블, 모달, 드롭다운)는 별도 컴포넌트 클래스로 분리하는 것이 낫다. 모든 페이지에서 공통으로 쓰이는 네비게이션 바는 `NavBar` 클래스로 분리하고 각 페이지 객체가 조합한다.

과도한 추상화 함정: 페이지 내 모든 요소를 메서드로 만들면 페이지 객체가 수백 줄이 된다. "자주 재사용되는가?"를 기준으로 메서드를 추가한다.

---

## Q3. 브랜칭 전략 선택은 팀 규모와 어떤 관계가 있는가?

팀 규모보다 정확히는 **동시 작업 수**와 **릴리즈 빈도**가 결정 요인이다.

동시 작업 수가 적고(3명 이하) 릴리즈가 잦으면(하루 여러 번) Trunk-Based가 최적이다. 브랜치가 없으니 머지 충돌도 없고 통합 지옥도 없다. 단, 이 전략이 작동하려면 feature flag 인프라와 강한 테스트 커버리지가 선행되어야 한다. 이 두 조건 없이 Trunk-Based를 시도하면 미완성 코드가 프로덕션에 나가는 사고가 발생한다.

팀 규모가 커질수록(10명 이상) 동시에 진행하는 기능이 많아져 브랜치 충돌 가능성이 높아진다. 이때 GitFlow처럼 명시적인 통합 브랜치(develop)를 두면 충돌 해결 지점이 명확해진다. 그러나 GitFlow는 릴리즈 브랜치, develop 브랜치, 핫픽스 브랜치를 모두 관리해야 하므로 운영 오버헤드가 크다. 팀이 이 복잡성을 감당할 여유가 없다면 GitHub Flow가 더 나은 선택이다.

결국 브랜칭 전략은 "우리 팀이 얼마나 자주 통합하고 얼마나 자주 배포하는가"에 맞춰야 한다. 좋은 전략이 따로 있는 게 아니라, 팀의 리듬에 맞는 전략이 있다.

---

## Q4. Trunk-Based Development에서 feature toggle은 어떤 역할을 하는가?

Feature toggle(feature flag)은 Trunk-Based를 가능하게 하는 핵심 메커니즘이다. 완성되지 않은 기능을 main에 머지하되, 플래그가 꺼진 상태로 배포한다. 플래그를 켜야만 기능이 활성화되므로 사용자에게는 보이지 않는다.

```python
# WHY: 코드는 main에 있지만 기능은 숨겨진 상태 — 통합과 릴리즈를 분리한다
from feature_flags import is_enabled

def checkout(user, cart):
    if is_enabled("new-payment-flow", user_id=user.id):
        return new_payment_processor.process(cart)
    else:
        return legacy_payment_processor.process(cart)
```

toggle의 종류도 다양하다. **Release toggle**은 미완성 기능을 숨기고, **Experiment toggle**은 A/B 테스트에 사용하며, **Ops toggle**은 성능 문제 시 특정 기능을 긴급 비활성화하는 킬 스위치 역할을 한다.

주의할 점은 toggle이 기술 부채가 된다는 것이다. 기능이 완전히 출시되면 toggle 코드를 제거해야 한다. 제거하지 않으면 코드베이스에 조건문이 쌓이고, 어떤 플래그가 켜져 있는지 추적하기 어려워진다. Toggle 생성 시 "이 플래그는 언제 제거하는가?"를 JIRA 티켓으로 남기는 것이 좋은 관습이다.

---

## Q5. Shift-Left Testing을 실제 팀에서 도입하는 방법은 무엇인가?

Shift-Left는 문화 변화이므로 도구보다 프로세스가 먼저다. 도구를 먼저 도입하고 문화를 나중에 바꾸려 하면 실패한다.

단계적 도입 방법을 생각해볼 수 있다. **1단계**는 Definition of Ready(DoR)를 정의하는 것이다. "이 기능을 개발 시작하기 전에 인수 테스트 시나리오가 있어야 한다"는 팀 규칙을 만든다. 기획·개발·QA가 스프린트 시작 전 시나리오를 같이 검토하는 Three Amigos 세션이 효과적이다.

**2단계**는 PR 머지 조건에 테스트 커버리지 임계값을 추가한다. 처음엔 현재 커버리지보다 5% 높게 설정하고, 분기마다 목표를 높인다. "커버리지를 낮추는 PR은 머지 불가"만으로도 개발자들이 테스트를 코드와 함께 작성하는 습관이 생긴다.

**3단계**는 버그 리포트를 재현 테스트로 전환한다. 버그가 발생하면 "이 버그를 재현하는 테스트 → 수정 → 테스트 통과" 순서로 처리한다. 이렇게 하면 같은 버그가 재발하지 않는다.

가장 흔한 실패 패턴은 "테스트 작성은 QA의 일"이라는 인식이다. Shift-Left에서 단위 테스트와 통합 테스트는 개발자의 책임이다.

---

## Q6. Flaky Test가 CI/CD 파이프라인에 미치는 영향과 해결 방법은?

Flaky test의 가장 큰 피해는 **신뢰 붕괴**다. CI가 자주 거짓 양성(false positive)을 내면 개발자들은 "어차피 flaky test 때문에 실패했겠지"라며 빨간 빌드를 무시하기 시작한다. 이 시점부터 CI는 형식적인 절차가 되고, 진짜 버그를 잡는 역할을 잃는다.

조직 수준의 해결 전략은 세 단계다.

**탐지**: Flaky test를 자동으로 식별한다. 같은 커밋에서 테스트를 3회 실행해서 결과가 다르면 flaky로 표시한다. Google의 경우 수백만 개 테스트 중 flaky를 자동 격리하는 시스템을 운영한다.

```yaml
# GitHub Actions retry 패턴 — flaky test 임시 완화
- name: Run tests with retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: pytest tests/e2e/ -v
```

**격리**: 확인된 flaky test는 별도 태그로 분류하고 main 파이프라인에서 제외한다. 별도 스케줄로 실행해서 수정 추적만 한다. 격리하지 않으면 팀 전체 생산성이 저하된다.

**근절**: 근본 원인을 찾아 수정한다. 대부분의 flaky test는 비동기 대기 부족, 테스트 간 공유 상태, 외부 서비스 의존 세 가지 중 하나다. 각각의 처방은 explicit wait, 테스트 픽스처 격리, 서비스 모킹이다. Flaky test 수정은 기능 개발과 동일한 우선순위로 취급해야 한다. "나중에 고치자"는 말은 "영원히 안 고친다"와 같다.
