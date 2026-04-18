package main

import (
	"context"
	"errors"
	"fmt"
	"time"

	"golang.org/x/sync/errgroup"
)

// 과제: errgroup을 사용한 에러 처리
//
// 목표:
// 1. errgroup으로 여러 goroutine 관리
// 2. 에러 발생 시 context 취소 및 에러 수집
//
// 실행 전: go get golang.org/x/sync/errgroup
//
// TODO: 아래 코드를 완성하세요

// fetchURL은 URL을 가져오는 것을 시뮬레이션합니다
func fetchURL(ctx context.Context, url string) error {
	// 시뮬레이션: "bad-url"이면 에러 반환
	if url == "bad-url" {
		return errors.New("failed to fetch: " + url)
	}

	select {
	case <-time.After(500 * time.Millisecond):
		fmt.Printf("Fetched: %s\n", url)
		return nil
	case <-ctx.Done():
		fmt.Printf("Cancelled: %s\n", url)
		return ctx.Err()
	}
}

func main() {
	urls := []string{
		"https://example.com",
		"https://google.com",
		"bad-url", // 이 URL에서 에러 발생
		"https://github.com",
	}

	// TODO 1: errgroup 생성 (context 포함)
	// g, ctx := errgroup.WithContext(context.Background())

	// TODO 2: 각 URL을 goroutine으로 처리
	// for _, url := range urls {
	//     url := url  // 클로저 캡처 (중요!)
	//     g.Go(func() error {
	//         return fetchURL(ctx, url)
	//     })
	// }

	// TODO 3: 모든 goroutine 완료 대기 및 에러 확인
	// if err := g.Wait(); err != nil {
	//     fmt.Printf("에러 발생: %v\n", err)
	// } else {
	//     fmt.Println("모든 URL 가져오기 성공!")
	// }
}

// 예상 출력:
// Fetched: https://example.com
// Cancelled: https://google.com
// Cancelled: https://github.com
// 에러 발생: failed to fetch: bad-url
