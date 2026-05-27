# 03 - Network I/O

소켓 프로그래밍과 I/O 멀티플렉싱을 배웁니다. 블로킹/논블로킹 I/O의 차이를 이해하고 epoll로 대량 연결을 처리하는 방법을 체험합니다.

## 소크라테스 질문

실습을 시작하기 전에 다음 질문들을 생각해보세요.

### 질문 1: 블로킹 read()에서 데이터가 없으면 무슨 일이?

> **힌트**: 소켓에서 read()를 호출했는데 상대방이 아직 데이터를 보내지 않았다면?
>
> 생각해볼 점:
> - 스레드는 어떤 상태가 되나요?
> - CPU를 사용하고 있을까요?
> - 언제 깨어나나요?

### 질문 2: 10,000개 연결을 1개 스레드로 처리할 수 있을까?

> **힌트**: C10K 문제
>
> 생각해볼 점:
> - 연결당 스레드를 만들면 어떤 문제가 생길까요?
> - 스레드 없이 여러 연결을 처리하려면?
> - "준비된" 연결만 처리하면 어떨까요?

### 질문 3: epoll이 select보다 빠른 진짜 이유는?

> **힌트**: 시간 복잡도를 생각해보세요.
>
> 생각해볼 점:
> - select는 매번 모든 fd를 검사해야 합니다
> - epoll은 "준비된 fd만" 반환합니다
> - 이벤트 기반 vs 폴링 기반

### 질문 4: HTTP와 WebSocket은 같은 TCP 소켓인데, 왜 HTTP가 대규모에서 유리한가?

> **힌트**: fd의 수명을 생각해보세요.
>
> 생각해볼 점:
> - HTTP 요청 처리 후 fd는 어떻게 되나요?
> - WebSocket 연결 중 fd는 어떻게 되나요?
> - 10만 동시 사용자를 처리하려면 fd가 몇 개 필요할까요?

## 참고 문서

- [04_System_Calls.md](../../docs/04_System_Calls.md) - 소켓 시스템 콜
- [05_Go_System_Integration.md](../../docs/05_Go_System_Integration.md) - Go netpoll

## 실습 단계

### Step 1: 원시 소켓 API

**목표**: 시스템 콜로 직접 TCP 서버/클라이언트 구현

**위치**: `step1_socket_basic/main.go`

**핵심 개념**:
- `socket()` - 소켓 생성
- `bind()` - 주소 바인딩
- `listen()` - 연결 대기
- `accept()` - 연결 수락
- `connect()` - 연결 요청

**검증 방법**:
```bash
# 터미널 1: 서버
go run main.go server

# 터미널 2: 클라이언트
go run main.go client

# strace로 시스템 콜 확인
strace -e socket,bind,listen,accept,connect,read,write go run main.go server
```

---

### Step 2: 블로킹 vs 논블로킹 I/O

**목표**: 논블로킹 소켓의 동작 이해

**위치**: `step2_blocking_nonblock/main.go`

**핵심 개념**:
- `O_NONBLOCK` 플래그
- `EAGAIN` / `EWOULDBLOCK` 에러
- 폴링 루프의 CPU 낭비

**검증 방법**:
```bash
# 블로킹 모드 실행
go run main.go blocking

# 논블로킹 모드 실행
go run main.go nonblocking

# CPU 사용률 관찰
top -d 1
```

---

### Step 3: epoll 멀티플렉싱

**목표**: epoll로 다중 연결을 효율적으로 처리

**위치**: `step3_epoll/main.go`

**핵심 개념**:
- `epoll_create1()` - epoll 인스턴스 생성
- `epoll_ctl()` - fd 등록/수정/삭제
- `epoll_wait()` - 이벤트 대기
- Edge-triggered vs Level-triggered

**검증 방법**:
```bash
# 서버 실행
go run main.go

# 다른 터미널에서 여러 클라이언트 연결
for i in {1..100}; do nc localhost 8080 & done

# epoll 시스템 콜 확인
strace -e epoll_create1,epoll_ctl,epoll_wait go run main.go
```

---

### Step 4: HTTP vs WebSocket - 소켓 레벨 심층 분석

**목표**: 동일한 TCP 소켓인데 왜 HTTP가 대규모 환경에서 더 효율적인지 이해

**위치**: `step4_http_vs_websocket/LEARN.md`

**핵심 개념**:
- 커널 vs 유저 공간에서의 프로토콜 해석
- fd 수명 관리 (HTTP: 순환, WebSocket: 고정)
- 무상태성(Stateless)이 스케일링에 유리한 이유
- Go 표준 라이브러리와 시스템 콜의 관계

**검증 방법**:
```bash
# fd 사용량 비교 실험
watch -n 1 'ls -la /proc/$(pgrep -f "go run")/fd | wc -l'

# HTTP vs WebSocket 시스템 콜 비교
strace -e socket,accept,read,write,close go run main.go http
strace -e socket,accept,read,write,close go run main.go websocket
```

## 완료 체크리스트

- [ ] Step 1: 원시 소켓 API로 서버/클라이언트 통신 성공
- [ ] Step 1: strace로 socket, bind, listen, accept 확인
- [ ] Step 2: 블로킹 vs 논블로킹 차이 이해
- [ ] Step 2: EAGAIN 에러 확인
- [ ] Step 3: epoll로 다중 연결 처리 성공
- [ ] Step 3: epoll_wait가 준비된 fd만 반환하는 것 확인
- [ ] Step 4: HTTP vs WebSocket fd 수명 차이 이해
- [ ] Step 4: 무상태성이 스케일링에 유리한 이유 설명 가능
- [ ] 소크라테스 질문 4개 모두 답변 가능

