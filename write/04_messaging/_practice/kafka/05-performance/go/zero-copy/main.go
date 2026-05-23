// Zero-Copy vs Traditional Copy 성능 비교
// Kafka가 sendfile()을 사용하는 이유를 직접 체험
//
// Go에서는 io.Copy()가 내부적으로 sendfile()을 사용할 수 있음
// 이 예제에서는 두 방식의 차이를 시뮬레이션
package main

import (
	"bytes"
	"crypto/rand"
	"fmt"
	"io"
	"net"
	"os"
	"sync"
	"time"
)

const (
	// 테스트 파일 크기: 50MB
	fileSize = 50 * 1024 * 1024
	// 전송 횟수
	transferCount = 5
	// 버퍼 크기 (Traditional Copy용)
	bufferSize = 64 * 1024 // 64KB
)

func main() {
	fmt.Println("=================================================")
	fmt.Println("  Zero-Copy vs Traditional Copy 성능 비교")
	fmt.Println("  (Kafka가 sendfile()을 사용하는 이유)")
	fmt.Println("=================================================")
	fmt.Println()

	// 1. 테스트 파일 생성
	testFile := createTestFile()
	defer os.Remove(testFile)

	// 2. Traditional Copy 테스트 (User Space 경유)
	fmt.Println("📦 Traditional Copy 테스트 중...")
	fmt.Println("   (Disk → Kernel → User → Kernel → Network)")
	tradDuration := benchmarkTraditionalCopy(testFile)

	// 3. Zero-Copy 테스트 (sendfile 시뮬레이션)
	fmt.Println("🚀 Zero-Copy 테스트 중...")
	fmt.Println("   (Disk → Kernel → Network)")
	zeroDuration := benchmarkZeroCopy(testFile)

	// 4. 결과 출력
	printResults(tradDuration, zeroDuration)
}

// createTestFile 테스트용 파일 생성
func createTestFile() string {
	fmt.Printf("📁 테스트 파일 생성 중 (%d MB)...\n", fileSize/(1024*1024))

	file, err := os.CreateTemp("", "zerocopy_benchmark_*.dat")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// 랜덤 데이터로 파일 채우기
	data := make([]byte, 1024*1024) // 1MB씩
	written := 0
	for written < fileSize {
		rand.Read(data)
		n, _ := file.Write(data)
		written += n
	}

	fmt.Printf("✅ 파일 생성 완료: %s\n\n", file.Name())
	return file.Name()
}

// startServer 테스트용 TCP 서버 시작
func startServer(ready chan<- net.Listener, done <-chan struct{}) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		panic(err)
	}

	ready <- listener

	go func() {
		<-done
		listener.Close()
	}()

	for {
		conn, err := listener.Accept()
		if err != nil {
			return
		}
		go func(c net.Conn) {
			defer c.Close()
			io.Copy(io.Discard, c) // 받은 데이터 버림
		}(conn)
	}
}

// benchmarkTraditionalCopy User Space를 경유하는 전통적인 복사
func benchmarkTraditionalCopy(filename string) time.Duration {
	// 서버 시작
	ready := make(chan net.Listener)
	done := make(chan struct{})
	go startServer(ready, done)
	listener := <-ready
	defer close(done)

	var totalDuration time.Duration
	var totalBytes int64

	for i := 0; i < transferCount; i++ {
		file, _ := os.Open(filename)
		conn, _ := net.Dial("tcp", listener.Addr().String())

		// User Space 버퍼를 경유하는 복사
		buffer := make([]byte, bufferSize)
		var bytesSent int64

		start := time.Now()

		for {
			// 1. 파일 → User Buffer (Kernel → User)
			n, err := file.Read(buffer)
			if err == io.EOF {
				break
			}

			// 2. User Buffer → Socket (User → Kernel)
			written, _ := conn.Write(buffer[:n])
			bytesSent += int64(written)
		}

		duration := time.Since(start)
		totalDuration += duration
		totalBytes += bytesSent

		file.Close()
		conn.Close()
	}

	avgDuration := totalDuration / time.Duration(transferCount)
	throughput := float64(totalBytes) / (1024 * 1024) / totalDuration.Seconds()

	fmt.Printf("   - 전송 횟수: %d\n", transferCount)
	fmt.Printf("   - 총 전송량: %.2f MB\n", float64(totalBytes)/(1024*1024))
	fmt.Printf("   - 평균 시간: %v\n", avgDuration)
	fmt.Printf("   - 처리량: %.2f MB/s\n\n", throughput)

	return avgDuration
}

