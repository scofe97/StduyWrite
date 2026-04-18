# 함수형 인터페이스
---
> 람다 표현식은 반드시 함수형 인터페이스(Functional Interface)라는 그릇에 담긴다. 표준 함수형 인터페이스를 숙지하면 매번 인터페이스를 직접 만들 필요 없이, 동작 파라미터화(Behavioral Parameterization) 패턴을 바로 적용할 수 있다.

## 1. 함수형 인터페이스란

함수형 인터페이스는 **추상 메서드가 정확히 하나**인 인터페이스다. SAM(Single Abstract Method) 인터페이스라고도 부른다. `default` 메서드나 `static` 메서드가 여럿 있어도 추상 메서드가 하나면 함수형 인터페이스로 인정된다:

```java
@FunctionalInterface
interface CustomInterface<T> {
    T myCall(); // 추상 메서드는 하나만

    default void printDefault() {
        System.out.println("Hello Default");
    }

    static void printStatic() {
        System.out.println("Hello Static");
    }
}
```

`@FunctionalInterface` 어노테이션은 세 가지 역할을 한다. 첫째, 이 인터페이스가 람다용으로 설계되었음을 코드에 명시한다. 둘째, 추상 메서드가 두 개 이상이면 컴파일 에러를 발생시켜 실수를 조기에 잡아준다. 셋째, 유지보수 과정에서 누군가 추상 메서드를 추가하는 것을 방지한다.

람다는 클래스나 추상 클래스에는 대입할 수 없고, 오직 함수형 인터페이스에만 대입할 수 있다. 또한 시그니처(매개변수 타입과 반환 타입)가 같더라도 서로 다른 인터페이스 타입 간에는 상호 대입이 불가능하다. 타입이 먼저 결정되고 나면 이후에는 다른 인터페이스 타입으로 변환할 수 없다.

## 2. 표준 함수형 인터페이스 비교

`java.util.function` 패키지는 자주 쓰이는 함수형 인터페이스를 미리 정의해 둔다. 대부분의 상황에서 직접 인터페이스를 만들 필요가 없다:

| 인터페이스 | 추상 메서드 | 입력 | 출력 | 주요 용도 |
|------------|-------------|------|------|-----------|
| `Function<T, R>` | `R apply(T t)` | T | R | 변환, 매핑 |
| `Consumer<T>` | `void accept(T t)` | T | 없음 | 출력, 저장 등 부수 효과 |
| `Supplier<T>` | `T get()` | 없음 | T | 객체 생성, 지연 초기화 |
| `Predicate<T>` | `boolean test(T t)` | T | boolean | 필터링, 조건 검사 |
| `UnaryOperator<T>` | `T apply(T t)` | T | T (동일 타입) | 단항 변환 연산 |
| `BinaryOperator<T>` | `T apply(T t1, T t2)` | T, T | T (동일 타입) | 이항 결합 연산 |

```java
// Function: 문자열 길이를 반환
Function<String, Integer> length = String::length;
System.out.println(length.apply("hello")); // 5

// Consumer: 출력이라는 부수 효과를 발생
Consumer<String> printer = System.out::println;
printer.accept("Hello, Consumer!");

// Supplier: 호출 시점에 값을 생성
Supplier<LocalDate> today = LocalDate::now;
System.out.println(today.get());

// Predicate: 조건 검사
Predicate<String> nonEmpty = s -> !s.isEmpty();
System.out.println(nonEmpty.test("hello")); // true

// UnaryOperator: 같은 타입으로 변환
UnaryOperator<String> toUpper = String::toUpperCase;
System.out.println(toUpper.apply("hello")); // HELLO

// BinaryOperator: 두 값을 하나로 결합
BinaryOperator<Integer> sum = Integer::sum;
System.out.println(sum.apply(5, 7)); // 12
```

`UnaryOperator<T>`와 `BinaryOperator<T>`를 별도로 제공하는 이유는 의도의 명시성 때문이다. `Function<Integer, Integer>`만 봐서는 같은 타입 간 변환인지 알 수 없지만, `UnaryOperator<Integer>`는 "입출력 타입이 동일한 단항 연산"임을 한눈에 드러낸다. 두 개 입력이 필요할 때는 `BiFunction<T, U, R>`, `BiConsumer<T, U>`, `BiPredicate<T, U>` 변형을 사용한다.

오토박싱/언박싱 비용이 우려될 때는 `IntFunction<R>`, `ToIntFunction<T>`, `IntUnaryOperator` 같은 기본형 특화 인터페이스를 사용한다. 예를 들어 `Function<Integer, Integer>` 대신 `IntUnaryOperator`를 쓰면 `Integer` 박싱 객체 생성을 피할 수 있다.

## 3. 동작 파라미터화 패턴

동작 파라미터화(Behavioral Parameterization)는 "어떤 동작을 수행할지"를 메서드 외부에서 전달받는 설계 방식이다. 요구사항이 바뀌어도 메서드 시그니처를 유지하면서 동작만 교체할 수 있어 DRY(Do Not Repeat Yourself) 원칙을 지킬 수 있다.

