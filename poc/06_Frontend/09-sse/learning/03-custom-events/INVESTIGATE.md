# 03. 커스텀 이벤트 - 조사 (INVESTIGATE)

> 서버에서 다양한 타입의 이벤트를 보내는 방법을 탐구합니다.

---

## 핵심 질문

### 1. 왜 커스텀 이벤트가 필요한가?
- 모든 메시지를 `onmessage`로 받으면 안 되는 이유는?
- 어떤 상황에서 이벤트를 타입별로 분리해야 할까?

### 2. 서버에서 이벤트 타입 지정
- `event:` 필드는 어떻게 사용하는가?
- `event:` 필드가 없으면 어떤 이벤트 타입이 되는가?

```
// 이 메시지의 이벤트 타입은?
data: Hello World

// 이 메시지의 이벤트 타입은?
event: notification
data: New message received
```

### 3. 클라이언트에서 수신 방법
- `onmessage`로 커스텀 이벤트를 받을 수 있는가?
- `addEventListener`와 `onmessage`의 차이는?

```javascript
// 이 두 코드의 차이점은?
eventSource.onmessage = (e) => console.log(e.data);
eventSource.addEventListener('message', (e) => console.log(e.data));

// notification 이벤트를 받으려면?
eventSource.addEventListener('notification', (e) => console.log(e.data));
// onnotification = ... 이 가능할까?
```

### 4. 이벤트 타입 네이밍 규칙
- 이벤트 타입에 공백이 들어갈 수 있는가?
- 대소문자 구분이 되는가?

---

## 탐색 활동

### 활동 1: 커스텀 이벤트 수신 테스트

Mock 서버의 `/events/custom` 엔드포인트는 3종류의 이벤트를 보냅니다:
- `notification`
- `update`
- `alert`

```javascript
const es = new EventSource('/events/custom');

// 각각 어떤 이벤트를 받는지 확인
es.onmessage = (e) => console.log('onmessage:', e.data);
es.addEventListener('notification', (e) => console.log('notification:', e.data));
es.addEventListener('update', (e) => console.log('update:', e.data));
es.addEventListener('alert', (e) => console.log('alert:', e.data));
```

`onmessage`가 호출되는가, 안 되는가?

### 활동 2: 메시지 형식 분석

서버가 보내는 SSE 메시지의 원본 형식을 Network 탭에서 확인하세요:

```
event: notification
data: {"id":1,"message":"notification event"}

event: update
data: {"id":2,"message":"update event"}
```

각 필드의 순서가 중요한가?

### 활동 3: 여러 핸들러 등록

```javascript
const es = new EventSource('/events');

// 같은 이벤트에 여러 핸들러 등록
es.addEventListener('message', (e) => console.log('handler1:', e.data));
es.addEventListener('message', (e) => console.log('handler2:', e.data));

// onmessage도 추가하면?
es.onmessage = (e) => console.log('onmessage:', e.data);
```

모든 핸들러가 호출되는가?

---

## 생각해볼 점

1. 실시간 대시보드를 만든다고 가정하면, 어떤 이벤트 타입들이 필요할까?
   - 예: `metrics`, `alert`, `statusChange`, ...

2. 채팅 애플리케이션에서 SSE를 사용한다면?
   - 메시지 수신, 사용자 입장/퇴장, 타이핑 표시...
   - 각각 별도 이벤트 타입으로 해야 할까?

3. 너무 많은 이벤트 타입을 만들면 어떤 문제가 생길까?

---

## 참고 키워드
- SSE event field
- addEventListener vs onmessage
- Named events in SSE
- Event routing pattern

---

학습 준비가 되었다면 [LEARN.md](./LEARN.md)로 진행하세요.
