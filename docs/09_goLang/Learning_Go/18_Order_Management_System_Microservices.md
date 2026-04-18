# 18. Order Management System - Go 마이크로서비스

> Thiago의 강의를 기반으로 한 마이크로서비스 아키텍처 학습 정리

## 핵심 개념 요약

### 1. 마이크로서비스 아키텍처

**모놀리스 vs 마이크로서비스**
```
모놀리스:
┌─────────────────────────────────┐
│  Single Application             │
│  - All features in one codebase │
│  - Single deployment unit       │
│  - Shared database              │
└─────────────────────────────────┘

마이크로서비스:
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Gateway  │──│ Orders   │──│ Stock    │
└──────────┘  └──────────┘  └──────────┘
                   │
              ┌──────────┐  ┌──────────┐
              │ Payments │──│ Kitchen  │
              └──────────┘  └──────────┘
```

**마이크로서비스 선택 기준**:
- 팀이 독립적으로 배포해야 할 때
- 서비스별로 다른 스케일링이 필요할 때
- 장애 격리가 중요할 때
- 기술 스택 다양화가 필요할 때

### 2. 통신 패턴

**동기 통신 (gRPC)**:
```
Gateway ──gRPC──> Orders ──gRPC──> Stock
                     │
                     └──gRPC──> Payments
```
- 즉각적인 응답 필요
- 요청-응답 패턴
- 실패 시 즉시 알 수 있음

**비동기 통신 (RabbitMQ)**:
```
Orders ──publish──> [Order Created Queue] ──consume──> Kitchen
                           │
                           └──consume──> Notifications
```
- 느슨한 결합
- 이벤트 기반
- 확장성 우수

### 3. gRPC & Protocol Buffers

**Proto 정의**:
```protobuf
syntax = "proto3";
option go_package = "common/api";
package api;

service OrderService {
    rpc CreateOrder(CreateOrderRequest) returns (Order);
    rpc GetOrder(GetOrderRequest) returns (Order);
}

message CreateOrderRequest {
    string customerID = 1;
    repeated ItemsWithQuantity items = 2;
}

message ItemsWithQuantity {
    string itemID = 1;
    int32 quantity = 2;
}

message Order {
    string ID = 1;
    string customerID = 2;
    string status = 3;
    repeated Item items = 4;
}

message Item {
    string ID = 1;
    string name = 2;
    int32 quantity = 3;
    string priceID = 4;  // Stripe 연동용
}
```

**Makefile로 코드 생성**:
```makefile
gen:
	# Regenerate gRPC code
	protoc --go_out=. --go-grpc_out=. common/api/order_management_system.proto
```

### 4. 계층형 아키텍처

```
┌─────────────────────────────────────────────┐
│                  Gateway                     │
│  (HTTP Entry Point)                          │
└─────────────────────────────────────────────┘
                    │ gRPC
┌─────────────────────────────────────────────┐
│               Transport Layer                │
│  (gRPC Handlers - Receive/Send)              │
└─────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────┐
│               Service Layer                  │
│  (Business Logic, Validation)                │
└─────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────┐
│               Storage Layer                  │
│  (Database Operations)                       │
└─────────────────────────────────────────────┘
```

**각 계층의 책임**:
- **Gateway**: HTTP 요청 수신, gRPC 클라이언트
- **Transport**: gRPC 서버, 요청/응답 직렬화
- **Service**: 비즈니스 로직, 검증
- **Storage**: 데이터 영속성

---

## 면접 질문 & 답변

### Q1: 마이크로서비스 아키텍처의 장단점은?

**장점**:
1. **독립적 배포**: 각 서비스를 개별적으로 배포 가능
2. **기술 다양성**: 서비스별로 적합한 기술 선택
3. **확장성**: 필요한 서비스만 스케일 아웃
4. **장애 격리**: 한 서비스 장애가 전체에 영향 제한
5. **팀 자율성**: 작은 팀이 서비스 전체 소유

**단점**:
1. **복잡성 증가**: 분산 시스템 관리 어려움
2. **네트워크 오버헤드**: 서비스 간 통신 비용
3. **데이터 일관성**: 분산 트랜잭션 어려움
4. **운영 부담**: 여러 서비스 모니터링 필요
5. **디버깅 어려움**: 분산 추적 필요

