package config

import (
	"strings"

	"github.com/knadh/koanf/v2"
)

// 전역 koanf 인스턴스
var k = koanf.New(".")

// Config는 애플리케이션 설정 구조체입니다.
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
	Host     string `koanf:"host"`
	Port     int    `koanf:"port"`
	Name     string `koanf:"name"`
	User     string `koanf:"user"`
	Password string `koanf:"password"`
}

// LogConfig는 로깅 설정입니다.
type LogConfig struct {
	Level  string `koanf:"level"`
	Format string `koanf:"format"`
}

// Load는 YAML 파일에서 설정을 로드합니다.
// TODO: 파일에서 설정 로드 구현
func Load(path string) (*Config, error) {
	// 힌트:
	// 1. file.Provider(path) 사용
	// 2. yaml.Parser() 사용
	// 3. k.Load() 호출
	// 4. k.Unmarshal() 호출

	// provider := file.Provider(path)
	// if err := k.Load(provider, yaml.Parser()); err != nil {
	//     return nil, err
	// }

	var cfg Config
	// if err := k.Unmarshal("", &cfg); err != nil {
	//     return nil, err
	// }

	return &cfg, nil
}

// LoadWithEnv는 YAML 파일과 환경변수를 병합하여 설정을 로드합니다.
// TODO: 환경변수 오버라이드 구현
func LoadWithEnv(path string) (*Config, error) {
	// 힌트:
	// 1. 먼저 파일 로드
	// 2. 환경변수 로드 (env.Provider 사용)
	// 3. 환경변수가 파일 설정을 오버라이드

	// 환경변수 형식: APP_SERVER_PORT → server.port
	// if err := k.Load(env.Provider("APP_", ".", func(s string) string {
	//     return strings.Replace(strings.ToLower(
	//         strings.TrimPrefix(s, "APP_")), "_", ".", -1)
	// }), nil); err != nil {
	//     return nil, err
	// }

	var cfg Config
	return &cfg, nil
}

// LoadMultiple은 여러 설정 파일을 병합합니다.
// TODO: 다중 파일 병합 구현
func LoadMultiple(paths ...string) (*Config, error) {
	// 힌트: 여러 파일을 순서대로 로드하면 나중 파일이 이전 값을 덮어씀
	// for _, path := range paths {
	//     if err := k.Load(file.Provider(path), yaml.Parser()); err != nil {
	//         return nil, err
	//     }
	// }

	var cfg Config
	return &cfg, nil
}

// LoadWithProfile은 기본 설정 + 프로파일별 설정을 로드합니다.
// TODO: 프로파일 기반 설정 로드 구현
func LoadWithProfile(basePath, profile string) (*Config, error) {
	// 힌트:
	// 1. 기본 설정 파일 로드 (config.yaml)
	// 2. 프로파일 설정 파일 로드 (config.dev.yaml, config.prod.yaml)
	// 3. 프로파일 설정이 기본 설정을 오버라이드

	// if profile != "" {
	//     profilePath := strings.Replace(basePath, ".yaml", "."+profile+".yaml", 1)
	//     k.Load(file.Provider(profilePath), yaml.Parser())
	// }

	var cfg Config
	return &cfg, nil
}

// Get은 키로 설정 값을 가져옵니다.
// TODO: 동적 설정 조회 구현
func Get(key string) interface{} {
	// 힌트: k.Get(key)
	return nil
}

// GetString은 문자열 설정 값을 가져옵니다.
func GetString(key string) string {
	// 힌트: k.String(key)
	return ""
}

// GetInt는 정수 설정 값을 가져옵니다.
func GetInt(key string) int {
	// 힌트: k.Int(key)
	return 0
}

// envKeyReplacer는 환경변수 키를 koanf 키로 변환합니다.
// APP_SERVER_PORT → server.port
func envKeyReplacer(s string) string {
	return strings.Replace(
		strings.ToLower(strings.TrimPrefix(s, "APP_")),
		"_", ".", -1)
}
