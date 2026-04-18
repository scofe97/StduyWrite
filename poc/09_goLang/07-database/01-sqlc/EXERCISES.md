# SQLC 실습 과제

## 목표

sqlc를 활용하여 타입 안전한 데이터베이스 코드를 생성하고 사용합니다.

---

## Phase 1: sqlc 설정

### Task 1.1: sqlc 설치
- [ ] sqlc CLI 설치
  ```bash
  go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
  ```
- [ ] 버전 확인: `sqlc version`
- [ ] SQLite 드라이버 설치: `go get -u modernc.org/sqlite`

### Task 1.2: sqlc.yaml 확인
- [ ] `sqlc.yaml` 파일 확인
- [ ] 설정 검증: `sqlc compile`
- [ ] 에러가 있으면 수정

### Task 1.3: 스키마 확인
- [ ] `db/schema.sql` 파일 확인
- [ ] posts 테이블 구조 이해
- [ ] 인덱스 확인

---

## Phase 2: 쿼리 작성

### Task 2.1: 기본 쿼리 확인 (db/queries/posts.sql)
- [ ] GetPost 쿼리 (`:one`) 확인
- [ ] ListPosts 쿼리 (`:many`) 확인
- [ ] CreatePost 쿼리 (`:one` + RETURNING) 확인
- [ ] DeletePost 쿼리 (`:exec`) 확인

### Task 2.2: 코드 생성
- [ ] `sqlc generate` 실행
- [ ] `internal/db/` 디렉토리에 파일 생성 확인:
  - `db.go`
  - `models.go`
  - `posts.sql.go`
- [ ] 생성된 코드 읽어보기

### Task 2.3: 모델 확인
- [ ] `internal/db/models.go` 열기
- [ ] Post 구조체 확인
- [ ] JSON 태그 확인

---

## Phase 3: 기본 CRUD

### Task 3.1: 데이터베이스 연결
- [ ] main.go에서 SQLite 연결
- [ ] 스키마 초기화 함수 호출
- [ ] 테스트: `go run main.go` 에러 없이 실행

### Task 3.2: 게시글 생성
- [ ] `queries.CreatePost()` 사용
- [ ] CreatePostParams 구조체 채우기
- [ ] 생성된 게시글 출력
- [ ] 테스트: 게시글 생성 확인

### Task 3.3: 게시글 조회
- [ ] `queries.GetPost(ctx, id)` 사용
- [ ] `queries.ListPosts(ctx)` 사용
- [ ] `queries.ListPostsByStatus(ctx, "draft")` 사용
- [ ] 테스트: 조회 결과 출력

### Task 3.4: 게시글 수정/삭제
- [ ] `queries.UpdatePost()` 사용
- [ ] `queries.UpdatePostStatus()` 사용
- [ ] `queries.DeletePost()` 사용
- [ ] 테스트: 수정/삭제 동작 확인

---

## Phase 4: 상태 관리

### Task 4.1: 상태 전이 구현
- [ ] draft → published 전이 함수
- [ ] published → archived 전이 함수
- [ ] 잘못된 전이 시 에러 반환
- [ ] 테스트:
  ```go
  // draft → published (OK)
  // published → draft (Error)
  ```

### Task 4.2: 상태별 카운트
- [ ] `queries.CountPostsByStatus()` 사용
- [ ] 각 상태별 게시글 수 출력
- [ ] 테스트:
  ```
  Draft: 3
  Published: 5
  Archived: 2
  ```

### Task 4.3: 검색 기능
- [ ] `queries.SearchPosts()` 사용
- [ ] 제목/내용에서 키워드 검색
- [ ] LIKE 패턴 적용 (`%keyword%`)
- [ ] 테스트:
  ```go
  posts, _ := queries.SearchPosts(ctx, "%hello%", "%hello%")
  ```

---

## Phase 5: 트랜잭션

### Task 5.1: 트랜잭션 기본
- [ ] `conn.BeginTx()` 로 트랜잭션 시작
- [ ] `queries.WithTx(tx)` 로 트랜잭션 쿼리 객체 생성
- [ ] `tx.Commit()` 또는 `tx.Rollback()` 호출
- [ ] 테스트: 트랜잭션 성공/실패 확인

