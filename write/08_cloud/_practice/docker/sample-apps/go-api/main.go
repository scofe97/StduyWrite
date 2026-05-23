// 간단한 Go HTTP API - Docker 실습용
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"
)

// HealthResponse 헬스체크 응답 구조체
type HealthResponse struct {
	Status    string    `json:"status"`
	Timestamp time.Time `json:"timestamp"`
	Version   string    `json:"version"`
}

// HelloResponse hello 엔드포인트 응답 구조체
type HelloResponse struct {
	Message   string    `json:"message"`
	Timestamp time.Time `json:"timestamp"`
}

func main() {
	port := getEnv("PORT", "8080")

	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/hello", helloHandler)
	http.HandleFunc("/", rootHandler)

	log.Printf("Starting server on port %s...", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}

// healthHandler 헬스체크 엔드포인트
func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := HealthResponse{
		Status:    "ok",
		Timestamp: time.Now(),
		Version:   "1.0.0",
	}
	json.NewEncoder(w).Encode(response)
}

// helloHandler hello 엔드포인트
func helloHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := HelloResponse{
		Message:   "Hello Docker!",
		Timestamp: time.Now(),
	}
	json.NewEncoder(w).Encode(response)
}

// rootHandler 루트 엔드포인트
func rootHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("Docker PoC API\nEndpoints: /health, /hello\n"))
}

// getEnv 환경변수 조회 (기본값 제공)
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
