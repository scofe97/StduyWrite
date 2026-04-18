# Virtual Thread Pinning: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Pinning이 성능에 미치는 실질적 영향과 측정 방법은 무엇인가

### 왜 이 질문이 중요한가
Pinning은 Virtual Thread의 가장 큰 성능 함정이다. 눈에 보이지 않게 캐리어 스레드를 점유해 전체 처리량을 저하시킨다. 영향 측정 방법을 알아야 마이그레이션 전후를 비교하고 개선 효과를 수치화할 수 있다.

### 답변
Pinning은 Virtual Thread가 `synchronized` 블록 안에서 블로킹 IO나 `LockSupport.park()`를 호출할 때 발생한다. 이 경우 Virtual Thread가 캐리어 스레드에서 분리(unmount)되지 못하고 캐리어 스레드를 계속 점유한다.

성능에 미치는 실질적 영향을 이해하려면 캐리어 스레드 수를 알아야 한다. 기본값은 `Runtime.getRuntime().availableProcessors()`다. 4코어 머신에서 캐리어 스레드가 4개라면, 동시에 4개의 Virtual Thread가 Pinning 상태면 새로운 Virtual Thread가 실행될 수 없다. IO 중심 애플리케이션에서 처리량이 플랫폼 스레드 기반과 동일하게 떨어지거나 오히려 나빠질 수 있다.

Pinning 측정 방법은 두 가지다.

첫째, JVM 플래그를 사용한 런타임 추적이다.

```bash
# Pinning 발생 시 스택 트레이스 출력
java -Djdk.tracePinnedThreads=full -jar app.jar

# 출력 예시:
# Thread[#21,ForkJoinPool-1-worker-1,5,CarrierThreads]
#     com.example.Service.doWork(Service.java:45) <-- monitors:1>
#     java.lang.Object.wait(Object.java) <-- monitors:1>
```

둘째, JFR(Java Flight Recorder) 이벤트를 사용한 측정이다.

```bash
java -XX:StartFlightRecording=filename=recording.jfr,duration=60s -jar app.jar
# jfr print --events jdk.VirtualThreadPinned recording.jfr
```

`jdk.VirtualThreadPinned` 이벤트는 Pinning 지속 시간, 스택 트레이스, 발생 빈도를 기록한다. 이 데이터로 어떤 코드가 가장 많이 Pinning을 유발하는지 핫스팟을 찾을 수 있다.

캐리어 스레드 수를 늘려 Pinning의 영향을 임시로 완화할 수 있다.

```bash
# 캐리어 스레드 수를 256으로 증가 (Pinning 발생 시 여유 캐리어 확보)
java -Djdk.virtualThreadScheduler.parallelism=256 -jar app.jar
```

이 방법은 임시 해결책이고, 근본 해결은 `synchronized`를 `ReentrantLock`으로 교체하는 것이다.

---

## Q2. synchronized를 ReentrantLock으로 바꿀 때 주의할 점은 무엇인가

### 왜 이 질문이 중요한가
Pinning 해결을 위해 `synchronized`를 `ReentrantLock`으로 기계적으로 교체하면 새로운 버그가 생긴다. 올바른 교체 방법과 교체해서는 안 되는 경우를 알아야 한다.

### 답변
`synchronized`와 `ReentrantLock`의 가장 큰 차이는 자동 해제 여부다. `synchronized`는 블록을 벗어나면(예외 포함) JVM이 자동으로 락을 해제한다. `ReentrantLock`은 반드시 `unlock()`을 명시적으로 호출해야 한다.

```java
// synchronized 패턴
synchronized (lock) {
    doWork(); // 예외 발생해도 락 자동 해제
}

// ReentrantLock 교체 — try-finally 필수
lock.lock();
try {
    doWork();
} finally {
    lock.unlock(); // 이 줄이 없으면 락이 영구 보유됨
}
```

`finally`에서 `unlock()`을 빠뜨리는 실수가 가장 흔하다. 특히 여러 return 경로가 있거나 예외 처리가 복잡한 경우에 발생한다.

재진입성(reentrancy) 동작은 동일하다. `ReentrantLock`도 같은 스레드가 여러 번 `lock()`을 호출할 수 있고, 같은 횟수만큼 `unlock()`을 호출해야 한다.

```java
// 재진입 — lock() 2회면 unlock()도 2회 필요
lock.lock();
try {
    lock.lock(); // 재진입 허용
    try { innerWork(); }
    finally { lock.unlock(); } // 첫 번째 해제
} finally {
    lock.unlock(); // 두 번째 해제
}
```

교체하면 안 되는 경우도 있다. 서드파티 라이브러리 코드나 JDK 내부 코드에 `synchronized`가 있다면 직접 교체할 수 없다. 예를 들어 `java.io.InputStream`, 오래된 JDBC 드라이버, 레거시 라이브러리 등이 그렇다. 이 경우 해당 라이브러리를 Virtual Thread를 지원하는 버전으로 업그레이드하거나, 해당 코드를 별도의 플랫폼 스레드 기반 실행자에서 실행하는 격리 전략을 사용해야 한다.

Java 24(JEP 491)에서는 `synchronized`도 Virtual Thread unmount를 지원하도록 개선될 예정이다. 이후에는 Pinning 문제가 대부분 해소된다.
