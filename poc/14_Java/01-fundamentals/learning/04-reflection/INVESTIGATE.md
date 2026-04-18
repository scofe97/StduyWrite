# 리플렉션: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 리플렉션 성능 비용과 프레임워크의 최적화 전략

### 왜 이 질문이 중요한가
Spring, Jackson, JPA 등 현대 자바 프레임워크는 모두 리플렉션을 기반으로 동작한다. 그런데 "리플렉션은 느리다"는 통념과 "Spring은 충분히 빠르다"는 현실 사이의 간격을 이해하지 못하면 불필요한 최적화를 하거나 실제 병목을 놓친다.

### 답변

리플렉션의 성능 비용은 세 가지 층위에서 발생한다. 첫째, `Class.forName()`이나 `getDeclaredMethods()` 같은 메타데이터 탐색 비용이다. 이는 JVM이 클래스 파일을 파싱하고 메서드 정보를 구성하는 작업이다. 둘째, `Method.invoke()` 호출 비용이다. 일반 메서드 호출은 JIT가 인라인화하여 실질적으로 0에 가까운 비용인 반면, `Method.invoke()`는 JIT 최적화 대상이 아니고 인자 배열 생성, 타입 검사, 접근 권한 확인 등의 오버헤드가 있다. 셋째, JIT 최적화 방해다. 일반 코드는 JIT가 호출 패턴을 분석해 인라인화, 메서드 특화 등을 적용하지만 리플렉션 호출은 런타임에야 어떤 메서드가 호출될지 알기 때문에 이런 최적화가 불가능하다.

프레임워크들은 이 비용을 감당하기 위해 두 가지 주요 전략을 쓴다. 첫 번째는 시작 시점에 일괄 처리 후 캐싱이다. Spring은 애플리케이션 시작 시 `BeanDefinition`을 구성하면서 리플렉션으로 클래스를 스캔하고, 결과를 캐시에 저장한다. 런타임 요청 처리 시에는 이미 캐시된 메타데이터를 사용하므로 리플렉션 비용이 없다.

```java
// Spring 내부 캐싱 패턴 (단순화)
private final Map<Class<?>, List<Method>> methodCache = new ConcurrentHashMap<>();

public List<Method> getAnnotatedMethods(Class<?> clazz, Class<? extends Annotation> ann) {
    return methodCache.computeIfAbsent(clazz, c ->
        Arrays.stream(c.getDeclaredMethods())
              .filter(m -> m.isAnnotationPresent(ann))
              .collect(toList())
    );
}
```

두 번째 전략은 코드 생성이다. Jackson은 처음 타입을 직렬화할 때 리플렉션으로 필드를 분석한 뒤, 해당 타입 전용 직렬화 코드를 바이트코드로 생성(cglib, ASM 사용)하여 이후 호출에서 일반 메서드 호출처럼 동작하게 만든다. Spring Data JPA도 리포지토리 인터페이스에 대한 구현체를 시작 시점에 프록시로 생성한다. Java 9+ 모듈 시스템에서는 `opens` 선언 없이 내부 패키지에 대한 리플렉션이 차단되므로 `module-info.java`에 명시적 허가가 필요하다는 점도 알아 두어야 한다.

---

## Q2. 모듈 시스템이 리플렉션에 미친 영향

### 왜 이 질문이 중요한가
Java 9 JPMS(Java Platform Module System) 도입 이후 기존 리플렉션 기반 코드가 `InaccessibleObjectException`으로 깨지는 사례가 많다. 이를 이해하지 못하면 마이그레이션 시 원인 불명의 에러를 만나게 된다.

### 답변

Java 8까지 리플렉션은 `setAccessible(true)`만 호출하면 어떤 클래스의 어떤 필드나 메서드든 접근할 수 있었다. 이는 캡슐화를 완전히 무력화하는 방식이었지만, 프레임워크들이 광범위하게 활용했다.

Java 9 모듈 시스템은 이 관계를 바꿨다. 모듈은 자신이 공개(`exports`)하지 않은 패키지에 대한 외부 접근을 차단한다. 리플렉션도 예외가 아니다. `exports`된 패키지의 public 멤버는 접근 가능하지만, `exports`되지 않은 패키지나 비공개 멤버에 접근하려면 해당 패키지가 `opens`되어 있어야 한다.

```
// module-info.java
module my.app {
    // exports는 컴파일 타임 public API 공개
    exports com.example.api;

    // opens는 런타임 리플렉션 허가 (Jackson, Spring이 필요로 함)
    opens com.example.domain to com.fasterxml.jackson.databind;

    // 모든 모듈에 opens (비추천 — 특정 모듈에만 열어주는 것이 원칙)
    opens com.example.dto;
}
```

실무에서 자주 마주치는 문제는 두 가지다. 첫째, Jackson이 DTO의 private 필드를 직렬화하려 할 때 `InaccessibleObjectException` 발생이다. 해결책은 `module-info.java`에 `opens com.example.dto to com.fasterxml.jackson.databind`를 추가하거나, DTO를 Record나 public getter가 있는 클래스로 변경하는 것이다. 둘째, Spring이 `@Autowired` private 필드에 주입하려 할 때 같은 에러가 발생한다. 생성자 주입 방식은 public 생성자를 호출하므로 이 문제가 없어 모듈 시스템과 더 호환적이다. JVM 시작 옵션 `--add-opens`로 임시 우회도 가능하지만 이는 모듈 시스템의 취지를 무력화하는 방법이라 장기적 해결책이 아니다.
