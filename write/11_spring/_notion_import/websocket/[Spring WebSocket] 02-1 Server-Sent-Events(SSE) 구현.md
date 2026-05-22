# [Spring WebSocket] 02-1. Server-Sent-Events(SSE) 구현하기

주제: Spring Netty

- 참고
    
    [[Spring + SSE] Server-Sent Events를 이용한 실시간 알림](https://velog.io/@max9106/Spring-SSE-Server-Sent-Events를-이용한-실시간-알림)
    
    [[NODE] 📚 Server Sent Events 💯 정리 (+사용법)](https://inpa.tistory.com/entry/NODE-📚-Server-Sent-Events-💯-정리-사용법)
    
    [Spring에서 Server-Sent-Events 구현하기](https://tecoble.techcourse.co.kr/post/2022-10-11-server-sent-events/)
    
    [2021-drop-the-code/EmitterRepository.java at main · woowacourse-teams/2021-drop-the-code](https://github.com/woowacourse-teams/2021-drop-the-code/blob/main/backend/src/main/java/com/wootech/dropthecode/repository/EmitterRepository.java)
    
    [알림 기능을 구현해보자 - SSE(Server-Sent-Events)!](https://gilssang97.tistory.com/69#레포지토리-구현)
    
    [Server Sent Events with Spring Boot and ReactJS](https://turkogluc.com/server-sent-events-with-spring-boot-and-reactjs/)
    
    [Server-Sent Events 사용하기 - Web API | MDN](https://developer.mozilla.org/ko/docs/Web/API/Server-sent_events/Using_server-sent_events)
    

# **Server-Sent Events(SSE)**

---

<aside>
💡 **NOTE**

> ***SSE**는 **데이터를 실시간으로 Streaming 하는 기술**이다!*
> 

![예시이미지 → checkbox클릭시 모든 client에 반영된다! (우리는 알람기능에 사용한다.)](%5BSpring%20WebSocket%5D%2002-1%20Server-Sent-Events(SSE)%20%EA%B5%AC%ED%98%84/checklist.gif)

예시이미지 → checkbox클릭시 모든 client에 반영된다! (우리는 알람기능에 사용한다.)

![Untitled](%5BSpring%20WebSocket%5D%2002-1%20Server-Sent-Events(SSE)%20%EA%B5%AC%ED%98%84/Untitled.png)

- 기존에는 **Server**의 변경된 데이터를 가져오기 위해서 새로고침, 혹은 지속적으로 **request**를 보내는 **ajax 폴링,** **외부 플러그인**을 사용해야 했다.
- 이외에도 **websocket**을 사용할 수 있지만 **HTTP 통신**을 이용하는 것이 아닌 **websocket**만을 위한 별도의 서버와 프로토콜로 통신하기 때문에 비용이 많이든다.
- **SSE**는 기존 **HTTP 웹 서버에서, HTTP API만으로 동작**되므로 **개발난이도가 매우 쉽다!**
</aside>

## ***Server-Sent Events 특징***

<aside>
✍️ **NOTE**

- 브라우저는 서버가 생성한 Stream을 계속해서 받는다(Server에서 보내는 Stream으로 Read Only)
- Connection 유지를 위해 **HTTP Protocol을 사용**, HTTP/2를 통한 multiplexing 사용가능
- 연결이 끊어지면 **EventSource**가 오류 이벤트를 발생시키고 자동으로 다시 연결을 시도
- 대부분의 브라우저에서 지원
</aside>

## ***Server-Sent Events 사용시점***

<aside>
✍️ **NOTE**

- 효율적인 단방향 통신이 필요한 경우
- 실시간 데이터 스트리밍에 **HTTP**를 사용하려는 경우**(RestFul의 Get Method와 유사)**
- 사용되는 예
    - 암호 화폐 또는 주가 피드 구독
    - 라이브 스포츠 점수 받기
    - **뉴스 업데이트 또는 알림**
</aside>

## ***Server-Sent Events VS WebSocket***

<aside>
✍️ **NOTE**

| **Socket** | **Server-Sent-Event** |
| --- | --- |
| 브라우저 지원 | 대부분 브라우저에서 지원 |
| 통신 방향 | 양방향 |
| 리얼타임 | Yes |
| 데이터 형태 | Binary, UTF-8 |
| 자동 재접속 | No |
| 최대 동시 접속 수 | 브라우저 연결 한도는 없지만 서버 셋업에 따라 다름 |
| 프로토콜 | websocket |
| 베터리 소모량 | 큼 |
| Firewall 친화적 | Nope |
- 사실 **Socket**하나만 알고 있어도 **SSE방식을 모두 구현할 수 있다**.
    - **Socket**은 양방향이기 때문에 SSE 역할도 해낼 수 있기 떄문
- 그러나 위에서 보는 것처럼 **Websocket**과 **SSE**의 **스펙차이 때문에 사용처에 따라 선택적으로 사용된다.**

### 웹소켓 사용처 (리얼타임)

- 카카오톡
- 주식 트레이딩 데이터

### SSE(알람)

- SNS 친구 요청이나 알람
</aside>

# Spring 개발

---

<aside>
💡 **NOTE**

> ***기본적인 흐름은 다음과 같다!***
> 

![SSE 연결요청](%5BSpring%20WebSocket%5D%2002-1%20Server-Sent-Events(SSE)%20%EA%B5%AC%ED%98%84/Untitled%201.png)

SSE 연결요청

![SSE 데이터 전달](%5BSpring%20WebSocket%5D%2002-1%20Server-Sent-Events(SSE)%20%EA%B5%AC%ED%98%84/Untitled%202.png)

SSE 데이터 전달

1. 클라이언트에서 SSE 연결 요청을 보낸다.
2. 서버에서는 클라이언트와 매핑되는 SSE 통신 객체를 만든다.
3. 서버에서 이벤트가 발생하면 해당 객체를 통해 클라이언트로 데이터를 전달한다.
</aside>

## **Controller 구현**

<aside>
✍️ **NOTE**

```java
@RestController
@RequestMapping("/alarms")
@RequiredArgsConstructor
@Slf4j
@Tag(name = "Alarms", description = "알람 관련 API, SSE 방식사용")
public class AlarmController {

	private final SseService sseService;

	@GetMapping(value = "/connect", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
	@Operation(summary = "사용자가 SSE에 연결됨")
	public SseEmitter subscribe(
		@RequestHeader(name = "Authorization") String accessToken) {

		log.info("컨트롤러에 접속됨");
		return alarmService.subscribe(accessToken);
	}

	//...
}
```

- 연결 요청을 처리하기 위해서, **MIME Type**을 `text/event-stream`형태로 받아줘야 한다.
- 반환값을 다른 객체로 감싸지말고,  `SseEmitter`로 해야 front에서 제대로 받을 수 있다.
</aside>

## Repository 구현

<aside>
✍️ **NOTE**

> *기존의 **JpaRepository**를 사용하기에는, **어떤 회원이 어떤 Emitter가 연결되었는지**, **어떤 이벤트들이 현재까지 발생했는지**를 저장하기에 까다로우므로 Repository를 따로 구현*
> 

```java
@Repository
public class EmitterRepository {

	private final Map<String, SseEmitter> emitters = new ConcurrentHashMap<>();
	private final Map<String, Object> eventCache = new ConcurrentHashMap<>();

	// emitterId 형식 => [유저의 accessToken] + _ + 생성시간

	/**
	 * Emitter를 저장한다
	 * @param emitterId
	 * @param sseEmitter
	 * @return
	 */
	public SseEmitter save(String emitterId, SseEmitter sseEmitter) {
		emitters.put(emitterId, sseEmitter);
		return sseEmitter;
	}

	/**
	 * 이벤트를 저장한다.
	 * @param eventCacheId
	 * @param event
	 */
	public void saveEventCache(String eventCacheId, Object event) {
		eventCache.put(eventCacheId, event);
	}

	/**
	 * 해당 회원과 관련된 모든 Emitter를 찾는다.
	 * @param memberId
	 * @return
	 */
	public Map<String, SseEmitter> findAllEmitterStartWithByMemberId(String memberId) {
		return emitters.entrySet().stream()
				.filter(entry -> entry.getKey().startsWith(memberId))
				.collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
	}

	/**
	 * 해당 회원과 관련된 모든 이벤트를 찾는다.
	 * @param memberId
	 * @return
	 */
	public Map<String, Object> findAllEventCacheStartWithByMemberId(String memberId) {
		return eventCache.entrySet().stream()
				.filter(entry -> entry.getKey().startsWith(memberId))
				.collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
	}

	/**
	 * Emitter를 지운다.
	 * @param id
	 */
	public void deleteById(String id) {
		emitters.remove(id);
	}

	/**
	 * 해당 회원과 관련된 모든 Emitter를 지운다.
	 * @param memberId
	 */
	public void deleteAllEmitterStartWithId(String memberId) {
		emitters.forEach(
				(key, emitter) -> {
					if (key.startsWith(memberId)) {
						emitters.remove(key);
					}
				}
		);
	}

	/**
	 * 해당 회원과 관련된 모든 이벤트를 지운다.
	 * @param memberId
	 */
	public void deleteAllEventCacheStartWithId(String memberId) {
		eventCache.forEach(
				(key, emitter) -> {
					if (key.startsWith(memberId)) {
						eventCache.remove(key);
					}
				}
		);
	}
}
```

- `Emitter`를 생성, 검색, 삭제
- `Emitter`의 이벤트를 생성, 검색, 삭제
</aside>

## Service 구현

<aside>
✍️ **NOTE**

> *어떻게 `SseEmitte`에 구독을 진행하는지와, 구독자들에게 어떻게 이벤트를 전달시키는지 알아보자!*
> 
- **전체 코드**
    
    ```java
    @Service
    @RequiredArgsConstructor
    @Slf4j
    public class AlarmService {
    
    	// 만료시간
    	private static final Long DEFAULT_TIMEOUT = Long.MAX_VALUE;
    	private static final String MESSAGE = "message";
    
    	private final SseRepository sseRepository;
    	private final AlarmRepository alarmRepository;
    	private final UserService userService;
    	private final PlanAuthService planAuthService;
    	private final PlanReadService planReadService;
    
    	/**
    	 * 사용자가 받을 emitter를 등록
    	 * @param accessToken
    	 * @return
    	 */
    	public SseEmitter subscribe(String accessToken) {
    
    		User user = userService.findUserEntity(accessToken, true);
    		String userId = String.valueOf(user.getId());
    
    		// 1 accessToken + _ + 현재 시간정보로 id 생성
    		String emitterId = makeTimeIncludeId(userId);
    
    		// 2 생성한 emitter repository에 저장
    		SseEmitter emitter = sseRepository.save(emitterId, new SseEmitter(DEFAULT_TIMEOUT));
    
    		// 3. emitter 만료되면 자동제거
    		emitter.onCompletion(() -> sseRepository.deleteById(emitterId));
    		emitter.onTimeout(() -> sseRepository.deleteById(emitterId));
    		emitter.onError((e) -> sseRepository.deleteById(emitterId));
    
    		// 503 에러를 방지하기 위한 더미 이벤트 전송
    		String eventId = makeTimeIncludeId(userId);
    		sendToClient(emitter, eventId, MESSAGE, emitterId, "EventStream Created. [userId=" + userId + "]");
    
    		return emitter;
    	}
    
    	/**
    	 * 여행계획에 다른 사용자를 초대한다.
    	 * @param accessToken
    	 * @param inviteDto
    	 */
    	public void sendInvitation(String accessToken, InviteDto inviteDto) {
    		planAuthService.addInviteUser(accessToken, inviteDto.getPlanId(), inviteDto.getNickname());
    
    		User sender = userService.findUserEntity(accessToken, true);
    		User receiver = userService.findUserEntityNickname(inviteDto.getNickname());
    		Plan plan = planReadService.getPlan(inviteDto.getPlanId());
    
    		Alarm alarm = Alarm.builder()
    			.receiver(receiver)
    			.sender(sender)
    			.type(AlarmType.INVITE)
    			.content(AlarmConstants.inviteMsg(plan.getTitle(), sender.getNickName()))
    			.url(AlarmConstants.getUrl(plan.getId().toString()))
    			.plan(plan)
    			.build();
    		alarmRepository.save(alarm);
    
    		send(receiver, AlarmDto.of(alarm));
    	}
    
    	/**
    	 * 초대에 대한 응답
    	 * @param accessToken
    	 * @param acceptDto
    	 */
    	public void receiveInvitation(String accessToken, AcceptDto acceptDto) {
    		PlanInviteDto planInviteDto = PlanInviteDto.builder()
    			.planId(acceptDto.getPlanId())
    			.accept(acceptDto.getAccept())
    			.build();
    
    		planAuthService.getInvite(accessToken, planInviteDto);
    
    		User sender = userService.findUserEntity(accessToken, true);
    		User receiver = userService.findUserEntityNickname(acceptDto.getSenderNickname());
    		Plan plan = planReadService.getPlan(acceptDto.getPlanId());
    		AlarmType alarmType;
    
    		if (acceptDto.getAccept()) {
    			alarmType = AlarmType.RECEIVE_OK;
    		} else {
    			alarmType = AlarmType.RECEIVE_DENY;
    		}
    
    		Alarm alarm = Alarm.builder()
    			.receiver(receiver)
    			.sender(sender)
    			.type(alarmType)
    			.content(AlarmConstants.acceptMsg(plan.getTitle(), sender.getNickName(), acceptDto.getAccept()))
    			.url(AlarmConstants.getUrl(plan.getId().toString()))
    			.plan(plan)
    			.build();
    
    		alarmRepository.save(alarm);
    		send(receiver, AlarmDto.of(alarm));
    	}
    
    	public Slice<AlarmDto> findAlarmList(String accessToken, Pageable pageable) {
    		User user = userService.findUserEntity(accessToken, true);
    		return alarmRepository.findByReceiver(user, pageable).map(AlarmDto::of);
    	}
    
    	public void removeAlarm(String accessToken, Long alarmId) {
    		User user = userService.findUserEntity(accessToken, true);
    		Alarm alarm = alarmRepository.findById(alarmId).orElseThrow(() -> new EntityNotFoundException("알람"));
    
    		if (alarm.getReceiver().getId().equals(user.getId())) {
    			alarmRepository.deleteById(alarmId);
    		}
    	}
    
    	/**
    	 * 유저에게 이벤트를 발생시킴!
    	 */
    	private void send(User user, Object data) {
    		String userId = String.valueOf(user.getId());
    		String eventId = userId + "_" + System.currentTimeMillis();
    
    		// 유저가 가지고 있는 모든 SseEmitter를 가져온다.
    		Map<String, SseEmitter> emitters = sseRepository.findAllEmitterStartWithByUserId(userId);
    
    		// 유저가 가지고 있는 모든 SseEmitter 이벤트 등록
    		emitters.forEach(
    			(key, emitter) -> {
    				// 데이터 캐시 저장(유실된 데이터 처리하기 위함)
    				sseRepository.saveEventCache(key, data);
    				// 데이터 전송
    				sendToClient(emitter, eventId, MESSAGE, key, data);
    			}
    		);
    	}
    
    	/**
    	 * emitter를 식별할 ID 생성 ([유저 PK] + _ + [생성시간])
    	 * @param userId
    	 * @return
    	 */
    	private String makeTimeIncludeId(String userId) {
    		return userId + "_" + System.currentTimeMillis();
    	}
    
    	/**
    	 * emiiter에 이벤트 넣어줌
    	 * @param emitter emitter
    	 * @param eventId event 아이디
    	 * @param emitterId  emitter 아이디
    	 * @param data front 보내줄 데이터
    	 */
    	private void sendToClient(SseEmitter emitter, String eventId, String eventName, String emitterId, Object data) {
    		try {
    			emitter.send(SseEmitter.event()
    				.id(eventId) // 이벤트 ID
    				.name(eventName) // 이벤트 이름(이벤트 유형)
    				.data(data)); // 이벤트에 전송되는 데이터
    		} catch (IOException exception) {
    			sseRepository.deleteById(emitterId);
    		}
    	}
    }
    ```
    

```java
String emitterId = makeTimeIncludeId(memberId);

private String makeTimeIncludeId(Long memberId) {
        return memberId + "_" + System.currentTimeMillis();
}

SseEmitter emitter = sseRepository.save(emitterId, new SseEmitter(DEFAULT_TIMEOUT));
```

```java
emitter.onCompletion(() -> sseRepository.deleteById(emitterId));
emitter.onTimeout(() -> sseRepository.deleteById(emitterId));
emitter.onError((e) -> sseRepository.deleteById(emitterId));
```

```bash
String eventId = makeTimeIncludeId(userId);
sendToClient(emitter, eventId, MESSAGE, emitterId, "EventStream Created. [userId=" + userId + "]");
```

```java
private void sendToClient(SseEmitter emitter, String eventId, String eventName, String emitterId, Object data) {
	try {
		emitter.send(SseEmitter.event()
			.id(eventId) // 이벤트 ID
			.name(eventName) // 이벤트 이름(이벤트 유형) message로 넣음
			.data(data)); // 이벤트에 전송되는 데이터
	} catch (IOException exception) {
		sseRepository.deleteById(emitterId);
	}
}
```

</aside>

# React

---

<aside>
💡 **NOTE**

```jsx
let eventSource = useRef < EventSource | null > null;

eventSource = new EventSourcePolyfill(`${BASE_URL}/connect`, {
    headers: {
        'Authorization': accessToken,
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Access-Control-Allow-Origin': '*',
    },
    heartbeatTimeout: 86400000,
});
```

```jsx
eventSource.addEventListener('open', (e) => {
    console.log("연결됨");
});
```

```jsx
eventSource.addEventListener('message', (e) => {
    console.log(e.data)
    console.log("알람옴!")
});
```

</aside>