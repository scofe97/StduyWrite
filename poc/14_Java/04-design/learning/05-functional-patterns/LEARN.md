# 함수형 디자인 패턴

---

> 함수형 프로그래밍은 순수 함수와 불변 데이터를 기반으로 부수 효과를 최소화한다. Java 8 이후 람다와 스트림이 도입되면서 OOP와 함수형 패러다임을 함께 활용하는 것이 실무 표준이 되었다.

## 명령형 vs 함수형

명령형(imperative) 코드는 "어떻게 할 것인가"를 단계별로 기술하고, 함수형(functional) 코드는 "무엇을 원하는가"를 선언적으로 표현한다. 함수형 스타일은 코드의 의도를 더 명확하게 드러내고, 병렬화와 테스트가 쉬운 코드를 만든다.

```java
record Order(String status, double amount) {}

List<Order> orders = List.of(
    new Order("COMPLETED", 100.0)
    , new Order("PENDING", 50.0)
    , new Order("COMPLETED", 200.0)
);

// 명령형: how에 집중, 중간 상태가 드러난다
double totalImperative = 0;
for (Order order : orders) {
    if ("COMPLETED".equals(order.status())) {
        totalImperative += order.amount();
    }
}

// 함수형: what에 집중, 파이프라인으로 의도가 명확하다
double totalFunctional = orders.stream()
        .filter(o -> "COMPLETED".equals(o.status()))
        .mapToDouble(Order::amount)
        .sum();
```

## 순수 함수

**순수 함수(pure function)**는 같은 입력에 항상 같은 출력을 반환하고, 외부 상태를 변경하거나 읽지 않는다. 순수 함수는 테스트가 쉽고 병렬 실행이 안전하며, 결과를 캐싱(memoization)할 수 있다. 부수 효과(데이터베이스 쓰기, 로그 출력 등)는 시스템의 경계로 밀어내는 것이 함수형 설계의 핵심이다.

```java
// 순수 함수: 외부 상태에 의존하지 않는다
static double applyDiscount(double price, double rate) {
    return price * (1 - rate);
}

// 불순 함수: 외부 상태를 읽거나 변경한다
private double discountRate = 0.1; // 외부 상태
double applyDiscount(double price) {
    return price * (1 - discountRate); // 외부 상태에 의존 → 순수 함수 아님
}

// 불변 record: 상태 변경 없이 새 인스턴스를 반환한다
record Money(long cents, String currency) {
    Money add(Money other) {
        if (!currency.equals(other.currency)) throw new IllegalArgumentException();
        return new Money(cents + other.cents, currency);
    }

    Money withDiscount(double rate) {
        return new Money((long)(cents * (1 - rate)), currency);
    }
}
```

## 함수 합성

**함수 합성(function composition)**은 작은 함수들을 연결하여 복잡한 처리 파이프라인을 만드는 기법이다. `Function.andThen()`과 `Function.compose()`를 사용하면 재사용 가능한 처리 단계를 선언적으로 조합할 수 있다. `andThen`은 왼쪽에서 오른쪽으로, `compose`는 오른쪽에서 왼쪽으로 실행 순서가 정해진다.

```java
// 개별 변환 함수들
Function<String, String> trim      = String::trim;
Function<String, String> toUpper   = String::toUpperCase;
Function<String, String> addPrefix = s -> "PREFIX_" + s;

// andThen: trim → toUpper → addPrefix 순서
Function<String, String> pipeline = trim
        .andThen(toUpper)
        .andThen(addPrefix);

String result = pipeline.apply("  hello world  "); // "PREFIX_HELLO WORLD"

// 실무 예: Predicate 합성
Predicate<String> notEmpty  = s -> !s.isEmpty();
Predicate<String> notTooLong = s -> s.length() <= 100;
Predicate<String> isValid   = notEmpty.and(notTooLong);

List<String> valid = inputs.stream()
        .filter(isValid)
        .toList();
```

## 커링

**커링(currying)**은 여러 인자를 받는 함수를 단일 인자를 받는 함수의 연쇄로 변환한다. 부분 적용(partial application)으로 특정 인자를 미리 고정한 특화 함수를 만들 수 있어 코드 재사용성이 높아진다. Java는 커링을 언어 차원에서 지원하지 않지만, `Function`을 반환하는 함수로 표현할 수 있다.

