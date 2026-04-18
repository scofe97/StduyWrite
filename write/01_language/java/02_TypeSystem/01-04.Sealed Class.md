# Sealed Class
---
> 상속 계층을 코드로 닫는다. Java 17부터 `sealed` 키워드로 어떤 클래스가 특정 타입을 확장할 수 있는지 컴파일 타임에 선언한다.

## 1. 왜 Sealed Class가 필요한가

Java의 기존 상속 모델은 `final`(확장 불가)과 `public`(모두 확장 가능) 사이의 중간 지점이 없었다. 라이브러리 설계자가 특정 클래스 계층을 의도한 타입으로만 닫고 싶어도, `package-private`을 쓰는 것 외에 마땅한 수단이 없었다. Sealed Class는 허용할 하위 타입을 명시적으로 열거함으로써 이 공백을 채운다.

컴파일러는 `sealed` 계층 전체를 알고 있으므로 `switch` 표현식에서 모든 경우를 검사(exhaustiveness check)할 수 있다. Pattern Matching과 결합하면 if-else 분기 없이 타입별 처리를 안전하게 작성할 수 있다.

## 2. 기본 문법

`sealed` 클래스는 `permits` 절에 허용할 직접 하위 타입을 나열한다:

```java
public sealed class Shape permits Circle, Rectangle, Triangle {
    public abstract double area();
}
```

`permits`에 나열된 각 하위 클래스는 반드시 세 가지 한정자 중 하나를 선택해야 한다:

- `final` — 더 이상 확장할 수 없다. 계층의 말단 노드다.
- `sealed` — 다시 하위 타입을 허용한다. 계층을 더 깊게 제어한다.
- `non-sealed` — 봉인을 해제하여 임의 클래스가 확장할 수 있다.

```java
public final class Circle extends Shape {
    private final double radius;
    public Circle(double radius) { this.radius = radius; }

    @Override
    public double area() { return Math.PI * radius * radius; }
}

public final class Rectangle extends Shape {
    private final double width, height;
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() { return width * height; }
}

public non-sealed class Triangle extends Shape {
    // 외부 라이브러리가 Triangle을 확장할 수 있도록 열어 둔다
    @Override
    public double area() { return 0; } // 생략
}
```

인터페이스도 동일한 문법을 지원한다:

```java
public sealed interface Expr permits Num, Add, Mul {}
public record Num(int value) implements Expr {}
public record Add(Expr left, Expr right) implements Expr {}
public record Mul(Expr left, Expr right) implements Expr {}
```

## 3. 컴파일 타임 제약

Sealed Class가 강제하는 규칙은 네 가지다:

- `permits`에 열거된 클래스는 반드시 같은 패키지(또는 같은 모듈) 안에 있어야 한다.
- `permits`에 나열되지 않은 외부 클래스는 `sealed` 타입을 확장할 수 없다.
- 하위 클래스는 `final`, `sealed`, `non-sealed` 중 하나를 반드시 명시해야 한다.
- 같은 파일 안에 모든 하위 타입이 있으면 `permits` 절을 생략할 수 있다(컴파일러가 추론).

## 4. Pattern Matching과의 시너지

Java 21에서 `switch` 표현식이 타입 패턴을 지원하면서 Sealed Class와의 시너지가 완성됐다. 컴파일러는 `sealed` 계층의 모든 경우를 파악하므로, `switch`가 모든 타입을 처리하지 않으면 컴파일 오류를 낸다:

```java
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    case Triangle t  -> computeTriangleArea(t);
    // default 불필요 — 컴파일러가 exhaustiveness를 보장한다
};
```

`Triangle`이 `non-sealed`이므로 컴파일러는 Triangle의 하위 타입을 알 수 없다. 이 경우 `default` 또는 `case Triangle t` 패턴이 남은 경우를 모두 처리해야 한다.

Guarded pattern으로 세분화도 가능하다:

```java
String describe = switch (shape) {
    case Circle c when c.radius() > 10 -> "큰 원";
    case Circle c                       -> "작은 원";
    case Rectangle r                    -> "직사각형";
    case Triangle t                     -> "삼각형";
};
```

## 5. 실무 활용

### 5-1. 도메인 모델링 — 결제 수단

결제 수단은 종류가 고정된 대표적인 예다. 외부에서 임의로 새 결제 수단을 추가하면 안 된다:

```java
public sealed interface PaymentMethod
        permits CreditCard, BankTransfer, Cryptocurrency {}

public record CreditCard(String number, YearMonth expiry) implements PaymentMethod {}
public record BankTransfer(String accountNo, String bankCode) implements PaymentMethod {}
public record Cryptocurrency(String walletAddress, String coin) implements PaymentMethod {}
```

처리 로직은 `switch`로 안전하게 분기한다:

```java
public BigDecimal calculateFee(PaymentMethod method) {
    return switch (method) {
        case CreditCard cc          -> cc.amount().multiply(new BigDecimal("0.015"));
        case BankTransfer bt        -> BigDecimal.ZERO;
        case Cryptocurrency crypto  -> crypto.amount().multiply(new BigDecimal("0.01"));
    };
}
```

새 결제 수단을 추가하면 `calculateFee`의 `switch`가 즉시 컴파일 오류를 낸다. 처리 누락이 런타임이 아닌 빌드 단계에서 발견된다.

### 5-2. 상태 머신

주문 상태 전이처럼 상태 집합이 고정된 경우에도 유용하다:

```java
public sealed interface OrderStatus
        permits Placed, Confirmed, Shipped, Delivered, Cancelled {}

public record Placed(LocalDateTime placedAt) implements OrderStatus {}
public record Confirmed(LocalDateTime confirmedAt) implements OrderStatus {}
public record Shipped(String trackingNo) implements OrderStatus {}
public record Delivered(LocalDateTime deliveredAt) implements OrderStatus {}
public record Cancelled(String reason) implements OrderStatus {}
```

각 상태가 고유한 데이터를 가질 수 있다는 점이 enum과의 핵심 차이다.

## 6. enum과의 비교

| 구분 | Sealed Class/Interface | enum |
|------|------------------------|------|
| 상태 보유 | 인스턴스마다 다른 데이터 가능 | 상수당 동일한 구조 |
| 메서드 정의 | 하위 타입별로 독립 구현 | 상수별 메서드 오버라이드 가능 |
| 확장성 | `permits`로 폐쇄적 확장 | 확장 불가(상수 추가만 가능) |
| 인스턴스 수 | 제한 없음 | 상수당 싱글톤 |
| Pattern Matching | `switch` exhaustiveness 완전 지원 | `switch`에서 사용 가능 |
| null 안전성 | 별도 처리 필요 | 내재적으로 null이 아닌 상수 |

**선택 기준**: 상수별로 구조가 다른 데이터를 담아야 한다면 Sealed Class, 동일한 구조의 유한 집합을 표현한다면 enum이 적합하다.

## 7. Record와의 조합

Java 16부터 `record`를 Sealed Interface의 구현체로 쓰는 패턴이 관용적이다. `record`는 `final`이므로 별도로 `final`을 명시하지 않아도 된다:

```java
public sealed interface Result<T> permits Result.Ok, Result.Err {
    record Ok<T>(T value) implements Result<T> {}
    record Err<T>(String message, Throwable cause) implements Result<T> {}
}
```

호출부는 `switch`로 성공/실패를 구분하고, 컴파일러가 두 경우를 모두 처리했는지 검증한다:

```java
Result<User> result = userService.findById(id);
String message = switch (result) {
    case Result.Ok<User> ok   -> "Found: " + ok.value().name();
    case Result.Err<User> err -> "Error: " + err.message();
};
```
