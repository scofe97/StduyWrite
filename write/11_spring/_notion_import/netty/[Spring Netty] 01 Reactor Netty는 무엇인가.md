# [Spring Netty] 01. Reactor Netty는 무엇인가?

주제: Spring Netty
연관 노트: [Java Study] 14-x. 소켓 프로그래밍 (https://www.notion.so/Java-Study-14-x-167da0b10b234316a48731cedfef316e?pvs=21), [Spring Netty] 동기/비동기 (https://www.notion.so/Spring-Netty-03453463e46f4e51bcad385bcba89de4?pvs=21)

- 참고
    
    [https://godekdls.github.io/Reactor Netty/gettingstarted/](https://godekdls.github.io/Reactor%20Netty/gettingstarted/)
    
    [자바 네트워크 소녀 Netty 정리](https://velog.io/@monami/Netty)
    
    [Spring Boot + Netty TCP 소켓 서버 (1) 프레임워크 선택 배경 - i-hope devlog](https://i-hope9.github.io/2020/12/08/SpringBoot-Netty-1-Background.html)
    
    [Spring Webflux - Netty 기본 개념](https://velog.io/@wnwjq462/Spring-Webflux-Netty-기본-개념)
    
    [Netty의 개념과 아키텍처](https://javacoding.tistory.com/143)
    

# Reactor Netty

---

<aside>
💡 **NOTE**

> *마이크로서비스 아키텍쳐에 적합한 **리액터 네티는 HTTP(웹소켓 포함), TCP, UPD**를 통한 네트워크 엔진을 제공한다.*
> 

![Untitled](%5BSpring%20Netty%5D%2001%20Reactor%20Netty%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80/Untitled.png)

- 순수 자바 코드로 소켓 프로그래밍을 작성하는 것보다 훨씬 편하게 코드 작성이 가능해짐!
    - 추상화
    - 안정적
    - 빠름

### ✅ Netty 장점

- TCP, SSL 지원
- byte stream 데이터를 쉽게 읽어올 수 있도록 제공하는 ByteBuf클래스가 존재!
- 자바 NIO 사용을 쉽게 할 수 있도록 지원하여 한 번에 여러 기기와 통신 가능!
- 통신(Channel)내 Context유지 가능, (세션관리가 가능)
</aside>

## **논블로킹 소켓의 동작방식**

<aside>
✍️ **NOTE**

![언제든 읽기/쓰기 작업의 완료상태를 확인할 수 있어, 한 스레드로 동시에 연결을 처리해줌.](%5BSpring%20Netty%5D%2001%20Reactor%20Netty%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80/Untitled%201.png)

언제든 읽기/쓰기 작업의 완료상태를 확인할 수 있어, 한 스레드로 동시에 연결을 처리해줌.

![Netty는 소켓의 모드와 상관없이 개발할 수 있도록, 추상화된 API를 제공한다.](%5BSpring%20Netty%5D%2001%20Reactor%20Netty%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80/Untitled%202.png)

Netty는 소켓의 모드와 상관없이 개발할 수 있도록, 추상화된 API를 제공한다.

- **논블로킹 소켓에서의 read 메서드**
    - 클라이언트가 아직 전송하지 않았거나, 데이터가 수신 버퍼까지 도달하지 않았다면, read메서드는 0을 리턴한다.
    - 비동기 호출이나 논블로킹 소켓을 사용하면 프로그램 복잡도가 증가한다.
    **(하지만 Netty는 이를 편하게 만들어줌!)**
</aside>