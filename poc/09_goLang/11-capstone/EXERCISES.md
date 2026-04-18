# Blog API Capstone 실습 과제

## 목표

이전 모듈에서 학습한 모든 라이브러리를 통합하여 완전한 Blog API를 구현합니다.

---

## Phase 1: 프로젝트 설정

### Task 1.1: 의존성 설치
- [ ] 모든 라이브러리 설치 (README 참고)
- [ ] `go mod tidy` 실행
- [ ] go.mod 파일 의존성 확인

### Task 1.2: sqlc 코드 생성
- [ ] `sqlc generate` 실행
- [ ] `internal/repository/` 디렉토리에 파일 생성 확인:
  - db.go
  - models.go
  - posts.sql.go
- [ ] 생성된 코드 리뷰

### Task 1.3: 기본 실행 테스트
- [ ] `go run cmd/server/main.go` 실행
- [ ] `curl http://localhost:8080/health` 테스트
- [ ] 로그 출력 확인

---

## Phase 2: 설정 통합 (koanf)

### Task 2.1: config.Load 사용
- [ ] main.go에서 `config.Load()` 호출
- [ ] 설정 값 로그로 출력
- [ ] 테스트: 설정 값 확인

### Task 2.2: 환경변수 오버라이드
- [ ] `BLOG_SERVER_PORT=9090` 테스트
- [ ] `BLOG_LOG_LEVEL=debug` 테스트
- [ ] 환경변수가 파일 설정을 오버라이드 확인

---

## Phase 3: 로깅 통합 (zerolog)

### Task 3.1: 로거 초기화
- [ ] main.go에서 zerolog 로거 생성
- [ ] 설정에 따라 ConsoleWriter/JSON 선택
- [ ] 로그 레벨 설정

### Task 3.2: 미들웨어 로깅
- [ ] router.go의 loggerMiddleware 확인
- [ ] 요청/응답 로깅 동작 확인
- [ ] 로그에 method, path, status, duration 포함 확인

### Task 3.3: 핸들러 로깅
- [ ] handlers.go에서 주요 작업 로깅
- [ ] 게시글 생성/삭제 시 로그 출력
- [ ] 에러 발생 시 에러 로그 출력

---

## Phase 4: 데이터베이스 통합 (sqlc)

### Task 4.1: 데이터베이스 연결
- [ ] main.go에서 SQLite 연결
- [ ] 스키마 초기화 (CREATE TABLE)
- [ ] 연결 테스트

### Task 4.2: 핸들러에서 쿼리 사용
- [ ] handlers.go에서 repository.Queries 사용
- [ ] ListPosts 핸들러 완성
- [ ] GetPost 핸들러 완성
- [ ] CreatePost 핸들러 완성
- [ ] UpdatePost 핸들러 완성
- [ ] DeletePost 핸들러 완성

### Task 4.3: API 테스트
- [ ] CRUD 전체 동작 테스트
  ```bash
  # 생성
  curl -X POST localhost:8080/api/posts -d '{"title":"Test","author":"john"}'

  # 조회
  curl localhost:8080/api/posts
  curl localhost:8080/api/posts/1

  # 수정
  curl -X PUT localhost:8080/api/posts/1 -d '{"title":"Updated"}'

  # 삭제
  curl -X DELETE localhost:8080/api/posts/1
  ```

---

## Phase 5: 상태 관리 통합 (FSM)

### Task 5.1: 도메인 모델 이해
- [ ] `internal/domain/post.go` 리뷰
- [ ] FSM 상태/이벤트 정의 확인
- [ ] Publish, Archive, Republish 메서드 확인

### Task 5.2: PublishPost 핸들러 구현
- [ ] DB에서 게시글 로드
- [ ] `domain.FromRepository()`로 도메인 객체 생성
- [ ] `post.Publish()` 호출 (FSM 전이)
- [ ] DB 상태 업데이트
- [ ] 에러 처리 (잘못된 전이)

### Task 5.3: ArchivePost 핸들러 구현
- [ ] 동일한 패턴으로 구현
- [ ] published 상태에서만 archive 가능 확인

