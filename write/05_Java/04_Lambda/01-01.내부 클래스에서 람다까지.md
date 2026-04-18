# 내부 클래스에서 람다까지
---
> 자바는 클래스 안에 클래스를 중첩하는 방식으로 캡슐화를 발전시켜 왔다. 익명 클래스가 그 정점이었지만, 람다 표현식(Lambda Expression)이 등장하면서 동작을 전달하는 방식이 근본적으로 바뀌었다.

## 1. 중첩 클래스의 네 가지 종류

중첩 클래스(Nested Class)란 한 클래스 내부에 다른 클래스를 정의하는 방식이다. 논리적으로 연관된 클래스를 한 곳에 묶어 캡슐화를 강화하고, 불필요한 `public` 메서드 노출을 줄일 수 있다. 자바는 중첩 클래스를 네 가지로 분류한다.

- **정적 중첩 클래스(Static Nested Class)**: `static` 키워드로 선언하며, 외부 클래스 인스턴스와 독립적으로 존재한다.
- **내부 클래스(Inner Class)**: 외부 클래스의 인스턴스에 종속되며, 외부 클래스의 모든 멤버에 접근할 수 있다.
- **지역 클래스(Local Class)**: 특정 메서드 내부에서만 선언되고 사용된다.
- **익명 클래스(Anonymous Class)**: 이름 없이 선언과 동시에 인스턴스를 생성한다.

"중첩"과 "내부"는 의미가 다르다. 정적 중첩 클래스는 위치만 내부에 있을 뿐 외부 클래스에 소속되지 않는다. 반면 내부 클래스는 외부 클래스의 구성 요소로서 실질적으로 내부에 속한다.

## 2. 정적 중첩 클래스

정적 중첩 클래스는 외부 클래스의 `static` 멤버에만 접근할 수 있다. 인스턴스 변수에는 접근하지 못하므로, 외부 클래스와 논리적으로 연관되지만 독립적으로 동작해야 하는 헬퍼 클래스에 적합하다:

```java
public class Network {
    public void sendMessage(String text) {
        NetworkMessage networkMessage = new NetworkMessage(text);
        networkMessage.print();
    }

    private static class NetworkMessage {
        private String content;

        public NetworkMessage(String content) {
            this.content = content;
        }

        public void print() {
            System.out.println("content = " + content);
        }
    }
}
```

`NetworkMessage`는 `Network` 외부에서 사용할 이유가 없으므로, `private static`으로 선언해 접근 범위를 좁힌다.

## 3. 내부 클래스

내부 클래스는 외부 클래스의 인스턴스가 생성된 뒤에야 생성할 수 있다. 외부 클래스의 `private` 멤버에 직접 접근하므로, 불필요한 getter를 제거하고 캡슐화를 강화한다:

```java
public class Car {
    private String model;
    private int chargeLevel;
    private Engine engine;

    public Car(String model, int chargeLevel) {
        this.model = model;
        this.chargeLevel = chargeLevel;
        this.engine = new Engine();
    }

    public void start() {
        engine.start();
        System.out.println(model + " 시작 완료");
    }

    public class Engine {
        public void start() {
            System.out.println("충전 레벨 확인: " + chargeLevel);
            System.out.println(model + "의 엔진을 사용합니다.");
        }
    }
}
```

`Engine`이 `Car`의 내부 클래스가 되면, `chargeLevel`과 `model`에 직접 접근할 수 있어 getter 메서드가 필요 없어진다.

## 4. 지역 클래스와 변수 캡처

지역 클래스(Local Class)는 메서드 내부에서만 선언되고, 해당 메서드의 지역 변수에 접근할 수 있다. 한 가지 중요한 제약이 있는데, 접근하는 지역 변수는 반드시 *effectively final*이어야 한다. 즉, 한 번 할당된 후 값이 변경되지 않아야 한다.

```java
public Printer process(int paramVar) {
    int localVar = 1; // 스택에 존재하며, 메서드 종료 시 제거된다.

    class LocalPrinter implements Printer {
        @Override
        public void print() {
            // process() 종료 후에도 localVar에 접근 가능한 이유:
            // LocalPrinter 인스턴스가 localVar의 복사본을 내부에 보유하기 때문이다.
            System.out.println("localVar = " + localVar);
            System.out.println("paramVar = " + paramVar);
        }
    }

    return new LocalPrinter();
}
```

메서드가 반환되면 스택 프레임이 사라지지만, 지역 클래스의 인스턴스는 힙에 살아 있다. 자바는 이 문제를 **변수 캡처(Variable Capture)**로 해결한다. 지역 클래스 인스턴스 생성 시점에 지역 변수의 값을 복사해 내부 필드로 보관한다. 두 값이 달라지면 동기화 문제가 생기므로, 캡처된 변수는 수정이 금지된다.

## 5. 익명 클래스의 한계

