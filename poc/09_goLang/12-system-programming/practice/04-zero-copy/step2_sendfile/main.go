package main

import (
	"fmt"
	"net"
	"os"
	"time"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.Sendfile

// Step 2: sendfile 시스템 콜
//
// 목표: sendfile을 사용하여 유저 공간 복사를 제거합니다.
//
// 준비:
//   dd if=/dev/urandom of=/tmp/largefile bs=1M count=100
//
// 실행:
//   터미널 1: go run main.go server
//   터미널 2: go run main.go client
//
// 검증: strace -e sendfile,read,write go run main.go server

const (
	serverAddr = "localhost:9002"
	testFile   = "/tmp/largefile"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("사용법: go run main.go [server|client]")
		return
	}

	ensureTestFile()

	switch os.Args[1] {
	case "server":
		runServer()
	case "client":
		runClient()
	default:
		fmt.Println("알 수 없는 모드")
	}
}

func runServer() {
	fmt.Println("=== sendfile 파일 전송 서버 ===")
	fmt.Println("(Zero-copy 방식)")

	listener, err := net.Listen("tcp", serverAddr)
	if err != nil {
		fmt.Printf("Listen 실패: %v\n", err)
		return
	}
	defer listener.Close()
	fmt.Printf("서버 시작: %s\n", serverAddr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Printf("Accept 실패: %v\n", err)
			continue
		}
		fmt.Printf("클라이언트 연결: %s\n", conn.RemoteAddr())

		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	// ----------------------------------------
	// Part 1: 소켓 fd 추출
	// ----------------------------------------
	// sendfile은 fd를 직접 사용하므로 net.Conn에서 fd 추출 필요

	tcpConn, ok := conn.(*net.TCPConn)
	if !ok {
		fmt.Println("TCPConn이 아닙니다")
		return
	}

	// RawConn으로 fd 접근
	rawConn, err := tcpConn.SyscallConn()
	if err != nil {
		fmt.Printf("RawConn 획득 실패: %v\n", err)
		return
	}

	var socketFd int
	rawConn.Control(func(fd uintptr) {
		socketFd = int(fd)
	})

	fmt.Printf("소켓 fd: %d\n", socketFd)

	// ----------------------------------------
	// Part 2: 파일 열기
	// ----------------------------------------
	file, err := os.Open(testFile)
	if err != nil {
		fmt.Printf("파일 열기 실패: %v\n", err)
		return
	}
	defer file.Close()

	fileInfo, _ := file.Stat()
	fileSize := fileInfo.Size()
	fileFd := int(file.Fd())

	fmt.Printf("전송할 파일: %s (%d bytes, fd: %d)\n", testFile, fileSize, fileFd)

	// ----------------------------------------
	// TODO 1: sendfile로 전송
	// ----------------------------------------
	// 힌트:
	// unix.Sendfile(outfd, infd, offset *int64, count int) (written int, err error)
	// - outfd: 출력 fd (소켓)
	// - infd: 입력 fd (파일)
	// - offset: 파일 내 시작 위치 (nil이면 현재 위치)
	// - count: 전송할 바이트 수

	start := time.Now()
	var totalSent int64

	// offset := int64(0)
	// remaining := fileSize
	//
	// for remaining > 0 {
	// 	// sendfile은 한 번에 전송할 수 있는 양이 제한될 수 있음
	// 	toSend := int(remaining)
	// 	if toSend > 1024*1024 { // 1MB씩 전송
	// 		toSend = 1024 * 1024
	// 	}
	//
	// 	n, err := unix.Sendfile(socketFd, fileFd, &offset, toSend)
	// 	if err != nil {
	// 		fmt.Printf("Sendfile 실패: %v\n", err)
	// 		break
	// 	}
	//
	// 	totalSent += int64(n)
	// 	remaining -= int64(n)
	// }

	fmt.Println("(TODO: sendfile 구현)")
	_ = socketFd
	_ = fileFd
	_ = fileSize

	elapsed := time.Since(start)
	fmt.Printf("전송 완료: %d bytes in %v\n", totalSent, elapsed)
	if elapsed.Seconds() > 0 {
		fmt.Printf("처리량: %.2f MB/s\n", float64(totalSent)/elapsed.Seconds()/1024/1024)
	}

	// ----------------------------------------
	// sendfile의 데이터 경로
	// ----------------------------------------
	fmt.Println(`
sendfile의 데이터 경로:

sendfile(socket_fd, file_fd, offset, count)

[디스크] --DMA--> [커널 버퍼] --직접전송--> [소켓 버퍼] --DMA--> [NIC]

총 복사 횟수:
   - DMA 복사: 2회 (디스크→커널, 소켓→NIC)
   - CPU 복사: 0~1회 (커널 내 scatter-gather 지원 시 0회)

장점:
   - 유저 공간 복사 제거
   - 컨텍스트 스위치 감소
   - CPU 사용률 감소
   - 메모리 대역폭 절약

제약사항:
   - infd는 mmap 가능한 파일이어야 함
   - outfd는 소켓이어야 함 (Linux 2.6.33 이후 완화)
   - 파일 내용을 수정할 수 없음
`)
}

func runClient() {
	fmt.Println("=== 파일 수신 클라이언트 ===")

	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		fmt.Printf("연결 실패: %v\n", err)
		return
	}
	defer conn.Close()

	buf := make([]byte, 32*1024)
	var totalReceived int64

	start := time.Now()

	for {
		n, err := conn.Read(buf)
		if err != nil {
			break
		}
		totalReceived += int64(n)
	}

	elapsed := time.Since(start)
	fmt.Printf("수신 완료: %d bytes in %v\n", totalReceived, elapsed)
	if elapsed.Seconds() > 0 {
		fmt.Printf("처리량: %.2f MB/s\n", float64(totalReceived)/elapsed.Seconds()/1024/1024)
	}
}

func ensureTestFile() {
	if _, err := os.Stat(testFile); os.IsNotExist(err) {
		fmt.Printf("테스트 파일 생성 중: %s (10MB)\n", testFile)
		f, _ := os.Create(testFile)
		defer f.Close()
		buf := make([]byte, 1024*1024)
		for i := 0; i < 10; i++ {
			f.Write(buf)
		}
	}
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. sendfile vs read+write 성능 비교
//    - strace로 시스템 콜 횟수 비교
//    - 처리량(throughput) 비교
//    - CPU 사용률 비교 (top으로 확인)
//
// 2. sendfile의 한계
//    - 파일을 수정하면서 전송할 수 없음
//    - 암호화/압축이 필요하면 사용 불가
//
// 3. 다른 Zero-copy 기법
//    - splice(): 파이프를 통한 커널 내 전송
//    - vmsplice(): 유저 버퍼를 파이프에 매핑
//    - copy_file_range(): 파일 간 커널 내 복사
