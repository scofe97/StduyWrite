# 불변 객체와 Record: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Record를 JPA Entity로 쓸 수 없는 이유

### 왜 이 질문이 중요한가
Java 16에서 Record가 정식 도입된 후 "DTO는 Record로 바꾸면 되겠다"는 이해는 맞지만, "Entity도 Record로 바꾸자"는 시도는 런타임 에러로 이어진다. 그 이유를 JPA의 내부 동작과 함께 이해하는 것이 중요하다.

### 답변

JPA가 Record를 Entity로 사용할 수 없는 이유는 네 가지다.

첫째, JPA는 Entity에 no-args 생성자를 요구한다. JPA 구현체(Hibernate 등)는 DB에서 데이터를 읽어올 때 기본 생성자로 빈 객체를 만든 뒤 setter나 리플렉션으로 필드를 채운다. Record는 모든 필드를 받는 canonical 생성자만 가지며 no-args 생성자가 없다.

둘째, JPA는 프록시(lazy loading을 위해)를 생성하기 위해 Entity 클래스를 상속한다. Hibernate는 `class UserProxy extends User`와 같은 서브클래스를 동적으로 만든다. Record는 `final` 클래스이므로 상속이 불가능하다.

```java
// 이 코드는 컴파일되지만 런타임에 Hibernate가 예외를 던진다
@Entity
record User(Long id, String name) {} // 불가
// Caused by: org.hibernate.MappingException:
//   Entity class must not be a record

// 올바른 사용: Entity는 일반 클래스, DTO/응답은 Record
@Entity
class User {
    @Id Long id;
    String name;
    protected User() {} // JPA 필수 no-args 생성자
    public User(Long id, String name) { ... }
}

record UserResponse(Long id, String name) {
    static UserResponse from(User user) {
        return new UserResponse(user.getId(), user.getName());
    }
}
```

셋째, JPA Entity는 상태가 변경 가능해야 한다. Dirty Checking(변경 감지)이 작동하려면 영속성 컨텍스트가 필드를 변경할 수 있어야 한다. Record의 모든 필드는 `final`이어서 생성 후 변경이 불가능하다.

넷째, Record의 `equals()`/`hashCode()`는 모든 필드 기반이다. JPA Entity의 동등성은 보통 ID 하나로 판단해야 하는데, Record의 자동 생성 메서드는 이 원칙에 맞지 않는다. 특히 ID가 null인 새 엔티티는 영속화 전 컬렉션에 넣으면 저장 후 ID가 채워져도 hash가 달라져 Set에서 찾지 못하는 문제가 생긴다.

---

## Q2. 깊은 불변성(Deep Immutability)을 보장하는 방법

### 왜 이 질문이 중요한가
`final` 필드를 가진 클래스를 만들었다고 불변이라 착각하는 경우가 많다. `final List<String> items`는 참조가 바뀌지 않을 뿐 리스트 내용물은 여전히 변경 가능하다. 진정한 불변성이 왜 중요하고 어떻게 달성하는지를 이해해야 스레드 안전하고 예측 가능한 코드를 작성할 수 있다.

### 답변

얕은 불변성(shallow immutability)은 필드 참조가 변경되지 않음을 보장하지만, 참조된 객체의 내부 상태는 여전히 변경 가능하다. 깊은 불변성(deep immutability)은 객체 그래프 전체가 변경 불가능함을 보장한다.

```java
// 얕은 불변 — final이지만 내용 변경 가능
public final class Order {
    private final List<Item> items; // items 자체는 바꿀 수 없지만

    public List<Item> getItems() {
        return items; // 외부에서 items.add(...)가 가능!
    }
}

// 깊은 불변 달성 전략 1: 방어적 복사
public final class Order {
    private final List<Item> items;

    public Order(List<Item> items) {
        this.items = List.copyOf(items); // 입력 복사
    }

    public List<Item> getItems() {
        return Collections.unmodifiableList(items); // 뷰 반환
        // 또는 return List.copyOf(items); // 매번 복사 (더 안전하나 비용 있음)
    }
}
```

깊은 불변성을 위한 전략은 세 가지다. 첫째, 불변 컬렉션 사용이다. `List.of()`, `Set.of()`, `Map.of()`(Java 9+)나 Guava의 `ImmutableList`는 수정 시 예외를 던진다. 생성자에서 `List.copyOf()`로 방어적 복사 후 저장하면 입력 컬렉션 변경의 영향도 받지 않는다.

둘째, 컬렉션의 원소도 불변이어야 한다. `List<Item>`에서 `Item`이 가변이면 원소를 꺼내 내부를 바꿀 수 있다. 원소 타입도 불변이거나 Record여야 진정한 깊은 불변성이 달성된다.

```java
// 원소도 불변으로
record Item(String name, int quantity) {} // Record는 자동으로 불변

public final class Order {
    private final List<Item> items;

    public Order(List<Item> items) {
        this.items = List.copyOf(items); // List와 원소 모두 불변
    }

    public List<Item> getItems() { return items; } // 이미 불변 리스트
}
```

셋째, 날짜처럼 가변 타입을 필드로 가질 때는 방어적 복사가 필수다. `java.util.Date`는 가변이므로 getter에서 그대로 반환하면 외부에서 변경 가능하다. `java.time.LocalDate`, `Instant` 등 불변 타입으로 교체하거나, 부득이하게 `Date`를 써야 한다면 반드시 복사해서 반환한다. Record는 이 모든 규칙을 개발자가 실수 없이 지켜야 한다는 점에서 완전한 해결책이 아니며, 가변 타입 필드가 있는 Record는 여전히 방어적 복사가 필요하다.
