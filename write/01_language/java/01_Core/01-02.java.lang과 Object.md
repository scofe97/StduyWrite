# java.lang과 Object
---
> `java.lang`은 자바가 자동으로 임포트하는 핵심 패키지로, 그 중심에는 모든 클래스의 조상인 `Object`가 있다. `Object`의 메서드를 올바르게 재정의하는 일은 컬렉션과 직렬화가 제대로 동작하기 위한 전제 조건이다.

## 1. java.lang 패키지

`java.lang`은 모든 자바 애플리케이션에 자동으로 `import`되는 유일한 패키지다. 별도로 `import`하지 않아도 `String`, `Integer`, `Math`, `System`, `Thread` 등을 바로 사용할 수 있는 이유가 여기에 있다. 대표 클래스를 기능별로 나누면 다음과 같다.

| 분류 | 주요 클래스 |
|------|------------|
| 최상위 | `Object` |
| 문자열 | `String`, `StringBuilder`, `StringBuffer` |
| 수치 래퍼 | `Integer`, `Long`, `Double`, `Boolean` 등 |
| 수학/시스템 | `Math`, `System`, `Runtime` |
| 스레드 | `Thread`, `Runnable` |
| 예외 기반 | `Throwable`, `Exception`, `Error` |
| 리플렉션 | `Class`, `ClassLoader` |

## 2. Object 클래스

자바의 모든 클래스는 명시적으로 다른 클래스를 상속하지 않으면 컴파일러가 묵시적으로 `Object`를 상속시킨다. 이 덕분에 `equals()`, `hashCode()`, `toString()`, `getClass()`, `clone()` 같은 기본 기능을 모든 객체가 공통으로 갖는다.

```java
// 컴파일러가 자동으로 extends Object를 추가한다
public class Car {
    private final String model;
    public Car(String model) { this.model = model; }
}
```

`Object`를 최상위 타입으로 두는 또 다른 이유는 다형성이다. `Object` 타입 변수 하나로 어떤 객체든 참조할 수 있으므로, Java 5 이전에는 제네릭이 없어 컬렉션이 `Object`를 원소 타입으로 사용했다.

### 2-1. equals()

*동등성(equality)*을 비교한다. 기본 구현은 `==`과 동일한 참조 동일성이므로, 논리적으로 같은 값을 가진 두 객체를 같다고 판단하려면 반드시 재정의해야 한다.

올바른 `equals()`는 다섯 가지 규약을 지켜야 한다.

- **반사성**: `x.equals(x)` → `true`
- **대칭성**: `x.equals(y)` = `y.equals(x)`
- **추이성**: `x=y, y=z` → `x=z`
- **일관성**: 상태가 변하지 않으면 결과도 변하지 않는다
- **null 비동등성**: `x.equals(null)` → `false`

```java
public class Person {
    private final String name;

    public Person(String name) { this.name = name; }

    @Override
    public boolean equals(Object obj) {
        if (obj == null)              return false;
        if (this == obj)              return true;
        if (!(obj instanceof Person)) return false;
        return name.equals(((Person) obj).name);
    }
}
```

Java 16부터는 `record`가 `equals()`와 `hashCode()`를 자동으로 생성해 준다. 값 객체(value object)라면 `record`로 대체하는 것이 가장 안전하다.

```java
// Record는 equals/hashCode/toString을 컴파일러가 생성한다
public record Point(int x, int y) {}

var p1 = new Point(1, 2);
var p2 = new Point(1, 2);
System.out.println(p1.equals(p2)); // true
```

### 2-2. hashCode()

`equals()`를 재정의하면 `hashCode()`도 반드시 함께 재정의해야 한다. `HashMap`, `HashSet` 같은 해시 기반 컬렉션은 두 단계로 객체를 비교한다. 먼저 `hashCode()`가 같은지 확인하고, 같을 때만 `equals()`를 호출한다. `equals()`는 같은데 `hashCode()`가 다르면 같은 키를 두 번 저장하는 버그가 생긴다.

```java
@Override
public int hashCode() {
    return Objects.hash(name); // Objects 유틸리티 사용 권장
}
```

모든 객체가 동일한 상수를 반환하면 모든 키가 한 버킷에 몰려 `HashMap` 조회가 `O(1)`에서 `O(n)`으로 저하된다. `Objects.hash()`나 IDE 자동 생성을 활용하는 이유가 여기에 있다.

