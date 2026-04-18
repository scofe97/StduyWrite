# Git-API Service

Runners-High 프로젝트의 Git 연동 서비스 (Go)

## 프로젝트 개요

이 서비스는 GitHub/GitLab API와의 외부 통신을 담당합니다.
Java TPS-API와 Kafka를 통해 비동기로 통신합니다.

```
┌─────────────┐     Kafka      ┌─────────────┐     REST     ┌─────────────┐
│   TPS-API   │ ──────────────►│   Git-API   │ ───────────► │  GitHub/    │
│   (Java)    │ ◄────────────── │    (Go)     │ ◄─────────── │  GitLab     │
└─────────────┘   Commands      └─────────────┘   API Calls  └─────────────┘
                  Events
```

---

## Go 초보자를 위한 가이드

### 1. Go 프로젝트 구조 이해

```
git-api/
├── cmd/                    # 실행 진입점 (main 패키지)
│   └── server/
│       └── main.go         # 앱 시작점
├── internal/               # 외부에서 import 불가능한 내부 코드
│   ├── config/             # 설정 관련
│   ├── handler/            # 요청 핸들러
│   ├── service/            # 비즈니스 로직
│   └── client/             # 외부 API 클라이언트
├── pkg/                    # 외부에서 import 가능한 공개 코드
│   ├── event/              # 이벤트 타입 정의
│   └── kafka/              # Kafka 유틸리티
├── go.mod                  # 의존성 정의 (Java의 pom.xml)
├── go.sum                  # 의존성 체크섬 (자동 생성)
├── Dockerfile              # 컨테이너 빌드
└── Makefile                # 빌드 명령어
```

### 2. Go 핵심 개념

#### 2.1 패키지 (Package)

```go
// 모든 Go 파일은 패키지 선언으로 시작
package main  // 실행 가능한 프로그램

package service  // 라이브러리 패키지
```

**규칙**:
- `package main` + `func main()` = 실행 파일
- 디렉토리명 = 패키지명 (권장)
- `internal/` 하위는 외부 import 불가

#### 2.2 Import

```go
import (
    // 표준 라이브러리
    "context"
    "fmt"

    // 외부 패키지 (go.mod에 정의)
    "go.uber.org/zap"

    // 프로젝트 내부 패키지
    "github.com/runners-high/git-api/internal/config"
)
```

#### 2.3 변수 선언

```go
// 명시적 타입
var name string = "hello"

// 타입 추론 (함수 내부에서만)
name := "hello"

// 여러 변수
var (
    host string
    port int
)
```

#### 2.4 함수

```go
// 기본 함수
func greet(name string) string {
    return "Hello, " + name
}

// 다중 반환 (Go의 특징!)
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

// 호출
result, err := divide(10, 2)
if err != nil {
    // 에러 처리
}
```

#### 2.5 구조체 (Struct) = Java의 Class

```go
// 정의
type User struct {
    ID   string
    Name string
    Age  int
}

// 생성
user := User{
    ID:   "1",
    Name: "John",
    Age:  25,
}

// 메서드 (리시버 함수)
func (u *User) GetFullInfo() string {
    return fmt.Sprintf("%s (%d)", u.Name, u.Age)
}
```

#### 2.6 인터페이스 (Interface)

```go
// 인터페이스 정의
type GitClient interface {
    CreateBranch(ctx context.Context, repo, branch string) error
    DeleteBranch(ctx context.Context, repo, branch string) error
}

// 구현 - 명시적 implements 키워드 없음!
// 메서드만 구현하면 자동으로 인터페이스 충족
type GitHubClient struct {
    token string
}

func (g *GitHubClient) CreateBranch(ctx context.Context, repo, branch string) error {
    // 구현
    return nil
}

func (g *GitHubClient) DeleteBranch(ctx context.Context, repo, branch string) error {
    // 구현
    return nil
}
```

#### 2.7 에러 처리 (Java의 Exception과 다름!)

```go
// Go는 예외 대신 에러 값 반환
result, err := someFunction()
if err != nil {
    // 에러 처리 필수!
    return err  // 또는 로깅 후 처리
}

// 에러 생성
import "errors"
err := errors.New("something went wrong")

import "fmt"
err := fmt.Errorf("user %s not found", userID)
```

#### 2.8 고루틴 (Goroutine) = 경량 스레드

```go
// 함수를 고루틴으로 실행
go someFunction()

// 익명 함수 고루틴
go func() {
    fmt.Println("Running in goroutine")
}()

// 채널로 고루틴 간 통신
ch := make(chan string)

go func() {
    ch <- "message"  // 전송
}()

msg := <-ch  // 수신 (블로킹)
```

#### 2.9 defer = Java의 finally

```go
func readFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close()  // 함수 종료 시 반드시 실행

    // 파일 작업...
    return nil
}
```

### 3. 이 프로젝트의 주요 패턴

#### 3.1 설정 로딩

