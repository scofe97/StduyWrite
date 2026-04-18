# Zerolog 힌트

막힐 때만 참고하세요! 스스로 해결하는 것이 학습에 더 효과적입니다.

---

## Phase 1: 기본 로깅

<details>
<summary>Task 1.2: InitLogger 구현이 어려워요</summary>

```go
func InitLogger() {
    // 개발 환경: ConsoleWriter (색상, 가독성)
    output := zerolog.ConsoleWriter{
        Out:        os.Stdout,
        TimeFormat: time.RFC3339,
    }
    logger = zerolog.New(output).With().Timestamp().Logger()

    // 기본 로그 레벨 설정
    zerolog.SetGlobalLevel(zerolog.InfoLevel)
}
```
</details>

<details>
<summary>Task 1.3: main.go에서 로거 사용하기</summary>

```go
func main() {
    logging.InitLogger()

    logger := logging.GetLogger()
    logger.Info().Msg("Application started")
}
```
</details>

---

## Phase 2: 로그 레벨

<details>
<summary>Task 2.1: 다양한 로그 레벨 사용</summary>

```go
logger := logging.GetLogger()

// Debug - 개발 중 디버깅 정보
logger.Debug().Str("module", "main").Msg("Debug message")

// Info - 일반 정보
logger.Info().Msg("Application started")

// Warn - 경고 (에러는 아니지만 주의 필요)
logger.Warn().Int("retry", 3).Msg("Connection retry")

// Error - 에러 발생
logger.Error().Err(errors.New("sample error")).Msg("Error occurred")
```
</details>

<details>
<summary>Task 2.2: 로그 레벨 설정 함수</summary>

```go
func InitLoggerWithLevel(level string) {
    lvl := getLogLevel(level)
    zerolog.SetGlobalLevel(lvl)

    output := zerolog.ConsoleWriter{
        Out:        os.Stdout,
        TimeFormat: time.RFC3339,
    }
    logger = zerolog.New(output).With().Timestamp().Logger()
}
```
</details>

---

## Phase 3: 구조화된 로깅

<details>
<summary>Task 3.1: 필드 체이닝</summary>

```go
// 다양한 필드 타입 사용
logger.Info().
    Str("user", "john").           // 문자열
    Int("age", 30).                // 정수
    Bool("active", true).          // 불리언
    Float64("score", 95.5).        // 실수
    Msg("User profile")

// 시간 로깅
start := time.Now()
// ... 작업 ...
logger.Info().
    Dur("elapsed", time.Since(start)).
    Msg("Task completed")

// 에러 로깅
err := errors.New("connection failed")
logger.Error().
    Err(err).                      // 자동으로 "error" 키로 추가
    Str("host", "localhost:5432").
    Msg("Database connection failed")
```
</details>

<details>
<summary>Task 3.2: LogWithContext 구현</summary>

```go
func LogWithContext(userID, action, message string) {
    logger.Info().
        Str("user_id", userID).
        Str("action", action).
        Msg(message)
}

// 사용 예:
// LogWithContext("user-123", "login", "User logged in")
// 출력: {"user_id":"user-123","action":"login","message":"User logged in"}
```
</details>

<details>
<summary>Task 3.3: LogWithFields 구현</summary>

```go
func LogWithFields(level string, fields map[string]interface{}, message string) {
    var event *zerolog.Event

    switch level {
    case "debug":
        event = logger.Debug()
    case "info":
        event = logger.Info()
    case "warn":
        event = logger.Warn()
    case "error":
        event = logger.Error()
    default:
        event = logger.Info()
    }

    // map의 각 필드를 추가
    for key, value := range fields {
        event = event.Interface(key, value)
    }

    event.Msg(message)
}

// 또는 Dict 사용:
func LogWithFieldsUsingDict(level string, fields map[string]interface{}, message string) {
    dict := zerolog.Dict()
    for key, value := range fields {
        switch v := value.(type) {
        case string:
            dict = dict.Str(key, v)
        case int:
            dict = dict.Int(key, v)
        case bool:
            dict = dict.Bool(key, v)
        default:
            dict = dict.Interface(key, v)
        }
    }
    logger.Info().Dict("data", dict).Msg(message)
}
```
</details>

