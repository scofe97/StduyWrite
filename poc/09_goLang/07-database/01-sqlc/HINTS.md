# SQLC 힌트

막힐 때만 참고하세요! 스스로 해결하는 것이 학습에 더 효과적입니다.

---

## Phase 1: sqlc 설정

<details>
<summary>Task 1.1: sqlc 설치 문제</summary>

**Windows에서 설치**:
```bash
# Go install (권장)
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest

# scoop 사용
scoop install sqlc

# 직접 다운로드
# https://github.com/sqlc-dev/sqlc/releases
```

**PATH 확인**:
```bash
# Go bin 디렉토리가 PATH에 있는지 확인
echo $GOPATH/bin
# 또는
go env GOPATH
```
</details>

<details>
<summary>Task 1.2: sqlc.yaml 설정 문제</summary>

```yaml
version: "2"
sql:
  - engine: "sqlite"
    queries: "db/queries/"
    schema: "db/schema.sql"
    gen:
      go:
        package: "db"
        out: "internal/db"
        emit_json_tags: true
        emit_empty_slices: true
```

**주의사항**:
- `queries`는 디렉토리 경로 (끝에 `/`)
- `schema`는 파일 경로
- `out` 디렉토리가 존재해야 함 (또는 자동 생성)
</details>

---

## Phase 2: 쿼리 작성

<details>
<summary>Task 2.2: sqlc generate 에러</summary>

**일반적인 에러**:

1. **스키마 파싱 에러**:
   ```
   error parsing schema: ...
   ```
   → `db/schema.sql` 문법 확인

2. **쿼리 파싱 에러**:
   ```
   error parsing query: ...
   ```
   → `db/queries/*.sql` 문법 확인

3. **타입 미스매치**:
   ```
   column "..." has type "..." but expression has type "..."
   ```
   → 컬럼 타입과 파라미터 타입 확인

**디버깅**:
```bash
# 상세 에러 확인
sqlc compile

# 특정 쿼리만 테스트
sqlc verify
```
</details>

<details>
<summary>생성된 코드 구조 이해</summary>

**db.go** - 인터페이스:
```go
type DBTX interface {
    ExecContext(context.Context, string, ...interface{}) (sql.Result, error)
    PrepareContext(context.Context, string) (*sql.Stmt, error)
    QueryContext(context.Context, string, ...interface{}) (*sql.Rows, error)
    QueryRowContext(context.Context, string, ...interface{}) *sql.Row
}

func New(db DBTX) *Queries

type Queries struct {
    db DBTX
}

func (q *Queries) WithTx(tx *sql.Tx) *Queries
```

**models.go** - 모델:
```go
type Post struct {
    ID        int64     `json:"id"`
    Title     string    `json:"title"`
    Content   string    `json:"content"`
    Status    string    `json:"status"`
    Author    string    `json:"author"`
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
}
```

**posts.sql.go** - 쿼리 함수:
```go
type CreatePostParams struct {
    Title   string
    Content string
    Status  string
    Author  string
}

func (q *Queries) CreatePost(ctx context.Context, arg CreatePostParams) (Post, error)
func (q *Queries) GetPost(ctx context.Context, id int64) (Post, error)
func (q *Queries) ListPosts(ctx context.Context) ([]Post, error)
```
</details>

---

## Phase 3: 기본 CRUD

<details>
<summary>Task 3.1: 데이터베이스 연결</summary>

```go
import (
    "database/sql"
    _ "modernc.org/sqlite"  // SQLite 드라이버
    "sqlc-learning/internal/db"
)

func main() {
    // 연결
    conn, err := sql.Open("sqlite", "blog.db")
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    // 연결 테스트
    if err := conn.Ping(); err != nil {
        log.Fatal(err)
    }

    // 스키마 초기화
    if err := initSchema(conn); err != nil {
        log.Fatal(err)
    }

    // Queries 객체 생성
    queries := db.New(conn)

    // ... 사용 ...
}
```
</details>

<details>
<summary>Task 3.2: 게시글 생성</summary>

```go
ctx := context.Background()

// 게시글 생성
post, err := queries.CreatePost(ctx, db.CreatePostParams{
    Title:   "Hello World",
    Content: "My first post content",
    Status:  "draft",
    Author:  "john",
})
if err != nil {
    log.Fatal(err)
}

fmt.Printf("Created post: %+v\n", post)
```
</details>

<details>
<summary>Task 3.3: 게시글 조회</summary>

