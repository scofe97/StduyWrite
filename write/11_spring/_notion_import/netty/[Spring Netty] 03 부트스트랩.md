# [Spring Netty] 03. 부트스트랩

주제: Spring Netty

- 참고
    
    [Netty 부트스트랩](https://shortstories.gitbook.io/studybook/netty/bd80_d2b8_c2a4_d2b8_b7a9)
    
    [Netty(2) - Bootstrap](https://kimyhcj.tistory.com/426)
    
    [자바 네트워크 소녀 Netty 정리](https://velog.io/@monami/Netty)
    
    [#Nettty Framework - 부트스트랩 (bootstrap)](https://swiftymind.tistory.com/26)
    

# **Netty 부트스트랩**

---

<aside>
💡 **NOTE**

> *Netty로 작성한 네트워크 프로그램이 시작할 때 가장 먼저 수행되는 일.*
> 

![논리적 구조](%5BSpring%20Netty%5D%2003%20%EB%B6%80%ED%8A%B8%EC%8A%A4%ED%8A%B8%EB%9E%A9/Untitled.png)

논리적 구조

![Bootstrap으로 Channel 생성](%5BSpring%20Netty%5D%2003%20%EB%B6%80%ED%8A%B8%EC%8A%A4%ED%8A%B8%EB%9E%A9/Untitled%201.png)

Bootstrap으로 Channel 생성

- 어플리케이션이 수행할 동작을 지정
- 프로그램에 대한 각종 설정을 지정한다.

- **예제코드**
    
    ```java
    public EchoServer() {
      bossGroup = new NioEventLoopGroup(1);
      workerGroup = new NioEventLoopGroup();
    
      bootstrap = new ServerBootstrap();
      bootstrap.group(bossGroup, workerGroup) // 1
          .channel(NioServerSocketChannel.class) // 2
          .childHandler(new ChannelInitializer<SocketChannel>() { // 3
            @Override
            protected void initChannel(SocketChannel socketChannel) throws Exception {
              ChannelPipeline pipeline = socketChannel.pipeline();
              // 핸들러 설정
              pipeline.addLast(new EchoServerHandler());
            }
          });
    }
    ```
    
</aside>

## *부트스트랩에서 설정가능한 내용*

<aside>
✍️ **NOTE**

- **이벤트 루프**
    - 소켓채널에서 발생한 이벤트를 처리하는 스레드모델에 대한 구현이 담겨있다.
- **채널 전송 모드 (소켓 모드 및 I/O 종류)**
    - 블로킹/논블로킹/epoll
- **채널 파이프라인**
    - 소켓 채널로 수신된 데이터를 처리할 핸들러를 지정한다.
- 소켓 주소와 포트
- 소켓 옵션
- 프로토콜

- 🤔 네트워크에서 수신한 데이터를 단일 스레드 DB에 저장하는 프로그램 (8080포트 사용, NIO 소켓모드)
    - **채널 전송모드**
        - 서버 소켓채널 NIO 사용
    - **채널 파이프라인**
        - 데이터 핸들러(이벤트 핸들러) → DB에 저장하는 로직
    - **이벤트 루프**
        - 단일 스레드를 지원하는 이벤트 루프 설정
    - 8080포트 바인딩
</aside>

# ***부트스트랩의 구조***

---

<aside>
💡 **NOTE**

> ***서버**를 위한 **ServerBootstrap**, **클라이언트**를 위한 **BootStrap**으로 나뉜다.*
> 
- 부트스트랩을 사용하면 네트워크 어플리케이션 작성시 유연성을 얻을 수 있다.
- 만약 NonBlockingServer와 BlockingServer의 경우, 소켓 채널 입출력 방식이 변경되어야 하면 소스코드 수정할 양이 무지막지하게 많다.
- 반면 **Netty를 사용한다면, 데이터 처리하는 코드를 변경하지 않고 부트스트랩의 설정만 변경해주면 된다!**
    - 이는 소켓 채널에 대한 입출력을 우아하게 추상화 했기 때문에 가능!
</aside>

## ***ServerBootstrap API***

<aside>
✍️ **NOTE**

- **group - 이벤트 루프 설정**
    - 클라이언트는 연결 요청 완료 후 데이터 송수신 처리를 위해 하나의 이벤트 루프로 모든 처리를 진행한다.
    - 서버는 연결 요청 수락을 위한 루프 그룹, 데이터 송수신 처리를 위한 루프 그룹 2가지가 필요하다.
        - EventLoopGroup(부모 스레드 그룹)
            - 클라이언트의 연결을 수락하는 역할
        - EventLoopGroup(자식 스레드 그룹)
            - 클라이언트 소켓과 연결된 소켓의 데이터 입출력 및 이벤트 처리를 담당
            
- **channel - 소켓 입출력 모드 설정**
    - 부트스트랩 클래스를 통해 채널의 입출력 모드를 설정할 수 있다.
    - 설정가능한 클래스 목록
        - LocalServerChannel.class
        - OioServerSocketChannel.class
        - NioServerSocketChannel.class
        - EpollServerSocketChannel.class
        
- **channelFactory - 소켓 입출력 모드 설정**

- **handler - 서버 소켓 채널의 이벤트 핸들러 설정**
    - 서버 소켓의 채널의 이벤트 핸들러 설정

- **chilHandler - 클라이언트 소켓 채널의 데이터 가공 핸들러 설정**
    - 클라이언트 소켓 채널로 송수신되는 데이터 가공 핸들러 설정

- **option - 서버 소켓 채널의 소켓 옵션 설정**

- **childOpion - 클라이언트 소켓 채널의 소켓 옵션 설정**

</aside>

## ***Bootstrap API***

<aside>
✍️ **NOTE**

- 기본적으로 ServerBootstrap과 같고, 몇가지 측면에서 미세한 차이들을 가진다.
- 클라이언트에서 사용하는 단일 소켓 채널에 대한 설정이므로 부모 자식이라는 관계에 해당하는 API들은 없다.
</aside>