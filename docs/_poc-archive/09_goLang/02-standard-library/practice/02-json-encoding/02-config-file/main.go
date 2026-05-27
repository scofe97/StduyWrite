package main

import (
	"encoding/json"
	"fmt"
	"os"
)

// 과제 2: 설정 파일 처리
// JSON 형식의 설정 파일을 읽어 구조체로 변환하고, 수정 후 다시 저장하는 프로그램을 작성하세요.

const configPath = "config.json"

// 샘플 설정 파일 내용
var sampleConfig = `{
	"server": {
		"host": "localhost",
		"port": 8080,
		"timeout_seconds": 30
	},
	"database": {
		"url": "postgres://localhost:5432/mydb",
		"max_connections": 10,
		"enable_ssl": false
	},
	"logging": {
		"level": "info",
		"format": "json",
		"output_path": "/var/log/app.log"
	}
}`

// TODO: 설정 구조체 정의
// - 중첩 구조체 사용 (ServerConfig, DatabaseConfig, LoggingConfig)
// - 적절한 json 태그 사용

type Config struct {
	// TODO: 필드 정의
}

type ServerConfig struct {
	// TODO: 필드 정의
}

type DatabaseConfig struct {
	// TODO: 필드 정의
}

type LoggingConfig struct {
	// TODO: 필드 정의
}

// TODO: 설정 파일 읽기 함수 구현
func LoadConfig(path string) (*Config, error) {
	// TODO:
	// 1. os.Open으로 파일 열기
	// 2. defer로 파일 닫기
	// 3. json.NewDecoder로 파싱
	// 4. 에러 처리 (파일 없음, JSON 파싱 실패 등)
	return nil, fmt.Errorf("not implemented")
}

// TODO: 설정 파일 저장 함수 구현
func SaveConfig(path string, config *Config) error {
	// TODO:
	// 1. os.Create로 파일 생성
	// 2. defer로 파일 닫기
	// 3. json.NewEncoder로 저장
	// 4. SetIndent로 보기 좋게 포맷팅
	return fmt.Errorf("not implemented")
}

func main() {
	// 샘플 설정 파일 생성
	os.WriteFile(configPath, []byte(sampleConfig), 0644)
	defer os.Remove(configPath) // 테스트 후 정리

	// TODO 1: 설정 파일 로드
	// config, err := LoadConfig(configPath)

	// TODO 2: 설정 값 출력
	// fmt.Printf("서버 포트: %d\n", config.Server.Port)

	// TODO 3: 설정 값 수정
	// config.Server.Port = 9090
	// config.Database.MaxConnections = 20

	// TODO 4: 수정된 설정 저장
	// SaveConfig(configPath, config)

	// TODO 5: 다시 로드하여 변경 확인
	// updatedConfig, _ := LoadConfig(configPath)
	// fmt.Printf("변경된 포트: %d\n", updatedConfig.Server.Port)

	fmt.Println("TODO: 설정 파일 처리 구현")
}
