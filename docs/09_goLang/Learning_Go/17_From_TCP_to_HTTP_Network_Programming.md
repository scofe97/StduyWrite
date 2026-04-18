# Chapter 17: From TCP to HTTP - Network Programming (면접 정리)

> ThePrimeagen의 "From TCP to HTTP" 강의를 기반으로 정리한 Go 네트워크 프로그래밍 학습 자료

---

## 📚 핵심 개념 정리

### 1. I/O 추상화: 파일과 네트워크의 통일

#### Go의 io.Reader 인터페이스

```go
// 파일 읽기와 네트워크 읽기는 동일한 인터페이스 사용
f, err := os.Open("messages.txt")
data := make([]byte, 8)
n, err := f.Read(data)  // 8바이트씩 읽기

// 네트워크 연결도 동일하게 처리
conn, err := listener.Accept()
n, err := conn.Read(data)  // 동일한 Read 메서드
```

> 💡 **핵심 통찰**: Go에서 파일, 네트워크 연결, 표준 입출력은 모두 `io.Reader`/`io.Writer` 인터페이스를 구현. 이를 통해 코드의 재사용성과 추상화 수준이 높아짐.

---

### 2. TCP vs UDP 프로토콜

#### TCP (Transmission Control Protocol)

| 특성 | 설명 |
|------|------|
| **순서 보장** | 패킷이 전송된 순서대로 도착 |
| **신뢰성** | ACK(확인응답)로 전송 확인 |
| **슬라이딩 윈도우** | 효율적인 데이터 전송 관리 |
| **핸드셰이크** | 3-way handshake로 연결 수립 |
| **스트리밍** | 데이터가 청크 단위로 도착 |

```go
// TCP 리스너 생성
listener, err := net.Listen("tcp", ":42069")
conn, err := listener.Accept()
```

#### UDP (User Datagram Protocol)

| 특성 | 설명 |
|------|------|
| **순서 미보장** | 패킷이 무작위 순서로 도착 가능 |
| **비연결성** | 핸드셰이크 없음 |
| **NACK** | Negative Acknowledgment 사용 |
| **무상태** | 연결 상태 유지 안함 |
| **빠른 속도** | 오버헤드가 적음 |

> 📝 **중요**: TCP는 데이터가 **순서대로** 도착함을 보장하지만, **완전하게** 도착함을 보장하지는 않음. 스트리밍 프로토콜이므로 청크 단위로 데이터 수신.

---

### 3. HTTP 메시지 구조

#### 요청 메시지 (Request)

```
Request Line (요청 라인)     GET /coffee HTTP/1.1
Field Lines (헤더)           Host: localhost:42069
                            Content-Type: text/plain
Empty Line                   \r\n
Message Body (본문)          { "coffee": "americano" }
```

#### 응답 메시지 (Response)

```
Status Line (상태 라인)      HTTP/1.1 200 OK
Field Lines (헤더)           Content-Length: 13
                            Content-Type: text/plain
Empty Line                   \r\n
Message Body (본문)          Hello, World!
```

#### CRLF (Carriage Return Line Feed)

```go
var CRLF = []byte("\r\n")  // 줄 구분자

// 암기 팁: "Registered Nurse" (RN = \r\n)
```

---

### 4. HTTP 파싱 구현

#### Request 구조체 설계

```go
type Request struct {
    RequestLine RequestLine
    Headers     *Headers
    Body        string
    state       ParserState  // 파서 상태 추적
}

type RequestLine struct {
    Method        string  // GET, POST, PUT, DELETE
    RequestTarget string  // /path/to/resource
    HttpVersion   string  // HTTP/1.1
}
```

#### 상태 머신 (State Machine) 패턴

```go
type ParserState string

const (
    StateInit    ParserState = "init"     // 요청 라인 파싱
    StateHeaders ParserState = "headers"  // 헤더 파싱
    StateBody    ParserState = "body"     // 본문 파싱
    StateDone    ParserState = "done"     // 파싱 완료
    StateError   ParserState = "error"    // 오류 상태
)

func (r *Request) Parse(data []byte) (int, error) {
    for {
        switch r.state {
        case StateInit:
            // 요청 라인 파싱
        case StateHeaders:
            // 헤더 파싱
        case StateBody:
            // 본문 파싱
        case StateDone:
            return read, nil
        }
    }
}
```

---

### 5. 헤더 파싱

#### RFC 규격에 따른 필드 라인

```
Field-Line = Field-Name ":" OWS Field-Value OWS CRLF

OWS = Optional White Space (선택적 공백)
```

#### 구현 시 주의사항

