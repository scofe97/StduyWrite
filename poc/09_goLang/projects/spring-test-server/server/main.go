package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net"
	"strings"
	"time"

	pb "github.com/runners-high/go-learning/09-spring-test-server/pb"
	"github.com/runners-high/go-learning/09-spring-test-server/interceptors"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"
)

// LearningServer는 학습용 gRPC 서버 구현체
type LearningServer struct {
	pb.UnimplementedLearningServiceServer
}

// =============================================================================
// 1. Unary RPC 구현
// =============================================================================

// SayHello - 가장 기본적인 Unary RPC
func (s *LearningServer) SayHello(ctx context.Context, req *pb.HelloRequest) (*pb.HelloResponse, error) {
	log.Printf("[Unary] SayHello called: name=%s, language=%s", req.Name, req.Language)

	// 메타데이터 확인 (헤더)
	if md, ok := metadata.FromIncomingContext(ctx); ok {
		log.Printf("[Metadata] Received headers: %v", md)
	}

	var message string
	switch req.Language {
	case "ko":
		message = fmt.Sprintf("안녕하세요, %s님!", req.Name)
	case "ja":
		message = fmt.Sprintf("こんにちは、%sさん！", req.Name)
	default:
		message = fmt.Sprintf("Hello, %s!", req.Name)
	}

	// 응답 메타데이터 설정 (트레일러)
	trailer := metadata.Pairs("processed-by", "go-grpc-server")
	grpc.SetTrailer(ctx, trailer)

	return &pb.HelloResponse{
		Message:   message,
		Timestamp: time.Now().Format(time.RFC3339),
	}, nil
}

// Calculate - 비즈니스 로직 예제
func (s *LearningServer) Calculate(ctx context.Context, req *pb.CalculateRequest) (*pb.CalculateResponse, error) {
	log.Printf("[Unary] Calculate called: a=%f, b=%f, op=%s", req.A, req.B, req.Operation)

	var result float64
	var opSymbol string

	switch req.Operation {
	case pb.Operation_OPERATION_ADD:
		result = req.A + req.B
		opSymbol = "+"
	case pb.Operation_OPERATION_SUBTRACT:
		result = req.A - req.B
		opSymbol = "-"
	case pb.Operation_OPERATION_MULTIPLY:
		result = req.A * req.B
		opSymbol = "*"
	case pb.Operation_OPERATION_DIVIDE:
		if req.B == 0 {
			return nil, status.Errorf(codes.InvalidArgument, "division by zero")
		}
		result = req.A / req.B
		opSymbol = "/"
	default:
		return nil, status.Errorf(codes.InvalidArgument, "unknown operation: %v", req.Operation)
	}

	return &pb.CalculateResponse{
		Result:     result,
		Expression: fmt.Sprintf("%.2f %s %.2f = %.2f", req.A, opSymbol, req.B, result),
	}, nil
}

// TestError - 다양한 gRPC 상태 코드 테스트
func (s *LearningServer) TestError(ctx context.Context, req *pb.ErrorRequest) (*pb.ErrorResponse, error) {
	log.Printf("[Unary] TestError called: type=%s", req.ErrorType)

	switch req.ErrorType {
	case pb.ErrorType_ERROR_TYPE_NONE:
		return &pb.ErrorResponse{Message: "No error"}, nil
	case pb.ErrorType_ERROR_TYPE_NOT_FOUND:
		return nil, status.Errorf(codes.NotFound, "resource not found")
	case pb.ErrorType_ERROR_TYPE_INVALID:
		return nil, status.Errorf(codes.InvalidArgument, "invalid argument provided")
	case pb.ErrorType_ERROR_TYPE_PERMISSION:
		return nil, status.Errorf(codes.PermissionDenied, "permission denied")
	case pb.ErrorType_ERROR_TYPE_INTERNAL:
		return nil, status.Errorf(codes.Internal, "internal server error")
	case pb.ErrorType_ERROR_TYPE_UNAVAILABLE:
		return nil, status.Errorf(codes.Unavailable, "service unavailable")
	case pb.ErrorType_ERROR_TYPE_DEADLINE:
		return nil, status.Errorf(codes.DeadlineExceeded, "deadline exceeded")
	default:
		return nil, status.Errorf(codes.Unknown, "unknown error type")
	}
}

