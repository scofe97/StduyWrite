// Practice 04: 서브라우터
// 목표: r.Route()로 라우트 그룹화 및 중첩

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
	r.Use(middleware.Logger)

	// 루트 라우트
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("API Server"))
	})

	// API v1 그룹
	r.Route("/api/v1", func(r chi.Router) {
		// v1 전용 미들웨어
		r.Use(func(next http.Handler) http.Handler {
			return http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) {
				w.Header().Set("X-API-Version", "v1")
				next.ServeHTTP(w, req)
			})
		})

		// /api/v1/users
		r.Route("/users", func(r chi.Router) {
			r.Get("/", listUsers)
			r.Post("/", createUser)
			r.Get("/{id}", getUser)
			r.Put("/{id}", updateUser)
			r.Delete("/{id}", deleteUser)
		})

		// /api/v1/products
		r.Route("/products", func(r chi.Router) {
			r.Get("/", listProducts)
			r.Get("/{id}", getProduct)
		})
	})

	// API v2 그룹
	r.Route("/api/v2", func(r chi.Router) {
		r.Use(func(next http.Handler) http.Handler {
			return http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) {
				w.Header().Set("X-API-Version", "v2")
				next.ServeHTTP(w, req)
			})
		})

		r.Get("/users", func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(map[string]interface{}{
				"version": "v2",
				"users":   []string{"alice", "bob"},
			})
		})
	})

	fmt.Println("Server starting on :8080")
	http.ListenAndServe(":8080", r)
}

// 핸들러 함수들
func listUsers(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode([]map[string]interface{}{
		{"id": 1, "name": "Alice"},
		{"id": 2, "name": "Bob"},
	})
}

func createUser(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusCreated)
	w.Write([]byte("User created"))
}

func getUser(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")
	json.NewEncoder(w).Encode(map[string]string{"id": id, "name": "Alice"})
}

func updateUser(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("User updated"))
}

func deleteUser(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNoContent)
}

func listProducts(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode([]map[string]interface{}{
		{"id": 1, "name": "Product A"},
	})
}

func getProduct(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")
	json.NewEncoder(w).Encode(map[string]string{"id": id})
}

// 테스트:
// curl http://localhost:8080/api/v1/users
// curl http://localhost:8080/api/v1/users/1
// curl http://localhost:8080/api/v1/products
// curl http://localhost:8080/api/v2/users
