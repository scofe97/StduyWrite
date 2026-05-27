package main

import (
	"context"
	"errors"
	"fmt"
	"math/rand"
	"time"
)

// 과제 3: 병렬 작업 취소
// 여러 고루틴이 병렬로 작업하다가, 하나라도 실패하면 모든 작업을 취소하는 함수를 구현하세요.

// 작업 결과
type TaskResult struct {
	ID     int
	Result string
	Err    error
}

// 개별 작업 시뮬레이션
// - 랜덤하게 성공/실패
// - 랜덤한 시간 소요
func doTask(ctx context.Context, id int) (string, error) {
	// 랜덤 처리 시간 (100ms ~ 500ms)
	duration := time.Duration(100+rand.Intn(400)) * time.Millisecond

	select {
	case <-time.After(duration):
		// 30% 확률로 실패
		if rand.Float32() < 0.3 {
			return "", fmt.Errorf("작업 %d 실패", id)
		}
		return fmt.Sprintf("작업 %d 완료", id), nil

	case <-ctx.Done():
		// 취소됨
		return "", ctx.Err()
	}
}

// TODO: 병렬 작업 실행 함수 구현
// - 여러 작업을 병렬로 실행
// - 하나라도 실패하면 나머지 모두 취소
// - 모두 성공하면 결과 반환
func RunParallel(ctx context.Context, taskCount int) ([]string, error) {
	// TODO:
	// 1. WithCancel로 취소 가능한 context 생성
	// 2. 각 작업을 고루틴으로 시작
	// 3. 결과를 채널로 수집
	// 4. 에러 발생 시 cancel() 호출
	// 5. 모든 고루틴 완료 대기

	return nil, fmt.Errorf("not implemented")
}

// TODO: (선택) 첫 번째 성공 결과만 반환하는 함수
// 여러 작업 중 가장 먼저 성공한 결과만 반환
func RunFirstSuccess(ctx context.Context, taskCount int) (string, error) {
	// TODO:
	// 1. 모든 작업 시작
	// 2. 첫 번째 성공 결과 수신 시 나머지 취소
	// 3. 모두 실패하면 에러 반환

	return "", fmt.Errorf("not implemented")
}

func main() {
	fmt.Println("=== 병렬 작업 취소 테스트 ===\n")

	// 랜덤 시드 설정
	rand.Seed(time.Now().UnixNano())

	// TODO 1: 5개 작업 병렬 실행
	fmt.Println("--- 테스트 1: 5개 작업 병렬 실행 ---")
	// ctx := context.Background()
	// results, err := RunParallel(ctx, 5)
	// if err != nil {
	//     fmt.Printf("실패: %v\n", err)
	// } else {
	//     fmt.Println("모든 작업 성공:")
	//     for _, r := range results {
	//         fmt.Printf("  - %s\n", r)
	//     }
	// }

	// TODO 2: 여러 번 실행하여 취소 동작 확인
	fmt.Println("\n--- 테스트 2: 10번 반복 실행 ---")
	// successCount := 0
	// for i := 0; i < 10; i++ {
	//     results, err := RunParallel(context.Background(), 5)
	//     if err != nil {
	//         fmt.Printf("시도 %d: 실패 - %v\n", i+1, err)
	//     } else {
	//         fmt.Printf("시도 %d: 성공 - %d개 완료\n", i+1, len(results))
	//         successCount++
	//     }
	// }
	// fmt.Printf("\n성공률: %d/10\n", successCount)

	// TODO 3: (선택) 첫 번째 성공 결과 테스트
	fmt.Println("\n--- 테스트 3: 첫 번째 성공 결과 ---")
	// result, err := RunFirstSuccess(context.Background(), 5)
	// if err != nil {
	//     fmt.Printf("모두 실패: %v\n", err)
	// } else {
	//     fmt.Printf("첫 번째 성공: %s\n", result)
	// }

	fmt.Println("\nTODO: 병렬 작업 취소 구현")
}

// 힌트:
// 1. errgroup 패키지 사용 가능 (golang.org/x/sync/errgroup)
// 2. 직접 구현 시:
//    - 결과 채널과 에러 채널 사용
//    - sync.WaitGroup으로 모든 고루틴 완료 대기
//    - 첫 번째 에러 발생 시 cancel() 호출

// 추가 예제를 위한 빈 선언
var _ = errors.New
var _ = context.WithCancel
