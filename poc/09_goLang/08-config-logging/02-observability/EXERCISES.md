# 14. 로깅 및 메트릭 연습 문제

## Exercise 1: Zap 로거 설정

**목표**: 개발/프로덕션 환경별 로거 구성

**요구사항**:
- 개발: 콘솔 출력, 읽기 쉬운 형식
- 프로덕션: JSON 출력, 구조화된 로그
- 로깅 레벨 동적 설정
- 로그 파일 로테이션

**예시**:
```go
// 개발 환경
2024-01-17T10:30:45.123+0900    INFO    main.go:42    Server started    {"port": 8080}

// 프로덕션 환경
{"level":"info","ts":1705456245.123,"caller":"main.go:42","msg":"Server started","port":8080}
```

## Exercise 2: 구조화된 로깅

**목표**: 컨텍스트가 풍부한 로그 작성

**요구사항**:
- 요청 ID 추적
- 사용자 정보 포함
- 에러 스택 트레이스
- 성능 타이밍

**필드 예시**:
```go
logger.Info("Request processed",
    zap.String("request_id", reqID),
    zap.String("user_id", userID),
    zap.String("method", "GET"),
    zap.String("path", "/api/users"),
    zap.Int("status", 200),
    zap.Duration("duration", duration),
)
```

## Exercise 3: Prometheus 메트릭 기본

**목표**: HTTP 서버에 기본 메트릭 추가

**요구사항**:
- 요청 총 개수 (Counter)
- 진행 중인 요청 수 (Gauge)
- 요청 지연 시간 (Histogram)
- `/metrics` 엔드포인트 노출

**메트릭**:
```
http_requests_total{method="GET",path="/api/users",status="200"} 1234
http_requests_in_progress 5
http_request_duration_seconds_bucket{le="0.1"} 1000
```

## Exercise 4: 커스텀 메트릭

**목표**: 비즈니스 메트릭 정의 및 수집

**요구사항**:
- 사용자 등록 수 (Counter)
- 활성 세션 수 (Gauge)
- 데이터베이스 쿼리 시간 (Histogram)
- 캐시 히트율 계산

## Exercise 5: 미들웨어 통합

**목표**: HTTP 미들웨어로 자동 로깅/메트릭 수집

**요구사항**:
- 모든 요청에 로그 자동 기록
- 요청별 고유 ID 생성
- 메트릭 자동 업데이트
- 에러 자동 로깅

**미들웨어 구조**:
```go
func LoggingMiddleware(logger *zap.Logger) func(http.Handler) http.Handler
func MetricsMiddleware(metrics *Metrics) func(http.Handler) http.Handler
```

## Exercise 6: 에러 추적

**목표**: 에러 발생 시 상세 컨텍스트 로깅

**요구사항**:
- 에러 발생 위치 추적
- 스택 트레이스 포함
- 관련 변수값 로깅
- 에러 메트릭 수집

**예시**:
```go
logger.Error("Database query failed",
    zap.Error(err),
    zap.String("query", sql),
    zap.Any("params", params),
    zap.Stack("stacktrace"),
)
```

## Exercise 7: 성능 프로파일링

**목표**: 함수 실행 시간 측정 및 기록

**요구사항**:
- defer를 사용한 타이밍 측정
- 느린 쿼리 탐지 (threshold)
- 히트맵용 히스토그램 메트릭
- 백분위 계산 (p50, p95, p99)

## Exercise 8: 로그 샘플링

**목표**: 고빈도 로그의 성능 영향 최소화

**요구사항**:
- 동일 메시지 샘플링 (예: 100개당 1개만 로깅)
- 에러는 항상 로깅
- 샘플링 설정 가능
- 샘플링 통계 메트릭

## 보너스 Exercise: 분산 추적

**목표**: OpenTelemetry 통합

**요구사항**:
- Trace ID 생성 및 전파
- Span 생성
- 로그와 Trace 연결
- Jaeger 또는 Zipkin 연동

## 성공 기준

- [ ] 로그가 구조화되어 JSON으로 출력됨
- [ ] 메트릭이 `/metrics`에서 조회 가능
- [ ] 모든 HTTP 요청이 자동 추적됨
- [ ] 에러 발생 시 충분한 컨텍스트 로깅
- [ ] 성능 오버헤드가 최소화됨

## 추가 과제

1. 로그 집계 시스템 연동 (ELK, Loki)
2. Grafana 대시보드 구성
3. 알림 규칙 설정 (Alertmanager)
4. 로그 분석 자동화 (이상 탐지)
