# 06. HTTP Server - 완전한 HTTP 서버

## 학습 목표

- HTTP 응답 메시지 작성
- 요청-응답 사이클 완성
- 핸들러 패턴 구현

## 핵심 개념

### HTTP 응답 구조

```
Status Line     HTTP/1.1 200 OK\r\n
Headers         Content-Type: text/plain\r\n
                Content-Length: 13\r\n
                Connection: close\r\n
Empty Line      \r\n
Body            Hello, World!
```

### 상태 코드

| 코드 | 의미 |
|------|------|
| 200 | OK |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |

## 실습 과제

### Task 1: 응답 작성 함수

```go
func WriteStatusLine(w io.Writer, statusCode int) error
func WriteHeaders(w io.Writer, headers *Headers) error
```

### Task 2: 서버 구조체

```go
type Server struct {
    port     int
    listener net.Listener
}

func Serve(port int) (*Server, error)
func (s *Server) Close() error
```

### Task 3: 연결 처리

```go
func handleConnection(conn net.Conn) {
    defer conn.Close()

    // 1. 요청 파싱
    request, err := RequestFromReader(conn)

    // 2. 응답 작성
    WriteStatusLine(conn, 200)
    headers := GetDefaultHeaders(len(body))
    WriteHeaders(conn, headers)
    conn.Write([]byte(body))
}
```

## 테스트 방법

```bash
# 서버 실행
go run .

# 다른 터미널에서 테스트
curl -v http://localhost:42069/hello
```

## 체크리스트

- [ ] 상태 라인 작성
- [ ] 기본 헤더 설정 (Content-Length, Content-Type, Connection)
- [ ] 동시 연결 처리 (고루틴)
- [ ] Graceful shutdown