```go
// 단일 조회
post, err := queries.GetPost(ctx, 1)
if err != nil {
    if err == sql.ErrNoRows {
        fmt.Println("Post not found")
    } else {
        log.Fatal(err)
    }
}

// 목록 조회
posts, err := queries.ListPosts(ctx)
if err != nil {
    log.Fatal(err)
}

for _, p := range posts {
    fmt.Printf("[%s] %s by %s\n", p.Status, p.Title, p.Author)
}

// 상태별 조회
drafts, _ := queries.ListPostsByStatus(ctx, "draft")
fmt.Printf("Found %d drafts\n", len(drafts))
```
</details>

<details>
<summary>Task 3.4: 게시글 수정/삭제</summary>

```go
// 게시글 수정
updated, err := queries.UpdatePost(ctx, db.UpdatePostParams{
    Title:   "Updated Title",
    Content: "Updated content",
    ID:      1,
})
if err != nil {
    log.Fatal(err)
}
fmt.Printf("Updated: %+v\n", updated)

// 상태 변경
published, err := queries.UpdatePostStatus(ctx, db.UpdatePostStatusParams{
    Status: "published",
    ID:     1,
})
fmt.Printf("New status: %s\n", published.Status)

// 삭제
err = queries.DeletePost(ctx, 1)
if err != nil {
    log.Fatal(err)
}
fmt.Println("Post deleted")
```
</details>

---

## Phase 4: 상태 관리

<details>
<summary>Task 4.1: 상태 전이 구현</summary>

```go
// 허용된 상태 전이 정의
var validTransitions = map[string][]string{
    "draft":     {"published"},
    "published": {"archived"},
    "archived":  {"published"},
}

func transitionStatus(queries *db.Queries, ctx context.Context, postID int64, newStatus string) (*db.Post, error) {
    // 현재 게시글 조회
    post, err := queries.GetPost(ctx, postID)
    if err != nil {
        return nil, err
    }

    // 전이 유효성 검사
    allowed := validTransitions[post.Status]
    isValid := false
    for _, s := range allowed {
        if s == newStatus {
            isValid = true
            break
        }
    }

    if !isValid {
        return nil, fmt.Errorf("invalid transition: %s → %s", post.Status, newStatus)
    }

    // 상태 업데이트
    updated, err := queries.UpdatePostStatus(ctx, db.UpdatePostStatusParams{
        Status: newStatus,
        ID:     postID,
    })
    return &updated, err
}
```
</details>

<details>
<summary>Task 4.3: 검색 기능</summary>

```go
// 검색 (LIKE 패턴)
keyword := "hello"
pattern := "%" + keyword + "%"

posts, err := queries.SearchPosts(ctx, pattern, pattern)
if err != nil {
    log.Fatal(err)
}

fmt.Printf("Found %d posts matching '%s'\n", len(posts), keyword)
for _, p := range posts {
    fmt.Printf("- %s\n", p.Title)
}
```
</details>

---

## Phase 5: 트랜잭션

<details>
<summary>Task 5.1: 트랜잭션 기본</summary>

```go
ctx := context.Background()

// 트랜잭션 시작
tx, err := conn.BeginTx(ctx, nil)
if err != nil {
    log.Fatal(err)
}

// 트랜잭션용 Queries 생성
qtx := queries.WithTx(tx)

// 작업 수행
post1, err := qtx.CreatePost(ctx, db.CreatePostParams{
    Title: "Post 1", Content: "...", Status: "draft", Author: "john",
})
if err != nil {
    tx.Rollback()
    log.Fatal(err)
}

post2, err := qtx.CreatePost(ctx, db.CreatePostParams{
    Title: "Post 2", Content: "...", Status: "draft", Author: "john",
})
if err != nil {
    tx.Rollback()
    log.Fatal(err)
}

// 커밋
if err := tx.Commit(); err != nil {
    log.Fatal(err)
}

fmt.Printf("Created posts: %d, %d\n", post1.ID, post2.ID)
```
</details>

<details>
<summary>Task 5.2: 트랜잭션 헬퍼 함수</summary>

```go
func runWithTransaction(ctx context.Context, conn *sql.DB, fn func(*db.Queries) error) error {
    tx, err := conn.BeginTx(ctx, nil)
    if err != nil {
        return err
    }

    qtx := db.New(tx)

    if err := fn(qtx); err != nil {
        if rbErr := tx.Rollback(); rbErr != nil {
            return fmt.Errorf("tx err: %v, rollback err: %v", err, rbErr)
        }
        return err
    }

    return tx.Commit()
}

// 사용 예
err := runWithTransaction(ctx, conn, func(qtx *db.Queries) error {
    _, err := qtx.CreatePost(ctx, db.CreatePostParams{...})
    if err != nil {
        return err
    }

    _, err = qtx.CreatePost(ctx, db.CreatePostParams{...})
    return err
})
```
</details>

