package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Server ServerConfig `yaml:"server"`
	Kafka  KafkaConfig  `yaml:"kafka"`
	GitHub GitHubConfig `yaml:"github"`
	GitLab GitLabConfig `yaml:"gitlab"`
}

type ServerConfig struct {
	Port int `yaml:"port"`
}

type KafkaConfig struct {
	Brokers       []string `yaml:"brokers"`
	ConsumerGroup string   `yaml:"consumerGroup"`
	Topics        Topics   `yaml:"topics"`
}

type Topics struct {
	Commands string `yaml:"commands"` // runners-high.git.commands
	Events   string `yaml:"events"`   // runners-high.git.events
}

type GitHubConfig struct {
	BaseURL string `yaml:"baseUrl"`
}

type GitLabConfig struct {
	BaseURL string `yaml:"baseUrl"`
}

func Load(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, err
	}

	return &cfg, nil
}

func LoadFromEnv() *Config {
	return &Config{
		Server: ServerConfig{
			Port: getEnvInt("SERVER_PORT", 8090),
		},
		Kafka: KafkaConfig{
			Brokers:       []string{getEnv("KAFKA_BROKERS", "localhost:9092")},
			ConsumerGroup: getEnv("KAFKA_CONSUMER_GROUP", "git-api"),
			Topics: Topics{
				Commands: getEnv("KAFKA_TOPIC_COMMANDS", "runners-high.git.commands"),
				Events:   getEnv("KAFKA_TOPIC_EVENTS", "runners-high.git.events"),
			},
		},
		GitHub: GitHubConfig{
			BaseURL: getEnv("GITHUB_BASE_URL", "https://api.github.com"),
		},
		GitLab: GitLabConfig{
			BaseURL: getEnv("GITLAB_BASE_URL", "https://gitlab.com/api/v4"),
		},
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		var result int
		if _, err := fmt.Sscanf(value, "%d", &result); err == nil {
			return result
		}
	}
	return defaultValue
}
