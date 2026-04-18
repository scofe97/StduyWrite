# AssertJ와 TDD 패턴
---
> AssertJ는 메서드 체이닝으로 테스트 의도를 자연어에 가깝게 표현한다. TDD는 테스트를 먼저 작성함으로써 설계를 개선하고 회귀 버그를 방지하는 개발 방법론이다.

## 1. AssertJ vs JUnit Assertions 비교

JUnit 5의 기본 `Assertions`도 충분히 유용하지만, AssertJ는 체이닝과 커스텀 메시지 측면에서 더 표현력이 높다. 특히 컬렉션과 문자열 검증에서 차이가 두드러진다.

```java
// JUnit 5 Assertions
assertEquals(3, orders.size());
assertTrue(orders.stream().anyMatch(o -> o.getStatus().equals("PENDING")));
assertNotNull(order.getId());

// AssertJ — 동일한 검증, 자연어에 가까운 표현
assertThat(orders).hasSize(3);
assertThat(orders).anyMatch(o -> o.getStatus().equals("PENDING"));
assertThat(order.getId()).isNotNull();
```

JUnit `Assertions`의 실패 메시지는 "expected: 3 but was: 2" 수준이지만, AssertJ는 컬렉션 내용을 함께 출력하여 원인 파악이 빠르다. 커스텀 메시지도 `as()` 메서드로 체인에 자연스럽게 붙는다.

| 항목 | JUnit Assertions | AssertJ |
|------|-----------------|---------|
| 체이닝 | 불가 | 가능 |
| 실패 메시지 품질 | 기본 | 상세 (컬렉션 내용 포함) |
| 커스텀 메시지 | 마지막 인자 | `as()` 체이닝 |
| 컬렉션 검증 | 제한적 | `contains`, `extracting`, `filteredOn` 등 풍부 |
| 의존성 | junit-jupiter | assertj-core |

## 2. 핵심 검증 API

### 2-1. 기본 검증과 문자열

```java
import static org.assertj.core.api.Assertions.*;

@Test
void 기본_검증() {
    Order order = new Order(1L, "PENDING", 5000);

    assertThat(order.getId()).isEqualTo(1L);
    assertThat(order.getStatus()).isEqualTo("PENDING");
    assertThat(order.getAmount()).isGreaterThan(0).isLessThan(10000);
    assertThat(order).isNotNull();
    assertThat(order).isInstanceOf(Order.class);
}

@Test
void 문자열_검증() {
    String message = "주문이 성공적으로 처리되었습니다";

    assertThat(message)
        .startsWith("주문")
        .contains("성공")
        .endsWith("습니다")
        .hasSize(17);
}
```

### 2-2. 컬렉션 검증

AssertJ의 컬렉션 API는 단순한 크기 검증을 넘어 내용, 필터링, 필드 추출까지 지원한다. `extracting()`은 컬렉션 원소에서 특정 필드를 추출하여 검증할 때 특히 유용하다.

```java
@Test
void 컬렉션_검증() {
    List<Order> orders = List.of(
        new Order(1L, "PENDING", 3000)
        , new Order(2L, "COMPLETED", 7000)
        , new Order(3L, "PENDING", 5000)
    );

    assertThat(orders)
        .hasSize(3)
        .isNotEmpty();

    // 특정 원소 포함 여부
    assertThat(orders)
        .extracting(Order::getStatus)
        .contains("PENDING", "COMPLETED")
        .doesNotContain("CANCELLED");

    // 여러 필드를 tuple로 추출하여 검증
    assertThat(orders)
        .extracting("id", "status")
        .contains(
            tuple(1L, "PENDING")
            , tuple(2L, "COMPLETED")
        );

    // 조건으로 필터링 후 검증
    assertThat(orders)
        .filteredOn(o -> o.getStatus().equals("PENDING"))
        .hasSize(2)
        .extracting(Order::getAmount)
        .containsExactlyInAnyOrder(3000, 5000);
}
```

## 3. 예외 검증

AssertJ의 예외 검증은 예외 타입뿐 아니라 메시지, 원인(cause), 체인 전체를 검증할 수 있다. `assertThatThrownBy`와 `assertThatCode`는 각각 예외가 발생해야 하는 경우와 발생하지 않아야 하는 경우에 사용한다.

