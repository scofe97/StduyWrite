# 생산자-소비자 패턴: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. synchronized와 ReentrantLock의 선택 기준은 무엇인가

### 왜 이 질문이 중요한가
`synchronized`는 단순하지만 제한적이고, `ReentrantLock`은 강력하지만 복잡하다. 언제 어떤 것을 쓸지 명확한 기준 없이 선택하면 불필요하게 복잡한 코드나 기능 부족 중 하나를 겪는다.

### 답변
`synchronized`를 선택하는 경우는 간단한 상호 배제가 필요하고 추가 기능이 필요 없을 때다. `synchronized`는 코드가 간결하고, JVM이 직접 지원해 JIT 최적화(biased locking, adaptive spinning)의 혜택을 잘 받으며, 예외 발생 시 자동으로 락을 해제해 실수를 줄인다.

`ReentrantLock`을 선택하는 경우는 다음 기능 중 하나라도 필요할 때다.

첫째, 타임아웃 락 획득이 필요한 경우다. `tryLock(time, unit)`으로 지정 시간 내에 락을 얻지 못하면 포기하는 로직을 구현할 수 있다.

```java
ReentrantLock lock = new ReentrantLock();

if (lock.tryLock(500, TimeUnit.MILLISECONDS)) {
    try { doWork(); }
    finally { lock.unlock(); }
} else {
    handleTimeout();
}
```

둘째, 인터럽트 가능한 락 획득이 필요한 경우다. `lockInterruptibly()`는 대기 중에 인터럽트를 받으면 `InterruptedException`을 던진다. `synchronized`는 인터럽트를 무시하고 계속 대기한다.

셋째, 공정성(fairness) 제어가 필요한 경우다. `new ReentrantLock(true)`로 공정 락을 만들면 대기 시간이 가장 긴 스레드가 먼저 락을 획득한다. `synchronized`는 비공정(non-fair)이라 스레드 기아(starvation)가 발생할 수 있다. 단, 공정 락은 처리량(throughput)이 낮아지는 트레이드오프가 있다.

넷째, 여러 조건 변수가 필요한 경우다. `lock.newCondition()`으로 하나의 락에 여러 독립적인 Condition을 만들 수 있다. `synchronized`는 하나의 조건 변수(`wait/notify`)만 지원한다.

```java
// 여러 조건 변수 활용 — 생산자-소비자
ReentrantLock lock = new ReentrantLock();
Condition notFull  = lock.newCondition();
Condition notEmpty = lock.newCondition();

// 생산자: 가득 찼을 때만 notFull 대기
// 소비자: 비었을 때만 notEmpty 대기
// synchronized는 notifyAll()이 생산자와 소비자 모두 깨워 불필요한 경쟁 발생
```

`ReentrantLock`을 쓸 때 반드시 `try-finally`로 `unlock()`을 보장해야 한다. 이 점이 `synchronized`에 비해 실수 가능성이 높은 부분이다.

---

## Q2. BlockingQueue 구현체별 특성과 선택 기준은 무엇인가

### 왜 이 질문이 중요한가
생산자-소비자 패턴의 핵심 자료구조인 `BlockingQueue`는 구현체마다 성능, 용량, 공정성이 크게 다르다. 잘못된 구현체 선택은 메모리 고갈, 처리량 저하, 불공정한 처리로 이어진다.

### 답변
주요 `BlockingQueue` 구현체의 특성을 비교하면 다음과 같다.

`ArrayBlockingQueue`는 고정 크기 배열 기반이다. 용량을 반드시 지정해야 하고, 단일 ReentrantLock으로 생산자와 소비자를 모두 동기화한다. 공정 모드를 선택할 수 있다. 메모리 사용량이 예측 가능하고, 배압(backpressure)을 자연스럽게 적용하기 좋다. 생산자와 소비자가 같은 락을 공유하므로 높은 처리량이 필요할 때는 차선책이다.

`LinkedBlockingQueue`는 선택적으로 용량을 지정할 수 있다(기본값: `Integer.MAX_VALUE`). 생산자와 소비자가 별도의 락(`putLock`, `takeLock`)을 사용해 동시에 put과 take가 가능하다. `ArrayBlockingQueue`보다 처리량이 높지만 노드 객체 생성으로 GC 압력이 있다. 용량을 지정하지 않으면 메모리 고갈 위험이 있으므로 운영 환경에서는 반드시 상한을 설정해야 한다.

```java
// 용량 무제한은 위험 — 생산자가 소비자보다 빠르면 OOM
BlockingQueue<Task> dangerous = new LinkedBlockingQueue<>();

// 안전한 사용 — 용량 제한
BlockingQueue<Task> safe = new LinkedBlockingQueue<>(1000);
```

`SynchronousQueue`는 내부 버퍼가 전혀 없다. 생산자가 put하면 소비자가 take할 때까지 블록된다. `Executors.newCachedThreadPool()`이 이 큐를 사용한다. 생산자가 소비자에게 직접 핸드오프(handoff)해야 할 때 적합하다.

`PriorityBlockingQueue`는 우선순위 기반 정렬을 지원하는 무제한 큐다. 요소가 `Comparable`을 구현하거나 `Comparator`를 제공해야 한다. 높은 우선순위 요소가 계속 들어오면 낮은 우선순위 요소는 영구히 처리되지 않을 수 있다(starvation).

`DelayQueue`는 지연 시간이 만료된 요소만 take할 수 있다. 스케줄된 작업 실행, 캐시 만료, 재시도 지연에 적합하다.

실무 선택 기준 요약: 처리량 우선이면 `LinkedBlockingQueue(capacity)`, 메모리 예측 가능성이 중요하면 `ArrayBlockingQueue`, 스레드 직접 핸드오프면 `SynchronousQueue`, 우선순위 처리면 `PriorityBlockingQueue`를 선택한다.
