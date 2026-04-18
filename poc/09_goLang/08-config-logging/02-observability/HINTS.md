# 14. 로깅 및 메트릭 힌트

## Zap 로거 초기화

### 개발 환경 로거

```go
import "go.uber.org/zap"

func NewDevelopmentLogger() (*zap.Logger, error) {
    config := zap.NewDevelopmentConfig()
    config.EncoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder
    return config.Build()
}

// 사용
logger, _ := NewDevelopmentLogger()
defer logger.Sync()
```

### 프로덕션 환경 로거

```go
func NewProductionLogger() (*zap.Logger, error) {
    config := zap.NewProductionConfig()
    config.OutputPaths = []string{"stdout", "app.log"}
    return config.Build()
}
```

### 커스텀 로거 설정

```go
func NewCustomLogger() (*zap.Logger, error) {
    config := zap.Config{
        Level:       zap.NewAtomicLevelAt(zap.InfoLevel),
        Development: false,
        Encoding:    "json",
        EncoderConfig: zapcore.EncoderConfig{
            TimeKey:        "ts",
            LevelKey:       "level",
            NameKey:        "logger",
            CallerKey:      "caller",
            MessageKey:     "msg",
            StacktraceKey:  "stacktrace",
            LineEnding:     zapcore.DefaultLineEnding,
            EncodeLevel:    zapcore.LowercaseLevelEncoder,
            EncodeTime:     zapcore.ISO8601TimeEncoder,
            EncodeDuration: zapcore.SecondsDurationEncoder,
            EncodeCaller:   zapcore.ShortCallerEncoder,
        },
        OutputPaths:      []string{"stdout"},
        ErrorOutputPaths: []string{"stderr"},
    }
    return config.Build()
}
```

## 구조화된 로깅

### 필드 타입

```go
// 문자열
logger.Info("message", zap.String("key", "value"))

// 숫자
logger.Info("message",
    zap.Int("count", 10),
    zap.Int64("timestamp", time.Now().Unix()),
    zap.Float64("percentage", 95.5),
)

// 시간
logger.Info("message",
    zap.Time("created_at", time.Now()),
    zap.Duration("elapsed", duration),
)

// 에러
logger.Error("operation failed", zap.Error(err))

// 객체 (JSON 직렬화)
logger.Info("user info", zap.Any("user", user))

// 배열
logger.Info("items", zap.Strings("names", []string{"a", "b", "c"}))
```

### 컨텍스트 로거

```go
// 기본 필드를 가진 로거 생성
requestLogger := logger.With(
    zap.String("request_id", uuid.New().String()),
    zap.String("user_id", userID),
)

// 이후 모든 로그에 기본 필드 자동 포함
requestLogger.Info("Processing request")
requestLogger.Error("Request failed", zap.Error(err))
```

## Prometheus 메트릭

### Counter

```go
import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "path", "status"},
    )
)

// 사용
httpRequestsTotal.WithLabelValues("GET", "/api/users", "200").Inc()
```

### Gauge

```go
var (
    activeConnections = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "active_connections",
            Help: "Number of active connections",
        },
    )
)

// 사용
activeConnections.Inc()       // 증가
activeConnections.Dec()       // 감소
activeConnections.Set(10)     // 직접 설정
activeConnections.Add(5)      // 값 추가
activeConnections.Sub(3)      // 값 감소
```

### Histogram

```go
var (
    requestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets, // 또는 커스텀: []float64{0.01, 0.05, 0.1, 0.5, 1, 5}
        },
        []string{"method", "path"},
    )
)

// 사용
start := time.Now()
// ... 작업 수행 ...
duration := time.Since(start).Seconds()
requestDuration.WithLabelValues("GET", "/api/users").Observe(duration)
```

### Summary

```go
var (
    responseTimes = promauto.NewSummaryVec(
        prometheus.SummaryOpts{
            Name:       "response_time_seconds",
            Help:       "Response time in seconds",
            Objectives: map[float64]float64{0.5: 0.05, 0.9: 0.01, 0.99: 0.001}, // p50, p90, p99
        },
        []string{"endpoint"},
    )
)

// 사용
responseTimes.WithLabelValues("/api/users").Observe(0.123)
```

## HTTP 미들웨어

### 로깅 미들웨어

