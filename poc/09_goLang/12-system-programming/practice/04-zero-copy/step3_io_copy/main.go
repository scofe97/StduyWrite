package main

import (
	"fmt"
	"io"
	"net"
	"os"
	"time"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = io.Copy

// Step 3: Go io.Copy의 내부 동작
//
// 목표: io.Copy가 자동으로 sendfile을 사용하는지 확인합니다.
// Go의 투명한 최적화를 이해합니다.
//
// 실행:
//   터미널 1: go run main.go server-iocopy
//   터미널 2: go run main.go server-manual
//   터미널 3: go run main.go client
//
// 검증:
//   strace -e sendfile,read,write go run main.go server-iocopy
//   strace -e sendfile,read,write go run main.go server-manual

const (
	ioCopyAddr = "localhost:9003"
	manualAddr = "localhost:9004"
	testFile   = "/tmp/largefile"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("사용법: go run main.go [server-iocopy|server-manual|client-iocopy|client-manual]")
		return
	}

	ensureTestFile()

	switch os.Args[1] {
	case "server-iocopy":
		runIoCopyServer()
	case "server-manual":
		runManualServer()
	case "client-iocopy":
		runClient(ioCopyAddr)
	case "client-manual":
		runClient(manualAddr)
	default:
		fmt.Println("알 수 없는 모드")
	}
}

// ----------------------------------------
// io.Copy 방식 (Go가 자동 최적화)
// ----------------------------------------

func runIoCopyServer() {
	fmt.Println("=== io.Copy 서버 ===")
	fmt.Println("(Go의 자동 최적화 확인)")

	listener, err := net.Listen("tcp", ioCopyAddr)
	if err != nil {
		fmt.Printf("Listen 실패: %v\n", err)
		return
	}
	defer listener.Close()
	fmt.Printf("서버 시작: %s\n", ioCopyAddr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleWithIoCopy(conn)
	}
}

func handleWithIoCopy(conn net.Conn) {
	defer conn.Close()

	file, err := os.Open(testFile)
	if err != nil {
		fmt.Printf("파일 열기 실패: %v\n", err)
		return
	}
	defer file.Close()

	fileInfo, _ := file.Stat()
	fmt.Printf("io.Copy로 전송: %s (%d bytes)\n", testFile, fileInfo.Size())

	// ----------------------------------------
	// TODO 1: io.Copy 사용
	// ----------------------------------------
	// io.Copy(dst, src)는 내부적으로:
	// 1. dst가 ReaderFrom을 구현하면 dst.ReadFrom(src) 호출
	// 2. src가 WriterTo를 구현하면 src.WriteTo(dst) 호출
	// 3. 둘 다 아니면 버퍼를 사용한 일반 복사
	//
	// net.TCPConn.ReadFrom()은 src가 *os.File이면 sendfile 사용!

	start := time.Now()

	// n, err := io.Copy(conn, file)
	// if err != nil {
	// 	fmt.Printf("io.Copy 실패: %v\n", err)
	// 	return
	// }

	fmt.Println("(TODO: io.Copy 구현)")
	var n int64

	elapsed := time.Since(start)
	fmt.Printf("전송 완료: %d bytes in %v\n", n, elapsed)

	// strace로 확인하면 sendfile 호출이 보일 것입니다!
	fmt.Println(`
strace로 확인해보세요:
  strace -e sendfile,read,write go run main.go server-iocopy

예상 결과:
  sendfile(4, 3, [...], ...) = ...
  (read/write 대신 sendfile이 호출됨)
`)
}

// ----------------------------------------
// 수동 버퍼 복사 방식 (최적화 없음)
// ----------------------------------------

func runManualServer() {
	fmt.Println("=== 수동 복사 서버 ===")
	fmt.Println("(버퍼를 통한 전통적인 방식)")

	listener, err := net.Listen("tcp", manualAddr)
	if err != nil {
		fmt.Printf("Listen 실패: %v\n", err)
		return
	}
	defer listener.Close()
	fmt.Printf("서버 시작: %s\n", manualAddr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleWithManualCopy(conn)
	}
}

