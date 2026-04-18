# 08. 스케일링 고려사항 - 학습 (LEARN)

## 학습 목표
WebSocket 기반 시스템의 스케일링 과제를 이해하고, 대규모 환경에서의 아키텍처 설계 및 한계를 면접에서 설명할 수 있다.

---

## A1. WebSocket 스케일링의 어려움

### Stateful 연결의 도전

**HTTP API는 Stateless입니다.** 어떤 서버가 요청을 처리해도 결과가 동일합니다. 반면 **WebSocket은 Stateful**입니다. 특정 서버에 연결이 유지되어 있어, 해당 서버만 클라이언트와 통신할 수 있습니다.

```mermaid
flowchart TB
    subgraph HTTP["HTTP API (Stateless)"]
        direction LR
        Client1["클라이언트"] --> LB1["로드밸런서"]
        LB1 --> S1A["서버 A"]
        LB1 --> S1B["서버 B"]
        LB1 --> S1C["서버 C"]
        Note1["어느 서버로 가도 OK"]
    end

    subgraph WebSocket["WebSocket (Stateful)"]
        direction LR
        Client2["클라이언트"] --> LB2["로드밸런서"]
        LB2 -->|"연결 유지"| S2A["서버 A<br/>(연결됨)"]
        LB2 -.->|"X"| S2B["서버 B"]
        LB2 -.->|"X"| S2C["서버 C"]
        Note2["반드시 서버 A로"]
    end
```

### 스케일링 차이점

| 항목 | HTTP API | WebSocket |
|------|----------|-----------|
| **상태** | Stateless | Stateful |
| **로드밸런싱** | 라운드로빈 OK | Sticky Session 필요 |
| **서버 추가** | 즉시 트래픽 분산 | 기존 연결 재분배 필요 |
| **서버 제거** | 다음 요청은 다른 서버로 | 연결 끊김, 재연결 필요 |
| **장애 복구** | 자동 (다른 서버로) | 클라이언트 재연결 필요 |

---

## A2. 로드밸런서 설정

### L4 vs L7 로드밸런서

**WebSocket은 HTTP 핸드셰이크로 시작합니다.** 따라서 L7(HTTP 인식) 로드밸런서가 필요합니다.

```mermaid
flowchart TB
    subgraph L4["L4 로드밸런서 (TCP)"]
        direction TB
        L4_LB["IP:Port 기반<br/>라우팅"]
        L4_P["장점: 빠름, 단순"]
        L4_C["단점: HTTP 헤더 못 봄"]
    end

    subgraph L7["L7 로드밸런서 (HTTP)"]
        direction TB
        L7_LB["HTTP 헤더 기반<br/>라우팅"]
        L7_P["장점: 쿠키, URL 인식"]
        L7_C["필수: WebSocket 업그레이드 지원"]
    end
```

### Sticky Session 구현 방식

**Sticky Session은 동일 클라이언트를 동일 서버로 라우팅합니다.**

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant LB as 로드밸런서
    participant S1 as 서버 1
    participant S2 as 서버 2

    C->>LB: WebSocket 핸드셰이크
    LB->>S1: 라우팅 (서버 1 선택)
    S1-->>LB: 101 Switching Protocols
    LB-->>C: Set-Cookie: SERVERID=s1

    Note over C,S1: WebSocket 연결 수립

    C->>LB: 재연결 시 (Cookie: SERVERID=s1)
    LB->>S1: 같은 서버로 라우팅
```

**구현 방식:**

| 방식 | 설명 | 장단점 |
|------|------|--------|
| **쿠키 기반** | `Set-Cookie: SERVERID=s1` | 브라우저 자동 전송, 범용적 |
| **IP 해시** | 클라이언트 IP로 서버 결정 | 쿠키 불필요, NAT 문제 |
| **URL 파라미터** | `ws://host?server=s1` | 명시적, 추가 구현 필요 |

### AWS ALB WebSocket 설정

```yaml
# ALB Target Group 설정
TargetGroup:
  Protocol: HTTP
  HealthCheckPath: /health
  # Sticky Session 활성화
  TargetGroupAttributes:
    - Key: stickiness.enabled
      Value: 'true'
    - Key: stickiness.type
      Value: lb_cookie
    - Key: stickiness.lb_cookie.duration_seconds
      Value: '86400'  # 24시간
```

---

