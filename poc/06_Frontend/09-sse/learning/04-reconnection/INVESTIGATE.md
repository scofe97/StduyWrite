# 04. 재연결 및 Last-Event-ID - 조사 (INVESTIGATE)

> SSE의 자동 재연결 메커니즘과 데이터 무결성 보장 방법을 탐구합니다.

---

## 핵심 질문

### 1. SSE의 자동 재연결
- 서버와 연결이 끊기면 어떻게 되는가?
- 브라우저가 자동으로 재연결을 시도하는가?
- 재연결 간격은 어떻게 결정되는가?

### 2. WebSocket과의 차이
- WebSocket은 연결이 끊기면 어떻게 되는가?
- WebSocket에서 재연결 로직을 직접 구현해야 하는 이유는?

```javascript
// WebSocket 재연결 (직접 구현 필요)
function connectWebSocket() {
  const ws = new WebSocket('ws://...');
  ws.onclose = () => {
    setTimeout(connectWebSocket, 3000);  // 직접 재연결
  };
}

// SSE 재연결 (자동!)
const es = new EventSource('/events');
es.onerror = () => {
  // 브라우저가 알아서 재연결함
  console.log('재연결 시도 중...');
};
```

### 3. retry: 필드
- 서버에서 `retry:` 필드로 무엇을 설정할 수 있는가?
- 클라이언트에서 재연결 간격을 변경할 수 있는가?

### 4. Last-Event-ID
- `id:` 필드는 왜 필요한가?
- 재연결 시 서버에 어떻게 전달되는가?
- 서버에서 이 정보를 어떻게 활용하는가?

```
// 서버가 보내는 메시지
id: 42
data: Some event

// 재연결 시 브라우저가 보내는 헤더
// Last-Event-ID: ???
```

---

## 탐색 활동

### 활동 1: 자동 재연결 관찰

1. `/events/error-simulation` 엔드포인트에 연결합니다
2. 이 엔드포인트는 5개의 이벤트 후 연결을 끊습니다
3. 브라우저가 자동으로 재연결하는지 관찰합니다
4. Network 탭에서 새로운 요청이 생기는지 확인합니다

```javascript
const es = new EventSource('/events/error-simulation');

es.onmessage = (e) => console.log('메시지:', e.data);
es.onerror = (e) => console.log('에러 - readyState:', es.readyState);
```

### 활동 2: retry 필드 확인

1. `/events/with-id` 엔드포인트에 연결합니다
2. Network 탭에서 첫 응답의 `retry:` 값을 확인합니다
3. 서버를 중지했다가 다시 시작하면 몇 초 후에 재연결되는가?

### 활동 3: Last-Event-ID 헤더 확인

1. `/events/with-id` 엔드포인트에 연결합니다
2. 몇 개의 메시지를 받은 후 서버를 중지합니다
3. 서버를 다시 시작합니다
4. Network 탭에서 재연결 요청의 `Last-Event-ID` 헤더를 확인합니다

---

## 생각해볼 점

1. 연결이 끊긴 동안 서버에서 발생한 이벤트들을 어떻게 복구할 수 있을까?

2. 이벤트 ID는 어떤 형식이어야 할까? (숫자? UUID? 타임스탬프?)

3. 너무 자주 재연결을 시도하면 어떤 문제가 생길까?

4. 모바일 환경에서 네트워크가 불안정할 때 SSE는 어떻게 동작할까?

---

## 참고 키워드
- SSE automatic reconnection
- retry field
- Last-Event-ID header
- Event stream recovery
- Exponential backoff

---

학습 준비가 되었다면 [LEARN.md](./LEARN.md)로 진행하세요.
