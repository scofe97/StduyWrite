# Virtual Thread 기초: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Virtual Thread를 CPU-bound 작업에 쓰면 안 되는 이유는 무엇인가

### 왜 이 질문이 중요한가
Virtual Thread가 "모든 스레드 문제를 해결한다"고 오해하면 CPU-bound 작업에 무분별하게 적용해 오히려 성능이 나빠진다. Virtual Thread의 설계 목적과 한계를 명확히 알아야 올바른 적용 범위를 판단할 수 있다.

### 답변
Virtual Thread는 IO-bound 작업의 스레드 블로킹 비용을 없애기 위해 설계되었다. JDK가 관리하는 소수의 캐리어 스레드(Carrier Thread, 기본값: CPU 코어 수)가 수백만 개의 Virtual Thread를 번갈아 실행한다. Virtual Thread가 IO 대기로 블록되면 캐리어 스레드에서 분리(unmount)되어 캐리어 스레드가 다른 Virtual Thread를 실행한다.

CPU-bound 작업에 Virtual Thread를 쓰면 안 되는 이유는 이 설계 때문이다. CPU-bound 작업은 블록되지 않고 계속 CPU를 사용한다. Virtual Thread가 블록되지 않으면 캐리어 스레드에서 분리되지 않고 계속 점유한다. 결국 CPU 코어 수만큼의 Virtual Thread가 모든 캐리어 스레드를 점유하고 나머지 Virtual Thread들은 대기한다.

```java
// CPU-bound 작업 — Virtual Thread의 이점 없음
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Long>> futures = IntStream.range(0, 1000)
        .mapToObj(i -> executor.submit(() -> {
            // CPU를 계속 사용하는 작업
            return fibonacci(45); // 블로킹 없음 → 캐리어 스레드 점유
        }))
        .toList();
    // 결과: 코어 수만큼만 병렬 실행, 나머지는 대기
    // 기존 ForkJoinPool(cores) 대비 오버헤드만 추가
}

// CPU-bound 작업의 올바른 도구 — ForkJoinPool 또는 고정 스레드 풀
ExecutorService pool = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors()
);
```

추가로 Virtual Thread는 스택 메모리를 힙에서 동적으로 할당하므로 생성 비용은 낮지만 스케줄링 오버헤드가 완전히 없는 것은 아니다. CPU-bound 작업 수천 개를 Virtual Thread로 만들면 스케줄링 오버헤드가 실제 처리 시간보다 커질 수 있다.

---

## Q2. 기존 스레드 풀 코드를 Virtual Thread로 마이그레이션할 때 주의점은 무엇인가

### 왜 이 질문이 중요한가
Virtual Thread 마이그레이션은 단순히 `newFixedThreadPool`을 `newVirtualThreadPerTaskExecutor`로 바꾸는 것이 아니다. 기존 코드의 가정들이 Virtual Thread에서 맞지 않는 경우가 많아 조용한 성능 저하나 버그가 발생한다.

### 답변
마이그레이션 시 확인해야 할 주의점은 다섯 가지다.

첫째, 스레드 풀 크기 기반 로직이다. 기존 코드에서 `ThreadPoolExecutor`의 스레드 수로 동시성을 제어했다면(`corePoolSize=10` → 동시 DB 연결 10개 제한), Virtual Thread로 전환하면 이 제한이 사라진다. `Executors.newVirtualThreadPerTaskExecutor()`는 작업마다 새 Virtual Thread를 만들어 동시 DB 연결이 폭발적으로 늘어날 수 있다.

```java
// 기존: 스레드 풀 크기로 DB 연결 수 암묵적 제한
ExecutorService pool = Executors.newFixedThreadPool(10); // 최대 10 연결

// Virtual Thread 전환 후: 연결 수 무제한 → DB 연결 풀 고갈
ExecutorService vtPool = Executors.newVirtualThreadPerTaskExecutor();

// 올바른 마이그레이션: Semaphore로 명시적 동시성 제한
Semaphore semaphore = new Semaphore(10);
ExecutorService vtPool = Executors.newVirtualThreadPerTaskExecutor();
// 각 작업에서:
semaphore.acquire();
try { doDbWork(); } finally { semaphore.release(); }
```

둘째, `synchronized` 블록의 Pinning 문제다. Virtual Thread가 `synchronized` 블록 안에서 블록되면 캐리어 스레드에서 분리되지 못하고 캐리어 스레드를 점유(pin)한다. 라이브러리 코드에 `synchronized`가 많으면 Virtual Thread의 이점이 사라진다. Java 21 기준 JVM 옵션 `-Djdk.tracePinnedThreads=full`로 Pinning 발생을 추적할 수 있다.

셋째, ThreadLocal 오용이다. Virtual Thread마다 독립적인 `ThreadLocalMap`이 생성된다. 수백만 개의 Virtual Thread가 생성되면 ThreadLocal 값이 많은 경우 메모리 압박이 심해진다. `ScopedValue`로 전환을 고려해야 한다.

넷째, 스레드 이름과 모니터링이다. Virtual Thread는 기본적으로 빈 이름을 가진다. 기존에 스레드 이름으로 로그를 추적하는 시스템이라면 Virtual Thread에 명시적 이름을 부여해야 한다.

```java
Thread.ofVirtual().name("vt-worker-", 0).factory(); // 이름 있는 Virtual Thread
```

다섯째, try-with-resources 방식의 ExecutorService 사용이다. Java 21+에서 `ExecutorService`는 `AutoCloseable`을 구현해 `close()`가 모든 작업 완료를 기다린다. 기존의 `shutdown() + awaitTermination()` 패턴을 `try(var exec = ...)` 패턴으로 단순화할 수 있다.
