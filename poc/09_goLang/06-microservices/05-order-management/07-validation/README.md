# 07. Validation & Error Handling - 검증 및 에러 처리

## 학습 목표

- gRPC 에러 핸들링 패턴
- 이중 검증 전략
- 에러 매핑 (gRPC → HTTP)

## 핵심 개념

### gRPC 상태 코드

| 코드 | 의미 | HTTP 매핑 |
|------|------|-----------|
| OK | 성공 | 200 |
| InvalidArgument | 잘못된 인자 | 400 |
| NotFound | 리소스 없음 | 404 |
| AlreadyExists | 이미 존재 | 409 |
| PermissionDenied | 권한 없음 | 403 |
| Internal | 내부 오류 | 500 |
| Unavailable | 서비스 불가 | 503 |

### 이중 검증 전략

```
Gateway (빠른 실패)     Orders (비즈니스 규칙)
     │                       │
     ├── 필수 필드 검사       ├── 아이템 병합
     ├── 형식 검증            ├── 재고 확인 (Stock 호출)
     └── 빈 배열 체크          └── 비즈니스 규칙 검증
```

## 실습 과제

### Task 1: Orders에서 gRPC 에러 반환

```go
// orders/grpc_handler.go (수정)
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

func (h *grpcHandler) CreateOrder(ctx context.Context, p *pb.CreateOrderRequest) (*pb.Order, error) {
    log.Printf("CreateOrder: customerID=%s, items=%d\n", p.CustomerID, len(p.Items))

    order, err := h.service.CreateOrder(ctx, p)
    if err != nil {
        // 에러 유형에 따라 적절한 gRPC 상태 코드 반환
        switch {
        case errors.Is(err, common.ErrNoItems):
            return nil, status.Error(codes.InvalidArgument, err.Error())
        case errors.Is(err, common.ErrInvalidItem):
            return nil, status.Error(codes.InvalidArgument, err.Error())
        case errors.Is(err, common.ErrOutOfStock):
            return nil, status.Error(codes.FailedPrecondition, err.Error())
        default:
            return nil, status.Error(codes.Internal, "internal server error")
        }
    }

    return order, nil
}
```

### Task 2: Gateway에서 gRPC 에러 처리

```go
// gateway/http_handler.go (수정)
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

func (h *Handler) handleCreateOrder(w http.ResponseWriter, r *http.Request) {
    customerID := r.PathValue("customerID")

    // 1. Gateway 레벨 검증
    var items []*pb.ItemsWithQuantity
    if err := common.ReadJSON(r, &items); err != nil {
        common.WriteError(w, http.StatusBadRequest, "invalid JSON body")
        return
    }

    if err := validateItems(items); err != nil {
        common.WriteError(w, http.StatusBadRequest, err.Error())
        return
    }

    // 2. gRPC 호출
    order, err := h.orderClient.CreateOrder(r.Context(), &pb.CreateOrderRequest{
        CustomerID: customerID,
        Items:      items,
    })

    if err != nil {
        // 3. gRPC 에러를 HTTP 에러로 변환
        handleGRPCError(w, err)
        return
    }

    common.WriteJSON(w, http.StatusOK, order)
}

// Gateway 레벨 검증
func validateItems(items []*pb.ItemsWithQuantity) error {
    if len(items) == 0 {
        return errors.New("items must have at least one item")
    }

    for _, item := range items {
        if item.ItemID == "" {
            return errors.New("item ID is required")
        }
        if item.Quantity <= 0 {
            return errors.New("quantity must be positive")
        }
    }

    return nil
}

// gRPC 에러 → HTTP 에러 변환
func handleGRPCError(w http.ResponseWriter, err error) {
    errStatus := status.Convert(err)

    var httpStatus int
    switch errStatus.Code() {
    case codes.InvalidArgument:
        httpStatus = http.StatusBadRequest
    case codes.NotFound:
        httpStatus = http.StatusNotFound
    case codes.FailedPrecondition:
        httpStatus = http.StatusConflict
    case codes.PermissionDenied:
        httpStatus = http.StatusForbidden
    case codes.Unauthenticated:
        httpStatus = http.StatusUnauthorized
    case codes.Unavailable:
        httpStatus = http.StatusServiceUnavailable
    default:
        httpStatus = http.StatusInternalServerError
    }

    common.WriteError(w, httpStatus, errStatus.Message())
}
```

### Task 3: 공통 에러 확장

