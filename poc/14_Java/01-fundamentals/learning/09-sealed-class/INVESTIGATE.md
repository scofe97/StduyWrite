# Sealed Class: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Sealed Class + Pattern Matching이 Visitor 패턴을 대체할 수 있는가?

### 왜 이 질문이 중요한가
Visitor 패턴은 타입 계층에 새 연산을 추가할 때 기존 클래스를 수정하지 않는 방법이다. Sealed Class와 Pattern Matching이 도입되면서 "Visitor가 필요 없어졌다"는 주장이 생겼는데, 이 주장의 범위와 한계를 이해해야 올바른 설계 결정을 내릴 수 있다.

### 답변

Visitor 패턴이 해결하는 문제는 타입 안전한 이중 디스패치(double dispatch)다. 도형 계층(`Circle`, `Rectangle`, `Triangle`)에 면적 계산, 둘레 계산, 렌더링 등 다양한 연산을 추가할 때, 각 연산을 별도 Visitor로 분리해서 도형 클래스를 수정하지 않고 확장한다. 단점은 보일러플레이트가 많고, 새 타입을 추가하면 모든 Visitor를 수정해야 한다는 점이다.

Sealed Class + Pattern Matching은 같은 문제를 훨씬 간결하게 해결한다.

```java
// Sealed 계층 정의
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double w, double h) implements Shape {}
record Triangle(double base, double height) implements Shape {}

// 연산을 switch 표현식으로 — Visitor 없이 타입 안전한 분기
double area(Shape shape) {
    return switch (shape) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.w() * r.h();
        case Triangle t  -> 0.5 * t.base() * t.height();
        // Sealed이므로 컴파일러가 모든 케이스 커버 여부를 검사
        // 새 타입이 추가되면 이 switch가 컴파일 에러를 냄 — 안전망
    };
}

double perimeter(Shape shape) {
    return switch (shape) {
        case Circle c    -> 2 * Math.PI * c.radius();
        case Rectangle r -> 2 * (r.w() + r.h());
        case Triangle t  -> throw new UnsupportedOperationException("needs sides");
    };
}
```

Sealed + Pattern Matching이 Visitor를 대체하기 어려운 경우는 두 가지다. 첫째, 타입 계층이 외부 라이브러리에 있어 `sealed`로 선언할 수 없는 경우다. 둘째, 연산이 매우 많고(수십 개) 각 연산이 별도 클래스로 캡슐화되어야 하는 경우다. 이때는 Visitor가 객체지향적 분리를 더 명확하게 표현한다.

결론적으로 Sealed Class + Pattern Matching은 내부 타입 계층에 대한 타입 안전 분기에서 Visitor를 대부분 대체할 수 있다. 컴파일러가 누락 케이스를 잡아주므로 안전성도 동일하고 코드는 훨씬 간결하다. 단, 외부 확장성이 핵심인 경우(새 타입 추가가 잦은 경우)에는 Visitor가 여전히 유용하다.

---

## Q2. enum vs Sealed Class 선택 기준

### 왜 이 질문이 중요한가
`enum`과 Sealed Class는 둘 다 "제한된 타입 집합"을 표현하지만 근본적으로 다른 도구다. "결제 상태를 enum으로 할까, Sealed Class로 할까"처럼 실무에서 자주 만나는 결정이다.

### 답변

`enum`의 핵심 특성은 상수 집합이다. 각 상수가 같은 타입이고 상태(필드)가 있을 수 있지만, 모든 상수가 동일한 구조를 가져야 한다. `PENDING`, `PROCESSING`, `COMPLETED` 같은 상태는 각각 다른 데이터를 가질 필요가 없으므로 enum이 자연스럽다.

Sealed Class의 핵심 특성은 서로 다른 구조를 가진 타입들의 닫힌 집합이다. 각 하위 타입이 서로 다른 필드를 가질 수 있다.

```java
// enum이 적합 — 모든 상수가 같은 구조, 추가 데이터 없거나 동일한 필드
enum OrderStatus {
    PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED;

    // 공통 필드는 enum에도 가능
    // 하지만 SHIPPED는 trackingNumber가 있고
    // CANCELLED는 reason이 있다면 → Sealed Class 고려
}

// Sealed Class가 적합 — 각 타입이 다른 데이터를 가짐
sealed interface PaymentResult permits Success, Failure, Pending {}
record Success(String transactionId, Instant at) implements PaymentResult {}
record Failure(String errorCode, String message) implements PaymentResult {}
record Pending(String referenceId, Duration timeout) implements PaymentResult {}

// 각 케이스가 완전히 다른 데이터 — enum으로는 표현이 어색
PaymentResult result = processPayment(order);
String msg = switch (result) {
    case Success s  -> "완료: " + s.transactionId();
    case Failure f  -> "실패: " + f.message();
    case Pending p  -> "대기 중, " + p.timeout().toMinutes() + "분 후 확인";
};
```

선택 기준을 정리하면 이렇다. 같은 구조의 상수 집합이고 `values()`, `ordinal()`, `name()` 같은 enum 기능이 필요하면 enum을 선택한다. 각 케이스가 서로 다른 데이터를 가지거나, 케이스별로 다른 타입 계층 구조가 필요하거나, 각 케이스에 대해 Pattern Matching을 활용하고 싶다면 Sealed Class를 선택한다. 실무에서는 처음에 enum으로 시작하고, 케이스별로 다른 데이터가 필요해지는 시점에 Sealed Class로 리팩토링하는 패턴이 자연스럽다.
