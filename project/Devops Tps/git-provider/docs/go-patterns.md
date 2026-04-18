# Git Provider Go 패턴 리뷰

이 문서는 git-provider 프로젝트에서 사용된 Go 문법과 디자인 패턴을 실제 코드 예시와 함께 정리한다.

---

## 1. 인터페이스 기반 다형성 (Strategy Pattern)

Go에는 `implements` 키워드가 없다. 구조체가 인터페이스에 정의된 메서드를 모두 구현하면 자동으로 해당 인터페이스를 만족한다(덕 타이핑). git-provider는 이 특성을 활용해 프로바이더별 설정과 인증을 다형적으로 처리한다.

### ProviderConfig 인터페이스

`internal/provider/config.go`에서 모든 프로바이더 설정이 따라야 하는 계약을 정의한다.

```go
// config.go
type ProviderConfig interface {
    GetType() ProviderType
    GetCredentials() Credentials
    GetBaseURL() string
    Validate() error
}
```

각 프로바이더는 이 인터페이스를 독립적으로 구현한다. GitHub는 Token만 필요하고, Bitbucket은 Username + AppPassword + Workspace가 필요하다는 차이가 구현체 내부에 캡슐화된다.

### Credentials 인터페이스

`internal/provider/credentials.go`에서 인증 방식을 추상화한다. 핵심 메서드는 `ApplyAuth(req *http.Request)` 하나뿐이며, 이것만 구현하면 어떤 인증 방식이든 HTTP 요청에 적용할 수 있다.

```go
// credentials.go
type Credentials interface {
    ApplyAuth(req *http.Request)
    GetAuthType() string
}

// TokenCredentials — Bearer Token (GitHub, GitLab)
type TokenCredentials struct {
    Token string
}

func (c *TokenCredentials) ApplyAuth(req *http.Request) {
    req.Header.Set("Authorization", "Bearer "+c.Token)
}

// BasicCredentials — Basic Auth (Bitbucket)
type BasicCredentials struct {
    Username string
    Password string
}

func (c *BasicCredentials) ApplyAuth(req *http.Request) {
    auth := c.Username + ":" + c.Password
    encoded := base64.StdEncoding.EncodeToString([]byte(auth))
    req.Header.Set("Authorization", "Basic "+encoded)
}
```

### 컴파일 타임 인터페이스 검증

Go에서 인터페이스 구현은 암시적이므로, 메서드 하나를 빠뜨려도 런타임에야 발견될 수 있다. 이를 방지하기 위해 "nil 할당 트릭"으로 컴파일 시점에 인터페이스 충족 여부를 검증한다.

```go
// 컴파일 타임에 인터페이스 구현 확인
var _ Credentials = (*TokenCredentials)(nil)    // credentials.go:44
var _ Credentials = (*BasicCredentials)(nil)    // credentials.go:70
var _ ProviderConfig = (*GitHubConfig)(nil)     // github.go:42
var _ ProviderConfig = (*BitbucketConfig)(nil)  // bitbucket.go:60
```

이 줄은 런타임에 아무 일도 하지 않는다. 하지만 `TokenCredentials`가 `Credentials`의 메서드를 하나라도 누락하면 컴파일 에러가 발생한다. 비용 없이 타입 안전성을 얻는 Go의 관용적 패턴이다.

---

## 2. Adapter Pattern

`internal/client/` 패키지가 이 패턴의 핵심이다. 각 프로바이더의 벤더 SDK가 반환하는 타입을 protobuf 공통 타입(`*pb.Repository`, `*pb.Branch` 등)으로 변환한다.

### GitHub — 타입 안전 SDK

go-github SDK는 `*github.Repository`처럼 타입이 정해져 있어 필드 접근이 안전하다.

```go
// client/github.go
func (c *GitHubClient) ListRepositories(ctx context.Context) ([]*pb.Repository, error) {
    repos, _, err := c.client.Repositories.List(ctx, "", &github.RepositoryListOptions{
        ListOptions: github.ListOptions{PerPage: 100},
    })
    if err != nil {
        return nil, fmt.Errorf("failed to list repositories: %w", err)
    }

    result := make([]*pb.Repository, len(repos))
    for i, repo := range repos {
        result[i] = c.convertRepository(repo)  // *github.Repository → *pb.Repository
    }
    return result, nil
}
```

