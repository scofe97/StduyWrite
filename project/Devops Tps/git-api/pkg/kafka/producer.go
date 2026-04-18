package kafka

import (
	"context"
	"encoding/json"
	"strings"
	"time"

	"github.com/segmentio/kafka-go"
	"go.uber.org/zap"
)

// Producer wraps Kafka producer functionality
type Producer struct {
	writer *kafka.Writer
	topic  string
	logger *zap.Logger
}

// NewProducer creates a new Kafka producer
func NewProducer(brokers string, topic string, logger *zap.Logger) (*Producer, error) {
	brokerList := strings.Split(brokers, ",")

	w := &kafka.Writer{
		Addr:         kafka.TCP(brokerList...),
		Topic:        topic,
		Balancer:     &kafka.LeastBytes{},
		RequiredAcks: kafka.RequireAll,
		MaxAttempts:  3,
		Async:        false, // 동기 모드 (에러 즉시 반환)
		Logger:       kafka.LoggerFunc(func(msg string, args ...interface{}) {
			logger.Debug(msg, zap.Any("args", args))
		}),
		ErrorLogger: kafka.LoggerFunc(func(msg string, args ...interface{}) {
			logger.Error(msg, zap.Any("args", args))
		}),
	}

	return &Producer{
		writer: w,
		topic:  topic,
		logger: logger,
	}, nil
}

// Publish sends an event to Kafka
func (p *Producer) Publish(event interface{}) error {
	data, err := json.Marshal(event)
	if err != nil {
		return err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	err = p.writer.WriteMessages(ctx, kafka.Message{
		Value: data,
	})

	if err != nil {
		p.logger.Error("Delivery failed",
			zap.String("topic", p.topic),
			zap.Error(err))
		return err
	}

	p.logger.Debug("Message delivered",
		zap.String("topic", p.topic))

	return nil
}

// PublishWithKey sends an event with a specific key for partitioning
func (p *Producer) PublishWithKey(key string, event interface{}) error {
	data, err := json.Marshal(event)
	if err != nil {
		return err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	err = p.writer.WriteMessages(ctx, kafka.Message{
		Key:   []byte(key),
		Value: data,
	})

	if err != nil {
		p.logger.Error("Delivery failed",
			zap.String("topic", p.topic),
			zap.String("key", key),
			zap.Error(err))
		return err
	}

	p.logger.Debug("Message delivered",
		zap.String("topic", p.topic),
		zap.String("key", key))

	return nil
}

// Flush waits for all messages to be delivered
// kafka-go의 동기 모드에서는 WriteMessages가 즉시 완료되므로
// 이 함수는 호환성을 위해 유지
func (p *Producer) Flush(timeoutMs int) int {
	// kafka-go 동기 모드에서는 flush가 필요 없음
	// 호환성을 위해 0 반환 (pending messages = 0)
	return 0
}

// Close closes the producer
func (p *Producer) Close() {
	if err := p.writer.Close(); err != nil {
		p.logger.Error("Error closing writer", zap.Error(err))
	}
}
