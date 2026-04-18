# 05. 에러 처리 - 조사 (INVESTIGATE)

> SSE 연결에서 발생할 수 있는 에러와 처리 방법을 탐구합니다.

---

## 핵심 질문

### 1. onerror 이벤트
- `onerror`는 언제 호출되는가?
- `onerror`의 event 객체에서 어떤 정보를 얻을 수 있는가?

```javascript
es.onerror = (event) => {
  console.log(event);  // 어떤 속성이 있을까?
  // event.message?
  // event.code?
  // event.reason?
};
```

### 2. 에러 종류 구분
- 네트워크 오류와 서버 오류를 어떻게 구분하는가?
- HTTP 404, 500 에러는 어떻게 처리되는가?

### 3. 재연결 vs 포기
- 어떤 경우에 재연결이 시도되고, 어떤 경우에 포기하는가?
- 무한 재연결을 방지하는 방법은?

### 4. 에러 복구 전략
- 폴백(fallback)은 언제 필요한가?
- SSE가 실패하면 어떤 대안이 있는가?

---

## 탐색 활동

### 활동 1: onerror 이벤트 분석

```javascript
const es = new EventSource('http://localhost:9999/not-exist');

es.onerror = (event) => {
  console.log('에러 타입:', event.type);
  console.log('이벤트 객체:', event);
  console.log('readyState:', es.readyState);
};
```

존재하지 않는 서버에 연결해보고, onerror에서 얻을 수 있는 정보를 확인하세요.

### 활동 2: HTTP 에러 응답

서버가 다른 HTTP 상태 코드를 반환하면 어떻게 되는지 테스트하세요:
- 200 OK: 정상 연결
- 404 Not Found: ?
- 500 Internal Server Error: ?
- 204 No Content: ?

### 활동 3: 연결 중 서버 중지

1. `/events` 엔드포인트에 연결합니다
2. 메시지를 몇 개 받은 후 서버를 중지합니다
3. onerror가 호출되는지, readyState가 어떻게 변하는지 관찰합니다
4. 재연결 시도가 발생하는지 확인합니다

---

## 생각해볼 점

1. 사용자에게 연결 오류를 어떻게 알려야 할까? (UI/UX 관점)

2. 모바일에서 네트워크가 자주 끊기는 경우, 어떻게 처리해야 할까?

3. 무한 재연결이 서버에 어떤 영향을 미칠까?

4. 서버가 완전히 다운된 경우와 일시적 네트워크 오류를 구분할 수 있을까?

---

## 참고 키워드
- EventSource onerror
- SSE error handling
- Connection timeout
- Fallback strategies
- Exponential backoff

---

학습 준비가 되었다면 [LEARN.md](./LEARN.md)로 진행하세요.