## A3. 메시지 브로드캐스트

### 문제: 서버 간 통신

**채팅방에 100만 명이 접속해 있고, 서버가 10대라면?** 서버 A의 사용자가 보낸 메시지를 서버 B, C, ...의 사용자에게 어떻게 전달할까요?

```mermaid
flowchart TB
    subgraph Problem["문제 상황"]
        U1["사용자 1<br/>(서버 A)"]
        U2["사용자 2<br/>(서버 B)"]
        U3["사용자 3<br/>(서버 C)"]

        U1 -->|"메시지 전송"| SA["서버 A"]
        SA -->|"???"| SB["서버 B"]
        SA -->|"???"| SC["서버 C"]
        SB --> U2
        SC --> U3
    end
```

### 해결: Redis Pub/Sub

**Redis Pub/Sub는 서버 간 메시지 브로드캐스트 채널을 제공합니다.**

```mermaid
flowchart TB
    subgraph Solution["Redis Pub/Sub 솔루션"]
        U1["사용자 1"] --> SA["서버 A"]
        SA -->|"PUBLISH"| Redis["Redis"]
        Redis -->|"SUBSCRIBE"| SA
        Redis -->|"SUBSCRIBE"| SB["서버 B"]
        Redis -->|"SUBSCRIBE"| SC["서버 C"]
        SB --> U2["사용자 2"]
        SC --> U3["사용자 3"]
    end
```

### 구현 예시 (Node.js + Redis)

```typescript
import { createClient } from 'redis';
import { WebSocketServer } from 'ws';

const pubClient = createClient();
const subClient = createClient().duplicate();

await pubClient.connect();
await subClient.connect();

const wss = new WebSocketServer({ port: 8080 });
const roomConnections = new Map<string, Set<WebSocket>>();

// Redis 구독: 다른 서버의 메시지 수신
await subClient.pSubscribe('chat:*', (message, channel) => {
  const roomId = channel.replace('chat:', '');
  const connections = roomConnections.get(roomId) || new Set();

  // 로컬 연결된 사용자에게 전송
  connections.forEach(ws => ws.send(message));
});

wss.on('connection', (ws, req) => {
  const roomId = req.url?.split('/').pop() || 'default';

  // 방에 연결 추가
  if (!roomConnections.has(roomId)) {
    roomConnections.set(roomId, new Set());
  }
  roomConnections.get(roomId)!.add(ws);

  ws.on('message', async (data) => {
    // Redis로 발행: 모든 서버에 브로드캐스트
    await pubClient.publish(`chat:${roomId}`, data.toString());
  });

  ws.on('close', () => {
    roomConnections.get(roomId)?.delete(ws);
  });
});
```

### 메시지 브로커 비교

| 브로커 | 장점 | 단점 | 적합한 경우 |
|--------|------|------|------------|
| **Redis Pub/Sub** | 간단, 빠름, 저지연 | 메시지 유실 가능, 영속성 없음 | 실시간 채팅, 알림 |
| **Redis Streams** | 메시지 영속성, 순서 보장 | 복잡도 증가 | 순서 중요한 경우 |
| **Kafka** | 대용량, 내구성, 리플레이 | 지연 시간 높음, 복잡 | 대규모 이벤트 스트리밍 |
| **RabbitMQ** | 유연한 라우팅, 메시지 보장 | 설정 복잡 | 복잡한 메시지 라우팅 |

---

## A4. 재접속 폭풍 대응

### 문제: 재접속 폭풍 (Reconnection Storm)

**네트워크 장애로 10만 연결이 동시에 끊기면?** 10만 클라이언트가 동시에 재연결을 시도하여 서버가 과부하됩니다.

```mermaid
sequenceDiagram
    participant Users as 10만 사용자
    participant LB as 로드밸런서
    participant Servers as 서버들

    Note over Users,Servers: 정상 상태

    rect rgb(255, 220, 220)
        Note over LB: 네트워크 1초 장애
        Users-xLB: 10만 연결 끊김
    end

    rect rgb(255, 200, 200)
        Note over Users,Servers: 재접속 폭풍!
        Users->>LB: 10만 동시 재연결
        Note over Servers: CPU 100%, 메모리 폭증
        LB--xUsers: 연결 거부, 타임아웃
    end
```

### 왜 WebSocket 재연결 폭풍이 더 위험한가? (HTTP vs WebSocket)

