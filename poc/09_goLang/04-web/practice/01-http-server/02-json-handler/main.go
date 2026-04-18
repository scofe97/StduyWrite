// Practice 02: JSON 요청/응답 처리
// 목표: JSON 인코딩/디코딩 구현

package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

type Response struct {
	Success bool        `json:"success"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

func main() {
	mux := http.NewServeMux()

	// GET /users - 사용자 목록 반환
	mux.HandleFunc("GET /users", func(w http.ResponseWriter, r *http.Request) {
		users := []User{
			{ID: 1, Name: "Alice", Email: "alice@example.com"},
			{ID: 2, Name: "Bob", Email: "bob@example.com"},
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(Response{Success: true, Data: users})
	})

	// POST /users - 사용자 생성
	mux.HandleFunc("POST /users", func(w http.ResponseWriter, r *http.Request) {
		var user User
		if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(Response{Success: false, Error: "invalid json"})
			return
		}

		// TODO: 실제로는 DB에 저장
		user.ID = 3

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(Response{Success: true, Data: user})
	})

	fmt.Println("Server starting on :8080")
	http.ListenAndServe(":8080", mux)
}

// 테스트:
// curl http://localhost:8080/users
// curl -X POST http://localhost:8080/users -d '{"name":"Charlie","email":"charlie@example.com"}'
