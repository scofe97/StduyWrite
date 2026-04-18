# Chapter 13: The Standard Library - 면접정리

## 핵심 개념 상세 설명

### 1. Go의 "배터리 포함" 철학

Go 표준 라이브러리는 현대 프로그래밍에 필요한 대부분의 기능을 제공합니다. 네트워킹, 파일 I/O, JSON 처리, 암호화, 테스팅 등 외부 의존성 없이 프로덕션 수준의 애플리케이션을 작성할 수 있습니다. 이 철학의 핵심은 단순하고 강력한 인터페이스 설계에 있습니다. 특히 io.Reader와 io.Writer는 Go 표준 라이브러리의 근간을 이루는 인터페이스로, 파일, 네트워크, 압축, 암호화 등 모든 I/O 작업이 이 두 인터페이스를 중심으로 동작합니다.

### 2. io.Reader와 io.Writer 인터페이스

io 패키지의 핵심 인터페이스는 놀라울 정도로 단순합니다. Reader는 Read 메서드 하나만, Writer는 Write 메서드 하나만 정의합니다.

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}
```

Read 메서드가 []byte를 반환하지 않고 매개변수로 받는 설계에는 중요한 이유가 있습니다. 호출자가 버퍼를 제공하면 버퍼를 재사용할 수 있어 메모리 할당을 최소화하고 가비지 컬렉션 부하를 줄입니다. 이는 고성능 서버 애플리케이션에서 특히 중요합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│              io.Reader Read Pattern                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   buf := make([]byte, 4096)  // 버퍼 한 번 생성                │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  for {                                                   │   │
│   │      n, err := reader.Read(buf)                         │   │
│   │                                                          │   │
│   │      ┌─────────────────────────────────────────────┐     │   │
│   │      │  STEP 1: Process data FIRST                 │     │   │
│   │      │  for _, b := range buf[:n] { ... }          │     │   │
│   │      │                                              │     │   │
│   │      │  ⚠️ n bytes may be returned WITH error!     │     │   │
│   │      └─────────────────────────────────────────────┘     │   │
│   │                                                          │   │
│   │      ┌─────────────────────────────────────────────┐     │   │
│   │      │  STEP 2: Check error AFTER                  │     │   │
│   │      │  if err == io.EOF { return result }         │     │   │
│   │      │  if err != nil { return err }               │     │   │
│   │      └─────────────────────────────────────────────┘     │   │
│   │  }                                                       │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   Key: io.EOF is not an error, it signals normal completion    │
└─────────────────────────────────────────────────────────────────┘
```

Read 메서드 사용 시 반드시 지켜야 할 규칙이 있습니다. 에러를 확인하기 전에 반드시 데이터를 먼저 처리해야 합니다. Read는 데이터와 함께 에러(특히 io.EOF)를 동시에 반환할 수 있기 때문입니다. io.EOF는 에러가 아니라 정상적인 스트림 종료 신호입니다.

### 3. Decorator 패턴과 Reader/Writer 체이닝

io 인터페이스의 진정한 강점은 Decorator 패턴을 통한 조합입니다. 기본 Reader에 기능을 덧씌워 압축, 암호화, 버퍼링 등을 추가할 수 있습니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Reader Chaining                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Application                                                   │
│       │                                                         │
│       ▼                                                         │
│   ┌──────────────────┐                                          │
│   │   gzip.Reader    │ ←── Decompresses data                    │
│   │   (Decorator)    │                                          │
│   └────────┬─────────┘                                          │
│            │                                                    │
│            ▼                                                    │
│   ┌──────────────────┐                                          │
│   │   bufio.Reader   │ ←── Adds buffering                       │
│   │   (Decorator)    │                                          │
│   └────────┬─────────┘                                          │
│            │                                                    │
│            ▼                                                    │
│   ┌──────────────────┐                                          │
│   │    os.File       │ ←── Base Reader (disk file)              │
│   │   (Source)       │                                          │
│   └──────────────────┘                                          │
│                                                                 │
│   Same countLetters() function works with:                      │
│   - Plain file, Gzipped file, Network stream, etc.              │
└─────────────────────────────────────────────────────────────────┘
```

이 패턴의 장점은 동일한 로직(예: 문자 수 세기)이 다양한 입력 소스에서 변경 없이 동작한다는 것입니다. 파일, 압축 파일, 네트워크 소켓, 메모리 버퍼 모두 io.Reader 인터페이스만 구현하면 됩니다.

### 4. time 패키지: Duration과 Time

Go의 time 패키지는 시간 처리의 모든 측면을 다룹니다. time.Duration은 경과 시간을 나타내는 정수형으로, int64 기반의 나노초 정밀도를 제공합니다. time.Time은 특정 시점을 나타내며, 내부적으로 wall clock과 monotonic clock을 모두 저장합니다.

```go
// Duration 생성과 사용
d := 2*time.Hour + 30*time.Minute  // 2시간 30분
d.Hours()   // 2.5 (float64)
d.Minutes() // 150.0 (float64)
d.Truncate(time.Hour)  // 2h0m0s (내림)
d.Round(time.Hour)     // 3h0m0s (반올림)