## TCP 연결 식별: 4-Tuple

### 왜 100개 연결 중 특정 클라이언트에게만 보낼 수 있나?

TCP 연결은 **4-Tuple**로 고유하게 식별됩니다. 커널은 이 4가지 정보를 조합하여 패킷을 올바른 소켓(fd)으로 라우팅합니다.

```
4-Tuple = (ServerIP, ServerPort, ClientIP, ClientPort)
```

예시:
```
연결1: (192.168.1.100, 8080, 10.0.0.50, 52341)  → fd=5
연결2: (192.168.1.100, 8080, 10.0.0.50, 52342)  → fd=6
연결3: (192.168.1.100, 8080, 10.0.0.51, 49200)  → fd=7
```

**동일한 클라이언트 IP**에서 여러 연결이 가능한 이유는 **Client Port(Ephemeral Port)가 다르기 때문**입니다.

### Go에서 4-Tuple 확인

```go
package main

import (
    "log"
    "net"
    "syscall"
)

func main() {
    listener, _ := net.Listen("tcp", ":8080")
    log.Println("Listen Socket 생성:", listener.Addr())

    for {
        conn, _ := listener.Accept()

        // 4-Tuple 정보
        localAddr := conn.LocalAddr().(*net.TCPAddr)
        remoteAddr := conn.RemoteAddr().(*net.TCPAddr)

        log.Printf("새 연결 - 4-Tuple:")
        log.Printf("  Server: %s:%d", localAddr.IP, localAddr.Port)
        log.Printf("  Client: %s:%d", remoteAddr.IP, remoteAddr.Port)

        // 커널 fd 확인 (syscall 레벨)
        file, _ := conn.(*net.TCPConn).File()
        log.Printf("  fd: %d", file.Fd())

        go handleClient(conn)
    }
}
```

### Ephemeral Port (임시 포트)

클라이언트가 `connect()`를 호출하면, 커널이 **자동으로 사용 가능한 포트를 할당**합니다.

| OS | 범위 | 확인 명령 |
|----|------|----------|
| Linux | 32768 - 60999 | `cat /proc/sys/net/ipv4/ip_local_port_range` |
| Windows | 49152 - 65535 | `netsh int ipv4 show dynamicport tcp` |
| macOS | 49152 - 65535 | `sysctl net.inet.ip.portrange` |

**Go 클라이언트에서 Ephemeral Port 확인**:
```go
conn, _ := net.Dial("tcp", "server:8080")
localAddr := conn.LocalAddr().(*net.TCPAddr)
log.Printf("할당된 클라이언트 포트: %d", localAddr.Port)
// 출력 예: "할당된 클라이언트 포트: 52341"
```

### Listen Socket vs Connection Socket

```
                    ┌─────────────────┐
                    │  Listen Socket  │ fd=3
                    │  :8080에서 대기  │
                    └────────┬────────┘
                             │ accept()
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │ Conn Socket │   │ Conn Socket │   │ Conn Socket │
    │    fd=5     │   │    fd=6     │   │    fd=7     │
    │ 클라이언트A  │   │ 클라이언트B  │   │ 클라이언트C  │
    └─────────────┘   └─────────────┘   └─────────────┘
```

**시스템 콜 흐름**:
```go
// 1. Listen Socket 생성
fd, _ := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)
syscall.Bind(fd, &addr)
syscall.Listen(fd, 128)  // backlog=128

// 2. accept() 호출 시 새 Connection Socket 생성
for {
    connFd, clientAddr, _ := syscall.Accept(fd)
    // connFd는 새로운 fd, 이 연결 전용
    // clientAddr에 클라이언트의 IP:Port 정보

    go func(cfd int) {
        buf := make([]byte, 1024)
        n, _ := syscall.Read(cfd, buf)  // 이 클라이언트에서만 읽기
        syscall.Write(cfd, buf[:n])     // 이 클라이언트에게만 쓰기
        syscall.Close(cfd)
    }(connFd)
}
```

### 패킷 라우팅 과정

패킷이 도착했을 때 커널이 올바른 소켓을 찾는 과정:

```
패킷 도착 (dst=192.168.1.100:8080, src=10.0.0.50:52341)
           │
           ▼
┌─────────────────────────────────────────┐
│           커널 TCP 스택                  │
│  ┌─────────────────────────────────┐    │
│  │       연결 해시 테이블 검색        │    │
│  │  key: (ServerIP, ServerPort,    │    │
│  │        ClientIP, ClientPort)    │    │
│  └─────────────────────────────────┘    │
│                  │                      │
│                  ▼                      │
│  hash(192.168.1.100, 8080,              │
│       10.0.0.50, 52341) → bucket[42]    │
│                  │                      │
│                  ▼                      │
│         fd=5 소켓의 수신 버퍼에 적재      │
└─────────────────────────────────────────┘
           │
           ▼
    애플리케이션 read(fd=5)로 데이터 수신
```

커널은 **해시 테이블**을 사용하여 O(1) 시간에 올바른 소켓을 찾습니다. 그래서 수천 개의 연결이 있어도 패킷 라우팅이 빠릅니다.

---

## 핵심 인사이트

(실습 완료 후 작성하세요)

1. 블로킹 I/O의 문제점은...
2. epoll의 핵심 원리는...
3. Edge-triggered와 Level-triggered의 차이는...
4. 4-Tuple로 연결을 식별하는 이유는...
5. Ephemeral Port가 필요한 이유는...
