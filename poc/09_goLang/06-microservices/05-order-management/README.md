# Order Management System: Go Microservices

> Thiago의 강의를 기반으로 한 실습 프로젝트

## 학습 목표

1. Go 마이크로서비스 아키텍처 이해
2. gRPC 서버/클라이언트 구현
3. Protocol Buffers 정의 및 코드 생성
4. 계층형 아키텍처 (Transport, Service, Storage)
5. Service Discovery 개념
6. 이벤트 기반 아키텍처 기초

## 폴더 구조

```
05-order-management/
├── 01-go-workspace/        # Go 워크스페이스 설정
├── 02-gateway-http/        # HTTP Gateway 서버
├── 03-grpc-basics/         # gRPC 기초 및 Proto 정의
├── 04-orders-service/      # 주문 서비스 구현
├── 05-layered-arch/        # 계층형 아키텍처 적용
├── 06-service-comm/        # 서비스 간 통신
└── 07-validation/          # 입력 검증 및 에러 핸들링
```

## 진행 방법

각 폴더의 README.md를 읽고 직접 코드를 작성하세요.

## 핵심 개념

### 마이크로서비스 아키텍처

```
┌──────────┐  HTTP   ┌─────────┐  gRPC   ┌──────────┐
│  Client  │────────>│ Gateway │────────>│  Orders  │
└──────────┘         └─────────┘         └──────────┘
                          │                    │
                          │               ┌────┴────┐
                          │               │         │
                          │          ┌────▼───┐ ┌───▼────┐
                          └─────────>│ Stock  │ │Payment │
                                     └────────┘ └────────┘
```

### 계층형 구조

```
Gateway (HTTP)
     │
Transport (gRPC Handler)
     │
Service (Business Logic)
     │
Storage (Database)
```

### gRPC 메시지 정의

```protobuf
service OrderService {
    rpc CreateOrder(CreateOrderRequest) returns (Order);
}

message CreateOrderRequest {
    string customerID = 1;
    repeated ItemsWithQuantity items = 2;
}
```

## 사전 준비

### 필수 도구 설치

```bash
# Protocol Buffers 컴파일러
brew install protobuf

# Go gRPC 플러그인
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Air (Hot Reloading)
go install github.com/air-verse/air@latest
```

### PATH 설정 확인

```bash
export PATH="$PATH:$(go env GOPATH)/bin"
```

## 참고 자료

- [gRPC Go Documentation](https://grpc.io/docs/languages/go/)
- [Protocol Buffers](https://protobuf.dev/)
- [Go Workspaces](https://go.dev/blog/get-familiar-with-workspaces)
- [HashiCorp Consul](https://www.consul.io/)