// benchmarkZeroCopy io.Copy를 사용한 Zero-Copy (sendfile 활용)
func benchmarkZeroCopy(filename string) time.Duration {
	// 서버 시작
	ready := make(chan net.Listener)
	done := make(chan struct{})
	go startServer(ready, done)
	listener := <-ready
	defer close(done)

	var totalDuration time.Duration
	var totalBytes int64
	var mu sync.Mutex

	for i := 0; i < transferCount; i++ {
		file, _ := os.Open(filename)
		conn, _ := net.Dial("tcp", listener.Addr().String())

		start := time.Now()

		// io.Copy는 내부적으로 sendfile() 시스템 콜 사용 가능
		// Go 런타임이 자동으로 최적화
		n, _ := io.Copy(conn, file)

		duration := time.Since(start)

		mu.Lock()
		totalDuration += duration
		totalBytes += n
		mu.Unlock()

		file.Close()
		conn.Close()
	}

	avgDuration := totalDuration / time.Duration(transferCount)
	throughput := float64(totalBytes) / (1024 * 1024) / totalDuration.Seconds()

	fmt.Printf("   - 전송 횟수: %d\n", transferCount)
	fmt.Printf("   - 총 전송량: %.2f MB\n", float64(totalBytes)/(1024*1024))
	fmt.Printf("   - 평균 시간: %v\n", avgDuration)
	fmt.Printf("   - 처리량: %.2f MB/s\n\n", throughput)

	return avgDuration
}

// printResults 결과 비교 출력
func printResults(tradDuration, zeroDuration time.Duration) {
	improvement := float64(tradDuration) / float64(zeroDuration)

	fmt.Println("=================================================")
	fmt.Println("  📊 결과 비교")
	fmt.Println("=================================================")
	fmt.Printf("  Traditional Copy: %v\n", tradDuration)
	fmt.Printf("  Zero-Copy:        %v\n", zeroDuration)
	fmt.Printf("  ------------------------------------------\n")
	fmt.Printf("  🏆 Zero-Copy가 %.2fx 더 빠름!\n", improvement)
	fmt.Println("=================================================")
	fmt.Println()
	fmt.Println("💡 Zero-Copy의 핵심 원리:")
	fmt.Println()
	fmt.Println("  [Traditional Copy - 4번 복사]")
	fmt.Println("  1. Disk → Kernel Buffer (DMA)")
	fmt.Println("  2. Kernel Buffer → User Buffer (CPU) ⚠️")
	fmt.Println("  3. User Buffer → Socket Buffer (CPU) ⚠️")
	fmt.Println("  4. Socket Buffer → NIC (DMA)")
	fmt.Println()
	fmt.Println("  [Zero-Copy - 2번 복사]")
	fmt.Println("  1. Disk → Kernel Buffer/Page Cache (DMA)")
	fmt.Println("  2. Kernel Buffer → NIC (DMA)")
	fmt.Println("  → User Space 완전 우회!")
	fmt.Println()
	fmt.Println("💡 Kafka에서의 활용:")
	fmt.Println("   - Broker가 Consumer에게 데이터 전송 시 sendfile() 사용")
	fmt.Println("   - 압축된 데이터를 해제하지 않고 그대로 전송 가능")
	fmt.Println("   - CPU 사용률 감소, Context Switch 감소")
	fmt.Println()
}

// demonstrateDataFlow 데이터 흐름 시각화 (교육용)
func demonstrateDataFlow() {
	fmt.Println("\n📚 데이터 흐름 비교 (교육용)")
	fmt.Println()

	// Traditional Copy 시각화
	traditionalFlow := []string{
		"[Disk] ──DMA──→ [Kernel Buffer]",
		"[Kernel Buffer] ──CPU──→ [User Buffer] ⚠️ Context Switch",
		"[User Buffer] ──CPU──→ [Socket Buffer] ⚠️ Context Switch",
		"[Socket Buffer] ──DMA──→ [NIC]",
	}

	fmt.Println("Traditional Copy (4-Copy):")
	for i, step := range traditionalFlow {
		fmt.Printf("  %d. %s\n", i+1, step)
	}

	fmt.Println()

	// Zero-Copy 시각화
	zeroCopyFlow := []string{
		"[Disk] ──DMA──→ [Kernel Buffer/Page Cache]",
		"[Kernel Buffer] ──DMA──→ [NIC]",
		"❌ User Space 접근 없음!",
	}

	fmt.Println("Zero-Copy (sendfile):")
	for i, step := range zeroCopyFlow {
		fmt.Printf("  %d. %s\n", i+1, step)
	}
}

// simulateMemoryCopy 메모리 복사 오버헤드 시뮬레이션
func simulateMemoryCopy() {
	fmt.Println("\n📊 메모리 복사 오버헤드 측정")

	dataSize := 100 * 1024 * 1024 // 100MB
	data := make([]byte, dataSize)
	rand.Read(data)

	// User Space 복사 시뮬레이션
	dest := make([]byte, dataSize)

	start := time.Now()
	copy(dest, data) // 메모리 간 복사
	copyDuration := time.Since(start)

	// Reader/Writer를 통한 복사
	reader := bytes.NewReader(data)
	writer := bytes.NewBuffer(nil)

	start = time.Now()
	io.Copy(writer, reader)
	ioCopyDuration := time.Since(start)

	fmt.Printf("  - 직접 메모리 복사: %v\n", copyDuration)
	fmt.Printf("  - io.Copy 사용: %v\n", ioCopyDuration)
	fmt.Printf("  - 데이터 크기: %d MB\n", dataSize/(1024*1024))
	fmt.Println()
	fmt.Println("  💡 이 복사 오버헤드가 네트워크 전송마다 발생!")
	fmt.Println("     Zero-Copy는 이 오버헤드를 제거합니다.")
}