```go
// 예: 서비스 간 통신 에러 핸들링
order, err := h.orderClient.CreateOrder(ctx, req)
if err != nil {
    // gRPC 에러 상태 추출
    status := status.Convert(err)
    if status.Code() == codes.InvalidArgument {
        return writeError(w, http.StatusBadRequest, status.Message())
    }
    return writeError(w, http.StatusInternalServerError, "order creation failed")
}
```

### Q2: gRPC를 선택한 이유는? REST와의 차이점은?

**gRPC 선택 이유**:
1. **성능**: Protocol Buffers의 바이너리 직렬화
2. **타입 안정성**: 컴파일 타임 검증
3. **코드 생성**: 클라이언트/서버 자동 생성
4. **스트리밍**: 양방향 스트리밍 지원
5. **HTTP/2**: 다중화, 헤더 압축

```go
// gRPC 서버 구현
type grpcHandler struct {
    pb.UnimplementedOrderServiceServer
    service OrderService
}

func (h *grpcHandler) CreateOrder(ctx context.Context, p *pb.CreateOrderRequest) (*pb.Order, error) {
    // 비즈니스 로직 호출
    if err := h.service.ValidateOrder(ctx, p); err != nil {
        return nil, status.Error(codes.InvalidArgument, err.Error())
    }

    order, err := h.service.CreateOrder(ctx, p)
    if err != nil {
        return nil, status.Error(codes.Internal, err.Error())
    }

    return order, nil
}
```

**REST vs gRPC**:
| 특성 | REST | gRPC |
|------|------|------|
| 포맷 | JSON (텍스트) | Protobuf (바이너리) |
| 프로토콜 | HTTP/1.1 | HTTP/2 |
| 타입 안정성 | 런타임 | 컴파일 타임 |
| 스트리밍 | 제한적 | 네이티브 지원 |
| 브라우저 지원 | 네이티브 | 프록시 필요 |

### Q3: Service Discovery가 필요한 이유는?

**문제 상황**:
```go
// 하드코딩된 주소 - 확장 불가능
conn, err := grpc.Dial("localhost:2000", grpc.WithInsecure())
```

**해결책 - Service Discovery**:
```
┌─────────────────────────────────────────────┐
│           Service Registry (Consul)          │
│                                              │
│  ┌─────────────────────────────────────┐    │
│  │ orders-service                       │    │
│  │   - instance1: 192.168.1.10:2000     │    │
│  │   - instance2: 192.168.1.11:2000     │    │
│  │   - instance3: 192.168.1.12:2000     │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
         ▲                    │
    Register              Discover
         │                    ▼
    ┌─────────┐          ┌─────────┐
    │ Orders  │          │ Gateway │
    └─────────┘          └─────────┘
```

**Service Discovery 유형**:
1. **Client-side**: 클라이언트가 직접 레지스트리 조회 (Consul)
2. **Server-side**: 로드 밸런서가 라우팅 (Kubernetes)

```go
// Service Discovery 추상화
type Registry interface {
    Register(ctx context.Context, instanceID, serviceName, hostPort string) error
    Deregister(ctx context.Context, instanceID, serviceName string) error
    Discover(ctx context.Context, serviceName string) ([]string, error)
    HealthCheck(instanceID, serviceName string) error
}
```

### Q4: 이벤트 기반 아키텍처의 장점은?

```
Order Created Event Flow:
┌─────────┐    ┌─────────────┐    ┌─────────┐
│ Orders  │───>│  RabbitMQ   │───>│ Kitchen │
└─────────┘    │             │    └─────────┘
               │  order.     │
               │  created    │───>│ Notif.  │
               │             │    └─────────┘
               └─────────────┘
```

**장점**:
1. **느슨한 결합**: 발행자가 구독자를 몰라도 됨
2. **확장성**: 새 구독자 쉽게 추가
3. **회복력**: 일시적 장애에 강함 (메시지 지속성)
4. **비동기 처리**: 긴 작업을 백그라운드에서 처리

