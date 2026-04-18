package main

import (
	"math/rand"
	"time"
)

type RepoResult struct {
	Provider string
	Repos    []string
	Error    error
}

// API 호출 시뮬레이션 (실제로는 1~3초 걸린다고 가정)
func fetchRepos(provider string, ch chan<- RepoResult) {
	// TODO: 구현
	// 1. time.Sleep으로 API 지연 시뮬레이션 (1~2초)
	delay := time.Duration(1000+rand.Intn(1000)) * time.Millisecond
	time.Sleep(delay)

	// 2. 결과를 채널에 전송
	ch <- RepoResult{
		Provider: provider,
		Repos:    []string{"repo1", "repo2"},
		Error:    nil,
	}
}
