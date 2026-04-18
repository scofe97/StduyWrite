# Git Provider Makefile
# Proto 컴파일 및 빌드 자동화

# 변수 정의
PROTO_DIR := api/proto
PB_DIR := pkg/pb
PROTO_FILES := $(shell find $(PROTO_DIR)/v1 -name "*.proto")

# ===================================================================
# Proto 컴파일
# ===================================================================

.PHONY: proto
proto: proto-deps
	@echo "==> Generating Go code from proto files..."
	@mkdir -p $(PB_DIR)/v1
	protoc \
		--proto_path=$(PROTO_DIR) \
		--go_out=$(PB_DIR) \
		--go_opt=paths=source_relative \
		--go-grpc_out=$(PB_DIR) \
		--go-grpc_opt=paths=source_relative \
		--grpc-gateway_out=$(PB_DIR) \
		--grpc-gateway_opt=paths=source_relative \
		v1/provider.proto \
		v1/branch.proto \
		v1/contents.proto \
		v1/mergerequest.proto \
		v1/cicd.proto \
		v1/workflow.proto
	@echo "==> Done!"

# Proto 도구 설치 확인
.PHONY: proto-deps
proto-deps:
	@which protoc > /dev/null || (echo "protoc not found. Install: brew install protobuf" && exit 1)
	@which protoc-gen-go > /dev/null || go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	@which protoc-gen-go-grpc > /dev/null || go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
	@which protoc-gen-grpc-gateway > /dev/null || go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway@latest

# ===================================================================
# 빌드
# ===================================================================

.PHONY: build
build:
	@echo "==> Building..."
	go build -o bin/git-provider ./cmd/server
	@echo "==> Done!"

.PHONY: run
run:
	go run ./cmd/server

# ===================================================================
# 개발 도구
# ===================================================================

.PHONY: test
test:
	go test -v ./...

.PHONY: clean
clean:
	rm -rf bin/
	rm -rf $(PB_DIR)/

.PHONY: fmt
fmt:
	go fmt ./...

.PHONY: tidy
tidy:
	go mod tidy

# ===================================================================
# 도움말
# ===================================================================

.PHONY: help
help:
	@echo "사용 가능한 명령어:"
	@echo "  make proto      - Proto 파일에서 Go 코드 생성"
	@echo "  make build      - 바이너리 빌드"
	@echo "  make run        - 서버 실행"
	@echo "  make test       - 테스트 실행"
	@echo "  make clean      - 빌드 결과물 삭제"
	@echo "  make fmt        - 코드 포맷팅"
	@echo "  make tidy       - go.mod 정리"
