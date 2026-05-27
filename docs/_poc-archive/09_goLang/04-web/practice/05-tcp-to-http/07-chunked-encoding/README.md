# 07. Chunked Encoding - 청크 인코딩

## 학습 목표

- Chunked Transfer Encoding 이해
- 스트리밍 응답 구현
- Trailers (트레일러) 구현

## 핵심 개념

### 청크 인코딩이 필요한 경우

1. 파일 크기를 미리 알 수 없을 때
2. 대용량 데이터를 메모리에 로드하지 않고 전송
3. 실시간 스트리밍 응답
4. 프록시 서버에서 응답 중계

### 청크 형식

```
Transfer-Encoding: chunked

20\r\n              <- 청크 크기 (16진수, 32바이트)
<32 bytes data>\r\n <- 데이터 + CRLF
1a\r\n              <- 다음 청크 (26바이트)
<26 bytes data>\r\n
0\r\n               <- 종료 청크 (크기 0)
\r\n                <- 빈 줄로 종료
```

### 16진수 변환

```go
// 10진수 → 16진수
fmt.Sprintf("%x", 32)   // "20"
fmt.Sprintf("%x", 255)  // "ff"

// 20 (hex) = 32 (decimal)
// 0x20 = 0010 0000 (binary) = 32
```

## 실습 과제

### Task 1: 청크 작성 함수

```go
func WriteChunkedBody(w io.Writer, data []byte) error {
    // 1. 크기 (16진수) + CRLF
    // 2. 데이터 + CRLF
}

func WriteChunkedEnd(w io.Writer) error {
    // "0\r\n\r\n" 작성
}
```

### Task 2: 프록시 핸들러

외부 서버 응답을 청크로 중계:

```go
func handleProxy(w *ResponseWriter, r *Request) {
    resp, _ := http.Get("https://httpbin.org/stream/5")

    headers.Delete("Content-Length")
    headers.Set("Transfer-Encoding", "chunked")

    buf := make([]byte, 32)
    for {
        n, err := resp.Body.Read(buf)
        if err == io.EOF {
            break
        }
        WriteChunkedBody(conn, buf[:n])
    }
    WriteChunkedEnd(conn)
}
```

### Task 3: Trailers 구현

```go
// 1. 헤더에 트레일러 선언
headers.Set("Trailer", "X-Checksum, X-Content-Length")

// 2. 청크 전송
// ...

// 3. 트레일러 작성
trailers := NewHeaders()
trailers.Set("X-Checksum", sha256Hash)
WriteTrailers(w, trailers)
```

## 테스트 방법

```bash
# netcat으로 청크 확인 (curl은 청크를 숨김)
echo "GET /proxy/stream/3 HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 42069
```

## 체크리스트

- [ ] 16진수 크기 작성
- [ ] 종료 청크 (0\r\n\r\n)
- [ ] Content-Length 제거
- [ ] Transfer-Encoding: chunked 설정
- [ ] Trailers 구현 (선택)
