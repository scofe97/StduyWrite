# SSE (Server-Sent Events) 학습 정리

## 1. SSE란?

### 정의
SSE(Server-Sent Events)란 서버에서 클라이언트로 단방향 실시간 데이터를 스트리밍하는 HTTP 기반 프로토콜입니다. 브라우저의 `EventSource` API로 연결하면, 서버가 `text/event-stream` 형식으로 이벤트를 지속적으로 푸시합니다.

### 왜 필요한가?
HTTP 요청-응답 모델은 클라이언트가 먼저 요청해야만 데이터를 받을 수 있습니다. 실시간 알림, 주식 가격, 대기열 상태처럼 서버가 주도적으로 데이터를 보내야 하는 경우, polling은 불필요한 요청이 많고 WebSocket은 양방향이 필요 없는 상황에서 과도합니다. SSE는 HTTP 위에서 단방향 스트리밍을 제공하여 이 간극을 메웁니다.

### 핵심 특징

| 특징 | 설명 |
|------|------|
| **단방향** | 서버 → 클라이언트만 가능. 클라이언트 → 서버는 별도 HTTP 요청 사용 |
| **HTTP 기반** | 별도 프로토콜 업그레이드 없음. 프록시, 로드밸런서 친화적 |
| **자동 재연결** | 연결 끊기면 브라우저가 자동으로 재연결 시도 |
| **Last-Event-ID** | 재연결 시 마지막 이벤트 ID를 서버에 전달하여 유실 방지 |
| **텍스트 전용** | 바이너리 데이터 전송 불가 (Base64 인코딩 필요) |

---

## 2. EventSource API (Ch02)

### 기본 사용

```typescript
const es = new EventSource('/events/basic');

es.onopen = () => console.log('연결됨');
es.onmessage = (e) => console.log('데이터:', e.data);
es.onerror = () => console.log('에러 발생');
```

### 인증이 필요한 경우

기본 `EventSource`는 커스텀 헤더를 설정할 수 없습니다. `event-source-polyfill`을 사용하면 Authorization 헤더를 추가할 수 있습니다.

```typescript
import { EventSourcePolyfill } from 'event-source-polyfill';

const es = new EventSourcePolyfill('/events/auth', {
  headers: { Authorization: `Bearer ${token}` },
  heartbeatTimeout: 60000,
});
```

**왜 Polyfill이 필요한가?** 브라우저 표준 EventSource는 URL과 withCredentials만 설정 가능하고, 커스텀 헤더를 지원하지 않기 때문입니다. 실무에서 JWT 인증이 필수적이므로 Polyfill이 거의 필수입니다.

---

## 3. 커스텀 이벤트 (Ch03)

### 서버에서 이벤트 타입 지정

```
event: user-joined
data: {"name": "Alice"}

event: message
data: {"text": "Hello"}
```

### 클라이언트에서 리스너 등록

```typescript
es.addEventListener('user-joined', (e) => {
  const data = JSON.parse(e.data);
});
```

`onmessage`는 `event:` 필드가 없는 기본 이벤트만 수신합니다. 커스텀 이벤트는 반드시 `addEventListener`로 등록해야 합니다.

---

## 4. 재연결 전략 (Ch04)

### Last-Event-ID 메커니즘

서버가 `id:` 필드를 보내면, 브라우저는 재연결 시 `Last-Event-ID` 헤더에 마지막 받은 ID를 포함합니다. 서버는 이 ID 이후의 이벤트만 전송하여 유실을 방지합니다.

```
id: 42
event: update
data: {"position": 5}
```

### Exponential Backoff

재연결 간격을 지수적으로 늘려서 서버 부하를 줄입니다.

```typescript
const delay = Math.min(30000, 1000 * Math.pow(2, attempt));
```

attempt 0: 1s → 1: 2s → 2: 4s → 3: 8s → 최대 30s

### 실습에서 배운 점
- `lastEventIdRef`를 useRef로 관리하여 리렌더링 없이 최신 ID 유지
- onopen에서 reconnectCount를 리셋하여 "성공하면 카운터 초기화" 패턴 적용
- cleanup 함수에서 disconnect + clearTimeout으로 좀비 타이머 방지

---

## 5. 에러 처리 전략 (Ch05)

