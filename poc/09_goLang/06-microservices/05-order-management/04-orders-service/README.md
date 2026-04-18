# 04. Orders Service - gRPC 서버 구현

## 학습 목표

- gRPC 서버 구현
- UnimplementedServer 패턴 이해
- gRPC 핸들러 작성

## 핵심 개념

### UnimplementedServer 패턴

gRPC Go에서는 forward compatibility를 위해 `UnimplementedXxxServer`를 임베딩합니다:

```go
type grpcHandler struct {
    pb.UnimplementedOrderServiceServer
    // 추가 필드
}
```

### 서버 등록 패턴

```go
grpcServer := grpc.NewServer()
pb.RegisterOrderServiceServer(grpcServer, handler)
```

## 실습 과제

### Task 1: gRPC 핸들러 구조체

```go
// orders/grpc_handler.go
package main

import (
    "context"
    "log"

    pb "common/api"
)

type grpcHandler struct {
    pb.UnimplementedOrderServiceServer
    // 나중에 서비스 주입
}

func NewGRPCHandler(grpcServer *grpc.Server) {
    handler := &grpcHandler{}
    pb.RegisterOrderServiceServer(grpcServer, handler)
}
```

### Task 2: CreateOrder 구현

```go
// orders/grpc_handler.go (계속)
func (h *grpcHandler) CreateOrder(ctx context.Context, p *pb.CreateOrderRequest) (*pb.Order, error) {
    log.Printf("New order received: customerID=%s, items=%v\n", p.CustomerID, p.Items)

    // 임시 구현 - 나중에 서비스 레이어 추가
    order := &pb.Order{
        ID:         "order-123",
        CustomerID: p.CustomerID,
        Status:     "pending",
        Items:      make([]*pb.Item, 0),
    }

    for _, item := range p.Items {
        order.Items = append(order.Items, &pb.Item{
            ID:       item.ItemID,
            Quantity: item.Quantity,
        })
    }

    return order, nil
}
```

### Task 3: 메인 함수

```go
// orders/main.go
package main

import (
    "common"
    "log"
    "net"

    "github.com/joho/godotenv"
    "google.golang.org/grpc"
)

func main() {
    godotenv.Load()

    grpcAddr := common.EnvString("GRPC_ADDR", ":2000")

    // TCP 리스너 생성
    lis, err := net.Listen("tcp", grpcAddr)
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    defer lis.Close()

    // gRPC 서버 생성
    grpcServer := grpc.NewServer()

    // 핸들러 등록
    NewGRPCHandler(grpcServer)

    log.Printf("gRPC server started at %s\n", grpcAddr)
    if err := grpcServer.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

### Task 4: 환경 변수

```bash
# orders/.env
GRPC_ADDR=:2000
```

### Task 5: Gateway에서 클라이언트 연결

```go
// gateway/main.go (수정)
package main

import (
    "common"
    pb "common/api"
    "log"
    "net/http"

    "github.com/joho/godotenv"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
)

func main() {
    godotenv.Load()

    httpAddr := common.EnvString("HTTP_ADDR", ":8080")
    ordersAddr := common.EnvString("ORDERS_ADDR", "localhost:2000")

    // Orders 서비스에 gRPC 연결
    conn, err := grpc.Dial(ordersAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err != nil {
        log.Fatalf("failed to connect to orders service: %v", err)
    }
    defer conn.Close()

    log.Printf("Connected to orders service at %s\n", ordersAddr)

    // gRPC 클라이언트 생성
    orderClient := pb.NewOrderServiceClient(conn)

    mux := http.NewServeMux()
    handler := NewHandler(orderClient)
    handler.RegisterRoutes(mux)

    log.Printf("Gateway started at %s\n", httpAddr)
    if err := http.ListenAndServe(httpAddr, mux); err != nil {
        log.Fatal(err)
    }
}
```

### Task 6: Handler에서 gRPC 호출

```go
// gateway/http_handler.go (수정)
type Handler struct {
    orderClient pb.OrderServiceClient
}

func NewHandler(orderClient pb.OrderServiceClient) *Handler {
    return &Handler{orderClient: orderClient}
}

func (h *Handler) handleCreateOrder(w http.ResponseWriter, r *http.Request) {
    customerID := r.PathValue("customerID")

    var items []*pb.ItemsWithQuantity
    if err := common.ReadJSON(r, &items); err != nil {
        common.WriteError(w, http.StatusBadRequest, err.Error())
        return
    }

    // gRPC 호출
    order, err := h.orderClient.CreateOrder(r.Context(), &pb.CreateOrderRequest{
        CustomerID: customerID,
        Items:      items,
    })
    if err != nil {
        common.WriteError(w, http.StatusInternalServerError, err.Error())
        return
    }

    common.WriteJSON(w, http.StatusOK, order)
}
```

## 테스트 방법

```bash
# 터미널 1: Orders 서비스
cd orders
go run .

# 터미널 2: Gateway
cd gateway
go run .

# 터미널 3: 테스트
curl -X POST http://localhost:8080/api/customers/123/orders \
  -H "Content-Type: application/json" \
  -d '[{"itemID":"item1","quantity":2}]'
```

## 체크리스트

- [ ] grpc_handler.go 작성
- [ ] CreateOrder 구현
- [ ] orders/main.go 작성
- [ ] Gateway에서 gRPC 클라이언트 연결
- [ ] Handler에서 gRPC 호출
- [ ] 통합 테스트

## 다음 단계

→ 05-layered-arch: 계층형 아키텍처 적용