```go
// 1. 필드 이름에는 콜론 앞 공백 불허
"Host: localhost"     // ✅ 유효
"Host : localhost"    // ❌ 무효 (필드명과 콜론 사이 공백)

// 2. 대소문자 구분 없음 (Case-Insensitive)
func (h *Headers) Get(name string) (string, bool) {
    name = strings.ToLower(name)  // 정규화
    value, exists := h.headers[name]
    return value, exists
}

// 3. 중복 헤더 처리 (콤마로 연결)
"Set-Cookie: a=1"
"Set-Cookie: b=2"
// → "Set-Cookie: a=1, b=2"
```

---

### 6. 본문 파싱

#### Content-Length 기반 파싱

```go
func (r *Request) parseBody(data []byte) (int, error) {
    length := getIntHeader(r.Headers, "Content-Length", 0)

    if length == 0 {
        r.state = StateDone
        return 0, nil
    }

    remaining := length - len(r.Body)
    toRead := min(remaining, len(data))
    r.Body += string(data[:toRead])

    if len(r.Body) == length {
        r.state = StateDone
    }

    return toRead, nil
}
```

#### Chunked Encoding (청크 인코딩)

- Content-Length 없이 데이터 전송
- 각 청크는 크기 + 데이터 + CRLF
- 크기가 0인 청크로 종료
- Trailers (후행 헤더) 지원

---

### 7. HTTP 서버 구현

#### 기본 서버 구조

```go
type Server struct {
    port   int
    closed bool
}

func Serve(port int) (*Server, error) {
    listener, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
    if err != nil {
        return nil, err
    }

    server := &Server{port: port}

    go func() {
        for !server.closed {
            conn, err := listener.Accept()
            if err != nil {
                continue
            }
            go handleConnection(conn)  // 동시성 처리
        }
    }()

    return server, nil
}
```

#### 응답 작성

```go
func WriteStatusLine(w io.Writer, statusCode int) error {
    var statusLine string
    switch statusCode {
    case 200:
        statusLine = "HTTP/1.1 200 OK\r\n"
    case 400:
        statusLine = "HTTP/1.1 400 Bad Request\r\n"
    case 404:
        statusLine = "HTTP/1.1 404 Not Found\r\n"
    case 500:
        statusLine = "HTTP/1.1 500 Internal Server Error\r\n"
    }
    _, err := w.Write([]byte(statusLine))
    return err
}
```

---

## 🎯 면접 예상 질문

### Q1. TCP와 UDP의 차이점을 설명하세요.

**A**: TCP는 연결 지향 프로토콜로 3-way handshake를 통해 연결을 수립하고, 패킷 순서 보장과 ACK를 통한 신뢰성 있는 전송을 제공합니다. 반면 UDP는 비연결성 프로토콜로 핸드셰이크 없이 바로 데이터를 전송하며, 순서나 도착을 보장하지 않지만 오버헤드가 적어 빠릅니다. HTTP/1.1과 HTTP/2는 TCP 위에서, HTTP/3(QUIC)은 UDP 위에서 자체적인 신뢰성 계층을 구현합니다.

### Q2. Go에서 io.Reader 인터페이스의 의미는?

**A**: `io.Reader`는 Go의 핵심 추상화로, 파일, 네트워크 연결, 문자열, 압축 스트림 등 다양한 소스에서 바이트를 읽는 통일된 인터페이스를 제공합니다. 단 하나의 메서드 `Read(p []byte) (n int, err error)`만 구현하면 되어, 코드 재사용성이 높고 테스트가 용이합니다.

### Q3. HTTP 요청의 구조를 설명하세요.

**A**: HTTP 요청은 네 부분으로 구성됩니다:
1. **Request Line**: 메서드, 경로, HTTP 버전 (예: `GET /api/users HTTP/1.1`)
2. **Headers**: 키-값 쌍의 메타데이터 (예: `Content-Type: application/json`)
3. **Empty Line**: 헤더와 본문을 구분하는 CRLF (`\r\n`)
4. **Body**: 선택적 메시지 본문

각 줄은 CRLF로 구분되며, 빈 줄이 헤더의 끝을 표시합니다.

### Q4. 상태 머신(State Machine) 패턴이 HTTP 파싱에 적합한 이유는?

**A**: HTTP는 스트리밍 프로토콜이므로 데이터가 청크 단위로 도착합니다. 상태 머신을 사용하면:
- 불완전한 데이터를 처리하고 나중에 이어서 파싱 가능
- 각 상태(요청라인→헤더→본문)의 전환을 명확히 관리
- 에러 상태를 독립적으로 처리
- 한 번의 호출로 여러 상태 전환 수행 가능

### Q5. Content-Length 헤더의 역할은?