### Bitbucket — `map[string]interface{}` 수동 변환

go-bitbucket SDK는 타입이 약한 편이다. 일부 응답이 `map[string]interface{}`로 돌아오기 때문에, 필드를 꺼낼 때 타입 단언(type assertion)이 필요하고 누락 시 기본값 처리를 해야 한다.

```go
// client/bitbucket.go
func (c *BitbucketClient) ListRepositories(ctx context.Context) ([]*pb.Repository, error) {
    repos, err := c.client.Repositories.ListForAccount(&bitbucket.RepositoriesOptions{
        Owner: c.workspace,
    })
    if err != nil {
        return nil, fmt.Errorf("failed to list repositories: %w", err)
    }

    result := make([]*pb.Repository, 0)
    for _, repo := range repos.Items {
        result = append(result, c.convertRepository(&repo))  // map 기반 → *pb.Repository
    }
    return result, nil
}
```

### converter 헬퍼 패턴

각 클라이언트는 `convertRepository()`, `convertBranch()` 같은 private 메서드를 가진다. SDK 타입 → protobuf 타입 변환 로직이 여기에 집중되므로, 비즈니스 로직과 변환 로직이 분리된다.

---

## 3. Factory Pattern

`internal/server/client_factory.go`에서 세 프로바이더의 클라이언트 생성을 중앙화한다. 각 팩토리 함수는 early validation → 생성 → 반환의 순서를 따른다.

```go
// client_factory.go
func createGitHubClient(ctx context.Context, config *pb.GitHubConfig) (*client.GitHubClient, error) {
    if config.Token == "" {
        return nil, fmt.Errorf("github token is required")  // early validation
    }
    return client.NewGitHubClient(ctx, config.Token, config.BaseUrl)  // 생성 + 반환
}

func createBitbucketClient(config *pb.BitbucketConfig) (*client.BitbucketClient, error) {
    if config.Email == "" {
        return nil, fmt.Errorf("bitbucket email is required")
    }
    if config.ApiToken == "" {
        return nil, fmt.Errorf("bitbucket api_token is required")
    }
    if config.Workspace == "" {
        return nil, fmt.Errorf("bitbucket workspace is required")
    }
    return client.NewBitbucketClient(config.Email, config.ApiToken, config.Workspace)
}
```

Bitbucket은 검증할 필드가 3개(email, apiToken, workspace)인 반면 GitHub는 1개(token)뿐이다. 팩토리 함수가 이런 프로바이더별 검증 차이를 흡수하므로, 호출하는 서비스 코드는 `createXxxClient()`만 호출하면 된다.

---

## 4. Proto oneof + Type Switch

protobuf의 `oneof`는 Go에서 Discriminated Union으로 매핑된다. 이 프로젝트에서 가장 빈번하게 사용되는 패턴으로, 모든 gRPC 서비스 메서드에서 프로바이더를 분기할 때 쓰인다.

### Protobuf 정의

```protobuf
// provider.proto
message ProviderConfig {
    oneof config {
        GitHubConfig github = 1;
        GitLabConfig gitlab = 2;
        BitbucketConfig bitbucket = 3;
    }
}
```

### Go에서의 사용

protoc가 `oneof`를 인터페이스 + wrapper 구조체로 생성한다. `Config` 필드의 실제 타입은 `*pb.ProviderConfig_Github`, `*pb.ProviderConfig_Gitlab`, `*pb.ProviderConfig_Bitbucket` 중 하나다.

```go
// git_server.go — ListRepositories
switch config := req.Provider.Config.(type) {
case *pb.ProviderConfig_Github:
    ghClient, clientErr := createGitHubClient(ctx, config.Github)
    if clientErr != nil {
        return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
    }
    repos, err = ghClient.ListRepositories(ctx)

case *pb.ProviderConfig_Gitlab:
    glClient, clientErr := createGitLabClient(config.Gitlab)
    if clientErr != nil {
        return nil, status.Errorf(codes.Internal, "failed to create gitlab client: %v", clientErr)
    }
    repos, err = glClient.ListRepositories(ctx)

case *pb.ProviderConfig_Bitbucket:
    bbClient, clientErr := createBitbucketClient(config.Bitbucket)
    if clientErr != nil {
        return nil, status.Errorf(codes.Internal, "failed to create bitbucket client: %v", clientErr)
    }
    repos, err = bbClient.ListRepositories(ctx)

default:
    return nil, status.Error(codes.InvalidArgument, "unknown provider type")
}
```

