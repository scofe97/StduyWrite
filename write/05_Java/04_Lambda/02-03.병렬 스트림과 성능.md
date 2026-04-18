# 병렬 스트림과 성능

---

> 병렬 스트림은 멀티코어를 활용하는 강력한 도구지만, 잘못 사용하면 순차 코드보다 느리거나 결과가 틀릴 수 있다. 언제 병렬화가 이득이고 언제 오히려 손해인지를 이해하는 것이 핵심이다.

## 병렬 스트림의 내부 동작: ForkJoinPool

`parallelStream()`을 호출하면 스트림 요소를 여러 **청크(chunk)**로 분할하고, 각 청크를 별도 스레드에서 처리한 뒤 결과를 합친다. 이 분할-처리-병합 과정은 **포크/조인 프레임워크(Fork/Join Framework)**가 담당한다.

포크/조인 프레임워크는 분할 정복 알고리즘과 유사하다. 작업을 재귀적으로 작은 서브태스크로 분할(fork)하고, 각 서브태스크의 결과를 합쳐(join) 최종 결과를 만든다. 내부적으로 `ForkJoinPool`을 사용하며, 기본 스레드 수는 `Runtime.getRuntime().availableProcessors()`가 반환하는 값, 즉 CPU 코어 수와 같다.

```java
// 순차 스트림을 병렬로 전환
long sum = LongStream.rangeClosed(1, 1_000_000L)
        .parallel()
        .reduce(0L, Long::sum);

// 병렬 스트림을 다시 순차로 전환
long sum2 = LongStream.rangeClosed(1, 1_000_000L)
        .parallel()
        .sequential() // 마지막 호출이 우선 적용
        .reduce(0L, Long::sum);
```

## Spliterator: 병렬 분할의 핵심

스트림을 병렬로 처리하려면 요소를 효율적으로 나눌 수 있어야 한다. 이 역할을 **Spliterator(분할 반복자)**가 담당한다. Iterator가 단순 순회만 제공하는 반면, Spliterator는 `trySplit()` 메서드로 자신의 일부를 다른 Spliterator에게 떼어줄 수 있다.

자료구조마다 분해 성능이 다르다.

| 자료구조 | 분해성 | 이유 |
|----------|--------|------|
| ArrayList | 우수 | 인덱스로 정확히 절반 분할 가능 |
| LinkedList | 나쁨 | 분할 시 전체 순회 필요 |
| IntStream.range | 우수 | 숫자 범위를 절반으로 나누기 쉬움 |
| Stream.iterate | 나쁨 | 이전 값에 의존하여 독립 분할 불가 |
| HashSet | 보통 | 버킷 기반 분할 가능하나 불균일할 수 있음 |
| TreeSet | 보통 | 균형 트리지만 분할 비용 있음 |

## Stream vs for-loop 성능 비교

스트림이 항상 for-loop보다 느리다는 것은 사실이 아니다. 상황에 따라 결과가 달라진다.

### 기본형 배열: for-loop의 압승

```java
// for-loop: ~0.36ms
int[] ints = new int[500_000];
int m = Integer.MIN_VALUE;
for (int i = 0; i < ints.length; i++) {
    if (ints[i] > m) m = ints[i];
}

// 순차 스트림: ~5.35ms (약 15배 느림)
int m2 = Arrays.stream(ints).reduce(Integer.MIN_VALUE, Math::max);
```

for-loop은 40년간 JIT 컴파일러가 최적화해온 코드 패턴이다. 기본형 배열을 단순 순회할 때는 스트림 파이프라인의 오버헤드(람다 호출, 객체 생성)가 JIT 최적화 이점을 압도한다.

### 래퍼 타입 컬렉션: 차이가 줄어든다

```java
// ArrayList<Integer> 500_000개
// for-loop: ~6.55ms
// 순차 스트림: ~8.33ms (약 1.27배 느림)
```

`ArrayList<Integer>`를 순회하는 비용 자체가 크기 때문에 둘의 성능 차이가 좁혀진다. `Integer`는 힙에 저장된 객체이므로 순회할 때마다 간접 참조(포인터 역참조)가 발생하고, 이 비용이 스트림 오버헤드를 희석시킨다.

### 요소당 계산 비용이 클 때: for-loop의 이점 소멸

```java
// 무거운 계산 함수가 포함된 경우
// for-loop vs 순차 스트림: 거의 동일
Arrays.stream(ints).mapToDouble(Sine::slowSin).reduce(Double.MIN_VALUE, Math::max);
```