### Task 5.2: 트랜잭션 헬퍼 함수
- [ ] `runWithTransaction()` 함수 구현
- [ ] 에러 시 자동 롤백
- [ ] 성공 시 자동 커밋
- [ ] 테스트: 헬퍼 함수로 트랜잭션 실행

### Task 5.3: 복합 작업 트랜잭션
- [ ] 여러 게시글을 한 트랜잭션에서 생성
- [ ] 하나라도 실패하면 전체 롤백
- [ ] 테스트:
  ```go
  // 3개 게시글 생성 시도
  // 2번째 실패 → 전체 롤백
  ```

---

## Phase 6: 고급 쿼리 (선택)

### Task 6.1: 페이지네이션 쿼리 추가
- [ ] `db/queries/posts.sql`에 새 쿼리 추가:
  ```sql
  -- name: ListPostsPaginated :many
  SELECT * FROM posts
  ORDER BY created_at DESC
  LIMIT ? OFFSET ?;
  ```
- [ ] `sqlc generate` 재실행
- [ ] 테스트: 페이지별 조회

### Task 6.2: 집계 쿼리
- [ ] 작성자별 게시글 수 쿼리 추가:
  ```sql
  -- name: CountPostsByAuthor :many
  SELECT author, COUNT(*) as count
  FROM posts
  GROUP BY author;
  ```
- [ ] 테스트: 집계 결과 출력

### Task 6.3: 조인 쿼리 (카테고리 테이블 사용)
- [ ] 카테고리 CRUD 쿼리 추가
- [ ] 게시글-카테고리 연결 쿼리 추가
- [ ] 게시글 + 카테고리 조인 쿼리 추가
- [ ] 테스트: 카테고리 포함 게시글 조회

---

## Bonus Tasks

### Bonus 1: Null 처리
- [ ] `sql.NullString` 타입 이해
- [ ] 선택적 필드에 Null 허용
- [ ] sqlc 설정에서 `emit_pointers_for_null_types` 사용

### Bonus 2: 배치 작업
- [ ] 여러 행을 한 번에 삽입하는 쿼리
- [ ] `UNION ALL` 또는 배치 INSERT
- [ ] 테스트: 100개 게시글 배치 생성

### Bonus 3: 마이그레이션
- [ ] goose 또는 golang-migrate 연동
- [ ] 스키마 버전 관리
- [ ] Up/Down 마이그레이션

---

## 학습 체크리스트

### 기본 개념
- [ ] sqlc.yaml 설정 이해
- [ ] 쿼리 어노테이션 (:one, :many, :exec)
- [ ] 파라미터 바인딩 (?)
- [ ] RETURNING 절 사용

### 코드 생성
- [ ] `sqlc generate` 명령어
- [ ] 생성된 모델 구조체 이해
- [ ] 생성된 쿼리 함수 시그니처 이해
- [ ] Params 구조체 사용

### 고급 기능
- [ ] 트랜잭션 사용 (WithTx)
- [ ] Null 타입 처리
- [ ] 복잡한 쿼리 (JOIN, GROUP BY)
- [ ] 페이지네이션

---

## 성공 기준

모든 Task를 완료하면:

```bash
$ sqlc generate
# 에러 없이 코드 생성

$ go run main.go

# 게시글 CRUD 테스트
Created post: {ID:1 Title:Hello World Status:draft Author:john}
Listed 3 posts
Updated status to: published
Deleted post ID: 1

# 트랜잭션 테스트
Transaction: Creating 3 posts...
All posts created successfully

# 검색 테스트
Found 2 posts matching 'hello'

# 상태별 카운트
Draft: 2
Published: 3
Archived: 1
```

---

**진행 방법**:
1. Phase 1부터 순서대로 진행
2. `sqlc generate` 후 생성된 코드 확인
3. 각 Task의 체크박스를 완료하면 체크
4. 막히면 `HINTS.md` 참고 (스포일러 주의!)
5. `LEARNED.md`에 학습 내용 정리

**예상 소요 시간**: 2-3시간