```go
// common/errors.go (확장)
package common

import "errors"

var (
    ErrNoItems       = errors.New("items must have at least one item")
    ErrInvalidItem   = errors.New("invalid item")
    ErrOrderNotFound = errors.New("order not found")
    ErrOutOfStock    = errors.New("some items are out of stock")
    ErrItemNotFound  = errors.New("item not found")
)
```

### Task 4: Service 에러 개선

```go
// orders/service.go (에러 처리 개선)
func (s *service) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.Order, error) {
    // 1. 검증
    if err := s.ValidateOrder(ctx, req); err != nil {
        return nil, err
    }

    // 2. 아이템 병합
    mergedItems := s.mergeItems(req.Items)

    // 3. Stock 확인
    stockResp, err := s.stockClient.CheckStock(ctx, &pb.CheckStockRequest{
        Items: mergedItems,
    })
    if err != nil {
        // Stock 서비스 호출 실패
        return nil, fmt.Errorf("failed to check stock: %w", err)
    }

    if !stockResp.InStock {
        return nil, common.ErrOutOfStock
    }

    // 4. 주문 생성
    order := &pb.Order{
        ID:         uuid.New().String(),
        CustomerID: req.CustomerID,
        Status:     "pending",
        Items:      stockResp.Items,
    }

    // 5. 저장
    if err := s.store.Create(ctx, order); err != nil {
        return nil, fmt.Errorf("failed to create order: %w", err)
    }

    return order, nil
}
```

### Task 5: Stock 에러 핸들링

```go
// stock/grpc_handler.go (에러 핸들링 추가)
func (h *grpcHandler) CheckStock(ctx context.Context, req *pb.CheckStockRequest) (*pb.CheckStockResponse, error) {
    if len(req.Items) == 0 {
        return nil, status.Error(codes.InvalidArgument, "items cannot be empty")
    }

    result := &pb.CheckStockResponse{
        InStock: true,
        Items:   make([]*pb.Item, 0),
    }

    for _, reqItem := range req.Items {
        item, exists := items[reqItem.ItemID]
        if !exists {
            // 아이템이 존재하지 않음
            return nil, status.Error(codes.NotFound,
                fmt.Sprintf("item %s not found", reqItem.ItemID))
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
```

## 테스트 케이스

### 정상 케이스
```bash
curl -X POST http://localhost:8080/api/customers/123/orders \
  -H "Content-Type: application/json" \
  -d '[{"itemID":"item1","quantity":2}]'
```

### 빈 아이템 (400 Bad Request)
```bash
curl -X POST http://localhost:8080/api/customers/123/orders \
  -H "Content-Type: application/json" \
  -d '[]'
```

### 잘못된 아이템 ID (400 Bad Request)
```bash
curl -X POST http://localhost:8080/api/customers/123/orders \
  -H "Content-Type: application/json" \
  -d '[{"itemID":"","quantity":2}]'
```

### 존재하지 않는 아이템 (404 Not Found)
```bash
curl -X POST http://localhost:8080/api/customers/123/orders \
  -H "Content-Type: application/json" \
  -d '[{"itemID":"invalid-item","quantity":2}]'
```

### 재고 부족 (409 Conflict)
```bash
curl -X POST http://localhost:8080/api/customers/123/orders \
  -H "Content-Type: application/json" \
  -d '[{"itemID":"item2","quantity":9999}]'
```

## 에러 흐름 다이어그램

```
Client                Gateway              Orders              Stock
  │                     │                    │                   │
  │── POST /orders ────>│                    │                   │
  │                     │── validate ───┐    │                   │
  │                     │               │    │                   │
  │<── 400 Bad Request ─│<──────────────┘    │                   │
  │                     │                    │                   │
  │                     │── gRPC ───────────>│                   │
  │                     │                    │── CheckStock ────>│
  │                     │                    │                   │
  │                     │                    │<── NotFound ──────│
  │                     │<── InvalidArg ─────│                   │
  │<── 400 Bad Request ─│                    │                   │
```

## 체크리스트

- [ ] Orders Handler에서 gRPC 상태 코드 반환
- [ ] Gateway에서 validateItems 구현
- [ ] Gateway에서 handleGRPCError 구현
- [ ] common/errors.go 확장
- [ ] Stock에서 에러 핸들링 추가
- [ ] 모든 테스트 케이스 확인

## 확장 과제

1. **커스텀 에러 타입**: 에러에 추가 정보 포함
2. **에러 로깅**: 에러 발생 시 상세 로깅
3. **재시도 로직**: 일시적 에러 시 자동 재시도
4. **Circuit Breaker**: 서비스 장애 시 빠른 실패
