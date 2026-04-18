# Zerolog 실습 과제

## 목표

zerolog를 활용하여 구조화된 로깅 시스템을 구현하며 고성능 로깅을 마스터합니다.

---

## Phase 1: 기본 로깅 구현

### Task 1.1: 프로젝트 초기화
- [ ] `go mod tidy` 또는 `go get` 실행하여 zerolog 설치
- [ ] `go get -u github.com/rs/zerolog` 실행
- [ ] go.mod 파일에 의존성 추가 확인

### Task 1.2: 로거 초기화 (logging/logger.go)
- [ ] `InitLogger()` 함수 구현
  - ConsoleWriter를 사용한 개발 환경 로거
  - 타임스탬프 포함
  - 기본 로그 레벨: Info
- [ ] 테스트: `go run main.go` → 초기화 메시지 출력 확인

### Task 1.3: main.go에서 로거 사용
- [ ] `logging.InitLogger()` 호출
- [ ] `logging.GetLogger()` 로 로거 인스턴스 획득
- [ ] Info 레벨 로그 출력: "Application started"
- [ ] 테스트: `go run main.go` → 로그 출력 확인

---

## Phase 2: 로그 레벨 활용

### Task 2.1: 다양한 로그 레벨 사용
- [ ] Debug 로그 출력: 모듈 정보 포함
- [ ] Info 로그 출력: 기본 정보
- [ ] Warn 로그 출력: 경고 상황 (예: 재시도)
- [ ] Error 로그 출력: 에러 객체 포함
- [ ] 테스트: 각 레벨별 출력 확인

### Task 2.2: 로그 레벨 설정 함수
- [ ] `InitLoggerWithLevel(level string)` 구현
  - "debug", "info", "warn", "error" 문자열 지원
  - `zerolog.SetGlobalLevel()` 사용
- [ ] 테스트:
  - `InitLoggerWithLevel("debug")` → Debug 로그 출력됨
  - `InitLoggerWithLevel("warn")` → Debug, Info 로그 출력 안됨

---

## Phase 3: 구조화된 로깅

### Task 3.1: 필드 체이닝
- [ ] main.go에서 다양한 필드 타입 사용
  - `Str("key", "value")`: 문자열
  - `Int("count", 42)`: 정수
  - `Bool("active", true)`: 불리언
  - `Dur("elapsed", duration)`: 시간
  - `Err(err)`: 에러
- [ ] 테스트: JSON 형식으로 필드 출력 확인

### Task 3.2: 컨텍스트 로깅 함수
- [ ] `LogWithContext(userID, action, message string)` 구현
  - user_id, action 필드를 포함한 로그
- [ ] 테스트:
  ```go
  LogWithContext("user-123", "login", "User logged in")
  // 출력: {"user_id":"user-123","action":"login","message":"User logged in"}
  ```

### Task 3.3: 다중 필드 로깅
- [ ] `LogWithFields(level string, fields map[string]interface{}, message string)` 구현
  - map의 키-값을 로그 필드로 추가
- [ ] 테스트:
  ```go
  fields := map[string]interface{}{
      "user": "john",
      "ip": "192.168.1.1",
      "action": "purchase",
  }
  LogWithFields("info", fields, "User action logged")
  ```

---

## Phase 4: 서브 로거

### Task 4.1: 컴포넌트별 서브 로거
- [ ] `CreateSubLogger(component string) zerolog.Logger` 구현
  - "component" 필드가 기본 포함된 로거 반환
- [ ] 테스트:
  ```go
  authLogger := CreateSubLogger("auth")
  authLogger.Info().Msg("Login attempt")
  // 출력: {"component":"auth","message":"Login attempt"}

  dbLogger := CreateSubLogger("database")
  dbLogger.Error().Err(err).Msg("Query failed")
  // 출력: {"component":"database","error":"...","message":"Query failed"}
  ```

