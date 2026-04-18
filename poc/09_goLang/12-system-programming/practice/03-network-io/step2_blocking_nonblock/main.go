//go:build linux

package main

import (
	"fmt"
	"os"
	"time"

	"golang.org/x/sys/unix"
)

// Step 2: 블로킹 vs 논블로킹 I/O
//
// 목표: 블로킹과 논블로킹 I/O의 차이를 체험합니다.
// 논블로킹 소켓에서 EAGAIN 에러를 직접 확인합니다.
//
// 실행:
//   go run main.go blocking
//   go run main.go nonblocking
//
// 검증: top으로 CPU 사용률 관찰

const port = 8081

func main() {
	if len(os.Args) < 2 {
		fmt.Println("사용법: go run main.go [blocking|nonblocking]")
		return
	}

	mode := os.Args[1]
	switch mode {
	case "blocking":
		runBlockingServer()
	case "nonblocking":
		runNonBlockingServer()
	default:
		fmt.Println("알 수 없는 모드:", mode)
	}
}

func runBlockingServer() {
	fmt.Println("=== 블로킹 서버 ===")

	serverFd, err := createServer(port, false) // blocking
	if err != nil {
		fmt.Printf("서버 생성 실패: %v\n", err)
		return
	}
	defer unix.Close(serverFd)

	fmt.Printf("블로킹 서버 시작: 포트 %d\n", port)
	fmt.Println("다른 터미널에서: nc localhost", port)

	// ----------------------------------------
	// 블로킹 Accept
	// ----------------------------------------
	// accept()는 연결이 올 때까지 스레드를 블록합니다
	// 이 동안 스레드는 SLEEPING 상태 (CPU 사용 없음)

	fmt.Println("\n클라이언트 연결 대기 중... (블로킹)")
	fmt.Println("(이 상태에서 스레드는 CPU를 사용하지 않습니다)")

	clientFd, _, err := unix.Accept(serverFd)
	if err != nil {
		fmt.Printf("Accept 실패: %v\n", err)
		return
	}
	defer unix.Close(clientFd)
	fmt.Println("클라이언트 연결됨!")

	// ----------------------------------------
	// 블로킹 Read
	// ----------------------------------------
	// read()도 데이터가 올 때까지 블록합니다

	fmt.Println("\n데이터 대기 중... (블로킹)")
	buf := make([]byte, 1024)
	n, err := unix.Read(clientFd, buf)
	if err != nil {
		fmt.Printf("Read 실패: %v\n", err)
		return
	}
	fmt.Printf("수신됨 (%d bytes): %s\n", n, string(buf[:n]))
}

func runNonBlockingServer() {
	fmt.Println("=== 논블로킹 서버 ===")

	serverFd, err := createServer(port, true) // nonblocking
	if err != nil {
		fmt.Printf("서버 생성 실패: %v\n", err)
		return
	}
	defer unix.Close(serverFd)

	fmt.Printf("논블로킹 서버 시작: 포트 %d\n", port)
	fmt.Println("다른 터미널에서: nc localhost", port)

	// ----------------------------------------
	// 논블로킹 Accept (폴링)
	// ----------------------------------------
	// TODO 1: 논블로킹 Accept 구현
	// 힌트:
	// - 논블로킹이면 연결이 없을 때 EAGAIN 에러 발생
	// - EAGAIN = "나중에 다시 시도하세요"
	// - 폴링 루프로 계속 확인해야 함

	fmt.Println("\n논블로킹 Accept 폴링 시작...")
	fmt.Println("(CPU 사용률을 관찰해보세요 - 높을 것입니다!)")

	var clientFd int
	pollCount := 0

	// for {
	// 	clientFd, _, err = unix.Accept(serverFd)
	// 	if err != nil {
	// 		// EAGAIN = 아직 연결 없음
	// 		if err == unix.EAGAIN || err == unix.EWOULDBLOCK {
	// 			pollCount++
	// 			if pollCount%100000 == 0 {
	// 				fmt.Printf("폴링 횟수: %d (아직 연결 없음)\n", pollCount)
	// 			}
	// 			continue  // 바로 다시 시도 (CPU 낭비!)
	// 		}
	// 		fmt.Printf("Accept 실패: %v\n", err)
	// 		return
	// 	}
	// 	break  // 연결 성공
	// }

	fmt.Println("(TODO: 논블로킹 Accept 구현)")
	clientFd = 4 // 임시값
	_ = pollCount

	fmt.Printf("클라이언트 연결됨! (fd: %d)\n", clientFd)

	// ----------------------------------------
	// TODO 2: 논블로킹 소켓으로 변환
	// ----------------------------------------
	// 힌트:
	// - 새로 accept된 소켓도 논블로킹으로 설정해야 함
	// - unix.SetNonblock(fd, true)

	// unix.SetNonblock(clientFd, true)

	// ----------------------------------------
	// 논블로킹 Read (폴링)
	// ----------------------------------------
	// TODO 3: 논블로킹 Read 구현
	// 힌트: Accept와 동일한 패턴

	fmt.Println("\n논블로킹 Read 폴링 시작...")

	buf := make([]byte, 1024)
	// var n int
	// pollCount = 0

	// for {
	// 	n, err = unix.Read(clientFd, buf)
	// 	if err != nil {
	// 		if err == unix.EAGAIN || err == unix.EWOULDBLOCK {
	// 			pollCount++
	// 			if pollCount%100000 == 0 {
	// 				fmt.Printf("Read 폴링 횟수: %d\n", pollCount)
	// 			}
	// 			continue
	// 		}
	// 		fmt.Printf("Read 실패: %v\n", err)
	// 		return
	// 	}
	// 	break
	// }
	// fmt.Printf("수신됨 (%d bytes): %s\n", n, string(buf[:n]))

	fmt.Println("(TODO: 논블로킹 Read 구현)")
	_ = buf

	// unix.Close(clientFd)
}

