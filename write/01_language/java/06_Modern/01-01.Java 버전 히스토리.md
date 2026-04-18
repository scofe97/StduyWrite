# Java 버전 히스토리

---

> Java는 6개월 주기 릴리스 모델로 전환하면서 빠른 혁신을 도입했고, LTS 버전을 중심으로 실무 생태계가 안정적으로 발전하고 있다.

## 릴리스 모델

Java 9부터 Oracle은 6개월 주기 릴리스 모델을 채택했다. 이전에는 수년에 걸쳐 대규모 기능을 묶어 출시했지만, 이 방식은 릴리스 지연과 예측 불가능성 문제를 낳았다. 새 모델에서는 매 3월과 9월에 새 버전이 나오며, 기능이 준비되면 즉시 포함된다.

*LTS(Long-Term Support)* 버전은 장기 지원을 제공하는 특별 버전이다. 일반 버전은 다음 릴리스까지만 업데이트를 받지만, LTS는 수년간 보안 패치와 버그 수정을 받는다. 실무에서는 Java 8, 11, 17, 21처럼 LTS 버전을 기준으로 마이그레이션 시점을 결정한다.

Oracle JDK와 OpenJDK의 지원 정책이 다르므로, 사용 중인 배포판의 EOL(End of Life) 일정을 반드시 확인해야 한다. Amazon Corretto, Eclipse Temurin, Microsoft Build of OpenJDK 등 다양한 배포판이 LTS에 대한 무료 장기 지원을 제공한다.

## 주요 LTS 버전별 핵심 기능

| 버전 | 출시 | 주요 기능 |
|------|------|----------|
| Java 8 | 2014.03 | Lambda 표현식, Stream API, Optional, java.time, Default Methods |
| Java 11 | 2018.09 | `var` 타입 추론, HTTP Client API, String 신규 메서드, ZGC |
| Java 17 | 2021.09 | Sealed Classes, Pattern Matching for `instanceof`, Records GA, Text Blocks GA |
| Java 21 | 2023.09 | Virtual Threads, Sequenced Collections, Pattern Matching for `switch` GA, Record Patterns GA |

## Java 8: 함수형 프로그래밍의 시작

Java 8은 Java 역사상 가장 혁신적인 릴리스였다. **Lambda 표현식**의 도입으로 함수를 일급 객체처럼 다룰 수 있게 되었고, 익명 클래스로 작성하던 보일러플레이트 코드를 대폭 줄였다.

**Stream API**는 컬렉션을 선언적으로 처리하는 방식을 제공한다. `filter`, `map`, `reduce` 같은 연산을 체이닝하여 데이터 파이프라인을 구성할 수 있으며, 병렬 스트림으로 멀티코어 활용도 쉬워졌다.

**Optional**은 `null` 처리를 명시적으로 만들기 위해 도입되었다. `NullPointerException`을 방어하는 코드를 줄이고, 값이 없을 수 있음을 타입 시스템에서 표현한다. `java.time` 패키지는 Joda-Time을 참고하여 불변(immutable) 날짜/시간 API를 제공했고, 기존 `Date`, `Calendar` 클래스의 설계 결함을 해결했다.

```java
// Java 8 Lambda + Stream + Optional
List<String> names = List.of("Alice", "Bob", "Charlie", "David");

Optional<String> first = names.stream()
        .filter(name -> name.startsWith("C"))
        .findFirst();

first.ifPresent(name -> System.out.println("Found: " + name));
```

## Java 11: 모던 Java의 기준선

Java 11은 Java 8 이후 많은 팀이 채택한 첫 LTS로, 실무의 마이그레이션 기준선 역할을 했다. `var` 키워드는 지역 변수의 타입 추론을 가능하게 하여 장황한 제네릭 타입 선언을 줄인다.

**HTTP Client API**가 표준 라이브러리에 포함되었다. Java 9에서 인큐베이터로 도입된 이 API는 HTTP/2와 WebSocket을 지원하며, 동기/비동기 방식을 모두 제공한다. 기존에 Apache HttpClient나 OkHttp 같은 외부 라이브러리에 의존하던 기본 HTTP 통신을 표준 API로 처리할 수 있게 되었다.

String 클래스에 `isBlank()`, `strip()`, `lines()`, `repeat()` 등 유용한 메서드가 추가되었다. `strip()`은 `trim()`과 달리 유니코드 공백 문자를 올바르게 처리한다.

```java
// Java 11 String API
String text = "  Hello World  \n  Next Line  ";

text.lines()
        .map(String::strip)
        .filter(line -> !line.isBlank())
        .forEach(System.out::println);
```

## Java 17: 현대적 타입 시스템

Java 17은 Java 11 이후 많은 프레임워크(Spring Boot 3.x 등)의 최소 요구 버전이 된 LTS다. **Sealed Classes**는 상속 계층을 명시적으로 제한한다. `permits` 키워드로 허용된 서브클래스만 상속할 수 있으므로, 컴파일러가 모든 가능한 하위 타입을 알 수 있다.

**Pattern Matching for `instanceof`**는 타입 검사와 캐스팅을 한 번에 처리한다. 기존에 `instanceof` 검사 후 별도로 캐스팅하던 패턴을 한 줄로 압축한다. **Records**는 데이터 캐리어 클래스의 보일러플레이트를 제거한다. `equals()`, `hashCode()`, `toString()`, 생성자, getter를 자동으로 생성한다.

```java
// Java 17 Sealed Classes + Pattern Matching
sealed interface Shape permits Circle, Rectangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double width, double height) implements Shape {}

double area(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
    };
}
```

## Java 21: 동시성 패러다임 전환

Java 21은 현재 최신 LTS로, **Virtual Threads**가 가장 중요한 기능이다. 기존 플랫폼 스레드(OS 스레드에 1:1 매핑)는 생성 비용이 크고 블로킹 I/O에서 OS 스레드를 점유하는 문제가 있었다. Virtual Threads는 JVM이 관리하는 경량 스레드로, 수백만 개를 생성할 수 있고 블로킹 I/O에서 캐리어 스레드를 반납하여 효율적으로 스케줄링된다.

**Sequenced Collections**는 `List`, `LinkedHashSet`, `LinkedHashMap` 등 순서가 있는 컬렉션에 일관된 인터페이스를 부여한다. `getFirst()`, `getLast()`, `reversed()` 메서드를 공통으로 사용할 수 있게 되었다. Pattern Matching for `switch`와 Record Patterns가 GA(General Availability)로 확정되어 실무 코드에 안전하게 적용할 수 있다.

```java
// Java 21 Virtual Threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i ->
        executor.submit(() -> {
            Thread.sleep(Duration.ofMillis(100));
            return i;
        })
    );
}
```

## 마이그레이션 고려사항

Java 9에서 도입된 **모듈 시스템(JPMS)**은 클래스패스 기반 코드와의 호환성 문제를 야기할 수 있다. 대부분의 라이브러리가 unnamed module로 동작하지만, JDK 내부 API에 대한 리플렉션 접근은 `--add-opens` 플래그가 필요하다.

Java 버전이 올라갈수록 **deprecated API가 제거**된다. `Thread.stop()`, `SecurityManager`, `Applet`, `RMI Activation` 등 오래된 API가 삭제되었으므로, 마이그레이션 전 `jdeprscan` 도구로 사용 중인 deprecated API를 확인해야 한다. `--release` 플래그와 함께 빌드하면 대상 버전의 API 제한을 컴파일 타임에 검증할 수 있다.
