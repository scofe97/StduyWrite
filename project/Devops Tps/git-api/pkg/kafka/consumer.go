package kafka

import (
	"context"
	"strings"
	"sync"

	"github.com/segmentio/kafka-go"
	"go.uber.org/zap"
)

// MessageHandler is a function that processes Kafka messages
type MessageHandler func(message []byte) error

// Consumer wraps Kafka consumer functionality
type Consumer struct {
	readers []*kafka.Reader
	topics  []string
	handler MessageHandler
	logger  *zap.Logger
	running bool
	mu      sync.RWMutex
	wg      sync.WaitGroup
}

// NewConsumer creates a new Kafka consumer
func NewConsumer(brokers string, groupID string, topics []string, logger *zap.Logger) (*Consumer, error) {
	brokerList := strings.Split(brokers, ",")

	// kafka-go Reader는 단일 토픽만 지원하므로 토픽별로 Reader 생성
	readers := make([]*kafka.Reader, 0, len(topics))
	for _, topic := range topics {
		r := kafka.NewReader(kafka.ReaderConfig{
			Brokers:  brokerList,
			GroupID:  groupID,
			Topic:    topic,
			MinBytes: 1,
			MaxBytes: 10e6, // 10MB
		})
		readers = append(readers, r)
	}

	return &Consumer{
		readers: readers,
		topics:  topics,
		logger:  logger,
	}, nil
}

// SetHandler sets the message handler function
func (c *Consumer) SetHandler(handler MessageHandler) {
	c.handler = handler
}

// Start begins consuming messages
func (c *Consumer) Start(ctx context.Context) error {
	c.mu.Lock()
	c.running = true
	c.mu.Unlock()

	c.logger.Info("Kafka consumer started",
		zap.Strings("topics", c.topics))

	// 각 Reader에 대해 goroutine 실행
	for _, reader := range c.readers {
		c.wg.Add(1)
		go c.consumeFromReader(ctx, reader)
	}

	// 모든 Reader가 종료될 때까지 대기
	c.wg.Wait()
	return nil
}

// consumeFromReader consumes messages from a single reader
func (c *Consumer) consumeFromReader(ctx context.Context, reader *kafka.Reader) {
	defer c.wg.Done()

	for {
		c.mu.RLock()
		running := c.running
		c.mu.RUnlock()

		if !running {
			return
		}

		select {
		case <-ctx.Done():
			c.logger.Info("Context cancelled, stopping consumer",
				zap.String("topic", reader.Config().Topic))
			return
		default:
			msg, err := reader.ReadMessage(ctx)
			if err != nil {
				// Context 취소 시 정상 종료
				if ctx.Err() != nil {
					return
				}
				c.logger.Error("Error reading message", zap.Error(err))
				continue
			}

			c.logger.Debug("Message received",
				zap.String("topic", msg.Topic),
				zap.Int("partition", msg.Partition),
				zap.Int64("offset", msg.Offset))

			if c.handler != nil {
				if err := c.handler(msg.Value); err != nil {
					c.logger.Error("Error handling message",
						zap.Error(err),
						zap.ByteString("message", msg.Value))
				}
			}
		}
	}
}

// Stop stops the consumer
func (c *Consumer) Stop() {
	c.mu.Lock()
	c.running = false
	c.mu.Unlock()
}

// Close closes the consumer
func (c *Consumer) Close() error {
	c.Stop()

	var lastErr error
	for _, reader := range c.readers {
		if err := reader.Close(); err != nil {
			lastErr = err
			c.logger.Error("Error closing reader", zap.Error(err))
		}
	}
	return lastErr
}