// Time 생성과 사용
now := time.Now()
t := time.Date(2024, time.March, 15, 14, 30, 0, 0, time.UTC)
```

Time 비교에서 중요한 점은 == 연산자 대신 Equal 메서드를 사용해야 한다는 것입니다. Equal은 타임존이 다르더라도 동일한 순간을 나타내면 true를 반환합니다. == 연산자는 내부 표현까지 정확히 같아야 true를 반환하므로 예상치 못한 결과가 발생할 수 있습니다.

### 5. Go의 시간 포맷팅: 레퍼런스 타임

Go는 독특한 시간 포맷팅 방식을 사용합니다. strftime 스타일의 %Y, %m, %d 대신 특정 레퍼런스 시간을 사용합니다. 이 레퍼런스 시간은 2006년 1월 2일 오후 3시 4분 5초입니다. 각 숫자가 고유하므로 파서가 어떤 부분이 연도, 월, 일인지 식별할 수 있습니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                 Go Time Reference                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Reference: Mon Jan 2 15:04:05 MST 2006                        │
│              01/02 03:04:05PM '06 -0700                         │
│                                                                 │
│   ┌─────────┬─────────────────────────────────────────────┐     │
│   │ Element │            Value & Meaning                  │     │
│   ├─────────┼─────────────────────────────────────────────┤     │
│   │  Year   │  2006 or 06                                 │     │
│   │  Month  │  01, Jan, January                           │     │
│   │  Day    │  02, 2, _2                                  │     │
│   │  Hour   │  15 (24h) or 03 (12h)                       │     │
│   │  Minute │  04                                         │     │
│   │  Second │  05                                         │     │
│   │  Zone   │  MST, -0700, Z07:00                         │     │
│   └─────────┴─────────────────────────────────────────────┘     │
│                                                                 │
│   Example:                                                      │
│   layout := "2006-01-02T15:04:05Z07:00"  // RFC3339             │
│   t.Format(layout) → "2024-03-15T14:30:00+09:00"                │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Monotonic Clock vs Wall Clock

시간 측정에서 중요한 개념이 있습니다. Wall Clock은 실제 시계 시간으로 NTP 동기화나 일광절약시간 변경으로 점프할 수 있습니다. 반면 Monotonic Clock은 시스템 부팅 후 단조 증가하는 타이머로, 경과 시간 측정에 적합합니다.

Go는 이 문제를 자동으로 처리합니다. time.Now()로 생성된 Time 값은 wall clock과 monotonic clock 모두를 저장하고, time.Since()나 두 Time 값의 Sub 연산 시 자동으로 monotonic clock을 사용합니다. 따라서 개발자가 별도로 신경 쓸 필요가 없습니다.

### 7. encoding/json: Struct Tags

JSON 마샬링/언마샬링에서 struct tag는 필드 이름 매핑, 필드 제외, 빈 값 처리를 제어합니다.

```go
type User struct {
    ID        int       `json:"id"`                    // JSON 키 이름 지정
    Email     string    `json:"email,omitempty"`       // 빈 값이면 제외
    Password  string    `json:"-"`                     // 항상 제외
    CreatedAt time.Time `json:"created_at"`
}
```

omitempty 옵션의 동작을 정확히 이해해야 합니다. string의 경우 빈 문자열 "", int의 경우 0, 포인터의 경우 nil이 빈 값입니다. 하지만 struct의 zero value는 빈 값으로 취급되지 않습니다. 중첩된 struct를 조건부로 제외하려면 포인터로 선언해야 합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                  omitempty Behavior                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Type          │  Empty Value  │  omitempty Behavior           │
│   ──────────────┼───────────────┼────────────────────────────   │
│   string        │  ""           │  ✓ Omitted                    │
│   int/float     │  0            │  ✓ Omitted                    │
│   bool          │  false        │  ✓ Omitted                    │
│   pointer       │  nil          │  ✓ Omitted                    │
│   slice/map     │  nil          │  ✓ Omitted                    │
│   slice/map     │  empty []     │  ✗ NOT omitted (len=0)        │
│   struct        │  zero value   │  ✗ NOT omitted                │
│   *struct       │  nil          │  ✓ Omitted                    │
│                                                                 │
│   ⚠️ For conditional struct exclusion, use *Struct (pointer)   │
└─────────────────────────────────────────────────────────────────┘
```

