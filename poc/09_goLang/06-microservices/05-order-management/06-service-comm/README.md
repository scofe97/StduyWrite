# 06. Service Communication - 서비스 간 통신

## 학습 목표

- 서비스 간 gRPC 통신 구현
- Stock 서비스 추가
- Orders에서 Stock 호출

## 핵심 개념

### 서비스 간 통신 흐름

```
Client → Gateway → Orders → Stock
           │          │        │
           │          └────────┘
           │             gRPC
           └──────────────────────
                   HTTP
```

### Stock 서비스 역할

- 재고 확인
- 가격 정보 제공
- 아이템 유효성 검증

## 실습 과제

### Task 1: Proto 확장 (Stock 서비스)

```protobuf
// common/api/order_management_system.proto (추가)
service StockService {
    rpc CheckStock(CheckStockRequest) returns (CheckStockResponse);
    rpc GetItems(GetItemsRequest) returns (GetItemsResponse);
}

message CheckStockRequest {
    repeated ItemsWithQuantity items = 1;
}

message CheckStockResponse {
    bool inStock = 1;
    repeated Item items = 2;
}

message GetItemsRequest {
    repeated string itemIDs = 1;
}

message GetItemsResponse {
    repeated Item items = 1;
}
```

### Task 2: 코드 재생성

```bash
cd common
make gen
```

### Task 3: Stock 서비스 생성

```bash
# 디렉토리 생성
mkdir stock
cd stock
go mod init stock

# go.work에 추가
cd ..
go work use ./stock
```

### Task 4: Stock 핸들러 구현

```go
// stock/grpc_handler.go
package main

import (
    "context"
    "log"

    pb "common/api"
    "google.golang.org/grpc"
)

type grpcHandler struct {
    pb.UnimplementedStockServiceServer
}

func NewGRPCHandler(grpcServer *grpc.Server) {
    handler := &grpcHandler{}
    pb.RegisterStockServiceServer(grpcServer, handler)
}

// 하드코딩된 아이템 데이터 (실제로는 DB)
var items = map[string]*pb.Item{
    "item1": {ID: "item1", Name: "Burger", Quantity: 100, PriceID: "price_burger"},
    "item2": {ID: "item2", Name: "Fries", Quantity: 50, PriceID: "price_fries"},
    "item3": {ID: "item3", Name: "Drink", Quantity: 200, PriceID: "price_drink"},
}

func (h *grpcHandler) CheckStock(ctx context.Context, req *pb.CheckStockRequest) (*pb.CheckStockResponse, error) {
    log.Printf("CheckStock: items=%v\n", req.Items)

    result := &pb.CheckStockResponse{
        InStock: true,
        Items:   make([]*pb.Item, 0),
    }

    for _, reqItem := range req.Items {
        item, exists := items[reqItem.ItemID]
        if !exists {
            result.InStock = false
            continue
        }

        if item.Quantity < reqItem.Quantity {
            result.InStock = false
        }

        result.Items = append(result.Items, &pb.Item{
            ID:       item.ID,
            Name:     item.Name,
            Quantity: reqItem.Quantity,
            PriceID:  item.PriceID,
        })
    }

    return result, nil
}

func (h *grpcHandler) GetItems(ctx context.Context, req *pb.GetItemsRequest) (*pb.GetItemsResponse, error) {
    log.Printf("GetItems: itemIDs=%v\n", req.ItemIDs)

    result := &pb.GetItemsResponse{
        Items: make([]*pb.Item, 0),
    }

    for _, id := range req.ItemIDs {
        if item, exists := items[id]; exists {
            result.Items = append(result.Items, item)
        }
    }

    return result, nil
}
```

### Task 5: Stock 메인

```go
// stock/main.go
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

    grpcAddr := common.EnvString("GRPC_ADDR", ":2001")

    lis, err := net.Listen("tcp", grpcAddr)
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    defer lis.Close()

    grpcServer := grpc.NewServer()
    NewGRPCHandler(grpcServer)

    log.Printf("Stock service started at %s\n", grpcAddr)
    if err := grpcServer.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

### Task 6: Orders에서 Stock 호출

```go
// orders/service.go (수정)
type service struct {
    store       OrderStore
    stockClient pb.StockServiceClient  // 추가
}

func NewService(store OrderStore, stockClient pb.StockServiceClient) *service {
    return &service{
        store:       store,
        stockClient: stockClient,
    }
}

func (s *service) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.Order, error) {
    // 1. 기본 검증
    if err := s.ValidateOrder(ctx, req); err != nil {
        return nil, err
    }

    // 2. 아이템 병합
    mergedItems := s.mergeItems(req.Items)

    // 3. Stock 서비스에서 재고 확인 및 아이템 정보 가져오기
    stockResp, err := s.stockClient.CheckStock(ctx, &pb.CheckStockRequest{
        Items: mergedItems,
    })
    if err != nil {
        return nil, fmt.Errorf("stock check failed: %w", err)
    }

    if !stockResp.InStock {
        return nil, errors.New("some items are out of stock")
    }

    // 4. 주문 생성 (Stock에서 받은 아이템 정보 사용)
    order := &pb.Order{
        ID:         uuid.New().String(),
        CustomerID: req.CustomerID,
        Status:     "pending",
        Items:      stockResp.Items,  // 가격 정보 포함
    }

    // 5. 저장
    if err := s.store.Create(ctx, order); err != nil {
        return nil, err
    }

    return order, nil
}
```

### Task 7: Orders Main 수정

```go
// orders/main.go (수정)
func main() {
    godotenv.Load()

    grpcAddr := common.EnvString("GRPC_ADDR", ":2000")
    stockAddr := common.EnvString("STOCK_ADDR", "localhost:2001")

    // Stock 서비스 연결
    stockConn, err := grpc.Dial(stockAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err != nil {
        log.Fatalf("failed to connect to stock service: %v", err)
    }
    defer stockConn.Close()

    stockClient := pb.NewStockServiceClient(stockConn)
    log.Printf("Connected to stock service at %s\n", stockAddr)

    lis, err := net.Listen("tcp", grpcAddr)
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    defer lis.Close()

    grpcServer := grpc.NewServer()

    store := NewMemoryStore()
    svc := NewService(store, stockClient)
    NewGRPCHandler(grpcServer, svc)

    log.Printf("Orders service started at %s\n", grpcAddr)
    if err := grpcServer.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

## 테스트 방법

```bash
# 터미널 1: Stock 서비스
cd stock && go run .

# 터미널 2: Orders 서비스
cd orders && go run .

# 터미널 3: Gateway
cd gateway && go run .

# 터미널 4: 테스트
curl -X POST http://localhost:8080/api/customers/123/orders \
  -H "Content-Type: application/json" \
  -d '[{"itemID":"item1","quantity":2},{"itemID":"item2","quantity":1}]'
```

## 아키텍처

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Gateway │────>│ Orders  │────>│  Stock  │
│  :8080  │     │  :2000  │     │  :2001  │
└─────────┘     └─────────┘     └─────────┘
    HTTP           gRPC           gRPC
```

## 체크리스트

- [ ] Proto에 StockService 추가
- [ ] make gen 실행
- [ ] stock/ 모듈 생성
- [ ] Stock 핸들러 구현
- [ ] Orders에서 Stock 클라이언트 추가
- [ ] 3개 서비스 통합 테스트

## 다음 단계

→ 07-validation: 에러 핸들링 고도화
