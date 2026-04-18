// Practice 04: 라우트 그룹화
// 목표: API 버전별 그룹화 및 인증 미들웨어

package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// 간단한 인증 미들웨어
func authMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		token := r.Header.Get("Authorization")
		if !strings.HasPrefix(token, "Bearer ") {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	})
}

// API 그룹 헬퍼
type RouterGroup struct {
	prefix     string
	mux        *http.ServeMux
	middleware func(http.Handler) http.Handler
}

func NewRouterGroup(mux *http.ServeMux, prefix string) *RouterGroup {
	return &RouterGroup{prefix: prefix, mux: mux}
}

func (g *RouterGroup) Use(mw func(http.Handler) http.Handler) {
	g.middleware = mw
}

func (g *RouterGroup) Handle(pattern string, handler http.HandlerFunc) {
	fullPattern := g.prefix + pattern
	var h http.Handler = handler
	if g.middleware != nil {
		h = g.middleware(h)
	}
	g.mux.Handle(fullPattern, h)
}

func main() {
	mux := http.NewServeMux()

	// Public API (v1)
	v1 := NewRouterGroup(mux, "/api/v1")
	v1.Handle("/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	// Protected API (v1) - 인증 필요
	v1Protected := NewRouterGroup(mux, "/api/v1")
	v1Protected.Use(authMiddleware)
	v1Protected.Handle("/users", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{"user": "authenticated"})
	})

	// API v2
	v2 := NewRouterGroup(mux, "/api/v2")
	v2.Handle("/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status":  "ok",
			"version": "2.0",
		})
	})

	fmt.Println("Server starting on :8080")
	http.ListenAndServe(":8080", mux)
}

// 테스트:
// curl http://localhost:8080/api/v1/health
// curl http://localhost:8080/api/v1/users  # 401 Unauthorized
// curl -H "Authorization: Bearer token" http://localhost:8080/api/v1/users
// curl http://localhost:8080/api/v2/health
