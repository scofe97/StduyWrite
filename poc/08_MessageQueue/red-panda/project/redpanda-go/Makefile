.PHONY: build run test clean

APP_NAME := redpanda-go
BUILD_DIR := bin

build:
	go build -o $(BUILD_DIR)/$(APP_NAME) ./cmd/app/

run-%:
	go run ./cmd/app/ $(subst run-,,$@)

test:
	go test ./... -v -count=1

test-%:
	go test ./internal/$(subst test-,,$@)/... -v -count=1

clean:
	rm -rf $(BUILD_DIR)

fmt:
	go fmt ./...

lint:
	golangci-lint run ./...
