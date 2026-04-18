# AssertJ와 TDD: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. TDD의 Red-Green-Refactor가 실무에서 깨지는 이유와 대응은 무엇인가?

### 왜 이 질문이 중요한가

TDD는 이론적으로 명확하지만 실무에서 지속하기 어렵다는 의견이 많다. "TDD를 해봤는데 잘 안 됐어요"라는 경험이 생기는 구체적인 원인을 파악해야 실질적인 대응 전략을 세울 수 있다.

### 답변

TDD의 Red-Green-Refactor 사이클이 실무에서 깨지는 원인은 다섯 가지로 나뉜다.

**첫째, 테스트 작성 비용이 구현 비용을 초과하는 경우**다. UI 컴포넌트, 외부 API 통합 코드, 데이터베이스 스키마처럼 초안이 자주 바뀌는 영역에서는 테스트를 먼저 작성하면 구현보다 테스트 수정에 더 많은 시간을 쓰게 된다.

**둘째, 도메인 지식이 부족한 상태에서 시작하는 경우**다. 무엇을 만들지 명확하지 않을 때 테스트를 먼저 쓰면 틀린 명세를 테스트로 굳혀버리는 역효과가 생긴다. 이 경우 스파이크(spike) 구현으로 도메인을 탐색한 뒤 TDD를 시작하는 것이 낫다.

**셋째, 레거시 코드와 혼재하는 경우**다. 테스트 없는 기존 코드에 새 기능을 TDD로 추가하면, 의존하는 레거시 코드가 테스트하기 어렵게 설계되어 있어 Mock 설정에 대부분의 시간을 쓰게 된다.

**넷째, 팀 전체가 TDD를 동의하지 않은 경우**다. 개인이 TDD를 실천해도 PR 리뷰에서 "테스트를 왜 먼저 썼냐"는 피드백을 받거나, 다른 사람이 구현을 먼저 작성하면 사이클이 깨진다.

**다섯째, Refactor 단계를 건너뛰는 습관**이다. Green을 만든 후 바로 다음 Red로 넘어가면 기술 부채가 누적된다. 리팩토링은 테스트가 통과한 직후, 코드가 생생할 때 해야 한다.

대응 전략은 TDD 적용 범위를 **"테스트하기 쉬운 코어 도메인 로직"**으로 한정하는 것이다. 외부 시스템 통합, UI, 탐색적 구현은 TDD보다 구현 후 테스트 추가가 현실적이다.

```java
// TDD가 잘 맞는 영역: 순수 비즈니스 로직
// Red: 먼저 실패하는 테스트를 작성한다
@Test
void discountedPriceCannotBeLowerThanCost() {
    var product = new Product(cost: 5000, price: 10000);
    assertThatThrownBy(() -> product.applyDiscount(0.6)) // 60% 할인 → 4000 < 원가
            .isInstanceOf(InvalidDiscountException.class);
}

// Green: 최소한의 코드로 통과시킨다
public void applyDiscount(double rate) {
    long discounted = (long)(price * (1 - rate));
    if (discounted < cost) throw new InvalidDiscountException();
    this.price = discounted;
}

// Refactor: 중복 제거, 네이밍 개선, 불변식 추출
```

---

## Q2. 테스트 피라미드를 지키기 어려운 상황과 현실적인 대응은 무엇인가?

### 왜 이 질문이 중요한가

테스트 피라미드(단위 > 통합 > E2E)는 이상적인 비율을 제시하지만, 많은 팀이 통합 테스트나 E2E 테스트에 의존하는 역피라미드(ice cream cone) 구조를 갖게 된다. 그 이유와 현실적 대응을 이해하면 팀의 테스트 전략을 개선할 수 있다.

### 답변

테스트 피라미드가 현실에서 무너지는 대표적인 상황은 세 가지다.

**첫째, 마이크로서비스 환경**이다. 서비스 간 계약이 핵심인 환경에서 단위 테스트만으로는 통합 지점의 오류를 잡을 수 없다. 계약 테스트(Consumer-Driven Contract Testing, 예: Pact)를 통합 테스트의 대안으로 사용하면 서비스 간 계약을 단위 테스트 속도로 검증할 수 있다.

**둘째, 복잡한 DB 쿼리가 핵심인 시스템**이다. JPA의 N+1 문제, 복잡한 조인, 인덱스 힌트처럼 실제 DB 없이 검증할 수 없는 로직은 단위 테스트로 커버할 수 없다. `@DataJpaTest`와 Testcontainers를 사용하면 실제 DB에 가까운 환경으로 빠른 슬라이스 테스트가 가능하다.

**셋째, 레거시 코드 커버리지 확보가 급선무인 경우**다. 단위 테스트를 먼저 만들기 위해 레거시 코드를 리팩토링해야 하는데, 안전망 없이 리팩토링하기 어렵다. 이 경우 E2E나 통합 테스트를 먼저 추가하여 안전망을 확보한 뒤, 점진적으로 단위 테스트로 대체하는 "인버티드 피라미드 탈출 전략"이 현실적이다.

```java
// Testcontainers로 실제 DB와 가까운 슬라이스 테스트
@DataJpaTest
@AutoConfigureTestDatabase(replace = NONE)
@Testcontainers
class OrderRepositoryTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url", postgres::getJdbcUrl);
        r.add("spring.datasource.username", postgres::getUsername);
        r.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired OrderRepository repo;

    @Test
    void findByStatusOrderByCreatedAtDesc_returnsInCorrectOrder() {
        // 실제 PostgreSQL에서 정렬 동작을 검증한다
        var orders = repo.findByStatusOrderByCreatedAtDesc(COMPLETED);
        assertThat(orders).isSortedAccordingTo(
                Comparator.comparing(Order::createdAt).reversed()
        );
    }
}
```

AssertJ를 활용하면 복잡한 검증도 읽기 쉽게 표현할 수 있다.

```java
// 컬렉션 검증: 조건을 만족하는 원소가 정확히 N개인지
assertThat(orders)
        .filteredOn(o -> o.status() == COMPLETED)
        .hasSize(3)
        .extracting(Order::amount)
        .allSatisfy(amount -> assertThat(amount).isPositive());

// 예외 검증: 메시지와 타입을 함께
assertThatThrownBy(() -> sut.confirm(cancelledOrder))
        .isInstanceOf(IllegalStateException.class)
        .hasMessageContaining("CANCELLED");

// 소프트 어서션: 첫 번째 실패에서 중단하지 않고 전체 검증
SoftAssertions.assertSoftly(softly -> {
    softly.assertThat(result.userId()).isEqualTo("user1");
    softly.assertThat(result.status()).isEqualTo(CONFIRMED);
    softly.assertThat(result.amount()).isEqualByComparingTo("10000");
});
```