### Task 4.2: 중첩 컨텍스트
- [ ] 서브 로거에 추가 필드를 더해 사용
  ```go
  authLogger := CreateSubLogger("auth")
  loginLogger := authLogger.With().Str("flow", "login").Logger()
  loginLogger.Info().Str("user", "john").Msg("Attempting login")
  ```

---

## Phase 5: HTTP 미들웨어 (선택)

### Task 5.1: 요청 로깅 미들웨어
- [ ] `RequestLogger(next http.HandlerFunc) http.HandlerFunc` 구현
  - 요청 시작: method, path 로깅
  - 요청 완료: method, path, status, duration 로깅
- [ ] 테스트:
  ```bash
  go run main.go &
  curl http://localhost:8080/
  # 로그에서 요청 정보 확인
  ```

### Task 5.2: 요청 ID 로깅
- [ ] `ContextLogger(requestID string) zerolog.Logger` 구현
  - request_id 필드가 포함된 로거 반환
- [ ] 미들웨어에서 요청 ID 생성 및 전달
- [ ] 테스트: 각 요청에 고유 ID가 로그에 포함됨

### Task 5.3: 에러 복구 미들웨어
- [ ] `RecoveryMiddleware(next http.HandlerFunc) http.HandlerFunc` 구현
  - panic 발생 시 복구
  - 에러 정보 로깅
  - 500 응답 반환
- [ ] 테스트: panic을 발생시키는 핸들러로 테스트

---

## Bonus Tasks

### Bonus 1: 환경 변수 기반 설정
- [ ] `LOG_LEVEL` 환경변수로 로그 레벨 설정
- [ ] `LOG_FORMAT` 환경변수로 출력 형식 설정 (json/console)
- [ ] 테스트:
  ```bash
  LOG_LEVEL=debug LOG_FORMAT=json go run main.go
  LOG_LEVEL=warn LOG_FORMAT=console go run main.go
  ```

### Bonus 2: 파일 로깅
- [ ] 파일에 로그 쓰기 구현
- [ ] 콘솔과 파일 동시 출력 (io.MultiWriter)
- [ ] 테스트: `app.log` 파일 생성 확인

### Bonus 3: 샘플링
- [ ] 고빈도 로그에 샘플링 적용
  ```go
  sampled := logger.Sample(&zerolog.BasicSampler{N: 10})
  // 10개 중 1개만 로깅
  ```
- [ ] 테스트: 루프에서 100번 로깅 → 약 10개만 출력

---

## 학습 체크리스트

### 기본 개념
- [ ] zerolog.New()로 로거 생성
- [ ] With().Timestamp().Logger() 체이닝
- [ ] Info(), Debug(), Warn(), Error() 레벨 사용
- [ ] Msg() vs Msgf() 차이

### 구조화된 로깅
- [ ] Str(), Int(), Bool(), Err() 필드 추가
- [ ] Dur() 로 시간 로깅
- [ ] Interface() 로 복잡한 타입 로깅

### 고급 기능
- [ ] 서브 로거 생성
- [ ] 전역 로그 레벨 설정
- [ ] ConsoleWriter vs JSON 출력 전환
- [ ] HTTP 미들웨어 구현

---

## 성공 기준

모든 Task를 완료하면:

```bash
$ go run main.go

# ConsoleWriter 출력
12:00:00 INF Application started
12:00:00 DBG Debug message module=main
12:00:00 WRN Connection retry retry=3
12:00:00 ERR Error occurred error="sample error"
12:00:00 INF User logged in action=login user_id=user-123

# JSON 출력 (LOG_FORMAT=json)
{"level":"info","time":"2024-01-01T12:00:00Z","message":"Application started"}
{"level":"debug","time":"2024-01-01T12:00:00Z","module":"main","message":"Debug message"}
```

---

**진행 방법**:
1. Phase 1부터 순서대로 진행
2. 각 Task의 체크박스를 완료하면 체크
3. 막히면 `HINTS.md` 참고 (스포일러 주의!)
4. 모든 Phase 완료 후 Bonus 도전
5. `LEARNED.md`에 학습 내용 정리

**예상 소요 시간**: 1.5-2시간