**HTTP 수천 요청과 WebSocket 수천 연결 요청은 근본적으로 다릅니다.**

```mermaid
flowchart TB
    subgraph HTTP["HTTP 수천 요청"]
        direction TB
        H1["요청 처리"] --> H2["응답 반환"]
        H2 --> H3["리소스 해제"]
        H3 --> H4["다음 요청 가능"]
    end

    subgraph WS["WebSocket 수천 연결"]
        direction TB
        W1["핸드셰이크"] --> W2["연결 수립"]
        W2 --> W3["메모리 점유"]
        W3 --> W4["계속 유지..."]
    end

    HTTP -->|"일시적 부하"| R1["빠르게 복구"]
    WS -->|"지속적 부하"| R2["리소스 계속 점유"]
```

#### 핵심 차이점

| | HTTP 요청 | WebSocket 연결 |
|--|----------|---------------|
| **요청 후** | 응답하고 끝 | **연결 유지** |
| **리소스** | 처리 후 해제 | 연결 종료까지 점유 |
| **상태** | Stateless | Stateful |
| **핸드셰이크** | Keep-Alive면 재사용 | **매번** TCP+TLS+HTTP Upgrade |

#### 핸드셰이크 비용 비교

**HTTP 요청:**
```
1. TCP 연결 (Keep-Alive면 재사용)
2. TLS (세션 재사용 가능)
3. HTTP 요청/응답
4. 끝 - 리소스 해제
```

**WebSocket 연결:**
```
1. TCP 3-way handshake
2. TLS handshake (wss://)
3. HTTP Upgrade 요청
4. 101 Switching Protocols 응답
5. Sec-WebSocket-Accept 검증
6. 소켓 객체 생성 (메모리)
7. 이벤트 리스너 등록
8. 파일 디스크립터 할당
→ HTTP보다 훨씬 비용이 높음
```

#### 수치로 비교 (수천 개 기준)

| 항목 | HTTP 수천 요청 | WebSocket 수천 연결 |
|------|--------------|-------------------|
| **메모리** | 일시적 수 MB, 곧 해제 | 수십 GB **지속 점유** |
| **파일 디스크립터** | 재사용 가능 | 연결당 1개 점유 |
| **1초 후** | 대부분 처리 완료 | 연결 수립 중 |
| **1시간 후** | 정상 상태 | **여전히** 수천 개 점유 |

#### 악순환 구조

```mermaid
flowchart TB
    Storm["수천 개 동시 재연결"]

    Storm --> Cost1["TCP+TLS 핸드셰이크<br/>(CPU 집약적)"]
    Storm --> Cost2["소켓 객체 생성<br/>(메모리)"]
    Storm --> Cost3["파일 디스크립터<br/>(OS 한계)"]

    Cost1 --> Problem["서버 과부하"]
    Cost2 --> Problem
    Cost3 --> Problem

    Problem --> Fail["새 연결 거부/타임아웃"]
    Fail --> Retry["클라이언트 재시도"]
    Retry --> Storm
```

**결론:**
```
HTTP 수천 요청 = "잠깐 바쁨" (처리하면 끝)
WebSocket 수천 연결 = "영구적 부담" (연결 유지 비용)
```

---

### 대응 전략 1: 지수 백오프의 한계와 Full Jitter

**기본 지수 백오프**는 재시도 간격을 지수적으로 증가시키고, **Jitter**는 랜덤 지연을 추가합니다.

#### 기본 구현 (문제 있음)

```typescript
// 기본 방식: 고정 지연 + 작은 Jitter
function basicBackoff(attempt: number): number {
  const baseDelay = Math.min(1000 * Math.pow(2, attempt), 30000);
  const jitter = Math.random() * 1000; // 0~1초 Jitter
  return baseDelay + jitter;
}

// 1차: 1000 + (0~1000) = 1000~2000ms
// 2차: 2000 + (0~1000) = 2000~3000ms
// 3차: 4000 + (0~1000) = 4000~5000ms
```

#### 문제점: 여전히 밀집됨

```
장애 발생 시점 (t=0)
├── 클라이언트 1: 1초 + jitter = 1~2초 후 재연결
├── 클라이언트 2: 1초 + jitter = 1~2초 후 재연결
├── 클라이언트 3: 1초 + jitter = 1~2초 후 재연결
└── ... 수천 개가 1~2초 사이에 몰림!
```

