package main

import (
	"zerolog-learning/logging"
)

func main() {
	// TODO: 로거 초기화
	// logging.InitLogger()

	// TODO: 다양한 로그 레벨 테스트
	// logger := logging.GetLogger()
	// logger.Info().Msg("Application started")
	// logger.Debug().Str("module", "main").Msg("Debug message")
	// logger.Warn().Int("retry", 3).Msg("Connection retry")
	// logger.Error().Err(errors.New("sample error")).Msg("Error occurred")

	// TODO: 컨텍스트 로깅 테스트
	// logging.LogWithContext("user-123", "login", "User logged in")

	// TODO: HTTP 서버로 미들웨어 테스트 (선택)
	// http.HandleFunc("/", logging.RequestLogger(homeHandler))
	// http.ListenAndServe(":8080", nil)

	_ = logging.GetLogger // 임시: import 에러 방지
}
