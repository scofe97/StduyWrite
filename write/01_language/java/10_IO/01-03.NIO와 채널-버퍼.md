# NIO와 채널-버퍼

---

> Java NIO는 기존 IO의 블로킹 스트림 모델을 채널과 버퍼 기반으로 대체해 고성능 I/O를 가능하게 한다. 소수의 스레드로 다수의 연결을 처리해야 하는 서버 애플리케이션에서 특히 중요하다.

## 1. IO vs NIO 비교

기존 IO(`java.io`)는 스트림 기반으로 동작한다. 데이터를 1바이트씩 순차적으로 읽으며, 데이터가 올 때까지 스레드가 블로킹된다. 단순하고 직관적이지만 연결 하나당 스레드 하나가 필요해 대규모 동시 접속에 취약하다.

Java 1.4에서 도입된 **NIO**(`java.nio`)는 채널과 버퍼를 중심으로 동작한다. 채널은 양방향 통신이 가능하고, 논블로킹 모드를 지원한다. Selector를 사용하면 하나의 스레드로 여러 채널을 동시에 관리할 수 있다.

| 항목 | IO | NIO |
|------|----|-----|
| 기본 단위 | 스트림 (단방향) | 채널 (양방향) |
| 버퍼 | 없음 (직접 처리) | Buffer 객체 필수 |
| 블로킹 | 항상 블로킹 | 블로킹 + 논블로킹 선택 |
| 멀티플렉싱 | 불가 | Selector로 가능 |
| 적합한 상황 | 단순 파일 I/O | 대규모 네트워크 서버 |

## 2. Buffer: 데이터 컨테이너

NIO에서 모든 데이터는 **Buffer**를 통해 이동한다. Buffer는 고정 크기 배열에 메타데이터(포인터)를 더한 객체다. 가장 많이 사용하는 것은 `ByteBuffer`다.

Buffer의 세 가지 핵심 포인터를 이해하는 것이 NIO의 출발점이다:

- **capacity**: 버퍼의 최대 크기 (생성 시 고정, 변경 불가)
- **limit**: 읽거나 쓸 수 있는 마지막 위치 (쓰기 모드에서는 capacity와 같음)
- **position**: 다음에 읽거나 쓸 위치 (작업할 때마다 증가)

쓰기 후 읽기로 전환할 때 `flip()`을 호출해야 한다. `flip()`은 `limit = position`으로 설정하고 `position = 0`으로 되돌려 방금 쓴 데이터를 처음부터 읽을 수 있도록 준비한다.

```java
// ByteBuffer 기본 사용
ByteBuffer buffer = ByteBuffer.allocate(1024); // capacity = 1024

// 쓰기 모드: position이 증가
buffer.put((byte) 'H');
buffer.put((byte) 'i');
// position=2, limit=1024

// flip(): 쓰기 → 읽기 모드 전환
buffer.flip();
// position=0, limit=2

// 읽기
while (buffer.hasRemaining()) {
    System.out.print((char) buffer.get()); // H, i
}

// clear(): 버퍼 초기화 (position=0, limit=capacity)
buffer.clear();

// Direct Buffer: JVM 힙 외부 메모리 사용 (IO 성능 향상)
ByteBuffer directBuffer = ByteBuffer.allocateDirect(1024);
```

## 3. Channel: 데이터 통로

**Channel**은 파일, 소켓 등 I/O 소스에 연결되는 양방향 통로다. 반드시 Buffer와 함께 사용한다. `FileChannel`은 파일 I/O에, `SocketChannel`은 TCP 네트워크 통신에 사용한다.

