package main

import (
	"fmt"
	"net"
	"os"
	"time"
)

// Step 1: 전통적인 read + write 방식
//
// 목표: 표준 방식으로 파일을 네트워크로 전송하고 복사 횟수를 이해합니다.
//
// 준비:
//   dd if=/dev/urandom of=/tmp/largefile bs=1M count=100
//
// 실행:
//   터미널 1: go run main.go server
//   터미널 2: go run main.go client
//
// 검증: strace -e read,write go run main.go server

const (
	serverAddr = "localhost:9001"
	testFile   = "/tmp/largefile"
	bufferSize = 32 * 1024 // 32KB
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("사용법: go run main.go [server|client]")
		return
	}

	// 테스트 파일이 없으면 생성
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
	fmt.Println("=== 전통적인 파일 전송 서버 ===")
	fmt.Println("(read + write 방식)")

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
	// TODO 1: 파일 열기
	// ----------------------------------------
	file, err := os.Open(testFile)
	if err != nil {
		fmt.Printf("파일 열기 실패: %v\n", err)
		return
	}
	defer file.Close()

	fileInfo, _ := file.Stat()
	fmt.Printf("전송할 파일: %s (%d bytes)\n", testFile, fileInfo.Size())

	// ----------------------------------------
	// TODO 2: read + write로 전송
	// ----------------------------------------
	// 전통적인 방식:
	// 1. read(): 파일 → 커널 버퍼 → 유저 버퍼 (복사 1회)
	// 2. write(): 유저 버퍼 → 커널 버퍼 → 네트워크 (복사 1회)
	// 총 유저 공간 복사: 2회

	buf := make([]byte, bufferSize)
	var totalSent int64

	start := time.Now()

	// for {
	// 	// read: 파일에서 버퍼로 읽기
	// 	n, err := file.Read(buf)
	// 	if err != nil {
	// 		if err.Error() == "EOF" {
	// 			break
	// 		}
	// 		fmt.Printf("Read 실패: %v\n", err)
	// 		return
	// 	}
	//
	// 	// write: 버퍼에서 소켓으로 쓰기
	// 	written, err := conn.Write(buf[:n])
	// 	if err != nil {
	// 		fmt.Printf("Write 실패: %v\n", err)
	// 		return
	// 	}
	// 	totalSent += int64(written)
	// }

	fmt.Println("(TODO: read + write 루프 구현)")
	_ = buf

	elapsed := time.Since(start)
	fmt.Printf("전송 완료: %d bytes in %v\n", totalSent, elapsed)
	fmt.Printf("처리량: %.2f MB/s\n", float64(totalSent)/elapsed.Seconds()/1024/1024)

	// ----------------------------------------
	// 메모리 복사 경로 설명
	// ----------------------------------------
	fmt.Println(`
전통적인 read + write의 데이터 경로:

1. read() 호출:
   [디스크] --DMA--> [커널 버퍼] --CPU복사--> [유저 버퍼]

2. write() 호출:
   [유저 버퍼] --CPU복사--> [소켓 버퍼] --DMA--> [NIC]

총 복사 횟수:
   - DMA 복사: 2회 (디스크→커널, 소켓→NIC)
   - CPU 복사: 2회 (커널→유저, 유저→소켓)
   = 총 4회 복사

문제점:
   - 데이터가 유저 공간을 불필요하게 거침
   - CPU 사이클 낭비
   - 메모리 대역폭 낭비
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
	fmt.Printf("서버에 연결됨: %s\n", serverAddr)

	// 데이터 수신 (discard)
	buf := make([]byte, bufferSize)
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
	fmt.Printf("처리량: %.2f MB/s\n", float64(totalReceived)/elapsed.Seconds()/1024/1024)
}

func ensureTestFile() {
	if _, err := os.Stat(testFile); os.IsNotExist(err) {
		fmt.Printf("테스트 파일 생성 중: %s (10MB)\n", testFile)

		f, _ := os.Create(testFile)
		defer f.Close()

		// 10MB 파일 생성
		buf := make([]byte, 1024*1024)
		for i := 0; i < 10; i++ {
			f.Write(buf)
		}
		fmt.Println("테스트 파일 생성 완료")
	}
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. 버퍼 크기가 성능에 미치는 영향
//    - 버퍼가 작으면? → 시스템 콜 횟수 증가
//    - 버퍼가 크면? → 메모리 사용량 증가
//
// 2. strace 결과 분석
//    - read와 write가 얼마나 호출되나요?
//    - 각 호출당 전송되는 바이트 수는?
//
// 3. 이 방식이 적합한 경우
//    - 데이터를 유저 공간에서 처리해야 할 때
//    - 압축, 암호화 등이 필요한 경우