### 8. JSON 스트림 처리: Encoder/Decoder

작은 JSON 데이터는 json.Marshal/Unmarshal을 사용하지만, 스트림 처리나 대용량 데이터에는 json.Encoder/Decoder가 적합합니다. Encoder와 Decoder는 io.Writer와 io.Reader 인터페이스를 사용하므로 파일, 네트워크 연결, HTTP 응답 등 모든 I/O 소스와 함께 작동합니다.

```go
// HTTP 응답 Body에서 직접 디코딩 (메모리 효율적)
var data Response
err := json.NewDecoder(res.Body).Decode(&data)

// 스트림에서 여러 JSON 객체 읽기
dec := json.NewDecoder(reader)
for dec.More() {
    var item Item
    if err := dec.Decode(&item); err != nil {
        return err
    }
    process(item)
}
```

### 9. net/http: Client 모범 사례

HTTP 클라이언트를 사용할 때 가장 중요한 규칙은 타임아웃 설정입니다. http.DefaultClient는 타임아웃이 없어 요청이 영원히 블록될 수 있습니다. 프로덕션 코드에서는 반드시 타임아웃을 설정한 클라이언트를 사용해야 합니다.

```go
// ✗ 피해야 할 코드 - 타임아웃 없음
res, err := http.Get("https://api.example.com/data")

// ✓ 올바른 방법 - 타임아웃 설정
client := &http.Client{
    Timeout: 30 * time.Second,
}
res, err := client.Get("https://api.example.com/data")
```

```
┌─────────────────────────────────────────────────────────────────┐
│               HTTP Client Best Practices                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   client := &http.Client{                                       │
│       Timeout: 30 * time.Second,    // 전체 요청 타임아웃       │
│       Transport: &http.Transport{                               │
│           MaxIdleConns:        100, // 전체 idle 연결 수        │
│           MaxIdleConnsPerHost: 10,  // 호스트당 idle 연결       │
│           IdleConnTimeout:     90 * time.Second,                │
│       },                                                        │
│   }                                                             │
│                                                                 │
│   // Context로 요청별 취소 가능하게                             │
│   req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)    │
│   res, err := client.Do(req)                                    │
│   if err != nil { return err }                                  │
│   defer res.Body.Close()  // ⚠️ 반드시 Body 닫기              │
│                                                                 │
│   Key Rules:                                                    │
│   1. Always set Timeout                                         │
│   2. Reuse client (create once, use many times)                 │
│   3. Always close res.Body                                      │
│   4. Use Context for cancellation                               │
└─────────────────────────────────────────────────────────────────┘
```

### 10. net/http: Server와 ServeMux

Go의 HTTP 서버는 http.Handler 인터페이스를 중심으로 동작합니다. ServeMux는 URL 경로를 핸들러에 매핑하는 라우터입니다. Go 1.22부터는 HTTP 메서드와 경로 변수를 직접 지원합니다.

