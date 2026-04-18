# 함수형 인터페이스: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 표준 함수형 인터페이스만으로 충분한가, 커스텀이 필요한 경우는 언제인가

### 왜 이 질문이 중요한가
java.util.function 패키지의 표준 인터페이스를 언제 쓰고 언제 커스텀을 만들지 판단하지 못하면 불필요하게 복잡한 타입을 도입하거나 반대로 중요한 의미론적 정보를 잃는다. 이 판단 기준은 API 설계 역량과 직결된다.

### 답변
표준 함수형 인터페이스(`Function<T,R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`, `BiFunction<T,U,R>` 등)는 대부분의 경우를 커버한다. 하지만 커스텀 함수형 인터페이스가 필요한 경우는 크게 세 가지다.

첫째, checked exception을 던져야 할 때다. 표준 인터페이스는 checked exception을 선언하지 않으므로 IOException이나 SQLException을 던지는 로직을 `Function`에 담으면 try-catch로 감싸야 한다. 이때 커스텀 인터페이스를 만들면 코드가 깔끔해진다.

```java
// checked exception을 허용하는 커스텀 인터페이스
@FunctionalInterface
public interface ThrowingFunction<T, R> {
    R apply(T t) throws Exception;
}

// 표준 Function으로 래핑하는 유틸
public static <T, R> Function<T, R> wrap(ThrowingFunction<T, R> f) {
    return t -> {
        try { return f.apply(t); }
        catch (Exception e) { throw new RuntimeException(e); }
    };
}
```

둘째, 의미론적 명확성이 필요할 때다. `Function<String, String>`은 어떤 변환인지 알 수 없지만 `EmailNormalizer`나 `PasswordHasher`처럼 이름 있는 인터페이스는 의도를 명시한다. 특히 같은 시그니처의 함수가 여러 개 필요하고 이들을 타입으로 구분해야 할 때 커스텀이 필수다.

셋째, 기본형(primitive) 특화가 필요할 때다. 표준 패키지는 `IntFunction`, `ToLongFunction` 등 기본형 특화를 제공하지만 모든 조합을 커버하지는 않는다. 성능이 중요한 루프에서 박싱/언박싱을 피하려면 커스텀 기본형 특화 인터페이스가 필요하다.

반대로 커스텀을 만들면 안 되는 경우도 있다. 단순히 파라미터 이름을 문서화하고 싶다는 이유만으로 커스텀을 만들면 표준 API와의 상호운용성이 떨어진다. 예컨대 `Comparator`를 받는 API에 커스텀 `MyComparator`를 전달할 수 없다.

---

## Q2. Predicate 체이닝과 단락 평가(short-circuit evaluation)는 어떻게 동작하는가

### 왜 이 질문이 중요한가
Predicate 체이닝은 복잡한 조건 로직을 선언적으로 표현할 수 있게 해준다. 단락 평가 동작을 모르면 부수 효과가 있는 Predicate를 체이닝할 때 예상치 못한 결과가 나올 수 있다.

### 답변
`Predicate<T>`는 `and()`, `or()`, `negate()` 디폴트 메서드를 제공해 체이닝을 지원한다. `and()`와 `or()`는 각각 `&&`와 `||`의 단락 평가를 따른다.

```java
Predicate<String> notNull = s -> s != null;
Predicate<String> notEmpty = s -> !s.isEmpty();
Predicate<String> longerThan5 = s -> s.length() > 5;

// and()는 앞의 Predicate가 false면 뒤를 실행하지 않음
Predicate<String> valid = notNull.and(notEmpty).and(longerThan5);
// null 입력 시: notNull → false → notEmpty, longerThan5 실행 안 됨

// or()는 앞의 Predicate가 true면 뒤를 실행하지 않음
Predicate<String> acceptable = notNull.or(s -> "default".equals(s));
```

단락 평가가 실무에서 중요한 이유는 Predicate 안에 DB 조회나 외부 API 호출 같은 비싼 연산이 있을 때다. 저렴한 검사를 앞에, 비싼 검사를 뒤에 배치하면 성능을 최적화할 수 있다.

`Predicate.not()` 정적 메서드(Java 11+)는 메서드 참조를 부정할 때 유용하다.

```java
// Java 11+ Predicate.not() 활용
List<String> result = list.stream()
    .filter(Predicate.not(String::isEmpty))
    .collect(Collectors.toList());
```

주의할 점은 `and()`와 `or()`가 새로운 Predicate 인스턴스를 반환한다는 것이다. 체이닝이 길어질수록 Predicate 객체 체인이 생기고, 극단적으로 많은 체이닝은 스택 깊이를 소모한다. 수백 개의 Predicate를 체이닝해야 한다면 `Stream.of(...).reduce(p -> true, Predicate::and)` 패턴을 쓰기보다 for 루프가 더 효율적일 수 있다.
