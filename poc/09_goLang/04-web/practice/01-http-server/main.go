package main

import (
	"log"
	"net/http"
)

func main() {
	// Step 1: net/http로 기본 서버 만들기
	// Step 2: Gin 프레임워크로 전환

	// 1. 라우터 생성
	mux := http.NewServeMux()

	// 2. 핸들러 등록
	mux.HandleFunc("GET /ping", pingHandler)

	// 3. 서버 시작
	log.Println("Server starting on :8070")
	log.Fatal(http.ListenAndServe(":8070", mux))
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"message": "pong"}`))
}