```go
func LoggingMiddleware(logger *zap.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            requestID := uuid.New().String()

            // 요청 로깅
            logger.Info("Request started",
                zap.String("request_id", requestID),
                zap.String("method", r.Method),
                zap.String("path", r.URL.Path),
                zap.String("remote_addr", r.RemoteAddr),
            )

            // ResponseWriter 래핑하여 status code 캡처
            wrapped := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

            next.ServeHTTP(wrapped, r)

            // 응답 로깅
            logger.Info("Request completed",
                zap.String("request_id", requestID),
                zap.Int("status", wrapped.statusCode),
                zap.Duration("duration", time.Since(start)),
            )
        })
    }
}

type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}
```

### 메트릭 미들웨어

```go
func MetricsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        // 진행 중인 요청 증가
        activeConnections.Inc()
        defer activeConnections.Dec()

        wrapped := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}
        next.ServeHTTP(wrapped, r)

        // 메트릭 기록
        duration := time.Since(start).Seconds()
        status := fmt.Sprintf("%d", wrapped.statusCode)

        httpRequestsTotal.WithLabelValues(r.Method, r.URL.Path, status).Inc()
        requestDuration.WithLabelValues(r.Method, r.URL.Path).Observe(duration)
    })
}
```

## 메트릭 엔드포인트

```go
import (
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
    // 메트릭 엔드포인트 노출
    http.Handle("/metrics", promhttp.Handler())

    // 나머지 라우트들...
    http.HandleFunc("/api/users", handleUsers)

    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## 성능 프로파일링

### 함수 타이밍

```go
func measureTime(logger *zap.Logger, operation string) func() {
    start := time.Now()
    return func() {
        duration := time.Since(start)
        logger.Info("Operation completed",
            zap.String("operation", operation),
            zap.Duration("duration", duration),
        )
    }
}

// 사용
func ProcessData() {
    defer measureTime(logger, "ProcessData")()

    // 작업 수행...
}
```

### 느린 쿼리 탐지

```go
func logSlowQuery(logger *zap.Logger, query string, duration time.Duration) {
    threshold := 1 * time.Second
    if duration > threshold {
        logger.Warn("Slow query detected",
            zap.String("query", query),
            zap.Duration("duration", duration),
            zap.Duration("threshold", threshold),
        )
    }
}
```

## 에러 처리

### 에러 로깅

```go
func handleError(logger *zap.Logger, err error, msg string) {
    if err != nil {
        logger.Error(msg,
            zap.Error(err),
            zap.Stack("stacktrace"),
        )
    }
}
```

### 에러 메트릭

```go
var (
    errorTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "errors_total",
            Help: "Total number of errors",
        },
        []string{"type", "operation"},
    )
)

func trackError(errType, operation string) {
    errorTotal.WithLabelValues(errType, operation).Inc()
}
```

## 로그 샘플링

```go
import "go.uber.org/zap/zapcore"

func NewSampledLogger() (*zap.Logger, error) {
    config := zap.NewProductionConfig()
    config.Sampling = &zap.SamplingConfig{
        Initial:    100,  // 처음 100개는 모두 로깅
        Thereafter: 100,  // 이후 100개당 1개만 로깅
    }
    return config.Build()
}
```

## 일반적인 패턴

### 전역 로거

```go
var logger *zap.Logger

func init() {
    var err error
    logger, err = zap.NewProduction()
    if err != nil {
        panic(err)
    }
}

func GetLogger() *zap.Logger {
    return logger
}
```

### 컨텍스트에 로거 저장

```go
type contextKey string

const loggerKey contextKey = "logger"

func WithLogger(ctx context.Context, logger *zap.Logger) context.Context {
    return context.WithValue(ctx, loggerKey, logger)
}

func LoggerFromContext(ctx context.Context) *zap.Logger {
    if logger, ok := ctx.Value(loggerKey).(*zap.Logger); ok {
        return logger
    }
    return zap.NewNop() // 기본 no-op 로거
}
```

## 디버깅 팁

### 로거 출력 확인

```go
// 즉시 플러시
defer logger.Sync()

// 강제 플러시
logger.Sync()
```

### 메트릭 확인

```bash
# 메트릭 엔드포인트 조회
curl http://localhost:8080/metrics

# 특정 메트릭 필터링
curl http://localhost:8080/metrics | grep http_requests_total
```