```go
// 이벤트 발행 예시
type OrderCreatedEvent struct {
    OrderID    string    `json:"order_id"`
    CustomerID string    `json:"customer_id"`
    Items      []Item    `json:"items"`
    CreatedAt  time.Time `json:"created_at"`
}

func (s *service) CreateOrder(ctx context.Context, req *CreateOrderRequest) (*Order, error) {
    order, err := s.store.Create(ctx, req)
    if err != nil {
        return nil, err
    }

    // 이벤트 발행
    event := OrderCreatedEvent{
        OrderID:    order.ID,
        CustomerID: order.CustomerID,
        Items:      order.Items,
        CreatedAt:  time.Now(),
    }

    return order, s.broker.Publish(ctx, "order.created", event)
}
```

### Q5: Go Workspace를 사용하는 이유는?

**모노레포 구조**:
```
order-management-system/
├── go.work              # 워크스페이스 정의
├── common/              # 공유 코드
│   ├── go.mod
│   └── api/
├── gateway/
│   └── go.mod
├── orders/
│   └── go.mod
├── payments/
│   └── go.mod
└── stock/
    └── go.mod
```

**go.work 파일**:
```go
go 1.22

use (
    ./common
    ./gateway
    ./orders
    ./payments
    ./stock
)
```

**장점**:
1. **로컬 개발 편의**: `replace` 지시문 불필요
2. **공유 코드 변경 즉시 반영**: common 변경 시 다른 모듈에서 즉시 사용
3. **통합 빌드/테스트**: 전체 워크스페이스 대상 명령 실행

### Q6: 계층형 아키텍처에서 각 계층의 역할은?

```go
// Storage Layer - 데이터 접근
type OrderStore interface {
    Create(ctx context.Context, order *Order) error
    Get(ctx context.Context, id string) (*Order, error)
    Update(ctx context.Context, order *Order) error
}

type mongoStore struct {
    db *mongo.Database
}

func (s *mongoStore) Create(ctx context.Context, order *Order) error {
    _, err := s.db.Collection("orders").InsertOne(ctx, order)
    return err
}

// Service Layer - 비즈니스 로직
type OrderService interface {
    CreateOrder(ctx context.Context, req *CreateOrderRequest) (*Order, error)
    ValidateOrder(ctx context.Context, req *CreateOrderRequest) error
}

type service struct {
    store       OrderStore
    stockClient pb.StockServiceClient
}

func (s *service) CreateOrder(ctx context.Context, req *CreateOrderRequest) (*Order, error) {
    // 1. 검증
    if err := s.ValidateOrder(ctx, req); err != nil {
        return nil, err
    }

    // 2. 재고 확인 (다른 서비스 호출)
    if _, err := s.stockClient.CheckStock(ctx, &pb.CheckStockRequest{
        Items: req.Items,
    }); err != nil {
        return nil, err
    }

    // 3. 주문 생성
    order := &Order{
        ID:         uuid.New().String(),
        CustomerID: req.CustomerID,
        Status:     "pending",
        Items:      req.Items,
    }

    return order, s.store.Create(ctx, order)
}

// Transport Layer - gRPC 핸들러
type grpcHandler struct {
    pb.UnimplementedOrderServiceServer
    service OrderService
}

func NewGRPCHandler(grpcServer *grpc.Server, service OrderService) {
    handler := &grpcHandler{service: service}
    pb.RegisterOrderServiceServer(grpcServer, handler)
}
```

### Q7: gRPC 에러 핸들링은 어떻게 하는가?

