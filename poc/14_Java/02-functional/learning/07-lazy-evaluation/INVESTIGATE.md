# 지연 평가: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. orElse vs orElseGet 성능 차이의 실질적 영향은 무엇인가

### 왜 이 질문이 중요한가
`orElse`와 `orElseGet`의 차이는 Optional을 다루는 코드에서 가장 자주 등장하는 실수 중 하나다. 기본값 생성 비용이 클 때 잘못된 선택은 불필요한 객체 생성이나 DB 쿼리로 이어진다.

### 답변
`orElse(T other)`는 항상 `other`를 평가한다. Optional이 값을 가지고 있어도 `other` 표현식이 실행된다. 반면 `orElseGet(Supplier<T> supplier)`는 Optional이 비어 있을 때만 Supplier를 호출한다.

```java
// orElse: Optional이 값을 가져도 "expensive" 메서드 호출됨
Optional<String> opt = Optional.of("value");
String result1 = opt.orElse(createExpensiveDefault());      // createExpensiveDefault() 호출됨
String result2 = opt.orElseGet(() -> createExpensiveDefault()); // 호출 안 됨
```

실질적 영향이 큰 경우는 세 가지다. 첫째, 기본값 생성이 DB 조회를 포함할 때다. `findById(id).orElse(repository.findDefault())`처럼 쓰면 값이 있어도 항상 DB를 조회한다. `orElseGet(() -> repository.findDefault())`로 바꿔야 한다.

둘째, 기본값 생성에 부수 효과가 있을 때다. 로그 기록, 카운터 증가, 외부 API 호출 등이 포함된 기본값 생성 로직이 의도치 않게 실행된다.

셋째, 생성 비용이 큰 객체일 때다. `new ArrayList<>(originalList)`처럼 컬렉션을 복사하거나 JSON을 파싱하는 기본값은 불필요하게 실행되면 낭비다.

```java
// 실수하기 쉬운 패턴
User user = userCache.get(id)
    .orElse(userRepository.findById(id)  // Optional이 있어도 DB 쿼리 실행!
        .orElseThrow());

// 올바른 패턴
User user = userCache.get(id)
    .orElseGet(() -> userRepository.findById(id)
        .orElseThrow());
```

단순 상수나 이미 생성된 객체를 기본값으로 쓸 때는 `orElse`가 더 간결하다. 성능 차이도 없고 Supplier 람다 생성 비용조차 없다. 판단 기준은 "기본값 표현식이 부수 효과가 있거나 비싼가"이다.

---

## Q2. 무한 스트림의 실무 활용 사례는 어떤 것이 있는가

### 왜 이 질문이 중요한가
무한 스트림은 학습 예제에서 자주 등장하지만 실무 활용 사례를 모르면 단순한 문법 지식에 그친다. 재시도 로직, 페이지네이션, 시퀀스 생성 등 실제 문제에 적용할 수 있어야 한다.

### 답변
무한 스트림은 `Stream.iterate(seed, f)`, `Stream.generate(supplier)`, `IntStream.range/rangeClosed`의 무한 버전으로 생성한다. Java 9부터 `iterate`에 종료 조건을 추가할 수 있다.

실무 활용 사례 첫 번째는 재시도(retry) 로직이다. 최대 N번까지 시도하고 성공하면 중단하는 패턴을 무한 스트림과 `filter + findFirst`로 표현할 수 있다.

```java
// 최대 5번 재시도, 성공 시 즉시 반환
Optional<Response> response = Stream.iterate(0, i -> i + 1)
    .limit(5)
    .map(attempt -> {
        try { return callExternalApi(); }
        catch (Exception e) { return null; }
    })
    .filter(Objects::nonNull)
    .findFirst();
```

두 번째는 페이지네이션이다. 다음 페이지가 없을 때까지 API를 반복 호출해 전체 데이터를 수집한다.

```java
// 페이지네이션 — 다음 페이지가 없을 때까지 수집
List<Item> allItems = Stream.iterate(
        fetchPage(0),
        page -> !page.isLast(),              // 종료 조건 (Java 9+)
        page -> fetchPage(page.getNumber() + 1)
    )
    .flatMap(page -> page.getContent().stream())
    .collect(Collectors.toList());
```

세 번째는 고유 ID나 시퀀스 번호 생성이다. AtomicLong과 `Stream.generate`를 조합해 스레드 안전한 ID 시퀀스를 만들 수 있다.

```java
AtomicLong counter = new AtomicLong();
Stream<Long> idStream = Stream.generate(counter::incrementAndGet);
```

네 번째는 주기적 작업 스케줄링이다. `Stream.iterate`로 시간을 증가시키며 특정 시점까지의 작업을 생성한다.

주의할 점은 무한 스트림에 `limit()`이나 단락 종단 연산 없이 `collect()`나 `forEach()`를 붙이면 무한 루프가 된다. `sorted()`나 `distinct()` 같은 stateful 중간 연산도 무한 스트림에서는 사용할 수 없다(전체 요소를 메모리에 올려야 하므로 OOM 발생).
