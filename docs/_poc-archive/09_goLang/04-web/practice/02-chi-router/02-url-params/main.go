// Practice 02: URL 파라미터 처리
// 목표: chi.URLParam으로 동적 라우팅 구현

package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

var users = map[int]User{
	1: {ID: 1, Name: "Alice", Email: "alice@example.com"},
	2: {ID: 2, Name: "Bob", Email: "bob@example.com"},
}

func main() {
	r := chi.NewRouter()
	r.Use(middleware.Logger)

	// URL 파라미터 사용
	r.Get("/users/{userID}", func(w http.ResponseWriter, r *http.Request) {
		userIDStr := chi.URLParam(r, "userID")
		userID, err := strconv.Atoi(userIDStr)
		if err != nil {
			http.Error(w, "invalid user id", http.StatusBadRequest)
			return
		}

		user, ok := users[userID]
		if !ok {
			http.Error(w, "user not found", http.StatusNotFound)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(user)
	})

	// 여러 파라미터
	r.Get("/orgs/{orgID}/users/{userID}", func(w http.ResponseWriter, r *http.Request) {
		orgID := chi.URLParam(r, "orgID")
		userID := chi.URLParam(r, "userID")

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{
			"orgID":  orgID,
			"userID": userID,
		})
	})

	// 와일드카드 (*) 사용
	r.Get("/files/*", func(w http.ResponseWriter, r *http.Request) {
		path := chi.URLParam(r, "*")
		fmt.Fprintf(w, "File path: %s", path)
	})

	fmt.Println("Server starting on :8080")
	http.ListenAndServe(":8080", r)
}

// 테스트:
// curl http://localhost:8080/users/1
// curl http://localhost:8080/orgs/acme/users/42
// curl http://localhost:8080/files/documents/report.pdf
