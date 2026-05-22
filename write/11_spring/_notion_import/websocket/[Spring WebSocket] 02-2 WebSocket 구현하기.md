# [Spring WebSocket] 02-2. WebSocket 구현하기

주제: Spring Netty

- 참고
    
    [Spring Websocket & STOMP](https://brunch.co.kr/@springboot/695)
    
    [[Java] ObjectMapper를 이용하여 JSON 파싱하기](https://velog.io/@zooneon/Java-ObjectMapper%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-JSON-%ED%8C%8C%EC%8B%B1%ED%95%98%EA%B8%B0)
    

# WebSocket 테스트 도구

---

<aside>
💡 **NOTE**

> *현재 페이지에서는 **Simple WebSocket Clinet를 사용했다.***
> 

### PostMan

![Untitled](%5BSpring%20WebSocket%5D%2002-2%20WebSocket%20%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0/Untitled.png)

### Simple WebSocket Client

[Simple WebSocket Client](https://chrome.google.com/webstore/detail/simple-websocket-client/pfdhoblngboilpfeibdedpjgfnlcodoo?hl=ko)

</aside>

# Spring WebSocket

---

<aside>
💡 **NOTE**

> *Spring boot에서 웹소켓을 연동해보자!*
> 

![대충 결과화면임](%5BSpring%20WebSocket%5D%2002-2%20WebSocket%20%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0/ezgif-1-81178ab83f.gif)

대충 결과화면임

### 의존성

```groovy
implementation 'org.springframework.boot:spring-boot-starter-websocket'
```

### 웹소켓 메시지 스펙

```java
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Message {
    private String type;
    private String sender;
    private String receiver;
    private Object data;

    public void setSender(String sender) {
        this.sender = sender;
    }

    public void newConnect(){
        this.type = "new";
    }

    public void closeConnect(){
        this.type = "close";
    }
}
```

### JSON 변환(**ObjectMapper)**

```java
public class Utils {
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private Utils() {
    }

    public static Message getObject(final String message) throws Exception {
        return objectMapper.readValue(message, Message.class);
    }

    public static String getString(final Message message) throws Exception {
        return objectMapper.writeValueAsString(message);
    }
}
```

</aside>

## WebSocketConfiguration

<aside>
✍️ **NOTE**

> *Spring boot에서 웹소켓을 연동해보자!*
> 

```java
@Configuration
@RequiredArgsConstructor
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry
                .addHandler(signalingSocketHandler(), "/room")
                .setAllowedOrigins("*");
    }

    @Bean
    public WebSocketHandler signalingSocketHandler(){
        return new WebSocketHandler();
    }
}
```

1. **웹소켓 서버**를 사용하도록 정의한다 → `@EnableWebScoket`
2. **웹소켓 서버**의 **엔드포인트**로 정한다 → `url:port/room`
3. 클라이언트에서 **웹소켓 서버**에 요청시 모든 요청 수락(CORS) → `setAllowdOrigins(”*”)`
4. `WebScoketHandler` 클래스를 **웹소켓 핸들러로 정의**한다.
</aside>

# WebSocketHandler

---

<aside>
💡 **NOTE**

> *웹소켓 핸들러는 **소켓의 통신에 관련된 함수들을 작성할 수 있다!***
> 

```java
@Component
@Log4j2
public class WebSocketHandler extends TextWebSocketHandler {

    private final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();

    // 웹 소켓 연결
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {}

		// 양방향 데이터 통신
    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage textMessage) throws Exception {}

		// 소켓 연결 종료
    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {}

		// 소켓 통신 에러
    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {}
}
```

</aside>

## WebSocket 최초연결 - `afterConnectionEstablished`

<aside>
✍️ **NOTE**

> ***웹소켓에 접속하면 발생하는 함수다!***
> 

```java
private final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();
```

![Untitled](%5BSpring%20WebSocket%5D%2002-2%20WebSocket%20%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0/Untitled%201.png)

```java
// 웹 소켓 연결
@Override
public void afterConnectionEstablished(WebSocketSession session) throws Exception {
		// 1. session 저장
		String sessionId = session.getId();
    sessions.put(sessionId, session);

		// 2. message 설정
    Message message = Message.builder().sender(sessionId).receiver("all").build();
    message.newConnect();

		// 3. 접속해 있는 모든 사용자에 알림(본인제외)
    sessions.values().forEach(s -> {
        try{
            if(!s.getId().equals(sessionId)){
                s.sendMessage(new TextMessage(Utils.getString(message)));
            }
        }catch (Exception e){

        }
    });
}
```

</aside>

## WebSocket 데이터 통신 - `handleTextMessage`

<aside>
✍️ **NOTE**

> ***웹소켓에서 데이터 통신 시 구현한다.***
> 

```java
@Override
protected void handleTextMessage(WebSocketSession session, TextMessage textMessage) throws Exception {
	  String sessionId = session.getId();
	  Message message = Utils.getObject(textMessage.getPayload());
	  message.setSender(session.getId());

		// 2. 접속해 있는 모든 사용자에 채팅보냄
	  sessions.values().forEach(s -> {
	      try{
	          if(!s.getId().equals(sessionId)){
	              s.sendMessage(new TextMessage(Utils.getString(message)));
	          }
	      }catch (Exception e){
	
	      }
	  });
	
	  if(receiver != null && receiver.isOpen()){
	      receiver.sendMessage(new TextMessage(Utils.getString(message)));
	  }
}
```

1. 
</aside>

## WebSocket 연결 종료 - `afterConnectionClosed`

<aside>
✍️ **NOTE**

> ***웹소켓에 접속해제 하면 발생한다.***
> 

![Untitled](%5BSpring%20WebSocket%5D%2002-2%20WebSocket%20%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0/Untitled%202.png)

```java
@Override
public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
    // 1. session 제거
		String sessionId = session.getId();
    sessions.remove(sessionId);

		// 2. message 설정
    final Message message = new Message();
    message.closeConnect();
    message.setSender(sessionId);

		// 3. 접속해 있는 모든 사용자에 알림(본인제외)
    sessions.values().forEach(s -> {
        try{
            if(!s.getId().equals(sessionId)){
                s.sendMessage(new TextMessage(Utils.getString(message)));
            }
        }catch (Exception e){

        }
    });
}
```

1. 
</aside>

## WebSocket 예외 발생 - `handleTransportError`

<aside>
✍️ **NOTE**

> ***웹소켓에서 에러 발생시 동작한다.***
> 

```java
@Override
public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {
    super.handleTransportError(session, exception);
}
```

</aside>