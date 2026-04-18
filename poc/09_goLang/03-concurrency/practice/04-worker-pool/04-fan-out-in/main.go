package main

import (
	"fmt"
	"sync"
	"time"
)

// 과제: Fan-out/Fan-in 패턴
//
// 목표:
// 1. Fan-out: 하나의 입력을 여러 워커로 분산
// 2. Fan-in: 여러 워커의 결과를 하나로 합치기
//
// TODO: 아래 코드를 완성하세요

// producer는 숫자를 생성하여 채널로 보냅니다
func producer(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		for _, n := range nums {
			out <- n
		}
		close(out)
	}()
	return out
}

// squareWorker는 입력을 받아 제곱한 결과를 반환합니다 (Fan-out)
func squareWorker(id int, in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in {
			fmt.Printf("Worker %d: %d 처리 중\n", id, n)
			time.Sleep(300 * time.Millisecond)
			out <- n * n
		}
		close(out)
	}()
	return out
}

// fanIn은 여러 채널의 결과를 하나로 합칩니다 (Fan-in)
func fanIn(channels ...<-chan int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup

	// TODO: 각 입력 채널에서 값을 읽어 out 채널로 전송
	// for _, ch := range channels {
	//     wg.Add(1)
	//     go func(c <-chan int) {
	//         defer wg.Done()
	//         for n := range c {
	//             out <- n
	//         }
	//     }(ch)
	// }

	// TODO: 모든 입력이 끝나면 out 채널 닫기
	// go func() {
	//     wg.Wait()
	//     close(out)
	// }()

	return out
}

func main() {
	start := time.Now()

	// 입력 생성
	input := producer(1, 2, 3, 4, 5, 6, 7, 8, 9)

	// TODO 1: Fan-out - 3개의 워커에게 작업 분배
	// 주의: 같은 input 채널을 여러 워커가 공유
	// w1 := squareWorker(1, input)
	// w2 := squareWorker(2, input)
	// w3 := squareWorker(3, input)

	// TODO 2: Fan-in - 결과 합치기
	// results := fanIn(w1, w2, w3)

	// TODO 3: 결과 출력
	// for result := range results {
	//     fmt.Printf("결과: %d\n", result)
	// }

	elapsed := time.Since(start)
	fmt.Printf("\n총 소요 시간: %v\n", elapsed)
}

// 예상 출력 (순서는 다를 수 있음):
// Worker 1: 1 처리 중
// Worker 2: 2 처리 중
// Worker 3: 3 처리 중
// 결과: 1
// Worker 1: 4 처리 중
// 결과: 4
// ...
// 총 소요 시간: ~1s (9개 작업, 3개 워커, 작업당 300ms)
