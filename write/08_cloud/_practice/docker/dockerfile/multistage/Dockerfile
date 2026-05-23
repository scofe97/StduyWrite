# Multi-stage build for Go application
# Stage 1: 빌드 환경
FROM golang:1.21-alpine AS builder

# 빌드에 필요한 도구 설치
RUN apk add --no-cache git

WORKDIR /build

# 의존성 파일 복사 및 다운로드
COPY go.mod go.sum ./
RUN go mod download

# 소스 코드 복사
COPY . .

# 정적 링크 바이너리 빌드
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o app .

# Stage 2: 실행 환경 (최소 이미지)
FROM scratch

WORKDIR /app

# 빌드된 바이너리만 복사
COPY --from=builder /build/app .

EXPOSE 8080

ENTRYPOINT ["./app"]
