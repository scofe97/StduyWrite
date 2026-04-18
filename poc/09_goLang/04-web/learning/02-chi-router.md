# Chi Router

## 학습 목표

Go-Chi 라우터를 사용하여 net/http 기반의 경량 라우팅 구현

---

## Chi의 특징

### net/http 100% 호환

Chi는 `http.Handler`를 완전히 준수합니다. 기존 net/http 코드와 자연스럽게 통합됩니다.

```go
r := chi.NewRouter()
// chi.Router는 http.Handler를 구현
http.ListenAndServe(":8080", r)
```

### 다른 라우터와 비교

| 특징 | net/http | Chi | Gin |
|------|----------|-----|-----|
| 의존성 | 없음 | 최소 | 많음 |
| URL 파라미터 | 수동 파싱 | `chi.URLParam()` | `c.Param()` |
| 미들웨어 | 수동 래핑 | `r.Use()` | `r.Use()` |
| 라우트 그룹 | 수동 | `r.Route()` | `r.Group()` |

---

## 핵심 개념

### 1. 기본 라우팅

```go
r := chi.NewRouter()

r.Get("/", homeHandler)
r.Post("/users", createUserHandler)
r.Put("/users/{id}", updateUserHandler)
r.Delete("/users/{id}", deleteUserHandler)
```

### 2. URL 파라미터

```go
r.Get("/users/{userID}", func(w http.ResponseWriter, r *http.Request) {
    userID := chi.URLParam(r, "userID")
    // userID 사용
})
```

### 3. 미들웨어

```go
r := chi.NewRouter()

// 전역 미들웨어
r.Use(middleware.Logger)
r.Use(middleware.Recoverer)

// 특정 라우트에만
r.With(authMiddleware).Get("/admin", adminHandler)
```

### 4. 서브라우터 (라우트 그룹)

```go
r.Route("/api/v1", func(r chi.Router) {
    r.Use(apiMiddleware)
    
    r.Route("/users", func(r chi.Router) {
        r.Get("/", listUsers)
        r.Post("/", createUser)
        r.Get("/{id}", getUser)
    })
})
```

### 5. 내장 미들웨어

| 미들웨어 | 역할 |
|----------|------|
| `middleware.Logger` | 요청 로깅 |
| `middleware.Recoverer` | 패닉 복구 |
| `middleware.RequestID` | 요청 ID 주입 |
| `middleware.RealIP` | 프록시 뒤 실제 IP |
| `middleware.Compress` | 응답 압축 |
| `middleware.Timeout` | 요청 타임아웃 |

---

## 미들웨어 작성

```go
func myMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // 요청 전 처리
        ctx := context.WithValue(r.Context(), "key", "value")
        
        // 다음 핸들러 호출
        next.ServeHTTP(w, r.WithContext(ctx))
        
        // 요청 후 처리
    })
}
```

---

## Spring과 비교

| Spring | Chi |
|--------|-----|
| `@PathVariable` | `chi.URLParam()` |
| `@RequestMapping("/api")` | `r.Route("/api", ...)` |
| `FilterChain` | 미들웨어 체인 |
| `Interceptor` | 미들웨어 |

---

## 참고 자료

- [Chi 공식 GitHub](https://github.com/go-chi/chi)
- [Chi 미들웨어 문서](https://pkg.go.dev/github.com/go-chi/chi/middleware)
