# 리플렉션과 애노테이션
---
> 리플렉션(Reflection)은 컴파일 시점에 알 수 없는 클래스의 구조를 런타임에 탐색하고 조작하는 메커니즘이다. Spring DI, JPA, 테스트 프레임워크가 코드를 "마법처럼" 동작시키는 근본 원리가 바로 여기에 있다.

## 1. Class 객체 획득

JVM은 클래스를 로드할 때 해당 클래스의 메타데이터를 `Class` 객체에 담아 메서드 영역(Method Area)에 저장한다. 이 `Class` 객체를 얻는 방법은 세 가지다:

```java
// 1. 클래스 리터럴 — 컴파일 시점에 타입이 확정될 때
Class<String> c1 = String.class;

// 2. getClass() — 이미 인스턴스가 있을 때
Class<?> c2 = "hello".getClass();

// 3. Class.forName() — 클래스명이 런타임에 결정될 때
Class<?> c3 = Class.forName("java.lang.String"); // ClassNotFoundException 가능
```

세 방법은 모두 동일한 `Class` 객체를 반환한다. 같은 클래스는 JVM 내에서 하나의 `Class` 객체만 존재하므로 `==` 비교가 가능하다. `Class.forName()`은 클래스가 클래스패스에 없으면 `ClassNotFoundException`을 던지므로 반드시 예외 처리가 필요하다.

## 2. 리플렉션 API

`Class` 객체를 통해 클래스의 생성자, 필드, 메서드 정보를 얻고 동적으로 실행할 수 있다.

### 2-1. 메타데이터 조회

`getDeclared*()` 계열은 상속받은 것을 제외하고 해당 클래스에 직접 선언된 멤버를 모두 가져온다. `get*()` 계열은 `public` 멤버만 가져오되 상속된 것도 포함한다:

```java
Class<?> clazz = String.class;

// 생성자
Constructor<?>[] ctors = clazz.getDeclaredConstructors();

// 필드 — 선언된 모든 필드 (private 포함)
Field[] fields = clazz.getDeclaredFields();
for (Field f : fields) {
    System.out.println(f.getType().getSimpleName() + " " + f.getName());
}

// 메서드 — 단일 메서드는 이름 + 파라미터 타입으로 특정
Method method = clazz.getDeclaredMethod("substring", int.class, int.class);

// 슈퍼클래스와 인터페이스
Class<?> superClass = clazz.getSuperclass();
Class<?>[] interfaces = clazz.getInterfaces();
```

### 2-2. 동적 객체 생성과 메서드 호출

클래스명을 문자열로 받아 런타임에 객체를 생성하는 패턴은 플러그인 시스템이나 팩토리에서 자주 쓰인다:

```java
// 클래스 정보 로드
Class<?> clazz = Class.forName("com.example.Hello");

// 기본 생성자로 인스턴스 생성
Object instance = clazz.getDeclaredConstructor().newInstance();

// 메서드 동적 호출
Method hello = clazz.getDeclaredMethod("hello");
String result = (String) hello.invoke(instance);
```

`invoke()`의 첫 번째 인자는 메서드를 실행할 인스턴스다. `static` 메서드라면 `null`을 전달한다. 반환 타입은 `Object`이므로 캐스팅이 필요하다.

### 2-3. 접근 제어 우회와 보안 이슈

`private` 필드나 메서드에 접근하려면 `setAccessible(true)`를 먼저 호출해야 한다:

```java
Field field = clazz.getDeclaredField("message");
field.setAccessible(true);          // 접근 제어 해제
field.set(instance, "변경된 값");   // 값 설정
Object value = field.get(instance); // 값 읽기
```

`setAccessible(true)`는 Java의 캡슐화를 런타임에 강제로 우회한다. 프레임워크 내부에서는 필수 기능이지만, 일반 애플리케이션 코드에서 남용하면 내부 구현에 의존하는 취약한 코드가 된다. Java 9 모듈 시스템 이후로는 모듈 경계를 넘는 `setAccessible()` 호출이 기본적으로 차단된다.

## 3. 애노테이션

**애노테이션(Annotation)**은 코드에 메타데이터를 붙이는 방법이다. 코드 자체의 동작을 바꾸지 않고, 컴파일러나 프레임워크가 이 정보를 읽어 추가 동작을 수행하도록 한다.

### 3-1. 내장 애노테이션

Java가 기본 제공하는 애노테이션은 컴파일러에게 직접 지시를 내린다:

- `@Override`: 슈퍼클래스 메서드를 올바르게 오버라이드했는지 컴파일러가 검증한다.
- `@Deprecated`: 사용을 지양해야 할 API임을 표시하고, 사용 시 컴파일 경고를 발생시킨다.
- `@SuppressWarnings("unchecked")`: 특정 컴파일러 경고를 억제한다.
- `@FunctionalInterface`: 인터페이스가 추상 메서드를 정확히 하나만 가지는지 컴파일러가 검증한다.

### 3-2. 메타 애노테이션

