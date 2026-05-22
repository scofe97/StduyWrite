# [Spring Netty] 04. 채널 파이프라인과 코덱 ⭐

주제: Spring Netty

- 참고
    
    [Netty 채널 파이프라인, 코덱](https://shortstories.gitbook.io/studybook/netty/cc44_b110_d30c_c774_d504_b77c_c7782c_cf54_b371)
    
    [자바 네트워크 소녀 Netty 정리](https://velog.io/@monami/Netty#4장-채널-파이프라인과-코덱)
    

# **채널 파이프라인, 코덱**

---

## 이벤트 실행

<aside>
✍️ **NOTE**

> *데이터를 처리하는 입출력은 Netty가 이벤트로 관리하기 떄문에 **이벤트 핸들러만 구현하면 된다.***
> 
- **소켓 채널 데이터 수신**
    1. Netty 이벤트 루프가 채널 파이프라인에 등록된 이벤트 핸들러를 가져온다.
    2. 이벤트 메서드가 구현되어 있으면 실행
    3. 마지막 이벤트 핸들러에 도달할 때 까지 다음 이벤트 핸들러를 가져와 1~2 반복
</aside>

## *채널 파이프 라인*

<aside>
✍️ **NOTE**

> ***입력* ↔️ *출력을 전달할 수 있도록 파이프라이닝 한다.***
> 

![채널과 이벤트 핸들러 사이의 통로 역할을 수행](%5BSpring%20Netty%5D%2004%20%EC%B1%84%EB%84%90%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%EC%BD%94%EB%8D%B1%20%E2%AD%90/Untitled.png)

채널과 이벤트 핸들러 사이의 통로 역할을 수행

![채널 파이프 라인 구조](%5BSpring%20Netty%5D%2004%20%EC%B1%84%EB%84%90%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%EC%BD%94%EB%8D%B1%20%E2%AD%90/Untitled%201.png)

채널 파이프 라인 구조

### 등록

```java
bootstrap = new ServerBootstrap();

bootstrap.group(bossGroup, workerGroup)
.channel(NioServerSocketChannel.class)
.handler(new LoggingHandler(LogLevel.INFO))
.childHandler(new ChannelInitializer<SocketChannel>() { // 1
  @Override
  protected void initChannel(SocketChannel socketChannel) throws Exception { // 2
    ChannelPipeline pipeline = socketChannel.pipeline(); // 3
    pipeline.addLast(new LoggingHandler(LogLevel.INFO)); // 4
    pipeline.addLast(new EchoServerHandler()); // 4
  }
});
```

1. `childrenHandler` 메소드를 통해서 설정
2. `initChannel`은 클라이언트 소켓 채널이 생성될 때 호출됨
3. Netty 내부에서 할당한 빈 채널 파이프라인 가져오기
4. 파이프라인에 이벤트 핸들러 등록

### 초기화 순서

```java
@Component
@RequiredArgsConstructor
public class ImageNettyChannelInitializer extends ChannelInitializer<SocketChannel> {

	private final ImageNettyInboundHandler imageNettyInboundHandler;

	@Override
	protected void initChannel(SocketChannel ch) {
		ChannelPipeline pipeline = ch.pipeline();

		ByteBuf delimiter = Unpooled.copiedBuffer("\n", CharsetUtil.UTF_8);
		int maxFrameLength = 5 * 1024 * 1024; // 5MB
		pipeline.addLast(new DelimiterBasedFrameDecoder(maxFrameLength, delimiter));

		pipeline.addLast(imageNettyInboundHandler);
	}
}
```

1. 클라이언트가 서버 소켓에 접속 요청
2. 해당 연결을 대응하는 클라이언트 소켓 채널 객체 생성
3. 빈 채널 파이프라인 객체 생성, 클라이언트 소켓 채널에 할당
4. 클라이언트 소켓 채널에 등록된 `ChannelInitalizer`객체를 가져와서 `initChannel` 호출
5. 클라이언트 소켓 채널에 할당되어있는 파이프라인을 가져와서 이벤트 핸들러 등록
</aside>

## *인 바운드이벤트 핸들러*

<aside>
✍️ **NOTE**

> ***연결 상대**가 **어떤 동작을 취했을 떄 발생하는 이벤트***
> 
- 채널 활성화, 데이터 수신 등
- Bottom-UP 형식으로 동작하기 때문에, 가장 먼저 등록한 Handler부터 마지막에 등록한 Handler 순서로 동작
- 이벤트 순서

![Untitled](%5BSpring%20Netty%5D%2004%20%EC%B1%84%EB%84%90%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%EC%BD%94%EB%8D%B1%20%E2%AD%90/Untitled%202.png)

| 메서드 | 설명 |
| --- | --- |
| **`channelRegistered`** | Channel이 EventLoop에 등록되고 입출력을 처리할 수 있으면 호출됨 |
| **`channelUnregistered`** | Channel이 EventLoop에서 등록 해제되고 입출력을 처리할 수 없으면 호출됨 |
| **`channelActive`** | Channel의 연결과 바인딩이 완료되어 활성화되면 호출됨 |
| **`channelInactive`** | Channel이 활성 상태에서 벗어나 로컷 피어에 대한 연결이 해제되면 호출됨 |
| **`channelReadComplete`** | Channel에서 읽기 작업이 완료되면 호출됨 |
| **`channelRead`** | Channel에서 데이터를 읽을 때 호출됨 |
| **`channelWritabilityChanged`** | Channel의 기록 가능 상태가 변경되면 호출된다. |
| **`userEventTriggered`** | POJO가 ChannelPipeline을 통해서 전달돼서 ChannelInboundHandler.fireUserEventTriggered()가 트리거되면 호출됨. |

- 참고코드
    
    ```java
    @Slf4j
    public abstract class AbstractNettyInboundHandler  extends SimpleChannelInboundHandler<ByteBuf> {
    
    	protected Map<String, StringBuilder> dataMap = new ConcurrentHashMap<>();
    
    	@Override
    	public void channelActive(ChannelHandlerContext ctx) {
    		log.info("Channel active: {}", ctx.channel());
    	}
    
    	// 클라이언트와 연결되어 트래픽을 생성할 준비가 되었을 때 호출하는 메서드
    	@Override
    	public void channelInactive(ChannelHandlerContext ctx) {
    		log.info("Channel inactive: {}", ctx.channel());
    	}
    
    	// 예외 발생시
    	@Override
    	public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
    		cause.printStackTrace();
    		ctx.close();
    	}
    
    	protected Map<String, String> parseData(String receivedData) {
    		String[] dataParts = receivedData.split(" ");
    		Map<String, String> dataMap = new HashMap<>();
    
    		if (dataParts.length == 4) {
    			dataMap.put("dataServer", dataParts[0]);
    			dataMap.put("dataType", dataParts[1]);
    			dataMap.put("dataValue", dataParts[2]);
    			dataMap.put("dataTime", dataParts[3]);
    		}
    
    		else if (dataParts.length == 5) {
    			dataMap.put("dataServer", dataParts[0]);
    			dataMap.put("dataType", dataParts[1]);
    			dataMap.put("dataValue", dataParts[2]);
    			dataMap.put("dataTime", dataParts[3]);
    			dataMap.put("dataIdentifier", dataParts[4]);
    		}
    
    		else{
    			log.error("데이터 양식이 이상합니다.");
    		}
    
    		return dataMap;
    	}
    }
    ```
    
</aside>

## *아웃바운드 이벤트 핸들러*

<aside>
✍️ **NOTE**

> *소켓 채널에서 발생한 이벤트 중 **프로그래머가 요청한 동작에 해당하는 이벤트***
> 
- 연결 요청, 데이터 요청, 소켓 닫기 등
- Top-Down 형식으로 동작하기 떄문에, 가장 마지막에 등록한 Handler부터 가장 먼저 등록한 Handler 순서로 동작

- **이벤트 순서**

| **메서드** | **설명** |
| --- | --- |
| **`bind**(ChannelHandlerContext, SocketAddress, ChannelPromise)` | Channel을 로컬 주소로 바인딩 요청 시 호출됨 |
| **`connect**(ChannelHandlerContext, SocketAddress, SocketAddress, ChannelPromise)` | Channel을 원격 피어로 연결 요청 시 호출됨 |
| **`disconnect**(ChannelHandlerContext, ChannelPromise)` | Channel을 원격 피어로부터 연결 해제 요청 시 호출됨 |
| **`close**(ChannelhandlerContext, ChannelPromise)` | Channel을 닫는 요청 시 호출됨 |
| **`deregister**(ChannelHandlerContext, ChannelPromise)` | Channel을 EventLoop에서 등록 해제 요청 시 호출됨 |
| **`read**(ChannelHandlerContext)` | Channel에서 데이터를 읽기 요청 시 호출 |
| **`flush**(ChannelHandlerContext)` | Channel을 통해 원격 피어로 큐에 있는 데이터의 플러시 요청 시 호출됨 |
| **`write**(ChannelHandlerContext, Object, ChannelPromise)` | Channel을 통해 원격 피어로 데이터 기록 요청 시 호출됨 |

- 참고코드
    
    ```java
    public void connect() {
    	// ChannelFuture: I/O operation의 결과나 상태를 제공하는 객체
    	// 지정한 host, port로 소켓을 바인딩하고 incoming connections을 받도록 준비함
    
    	// 서버에 연결하고, 연결이 완료될 때까지 대기합니다.
    	ChannelFuture clientChannelFuture = bootstrap.connect(tcpPort);
    
    	// 연결 상태를 확인하기 위한 ChannelFutureListener 추가합니다.
    	clientChannelFuture.addListener((ChannelFutureListener) future -> {
    
    		// 연결 성공
    		if (future.isSuccess()) {
    			Channel channel = future.channel();
    			log.info("Connected to the server successfully.");
    
    			managers.forEach(manager -> manager.sendData(channel));
    
    		}
    		// 연결실패
    		else {
    			log.error("Failed to connect to the server. Cause: ", future.cause());
    		}
    	});
    
    	// 동기화를 대신에 채널에서 수행합니다.
    	clientChannel = clientChannelFuture.channel();
    	clientChannel.closeFuture().addListener((ChannelFuture future) -> log.info("Server channel closed."));
    }
    ```
    
    ```java
    public <T> void sendData(Channel channel, String dataType, T data) {
    
    	// 데이터 전송시간 ex) 2023-04-17/10:12:34.123
    	LocalDateTime currentTime = LocalDateTime.now();
    	long unixTimestamp = currentTime.toEpochSecond(ZoneOffset.UTC);
    
    	String combinedData = clientName + " " + dataType + " " + data + " " + unixTimestamp;
    
    	ChannelFuture future = channel.writeAndFlush(combinedData);
    
    	future.addListener((ChannelFutureListener)channelFuture -> {
    		if (!channelFuture.isSuccess()) {
    			log.error("Failed to send data. Retrying...");
    
    			// TODO 실패시 로직 처리
    
    		} else {
    			log.info("Data sent successfully. Data:");
    		}
    	});
    }
    ```
    
</aside>

## *이벤트 이동 경로 및 메서드 실행*

<aside>
✍️ **NOTE**

- **서로 다른 이벤트 메서드를 구현한 이벤트 핸들러 등록**
    - 이벤트 핸들러 등록 순서에 관계없이 이벤트 순서에 따라 실행
- **같은 이벤트 메서드를 구현한 이벤트 핸들러 등록**
    - 먼저 등록된, 이벤트 핸들러의 메서드만 호출되고 이벤트를 소모함
    - 두번째 이벤트 핸들러의 메서드도 호출하고 싶으면 첫번째 이벤트 핸들러에서 `ctx.fireChannelRead()`같은 방법으로 직접 이벤트 발생시켜 넘겨줌

```java
ChannelPipeline p = channel().pipeline();
p.addLast("1", new InboundReadHandler());
p.addLast("2", new InboundActiveHandler());
p.addLast("3", new OutboundWriteHandler());
p.addLast("4", new OutboundWriteHandler());
p.addLast("5", new ChannelDuplexHandler());
```

</aside>

## *코덱*

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20Netty%5D%2004%20%EC%B1%84%EB%84%90%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%EC%BD%94%EB%8D%B1%20%E2%AD%90/Untitled%203.png)

- **인코더**
    - 전송할 데이터를 전송 프로토콜에 맞춰 변환
    - ChannelOutboundHandler
- **디코더**
    - 수신한 데이터를 전송 프로토콜에 맞춰 변환
    - ChannelInboundHandler
</aside>