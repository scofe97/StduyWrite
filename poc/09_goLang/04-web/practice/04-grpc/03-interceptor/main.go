// Practice 03: 인터셉터 (미들웨어)
// 목표: 모든 RPC 요청에 공통 로직 적용

package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"google.golang.org/grpc"
)

// ===== Unary 인터셉터 =====

func loggingInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	// 1. 요청 전 처리
	start := time.Now()
	log.Printf("[START] %s", info.FullMethod)

	// 2. 실제 핸들러 호출
	resp, err := handler(ctx, req)

	// 3. 요청 후 처리
	log.Printf("[END] %s - Duration: %v, Error: %v",
		info.FullMethod, time.Since(start), err)

	return resp, err
}

// ===== 인증 인터셉터 =====

func authInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	// metadata에서 인증 정보 추출
	// md, ok := metadata.FromIncomingContext(ctx)
	// if !ok {
	//     return nil, status.Errorf(codes.Unauthenticated, "missing metadata")
	// }
	// token := md["authorization"]

	return handler(ctx, req)
}

// ===== 서버에 인터셉터 등록 =====

func setupServer() {
	// 단일 인터셉터
	_ = grpc.NewServer(
		grpc.UnaryInterceptor(loggingInterceptor),
	)

	// 여러 인터셉터 체이닝
	_ = grpc.NewServer(
		grpc.ChainUnaryInterceptor(
			loggingInterceptor, // 1번째 실행
			authInterceptor,    // 2번째 실행
		),
	)
}

func main() {
	fmt.Println("=== gRPC Interceptor Practice ===")
	fmt.Println("")
	fmt.Println("인터셉터 종류:")
	fmt.Println("- UnaryInterceptor: 단일 요청-응답")
	fmt.Println("- StreamInterceptor: 스트리밍 RPC")
	fmt.Println("")
	fmt.Println("인터셉터 시그니처:")
	fmt.Println("func(ctx, req, info, handler) (resp, error)")
	fmt.Println("")
	fmt.Println("체이닝:")
	fmt.Println("- grpc.ChainUnaryInterceptor(a, b, c)")
	fmt.Println("- 실행 순서: a → b → c → handler → c → b → a")
	fmt.Println("")
	fmt.Println("Spring 비교:")
	fmt.Println("- Filter + Interceptor = gRPC Interceptor")
	fmt.Println("- FilterChain = ChainUnaryInterceptor")

	setupServer()
}