### 상태 머신

```
disconnected → connecting → connected
                    ↓            ↓
                  error ←────── error
                    ↓
           fallback-polling
```

### readyState 기반 에러 분류

`onerror` 이벤트에서 `readyState`를 확인하여 에러 심각도를 판단합니다.

| readyState | 의미 | 대응 |
|-----------|------|------|
| `CONNECTING (0)` | 일시적 에러, 브라우저가 재연결 시도 중 | 대기 |
| `CLOSED (2)` | 치명적 에러, 연결 완전 종료 | 수동 재연결 또는 fallback |

### Heartbeat 타임아웃

서버가 주기적으로 빈 코멘트(`:heartbeat`)를 보내고, 클라이언트는 마지막 이벤트 시간을 추적합니다. 일정 시간 이벤트가 없으면 연결이 죽은 것으로 판단하여 재연결합니다.

### Polling Fallback

SSE 재시도가 maxRetries를 초과하면, 일반 HTTP polling으로 자동 전환합니다. 실시간성은 떨어지지만 데이터 수신은 보장됩니다.

---

## 6. React 통합 패턴 (Ch06)

### AbortController + isMountedRef 패턴

React 18 Strict Mode는 개발 환경에서 mount → unmount → remount를 시뮬레이션합니다. 이 과정에서 첫 번째 마운트의 EventSource가 정리되지 않으면 좀비 연결이 남습니다.

```typescript
const abortControllerRef = useRef<AbortController | null>(null);
const isMountedRef = useRef(true);

const connect = useCallback(() => {
  abortControllerRef.current = new AbortController();
  const es = new EventSource(url);

  es.onmessage = (e) => {
    if (!isMountedRef.current) return;  // 언마운트 후 setState 방지
    setMessages(prev => [...prev, e.data]);
  };
}, [url]);
```

### 왜 isMountedRef가 필요한가?

비동기 이벤트(SSE 메시지)가 컴포넌트 언마운트 후에 도착할 수 있습니다. 이때 `setState`를 호출하면 메모리 누수 경고가 발생합니다. `isMountedRef`로 가드하여 언마운트된 컴포넌트에 상태 업데이트를 방지합니다.

### useEffect cleanup

```typescript
useEffect(() => {
  isMountedRef.current = true;
  connect();

  return () => {
    isMountedRef.current = false;
    abortControllerRef.current?.abort();
    eventSourceRef.current?.close();
  };
}, []);
```

---

## 7. WebSocket vs SSE 비교 (Ch07)

| 항목 | SSE | WebSocket |
|------|-----|-----------|
| **방향** | 단방향 (서버→클라이언트) | 양방향 |
| **프로토콜** | HTTP | ws:// (업그레이드 필요) |
| **재연결** | 브라우저 내장 자동 재연결 | 직접 구현 필요 |
| **헤더** | 매 연결마다 HTTP 헤더 전송 | 최초 핸드셰이크만 |
| **프록시 호환** | 우수 (일반 HTTP) | 제한적 (Upgrade 필요) |
| **연결 비용** | 낮음 (단방향 버퍼) | 높음 (양방향 버퍼) |

### 선택 기준

SSE가 유리한 경우: 서버 → 클라이언트 단방향 푸시 (알림, 대기열, 주식 가격)
WebSocket이 유리한 경우: 양방향 통신 필요 (채팅, 게임, 실시간 협업)

**핵심**: "양방향이 필요한가?"가 선택의 핵심 기준입니다. 단방향이면 SSE가 인프라 비용과 구현 복잡도에서 유리합니다.

---

## 8. 대규모 아키텍처 패턴 (Ch08)

### Full Jitter (AWS 권장)

```typescript
const calculatedCeiling = Math.min(ceiling, baseMs * Math.pow(2, attempt));
return Math.random() * calculatedCeiling;
```

**기본 지수 백오프와의 차이**: 기본 백오프(`base * 2^attempt`)는 모든 클라이언트가 같은 시점에 재시도합니다. Full Jitter는 0부터 ceiling까지 균등 분포하여 thundering herd를 방지합니다.

