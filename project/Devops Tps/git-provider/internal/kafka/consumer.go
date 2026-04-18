package kafka

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/twmb/franz-go/pkg/kgo"
)

type MessageHandler func(ctx context.Context, topic string, key, value []byte) error

type EventConsumer struct {
	client   *kgo.Client
	handlers map[string]MessageHandler
}

func NewEventConsumer(client *kgo.Client) *EventConsumer {
	return &EventConsumer{
		client:   client,
		handlers: make(map[string]MessageHandler),
	}
}

func (c *EventConsumer) RegisterHandler(topic string, handler MessageHandler) {
	c.handlers[topic] = handler
}

func (c *EventConsumer) Run(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			return
		default:
		}

		fetches := c.client.PollFetches(ctx)
		if errs := fetches.Errors(); len(errs) > 0 {
			for _, e := range errs {
				log.Printf("kafka fetch error topic=%s partition=%d: %v", e.Topic, e.Partition, e.Err)
			}
			continue
		}

		fetches.EachRecord(func(record *kgo.Record) {
			handler, ok := c.handlers[record.Topic]
			if !ok {
				return
			}
			if err := handler(ctx, record.Topic, record.Key, record.Value); err != nil {
				log.Printf("handler error topic=%s key=%s: %v", record.Topic, string(record.Key), err)
			}
		})
	}
}

func (c *EventConsumer) Close() {
	c.client.Close()
}

// ParseEvent is a helper to unmarshal JSON event from Kafka message value.
func ParseEvent[T any](value []byte) (T, error) {
	var event T
	if err := json.Unmarshal(value, &event); err != nil {
		return event, fmt.Errorf("unmarshal event: %w", err)
	}
	return event, nil
}
