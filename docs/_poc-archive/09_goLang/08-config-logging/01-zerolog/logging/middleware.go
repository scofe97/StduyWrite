package logging

import (
	"net/http"
	"time"

	"github.com/rs/zerolog"
)

// RequestLogger는 HTTP 요청을 로깅하는 미들웨어입니다.
// TODO: 요청 시작/종료 시간, 상태 코드, 경로를 로깅하는 미들웨어 구현
func RequestLogger(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		// TODO: 요청 시작 로그
		// logger.Info().
		//     Str("method", r.Method).
		//     Str("path", r.URL.Path).
		//     Msg("Request started")

		// 응답 상태 코드를 캡처하기 위한 래퍼
		wrapped := &responseWriter{ResponseWriter: w, status: http.StatusOK}

		// 다음 핸들러 실행
		next.ServeHTTP(wrapped, r)

		// TODO: 요청 완료 로그
		// logger.Info().
		//     Str("method", r.Method).
		//     Str("path", r.URL.Path).
		//     Int("status", wrapped.status).
		//     Dur("duration", time.Since(start)).
		//     Msg("Request completed")

		_ = start // 임시: 컴파일 에러 방지
	}
}

// responseWriter는 상태 코드를 캡처하기 위한 래퍼입니다.
type responseWriter struct {
	http.ResponseWriter
	status int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.status = code
	rw.ResponseWriter.WriteHeader(code)
}

// ChainedMiddleware는 여러 미들웨어를 체이닝합니다.
// TODO: 미들웨어 체이닝 구현 (선택)
func ChainedMiddleware(middlewares ...func(http.HandlerFunc) http.HandlerFunc) func(http.HandlerFunc) http.HandlerFunc {
	return func(final http.HandlerFunc) http.HandlerFunc {
		for i := len(middlewares) - 1; i >= 0; i-- {
			final = middlewares[i](final)
		}
		return final
	}
}

// ContextLogger는 요청별 컨텍스트 로거를 생성합니다.
// TODO: 요청 ID를 포함한 컨텍스트 로거 구현
func ContextLogger(requestID string) zerolog.Logger {
	// 힌트: logger.With().Str("request_id", requestID).Logger()
	return logger
}

// RecoveryMiddleware는 패닉을 복구하고 로깅하는 미들웨어입니다.
// TODO: 패닉 복구 및 에러 로깅 구현 (선택)
func RecoveryMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				// TODO: 패닉 로깅
				// logger.Error().
				//     Interface("panic", err).
				//     Str("path", r.URL.Path).
				//     Msg("Panic recovered")

				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			}
		}()

		next.ServeHTTP(w, r)
	}
}
