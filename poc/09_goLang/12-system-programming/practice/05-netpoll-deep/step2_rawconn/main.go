package main

import (
	"fmt"
	"net"
	"time"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.IPPROTO_TCP

// Step 2: RawConn으로 저수준 소켓 제어
//
// 목표: Go의 net 패키지와 raw 시스템 콜을 혼합하여 사용합니다.
// 소켓 옵션 설정, 저수준 I/O 등 세밀한 제어가 필요할 때 사용합니다.
//
// 실행: go run main.go
// 검증: strace -e setsockopt,getsockopt go run main.go

const serverAddr = "localhost:9006"

func main() {
	fmt.Println("=== RawConn으로 저수준 소켓 제어 ===")

	// ----------------------------------------
	// Part 1: 서버 소켓 생성 및 RawConn 획득
	// ----------------------------------------
	listener, err := net.Listen("tcp", serverAddr)
	if err != nil {
		fmt.Printf("Listen 실패: %v\n", err)
		return
	}
	defer listener.Close()

	// TCPListener에서 RawConn 획득
	tcpListener, ok := listener.(*net.TCPListener)
	if !ok {
		fmt.Println("TCPListener가 아닙니다")
		return
	}

	rawListener, err := tcpListener.SyscallConn()
	if err != nil {
		fmt.Printf("RawConn 획득 실패: %v\n", err)
		return
	}

	// ----------------------------------------
	// TODO 1: Control()로 소켓 옵션 설정
	// ----------------------------------------
	// Control(func(fd uintptr))은 fd에 직접 접근하여
	// 시스템 콜을 호출할 수 있게 합니다.

	// rawListener.Control(func(fd uintptr) {
	// 	// SO_REUSEPORT 설정 (여러 프로세스가 같은 포트 바인드)
	// 	err := unix.SetsockoptInt(int(fd), unix.SOL_SOCKET, unix.SO_REUSEPORT, 1)
	// 	if err != nil {
	// 		fmt.Printf("SO_REUSEPORT 설정 실패: %v\n", err)
	// 	} else {
	// 		fmt.Println("SO_REUSEPORT 설정 성공")
	// 	}
	// })

	fmt.Println("(TODO: Control()로 소켓 옵션 설정)")
	_ = rawListener

	fmt.Printf("서버 시작: %s\n", serverAddr)

	// ----------------------------------------
	// Part 2: 클라이언트 연결 대기
	// ----------------------------------------
	go func() {
		time.Sleep(100 * time.Millisecond)
		runClient()
	}()

	conn, err := listener.Accept()
	if err != nil {
		fmt.Printf("Accept 실패: %v\n", err)
		return
	}
	defer conn.Close()

	fmt.Printf("클라이언트 연결: %s\n", conn.RemoteAddr())

	// ----------------------------------------
	// Part 3: TCPConn의 RawConn
	// ----------------------------------------
	tcpConn, ok := conn.(*net.TCPConn)
	if !ok {
		fmt.Println("TCPConn이 아닙니다")
		return
	}

	rawConn, err := tcpConn.SyscallConn()
	if err != nil {
		fmt.Printf("RawConn 획득 실패: %v\n", err)
		return
	}

	// ----------------------------------------
	// TODO 2: 소켓 정보 조회
	// ----------------------------------------
	// rawConn.Control(func(fd uintptr) {
	// 	// TCP_NODELAY 상태 확인
	// 	val, err := unix.GetsockoptInt(int(fd), unix.IPPROTO_TCP, unix.TCP_NODELAY)
	// 	if err == nil {
	// 		fmt.Printf("TCP_NODELAY: %d\n", val)
	// 	}
	//
	// 	// SO_SNDBUF 확인
	// 	sndbuf, err := unix.GetsockoptInt(int(fd), unix.SOL_SOCKET, unix.SO_SNDBUF)
	// 	if err == nil {
	// 		fmt.Printf("SO_SNDBUF: %d bytes\n", sndbuf)
	// 	}
	//
	// 	// SO_RCVBUF 확인
	// 	rcvbuf, err := unix.GetsockoptInt(int(fd), unix.SOL_SOCKET, unix.SO_RCVBUF)
	// 	if err == nil {
	// 		fmt.Printf("SO_RCVBUF: %d bytes\n", rcvbuf)
	// 	}
	// })

	fmt.Println("(TODO: 소켓 정보 조회)")

	// ----------------------------------------
	// TODO 3: TCP_NODELAY 설정 (Nagle 알고리즘 비활성화)
	// ----------------------------------------
	// Nagle 알고리즘: 작은 패킷을 모아서 전송 (레이턴시 증가)
	// TCP_NODELAY: 즉시 전송 (저지연 필요 시)

	// rawConn.Control(func(fd uintptr) {
	// 	err := unix.SetsockoptInt(int(fd), unix.IPPROTO_TCP, unix.TCP_NODELAY, 1)
	// 	if err != nil {
	// 		fmt.Printf("TCP_NODELAY 설정 실패: %v\n", err)
	// 	} else {
	// 		fmt.Println("TCP_NODELAY 설정 성공")
	// 	}
	// })

	fmt.Println("(TODO: TCP_NODELAY 설정)")

	// ----------------------------------------
	// TODO 4: RawConn.Read()로 저수준 읽기
	// ----------------------------------------
	// Read(func(fd uintptr) bool)
	// - 반환값 true: 작업 완료
	// - 반환값 false: EAGAIN, 다시 시도 필요 (netpoll이 관리)

	buf := make([]byte, 1024)
	var n int

	// err = rawConn.Read(func(fd uintptr) bool {
	// 	var readErr error
	// 	n, readErr = unix.Read(int(fd), buf)
	// 	if readErr != nil {
	// 		if readErr == unix.EAGAIN {
	// 			return false // 다시 시도 필요
	// 		}
	// 		return true // 에러
	// 	}
	// 	return true // 성공
	// })
	// if err == nil && n > 0 {
	// 	fmt.Printf("RawConn.Read로 수신: %s\n", string(buf[:n]))
	// }

	fmt.Println("(TODO: RawConn.Read() 구현)")
	_ = rawConn
	_ = n
	_ = buf

	// ----------------------------------------
	// TODO 5: RawConn.Write()로 저수준 쓰기
	// ----------------------------------------
	response := []byte("Hello from server (via RawConn)!")

	// err = rawConn.Write(func(fd uintptr) bool {
	// 	_, writeErr := unix.Write(int(fd), response)
	// 	if writeErr != nil {
	// 		if writeErr == unix.EAGAIN {
	// 			return false
	// 		}
	// 		return true
	// 	}
	// 	return true
	// })
	// if err == nil {
	// 	fmt.Println("RawConn.Write로 전송 완료")
	// }

	fmt.Println("(TODO: RawConn.Write() 구현)")
	_ = response
}

func runClient() {
	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		fmt.Printf("클라이언트 연결 실패: %v\n", err)
		return
	}
	defer conn.Close()

	conn.Write([]byte("Hello from client!"))

	buf := make([]byte, 1024)
	n, _ := conn.Read(buf)
	if n > 0 {
		fmt.Printf("클라이언트 수신: %s\n", string(buf[:n]))
	}
}

