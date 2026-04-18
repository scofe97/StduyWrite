# 02. Gateway HTTP - HTTP 서버 구현

## 학습 목표

- Go 1.22+ HTTP 라우팅 패턴
- JSON 헬퍼 함수 구현
- 환경 변수 기반 설정

## 핵심 개념

### Go 1.22+ HTTP 라우팅

```go
// 새로운 패턴: METHOD /path
mux.HandleFunc("POST /api/customers/{customerID}/orders", h.handleCreateOrder)
mux.HandleFunc("GET /api/orders/{orderID}", h.handleGetOrder)

// 경로 파라미터 추출
customerID := r.PathValue("customerID")
```

### JSON 헬퍼 패턴

모든 서비스에서 재사용 가능한 JSON 헬퍼:

```go
// 응답 작성
WriteJSON(w, http.StatusOK, data)

// 요청 파싱
ReadJSON(r, &items)

// 에러 응답
WriteError(w, http.StatusBadRequest, "invalid request")
```

## 실습 과제

### Task 1: JSON 헬퍼 작성

```go
// common/json.go
package common

import (
    "encoding/json"
    "net/http"
)

func WriteJSON(w http.ResponseWriter, status int, data any) error {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    return json.NewEncoder(w).Encode(data)
}

func ReadJSON(r *http.Request, data any) error {
    return json.NewDecoder(r.Body).Decode(data)
}

func WriteError(w http.ResponseWriter, status int, message string) error {
    return WriteJSON(w, status, map[string]string{"error": message})
}
```

### Task 2: HTTP Handler 구조체

```go
// gateway/http_handler.go
package main

import "net/http"

type Handler struct {
    // 나중에 gRPC 클라이언트 추가
}

func NewHandler() *Handler {
    return &Handler{}
}

func (h *Handler) RegisterRoutes(mux *http.ServeMux) {
    mux.HandleFunc("POST /api/customers/{customerID}/orders", h.handleCreateOrder)
    mux.HandleFunc("GET /api/orders/{orderID}", h.handleGetOrder)
}
```

### Task 3: Handler 메서드 구현

```go
// gateway/http_handler.go (계속)
func (h *Handler) handleCreateOrder(w http.ResponseWriter, r *http.Request) {
    customerID := r.PathValue("customerID")

    var items []struct {
        ItemID   string `json:"item_id"`
        Quantity int    `json:"quantity"`
    }

    if err := common.ReadJSON(r, &items); err != nil {
        common.WriteError(w, http.StatusBadRequest, err.Error())
        return
    }

    // TODO: gRPC 호출

    common.WriteJSON(w, http.StatusOK, map[string]any{
        "message":     "order created",
        "customer_id": customerID,
        "items":       items,
    })
}

func (h *Handler) handleGetOrder(w http.ResponseWriter, r *http.Request) {
    orderID := r.PathValue("orderID")

    common.WriteJSON(w, http.StatusOK, map[string]any{
        "order_id": orderID,
        "status":   "pending",
    })
}
```

### Task 4: 메인 함수

```go
// gateway/main.go
package main

import (
    "common"
    "log"
    "net/http"

    "github.com/joho/godotenv"
)

func main() {
    godotenv.Load()

    httpAddr := common.EnvString("HTTP_ADDR", ":8080")

    mux := http.NewServeMux()
    handler := NewHandler()
    handler.RegisterRoutes(mux)

    log.Printf("Gateway started at %s\n", httpAddr)
    if err := http.ListenAndServe(httpAddr, mux); err != nil {
        log.Fatal(err)
    }
}
```

### Task 5: 환경 변수 파일

```bash
# gateway/.env
HTTP_ADDR=:8080
```

## 테스트 방법

```bash
# 서버 실행
cd gateway
go run .

# 다른 터미널에서 테스트
curl -X POST http://localhost:8080/api/customers/123/orders \
  -H "Content-Type: application/json" \
  -d '[{"item_id":"item1","quantity":2}]'
```

## 체크리스트

- [ ] common/json.go 작성
- [ ] Handler 구조체 및 RegisterRoutes 구현
- [ ] handleCreateOrder, handleGetOrder 구현
- [ ] main.go 작성
- [ ] curl로 테스트

## 다음 단계

→ 03-grpc-basics: gRPC 및 Protocol Buffers