func handleWithManualCopy(conn net.Conn) {
	defer conn.Close()

	file, err := os.Open(testFile)
	if err != nil {
		fmt.Printf("파일 열기 실패: %v\n", err)
		return
	}
	defer file.Close()

	fileInfo, _ := file.Stat()
	fmt.Printf("수동 복사로 전송: %s (%d bytes)\n", testFile, fileInfo.Size())

	// ----------------------------------------
	// TODO 2: 수동 버퍼 복사
	// ----------------------------------------
	// io.Copy 대신 직접 버퍼를 통해 복사
	// 이 방식은 sendfile을 사용하지 않음

	buf := make([]byte, 32*1024)
	var total int64

	start := time.Now()

	// for {
	// 	n, readErr := file.Read(buf)
	// 	if n > 0 {
	// 		written, writeErr := conn.Write(buf[:n])
	// 		total += int64(written)
	// 		if writeErr != nil {
	// 			break
	// 		}
	// 	}
	// 	if readErr != nil {
	// 		break
	// 	}
	// }

	fmt.Println("(TODO: 수동 복사 구현)")
	_ = buf

	elapsed := time.Since(start)
	fmt.Printf("전송 완료: %d bytes in %v\n", total, elapsed)

	fmt.Println(`
strace로 확인해보세요:
  strace -e sendfile,read,write go run main.go server-manual

예상 결과:
  read(3, ..., 32768) = ...
  write(4, ..., ...) = ...
  (sendfile 대신 read/write 반복)
`)
}

func runClient(addr string) {
	fmt.Printf("=== 클라이언트 (연결: %s) ===\n", addr)

	conn, err := net.Dial("tcp", addr)
	if err != nil {
		fmt.Printf("연결 실패: %v\n", err)
		return
	}
	defer conn.Close()

	buf := make([]byte, 32*1024)
	var total int64
	start := time.Now()

	for {
		n, err := conn.Read(buf)
		if err != nil {
			break
		}
		total += int64(n)
	}

	elapsed := time.Since(start)
	fmt.Printf("수신 완료: %d bytes in %v\n", total, elapsed)
}

func ensureTestFile() {
	if _, err := os.Stat(testFile); os.IsNotExist(err) {
		fmt.Printf("테스트 파일 생성: %s (10MB)\n", testFile)
		f, _ := os.Create(testFile)
		defer f.Close()
		buf := make([]byte, 1024*1024)
		for i := 0; i < 10; i++ {
			f.Write(buf)
		}
	}
}

// ----------------------------------------
// Go의 투명한 최적화 설명
// ----------------------------------------

func goOptimizationExplanation() {
	fmt.Println(`
Go의 io.Copy 최적화 원리:

1. 인터페이스 체크
   if wt, ok := src.(WriterTo); ok {
       return wt.WriteTo(dst)
   }
   if rt, ok := dst.(ReaderFrom); ok {
       return rt.ReadFrom(src)
   }

2. net.TCPConn.ReadFrom() 구현 (src가 *os.File일 때)
   - Linux: sendfile() 시스템 콜 사용
   - macOS: sendfile() 또는 splice() 사용
   - Windows: TransmitFile() 사용

3. 개발자 관점
   - io.Copy(conn, file)만 호출
   - Go 런타임이 자동으로 최적의 방법 선택
   - 명시적인 sendfile 호출 불필요

투명한 최적화의 장점:
   - 코드가 간단하고 읽기 쉬움
   - 플랫폼 간 이식성
   - Go 버전 업그레이드로 자동 최적화 개선

주의사항:
   - 최적화가 적용되는 조건을 알아야 함
   - 특수한 경우 수동 최적화가 필요할 수 있음
   - 성능 측정으로 실제 동작 확인 필요
`)
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. io.Copy가 sendfile을 사용하는 조건
//    - src: *os.File
//    - dst: *net.TCPConn
//    - 둘 다 만족해야 sendfile 사용
//
// 2. 최적화가 적용되지 않는 경우
//    - src가 io.Reader인 경우 (파일이 아님)
//    - dst가 io.Writer인 경우 (소켓이 아님)
//    - 래핑된 Reader/Writer (bufio 등)
//
// 3. 확인 방법
//    - strace로 시스템 콜 확인
//    - 벤치마크로 성능 비교
//
// 4. 실무에서의 선택
//    - 대부분: io.Copy 사용 (충분히 빠름)
//    - 극한 성능: unix.Sendfile 직접 사용
