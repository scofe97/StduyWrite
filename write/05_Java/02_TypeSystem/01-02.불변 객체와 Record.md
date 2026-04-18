# 불변 객체와 Record
---
> 불변 객체(Immutable Object)는 공유 참조의 사이드 이펙트를 원천 차단하는 설계 기법이다. Java 16에서 정식 도입된 Record는 불변 객체 작성의 반복적인 보일러플레이트를 제거해준다.

## 1. 불변 객체가 필요한 이유

Java에서는 하나의 객체를 여러 변수가 참조하는 것을 막을 방법이 없다. 문제는 공유 자체가 아니라, 공유된 상태를 누군가 변경할 때 발생한다. 어느 한 쪽이 값을 바꾸면 나머지 참조자들이 예상치 못한 상태를 보게 되는 것이 사이드 이펙트(Side Effect)다.

불변 객체는 이 문제를 근본적으로 차단한다. 상태가 생성 시점에 고정되므로 어떤 참조자도 내부 값을 변경할 수 없고, 결과적으로 다음 이점이 따라온다:

- 멀티스레드 환경에서 동기화 없이 안전하게 공유할 수 있다
- 동일 값의 객체를 재사용할 수 있어 GC 압력이 줄어든다
- 예외가 발생해도 객체 상태가 손상되지 않는다 (실패 원자성)

## 2. 불변 객체 생성 규칙

불변 클래스를 만들 때 지켜야 할 규칙은 세 가지다:

- 모든 필드를 `private final`로 선언해 외부에서 수정 불가능하게 한다
- `final class`로 선언해 상속을 막는다 (서브클래스가 가변 상태를 추가할 수 없도록)
- 내부에 가변 객체가 있다면 외부에서 접근하거나 변경할 수 없도록 방어적 복사를 사용한다

```java
public final class Complex {           // final class: 상속 불가
    private final double re;           // private final: 수정 불가
    private final double im;

    public Complex(double re, double im) {
        this.re = re;
        this.im = im;
    }

    public double realPart() { return re; }
    public double imaginaryPart() { return im; }
    // setter 없음
}
```

가변 필드를 포함하는 경우 방어적 복사(Defensive Copy)가 필수다. 생성자에서 외부 객체를 그대로 저장하면 외부에서 해당 객체를 변경해 불변성을 깰 수 있다:

```java
public final class Period {
    private final Date start;
    private final Date end;

    public Period(Date start, Date end) {
        // 방어적 복사: 외부 참조를 그대로 저장하지 않는다
        this.start = new Date(start.getTime());
        this.end = new Date(end.getTime());
    }

    public Date start() {
        return new Date(start.getTime()); // getter도 복사본 반환
    }
}
```

실무에서는 `Date` 대신 Java 8의 `LocalDate`, `LocalDateTime` 같은 불변 날짜 클래스를 사용하면 방어적 복사가 불필요해진다.

## 3. withXxx() 패턴

불변 객체에서 "값을 변경한" 새 객체가 필요할 때 관례적으로 `withXxx()` 메서드를 사용한다. 커피에 설탕을 추가하면 원래 커피가 바뀌는 것이 아니라 새로운 커피가 만들어지는 것처럼, `with` 메서드는 지정한 수정 사항을 반영한 **새 인스턴스**를 반환한다:

```java
public final class ImmutablePoint {
    private final int x;
    private final int y;

    public ImmutablePoint(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // 원본은 그대로, x만 바꾼 새 객체 반환
    public ImmutablePoint withX(int newX) {
        return new ImmutablePoint(newX, this.y);
    }

    public ImmutablePoint withY(int newY) {
        return new ImmutablePoint(this.x, newY);
    }
}
```

Java 표준 라이브러리에서도 동일한 패턴이 쓰인다. `LocalDate.withYear(2025)`나 `LocalTime.withHour(9)`가 그 예다.

## 4. Java Record

Record는 Java 16에서 정식 도입된 클래스 유형으로, 불변 데이터 전달 객체를 간결하게 선언하는 수단이다. 단 한 줄 선언이 방대한 보일러플레이트를 대체한다:

```java
public record Person(String name, int age) {}
```

컴파일러는 위 선언으로부터 다음을 자동 생성한다:

- 모든 필드를 인자로 받는 주 생성자(Canonical Constructor)
- 각 필드의 접근자 메서드 (`name()`, `age()`)
- 값 기반 `equals()`, `hashCode()`, `toString()`
- `private final` 필드 선언
- `final` 클래스 선언

자동 생성 결과를 풀어쓰면 다음과 같다:

```java
public final class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String name() { return name; }
    public int age()     { return age; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }

    @Override
    public int hashCode() { return Objects.hash(name, age); }

    @Override
    public String toString() { return "Person[name=" + name + ", age=" + age + "]"; }
}
```

