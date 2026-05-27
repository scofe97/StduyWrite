// Practice 01: 기본 HTTP 서버
// 목표: net/http로 간단한 HTTP 서버 구현

package main

import (
	"fmt"
	"net/http"
)

func main() {
	// TODO: "/" 경로에 "Hello, World!" 응답하는 핸들러 등록
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello, World!")
	})

	// TODO: "/health" 경로에 상태 체크 핸들러 등록
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	})

	// 서버 시작
	fmt.Println("Server starting on :8080")
	http.ListenAndServe(":8080", nil)
}

// 실행: go run main.go
// 테스트: curl http://localhost:8080
// 테스트: curl http://localhost:8080/health