**1초 범위의 Jitter로는 수천 개의 요청을 충분히 분산시키지 못합니다.**

#### 해결책: Full Jitter (AWS 권장)

```typescript
// Full Jitter: 0부터 계산된 값 사이에서 랜덤
function fullJitter(attempt: number): number {
  const ceiling = Math.min(30000, 1000 * Math.pow(2, attempt));
  return Math.random() * ceiling; // 0 ~ ceiling 사이 랜덤
}

// 1차: random(0, 1000)  → 0~1초 어디든
// 2차: random(0, 2000)  → 0~2초 어디든
// 3차: random(0, 4000)  → 0~4초 어디든
```

```mermaid
flowchart LR
    subgraph Basic["기본: 고정 + 작은 Jitter"]
        B1["1차: 1000~2000ms"]
        B2["2차: 2000~3000ms"]
    end

    subgraph Full["Full Jitter"]
        F1["1차: 0~1000ms"]
        F2["2차: 0~2000ms"]
    end

    Basic -->|"여전히 밀집"| Problem["1초 안에 수천 요청"]
    Full -->|"넓게 분산"| Solution["시간대별 분산"]
```

#### 추가 전략: Initial Delay

**1차 시도부터 분산시키려면 연결 끊김 감지 후 즉시가 아닌, 랜덤 지연 후 재연결:**

```typescript
function onDisconnect() {
  // 즉시 재연결 X
  // 0~5초 사이 랜덤 지연 후 첫 재연결 시도
  const initialDelay = Math.random() * 5000;

  setTimeout(() => {
    reconnectWithBackoff();
  }, initialDelay);
}
```

#### 지수 백오프의 진짜 효과

**1차 실패는 불가피합니다.** 지수 백오프의 효과는 2차, 3차 시도에서 나타납니다.

```mermaid
sequenceDiagram
    participant C1 as 클라이언트 1
    participant C2 as 클라이언트 2
    participant C3 as 클라이언트 3
    participant S as 서버

    Note over S: 장애 발생 (t=0)

    rect rgb(255, 220, 220)
        Note over C1,S: 1차 시도 - 여전히 밀집
        C1->>S: 재연결 (실패)
        C2->>S: 재연결 (실패)
        C3->>S: 재연결 (실패)
    end

    rect rgb(255, 255, 200)
        Note over C1,S: 2차 시도 - 분산 시작 (Full Jitter)
        Note over C1: 0.5초 후
        Note over C2: 1.8초 후
        Note over C3: 1.2초 후
    end

    rect rgb(220, 255, 220)
        Note over C1,S: 3차 시도 - 더 넓게 분산
        C1->>S: 재연결 (성공!)
        Note over C1: 더 이상 재시도 안 함
        C3->>S: 재연결 (성공!)
        C2->>S: 재연결 (성공!)
    end
```

**핵심:** 성공한 클라이언트는 재시도 안 함 → 시간이 지날수록 부하 감소

#### 완전한 구현

```typescript
class ReconnectionStrategy {
  private attempt = 0;
  private maxDelay = 30000;

  getDelay(): number {
    // Full Jitter: 0부터 ceiling 사이 랜덤
    const ceiling = Math.min(
      this.maxDelay,
      1000 * Math.pow(2, this.attempt)
    );

    this.attempt++;
    return Math.random() * ceiling;
  }

  reset() {
    this.attempt = 0;
  }
}

function onDisconnect() {
  const strategy = new ReconnectionStrategy();

  // Initial Delay: 첫 시도부터 분산
  const initialDelay = Math.random() * 5000;

  setTimeout(() => reconnect(strategy), initialDelay);
}

function reconnect(strategy: ReconnectionStrategy) {
  const delay = strategy.getDelay();

  setTimeout(async () => {
    try {
      await connect();
      strategy.reset();
    } catch {
      reconnect(strategy);
    }
  }, delay);
}
```

#### 전략 비교

| 전략 | 1차 시도 | 2차+ 시도 | 효과 |
|------|---------|---------|------|
| **기본 백오프** | 밀집 | 약간 분산 | 부족 |
| **Full Jitter** | 밀집 | 넓게 분산 | 양호 |
| **Initial Delay** | 분산 | - | 1차에 효과 |
| **Full Jitter + Initial Delay** | 분산 | 넓게 분산 | **최선** |

