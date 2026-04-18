package main

import (
	"flag"
	"fmt"
	"io"
	"net"
	"runtime"
	"sync"
	"sync/atomic"
	"time"
)

// Step 3: 성능 벤치마크
//
// 목표: GOMAXPROCS와 연결 수에 따른 성능을 측정합니다.
// Go의 네트워크 성능 특성을 이해합니다.
//
// 실행:
//   GOMAXPROCS=1 go run main.go
//   GOMAXPROCS=2 go run main.go
//   GOMAXPROCS=4 go run main.go
//
// 또는:
//   go run main.go -connections=1000 -duration=10s

var (
	numConnections = flag.Int("connections", 100, "동시 연결 수")
	duration       = flag.Duration("duration", 5*time.Second, "벤치마크 지속 시간")
	messageSize    = flag.Int("msgsize", 1024, "메시지 크기 (bytes)")
)

const serverAddr = "localhost:9007"

// 통계
var (
	totalMessages   int64
	totalBytes      int64
	activeConns     int64
	benchmarkActive int32
)

func main() {
	flag.Parse()

	fmt.Println("=== Go 네트워크 성능 벤치마크 ===")
	fmt.Printf("GOMAXPROCS: %d\n", runtime.GOMAXPROCS(0))
	fmt.Printf("동시 연결 수: %d\n", *numConnections)
	fmt.Printf("메시지 크기: %d bytes\n", *messageSize)
	fmt.Printf("지속 시간: %v\n", *duration)
	fmt.Println()

	// 서버 시작
	go runServer()
	time.Sleep(100 * time.Millisecond)

	// 벤치마크 실행
	runBenchmark()
}

func runServer() {
	listener, err := net.Listen("tcp", serverAddr)
	if err != nil {
		fmt.Printf("Listen 실패: %v\n", err)
		return
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleEcho(conn)
	}
}

func handleEcho(conn net.Conn) {
	defer conn.Close()

	buf := make([]byte, 4096)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			return
		}
		_, err = conn.Write(buf[:n])
		if err != nil {
			return
		}
	}
}

func runBenchmark() {
	// ----------------------------------------
	// TODO 1: 벤치마크 클라이언트 시작
	// ----------------------------------------
	atomic.StoreInt32(&benchmarkActive, 1)

	var wg sync.WaitGroup

	fmt.Printf("%d개의 클라이언트 연결 중...\n", *numConnections)

	for i := 0; i < *numConnections; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			runBenchmarkClient()
		}()
	}

	// 진행 상황 모니터링
	go monitorProgress()

	// 지정된 시간 동안 실행
	time.Sleep(*duration)

	// 벤치마크 종료
	atomic.StoreInt32(&benchmarkActive, 0)
	fmt.Println("\n\n벤치마크 종료 중...")

	// 클라이언트들이 종료될 때까지 대기
	done := make(chan struct{})
	go func() {
		wg.Wait()
		close(done)
	}()

	select {
	case <-done:
	case <-time.After(2 * time.Second):
		fmt.Println("일부 클라이언트가 아직 실행 중...")
	}

	// ----------------------------------------
	// TODO 2: 결과 출력
	// ----------------------------------------
	printResults()
}

func runBenchmarkClient() {
	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		return
	}
	defer conn.Close()

	atomic.AddInt64(&activeConns, 1)
	defer atomic.AddInt64(&activeConns, -1)

	msg := make([]byte, *messageSize)
	buf := make([]byte, *messageSize)

	for atomic.LoadInt32(&benchmarkActive) == 1 {
		// 메시지 전송
		_, err := conn.Write(msg)
		if err != nil {
			return
		}

		// 응답 수신
		_, err = io.ReadFull(conn, buf)
		if err != nil {
			return
		}

		atomic.AddInt64(&totalMessages, 1)
		atomic.AddInt64(&totalBytes, int64(*messageSize*2)) // 송신 + 수신
	}
}

