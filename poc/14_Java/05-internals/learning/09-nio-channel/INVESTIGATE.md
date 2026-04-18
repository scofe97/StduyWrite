# NIO와 채널-버퍼: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. NIO Selector 기반 서버 vs Virtual Thread 기반 서버, 2026년 기준 어떤 것을 선택해야 하는가?

### 왜 이 질문이 중요한가
Java 21에서 Virtual Thread가 정식 출시되면서 NIO Selector 기반의 비동기 서버 모델의 존재 이유가 근본적으로 흔들렸다. Netty, Vert.x 같은 리액티브 프레임워크를 선택하는 근거가 "스레드 수를 줄이기 위해서"였는데, Virtual Thread가 그 문제를 해결한다면 복잡한 Selector 모델이 필요한가? 2026년 기준으로 명확한 선택 기준을 세울 수 있어야 한다.

### 답변

NIO Selector 모델과 Virtual Thread 모델의 핵심 차이는 **프로그래밍 모델의 복잡도**와 **CPU 바운드 vs I/O 바운드 처리 방식**이다.

**NIO Selector 모델의 동작 방식**: 소수의 OS 스레드(보통 CPU 코어 수)가 수천 개의 채널을 멀티플렉싱한다. I/O가 준비된 채널만 이벤트 루프에서 처리하므로 컨텍스트 스위칭이 최소화된다. 단, 콜백/CompletableFuture 기반의 비동기 코드 스타일이 필요해 가독성과 디버깅이 어렵다.

**Virtual Thread 모델**: 커넥션마다 Virtual Thread를 생성한다. I/O 블로킹 시 Virtual Thread가 마운트 해제(unmount)되어 캐리어 스레드를 양보하므로, 블로킹 코드 스타일로 작성해도 실제로는 비동기처럼 동작한다.

```java
// Virtual Thread 서버 (Java 21+) - 동기 코드 스타일
try (var serverSocket = new ServerSocket(8080)) {
    while (true) {
        Socket socket = serverSocket.accept();
        Thread.ofVirtual().start(() -> handle(socket));  // 가상 스레드
    }
}

// NIO Selector 서버 - 이벤트 루프 스타일 (복잡도 높음)
Selector selector = Selector.open();
serverChannel.register(selector, SelectionKey.OP_ACCEPT);
while (true) {
    selector.select();
    for (SelectionKey key : selector.selectedKeys()) {
        if (key.isAcceptable()) { /* accept */ }
        else if (key.isReadable()) { /* read */ }
    }
}
```

**2026년 기준 선택 기준**:

| 상황 | 권장 | 이유 |
|------|------|------|
| 신규 서비스 (Spring Boot 3.x+) | Virtual Thread | `-Dspring.threads.virtual.enabled=true` 한 줄, 코드 변경 없음 |
| I/O 집약, 고동시성 (수만 커넥션) | Virtual Thread | 동일 성능, 코드 단순 |
| 극한 저레이턴시 (게임 서버, HFT) | NIO Selector (Netty) | 컨텍스트 스위칭 절대 최소화 |
| 기존 Netty/Vert.x 시스템 | 유지 | 마이그레이션 비용 > 이득 |
| CPU 집약 작업 혼합 | Virtual Thread + 별도 스레드풀 | CPU 작업은 여전히 OS 스레드 필요 |

결론: **2026년 신규 프로젝트에서 NIO Selector를 직접 작성하는 것은 과도한 복잡도다.** Netty 같은 성숙한 프레임워크 없이 직접 Selector를 구현하면 엣지 케이스 버그 위험이 크다. Virtual Thread + 동기 코드가 대부분의 경우 더 단순하고 충분히 빠르다.

---

## Q2. ByteBuffer의 flip/clear가 혼란스러운 이유와 올바른 사용 패턴은?

### 왜 이 질문이 중요한가
NIO를 처음 쓰는 개발자의 80%가 `flip()` 호출을 빠뜨리거나 `clear()` vs `compact()`를 혼동해서 버그를 만든다. ByteBuffer의 상태 기계를 이해하지 못하면 데이터가 무음으로 손실되거나 0만 읽히는 증상이 나타난다. 실무에서 NIO를 직접 다룰 일이 있다면 이 개념은 완벽히 이해해야 한다.

### 답변

ByteBuffer는 세 가지 포인터(`position`, `limit`, `capacity`)로 상태를 관리한다. 혼란의 근원은 **쓰기 모드와 읽기 모드가 동일한 필드를 다른 의미로 사용**한다는 점이다.

```
쓰기 모드:
  position = 다음 쓸 위치
  limit = capacity (끝까지 쓸 수 있음)
  [0 ... position ... limit/capacity]

flip() 호출 후 읽기 모드:
  limit = 이전 position (쓴 데이터의 끝)
  position = 0 (읽기 시작점)
  [0 ... position → limit ... capacity]
```

**올바른 사용 패턴**:

```java
ByteBuffer buf = ByteBuffer.allocate(1024);

// 1. 채널에서 읽기 (버퍼에 쓰기)
channel.read(buf);         // position이 증가

// 2. 버퍼에서 데이터 처리 (버퍼에서 읽기) 전에 반드시 flip
buf.flip();                // limit = position, position = 0
while (buf.hasRemaining()) {
    byte b = buf.get();    // position 증가
}

// 3-A. 버퍼 재사용 (완전히 소비한 경우)
buf.clear();               // position = 0, limit = capacity (초기화)

// 3-B. 버퍼 재사용 (일부만 읽은 경우, 나머지 데이터 보존)
buf.compact();             // 미읽은 데이터를 앞으로 이동, position = 나머지 크기
```

**흔한 실수와 증상**:

```java
// 실수: flip() 없이 읽기
channel.read(buf);
// buf.flip() 빠뜨림!
while (buf.hasRemaining()) { buf.get(); }  // limit이 capacity이므로 초기화된 0만 읽힘

// 실수: flip()을 두 번 호출
buf.flip(); processData(buf); buf.flip();  // 두 번째 flip은 limit=0 → 데이터 없음
```

Direct Buffer(`ByteBuffer.allocateDirect()`)는 JVM 힙 외부에 메모리를 할당해 커널과 JVM 간 복사를 줄인다. 파일 채널이나 네트워크 I/O의 hot path에서 유리하지만, 할당/해제 비용이 높고 GC로 회수되지 않으므로 풀링(pooling)이 필수다.
