# [Spring WebSocket] 01-1. HTTP통신과 TCP통신의 개념

주제: Spring Netty

- 참고
    
    [HTTP 통신과 TCP 통신 그리고 웹 소켓에 대한 기본 개념 정리](https://sooolog.dev/HTTP-%ED%86%B5%EC%8B%A0%EA%B3%BC-TCP-%ED%86%B5%EC%8B%A0-%EA%B7%B8%EB%A6%AC%EA%B3%A0-%EC%9B%B9-%EC%86%8C%EC%BC%93%EC%97%90-%EB%8C%80%ED%95%9C-%EA%B8%B0%EB%B3%B8-%EA%B0%9C%EB%85%90-%EC%A0%95%EB%A6%AC/)
    
    [[C#] TCP/IP 프로토콜과 소켓 프로그래밍](https://itmining.tistory.com/127)
    

# **HTTP통신과 TCP통신의 개념**

---

## OSI(Open Systems Interconnection) 7 Layer

<aside>
✍️ **NOTE**

> *지금 우리가 배우려하는 **HTTP**와 **TCP**는 **모두 특정 layer(계층)의 규약으로 해석할 수 있다.***
> 

![TCP는 4계층, HTTP는 7계층](%5BSpring%20WebSocket%5D%2001-1%20HTTP%ED%86%B5%EC%8B%A0%EA%B3%BC%20TCP%ED%86%B5%EC%8B%A0%EC%9D%98%20%EA%B0%9C%EB%85%90/Untitled.png)

TCP는 4계층, HTTP는 7계층

![각 7계층마다 프로토콜 사용방식의 헤더를 받는다 (= 패킷)](%5BSpring%20WebSocket%5D%2001-1%20HTTP%ED%86%B5%EC%8B%A0%EA%B3%BC%20TCP%ED%86%B5%EC%8B%A0%EC%9D%98%20%EA%B0%9C%EB%85%90/Untitled%201.png)

각 7계층마다 프로토콜 사용방식의 헤더를 받는다 (= 패킷)

### OSI 7계층

- iSO(국제표준기구)에서 만든 네트워크 7계층
- 데이터를 받기위해선 1→7계층을 거쳐야한다. ⇒ **HTTP도 TCP 통신을 거쳐야한다.**

### Protocol

- 상호간의 접속이나, 통신방식, 주고받을 자료의 형식, 오류 검출방식, 코드 변환방식, 전송속도 등에 대하여 이미 정해진 약속
</aside>

## TCP 통신

<aside>
✍️ **NOTE**

- **3-way-handshake**라는 과정을 거치고 **연결이 이루어진다.**
- **4-way-handshake**라는 과정을 거치고 **연결이 종료된다.**
- **TCP 통신**에서는 **소켓을 이용한 연결방식을 사용한다**
    - 양방향 통신이 가능해진다!
    - 클라이언트와 서버가 서로 요청을 보낼 수 있는 개념
</aside>

## **HTTP통신**

<aside>
✍️ **NOTE**

> ***HTTP통신** 역시 **TCP** 위에서 이루어지는 방식인데 **어떤점이 다른걸까?***
> 

![TCP의 연결 - 전송 - 종료 이미지](%5BSpring%20WebSocket%5D%2001-1%20HTTP%ED%86%B5%EC%8B%A0%EA%B3%BC%20TCP%ED%86%B5%EC%8B%A0%EC%9D%98%20%EA%B0%9C%EB%85%90/Untitled%202.png)

TCP의 연결 - 전송 - 종료 이미지

- **TCP 통신의 흐름**은 `*connect → transmit → disconnect*`의 과정을 거친다.
- **HTTP 통신**의 흐름은 `*connect → transmit(HTTP 방식) → disconnect*`의 과정을 거친다.
    - `connect`와 `disconnect`는 **TCP의 방식**으로 처리
    - `transmit`을 **HTTP의 방식**으로 처리
- **HTTP 통신**과 **TCP 통신**의 차이점은 **단방향 통신이다.**

### 의문점

- **HTTP통신**은 **TCP**를 거쳐야하니, **3~4 way handshake** 과정을 거친다.
- **TCP**에서 **소켓을 사용**하여 연결과 끊음을 진행한다.
- 데이터 전송과정은 7계층에서 이루어지지만, 이거마저도 **TCP**를 사용한다.
- ❓ **TCP방식을 거의 다쓰는거 같은데 HTTP는 왜 TCP 처럼 양방향은 왜 안되냐?**

👏  HTTP 통신이 소켓 기반인 이유는 애초에 TCP기반이기 떄문이고, **데이터 전송할때 사용되는 소켓의 통신방식이 TCP와 다르게 동작하기 떄문이다.** 
(애초에 소켓이 사용되는 계층이 서로 다르다.)

</aside>

# **HTTP 프로그래밍과 소켓 프로그래밍**

---

## HTTP 프로그래밍

<aside>
✍️ **NOTE**

> ***HTTP 프로그래밍 ⇒  HTTP 통신을 하기위한 프로그래밍이다.***
> 

![HTTP의 대표적인 request/response](%5BSpring%20WebSocket%5D%2001-1%20HTTP%ED%86%B5%EC%8B%A0%EA%B3%BC%20TCP%ED%86%B5%EC%8B%A0%EC%9D%98%20%EA%B0%9C%EB%85%90/Untitled%203.png)

HTTP의 대표적인 request/response

- 하지만 HTTP에서도 소켓을 사용하므로, 꼭 소켓을 사용한다고 해서 소켓 프로그래밍이라고 하지 않는다.
- 해당 **소켓이 어떠한 용도로 사용되느냐**에 따라서 HTTP 프로그래밍이 될수도, 소켓 프로그래밍이 될수도 있다.

---

***[📌 참고]***

- **HTTP 프로그래밍**은 단방향 통신이 가능하게 한다
- **HTTP 통신**의 목적은 애초에 **html, JSON, image 같은 파일전송에 있다!**
</aside>

## 소켓 프로그래밍

<aside>
✍️ **NOTE**

> ***소켓 프로그래밍 ⇒  실시간 서비스를 구현한다.***
> 

![Untitled](%5BSpring%20WebSocket%5D%2001-1%20HTTP%ED%86%B5%EC%8B%A0%EA%B3%BC%20TCP%ED%86%B5%EC%8B%A0%EC%9D%98%20%EA%B0%9C%EB%85%90/Untitled%204.png)

- 동영상 Streaming이나, 실시간 채팅을 구현할 때 사용함
- 주로 웹 소켓이라는 기술 사용
</aside>