func monitorProgress() {
	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	var lastMessages int64
	var lastBytes int64
	lastTime := time.Now()

	for range ticker.C {
		if atomic.LoadInt32(&benchmarkActive) == 0 {
			return
		}

		now := time.Now()
		elapsed := now.Sub(lastTime).Seconds()

		currentMessages := atomic.LoadInt64(&totalMessages)
		currentBytes := atomic.LoadInt64(&totalBytes)

		msgPerSec := float64(currentMessages-lastMessages) / elapsed
		mbPerSec := float64(currentBytes-lastBytes) / elapsed / 1024 / 1024

		fmt.Printf("\r[진행] 연결: %d, 메시지/초: %.0f, 처리량: %.2f MB/s, 고루틴: %d",
			atomic.LoadInt64(&activeConns),
			msgPerSec,
			mbPerSec,
			runtime.NumGoroutine())

		lastMessages = currentMessages
		lastBytes = currentBytes
		lastTime = now
	}
}

func printResults() {
	fmt.Println("\n")
	fmt.Println("=" + "=")
	fmt.Println("벤치마크 결과")
	fmt.Println("=" + "=")

	messages := atomic.LoadInt64(&totalMessages)
	bytes := atomic.LoadInt64(&totalBytes)
	durationSec := duration.Seconds()

	fmt.Printf("총 메시지 수: %d\n", messages)
	fmt.Printf("총 전송량: %.2f MB\n", float64(bytes)/1024/1024)
	fmt.Printf("평균 메시지/초: %.0f\n", float64(messages)/durationSec)
	fmt.Printf("평균 처리량: %.2f MB/s\n", float64(bytes)/durationSec/1024/1024)
	fmt.Printf("연결당 메시지/초: %.0f\n", float64(messages)/durationSec/float64(*numConnections))

	fmt.Println()
	fmt.Println("환경 정보:")
	fmt.Printf("  GOMAXPROCS: %d\n", runtime.GOMAXPROCS(0))
	fmt.Printf("  NumCPU: %d\n", runtime.NumCPU())
	fmt.Printf("  동시 연결 수: %d\n", *numConnections)
	fmt.Printf("  메시지 크기: %d bytes\n", *messageSize)
}

// ----------------------------------------
// 벤치마크 실험 가이드
// ----------------------------------------

func benchmarkGuide() {
	fmt.Println(`
벤치마크 실험 가이드:

1. GOMAXPROCS 영향 테스트
   GOMAXPROCS=1 go run main.go -connections=100
   GOMAXPROCS=2 go run main.go -connections=100
   GOMAXPROCS=4 go run main.go -connections=100

   예상 결과:
   - I/O bound 워크로드에서는 GOMAXPROCS 증가 효과 제한적
   - CPU bound 워크로드에서는 선형에 가깝게 증가

2. 연결 수 영향 테스트
   go run main.go -connections=10
   go run main.go -connections=100
   go run main.go -connections=1000

   예상 결과:
   - 연결 수 증가에 따른 총 처리량 변화
   - 연결당 처리량 감소 (컨텍스트 스위치 오버헤드)

3. 메시지 크기 영향 테스트
   go run main.go -msgsize=64
   go run main.go -msgsize=1024
   go run main.go -msgsize=65536

   예상 결과:
   - 작은 메시지: 메시지/초 높음, MB/s 낮음
   - 큰 메시지: 메시지/초 낮음, MB/s 높음

4. 최대 연결 수 테스트
   ulimit -n 100000  # fd 제한 증가
   go run main.go -connections=10000

   주의:
   - 시스템 리소스 고갈 주의
   - ulimit 확인 필요
`)
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. GOMAXPROCS=1에서도 높은 처리량이 나오는 이유
//    - 네트워크 I/O는 대부분 대기 시간
//    - CPU 시간은 상대적으로 적음
//    - epoll이 효율적으로 이벤트 처리
//
// 2. GOMAXPROCS 증가의 효과
//    - 암호화/압축 등 CPU 작업이 있으면 효과적
//    - 순수 I/O만 하면 효과 제한적
//    - 스케줄링 오버헤드가 증가할 수도 있음
//
// 3. 연결 수 증가의 영향
//    - 고루틴 생성/관리 오버헤드
//    - 스케줄러 부하 증가
//    - 메모리 사용량 증가
//    - 하지만 스레드 방식보다 훨씬 적은 오버헤드
//
// 4. 실무에서의 튜닝
//    - 워크로드 특성 파악 (CPU bound vs I/O bound)
//    - 적절한 GOMAXPROCS 설정
//    - 연결 풀링 고려
//    - 프로파일링으로 병목점 확인
