# INVESTIGATE: react-use-websocket 라이브러리

## 학습 목표
`react-use-websocket` 라이브러리의 핵심 기능과 사용 패턴을 이해합니다.

---

## 소크라테스 질문

### Q1. useWebSocket 반환값

> `useWebSocket`의 반환값인 `sendMessage`, `lastMessage`, `readyState`는 각각 어떤 역할을 하는가?

**생각해볼 점:**
- `sendMessage`와 네이티브 `socket.send()`의 차이점은?
- `lastMessage`는 왜 단일 값인가? 모든 메시지가 필요하면?
- `readyState`는 어떤 타입이고, 어떻게 활용하는가?

---

### Q2. 조건부 연결 패턴

> URL을 `null`로 전달하면 어떤 일이 발생하며, 왜 이 패턴이 유용한가?

**생각해볼 점:**
- 특정 조건이 만족될 때만 WebSocket을 연결하려면?
- `shouldConnect` 옵션과 `null` URL의 차이는?
- 조건부 연결의 실제 사용 사례는?

```typescript
// 이 코드는 어떻게 동작할까?
const { sendMessage } = useWebSocket(isLoggedIn ? WS_URL : null);
```

---

### Q3. 메시지 히스토리

> 모든 수신 메시지를 저장하려면 `lastMessage` 외에 어떤 옵션을 사용해야 하는가?

**생각해볼 점:**
- `lastMessage`만으로 충분하지 않은 경우는?
- 메시지 히스토리를 직접 관리하는 것과 라이브러리 옵션 사용의 차이는?

---

### Q4. 옵션 객체

> `useWebSocket`의 주요 옵션들(`onOpen`, `onMessage`, `onClose`, `onError`)은 어떻게 활용되는가?

**생각해볼 점:**
- 콜백으로 전달하는 것과 반환값(`lastMessage`)을 사용하는 것의 차이는?
- 언제 콜백을 사용하고 언제 반환값을 사용해야 하는가?

---

## 다음 단계
질문에 대한 답을 찾았다면 `LEARN.md`에 정리하고, `practice/` 폴더에서 실습합니다.
