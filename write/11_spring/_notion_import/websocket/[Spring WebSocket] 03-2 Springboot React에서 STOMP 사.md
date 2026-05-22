# [Spring WebSocket] 03-2. Springboot/React에서 STOMP 사용하기

주제: Spring Netty

- 참고
    
    [동아리 홈페이지 투표 개발 2 - WebSocket과 STOMP](https://woo-chang.tistory.com/46)
    
    [[Spring-Boot] WebSocket 구현하기 (2)](https://velog.io/@prm1247/Spring-Boot-WebSocket-구현하기-2)
    
    [Spring STOMP 웹소켓을 이용해 채팅서비스 구현해보기(채팅방 구분, 채팅 저장)](https://blog.naver.com/PostView.naver?blogId=qjawnswkd&logNo=222283176175&parentCategoryNo=&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView)
    

# Springboot

---

<aside>
💡 **NOTE**

![이해를 돕기위한 예시 이미지 자료](%5BSpring%20WebSocket%5D%2003-2%20Springboot%20React%EC%97%90%EC%84%9C%20STOMP%20%EC%82%AC/Untitled.png)

이해를 돕기위한 예시 이미지 자료

```groovy
implementation 'org.springframework.boot:spring-boot-starter-websocket'
```

1. 클라이언트(Sender)가 메시지를 보내면 STOMP 통신을 통해 서버에 메시지가 전달됩니다.
2. **Controller**의 `@MessageMapping`을 통해 메시지를 받습니다.
3. **Controller**의 `@SendTo`를 사용하여 특정 주제를 구독하는 클라이언트에게 메시지를 보냅니다.
</aside>

## Springboot - **WebSocket Config**

<aside>
✍️ **NOTE**

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

	@Override
	public void configureMessageBroker(MessageBrokerRegistry config) {
		// server -> client		
		// ex /plans/greeting (서버가 보냄)
		config.enableSimpleBroker("/client");

		// client -> server
		// ex /send/hello (클라이언트가 보냄)
		config.setApplicationDestinationPrefixes("/server");
	}

	@Override
	public void registerStompEndpoints(StompEndpointRegistry registry) {
		// 클라이언트에서 socket 접속을 위한 경로
		registry.addEndpoint("/share")
			.setAllowedOriginPatterns("*")
			.withSockJS();
	}
}
```

```jsx
// 해당 경로로 Socket 연결시킨다.
const socket = new SockJS("http://localhost:8080/api/share");
const stompClient = Stomp.over(socket);

// 해당 경로를 구독한다.
stompClient.subscribe("/client/1/titleModify", (data) => {
    // ...
});

// 해당 경로로 websocket을 보낸다.
stompClient.send(
    "/server/1/title",
    // ...
);
```

### @EnableWebSocketMessageBroker

- `@Configuration` 클래스에 추가하여, WebSocket을 통한 브로커 메시징을 활성화하도록 한다.
- `WebSocketMessageBrokerConfiguration` 인터페이스를 구현하여 WebSocket 설정을 사용자가 커스텀할 수 있다.

### configureMessageBroker

- `‘/share’`으로 시작하는 주제에 대한 메시지 브로드캐스팅을 활성화시킨다.
- `setApplicationDestinationPrefixes`메시지 처리 메서드로 라우팅되는 수신 메시지의 접두사를 설정한다.

### registerStompEndpoints

- WebSocket 연결을 위한 endpoint을 구성한다
- `withSockJS()`는 WebSocket을 지원하지 않는 클라이언트에 대한 옵션을 활성화한다.
</aside>

## Springboot - **WebSocket 수신/전송**

<aside>
✍️ **NOTE**

```java
@MessageMapping("/{planId}/title")
@SendTo("/client/{planId}/titleModify")
@Operation(summary = "일정 제목 수정")
public ResponseEntity<Response<?>> titleModify(@Header(name = "Authorization") String accessToken,
                                               @DestinationVariable Long planId, @RequestBody PlanTitleDto planTitle) {
		// ...
    return ResponseEntity.ok(Response.of("", 200, "success"));
}
```

- `@MessageMapping` : client → sever로 응답 받는다.
- `@SendTo` : server → client로 요청 보낸다.

```jsx
// 받기
// stompClient.subscribe(destination, callback, headers(선택사항));
stompClient.subscribe("/client/1/titleModify", (data) => {
  setPlanData(JSON.parse(data.body));
});

// 보내기
stompClient.send(
    "/server/1/title",
    { Authorization: accessToken },
    JSON.stringify({ title: "New Title" })
);
```

- `stompClient.subscribe` : server → clinet로 응답 받는다
- `stompClient.send` : client → server로 요청 보낸다
</aside>

# React

---

<aside>
✍️ **NOTE**

![유저 1이 이벤트를 일으킴](%5BSpring%20WebSocket%5D%2003-2%20Springboot%20React%EC%97%90%EC%84%9C%20STOMP%20%EC%82%AC/CPT2303281526-826x291.gif)

유저 1이 이벤트를 일으킴

![유저 2는 유저1이 일으키는 이벤트를 실시간으로 받음](%5BSpring%20WebSocket%5D%2003-2%20Springboot%20React%EC%97%90%EC%84%9C%20STOMP%20%EC%82%AC/CPT2303281526-790x200.gif)

유저 2는 유저1이 일으키는 이벤트를 실시간으로 받음

</aside>

## React - **SockJS,** Stompjs이브러리 추가

<aside>
✍️ **NOTE**

```jsx
import Stomp from "stompjs";
import SockJS from "sockjs-client";
```

SockJS는 애플리케이션이 WebSocket API를 사용하도록 하지만 코드를 변경할 필요 없이 런타임에 WebSocket이 아닌 대안으로 대처하는 것을 의미하며 이를 **WebSocket Emulation**을 이용한다고 합니다!

- WebSocket을 지원하지 않는 브라우저라 할지라도, 다른 기술을 사용하여 지속성 있는 연결을 지원할 수 있도록 도와줍니다.
- 먼저 WebSocket 연결을 시도하지만 `HTTP Streaming`, `Long-Polling`과 같은 HTTP 기반의 다른 기술로 전환해 연결을 시도합니다.
</aside>

## React - stompClient 연결

<aside>
✍️ **NOTE**

```jsx
const socket = new SockJS(connectUrl);
const stompClient = Stomp.over(socket);

const connectWebSocket = () => {
    const socket = new SockJS(connectUrl);
    const stompClient = Stomp.over(socket);

    stompClient.connect(
        // 헤더
        {
            'Authorization': accessToken,
        },
        () => {
            // 연결 성공시 이벤트
            console.log("WebSocket connected");
            setStompClient(stompClient);
        },
        (error) => {
            // 연결 실패시 이벤트
            console.error("WebSocket error: ", error);
        }
    );
};
```

```jsx
useEffect(() => {
    connectPlan() // 
    connectWebSocket(); // 

    Cleanup function
    return () => {
        if (stompClient) {
            stompClient.disconnect();
        }
    };
}, []);
```

</aside>

## React - stompClient 구독(receiver)

<aside>
✍️ **NOTE**

```jsx
useEffect(() => {
    if (stompClient) {
        stompClient.subscribe(`/client/${planId}/title`, (data) => {
            // 일정 제목 수정
            console.log(`일정 제목 수정`);
            setText("일정 제목 수정")
				});

        stompClient.subscribe(`/client/${planId}/places/${planPlaceId}/stay-time`, (data) => {
            // 일정 장소 머무는 시간 수정
            console.log(`일정 장소 머무는 시간 수정`);
            setText(`일정 장소 머무는 시간 수정`);
        });

				// ...
    }
}, [stompClient]);
```

</aside>

## React - stompClient 보내기(send)

<aside>
✍️ **NOTE**

```jsx
const handleTitleModify = () => {
    stompClient.send(
        `/server/${planId}/title`,
        {Authorization: accessToken},
        JSON.stringify({data: "data"})
    );
};

const handlePlaceStayTimeModify = () => {
    setCount(+1);
    stompClient.send(
        `/server/${planId}/places/${planPlaceId}/title`,
        {Authorization: accessToken},
        JSON.stringify({data: "data"})
    );
};
```

</aside>