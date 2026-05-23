// Page Cache 효과 측정
// Kafka가 JVM Heap 대신 OS Page Cache를 사용하는 이유를 직접 체험
package main

import (
	"crypto/rand"
	"fmt"
	"os"
	"runtime"
	"time"
)

const (
	// 테스트 파일 크기: 200MB
	fileSize = 200 * 1024 * 1024
	// 읽기 반복 횟수
	readIterations = 5
	// 버퍼 크기
	bufferSize = 64 * 1024 // 64KB
)

func main() {
	fmt.Println("=================================================")
	fmt.Println("  Page Cache 효과 측정")
	fmt.Println("  (Kafka가 OS Page Cache를 활용하는 이유)")
	fmt.Println("=================================================")
	fmt.Println()

	// 시스템 정보 출력
	printSystemInfo()

	// 1. 테스트 파일 생성
	testFile := createTestFile()
	defer os.Remove(testFile)

	// 2. Cold Read (Page Cache 없음)
	fmt.Println("❄️  Cold Read 테스트 (Page Cache 미사용)...")
	coldDuration := benchmarkColdRead(testFile)

	// 3. Warm Read (Page Cache 사용)
	fmt.Println("🔥 Warm Read 테스트 (Page Cache 사용)...")
	warmDuration := benchmarkWarmRead(testFile)

	// 4. 반복 읽기 (캐시 공유 효과)
	fmt.Println("🔄 반복 읽기 테스트 (다중 Consumer 시뮬레이션)...")
	repeatDurations := benchmarkRepeatedReads(testFile)

	// 5. 결과 출력
	printResults(coldDuration, warmDuration, repeatDurations)
}

// printSystemInfo 시스템 정보 출력
func printSystemInfo() {
	fmt.Printf("📊 시스템 정보:\n")
	fmt.Printf("   - OS: %s\n", runtime.GOOS)
	fmt.Printf("   - Architecture: %s\n", runtime.GOARCH)
	fmt.Printf("   - CPUs: %d\n", runtime.NumCPU())

	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	fmt.Printf("   - Go Heap Alloc: %.2f MB\n", float64(m.Alloc)/(1024*1024))
	fmt.Printf("   - Go Heap Sys: %.2f MB\n", float64(m.Sys)/(1024*1024))
	fmt.Println()
}

// createTestFile 테스트용 파일 생성
func createTestFile() string {
	fmt.Printf("📁 테스트 파일 생성 중 (%d MB)...\n", fileSize/(1024*1024))

	file, err := os.CreateTemp("", "pagecache_benchmark_*.dat")
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

	// 디스크에 확실히 쓰기
	file.Sync()

	fmt.Printf("✅ 파일 생성 완료: %s\n\n", file.Name())
	return file.Name()
}

// dropPageCache Page Cache 무효화 시도 (권한 필요)
func dropPageCache() {
	// macOS/Linux에서 Page Cache를 drop하려면 root 권한 필요
	// 여기서는 시뮬레이션을 위해 다른 방법 사용

	// 큰 더미 데이터를 읽어서 캐시 밀어내기
	dummyFile, err := os.CreateTemp("", "dummy_*.dat")
	if err != nil {
		return
	}
	defer os.Remove(dummyFile.Name())
	defer dummyFile.Close()

	// 500MB 더미 데이터 생성 및 읽기로 캐시 밀어내기
	dummyData := make([]byte, 1024*1024)
	for i := 0; i < 500; i++ {
		rand.Read(dummyData)
		dummyFile.Write(dummyData)
	}
	dummyFile.Sync()

	// 다시 읽어서 캐시 교체
	dummyFile.Seek(0, 0)
	for i := 0; i < 500; i++ {
		dummyFile.Read(dummyData)
	}
}

// benchmarkColdRead Page Cache가 비어있을 때 읽기
func benchmarkColdRead(filename string) time.Duration {
	// Page Cache 비우기 시도
	dropPageCache()

	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	buffer := make([]byte, bufferSize)
	totalRead := 0

	start := time.Now()

	for {
		n, err := file.Read(buffer)
		if err != nil {
			break
		}
		totalRead += n
	}

	duration := time.Since(start)

	fmt.Printf("   - 읽은 크기: %.2f MB\n", float64(totalRead)/(1024*1024))
	fmt.Printf("   - 소요 시간: %v\n", duration)
	fmt.Printf("   - 처리량: %.2f MB/s\n\n", float64(totalRead)/(1024*1024)/duration.Seconds())

	return duration
}

// benchmarkWarmRead Page Cache에 데이터가 있을 때 읽기
func benchmarkWarmRead(filename string) time.Duration {
	// 먼저 한 번 읽어서 Page Cache에 로드
	file, _ := os.Open(filename)
	buffer := make([]byte, bufferSize)
	for {
		_, err := file.Read(buffer)
		if err != nil {
			break
		}
	}
	file.Close()

	// 실제 측정
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	totalRead := 0

	start := time.Now()

	for {
		n, err := file.Read(buffer)
		if err != nil {
			break
		}
		totalRead += n
	}

	duration := time.Since(start)

	fmt.Printf("   - 읽은 크기: %.2f MB\n", float64(totalRead)/(1024*1024))
	fmt.Printf("   - 소요 시간: %v\n", duration)
	fmt.Printf("   - 처리량: %.2f MB/s\n\n", float64(totalRead)/(1024*1024)/duration.Seconds())

	return duration
}

