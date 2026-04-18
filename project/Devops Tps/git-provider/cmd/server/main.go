package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"

	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"github.com/twmb/franz-go/pkg/kgo"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/reflection"

	"github.com/runners-high/git-provider/internal/cicd"
	"github.com/runners-high/git-provider/internal/kafka"
	"github.com/runners-high/git-provider/internal/middleware"
	"github.com/runners-high/git-provider/internal/pipeline"
	"github.com/runners-high/git-provider/internal/server"
	"github.com/runners-high/git-provider/internal/workflow"
	pb "github.com/runners-high/git-provider/pkg/pb/v1"
)

const (
	grpcPort = ":50051"
	httpPort = ":8080"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Kafka 브로커 주소
	brokers := getEnv("KAFKA_BROKERS", "localhost:19092")

	// Pipeline Store (인메모리)
	store := pipeline.NewStore()

	// Workflow Store (인메모리)
	wfStore := workflow.NewStore()

	// Kafka Producer
	producer, err := newKafkaProducer(brokers)
	if err != nil {
		log.Printf("WARNING: Kafka producer init failed (CI/CD events disabled): %v", err)
	}

	// Kafka Consumer + 핸들러 등록
	consumer, err := newKafkaConsumer(brokers)
	if err != nil {
		log.Printf("WARNING: Kafka consumer init failed (event processing disabled): %v", err)
	}

	// Workflow Engine
	var wfEngine *workflow.Engine
	if producer != nil {
		wfEngine = workflow.NewEngine(wfStore, producer)
	}

	if consumer != nil && producer != nil {
		consumer.RegisterHandler(kafka.TopicGitEvents, makeGitEventHandler(store, producer, wfEngine))
		consumer.RegisterHandler(kafka.TopicCICDResults, makeBuildResultHandler(store))
		consumer.RegisterHandler(kafka.TopicCICDCommands, cicd.MakeCommandHandler(store, producer))
		if wfEngine != nil {
			consumer.RegisterHandler(kafka.TopicCICDEvents, wfEngine.MakeCICDEventHandler())
		}
		go consumer.Run(ctx)
	}

	// gRPC 서버 시작 (goroutine)
	go startGRPCServer(store, producer, wfStore)

	// REST Gateway 시작 (goroutine)
	go startRESTGateway()

	fmt.Println("===========================================")
	fmt.Println("  Git Provider Server Started!")
	fmt.Println("===========================================")
	fmt.Printf("  gRPC Server: localhost%s\n", grpcPort)
	fmt.Printf("  REST Server: localhost%s\n", httpPort)
	fmt.Printf("  Kafka:       %s\n", brokers)
	fmt.Println("===========================================")
	fmt.Println()
	fmt.Println("REST API 테스트:")
	fmt.Println("  curl -X POST http://localhost:8080/v1/repositories/list \\")
	fmt.Println("    -H 'Content-Type: application/json' \\")
	fmt.Println("    -d '{\"provider\": {\"github\": {\"token\": \"YOUR_TOKEN\"}}}'")
	fmt.Println()
	fmt.Println("CI/CD API 테스트:")
	fmt.Println("  curl -X POST http://localhost:8080/v1/pipelines/create \\")
	fmt.Println("    -H 'Content-Type: application/json' \\")
	fmt.Println("    -d '{\"name\":\"my-pipeline\",\"repository\":\"owner/app\",\"branch_pattern\":\"main\",\"jenkins_job_name\":\"my-job\",\"ci_config\":{\"jenkins\":{\"url\":\"http://localhost:9090\",\"username\":\"admin\",\"api_token\":\"admin\"}}}'")
	fmt.Println()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	fmt.Println("\nShutting down server...")
	cancel()
	if producer != nil {
		producer.Close()
	}
	if consumer != nil {
		consumer.Close()
	}
}

func startGRPCServer(store *pipeline.Store, producer *kafka.EventProducer, wfStore *workflow.Store) {
	lis, err := net.Listen("tcp", grpcPort)
	if err != nil {
		log.Fatalf("Failed to listen on %s: %v", grpcPort, err)
	}

	grpcServer := grpc.NewServer(
		grpc.ChainUnaryInterceptor(
			middleware.RecoveryInterceptor(),
			middleware.LoggingInterceptor(),
		),
	)

	// GitService 등록
	gitServer := server.NewGitServer()
	pb.RegisterGitServiceServer(grpcServer, gitServer)

	// ContentsService 등록
	contentsServer := server.NewContentsServer()
	pb.RegisterContentsServiceServer(grpcServer, contentsServer)

	// BranchService 등록
	branchServer := server.NewBranchServer()
	pb.RegisterBranchServiceServer(grpcServer, branchServer)

	// MergeRequestService 등록
	mrServer := server.NewMergeRequestServer()
	pb.RegisterMergeRequestServiceServer(grpcServer, mrServer)

	// CICDService 등록
	cicdServer := server.NewCICDServer(store, producer)
	pb.RegisterCICDServiceServer(grpcServer, cicdServer)

	// WorkflowService 등록
	workflowServer := server.NewWorkflowServer(wfStore)
	pb.RegisterWorkflowServiceServer(grpcServer, workflowServer)

	// Reflection 활성화 (grpcurl 등 도구에서 사용)
	reflection.Register(grpcServer)

	log.Printf("gRPC server listening on %s", grpcPort)
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC: %v", err)
	}
}

