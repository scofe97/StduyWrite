# 소켓 프로그래밍

---

> 소켓(Socket)은 네트워크 상의 두 프로세스가 데이터를 주고받는 통신 엔드포인트다. Java는 블로킹 소켓부터 NIO 기반 논블로킹, Java 21의 Virtual Thread까지 다양한 서버 구현 방식을 제공한다.

## 1. TCP 소켓: ServerSocket과 Socket

Java의 TCP 통신은 서버측 `ServerSocket`과 클라이언트측 `Socket`으로 이뤄진다. `ServerSocket`은 특정 포트에서 연결 요청을 기다리고, 요청이 오면 `accept()`로 새 `Socket` 객체를 생성한다. 이후 통신은 `ServerSocket`과 무관하게 두 `Socket` 사이에서만 이뤄진다.

클라이언트-서버 통신 흐름은 다음과 같다:

- 서버: `ServerSocket` 생성 → 포트 바인딩 → `accept()` 대기
- 클라이언트: `Socket` 생성과 동시에 서버 IP/포트로 연결 시도
- 서버: `accept()` 반환으로 연결된 `Socket` 획득
- 양측: `InputStream` / `OutputStream`으로 데이터 교환
- 양측: `socket.close()`로 연결 종료

기본 에코 서버 구현:

```java
// 서버 (단일 클라이언트, 블로킹)
public class EchoServer {
    public static void main(String[] args) throws IOException {
        try (ServerSocket serverSocket = new ServerSocket(9000)) {
            System.out.println("서버 시작: port 9000");

            Socket socket = serverSocket.accept(); // 연결 대기 (블로킹)
            System.out.println("클라이언트 연결: " + socket.getRemoteSocketAddress());

            try (socket;
                 BufferedReader in = new BufferedReader(
                     new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
                 PrintWriter out = new PrintWriter(
                     new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true)) {

                String line;
                while ((line = in.readLine()) != null) {
                    System.out.println("수신: " + line);
                    out.println("ECHO: " + line); // 에코
                }
            }
        }
    }
}

// 클라이언트
public class EchoClient {
    public static void main(String[] args) throws IOException {
        try (Socket socket = new Socket("localhost", 9000);
             PrintWriter out = new PrintWriter(
                 new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true);
             BufferedReader in = new BufferedReader(
                 new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8))) {

            out.println("Hello");
            System.out.println(in.readLine()); // ECHO: Hello
        }
    }
}
```

## 2. Thread-per-Connection 멀티스레드 서버

단일 스레드 서버는 한 클라이언트와 통신하는 동안 다른 클라이언트의 연결을 처리하지 못한다. `accept()` 이후 각 클라이언트를 별도 스레드에서 처리하는 *Thread-per-Connection* 방식으로 이 문제를 해결한다.

```java
public class ThreadPerConnectionServer {
    public static void main(String[] args) throws IOException {
        try (ServerSocket serverSocket = new ServerSocket(9000)) {
            System.out.println("서버 시작");
            while (true) {
                Socket socket = serverSocket.accept();
                // 클라이언트마다 새 스레드 생성
                new Thread(new ClientHandler(socket)).start();
            }
        }
    }
}

class ClientHandler implements Runnable {
    private final Socket socket;

    ClientHandler(Socket socket) { this.socket = socket; }

    @Override
    public void run() {
        try (socket;
             BufferedReader in = new BufferedReader(
                 new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
             PrintWriter out = new PrintWriter(
                 new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true)) {

            String line;
            while ((line = in.readLine()) != null) {
                out.println("ECHO: " + line);
            }
        } catch (IOException e) {
            System.err.println("클라이언트 처리 오류: " + e.getMessage());
        }
    }
}
```

스레드를 매번 생성하면 객체 생성 비용이 크다. `ExecutorService`를 사용해 스레드 풀로 전환하면 스레드 생성 비용을 줄이고 최대 동시 처리 수를 제어할 수 있다.

```java
public class ThreadPoolServer {
    private static final int POOL_SIZE = 100;

    public static void main(String[] args) throws IOException {
        ExecutorService executor = Executors.newFixedThreadPool(POOL_SIZE);

        try (ServerSocket serverSocket = new ServerSocket(9000)) {
            while (true) {
                Socket socket = serverSocket.accept();
                executor.submit(new ClientHandler(socket));
            }
        } finally {
            executor.shutdown();
        }
    }
}
```

