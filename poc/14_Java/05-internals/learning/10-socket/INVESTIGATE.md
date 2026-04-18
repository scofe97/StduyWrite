# 소켓 프로그래밍: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Thread-per-Connection 모델의 확장성 한계는 무엇인가?

### 왜 이 질문이 중요한가
Thread-per-Connection은 Java 소켓 프로그래밍의 가장 직관적인 모델이지만, 왜 대규모 서비스에서 사용할 수 없는지 구체적 수치로 설명할 수 있어야 한다. 이 한계를 이해해야 NIO, 리액티브 프레임워크, Virtual Thread가 왜 필요한지 동기가 생긴다.

### 답변

Thread-per-Connection 모델은 클라이언트 연결마다 OS 스레드를 하나 생성해 처리한다. 직관적이고 코드가 단순하지만 두 가지 근본적 한계가 있다.

**한계 1: OS 스레드 생성 비용과 메모리.** 기본 JVM 스레드 스택 크기는 512KB~1MB(플랫폼/설정에 따라 다름)다. 1만 개의 동시 연결을 처리하려면 스택만 5~10GB가 필요하다. 실제로는 그보다 훨씬 전에 OS의 스레드 수 제한(`/proc/sys/kernel/threads-max`, 기본 수만 개)에 걸린다.

```bash
# 스레드 스택 크기 확인 및 조정
java -Xss256k MyServer  # 스택을 256KB로 줄이면 4만 스레드 가능 (10GB)
# 하지만 스택 오버플로우 위험, 재귀 깊이 제한

# 현재 JVM 스레드 수 모니터링
jstack <PID> | grep "^\"" | wc -l
```

**한계 2: 컨텍스트 스위칭 오버헤드.** 수천 개의 스레드가 I/O 블로킹으로 대기할 때, 활성 스레드를 찾아 스케줄링하는 OS의 컨텍스트 스위칭 비용이 급증한다. CPU가 실제 연산 대신 스레드 관리에 시간을 소비하는 것이다.

```
C10K 문제 (1만 동시 연결):
- Thread-per-Connection: ~10,000 OS 스레드 → 메모리 10GB+, CPU 70%+ 컨텍스트 스위칭
- NIO Selector: ~4 OS 스레드 (CPU 코어 수) → 이벤트 루프로 처리
- Virtual Thread: ~4 캐리어 스레드 + ~10,000 가상 스레드 → 스택 수KB, 힙 관리
```

Thread-per-Connection이 여전히 유효한 경우는 동시 연결 수가 수백 이하이고 각 요청 처리 시간이 짧은 내부 관리 서비스다. 이 범위라면 단순성이 성능보다 중요하다.

---

## Q2. Virtual Thread가 C10K 문제를 어떻게 해결하는가?

### 왜 이 질문이 중요한가
Virtual Thread(Project Loom, Java 21 정식 출시)는 Java 동시성 역사에서 가장 중요한 변화 중 하나다. NIO와 리액티브 프로그래밍이 해결하려 했던 문제를 "동기 코드 스타일을 유지하면서" 해결한다는 점에서 패러다임 전환이다. 면접에서 "Java 21의 주요 기능"을 물으면 Virtual Thread를 원리 수준에서 설명할 수 있어야 한다.

### 답변

Virtual Thread는 JVM이 관리하는 경량 스레드로, OS 스레드(캐리어 스레드) 위에서 M:N으로 멀티플렉싱된다. OS 스레드 스택(수백 KB~수 MB) 대신 힙에 연속되지 않은 스택 청크를 사용해 수백 바이트에서 시작한다.

**핵심 메커니즘: 마운트/언마운트(mount/unmount)**

```
Virtual Thread 실행 중 블로킹 I/O 발생 시:
1. JVM이 블로킹 감지 (java.net, java.nio 등 JDK 내장 I/O)
2. Virtual Thread가 캐리어 스레드에서 언마운트 (스택 상태를 힙에 저장)
3. 캐리어 스레드는 즉시 다른 Virtual Thread 실행
4. I/O 완료 시 Virtual Thread가 다시 마운트 (어느 캐리어 스레드든 가능)
```

```java
// Virtual Thread per request - Thread-per-Connection 코드와 동일하지만 확장 가능
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    while (true) {
        Socket socket = serverSocket.accept();
        executor.submit(() -> {
            // 블로킹 I/O 자유롭게 사용 가능
            InputStream in = socket.getInputStream();
            byte[] buf = in.readNBytes(1024);  // 블로킹 → 언마운트 → 다른 VT 실행
            processRequest(buf);
        });
    }
}
```

**성능 특성**:

```
1만 동시 연결 시 메모리 비교:
OS Thread (1MB 스택): ~10GB
Virtual Thread (초기 수백 바이트): ~수십 MB
```

**함정: 핀닝(Pinning).** Virtual Thread가 언마운트되지 못하고 캐리어 스레드에 고정되는 경우다. `synchronized` 블록 내에서 블로킹 I/O를 호출하거나, native 메서드를 호출할 때 발생한다. 핀닝이 발생하면 캐리어 스레드가 블로킹되어 Virtual Thread의 장점이 사라진다.

```java
// 핀닝 발생 패턴 (Java 21 기준)
synchronized (lock) {
    socket.read(buf);  // synchronized 내 블로킹 → 캐리어 스레드 핀닝
}

// 해결: ReentrantLock으로 교체
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    socket.read(buf);  // ReentrantLock은 핀닝 없이 언마운트 가능
} finally { lock.unlock(); }

// 핀닝 감지
java -Djdk.tracePinnedThreads=full MyApp
```

Java 24에서는 `synchronized` 내 핀닝 문제가 해결될 예정(JEP 491)이므로, 향후 이 제약은 사라진다.
