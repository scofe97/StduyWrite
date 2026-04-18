# Stage 1: Build
FROM golang:1.25-alpine AS builder

RUN apk add --no-cache git

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /git-provider ./cmd/server

# Stage 2: Run
FROM alpine:3.20

RUN apk add --no-cache ca-certificates

COPY --from=builder /git-provider /usr/local/bin/git-provider

EXPOSE 50051 8080

ENTRYPOINT ["git-provider"]