```java
// 커링: (a, b) -> result 를 a -> (b -> result) 로 변환
Function<Double, Function<Double, Double>> curriedDiscount =
        rate -> price -> price * (1 - rate);

// 부분 적용: rate를 미리 고정
Function<Double, Double> vipDiscount    = curriedDiscount.apply(0.2);
Function<Double, Double> memberDiscount = curriedDiscount.apply(0.1);

double vipPrice    = vipDiscount.apply(10000.0);    // 8000.0
double memberPrice = memberDiscount.apply(10000.0); // 9000.0

// 실무 예: 로거 팩토리
Function<String, Consumer<String>> logger =
        level -> message -> System.out.println("[" + level + "] " + message);

Consumer<String> infoLog  = logger.apply("INFO");
Consumer<String> errorLog = logger.apply("ERROR");

infoLog.accept("Server started");    // [INFO] Server started
errorLog.accept("Connection failed"); // [ERROR] Connection failed
```

## Optional as Monad

**Optional**은 값이 있거나 없을 수 있는 컨테이너로, `null`을 명시적으로 다루게 한다. `map()`, `flatMap()`, `filter()`를 통해 모나드 패턴처럼 체이닝할 수 있으며, 중간에 `null`이 발생해도 파이프라인이 안전하게 흐른다. `isPresent()`로 값을 확인하고 `get()`하는 방식은 Optional의 의도에 맞지 않으며, 변환 체이닝을 활용하는 것이 올바른 사용법이다.

```java
record User(String name, String email) {}
record Order(Long id, String userId) {}

// null 방어 코드 방식 (나쁜 예)
String email = null;
User user = userRepo.findById(userId);
if (user != null) {
    email = user.email();
}

// Optional 체이닝 방식 (좋은 예)
Optional<String> email = userRepo.findById(userId)
        .map(User::email)
        .filter(e -> e.contains("@"));

// flatMap: Optional을 반환하는 메서드 체이닝
Optional<Order> latestOrder = userRepo.findById(userId)    // Optional<User>
        .flatMap(user -> orderRepo.findLatest(user.name())) // Optional<Order>
        .filter(order -> order.id() != null);

// 최종 처리
String result = latestOrder
        .map(o -> "Order #" + o.id())
        .orElse("주문 없음");
```

## GoF 패턴의 함수형 대안

Java 21에서 람다와 `sealed interface`를 활용하면 GoF 패턴을 더 간결하게 표현할 수 있다. 별도 클래스 없이 람다로 전략을 주입하거나, 데코레이터를 함수 합성으로 표현하면 코드량이 크게 줄어든다.

```java
// Strategy → @FunctionalInterface + 람다
@FunctionalInterface
interface PricingStrategy {
    double apply(double basePrice);
}

PricingStrategy vip    = price -> price * 0.8;
PricingStrategy member = price -> price * 0.9;
PricingStrategy bulk   = price -> price > 10000 ? price * 0.85 : price;

// Decorator → Function.andThen()으로 합성
Function<String, String> sanitize = String::trim;
Function<String, String> validate = s -> {
    if (s.isEmpty()) throw new IllegalArgumentException("blank input");
    return s;
};
Function<String, String> normalize = String::toLowerCase;

Function<String, String> processInput = sanitize
        .andThen(validate)
        .andThen(normalize);

// Command → Runnable / Supplier 람다
Runnable saveOrder   = () -> orderRepo.save(order);
Runnable sendEmail   = () -> emailService.send(order.email());
Runnable fullProcess = () -> { saveOrder.run(); sendEmail.run(); };

// Observer → Consumer 목록
List<Consumer<Order>> listeners = new ArrayList<>();
listeners.add(order -> emailService.sendConfirmation(order));
listeners.add(order -> inventoryService.reserve(order));

// 발행
listeners.forEach(l -> l.accept(newOrder));
```

| GoF 패턴 | 함수형 대안 | 절감 효과 |
|---------|-----------|---------|
| Strategy | `@FunctionalInterface` + 람다 | 구현 클래스 제거 |
| Decorator | `Function.andThen()` 합성 | 추상 클래스 제거 |
| Command | `Runnable` / `Supplier` 람다 | 커맨드 클래스 제거 |
| Observer | `Consumer<T>` 목록 | 리스너 인터페이스 단순화 |
| Factory | 정적 팩토리 메서드 + `switch` 표현식 | 팩토리 클래스 제거 |
