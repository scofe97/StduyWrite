# [Spring Netty] NIO Connector 와 BIO Connector

주제: Spring Netty
연관 노트: [OS Stduy] 02-2. 비동기 프로그래밍, Non-Blocking (https://www.notion.so/OS-Stduy-02-2-Non-Blocking-edac32cd9909475396f2c649d8f43e8d?pvs=21)

- 참고
    
    [[Java] NIO](https://velog.io/@mmy789/Java-NIO-1)
    
    [19장. NIO 기반 입출력 및 네트워킹. -  ppt download](https://slidesplayer.org/slide/15151763/)
    
    [자바네트워크 제15주 Java NIO 버퍼, 채널, 셀렉터. -  ppt download](https://slidesplayer.org/slide/16177712/)
    

# **Connector**

---

<aside>
💡 **NOTE**

> *Servlet Container와 클라이언트를 연결시켜준다.*
> 
- **톰캣으로 첫 요청이 들어오는 곳이다.**
- **Connector**은 클라이언트의 요청을 받아 이를 토대로 **Servlet**이 처리 할 수 있는 `HttpServletResquest`를 생성한다.

### ✅ 요약

- NIO 쓰는이유
    - 불특정 다수의 클라이언트 연결을 None-Blocking이나 비동기 처리가 가능해져서 과도한 쓰레드 생성을 막을 수 있다.
- 이러한 장점 때문에, 톰캣에서 NIO방식을 이용한 NIO Connector을 사용
</aside>

## ***BIO Connector와 NIO Connector***

<aside>
✍️ **NOTE**

> ***Connector는 2가지 종류의 Connector가 존재한다.***
> 

|  | IO | NIO |
| --- | --- | --- |
| 입출력 방식 | **스트림 방식** | **채널 방식** |
| 버퍼 방식 | **넌버퍼** | **버퍼** |
| 비동기 방식 | 지원 안함 | 지원 |
| 블로킹/넌블로킹 유무 | 블로킹 방식만 지원 | 블로킹 / 넌블로킹 방식 모두 가능 |

### **BIo Connector(Blocking IO 방식)**

- 기존 **자바에서 사용하는 방식 (**`ServerSocket`, `Socket`)
- `read()`, `write()`, `accept()`와 같은 스트림 입출력에서 블로킹이 걸린다.
- 한 번에 한 연결만 처리할 수 있다.
- IO 스레드가 블로킹되면 다른일을 할 수 없고, 블로킹을 빠져나오기 위해 인터럽트도 할 수 없어진다.

### **NIO Connector(None-Blocking 방식)**

- **JDK 1.4부터 NIO라는 논블록킹 I/O API가 추가되었다!**
- **입출력 작업 시 스레드가 블로킹되지 않는다.**
- 준비가 완료된 채널만 선택해서 작업 스레드가 처리하기 때문에, 스레드가 블로킹 되지 않는다. (작업 준비가 완료되었다 → 지금 바로 읽고 쓸 수 있는 상태)
- 핵심객체는 **멀티플렉서(multiplexor)**인 **셀렉터(Selector)**
</aside>

## ***스트림과 채널의 차이***

<aside>
✍️ **NOTE**

- **스트림**
    - 입력 스트림과, 출력 스트림이 구분되어 있다.
    - 데이터를 읽기 위해서는 입력 스트림을 통해 읽어야하고, 출력을 위해서는 출력 스트림을 사용해야 한다.
- **채널**
    - 양방향 입출력 가능
    - 입력과 출력을 위한 별도의 채널이 필요하지 않다.
</aside>

## ***None Buffer 와 Buffer 의 차이***

<aside>
✍️ **NOTE**

![스트림 VS 버퍼](%5BSpring%20Netty%5D%20NIO%20Connector%20%EC%99%80%20BIO%20Connector/Untitled.png)

스트림 VS 버퍼

- **None Buffer(IO)는 대체로 느림**
    - 1바이트 정보를 입력받고 출력할 때, 입력 스트림에서 1바이트를 쓰고 출력 스트림에서 1바이트를 써야한다.
    - 따라서 버퍼를 제공해주는 보조 스트림(구현체)인 `BufferedInputStream`, `BufferedOutputStream`을 연결해서 사용
- **NIO는 버퍼를 사용하여 입출력하기 떄문에 IO보다 성능이 좋음**
    - 채널은 입력된 데이터를 버퍼에 저장하고, 저장되어 있던 데이터를 출력한다.
</aside>

## ***BIO와 NIO 방식 비교***

<aside>
✍️ **NOTE**

![톰캣의 NIO Connector](%5BSpring%20Netty%5D%20NIO%20Connector%20%EC%99%80%20BIO%20Connector/Untitled%201.png)

톰캣의 NIO Connector

![BIO 방식( 1커넥션 = 1쓰레드 )](%5BSpring%20Netty%5D%20NIO%20Connector%20%EC%99%80%20BIO%20Connector/Untitled%202.png)

BIO 방식( 1커넥션 = 1쓰레드 )

![NIO 방식 (N커넥션 = 1쓰레드)](%5BSpring%20Netty%5D%20NIO%20Connector%20%EC%99%80%20BIO%20Connector/Untitled%203.png)

NIO 방식 (N커넥션 = 1쓰레드)

1. 브라우저로 부터 요청을 받는다. (이는 다중 요청일 수도 있고, 단일 요청일 수도 있다.)
2. 서버 소켓으로 요청이 입력되면 Acceptor Thread가 요청을 받고 이를 **Acceptor Queue**(버퍼)에 적재한다.
3. 커넥터 프로그램 큐에서 Poll해와 이를 worker Thread에게 할당한다.
</aside>

## *B**IO와 NIO 선택** ⭐*

<aside>
✍️ **NOTE**

> *네트워크 프로그램을 개발할 때 IO와 NIO 선택 기준에 대해 생각해보자.*
> 
- NIO는 불특정 다수의 클라이언트 연결 또는 멀티 파일들을 None-Blocking이나 비동기로 처리할 수 있기 떄문에 과도한 스레드 생성을 피하고 스레드를 효과적으로 재사용할 수 있다.
- 운영체제의 버퍼(다이렉트 버퍼)를 이용한 입출력이 가능하기 때문에 입출력 성능이 향상된다.
- NIO는 **연결 클라이언트 수가 많고**, **하나의 입출력 처리 작업이 오래 걸리지 않는 경우에 사용하는 것이 좋다.**
- 스레드에서 입출력 처리가 오래 걸린다면 대기하는 작업의 수가 늘어나기 때문에, 제한된 스레드로 처리하는 것이 오히려 불리할 수 있다.
- 대용량 데이터를 처리하는 경우 IO를 사용하는것이 더 유리하다.
    - NIO는 버퍼의 할당 크기도 문제되고, 모든 입출력이 버퍼를 무조건 사용해야 해서 즉시 처리하는 IO보다는 좀 더 복잡하다.
    - 연결 클라이언트 수가 적고, 전송되는 데이터가 대용량이면서 순차적으로 처리될 필요성이 있을 경우에는 IO로 서버를 구현하는 것이 좋다.
</aside>