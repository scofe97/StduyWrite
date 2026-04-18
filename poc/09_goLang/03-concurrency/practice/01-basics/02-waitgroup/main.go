package main

import (
	"fmt"
	"sync"
	"time"
)

// 과제: WaitGroup으로 동기화
//
// 목표:
// 1. sync.WaitGroup 사용법 이해
// 2. 여러 goroutine의 완료를 대기하기
//
// TODO: 아래 코드를 완성하세요

func worker(id int, wg *sync.WaitGroup) {
	// TODO: defer wg.Done() 추가

	fmt.Printf("Worker %d 시작\n", id)
	time.Sleep(time.Second)
	fmt.Printf("Worker %d 완료\n", id)
}

func main() {
	var wg sync.WaitGroup

	// 3개의 워커 실행
	for i := 1; i <= 3; i++ {
		// TODO 1: wg.Add(1) 호출
		// TODO 2: worker를 goroutine으로 실행
	}

	// TODO 3: 모든 워커 완료 대기
	// wg.Wait()

	fmt.Println("모든 워커 완료!")
}

// 예상 출력 (순서는 다를 수 있음):
// Worker 1 시작
// Worker 2 시작
// Worker 3 시작
// Worker 1 완료
// Worker 2 완료
// Worker 3 완료
// 모든 워커 완료!