```go
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

// 서버 측 - 에러 반환
func (h *grpcHandler) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.Order, error) {
    if len(req.Items) == 0 {
        return nil, status.Error(codes.InvalidArgument, "items must have at least one item")
    }

    order, err := h.service.CreateOrder(ctx, req)
    if err != nil {
        if errors.Is(err, ErrNoItems) {
            return nil, status.Error(codes.InvalidArgument, err.Error())
        }
        return nil, status.Error(codes.Internal, "failed to create order")
    }

    return order, nil
}

// 클라이언트 측 - 에러 처리
func (h *httpHandler) handleCreateOrder(w http.ResponseWriter, r *http.Request) {
    order, err := h.orderClient.CreateOrder(r.Context(), req)
    if err != nil {
        errStatus := status.Convert(err)

        switch errStatus.Code() {
        case codes.InvalidArgument:
            writeError(w, http.StatusBadRequest, errStatus.Message())
        case codes.NotFound:
            writeError(w, http.StatusNotFound, errStatus.Message())
        case codes.Unavailable:
            writeError(w, http.StatusServiceUnavailable, "service temporarily unavailable")
        default:
            writeError(w, http.StatusInternalServerError, "internal server error")
        }
        return
    }

    writeJSON(w, http.StatusOK, order)
}
```

**gRPC 상태 코드**:
| 코드 | 의미 | HTTP 매핑 |
|------|------|-----------|
| OK | 성공 | 200 |
| InvalidArgument | 잘못된 인자 | 400 |
| NotFound | 리소스 없음 | 404 |
| AlreadyExists | 이미 존재 | 409 |
| PermissionDenied | 권한 없음 | 403 |
| Internal | 내부 오류 | 500 |
| Unavailable | 서비스 불가 | 503 |

### Q8: 입력 검증 전략은?

```go
// Gateway 검증 (HTTP 레벨)
func validateItems(items []*pb.ItemsWithQuantity) error {
    if len(items) == 0 {
        return errors.New("items must have at least one item")
    }

    for _, item := range items {
        if item.ItemID == "" {
            return errors.New("item ID is required")
        }
        if item.Quantity <= 0 {
            return errors.New("item quantity must be positive")
        }
    }

    return nil
}

// Service 검증 (비즈니스 레벨)
func (s *service) ValidateOrder(ctx context.Context, req *pb.CreateOrderRequest) error {
    if len(req.Items) == 0 {
        return common.ErrNoItems
    }

    // 중복 아이템 병합
    merged := s.mergeItemsQuantity(req.Items)

    // 재고 서비스 검증
    for _, item := range merged {
        available, err := s.stockClient.CheckAvailability(ctx, item.ItemID)
        if err != nil {
            return fmt.Errorf("stock check failed: %w", err)
        }
        if available < item.Quantity {
            return fmt.Errorf("insufficient stock for item %s", item.ItemID)
        }
    }

    return nil
}

// 아이템 수량 병합
func (s *service) mergeItemsQuantity(items []*pb.ItemsWithQuantity) []*pb.ItemsWithQuantity {
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

**이중 검증의 이유**:
1. Gateway: 빠른 실패, 잘못된 요청 조기 차단
2. Service: 비즈니스 규칙 검증, 다른 서비스에서도 호출될 수 있음

---

## 주요 코드 패턴

### HTTP JSON 헬퍼

```go
// common/json.go
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

### 환경 변수 헬퍼

```go
// common/env.go
func EnvString(key, fallback string) string {
    if val, ok := os.LookupEnv(key); ok {
        return val
    }
    return fallback
}

func EnvInt(key string, fallback int) int {
    if val, ok := os.LookupEnv(key); ok {
        if i, err := strconv.Atoi(val); err == nil {
            return i
        }
    }
    return fallback
}
```

### 공통 에러 정의

```go
// common/errors.go
var (
    ErrNoItems      = errors.New("items must have at least one item")
    ErrInvalidItem  = errors.New("invalid item")
    ErrOrderNotFound = errors.New("order not found")
)
```

### Go 1.22+ HTTP 라우팅

