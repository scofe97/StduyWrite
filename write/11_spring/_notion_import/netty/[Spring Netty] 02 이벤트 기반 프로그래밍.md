# [Spring Netty] 02. 이벤트 기반 프로그래밍

주제: Spring Netty

- 참고
    
    [event driven · nene](https://pparkhyung.gitbooks.io/nene/content/event_driven.html)
    
    [Netty 주요 특징](https://shortstories.gitbook.io/studybook/netty/c8fc_c694_d2b9_c9d5)
    

# **이벤트 기반 프로그래밍**

---

<aside>
💡 **NOTE**

> *각 이벤트를 정의해두고 **이벤트가 발생했을 때 실행될 코드를 준비해둔다.***
> 
- 이벤트가 발생하면 알림(notification)을 발생하여 등록된 이벤트 처리 구문을 자동으로 수행시킨다.
- **비동기 호출을 지원하는 디자인 패턴**
    - 티켓을 활용한 퓨처 패턴
    - **이벤트 리스너 (옵저버 패턴)**
    - Node.js(콜백 함수)
    - **Netty(리액터 패턴)**
    

### 프로그래밍 방식의 변화

- Sync I/O -> Multi Thread -> Thread Pool -> Non-Blocking(selector) -> Event-Driven -> **Reactor**
</aside>

## ***이벤트 기반 네트워크 프로그래밍***

<aside>
✍️ **NOTE**

> ***이벤트를 발생시키는 객체와 발생될 이벤트 종류를 정의한다.***
> 

![Untitled](%5BSpring%20Netty%5D%2002%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D/Untitled.png)

- 이벤트 발생 주체 → ‘소켓’
- 이벤트 종류 → 소켓연결, 데이터 송수신이다.

![Untitled](%5BSpring%20Netty%5D%2002%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D/Untitled%201.png)

- Netty는 데이터를 소켓으로 접근하기 위해 채널에 직접 `read/write` 하지 않고 **데이터 핸들러**를 통한다.
    - 서버 코드를 클라이언트에서 재사용 가능
    - 이벤트에 따라 로직 분리
    - Netty의 이벤트 핸들러는 에러 이벤트도 같이 정의
    (에러처리 부담이 낮아짐)
</aside>

## ***리액터(reactor) 패턴***

<aside>
✍️ **NOTE**

- **이벤트를 반응하는 객체(reactor)**를 만들어, 이벤트가 발생하면 application대신 reactor가 대신 처리한다.
- reactor는 이벤트가 발생하길 기다리고, 이벤트가 발생하면 event handler에게 이벤트를 전달한다.
- event handler는 상황에 맞는 이벤트 처리 로직을 작성해야 한다.
</aside>

## ***퓨처(future) 패턴***

<aside>
✍️ **NOTE**

- 함수 호출을 하면 결과 성공 여부를 확인할 수 있는 futuer객체를 즉시 리턴한다.
- future객체를 통해 성공/실패 여부, 에러 발생여부를 확인한다.
- 주기적으로 확인(while문 등)하는 불편함이 발생한다.
    - 이를 해소하기 위해, 원하는 이벤트(작업완료, 에러발생)가 발생하면 그 이벤트에 맞는 객체(Listener)를 미리 등록하여 이벤트 통지를 받아 수행하도록 프로그래밍할 수 있다.

- **이벤트 리스너**는 옵저버패턴이다.
- **퓨처 패턴**은 프로미스 패턴이라고 불리기도 한다.
</aside>