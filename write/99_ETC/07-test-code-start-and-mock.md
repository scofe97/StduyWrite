---
title: 테스트 코드 시작과 Mock 활용
tags: [testing, tdd, mock, junit, beginner]
status: draft
source:
  - youtube: 재미 채널 — "TDD 환경 + Mock Q&A"
  - Meszaros G. xUnit Test Patterns (2007) — Test Double 5종 (Dummy, Stub, Spy, Mock, Fake)
  - Fowler M. "Mocks Aren't Stubs" (2007) — https://martinfowler.com/articles/mocksArentStubs.html
  - Beck K. Test-Driven Development by Example (2002)
related: []
updated: 2026-05-09
---

# 테스트 코드 시작과 Mock 활용
---
> 테스트 입문자가 가장 자주 막히는 두 지점은 "어떻게 시작하는가"와 "Mock을 어디까지 써야 하는가"다. 답의 출발점은 동일하다 — **잘 만들려는 욕심을 버리고 일단 작성**.
>
> - 진입 단계의 "동작 우선" 휴리스틱
> - Mock 어려움의 진짜 원인 분리
> - Test Double 표준 분류와 강사 의견의 위치

## 1. 이 문서의 출처와 위치

본 문서는 한국 백엔드 채널 "재미"의 Q&A 영상을 정리한 것이다. 두 질문이 묶여 있다.

- 질문 1: "TDD 환경 구축이 쉽지 않다. 어떻게 접근할까?"
- 질문 2: "테스트 코드를 작성해 보고 싶은데 어떻게 시작해야 하나?"

이 문서는 `99_ETC/`에 임시 배치한다. 이유는 `runners-high/write/`의 카테고리 체계에 testing 카테고리가 아직 없기 때문이다. 세컨드 브레인 하네스 §4.4에 따르면 신규 카테고리 신설은 5개 이상 문서 확보 시. 향후 테스트 관련 문서가 누적되면 `12_testing/` 같은 별도 카테고리로 이동한다.

## 2. 진입 단계 — "잘 만들려는 욕심"이 진짜 장벽

강사가 영상 첫 문단에서 명시적으로 거부하는 사고 방식은 다음과 같다.

```
잘못된 시작
─────────
"좋은 테스트가 무엇인지 먼저 학습한다"
   → 책 읽기 (xUnit Patterns, TDD by Example)
   → 베스트 프랙티스 정리
   → 의존성 주입 패턴 검토
   → 테스트 더블 분류 학습
   → ... (영원히 시작 못 함)
```

강사 표현: "처음부터 너무 잘 만들고 테스트를 능숙하게 쓰고 싶어서 그런 것 같다. 그 생각을 버려야 한다." 본인도 과거 프로젝트 생성 직후 `test/` 폴더부터 지웠다는 자기 고백이 이어진다.

권장 시작 절차는 단순하다.

```
권장 시작
─────────
1. IDE 단축키로 테스트 클래스 생성 (Cmd+Shift+T 등)
2. 해결하고 싶은 동작 1개를 떠올린다
   (예: "버그 X가 다시는 발생하지 않게")
3. 그 동작을 검증하는 테스트 1개만 작성
4. 통과시킨다
5. 다음 테스트 추가
```

이 절차의 핵심은 "잘 만들려는 욕심"을 차단하는 것이다. 세련된 구조는 작성 경험이 누적된 뒤에 자연히 드러난다.

## 3. 의존성 많은 코드를 만났을 때 — 멈추지 마라

진입 직후 입문자가 흔히 막히는 지점은 "테스트하려는 클래스가 의존성을 너무 많이 가지고 있을 때"다.

```java
// 입문자가 멈추는 순간
public final class OrderService {
    private final OrderRepository orderRepository;
    private final UserRepository userRepository;
    private final ProductRepository productRepository;
    private final PaymentClient paymentClient;
    private final NotificationSender notificationSender;
    private final OrderKeyGenerator orderKeyGenerator;
    // ... 7~8개의 의존성

    public Order placeOrder(...) { ... }
}
```

입문자의 사고 흐름: "이걸 다 어떻게 처리하지? Mock을 만들어야 하나? Stub으로 하나? 어디까지 진짜 객체로?"

강사 답변은 단호하다 — **고민하지 말고 일단 다 Mock으로 채워라.**

