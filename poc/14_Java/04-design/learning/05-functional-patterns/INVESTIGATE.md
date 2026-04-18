# 함수형 디자인 패턴: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 모나드 패턴이 Java에서 제한적인 이유는 무엇인가?

### 왜 이 질문이 중요한가

Haskell이나 Scala에서 모나드는 언어 차원의 일급 시민이지만, Java에서는 `Optional`, `Stream`, `CompletableFuture`가 모나드적 동작을 제공하면서도 진정한 의미의 모나드가 아니다. 이 차이를 이해하면 Java에서 함수형 패턴의 경계와 실무 활용 범위를 정확히 파악할 수 있다.

### 답변

모나드는 세 가지 법칙(왼쪽 항등, 오른쪽 항등, 결합 법칙)을 만족하는 타입 구조다. Java에서 제한적인 이유는 언어와 타입 시스템 차원의 제약에서 비롯된다.

첫째, **제네릭 타입 시스템의 한계**다. 진정한 모나드 추상화는 `Monad<M>` 같은 고차 타입(higher-kinded type)이 필요하다. Java의 제네릭은 `List<T>`는 표현하지만 `M<T>` 형태의 타입 생성자를 타입 파라미터로 받는 것을 지원하지 않는다. 따라서 `Optional`, `Stream`, `CompletableFuture`를 하나의 `Monad` 인터페이스로 추상화할 수 없다.

```java
// Java에서 불가능한 패턴: 고차 타입 파라미터
interface Monad<M<_>, A> { // 문법 오류: Java는 이 표현을 지원하지 않는다
    <B> M<B> flatMap(Function<A, M<B>> f);
}

// 실제 Java에서 각 타입이 독립적으로 flatMap을 구현한다
Optional<String>          opt    = Optional.of("hello").flatMap(s -> Optional.of(s.trim()));
Stream<String>            stream = Stream.of("a", "b").flatMap(s -> Stream.of(s, s.toUpperCase()));
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "hi")
        .thenCompose(s -> CompletableFuture.completedFuture(s.toUpperCase()));
```

둘째, **`Optional`의 모나드 법칙 위반 사례**가 있다. `Optional.of(null)`은 `NullPointerException`을 던지는데, 순수 함수형 모나드라면 `null`도 감싸서 전파해야 한다. 이는 Java가 null-safety보다 빠른 실패를 선택한 설계 결정이다.

셋째, **검사 예외(checked exception)와의 충돌**이다. 람다 내부에서 검사 예외를 던지면 `Function`, `Consumer` 같은 표준 함수형 인터페이스를 그대로 사용할 수 없다. 함수형 합성 파이프라인 중간에 예외가 끼어들면 체이닝이 끊어진다.

```java
// 검사 예외가 있으면 람다를 직접 쓸 수 없다
List<String> paths = List.of("file1.txt", "file2.txt");

// 컴파일 오류: readFile이 IOException(검사 예외)을 던진다
paths.stream()
        .map(p -> readFile(p)) // IOException은 Function<String, String>에 맞지 않는다
        .toList();

// 우회: 예외를 런타임 예외로 감싸거나 Either 타입을 활용
paths.stream()
        .map(p -> {
            try { return readFile(p); }
            catch (IOException e) { throw new UncheckedIOException(e); }
        })
        .toList();
```

---

## Q2. 함수형 디자인이 OOP와 공존하는 실무 경계는 어디인가?

### 왜 이 질문이 중요한가

"모든 것을 함수형으로"라는 극단적 접근은 Java에서 오히려 코드를 읽기 어렵게 만든다. 반대로 "함수형은 학문적이라 실무에 안 맞는다"는 편견도 문제다. 어디서 함수형을 쓰고 어디서 OOP를 쓸지를 판단하는 기준이 중요하다.

### 답변

실무 경계를 정하는 핵심 질문은 **"이 코드에 부수 효과(side effect)가 있는가?"** 이다.

**함수형이 유리한 영역**은 변환(transformation)과 계산(computation)이다. 데이터를 가져와서 필터링하고 변환하는 파이프라인, 비즈니스 규칙 계산, 이벤트 변환이 여기에 해당한다. 순수 함수로 구성되므로 테스트가 쉽고 병렬화가 안전하다.

```java
// 함수형이 유리: 순수 변환 파이프라인
BigDecimal totalRevenue = orders.stream()
        .filter(o -> o.status() == COMPLETED)
        .filter(o -> o.createdAt().isAfter(lastMonth))
        .map(Order::amount)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
```

**OOP가 유리한 영역**은 상태 관리와 협력 모델이다. 엔티티, 애그리게이트, 서비스 계층의 오케스트레이션은 상태와 행동을 묶는 OOP의 강점이 발휘되는 영역이다.

```java
// OOP가 유리: 상태와 행동을 묶는 도메인 모델
class Order {
    private OrderStatus status;
    private final List<OrderItem> items;

    public void confirm() {
        if (status != PENDING) throw new IllegalStateException();
        this.status = CONFIRMED;
        // 도메인 이벤트 발행 등 상태 전이 로직
    }
}
```

실무 아키텍처에서 자주 쓰이는 경계는 **"도메인 모델은 OOP, 유스케이스 내 데이터 처리는 함수형"**이다. 스프링 애플리케이션에서 `@Service`의 오케스트레이션 코드는 OOP로, 그 안에서 컬렉션을 다루는 코드는 스트림 API로 작성하는 것이 전형적인 공존 패턴이다.

| 영역 | 권장 스타일 | 이유 |
|------|-----------|------|
| 도메인 엔티티 | OOP | 상태 전이, 불변식 보호 |
| 비즈니스 규칙 계산 | 함수형 | 순수 함수, 테스트 용이 |
| 컬렉션 처리 | Stream API | 선언적, 파이프라인 합성 |
| 서비스 오케스트레이션 | OOP + 일부 함수형 | 의존성 관리는 OOP, 변환은 함수형 |
| I/O, 부수 효과 | OOP (명확한 경계) | 테스트 격리를 위해 인터페이스로 추상화 |