`default` 케이스가 중요한 이유가 있다. proto 파일에 새 프로바이더(예: Azure DevOps)를 추가했지만 Go 코드를 업데이트하지 않았을 때, `default`가 없으면 nil 응답이 조용히 반환된다. `default`가 명시적 에러를 반환하므로 누락된 구현을 즉시 발견할 수 있다.

### 이 패턴이 반복되는 곳

`git_server.go`의 모든 메서드(8개), `branch_server.go`(5개), `contents_server.go`(3개), `mr_server.go`(11개) 등 총 27개 이상의 RPC 메서드에서 동일한 switch 구조가 반복된다. 프로바이더가 요청(per-request)마다 달라질 수 있기 때문에 이 분기를 피할 수 없다.

---

## 5. 동시성 패턴

### Goroutine 병렬 실행

`main.go`에서 gRPC 서버, REST Gateway, Kafka Consumer를 각각 goroutine으로 띄운다. 세 서버가 서로 독립적이므로 병렬 실행이 자연스럽다.

```go
// main.go
go consumer.Run(ctx)           // Kafka 소비 루프
go startGRPCServer(store, producer, wfStore)  // gRPC :50051
go startRESTGateway()          // REST :8080
```

### Graceful Shutdown

`signal.Notify`로 OS 시그널(SIGINT, SIGTERM)을 채널로 받고, `<-quit`로 블로킹하다가 시그널이 오면 `cancel()`로 context를 취소하여 모든 goroutine에 종료를 전파한다.

```go
// main.go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

// ... 서버 시작 ...

quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
<-quit  // 여기서 블로킹 — 시그널 올 때까지

cancel()            // context 취소 → 모든 goroutine에 전파
producer.Close()    // Kafka producer 정리
consumer.Close()    // Kafka consumer 정리
```

### Jenkins 폴링: Ticker + Timeout + Select

Jenkins는 Webhook을 제공하지 않는 환경이 많아서, HTTP 폴링으로 빌드 상태를 추적한다. `time.NewTicker`로 주기적 폴링, `time.After`로 타임아웃, `select`로 두 채널을 동시에 감시하는 패턴이다.

```go
// cicd_server.go — pollBuildNumber
ticker := time.NewTicker(2 * time.Second)   // 2초마다 큐 확인
defer ticker.Stop()
timeout := time.After(60 * time.Second)     // 최대 60초

for {
    select {
    case <-timeout:
        log.Printf("timeout waiting for build number from queue %d", queueID)
        return
    case <-ticker.C:
        item, err := client.GetQueueItem(ctx, queueID)
        if err != nil {
            continue  // 일시적 에러 → 다음 틱에 재시도
        }
        if item.Executable != nil && item.Executable.Number > 0 {
            jenkinsBuildNumber = item.Executable.Number
            goto pollStatus  // 빌드 번호 확보 → 상태 폴링으로 전환
        }
    }
}
```

이 패턴이 두 단계로 적용된다.
1. **큐 폴링** — 2초 간격, 60초 타임아웃 (빌드 번호 획득)
2. **빌드 폴링** — 5초 간격, 30분 타임아웃 (빌드 완료 대기)

### Mutex로 워크플로우 상태 보호

`workflow/engine.go`의 `Engine`은 여러 Kafka 핸들러에서 동시에 호출될 수 있으므로, `sync.Mutex`로 실행 상태(Execution)를 보호한다.

```go
// engine.go
type Engine struct {
    mu       sync.Mutex
    store    *Store
    producer *kafka.EventProducer
}

func (e *Engine) executeNextStep(ctx context.Context, exec *pb.Execution) {
    e.mu.Lock()
    defer e.mu.Unlock()
    e.executeNextStepLocked(ctx, exec)
}
```

`Locked` 접미사 컨벤션에 주목하자. `executeNextStepLocked`, `completeExecutionLocked`, `failExecutionLocked`처럼 "이미 락을 잡은 상태에서 호출해야 한다"는 계약을 함수명으로 명시한다. Go 표준 라이브러리(예: `sync.Pool`)에서도 사용하는 관용적 네이밍이다.

