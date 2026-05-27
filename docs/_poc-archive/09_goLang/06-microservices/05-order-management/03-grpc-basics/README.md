# 03. gRPC Basics - Protocol Buffers & gRPC

## 학습 목표

- Protocol Buffers 문법 이해
- .proto 파일 작성
- Go 코드 생성
- gRPC 서비스 인터페이스 이해

## 핵심 개념

### Protocol Buffers란?

Google이 개발한 언어 중립적 직렬화 포맷:
- 바이너리 포맷으로 JSON보다 작고 빠름
- 스키마 정의 (.proto 파일)
- 다양한 언어로 코드 생성

### gRPC란?

HTTP/2 기반의 RPC 프레임워크:
- 양방향 스트리밍 지원
- 타입 안전성 (컴파일 타임 검증)
- 자동 코드 생성

## 실습 과제

### Task 1: Proto 파일 작성

```protobuf
// common/api/order_management_system.proto
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

message GetOrderRequest {
    string orderID = 1;
    string customerID = 2;
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
    string priceID = 4;
}
```

### Task 2: Makefile 작성

```makefile
# common/Makefile
.PHONY: gen

gen:
	protoc --go_out=. --go-grpc_out=. api/order_management_system.proto
```

### Task 3: 코드 생성

```bash
cd common
make gen
```

생성되는 파일:
- `api/order_management_system.pb.go` - 메시지 정의
- `api/order_management_system_grpc.pb.go` - 서비스 인터페이스

### Task 4: 생성된 코드 이해

```go
// 자동 생성된 서버 인터페이스
type OrderServiceServer interface {
    CreateOrder(context.Context, *CreateOrderRequest) (*Order, error)
    GetOrder(context.Context, *GetOrderRequest) (*Order, error)
    mustEmbedUnimplementedOrderServiceServer()
}

// 자동 생성된 클라이언트
type OrderServiceClient interface {
    CreateOrder(ctx context.Context, in *CreateOrderRequest, opts ...grpc.CallOption) (*Order, error)
    GetOrder(ctx context.Context, in *GetOrderRequest, opts ...grpc.CallOption) (*Order, error)
}

// 클라이언트 생성 함수
func NewOrderServiceClient(cc grpc.ClientConnInterface) OrderServiceClient
```

### Task 5: 의존성 추가

```bash
cd common
go get google.golang.org/grpc
go get google.golang.org/protobuf
```

## Proto 문법 정리

### 타입

| Proto | Go |
|-------|-----|
| string | string |
| int32 | int32 |
| int64 | int64 |
| bool | bool |
| bytes | []byte |
| float | float32 |
| double | float64 |

### 필드 수식어

```protobuf
message Example {
    string name = 1;                    // 단일 필드
    repeated string tags = 2;           // 슬라이스 (배열)
    optional int32 age = 3;             // 선택적 필드
    map<string, string> metadata = 4;   // 맵
}
```

### 필드 번호 규칙

- 1-15: 1바이트 (자주 사용하는 필드)
- 16-2047: 2바이트
- 19000-19999: 예약됨 (사용 불가)

## 체크리스트

- [ ] common/api 디렉토리 생성
- [ ] .proto 파일 작성
- [ ] Makefile 작성
- [ ] make gen 실행
- [ ] 생성된 코드 확인 및 이해

## 다음 단계

→ 04-orders-service: 주문 서비스 gRPC 서버 구현
