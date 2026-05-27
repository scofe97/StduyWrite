# Stage 07: gRPC 고급 기능

**완료일**: 2025-01-13

---

## 학습 목표

gRPC의 고급 기능을 이해하고 프로덕션 환경에서 필요한 보안/성능/확장성 구현

---

## 1. TLS 보안 연결 ✅

### 왜 TLS가 필요한가?

`insecure.NewCredentials()` 사용 시 발생 가능한 공격:

| 공격 | 설명 | TLS 해결책 |
|------|------|-----------|
| 도청 (Eavesdropping) | 중간에서 데이터 엿보기 | **암호화** |
| 변조 (Tampering) | 데이터 위조 | **무결성 검증** |
| 위장 (Spoofing) | 가짜 서버가 진짜인 척 | **인증서 검증** |

### 인증서 생성 (개발용 - SAN 포함)

```bash
mkdir certs && cd certs
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

| 파일 | 역할 | 공개 여부 |
|------|------|-----------|
| `server.crt` | 공개 인증서 (신분증) | 공개 가능 |
| `server.key` | 개인 키 (도장) | **절대 비공개** |

### TLS 서버 구현

```go
import "google.golang.org/grpc/credentials"

creds, err := credentials.NewServerTLSFromFile("./certs/server.crt", "./certs/server.key")
grpcServer := grpc.NewServer(grpc.Creds(creds))
```

### TLS 클라이언트 구현

```go
creds, err := credentials.NewClientTLSFromFile("./certs/server.crt", "")
conn, err := grpc.NewClient("localhost:50051",
    grpc.WithTransportCredentials(creds),
)
```

---

## 2. Server Streaming ✅

### Unary vs Streaming

| 상황 | Unary 문제점 |
|------|-------------|
| 10,000개 데이터 조회 | 메모리에 전부 로드 → OOM 위험 |
| 실시간 로그 전송 | 응답이 "끝나야" 전송 → 실시간 불가 |

### 스트리밍 유형

| 유형 | 요청 | 응답 | 사용 사례 |
|------|------|------|-----------|
| **Unary** | 1개 | 1개 | 단순 조회 |
| **Server Streaming** | 1개 | N개 | 대량 데이터, 실시간 피드 |
| **Client Streaming** | N개 | 1개 | 파일 업로드 |
| **Bidirectional** | N개 | N개 | 채팅 |

### proto 정의

```protobuf
service ProviderService {
  rpc ListProviders(ListProviderRequest) returns (stream Provider);
}
```

### 서버 구현

```go
func (s *providerServer) ListProviders(req *pb.ListProviderRequest, stream pb.ProviderService_ListProvidersServer) error {
    for _, provider := range s.providers {
        if err := stream.Send(provider); err != nil {
            return err
        }
    }
    return nil  // nil = 스트림 종료
}
```

### 클라이언트 구현

```go
stream, err := client.ListProviders(ctx, &pb.ListProviderRequest{})

for {
    provider, err := stream.Recv()
    if err == io.EOF {
        break  // 스트림 종료
    }
    if err != nil {
        return err
    }
    // provider 처리
}
```

---

## 3. Metadata와 인터셉터 ✅

### Metadata (HTTP 헤더와 유사)

모든 Request에 토큰 필드 추가 → 비효율적
**Metadata**로 메타 정보 분리 전달

**클라이언트 (전송)**:
```go
import "google.golang.org/grpc/metadata"

md := metadata.Pairs(
    "authorization", "Bearer my-token",
    "x-request-id", "req-12345",
)
ctx = metadata.NewOutgoingContext(ctx, md)
```

**서버 (수신)**:
```go
md, ok := metadata.FromIncomingContext(ctx)
if ok {
    auth := md["authorization"]
    reqID := md["x-request-id"]
}
```

### 인터셉터 (미들웨어)

모든 요청을 **한 곳에서** 가로채서 공통 처리

```go
func loggingInterceptor(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error) {
    // 1. 요청 전 처리
    start := time.Now()
    log.Printf("Method: %s", info.FullMethod)

    // 2. 실제 핸들러 호출
    resp, err := handler(ctx, req)

    // 3. 요청 후 처리
    log.Printf("Duration: %v", time.Since(start))

    return resp, err
}
```

### 인터셉터 등록

```go
// 단일 인터셉터
grpcServer := grpc.NewServer(
    grpc.UnaryInterceptor(loggingInterceptor),
)