---

## Phase 4: 서브 로거

<details>
<summary>Task 4.1: CreateSubLogger 구현</summary>

```go
func CreateSubLogger(component string) zerolog.Logger {
    return logger.With().Str("component", component).Logger()
}

// 사용 예:
// authLogger := CreateSubLogger("auth")
// authLogger.Info().Msg("Login attempt")
// 출력: {"component":"auth","message":"Login attempt"}
```
</details>

<details>
<summary>Task 4.2: 중첩 컨텍스트</summary>

```go
// 컴포넌트 로거 생성
authLogger := CreateSubLogger("auth")

// 추가 컨텍스트 레이어
loginLogger := authLogger.With().
    Str("flow", "login").
    Logger()

// 사용
loginLogger.Info().
    Str("user", "john").
    Msg("Attempting login")
// 출력: {"component":"auth","flow":"login","user":"john","message":"Attempting login"}

// 실패 시
loginLogger.Warn().
    Str("user", "john").
    Str("reason", "invalid_password").
    Msg("Login failed")
```
</details>

---

## Phase 5: HTTP 미들웨어

<details>
<summary>Task 5.1: RequestLogger 구현</summary>

```go
func RequestLogger(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        // 요청 시작 로그
        logger.Info().
            Str("method", r.Method).
            Str("path", r.URL.Path).
            Str("remote_addr", r.RemoteAddr).
            Msg("Request started")

        // 응답 래퍼
        wrapped := &responseWriter{ResponseWriter: w, status: http.StatusOK}

        // 핸들러 실행
        next.ServeHTTP(wrapped, r)

        // 요청 완료 로그
        logger.Info().
            Str("method", r.Method).
            Str("path", r.URL.Path).
            Int("status", wrapped.status).
            Dur("duration", time.Since(start)).
            Msg("Request completed")
    }
}
```
</details>

<details>
<summary>Task 5.2: ContextLogger 구현</summary>

```go
func ContextLogger(requestID string) zerolog.Logger {
    return logger.With().
        Str("request_id", requestID).
        Logger()
}

// 미들웨어에서 사용:
func RequestLoggerWithID(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // 요청 ID 생성
        requestID := fmt.Sprintf("%d", time.Now().UnixNano())

        // 컨텍스트 로거 생성
        reqLogger := ContextLogger(requestID)

        reqLogger.Info().
            Str("method", r.Method).
            Str("path", r.URL.Path).
            Msg("Request started")

        // ... 핸들러 실행 ...
    }
}
```
</details>

<details>
<summary>Task 5.3: RecoveryMiddleware 구현</summary>

```go
func RecoveryMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                // 스택 트레이스 캡처
                logger.Error().
                    Interface("panic", err).
                    Str("method", r.Method).
                    Str("path", r.URL.Path).
                    Msg("Panic recovered")

                http.Error(w, "Internal Server Error", http.StatusInternalServerError)
            }
        }()

        next.ServeHTTP(w, r)
    }
}

// 테스트용 핸들러
func panicHandler(w http.ResponseWriter, r *http.Request) {
    panic("something went wrong!")
}
```
</details>

---

## Bonus Tasks

<details>
<summary>Bonus 1: 환경 변수 기반 설정</summary>

```go
func InitLoggerFromEnv() {
    // 로그 레벨
    level := os.Getenv("LOG_LEVEL")
    if level == "" {
        level = "info"
    }
    zerolog.SetGlobalLevel(getLogLevel(level))

    // 출력 형식
    format := os.Getenv("LOG_FORMAT")

    var output io.Writer
    if format == "json" {
        output = os.Stdout
    } else {
        output = zerolog.ConsoleWriter{
            Out:        os.Stdout,
            TimeFormat: time.RFC3339,
        }
    }

    logger = zerolog.New(output).With().Timestamp().Logger()
}
```
</details>

<details>
<summary>Bonus 2: 파일 로깅</summary>