---

## 6. 에러 처리 전략

### gRPC Status Codes 선택 기준

| 상황 | Status Code | 예시 |
|------|-------------|------|
| 필수 파라미터 누락 | `codes.InvalidArgument` | `"provider config is required"` |
| 리소스 미존재 | `codes.NotFound` | `"pipeline not found"` |
| 서버 내부 오류 | `codes.Internal` | `"failed to create github client"` |

```go
// cicd_server.go
if req.PipelineId == "" {
    return nil, status.Error(codes.InvalidArgument, "pipeline_id is required")
}

p, err := s.store.GetPipeline(req.PipelineId)
if err != nil {
    return nil, status.Errorf(codes.NotFound, "pipeline not found: %v", err)
}
```

grpc-gateway가 이 코드를 HTTP 상태 코드로 자동 매핑한다: `InvalidArgument` → 400, `NotFound` → 404, `Internal` → 500.

### 에러 래핑 (`%w`)

`fmt.Errorf`의 `%w` 동사로 원본 에러를 래핑하면, 호출자가 `errors.Is()`나 `errors.As()`로 원본 에러를 꺼낼 수 있다.

```go
// producer.go
func (p *EventProducer) Publish(ctx context.Context, topic, key string, event any) error {
    data, err := json.Marshal(event)
    if err != nil {
        return fmt.Errorf("marshal event: %w", err)  // 컨텍스트 + 원본 에러
    }
    // ...
    if err := results.FirstErr(); err != nil {
        return fmt.Errorf("produce to %s: %w", topic, err)  // 토픽 정보 포함
    }
    return nil
}
```

에러 메시지에 항상 "무엇을 하다가"(컨텍스트)를 붙이므로, 로그만 봐도 에러 발생 지점과 원인을 추적할 수 있다.

### 3단계 검증 패턴

대부분의 RPC 메서드가 파라미터 → 클라이언트 생성 → 비즈니스 로직 순서로 검증한다.

```go
// git_server.go — GetRepository
// 1단계: 파라미터 검증
if req.Provider == nil {
    return nil, status.Error(codes.InvalidArgument, "provider config is required")
}
if req.Repository == "" {
    return nil, status.Error(codes.InvalidArgument, "repository name is required")
}

// 2단계: 클라이언트 생성 (팩토리 + 인증 검증)
ghClient, clientErr := createGitHubClient(ctx, config.Github)
if clientErr != nil {
    return nil, status.Errorf(codes.Internal, "failed to create github client: %v", clientErr)
}

// 3단계: 비즈니스 로직
repo, err = ghClient.GetRepository(ctx, req.Namespace, req.Repository)
if err != nil {
    return nil, status.Errorf(codes.Internal, "failed to get repository: %v", err)
}
```

각 단계에서 실패하면 즉시 반환하는 "early return" 스타일이다. Go에서 try-catch 없이 에러를 처리하는 기본 방법이며, 중첩을 피하고 정상 경로를 함수의 마지막에 배치한다.

---

## 7. Middleware / Interceptor

### HTTP CORS: Higher-order Function

`CORSWrapper`는 `http.Handler`를 받아서 CORS 헤더를 추가한 새 `http.Handler`를 반환하는 고차 함수다.

```go
// middleware/cors.go
func CORSWrapper(handler http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        w.Header().Set("Access-Control-Max-Age", "86400")

        if r.Method == http.MethodOptions {
            w.WriteHeader(http.StatusNoContent)
            return  // preflight는 여기서 끝
        }

        handler.ServeHTTP(w, r)  // 실제 핸들러 실행
    })
}
```

사용하는 쪽에서는 `http.ListenAndServe(httpPort, middleware.CORSWrapper(mux))`처럼 감싸기만 하면 된다. 데코레이터 패턴의 Go 스타일 구현이다.

### gRPC Logging Interceptor: 클로저가 요청 메타데이터를 캡처

gRPC 인터셉터는 함수를 반환하는 함수다. 반환된 클로저가 매 요청마다 실행되면서 메서드명, 소요 시간, 상태 코드를 로깅한다.