### 2-3. toString()

`println`, 문자열 연결(`+`), 로그 출력 시 자동으로 호출된다. 기본 구현은 `ClassName@16진수해시`처럼 보여 디버깅에 전혀 도움이 안 된다. 모든 구체 클래스에서 재정의하는 것을 권장한다.

```java
@Override
public String toString() {
    return "Person{name='" + name + "', age=" + age + '}';
}
```

### 2-4. clone()

`Cloneable`을 구현하면 `clone()`을 사용할 수 있지만, 얕은 복사(shallow copy) 문제와 `CloneNotSupportedException` 처리, 상속 계층에서의 동작 불일치 등 함정이 많다. 배열 복사를 제외하고는 **복사 생성자**나 **복사 팩토리 메서드**를 쓰는 것이 낫다.

```java
public class Person {
    private final String name;
    private final int    age;

    // 복사 생성자
    public Person(Person other) {
        this.name = other.name;
        this.age  = other.age;
    }

    // 복사 팩토리
    public static Person copyOf(Person other) {
        return new Person(other.name, other.age);
    }
}
```

### 2-5. getClass()

런타임에 객체가 실제로 어떤 클래스인지 `Class` 객체로 반환한다. 리플렉션 API의 출발점이며, 동적 객체 생성이나 타입 정보 조회에 사용된다. 단, 리플렉션은 타입 안전성이 낮고 캡슐화를 위반할 수 있어 꼭 필요한 경우에만 써야 한다.

```java
Object obj = new String("hello");
Class<?> clazz = obj.getClass();

System.out.println(clazz.getName());       // java.lang.String
System.out.println(clazz.getSimpleName()); // String
```

## 3. 다형성(Polymorphism)

다형성은 *같은 타입의 참조 변수로 서로 다른 클래스의 인스턴스를 다루는 능력*이다. **업캐스팅(upcasting)**과 **오버라이딩(overriding)**이 합쳐져 동작한다.

### 3-1. 컴파일타임 vs 런타임

- **정적 의존관계(컴파일타임)**: 변수 선언 타입을 보고 어떤 메서드를 호출할 수 있는지 결정한다. `Object obj`라면 `Object`에 선언된 메서드만 컴파일러가 허용한다.
- **동적 의존관계(런타임)**: 실제 인스턴스 타입에 따라 오버라이딩된 메서드가 호출된다. `obj`에 `Dog`가 들어있으면 `Dog.toString()`이 호출된다.

```java
private static void print(Object obj) {
    // 컴파일타임: Object에 선언된 toString()만 호출 가능
    // 런타임: 실제 인스턴스(Dog, Car 등)의 toString()이 호출됨
    System.out.println("객체 정보: " + obj.toString());
}
```

이 설계 덕분에 `print()` 메서드는 새 클래스가 추가되어도 수정할 필요가 없다. `toString()`만 오버라이딩하면 기존 코드가 새 동작을 자동으로 인식한다. 이것이 OCP(개방-폐쇄 원칙)가 `Object`에서 자연스럽게 실현되는 방식이다.

### 3-2. 업캐스팅과 다운캐스팅

업캐스팅(자식 → 부모)은 암묵적으로 이뤄진다. 다운캐스팅(부모 → 자식)은 `instanceof`로 타입을 먼저 확인해야 하며, Java 16부터는 *패턴 매칭 instanceof*로 캐스팅과 변수 선언을 한 번에 처리할 수 있다.

```java
private static void action(Object obj) {
    // Java 16+ 패턴 매칭 instanceof
    if (obj instanceof Dog dog) {
        dog.sound(); // 별도 캐스팅 불필요
    }
    if (obj instanceof Car car) {
        car.move();
    }
}
```

메서드 오버로딩(overloading)은 컴파일타임에 매개변수 타입으로 어떤 메서드를 호출할지 결정한다. 매개변수 타입이 `Object`인 메서드와 `String`인 메서드가 있을 때, `Object` 변수에 `String`을 담아 전달하면 `Object` 버전이 호출된다. 오버로딩과 오버라이딩을 혼동하지 않도록 주의해야 한다.

## 4. Objects 유틸리티 클래스

