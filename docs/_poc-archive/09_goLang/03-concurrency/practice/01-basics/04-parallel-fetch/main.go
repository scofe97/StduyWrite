package main

import (
	"fmt"
	"time"
)

// 과제: 병렬 API 호출
//
// 목표:
// 1. 여러 API를 병렬로 호출하여 시간 단축
// 2. 채널을 사용한 결과 수집
//
// TODO: 아래 코드를 완성하세요

// API 응답을 시뮬레이션하는 함수
func fetchAPI(name string, delay time.Duration) string {
	time.Sleep(delay)
	return fmt.Sprintf("%s 응답 (지연: %v)", name, delay)
}

func main() {
	start := time.Now()

	apis := []struct {
		name  string
		delay time.Duration
	}{
		{"GitHub API", 500 * time.Millisecond},
		{"GitLab API", 700 * time.Millisecond},
		{"Bitbucket API", 600 * time.Millisecond},
	}

	// TODO 1: 결과를 받을 채널 생성
	// results := make(chan string, len(apis))

	// TODO 2: 각 API를 goroutine으로 호출
	// for _, api := range apis {
	//     go func(name string, delay time.Duration) {
	//         results <- fetchAPI(name, delay)
	//     }(api.name, api.delay)
	// }

	// TODO 3: 모든 결과 수신 및 출력
	// for i := 0; i < len(apis); i++ {
	//     fmt.Println(<-results)
	// }

	elapsed := time.Since(start)
	fmt.Printf("\n총 소요 시간: %v\n", elapsed)

	// 예상: 순차 실행 시 1.8초, 병렬 실행 시 ~700ms
}

// 예상 출력:
// GitHub API 응답 (지연: 500ms)
// GitLab API 응답 (지연: 700ms)
// Bitbucket API 응답 (지연: 600ms)
//
// 총 소요 시간: ~700ms