// createServer는 TCP 서버 소켓을 생성합니다.
func createServer(port int, nonblock bool) (int, error) {
	// ----------------------------------------
	// TODO 4: 서버 소켓 생성
	// ----------------------------------------
	// 힌트:
	// - nonblock=true이면 unix.SOCK_NONBLOCK 추가
	// - unix.Socket(domain, typ|unix.SOCK_NONBLOCK, proto)

	flags := unix.SOCK_STREAM
	if nonblock {
		flags |= unix.SOCK_NONBLOCK
	}

	serverFd, err := unix.Socket(unix.AF_INET, flags, 0)
	if err != nil {
		return -1, fmt.Errorf("socket: %w", err)
	}

	// SO_REUSEADDR 설정
	unix.SetsockoptInt(serverFd, unix.SOL_SOCKET, unix.SO_REUSEADDR, 1)

	// 바인드
	addr := &unix.SockaddrInet4{Port: port, Addr: [4]byte{127, 0, 0, 1}}
	if err := unix.Bind(serverFd, addr); err != nil {
		unix.Close(serverFd)
		return -1, fmt.Errorf("bind: %w", err)
	}

	// 리슨
	if err := unix.Listen(serverFd, 10); err != nil {
		unix.Close(serverFd)
		return -1, fmt.Errorf("listen: %w", err)
	}

	return serverFd, nil
}

// ----------------------------------------
// Part 3: 폴링의 문제점 해결
// ----------------------------------------
// 위의 논블로킹 폴링은 CPU를 100% 사용합니다.
// 이를 해결하는 방법들:

func improvedPolling() {
	// 방법 1: sleep 추가 (단순하지만 레이턴시 증가)
	// for {
	// 	_, _, err := unix.Accept(serverFd)
	// 	if err == unix.EAGAIN {
	// 		time.Sleep(10 * time.Millisecond)  // CPU 낭비 감소
	// 		continue
	// 	}
	// }
	_ = time.Sleep

	// 방법 2: select/poll/epoll 사용 (다음 Step에서!)
	// - fd가 "준비"될 때까지 효율적으로 대기
	// - CPU를 낭비하지 않음
	// - 여러 fd를 동시에 모니터링 가능
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. 블로킹 I/O의 장점과 단점
//    장점: 코드가 간단, CPU 낭비 없음
//    단점: 하나의 연결만 처리 가능 (다중 연결하려면 스레드 필요)
//
// 2. 논블로킹 폴링의 문제
//    - CPU 100% 사용 (busy waiting)
//    - 레이턴시: sleep 사용하면 응답 지연
//
// 3. 해결책: I/O 멀티플렉싱
//    - select(): 제한된 fd 개수
//    - poll(): fd 개수 제한 없음, 하지만 O(n) 검사
//    - epoll(): O(1) 이벤트 통지, Linux 전용
//
// 4. Go의 접근법
//    - 논블로킹 소켓 + epoll + 고루틴
//    - 개발자는 블로킹처럼 코딩, 런타임이 논블로킹으로 처리