// 체이닝 (여러 개)
grpcServer := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        loggingInterceptor,  // 1번째 실행
        authInterceptor,     // 2번째 실행
    ),
)
```

### Spring vs gRPC 비교

| Spring | gRPC |
|--------|------|
| Filter + Interceptor | Interceptor만 |
| `FilterChain` | `ChainUnaryInterceptor` |
| `chain.doFilter()` | `handler(ctx, req)` |

---

## 4. Status Codes 에러 처리 ✅

### 문제점

```go
return nil, fmt.Errorf("not found")  // 문자열 파싱 필요
```

### gRPC Status Codes

| 코드 | 의미 | HTTP 비유 |
|------|------|-----------|
| `codes.OK` | 성공 | 200 |
| `codes.NotFound` | 리소스 없음 | 404 |
| `codes.InvalidArgument` | 잘못된 입력 | 400 |
| `codes.Unauthenticated` | 인증 필요 | 401 |
| `codes.PermissionDenied` | 권한 없음 | 403 |
| `codes.Internal` | 서버 오류 | 500 |

### 서버 (에러 반환)

```go
import "google.golang.org/grpc/codes"
import "google.golang.org/grpc/status"

return nil, status.Errorf(codes.NotFound, "프로바이더 없음: %s", req.Type)
```

### 클라이언트 (에러 처리)

```go
resp, err := client.GetProvider(ctx, req)
if err != nil {
    st, ok := status.FromError(err)
    if ok {
        switch st.Code() {
        case codes.NotFound:
            // 리소스 없음 처리
        case codes.Unauthenticated:
            // 인증 필요 처리
        }
    }
}
```

---

## 5. gRPC-Gateway ✅ (개념)

### 목적

gRPC 서버 하나로 **REST + gRPC** 동시 제공

```
웹 브라우저 ──── REST ────┐
curl ──────── REST ───────┼──▶ gRPC-Gateway ──▶ gRPC 서버
Go 클라이언트 ── gRPC ────┘
```

### proto에 HTTP 매핑

```protobuf
import "google/api/annotations.proto";

service ProviderService {
  rpc GetProvider(GetProviderRequest) returns (GetProviderResponse) {
    option (google.api.http) = {
      get: "/v1/providers/{type}"
    };
  }
}
```

### 매핑 결과

| gRPC | REST |
|------|------|
| `GetProvider({type: "github"})` | `GET /v1/providers/github` |
| `ListProviders({})` | `GET /v1/providers` |

### 장점

- 코드 1개로 gRPC + REST
- 내부: gRPC (빠름)
- 외부: REST (범용성)

---

## 파일 구조

```
07-grpc-advanced/
├── go.mod
├── go.sum
├── proto/
│   ├── provider.proto          ← stream 추가
│   ├── provider.pb.go
│   └── provider_grpc.pb.go
├── certs/
│   ├── server.crt
│   └── server.key
├── server-tls/
│   └── main.go                 ← TLS + Streaming + Interceptor + Status
├── client-tls/
│   └── main.go                 ← TLS + Streaming + Metadata + Status
└── LEARNED.md
```

---

## 핵심 정리

| 주제 | 핵심 |
|------|------|
| **TLS** | `credentials.NewServerTLSFromFile()` |
| **Streaming** | `stream.Send()` / `stream.Recv()` + `io.EOF` |
| **Metadata** | `metadata.NewOutgoingContext()` / `FromIncomingContext()` |
| **Interceptor** | `grpc.ChainUnaryInterceptor()` |
| **Status Codes** | `status.Errorf(codes.NotFound, ...)` |
| **gRPC-Gateway** | proto에 `google.api.http` 옵션 |

---

## 실행 방법

```bash
# 1. 인증서 생성 (SAN 포함)
cd 07-grpc-advanced/certs
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

# 2. 서버 실행
cd 07-grpc-advanced
go run ./server-tls

# 3. 클라이언트 실행 (다른 터미널)
cd 07-grpc-advanced
go run ./client-tls
```