사과 필터링 예제로 발전 과정을 살펴본다. 처음에는 녹색 사과만 필터링했다:

```java
public List<Apple> filterGreenApples(List<Apple> inventory) {
    List<Apple> result = new ArrayList<>();
    for (Apple apple : inventory) {
        if (GREEN.equals(apple.color())) {
            result.add(apple);
        }
    }
    return result;
}
```

빨간 사과도 필터링하려면 거의 동일한 메서드를 하나 더 만들어야 한다. 색을 파라미터로 뽑아내도, 무게 조건이 추가되면 또 반복된다. 근본 해결책은 동작 자체를 파라미터로 전달하는 것이다:

```java
// 자바 8 이전: Predicate 구현 클래스를 별도로 작성
public class AppleGreenColorPredicate implements ApplePredicate {
    @Override
    public boolean test(Apple apple) {
        return GREEN.equals(apple.color());
    }
}
filterApples(inventory, new AppleGreenColorPredicate());

// 자바 8 이후: 람다로 직접 전달
filterApples(inventory, apple -> GREEN.equals(apple.color()));
```

제네릭을 활용하면 Apple뿐 아니라 어떤 타입에도 적용할 수 있다:

```java
public static <T> List<T> filter(List<T> list, Predicate<T> p) {
    List<T> result = new ArrayList<>();
    for (T e : list) {
        if (p.test(e)) {
            result.add(e);
        }
    }
    return result;
}

List<Apple> redApples = filter(inventory, apple -> RED.equals(apple.color()));
List<Integer> evenNumbers = filter(numbers, i -> i % 2 == 0);
```

동작 파라미터화를 적용하면 "각 항목에 적용할 동작"과 "컬렉션을 순회하는 로직"이 분리된다. 순회 코드는 재사용되고, 동작만 교체하면 된다.

## 4. Predicate 조합

`Predicate<T>`는 `and`, `or`, `negate` 세 가지 디폴트 메서드로 조건을 조합한다. 복잡한 조건도 별도 메서드 없이 선언적으로 표현할 수 있다:

```java
Predicate<Apple> redApple = apple -> RED.equals(apple.getColor());

// negate: 조건 반전 — 빨간 사과가 아닌 것
Predicate<Apple> notRedApple = redApple.negate();

// and: 두 조건 모두 만족 — 빨갛고 무거운 사과
Predicate<Apple> redAndHeavy = redApple.and(apple -> apple.getWeight() > 150);

// or: 둘 중 하나 만족 — 빨갛고 무겁거나 녹색인 사과
Predicate<Apple> redHeavyOrGreen = redApple
        .and(apple -> apple.getWeight() > 150)
        .or(apple -> GREEN.equals(apple.getColor()));
```

`and`와 `or`는 단락 평가(Short-Circuit Evaluation)를 따른다. `and`는 첫 번째 조건이 `false`이면 두 번째를 평가하지 않고, `or`는 첫 번째 조건이 `true`이면 두 번째를 평가하지 않는다.

## 5. 함수 합성

`Function<T, R>`은 `andThen`과 `compose` 두 가지 메서드로 함수를 합성한다. 두 메서드의 차이는 실행 순서다:

```java
Function<Integer, Integer> f = x -> x + 1; // x에 1을 더한다
Function<Integer, Integer> g = x -> x * 2; // x에 2를 곱한다

// andThen: f 먼저, g 나중 → g(f(x))
Function<Integer, Integer> fThenG = f.andThen(g);
System.out.println(fThenG.apply(1)); // (1+1)*2 = 4

// compose: g 먼저, f 나중 → f(g(x))
Function<Integer, Integer> fOfG = f.compose(g);
System.out.println(fOfG.apply(1)); // (1*2)+1 = 3
```

`andThen`은 수학의 `g ∘ f` (f를 먼저 적용)에 해당하고, `compose`는 `f ∘ g` (g를 먼저 적용)에 해당한다. 데이터 변환 파이프라인을 구성할 때 `andThen`을 연속 호출하면 가독성 좋은 처리 흐름을 만들 수 있다.

`Comparator`도 `reversed()`와 `thenComparing()`을 제공하므로 정렬 기준을 유연하게 조합할 수 있다:

```java
inventory.sort(
    Comparator.comparing(Apple::getWeight)
              .reversed()
              .thenComparing(Apple::getCountry)
);
```

## 6. 직접 함수형 인터페이스를 만드는 경우

표준 함수형 인터페이스만으로 대부분의 상황을 처리할 수 있지만, 세 가지 경우에는 직접 만드는 것이 낫다.

- 자주 쓰이면서 인터페이스 이름 자체가 용도를 명확히 설명할 때 (`Comparator<T>` 처럼)
- 반드시 따라야 하는 계약(contract)이 있을 때 — 예를 들어 `equals` 규약처럼
- 유용한 `default` 메서드를 여러 개 제공해야 할 때

직접 만든 함수형 인터페이스에는 반드시 `@FunctionalInterface`를 붙인다. 자바 표준 라이브러리의 `Comparator`, `Runnable`, `Callable`도 모두 이 어노테이션을 달고 있다.
