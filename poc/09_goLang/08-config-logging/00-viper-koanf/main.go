package main

import (
	"fmt"
	"koanf-learning/config"
)

func main() {
	// TODO: 설정 로드
	// cfg, err := config.Load("configs/config.yaml")
	// if err != nil {
	//     log.Fatalf("Failed to load config: %v", err)
	// }

	// TODO: 설정 값 출력
	// fmt.Printf("Server Port: %d\n", cfg.Server.Port)
	// fmt.Printf("Database Host: %s\n", cfg.Database.Host)
	// fmt.Printf("Log Level: %s\n", cfg.Log.Level)

	// TODO: 환경변수 오버라이드 테스트
	// APP_SERVER_PORT=9090 go run main.go
	// → Server Port가 9090으로 변경되어야 함

	// TODO: 다중 환경 설정 테스트
	// cfg, err := config.LoadWithEnv("configs/config.yaml", "dev")
	// → config.dev.yaml의 값이 병합됨

	_ = config.Load // 임시: import 에러 방지
	fmt.Println("koanf learning module")
}
