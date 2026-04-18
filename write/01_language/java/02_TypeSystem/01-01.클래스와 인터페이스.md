# 클래스와 인터페이스
---
> 클래스와 인터페이스를 쓰기 편하고, 견고하며, 유연하게 만드는 방법을 정리한다. 상속보다 컴포지션을 선택하고, 인터페이스로 타입을 정의하는 원칙이 핵심이다.

## 1. 접근 제어

접근 제어(Access Control)는 클래스 내부 구현을 외부로부터 숨기는 캡슐화의 도구다. Java는 네 가지 접근 수준을 제공하며, 가능한 한 좁은 범위를 선택하는 것이 원칙이다.

| 접근 수준 | 키워드 | 같은 클래스 | 같은 패키지 | 하위 클래스 | 외부 |
|-----------|--------|------------|------------|------------|------|
| private | `private` | O | X | X | X |
| package-private | (없음) | O | O | X | X |
| protected | `protected` | O | O | O | X |
| public | `public` | O | O | O | O |

설계 원칙은 단순하다. 공개 API로 의도한 것만 `public`으로 선언하고, 나머지는 최대한 좁힌다. 특히 `protected`는 상속 계층에 노출되므로 사실상 공개 API에 준하는 책임이 따른다.

## 2. 상속 vs 합성

상속은 강력하지만 캡슐화를 깨트리는 대표적인 설계 결함을 유발한다. 슈퍼 클래스의 내부 구현이 변경되면 서브클래스가 의도치 않게 깨질 수 있고, 강한 결합으로 인해 유연성과 재사용성이 모두 떨어진다.

관계를 판단하는 기준은 명확하다. "A는 B이다(Is-A)"가 성립할 때만 상속을 사용하고, "A는 B를 가진다(Has-A)"라면 합성(Composition)을 선택한다:

```java
class Engine {}           // 엔진 클래스
class Automobile {}       // 탈것 부모 클래스

class Car extends Automobile {    // Car Is-A Automobile → 상속
    private Engine engine;        // Car Has-A Engine → 합성
}
```

합성과 전달(Delegation) 패턴을 조합하면 기존 클래스를 깨지 않고 기능을 확장할 수 있다. 아래 예시에서 `ForwardingSet`은 `Set` 인터페이스를 구현하고 내부 `Set`에 작업을 위임하는 래퍼다:

```java
public class ForwardingSet<E> implements Set<E> {
    private final Set<E> s;

    public ForwardingSet(Set<E> s) {
        this.s = s;
    }

    public void clear() { s.clear(); }
    public boolean contains(Object o) { return s.contains(o); }
    // 나머지 Set 메서드도 s에 위임...
}

public class InstrumentedSet<E> extends ForwardingSet<E> {
    private int addCount = 0;

    public InstrumentedSet(Set<E> s) {
        super(s);
    }

    @Override
    public boolean add(E e) {
        addCount++;
        return super.add(e);
    }

    @Override
    public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();
        return super.addAll(c);
    }

    public int getAddCount() {
        return addCount;
    }
}
```

`InstrumentedSet`은 `HashSet`, `TreeSet` 등 어떤 `Set` 구현체든 감쌀 수 있다. 상속이었다면 특정 구현체에 종속되었겠지만, 합성 덕분에 구현체 교체가 자유롭다.

## 3. 추상 클래스 vs 인터페이스

추상 클래스와 인터페이스는 모두 타입을 정의하는 수단이지만, 근본적인 차이가 있다. 추상 클래스는 단일 상속만 허용하므로 새 타입을 끼워 넣기 어렵고, 인터페이스는 다중 구현이 가능해 기존 클래스에도 자유롭게 추가할 수 있다.

인터페이스의 이점은 세 가지로 요약된다:

- 다중 구현(믹스인)이 가능하여 클래스가 여러 타입으로 동작할 수 있다
- API와 구현체를 분리함으로써 모듈화와 재사용성이 향상된다
- 데코레이터, 래퍼 같은 패턴 구현이 자연스럽다

두 방식의 장점을 동시에 취하려면 **추상 골격 구현(Skeletal Implementation)** 패턴을 사용한다. 인터페이스로 타입을 정의하고, 추상 클래스로 공통 구현을 제공하는 방식이다:

```java
public interface Book {
    void openBook();
    void prepareContent();
    void interpretContent();
    void closeBook();
    void readBook();
}

public abstract class AbstractBook implements Book {
    @Override
    public void openBook() {
        System.out.println("Opening the book.");
    }

    @Override
    public void closeBook() {
        System.out.println("Closing the book.");
    }

    // 템플릿 메서드: 골격 구현에서 전체 흐름을 제어
    @Override
    public void readBook() {
        openBook();
        prepareContent();
        interpretContent();
        closeBook();
    }

    // 서브클래스가 반드시 구현해야 하는 부분
    @Override
    public abstract void prepareContent();

    @Override
    public abstract void interpretContent();
}
```

`FictionBook`과 `NonFictionBook`은 `prepareContent()`와 `interpretContent()`만 구현하면 된다. 공통 흐름은 골격 구현이 담당한다.