```java
@Test
void 예외_발생_검증() {
    InventoryService service = new InventoryService();

    assertThatThrownBy(() -> service.decrease(1L, -5))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("수량은 양수여야 합니다")
        .hasMessageContaining("양수");
}

@Test
void 예외_원인_검증() {
    assertThatThrownBy(() -> orderService.processWithDb(1L))
        .isInstanceOf(OrderProcessingException.class)
        .hasCauseInstanceOf(DataAccessException.class);
}

@Test
void 예외_미발생_검증() {
    assertThatCode(() -> service.decrease(1L, 5))
        .doesNotThrowAnyException();
}

@Test
void 특정_예외_타입_검증() {
    // catchThrowableOfType으로 예외 객체에 직접 접근
    OutOfStockException ex = catchThrowableOfType(
        () -> service.decrease(1L, 999)
        , OutOfStockException.class
    );

    assertThat(ex.getProductId()).isEqualTo(1L);
    assertThat(ex.getRequestedQty()).isEqualTo(999);
}
```

## 4. satisfiesExactly와 Optional 검증

`satisfiesExactly()`는 컬렉션의 각 원소에 대한 조건을 순서대로 정의한다. `contains()`나 `extracting()`보다 복합 조건 검증에 적합하다.

```java
@Test
void satisfiesExactly_순서있는_복합검증() {
    List<Order> orders = orderService.findAll();

    assertThat(orders).satisfiesExactly(
        first -> {
            assertThat(first.getStatus()).isEqualTo("PENDING");
            assertThat(first.getAmount()).isGreaterThan(0);
        }
        , second -> {
            assertThat(second.getStatus()).isEqualTo("COMPLETED");
            assertThat(second.getAmount()).isEqualTo(5000);
        }
    );
}
```

`Optional` 검증은 `isPresent()`, `isEmpty()`, `hasValue()`로 래핑 여부와 값을 함께 검증한다:

```java
@Test
void Optional_검증() {
    Optional<Order> found = orderService.findById(1L);
    Optional<Order> notFound = orderService.findById(999L);

    assertThat(found)
        .isPresent()
        .hasValueSatisfying(order -> {
            assertThat(order.getId()).isEqualTo(1L);
            assertThat(order.getStatus()).isEqualTo("PENDING");
        });

    assertThat(notFound).isEmpty();
}
```

## 5. 커스텀 Assertion

프로젝트 도메인에 맞는 커스텀 Assertion을 만들면 반복 검증 코드를 제거하고 테스트 의도를 도메인 언어로 표현할 수 있다. `AbstractAssert<S, A>`를 상속해 구현한다.

```java
// 커스텀 Assertion 클래스
class OrderAssert extends AbstractAssert<OrderAssert, Order> {

    private OrderAssert(Order order) {
        super(order, OrderAssert.class);
    }

    static OrderAssert assertThatOrder(Order order) {
        return new OrderAssert(order);
    }

    OrderAssert isPending() {
        isNotNull();
        if (!"PENDING".equals(actual.getStatus())) {
            failWithMessage("주문 상태가 PENDING이어야 하는데 <%s>입니다", actual.getStatus());
        }
        return this;
    }

    OrderAssert hasAmount(int expected) {
        isNotNull();
        if (actual.getAmount() != expected) {
            failWithMessage("주문 금액이 <%d>이어야 하는데 <%d>입니다", expected, actual.getAmount());
        }
        return this;
    }
}

// 사용 예시
@Test
void 커스텀_Assertion_활용() {
    Order order = orderService.placeOrder(1L, 3);

    assertThatOrder(order)
        .isPending()
        .hasAmount(15000);
}
```

## 6. Given-When-Then 패턴

*Given-When-Then*은 BDD(Behavior-Driven Development)에서 유래한 테스트 구조화 패턴이다. 각 블록이 테스트의 서로 다른 역할을 담당하므로, 처음 읽는 사람도 테스트 시나리오를 빠르게 파악할 수 있다.

