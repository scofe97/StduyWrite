# WebSocket

## 학습 목표

Go에서 WebSocket을 사용하여 실시간 양방향 통신 구현

---

## WebSocket이란?

### HTTP vs WebSocket

| 특성 | HTTP | WebSocket |
|------|------|-----------|
| 연결 | 요청-응답 후 종료 | 지속적 연결 |
| 방향 | 클라이언트 → 서버 | 양방향 |
| 오버헤드 | 매 요청마다 헤더 | 초기 핸드셰이크만 |
| 사용 사례 | REST API | 실시간 채팅, 게임 |

### WebSocket 핸드셰이크

```
클라이언트 → 서버: HTTP Upgrade 요청
Connection: Upgrade
Upgrade: websocket

서버 → 클라이언트: HTTP 101 Switching Protocols
```

이후 TCP 연결을 유지하며 양방향 통신

---

## gorilla/websocket

Go에서 가장 많이 사용되는 WebSocket 라이브러리

### 기본 사용법

**업그레이더 설정**:
```go
var upgrader = websocket.Upgrader{
    ReadBufferSize:  1024,
    WriteBufferSize: 1024,
    CheckOrigin: func(r *http.Request) bool {
        return true // 개발용: 모든 origin 허용
    },
}
```

**연결 업그레이드**:
```go
func wsHandler(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Println(err)
        return
    }
    defer conn.Close()
    
    // 메시지 처리 루프
    for {
        messageType, p, err := conn.ReadMessage()
        if err != nil {
            return
        }
        // 에코
        conn.WriteMessage(messageType, p)
    }
}
```

### 메시지 타입

| 타입 | 상수 | 용도 |
|------|------|------|
| Text | `websocket.TextMessage` | JSON, 문자열 |
| Binary | `websocket.BinaryMessage` | 바이너리 데이터 |
| Ping | `websocket.PingMessage` | 연결 상태 확인 |
| Pong | `websocket.PongMessage` | Ping 응답 |
| Close | `websocket.CloseMessage` | 연결 종료 |

---

## 주요 패턴

### 1. 에코 서버

클라이언트가 보낸 메시지를 그대로 반환

### 2. 브로드캐스트

한 클라이언트의 메시지를 모든 연결된 클라이언트에게 전송

```go
type Hub struct {
    clients    map[*websocket.Conn]bool
    broadcast  chan []byte
    register   chan *websocket.Conn
    unregister chan *websocket.Conn
}
```

### 3. 채팅방

특정 그룹의 클라이언트에게만 메시지 전송

---

## 연결 관리

### Ping/Pong

```go
conn.SetPingHandler(func(appData string) error {
    return conn.WriteControl(
        websocket.PongMessage, 
        []byte(appData), 
        time.Now().Add(time.Second),
    )
})
```

### Graceful Close

```go
conn.WriteMessage(
    websocket.CloseMessage,
    websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""),
)
```

---

## Spring과 비교

| Spring | Go |
|--------|-----|
| `@ServerEndpoint` | `upgrader.Upgrade()` |
| `@OnMessage` | `conn.ReadMessage()` |
| `Session.sendMessage()` | `conn.WriteMessage()` |
| `@OnOpen/@OnClose` | defer conn.Close() |

---

## TCP 연결과 소켓 기초

WebSocket은 HTTP Upgrade 후 **TCP 연결을 유지**합니다. 서버가 100개의 클라이언트와 연결되었을 때, 특정 클라이언트에게만 메시지를 보낼 수 있는 이유는 TCP의 연결 식별 방식 때문입니다.

### 4-Tuple: 연결 식별자

TCP 연결은 4가지 요소로 고유하게 식별됩니다:

| 요소 | 설명 | 예시 |
|------|------|------|
| Server IP | 서버 주소 | `192.168.1.100` |
| Server Port | 서버 포트 | `8080` |
| Client IP | 클라이언트 주소 | `10.0.0.50` |
| Client Port | 클라이언트 포트 | `52341` (임시 포트) |

동일한 클라이언트 IP에서 여러 WebSocket 연결을 열어도, **Client Port(Ephemeral Port)가 다르기 때문에** 각 연결이 구분됩니다.

### Ephemeral Port (임시 포트)

클라이언트가 서버에 연결할 때, OS가 자동으로 임시 포트를 할당합니다:

| OS | 범위 |
|----|------|
| Linux | 32768 - 60999 |
| Windows/macOS | 49152 - 65535 |

```go
// Go에서 연결 정보 확인
func handleConn(conn *websocket.Conn) {
    // 4-Tuple 정보 얻기
    localAddr := conn.LocalAddr()   // 서버 IP:Port
    remoteAddr := conn.RemoteAddr() // 클라이언트 IP:Port (Ephemeral Port 포함)

    log.Printf("연결: %s → %s", remoteAddr, localAddr)
    // 출력 예: "연결: 10.0.0.50:52341 → 192.168.1.100:8080"
}
```

### Listen Socket vs Connection Socket

서버는 두 종류의 소켓을 사용합니다:

| 종류 | 수량 | 역할 |
|------|------|------|
| Listen Socket | 1개 (포트당) | 새 연결 대기, `accept()` |
| Connection Socket | N개 (연결당) | 데이터 송수신, `read()`/`write()` |

```go
// Listen Socket - 8080 포트에서 대기
listener, _ := net.Listen("tcp", ":8080")

for {
    // accept()가 Connection Socket 반환
    conn, _ := listener.Accept()  // 새 소켓 생성 (fd 할당)

    go handleClient(conn)  // 고루틴으로 처리
}
```

### 상세 학습

TCP 소켓의 시스템 콜 레벨 동작은 다음 문서를 참조하세요:

- **시스템 프로그래밍**: `02-go/11-system-programming/03-network-io/` - epoll, 시스템 콜 분석
- **프론트엔드 관점**: `01-frontend/08-websocket/01-basics/LEARN.md` - 4-Tuple, 패킷 라우팅 상세

---

## 참고 자료

- [gorilla/websocket GitHub](https://github.com/gorilla/websocket)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
