package logging

import (
	"os"
	"time"

	"github.com/rs/zerolog"
)

// 전역 로거 인스턴스
var logger zerolog.Logger

// InitLogger는 애플리케이션 로거를 초기화합니다.
// TODO: 로거 초기화 구현
// - 환경에 따라 ConsoleWriter 또는 JSON 출력 선택
// - 로그 레벨 설정 (Debug, Info, Warn, Error)
// - 타임스탬프 포맷 설정
func InitLogger() {
	// 힌트: 개발 환경에서는 ConsoleWriter 사용
	// output := zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.RFC3339}
	// logger = zerolog.New(output).With().Timestamp().Logger()

	// 힌트: 프로덕션 환경에서는 JSON 출력
	// logger = zerolog.New(os.Stdout).With().Timestamp().Logger()
}

// InitLoggerWithLevel은 특정 로그 레벨로 로거를 초기화합니다.
// TODO: 로그 레벨 파라미터 받아서 초기화
func InitLoggerWithLevel(level string) {
	// 힌트: zerolog.SetGlobalLevel(zerolog.InfoLevel)
	// 힌트: level 문자열을 zerolog.Level로 변환
}

// GetLogger는 현재 로거 인스턴스를 반환합니다.
func GetLogger() zerolog.Logger {
	return logger
}

// LogWithContext는 컨텍스트 정보를 포함한 로그를 출력합니다.
// TODO: userId, action, message를 포함한 구조화된 로그 출력
func LogWithContext(userID, action, message string) {
	// 힌트: logger.Info().Str("user_id", userID).Str("action", action).Msg(message)
}

// LogWithFields는 여러 필드를 포함한 로그를 출력합니다.
// TODO: map[string]interface{} 형태의 필드들을 로그에 추가
func LogWithFields(level string, fields map[string]interface{}, message string) {
	// 힌트: zerolog.Dict() 또는 여러 Str/Int 체이닝 사용
}

// CreateSubLogger는 기본 필드가 포함된 서브 로거를 생성합니다.
// TODO: 특정 컴포넌트용 서브 로거 생성
func CreateSubLogger(component string) zerolog.Logger {
	// 힌트: logger.With().Str("component", component).Logger()
	return logger
}

// 샘플 핸들러 함수 (HTTP 미들웨어 테스트용)
func SampleHandler() {
	// 이 함수에서 로깅 테스트
	logger.Info().Msg("Handler executed")
}

// --- 유틸리티 함수 ---

// getLogLevel은 문자열을 zerolog.Level로 변환합니다.
func getLogLevel(level string) zerolog.Level {
	switch level {
	case "debug":
		return zerolog.DebugLevel
	case "info":
		return zerolog.InfoLevel
	case "warn":
		return zerolog.WarnLevel
	case "error":
		return zerolog.ErrorLevel
	default:
		return zerolog.InfoLevel
	}
}

// 임시: 컴파일 에러 방지용
var _ = os.Stdout
var _ = time.Now