```go
mux := http.NewServeMux()

// Go 1.22+ 라우팅
mux.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    // ...
})

mux.HandleFunc("POST /users", createUserHandler)
mux.HandleFunc("DELETE /users/{id}", deleteUserHandler)
```

http.DefaultServeMux 사용은 피해야 합니다. 전역 상태를 사용하므로 테스트가 어렵고, 서드파티 패키지가 핸들러를 등록할 수 있어 보안 위험이 있습니다.

### 11. 미들웨어 패턴

미들웨어는 func(http.Handler) http.Handler 시그니처를 따르는 함수로, 핸들러를 감싸서 전처리/후처리를 추가합니다. 로깅, 인증, 압축, CORS 등 횡단 관심사를 처리하는 데 사용합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                   Middleware Chain                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Request                                                       │
│      │                                                          │
│      ▼                                                          │
│   ┌───────────────────────────────────────────────────────┐     │
│   │  Logging Middleware                                   │     │
│   │  - Log request start                                  │     │
│   │      │                                                │     │
│   │      ▼                                                │     │
│   │  ┌─────────────────────────────────────────────────┐  │     │
│   │  │  Auth Middleware                                │  │     │
│   │  │  - Validate token                               │  │     │
│   │  │      │                                          │  │     │
│   │  │      ▼                                          │  │     │
│   │  │  ┌─────────────────────────────────────────┐    │  │     │
│   │  │  │  Business Handler                       │    │  │     │
│   │  │  │  - Process request                      │    │  │     │
│   │  │  │  - Write response                       │    │  │     │
│   │  │  └─────────────────────────────────────────┘    │  │     │
│   │  │      │                                          │  │     │
│   │  │  - (post-processing if any)                     │  │     │
│   │  └─────────────────────────────────────────────────┘  │     │
│   │      │                                                │     │
│   │  - Log request duration                               │     │
│   └───────────────────────────────────────────────────────┘     │
│      │                                                          │
│      ▼                                                          │
│   Response                                                      │
└─────────────────────────────────────────────────────────────────┘

Code:
handler := LoggingMW(AuthMW(businessHandler))
// 또는
handler := chain(LoggingMW, AuthMW)(businessHandler)
```

```go
// 미들웨어 구현 예시
func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        slog.Info("request started", "path", r.URL.Path)

        next.ServeHTTP(w, r)  // 다음 핸들러 호출

        slog.Info("request completed",
            "path", r.URL.Path,
            "duration", time.Since(start))
    })
}
```

### 12. log/slog: 구조화된 로깅

Go 1.21에서 도입된 log/slog는 구조화된 로깅의 표준입니다. 키-값 쌍으로 구조화된 데이터를 로깅하여 로그 분석 도구에서 쉽게 파싱하고 검색할 수 있습니다.

```go
// 기본 사용
slog.Info("user login", "user_id", userID, "ip", clientIP)
// 출력: 2024/03/15 14:30:00 INFO user login user_id=123 ip=192.168.1.1

