# 05. Layered Architecture - 계층형 아키텍처

## 학습 목표

- Transport, Service, Storage 계층 분리
- 인터페이스 기반 의존성 주입
- 관심사 분리 원칙 적용

## 핵심 개념

### 계층 구조

```
┌─────────────────────────────────────┐
│        Transport Layer              │
│  (gRPC Handler - 요청/응답 처리)     │
└─────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         Service Layer               │
│  (비즈니스 로직, 검증)               │
└─────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         Storage Layer               │
│  (데이터 영속성)                     │
└─────────────────────────────────────┘
```

### 각 계층의 책임

| 계층 | 책임 | 의존 방향 |
|------|------|----------|
| Transport | 요청 파싱, 응답 직렬화 | → Service |
| Service | 비즈니스 로직, 검증 | → Storage |
| Storage | 데이터베이스 접근 | - |

## 실습 과제

### Task 1: 타입 정의 (인터페이스)

```go
// orders/types.go
package main

import (
    "context"

    pb "common/api"
)

type OrderService interface {
    CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.Order, error)
    ValidateOrder(ctx context.Context, req *pb.CreateOrderRequest) error
}

type OrderStore interface {
    Create(ctx context.Context, order *pb.Order) error
    Get(ctx context.Context, orderID, customerID string) (*pb.Order, error)
}
```

### Task 2: Storage 구현

```go
// orders/storage.go
package main

import (
    "context"
    "sync"

    pb "common/api"
)

// 메모리 기반 스토어 (개발용)
type memoryStore struct {
    mu     sync.RWMutex
    orders map[string]*pb.Order
}

func NewMemoryStore() *memoryStore {
    return &memoryStore{
        orders: make(map[string]*pb.Order),
    }
}

func (s *memoryStore) Create(ctx context.Context, order *pb.Order) error {
    s.mu.Lock()
    defer s.mu.Unlock()

    s.orders[order.ID] = order
    return nil
}

func (s *memoryStore) Get(ctx context.Context, orderID, customerID string) (*pb.Order, error) {
    s.mu.RLock()
    defer s.mu.RUnlock()

    order, exists := s.orders[orderID]
    if !exists {
        return nil, common.ErrOrderNotFound
    }

    if order.CustomerID != customerID {
        return nil, common.ErrOrderNotFound
    }

    return order, nil
}
```

### Task 3: Service 구현

```go
// orders/service.go
package main

import (
    "context"

    "common"
    pb "common/api"
    "github.com/google/uuid"
)

type service struct {
    store OrderStore
}

func NewService(store OrderStore) *service {
    return &service{store: store}
}

func (s *service) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.Order, error) {
    // 1. 검증
    if err := s.ValidateOrder(ctx, req); err != nil {
        return nil, err
    }

    // 2. 아이템 병합
    mergedItems := s.mergeItems(req.Items)

    // 3. 주문 생성
    order := &pb.Order{
        ID:         uuid.New().String(),
        CustomerID: req.CustomerID,
        Status:     "pending",
        Items:      make([]*pb.Item, 0, len(mergedItems)),
    }

    for _, item := range mergedItems {
        order.Items = append(order.Items, &pb.Item{
            ID:       item.ItemID,
            Quantity: item.Quantity,
        })
    }

    // 4. 저장
    if err := s.store.Create(ctx, order); err != nil {
        return nil, err
    }

    return order, nil
}

func (s *service) ValidateOrder(ctx context.Context, req *pb.CreateOrderRequest) error {
    if len(req.Items) == 0 {
        return common.ErrNoItems
    }

    for _, item := range req.Items {
        if item.ItemID == "" {
            return common.ErrInvalidItem
        }
        if item.Quantity <= 0 {
            return common.ErrInvalidItem
        }
    }

    return nil
}

// 중복 아이템 병합
func (s *service) mergeItems(items []*pb.ItemsWithQuantity) []*pb.ItemsWithQuantity {
    merged := make(map[string]int32)

    for _, item := range items {
        merged[item.ItemID] += item.Quantity
    }

    result := make([]*pb.ItemsWithQuantity, 0, len(merged))
    for id, qty := range merged {
        result = append(result, &pb.ItemsWithQuantity{
            ItemID:   id,
            Quantity: qty,
        })
    }

    return result
}
```

### Task 4: Transport (Handler) 수정

```go
// orders/grpc_handler.go (수정)
package main

import (
    "context"
    "log"

    pb "common/api"
    "google.golang.org/grpc"
)

type grpcHandler struct {
    pb.UnimplementedOrderServiceServer
    service OrderService  // 서비스 주입
}

func NewGRPCHandler(grpcServer *grpc.Server, service OrderService) {
    handler := &grpcHandler{service: service}
    pb.RegisterOrderServiceServer(grpcServer, handler)
}

func (h *grpcHandler) CreateOrder(ctx context.Context, p *pb.CreateOrderRequest) (*pb.Order, error) {
    log.Printf("CreateOrder: customerID=%s, items=%d\n", p.CustomerID, len(p.Items))

    // 서비스 레이어에 위임
    return h.service.CreateOrder(ctx, p)
}
```

### Task 5: 공통 에러 정의

```go
// common/errors.go
package common

import "errors"

var (
    ErrNoItems       = errors.New("items must have at least one item")
    ErrInvalidItem   = errors.New("invalid item")
    ErrOrderNotFound = errors.New("order not found")
)
```

### Task 6: Main 수정 (의존성 조립)

```go
// orders/main.go (수정)
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

    lis, err := net.Listen("tcp", grpcAddr)
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    defer lis.Close()

    grpcServer := grpc.NewServer()

    // 의존성 조립 (Composition Root)
    store := NewMemoryStore()
    svc := NewService(store)
    NewGRPCHandler(grpcServer, svc)

    log.Printf("gRPC server started at %s\n", grpcAddr)
    if err := grpcServer.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

## 아키텍처 다이어그램

```
main.go (Composition Root)
    │
    ├── store := NewMemoryStore()
    │       │
    │       └── OrderStore interface
    │
    ├── svc := NewService(store)
    │       │
    │       └── OrderService interface
    │
    └── NewGRPCHandler(server, svc)
            │
            └── grpcHandler struct
                    │
                    └── pb.UnimplementedOrderServiceServer
```

## 체크리스트

- [ ] types.go - 인터페이스 정의
- [ ] storage.go - 메모리 스토어 구현
- [ ] service.go - 비즈니스 로직 구현
- [ ] grpc_handler.go - 서비스 주입
- [ ] common/errors.go - 공통 에러
- [ ] main.go - 의존성 조립
- [ ] 통합 테스트

## 다음 단계

→ 06-service-comm: 서비스 간 통신 (Orders → Stock)
