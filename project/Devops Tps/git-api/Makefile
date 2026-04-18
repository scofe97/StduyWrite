.PHONY: build run test clean docker-build docker-run lint fmt deps

# Variables
APP_NAME := git-api
BUILD_DIR := ./build
MAIN_PATH := ./cmd/server

# Go commands
GO := go
GOFMT := gofmt
GOLINT := golangci-lint

# Build the application
build:
	@echo "Building $(APP_NAME)..."
	@mkdir -p $(BUILD_DIR)
	$(GO) build -o $(BUILD_DIR)/$(APP_NAME) $(MAIN_PATH)
	@echo "Build complete: $(BUILD_DIR)/$(APP_NAME)"

# Run the application
run:
	@echo "Running $(APP_NAME)..."
	$(GO) run $(MAIN_PATH)/main.go

# Run tests
test:
	@echo "Running tests..."
	$(GO) test -v -race -cover ./...

# Run tests with coverage report
test-coverage:
	@echo "Running tests with coverage..."
	$(GO) test -v -race -coverprofile=coverage.out ./...
	$(GO) tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report: coverage.html"

# Clean build artifacts
clean:
	@echo "Cleaning..."
	@rm -rf $(BUILD_DIR)
	@rm -f coverage.out coverage.html
	@echo "Clean complete"

# Download dependencies
deps:
	@echo "Downloading dependencies..."
	$(GO) mod download
	$(GO) mod tidy
	@echo "Dependencies downloaded"

# Format code
fmt:
	@echo "Formatting code..."
	$(GOFMT) -s -w .
	@echo "Format complete"

# Lint code
lint:
	@echo "Linting code..."
	$(GOLINT) run ./...
	@echo "Lint complete"

# Build Docker image
docker-build:
	@echo "Building Docker image..."
	docker build -t $(APP_NAME):latest .
	@echo "Docker build complete"

# Run with Docker
docker-run:
	@echo "Running with Docker..."
	docker run --rm \
		-e KAFKA_BROKERS=host.docker.internal:9092 \
		-e KAFKA_CONSUMER_GROUP=git-api \
		-e KAFKA_TOPIC_COMMANDS=runners-high.git.commands \
		-e KAFKA_TOPIC_EVENTS=runners-high.git.events \
		$(APP_NAME):latest

# Generate mocks (if using mockgen)
mocks:
	@echo "Generating mocks..."
	$(GO) generate ./...
	@echo "Mocks generated"

# Run all checks before commit
pre-commit: fmt lint test
	@echo "Pre-commit checks passed"

# Help
help:
	@echo "Available commands:"
	@echo "  make build         - Build the application"
	@echo "  make run           - Run the application"
	@echo "  make test          - Run tests"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make deps          - Download dependencies"
	@echo "  make fmt           - Format code"
	@echo "  make lint          - Lint code"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run with Docker"
	@echo "  make pre-commit    - Run all checks before commit"
