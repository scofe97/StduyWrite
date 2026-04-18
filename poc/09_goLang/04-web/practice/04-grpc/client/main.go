package main

import (
	"context"
	"google.golang.org/grpc/credentials"
	"log"
	"time"

	pb "go-learning/06-grpc/proto"

	"google.golang.org/grpc"
)

func main() {
	// 1. 서버에 연결
	log.Println("=== 1. 서버 연결 ===")
	creds, err := credentials.NewClientTLSFromFile("../certs/server.crt", "")
	if err != nil {
		log.Fatalf("인증서 로드 실패: %v", err)
	}

	conn, err := grpc.NewClient("localhost:50051",
		grpc.WithTransportCredentials(creds),
	)

	if err != nil {
		log.Fatalf("연결 실패: %v", err)
	}
	defer conn.Close()
	log.Println("연결 성공!")

	// 2. 클라이언트 생성
	log.Println("\n=== 2. 클라이언트 생성 ===")
	client := pb.NewProviderServiceClient(conn)
	log.Println("클라이언트 생성 완료!")

	// 3. GetProvider 호출
	log.Println("\n=== 3. GetProvider(github) 호출 ===")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	resp, err := client.GetProvider(ctx, &pb.GetProviderRequest{
		Type: "github",
	})
	if err != nil {
		log.Fatalf("호출 실패: %v", err)
	}

	log.Printf("응답 받음!")
	log.Printf("  - Type: %s", resp.Provider.Type)
	log.Printf("  - URL: %s", resp.Provider.BaseUrl)
	log.Printf("  - Token: %s", resp.Provider.Token)
}