func startRESTGateway() {
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	// gRPC Gateway 설정
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}

	// GitService 핸들러 등록
	err := pb.RegisterGitServiceHandlerFromEndpoint(ctx, mux, "localhost"+grpcPort, opts)
	if err != nil {
		log.Fatalf("Failed to register GitService gateway: %v", err)
	}

	// ContentsService 핸들러 등록
	err = pb.RegisterContentsServiceHandlerFromEndpoint(ctx, mux, "localhost"+grpcPort, opts)
	if err != nil {
		log.Fatalf("Failed to register ContentsService gateway: %v", err)
	}

	// BranchService 핸들러 등록
	err = pb.RegisterBranchServiceHandlerFromEndpoint(ctx, mux, "localhost"+grpcPort, opts)
	if err != nil {
		log.Fatalf("Failed to register BranchService gateway: %v", err)
	}

	// MergeRequestService 핸들러 등록
	err = pb.RegisterMergeRequestServiceHandlerFromEndpoint(ctx, mux, "localhost"+grpcPort, opts)
	if err != nil {
		log.Fatalf("Failed to register MergeRequestService gateway: %v", err)
	}

	// CICDService 핸들러 등록
	err = pb.RegisterCICDServiceHandlerFromEndpoint(ctx, mux, "localhost"+grpcPort, opts)
	if err != nil {
		log.Fatalf("Failed to register CICDService gateway: %v", err)
	}

	// WorkflowService 핸들러 등록
	err = pb.RegisterWorkflowServiceHandlerFromEndpoint(ctx, mux, "localhost"+grpcPort, opts)
	if err != nil {
		log.Fatalf("Failed to register WorkflowService gateway: %v", err)
	}

	log.Printf("REST gateway listening on %s", httpPort)
	if err := http.ListenAndServe(httpPort, middleware.CORSWrapper(mux)); err != nil {
		log.Fatalf("Failed to serve HTTP: %v", err)
	}
}

// =============================================================================
// Kafka 초기화
// =============================================================================

func newKafkaProducer(brokers string) (*kafka.EventProducer, error) {
	seeds := strings.Split(brokers, ",")
	client, err := kgo.NewClient(
		kgo.SeedBrokers(seeds...),
	)
	if err != nil {
		return nil, fmt.Errorf("create kafka producer: %w", err)
	}
	return kafka.NewEventProducer(client), nil
}

func newKafkaConsumer(brokers string) (*kafka.EventConsumer, error) {
	seeds := strings.Split(brokers, ",")
	client, err := kgo.NewClient(
		kgo.SeedBrokers(seeds...),
		kgo.ConsumerGroup("git-provider"),
		kgo.ConsumeTopics(kafka.TopicGitEvents, kafka.TopicCICDResults, kafka.TopicCICDCommands, kafka.TopicCICDEvents),
	)
	if err != nil {
		return nil, fmt.Errorf("create kafka consumer: %w", err)
	}
	return kafka.NewEventConsumer(client), nil
}

// =============================================================================
// Kafka 이벤트 핸들러
// =============================================================================

func makeGitEventHandler(store *pipeline.Store, producer *kafka.EventProducer, wfEngine *workflow.Engine) kafka.MessageHandler {
	// Workflow engine handler (if available)
	var wfHandler kafka.MessageHandler
	if wfEngine != nil {
		wfHandler = wfEngine.MakeGitEventHandler()
	}

	return func(ctx context.Context, topic string, key, value []byte) error {
		event, err := kafka.ParseEvent[kafka.GitEvent](value)
		if err != nil {
			return err
		}

		log.Printf("git event: type=%s repo=%s branch=%s", event.EventType, event.Repository, event.Branch)

		// Workflow engine 매칭 (이벤트 기반 워크플로우)
		if wfHandler != nil {
			if err := wfHandler(ctx, topic, key, value); err != nil {
				log.Printf("workflow engine error: %v", err)
			}
		}

		return nil
	}
}

func makeBuildResultHandler(store *pipeline.Store) kafka.MessageHandler {
	return func(ctx context.Context, topic string, key, value []byte) error {
		event, err := kafka.ParseEvent[kafka.BuildResultEvent](value)
		if err != nil {
			return err
		}

		log.Printf("build result: pipeline=%s build=%d status=%s", event.PipelineID, event.BuildNumber, event.Status)

		status := mapBuildStatus(event.Status)
		return store.UpdateBuildStatus(event.PipelineID, int32(event.BuildNumber), status, event.URL, int32(event.DurationSeconds))
	}
}

func mapBuildStatus(result string) pb.BuildStatus {
	switch result {
	case "SUCCESS":
		return pb.BuildStatus_BUILD_STATUS_SUCCESS
	case "FAILURE":
		return pb.BuildStatus_BUILD_STATUS_FAILURE
	case "ABORTED":
		return pb.BuildStatus_BUILD_STATUS_ABORTED
	default:
		return pb.BuildStatus_BUILD_STATUS_FAILURE
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
