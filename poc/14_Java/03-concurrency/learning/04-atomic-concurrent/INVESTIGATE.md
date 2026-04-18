# Atomic과 동시성 컬렉션: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. LongAdder가 AtomicLong보다 빠른 이유는 무엇인가

### 왜 이 질문이 중요한가
카운터, 통계 수집, 메트릭 집계처럼 매우 높은 빈도로 증가 연산이 발생하는 상황에서 AtomicLong과 LongAdder 중 무엇을 선택하느냐는 수십 배의 성능 차이를 만들 수 있다. 내부 동작을 이해해야 올바른 선택을 한다.

### 답변
`AtomicLong`은 단일 long 변수에 CAS(Compare-And-Swap) 연산을 사용한다. CAS는 현재 값이 예상 값과 같을 때만 새 값으로 교체하는 하드웨어 명령어다. 경쟁이 낮을 때는 매우 효율적이지만, 많은 스레드가 동시에 같은 변수에 CAS를 시도하면 대부분의 시도가 실패하고 재시도(spin retry)한다. 스레드 수가 늘수록 충돌 확률이 높아지고 재시도 횟수가 기하급수적으로 증가한다.

`LongAdder`는 이 문제를 분산 카운터 방식으로 해결한다. 내부적으로 하나의 `base` 값과 여러 `Cell` 배열을 유지한다. 각 스레드는 자신에게 할당된 Cell에 독립적으로 값을 더한다. 경쟁이 없을 때는 base에 직접 더하고, 경쟁이 감지되면 동적으로 Cell을 생성해 스레드를 분산시킨다. `sum()`을 호출할 때 base와 모든 Cell의 합을 반환한다.

```java
// 높은 경쟁 환경에서의 성능 차이
AtomicLong atomic = new AtomicLong();
LongAdder adder = new LongAdder();

// 16개 스레드, 각 1,000,000번 증가 — LongAdder가 수 배 빠름
IntStream.range(0, 16).parallel().forEach(i -> {
    for (int j = 0; j < 1_000_000; j++) {
        atomic.incrementAndGet(); // 높은 경쟁, 많은 CAS 실패
        adder.increment();        // 각 스레드가 독립 Cell 사용
    }
});

long atomicResult = atomic.get();
long adderResult = adder.sum(); // 합산 시점에 정확한 합계 반환
```

`LongAdder`의 트레이드오프는 `sum()`이 스냅샷이 아니라는 점이다. `sum()` 실행 중에도 다른 스레드가 Cell을 업데이트할 수 있어 반환값이 정확한 시점의 값이 아닐 수 있다. 따라서 정확한 순간 값이 필요하고 읽기가 쓰기보다 많은 경우는 `AtomicLong`이 적합하고, 쓰기가 압도적으로 많고 최종 합계만 필요한 통계/메트릭 수집은 `LongAdder`가 적합하다.

---

## Q2. ConcurrentHashMap의 size()가 정확하지 않은 이유는 무엇인가

### 왜 이 질문이 중요한가
`ConcurrentHashMap.size()`의 반환값을 신뢰하고 로직을 짜면 예상과 다른 동작을 경험할 수 있다. 이 특성을 이해해야 동시성 환경에서 안전한 컬렉션 사용 패턴을 설계할 수 있다.

### 답변
`ConcurrentHashMap`은 Java 8부터 내부적으로 `LongAdder`와 유사한 분산 카운팅 방식으로 크기를 추적한다. `baseCount`와 `counterCells` 배열을 사용해 각 스레드가 독립적으로 카운트를 업데이트한다. `size()`는 이들의 합을 반환하지만, 이 합산 과정 중에도 다른 스레드가 요소를 추가하거나 제거할 수 있다.

`size()`가 반환하는 값은 메서드 호출 당시의 스냅샷이 아니라 "호출 시점 전후의 어느 순간에 성립했던 크기"다. 즉, 반환된 값이 실제로 존재했던 크기이긴 하지만 `size()` 반환 직후에는 이미 달라져 있을 수 있다.

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 이 패턴은 안전하지 않음 — size()와 실제 상태가 일치하지 않을 수 있음
if (map.size() < MAX_SIZE) {
    map.put(key, value); // size() 확인 후 put 사이에 다른 스레드가 put할 수 있음
}

// 올바른 패턴 — 원자적 연산 사용
map.putIfAbsent(key, value);
map.computeIfAbsent(key, k -> computeValue(k));
```

실무에서 주의할 패턴은 `size() == 0`으로 빈 컬렉션을 확인하는 것이다. `isEmpty()`를 사용해도 마찬가지로 순간적인 상태를 반영한다. 더 신뢰할 수 있는 "empty check" 방법은 `map.isEmpty()`를 확인한 직후 다른 스레드가 요소를 추가할 수 있다는 사실을 항상 인지하는 것이다.

`mappingCount()`(Java 8+)는 `int` 오버플로우 가능성이 있는 `size()` 대신 `long`을 반환하므로 큰 맵에는 `mappingCount()`를 사용하는 것이 좋다. 그러나 정확성 문제는 동일하게 존재한다.

핵심 원칙은 `ConcurrentHashMap`의 크기나 존재 여부를 확인한 뒤 별도의 연산을 수행하는 check-then-act 패턴을 피하고, `putIfAbsent`, `computeIfAbsent`, `compute`, `merge` 같은 원자적 메서드를 사용하는 것이다.
