package main

import (
	"fmt"
	"time"
)

// 과제: 기본 워커 풀 구현
//
// 목표:
// 1. 고정된 수의 워커가 작업 큐에서 작업을 처리
// 2. 채널을 사용한 작업 분배와 결과 수집
//
// TODO: 아래 코드를 완성하세요

// worker는 jobs 채널에서 작업을 받아 처리하고 results 채널로 결과를 보냅니다
func worker(id int, jobs <-chan int, results chan<- int) {
	// TODO: jobs 채널에서 작업을 range로 읽기
	// for job := range jobs {
	//     fmt.Printf("Worker %d: 작업 %d 처리 중...\n", id, job)
	//     time.Sleep(500 * time.Millisecond)  // 작업 시뮬레이션
	//     results <- job * 2  // 결과 전송
	// }
}

func main() {
	numJobs := 9
	numWorkers := 3

	// TODO 1: jobs 채널 생성 (버퍼 크기: numJobs)
	// jobs := make(chan int, numJobs)

	// TODO 2: results 채널 생성 (버퍼 크기: numJobs)
	// results := make(chan int, numJobs)

	// TODO 3: 워커 시작
	// for w := 1; w <= numWorkers; w++ {
	//     go worker(w, jobs, results)
	// }

	// TODO 4: 작업 전송
	// for j := 1; j <= numJobs; j++ {
	//     jobs <- j
	// }
	// close(jobs)  // 더 이상 작업 없음

	// TODO 5: 결과 수집
	// for a := 1; a <= numJobs; a++ {
	//     result := <-results
	//     fmt.Printf("결과: %d\n", result)
	// }

	fmt.Println("모든 작업 완료!")
}

// 예상 출력 (순서는 다를 수 있음):
// Worker 1: 작업 1 처리 중...
// Worker 2: 작업 2 처리 중...
// Worker 3: 작업 3 처리 중...
// 결과: 2
// Worker 1: 작업 4 처리 중...
// ...
// 모든 작업 완료!
