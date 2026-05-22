# [Spring Netty] 06-2. Spring Netty Client 구현

주제: Spring Netty

- 참고
    
    https://github.com/Jsing/netty-network-programming
    
    [Spring - 스프링 프로젝트에서 netty사용하기](https://myhappyman.tistory.com/172)
    
    [Spring Boot Reactor Netty Configuration | Baeldung](https://www.baeldung.com/spring-boot-reactor-netty)
    
    [Spring Boot Netty Client 서버에 접속 프로그램 전체 프로그램 첨부](https://m.blog.naver.com/codebrain0110/220923546688)
    

# *Spring Netty Client*

---

## *InetSocketAddress*

<aside>
✍️ **NOTE**

```java
@Bean
public InetSocketAddress dataInetSocketAddress() {
	return new InetSocketAddress(host, dataPort);
}
```

</aside>

## *BootStrap*

<aside>
✍️ **NOTE**

```java
@Bean
public Bootstrap nettyBootstrap(EventLoopGroup eventLoopGroup) {
	Bootstrap bootstrap = new Bootstrap()
		.group(eventLoopGroup) // 이벤트 루프 설정
		.channel(NioSocketChannel.class) // 소켓 입출력 모드 설정
		.option(ChannelOption.TCP_NODELAY, true) // TCP_NODELAY 소켓 옵션을 설정(Nagle 알고리즘 사용 X)
		.option(ChannelOption.ALLOCATOR, PooledByteBufAllocator.DEFAULT); // PooledByteBufAllocator 사용
	return bootstrap;
}
```

- **TCP_NODELAY**
    - Nagle 알고리즘을 활성/비활성화 하는 코드
    - Nagle 알고리즘 → 작은 패킷을 모아서 한번에 보내는 알고리즘 (혼잡도는 줄지만, 대기시간이 늘어남)
    - 전송시간 증가, 트래픽도 증가.. (현재 작은 데이터를 자주보내므로,  어울린다고 판단)
- **PooledByteBufAllocator**
    - Netty의 바이트 버퍼 할당자
    - 메모리 할당과 해제이 관련된 오버헤드를 줄이기 위해 메모리를 풀(Pool)에서 가져오거나 반환하는 방식 사용
    - 메모리를 재사용하므로, 성능 향상과 메모리 사용량 감소 기대.
    - **PooledByteBufAllocator.DEFAULT**는 기본 인스턴스를 사용하므로 동일한 인스턴스를 여러 채널에서 공유하게 된다.
</aside>

## *connect*

<aside>
✍️ **NOTE**

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

</aside>