요소당 처리 비용(Q)이 크면 순회 비용은 상대적으로 무의미해진다. 전체 비용을 `N * Q`로 보면, Q가 충분히 크면 스트림의 추상화 비용이 사라진다.

### 박싱/언박싱 함정

병렬 스트림에서 성능이 오히려 저하되는 대표적인 원인은 오토박싱이다.

```java
// 느린 병렬 스트림: iterate + boxing 문제
long sum1 = Stream.iterate(1L, i -> i + 1)
        .limit(10_000_000L)
        .parallel()
        .reduce(0L, Long::sum); // ~164ms

// 빠른 병렬 스트림: rangeClosed + 기본형 특화 스트림
long sum2 = LongStream.rangeClosed(1, 10_000_000L)
        .parallel()
        .reduce(0L, Long::sum); // ~1ms
```

`Stream.iterate`가 느린 이유는 두 가지다. 첫째, `Long` 박싱 객체를 생성하므로 언박싱 오버헤드가 발생한다. 둘째, `iterate`는 이전 값에 의존하기 때문에 독립 청크로 분할하기 어렵다. `LongStream.rangeClosed`는 기본형을 직접 다루고 범위를 쉽게 절반으로 나눌 수 있어 병렬 처리에 적합하다.

## 벤치마크 방법론: JMH

마이크로벤치마크(micro-benchmark)는 JVM 워밍업, JIT 컴파일, 가비지 컬렉션 등의 영향을 받아 단순 측정이 부정확하다. 정확한 측정을 위해 **JMH(Java Microbenchmark Harness)**를 사용한다.

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Thread)
public class StreamBenchmark {

    private long N = 10_000_000L;

    @Benchmark
    public long iterativeSum() {
        long result = 0;
        for (long i = 1L; i <= N; i++) result += i;
        return result;
    }

    @Benchmark
    public long parallelRangedSum() {
        return LongStream.rangeClosed(1, N)
                .parallel()
                .reduce(0L, Long::sum);
    }
}
```

JMH는 워밍업 반복과 측정 반복을 분리하고, 여러 포크(fork)에서 실행하여 JIT 최적화 효과를 통제한다. "빠르다"는 주장은 반드시 JMH 결과로 뒷받침해야 한다.

## 병렬 스트림 사용 지침

병렬 스트림을 언제 사용할지 판단하는 기준이다.

**적합한 조건**
- 데이터량이 충분히 크다 (소량 데이터는 스레드 분할 오버헤드가 더 크다)
- 요소당 처리 비용(Q)이 충분히 높다
- 분해하기 좋은 자료구조다 (ArrayList, 배열, IntStream.range 등)
- 연산이 순서에 무관하다

**피해야 할 조건**
- `limit`, `findFirst`처럼 순서 의존적 연산이 포함된 경우 (순차 스트림이 더 빠르다)
- 데이터 소스가 `LinkedList`나 `Stream.iterate`처럼 분할 비용이 큰 경우
- 박싱/언박싱이 발생하는 경우 (기본형 특화 스트림으로 교체)

## 병렬 스트림의 주의사항

### 공유 가변 상태를 피하라

병렬 스트림에서 가장 흔한 실수는 여러 스레드가 공유 변수를 동시에 수정하는 것이다.

```java
// 데이터 레이스(data race) 발생 코드
public class Accumulator {
    public long total = 0;
    public void add(long value) { total += value; } // total += value는 원자적이지 않다
}

Accumulator acc = new Accumulator();
LongStream.rangeClosed(1, 10_000_000L)
        .parallel()
        .forEach(acc::add); // 매 실행마다 다른 결과 반환
```

`total += value`는 읽기-수정-쓰기 세 단계로 구성된 비원자적 연산이다. 여러 스레드가 동시에 실행하면 일부 업데이트가 누락된다. 병렬 스트림에서 올바른 결과를 얻으려면 반드시 **공유 가변 상태를 제거**하고 `reduce` 같은 불변 집계 연산을 사용해야 한다.

```java
// 올바른 방법: reduce는 각 스레드가 독립적으로 처리
long sum = LongStream.rangeClosed(1, 10_000_000L)
        .parallel()
        .reduce(0L, Long::sum);
```

### 스레드 풀 크기를 고려하라

`ForkJoinPool`의 기본 스레드 수는 CPU 코어 수다. I/O 바운드 작업을 병렬 스트림으로 처리하면 스레드가 블로킹되어 다른 병렬 작업까지 지연될 수 있다. I/O 바운드 작업에는 `CompletableFuture`와 커스텀 `Executor`를 사용하는 것이 더 적합하다.