```go
// gateway/http_handler.go
type Handler struct {
    orderClient pb.OrderServiceClient
}

func NewHandler(orderClient pb.OrderServiceClient) *Handler {
    return &Handler{orderClient: orderClient}
}

func (h *Handler) RegisterRoutes(mux *http.ServeMux) {
    // Go 1.22+ 패턴: METHOD /path
    mux.HandleFunc("POST /api/customers/{customerID}/orders", h.handleCreateOrder)
    mux.HandleFunc("GET /api/customers/{customerID}/orders/{orderID}", h.handleGetOrder)
}

func (h *Handler) handleCreateOrder(w http.ResponseWriter, r *http.Request) {
    customerID := r.PathValue("customerID")

    var items []*pb.ItemsWithQuantity
    if err := common.ReadJSON(r, &items); err != nil {
        common.WriteError(w, http.StatusBadRequest, err.Error())
        return
    }

    order, err := h.orderClient.CreateOrder(r.Context(), &pb.CreateOrderRequest{
        CustomerID: customerID,
        Items:      items,
    })

    if err != nil {
        // gRPC 에러 처리
        errStatus := status.Convert(err)
        if errStatus.Code() == codes.InvalidArgument {
            common.WriteError(w, http.StatusBadRequest, errStatus.Message())
            return
        }
        common.WriteError(w, http.StatusInternalServerError, "failed to create order")
        return
    }

    common.WriteJSON(w, http.StatusOK, order)
}
```

---

## 개발 도구 설정

### Air (Hot Reloading)

```toml
# .air.toml
root = "."
tmp_dir = "tmp"

[build]
  cmd = "go build -o ./tmp/main ."
  bin = "./tmp/main"
  delay = 1000
  exclude_dir = ["assets", "tmp", "vendor"]
  exclude_file = []
  exclude_regex = ["_test.go"]
  exclude_unchanged = false
  follow_symlink = false
  full_bin = ""
  include_dir = []
  include_ext = ["go", "tpl", "tmpl", "html"]
  kill_delay = "0s"
  log = "build-errors.log"
  send_interrupt = false
  stop_on_error = true

[log]
  time = false

[color]
  app = ""
  build = "yellow"
  main = "magenta"
  runner = "green"
  watcher = "cyan"

[misc]
  clean_on_exit = false
```

### Makefile

```makefile
.PHONY: gen run-gateway run-orders

gen:
	protoc --go_out=. --go-grpc_out=. common/api/*.proto

run-gateway:
	cd gateway && air

run-orders:
	cd orders && air

run-all:
	make -j2 run-gateway run-orders
```

---

## 아키텍처 다이어그램

### 전체 시스템 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client (Browser/App)                     │
└─────────────────────────────────────────────────────────────────┘
                                    │ HTTP
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                           Gateway                                │
│  - HTTP Server                                                   │
│  - JSON <-> Protobuf 변환                                        │
│  - 요청 라우팅                                                    │
└─────────────────────────────────────────────────────────────────┘
         │ gRPC              │ gRPC              │ gRPC
         ▼                   ▼                   ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Orders    │────>│    Stock     │     │   Payments   │
│              │     │              │     │   (Stripe)   │
└──────────────┘     └──────────────┘     └──────────────┘
         │                                        │
         │ Event (RabbitMQ)                       │ Webhook
         ▼                                        ▼
┌──────────────┐                         ┌──────────────┐
│   Kitchen    │                         │   Orders     │
│              │                         │ (상태 업데이트) │
└──────────────┘                         └──────────────┘
```

### 주문 생성 시퀀스

```
Client      Gateway      Orders       Stock       Payments
  │            │           │            │            │
  │──POST────>│            │            │            │
  │            │──gRPC────>│            │            │
  │            │            │──gRPC────>│            │
  │            │            │<──Stock OK│            │
  │            │            │──gRPC──────────────────>│
  │            │            │<──Payment Link─────────│
  │            │<──Order───│            │            │
  │<──JSON────│            │            │            │
```

---

## 핵심 포인트 정리

1. **마이크로서비스는 만병통치약이 아님**: 복잡성 vs 이점 트레이드오프 고려

2. **gRPC는 내부 통신에 적합**: 브라우저 직접 통신은 Gateway 통해

3. **Service Discovery로 동적 확장**: 하드코딩된 주소 제거

4. **이벤트 기반으로 느슨한 결합**: 서비스 간 직접 의존 최소화

5. **계층형 아키텍처로 관심사 분리**: Transport, Service, Storage 분리

6. **이중 검증으로 안정성 확보**: Gateway + Service 레벨 검증

7. **Go Workspace로 모노레포 관리**: 공유 코드 효율적 관리

8. **에러 핸들링 표준화**: gRPC 상태 코드를 HTTP로 매핑