익명 클래스는 지역 클래스에서 이름을 제거한 형태다. 선언과 인스턴스 생성이 동시에 이루어진다:

```java
Printer printer = new Printer() {
    @Override
    public void print() {
        System.out.println("익명 클래스 출력");
    }
};
```

내부적으로 자바는 이 클래스를 `OuterClass$1`처럼 바깥 클래스 이름에 `$`와 숫자를 붙여 명명한다. 익명 클래스는 단발성 구현체에 유용하지만, 두 가지 한계가 있다. 첫째, 메서드가 하나뿐인 인터페이스를 구현할 때조차 `new Interface() { @Override ... }` 라는 반복 코드가 필요하다. 둘째, `this`가 익명 클래스 자신을 가리키므로 외부 인스턴스를 참조하려면 `OuterClass.this` 처럼 명시해야 한다.

## 6. 람다 표현식 도입 배경

자바 8 이전에는 동작(Behavior)을 전달하려면 반드시 클래스와 인스턴스가 필요했다. 정렬 조건 하나를 바꾸려 해도 `Comparator` 구현 클래스를 따로 만들어야 했다. 람다 표현식은 이 문제를 해결하기 위해 설계되었다. 함수형 인터페이스(Functional Interface), 즉 추상 메서드가 하나뿐인 인터페이스를 구현하는 익명 함수를 간결한 문법으로 표현한다.

```java
// 익명 클래스 방식 (자바 7 이전)
Collections.sort(words, new Comparator<String>() {
    public int compare(String s1, String s2) {
        return Integer.compare(s1.length(), s2.length());
    }
});

// 람다 표현식 (자바 8 이후)
Collections.sort(words, (s1, s2) -> Integer.compare(s1.length(), s2.length()));
```

코드량이 절반 이하로 줄어들고, 핵심 로직인 `Integer.compare(...)` 부분이 훨씬 잘 드러난다.

## 7. 람다 기본 문법

람다 표현식의 구조는 `(파라미터) -> 본문`이다. 파라미터 타입은 컴파일러가 문맥에서 추론하므로 대부분 생략한다:

```java
// 파라미터 타입 명시
(String s) -> s.length()

// 타입 추론으로 생략
(s) -> s.length()

// 파라미터 1개일 때 괄호 생략 가능
s -> s.length()

// 본문이 여러 줄이면 중괄호와 return 필수
(int x, int y) -> {
    System.out.println("결과:");
    return x + y;
}

// 파라미터 없음
() -> 42
```

람다는 네 가지 특성을 갖는다. 이름이 없는 **익명** 함수이고, 특정 클래스에 종속되지 않는 **함수**다. 메서드 인수로 **전달**하거나 변수에 저장할 수 있으며, 익명 클래스보다 훨씬 **간결**하다.

익명 클래스와 중요한 차이가 하나 있다. 익명 클래스에서 `this`는 익명 클래스 자신을 가리키지만, 람다에서 `this`는 람다를 감싸는 외부 인스턴스를 가리킨다. 람다는 자신을 참조하는 방법이 없으므로, 재귀나 자기 참조가 필요한 경우에는 익명 클래스를 써야 한다.

## 8. 메서드 참조

메서드 참조(Method Reference)는 람다가 기존 메서드를 그대로 호출할 때 `클래스::메서드` 형식으로 더 간결하게 표현하는 문법이다. 네 가지 종류가 있다:

| 유형 | 문법 | 람다 동치 |
|------|------|-----------|
| 정적 메서드 참조 | `Integer::parseInt` | `s -> Integer.parseInt(s)` |
| 바운드 인스턴스 메서드 참조 | `list::contains` | `s -> list.contains(s)` |
| 언바운드 인스턴스 메서드 참조 | `String::toLowerCase` | `str -> str.toLowerCase()` |
| 생성자 참조 | `Apple::new` | `() -> new Apple()` |

바운드(Bound)와 언바운드(Unbound)의 차이는 수신 객체가 고정되어 있는지 여부다. 바운드는 `list`라는 특정 인스턴스가 이미 정해져 있고, 언바운드는 람다 실행 시 첫 번째 파라미터가 수신 객체가 된다.

```java
// 정적 메서드 참조
Function<String, Integer> parser = Integer::parseInt;
System.out.println(parser.apply("100")); // 100

// 언바운드 인스턴스 메서드 참조
Function<String, String> toLower = String::toLowerCase;
System.out.println(toLower.apply("HELLO")); // hello

// 생성자 참조
Supplier<TreeMap<String, Integer>> mapFactory = TreeMap::new;
TreeMap<String, Integer> map = mapFactory.get();
```

메서드 참조가 항상 더 좋은 것은 아니다. 파라미터 이름이 문맥을 설명해주는 경우에는 람다가 더 읽기 쉽다. `(order, item) -> order.addItem(item)` 처럼 인자 이름이 의미를 드러낼 때는 메서드 참조로 바꾸면 오히려 의도가 흐려진다.
