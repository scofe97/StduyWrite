package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"time"
)

// 과제 1: 타임아웃 HTTP 클라이언트
// 5초 타임아웃이 있는 HTTP 클라이언트를 구현하고, 타임아웃 시 적절한 에러를 반환하세요.

// 테스트용 느린 서버 URL (httpbin.org 사용)
const (
	// 2초 지연 후 응답 (성공 케이스)
	fastURL = "https://httpbin.org/delay/2"
	// 10초 지연 후 응답 (타임아웃 케이스)
	slowURL = "https://httpbin.org/delay/10"
)

// TODO: 타임아웃이 있는 HTTP GET 요청 함수 구현
// - ctx를 사용하여 요청 생성 (http.NewRequestWithContext)
// - 타임아웃 발생 시 context.DeadlineExceeded 에러 반환
// - 반환: 응답 바이트, 에러
func FetchWithTimeout(ctx context.Context, url string) ([]byte, error) {
	// TODO:
	// 1. http.NewRequestWithContext로 요청 생성
	// 2. http.DefaultClient.Do로 요청 실행
	// 3. 응답 바디 읽기
	// 4. 에러 처리 (타임아웃 vs 일반 에러 구분)
	return nil, fmt.Errorf("not implemented")
}

// TODO: 타임아웃 에러인지 확인하는 헬퍼 함수
func IsTimeoutError(err error) bool {
	// TODO:
	// errors.Is(err, context.DeadlineExceeded) 사용
	return false
}

func main() {
	fmt.Println("=== 타임아웃 HTTP 클라이언트 테스트 ===\n")

	// TODO 1: 5초 타임아웃 컨텍스트 생성
	// ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	// defer cancel()

	// TODO 2: 빠른 응답 테스트 (2초 지연 → 성공해야 함)
	fmt.Println("--- 테스트 1: 빠른 응답 (2초 지연) ---")
	// body, err := FetchWithTimeout(ctx, fastURL)
	// if err != nil {
	//     fmt.Printf("에러: %v\n", err)
	// } else {
	//     fmt.Printf("성공: %d 바이트 수신\n", len(body))
	// }

	// TODO 3: 새 컨텍스트로 느린 응답 테스트 (10초 지연 → 타임아웃)
	fmt.Println("\n--- 테스트 2: 느린 응답 (10초 지연) ---")
	// ctx2, cancel2 := context.WithTimeout(context.Background(), 5*time.Second)
	// defer cancel2()
	// body, err := FetchWithTimeout(ctx2, slowURL)
	// if err != nil {
	//     if IsTimeoutError(err) {
	//         fmt.Println("타임아웃 발생!")
	//     } else {
	//         fmt.Printf("에러: %v\n", err)
	//     }
	// }

	// TODO 4: (선택) 타임아웃 시간 조절 테스트
	// 3초, 5초, 10초 타임아웃으로 같은 URL 호출해보기

	fmt.Println("\nTODO: 타임아웃 HTTP 클라이언트 구현")
}

// 힌트: http.NewRequestWithContext 사용법
// req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
// resp, err := http.DefaultClient.Do(req)
// 타임아웃 시 err에 context.DeadlineExceeded가 포함됨

// 추가 예제를 위한 빈 선언
var _ = io.ReadAll
var _ = time.Second
var _ = http.StatusOK
