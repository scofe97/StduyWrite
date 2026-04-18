package main

import (
	"context"
	"os"
	"os/signal"
	"strings"
	"syscall"

	"github.com/runners-high/git-api/internal/config"
	"github.com/runners-high/git-api/internal/handler"
	"github.com/runners-high/git-api/internal/service"
	"github.com/runners-high/git-api/pkg/kafka"
	"go.uber.org/zap"
)

func main() {
	// 로거 초기화: 프로덕션 레벨의 zap 로거를 생성한다.
	logger, err := zap.NewProduction()
	if err != nil {
		panic(err)
	}
	defer logger.Sync() // 프로그램 종료시 로그 플러시

	logger.Info("Starting git-api service")

	// 구성 로드: 환경변수로부터 Kafka 설정 조회
	cfg := config.LoadFromEnv()

	// 카프카 프로듀서 생성
	producer, err := kafka.NewProducer(
		strings.Join(cfg.Kafka.Brokers, ","),
		cfg.Kafka.Topics.Events,
		logger,
	)
	if err != nil {
		logger.Fatal("Failed to create Kafka producer", zap.Error(err))
	}
	defer producer.Close()

	// 서비스 생성
	gitService := service.NewGitService(producer, logger)

	// 핸들러 생성
	kafkaHandler := handler.NewKafkaHandler(gitService, logger)

	// Kafka 컨슈머 생성
	consumer, err := kafka.NewConsumer(
		strings.Join(cfg.Kafka.Brokers, ","),
		cfg.Kafka.ConsumerGroup,
		[]string{cfg.Kafka.Topics.Commands},
		logger,
	)
	if err != nil {
		logger.Fatal("Failed to create Kafka consumer", zap.Error(err))
	}
	defer consumer.Close()

	// 핸들러 설정: 컨슈머가 메시지를 받을 . 호출할 핸들러 등록
	consumer.SetHandler(kafkaHandler.Handle)

	// 컨텍스트를 사용하여 안전한 종료 사용
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// 종료 시그널
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		sig := <-sigChan
		logger.Info("Received shutdown signal", zap.String("signal", sig.String()))
		cancel()
	}()

	// 컨슈머 시작
	logger.Info("Starting Kafka consumer",
		zap.Strings("topics", []string{cfg.Kafka.Topics.Commands}),
		zap.String("consumerGroup", cfg.Kafka.ConsumerGroup))

	if err := consumer.Start(ctx); err != nil {
		logger.Error("Consumer stopped with error", zap.Error(err))
	}

	logger.Info("git-api service stopped")
}
