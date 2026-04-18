// Sequential I/O vs Random I/O 성능 비교 벤치마크
// Kafka가 Sequential I/O를 사용하는 이유를 직접 체험
//
// 실행 방법:
//   cd sequential-io && go run main.go
//
// 학습 포인트:
//   - Sequential I/O: 연속된 블록을 순서대로 읽음 (OS Prefetch 최적화)
//   - Random I/O: 랜덤한 위치의 블록을 읽음 (Seek 오버헤드 발생)
//   - SSD에서도 Sequential이 더 빠른 이유: FTL 매핑, Prefetch 최적화
package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
	"os"
	"time"

	"golang.org/x/sys/unix"
)

const (
	// 테스트 파일 크기: 500MB (Page Cache 영향 최소화)
	fileSize = 500 * 1024 * 1024
	// 블록 크기: 4KB (일반적인 디스크 블록 크기)
	blockSize = 4 * 1024
	// 읽기 횟수
	readCount = 50000
)

func main() {
	fmt.Println("=================================================")
	fmt.Println("  Sequential I/O vs Random I/O 성능 비교")
	fmt.Println("  (Kafka가 Sequential I/O를 선택한 이유)")
	fmt.Println("=================================================")
	fmt.Println()
	fmt.Printf("📋 테스트 설정:\n")
	fmt.Printf("   - 파일 크기: %d MB\n", fileSize/(1024*1024))
	fmt.Printf("   - 블록 크기: %d KB\n", blockSize/1024)
	fmt.Printf("   - 읽기 횟수: %d\n", readCount)
	fmt.Println()

	// 1. 테스트 파일 생성
	testFile := createTestFile()
	defer os.Remove(testFile)

	// 2. 캐시 무효화를 위해 잠시 대기
	fmt.Println("⏳ 캐시 안정화 대기 중...")
	time.Sleep(2 * time.Second)

	// 3. Random Read 먼저 (캐시 없는 상태에서)
	fmt.Println("🔀 Random Read 테스트 중...")
	randDuration, randThroughput := benchmarkRandomRead(testFile)

	// 4. Sequential Read (비교를 위해)
	fmt.Println("📖 Sequential Read 테스트 중...")
	seqDuration, seqThroughput := benchmarkSequentialRead(testFile)

	// 5. 결과 출력
	printResults(seqDuration, randDuration, seqThroughput, randThroughput)
}

// createTestFile 테스트용 파일 생성 (Direct I/O 사용)
func createTestFile() string {
	fmt.Printf("📁 테스트 파일 생성 중 (%d MB)...\n", fileSize/(1024*1024))

	file, err := os.CreateTemp("", "io_benchmark_*.dat")
	if err != nil {
		panic(err)
	}

	// macOS: F_NOCACHE로 Page Cache 우회
	unix.FcntlInt(file.Fd(), unix.F_NOCACHE, 1)

	// 랜덤 데이터로 파일 채우기
	data := make([]byte, 1024*1024) // 1MB씩 쓰기
	written := 0
	for written < fileSize {
		rand.Read(data)
		n, err := file.Write(data)
		if err != nil {
			panic(err)
		}
		written += n
	}

	file.Sync() // 디스크에 확실히 쓰기
	file.Close()

	fmt.Printf("✅ 파일 생성 완료: %s\n\n", file.Name())
	return file.Name()
}

// benchmarkSequentialRead 순차 읽기 벤치마크
func benchmarkSequentialRead(filename string) (time.Duration, float64) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// macOS: F_NOCACHE로 Page Cache 우회
	unix.FcntlInt(file.Fd(), unix.F_NOCACHE, 1)

	buffer := make([]byte, blockSize)
	totalRead := 0

	start := time.Now()

	for i := 0; i < readCount; i++ {
		n, err := file.Read(buffer)
		if err != nil {
			// EOF에 도달하면 처음으로
			file.Seek(0, 0)
			continue
		}
		totalRead += n
	}

	duration := time.Since(start)
	throughput := float64(totalRead) / (1024 * 1024) / duration.Seconds()

	fmt.Printf("   - 읽은 블록 수: %d\n", readCount)
	fmt.Printf("   - 총 읽은 크기: %.2f MB\n", float64(totalRead)/(1024*1024))
	fmt.Printf("   - 소요 시간: %v\n", duration)
	fmt.Printf("   - 처리량: %.2f MB/s\n\n", throughput)

	return duration, throughput
}

