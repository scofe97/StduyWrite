# [Spring Netty] 06-1. Spring Netty Component 및 Architecture (Server 구현) ⭐

주제: Spring Netty
연관 노트: [Java Study] 14-x. 소켓 프로그래밍 (https://www.notion.so/Java-Study-14-x-167da0b10b234316a48731cedfef316e?pvs=21)

- 참고
    
    [Netty의 기본 Component 및 Architecture](https://effectivesquid.tistory.com/entry/Netty의-기본-Component-및-Architecture)
    
    [Netty 채널 소개와 채널 핸들러](https://happygrammer.github.io/netty/handler/)
    
    [[ 네티 인 액션 ] 7. EventLoop와 스레딩 모델](https://velog.io/@qkrqudcks7/네티-인-액션-7.-EventLoop와-스레딩-모델)
    
    [[NHN FORWARD 2021] AI펭톡 TCP Gateway 서버 개발기 with Netty](https://www.youtube.com/watch?v=pu2Y4nVWixo&ab_channel=NHNCloud)
    
    https://github.com/Jsing/netty-network-programming
    

# Netty Server

---

<aside>
💡 **NOTE**

> *모든 네티 서버에는 다음 항목이 필요하다*
> 

![Untitled](%5BSpring%20Netty%5D%2006-1%20Spring%20Netty%20Component%20%EB%B0%8F%20Archi/Untitled.png)

- **하나 이상의 ChannelHandler**
    - 이 컴포넌트는 클라이언트로부터 받은 데이터를 서버측에서 처리하는 비즈니스 논리를 구현한다.
- **부트스트랩**
    - 서버를 구성하는 시동 코드를 의미한다.
    - 최소한 서버가 연결 요청을 수신하는 포트 서버와 바인딩하는 코드가 있어야 한다.
    
- **Netty는 다음과 같은 Componet를 통해 데이터를 처리한다.**
    - `Channel`, `EventLoop`, `ChannelFuture`
    - `ChannelHandler`, `ChannelPipeline`
    - `Bootstrap`
</aside>

## ***Channel***

<aside>
✍️ **NOTE**

### 자바 네트워크

![Socket을 사용해서 bind, accept, read를 진행한다.](%5BSpring%20Netty%5D%2006-1%20Spring%20Netty%20Component%20%EB%B0%8F%20Archi/Untitled%201.png)

Socket을 사용해서 bind, accept, read를 진행한다.

- 기본 입출력 작업(`bind`, `connect`, `read`, `write`)은 네트워크 전송에서 제공하는 기본형을 이용한다.
- **자바 기반 네트워크 기본 구조는 Socket클래스이다.**

### Netty 네트워크

- **Netty**의 **Channel 인터페이스**는 Socket으로 직접 작업할 때의 복잡성을 크게 완화하는 API를 제공한다.
- **Netty**는 Channel 인터페이스를 구현한 몇가지 특수한 구현체를 제공한다 (**NioSocketChannel**만 알면된다)
    
    
    | **클래스** | **기능** |
    | --- | --- |
    | EmbeddedChannel | 실제 연결없이 ChannelHandlers 의 테스트를 할 수 있도록 구현한 채널 클래스 |
    | EpollChannel | 최대 성능을 위해 EPOLL Edge-Triggered Mode 를 사용 하는 Linux 용으로 최적화된 채널 클래스 |
    | KQueueChannel | jni 라이브러리를 사용 하는 채널 클래스 |
    | LocalChannel | 로컬 채널 클래스 |
    | NioServerChannel | NIO 채널 클래스 |
    | **NioSocketChannel** | NIO 소켓 클래스 |

</aside>

## ***EventLoop***

<aside>
✍️ **NOTE**

![EventLoop, Thread, EvnetLoopGroup 관계](%5BSpring%20Netty%5D%2006-1%20Spring%20Netty%20Component%20%EB%B0%8F%20Archi/Untitled%202.png)

EventLoop, Thread, EvnetLoopGroup 관계

- EventLoop는 연결의 수명주기 중 발생하는 이벤트를 처리하는 Netty의 핵심 추상화를 정의한다.
- Netty의 스레드 처리 모델은 내용이 많으므로 별도의 글을 통해 설명하겠다.
</aside>

## ***ChannelFuture***

<aside>
✍️ **NOTE**

```java
// ChannelFuture: I/O operation의 결과나 상태를 제공하는 객체
// 지정한 host, port로 소켓을 바인딩하고 incoming connections을 받도록 준비함
ChannelFuture serverChannelFuture = serverBootstrap.bind(tcpPort).sync();
```

- 네티의 모든 I/O 처리는 비동기식이다.
- 비동기식은 I/O 작업의 호출이 완료 여부와 상관없이 즉시 반환되며, 이때 **ChannelFuture 인터페이스를 통해서 I/O처리가 완료 되었는지 확인 하고 결과를 검색할 수 있다.**

- **ChannelFuture 함수**
    - `addListener()`
        - 작업 리스너 등록
    - `removeListener()`
        - 작업 리스너 제거
    - `await()`
        - I/O 작업 완료 대기
    - `sync()`
        - I/O 작업 대기중 실패 하면 실패 이유 반환
</aside>

## ***ChannelHandler***

<aside>
✍️ **NOTE**

### ChannelInobundHandler

- Channel의 입력 데이터 처리
- `channelRead()`
    - 메시지가 들어올때 마다 호출된다.
- `channelReadComplete()`
    - channelRead()의 마지막 호출에서 현재 일관 처리의 마지막 메시지를 처리했음을 통보
- `exceptCaught()`
    - 읽기 작업중 예와 발생시 나온다.

### ChannelOutboundHandler

- Channel의 출력 데이터를 처리
- `bind()`
- `connect()`
- `read()`
- `flush()`
</aside>

## ***ChannelPipeline, ChannelHandlerContext, ChannelInitializer***

<aside>
✍️ **NOTE**

> ***ChannelHandler 체인을 위한 컨테이너를 제공하며, 체인 상에서 인바운드 아웃바운드 이벤트를 전파하는 API를 정의한다!***
> 
- Channel이 생성되면, 여기에 자동으로 자체적인 ChannelPipeline이 할당된다.
    1. `ChannelInitializer`구현체를 `ServerBootstrap`에 등록한다.
    2. `ChannelInitializer.initChannel()`이 호출되면 `ChannelInitializer`가 `ChannelHandler`의 커스텀 집합을 파이프라인에 설치한다.
    3. `ChannelInitializer`는 `ChannelPipeline`에서 자신을 제거한다.

![***ChannelInboundHandler, ChannelOutboundHandler**의 구현을 구분해서, 핸들러간 데이터 전달이 동일한 방향으로 수행되도록한다.*](%5BSpring%20Netty%5D%2006-1%20Spring%20Netty%20Component%20%EB%B0%8F%20Archi/Untitled%203.png)

***ChannelInboundHandler, ChannelOutboundHandler**의 구현을 구분해서, 핸들러간 데이터 전달이 동일한 방향으로 수행되도록한다.*

```java
@Component
@RequiredArgsConstructor
public class NettyChannelInitializer extends ChannelInitializer<SocketChannel> {

	private final NettyHandler nettyHandler;

	@Override
	protected void initChannel(SocketChannel socketChannel) throws Exception {
		ChannelPipeline pipeline = socketChannel.pipeline();

		pipeline.addLast(nettyHandler);
	}
}
```

### ChannelHandlerContext

- **ChannelHandler**와 **ChannlerPipeline**간 연결을 나타낸다.
- **ChannelHandler**를 **ChannelPipeline**에 추가시 할당

### ChannelInitializer

- 여러 **ChannelHandler**를 **CahnnelPipeline**에 할당하기 위한 클래스
- **Channel** 생성 시 호출
</aside>

## *Bootstrap*

<aside>
✍️ **NOTE**

```java
@Bean
public ServerBootstrap serverBootstrap(NettyChannelInitializer nettyChannelInitializer) {

	// boss: incoming connection을 수락하고, 수락한 connection을 worker에게 등록(register)
	// worker: boss가 수락한 연결의 트래픽 관리
	NioEventLoopGroup bossGroup = new NioEventLoopGroup(bossCount);
	NioEventLoopGroup workerGroup = new NioEventLoopGroup(workerCount);

	// ServerBootstrap: 서버 설정을 도와주는 class
	ServerBootstrap b = new ServerBootstrap();
	b.group(bossGroup, workerGroup)
		.channel(NioServerSocketChannel.class)
		.handler(new LoggingHandler(LogLevel.DEBUG))
		.childHandler(nettyChannelInitializer);

	b.option(ChannelOption.SO_BACKLOG, backlog);
	return b;
}
```

</aside>

## 진행순서 ⭐

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20Netty%5D%2006-1%20Spring%20Netty%20Component%20%EB%B0%8F%20Archi/Untitled%204.png)

```java
// 1. 부트스트랩에서 채널생성
@Bean
public ServerBootstrap serverBootstrap(NettyChannelInitializer nettyChannelInitializer) {

	// boss: incoming connection을 수락하고, 수락한 connection을 worker에게 등록(register)
	// worker: boss가 수락한 연결의 트래픽 관리
	NioEventLoopGroup bossGroup = new NioEventLoopGroup(bossCount);
	NioEventLoopGroup workerGroup = new NioEventLoopGroup(workerCount);

	// ServerBootstrap: 서버 설정을 도와주는 class
	ServerBootstrap b = new ServerBootstrap();
	b.group(bossGroup, workerGroup)
		.channel(NioServerSocketChannel.class) // NioServerSocket 사용
		.handler(new LoggingHandler(LogLevel.DEBUG)) // 
		.childHandler(nettyChannelInitializer);

	// SO_BACKLOG: 동시에 수용 가능한 최대 incoming connections 개수
	b.option(ChannelOption.SO_BACKLOG, backlog);
	return b;
}

// 2. 생성된 채널을 사용해 ChannelFuture 만든다.
// 지정된 TcpPort로 서버소켓을 바인딩하고 준비
ChannelFuture serverChannelFuture = serverBootstrap.bind(tcpPort).sync();

// 서버 소켓이 닫힐 때까지 기다림
serverChannel = serverChannelFuture.channel().closeFuture().sync().channel();

```

</aside>