```java
// FileChannel: 파일 읽기
try (FileChannel channel = FileChannel.open(
        Path.of("data.txt")
        , StandardOpenOption.READ)) {

    ByteBuffer buffer = ByteBuffer.allocate(1024);

    while (channel.read(buffer) > 0) {
        buffer.flip();
        while (buffer.hasRemaining()) {
            System.out.print((char) buffer.get());
        }
        buffer.clear();
    }
}

// FileChannel: 파일 간 직접 복사 (OS 레벨 최적화)
try (FileChannel src = FileChannel.open(Path.of("source.txt"), StandardOpenOption.READ);
     FileChannel dst = FileChannel.open(
             Path.of("dest.txt")
             , StandardOpenOption.WRITE
             , StandardOpenOption.CREATE)) {
    src.transferTo(0, src.size(), dst); // OS가 직접 처리
}
```

## 4. Selector와 멀티플렉싱

**Selector**는 NIO의 핵심 컴포넌트로, 하나의 스레드로 여러 `Channel`을 동시에 모니터링한다. 각 `Channel`을 Selector에 등록하고, I/O 이벤트(연결, 읽기, 쓰기)가 준비된 Channel만 골라 처리한다. 이 방식을 *멀티플렉싱(Multiplexing)*이라 한다.

```java
// 논블로킹 서버 스켈레톤
Selector selector = Selector.open();

ServerSocketChannel serverChannel = ServerSocketChannel.open();
serverChannel.bind(new InetSocketAddress(8080));
serverChannel.configureBlocking(false); // 논블로킹 모드 필수
serverChannel.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select(); // 이벤트가 있을 때까지 대기

    for (SelectionKey key : selector.selectedKeys()) {
        if (key.isAcceptable()) {
            SocketChannel client = serverChannel.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        } else if (key.isReadable()) {
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(256);
            int bytesRead = client.read(buffer);
            if (bytesRead == -1) {
                client.close();
            } else {
                buffer.flip();
                client.write(buffer); // 에코
            }
        }
    }
    selector.selectedKeys().clear();
}
```

## 5. NIO.2: Path와 Files API

Java 7에서 도입된 **NIO.2**(`java.nio.file`)는 파일 시스템 작업을 위한 현대적 API를 제공한다. 기존 `java.io.File`의 한계(예외 없는 실패, 심볼릭 링크 미지원)를 극복한다.

`Path`는 파일 경로를 표현하고, `Files`는 파일 작업 유틸리티를 제공한다:

```java
import java.nio.file.*;

Path path = Path.of("/tmp/data.txt");

// 파일 읽기 (소용량)
String content = Files.readString(path, StandardCharsets.UTF_8);
List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);

// 파일 쓰기
Files.writeString(path, "Hello", StandardCharsets.UTF_8);
Files.write(path, List.of("line1", "line2"), StandardCharsets.UTF_8);

// 디렉토리 순회 (재귀)
try (Stream<Path> walk = Files.walk(Path.of("/tmp"))) {
    walk.filter(Files::isRegularFile)
        .filter(p -> p.toString().endsWith(".java"))
        .forEach(System.out::println);
}

// 파일 정보
System.out.println(Files.exists(path));
System.out.println(Files.size(path));
System.out.println(Files.getLastModifiedTime(path));
```

## 6. WatchService: 파일 시스템 이벤트 감지

**`WatchService`**는 디렉토리의 변경 사항(생성, 수정, 삭제)을 OS 레벨에서 감지하는 API다. 설정 파일을 동적으로 리로드하거나, 특정 디렉토리에 파일이 생기면 자동으로 처리해야 하는 경우에 사용한다. 폴링(polling) 방식보다 훨씬 효율적이다.

```java
WatchService watchService = FileSystems.getDefault().newWatchService();

Path dir = Path.of("/tmp/watch");
dir.register(
    watchService
    , StandardWatchEventKinds.ENTRY_CREATE
    , StandardWatchEventKinds.ENTRY_MODIFY
    , StandardWatchEventKinds.ENTRY_DELETE
);

System.out.println("감지 시작...");
while (true) {
    WatchKey key = watchService.take(); // 이벤트 발생까지 블로킹

    for (WatchEvent<?> event : key.pollEvents()) {
        Path changed = (Path) event.context();
        System.out.printf("[%s] %s%n", event.kind(), changed);
    }

    key.reset(); // 다음 이벤트를 받으려면 reset 필수
}
```