// benchmarkRepeatedReads 여러 번 반복 읽기 (다중 Consumer 시뮬레이션)
func benchmarkRepeatedReads(filename string) []time.Duration {
	durations := make([]time.Duration, readIterations)
	buffer := make([]byte, bufferSize)

	for i := 0; i < readIterations; i++ {
		file, _ := os.Open(filename)
		totalRead := 0

		start := time.Now()

		for {
			n, err := file.Read(buffer)
			if err != nil {
				break
			}
			totalRead += n
		}

		duration := time.Since(start)
		durations[i] = duration
		file.Close()

		fmt.Printf("   - 반복 %d: %v (%.2f MB/s)\n",
			i+1, duration, float64(totalRead)/(1024*1024)/duration.Seconds())
	}
	fmt.Println()

	return durations
}

// printResults 결과 비교 출력
func printResults(coldDuration, warmDuration time.Duration, repeatDurations []time.Duration) {
	cacheSpeedup := float64(coldDuration) / float64(warmDuration)

	// 반복 읽기 평균
	var totalRepeat time.Duration
	for _, d := range repeatDurations {
		totalRepeat += d
	}
	avgRepeat := totalRepeat / time.Duration(len(repeatDurations))

	fmt.Println("=================================================")
	fmt.Println("  📊 결과 비교")
	fmt.Println("=================================================")
	fmt.Printf("  Cold Read (디스크):     %v\n", coldDuration)
	fmt.Printf("  Warm Read (캐시):       %v\n", warmDuration)
	fmt.Printf("  반복 읽기 평균:         %v\n", avgRepeat)
	fmt.Printf("  ------------------------------------------\n")
	fmt.Printf("  🏆 Page Cache로 %.2fx 더 빠름!\n", cacheSpeedup)
	fmt.Println("=================================================")
	fmt.Println()

	printKafkaPageCacheExplanation()
	printMemoryUsageComparison()
}

// printKafkaPageCacheExplanation Kafka Page Cache 설명
func printKafkaPageCacheExplanation() {
	fmt.Println("💡 Kafka가 Page Cache를 활용하는 이유:")
	fmt.Println()
	fmt.Println("  1️⃣  GC 없음")
	fmt.Println("      - JVM Heap에 캐싱하면 GC 시 Stop-the-World 발생")
	fmt.Println("      - Page Cache는 OS 영역이므로 JVM GC 대상 아님")
	fmt.Println("      - Latency 스파이크 방지")
	fmt.Println()
	fmt.Println("  2️⃣  JVM 재시작해도 캐시 유지")
	fmt.Println("      - Page Cache는 OS 레벨에서 관리")
	fmt.Println("      - Kafka 프로세스 재시작해도 캐시 유효")
	fmt.Println("      - 빠른 웜업 없이 즉시 고성능 서빙")
	fmt.Println()
	fmt.Println("  3️⃣  OS가 자동 관리")
	fmt.Println("      - LRU(Least Recently Used) 자동 적용")
	fmt.Println("      - Read-ahead로 다음 데이터 미리 로드")
	fmt.Println("      - 개발자가 캐시 관리 로직 작성 불필요")
	fmt.Println()
	fmt.Println("  4️⃣  여러 Consumer가 캐시 공유")
	fmt.Println("      - Consumer A가 읽은 데이터를 Consumer B도 캐시에서 읽음")
	fmt.Println("      - 디스크 I/O 최소화")
	fmt.Println()
}

// printMemoryUsageComparison 메모리 사용 비교
func printMemoryUsageComparison() {
	fmt.Println("📊 Kafka 권장 메모리 구조 (32GB RAM 예시):")
	fmt.Println()
	fmt.Println("  ┌────────────────────────────────────────┐")
	fmt.Println("  │  커널 영역         │ ~1GB              │")
	fmt.Println("  ├────────────────────┼───────────────────┤")
	fmt.Println("  │  JVM Heap          │ ~6GB (작게!)      │")
	fmt.Println("  ├────────────────────┼───────────────────┤")
	fmt.Println("  │  Page Cache ⭐     │ ~25GB (크게!)     │")
	fmt.Println("  └────────────────────┴───────────────────┘")
	fmt.Println()
	fmt.Println("  💡 Kafka는 JVM Heap을 작게 유지하고")
	fmt.Println("     Page Cache를 최대한 활용합니다!")
	fmt.Println()
	fmt.Println("  확인 방법 (Linux):")
	fmt.Println("  $ free -h")
	fmt.Println("  $ cat /proc/meminfo | grep -E '^(Cached|Buffers)'")
	fmt.Println()
}

// simulateMultipleConsumers 다중 Consumer 시뮬레이션
func simulateMultipleConsumers(filename string) {
	fmt.Println("\n🔄 다중 Consumer 시뮬레이션")
	fmt.Println("   (동일 데이터를 여러 Consumer가 읽을 때)")
	fmt.Println()

	// 먼저 파일을 Page Cache에 로드
	file, _ := os.Open(filename)
	buffer := make([]byte, bufferSize)
	for {
		_, err := file.Read(buffer)
		if err != nil {
			break
		}
	}
	file.Close()

	// 5개의 "Consumer"가 동시에 읽기
	numConsumers := 5
	results := make(chan struct {
		id       int
		duration time.Duration
	}, numConsumers)

	for i := 0; i < numConsumers; i++ {
		go func(consumerID int) {
			file, _ := os.Open(filename)
			defer file.Close()

			buf := make([]byte, bufferSize)
			start := time.Now()

			for {
				_, err := file.Read(buf)
				if err != nil {
					break
				}
			}

			results <- struct {
				id       int
				duration time.Duration
			}{consumerID, time.Since(start)}
		}(i)
	}

	// 결과 수집
	for i := 0; i < numConsumers; i++ {
		r := <-results
		fmt.Printf("   Consumer %d: %v\n", r.id, r.duration)
	}

	fmt.Println()
	fmt.Println("   💡 모든 Consumer가 Page Cache를 공유하므로")
	fmt.Println("      디스크 I/O 없이 빠르게 읽을 수 있습니다!")
}
