# 06. React 통합 - 조사 (INVESTIGATE)

> React 애플리케이션에서 SSE를 사용하는 방법을 탐구합니다.

---

## 핵심 질문

### 1. useEffect에서 EventSource 관리
- EventSource 객체는 언제 생성하고 언제 정리해야 하는가?
- cleanup 함수에서 `close()`를 호출하지 않으면 어떻게 되는가?

```javascript
useEffect(() => {
  const es = new EventSource('/events');
  // ...

  return () => {
    // 여기서 뭘 해야 할까?
  };
}, []);
```

### 2. 상태 업데이트 패턴
- SSE로 받은 데이터를 React 상태에 어떻게 반영하는가?
- 메시지가 빠르게 들어올 때 성능 문제가 있는가?

```javascript
const [messages, setMessages] = useState([]);

es.onmessage = (e) => {
  setMessages(prev => [...prev, e.data]);  // 이 방식이 최선인가?
};
```

### 3. 커스텀 훅 설계
- `useSSE` 훅은 어떻게 설계해야 하는가?
- 반환해야 하는 값들은?

```javascript
const { data, error, isConnected } = useSSE('/events');
```

### 4. POST 요청이 필요한 경우
- EventSource는 GET만 지원하는데, POST가 필요하면?
- `@microsoft/fetch-event-source` 라이브러리는 어떤 문제를 해결하는가?

### 5. SSE 전용 라이브러리
- WebSocket에는 `react-use-websocket`이 있는데, SSE에도 비슷한 것이 있는가?
- 직접 훅을 만드는 것과 라이브러리 사용의 장단점은?

---

## 탐색 활동

### 활동 1: cleanup 필요성 확인

```javascript
// cleanup 없이 테스트
function BadComponent() {
  useEffect(() => {
    const es = new EventSource('/events');
    es.onmessage = (e) => console.log(e.data);
    // return 없음!
  }, []);
}
```

컴포넌트를 마운트/언마운트하면서 Network 탭을 관찰하세요.
연결이 정리되는가, 계속 유지되는가?

### 활동 2: Strict Mode에서의 동작

```javascript
<React.StrictMode>
  <App />
</React.StrictMode>
```

Strict Mode에서 useEffect가 두 번 실행되면 어떤 일이 발생하는가?

### 활동 3: fetch-event-source 조사

`@microsoft/fetch-event-source` 라이브러리를 조사하세요:
- 어떤 기능을 제공하는가?
- EventSource API와 어떻게 다른가?
- POST 요청을 어떻게 보내는가?

---

## 생각해볼 점

1. SSE 연결은 컴포넌트 레벨에서 관리해야 할까, 전역 상태에서 관리해야 할까?

2. 여러 컴포넌트가 같은 SSE 데이터를 필요로 하면 어떻게 해야 할까?

3. 페이지 이동 시 SSE 연결을 어떻게 처리해야 할까?

4. 서버 컴포넌트(Server Component)에서 SSE를 사용할 수 있을까?

---

## 참고 키워드
- React useEffect cleanup
- Custom hooks for SSE
- @microsoft/fetch-event-source
- React state batching
- Strict Mode double invocation

---

학습 준비가 되었다면 [LEARN.md](./LEARN.md)로 진행하세요.