### 대응 전략 2: Socket.IO 폴백

**Socket.IO는 WebSocket 실패 시 자동으로 Long Polling으로 폴백합니다.**

```mermaid
flowchart TB
    Start["연결 시도"] --> WS{"WebSocket<br/>가능?"}

    WS -->|"Yes"| WSConn["WebSocket 연결"]
    WS -->|"No"| LP["Long Polling 폴백"]

    WSConn --> Monitor["연결 모니터링"]
    LP --> Monitor

    Monitor -->|"연결 끊김"| Retry["재연결 시도"]
    Retry -->|"지수 백오프"| WS
```

```javascript
// Socket.IO 클라이언트 설정
const socket = io('https://example.com', {
  // 폴백 순서
  transports: ['websocket', 'polling'],

  // 재연결 설정
  reconnection: true,
  reconnectionAttempts: 10,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 30000,
  randomizationFactor: 0.5, // Jitter
});
```

### 대응 전략 3: 서버 측 보호

```typescript
// 연결 속도 제한 (Rate Limiting)
const connectionRateLimit = new RateLimit({
  windowMs: 1000, // 1초
  max: 1000, // 최대 1000 연결/초
  message: 'Too many connections',
});

// 서킷 브레이커
const circuitBreaker = new CircuitBreaker({
  threshold: 50, // 50% 실패 시
  timeout: 30000, // 30초 차단
  onOpen: () => console.log('Circuit opened: rejecting new connections'),
});
```

---

## A5. 언제 WebSocket을 선택하지 말아야 하는가

### 1. 단방향 상태 확인만 필요할 때

**SSE(Server-Sent Events)가 더 적합합니다.**

| 요구사항 | WebSocket | SSE |
|----------|:---------:|:---:|
| 서버→클라이언트 단방향 | 과도함 | 적합 |
| 양방향 통신 | 적합 | 부적합 |
| 자동 재연결 | 수동 구현 | 브라우저 내장 |
| HTTP 호환성 | 업그레이드 필요 | 100% 호환 |
| 방화벽 통과 | 차단 가능 | HTTP이므로 통과 |

```mermaid
flowchart TB
    Q1{"양방향 통신<br/>필요?"} -->|"No"| SSE["SSE 선택"]
    Q1 -->|"Yes"| WS["WebSocket 선택"]
```

### 2. 50만+ 동시접속 환경

**연결 유지 비용이 요청 비용을 초과합니다.**

```
WebSocket: 50만 연결 × 10KB = 5GB 메모리 상주
Polling:   요청당 처리 후 해제 (Stateless)
```

| 항목 | WebSocket | 폴링 |
|------|:---------:|:----:|
| 서버 메모리 | 5~10GB | 낮음 |
| 스케일 아웃 | 복잡 | 서버 추가만 |
| 재접속 폭풍 | 위험 | 없음 |
| 로드밸런싱 | Sticky 필요 | 라운드로빈 |

**대기열, 상태 조회 같은 가벼운 요청은 폴링이 더 효율적입니다.**

### 3. 기업 네트워크 환경 (방화벽)

**많은 기업 방화벽과 프록시가 WebSocket을 차단합니다.**

```mermaid
flowchart LR
    subgraph Blocked["WebSocket 차단"]
        C1["클라이언트"] --> F1["기업 방화벽"]
        F1 -->|"ws:// 차단"| X1["❌"]
    end

    subgraph Allowed["HTTP 통과"]
        C2["클라이언트"] --> F2["기업 방화벽"]
        F2 -->|"HTTP OK"| S2["서버"]
    end
```

**이유:**
- `ws://`는 HTTP가 아닌 별도 프로토콜로 업그레이드
- 딥 패킷 검사(DPI)가 비-HTTP 트래픽 차단
- 보안 정책이 HTTP/HTTPS만 허용

**대안:**
- `wss://` (TLS 암호화) 사용 시 통과 확률 높음
- SSE 사용 (HTTP 기반)
- Long Polling 폴백

### 4. WebSocket을 선택해야 할 때

**반대로, 다음 상황에서는 WebSocket이 최선의 선택입니다.**

