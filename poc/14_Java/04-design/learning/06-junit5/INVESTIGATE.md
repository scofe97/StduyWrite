# JUnit 5 기초: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. @Nested 테스트의 구조적 장점과 남용 경계는 어디인가?

### 왜 이 질문이 중요한가

`@Nested`는 테스트 클래스를 계층적으로 구조화하는 강력한 도구지만, 잘못 사용하면 테스트 코드가 프로덕션 코드보다 복잡해진다. 장점과 한계를 함께 이해해야 효과적으로 활용할 수 있다.

### 답변

`@Nested`의 구조적 장점은 **Given 조건별 테스트 그룹화**다. 동일한 대상에 대해 여러 시나리오를 테스트할 때, 조건(상태)을 외부 클래스에 설정하고 그 조건 아래 세부 케이스를 내부 클래스에 담으면 `@BeforeEach`를 계층적으로 공유할 수 있다. 테스트 이름도 계층 구조로 읽히므로 IDE에서 가독성이 높아진다.

```java
@DisplayName("OrderService")
class OrderServiceTest {

    OrderService sut;
    Order order;

    @BeforeEach
    void setUp() {
        sut = new OrderService(/* mocks */);
    }

    @Nested
    @DisplayName("주문이 PENDING 상태일 때")
    class WhenOrderIsPending {

        @BeforeEach
        void setUp() {
            order = new Order(Status.PENDING); // 외부 조건 설정
        }

        @Test
        @DisplayName("confirm()을 호출하면 CONFIRMED 상태가 된다")
        void confirmChangesStatusToConfirmed() {
            sut.confirm(order);
            assertThat(order.status()).isEqualTo(Status.CONFIRMED);
        }

        @Test
        @DisplayName("cancel()을 호출하면 CANCELLED 상태가 된다")
        void cancelChangesStatusToCancelled() {
            sut.cancel(order);
            assertThat(order.status()).isEqualTo(Status.CANCELLED);
        }
    }

    @Nested
    @DisplayName("주문이 CONFIRMED 상태일 때")
    class WhenOrderIsConfirmed {

        @BeforeEach
        void setUp() {
            order = new Order(Status.CONFIRMED);
        }

        @Test
        @DisplayName("confirm()을 다시 호출하면 예외가 발생한다")
        void confirmThrowsException() {
            assertThatThrownBy(() -> sut.confirm(order))
                    .isInstanceOf(IllegalStateException.class);
        }
    }
}
```

**남용 경계**는 세 가지로 정리할 수 있다. 첫째, 중첩 깊이가 3단계를 넘어가면 `@BeforeEach`의 실행 순서를 추적하기 어려워진다. 둘째, 조건이 아닌 단순 기능별 그룹화에 `@Nested`를 쓰면 `@Tag`나 `@DisplayName` 수준으로 충분한 경우에 불필요한 클래스가 늘어난다. 셋째, 내부 클래스가 외부 클래스의 상태를 변경하면 테스트 간 격리가 깨질 수 있다. `@Nested` 클래스는 외부 클래스 인스턴스를 공유하므로 상태를 읽기만 해야 한다.

---

## Q2. 파라미터화 테스트로 테스트 커버리지를 극대화하는 전략은 무엇인가?

### 왜 이 질문이 중요한가

파라미터화 테스트는 동일한 로직을 여러 입력 값으로 검증하는 효율적인 방법이지만, 잘못 사용하면 테스트의 의도가 불명확해지고 실패 원인을 파악하기 어려워진다.

### 답변

파라미터화 테스트의 핵심 전략은 **경계값 분석(Boundary Value Analysis)**과 **동치 분류(Equivalence Partitioning)**를 소스로 활용하는 것이다. 단순히 많은 값을 넣는 것이 아니라, 동작이 달라지는 경계와 대표 케이스를 선별해야 한다.

```java
@ParameterizedTest(name = "가격={0}, 수량={1} → 예상총액={2}")
@CsvSource({
        "100, 1, 100",   // 최소 수량
        "100, 10, 1000", // 일반 케이스
        "100, 0, 0",     // 경계값: 수량 0
        "0, 5, 0",       // 경계값: 가격 0
})
void calculateTotal(int price, int quantity, int expected) {
    assertThat(sut.calculateTotal(price, quantity)).isEqualTo(expected);
}

// 복잡한 객체는 @MethodSource 활용
@ParameterizedTest
@MethodSource("invalidOrderRequests")
void rejectsInvalidOrder(CreateOrderRequest request, String expectedErrorField) {
    var violations = validator.validate(request);
    assertThat(violations).anyMatch(v -> v.getPropertyPath().toString().equals(expectedErrorField));
}

static Stream<Arguments> invalidOrderRequests() {
    return Stream.of(
            Arguments.of(new CreateOrderRequest(null, "prod1", 1), "userId")
            , Arguments.of(new CreateOrderRequest("user1", null, 1), "productId")
            , Arguments.of(new CreateOrderRequest("user1", "prod1", 0), "quantity")
            , Arguments.of(new CreateOrderRequest("user1", "prod1", -1), "quantity")
    );
}
```

커버리지 극대화 전략은 네 가지다. 첫째, 경계값(0, -1, MAX_INT, null, 빈 문자열)을 반드시 포함한다. 둘째, 성공 케이스와 실패 케이스를 같은 파라미터 소스에 섞지 않고 분리한다. 셋째, `@DisplayName`과 `name` 속성으로 각 케이스의 의도를 명시한다. 넷째, 파라미터가 5개를 넘어가면 `@MethodSource`로 전환하고 케이스 생성 메서드에 주석으로 분류 근거를 남긴다.