## 4. default 메서드

Java 8에서 도입된 `default` 메서드는 인터페이스에 구현을 포함할 수 있게 한다. 기존 인터페이스를 구현한 모든 클래스를 수정하지 않고도 새 메서드를 추가할 수 있어 진화에 유리하다.

올바른 사용 지침은 두 가지다:

- 남용하지 않고 추상적인 계약을 명확히 표현하는 데 집중한다
- 간단한 확장이나 유틸리티 메서드에만 적용한다

`default` 메서드는 인터페이스의 타입 정의 역할을 보조하는 수단이지, 구현 상속을 대체하는 수단이 아니다. 복잡한 구현 로직은 골격 추상 클래스에 두는 것이 더 적합하다.

## 5. 인터페이스의 다중 상속과 다이아몬드 문제

인터페이스는 다중 구현이 가능하기 때문에 `default` 메서드가 충돌하는 **다이아몬드 문제(Diamond Problem)**가 발생할 수 있다. Java는 이를 세 가지 규칙으로 해결한다:

- 클래스의 메서드가 항상 인터페이스 `default` 메서드보다 우선한다
- 더 구체적인 인터페이스의 `default` 메서드가 덜 구체적인 것보다 우선한다
- 두 인터페이스가 같은 시그니처의 `default` 메서드를 제공하고 우선순위를 판별할 수 없으면 구현 클래스가 직접 오버라이드해야 한다

```java
interface A {
    default void hello() { System.out.println("A"); }
}

interface B extends A {
    default void hello() { System.out.println("B"); }
}

class C implements A, B {
    // B가 A보다 구체적이므로 B.hello()가 자동 선택된다
}

class D implements A, B {
    @Override
    public void hello() {
        B.super.hello(); // 명시적으로 선택도 가능
    }
}
```

## 6. 태그 클래스 대신 클래스 계층 구조

하나의 클래스가 여러 의미를 enum 태그로 구분하는 **태그 클래스(Tagged Class)**는 설계 안티패턴이다. 불필요한 필드가 공존하고, `switch` 문이 늘어나며, 메모리 낭비가 발생한다.

태그 클래스를 계층 구조로 전환하면 코드가 명확해진다:

```java
// 태그 클래스 (안티패턴)
public class Figure {
    enum Shape { RECTANGLE, CIRCLE }
    private final Shape shape;
    private final double length;   // 사각형에서만 사용
    private final double width;    // 사각형에서만 사용
    private final double radius;   // 원에서만 사용
    // ...
}

// 계층 구조로 전환
abstract class Shape {
    abstract double area();
}

class Circle extends Shape {
    private final double radius;
    Circle(double radius) { this.radius = radius; }

    @Override
    double area() { return Math.PI * radius * radius; }
}

class Rectangle extends Shape {
    private final double length;
    private final double width;
    Rectangle(double length, double width) {
        this.length = length;
        this.width = width;
    }

    @Override
    double area() { return length * width; }
}
```

각 클래스는 자신에게 필요한 필드만 가지며, `area()` 구현이 각자의 책임으로 분산된다.

## 7. 중첩 클래스는 static을 권장한다

중첩 클래스(Nested Class)는 자신을 둘러싼 바깥 클래스에서만 쓰이는 클래스다. 네 가지 종류가 있다:

- 정적 멤버 클래스
- 비정적 멤버 클래스
- 익명 클래스
- 지역 클래스

비정적 멤버 클래스는 외부 클래스 인스턴스와 자동으로 연결된다. 이 숨겨진 참조가 메모리 누수의 원인이 될 수 있다:

```java
public class OuterClass {
    private int outerField = 100;

    class NonStaticInner {   // 외부 인스턴스에 대한 숨겨진 참조 보유
        void display() {
            System.out.println(outerField);
        }
    }
}
```

반면 정적 멤버 클래스는 외부 인스턴스 참조를 유지하지 않는다. 외부 클래스 없이 독립적으로 생성할 수 있고, 재사용성도 높다:

```java
public class OuterClass {
    private static int outerStaticField = 200;

    static class StaticNested {  // 외부 인스턴스 참조 없음
        void display() {
            System.out.println(outerStaticField);
        }
    }
}
```

멤버 클래스가 외부 인스턴스에 접근할 필요가 없다면 항상 `static`을 붙이는 것이 원칙이다.

## 8. Java 21에서의 설계 지침

Java 21 기준으로 클래스와 인터페이스 설계에 적용할 수 있는 지침을 정리하면 다음과 같다:

- 상속 설계가 명확하지 않으면 `final`로 막거나, 상속용으로 설계하고 문서화한다
- 값 객체에는 `record`를 우선 고려한다 (자동으로 `final`, 불변성 보장)
- 제한된 타입 계층은 `sealed` 인터페이스/클래스로 명시적으로 표현한다
- 인터페이스는 타입 정의에 집중하고, `default` 메서드는 최소한으로 사용한다
- 중첩 클래스가 외부 상태 접근이 불필요하면 반드시 `static`을 선언한다