// TestDelay - Deadline/Timeout 테스트
func (s *LearningServer) TestDelay(ctx context.Context, req *pb.DelayRequest) (*pb.DelayResponse, error) {
	log.Printf("[Unary] TestDelay called: delay=%dms", req.DelayMs)

	start := time.Now()
	delay := time.Duration(req.DelayMs) * time.Millisecond

	select {
	case <-time.After(delay):
		actualDelay := time.Since(start).Milliseconds()
		return &pb.DelayResponse{
			Message:       fmt.Sprintf("Delayed for %d ms", actualDelay),
			ActualDelayMs: actualDelay,
		}, nil
	case <-ctx.Done():
		// 클라이언트가 취소하거나 deadline 초과
		return nil, status.Errorf(codes.DeadlineExceeded, "request cancelled or deadline exceeded")
	}
}

// =============================================================================
// 2. Server Streaming RPC 구현
// =============================================================================

// StreamNumbers - 숫자 스트리밍
func (s *LearningServer) StreamNumbers(req *pb.NumberRequest, stream pb.LearningService_StreamNumbersServer) error {
	log.Printf("[ServerStream] StreamNumbers called: start=%d, end=%d", req.Start, req.End)

	total := req.End - req.Start + 1
	delay := time.Duration(req.DelayMs) * time.Millisecond

	for i := req.Start; i <= req.End; i++ {
		// 컨텍스트 취소 확인
		if err := stream.Context().Err(); err != nil {
			log.Printf("[ServerStream] Context cancelled")
			return status.Errorf(codes.Cancelled, "client cancelled")
		}

		resp := &pb.NumberResponse{
			Value: i,
			Index: i - req.Start + 1,
			Total: total,
		}

		if err := stream.Send(resp); err != nil {
			return err
		}

		log.Printf("[ServerStream] Sent: %d (%d/%d)", i, resp.Index, total)

		if delay > 0 {
			time.Sleep(delay)
		}
	}

	return nil
}

// StreamLogs - 로그 스트리밍 시뮬레이션
func (s *LearningServer) StreamLogs(req *pb.LogRequest, stream pb.LearningService_StreamLogsServer) error {
	log.Printf("[ServerStream] StreamLogs called: service=%s, count=%d", req.ServiceName, req.Count)

	levels := []pb.LogLevel{pb.LogLevel_LOG_LEVEL_DEBUG, pb.LogLevel_LOG_LEVEL_INFO, pb.LogLevel_LOG_LEVEL_WARN, pb.LogLevel_LOG_LEVEL_ERROR}
	messages := []string{
		"Connection established",
		"Processing request",
		"Cache miss, fetching from database",
		"Response sent successfully",
		"Slow query detected",
		"Memory usage high",
		"Request timeout warning",
		"Authentication successful",
	}

	for i := 0; i < int(req.Count); i++ {
		level := levels[rand.Intn(len(levels))]

		// 최소 레벨 필터링
		if level < req.MinLevel {
			level = req.MinLevel
		}

		resp := &pb.LogResponse{
			Timestamp: time.Now().Format(time.RFC3339Nano),
			Level:     level,
			Message:   messages[rand.Intn(len(messages))],
			Service:   req.ServiceName,
		}

		if err := stream.Send(resp); err != nil {
			return err
		}

		time.Sleep(100 * time.Millisecond)
	}

	return nil
}

// DownloadFile - 파일 다운로드 시뮬레이션
func (s *LearningServer) DownloadFile(req *pb.FileRequest, stream pb.LearningService_DownloadFileServer) error {
	log.Printf("[ServerStream] DownloadFile called: filename=%s, chunkSize=%d", req.Filename, req.ChunkSize)

	// 가상의 파일 데이터 생성 (1MB)
	totalSize := 1024 * 1024
	chunkSize := int(req.ChunkSize)
	if chunkSize <= 0 {
		chunkSize = 64 * 1024 // 기본 64KB
	}

	totalChunks := (totalSize + chunkSize - 1) / chunkSize

	for i := 0; i < totalChunks; i++ {
		// 청크 데이터 생성
		size := chunkSize
		if (i+1)*chunkSize > totalSize {
			size = totalSize - i*chunkSize
		}
		data := make([]byte, size)
		rand.Read(data)

		chunk := &pb.FileChunk{
			Data:        data,
			ChunkNumber: int32(i + 1),
			TotalChunks: int32(totalChunks),
			Filename:    req.Filename,
		}

		if err := stream.Send(chunk); err != nil {
			return err
		}

		log.Printf("[ServerStream] Sent chunk %d/%d", i+1, totalChunks)
	}

	return nil
}

// =============================================================================
// 3. Client Streaming RPC 구현
// =============================================================================

