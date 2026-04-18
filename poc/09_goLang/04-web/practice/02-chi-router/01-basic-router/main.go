// Practice 01: Chi 기본 라우팅
// 목표: Chi 라우터의 기본 사용법 이해

package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func main() {
	r := chi.NewRouter()

	// 기본 미들웨어
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	// 기본 라우트
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Welcome to Chi!"))
	})

	// JSON 응답
	r.Get("/api/status", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{
			"status": "ok",
			"router": "chi",
		})
	})

	// 메서드별 라우트
	r.Post("/api/echo", func(w http.ResponseWriter, r *http.Request) {
		var body map[string]interface{}
		json.NewDecoder(r.Body).Decode(&body)
		json.NewEncoder(w).Encode(body)
	})

	fmt.Println("Server starting on :8080")
	http.ListenAndServe(":8080", r)
}

// go mod init chi-practice
// go get github.com/go-chi/chi/v5
// go run main.go
