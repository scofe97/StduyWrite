package config

import (
	"strings"

	"github.com/knadh/koanf/parsers/yaml"
	"github.com/knadh/koanf/providers/env"
	"github.com/knadh/koanf/providers/file"
	"github.com/knadh/koanf/v2"
)

var k = koanf.New(".")

// Config는 애플리케이션 설정입니다.
type Config struct {
	Server   ServerConfig   `koanf:"server"`
	Database DatabaseConfig `koanf:"database"`
	Log      LogConfig      `koanf:"log"`
}

// ServerConfig는 서버 설정입니다.
type ServerConfig struct {
	Host string `koanf:"host"`
	Port int    `koanf:"port"`
}

// DatabaseConfig는 데이터베이스 설정입니다.
type DatabaseConfig struct {
	Path string `koanf:"path"`
}

// LogConfig는 로깅 설정입니다.
type LogConfig struct {
	Level  string `koanf:"level"`
	Format string `koanf:"format"`
}

// Load는 설정 파일을 로드합니다.
// TODO: 설정 로드 구현
func Load(path string) (*Config, error) {
	// 파일 로드
	if err := k.Load(file.Provider(path), yaml.Parser()); err != nil {
		return nil, err
	}

	// 환경변수 오버라이드 (BLOG_ 접두사)
	// BLOG_SERVER_PORT=9090 → server.port=9090
	err := k.Load(env.Provider("BLOG_", ".", func(s string) string {
		return strings.Replace(
			strings.ToLower(strings.TrimPrefix(s, "BLOG_")),
			"_", ".", -1)
	}), nil)
	if err != nil {
		return nil, err
	}

	var cfg Config
	if err := k.Unmarshal("", &cfg); err != nil {
		return nil, err
	}

	return &cfg, nil
}
