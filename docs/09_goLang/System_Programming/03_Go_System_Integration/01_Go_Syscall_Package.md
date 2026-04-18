# Go Syscall Package (Go syscall 패키지)

Go에서 직접 시스템 콜을 호출하는 방법을 다룹니다.

---

## 두 가지 패키지

### 1. syscall (표준 라이브러리)

```go
import "syscall"
```

- Go 표준 라이브러리에 포함
- **Deprecated**: 새 기능 추가 안 됨
- 기본적인 시스템 콜만 포함

### 2. golang.org/x/sys/unix (권장)

```go
import "golang.org/x/sys/unix"
```

- 외부 패키지 (go get 필요)
- **활발히 유지보수**
- 더 많은 시스템 콜과 상수 포함
- Linux, BSD, macOS 등 지원

```bash
go get golang.org/x/sys/unix
```

---

## 기본 사용법

### 파일 열기/읽기

```go
package main

import (
    "fmt"
    "golang.org/x/sys/unix"
)

func main() {
    // open() 시스템 콜 직접 호출
    fd, err := unix.Open("/etc/hostname", unix.O_RDONLY, 0)
    if err != nil {
        fmt.Printf("open error: %v\n", err)
        return
    }
    defer unix.Close(fd)

    // read() 시스템 콜
    buf := make([]byte, 256)
    n, err := unix.Read(fd, buf)
    if err != nil {
        fmt.Printf("read error: %v\n", err)
        return
    }

    fmt.Printf("Read %d bytes: %s\n", n, string(buf[:n]))
}
```

### os 패키지와 비교

```go
// os 패키지 사용 (권장)
file, _ := os.Open("/etc/hostname")
defer file.Close()
data, _ := io.ReadAll(file)

// syscall 직접 사용 (저수준 제어 필요 시)
fd, _ := unix.Open("/etc/hostname", unix.O_RDONLY, 0)
defer unix.Close(fd)
buf := make([]byte, 256)
n, _ := unix.Read(fd, buf)
```

**언제 syscall을 직접 사용하나?**
- os 패키지가 지원하지 않는 기능 필요 시
- 특정 플래그나 옵션 사용 시
- 성능 최적화 필요 시

---

## 자주 사용하는 시스템 콜

### 파일 관련

```go
// open
fd, err := unix.Open(path, flags, mode)

// read/write
n, err := unix.Read(fd, buf)
n, err := unix.Write(fd, buf)

// pread/pwrite (오프셋 지정)
n, err := unix.Pread(fd, buf, offset)
n, err := unix.Pwrite(fd, buf, offset)

// close
err := unix.Close(fd)

// 파일 정보
var stat unix.Stat_t
err := unix.Stat(path, &stat)
fmt.Printf("Size: %d\n", stat.Size)
```

### mmap

```go
// 파일 메모리 매핑
fd, _ := unix.Open("large_file.dat", unix.O_RDONLY, 0)
var stat unix.Stat_t
unix.Fstat(fd, &stat)

data, err := unix.Mmap(fd, 0, int(stat.Size),
    unix.PROT_READ, unix.MAP_SHARED)
if err != nil {
    panic(err)
}
defer unix.Munmap(data)

// data를 []byte로 직접 접근
fmt.Printf("First byte: %d\n", data[0])
```

### epoll (Linux 전용)

```go
// epoll 인스턴스 생성
epfd, _ := unix.EpollCreate1(0)
defer unix.Close(epfd)

// fd 등록
event := unix.EpollEvent{
    Events: unix.EPOLLIN,
    Fd:     int32(clientFd),
}
unix.EpollCtl(epfd, unix.EPOLL_CTL_ADD, clientFd, &event)

// 이벤트 대기
events := make([]unix.EpollEvent, 100)
n, _ := unix.EpollWait(epfd, events, -1)

for i := 0; i < n; i++ {
    fd := int(events[i].Fd)
    // 처리
}
```

---

## 소켓 프로그래밍

### TCP 서버 (저수준)

```go
package main

import (
    "fmt"
    "golang.org/x/sys/unix"
)

func main() {
    // socket() 생성
    fd, err := unix.Socket(unix.AF_INET, unix.SOCK_STREAM, 0)
    if err != nil {
        panic(err)
    }
    defer unix.Close(fd)

    // SO_REUSEADDR 설정
    unix.SetsockoptInt(fd, unix.SOL_SOCKET, unix.SO_REUSEADDR, 1)

    // bind()
    addr := &unix.SockaddrInet4{Port: 8080}
    copy(addr.Addr[:], []byte{0, 0, 0, 0})  // INADDR_ANY
    if err := unix.Bind(fd, addr); err != nil {
        panic(err)
    }

    // listen()
    if err := unix.Listen(fd, 128); err != nil {
        panic(err)
    }

    fmt.Println("Listening on :8080")

    for {
        // accept()
        clientFd, clientAddr, err := unix.Accept(fd)
        if err != nil {
            continue
        }

        go handleClient(clientFd, clientAddr)
    }
}

func handleClient(fd int, addr unix.Sockaddr) {
    defer unix.Close(fd)

    buf := make([]byte, 1024)
    n, _ := unix.Read(fd, buf)

    response := "HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
    unix.Write(fd, []byte(response))

    fmt.Printf("Handled request: %s\n", string(buf[:n]))
}
```