// JSON 출력
handler := slog.NewJSONHandler(os.Stdout, nil)
logger := slog.New(handler)
logger.Info("user login", "user_id", userID, "ip", clientIP)
// 출력: {"time":"...","level":"INFO","msg":"user login","user_id":123,"ip":"192.168.1.1"}
```

성능이 중요한 경우 LogAttrs 메서드를 사용합니다. 일반 Info/Error 메서드는 인터페이스로 값을 전달하므로 할당이 발생하지만, LogAttrs는 타입이 정해진 속성을 사용해 할당을 최소화합니다.

---

## 비교표

### io 인터페이스 조합

| 인터페이스 | 조합 | 용도 |
|-----------|------|------|
| Reader | 기본 | 읽기 전용 |
| Writer | 기본 | 쓰기 전용 |
| Closer | 기본 | 닫기 전용 |
| ReadCloser | Reader + Closer | 파일 읽기 |
| WriteCloser | Writer + Closer | 파일 쓰기 |
| ReadWriter | Reader + Writer | 양방향 I/O |
| ReadWriteCloser | Reader + Writer + Closer | 네트워크 연결 |

### Marshal/Unmarshal vs Encoder/Decoder

| 특성 | Marshal/Unmarshal | Encoder/Decoder |
|------|-------------------|-----------------|
| 입출력 | []byte | io.Reader/Writer |
| 메모리 | 전체 버퍼 필요 | 스트림 처리 |
| 용도 | 작은 데이터 | 대용량/스트림 |
| 복수 객체 | 수동 처리 | 자동 처리 |

### 시간 상수

| 상수 | 형식 | 예시 |
|------|------|------|
| RFC3339 | 2006-01-02T15:04:05Z07:00 | 2024-03-15T14:30:00+09:00 |
| RFC822 | 02 Jan 06 15:04 MST | 15 Mar 24 14:30 KST |
| Kitchen | 3:04PM | 2:30PM |
| DateOnly | 2006-01-02 | 2024-03-15 |
| TimeOnly | 15:04:05 | 14:30:00 |

### slog 레벨

| 레벨 | 값 | 용도 |
|------|-----|------|
| Debug | -4 | 개발 디버깅 |
| Info | 0 | 일반 정보 |
| Warn | 4 | 경고 |
| Error | 8 | 오류 |

---

## 면접 예상 질문 및 모범 답안

### Q1. io.Reader의 Read 메서드가 왜 []byte를 반환하지 않고 매개변수로 받나요? 이 설계의 장점은 무엇인가요?

**모범 답안:**

Read 메서드가 버퍼를 매개변수로 받는 설계는 메모리 효율성을 위한 것입니다.

만약 Read가 []byte를 반환한다면 매번 새로운 슬라이스를 할당해야 합니다. 큰 파일을 4KB 청크로 읽는다면 수천 번의 할당이 발생하고, 이 모든 슬라이스가 가비지 컬렉터에 의해 수집되어야 합니다.

현재 설계에서는 호출자가 버퍼를 한 번 생성하고 반복해서 재사용할 수 있습니다. 이는 할당을 최소화하고 GC 부하를 크게 줄입니다. 고성능 서버에서 초당 수천 개의 요청을 처리할 때 이 차이는 매우 중요합니다.

또한 이 설계는 호출자가 버퍼 크기를 제어할 수 있게 합니다. 작은 데이터에는 작은 버퍼를, 대용량 전송에는 큰 버퍼를 사용하여 최적의 성능을 얻을 수 있습니다. 반환된 n 값으로 실제로 읽은 바이트 수를 알 수 있고, 에러와 함께 부분 데이터도 받을 수 있어 더 세밀한 제어가 가능합니다.

---

### Q2. io.EOF 처리 시 주의할 점은 무엇인가요? Read 메서드에서 에러를 어떻게 처리해야 하나요?

**모범 답안:**

io.EOF는 에러가 아니라 정상적인 스트림 종료 신호입니다. 파일 끝이나 네트워크 스트림 종료를 나타냅니다.

Read 메서드 사용 시 가장 중요한 규칙은 에러를 확인하기 전에 반드시 데이터를 먼저 처리해야 한다는 것입니다. Read는 마지막 데이터 청크와 함께 io.EOF를 반환할 수 있습니다. 에러를 먼저 확인하면 마지막 데이터를 놓칠 수 있습니다.

```go
for {
    n, err := reader.Read(buf)
    // 1. 먼저 데이터 처리 (n > 0인 경우)
    processData(buf[:n])
    // 2. 그 다음 에러 확인
    if err == io.EOF {
        return nil  // 정상 종료
    }
    if err != nil {
        return err  // 실제 에러
    }
}
```

errors.Is(err, io.EOF)를 사용하는 것도 좋은 방법입니다. 래핑된 에러도 정확히 비교할 수 있습니다. io.EOF를 errors.New로 새로 생성하거나 래핑하면 안 됩니다. 표준 라이브러리의 함수들이 io.EOF를 특별히 처리하기 때문입니다.

---

### Q3. Go의 시간 포맷팅이 다른 언어와 다른 점을 설명하고, 레퍼런스 타임의 의미를 설명해주세요.

**모범 답안:**

Go는 strftime 스타일의 %Y, %m, %d 같은 포맷 지정자 대신 특정 레퍼런스 시간을 사용합니다. 이 레퍼런스 시간은 2006년 1월 2일 오후 3시 4분 5초 MST입니다.

이 시간이 선택된 이유는 각 구성 요소가 고유한 숫자를 가지기 때문입니다. 월은 1, 일은 2, 시는 15(24시간) 또는 3(12시간), 분은 4, 초는 5, 연도는 6입니다. 숫자로 표현하면 01/02 03:04:05 '06입니다. 미국식 월/일/연도 순서로 1, 2, 3, 4, 5, 6이 됩니다.

이 접근 방식의 장점은 포맷 문자열이 실제 출력의 예시처럼 보인다는 것입니다. "2006-01-02"라는 포맷은 "2024-03-15" 같은 출력을 생성한다는 것이 직관적으로 이해됩니다. 단점은 처음 배울 때 이 특정 날짜를 암기해야 한다는 것입니다.

time 패키지는 time.RFC3339, time.Kitchen 같은 미리 정의된 상수도 제공하여 자주 사용되는 포맷을 쉽게 사용할 수 있습니다.

---

### Q4. http.DefaultClient를 사용하면 안 되는 이유는 무엇인가요? 프로덕션에서 HTTP 클라이언트를 어떻게 구성해야 하나요?

**모범 답안:**

http.DefaultClient는 타임아웃이 설정되어 있지 않습니다. 이는 원격 서버가 응답하지 않으면 요청이 영원히 블록될 수 있다는 의미입니다. 프로덕션 환경에서 이는 goroutine 누수, 연결 고갈, 서비스 중단으로 이어질 수 있습니다.

프로덕션에서는 다음과 같이 클라이언트를 구성해야 합니다.

첫째, 반드시 Timeout을 설정합니다. 전체 요청에 대한 최대 시간을 지정합니다. 둘째, Transport를 구성하여 연결 풀을 관리합니다. MaxIdleConns, MaxIdleConnsPerHost, IdleConnTimeout을 설정하여 연결을 효율적으로 재사용합니다. 셋째, 클라이언트를 재사용합니다. 요청마다 새 클라이언트를 생성하면 연결 재사용의 이점을 잃습니다.

```go
var httpClient = &http.Client{
    Timeout: 30 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
    },
}
```

추가로 context를 사용하여 요청별 타임아웃이나 취소를 지원하고, res.Body를 항상 닫아 연결이 풀로 반환되도록 해야 합니다.

---

### Q5. Go HTTP 서버에서 미들웨어 패턴을 설명하고 구현 방법을 보여주세요.

**모범 답안:**

미들웨어는 HTTP 핸들러를 감싸서 전처리와 후처리를 추가하는 패턴입니다. Go에서는 func(http.Handler) http.Handler 시그니처로 구현합니다. 핸들러를 받아서 새로운 핸들러를 반환하며, 내부에서 원래 핸들러를 호출합니다.

```go
func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        slog.Info("request started", "method", r.Method, "path", r.URL.Path)

        next.ServeHTTP(w, r)  // 다음 핸들러 호출

        slog.Info("request completed", "duration", time.Since(start))
    })
}
```

미들웨어는 체이닝하여 사용합니다. 가장 바깥 미들웨어가 먼저 실행되고, 안쪽으로 들어가면서 각 미들웨어의 전처리가 실행됩니다. 핵심 핸들러가 실행된 후 역순으로 후처리가 실행됩니다.

```go
handler := LoggingMiddleware(AuthMiddleware(RateLimitMiddleware(businessHandler)))
```

이 패턴은 로깅, 인증, 권한 확인, 요청 속도 제한, CORS 처리, 압축, 에러 복구 등 횡단 관심사를 깔끔하게 분리합니다. 각 미들웨어는 단일 책임을 가지며 독립적으로 테스트할 수 있습니다.

---

### Q6. json.Marshal/Unmarshal과 json.Encoder/Decoder의 차이점과 각각 언제 사용해야 하는지 설명해주세요.

**모범 답안:**

json.Marshal과 Unmarshal은 []byte와 Go 값 사이의 변환을 수행합니다. 전체 데이터가 메모리에 있어야 하며, 결과도 []byte로 메모리에 저장됩니다. 작은 JSON 데이터를 처리할 때 간단하게 사용할 수 있습니다.

json.Encoder와 Decoder는 io.Writer와 io.Reader를 대상으로 작업합니다. 스트림 기반이므로 전체 데이터를 메모리에 로드하지 않고 처리할 수 있습니다.

Encoder/Decoder를 사용해야 하는 경우는 다음과 같습니다. HTTP 응답 Body에서 직접 디코딩할 때 중간 []byte 변환 없이 처리할 수 있어 효율적입니다. 대용량 JSON 파일을 처리할 때 메모리 사용을 제어할 수 있습니다. 한 스트림에 여러 JSON 객체가 있을 때 Decoder의 More() 메서드로 순차 처리할 수 있습니다. 파일에 JSON을 쓸 때 Encoder를 사용하면 직접 쓸 수 있습니다.

```go
// HTTP 응답 처리 - Decoder 사용
err := json.NewDecoder(res.Body).Decode(&data)