Record에는 정적 필드와 메서드, 인스턴스 메서드를 추가할 수 있다:

```java
public record Person(String name, int age) {
    public static final int LEGAL_ADULT_AGE = 18;

    public boolean isAdult() {
        return age >= LEGAL_ADULT_AGE;
    }

    public String greeting() {
        return "Hello, " + name + ". You are " + (isAdult() ? "an adult." : "not an adult.");
    }
}
```

## 5. 컴팩트 생성자

Record의 주 생성자를 간결하게 재정의하는 방법이 **컴팩트 생성자(Compact Constructor)**다. 매개변수 목록과 필드 대입을 명시하지 않아도 컴파일러가 자동으로 처리해 주며, 검증과 정규화 로직에 집중할 수 있다:

```java
public record Person(String name, int age) {
    public Person {                         // 매개변수 목록 생략
        if (name == null) name = "Unknown"; // name 매개변수를 조작
        if (age < 0)      age = 0;
        // 컴파일러가 this.name = name; this.age = age; 를 자동 추가
    }
}
```

컴팩트 생성자 내부에서 `name`과 `age`는 필드가 아닌 **매개변수**처럼 동작한다. `final` 필드는 아직 초기화되지 않았기 때문에 `this.name`에 직접 접근할 수 없다. 컴파일러가 생성자 블록 끝에 `this.name = name; this.age = age;`를 자동으로 삽입한다.

## 6. Record의 제약

Record를 사용할 때 알아야 할 제약은 세 가지다:

- 다른 클래스를 상속할 수 없다 (`java.lang.Record`를 암묵적으로 상속하기 때문)
- 인스턴스 필드를 추가할 수 없다 (정적 필드는 허용)
- 모든 인스턴스 필드는 반드시 `final`이다

인터페이스 구현은 자유롭다:

```java
public record AddressRecord(
        String street
        , String city
        , String zipCode)
        implements Comparable<AddressRecord> {

    @Override
    public int compareTo(AddressRecord other) {
        return this.zipCode.compareTo(other.zipCode);
    }
}
```

## 7. Jackson 직렬화/역직렬화

전통적인 클래스에서 Jackson은 기본 생성자(No-Args Constructor)로 객체를 생성한 뒤 setter로 값을 주입한다. Record에는 기본 생성자가 없지만, Jackson 2.12 이상에서는 Record의 주 생성자를 자동으로 인식해 역직렬화한다:

```java
public record UserDTO(String name, int age) {}
```

직렬화는 접근자 메서드(`name()`, `age()`)를 통해 필드 값을 읽으므로 별도 설정이 필요 없다:

```java
ObjectMapper mapper = new ObjectMapper();

// 직렬화
UserDTO user = new UserDTO("John", 30);
String json = mapper.writeValueAsString(user);
// 결과: {"name":"John","age":30}

// 역직렬화
String json2 = "{\"name\":\"Jane\",\"age\":25}";
UserDTO restored = mapper.readValue(json2, UserDTO.class);
// 결과: UserDTO[name=Jane, age=25]
```

## 8. Record를 DTO로 사용하는 실무 패턴

API 요청/응답 DTO로 Record를 사용할 때 컴팩트 생성자에서 입력값을 검증하는 패턴이 유용하다:

```java
public record CreateUserRequest(String name, int age) {
    public CreateUserRequest {
        if (name == null || name.isBlank())
            throw new IllegalArgumentException("이름은 필수입니다.");
        if (age < 0 || age > 150)
            throw new IllegalArgumentException("나이가 올바르지 않습니다.");
        name = name.strip(); // 정규화
    }
}
```

빌더 패턴이 필요한 경우 Record 내부에 정적 `Builder` 클래스를 선언할 수 있다. 다만 필드 수가 적고 모든 필드가 필수라면 주 생성자를 직접 사용하는 것이 더 간결하다:

```java
public record Person(String name, int age) {
    public static class Builder {
        private String name;
        private int age;

        public Builder name(String name) { this.name = name; return this; }
        public Builder age(int age)      { this.age = age;  return this; }
        public Person build()            { return new Person(name, age); }
    }
}
```

## 9. 모든 클래스를 불변으로 만들면 안 된다

불변 객체는 장점이 많지만, 상태 변경마다 새 객체를 생성해야 한다는 비용이 따른다. 대용량 데이터를 반복적으로 수정하는 경우라면 불변 객체가 GC 부담을 키우고 성능을 저하시킬 수 있다. `StringBuilder`가 불변 `String` 대신 가변으로 설계된 이유가 바로 이것이다. 불변이 기본 원칙이되, 성능 요구사항이 충돌하는 지점에서는 가변 대안을 검토한다.
