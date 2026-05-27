package main

import (
	"fmt"
	"os"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.AF_INET

// Step 1: 원시 소켓 API로 TCP 서버/클라이언트
//
// 목표: 시스템 콜로 직접 TCP 통신을 구현합니다.
// Go의 net 패키지 대신 unix 패키지로 저수준 구현합니다.
//
// 실행:
//   터미널 1: go run main.go server
//   터미널 2: go run main.go client
//
// 검증: strace -e socket,bind,listen,accept,connect go run main.go server

const (
	serverAddr = "127.0.0.1"
	serverPort = 8080
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("사용법: go run main.go [server|client]")
		return
	}

	mode := os.Args[1]
	switch mode {
	case "server":
		runServer()
	case "client":
		runClient()
	default:
		fmt.Println("알 수 없는 모드:", mode)
	}
}

func runServer() {
	fmt.Println("=== TCP Server (원시 소켓 API) ===")

	// ----------------------------------------
	// TODO 1: 소켓 생성
	// ----------------------------------------
	// 힌트:
	// unix.Socket(domain, typ, proto) (fd int, err error)
	// - domain: unix.AF_INET (IPv4)
	// - typ: unix.SOCK_STREAM (TCP)
	// - proto: 0 (자동 선택)

	// serverFd, err := unix.Socket(unix.AF_INET, unix.SOCK_STREAM, 0)
	// if err != nil {
	// 	fmt.Printf("소켓 생성 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Close(serverFd)
	// fmt.Printf("서버 소켓 fd: %d\n", serverFd)

	fmt.Println("(TODO: 소켓 생성 구현)")
	serverFd := 3 // 임시값

	// ----------------------------------------
	// TODO 2: SO_REUSEADDR 옵션 설정 (선택)
	// ----------------------------------------
	// 힌트: 서버 재시작 시 "address already in use" 방지

	// unix.SetsockoptInt(serverFd, unix.SOL_SOCKET, unix.SO_REUSEADDR, 1)

	// ----------------------------------------
	// TODO 3: 주소 바인딩
	// ----------------------------------------
	// 힌트:
	// unix.Bind(fd, sa unix.Sockaddr) error
	// - Sockaddr 구조체를 만들어야 함

	// addr := &unix.SockaddrInet4{
	// 	Port: serverPort,
	// 	Addr: [4]byte{127, 0, 0, 1},
	// }
	// err = unix.Bind(serverFd, addr)
	// if err != nil {
	// 	fmt.Printf("바인드 실패: %v\n", err)
	// 	return
	// }
	// fmt.Printf("바인드 완료: %s:%d\n", serverAddr, serverPort)

	fmt.Println("(TODO: 주소 바인딩 구현)")

	// ----------------------------------------
	// TODO 4: 연결 대기 시작
	// ----------------------------------------
	// 힌트:
	// unix.Listen(fd, backlog) error
	// - backlog: 대기 큐 크기

	// err = unix.Listen(serverFd, 10)
	// if err != nil {
	// 	fmt.Printf("리슨 실패: %v\n", err)
	// 	return
	// }
	// fmt.Println("연결 대기 중...")

	fmt.Println("(TODO: 리슨 구현)")

	// ----------------------------------------
	// TODO 5: 연결 수락 및 처리
	// ----------------------------------------
	// 힌트:
	// unix.Accept(fd) (nfd int, sa Sockaddr, err error)
	// - nfd: 새 연결의 소켓 fd
	// - sa: 클라이언트 주소

	// for {
	// 	clientFd, clientAddr, err := unix.Accept(serverFd)
	// 	if err != nil {
	// 		fmt.Printf("Accept 실패: %v\n", err)
	// 		continue
	// 	}
	//
	// 	// 클라이언트 정보 출력
	// 	if addr, ok := clientAddr.(*unix.SockaddrInet4); ok {
	// 		fmt.Printf("클라이언트 연결: %d.%d.%d.%d:%d (fd: %d)\n",
	// 			addr.Addr[0], addr.Addr[1], addr.Addr[2], addr.Addr[3],
	// 			addr.Port, clientFd)
	// 	}
	//
	// 	// 데이터 수신
	// 	buf := make([]byte, 1024)
	// 	n, err := unix.Read(clientFd, buf)
	// 	if err != nil {
	// 		fmt.Printf("읽기 실패: %v\n", err)
	// 		unix.Close(clientFd)
	// 		continue
	// 	}
	// 	fmt.Printf("수신: %s\n", string(buf[:n]))
	//
	// 	// 응답 전송
	// 	response := []byte("Hello from server!\n")
	// 	unix.Write(clientFd, response)
	//
	// 	unix.Close(clientFd)
	// }

	fmt.Println("(TODO: Accept 루프 구현)")
	_ = serverFd
}

func runClient() {
	fmt.Println("=== TCP Client (원시 소켓 API) ===")

	// ----------------------------------------
	// TODO 6: 소켓 생성
	// ----------------------------------------
	// clientFd, err := unix.Socket(unix.AF_INET, unix.SOCK_STREAM, 0)
	// if err != nil {
	// 	fmt.Printf("소켓 생성 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Close(clientFd)

	fmt.Println("(TODO: 클라이언트 소켓 생성 구현)")
	clientFd := 3 // 임시값

	// ----------------------------------------
	// TODO 7: 서버에 연결
	// ----------------------------------------
	// 힌트:
	// unix.Connect(fd, sa) error

	// serverSockAddr := &unix.SockaddrInet4{
	// 	Port: serverPort,
	// 	Addr: [4]byte{127, 0, 0, 1},
	// }
	// err = unix.Connect(clientFd, serverSockAddr)
	// if err != nil {
	// 	fmt.Printf("연결 실패: %v\n", err)
	// 	return
	// }
	// fmt.Println("서버에 연결됨")

	fmt.Println("(TODO: Connect 구현)")

	// ----------------------------------------
	// TODO 8: 데이터 송수신
	// ----------------------------------------
	// message := []byte("Hello from client!\n")
	// unix.Write(clientFd, message)
	// fmt.Printf("전송: %s", string(message))
	//
	// buf := make([]byte, 1024)
	// n, _ := unix.Read(clientFd, buf)
	// fmt.Printf("수신: %s", string(buf[:n]))

	fmt.Println("(TODO: 데이터 송수신 구현)")
	_ = clientFd
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. socket() → bind() → listen() → accept() 순서가 왜 필요한가요?
//    - 각 단계에서 커널은 무엇을 설정하나요?
//
// 2. accept()가 새 fd를 반환하는 이유는?
//    - 서버 소켓 fd와 클라이언트 연결 fd의 역할 차이
//
// 3. SO_REUSEADDR의 역할은?
//    - TIME_WAIT 상태에 대해 알아보세요
//
// 4. net.Listen() vs unix.Socket()
//    - Go 표준 라이브러리는 어떤 추상화를 제공하나요?