**A**: Content-Length는 본문의 정확한 바이트 수를 미리 알려줍니다. 수신측은 이 값만큼 읽으면 본문이 끝났음을 알 수 있습니다. Content-Length가 없으면 연결이 닫힐 때까지 읽거나, Chunked Transfer Encoding을 사용해야 합니다. RFC에 따르면 요청에는 Content-Length를 "should(권장)" 포함하도록 규정합니다.

---

## 💻 실습 포인트

### 1. 바이트 단위 읽기 연습
```go
// 8바이트씩 파일 읽기
data := make([]byte, 8)
for {
    n, err := file.Read(data)
    if err == io.EOF {
        break
    }
    fmt.Printf("Read %d bytes: %s\n", n, data[:n])
}
```

### 2. TCP 서버 구현
```go
listener, _ := net.Listen("tcp", ":8080")
for {
    conn, _ := listener.Accept()
    go handleConnection(conn)  // 고루틴으로 동시 처리
}
```

### 3. HTTP 파서 테스트
```go
func TestParseRequestLine(t *testing.T) {
    input := []byte("GET /coffee HTTP/1.1\r\n")
    rl, _, err := parseRequestLine(input)

    require.NoError(t, err)
    assert.Equal(t, "GET", rl.Method)
    assert.Equal(t, "/coffee", rl.RequestTarget)
    assert.Equal(t, "1.1", rl.HttpVersion)
}
```

---

## 📊 성능 고려사항

| 요소 | 권장사항 |
|------|----------|
| **버퍼 크기** | 1KB~4KB (헤더 파싱), 8KB~64KB (본문) |
| **메모리 할당** | 재사용 가능한 버퍼 풀 사용 |
| **파싱 전략** | 스트리밍 파싱으로 메모리 효율화 |
| **동시성** | 각 연결마다 고루틴 할당 |
| **연결 관리** | Keep-Alive로 연결 재사용 |

---

## 🔗 관련 RFC 문서

- **RFC 9110**: HTTP Semantics (의미론)
- **RFC 9112**: HTTP/1.1 Message Syntax (메시지 구문)
- **RFC 2119**: RFC 내 키워드 정의 (MUST, SHOULD, MAY 등)

---

### 8. Response Writer 패턴

Go 표준 라이브러리의 `http.ResponseWriter`와 유사한 패턴입니다.

```go
// Handler 함수 시그니처 (Go 표준 라이브러리와 유사)
type Handler func(w *ResponseWriter, r *Request)

// ResponseWriter 구조체
type ResponseWriter struct {
    writer io.Writer  // 기저 연결 (net.Conn)
}

func NewWriter(w io.Writer) *ResponseWriter {
    return &ResponseWriter{writer: w}
}

func (w *ResponseWriter) WriteStatusLine(statusCode int) error {
    // HTTP/1.1 200 OK\r\n
}

func (w *ResponseWriter) WriteHeaders(h *Headers) error {
    // 모든 헤더 작성 후 빈 줄 추가
}

func (w *ResponseWriter) WriteBody(body []byte) (int, error) {
    return w.writer.Write(body)
}
```

> 💡 **설계 이유**: Handler가 응답을 직접 제어할 수 있게 하면서, 상태 코드, 헤더, 본문 작성을 캡슐화합니다.

---

### 9. Chunked Encoding (청크 인코딩) 상세

파일 크기를 미리 알 수 없거나 스트리밍 데이터를 전송할 때 사용합니다.

#### 청크 인코딩 형식

```
Transfer-Encoding: chunked

<chunk-size in hex>\r\n
<chunk-data>\r\n
<chunk-size in hex>\r\n
<chunk-data>\r\n
0\r\n
\r\n
```

#### 구현 예시

```go
func WriteChunkedBody(w io.Writer, data []byte) error {
    // 1. 청크 크기 (16진수) + CRLF
    size := fmt.Sprintf("%x\r\n", len(data))
    w.Write([]byte(size))

    // 2. 데이터 + CRLF
    w.Write(data)
    w.Write([]byte("\r\n"))

    return nil
}

func WriteChunkedEnd(w io.Writer) error {
    // 크기 0인 청크로 종료
    _, err := w.Write([]byte("0\r\n\r\n"))
    return err
}
```

#### 16진수 변환

```go
// 32 (10진수) = 20 (16진수)
fmt.Sprintf("%x", 32)  // "20"

// 0x20 = 0010 0000 (2진수) = 32 (10진수)
```

---

### 10. Trailers (트레일러)

청크 인코딩 후 추가되는 헤더입니다.

```
HTTP/1.1 200 OK
Transfer-Encoding: chunked
Trailer: X-Checksum, X-Content-Length

20\r\n
<32 bytes of data>\r\n
0\r\n
X-Checksum: abc123...\r\n
X-Content-Length: 1024\r\n
\r\n
```