### net 패키지와 비교

```go
// net 패키지 (권장)
listener, _ := net.Listen("tcp", ":8080")
for {
    conn, _ := listener.Accept()
    go handleConn(conn)
}

// syscall 직접 사용
fd, _ := unix.Socket(unix.AF_INET, unix.SOCK_STREAM, 0)
unix.Bind(fd, &unix.SockaddrInet4{Port: 8080})
unix.Listen(fd, 128)
```

---

## sendfile 사용

```go
package main

import (
    "fmt"
    "golang.org/x/sys/unix"
)

func sendFileZeroCopy(outFd, inFd int, count int) error {
    var offset int64 = 0

    for count > 0 {
        // sendfile 시스템 콜 직접 호출
        n, err := unix.Sendfile(outFd, inFd, &offset, count)
        if err != nil {
            return err
        }
        count -= n
    }
    return nil
}

func main() {
    // 파일 열기
    fileFd, _ := unix.Open("large_video.mp4", unix.O_RDONLY, 0)
    defer unix.Close(fileFd)

    // 소켓 생성 및 연결 (생략)
    socketFd := createSocket()
    defer unix.Close(socketFd)

    // 파일 크기 확인
    var stat unix.Stat_t
    unix.Fstat(fileFd, &stat)

    // Zero-copy 전송
    err := sendFileZeroCopy(socketFd, fileFd, int(stat.Size))
    if err != nil {
        fmt.Printf("sendfile error: %v\n", err)
    }
}
```

---

## 에러 처리

### Errno

```go
n, err := unix.Read(fd, buf)
if err != nil {
    // unix.Errno 타입으로 변환
    if errno, ok := err.(unix.Errno); ok {
        switch errno {
        case unix.EAGAIN:
            // 논블로킹 소켓에서 데이터 없음
            fmt.Println("Would block, try again later")
        case unix.EINTR:
            // 시그널에 의해 중단됨
            fmt.Println("Interrupted, retry")
        default:
            fmt.Printf("Error: %v\n", errno)
        }
    }
}
```

### 주요 errno 값

| 값 | Go 상수 | 설명 |
|----|---------|------|
| EAGAIN | `unix.EAGAIN` | 리소스 일시적 불가 |
| EINTR | `unix.EINTR` | 시그널 인터럽트 |
| ENOENT | `unix.ENOENT` | 파일 없음 |
| EACCES | `unix.EACCES` | 권한 없음 |
| EBADF | `unix.EBADF` | 잘못된 fd |

---

## Syscall vs Rawconn

### RawConn 인터페이스

net 패키지의 Conn에서 저수준 fd에 접근하는 방법입니다.

```go
conn, _ := net.Dial("tcp", "example.com:80")

// RawConn 얻기
rawConn, err := conn.(*net.TCPConn).SyscallConn()
if err != nil {
    panic(err)
}

// fd에 직접 작업
rawConn.Control(func(fd uintptr) {
    // TCP_NODELAY 설정
    unix.SetsockoptInt(int(fd), unix.IPPROTO_TCP, unix.TCP_NODELAY, 1)

    // 수신 버퍼 크기 설정
    unix.SetsockoptInt(int(fd), unix.SOL_SOCKET, unix.SO_RCVBUF, 1024*1024)
})
```

**장점**: net 패키지의 편리함 + 저수준 설정

---

## 크로스 플랫폼 고려

### 빌드 태그 사용

```go
//go:build linux
// +build linux

package main

import "golang.org/x/sys/unix"

func useEpoll() {
    epfd, _ := unix.EpollCreate1(0)
    // Linux 전용 코드
}
```

```go
//go:build darwin
// +build darwin

package main

import "golang.org/x/sys/unix"

func useKqueue() {
    kq, _ := unix.Kqueue()
    // macOS/BSD 전용 코드
}
```

### OS별 상수 차이

```go
// Linux
unix.EPOLLIN
unix.EPOLL_CTL_ADD

// BSD/macOS
unix.EVFILT_READ
unix.EV_ADD
```

---

## 핵심 정리

| 개념 | 설명 |
|------|------|
| **syscall** | Go 표준 라이브러리, deprecated |
| **golang.org/x/sys/unix** | 권장되는 외부 패키지, 더 완전함 |
| **RawConn** | net.Conn에서 fd에 접근하는 인터페이스 |
| **빌드 태그** | OS별 코드 분리 |

---

## 다음 문서

→ [02_Go_Network_Internals](./02_Go_Network_Internals.md): Go net 패키지의 내부 구조
