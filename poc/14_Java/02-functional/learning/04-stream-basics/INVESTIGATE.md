# 스트림 기초: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Stream이 일회용인 설계 이유는 무엇인가

### 왜 이 질문이 중요한가
Stream을 재사용하려다 `IllegalStateException`을 만나는 것은 흔한 실수다. 이 제약이 단순한 구현 한계인지 의도적 설계인지를 이해해야 스트림 파이프라인을 올바르게 설계할 수 있다.

### 답변
Stream이 일회용인 것은 의도적 설계다. Stream은 데이터 소스(컬렉션, 파일, 네트워크 등)에 대한 파이프라인 뷰(view)이지 데이터를 복사해 담는 컨테이너가 아니다. 파이프라인을 한 번 소비(terminate)하면 내부 소스 이터레이터가 끝까지 진행된 상태가 되고, 이 이터레이터를 재설정하는 일반적인 방법이 없다.

일회용 설계는 메모리 효율과 관련이 있다. 스트림이 모든 요소를 메모리에 유지한다면 재사용이 가능하지만 거대한 데이터셋(파일 스트림, 무한 스트림)에는 적용할 수 없다. 일회용 모델은 처리된 요소를 즉시 버릴 수 있어 메모리 사용량을 최소화한다.

```java
Stream<String> stream = list.stream();
stream.forEach(System.out::println); // 정상

stream.forEach(System.out::println); // IllegalStateException: stream has already been operated upon or closed

// 재사용이 필요하면 매번 새 Stream을 생성
Supplier<Stream<String>> streamSupplier = list::stream;
streamSupplier.get().forEach(System.out::println);
streamSupplier.get().filter(s -> s.length() > 3).forEach(System.out::println);
```

네트워크 소켓이나 파일에서 읽는 스트림은 본질적으로 재사용 불가능하다. 스트림 API가 컬렉션과 이런 IO 소스를 동일한 인터페이스로 처리하려면 가장 제약이 강한 쪽(일회용)에 맞춰야 한다. 이것이 일관성 있는 API를 위한 설계 절충이다.

실무에서는 동일한 데이터에 여러 스트림 연산을 적용해야 할 때 `Supplier<Stream<T>>`를 필드나 지역 변수로 보관하거나, 중간 결과를 컬렉션으로 수집 후 다시 스트림을 열거나, `stream.peek()`으로 사이드 이펙트를 끼워넣는 방식을 사용한다. 마지막 방법은 디버깅 용도로는 유용하지만 프로덕션 코드에서는 피해야 한다.

---

## Q2. 중간 연산의 지연 평가(lazy evaluation)가 실무에서 주는 이점은 무엇인가

### 왜 이 질문이 중요한가
지연 평가는 스트림 성능의 핵심이다. 이를 이해하지 못하면 불필요한 연산을 포함한 파이프라인을 작성하거나, 지연 평가가 주는 최적화 기회를 놓친다.

### 답변
스트림의 중간 연산(`filter`, `map`, `flatMap`, `sorted`, `distinct` 등)은 즉시 실행되지 않는다. 종단 연산(`collect`, `forEach`, `findFirst`, `count` 등)이 호출될 때 파이프라인이 한꺼번에 실행된다. 각 요소는 파이프라인 전체를 통과한 뒤 다음 요소로 넘어가는 방식(vertical/depth-first 실행)으로 처리된다.

```java
// 지연 평가 확인: 아래 코드에서 몇 번의 map과 filter가 실행될까?
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

Optional<Integer> result = numbers.stream()
    .filter(n -> { System.out.println("filter: " + n); return n % 2 == 0; })
    .map(n -> { System.out.println("map: " + n); return n * n; })
    .filter(n -> n > 10)
    .findFirst(); // 종단 연산

// 출력: filter 1, filter 2, map 2, filter 4(4>10? false), filter 3, ...filter 4, map 4, filter(16>10? true) → 멈춤
// 전체 10개 요소를 처리하지 않음!
```

지연 평가의 실무 이점은 세 가지다. 첫째, 단락(short-circuit) 최적화다. `findFirst()`, `anyMatch()`, `limit()` 같은 연산과 결합하면 조건을 만족하는 첫 요소를 찾자마자 나머지 처리를 중단한다. 수백만 건의 데이터에서 첫 번째 조건 만족 요소를 찾을 때 전체를 순회하지 않는다.

둘째, 무한 스트림이 가능하다. `Stream.iterate()`나 `Stream.generate()`로 무한한 요소를 생성하는 스트림을 만들고 `limit()`으로 원하는 만큼만 가져올 수 있다.

```java
// 무한 스트림 + 지연 평가
Stream.iterate(0, n -> n + 1)
    .filter(n -> n % 7 == 0)
    .limit(10)
    .forEach(System.out::println); // 0, 7, 14, ... 63 — 무한 루프 없음
```

셋째, 연산 융합(operation fusion)이다. JVM의 스트림 구현은 여러 연산을 하나의 패스로 합칠 수 있다. `filter().map()`은 각 요소에 대해 filter와 map을 연속 적용하는 단일 루프로 실행되어 중간 컬렉션 생성 없이 처리한다.

주의할 점은 `sorted()`와 `distinct()`는 stateful 중간 연산으로 지연 평가의 혜택을 제한적으로만 받는다. `sorted()`는 전체 요소를 메모리에 모아야 정렬할 수 있고, `distinct()`는 이미 본 요소를 추적하는 상태를 유지해야 한다.
