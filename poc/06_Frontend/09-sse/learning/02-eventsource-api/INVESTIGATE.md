# 02. EventSource API - 조사 (INVESTIGATE)

> EventSource API를 깊이 이해하기 위한 질문들입니다.

---

## 핵심 질문

### 1. EventSource 객체 생성과 연결
- `new EventSource(url)` 호출 시 즉시 연결이 시작되는가?
- 연결이 설정되기 전에 메시지를 받을 수 있는가?

### 2. readyState 속성
- EventSource의 readyState는 어떤 값들을 가지는가?
- WebSocket의 readyState와 비교하면 어떤 차이가 있는가?

```javascript
// EventSource
EventSource.CONNECTING  // = ?
EventSource.OPEN        // = ?
EventSource.CLOSED      // = ?

// WebSocket
WebSocket.CONNECTING    // = 0
WebSocket.OPEN          // = 1
WebSocket.CLOSING       // = 2  <-- 이건?
WebSocket.CLOSED        // = 3
```

### 3. 이벤트 핸들러
- `onopen`, `onmessage`, `onerror` 각각 언제 호출되는가?
- 이 세 가지 외에 다른 이벤트가 있는가?

### 4. EventSource vs Fetch
- `fetch`로도 스트리밍을 받을 수 있는데, EventSource를 사용하는 이유는?
- 어떤 상황에서 fetch가 더 적합한가?

### 5. withCredentials 옵션
- `new EventSource(url, { withCredentials: true })`는 언제 사용하는가?
- 쿠키 기반 인증과 어떤 관련이 있는가?

---

## 탐색 활동

### 활동 1: readyState 변화 관찰

```javascript
const es = new EventSource('/events');
console.log('생성 직후:', es.readyState);

es.onopen = () => {
  console.log('onopen:', es.readyState);
};

es.onerror = () => {
  console.log('onerror:', es.readyState);
};
```

위 코드를 실행하고 readyState 변화를 관찰하세요.

### 활동 2: 이벤트 객체 분석
`onmessage` 핸들러에서 받는 `event` 객체의 속성들을 확인하세요:

```javascript
es.onmessage = (event) => {
  console.log('data:', event.data);
  console.log('origin:', event.origin);
  console.log('lastEventId:', event.lastEventId);
  // 다른 속성들은?
};
```

### 활동 3: WebSocket과 API 비교

| 항목 | EventSource | WebSocket |
|------|-------------|-----------|
| 생성 | `new EventSource(url)` | `new WebSocket(url)` |
| 상태 | `readyState` | `readyState` |
| 수신 | `onmessage` | `onmessage` |
| 전송 | ? | `send()` |
| 종료 | `close()` | `close()` |
| 바이너리 | ? | `binaryType` |

빈칸을 채워보세요.

---

## 생각해볼 점

1. EventSource에 `send()` 메서드가 없는 이유는 무엇일까?

2. CORS 문제가 발생하면 어떻게 해결해야 할까?

3. 인증이 필요한 SSE 엔드포인트에 어떻게 토큰을 전달할 수 있을까?

---

## 참고 키워드
- EventSource constructor
- EventSource.readyState
- MessageEvent interface
- CORS and SSE
- withCredentials

---

학습 준비가 되었다면 [LEARN.md](./LEARN.md)로 진행하세요.