*메타 애노테이션(Meta-Annotation)*은 애노테이션을 정의할 때 사용하는 애노테이션이다. 커스텀 애노테이션의 동작 범위와 생존 시점을 결정한다:

```java
@Target({ElementType.METHOD, ElementType.TYPE})  // 적용 가능 위치
@Retention(RetentionPolicy.RUNTIME)               // 런타임까지 유지
@Inherited                                         // 자식 클래스에 상속
@Documented                                        // Javadoc에 포함
public @interface MyAnnotation {
    String value() default "";
}
```

`@Retention` 정책은 애노테이션 정보가 언제까지 유지될지를 결정한다:

| 정책 | 유지 범위 | 주요 용도 |
|------|-----------|-----------|
| `SOURCE` | 소스 코드만 | `@Override`, `@SuppressWarnings` |
| `CLASS` | `.class` 파일까지 (기본값) | 바이트코드 분석 도구 |
| `RUNTIME` | JVM 실행 중 | Spring `@Component`, JPA `@Entity` |

리플렉션으로 애노테이션을 읽으려면 반드시 `RetentionPolicy.RUNTIME`이어야 한다. `SOURCE`나 `CLASS`는 런타임에 정보가 사라진다.

### 3-3. 커스텀 애노테이션 정의

애노테이션은 `@interface` 키워드로 정의하고, 속성은 메서드 형태로 선언한다:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Task {
    String description() default "No description";
    int priority() default 0;
}
```

속성에 `default` 값을 지정하면 애노테이션 사용 시 생략 가능하다. 속성이 `value()` 하나뿐이라면 `@Task("설명")` 형태로 축약할 수 있다.

## 4. 리플렉션과 애노테이션 조합

리플렉션과 애노테이션을 함께 사용하면 프레임워크 수준의 동작을 구현할 수 있다. 런타임에 특정 애노테이션이 붙은 메서드를 찾아 자동으로 실행하는 패턴이 대표적이다:

```java
// 사용 측
public class ReportService {

    @Task(description = "월간 보고서 생성", priority = 1)
    public void generateMonthlyReport() { /* ... */ }

    @Task(description = "데이터 정합성 검증", priority = 2)
    public void validateData() { /* ... */ }
}
```

```java
// 프레임워크 측 — @Task 애노테이션이 붙은 메서드를 우선순위 순으로 실행
public class TaskRunner {

    public void run(Object target) throws Exception {
        Class<?> clazz = target.getClass();

        Arrays.stream(clazz.getDeclaredMethods())
            .filter(m -> m.isAnnotationPresent(Task.class))
            .sorted(Comparator.comparingInt(
                m -> m.getAnnotation(Task.class).priority()
            ))
            .forEach(m -> {
                Task task = m.getAnnotation(Task.class);
                System.out.println("실행: " + task.description());
                try {
                    m.invoke(target);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            });
    }
}
```

## 5. 프레임워크 활용 원리

Spring과 JPA가 내부적으로 리플렉션을 사용하는 방식을 이해하면, 프레임워크의 동작이 "마법"처럼 느껴지지 않는다.

**Spring DI**: `@Component`가 붙은 클래스를 클래스패스 스캔으로 찾고, `@Autowired` 필드나 생성자에 `setAccessible(true)` 후 의존성을 주입한다. 이 때문에 `private` 필드에도 주입이 가능하다.

**JPA**: `@Entity` 클래스의 기본 생성자(no-arg constructor)를 리플렉션으로 호출해 인스턴스를 생성한 뒤, `@Column`으로 매핑된 필드에 직접 값을 설정한다. JPA 엔티티에 기본 생성자가 반드시 필요한 이유가 바로 이것이다.

**JUnit**: `@Test`가 붙은 메서드를 리플렉션으로 탐색하고, 각 테스트마다 새 인스턴스를 생성해 실행한다.

## 6. Java 21과 모듈 시스템

Java 9에서 도입된 모듈 시스템(Module System)은 리플렉션 접근에 제약을 추가했다. 모듈이 `opens` 선언 없이 패키지를 닫아두면, 다른 모듈에서 해당 패키지에 `setAccessible(true)`를 호출할 수 없다:

```java
// module-info.java
module com.example.app {
    // 리플렉션 접근을 허용할 패키지 선언
    opens com.example.internal to spring.core;

    // 모든 모듈에 opens — 보안상 권장하지 않음
    opens com.example.model;
}
```

기존 라이브러리가 모듈 선언 없이 동작하지 않을 때는 JVM 실행 시 `--add-opens` 플래그로 일시적으로 열 수 있다:

```bash
java --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.util=ALL-UNNAMED \
     -jar app.jar
```

Spring Boot 3.x는 Jakarta EE 9 기반으로 모듈 시스템과 호환되도록 설계되었으므로, 올바르게 의존성을 구성하면 `--add-opens` 없이 동작한다. 레거시 라이브러리를 사용할 때 이 플래그가 필요해지는 경우가 많다.
