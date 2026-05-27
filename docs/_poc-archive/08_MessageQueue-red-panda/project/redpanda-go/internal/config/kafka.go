package config

import (
	"os"

	"github.com/twmb/franz-go/pkg/kgo"
)

// DefaultBrokers returns broker addresses from env or defaults.
func DefaultBrokers() []string {
	if brokers := os.Getenv("KAFKA_BROKERS"); brokers != "" {
		return []string{brokers}
	}
	return []string{"localhost:19092"}
}

// NewClient creates a franz-go client with the given options.
// Base options (seed brokers) are prepended automatically.
func NewClient(opts ...kgo.Opt) (*kgo.Client, error) {
	baseOpts := []kgo.Opt{
		kgo.SeedBrokers(DefaultBrokers()...),
	}
	allOpts := append(baseOpts, opts...)
	return kgo.NewClient(allOpts...)
}
