# Blog API Capstone 힌트

막힐 때만 참고하세요! 스스로 해결하는 것이 학습에 더 효과적입니다.

---

## Phase 2: 설정 통합

<details>
<summary>Task 2.1: main.go에서 설정 로드</summary>

```go
func main() {
    // 설정 로드
    cfg, err := config.Load("configs/config.yaml")
    if err != nil {
        log.Fatalf("Failed to load config: %v", err)
    }

    fmt.Printf("Server will start on %s:%d\n", cfg.Server.Host, cfg.Server.Port)
    fmt.Printf("Database: %s\n", cfg.Database.Path)
    fmt.Printf("Log level: %s\n", cfg.Log.Level)

    // ... 계속
}
```
</details>

---

## Phase 3: 로깅 통합

<details>
<summary>Task 3.1: 로거 초기화</summary>

```go
import (
    "os"
    "time"
    "github.com/rs/zerolog"
)

func setupLogger(level, format string) zerolog.Logger {
    // 로그 레벨 설정
    var lvl zerolog.Level
    switch level {
    case "debug":
        lvl = zerolog.DebugLevel
    case "info":
        lvl = zerolog.InfoLevel
    case "warn":
        lvl = zerolog.WarnLevel
    case "error":
        lvl = zerolog.ErrorLevel
    default:
        lvl = zerolog.InfoLevel
    }
    zerolog.SetGlobalLevel(lvl)

    // 출력 형식
    var output io.Writer
    if format == "console" {
        output = zerolog.ConsoleWriter{
            Out:        os.Stdout,
            TimeFormat: time.RFC3339,
        }
    } else {
        output = os.Stdout
    }

    return zerolog.New(output).With().Timestamp().Logger()
}
```
</details>

---

## Phase 4: 데이터베이스 통합

<details>
<summary>Task 4.1: 데이터베이스 연결</summary>

```go
import (
    "database/sql"
    _ "modernc.org/sqlite"
    "blog-api/internal/repository"
)

func main() {
    // ... 설정 로드 ...

    // 데이터베이스 연결
    db, err := sql.Open("sqlite", cfg.Database.Path)
    if err != nil {
        logger.Fatal().Err(err).Msg("Failed to connect database")
    }
    defer db.Close()

    // 스키마 초기화
    if err := initSchema(db); err != nil {
        logger.Fatal().Err(err).Msg("Failed to initialize schema")
    }

    // ... 계속 ...
}

func initSchema(db *sql.DB) error {
    schema := `
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'draft',
        author TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
    `
    _, err := db.Exec(schema)
    return err
}
```
</details>

<details>
<summary>Task 4.2: 핸들러에서 쿼리 사용</summary>

**handlers.go 수정**:

```go
type Handler struct {
    queries *repository.Queries
    logger  zerolog.Logger
}

func NewHandler(db *sql.DB, logger zerolog.Logger) *Handler {
    return &Handler{
        queries: repository.New(db),
        logger:  logger,
    }
}

func (h *Handler) ListPosts(w http.ResponseWriter, r *http.Request) {
    posts, err := h.queries.ListPosts(r.Context())
    if err != nil {
        h.logger.Error().Err(err).Msg("Failed to list posts")
        respondError(w, http.StatusInternalServerError, "Failed to list posts")
        return
    }
    respondJSON(w, http.StatusOK, posts)
}

func (h *Handler) GetPost(w http.ResponseWriter, r *http.Request) {
    idStr := chi.URLParam(r, "id")
    id, err := strconv.ParseInt(idStr, 10, 64)
    if err != nil {
        respondError(w, http.StatusBadRequest, "Invalid ID")
        return
    }

    post, err := h.queries.GetPost(r.Context(), id)
    if err == sql.ErrNoRows {
        respondError(w, http.StatusNotFound, "Post not found")
        return
    }
    if err != nil {
        h.logger.Error().Err(err).Int64("id", id).Msg("Failed to get post")
        respondError(w, http.StatusInternalServerError, "Failed to get post")
        return
    }
    respondJSON(w, http.StatusOK, post)
}

func (h *Handler) CreatePost(w http.ResponseWriter, r *http.Request) {
    var req CreatePostRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "Invalid request body")
        return
    }

    if req.Title == "" || req.Author == "" {
        respondError(w, http.StatusBadRequest, "Title and author are required")
        return
    }

    post, err := h.queries.CreatePost(r.Context(), repository.CreatePostParams{
        Title:   req.Title,
        Content: req.Content,
        Status:  "draft",
        Author:  req.Author,
    })
    if err != nil {
        h.logger.Error().Err(err).Msg("Failed to create post")
        respondError(w, http.StatusInternalServerError, "Failed to create post")
        return
    }

    h.logger.Info().Int64("id", post.ID).Str("title", post.Title).Msg("Post created")
    respondJSON(w, http.StatusCreated, post)
}
```
</details>

