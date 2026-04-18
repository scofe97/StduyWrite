# 07. WebSocket vs SSE - 조사 (INVESTIGATE)

> 두 기술의 차이점을 깊이 이해하고, 올바른 선택 기준을 탐구합니다.

---

## 핵심 질문

### 1. 기술적 차이
- WebSocket과 SSE의 가장 근본적인 차이는 무엇인가?
- 왜 WebSocket은 별도의 프로토콜(ws://)을 사용하고, SSE는 HTTP를 사용하는가?

### 2. 성능 비교
- 대용량 데이터 전송에서 어떤 기술이 유리한가?
- 연결 수가 많아지면 어떤 차이가 생기는가?
- 브라우저 연결 제한은 어떻게 다른가?

### 3. 인프라 고려사항
- 기업 방화벽에서 각 기술이 어떻게 처리되는가?
- 로드 밸런서와의 호환성은?
- CDN을 통한 배포가 가능한가?

### 4. 실무 사례
- ChatGPT가 SSE를 사용하는 이유는?
- 채팅 앱이 WebSocket을 사용하는 이유는?
- 주식 시세 표시에는 어떤 기술이 적합한가?

---

## 탐색 활동

### 활동 1: 방화벽 문제 조사

Reddit, Stack Overflow 등에서 "WebSocket firewall blocked" 검색:
- 어떤 환경에서 문제가 발생하는가?
- 해결책은 무엇인가?

### 활동 2: 연결 제한 테스트

브라우저에서 여러 SSE 연결을 열어보세요:

```javascript
// 동일 도메인에 여러 연결
for (let i = 0; i < 10; i++) {
  new EventSource(`/events?id=${i}`);
}
```

- 몇 개까지 동시 연결이 가능한가?
- HTTP/1.1 vs HTTP/2에서 차이가 있는가?

### 활동 3: 실제 서비스 분석

다음 서비스들이 어떤 기술을 사용하는지 조사하세요:
- ChatGPT / Claude
- Slack
- Discord
- GitHub Actions 로그
- Jira 실시간 업데이트

---

## 생각해볼 점

1. "단순함이 이긴다"라는 관점에서, 언제 SSE를 선택해야 할까?

2. 새벽 3시에 연결 문제를 디버깅한다고 가정하면, 어떤 기술이 더 디버깅하기 쉬울까?

3. 하이브리드 접근법(SSE + REST API)은 언제 적합한가?

4. 미래에 WebTransport가 보편화되면 SSE와 WebSocket의 역할은 어떻게 변할까?

---

## 참고 키워드
- WebSocket vs SSE comparison
- SSE browser connection limit
- WebSocket proxy issues
- Real-time web architecture
- HTTP/2 multiplexing

---

학습 준비가 되었다면 [LEARN.md](./LEARN.md)로 진행하세요.
