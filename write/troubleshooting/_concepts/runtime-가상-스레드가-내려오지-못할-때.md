---
title: 가상 스레드가 내려오지 못할 때 — pinning 과 그 교착
tags: [concept, jvm, thread, concurrency, pinning]
status: draft
source:
  - https://openjdk.org/jeps/491
  - https://github.com/openjdk/jdk21u/blob/jdk-21.0.3-ga/src/java.base/share/classes/java/lang/VirtualThread.java
  - https://netflixtechblog.com/java-21-virtual-threads-dude-wheres-my-lock-3052540e231d
related:
  - ./README.md
  - ../runtime/2026-09-10_CPU 는 노는데 응답이 끊긴 서비스.md
  - ../../01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/ch05_efficient-concurrency/01-04.자바와 가상 스레드 — Virtual Threads.md
updated: 2026-09-13
---

# 가상 스레드가 내려오지 못할 때

---

> 가상 스레드는 기다릴 때 캐리어에서 내려오는 것이 존재 이유입니다. `synchronized` 안에서는 내려오지 못하고, 그것이 성능 저하로 끝나지 않고 교착까지 갑니다.

## 두 층과 내려오기

> 가상 스레드는 수만 개까지 늘지만, 실제로 도는 자리는 CPU 수만큼입니다.

요청 하나에 **가상 스레드**(virtual thread)가 하나 생깁니다. JVM 이 관리하는 가벼운 실행 단위라 수만 개를 만들어도 부담이 적습니다. 하지만 실제로 CPU 에서 돌려면 아래층의 **캐리어 스레드**(carrier thread)에 올라타야 합니다. 캐리어는 진짜 OS 스레드이고, 개수의 기본값은 JVM 이 보는 CPU 수입니다[^park].

올라타는 것을 mount, 내려오는 것을 unmount 라고 합니다. 가상 스레드는 I/O 나 락을 기다리는 순간 내려와 자리를 비웁니다. 그래서 캐리어 몇 개로 요청 수천 개를 돌릴 수 있습니다. 이 구조의 전제는 **기다릴 때 반드시 내려온다**는 것입니다.



## 내려오지 못하는 두 자리

> JDK 21 에서 `synchronized` 안의 블로킹과 네이티브 호출은 내려오지 못합니다. 이것을 pinning 이라고 부릅니다.

JVM 이 `synchronized` 잠금(모니터)의 주인을 **가상 스레드가 아니라 그 아래 캐리어로 기록**하기 때문입니다[^jep491]. 블록 안에서 내려가 버리면 같은 캐리어에 올라온 다른 가상 스레드가 그 잠금의 주인으로 보입니다. 상호 배제가 깨지므로 JVM 이 내려가기를 막습니다.

JDK 21.0.3 에서 확인한 재현입니다. `synchronized` 를 떼는 것 말고는 아무것도 바꾸지 않았습니다.

```java
static final ReentrantLock lock = new ReentrantLock();

static synchronized void insideSynchronized() {   // ← 이 한 단어가 전부
    lock.lock();
    try { } finally { lock.unlock(); }
}

public static void main(String[] a) throws Exception {
    lock.lock();                                   // main 이 락을 쥔 채 안 놓는다
    for (int i = 0; i < 4; i++)
        Thread.ofVirtual().start(Pin::insideSynchronized);   // 캐리어 4개를 채운다
    Thread.sleep(1000);
    Thread.ofVirtual().start(() -> System.out.println("LATE 실행됨"));   // 5번째
}
```

| 선언 | 5번째 가상 스레드 |
|------|------------------|
| `static synchronized void` | `LATE 실행됨` 이 **안 찍힙니다** |
| `static void` | `LATE 실행됨` 이 찍힙니다 |

락을 기다리는 것 자체는 정상이고 `ReentrantLock` 대기는 원래 unmount 되는 연산입니다. 그 대기가 `synchronized` **안**이면 모니터 주인이 캐리어로 적혀 있어 내려가지 못합니다. 문제는 기다린 대상이 아니라 기다린 **장소**입니다.

`-Djdk.tracePinnedThreads=short` 를 켜면 JVM 이 그 자리를 직접 지목합니다.