---

## Phase 5: 상태 관리 통합

<details>
<summary>Task 5.2: PublishPost 핸들러 구현</summary>

```go
func (h *Handler) PublishPost(w http.ResponseWriter, r *http.Request) {
    idStr := chi.URLParam(r, "id")
    id, err := strconv.ParseInt(idStr, 10, 64)
    if err != nil {
        respondError(w, http.StatusBadRequest, "Invalid ID")
        return
    }

    // 1. DB에서 게시글 로드
    dbPost, err := h.queries.GetPost(r.Context(), id)
    if err == sql.ErrNoRows {
        respondError(w, http.StatusNotFound, "Post not found")
        return
    }
    if err != nil {
        h.logger.Error().Err(err).Int64("id", id).Msg("Failed to get post")
        respondError(w, http.StatusInternalServerError, "Failed to get post")
        return
    }

    // 2. 도메인 객체로 변환
    post := domain.FromRepository(
        dbPost.ID,
        dbPost.Title,
        dbPost.Content,
        dbPost.Status,
        dbPost.Author,
        dbPost.CreatedAt,
        dbPost.UpdatedAt,
    )

    // 3. FSM 상태 전이
    if err := post.Publish(); err != nil {
        h.logger.Warn().
            Err(err).
            Int64("id", id).
            Str("current_status", dbPost.Status).
            Msg("Cannot publish post")
        respondError(w, http.StatusBadRequest, err.Error())
        return
    }

    // 4. DB 업데이트
    updated, err := h.queries.UpdatePostStatus(r.Context(), repository.UpdatePostStatusParams{
        Status: post.Status,
        ID:     id,
    })
    if err != nil {
        h.logger.Error().Err(err).Int64("id", id).Msg("Failed to update post status")
        respondError(w, http.StatusInternalServerError, "Failed to update post")
        return
    }

    h.logger.Info().Int64("id", id).Str("status", updated.Status).Msg("Post published")
    respondJSON(w, http.StatusOK, updated)
}
```
</details>

<details>
<summary>Task 5.3: ArchivePost 핸들러 구현</summary>

```go
func (h *Handler) ArchivePost(w http.ResponseWriter, r *http.Request) {
    idStr := chi.URLParam(r, "id")
    id, err := strconv.ParseInt(idStr, 10, 64)
    if err != nil {
        respondError(w, http.StatusBadRequest, "Invalid ID")
        return
    }

    // DB에서 게시글 로드
    dbPost, err := h.queries.GetPost(r.Context(), id)
    if err == sql.ErrNoRows {
        respondError(w, http.StatusNotFound, "Post not found")
        return
    }
    if err != nil {
        respondError(w, http.StatusInternalServerError, "Failed to get post")
        return
    }

    // 도메인 객체로 변환 + FSM 전이
    post := domain.FromRepository(
        dbPost.ID, dbPost.Title, dbPost.Content,
        dbPost.Status, dbPost.Author,
        dbPost.CreatedAt, dbPost.UpdatedAt,
    )

    if err := post.Archive(); err != nil {
        respondError(w, http.StatusBadRequest, err.Error())
        return
    }

    // DB 업데이트
    updated, err := h.queries.UpdatePostStatus(r.Context(), repository.UpdatePostStatusParams{
        Status: post.Status,
        ID:     id,
    })
    if err != nil {
        respondError(w, http.StatusInternalServerError, "Failed to update post")
        return
    }

    h.logger.Info().Int64("id", id).Str("status", updated.Status).Msg("Post archived")
    respondJSON(w, http.StatusOK, updated)
}
```
</details>