## 3. NIO 기반 서버: Selector + SocketChannel

Thread-per-Connection 방식은 스레드 수가 곧 동시 처리 한계다. 스레드는 OS 리소스를 많이 소비하므로, 수천 개의 동시 연결에서는 메모리와 컨텍스트 스위칭 비용이 문제가 된다.

NIO의 `Selector`를 사용하면 **하나의 스레드**로 수천 개의 채널을 관리할 수 있다. 각 채널을 논블로킹으로 설정하고 Selector에 등록하면, Selector가 I/O 이벤트가 준비된 채널만 골라 알려준다.

```java
public class NioEchoServer {
    public static void main(String[] args) throws IOException {
        Selector selector = Selector.open();

        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.bind(new InetSocketAddress(9000));
        serverChannel.configureBlocking(false);
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);

        System.out.println("NIO 서버 시작");

        while (true) {
            selector.select();

            Iterator<SelectionKey> iter = selector.selectedKeys().iterator();
            while (iter.hasNext()) {
                SelectionKey key = iter.next();
                iter.remove();

                if (key.isAcceptable()) {
                    SocketChannel client = serverChannel.accept();
                    client.configureBlocking(false);
                    client.register(selector, SelectionKey.OP_READ);
                    System.out.println("연결: " + client.getRemoteAddress());

                } else if (key.isReadable()) {
                    SocketChannel client = (SocketChannel) key.channel();
                    ByteBuffer buffer = ByteBuffer.allocate(256);
                    int read = client.read(buffer);

                    if (read == -1) {
                        client.close();
                    } else {
                        buffer.flip();
                        client.write(buffer); // 에코
                    }
                }
            }
        }
    }
}
```

## 4. Virtual Thread 기반 서버 (Java 21)

Java 21에서 정식 도입된 **Virtual Thread**는 Thread-per-Connection의 간결함과 NIO의 확장성을 동시에 제공한다. Virtual Thread는 JVM이 관리하는 경량 스레드로, 블로킹 I/O 호출 시 OS 스레드를 점유하지 않고 다른 Virtual Thread에게 양보한다. 수십만 개의 Virtual Thread를 생성해도 메모리 부담이 작다.

```java
public class VirtualThreadServer {
    public static void main(String[] args) throws IOException {
        // Virtual Thread를 사용하는 ExecutorService (Java 21+)
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
             ServerSocket serverSocket = new ServerSocket(9000)) {

            System.out.println("Virtual Thread 서버 시작");

            while (true) {
                Socket socket = serverSocket.accept();
                // 각 클라이언트를 Virtual Thread에서 처리
                executor.submit(() -> handleClient(socket));
            }
        }
    }

    private static void handleClient(Socket socket) {
        try (socket;
             BufferedReader in = new BufferedReader(
                 new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
             PrintWriter out = new PrintWriter(
                 new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true)) {

            String line;
            while ((line = in.readLine()) != null) {
                out.println("ECHO: " + line);
            }
        } catch (IOException e) {
            System.err.println("오류: " + e.getMessage());
        }
    }
}
```

## 5. 서버 모델 비교

세 방식은 코드 복잡도와 확장성에서 뚜렷한 차이가 있다.

| 항목 | Thread-per-Connection | NIO (Selector) | Virtual Thread |
|------|-----------------------|----------------|----------------|
| 코드 복잡도 | 낮음 | 높음 | 낮음 |
| 동시 연결 한계 | ~수천 (OS 스레드 제한) | 수십만 | 수십만 |
| 블로킹 I/O | 스레드 점유 | 해당 없음 | JVM이 자동 관리 |
| CPU 집약 작업 | 적합 | 비적합 | 적합 |
| 도입 버전 | Java 1.0 | Java 1.4 | Java 21 |

Thread-per-Connection은 단순하지만 스레드 비용 때문에 수천 동시 연결 이상에서 한계가 있다. NIO는 확장성은 뛰어나지만 콜백 스타일의 복잡한 코드가 단점이다. Virtual Thread는 기존 블로킹 스타일 코드를 유지하면서 NIO 수준의 확장성을 제공해, Java 21 이상에서 서버를 새로 만든다면 Virtual Thread가 가장 합리적인 선택이다.