// API 응답 작성 - Encoder 사용
w.Header().Set("Content-Type", "application/json")
err := json.NewEncoder(w).Encode(response)
```

작은 설정 파일이나 단순한 데이터 구조에는 Marshal/Unmarshal이 더 간단합니다.

---

## 실무 체크리스트

### io 사용 시
- [ ] Read 루프에서 에러 확인 전 데이터를 먼저 처리하는가?
- [ ] io.EOF를 정상 종료로 처리하는가?
- [ ] 버퍼를 루프 밖에서 생성하여 재사용하는가?
- [ ] Closer를 defer로 닫는가?

### time 사용 시
- [ ] Time 비교에 Equal() 메서드를 사용하는가?
- [ ] 포맷 문자열에 Go 레퍼런스 타임(2006-01-02 15:04:05)을 사용하는가?
- [ ] 경과 시간 측정에 time.Since() 또는 Sub()을 사용하는가?
- [ ] Ticker를 Stop()으로 정리하는가?

### JSON 사용 시
- [ ] 적절한 struct tag를 사용하는가?
- [ ] omitempty의 동작을 이해하고 사용하는가?
- [ ] 스트림 데이터에 Encoder/Decoder를 사용하는가?
- [ ] 커스텀 타입에 Marshaler/Unmarshaler 인터페이스 구현이 필요한가?

### HTTP 클라이언트 사용 시
- [ ] Timeout이 설정된 클라이언트를 사용하는가?
- [ ] http.DefaultClient 사용을 피하는가?
- [ ] 클라이언트를 재사용하는가?
- [ ] res.Body를 항상 닫는가?
- [ ] Context를 사용하여 취소를 지원하는가?

### HTTP 서버 사용 시
- [ ] 서버 타임아웃(Read, Write, Idle)을 설정했는가?
- [ ] http.DefaultServeMux 사용을 피하는가?
- [ ] 미들웨어로 횡단 관심사를 분리하는가?
- [ ] Graceful shutdown을 구현했는가?

### 로깅 시
- [ ] 구조화된 로깅(slog)을 사용하는가?
- [ ] 적절한 로그 레벨을 사용하는가?
- [ ] 성능 중요 경로에서 LogAttrs를 사용하는가?
- [ ] 요청별 컨텍스트 정보를 포함하는가?

---

## 참고 자료

- [io package](https://pkg.go.dev/io)
- [time package](https://pkg.go.dev/time)
- [encoding/json package](https://pkg.go.dev/encoding/json)
- [net/http package](https://pkg.go.dev/net/http)
- [log/slog package](https://pkg.go.dev/log/slog)
- [Writing Web Applications](https://go.dev/doc/articles/wiki/)
- [Go by Example: HTTP Server](https://gobyexample.com/http-servers)