```java
@Test
@DisplayName("재고가 충분할 때 주문하면 재고가 감소한다")
void 재고_충분_시_주문_성공() {
    // Given — 테스트 환경 설정 (초기 상태)
    Inventory inventory = new Inventory(1L, 50);
    given(inventoryRepository.findByProductId(1L)).willReturn(inventory);

    // When — 테스트 대상 동작 실행 (단 하나의 행위)
    orderService.placeOrder(1L, 3);

    // Then — 기대 결과 검증
    assertThat(inventory.getQuantity()).isEqualTo(47);
    then(orderRepository).should().save(any(Order.class));
}
```

각 블록은 주석이나 빈 줄로 명시적으로 구분한다. When 블록에는 단 하나의 동작만 있어야 한다. 두 개 이상의 When이 필요하다면 테스트를 분리해야 한다는 신호다.

## 7. Arrange-Act-Assert 패턴

*Arrange-Act-Assert*(AAA)는 Given-When-Then과 동일한 구조를 xUnit 커뮤니티에서 다르게 명명한 것이다. 목 기반 단위 테스트에서 더 자주 사용되며, 의미는 동일하다.

```java
@Test
void 할인_쿠폰_적용_시_금액_감소() {
    // Arrange
    Order order = Order.builder()
        .productId(1L)
        .quantity(2)
        .unitPrice(10000)
        .build();
    Coupon coupon = new Coupon("SAVE10", 10); // 10% 할인

    // Act
    int finalPrice = pricingService.applyDiscount(order, coupon);

    // Assert
    assertThat(finalPrice).isEqualTo(18000); // 20000 - 10%
}
```

## 8. TDD 사이클 — Red, Green, Refactor

TDD(Test-Driven Development)는 구현 전에 테스트를 먼저 작성하는 개발 방법론이다. 짧은 피드백 루프를 통해 설계를 점진적으로 개선하며, 회귀 버그를 자동으로 방지하는 안전망을 구축한다.

세 단계 사이클은 다음과 같다:

- **Red**: 실패하는 테스트를 먼저 작성한다. 구현이 없으므로 컴파일 오류나 테스트 실패가 발생한다.
- **Green**: 테스트를 통과시키는 최소한의 코드만 작성한다. 이 단계에서는 깔끔한 코드보다 통과가 우선이다.
- **Refactor**: 테스트가 통과된 상태를 유지하면서 코드를 개선한다. 중복 제거, 명명 개선, 추상화가 이 단계에서 이루어진다.

```java
// Step 1 — Red: 실패하는 테스트 작성
@Test
void 이메일_형식이_올바르지_않으면_예외를_던진다() {
    UserService service = new UserService();
    // UserService가 아직 없으므로 컴파일 오류 발생 → Red
    assertThatThrownBy(() -> service.register("invalid-email", "password"))
        .isInstanceOf(InvalidEmailException.class);
}

// Step 2 — Green: 최소 구현으로 테스트 통과
class UserService {
    void register(String email, String password) {
        if (!email.contains("@")) {
            throw new InvalidEmailException(email);
        }
        // 최소한의 구현만 작성한다
    }
}

// Step 3 — Refactor: 구현 개선 (테스트는 여전히 통과)
class UserService {
    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$");

    void register(String email, String password) {
        if (!EMAIL_PATTERN.matcher(email).matches()) {
            throw new InvalidEmailException(email);
        }
    }
}
```

## 9. 테스트 네이밍 규칙

좋은 테스트 이름은 실패했을 때 무엇이 잘못되었는지를 이름만으로 알 수 있어야 한다. 네이밍에는 두 가지 접근이 주로 사용된다.

**한국어 스네이크 케이스** 방식은 한국어 팀에서 가독성이 높다:

```java
// 패턴: [조건]_[동작]_[결과]
void 재고가_없을때_주문하면_예외가_발생한다() { }
void 이메일이_중복될때_회원가입하면_실패한다() { }
void 빈_장바구니에서_결제하면_빈배열을_반환한다() { }
```

**영어 메서드명 + `@DisplayName`** 방식은 JUnit 리포트와 IDE 모두에서 유리하다:

```java
@Test
@DisplayName("재고가 없을 때 주문하면 OutOfStockException이 발생한다")
void placeOrder_whenNoStock_throwsOutOfStockException() { }
```

두 방식 모두 "상태 → 동작 → 결과" 구조를 유지하는 것이 핵심이다. 단순히 메서드명을 반복하는 `testPlaceOrder()` 방식은 실패 원인을 전혀 알려주지 않는다.

