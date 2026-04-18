package kafka

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/twmb/franz-go/pkg/kgo"
)

type EventProducer struct {
	client *kgo.Client
}

func NewEventProducer(client *kgo.Client) *EventProducer {
	return &EventProducer{client: client}
}

func (p *EventProducer) Publish(ctx context.Context, topic, key string, event any) error {
	data, err := json.Marshal(event)
	if err != nil {
		return fmt.Errorf("marshal event: %w", err)
	}

	record := &kgo.Record{
		Topic: topic,
		Key:   []byte(key),
		Value: data,
	}

	results := p.client.ProduceSync(ctx, record)
	if err := results.FirstErr(); err != nil {
		return fmt.Errorf("produce to %s: %w", topic, err)
	}
	return nil
}

func (p *EventProducer) Close() {
	p.client.Close()
}