**실무 예시**: 10,000명이 동시에 서버 장애를 경험한 경우, 기본 백오프는 1초 후 10,000개 요청이 동시에 들어오지만, Full Jitter는 0~1초 사이에 골고루 분산됩니다.

### 어댑티브 폴링

서버가 응답에 TTL(Time-To-Live)을 포함하여 클라이언트의 폴링 주기를 제어합니다.

```json
{ "position": 500, "total": 10000, "ttl": 5000 }
```

대기열 앞쪽 사용자는 짧은 TTL(빠른 폴링), 뒤쪽 사용자는 긴 TTL(느린 폴링)을 받습니다. 이렇게 서버가 부하를 능동적으로 조절합니다.

### TTL Jitter

같은 TTL을 받은 클라이언트들이 동시에 요청하는 것을 방지합니다.

```typescript
const jitter = ttl * 0.2 * (Math.random() * 2 - 1);  // ±20%
return Math.max(500, ttl + jitter);
```

TTL=3000ms → 실제 폴링 간격: 2400~3600ms 사이 랜덤

### 재연결 시 같은 서버 필요 여부

상태 저장 위치에 따라 결정됩니다:
- **로컬 메모리** (변수, Map): 같은 서버 필수 → Sticky Session
- **외부 저장소** (Redis, DB): 아무 서버나 가능 → 로드밸런서 자유 배분
- **SSE Last-Event-ID**: 서버가 외부 저장소에서 이벤트를 조회하면 Sticky 불필요

---

## 9. 면접 대비 요약

### 한 줄 정의
"SSE란 HTTP 기반의 서버→클라이언트 단방향 실시간 스트리밍 프로토콜로, EventSource API와 자동 재연결을 통해 간단하게 실시간 데이터를 수신할 수 있습니다."

### 핵심 포인트 3가지
1. **단방향 + HTTP 기반**: WebSocket과 달리 프로토콜 업그레이드가 필요 없어 프록시/로드밸런서 친화적입니다.
2. **Last-Event-ID로 유실 방지**: 재연결 시 마지막 이벤트 ID를 서버에 전달하여 빠진 이벤트를 재전송받습니다.
3. **Full Jitter로 thundering herd 방지**: 대규모 재연결 시 0~ceiling 균등 분포로 요청을 분산합니다.

### 자주 묻는 질문

**Q: SSE와 WebSocket 중 어떤 걸 선택하나요?**
A: 양방향 통신이 필요하면 WebSocket, 서버→클라이언트 단방향이면 SSE를 선택합니다. SSE는 HTTP 기반이라 인프라 비용이 낮고, 자동 재연결과 Last-Event-ID가 내장되어 구현이 간단합니다.

**Q: SSE 연결이 끊기면 어떻게 되나요?**
A: 브라우저가 자동으로 재연결을 시도합니다. Last-Event-ID 헤더로 마지막 수신 이벤트를 서버에 알려주어 이벤트 유실을 방지합니다. 서버의 `retry:` 필드로 재연결 간격을 제어할 수 있습니다.

**Q: 대규모 트래픽에서 SSE/폴링을 어떻게 관리하나요?**
A: 서버가 TTL로 클라이언트 폴링 주기를 제어하고(어댑티브 폴링), 클라이언트는 TTL에 ±20% Jitter를 적용합니다. 에러 재시도에는 Full Jitter를 사용하여 동시 요청 폭주를 방지합니다.

---

## 10. 실습 프로젝트 구조

```
09-sse/
├── learning/                    # 학습 문서 (Ch00~Ch08)
│   ├── 00-realtime-overview/
│   ├── 01-basics/
│   ├── 02-eventsource-api/
│   ├── 03-custom-events/
│   ├── 04-reconnection/
│   ├── 05-error-handling/
│   ├── 06-react-integration/
│   ├── 07-websocket-comparison/
│   └── 08-large-scale-architecture/
├── practice/
│   ├── react-app/               # 통합 React 앱 (React Router)
│   │   └── src/
│   │       ├── hooks/ch{02~08}/ # 챕터별 커스텀 훅
│   │       ├── components/ch{02~08}/ # 데모 컴포넌트
│   │       └── pages/           # 챕터별 페이지
│   └── server/main.go           # 통합 Go 서버 (port 3001)
└── LEARNED.md                   # 이 파일
```
