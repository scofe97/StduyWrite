# 스레드 생명주기: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 스레드 상태 전이에서 BLOCKED와 WAITING의 차이는 무엇인가

### 왜 이 질문이 중요한가
스레드 덤프(thread dump)를 분석해 성능 문제나 데드락을 진단할 때 BLOCKED와 WAITING을 구분하지 못하면 원인을 잘못 파악한다. 두 상태는 모두 "대기 중"이지만 원인과 해결책이 다르다.

### 답변
BLOCKED 상태는 스레드가 `synchronized` 블록이나 메서드에 진입하려고 모니터 락(monitor lock)을 기다리는 상태다. 다른 스레드가 해당 락을 보유하고 있어 진입하지 못한다. 락이 해제되는 순간 JVM이 BLOCKED 스레드 중 하나를 선택해 RUNNABLE로 전환한다. 스레드 자신이 아무것도 할 수 없고 오직 락 해제만 기다린다.

WAITING 상태는 스레드가 명시적으로 다른 스레드의 통보를 기다리는 상태다. `Object.wait()`, `Thread.join()`, `LockSupport.park()`를 호출하면 진입한다. 다른 스레드가 `Object.notify()`, `Thread.interrupt()`, `LockSupport.unpark()`를 호출해야 깨어난다.

```java
// BLOCKED 예시 — 모니터 락 경쟁
synchronized (lock) {   // Thread-1이 여기 진입 중이면
    // ...              // Thread-2는 synchronized(lock) 앞에서 BLOCKED
}

// WAITING 예시 — 명시적 대기
synchronized (lock) {
    while (!condition) {
        lock.wait();    // 스레드가 락을 반납하고 WAITING 상태로 전환
    }
}
// 다른 스레드에서:
synchronized (lock) {
    condition = true;
    lock.notify();      // WAITING 스레드를 BLOCKED로 전환 (다시 락 경쟁)
}
```

스레드 덤프에서의 차이도 중요하다. BLOCKED 스레드는 어떤 락을 기다리는지와 그 락을 보유한 스레드를 보여준다. WAITING 스레드는 어떤 조건을 기다리는지(`waiting on <0x...>`)를 보여준다.

TIMED_WAITING은 WAITING과 같지만 시간 제한이 있다. `Thread.sleep(ms)`, `wait(ms)`, `LockSupport.parkNanos(ns)`가 이 상태를 만든다.

실무에서 스레드 덤프에 BLOCKED 스레드가 많으면 락 경쟁(lock contention)이 문제다. `synchronized` 범위를 줄이거나 `ReentrantLock`으로 전환하거나 락-프리 자료구조를 고려한다. WAITING 스레드가 많으면 조건 변수 패턴의 로직을 검토한다.

---

## Q2. interrupt 메커니즘의 협력적 성격은 무엇을 의미하는가

### 왜 이 질문이 중요한가
`Thread.interrupt()`가 스레드를 즉시 중단시킨다고 오해하면 잘못된 취소(cancellation) 메커니즘을 만든다. 협력적 취소 패턴을 이해해야 안전하고 응답성 있는 작업 취소를 구현할 수 있다.

### 답변
`Thread.interrupt()`는 스레드를 강제로 중단시키지 않는다. 단지 대상 스레드의 인터럽트 플래그(interrupt flag)를 true로 설정할 뿐이다. 실제 중단 여부는 해당 스레드가 플래그를 확인하고 스스로 종료 처리를 하는지에 달려 있다. 이것이 "협력적(cooperative)"의 의미다.

WAITING이나 TIMED_WAITING 상태의 스레드(`sleep`, `wait`, `join` 등)는 인터럽트 시 즉시 깨어나 `InterruptedException`을 던진다. 동시에 인터럽트 플래그는 자동으로 clear된다. RUNNABLE 상태의 스레드는 스스로 `Thread.currentThread().isInterrupted()`를 확인해야 한다.

```java
// 올바른 인터럽트 처리
public void run() {
    while (!Thread.currentThread().isInterrupted()) {
        doWork();
    }
    // 정리 작업
    cleanup();
}

// InterruptedException 처리 — 플래그 복원이 중요
public void doWork() {
    try {
        Thread.sleep(1000);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt(); // 플래그 복원 필수!
        return; // 또는 상위로 전파
    }
}
```

`InterruptedException`을 catch하고 아무것도 안 하는 것은 인터럽트 신호를 삼켜버리는 안티패턴이다. 인터럽트 플래그가 clear된 상태에서 상위 코드가 종료 여부를 확인할 방법이 없어진다. 반드시 `Thread.currentThread().interrupt()`로 플래그를 복원하거나 예외를 상위로 전파해야 한다.

ExecutorService에서 `Future.cancel(true)`를 호출하면 내부적으로 작업 스레드에 interrupt를 보낸다. 작업이 올바르게 인터럽트를 처리하지 않으면 취소 요청이 무시된다. 특히 `while(true)` 루프 내에서 `InterruptedException`을 삼키는 코드는 취소 불가능한 작업이 된다.
