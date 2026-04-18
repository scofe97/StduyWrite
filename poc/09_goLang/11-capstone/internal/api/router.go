package api

import (
	"database/sql"
	"net/http"
	"time"

	"blog-api/internal/api/handlers"

	"github.com/go-chi/chi/v5"
	"github.com/rs/zerolog"
)

// NewRouter는 API 라우터를 생성합니다.
// TODO: 라우터 구현
func NewRouter(db *sql.DB, logger zerolog.Logger) http.Handler {
	r := chi.NewRouter()

	// 미들웨어
	r.Use(loggerMiddleware(logger))
	r.Use(recovererMiddleware(logger))

	// 핸들러 생성
	h := handlers.NewHandler(db, logger)

	// 라우트 정의
	r.Get("/health", healthHandler)

	r.Route("/api/posts", func(r chi.Router) {
		r.Get("/", h.ListPosts)
		r.Post("/", h.CreatePost)

		r.Route("/{id}", func(r chi.Router) {
			r.Get("/", h.GetPost)
			r.Put("/", h.UpdatePost)
			r.Delete("/", h.DeletePost)

			// 상태 변경 액션
			r.Post("/publish", h.PublishPost)
			r.Post("/archive", h.ArchivePost)
		})
	})

	return r
}

// healthHandler는 헬스 체크 핸들러입니다.
func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"status":"ok"}`))
}

// loggerMiddleware는 요청 로깅 미들웨어입니다.
func loggerMiddleware(logger zerolog.Logger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()

			// 응답 래퍼
			wrapped := &responseWriter{ResponseWriter: w, status: http.StatusOK}

			next.ServeHTTP(wrapped, r)

			logger.Info().
				Str("method", r.Method).
				Str("path", r.URL.Path).
				Int("status", wrapped.status).
				Dur("duration", time.Since(start)).
				Msg("Request handled")
		})
	}
}

// recovererMiddleware는 패닉 복구 미들웨어입니다.
func recovererMiddleware(logger zerolog.Logger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			defer func() {
				if err := recover(); err != nil {
					logger.Error().
						Interface("panic", err).
						Str("path", r.URL.Path).
						Msg("Panic recovered")

					http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				}
			}()

			next.ServeHTTP(w, r)
		})
	}
}

type responseWriter struct {
	http.ResponseWriter
	status int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.status = code
	rw.ResponseWriter.WriteHeader(code)
}
