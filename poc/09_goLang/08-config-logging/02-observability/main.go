package main

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.uber.org/zap"
)

// Metrics 애플리케이션 메트릭
type Metrics struct {
	RequestsTotal   *prometheus.CounterVec
	RequestDuration *prometheus.HistogramVec
	ActiveRequests  prometheus.Gauge
}

var (
	logger  *zap.Logger
	metrics *Metrics
)

func main() {
	// TODO: 로거 초기화
	var err error
	logger, err = initLogger()
	if err != nil {
		log.Fatalf("Failed to initialize logger: %v", err)
	}
	defer logger.Sync()

	// TODO: 메트릭 초기화
	metrics = initMetrics()

	// TODO: HTTP 라우터 설정
	mux := http.NewServeMux()

	// 애플리케이션 엔드포인트
	mux.HandleFunc("/", handleRoot)
	mux.HandleFunc("/api/users", handleUsers)

	// 메트릭 엔드포인트
	mux.Handle("/metrics", promhttp.Handler())

	// TODO: 미들웨어 체인 구성
	handler := LoggingMiddleware(logger)(MetricsMiddleware(metrics)(mux))

	// 서버 시작
	addr := ":8080"
	logger.Info("Server starting", zap.String("addr", addr))
	if err := http.ListenAndServe(addr, handler); err != nil {
		logger.Fatal("Server failed", zap.Error(err))
	}
}

// initLogger 로거를 초기화합니다
func initLogger() (*zap.Logger, error) {
	// TODO: 환경에 따라 로거 설정
	// 개발: zap.NewDevelopment()
	// 프로덕션: zap.NewProduction()

	// TODO: 커스텀 설정
	// config := zap.NewProductionConfig()
	// config.OutputPaths = []string{"stdout", "app.log"}
	// return config.Build()

	return zap.NewDevelopment()
}

// initMetrics 메트릭을 초기화합니다
func initMetrics() *Metrics {
	// TODO: Counter 메트릭 정의
	requestsTotal := promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_requests_total",
			Help: "Total number of HTTP requests",
		},
		[]string{"method", "path", "status"},
	)

	// TODO: Histogram 메트릭 정의
	requestDuration := promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "http_request_duration_seconds",
			Help:    "HTTP request duration in seconds",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"method", "path"},
	)

	// TODO: Gauge 메트릭 정의
	activeRequests := promauto.NewGauge(
		prometheus.GaugeOpts{
			Name: "http_requests_in_progress",
			Help: "Number of HTTP requests currently being processed",
		},
	)

	return &Metrics{
		RequestsTotal:   requestsTotal,
		RequestDuration: requestDuration,
		ActiveRequests:  activeRequests,
	}
}

// LoggingMiddleware 요청/응답을 로깅하는 미들웨어
func LoggingMiddleware(logger *zap.Logger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()

			// TODO: 요청 정보 로깅
			// logger.Info("Request started",
			//     zap.String("method", r.Method),
			//     zap.String("path", r.URL.Path),
			//     zap.String("remote_addr", r.RemoteAddr),
			// )

			// ResponseWriter 래핑
			wrapped := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

			next.ServeHTTP(wrapped, r)

			// TODO: 응답 정보 로깅
			duration := time.Since(start)
			// logger.Info("Request completed",
			//     zap.String("method", r.Method),
			//     zap.String("path", r.URL.Path),
			//     zap.Int("status", wrapped.statusCode),
			//     zap.Duration("duration", duration),
			// )

			_ = duration
		})
	}
}

// MetricsMiddleware 메트릭을 수집하는 미들웨어
func MetricsMiddleware(m *Metrics) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()

			// TODO: 진행 중인 요청 증가
			// m.ActiveRequests.Inc()
			// defer m.ActiveRequests.Dec()

			wrapped := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}
			next.ServeHTTP(wrapped, r)

			// TODO: 메트릭 기록
			duration := time.Since(start).Seconds()
			status := fmt.Sprintf("%d", wrapped.statusCode)

			// m.RequestsTotal.WithLabelValues(r.Method, r.URL.Path, status).Inc()
			// m.RequestDuration.WithLabelValues(r.Method, r.URL.Path).Observe(duration)

			_ = duration
			_ = status
		})
	}
}

// responseWriter status code를 캡처하는 ResponseWriter
type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

// handleRoot 루트 엔드포인트
func handleRoot(w http.ResponseWriter, r *http.Request) {
	// TODO: 구조화된 로그 작성
	// logger.Info("Root endpoint accessed",
	//     zap.String("user_agent", r.UserAgent()),
	// )

	fmt.Fprintf(w, "Welcome to Observability Demo!\n")
	fmt.Fprintf(w, "Try:\n")
	fmt.Fprintf(w, "  GET /api/users - User API\n")
	fmt.Fprintf(w, "  GET /metrics   - Prometheus metrics\n")
}

// handleUsers 사용자 API 엔드포인트
func handleUsers(w http.ResponseWriter, r *http.Request) {
	// TODO: 작업 시간 측정
	// start := time.Now()

	// 시뮬레이션: 데이터베이스 쿼리
	time.Sleep(100 * time.Millisecond)

	// TODO: 성공 로그
	// logger.Info("Users fetched",
	//     zap.Int("count", 10),
	//     zap.Duration("query_time", time.Since(start)),
	// )

	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, `{"users": ["alice", "bob", "charlie"]}`)
}

// simulateError 에러 시뮬레이션 예제
func simulateError() error {
	err := fmt.Errorf("database connection failed")

	// TODO: 에러 로깅
	// logger.Error("Operation failed",
	//     zap.Error(err),
	//     zap.String("operation", "fetchUsers"),
	//     zap.Stack("stacktrace"),
	// )

	return err
}