```bash
Thread[#26,ForkJoinPool-1-worker-1,5,CarrierThreads]
    Pin.insideSynchronized(Pin.java:9) <== monitors:1

"ForkJoinPool-1-worker-1" #26 daemon prio=5 cpu=0.22ms elapsed=3.95s
   Carrying virtual thread #25
```

`monitors:1` 이 "이 프레임이 모니터를 쥐고 있어 내려보내지 못했다"는 표시입니다. 아래 스레드 덤프에서 3.95 초 동안 쓴 CPU 가 0.22ms 입니다. **가상 스레드를 업은 채 멈춰 있다는 표시와 낮은 CPU 가 같이 나오는 것**이 pinning 의 지문입니다.



## 왜 교착까지 가는가

> 고갈은 기다리면 풀리고 교착은 안 풀립니다. 가르는 것은 기다림이 원을 그리느냐입니다.

자리를 못 내주는 것이 성능 저하로 끝나지 않습니다. 락을 넘겨받을 스레드까지 캐리어를 못 얻으면 서로를 영원히 기다립니다. 원이 닫히는 모양은 이렇습니다.

1. 가상 스레드 A~D 가 `synchronized` 안에서 락을 기다립니다. pinning 이라 캐리어를 하나씩 붙든 채 멈춥니다
2. 락을 쥐고 있던 스레드가 락을 풀면서 대기열의 다음 차례 E 에게 신호를 보냅니다
3. E 는 `synchronized` 밖에서 기다리던 스레드라 캐리어에서 내려와 있었습니다. 락을 가져가려면 다시 올라타야 합니다
4. 캐리어는 A~D 가 쥐고 있고, A~D 는 락을 얻어야 놓습니다

E 는 캐리어를, 캐리어는 A~D 를, A~D 는 락을 기다립니다. 락은 E 가 가져가기를 기다립니다. 끝이 처음으로 돌아오므로 원이 닫힙니다. 락 하나와 자리 N 개짜리 세마포어의 교착이고, 캐리어 풀이 그 세마포어입니다.

**락은 비어 있는데 아무도 가져가지 못하는** 상태가 여기서 나옵니다. 힙 덤프에서 락의 주인 필드가 비어 있는데 대기자만 쌓여 있으면 이 모양입니다. 부하가 0 이 돼도 원은 안에서 끊기지 않습니다. JEP 491 도 스케줄러의 플랫폼 스레드가 전부 pinning 에 묶이면 기아나 교착으로 이어질 수 있다고 경고합니다[^jep491].



## 풀은 왜 캐리어를 더 안 만드나

> 상한 때문이 아닙니다. 늘릴 수 있는데 늘려야 할 이유를 전달받지 못합니다.

스케줄러의 `maxPoolSize` 기본값은 256 이라 CPU 수보다 훨씬 여유가 있습니다[^park]. `ForkJoinPool` 에는 워커가 블로킹을 신고하면 예비 스레드를 붙여 병렬성을 유지하는 보상(compensation) 경로도 있습니다[^fjp].

문제는 pinning 이 그 신고를 거치지 않는다는 데 있습니다. `VirtualThread.parkOnCarrierThread()` 는 풀에 알리지 않고 `U.park()` 로 캐리어를 그 자리에 재웁니다[^park]. 풀 입장에서는 그 워커가 계산 중인 것과 구분되지 않습니다.

## 관측이 갈리는 자리

> 손에 익은 도구가 헛돕니다. 가상 스레드 스택은 `Thread.dump_to_file`, 락의 주인은 힙 덤프입니다.

| 도구 | 멈춘 동안 보이는 것 |
|------|-------------------|
| `jcmd <pid> Thread.print` | 캐리어가 `Carrying virtual thread` 로만 표시됨. 앱의 호출 스택은 없음 |
| `jcmd <pid> Thread.dump_to_file` | 가상 스레드마다 `parkOnCarrierThread` 아래 대기 스택 |
| `jcmd <pid> GC.heap_dump` | 락 객체와 주인 필드 |
| JFR `jdk.VirtualThreadPinned` | **0건** |

`Thread.print` 는 jstack 과 같은 형식이라 가상 스레드의 호출 스택이 나오지 않습니다. 멈춘 JVM 이 할 일 없는 JVM 으로 보이는 이유입니다.

