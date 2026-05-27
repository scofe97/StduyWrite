package main

import (
	"fmt"
	"time"
)

func main() {
	// 실험 1
	// WaitGroup()

	// 실험 2
	// Channel()

	// 실험 3
	//MultiGoroutine()

	// 실험 4
	//BufferedChannel()

	ch := make(chan RepoResult)
	providers := []string{"GitHub", "GitLab", "Bitbucket"}

	start := time.Now()

	// TODO: 각 provider에 대해 goroutine으로 fetchRepos 호출
	for _, provider := range providers {
		go fetchRepos(provider, ch)
	}

	// TODO: 3개 결과 수신 및 출력
	for i := 0; i < len(providers); i++ {
		result := <-ch
		fmt.Printf("%s: %v\n", result.Provider, result.Repos)
	}

	fmt.Printf("총 소요시간: %v\n", time.Since(start))
	// 순차 실행이면 3~6초, 병렬이면 1~2초!
}
