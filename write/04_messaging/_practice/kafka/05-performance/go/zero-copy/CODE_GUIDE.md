# Zero-Copy 코드 가이드

## 개요
Zero-Copy와 Traditional Copy의 성능 차이를 측정하는 Go 벤치마크 코드입니다.
실제 네트워크 전송을 통해 sendfile() 시스템 콜의 효과를 체험합니다.

## 사용된 Go 문법

### 1. 네트워크 서버 생성

```go
import "net"

// TCP 리스너 생성 (포트 0 = 자동 할당)
listener, err := net.Listen("tcp", "127.0.0.1:0")

// 클라이언트 연결 수락
conn, err := listener.Accept()

// 클라이언트로 연결
conn, err := net.Dial("tcp", listener.Addr().String())
```
- `net.Listen()`: TCP 서버 리스너 생성
- `:0`: OS가 사용 가능한 포트 자동 할당
- `listener.Addr()`: 할당된 주소 확인

### 2. 채널 (Channel) - 고루틴 간 통신

```go
ready := make(chan net.Listener)  // 리스너 전달용 채널
done := make(chan struct{})        // 종료 신호용 채널

// 채널로 값 보내기
ready <- listener

// 채널에서 값 받기
listener := <-ready

// 채널 닫기 (종료 신호)
close(done)
```
- `chan T`: 타입 T를 전달하는 채널
- `struct{}`: 빈 구조체 (메모리 0바이트, 신호용)
- `<-chan`: 수신 전용, `chan<-`: 송신 전용

### 3. 고루틴 (Goroutine) - 경량 스레드

```go
// 익명 함수를 고루틴으로 실행
go func() {
    // 백그라운드 작업
}()

// 매개변수 전달
go func(c net.Conn) {
    defer c.Close()
    // c 사용
}(conn)
```
- `go`: 새 고루틴에서 함수 실행
- 클로저 변수 주의: 루프에서는 매개변수로 전달

### 4. io 패키지 - 스트림 처리

```go
import "io"

// Zero-Copy: 파일 → 네트워크 직접 전송
n, err := io.Copy(conn, file)  // dst, src 순서

// 데이터 버리기 (테스트용)
io.Copy(io.Discard, reader)
```
- `io.Copy(dst, src)`: src에서 dst로 복사
- 내부적으로 `sendfile()` 시스템 콜 사용 가능
- `io.Discard`: /dev/null과 동일

### 5. Traditional Copy - 버퍼 경유

```go
buffer := make([]byte, 64*1024)  // 64KB 버퍼

for {
    // 1. 파일 → 버퍼 (Kernel → User Space)
    n, err := file.Read(buffer)
    if err == io.EOF {
        break
    }

    // 2. 버퍼 → 소켓 (User Space → Kernel)
    conn.Write(buffer[:n])
}
```
- 슬라이스 `buffer[:n]`: 실제 읽은 만큼만 사용
- 2번의 User Space 복사 발생

### 6. sync.Mutex - 동시성 제어

```go
import "sync"

var mu sync.Mutex

mu.Lock()
totalBytes += n  // 크리티컬 섹션
mu.Unlock()
```
- `Mutex`: 상호 배제 (Mutual Exclusion)
- 여러 고루틴이 공유 변수 접근 시 필요

### 7. bytes 패키지 - 메모리 버퍼

```go
import "bytes"

// 읽기용 버퍼
reader := bytes.NewReader(data)

// 쓰기용 버퍼
writer := bytes.NewBuffer(nil)

// 복사
io.Copy(writer, reader)
```
- `bytes.Reader`: []byte를 io.Reader로 래핑
- `bytes.Buffer`: 가변 크기 바이트 버퍼

## 핵심 알고리즘

### Traditional Copy (4번 복사)
```
[Disk] ──DMA──→ [Kernel Buffer]
[Kernel Buffer] ──CPU──→ [User Buffer]    ⚠️ Context Switch
[User Buffer] ──CPU──→ [Socket Buffer]    ⚠️ Context Switch
[Socket Buffer] ──DMA──→ [NIC]
```

### Zero-Copy (2번 복사)
```
[Disk] ──DMA──→ [Kernel Buffer/Page Cache]
[Kernel Buffer] ──DMA──→ [NIC]
❌ User Space 접근 없음!
```

## 시스템 콜 확인

```bash
# macOS: dtrace로 시스템 콜 추적
sudo dtruss -c go run main.go 2>&1 | grep -E "sendfile|read|write"

# Linux: strace로 시스템 콜 추적
strace -c go run main.go 2>&1 | grep -E "sendfile|read|write"
```

## Go의 Zero-Copy 지원

```go
// Go 런타임이 자동으로 최적화
io.Copy(conn, file)

// 내부적으로 다음과 같이 동작:
// - Linux: sendfile() 또는 splice()
// - macOS: sendfile()
// - Windows: TransmitFile()
```

Go의 `io.Copy`는 소스와 목적지 타입에 따라 자동으로 최적화된 시스템 콜을 사용합니다.

## 실행 결과 해석

| 항목 | Traditional | Zero-Copy | 이유 |
|------|-------------|-----------|------|
| 복사 횟수 | 4회 | 2회 | User Space 우회 |
| Context Switch | 2회 | 0회 | Kernel 내 처리 |
| CPU 사용 | 높음 | 낮음 | DMA로 대체 |
| 메모리 대역폭 | 2배 소비 | 1배 | 복사 감소 |