## 10. 좋은 테스트의 특성 — FIRST

*FIRST*는 좋은 단위 테스트가 갖춰야 할 다섯 가지 특성의 약자다. 이 원칙을 위반하는 테스트는 신뢰할 수 없는 안전망이 된다.

- **Fast**: 테스트는 빠르게 실행되어야 한다. 느린 테스트는 실행을 꺼리게 만들고, 피드백 루프를 느리게 한다. 단위 테스트는 밀리초 단위여야 한다.
- **Independent**: 각 테스트는 독립적으로 실행되어야 한다. 다른 테스트의 실행 순서나 결과에 의존하는 테스트는 간헐적 실패(flaky test)를 유발한다.
- **Repeatable**: 어떤 환경에서도 동일한 결과를 내야 한다. 시스템 시간, 랜덤값, 외부 API 의존은 테스트를 불안정하게 만든다.
- **Self-validating**: 테스트는 스스로 성공/실패를 판단해야 한다. 로그를 보고 사람이 판단해야 하는 테스트는 자동화의 이점을 잃는다.
- **Timely**: 테스트는 구현과 함께 작성되어야 한다. 오래된 코드에 나중에 테스트를 추가하면 테스트 가능성(testability)이 낮아 리팩토링이 필요한 경우가 많다.

```java
// FIRST 위반 예시 — Independent 위반
static int counter = 0;

@Test
void 첫번째_테스트() {
    counter++;
    assertEquals(1, counter); // 실행 순서에 따라 실패할 수 있다
}

@Test
void 두번째_테스트() {
    counter++;
    assertEquals(2, counter); // 첫번째_테스트에 의존한다
}

// FIRST 준수 예시 — 각 테스트가 독립적
@Test
void 주문_생성_성공() {
    // Arrange에서 모든 상태를 로컬로 초기화한다
    OrderService service = new OrderService(mock(InventoryRepository.class));
    // ...
}
```

## 11. 테스트 피라미드

*테스트 피라미드*는 Mike Cohn이 제안한 테스트 전략 모델이다. 아래로 갈수록 빠르고 저렴하며 많이 작성해야 하고, 위로 갈수록 느리고 비싸며 적게 유지해야 한다.

세 계층의 특성은 다음과 같다:

| 계층 | 대상 | 속도 | 비용 | 권장 비율 |
|------|------|------|------|----------|
| **Unit** | 단일 클래스/메서드 | 밀리초 | 낮음 | ~70% |
| **Integration** | 모듈 간 상호작용, DB, API | 초 단위 | 중간 | ~20% |
| **E2E** | 전체 시스템 사용자 시나리오 | 분 단위 | 높음 | ~10% |

단위 테스트는 비즈니스 로직의 경계 조건과 예외 경로를 빠짐없이 커버한다. 통합 테스트는 Repository-DB, HTTP Client-외부 API처럼 실제 연결이 필요한 지점만 집중 검증한다. E2E 테스트는 핵심 사용자 시나리오(주문 생성 → 결제 → 배송)만 선별하여 유지 비용을 낮춘다.

```java
// Unit Test — 순수 로직, 의존성 없음
@Test
void 할인율_10퍼센트_적용_시_금액_감소() {
    PricingService service = new PricingService();
    int result = service.applyDiscount(10000, 10);
    assertThat(result).isEqualTo(9000);
}

// Integration Test — Spring Context, 실제 DB 사용
@SpringBootTest
@Transactional
class OrderRepositoryIntegrationTest {

    @Autowired
    OrderRepository orderRepository;

    @Test
    void 저장_후_조회() {
        Order order = new Order(null, "PENDING", 5000);
        Order saved = orderRepository.save(order);

        Optional<Order> found = orderRepository.findById(saved.getId());
        assertThat(found).isPresent()
            .hasValueSatisfying(o -> assertThat(o.getStatus()).isEqualTo("PENDING"));
    }
}
```

피라미드를 역전시킨 *아이스크림 콘* 안티패턴(E2E 위주)은 느리고 불안정한 테스트 스위트를 만든다. E2E 테스트가 많아질수록 CI 시간이 늘어나고, 간헐적 실패(flaky test)가 증가하여 팀이 테스트를 신뢰하지 않게 된다.
