package common

// Message represents a generic Kafka message for learning purposes.
type Message struct {
	Key   string
	Value []byte
	Topic string
}
