# Go 표준 라이브러리 HTTP 서버

## 학습 목표

net/http 패키지를 사용하여 HTTP 서버의 기초를 이해합니다.

---

## 핵심 개념

### 1. http.Handler 인터페이스

Go HTTP 서버의 핵심은 `http.Handler` 인터페이스입니다.

```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

모든 HTTP 요청 처리는 이 인터페이스를 구현하는 것에서 시작합니다.

### 2. http.HandlerFunc

함수를 핸들러로 변환하는 어댑터입니다.

```go
// 함수 정의
func hello(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello, World!"))
}

// 핸들러로 등록
http.HandleFunc("/hello", hello)
```

### 3. http.ServeMux (라우터)

요청 URL을 핸들러에 매핑하는 기본 라우터입니다.

```go
mux := http.NewServeMux()
mux.HandleFunc("/users", usersHandler)
mux.HandleFunc("/products", productsHandler)

http.ListenAndServe(":8080", mux)
```

### 4. 미들웨어 패턴

핸들러를 감싸서 공통 기능을 추가합니다.

```go
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Printf("%s %s", r.Method, r.URL.Path)
        next.ServeHTTP(w, r)
    })
}
```

### 5. JSON 처리

```go
// 요청 파싱
var user User
json.NewDecoder(r.Body).Decode(&user)

// 응답 작성
w.Header().Set("Content-Type", "application/json")
json.NewEncoder(w).Encode(response)
```

---

## 주요 타입

| 타입 | 역할 |
|------|------|
| `http.ResponseWriter` | 응답 작성 인터페이스 |
| `http.Request` | 요청 정보 구조체 |
| `http.ServeMux` | URL 라우터 |
| `http.Server` | 서버 설정 구조체 |

---

## Spring과 비교

| 항목 | Spring | Go net/http |
|------|--------|-------------|
| 컨트롤러 | `@Controller` | `http.Handler` |
| 라우팅 | `@GetMapping` | `mux.HandleFunc()` |
| 미들웨어 | Filter + Interceptor | 함수 래핑 |
| JSON | `@RequestBody` | `json.Decoder` |

---

## 참고 자료

- [net/http 공식 문서](https://pkg.go.dev/net/http)