```java
@Test
void placeOrder_works() {
    // 일단 다 Mock
    OrderRepository orderRepository = mock(OrderRepository.class);
    UserRepository userRepository = mock(UserRepository.class);
    ProductRepository productRepository = mock(ProductRepository.class);
    PaymentClient paymentClient = mock(PaymentClient.class);
    NotificationSender notificationSender = mock(NotificationSender.class);
    OrderKeyGenerator orderKeyGenerator = mock(OrderKeyGenerator.class);

    OrderService service = new OrderService(
        orderRepository, userRepository, productRepository,
        paymentClient, notificationSender, orderKeyGenerator
    );

    // 검증하고 싶은 동작 1개
    Order result = service.placeOrder(...);

    assertThat(result).isNotNull();
}
```

강사 표현: "테스트가 돌아가게 한 다음에 리팩토링 하면 된다. 처음부터 어떻게 좋은 테스트를 만들지 고민하지 말고 그냥 일단 만들어라."

## 4. Mock이 어렵다 — 어려움의 진짜 원인 분리

질문 1의 "Mock이 쉽지 않다"라는 표현이 가리키는 어려움은 두 가지로 분리해야 한다.

| 어려움의 종류 | 원인 | 해결 |
|--------------|------|------|
| Mock 객체 생성이 어렵다 | API 사용법 모름 | `mock(Class.class)` 한 줄로 끝 |
| 어디까지 Mock 할지가 어렵다 | 테스트 더블 분류 학습 부재 | 입문자는 다 Mock으로 시작, 익숙해지면 분리 |

강사가 Q&A에서 답한 부분은 두 번째 어려움이다. 답: **일단 다 Mock**. 그 다음 단계로 넘어가는 시점은 "테스트가 너무 깨지기 쉽다"는 신호가 보일 때다.

## 5. 테스트 더블 표준 분류 — 학습은 나중에

강사는 의도적으로 테스트 더블 분류를 다루지 않는다. 입문자가 분류 학습에 시간을 쓰다 진입을 못 하는 패턴을 경계하기 위함이다. 다만 학습자가 어느 정도 작성 경험을 쌓고 나면 표준 분류를 알아야 코드 리뷰가 쉬워진다.

표준 분류는 Gerard Meszaros의 *xUnit Test Patterns* (2007)에서 정립되었다.

| Test Double | 정의 | 사용 예 |
|-------------|------|---------|
| Dummy | 인자 채우기용. 실제로 사용되지 않음. | 호출 안 되는 의존성 주입용 |
| Stub | 정해진 응답만 반환 | "항상 user 객체를 반환하라" |
| Spy | Stub + 호출 기록 | "save가 몇 번 호출됐는지 검증" |
| Mock | 사전 기대(expectation) 설정 후 검증 | "save는 정확히 이 인자로 1번 호출돼야 함" |
| Fake | 단순화된 진짜 구현 | InMemoryRepository |

Mockito 같은 프레임워크에서 `mock()`은 사실상 Stub + Spy를 합친 형태다. 엄밀한 Mock(사전 기대 설정)은 Mockito의 `verify()`와 `when().thenReturn()` 조합으로 구현한다.

## 6. Classical vs Mockist — 학파 차이

Martin Fowler가 "Mocks Aren't Stubs" (2007)에서 정리한 두 학파는 다음과 같다.

| 학파 | 검증 대상 | Mock 사용 |
|------|----------|----------|
| Classical (Detroit School) | 결과 상태 (state) | 외부 시스템만 Mock, 내부 협력 객체는 진짜 |
| Mockist (London School) | 상호작용 (interaction) | 모든 협력 객체를 Mock |

강사가 Q&A에서 보여준 "다 Mock" 권장은 표준 분류상 Mockist에 가깝다. 다만 강사의 의도는 학파 선택이 아니라 진입 장벽 낮추기다 — Classical로 시작하든 Mockist로 시작하든, 일단 작성하는 것이 학파 선택보다 우선이라는 입장.

## 7. TDD vs 일반 테스트 — 강사가 명시한 구분

영상 후반에서 강사는 본인이 보여준 절차가 TDD가 아니라고 정정한다.

```
TDD 정의 (Kent Beck)
─────────────────
1. Red — 실패하는 테스트 작성
2. Green — 테스트가 통과하도록 최소한의 코드 작성
3. Refactor — 코드 개선

강사가 보여준 절차
─────────────────
1. 코드 먼저 작성
2. 그 코드를 검증하는 테스트 작성
3. 통과시킨다
4. 점진적으로 개선
```

차이는 "테스트가 코드 작성을 주도하는가"다. TDD는 테스트가 설계를 주도한다. 강사가 보여준 절차는 후행 테스트 작성 (test-after) 이다. 둘 다 가치가 있고, 입문자는 후행 작성으로 시작해 익숙해지면 TDD로 격상하는 경로가 일반적이다.

강사 표현: "TDD 환경을 구성하는 것과 Mock 사용은 사실 상관이 없다. 그냥 계속 만들어 봐야 한다."

