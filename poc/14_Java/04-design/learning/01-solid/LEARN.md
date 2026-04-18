# SOLID 원칙

---

> 객체지향 설계의 5가지 원칙(SOLID)은 변경에 강하고 이해하기 쉬운 코드를 만들기 위한 지침이다. 각 원칙은 독립적으로 존재하지만, 함께 적용할 때 클래스 간 결합도를 낮추고 응집도를 높이는 효과가 극대화된다.

## 원칙 요약

| 원칙 | 이름 | 핵심 질문 | 위반 신호 |
|------|------|----------|----------|
| SRP | 단일 책임 원칙 | 이 클래스가 바뀌는 이유가 하나인가? | 메서드가 서로 무관한 작업을 수행 |
| OCP | 개방-폐쇄 원칙 | 기존 코드 수정 없이 기능 추가가 가능한가? | `if/switch`로 타입을 분기하는 코드 |
| LSP | 리스코프 치환 원칙 | 하위 타입이 상위 타입을 완전히 대체할 수 있는가? | 오버라이드 후 예외를 던지거나 동작을 축소 |
| ISP | 인터페이스 분리 원칙 | 구현체가 사용하지 않는 메서드가 있는가? | 빈 구현(`throw new UnsupportedOperationException()`) |
| DIP | 의존성 역전 원칙 | 고수준 모듈이 저수준 구현에 직접 의존하는가? | `new ConcreteClass()`가 비즈니스 로직 안에 존재 |

## SRP — 단일 책임 원칙

**Single Responsibility Principle**은 클래스가 변경되는 이유가 오직 하나여야 한다는 원칙이다. 여기서 "이유"는 기능적 관심사가 아니라 변경을 요구하는 **이해관계자(actor)**를 의미한다. 회계팀의 요구로 바뀌는 로직과 개발팀의 요구로 바뀌는 로직은 서로 다른 책임이므로 분리되어야 한다.

```java
// 위반: 보고서 생성과 저장이라는 두 가지 책임이 혼재한다
class ReportService {
    public String generateHtml(Report report) { /* 렌더링 로직 */ }
    public void saveToFile(String html, Path path) { /* 파일 I/O 로직 */ }
}

// 준수: 각 클래스가 하나의 이유로만 변경된다
class ReportRenderer {
    public String generateHtml(Report report) { /* 렌더링만 담당 */ }
}

class ReportPersistence {
    public void saveToFile(String html, Path path) { /* 저장만 담당 */ }
}
```

## OCP — 개방-폐쇄 원칙

**Open-Closed Principle**은 소프트웨어 엔티티가 확장에는 열려 있고 수정에는 닫혀 있어야 한다는 원칙이다. 새로운 동작을 추가할 때 기존 코드를 건드리지 않도록 추상화 지점을 설계하는 것이 핵심이다. 인터페이스나 추상 클래스를 통해 확장 지점을 만들면 달성할 수 있다.

```java
// 위반: 새로운 할인 정책이 추가될 때마다 기존 메서드를 수정해야 한다
class DiscountCalculator {
    public double calculate(String type, double price) {
        if ("VIP".equals(type)) return price * 0.8;
        if ("MEMBER".equals(type)) return price * 0.9;
        return price;
    }
}

// 준수: 새 정책은 새 구현체를 추가하기만 하면 된다
interface DiscountPolicy {
    double apply(double price);
}

record VipDiscount() implements DiscountPolicy {
    public double apply(double price) { return price * 0.8; }
}

record MemberDiscount() implements DiscountPolicy {
    public double apply(double price) { return price * 0.9; }
}
```

## LSP — 리스코프 치환 원칙

**Liskov Substitution Principle**은 상위 타입의 객체를 하위 타입의 객체로 교체해도 프로그램의 정확성이 깨지지 않아야 한다는 원칙이다. 단순히 컴파일이 되는 것을 넘어, **행동(behavior)**이 계약을 만족해야 한다. 정사각형이 직사각형을 상속하면 너비/높이를 독립적으로 설정한다는 직사각형의 계약을 위반하는 전형적인 위반 사례다.

```java
// 위반: 정사각형은 너비와 높이가 독립적이라는 직사각형의 계약을 깬다
class Rectangle {
    protected int width, height;
    public void setWidth(int w) { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int area() { return width * height; }
}

class Square extends Rectangle {
    @Override
    public void setWidth(int w) { this.width = w; this.height = w; } // 계약 위반
}

// 준수: 공통 추상화로 분리하고 각자의 계약을 지킨다
interface Shape {
    int area();
}

record Rectangle(int width, int height) implements Shape {
    public int area() { return width * height; }
}

record Square(int side) implements Shape {
    public int area() { return side * side; }
}
```

## ISP — 인터페이스 분리 원칙

**Interface Segregation Principle**은 클라이언트가 자신이 사용하지 않는 메서드에 의존하도록 강요받아서는 안 된다는 원칙이다. 하나의 뚱뚱한 인터페이스보다 역할별로 분리된 작은 인터페이스 여러 개가 변경에 더 유연하다. 구현체가 빈 메서드나 예외를 반환한다면 ISP 위반의 강력한 신호다.

```java
// 위반: Robot은 eat()을 구현할 수 없지만 강제된다
interface Worker {
    void work();
    void eat();
    void sleep();
}

class Robot implements Worker {
    public void work() { /* 구현 */ }
    public void eat() { throw new UnsupportedOperationException(); } // 위반
    public void sleep() { throw new UnsupportedOperationException(); } // 위반
}

// 준수: 역할에 따라 인터페이스를 분리한다
interface Workable { void work(); }
interface Eatable  { void eat(); }
interface Sleepable { void sleep(); }

class Human implements Workable, Eatable, Sleepable {
    public void work() { /* 구현 */ }
    public void eat()  { /* 구현 */ }
    public void sleep() { /* 구현 */ }
}

class Robot implements Workable {
    public void work() { /* 구현 */ }
}
```

## DIP — 의존성 역전 원칙

**Dependency Inversion Principle**은 고수준 모듈이 저수준 모듈에 의존하는 것이 아니라, 양쪽 모두 추상화에 의존해야 한다는 원칙이다. 비즈니스 로직(고수준)이 데이터베이스나 외부 API(저수준)에 직접 의존하면 저수준이 바뀔 때 고수준도 수정해야 한다. 스프링의 DI 컨테이너는 이 원칙을 인프라 수준에서 강제해주는 도구다.

```java
// 위반: OrderService가 구체 클래스에 직접 의존한다
class OrderService {
    private final MySQLOrderRepository repo = new MySQLOrderRepository(); // 저수준에 직접 의존

    public void placeOrder(Order order) {
        repo.save(order);
    }
}

// 준수: 고수준과 저수준 모두 인터페이스에 의존한다
interface OrderRepository {
    void save(Order order);
}

class MySQLOrderRepository implements OrderRepository {
    public void save(Order order) { /* MySQL 저장 로직 */ }
}

class OrderService {
    private final OrderRepository repo; // 추상화에 의존

    public OrderService(OrderRepository repo) { // 생성자 주입
        this.repo = repo;
    }

    public void placeOrder(Order order) {
        repo.save(order);
    }
}
```
