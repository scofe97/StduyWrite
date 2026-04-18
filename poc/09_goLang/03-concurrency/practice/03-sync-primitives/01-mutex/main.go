package main

import (
	"fmt"
	"sync"
)

// 과제: Mutex로 Race Condition 해결
//
// 목표:
// 1. 공유 변수 접근 시 race condition 이해
// 2. sync.Mutex로 상호 배제 구현
//
// 테스트: go run -race main.go
//
// TODO: 아래 코드를 완성하세요

var (
	counter int
	// TODO: mu sync.Mutex 추가
)

func increment(wg *sync.WaitGroup) {
	defer wg.Done()

	for i := 0; i < 1000; i++ {
		// TODO: Lock/Unlock 추가
		counter++
	}
}

func main() {
	var wg sync.WaitGroup

	// 10개의 goroutine이 동시에 counter 증가
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment(&wg)
	}

	wg.Wait()

	fmt.Printf("최종 카운터: %d\n", counter)
	fmt.Printf("예상 값: %d\n", 10*1000)

	if counter == 10000 {
		fmt.Println("✓ 정확!")
	} else {
		fmt.Println("✗ Race condition 발생!")
	}
}

// Mutex 없이 실행하면:
// 최종 카운터: 7234 (매번 다름)
// 예상 값: 10000
// ✗ Race condition 발생!
//
// Mutex 추가 후:
// 최종 카운터: 10000
// 예상 값: 10000
// ✓ 정확!