---

## Phase 6: 완성도 높이기

<details>
<summary>Task 6.3: 그레이스풀 셧다운</summary>

**main.go 전체 구조**:

```go
func main() {
    // 1. 설정 로드
    cfg, err := config.Load("configs/config.yaml")
    if err != nil {
        log.Fatalf("Failed to load config: %v", err)
    }

    // 2. 로거 초기화
    logger := setupLogger(cfg.Log.Level, cfg.Log.Format)
    logger.Info().Msg("Starting Blog API server")

    // 3. 데이터베이스 연결
    db, err := sql.Open("sqlite", cfg.Database.Path)
    if err != nil {
        logger.Fatal().Err(err).Msg("Failed to connect database")
    }
    defer db.Close()

    if err := initSchema(db); err != nil {
        logger.Fatal().Err(err).Msg("Failed to initialize schema")
    }

    // 4. 라우터 설정
    router := api.NewRouter(db, logger)

    // 5. 서버 시작
    startServer(cfg.Server.Host, cfg.Server.Port, router, logger)
}

func startServer(host string, port int, handler http.Handler, logger zerolog.Logger) {
    addr := fmt.Sprintf("%s:%d", host, port)

    srv := &http.Server{
        Addr:         addr,
        Handler:      handler,
        ReadTimeout:  10 * time.Second,
        WriteTimeout: 10 * time.Second,
    }

    go func() {
        logger.Info().Str("addr", addr).Msg("Server starting")
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            logger.Fatal().Err(err).Msg("Server error")
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    logger.Info().Msg("Shutting down server...")

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        logger.Error().Err(err).Msg("Server forced to shutdown")
    }

    logger.Info().Msg("Server exited properly")
}
```
</details>

---

## 일반적인 문제 해결

<details>
<summary>sqlc 생성 코드 import 에러</summary>

**문제**: `package blog-api/internal/repository is not in GOROOT`

**해결**:
1. go.mod의 모듈 이름 확인: `module blog-api`
2. import 경로 확인: `"blog-api/internal/repository"`
3. sqlc.yaml의 package/out 설정 확인
4. `sqlc generate` 재실행
5. `go mod tidy` 실행
</details>

<details>
<summary>순환 import 에러</summary>

**문제**: `import cycle not allowed`

**해결**:
- domain 패키지는 다른 internal 패키지를 import하지 않아야 함
- repository → domain (OK)
- api → domain (OK)
- api → repository (OK)
- domain → repository (X)
</details>

<details>
<summary>Time 타입 문제</summary>

**문제**: sqlc 생성 모델과 domain 모델의 시간 타입이 다름

**해결**:
```go
// sqlc 모델 (repository/models.go)
type Post struct {
    CreatedAt time.Time
    UpdatedAt time.Time
}

// domain.FromRepository에서 직접 사용 가능
post := domain.FromRepository(
    dbPost.ID,
    // ...
    dbPost.CreatedAt,  // time.Time
    dbPost.UpdatedAt,  // time.Time
)
```
</details>

---

## 추가 리소스

**완성된 main.go 예시 구조**:

```
main()
├── config.Load()           # 설정 로드
├── setupLogger()           # 로거 초기화
├── sql.Open()              # DB 연결
├── initSchema()            # 스키마 초기화
├── api.NewRouter()         # 라우터 생성
└── startServer()           # 서버 시작
    ├── go ListenAndServe() # 고루틴
    ├── signal.Notify()     # 시그널 대기
    └── srv.Shutdown()      # 그레이스풀 셧다운
```

**유용한 디버깅 명령어**:

```bash
# SQLite 데이터 확인
sqlite3 blog.db "SELECT * FROM posts;"

# 로그 실시간 확인
go run cmd/server/main.go 2>&1 | jq .

# curl 상세 출력
curl -v localhost:8080/api/posts
```

---

**힌트를 너무 많이 봤다면**: 처음부터 다시 도전해보세요!