```go
// middleware/interceptor.go
func LoggingInterceptor() grpc.UnaryServerInterceptor {
    return func(
        ctx context.Context,
        req any,
        info *grpc.UnaryServerInfo,    // FullMethod 등 메타데이터
        handler grpc.UnaryHandler,
    ) (any, error) {
        start := time.Now()
        resp, err := handler(ctx, req)  // 실제 핸들러 실행
        duration := time.Since(start)

        if err != nil {
            st, _ := status.FromError(err)
            log.Printf("[gRPC] %s | %s | %v | %s", info.FullMethod, st.Code(), duration, st.Message())
        } else {
            log.Printf("[gRPC] %s | OK | %v", info.FullMethod, duration)
        }
        return resp, err
    }
}
```

### gRPC Recovery Interceptor: `defer` + `recover()`

Go에서 패닉이 발생하면 goroutine이 죽고 프로세스가 종료될 수 있다. Recovery 인터셉터가 `defer` + `recover()`로 패닉을 잡아서 gRPC `Internal` 에러로 변환한다.

```go
// middleware/interceptor.go
func RecoveryInterceptor() grpc.UnaryServerInterceptor {
    return func(
        ctx context.Context,
        req any,
        info *grpc.UnaryServerInfo,
        handler grpc.UnaryHandler,
    ) (resp any, err error) {
        defer func() {
            if r := recover(); r != nil {
                log.Printf("[gRPC] PANIC in %s: %v\n%s", info.FullMethod, r, debug.Stack())
                err = status.Errorf(codes.Internal, "internal server error")
            }
        }()
        return handler(ctx, req)
    }
}
```

주목할 점은 `err`이 named return이라는 것이다. `defer` 안에서 `err`를 할당하면 함수의 반환값이 바뀌므로, 패닉 대신 에러 응답이 클라이언트에 전달된다.

### 인터셉터 체이닝

`main.go`에서 `grpc.ChainUnaryInterceptor`로 두 인터셉터를 체인한다. Recovery가 먼저 등록되어 모든 패닉을 잡고, Logging이 그 다음에 요청 로그를 남긴다.

```go
// main.go
grpcServer := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        middleware.RecoveryInterceptor(),  // 1순위: 패닉 복구
        middleware.LoggingInterceptor(),   // 2순위: 요청 로깅
    ),
)
```

---

## 8. 임베딩 (Composition over Inheritance)

Go에는 상속이 없다. 대신 구조체 임베딩으로 다른 타입의 메서드를 "물려받는다". git-provider의 모든 gRPC 서버가 `pb.UnimplementedXxxServiceServer`를 임베딩한다.

```go
// git_server.go
type GitServer struct {
    pb.UnimplementedGitServiceServer  // 임베딩
}

// cicd_server.go
type CICDServer struct {
    pb.UnimplementedCICDServiceServer  // 임베딩
    store    *pipeline.Store
    producer *kafka.EventProducer
}
```

### 왜 Unimplemented를 임베딩하는가

protoc가 생성하는 `UnimplementedGitServiceServer`는 모든 RPC 메서드의 기본 구현("unimplemented" 에러 반환)을 가진다. 이것을 임베딩하면 두 가지 이점이 있다.

1. **forward compatibility**: proto 파일에 새 RPC를 추가해도 기존 서버 코드가 컴파일된다. 구현하지 않은 메서드는 `Unimplemented` 에러를 자동 반환한다.
2. **점진적 구현**: 전체 RPC를 한 번에 구현하지 않아도 서버가 정상 동작한다. 필요한 메서드만 오버라이드(재정의)하면 된다.

임베딩 없이 인터페이스를 직접 구현하면, proto에 RPC 하나 추가할 때마다 모든 서버 구현체에서 컴파일 에러가 발생한다.

---

## 9. 의존성 주입

### Constructor Injection

의존성이 필요한 서비스는 생성자 함수(`NewXxx`)의 파라미터로 주입받는다.

```go
// cicd_server.go
func NewCICDServer(store *pipeline.Store, producer *kafka.EventProducer) *CICDServer {
    return &CICDServer{
        store:    store,
        producer: producer,
    }
}
```

호출하는 쪽(`main.go`)에서 의존성을 직접 생성하고 주입한다.

```go
// main.go
store := pipeline.NewStore()
producer, _ := newKafkaProducer(brokers)
cicdServer := server.NewCICDServer(store, producer)
```

