package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

// HealthResponse는 /health 엔드포인트의 응답 구조체이다.
type HealthResponse struct {
	Status    string `json:"status"`
	Timestamp string `json:"timestamp"`
	Version   string `json:"version"`
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8081"
	}

	mux := http.NewServeMux()

	// GET / — 메인 페이지
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		fmt.Fprintln(w, "Hello from Jenkins Pipeline!")
	})

	// GET /health — 헬스체크 엔드포인트
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		resp := HealthResponse{
			Status:    "ok",
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Version:   getVersion(),
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(resp)
	})

	addr := ":" + port
	log.Printf("서버 시작: http://localhost%s\n", addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("서버 시작 실패: %v", err)
	}
}

// getVersion은 VERSION 환경변수를 반환한다. 미설정 시 "dev"를 반환한다.
func getVersion() string {
	v := os.Getenv("VERSION")
	if v == "" {
		return "dev"
	}
	return v
}
