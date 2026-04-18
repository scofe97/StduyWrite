# Zerolog 로깅 프레임워크 학습

## 학습 목표

Zero-allocation 로깅 라이브러리 zerolog를 사용하여 고성능 구조화된 로깅을 익힙니다.

## Zerolog란?

zerolog는 Go를 위한 고성능 JSON 로거입니다.

**주요 특징**:
- Zero-allocation: 메모리 할당 없이 로깅 (성능 최적화)
- 구조화된 로깅: JSON 형식의 로그 출력
- 체이닝 API: 직관적인 메서드 체이닝
- 레벨 기반 로깅: Debug, Info, Warn, Error, Fatal, Panic

**주요 사용처**:
- 고성능 마이크로서비스
- 구조화된 로그가 필요한 프로덕션 환경
- Elasticsearch, Loki 등 로그 집계 시스템 연동

## 핵심 개념

### 1. 체이닝 API

```go
log.Info().
    Str("user", "john").
    Int("age", 30).
    Msg("User created")
// 출력: {"level":"info","user":"john","age":30,"message":"User created"}
```

### 2. 로그 레벨

| 레벨 | 용도 |
|------|------|
| Trace | 매우 상세한 디버깅 |
| Debug | 개발 중 디버깅 |
| Info | 일반 정보 |
| Warn | 경고 (에러는 아님) |
| Error | 에러 발생 |
| Fatal | 심각한 에러 (os.Exit(1)) |
| Panic | 패닉 발생 (panic()) |

### 3. 출력 형식

**JSON (프로덕션)**:
```go
logger = zerolog.New(os.Stdout).With().Timestamp().Logger()
// {"level":"info","time":"2024-01-01T12:00:00Z","message":"Hello"}
```

**ConsoleWriter (개발)**:
```go
output := zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.RFC3339}
logger = zerolog.New(output).With().Timestamp().Logger()
// 12:00:00 INF Hello
```

## 프로젝트 구조

```
23-zerolog/
├── main.go              # 엔트리 포인트
├── logging/
│   ├── logger.go        # 로거 초기화 및 유틸리티
│   └── middleware.go    # HTTP 로깅 미들웨어
├── go.mod
├── README.md            # 이 파일
├── EXERCISES.md         # 실습 과제
├── HINTS.md             # 힌트
└── LEARNED.md           # 학습 회고
```

## 학습 흐름

### 1단계: 기본 로깅
- 로거 초기화
- 로그 레벨별 출력
- 필드 추가 (Str, Int, Bool, Err)

### 2단계: 구조화된 로깅
- 컨텍스트 로깅
- 서브 로거 생성
- 다중 필드 로깅

### 3단계: HTTP 미들웨어
- 요청/응답 로깅
- 요청 ID 추적
- 에러 복구 및 로깅

## 주요 API

### 로거 생성

```go
// 기본 로거 (JSON)
logger := zerolog.New(os.Stdout)

// 타임스탬프 포함
logger := zerolog.New(os.Stdout).With().Timestamp().Logger()

// 기본 필드 포함
logger := zerolog.New(os.Stdout).With().
    Timestamp().
    Str("service", "my-app").
    Logger()
```

### 로그 출력

```go
// 단순 메시지
logger.Info().Msg("Hello")

// 필드 추가
logger.Info().
    Str("user", "john").
    Int("count", 42).
    Bool("active", true).
    Msg("User action")

// 에러 로깅
logger.Error().Err(err).Msg("Operation failed")

// Duration 로깅
logger.Info().Dur("elapsed", duration).Msg("Task completed")
```

### 서브 로거

```go
// 특정 컴포넌트용 로거
authLogger := logger.With().Str("component", "auth").Logger()
authLogger.Info().Msg("Login attempt")
// {"level":"info","component":"auth","message":"Login attempt"}
```

## 실행 예시

```bash
# 의존성 설치
go get -u github.com/rs/zerolog

# 실행
go run main.go

# 로그 레벨 변경 (환경변수)
LOG_LEVEL=debug go run main.go
```

## 참고 자료

- [Zerolog GitHub](https://github.com/rs/zerolog)
- [Zerolog Godoc](https://pkg.go.dev/github.com/rs/zerolog)
- [Structured Logging Best Practices](https://www.loggly.com/blog/go-logging-tips/)

### 연관 모듈
- **24-koanf**: 설정 관리 → 로그 레벨 설정에 활용
- **25-go-chi**: HTTP 라우터 → 미들웨어 통합에 활용
- **28-capstone**: 통합 프로젝트에서 전체 활용

## 다음 단계

1. `EXERCISES.md`에서 TODO 체크박스 확인
2. 각 파일의 TODO 주석을 채우며 구현
3. `HINTS.md`는 막힐 때만 참고
4. 완료 후 `LEARNED.md`에 회고 작성

## 디버깅 팁

```bash
# 로그 출력 확인
go run main.go 2>&1 | head -10

# JSON 파싱 테스트 (jq 사용)
go run main.go 2>&1 | jq .

# 특정 레벨만 필터링
go run main.go 2>&1 | jq 'select(.level == "error")'
```

## 성공 기준

- [ ] 기본 로거 초기화 완료
- [ ] 모든 로그 레벨 사용 가능
- [ ] 컨텍스트 로깅 구현
- [ ] HTTP 미들웨어 동작
- [ ] ConsoleWriter/JSON 전환 가능

---

**시작하기**: `EXERCISES.md`를 열고 첫 번째 TODO부터 시작하세요!
