// Practice 04: Status Code 에러 처리
// 목표: gRPC 표준 에러 코드 사용

package main

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// ===== 서버: 에러 반환 =====

func handleRequest(ctx context.Context, userID string) error {
	// 잘못된 입력
	if userID == "" {
		return status.Errorf(codes.InvalidArgument, "user_id is required")
	}

	// 리소스 없음
	if userID == "unknown" {
		return status.Errorf(codes.NotFound, "user not found: %s", userID)
	}

	// 인증 필요
	// return status.Errorf(codes.Unauthenticated, "authentication required")

	// 권한 없음
	// return status.Errorf(codes.PermissionDenied, "access denied")

	// 서버 오류
	// return status.Errorf(codes.Internal, "database connection failed")

	return nil
}

// ===== 클라이언트: 에러 처리 =====

func handleError(err error) {
	if err == nil {
		return
	}

	st, ok := status.FromError(err)
	if !ok {
		// gRPC 에러가 아닌 일반 에러
		log.Printf("Unknown error: %v", err)
		return
	}

	switch st.Code() {
	case codes.NotFound:
		log.Printf("Resource not found: %s", st.Message())
	case codes.InvalidArgument:
		log.Printf("Invalid input: %s", st.Message())
	case codes.Unauthenticated:
		log.Printf("Authentication required")
	case codes.PermissionDenied:
		log.Printf("Permission denied")
	case codes.Internal:
		log.Printf("Server error: %s", st.Message())
	default:
		log.Printf("gRPC error [%s]: %s", st.Code(), st.Message())
	}
}

func main() {
	fmt.Println("=== gRPC Error Handling Practice ===")
	fmt.Println("")
	fmt.Println("주요 Status Codes:")
	fmt.Println("| Code              | HTTP | 의미           |")
	fmt.Println("|-------------------|------|----------------|")
	fmt.Println("| codes.OK          | 200  | 성공           |")
	fmt.Println("| codes.NotFound    | 404  | 리소스 없음    |")
	fmt.Println("| codes.InvalidArg  | 400  | 잘못된 입력    |")
	fmt.Println("| codes.Unauth      | 401  | 인증 필요      |")
	fmt.Println("| codes.PermDenied  | 403  | 권한 없음      |")
	fmt.Println("| codes.Internal    | 500  | 서버 오류      |")
	fmt.Println("")

	// 에러 생성 및 처리 예시
	err := handleRequest(context.Background(), "")
	handleError(err)

	err = handleRequest(context.Background(), "unknown")
	handleError(err)

	err = handleRequest(context.Background(), "valid-user")
	if err == nil {
		fmt.Println("Success: valid-user")
	}
}
