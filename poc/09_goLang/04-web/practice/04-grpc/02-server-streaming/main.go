// Practice 02: Server Streaming RPC
// 목표: 서버가 여러 응답을 스트리밍으로 전송

package main

import (
	"fmt"
	"io"
)

/*
proto/numbers.proto:

syntax = "proto3";
package numbers;
option go_package = "./proto";

service NumberService {
  // 서버 스트리밍: 1개 요청 → N개 응답
  rpc GenerateNumbers (NumberRequest) returns (stream NumberResponse);
}

message NumberRequest {
  int32 count = 1;
}

message NumberResponse {
  int32 number = 1;
}
*/

// ===== 서버 구현 패턴 =====

/*
func (s *server) GenerateNumbers(req *pb.NumberRequest, stream pb.NumberService_GenerateNumbersServer) error {
    for i := int32(0); i < req.Count; i++ {
        if err := stream.Send(&pb.NumberResponse{Number: i}); err != nil {
            return err
        }
        time.Sleep(time.Second)  // 1초 간격으로 전송
    }
    return nil  // nil 반환 = 스트림 종료
}
*/

// ===== 클라이언트 구현 패턴 =====

/*
func clientStreaming(client pb.NumberServiceClient) {
    stream, err := client.GenerateNumbers(ctx, &pb.NumberRequest{Count: 10})
    if err != nil {
        log.Fatal(err)
    }

    for {
        resp, err := stream.Recv()
        if err == io.EOF {
            break  // 스트림 종료
        }
        if err != nil {
            log.Fatal(err)
        }
        fmt.Printf("Received: %d\n", resp.Number)
    }
}
*/

func main() {
	fmt.Println("=== Server Streaming RPC Practice ===")
	fmt.Println("")
	fmt.Println("Server Streaming 패턴:")
	fmt.Println("- 클라이언트: 1개 요청")
	fmt.Println("- 서버: N개 응답 (스트림)")
	fmt.Println("")
	fmt.Println("사용 사례:")
	fmt.Println("- 대량 데이터 조회 (페이지네이션 대신)")
	fmt.Println("- 실시간 피드/로그 전송")
	fmt.Println("- 긴 처리 작업의 진행 상황 보고")
	fmt.Println("")
	fmt.Println("핵심 메서드:")
	fmt.Println("- 서버: stream.Send() → 데이터 전송")
	fmt.Println("- 클라이언트: stream.Recv() → 데이터 수신")
	fmt.Printf("- 종료 감지: err == io.EOF (%v)\n", io.EOF)
}
