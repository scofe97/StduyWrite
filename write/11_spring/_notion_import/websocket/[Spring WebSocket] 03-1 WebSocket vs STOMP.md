# [Spring WebSocket] 03-1. WebSocket vs STOMP

주제: Spring Netty

- 참고
    
    [동아리 홈페이지 투표 개발 2 - WebSocket과 STOMP](https://woo-chang.tistory.com/46)
    
    [Spring Websocket & STOMP](https://brunch.co.kr/@springboot/695)
    

# **WebSocket**

---

<aside>
💡 **NOTE**

> ***하나의 TCP 접속에 전이중 통신을 제공하는 컴퓨터 통신 프로토콜이다!***
> 
- TCP를 간단히 설명하자면 인터넷에서 해당 프로토콜의 단위인 세그먼트를 안정적으로, 순서대로 에러 없이 보내도록 하는 프토콜이다.
- 웹소켓은 OSI 모델 계층에서 Application Layer에 위치하기에 하위 Transport Layer의 TCP에 의존하고 있다.
</aside>

## **WebSocket HandShake**

<aside>
✍️ **NOTE**

> *연결을 위해 웹소켓 초기화 과정이 필요하며, 이를 **WebSocket HandShake**라고 한다.*
> 

![Untitled](%5BSpring%20WebSocket%5D%2003-1%20WebSocket%20vs%20STOMP/Untitled.png)

- **클라이언트**는 **HandShake** 요청을 전송하고 이에 대한 응답을 받게 된다.

### 요청 헤더

```json
GET /chat HTTP/1.1
Host: localhost:8000
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

- **Upgrade**
    - 프로토콜을 전환하기 위해서 사용하는 헤더
    - 웹소켓 요청시 반드시 websocket이라는 값을 가져야 한다.
- **Connection**
    - 현재의 전송이 완료된 후 네트워크 접속을 유지할 것인가에 대한 헤더 정보
    - 웹소켓 요청 시 반드시 Upgrade라는 값을 가져야 한다.
- **Sec-WebSockey-Key**
    - 유효한 요청인지 확인하기 위해 사용하는 키값이다.
- **Sec-WebSocket-Version**
    - 클라이언트가 사용하고자 하는 웹소켓 프로토콜 버전이다.

### 응답 헤더

```json
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

- Sec-WebSocket-Accept
    - 요청의 Sec-WebSocke-Key에 유니크 값을 더해 SHA-1로 해싱 후 base64로 인코딩한 결과
    - 웹소켓 연결의 시작을 알린다.
</aside>

# STOMP

---

<aside>
💡 **NOTE**

> ***메시지 전송을 효율적으로 처리하기 위한 프로토콜이다!***
> 
- **STOMP**는 SImple Text Oriented Messaging Protocol의 약자로, 메시징 전송을 효율적으로 하기 위한 프로토콜로, **pub/sub 방식으로 동작**한다.

### WebSocket보다 편리한점

- **WebSocket** 프로토콜은 `Text`, `Binary` 두 가지 메시지 타입은 정의하지만 메시지의 내용에 대해서는 정의하지 않는다.
- 따라서 **WebSocket**만 사용하게 되었을 때, 메시지가 어떤 요청인지, 어떤 형식인지, 어떻게 처리해야 하는지 정해져 있지 않아 별도의 구현이 필요하다.
- 이를 해결하기 위해 **STOMP**를 서브 프로토콜로 **WebSocket**위에서 사용한다.
</aside>

## ***PUB/SUB(발행/구독)에 대한 이해***

<aside>
✍️ **NOTE**

발행자의 메시지의 타겟을 `no01`로 설정해 메세지를 보냈는데, 서버에서는 발행자의 메세지를 확인한 후 `no01`을 구독하는 **모든 사용자(클라이언트)에게 메세지를 보낸다.**

![2명의 클라이언트가 있으며, 구독하는 주소를 no01로 둔다.](%5BSpring%20WebSocket%5D%2003-1%20WebSocket%20vs%20STOMP/Untitled%201.png)

2명의 클라이언트가 있으며, 구독하는 주소를 no01로 둔다.

다음 이미지에서 사용자3은 `no02`를 구독하기에 `no01` 메세지를 받지 못한다.

![구독 url이 다르다면 메세지를 받지 못한다!](%5BSpring%20WebSocket%5D%2003-1%20WebSocket%20vs%20STOMP/Untitled%202.png)

구독 url이 다르다면 메세지를 받지 못한다!

채팅 메시지는 단방향으로 받기만 하지 않고, 서로 메세지를 주고 받는다.

![채팅의 경우 구독과 발행을 동시에 진행한다](%5BSpring%20WebSocket%5D%2003-1%20WebSocket%20vs%20STOMP/Untitled%203.png)

채팅의 경우 구독과 발행을 동시에 진행한다

![각 클라이언트는, 구독중인 데이터를 받기위한 queue가 존재한다.](%5BSpring%20WebSocket%5D%2003-1%20WebSocket%20vs%20STOMP/Untitled%204.png)

각 클라이언트는, 구독중인 데이터를 받기위한 queue가 존재한다.

</aside>