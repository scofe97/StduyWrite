// Practice 03: 미들웨어 체인
// 목표: 여러 미들웨어 조합 및 특정 라우트에만 적용

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

// 커스텀 미들웨어: 요청 시간 측정
func timingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		log.Printf("Request took: %v", time.Since(start))
	})
}

// 커스텀 미들웨어: API Key 인증
func apiKeyAuth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		apiKey := r.Header.Get("X-API-Key")
		if apiKey != "secret-key" {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	})
}

// 커스텀 미들웨어: Context에 값 주입
func userCtx(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx := context.WithValue(r.Context(), "user", "admin")
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

func main() {
	r := chi.NewRouter()

	// 전역 미들웨어 (모든 요청에 적용)
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(timingMiddleware)

	// 공개 라우트
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Public endpoint"))
	})

	// 특정 라우트에만 미들웨어 적용 (With)
	r.With(apiKeyAuth).Get("/protected", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Protected endpoint - you have access!"))
	})

	// 미들웨어 체인 조합
	r.With(apiKeyAuth, userCtx).Get("/admin", func(w http.ResponseWriter, r *http.Request) {
		user := r.Context().Value("user").(string)
		fmt.Fprintf(w, "Admin endpoint - user: %s", user)
	})

	fmt.Println("Server starting on :8080")
	http.ListenAndServe(":8080", r)
}

// 테스트:
// curl http://localhost:8080/
// curl http://localhost:8080/protected  # 401
// curl -H "X-API-Key: secret-key" http://localhost:8080/protected
// curl -H "X-API-Key: secret-key" http://localhost:8080/admin
