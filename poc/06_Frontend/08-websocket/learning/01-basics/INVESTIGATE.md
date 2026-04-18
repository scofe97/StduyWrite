# INVESTIGATE: WebSocket 기초

## 학습 목표
WebSocket의 기본 개념과 HTTP와의 차이점을 이해합니다.

---

## 소크라테스 질문

### Q1. HTTP vs WebSocket 비교

> HTTP 요청-응답 모델과 WebSocket은 어떤 상황에서 각각 적합한가?

**생각해볼 점:**
- 채팅 애플리케이션에서 새 메시지를 받으려면?
- 주식 시세를 실시간으로 보여주려면?
- 사용자 프로필 정보를 가져오려면?

---

### Q2. 핸드셰이크 과정

> WebSocket 연결 시 "프로토콜 업그레이드"란 무엇인가?

**생각해볼 점:**
- WebSocket은 처음에 어떤 프로토콜로 시작하는가?
- `Upgrade: websocket` 헤더의 역할은?
- 왜 처음부터 WebSocket 프로토콜을 사용하지 않는가?

---

### Q3. 양방향 통신

> "양방향 통신(Full-Duplex)"이 왜 중요한가?

**생각해볼 점:**
- HTTP에서 서버가 먼저 클라이언트에게 데이터를 보낼 수 있는가?
- Long Polling으로 실시간 통신을 구현하면 어떤 문제가 생기는가?
- WebSocket에서 서버와 클라이언트가 동시에 데이터를 보내면?

---

### Q4. 네이티브 API

> 브라우저 WebSocket API의 핵심 메서드와 이벤트는 무엇인가?

**생각해볼 점:**
- `new WebSocket(url)`로 생성하면 바로 연결되는가?
- `onopen`, `onmessage`, `onclose`, `onerror`의 호출 순서는?
- `send()` 메서드는 언제 호출해도 되는가?

---

## 다음 단계
질문에 대한 답을 찾았다면 `LEARN.md`에 정리하고, `practice/` 폴더에서 실습합니다.