### 의존성이 없는 서비스 vs 있는 서비스

```go
// 의존성 없음 — 빈 생성자
func NewGitServer() *GitServer {
    return &GitServer{}
}

// 의존성 있음 — store, producer 주입
func NewCICDServer(store *pipeline.Store, producer *kafka.EventProducer) *CICDServer {
    return &CICDServer{store: store, producer: producer}
}
```

GitService, BranchService, ContentsService, MergeRequestService는 상태 없이 프로바이더 API만 호출하므로 의존성이 없다. CICDService와 WorkflowService는 인메모리 스토어와 Kafka 프로듀서가 필요하므로 주입받는다.

### BuildStore 인터페이스 — 테스트 용이성

`cicd/trigger.go`에서 `pipeline.Store`를 직접 참조하지 않고 `BuildStore` 인터페이스로 추상화한다.

```go
// trigger.go
type BuildStore interface {
    AddBuild(pipelineID, trigger, branch, commitSHA string) (*pb.Build, error)
    UpdateBuildStatus(pipelineID string, buildNumber int32, status pb.BuildStatus, url string, durationSeconds int32) error
    GetPipeline(id string) (*pb.Pipeline, error)
}
```

이렇게 하면 테스트 시 실제 `pipeline.Store` 대신 목(mock) 구현을 주입할 수 있다. 전체 스토어의 메서드 중 트리거 로직이 사용하는 3개만 인터페이스로 추출했으므로, 목의 구현 비용도 최소화된다.

---

## 10. 제네릭 함수

Go 1.18에서 도입된 제네릭을 Kafka 이벤트 파싱에 활용한다.

```go
// consumer.go
func ParseEvent[T any](value []byte) (T, error) {
    var event T
    if err := json.Unmarshal(value, &event); err != nil {
        return event, fmt.Errorf("unmarshal event: %w", err)
    }
    return event, nil
}
```

사용하는 쪽에서 타입 파라미터를 명시한다.

```go
event, err := kafka.ParseEvent[kafka.GitEvent](value)          // GitEvent로 역직렬화
cmd, err := kafka.ParseEvent[kafka.TriggerBuildCommand](value)  // TriggerBuildCommand로
event, err := kafka.ParseEvent[kafka.BuildCompletedEvent](value) // BuildCompletedEvent로
```

제네릭 없이 구현했다면 각 이벤트 타입마다 `ParseGitEvent()`, `ParseBuildCommand()` 같은 함수를 따로 만들어야 했을 것이다. `ParseEvent[T]` 하나로 모든 이벤트 타입을 처리한다.

---

## 11. Kafka Consumer 패턴: Handler Registry

Kafka 컨슈머가 하나의 클라이언트로 여러 토픽을 소비하면서, 토픽별로 다른 핸들러를 실행하는 패턴이다.

```go
// consumer.go
type MessageHandler func(ctx context.Context, topic string, key, value []byte) error

type EventConsumer struct {
    client   *kgo.Client
    handlers map[string]MessageHandler  // 토픽 → 핸들러 맵
}

func (c *EventConsumer) RegisterHandler(topic string, handler MessageHandler) {
    c.handlers[topic] = handler
}

func (c *EventConsumer) Run(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return  // graceful shutdown
        default:
        }

        fetches := c.client.PollFetches(ctx)
        // ... 에러 처리 ...

        fetches.EachRecord(func(record *kgo.Record) {
            handler, ok := c.handlers[record.Topic]
            if !ok {
                return  // 핸들러 미등록 토픽 → 무시
            }
            if err := handler(ctx, record.Topic, record.Key, record.Value); err != nil {
                log.Printf("handler error topic=%s key=%s: %v",
                    record.Topic, string(record.Key), err)
            }
        })
    }
}
```

핵심은 `MessageHandler`가 함수 타입이라는 점이다. 인터페이스가 아니라 함수 시그니처로 계약을 정의하므로, 핸들러 등록 시 클로저를 바로 넘길 수 있다. `MakeGitEventHandler()`, `MakeCommandHandler()`, `MakeCICDEventHandler()` 모두 `MessageHandler`를 반환하는 팩토리 함수이고, 내부에서 클로저로 필요한 의존성(store, producer, engine)을 캡처한다.