```go
import "io"

func InitLoggerWithFile(filename string) error {
    // 파일 열기
    file, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
    if err != nil {
        return err
    }

    // 콘솔과 파일에 동시 출력
    consoleWriter := zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.RFC3339}
    multi := io.MultiWriter(consoleWriter, file)

    logger = zerolog.New(multi).With().Timestamp().Logger()
    return nil
}
```
</details>

<details>
<summary>Bonus 3: 샘플링</summary>

```go
// 기본 샘플러 - N개 중 1개만 로깅
sampled := logger.Sample(&zerolog.BasicSampler{N: 10})

for i := 0; i < 100; i++ {
    sampled.Info().Int("iteration", i).Msg("Loop iteration")
}
// 약 10개의 로그만 출력

// 레벨별 샘플러
levelSampler := &zerolog.LevelSampler{
    DebugSampler: &zerolog.BasicSampler{N: 100},  // Debug: 100개 중 1개
    InfoSampler:  &zerolog.BasicSampler{N: 10},   // Info: 10개 중 1개
    WarnSampler:  nil,                              // Warn: 전부 출력
}

sampledLogger := logger.Sample(levelSampler)
```
</details>

---

## 일반적인 문제 해결

<details>
<summary>로그가 출력되지 않아요</summary>

**체크리스트**:
1. `InitLogger()` 호출했나요?
2. 전역 로그 레벨이 너무 높지 않나요? (Error로 설정하면 Info 출력 안됨)
3. `Msg()` 호출을 빠뜨리지 않았나요?

```go
// 잘못된 예 - Msg() 없음
logger.Info().Str("key", "value")  // 출력 안됨!

// 올바른 예
logger.Info().Str("key", "value").Msg("message")
```
</details>

<details>
<summary>ConsoleWriter 색상이 안 나와요</summary>

**Windows에서**:
```go
// Windows에서는 색상 지원을 위해 추가 설정 필요
output := zerolog.ConsoleWriter{
    Out:        os.Stdout,
    NoColor:    false,  // 색상 활성화
    TimeFormat: time.RFC3339,
}
```

**터미널 확인**: 색상을 지원하는 터미널(Windows Terminal, Git Bash 등) 사용
</details>

<details>
<summary>JSON 출력 시 이스케이프 문제</summary>

특수 문자가 이스케이프됨:
```go
logger.Info().Str("path", "C:\\Users").Msg("test")
// 출력: {"path":"C:\\Users"} - 정상

// Raw JSON 필요 시
logger.Info().RawJSON("data", []byte(`{"nested":"value"}`)).Msg("test")
```
</details>

<details>
<summary>Timestamp 형식 변경</summary>

```go
// 전역 설정
zerolog.TimeFieldFormat = time.RFC3339Nano  // 나노초 포함
zerolog.TimeFieldFormat = "2006-01-02"      // 날짜만
zerolog.TimeFieldFormat = zerolog.TimeFormatUnix  // Unix timestamp

// ConsoleWriter에서만 변경
output := zerolog.ConsoleWriter{
    Out:        os.Stdout,
    TimeFormat: "15:04:05",  // 시간만
}
```
</details>

---

## 추가 리소스

**유용한 패턴**:

```go
// 조건부 로깅
if verbose {
    logger = logger.Level(zerolog.DebugLevel)
}

// 필드 미리 설정
baseLogger := logger.With().
    Str("service", "my-app").
    Str("version", "1.0.0").
    Logger()

// 배열 로깅
logger.Info().
    Strs("tags", []string{"go", "logging"}).
    Ints("ids", []int{1, 2, 3}).
    Msg("Arrays")

// 중첩 객체
logger.Info().
    Dict("user", zerolog.Dict().
        Str("name", "john").
        Int("age", 30)).
    Msg("Nested object")
```

**참고 프로젝트**:
- [zerolog examples](https://github.com/rs/zerolog/tree/master/_examples)
- [Go Microservices logging](https://github.com/ThreeDotsLabs/wild-workouts-go-ddd-example)

---

**힌트를 너무 많이 봤다면**: 파일을 삭제하고 처음부터 다시 도전해보세요!