## 8. 강사가 본인 프로젝트에서 쓰는 테스트 분리 패턴

영상에서 강사는 본인 프로젝트의 테스트 분리 관행을 짧게 보여준다.

```
src/test/java/
├── unit/                       (기본 — CI에서 실행)
│   └── OrderServiceTest.java
├── develop/                    (수동 실행 — CI에서 제외)
│   └── ExperimentalTest.java   (작성 중인 거친 테스트)
└── context/                    (CI에서 실행)
    └── OrderContextTest.java   (잘 정돈된 통합 테스트)
```

핵심 의도는 "거친 테스트 작성을 독려"하는 것. `develop/`은 CI에서 빠지므로 작성 부담 없이 실험 가능. 이 안에서 "괜찮은 테스트"가 나오면 `context/`로 승격한다.

이 패턴은 표준 절차는 아니지만 입문자가 "테스트를 작성하면 CI가 깨질까 봐" 위축되는 것을 막는 휴리스틱이다.

## 9. 입문자에게 강사가 강조한 메타 메시지

| 메시지 | 의미 |
|--------|------|
| 두려워하지 마라 | 처음 짠 테스트가 엉망인 건 자연스럽다 |
| 일단 많이 짜라 | 좋은 테스트는 작성 경험 누적의 결과 |
| 같은 버그 두 번 발생 방지가 1차 목표 | 거창한 SRP/SOLID 적용보다 구체적 효용 |
| 테스트도 리팩터링 대상 | 처음부터 완벽할 필요 없음 |
| TDD 학습은 TDD 시도로만 가능 | 책 읽기로 TDD 능력은 안 늘어남 |

이 메시지의 공통 원리는 "행동 우선, 이론 나중"이다. 강사가 영상에서 반복적으로 인용하는 책의 관점 ("테스트도 코드 리뷰하고 개선하는 대상")은 표준 진영의 합의이기도 하다 (*xUnit Patterns* §1.3).

## 10. 강사 의견 vs 표준 비교

| 주제 | 강사 (재미) | 표준 |
|------|-------------|------|
| 시작 절차 | 코드 작성 후 테스트 (test-after) | TDD (Beck) — Red-Green-Refactor |
| Mock 정책 | 입문자는 다 Mock | Classical: 외부 시스템만 / Mockist: 모두 |
| Test Double 학습 시점 | 작성 경험 누적 후 | 학습 초기에 분류 명확히 |
| 통합 vs 단위 | 통합으로도 충분한 경우가 많다 | Test Pyramid (Cohn) — 단위 테스트 우선 |
| TDD 학습법 | 직접 시도 반복 | Kata 같은 구조화된 연습 |

차이의 원인은 강사가 입문자의 진입 장벽 낮추기를 우선시한다는 점에 있다. 어느 정도 작성 경험이 누적되면 학습자는 표준 분류와 학파를 익혀야 코드 리뷰와 협업이 원활해진다.

## 11. 정리

- 테스트 시작의 진짜 장벽은 기술이 아니라 "잘 만들려는 욕심"이다.
- 진입 단계: 단축키로 테스트 만들고, 검증하고 싶은 동작 1개부터 작성.
- 의존성 많은 코드는 일단 다 Mock으로 채우고 통과시킨다. 분류 학습은 나중.
- "Mock이 어렵다"는 두 가지 어려움의 합. 생성은 한 줄, 어디까지 Mock 할지는 경험.
- 강사가 보여준 절차는 TDD가 아니라 test-after. 둘 다 가치 있고 시작 단계에선 test-after가 진입 부담이 낮다.
- `develop/` 같은 CI 제외 폴더로 거친 테스트 작성을 독려하는 패턴이 유효하다.
- 표준 분류 (Test Double 5종, Classical vs Mockist)는 작성 경험 누적 후 학습한다.

## 12. 향후 카테고리 분리 후보

테스트 관련 문서가 5개 이상 누적되면 다음 구조로 분리할 후보다.

```
write/12_testing/
├── README.md
├── 01-01.테스트 코드 시작과 Mock 활용.md   (현 문서를 이전)
├── 01-02.Test Double 5종 분류와 적용 시점.md
├── 02-01.TDD 절차와 Kata 연습.md
├── 02-02.통합 테스트 vs 단위 테스트 트레이드오프.md
├── 03-01.Spring Boot 테스트 슬라이스.md
└── 03-02.Testcontainers 활용.md
```

이 시점이 오면 본 문서는 `99_ETC/`에서 `12_testing/01-01.`로 이동하고, MOC와 인바운드 링크를 함께 갱신한다 (세컨드 브레인 하네스 §9 이관 프로토콜 준용).
