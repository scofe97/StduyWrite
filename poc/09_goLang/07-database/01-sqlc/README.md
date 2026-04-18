# SQLC 타입 안전 SQL 학습

## 학습 목표

sqlc를 사용하여 SQL-first 접근 방식으로 타입 안전한 데이터베이스 코드를 생성하는 방법을 익힙니다.

## SQLC란?

sqlc는 SQL 쿼리에서 타입 안전한 Go 코드를 생성하는 도구입니다.

**주요 특징**:
- SQL-first: SQL을 직접 작성, ORM 불필요
- 컴파일 타임 타입 체크
- 쿼리 유효성 검증
- 고성능 (반사 없음)

**ORM과 비교**:
| 항목 | sqlc | GORM/Ent |
|------|------|----------|
| 접근 방식 | SQL-first | Code-first |
| 타입 안전 | 컴파일 타임 | 런타임 |
| 학습 곡선 | SQL 지식 필요 | ORM 문법 학습 |
| 성능 | 최적화 가능 | 추상화 오버헤드 |
| 유연성 | 높음 | 중간 |

## 핵심 개념

### 1. 쿼리 어노테이션

```sql
-- name: GetUser :one
SELECT * FROM users WHERE id = ?;

-- name: ListUsers :many
SELECT * FROM users ORDER BY created_at;

-- name: CreateUser :exec
INSERT INTO users (name, email) VALUES (?, ?);

-- name: CreateUserReturning :one
INSERT INTO users (name, email) VALUES (?, ?) RETURNING *;
```

### 2. 어노테이션 타입

| 타입 | 설명 | 반환 |
|------|------|------|
| `:one` | 단일 행 반환 | `(Model, error)` |
| `:many` | 여러 행 반환 | `([]Model, error)` |
| `:exec` | 실행만 (반환 없음) | `error` |
| `:execresult` | 실행 결과 반환 | `(sql.Result, error)` |
| `:execrows` | 영향 받은 행 수 | `(int64, error)` |

### 3. 생성된 코드

```go
// sqlc가 생성한 코드
type Post struct {
    ID        int64
    Title     string
    Content   string
    Status    string
    Author    string
    CreatedAt time.Time
    UpdatedAt time.Time
}

func (q *Queries) GetPost(ctx context.Context, id int64) (Post, error)
func (q *Queries) ListPosts(ctx context.Context) ([]Post, error)
func (q *Queries) CreatePost(ctx context.Context, arg CreatePostParams) (Post, error)
```

## 프로젝트 구조

```
26-sqlc/
├── main.go              # 엔트리 포인트
├── sqlc.yaml            # sqlc 설정
├── db/
│   ├── schema.sql       # 데이터베이스 스키마
│   └── queries/
│       └── posts.sql    # SQL 쿼리 (어노테이션 포함)
├── internal/db/         # sqlc 생성 코드 (자동 생성)
│   ├── db.go
│   ├── models.go
│   └── posts.sql.go
├── go.mod
├── README.md            # 이 파일
├── EXERCISES.md         # 실습 과제
├── HINTS.md             # 힌트
└── LEARNED.md           # 학습 회고
```

## 학습 흐름

### 1단계: sqlc 설정
- sqlc 설치
- sqlc.yaml 설정
- 스키마 작성

### 2단계: 쿼리 작성
- 기본 CRUD 쿼리
- 어노테이션 타입 이해
- 파라미터 바인딩

### 3단계: 코드 생성 및 사용
- `sqlc generate` 실행
- 생성된 코드 이해
- Go 코드에서 사용

### 4단계: 트랜잭션
- `WithTx()` 사용
- 트랜잭션 패턴

## 주요 명령어

### sqlc 설치

```bash
# Go install
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest

# 또는 brew (macOS)
brew install sqlc

# Windows (scoop)
scoop install sqlc
```

### 코드 생성

```bash
# 코드 생성
sqlc generate

# 설정 검증
sqlc compile

# 쿼리 검증
sqlc verify
```

## 실행 예시

```bash
# 1. sqlc 설치
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest

# 2. SQLite 드라이버 설치
go get -u modernc.org/sqlite

# 3. 코드 생성
sqlc generate

# 4. 실행
go run main.go
```

## 참고 자료

- [SQLC 공식 문서](https://sqlc.dev/)
- [SQLC GitHub](https://github.com/sqlc-dev/sqlc)
- [SQLC Playground](https://play.sqlc.dev/)

### 연관 모듈
- **25-go-chi**: HTTP 핸들러에서 sqlc 사용
- **27-fsm**: 상태 전이와 함께 DB 업데이트
- **28-capstone**: 전체 Blog API에서 통합

## 다음 단계

1. `EXERCISES.md`에서 TODO 체크박스 확인
2. sqlc 설치 및 코드 생성
3. 각 파일의 TODO 주석을 채우며 구현
4. `HINTS.md`는 막힐 때만 참고
5. 완료 후 `LEARNED.md`에 회고 작성

## 디버깅 팁

```bash
# sqlc 설정 확인
sqlc compile

# 생성된 코드 확인
cat internal/db/models.go

# SQLite 데이터 확인
sqlite3 blog.db "SELECT * FROM posts;"
```

## 성공 기준

- [ ] sqlc 설치 및 설정 완료
- [ ] 코드 생성 성공
- [ ] CRUD 작업 동작
- [ ] 트랜잭션 사용 가능
- [ ] 타입 안전하게 쿼리 작성

---

**시작하기**: `EXERCISES.md`를 열고 첫 번째 TODO부터 시작하세요!
