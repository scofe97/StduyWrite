package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"log"
	"net"

	pb "go-learning/06-grpc/proto"
)

type providerServer struct {
	pb.UnimplementedProviderServiceServer
	providers map[string]*pb.Provider
}

func newProviderServer() *providerServer {
	return &providerServer{
		providers: map[string]*pb.Provider{ // ← 이 줄 추가!
			"github®": {
				Type:    "github",
				BaseUrl: "https://api.github.com",
				Token:   "ghp_xxx",
			},
			"azure": {
				Type:    "azure",
				BaseUrl: "https://dev.azure.com",
				Token:   "pat_xxx",
			},
		}, // ← 닫는 괄호
	}
}

func (s *providerServer) GetProvider(ctx context.Context, req *pb.GetProviderRequest) (*pb.GetProviderResponse, error) {
	log.Printf("GetProvider 호출: %s", req.Type)

	// 맵에서 조회
	provider, exists := s.providers[req.Type]
	if !exists {
		return nil, fmt.Errorf("프로바이더를 찾을 수 없음: %s", req.Type)
	}

	// 응답 반환
	return &pb.GetProviderResponse{
		Provider: provider,
	}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("포트 열기 실패: %v", err)
	}

	// gRPC 서버 생성
	creds, err := credentials.NewServerTLSFromFile("../certs/server.crt", "../certs/server.key")
	grpcServer := grpc.NewServer(grpc.Creds(creds))

	pb.RegisterProviderServiceServer(grpcServer, newProviderServer())

	log.Println("grpc 서버 생성 완료")

	log.Println("서버 시작: localhost:50051")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("서버 실행 실패: %v", err)
	}
}
