package middleware

import (
	"context"
	"log"
	"runtime/debug"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// LoggingInterceptor logs method name, duration, and error for every unary RPC.
func LoggingInterceptor() grpc.UnaryServerInterceptor {
	return func(
		ctx context.Context,
		req any,
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (any, error) {
		start := time.Now()
		resp, err := handler(ctx, req)
		duration := time.Since(start)

		if err != nil {
			st, _ := status.FromError(err)
			log.Printf("[gRPC] %s | %s | %v | %s", info.FullMethod, st.Code(), duration, st.Message())
		} else {
			log.Printf("[gRPC] %s | OK | %v", info.FullMethod, duration)
		}

		return resp, err
	}
}

// RecoveryInterceptor catches panics in RPC handlers and returns gRPC Internal error.
func RecoveryInterceptor() grpc.UnaryServerInterceptor {
	return func(
		ctx context.Context,
		req any,
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (resp any, err error) {
		defer func() {
			if r := recover(); r != nil {
				log.Printf("[gRPC] PANIC in %s: %v\n%s", info.FullMethod, r, debug.Stack())
				err = status.Errorf(codes.Internal, "internal server error")
			}
		}()
		return handler(ctx, req)
	}
}