JFR 이 0건인 이유는 소스에 있습니다. pinning 이벤트는 멈춤이 끝난 **뒤에** 기록됩니다[^park]. 영원히 멈춘 가상 스레드에는 그 순간이 오지 않습니다. 실험에서 락을 풀자 이벤트 4건이 그제야 찍혔습니다. pinning 이 시작된 뒤에 녹화를 켰을 때는 락이 풀린 뒤에도 0건이었는데, 이 차이가 녹화 시작 시점 때문인지 JFR 초기화 여부 때문인지는 가르지 못했습니다. 두 결과가 같은 쪽을 가리키므로 **JVM 을 켤 때부터 녹화**해 두는 편이 안전합니다.

```bash
# 가상 스레드까지 담는 덤프 (JDK 21+)
jcmd <pid> Thread.dump_to_file -format=json /tmp/vt.json
grep -c 'parkOnCarrierThread' /tmp/vt.json

# 락의 주인 — 스레드 덤프에 안 나오므로 힙 덤프를 MAT 로 연다
jcmd <pid> GC.heap_dump /tmp/heap.hprof

# 재발 확인 — 녹화는 JVM 을 켤 때부터
java -XX:StartFlightRecording=name=pin,settings=profile -jar app.jar
jfr print --events jdk.VirtualThreadPinned /tmp/pin.jfr
```



## 무엇을 고치나

> 응급은 가상 스레드를 끄는 것이고, 재발 방지는 블로킹을 감싼 `synchronized` 를 걷어내는 것입니다.

응급으로는 가상 스레드를 끕니다. 스프링 부트라면 `spring.threads.virtual.enabled=false` 로 플랫폼 스레드 풀로 돌아갑니다[^boot-vt]. 처리량은 줄지만 교착은 사라집니다.

재발 방지는 블로킹이 일어나는 `synchronized` 블록을 `java.util.concurrent` 락으로 바꾸거나 JDK 24 이상으로 올리는 것입니다. JEP 491 이 `synchronized` 안에서도 unmount 되도록 고쳤습니다[^jep491]. 범인이 자기 코드가 아니라 라이브러리인 경우가 많으므로, 애플리케이션 코드만 뒤져서는 못 찾습니다.



## 관련 문서

- [개념 노트 진입점](./README.md)
- [CPU 는 노는데 응답이 끊긴 서비스](../runtime/2026-09-10_CPU%20는%20노는데%20응답이%20끊긴%20서비스.md) — 이 개념이 나온 문항
- [자바와 가상 스레드](../../01_language/book/Inside%20the%20Java%20Virtual%20Machine%20JVM%20Advanced%20Features%20and%20Best%20Practices/ch05_efficient-concurrency/01-04.자바와%20가상%20스레드%20—%20Virtual%20Threads.md) — mount·unmount 의 원리

---

[^park]: [JDK 21.0.3 `VirtualThread.java`](https://github.com/openjdk/jdk21u/blob/jdk-21.0.3-ga/src/java.base/share/classes/java/lang/VirtualThread.java) — `parkOnCarrierThread()` 가 `setState(PINNED)` 후 `U.park()` 로 캐리어를 재웁니다. park 가 끝난 뒤에야 `VirtualThreadPinnedEvent` 를 커밋합니다. `createDefaultScheduler()` 의 `parallelism` 기본값은 `availableProcessors()`, `maxPoolSize` 기본값은 `max(parallelism, 256)` 입니다.
[^jep491]: [JEP 491: Synchronize Virtual Threads without Pinning](https://openjdk.org/jeps/491) — JDK 24. 모니터 주인을 캐리어로 기록해 unmount 를 막는 이유는 "The reason for pinning" 절, 기아·교착 경고는 "Overcoming pinning" 절에 있습니다.
[^fjp]: [JDK 21.0.3 `ForkJoinPool.java`](https://github.com/openjdk/jdk21u/blob/jdk-21.0.3-ga/src/java.base/share/classes/java/util/concurrent/ForkJoinPool.java) — `managedBlock()` 문서 주석 "possibly arranges for a spare thread to be activated if necessary to ensure sufficient parallelism". `VirtualThread.java` 에는 이 호출이 없습니다.
[^boot-vt]: [Spring Boot — Application Properties](https://docs.spring.io/spring-boot/appendix/application-properties/index.html) — `spring.threads.virtual.enabled` "Whether to use virtual threads.", 기본값 `false`.