// SumNumbers - 여러 숫자 받아서 합계 반환
func (s *LearningServer) SumNumbers(stream pb.LearningService_SumNumbersServer) error {
	log.Printf("[ClientStream] SumNumbers started")

	var sum float64
	var count int32

	for {
		req, err := stream.Recv()
		if err == io.EOF {
			// 클라이언트 스트리밍 완료
			log.Printf("[ClientStream] Received %d numbers, sum=%.2f", count, sum)

			var avg float64
			if count > 0 {
				avg = sum / float64(count)
			}

			return stream.SendAndClose(&pb.SumResponse{
				Sum:     sum,
				Count:   count,
				Average: avg,
			})
		}
		if err != nil {
			return err
		}

		sum += req.Value
		count++
		log.Printf("[ClientStream] Received: %.2f (running sum: %.2f)", req.Value, sum)
	}
}

// UploadFile - 파일 업로드 시뮬레이션
func (s *LearningServer) UploadFile(stream pb.LearningService_UploadFileServer) error {
	log.Printf("[ClientStream] UploadFile started")

	var totalBytes int64
	var chunksReceived int32
	var filename string

	for {
		chunk, err := stream.Recv()
		if err == io.EOF {
			log.Printf("[ClientStream] Upload complete: %s, %d bytes, %d chunks",
				filename, totalBytes, chunksReceived)

			return stream.SendAndClose(&pb.UploadResponse{
				Filename:       filename,
				TotalBytes:     totalBytes,
				ChunksReceived: chunksReceived,
				Success:        true,
			})
		}
		if err != nil {
			return err
		}

		filename = chunk.Filename
		totalBytes += int64(len(chunk.Data))
		chunksReceived++

		log.Printf("[ClientStream] Received chunk %d/%d for %s",
			chunk.ChunkNumber, chunk.TotalChunks, filename)
	}
}

// =============================================================================
// 4. Bidirectional Streaming RPC 구현
// =============================================================================

// Chat - 실시간 채팅
func (s *LearningServer) Chat(stream pb.LearningService_ChatServer) error {
	log.Printf("[BiStream] Chat started")

	for {
		msg, err := stream.Recv()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			return err
		}

		log.Printf("[BiStream] Received from %s: %s", msg.User, msg.Content)

		// 에코 응답 + 시스템 메시지
		responses := []*pb.ChatMessage{
			{
				User:      msg.User,
				Content:   msg.Content,
				Timestamp: time.Now().Format(time.RFC3339),
				Type:      pb.MessageType_MESSAGE_TYPE_TEXT,
			},
			{
				User:      "System",
				Content:   fmt.Sprintf("Message from %s received!", msg.User),
				Timestamp: time.Now().Format(time.RFC3339),
				Type:      pb.MessageType_MESSAGE_TYPE_SYSTEM,
			},
		}

		for _, resp := range responses {
			if err := stream.Send(resp); err != nil {
				return err
			}
		}
	}
}

// Echo - 양방향 에코 (대문자 변환)
func (s *LearningServer) Echo(stream pb.LearningService_EchoServer) error {
	log.Printf("[BiStream] Echo started")

	for {
		req, err := stream.Recv()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			return err
		}

		log.Printf("[BiStream] Echo received: %s (repeat=%d)", req.Message, req.Repeat)

		// repeat 횟수만큼 응답
		repeat := int(req.Repeat)
		if repeat <= 0 {
			repeat = 1
		}

		for i := 0; i < repeat; i++ {
			resp := &pb.EchoResponse{
				Original:    req.Message,
				Transformed: strings.ToUpper(req.Message),
				Sequence:    int32(i + 1),
			}

			if err := stream.Send(resp); err != nil {
				return err
			}
		}
	}
}

// =============================================================================
// 서버 시작
// =============================================================================

func main() {
	port := ":50052" // Spring Boot 테스트용 포트

	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	// 인터셉터 설정
	opts := []grpc.ServerOption{
		grpc.ChainUnaryInterceptor(
			interceptors.LoggingUnaryInterceptor,
			interceptors.RecoveryUnaryInterceptor,
		),
		grpc.ChainStreamInterceptor(
			interceptors.LoggingStreamInterceptor,
		),
	}

	grpcServer := grpc.NewServer(opts...)
	pb.RegisterLearningServiceServer(grpcServer, &LearningServer{})

	// Reflection 활성화 (grpcurl 테스트용)
	reflection.Register(grpcServer)

	log.Printf("===========================================")
	log.Printf("  gRPC Learning Server started on %s", port)
	log.Printf("  - Unary RPC: SayHello, Calculate, TestError, TestDelay")
	log.Printf("  - Server Streaming: StreamNumbers, StreamLogs, DownloadFile")
	log.Printf("  - Client Streaming: SumNumbers, UploadFile")
	log.Printf("  - Bidirectional: Chat, Echo")
	log.Printf("===========================================")

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