#### 트레일러 사용 규칙

1. **사전 선언 필수**: `Trailer` 헤더에 트레일러 이름 명시
2. **동적 계산 값에 적합**: 체크섬, 최종 길이 등
3. **빈 줄로 종료**: 헤더와 동일하게 CRLF로 종료

```go
// 트레일러 설정
headers.Set("Trailer", "X-Checksum, X-Content-Length")

// 청크 전송 후 트레일러 작성
trailers := NewHeaders()
trailers.Set("X-Checksum", sha256Hash)
trailers.Set("X-Content-Length", fmt.Sprintf("%d", totalLength))
WriteTrailers(w, trailers)
```

---

### 11. Binary Data 전송

HTTP는 텍스트 프로토콜이지만 바이너리 데이터도 전송 가능합니다.

```go
// Content-Type으로 바이너리 형식 지정
headers.Set("Content-Type", "image/png")      // 이미지
headers.Set("Content-Type", "video/mp4")      // 비디오
headers.Set("Content-Type", "application/pdf") // PDF

// 파일 전송 예시
func handleVideo(w *ResponseWriter, r *Request) {
    data, _ := os.ReadFile("video.mp4")

    headers := GetDefaultHeaders(len(data))
    headers.Replace("Content-Type", "video/mp4")

    w.WriteStatusLine(200)
    w.WriteHeaders(headers)
    w.WriteBody(data)
}
```

---

### 12. HTTP/2 및 HTTP/3 비교

| 특성 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|--------|--------|
| **전송 계층** | TCP | TCP | UDP (QUIC) |
| **형식** | 텍스트 | 바이너리 | 바이너리 |
| **다중화** | 불가 | 가능 | 가능 |
| **헤더 압축** | 없음 | HPACK | QPACK |
| **서버 푸시** | 없음 | 지원 | 지원 |
| **암호화** | 선택적 (HTTPS) | 사실상 필수 | 필수 |

> 📝 **HTTP/3**: UDP 위에서 TCP의 신뢰성을 구현한 QUIC 프로토콜 사용. 빠른 연결 수립과 패킷 손실에 강함.

---

## 🎯 추가 면접 예상 질문

### Q6. Chunked Encoding은 언제 사용하나요?

**A**: 다음 상황에서 사용합니다:
1. **스트리밍 데이터**: 전체 크기를 미리 알 수 없는 경우
2. **대용량 파일**: 10GB 파일을 메모리에 로드하지 않고 전송
3. **실시간 응답**: 서버가 데이터를 생성하면서 바로 전송
4. **프록시 서버**: 다른 서버의 응답을 중계할 때

Content-Length 대신 `Transfer-Encoding: chunked` 헤더를 사용합니다.

### Q7. HTTP Trailers의 용도는?

**A**: 트레일러는 본문 전송 후에만 알 수 있는 메타데이터를 전달합니다:
- **체크섬**: SHA-256 해시로 데이터 무결성 검증
- **최종 크기**: 실제 전송된 바이트 수
- **처리 결과**: 스트리밍 처리 중 발생한 정보

`Trailer` 헤더에 미리 트레일러 이름을 선언해야 합니다.

### Q8. HTTP/2와 HTTP/3의 주요 차이점은?

**A**:
- **HTTP/2**: TCP 기반, HPACK 헤더 압축, Head-of-Line Blocking 문제 존재
- **HTTP/3**: QUIC(UDP) 기반, QPACK 헤더 압축, 패킷 손실에 강함, 연결 수립 더 빠름

HTTP/3는 모바일 환경이나 불안정한 네트워크에서 더 나은 성능을 제공합니다.

---

## 핵심 요약

1. **I/O 추상화**: Go의 `io.Reader`/`io.Writer`로 파일과 네트워크를 동일하게 처리
2. **TCP 특성**: 순서 보장, 신뢰성 있는 전송, 스트리밍 프로토콜
3. **HTTP 구조**: 시작 라인 + 헤더 + 빈 줄 + 본문
4. **CRLF**: `\r\n`은 HTTP의 줄 구분자 (암기: Registered Nurse)
5. **상태 머신**: 스트리밍 데이터 파싱의 핵심 패턴
6. **헤더 규칙**: 대소문자 무시, 중복시 콤마 연결
7. **Content-Length**: 본문 크기 결정의 핵심 헤더
8. **Chunked Encoding**: 크기 미상 데이터의 스트리밍 전송
9. **Trailers**: 본문 후 동적 계산 메타데이터 전송
10. **HTTP/2, HTTP/3**: 바이너리 프로토콜, 다중화, 헤더 압축
