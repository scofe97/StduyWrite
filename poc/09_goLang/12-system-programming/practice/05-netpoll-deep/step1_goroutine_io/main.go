package main

import (
	"fmt"
	"io"
	"net"
	"runtime"
	"sync"
	"sync/atomic"
	"time"
)

// Step 1: 고루틴 I/O의 실제 동작
//
// 목표: Go가 블로킹 API를 논블로킹으로 구현하는 방식을 이해합니다.
// GOMAXPROCS=1에서도 수천 개의 연결을 처리할 수 있는 원리를 체험합니다.
//
// 실행:
//   GOMAXPROCS=1 go run main.go
//   (다른 터미널에서 클라이언트 연결)
//
// 검증:
//   GODEBUG=schedtrace=1000 go run main.go

const (
	serverAddr      = "localhost:9005"
	numClients      = 100 // 동시 연결 수
	messageInterval = 100 * time.Millisecond
)

var (
	activeConnections int64
	messagesReceived  int64
)

func main() {
	fmt.Println("=== 고루틴 I/O 동작 확인 ===")
	fmt.Printf("GOMAXPROCS: %d\n", runtime.GOMAXPROCS(0))
	fmt.Printf("NumCPU: %d\n", runtime.NumCPU())

	// ----------------------------------------
	// Part 1: 서버 시작
	// ----------------------------------------
	go runServer()
	time.Sleep(100 * time.Millisecond) // 서버 시작 대기

	// ----------------------------------------
	// Part 2: 다수의 클라이언트 연결
	// ----------------------------------------
	fmt.Printf("\n%d개의 클라이언트 연결 시작...\n", numClients)

	var wg sync.WaitGroup
	for i := 0; i < numClients; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			runClient(id)
		}(i)
	}

	// ----------------------------------------
	// Part 3: 상태 모니터링
	// ----------------------------------------
	go monitorStatus()

	// 일정 시간 후 종료
	time.Sleep(5 * time.Second)
	fmt.Println("\n테스트 완료")

	fmt.Printf("최종 통계:\n")
	fmt.Printf("  활성 연결: %d\n", atomic.LoadInt64(&activeConnections))
	fmt.Printf("  처리된 메시지: %d\n", atomic.LoadInt64(&messagesReceived))
}

func runServer() {
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
			continue
		}

		// ----------------------------------------
		// TODO 1: 연결당 고루틴 생성
		// ----------------------------------------
		// 핵심: 각 연결마다 고루틴이 생성되어 처리
		// GOMAXPROCS=1이어도 모든 연결이 처리됨!
		// 왜? I/O 대기 중인 고루틴은 OS 스레드를 점유하지 않음

		go handleClient(conn)
	}
}

func handleClient(conn net.Conn) {
	defer conn.Close()

	atomic.AddInt64(&activeConnections, 1)
	defer atomic.AddInt64(&activeConnections, -1)

	buf := make([]byte, 1024)

	for {
		// ----------------------------------------
		// TODO 2: 블로킹처럼 보이는 Read
		// ----------------------------------------
		// conn.Read()는 블로킹처럼 보이지만:
		// 1. 내부적으로 소켓은 논블로킹으로 설정됨
		// 2. 데이터가 없으면 고루틴이 "파킹"됨
		// 3. OS 스레드는 다른 고루틴 실행
		// 4. 데이터 도착 시 netpoll이 고루틴 깨움

		n, err := conn.Read(buf)
		if err != nil {
			if err != io.EOF {
				// 에러 무시 (연결 종료)
			}
			return
		}

		atomic.AddInt64(&messagesReceived, 1)

		// 에코 응답
		conn.Write(buf[:n])
	}
}

func runClient(id int) {
	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		return
	}
	defer conn.Close()

	// 주기적으로 메시지 전송
	for i := 0; i < 10; i++ {
		msg := fmt.Sprintf("Client %d, message %d", id, i)
		conn.Write([]byte(msg))

		// 응답 읽기
		buf := make([]byte, 1024)
		conn.SetReadDeadline(time.Now().Add(time.Second))
		conn.Read(buf)

		time.Sleep(messageInterval)
	}
}

func monitorStatus() {
	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	for range ticker.C {
		var memStats runtime.MemStats
		runtime.ReadMemStats(&memStats)

		fmt.Printf("\r[상태] 연결: %d, 메시지: %d, 고루틴: %d, 힙: %dMB",
			atomic.LoadInt64(&activeConnections),
			atomic.LoadInt64(&messagesReceived),
			runtime.NumGoroutine(),
			memStats.Alloc/1024/1024)
	}
}

// ----------------------------------------
// Go netpoll의 동작 원리
// ----------------------------------------

func netpollExplanation() {
	fmt.Println(`
Go netpoll의 동작 원리:

1. 소켓 생성 시
   - 소켓이 논블로킹으로 설정됨
   - 소켓 fd가 epoll에 등록됨

2. conn.Read() 호출 시
   a. read() 시스템 콜 시도
   b. 데이터가 있으면 → 즉시 반환
   c. EAGAIN이면 (데이터 없음) →
      - 현재 고루틴을 "파킹" (waiting 상태)
      - fd를 epoll에 등록 (아직 안 했다면)
      - OS 스레드는 다른 고루틴 실행

3. 데이터 도착 시
   a. epoll_wait()가 fd가 읽기 가능함을 감지
   b. netpoll이 해당 fd를 기다리는 고루틴을 찾음
   c. 고루틴을 "언파킹" (runnable 상태)
   d. 스케줄러가 고루틴을 실행

핵심 포인트:
   - 개발자: 블로킹 코드처럼 작성
   - 런타임: 논블로킹으로 처리
   - 결과: 적은 스레드로 많은 연결 처리
`)
}

// ----------------------------------------
// GODEBUG=schedtrace 출력 해석
// ----------------------------------------

func schedtraceExplanation() {
	fmt.Println(`
GODEBUG=schedtrace=1000 출력 예시:

SCHED 1000ms: gomaxprocs=1 idleprocs=0 threads=3 spinningthreads=0
  idlethreads=1 runqueue=0 [0]

해석:
  - gomaxprocs=1: 사용 중인 P(프로세서) 수
  - idleprocs=0: 유휴 P 수
  - threads=3: 총 OS 스레드 수
  - runqueue=0: 전역 실행 큐의 고루틴 수
  - [0]: 각 P의 로컬 실행 큐 크기

관찰 포인트:
  - GOMAXPROCS=1이어도 여러 연결 처리 가능
  - threads는 GOMAXPROCS보다 클 수 있음 (CGO, 블로킹 syscall)
  - runqueue가 계속 0이면 I/O bound 워크로드
`)
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. 왜 GOMAXPROCS=1에서도 100개 연결을 처리할 수 있나요?
//    - I/O 대기 중인 고루틴은 OS 스레드를 차지하지 않음
//    - netpoll이 데이터 도착 시 고루틴 깨움
//
// 2. 고루틴 수가 연결 수와 같은 이유는?
//    - 연결당 고루틴 패턴 (goroutine per connection)
//    - C10K 문제를 해결하는 Go의 방식
//
// 3. 메모리 사용량이 적은 이유는?
//    - 고루틴 스택: 2KB 시작 (스레드: 1MB)
//    - 필요시 자동 증가
//
// 4. CPU 사용률이 낮은 이유는?
//    - I/O bound 워크로드
//    - 대부분의 시간을 epoll_wait에서 대기
