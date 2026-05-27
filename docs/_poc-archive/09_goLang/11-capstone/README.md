# Blog API - Capstone Project

## 개요

이 프로젝트는 이전 모듈에서 학습한 모든 라이브러리를 통합한 캡스톤 프로젝트입니다.

**통합 라이브러리**:
- **zerolog** (23): 구조화된 로깅
- **koanf** (24): 설정 관리
- **go-chi** (25): HTTP 라우터
- **sqlc** (26): 타입 안전 SQL
- **fsm** (27): 상태 기계

## 기능

### 게시글 CRUD
- `POST /api/posts` - 게시글 생성 (draft 상태)
- `GET /api/posts` - 게시글 목록
- `GET /api/posts/:id` - 게시글 상세
- `PUT /api/posts/:id` - 게시글 수정
- `DELETE /api/posts/:id` - 게시글 삭제

### 상태 관리 (FSM)
- `POST /api/posts/:id/publish` - draft → published
- `POST /api/posts/:id/archive` - published → archived

```
[draft] --publish--> [published] --archive--> [archived]
                          ^                       |
                          +-----republish---------+
```

## 프로젝트 구조

```
28-capstone/
├── cmd/
│   └── server/
│       └── main.go          # 애플리케이션 진입점
├── internal/
│   ├── api/
│   │   ├── router.go        # chi 라우터 설정
│   │   └── handlers/
│   │       └── handlers.go  # HTTP 핸들러
│   ├── config/
│   │   └── config.go        # koanf 설정 로드
│   ├── domain/
│   │   └── post.go          # 도메인 모델 + FSM
│   └── repository/          # sqlc 생성 코드
│       └── .gitkeep
├── db/
│   ├── schema.sql           # 데이터베이스 스키마
│   └── queries/
│       └── posts.sql        # SQL 쿼리
├── configs/
│   └── config.yaml          # 설정 파일
├── sqlc.yaml                # sqlc 설정
├── go.mod
├── README.md
├── EXERCISES.md
├── HINTS.md
└── LEARNED.md
```

## 시작하기

### 1. 의존성 설치

```bash
cd 28-capstone

# 모든 의존성 설치
go get -u github.com/go-chi/chi/v5
go get -u github.com/rs/zerolog
go get -u github.com/knadh/koanf/v2
go get -u github.com/knadh/koanf/parsers/yaml
go get -u github.com/knadh/koanf/providers/file
go get -u github.com/knadh/koanf/providers/env
go get -u github.com/looplab/fsm
go get -u modernc.org/sqlite

go mod tidy
```

### 2. sqlc 코드 생성

```bash
# sqlc 설치 (이미 설치했다면 건너뛰기)
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest

# 코드 생성
sqlc generate
```

### 3. 서버 실행

```bash
go run cmd/server/main.go
```

### 4. API 테스트

```bash
# 헬스 체크
curl http://localhost:8080/health

# 게시글 생성
curl -X POST http://localhost:8080/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello World","content":"My first post","author":"john"}'

# 게시글 목록
curl http://localhost:8080/api/posts

# 게시글 상세
curl http://localhost:8080/api/posts/1

# 게시글 발행
curl -X POST http://localhost:8080/api/posts/1/publish

# 게시글 보관
curl -X POST http://localhost:8080/api/posts/1/archive
```

## 설정

### config.yaml

```yaml
server:
  host: "localhost"
  port: 8080

database:
  path: "blog.db"

log:
  level: "info"
  format: "console"
```

### 환경변수 오버라이드

```bash
# 포트 변경
BLOG_SERVER_PORT=9090 go run cmd/server/main.go

# 로그 레벨 변경
BLOG_LOG_LEVEL=debug go run cmd/server/main.go
```

## 학습 목표

1. **통합 경험**: 여러 라이브러리를 함께 사용
2. **실무 패턴**: 실제 API 서버 구조 이해
3. **계층 분리**: 도메인, API, 저장소 계층 분리
4. **에러 처리**: 각 계층별 에러 처리

## 다음 단계

1. `EXERCISES.md`에서 단계별 과제 확인
2. TODO 주석을 따라 구현 완성
3. `HINTS.md`는 막힐 때만 참고
4. 완료 후 `LEARNED.md`에 회고 작성

---

**시작하기**: sqlc generate 실행 후 `EXERCISES.md`를 열고 시작하세요!