| 상황 | 이유 |
|------|------|
| **양방향 실시간 통신** | 채팅, 협업 도구 - 클라이언트도 서버로 데이터 전송 |
| **고빈도 메시지** | 초당 수십 건 이상 메시지 교환 시 HTTP 오버헤드 회피 |
| **저지연 필수** | 게임, 트레이딩 - 밀리초 단위 응답 필요 |
| **바이너리 데이터** | 파일 전송, 미디어 스트리밍 - 프레임 기반 효율적 전송 |
| **상태 기반 프로토콜** | 턴제 게임, 실시간 경매 - 연결 상태 유지 필요 |

### 기술 선택 플로우차트

```mermaid
flowchart TD
    Start["실시간 통신 필요"] --> Q1{"양방향 통신<br/>필요?"}

    Q1 -->|"Yes"| Q2{"고빈도 메시지?<br/>(초당 10건+)"}
    Q1 -->|"No"| SSE["✅ SSE 선택<br/>(단방향, 간단)"]

    Q2 -->|"Yes"| Q3{"동시접속<br/>규모?"}
    Q2 -->|"No"| Consider["양방향이지만<br/>저빈도면 재고"]

    Q3 -->|"< 10만"| WS["✅ WebSocket 선택"]
    Q3 -->|"> 50만"| Hybrid["⚠️ 하이브리드 고려<br/>(폴링 + 캐시)"]

    Consider --> Q4{"방화벽<br/>환경?"}
    Q4 -->|"기업 네트워크"| Fallback["SSE + 폴백"]
    Q4 -->|"일반 환경"| WS
```

---

## A6. 2026년 기준 신기술: WebTransport

### WebTransport란?

**HTTP/3 기반의 양방향 통신 API입니다.** WebSocket의 후계자로 기대됩니다.

| 특성 | WebSocket | WebTransport |
|------|-----------|--------------|
| **기반 프로토콜** | TCP | QUIC (UDP) |
| **핸드셰이크** | TCP + TLS + HTTP | QUIC (더 빠름) |
| **스트림** | 단일 연결 | 다중 스트림 |
| **신뢰성** | 항상 신뢰 | 선택 가능 (신뢰/비신뢰) |
| **지연 시간** | 중간 | 낮음 |

### 브라우저 지원 현황 (2026년)

| 브라우저 | 지원 |
|----------|:----:|
| Chrome | ✅ |
| Edge | ✅ |
| Firefox | 🔄 실험적 |
| Safari | ❌ 미지원 |

**결론:** WebSocket이 현재 실용적인 선택. WebTransport는 2~3년 후 생태계 성숙 시 대안.

---

## 요약

```mermaid
flowchart LR
    subgraph Challenges["스케일링 과제"]
        C1["Stateful 연결"]
        C2["서버 간 브로드캐스트"]
        C3["재접속 폭풍"]
        C4["방화벽 차단"]
    end

    subgraph Solutions["해결책"]
        S1["Sticky Session"]
        S2["Redis Pub/Sub"]
        S3["지수 백오프 + Jitter"]
        S4["SSE/Long Polling 폴백"]
    end

    C1 --> S1
    C2 --> S2
    C3 --> S3
    C4 --> S4
```

| 핵심 개념 | 설명 |
|----------|------|
| **Stateful 연결** | 로드밸런싱에 Sticky Session 필요 |
| **Redis Pub/Sub** | 서버 간 메시지 브로드캐스트 |
| **HTTP vs WS 연결** | HTTP는 처리 후 해제, WS는 계속 점유 |
| **재접속 폭풍** | Full Jitter + Initial Delay로 완화 |
| **대안 기술** | SSE (단방향), 폴링 (대규모) |
| **WebTransport** | 미래 기술, 현재는 WebSocket 사용 |

---

## 면접 질문 대비

### Q: "WebSocket 서버를 어떻게 스케일 아웃하겠습니까?"

**모범 답변:**
> "WebSocket은 Stateful 연결이므로 HTTP와 다른 전략이 필요합니다.
>
> 1. **로드밸런서**: L7 + Sticky Session (쿠키 또는 IP 해시)
> 2. **서버 간 통신**: Redis Pub/Sub로 메시지 브로드캐스트
> 3. **재접속 대비**: 지수 백오프 + Jitter 재연결 로직
> 4. **모니터링**: 연결 수, 메모리, 재연결률 모니터링
>
> 단, 50만+ 대규모 환경에서는 연결 유지 비용을 고려하여 폴링이나 SSE도 검토하겠습니다."

---

이전 섹션: [07. 실제 코드 분석](../07-real-world/)