`java.util.Objects`는 `null`-안전한 연산을 제공하는 정적 유틸리티 클래스다. `Object`와 이름이 비슷하지만 다른 패키지에 있으며 인스턴스화할 수 없다.

```java
// requireNonNull: null이면 NullPointerException, 아니면 그대로 반환
String name = Objects.requireNonNull(input, "name must not be null");

// equals: 두 인수 중 하나가 null이어도 NPE 없이 비교
boolean same = Objects.equals(a, b);

// hash: 여러 필드를 조합한 hashCode 생성
int h = Objects.hash(name, age);

// toString: null이면 기본값 반환
String s = Objects.toString(obj, "N/A");
```

`Objects.requireNonNull()`은 생성자나 메서드의 첫 줄에서 매개변수를 검증하는 표준적인 방법이다. 나중에 `NullPointerException`이 엉뚱한 곳에서 터지는 것을 방지하고, 어느 필드가 문제인지 예외 메시지로 즉각 알 수 있다.

## 5. 래퍼 클래스(Wrapper Class)

기본형(primitive)은 `null`을 가질 수 없고 메서드를 직접 호출할 수 없다. 래퍼 클래스는 기본형을 객체로 감싸 제네릭 컬렉션에 넣거나 유틸리티 메서드를 사용할 수 있게 해준다.

| 기본형 | 래퍼 클래스 |
|--------|------------|
| `int` | `Integer` |
| `long` | `Long` |
| `double` | `Double` |
| `boolean` | `Boolean` |
| `char` | `Character` |

### 5-1. 오토박싱과 언박싱

Java 5부터 컴파일러가 기본형과 래퍼 타입 사이의 변환 코드(`valueOf()`, `intValue()` 등)를 자동으로 삽입한다. 이것이 *오토박싱(autoboxing)*과 *언박싱(unboxing)*이다.

```java
// 오토박싱: int → Integer (컴파일러가 Integer.valueOf(10) 삽입)
Integer boxed = 10;

// 언박싱: Integer → int (컴파일러가 boxed.intValue() 삽입)
int primitive = boxed;

// valueOf() 사용 권장 (new Integer()는 deprecated)
Integer i = Integer.valueOf(42);
int     n = Integer.parseInt("42"); // 기본형 반환
```

### 5-2. 정수 캐시(-128 ~ 127)

`Integer.valueOf()`는 `-128`에서 `127` 사이의 값을 JVM이 미리 생성한 캐시 객체로 반환한다. 이 범위 안에서 `==` 비교가 `true`가 되는 것은 같은 객체를 가리키기 때문이다. 범위 밖에서는 매번 새 객체가 생성되어 `==`이 `false`가 된다.

```java
Integer a = Integer.valueOf(100);
Integer b = Integer.valueOf(100);
System.out.println(a == b);      // true  (캐시 범위 내)
System.out.println(a.equals(b)); // true

Integer c = Integer.valueOf(200);
Integer d = Integer.valueOf(200);
System.out.println(c == d);      // false (캐시 범위 밖, 별개 객체)
System.out.println(c.equals(d)); // true
```

래퍼 객체끼리는 반드시 `equals()`로 비교해야 한다. `==`는 참조 동일성을 비교하므로 캐시 범위 밖에서 예상치 못한 버그가 생긴다. Java 21 기준으로 `Long`, `Short`, `Byte`, `Character`도 동일한 범위의 캐시를 유지한다.

### 5-3. 성능 주의

반복 연산이 많은 루프에서 래퍼 타입을 쓰면 오토박싱이 반복 발생해 불필요한 객체가 대량 생성된다. 연산 결과를 누적하거나 반복 횟수가 많은 코드에서는 기본형을 직접 사용하는 것이 안전하다.

```java
// ❌ Long으로 선언하면 루프마다 Long 객체가 생성된다
Long sum = 0L;
for (long i = 0; i < 1_000_000; i++) {
    sum += i;
}

// ✅ long 기본형 사용
long sum = 0L;
for (long i = 0; i < 1_000_000; i++) {
    sum += i;
}
```

일반적인 웹 애플리케이션에서 병목은 메모리 연산보다 네트워크나 I/O에 있다. 래퍼 타입이 코드의 의미를 더 잘 전달한다면(예: `null` 표현이 필요한 경우) 래퍼 타입을 쓰되, 연산량이 많은 핵심 경로에서는 기본형으로 내려가는 것이 맞다.
