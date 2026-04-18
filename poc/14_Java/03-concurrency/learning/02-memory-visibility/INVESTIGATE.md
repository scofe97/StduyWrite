# 메모리 가시성: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. volatile만으로 동시성 문제를 해결할 수 없는 이유는 무엇인가

### 왜 이 질문이 중요한가
`volatile`을 만능 동기화 수단으로 오해하면 경쟁 조건(race condition)이 있는 코드를 안전하다고 착각한다. volatile의 보장 범위를 정확히 알아야 어떤 상황에서 충분하고 어떤 상황에서 부족한지 판단할 수 있다.

### 답변
`volatile`은 두 가지를 보장한다. 첫째, 가시성(visibility): volatile 변수에 대한 쓰기는 이후 그 변수를 읽는 모든 스레드에게 즉시 보인다. CPU 캐시를 우회해 메인 메모리에 직접 쓰고 읽는다. 둘째, 재배치 방지(reordering prevention): volatile 읽기/쓰기 주변의 명령어 재배치를 막아 happens-before 관계를 형성한다.

volatile이 해결하지 못하는 것은 원자성(atomicity)이다. `count++`는 읽기-수정-쓰기(read-modify-write)의 세 단계 연산이다. volatile은 각 단계를 원자적으로 만들지 않는다.

```java
volatile int count = 0;

// 두 스레드가 동시에 실행하면 경쟁 조건 발생
void increment() {
    count++; // read(0) → modify(1) → write(1)
             // 두 스레드가 동시에 read(0)하면 둘 다 write(1) → count=1 (2여야 함)
}
```

volatile이 적합한 경우는 단일 스레드가 쓰고 여러 스레드가 읽는 패턴이다. 또는 플래그 변수처럼 단순 대입(assign)만 하는 경우다. 복합 연산(check-then-act, read-modify-write)에는 `synchronized`, `AtomicInteger`, `ReentrantLock` 같은 더 강한 동기화가 필요하다.

```java
// volatile이 충분한 경우 — 단순 플래그
volatile boolean running = true;
void stop() { running = false; }    // 단순 쓰기
void run() { while (running) {...} } // 단순 읽기

// volatile이 부족한 경우 — 복합 연산
// AtomicInteger나 synchronized 필요
AtomicInteger counter = new AtomicInteger();
counter.incrementAndGet(); // 원자적 read-modify-write
```

---

## Q2. 데드락 감지와 예방 전략은 무엇인가

### 왜 이 질문이 중요한가
데드락은 운영 환경에서 시스템을 완전히 멈추게 만드는 심각한 버그다. 발생 후 스레드 덤프로 진단하는 방법과 설계 단계에서 예방하는 방법을 모두 알아야 한다.

### 답변
데드락은 두 개 이상의 스레드가 서로가 보유한 락을 기다리며 영구적으로 멈추는 상태다. 발생 조건은 네 가지(상호 배제, 점유 대기, 비선점, 순환 대기)이며, 이 중 하나를 깨면 데드락이 불가능해진다.

감지 방법은 두 가지다. 첫째, JVM 스레드 덤프다. `kill -3 <pid>`(Unix) 또는 `jstack <pid>`로 스레드 덤프를 얻으면 JVM이 데드락을 자동으로 감지하고 관련 스레드와 락 정보를 출력한다.

```
Found one Java-level deadlock:
"Thread-1": waiting to lock monitor 0x... (object 0x..., a java.lang.Object),
  which is held by "Thread-0"
"Thread-0": waiting to lock monitor 0x... (object 0x..., a java.lang.Object),
  which is held by "Thread-1"
```

둘째, `ThreadMXBean`을 사용한 프로그래밍 방식 감지다.

```java
ThreadMXBean bean = ManagementFactory.getThreadMXBean();
long[] deadlockedThreads = bean.findDeadlockedThreads();
if (deadlockedThreads != null) {
    ThreadInfo[] infos = bean.getThreadInfo(deadlockedThreads, true, true);
    // 알림 전송, 스레드 덤프 기록 등
}
```

예방 전략은 네 가지다. 첫째, 락 순서 고정이다. 여러 락을 획득할 때 항상 같은 순서로 획득한다. `lock1 → lock2` 순서를 전체 코드에서 일관되게 지키면 순환 대기가 불가능해진다.

둘째, 타임아웃을 사용하는 `tryLock()`이다. `ReentrantLock.tryLock(timeout, unit)`은 지정 시간 내에 락을 얻지 못하면 false를 반환한다. 락 획득 실패 시 이미 보유한 락을 모두 해제하고 재시도하면 데드락을 피할 수 있다.

```java
boolean acquired = lock1.tryLock(100, TimeUnit.MILLISECONDS);
if (acquired) {
    try {
        if (lock2.tryLock(100, TimeUnit.MILLISECONDS)) {
            try { doWork(); }
            finally { lock2.unlock(); }
        }
    } finally { lock1.unlock(); }
}
```

셋째, 락 범위 최소화다. 락을 보유하는 시간을 최소화하면 다른 스레드가 대기하는 시간이 줄어 데드락 가능성이 낮아진다.

넷째, 고수준 동시성 도구 사용이다. `ConcurrentHashMap`, `BlockingQueue`, `Semaphore` 등 검증된 동시성 자료구조를 사용하면 직접 락을 관리하는 코드를 줄여 데드락 가능성을 낮춘다.
