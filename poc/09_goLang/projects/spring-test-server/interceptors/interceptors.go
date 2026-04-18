package interceptors

import (
	"context"
	"log"
	"runtime/debug"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

// =============================================================================
// Unary Interceptors
// =============================================================================

// LoggingUnaryInterceptor - 요청/응답 로깅
func LoggingUnaryInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	start := time.Now()

	// 메타데이터 로깅
	if md, ok := metadata.FromIncomingContext(ctx); ok {
		log.Printf("[Interceptor] Headers: %v", md)
	}

	// 핸들러 실행
	resp, err := handler(ctx, req)

	// 결과 로깅
	duration := time.Since(start)
	statusCode := codes.OK
	if err != nil {
		if st, ok := status.FromError(err); ok {
			statusCode = st.Code()
		}
	}

	log.Printf("[Interceptor] Method=%s | Duration=%v | Status=%s",
		info.FullMethod, duration, statusCode)

	return resp, err
}

// RecoveryUnaryInterceptor - 패닉 복구
func RecoveryUnaryInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (resp interface{}, err error) {
	defer func() {
		if r := recover(); r != nil {
			log.Printf("[Recovery] Panic recovered: %v\n%s", r, debug.Stack())
			err = status.Errorf(codes.Internal, "internal server error: %v", r)
		}
	}()

	return handler(ctx, req)
}

// AuthUnaryInterceptor - 인증 검사 (예제)
func AuthUnaryInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	// 메타데이터에서 토큰 추출
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, status.Errorf(codes.Unauthenticated, "metadata is not provided")
	}

	// Authorization 헤더 확인
	tokens := md.Get("authorization")
	if len(tokens) == 0 {
		return nil, status.Errorf(codes.Unauthenticated, "authorization token is not provided")
	}

	// 간단한 토큰 검증 (실제로는 JWT 검증 등)
	token := tokens[0]
	if token != "Bearer valid-token" {
		return nil, status.Errorf(codes.Unauthenticated, "invalid token")
	}

	return handler(ctx, req)
}

// =============================================================================
// Stream Interceptors
// =============================================================================

// LoggingStreamInterceptor - 스트림 요청 로깅
func LoggingStreamInterceptor(
	srv interface{},
	ss grpc.ServerStream,
	info *grpc.StreamServerInfo,
	handler grpc.StreamHandler,
) error {
	start := time.Now()

	log.Printf("[StreamInterceptor] Started: %s (ClientStream=%v, ServerStream=%v)",
		info.FullMethod, info.IsClientStream, info.IsServerStream)

	// 래핑된 스트림 사용
	wrappedStream := &loggingServerStream{ServerStream: ss}
	err := handler(srv, wrappedStream)

	duration := time.Since(start)
	statusCode := codes.OK
	if err != nil {
		if st, ok := status.FromError(err); ok {
			statusCode = st.Code()
		}
	}

	log.Printf("[StreamInterceptor] Completed: %s | Duration=%v | Status=%s | Messages: Sent=%d, Recv=%d",
		info.FullMethod, duration, statusCode,
		wrappedStream.sentCount, wrappedStream.recvCount)

	return err
}

// loggingServerStream - 스트림 래퍼 (메시지 카운트)
type loggingServerStream struct {
	grpc.ServerStream
	sentCount int
	recvCount int
}

func (s *loggingServerStream) SendMsg(m interface{}) error {
	err := s.ServerStream.SendMsg(m)
	if err == nil {
		s.sentCount++
	}
	return err
}

func (s *loggingServerStream) RecvMsg(m interface{}) error {
	err := s.ServerStream.RecvMsg(m)
	if err == nil {
		s.recvCount++
	}
	return err
}

// =============================================================================
// Interceptor 체인 헬퍼
// =============================================================================

// ChainUnaryInterceptors - 여러 Unary 인터셉터 체이닝 (참고용, grpc.ChainUnaryInterceptor 사용 권장)
func ChainUnaryInterceptors(interceptors ...grpc.UnaryServerInterceptor) grpc.UnaryServerInterceptor {
	return func(
		ctx context.Context,
		req interface{},
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (interface{}, error) {
		// 인터셉터 체인 구성
		chain := handler
		for i := len(interceptors) - 1; i >= 0; i-- {
			currentInterceptor := interceptors[i]
			currentHandler := chain
			chain = func(ctx context.Context, req interface{}) (interface{}, error) {
				return currentInterceptor(ctx, req, info, currentHandler)
			}
		}
		return chain(ctx, req)
	}
}
