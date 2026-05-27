package main

import (
	"context"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	"io"
	"log"
	"time"

	pb "go-learning/07-grpc-advanced/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials" // TLS용 (insecure 대신)
)

func main() {
	// 1. TLS 인증서 로드 (공개 인증서만 필요)
	log.Println("=== 1. TLS 인증서 로드 ===")
	creds, err := credentials.NewClientTLSFromFile("./certs/server.crt", "")
	if err != nil {
		log.Fatalf("인증서 로드 실패: %v", err)
	}
	log.Println("✅ 인증서 로드 완료")

	// 2. TLS로 서버에 연결
	log.Println("\n=== 2. TLS 서버 연결 ===")
	conn, err := grpc.NewClient("localhost:50051",
		grpc.WithTransportCredentials(creds), // insecure 대신 TLS
	)
	if err != nil {
		log.Fatalf("연결 실패: %v", err)
	}
	defer conn.Close()
	log.Println("🔒 TLS 연결 성공!")

	// 3. 클라이언트 생성
	log.Println("\n=== 3. 클라이언트 생성 ===")
	client := pb.NewProviderServiceClient(conn)
	log.Println("클라이언트 생성 완료!")

	// 4. GetProvider 호출
	log.Println("\n=== 4. GetProvider(github) 호출 ===")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	md := metadata.Pairs(
		"authorization", "Bearer my-secret-token",
		"x-request-id", "req-12345",
	)
	ctx = metadata.NewOutgoingContext(ctx, md)

	resp, err := client.GetProvider(ctx, &pb.GetProviderRequest{
		Type: "unknown",
	})
	if err != nil {
		st, ok := status.FromError(err)
		if ok {
			log.Printf("Code: %s", st.Code())
			log.Printf("Message: %s", st.Message())

			if st.Code() == codes.NotFound {
				log.Println("→ 프로바이더가 존재하지 않습니다")
			}
		}
	}

	// 5. ListProviders 스트리밍 호출
	log.Println("\n=== 5. ListProviders (Server Streaming) ===")

	stream, err := client.ListProviders(ctx, &pb.ListProviderRequest{})
	if err != nil {
		log.Fatalf("스트림 생성 실패: %v", err)
	}

	// 스트림에서 하나씩 수신
	for {
		provider, err := stream.Recv()
		if err == io.EOF {
			// 스트림 종료
			log.Println("✅ 스트림 종료")
			break
		}
		if err != nil {
			log.Fatalf("수신 실패: %v", err)
		}

		log.Printf("  📥 수신: %s - %s", provider.Type, provider.BaseUrl)
	}

	log.Printf("✅ 응답 받음! (암호화된 채널)")
	log.Printf("  - Type: %s", resp.Provider.Type)
	log.Printf("  - URL: %s", resp.Provider.BaseUrl)
	log.Printf("  - Token: %s", resp.Provider.Token)
}