### Task 5.4: 상태 전이 테스트
- [ ] 테스트 시나리오:
  ```bash
  # 1. 게시글 생성 (draft)
  curl -X POST localhost:8080/api/posts -d '{"title":"Test","author":"john"}'
  # → status: "draft"

  # 2. 발행 (draft → published)
  curl -X POST localhost:8080/api/posts/1/publish
  # → status: "published"

  # 3. 재발행 시도 (이미 published → 에러)
  curl -X POST localhost:8080/api/posts/1/publish
  # → error: "cannot publish"

  # 4. 보관 (published → archived)
  curl -X POST localhost:8080/api/posts/1/archive
  # → status: "archived"
  ```

---

## Phase 6: 완성도 높이기

### Task 6.1: 에러 응답 개선
- [ ] 일관된 에러 응답 형식
- [ ] HTTP 상태 코드 적절히 사용
- [ ] 에러 메시지 사용자 친화적으로

### Task 6.2: 입력 유효성 검사
- [ ] 빈 제목 체크
- [ ] 빈 작성자 체크
- [ ] 유효성 에러 시 400 Bad Request

### Task 6.3: 그레이스풀 셧다운
- [ ] main.go의 startServer 함수 활성화
- [ ] Ctrl+C로 종료 테스트
- [ ] "Server exited properly" 메시지 확인

---

## Bonus Tasks

### Bonus 1: 페이지네이션
- [ ] ListPosts에 페이지네이션 추가
- [ ] 쿼리 파라미터: `?page=1&limit=10`
- [ ] 응답에 total, page, limit 포함

### Bonus 2: 검색 기능
- [ ] `GET /api/posts?q=keyword` 검색
- [ ] 제목/내용에서 검색
- [ ] sqlc 쿼리 추가 필요

### Bonus 3: 상태별 필터링
- [ ] `GET /api/posts?status=published` 필터
- [ ] 여러 상태 필터 지원

### Bonus 4: 통합 테스트
- [ ] httptest 패키지로 테스트 작성
- [ ] 각 엔드포인트 테스트
- [ ] 에러 케이스 테스트

---

## 학습 체크리스트

### 통합 확인
- [ ] koanf로 설정 로드
- [ ] zerolog로 로깅
- [ ] chi로 라우팅
- [ ] sqlc로 DB 접근
- [ ] fsm으로 상태 관리

### 아키텍처
- [ ] cmd: 애플리케이션 진입점
- [ ] internal/api: HTTP 계층
- [ ] internal/domain: 비즈니스 로직
- [ ] internal/repository: 데이터 접근
- [ ] internal/config: 설정 관리

### 패턴
- [ ] 의존성 주입 (Handler에 DB, Logger 전달)
- [ ] 계층 분리 (API → Domain → Repository)
- [ ] 에러 처리 (각 계층별)

---

## 성공 기준

모든 Task를 완료하면:

```bash
# 서버 시작
$ go run cmd/server/main.go
{"level":"info","time":"...","message":"Starting Blog API server"}
{"level":"info","config":{"port":8080,"db":"blog.db"},"message":"Config loaded"}

# 게시글 생성
$ curl -X POST localhost:8080/api/posts \
    -H "Content-Type: application/json" \
    -d '{"title":"Hello","content":"World","author":"john"}'
{"success":true,"data":{"id":1,"title":"Hello","status":"draft"}}

# 발행
$ curl -X POST localhost:8080/api/posts/1/publish
{"success":true,"data":{"id":1,"status":"published"}}

# 보관
$ curl -X POST localhost:8080/api/posts/1/archive
{"success":true,"data":{"id":1,"status":"archived"}}

# 잘못된 전이
$ curl -X POST localhost:8080/api/posts/1/publish
{"success":false,"error":"cannot publish: event publish inappropriate in current state archived"}

# 서버 로그
{"level":"info","method":"POST","path":"/api/posts","status":201,"duration":"2.5ms","message":"Request handled"}
{"level":"info","method":"POST","path":"/api/posts/1/publish","status":200,"duration":"1.2ms","message":"Request handled"}
```

---

**진행 방법**:
1. Phase 1부터 순서대로 진행
2. 각 Phase 완료 후 다음으로
3. 막히면 `HINTS.md` 참고
4. 완료 후 `LEARNED.md`에 전체 회고

**예상 소요 시간**: 3-4시간
