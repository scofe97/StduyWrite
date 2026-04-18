# 01. SSE 기초 - 조사 (INVESTIGATE)

> 학습 전 스스로 답해보세요. 정답을 찾지 못해도 괜찮습니다.
> 중요한 것은 **질문을 던지는 것**입니다.

---

## 핵심 질문

### 1. SSE란 무엇인가?
- Server-Sent Events의 약자라면, 정확히 어떤 이벤트를 어떻게 전송하는 것인가?
- HTML5 표준에 포함되어 있다면, 별도의 라이브러리 없이 사용 가능한가?

### 2. HTTP로 어떻게 실시간 데이터를 받을 수 있는가?
- 일반적인 HTTP 요청은 요청-응답 후 연결이 끊어지는데, 어떻게 지속적으로 데이터를 받는가?
- Long Polling과 SSE의 차이점은 무엇인가?

### 3. SSE는 왜 단방향인가?
- 서버→클라이언트로만 전송 가능한 이유는?
- 클라이언트가 서버로 데이터를 보내야 한다면 어떻게 해야 하는가?

### 4. text/event-stream 형식의 구조는?
- 데이터는 어떤 형식으로 전송되는가?
- JSON을 보내려면 어떻게 해야 하는가?

### 5. 브라우저 지원 현황은?
- 모든 브라우저에서 SSE를 지원하는가?
- 지원하지 않는 환경에서는 어떻게 대응하는가?

---

## 탐색 활동

### 활동 1: SSE와 관련 기술 비교
다음 기술들이 어떻게 실시간 통신을 구현하는지 비교해보세요:
- **Polling**: ?
- **Long Polling**: ?
- **SSE**: ?
- **WebSocket**: ?

### 활동 2: 브라우저 개발자 도구 관찰
1. Mock 서버를 실행합니다: `yarn mock-server`
2. 브라우저에서 `http://localhost:3001/events`에 접속합니다
3. 개발자 도구 > Network 탭을 열고 관찰합니다
   - Content-Type은 무엇인가?
   - 응답이 완료되지 않고 계속 수신되는 것을 확인
   - 데이터 형식을 관찰

### 활동 3: SSE 메시지 구조 분석
서버에서 전송하는 SSE 메시지의 구조를 직접 확인해보세요:
```
data: {"time":"2024-01-01T00:00:00.000Z","message":"Update from server"}

event: notification
data: {"id":1,"message":"New notification"}

id: 123
data: Some data with ID

retry: 5000
data: Reconnect after 5 seconds if disconnected
```

각 필드(`data:`, `event:`, `id:`, `retry:`)의 역할은 무엇인가?

---

## 생각해볼 점

1. 채팅 애플리케이션에 SSE를 사용할 수 있을까? 왜 / 왜 안 될까?

2. 뉴스 피드나 알림 기능에 SSE가 적합한 이유는 무엇일까?

3. 바이너리 데이터(이미지, 파일)를 SSE로 전송할 수 있을까?

---

## 참고 키워드
- Server-Sent Events
- EventSource API
- text/event-stream
- HTTP Keep-Alive
- Chunked Transfer Encoding

---

학습 준비가 되었다면 [LEARN.md](./LEARN.md)로 진행하세요.
