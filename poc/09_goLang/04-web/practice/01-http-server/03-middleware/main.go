// Practice 03: 미들웨어 구현
// 목표: 로깅, 복구, CORS 미들웨어 작성

package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

// 로깅 미들웨어
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		// 다음 핸들러 호출
		next.ServeHTTP(w, r)

		// 요청 완료 후 로깅
		log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
	})
}

// 패닉 복구 미들웨어
func recoveryMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Printf("panic recovered: %v", err)
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

// CORS 미들웨어
func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

// 미들웨어 체인 헬퍼
func chain(h http.Handler, middlewares ...func(http.Handler) http.Handler) http.Handler {
	for i := len(middlewares) - 1; i >= 0; i-- {
		h = middlewares[i](h)
	}
	return h
}

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello with middleware!")
	})

	mux.HandleFunc("/panic", func(w http.ResponseWriter, r *http.Request) {
		panic("something went wrong!")
	})

	// 미들웨어 적용
	handler := chain(mux, recoveryMiddleware, loggingMiddleware, corsMiddleware)

	fmt.Println("Server starting on :8080")
	http.ListenAndServe(":8080", handler)
}

// 테스트:
// curl http://localhost:8080
// curl http://localhost:8080/panic