// benchmarkRandomRead 랜덤 읽기 벤치마크
func benchmarkRandomRead(filename string) (time.Duration, float64) {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// macOS: F_NOCACHE로 Page Cache 우회
	unix.FcntlInt(file.Fd(), unix.F_NOCACHE, 1)

	buffer := make([]byte, blockSize)
	totalRead := 0
	maxBlocks := int64(fileSize / blockSize)

	// 진정한 랜덤 오프셋 미리 생성 (crypto/rand 사용)
	offsets := make([]int64, readCount)
	for i := range offsets {
		n, _ := rand.Int(rand.Reader, big.NewInt(maxBlocks))
		offsets[i] = n.Int64() * blockSize
	}

	start := time.Now()

	for i := 0; i < readCount; i++ {
		// 랜덤 위치로 이동 (Seek 오버헤드 발생)
		file.Seek(offsets[i], 0)
		n, err := file.Read(buffer)
		if err != nil {
			continue
		}
		totalRead += n
	}

	duration := time.Since(start)
	throughput := float64(totalRead) / (1024 * 1024) / duration.Seconds()

	fmt.Printf("   - 읽은 블록 수: %d\n", readCount)
	fmt.Printf("   - 총 읽은 크기: %.2f MB\n", float64(totalRead)/(1024*1024))
	fmt.Printf("   - 소요 시간: %v\n", duration)
	fmt.Printf("   - 처리량: %.2f MB/s\n\n", throughput)

	return duration, throughput
}

// printResults 결과 비교 출력
func printResults(seqDuration, randDuration time.Duration, seqThroughput, randThroughput float64) {
	timeRatio := float64(randDuration) / float64(seqDuration)
	throughputRatio := seqThroughput / randThroughput

	fmt.Println("=================================================")
	fmt.Println("  📊 결과 비교")
	fmt.Println("=================================================")
	fmt.Printf("  Sequential I/O: %v (%.2f MB/s)\n", seqDuration, seqThroughput)
	fmt.Printf("  Random I/O:     %v (%.2f MB/s)\n", randDuration, randThroughput)
	fmt.Printf("  ------------------------------------------\n")
	fmt.Printf("  🏆 Sequential이 %.1fx 더 빠름!\n", timeRatio)
	fmt.Printf("  📈 처리량 비율: %.1fx\n", throughputRatio)
	fmt.Println("=================================================")
	fmt.Println()

	// SSD vs HDD 설명
	fmt.Println("💡 결과 해석:")
	fmt.Println()
	if timeRatio < 2 {
		fmt.Println("   ⚠️  SSD 환경에서는 차이가 적게 나타납니다.")
		fmt.Println("   - SSD는 Random I/O 성능이 HDD보다 10~100배 좋음")
		fmt.Println("   - 그래도 Sequential이 더 빠른 이유:")
		fmt.Println("     1. OS Prefetch/Read-ahead 최적화")
		fmt.Println("     2. SSD 내부 FTL 매핑 효율성")
		fmt.Println("     3. 연속 블록 읽기 시 버스 효율성")
	} else {
		fmt.Println("   ✅ Sequential I/O가 확실히 빠릅니다!")
	}
	fmt.Println()

	fmt.Println("📊 실제 환경에서의 차이:")
	fmt.Println("   ┌─────────────┬─────────────┬─────────────┐")
	fmt.Println("   │   환경      │ Sequential  │   Random    │")
	fmt.Println("   ├─────────────┼─────────────┼─────────────┤")
	fmt.Println("   │ HDD         │ ~100 MB/s   │ ~1 MB/s     │")
	fmt.Println("   │ SATA SSD    │ ~500 MB/s   │ ~50 MB/s    │")
	fmt.Println("   │ NVMe SSD    │ ~3000 MB/s  │ ~500 MB/s   │")
	fmt.Println("   └─────────────┴─────────────┴─────────────┘")
	fmt.Println()

	fmt.Println("💡 Kafka가 Sequential I/O를 선택한 이유:")
	fmt.Println("   1. 메시지는 Append-Only로 순차 쓰기")
	fmt.Println("   2. Consumer는 Offset 순서대로 순차 읽기")
	fmt.Println("   3. 디스크 헤드 이동 최소화 (HDD)")
	fmt.Println("   4. OS Prefetch 최적화 활용 (SSD)")
	fmt.Println("   5. 어떤 디스크에서든 Sequential이 더 빠름!")
	fmt.Println()
}