---

## Phase 6: 고급 쿼리

<details>
<summary>Task 6.1: 페이지네이션 쿼리</summary>

```sql
-- db/queries/posts.sql에 추가

-- name: ListPostsPaginated :many
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT ? OFFSET ?;
```

**사용**:
```go
// 페이지당 10개, 2페이지
limit := int64(10)
offset := int64(10) // (page - 1) * limit

posts, err := queries.ListPostsPaginated(ctx, limit, offset)
```
</details>

<details>
<summary>Task 6.2: 집계 쿼리</summary>

```sql
-- db/queries/posts.sql에 추가

-- name: CountPostsByAuthor :many
SELECT author, COUNT(*) as count
FROM posts
GROUP BY author
ORDER BY count DESC;
```

**sqlc 생성 결과**:
```go
type CountPostsByAuthorRow struct {
    Author string
    Count  int64
}

func (q *Queries) CountPostsByAuthor(ctx context.Context) ([]CountPostsByAuthorRow, error)
```

**사용**:
```go
stats, err := queries.CountPostsByAuthor(ctx)
for _, s := range stats {
    fmt.Printf("%s: %d posts\n", s.Author, s.Count)
}
```
</details>

---

## 일반적인 문제 해결

<details>
<summary>sqlc generate 후 import 에러</summary>

**문제**: `package sqlc-learning/internal/db is not in GOROOT`

**해결**:
1. go.mod 모듈 이름 확인
2. import 경로 일치 확인
3. `go mod tidy` 실행

```go
// go.mod
module sqlc-learning

// main.go
import "sqlc-learning/internal/db"  // 모듈 이름과 일치
```
</details>

<details>
<summary>SQLite 타입 매핑 문제</summary>

**SQLite → Go 타입 매핑**:
- `INTEGER` → `int64`
- `TEXT` → `string`
- `REAL` → `float64`
- `BLOB` → `[]byte`
- `DATETIME` → `time.Time`

**Null 처리**:
```yaml
# sqlc.yaml
gen:
  go:
    emit_pointers_for_null_types: true
    # 또는
    overrides:
      - column: "posts.deleted_at"
        go_type: "sql.NullTime"
```
</details>

<details>
<summary>RETURNING 절이 동작하지 않아요</summary>

**SQLite 3.35+ 필요**:
- RETURNING은 SQLite 3.35.0 (2021-03-12) 이상에서 지원
- modernc.org/sqlite는 최신 버전 지원

**대안 (오래된 SQLite)**:
```sql
-- name: CreatePost :exec
INSERT INTO posts (title, content, status, author) VALUES (?, ?, ?, ?);

-- name: GetLastInsertPost :one
SELECT * FROM posts WHERE id = last_insert_rowid();
```

```go
err := queries.CreatePost(ctx, params)
post, err := queries.GetLastInsertPost(ctx)
```
</details>

<details>
<summary>트랜잭션에서 데드락</summary>

**원인**: 같은 테이블에 동시 접근

**해결**:
1. 트랜잭션 시간 최소화
2. 일관된 순서로 테이블 접근
3. 적절한 격리 수준 설정

```go
tx, err := conn.BeginTx(ctx, &sql.TxOptions{
    Isolation: sql.LevelSerializable,
})
```
</details>

---

## 추가 리소스

**유용한 sqlc 설정**:

```yaml
version: "2"
sql:
  - engine: "sqlite"
    queries: "db/queries/"
    schema: "db/schema.sql"
    gen:
      go:
        package: "db"
        out: "internal/db"
        emit_json_tags: true
        emit_empty_slices: true
        emit_prepared_queries: false  # 준비된 쿼리 (성능 향상)
        emit_interface: true           # 인터페이스 생성 (테스트용)
        emit_exact_table_names: true   # 테이블 이름 그대로 사용
```

**참고 프로젝트**:
- [sqlc examples](https://github.com/sqlc-dev/sqlc/tree/main/examples)
- [sqlc playground](https://play.sqlc.dev/)

---

**힌트를 너무 많이 봤다면**: 파일을 삭제하고 처음부터 다시 도전해보세요!
