# 스트림 수집: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. groupingBy 다운스트림 수집기 조합 패턴은 어떻게 활용하는가

### 왜 이 질문이 중요한가
`groupingBy`는 단순 그룹화를 넘어 다운스트림 수집기와 조합하면 SQL의 GROUP BY + 집계 함수 수준의 표현력을 갖는다. 이 패턴을 모르면 스트림 결과를 컬렉션으로 수집한 뒤 다시 루프를 돌리는 비효율적인 코드를 작성하게 된다.

### 답변
`Collectors.groupingBy(classifier, downstream)`의 두 번째 인수는 각 그룹에 적용할 수집기다. 이를 통해 단일 스트림 파이프라인으로 복잡한 집계를 표현할 수 있다.

```java
record Order(String customer, String category, int amount) {}

List<Order> orders = List.of(
    new Order("Alice", "FOOD", 100),
    new Order("Alice", "BOOK", 200),
    new Order("Bob",   "FOOD", 150),
    new Order("Bob",   "FOOD", 50)
);

// 고객별 카테고리별 주문 수
Map<String, Map<String, Long>> countByCustomerAndCategory = orders.stream()
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.groupingBy(Order::category, Collectors.counting())
    ));

// 고객별 총 주문 금액
Map<String, Integer> totalByCustomer = orders.stream()
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.summingInt(Order::amount)
    ));

// 고객별 최대 주문 금액
Map<String, Optional<Order>> maxByCustomer = orders.stream()
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.maxBy(Comparator.comparingInt(Order::amount))
    ));

// 고객별 카테고리 목록 (중복 제거)
Map<String, Set<String>> categoriesByCustomer = orders.stream()
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.mapping(Order::category, Collectors.toSet())
    ));
```

`Collectors.mapping()`은 다운스트림 수집기에 적용하기 전 요소를 변환하는 어댑터다. `Collectors.collectingAndThen()`은 수집 완료 후 결과를 변환한다. 이 두 가지를 조합하면 표현력이 크게 높아진다.

```java
// 고객별 주문을 불변 리스트로 수집
Map<String, List<Order>> ordersByCustomer = orders.stream()
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.collectingAndThen(
            Collectors.toList(),
            Collections::unmodifiableList
        )
    ));
```

Java 16+에서는 `Collectors.teeing()`으로 두 수집기를 병렬 적용 후 결과를 합칠 수 있다. 한 번의 스트림 순회로 두 가지 집계를 동시에 수행하는 패턴이다.

---

## Q2. reduce와 collect의 병렬 안전성 차이는 무엇인가

### 왜 이 질문이 중요한가
`parallelStream()`을 쓸 때 `reduce`와 `collect`를 잘못 선택하면 결과가 틀리거나 성능이 오히려 나빠진다. 이 차이를 이해하는 것은 병렬 스트림을 올바르게 사용하는 전제 조건이다.

### 답변
`reduce`는 불변 축약(immutable reduction)을 수행한다. 각 단계에서 새 값을 생성하며 기존 값을 수정하지 않는다. 병렬 실행 시 스트림이 여러 서브스트림으로 분할되고, 각 서브스트림이 독립적으로 reduce를 수행한 뒤 부분 결과를 combiner로 합친다.

```java
// reduce: 올바른 병렬 사용 (덧셈은 결합 법칙 성립)
int sum = numbers.parallelStream()
    .reduce(0, Integer::sum); // 안전

// reduce로 문자열 연결 — 병렬에서 비효율적
String joined = strings.parallelStream()
    .reduce("", String::concat); // 결과는 맞지만 성능 최악 (O(n²) 문자 복사)
```

`collect`는 가변 축약(mutable reduction)을 수행한다. 각 스레드가 로컬 컨테이너(예: `ArrayList`)를 만들어 요소를 추가하고, 마지막에 컨테이너들을 합친다. 이 방식은 새 객체를 계속 생성하는 `reduce`보다 훨씬 효율적이다.

```java
// collect: 병렬에서 효율적인 문자열 수집
String joined = strings.parallelStream()
    .collect(Collectors.joining()); // 각 스레드가 StringBuilder 사용 후 합침

// ArrayList 수집
List<String> result = strings.parallelStream()
    .collect(Collectors.toList()); // 각 스레드가 로컬 리스트 생성 후 합침
```

병렬 안전성의 핵심 요건은 `collect`의 경우 각 스레드의 컨테이너가 독립적이어야 하고 합치기(combiner)가 올바르게 구현되어야 한다는 것이다. `Collectors.toList()`같은 표준 수집기는 이미 병렬 안전하다. 커스텀 `Collector`를 만들 때 `CONCURRENT` 특성을 잘못 설정하면 동시성 버그가 발생한다.

`reduce`를 병렬로 사용할 때는 연산이 결합 법칙(associativity)과 항등원(identity element)을 만족해야 한다. 뺄셈이나 나눗셈은 결합 법칙이 성립하지 않아 병렬 reduce에서 결과가 달라진다.

```java
// 잘못된 reduce — 병렬에서 결과 달라짐
int wrong = numbers.parallelStream()
    .reduce(0, (a, b) -> a - b); // 뺄셈은 결합 법칙 불성립
```
