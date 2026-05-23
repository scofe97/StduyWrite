# =============================================================================
# Multi-stage Dockerfile: Go 애플리케이션
# Stage 1 (build): 소스 컴파일 → 정적 바이너리 생성
# Stage 2 (run):   최소 이미지에 바이너리만 복사하여 실행
# =============================================================================

# --- Stage 1: Build ---
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Go 모듈 초기화 (의존성이 있다면 go.mod/go.sum 먼저 복사하여 캐시 활용)
COPY src/main.go .
RUN go mod init sample-app && \
    CGO_ENABLED=0 GOOS=linux go build -o /app/server main.go

# --- Stage 2: Run ---
FROM alpine:3.19

# 보안: root가 아닌 별도 사용자로 실행
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app
COPY --from=builder /app/server .

# 소유권 변경
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8081

# 헬스체크: 30초마다 /health 엔드포인트 확인
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:8081/health || exit 1

ENTRYPOINT ["./server"]
