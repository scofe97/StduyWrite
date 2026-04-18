// Practice 01: Unary RPC
// 목표: 기본적인 요청-응답 패턴 이해

package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

// 참고: 실제 구현 시 proto 파일 생성 필요
// 이 파일은 구조 이해를 위한 예시입니다

/*
proto/greeter.proto:

syntax = "proto3";
package greeter;
option go_package = "./proto";

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply);
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
*/

// ===== 서버 =====

func runServer() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	// pb.RegisterGreeterServer(s, &server{})  // 실제 구현

	log.Println("gRPC server listening on :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}

// ===== 클라이언트 =====

func runClient() {
	conn, err := grpc.NewClient("localhost:50051",
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		log.Fatalf("Did not connect: %v", err)
	}
	defer conn.Close()

	// client := pb.NewGreeterClient(conn)  // 실제 구현
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	// resp, err := client.SayHello(ctx, &pb.HelloRequest{Name: "World"})
	_ = ctx
	fmt.Println("Unary RPC completed")
}

func main() {
	fmt.Println("=== Unary RPC Practice ===")
	fmt.Println("")
	fmt.Println("Steps to implement:")
	fmt.Println("1. Define proto file with service and messages")
	fmt.Println("2. Generate Go code: protoc --go_out=. --go-grpc_out=. proto/*.proto")
	fmt.Println("3. Implement server interface")
	fmt.Println("4. Create client and call RPC")
	fmt.Println("")
	fmt.Println("Run server: go run main.go server")
	fmt.Println("Run client: go run main.go client")
}

// protoc 설치:
// brew install protobuf
// go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
// go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
