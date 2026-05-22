# [Spring WebSocket] 01-2. HTTP vs Socket

주제: Spring Netty

- 참고
    
    [WebSocket & Spring](https://velog.io/@guswns3371/WebSocket-Spring)
    
    [Spring Websocket & STOMP](https://brunch.co.kr/@springboot/695)
    

# HTTP

---

<aside>
💡 **NOTE**

> ***Client**의 요청이 있을때만, **Server**가 응답해서 **정보를 전송하고 곧바로 연결을 끊는 방식!***
> 

![한쪽에서만 요청하고 반대쪽에서 응답함](%5BSpring%20WebSocket%5D%2001-2%20HTTP%20vs%20Socket/Untitled.png)

한쪽에서만 요청하고 반대쪽에서 응답함

- **Clinet ➡️ Server(Request)**,  **Clinet** ⬅️ **Sever(Resposne)** 형식의 **단방향통신.**
- 연결상태를 유지하지 않음 `stateless`
- 매 요청마다 대량의 정보를 만들어서 통신해야한다.

### HTTP의 실시간 통신 방식

- Polling
- Long Polling
- Streaming
</aside>

## Polling

<aside>
✍️ **NOTE**

> *브라우저가 **일정한 주기마다 서버에 HTTP 요청을 보내주는 방식***
> 

![Untitled](%5BSpring%20WebSocket%5D%2001-2%20HTTP%20vs%20Socket/Untitled%201.png)

- 실시간 데이터의 업데이트 주기는 예측 불가능하므로, 불필요한 요청에 따른 서버 및 네트워크 과부하가 발생한다
- 실시간 야구 문자 중계같이 5~10초마다 주기로 계속 업데이트 한다.
- **☑️ 이벤트가 없어도 요청 → 서버 클라 부담**

### 단점

- time interval을 어떻게 잡냐에 따라 서버의 부하가 올라가거나 실시간성이 떨어지는 trade off 관계를 갖는다
</aside>

## long Polling

<aside>
✍️ **NOTE**

> ***HTTP 요청** 시 서버는 해당 **연결을 바로 해제하지 않고, 일정시간 대기하는 방식***
> 

![Untitled](%5BSpring%20WebSocket%5D%2001-2%20HTTP%20vs%20Socket/Untitled%202.png)

- **polling**의 서버 부하를 줄이면서 실시간 성을 높이기 위한 방식
- 서버에 연결 요청을 보내놓고 **서버는 이벤트가 발생하면 응답, 다시 연결**
- **☑️ 이벤트가 발생하면 모든 클라이언트에게 동시에 응답을 보내고, 연결을 끊고 새로운 요청을 받는다 → 서버부담**

### 단점

- 여러 클라이언트와 잦은 데이터 변경이 일어나면 서버의 부담이 크다.
</aside>

## Streaming

<aside>
✍️ **NOTE**

> *요청에 대한 응답을 완료하지 않은 상태에서 **계속해서 데이터를 받는 방식이다.***
> 

![Untitled](%5BSpring%20WebSocket%5D%2001-2%20HTTP%20vs%20Socket/Untitled%203.png)

- **long polling**의 연결구축에 대한 부하를 해결하는 방식이다.
- 서버는 무한정 혹은 일정 시간동안 요청을 대기시키고, chunked 메시지를 이용해서 응답 시 연결을 계속 유지한다.
- **☑️  서버에 연결 요청을 보내놓고 계속해서 응답 데이터를 다운받는다. 서버는 이벤트가 발생하면 응답을 보낸다( 클라이언트 → 서버 데이터 전송이 힘들다.)**

### 단점

- 클라이언트에서 서버로 데이터를 보내는게 힘들다.
</aside>

# Socket 통신

---

<aside>
💡 **NOTE**

> ***Client**와 **Server**가 **특정port**를 통해 연결을 성립하고 있어, **실시간으로 양방향 통실을 하는 방식!***
> 

![화살표가 양쪽으로 자유롭게 요청, 응답](%5BSpring%20WebSocket%5D%2001-2%20HTTP%20vs%20Socket/Untitled%204.png)

화살표가 양쪽으로 자유롭게 요청, 응답

- **Clinet ↔ Server** 형식의 양방향 통신 (Server도 Clinet에게 요청을 보낼 수 있다)
- 연결상태를 유지한다 `stateful`
- **최초의 hansshake 과정**에서는 **HTTP 프로토콜**을 이용하기 떄문에, 기존의 HTTP와 비슷하게 데이터를 주고 받지만, **이후에는 간단한 데이터만 오고 간다.**
</aside>

## 웹 소켓

<aside>
✍️ **NOTE**

> ***7계층에서 양방향 통신을 위해서 만들어진 protocol 기술!***
> 
- 일반 소켓(TCP 기반 소켓) 처럼 양방향 실시간 통신이 가능하며, IP와 포트를 사용한 통신을 한다는 점에서 공통점이 있다
- 하지만, 웹 소켓은 기본적으로 HTTP 기반(7 계층)에서 작동하며, 일반 소켓은 TCP기반(4계층)에서 작동한다.

![웹 소켓 통신](%5BSpring%20WebSocket%5D%2001-2%20HTTP%20vs%20Socket/Untitled%205.png)

웹 소켓 통신

- 웹 소켓은 **WebSocket 프로토콜**이라는 새로운 규약에서 이루어진다.
- 웹 소켓 통신을 위한 별도의 port는 없으며 **port 80**, **443**을 사용하도록 설계되었다.
    - **HTTP -** **80,** **HTTPS -** **443**에서 이루어지므로 **HTTP**, **HTTPS**와 호환된다!
</aside>

# **HTTP vs Socket**

---

<aside>
💡 **NOTE**

![Untitled](%5BSpring%20WebSocket%5D%2001-2%20HTTP%20vs%20Socket/Untitled%206.png)

![HTTP vs 웹소켓 짤비교](%5BSpring%20WebSocket%5D%2001-2%20HTTP%20vs%20Socket/Untitled%207.png)

HTTP vs 웹소켓 짤비교

</aside>