// ----------------------------------------
// 유용한 소켓 옵션들
// ----------------------------------------

func socketOptionsExplanation() {
	fmt.Println(`
유용한 소켓 옵션들:

1. SOL_SOCKET 레벨
   - SO_REUSEADDR: TIME_WAIT 상태에서도 바인드 허용
   - SO_REUSEPORT: 여러 프로세스가 같은 포트 바인드
   - SO_SNDBUF: 송신 버퍼 크기
   - SO_RCVBUF: 수신 버퍼 크기
   - SO_KEEPALIVE: TCP keepalive 활성화

2. IPPROTO_TCP 레벨
   - TCP_NODELAY: Nagle 알고리즘 비활성화
   - TCP_KEEPIDLE: keepalive 시작 전 유휴 시간
   - TCP_KEEPINTVL: keepalive 간격
   - TCP_KEEPCNT: keepalive 최대 재시도 횟수
   - TCP_QUICKACK: 지연 ACK 비활성화

3. 언제 RawConn이 필요한가?
   - Go 표준 라이브러리가 지원하지 않는 소켓 옵션
   - 플랫폼별 특수 기능
   - 성능 튜닝
   - 저수준 프로토콜 구현
`)
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. RawConn.Read/Write의 반환값 의미
//    - true: 작업 완료 (성공 또는 에러)
//    - false: EAGAIN, netpoll이 다시 호출해줌
//
// 2. Control vs Read/Write
//    - Control: 즉시 실행, 반환값 없음
//    - Read/Write: netpoll 통합, 비동기 지원
//
// 3. Go 표준 라이브러리와의 혼합
//    - net.Conn으로 일반 작업
//    - RawConn으로 특수 작업
//    - 두 API를 혼합해서 사용 가능