```go
// internal/config/config.go
type Config struct {
    Kafka KafkaConfig
}

func LoadFromEnv() *Config {
    return &Config{
        Kafka: KafkaConfig{
            Brokers: strings.Split(getEnv("KAFKA_BROKERS", "localhost:9092"), ","),
        },
    }
}
```

#### 3.2 의존성 주입

```go
// main.go에서 수동 의존성 주입
func main() {
    // 1. 설정 로드
    cfg := config.LoadFromEnv()

    // 2. Kafka Producer 생성
    producer, _ := kafka.NewProducer(cfg.Kafka.Brokers, ...)

    // 3. Service에 Producer 주입
    gitService := service.NewGitService(producer, logger)

    // 4. Handler에 Service 주입
    handler := handler.NewKafkaHandler(gitService, logger)
}
```

#### 3.3 컨텍스트 (Context)

```go
// 타임아웃, 취소, 값 전달에 사용
ctx := context.Background()  // 루트 컨텍스트

// 타임아웃 컨텍스트
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()

// API 호출에 전달
client.CreateBranch(ctx, repo, branch)
```

### 4. 빌드 및 실행

#### 4.1 의존성 설치

```bash
# go.sum 생성 및 의존성 다운로드
go mod tidy
go mod download
```

#### 4.2 빌드

```bash
# 바이너리 빌드
go build -o build/git-api ./cmd/server

# 또는 Makefile 사용
make build
```

#### 4.3 실행

```bash
# 직접 실행
go run ./cmd/server/main.go

# 빌드 후 실행
./build/git-api

# Docker로 실행
make docker-build
make docker-run
```

#### 4.4 테스트

```bash
# 전체 테스트
go test ./...

# 상세 출력
go test -v ./...

# 커버리지
go test -cover ./...
```

### 5. 환경 변수

```bash
# Kafka
KAFKA_BROKERS=localhost:9092
KAFKA_CONSUMER_GROUP=git-api
KAFKA_TOPIC_COMMANDS=runners-high.git.commands
KAFKA_TOPIC_EVENTS=runners-high.git.events

# GitHub (선택)
GITHUB_DEFAULT_TOKEN=ghp_xxxx

# GitLab (선택)
GITLAB_DEFAULT_TOKEN=glpat-xxxx
GITLAB_BASE_URL=https://gitlab.com
```

### 6. Java vs Go 비교

| Java | Go | 설명 |
|------|-----|------|
| `class User {}` | `type User struct {}` | 타입 정의 |
| `new User()` | `User{}` 또는 `&User{}` | 인스턴스 생성 |
| `implements Interface` | (자동) | 인터페이스 구현 |
| `try-catch` | `if err != nil` | 에러 처리 |
| `Thread` | `go func()` | 병렬 처리 |
| `finally` | `defer` | 정리 코드 |
| `null` | `nil` | 널 값 |
| `private/public` | 소문자/대문자 | 가시성 |
| `Maven/Gradle` | `go mod` | 의존성 관리 |
| `@Autowired` | 생성자 주입 | 의존성 주입 |

### 7. 자주 쓰는 명령어

```bash
# 모듈 초기화
go mod init github.com/your/project

# 의존성 정리
go mod tidy

# 코드 포맷팅
go fmt ./...
gofmt -s -w .

# 린트
golangci-lint run ./...

# 테스트
go test -v -race -cover ./...

# 빌드
go build -o app ./cmd/server
```

### 8. 추천 학습 자료

1. **A Tour of Go** - https://go.dev/tour/
2. **Effective Go** - https://go.dev/doc/effective_go
3. **Go by Example** - https://gobyexample.com/

---

## 서비스 아키텍처

### Kafka 이벤트 흐름

```
TPS-API (Java)                          Git-API (Go)
     │                                       │
     │  BranchCreateRequested               │
     ├──────────────────────────────────────►│
     │  (runners-high.git.commands)          │
     │                                       ▼
     │                              GitHub/GitLab API 호출
     │                                       │
     │  BranchCreated / OperationFailed      │
     │◄──────────────────────────────────────┤
     │  (runners-high.git.events)            │
     ▼                                       │
  DB 업데이트                                 │
```

### 지원하는 이벤트

**Commands (요청)**:
- `BRANCH_CREATE_REQUESTED` - 브랜치 생성
- `BRANCH_DELETE_REQUESTED` - 브랜치 삭제
- `REPOSITORY_SYNC_REQUESTED` - 저장소 동기화
- `PR_CREATE_REQUESTED` - PR/MR 생성

**Results (응답)**:
- `BRANCH_CREATED` - 브랜치 생성 완료
- `BRANCH_DELETED` - 브랜치 삭제 완료
- `REPOSITORY_SYNCED` - 저장소 동기화 완료
- `PR_CREATED` - PR/MR 생성 완료
- `OPERATION_FAILED` - 작업 실패

---

## 라이선스

MIT License
