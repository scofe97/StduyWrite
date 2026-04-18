# 병렬 스트림: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. parallelStream이 오히려 느려지는 조건은 무엇인가

### 왜 이 질문이 중요한가
"병렬은 빠르다"는 오해가 성능 문제를 만드는 가장 흔한 원인 중 하나다. parallelStream이 느려지는 조건을 알아야 올바른 벤치마크를 설계하고 병렬화 결정을 내릴 수 있다.

### 답변
parallelStream이 느려지는 조건은 크게 네 가지다.

첫째, 데이터 크기가 작을 때다. 병렬 처리는 스트림을 서브스트림으로 분할하고(fork), 각 스레드에 작업을 분배하고, 결과를 합치는(join) 오버헤드가 있다. 이 오버헤드가 실제 계산 비용보다 크면 순차 처리가 빠르다. 일반적으로 요소 수가 10,000개 미만이거나 처리 로직이 매우 단순하면 순차 스트림이 낫다.

둘째, 분할 비용이 클 때다. `ArrayList`나 배열은 인덱스 기반으로 O(1)에 분할되지만, `LinkedList`는 분할하려면 전체를 순회해야 한다. `Spliterator.SIZED | SUBSIZED` 특성이 없는 소스는 병렬화 효율이 낮다.

```java
// 분할 효율 좋음
List<Integer> arrayList = new ArrayList<>(data);
arrayList.parallelStream().map(...); // ArrayList: 효율적

// 분할 효율 나쁨
LinkedList<Integer> linked = new LinkedList<>(data);
linked.parallelStream().map(...); // LinkedList: 순차와 차이 없거나 느림
```

셋째, 스레드 간 공유 상태가 있을 때다. 병렬 스트림에서 외부 변수를 변경하면 경쟁 조건이 발생하고, 동기화를 추가하면 병렬성의 이점이 사라진다.

넷째, IO 바운드 작업일 때다. 병렬 스트림은 CPU 코어 수 기반의 ForkJoinPool을 사용한다. IO 대기 시간이 긴 작업(DB 조회, HTTP 요청)에 parallelStream을 쓰면 스레드가 IO를 기다리며 ForkJoinPool을 점유해 다른 병렬 작업을 방해한다. IO 바운드 작업은 `CompletableFuture`와 별도 스레드 풀을 사용해야 한다.

---

## Q2. ForkJoinPool 공유 문제와 커스텀 풀 해결책은 무엇인가

### 왜 이 질문이 중요한가
모든 parallelStream은 JVM 전체에서 공유되는 common ForkJoinPool을 사용한다. 이 사실을 모르면 한 서비스의 병렬 스트림이 다른 서비스의 병렬 처리를 방해하는 문제를 진단하기 어렵다.

### 답변
`ForkJoinPool.commonPool()`은 JVM당 하나 존재하며 `parallelism`이 기본적으로 `Runtime.getRuntime().availableProcessors() - 1`로 설정된다. 모든 `parallelStream()`과 `CompletableFuture`의 기본 실행은 이 풀을 공유한다.

공유 풀의 문제는 실제로 발생한다. 웹 애플리케이션에서 요청 처리 중 parallelStream을 쓰면 여러 요청의 병렬 스트림이 같은 풀을 두고 경쟁한다. 한 요청이 비싼 병렬 처리를 시작하면 다른 요청의 병렬 처리가 지연된다. 또한 blocking 연산(Thread.sleep, IO 대기)이 commonPool 스레드를 점유하면 ForkJoinPool의 work-stealing이 마비된다.

해결책은 커스텀 ForkJoinPool에서 작업을 실행하는 것이다.

```java
// 커스텀 ForkJoinPool에서 parallelStream 실행
ForkJoinPool customPool = new ForkJoinPool(4); // 4개 스레드
try {
    List<Result> results = customPool.submit(() ->
        largeList.parallelStream()
            .map(this::expensiveOperation)
            .collect(Collectors.toList())
    ).get();
} finally {
    customPool.shutdown();
}
```

이 패턴이 동작하는 이유는 `ForkJoinTask`가 현재 스레드가 속한 풀에서 서브태스크를 스케줄하기 때문이다. `customPool.submit()`에서 실행되는 스트림은 customPool의 스레드들을 사용한다.

주의할 점이 있다. 이 동작은 내부 구현에 의존하는 것으로 공식 보장이 아니다. Java 21+의 Virtual Thread 환경에서는 이 패턴이 다르게 동작할 수 있다. 또한 커스텀 풀을 매번 생성하면 풀 생성 비용이 병목이 되므로 풀을 재사용해야 한다.

실무에서는 parallelStream 대신 `CompletableFuture`와 명시적 Executor를 조합하는 방식이 더 투명하고 제어하기 쉽다. parallelStream은 CPU 바운드 작업에서 단순한 경우에만 사용하고, 복잡한 병렬 처리는 명시적 스레드 풀로 관리하는 것이 권장된다.
