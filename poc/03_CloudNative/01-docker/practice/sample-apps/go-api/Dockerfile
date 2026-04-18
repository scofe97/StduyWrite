# Multi-stage build for Go API
# Stage 1: 빌드 환경
FROM golang:1.21-alpine AS builder

WORKDIR /build

# 의존성 파일 복사 및 다운로드 (캐시 최적화)
COPY go.mod go.sum ./
RUN go mod download

# 소스 코드 복사 및 빌드
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: 실행 환경
FROM scratch

WORKDIR /app

# 빌드된 바이너리만 복사
COPY --from=builder /build/main .

EXPOSE 8080

CMD ["./main"]
