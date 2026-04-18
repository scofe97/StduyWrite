package main

import (
	"fmt"
	"sync"
	"time"
)

// 과제: Semaphore로 동시성 제한
//
// 목표:
// 1. 채널을 사용한 세마포어 구현
// 2. 동시 실행 수 제한
//
// TODO: 아래 코드를 완성하세요

func processTask(id int, sem chan struct{}, wg *sync.WaitGroup) {
	defer wg.Done()

	// TODO 1: 세마포어 슬롯 획득
	// sem <- struct{}{}

	fmt.Printf("Task %d 시작 (현재 동시 실행: %d)\n", id, len(sem))
	time.Sleep(time.Second) // 작업 시뮬레이션
	fmt.Printf("Task %d 완료\n", id)

	// TODO 2: 세마포어 슬롯 반환
	// <-sem
}

func main() {
	maxConcurrent := 3 // 동시 실행 최대 3개
	numTasks := 10

	// TODO 3: 세마포어용 채널 생성 (버퍼 크기 = maxConcurrent)
	// sem := make(chan struct{}, maxConcurrent)

	var wg sync.WaitGroup

	start := time.Now()

	// TODO 4: 작업 실행
	// for i := 1; i <= numTasks; i++ {
	//     wg.Add(1)
	//     go processTask(i, sem, &wg)
	// }

	// wg.Wait()

	elapsed := time.Since(start)
	fmt.Printf("\n총 소요 시간: %v\n", elapsed)
	fmt.Printf("예상 시간: ~%v (10개 작업, 동시 3개, 작업당 1초)\n",
		time.Duration((numTasks/maxConcurrent)+1)*time.Second)
}

// 예상 출력:
// Task 1 시작 (현재 동시 실행: 1)
// Task 2 시작 (현재 동시 실행: 2)
// Task 3 시작 (현재 동시 실행: 3)
// Task 1 완료
// Task 4 시작 (현재 동시 실행: 3)
// ...
// 총 소요 시간: ~4s
