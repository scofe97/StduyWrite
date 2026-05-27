package main

import (
	"context"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	"log"
	"net"
	"time"

	pb "go-learning/07-grpc-advanced/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials" // TLS용
)

type providerServer struct {
	pb.UnimplementedProviderServiceServer
	providers map[string]*pb.Provider
}

func newProviderServer() *providerServer {
	return &providerServer{
		providers: map[string]*pb.Provider{
			"github": {
				Type:    "github",
				BaseUrl: "https://api.github.com",
				Token:   "ghp_xxx",
			},
			"azure": {
				Type:    "azure",
				BaseUrl: "https://dev.azure.com",
				Token:   "pat_xxx",
			},
		},
	}
}

func (s *providerServer) GetProvider(ctx context.Context, req *pb.GetProviderRequest) (*pb.GetProviderResponse, error) {
	// Metadata 수신
	md, ok := metadata.FromIncomingContext(ctx)
	if ok {
		if auth := md["authorization"]; len(auth) > 0 {
			log.Printf("[Metadata] Authorization: %s", auth[0])
		}
		if reqID := md["x-request-id"]; len(reqID) > 0 {
			log.Printf("[Metadata] Request-ID: %s", reqID[0])
		}
	}

	log.Printf("GetProvider 호출: %s", req.Type)

	provider, exists := s.providers[req.Type]
	if !exists {
		return nil, status.Errorf(codes.NotFound, "프로바이더를 찾을 . 없음: %s", req.Type)
	}

	return &pb.GetProviderResponse{
		Provider: provider,
	}, nil
}

func (s *providerServer) ListProviders(req *pb.ListProviderRequest, stream pb.ProviderService_ListProvidersServer) error {
	log.Println("[Stream] ListProviders 호출")

	for providerType, provider := range s.providers {
		log.Printf("[Stream] 전송: %s", providerType)

		// 하나씩 스트림으로 전송
		if err := stream.Send(provider); err != nil {
			return err
		}

		// 스트리밍 효과를 보기 위해 잠시 대기 (선택사항)
		time.Sleep(500 * time.Millisecond)
	}

	log.Println("[Stream] 전송 완료")
	return nil
}

func loggingInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	// 1. 요청 전 처리
	start := time.Now()

	md, _ := metadata.FromIncomingContext(ctx)
	log.Printf("[Interceptor] Method: %s", info.FullMethod)
	if auth := md["authorization"]; len(auth) > 0 {
		log.Printf("[Interceptor] Auth: %s", auth[0])
	}

	// 2. 실제 핸들러 호출
	resp, err := handler(ctx, req)

	// 3. 요청 후 처리
	log.Printf("[Interceptor] Duration: %v", time.Since(start))

	return resp, err
}

func authInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, status.Errorf(codes.Unauthenticated, "metadata 없음")
	}

	auth := md["authorization"]
	if len(auth) == 0 || auth[0] != "Bearer my-secret-token" {
		return nil, status.Errorf(codes.Unauthenticated, "인증 실패")
	}

	// 인증 성공 → 핸들러 실행
	return handler(ctx, req)
}

func main() {
	// 1. TLS 인증서 로드
	creds, err := credentials.NewServerTLSFromFile("./certs/server.crt", "./certs/server.key")
	if err != nil {
		log.Fatalf("인증서 로드 실패: %v", err)
	}
	log.Println("✅ TLS 인증서 로드 완료")

	// 2. TCP 리스너
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("포트 열기 실패: %v", err)
	}

	// 3. TLS가 적용된 gRPC 서버 생성
	grpcServer := grpc.NewServer(
		grpc.Creds(creds),
		grpc.ChainUnaryInterceptor(loggingInterceptor, authInterceptor), // 추가
	)

	// 4. 서비스 등록
	pb.RegisterProviderServiceServer(grpcServer, newProviderServer())

	log.Println("🔒 TLS gRPC 서버 시작: localhost:50051")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("서버 실행 실패: %v", err)
	}
}
