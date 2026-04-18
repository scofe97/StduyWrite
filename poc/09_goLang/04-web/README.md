# 04-web

Go 웹 개발의 핵심 기술을 학습합니다. HTTP 서버부터 gRPC, TCP까지.

## 구조

```
04-web/
├── learning/
│   ├── 01-http-server.md
│   ├── 02-chi-router.md
│   ├── 03-websocket.md
│   ├── 04-grpc.md
│   └── 05-tcp-to-http.md
├── practice/
│   ├── 01-http-server/
│   ├── 02-chi-router/
│   ├── 03-websocket/
│   ├── 04-grpc/
│   └── 05-tcp-to-http/
└── README.md
```

## 학습 순서

| # | 토픽 | learning | practice |
|---|------|----------|----------|
| 1 | HTTP Server (Gin) | 01 | 01-http-server (go.mod + handlers/ + middleware/ + models/ + 4개) |
| 2 | Chi Router | 02 | 02-chi-router (go.mod + handlers/ + middleware/ + 4개) |
| 3 | WebSocket | 03 | 03-websocket (go.mod + main.go + 4개) |
| 4 | gRPC | 04 | 04-grpc (go.mod + certs/ + client/ + server/ + proto/ + 4개) |
| 5 | TCP to HTTP | 05 | 05-tcp-to-http (7개 step) |

## 주요 라이브러리

| 토픽 | 라이브러리 | 설치 |
|------|-----------|------|
| HTTP Server | gin-gonic/gin | `go get github.com/gin-gonic/gin` |
| Chi Router | go-chi/chi | `go get github.com/go-chi/chi/v5` |
| WebSocket | gorilla/websocket | `go get github.com/gorilla/websocket` |
| gRPC | google.golang.org/grpc | `go get google.golang.org/grpc` |

## 참고 자료

- [Gin 공식 문서](https://github.com/gin-gonic/gin)
- [Chi GitHub](https://github.com/go-chi/chi)
- [gorilla/websocket](https://github.com/gorilla/websocket)
- [gRPC-Go](https://grpc.io/docs/languages/go/)
