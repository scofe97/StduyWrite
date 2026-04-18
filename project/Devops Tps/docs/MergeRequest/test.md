# MergeRequest 테스트

## API 테스트 시나리오

### ListMergeRequests

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| OPEN MR 목록 조회 | status=OPEN | OPEN 상태 MR 목록 반환 |
| MERGED MR 목록 조회 | status=MERGED | MERGED 상태 MR 목록 반환 |
| 전체 상태 조회 | status 없음 | 기본 OPEN 목록 반환 |
| MR 없는 저장소 | 빈 저장소 | 빈 배열, totalCount=0 반환 |

**curl 예시**

```bash
# OPEN MR 목록
curl "http://localhost:8080/v1/merge-requests/550e8400-e29b-41d4-a716-446655440000/list?namespace=myorg&repository=myrepo&status=OPEN"

# POST 방식
curl -X POST "http://localhost:8080/v1/merge-requests/list" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "namespace": "myorg",
    "repository": "myrepo",
    "status": "OPEN"
  }'
```

---

### GetMergeRequest

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 존재하는 MR 조회 | number=42 | MR 상세 정보 반환 |
| 존재하지 않는 MR | number=9999 | 404 Not Found |
| MERGED 상태 MR 조회 | number=10 (merged) | mergedAt 필드 채워진 응답 반환 |

**curl 예시**

```bash
curl "http://localhost:8080/v1/merge-requests/550e8400-e29b-41d4-a716-446655440000/42?namespace=myorg&repository=myrepo"
```

---

### CreateMergeRequest

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 일반 MR 생성 | title, source/target branch | OPEN 상태 MR 반환 |
| Draft MR 생성 | draft=true | GitHub: draft=true, GitLab: 타이틀에 "Draft: " 접두사 |
| Bitbucket Draft 생성 | draft=true (Bitbucket) | OPEN MR으로 생성됨 (Draft 무시) |
| 동일 브랜치 MR 생성 | source=main, target=main | 400 또는 422 에러 |
| 타겟 브랜치 없음 | targetBranch=nonexistent | 404 Not Found |

**curl 예시 - 일반 MR 생성**

```bash
curl -X POST "http://localhost:8080/v1/merge-requests/create" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "namespace": "myorg",
    "repository": "myrepo",
    "title": "feat: Add login feature",
    "description": "## Summary\n- 로그인 기능 구현",
    "sourceBranch": "feature/login",
    "targetBranch": "main"
  }'
```

**curl 예시 - Draft MR 생성**

```bash
curl -X POST "http://localhost:8080/v1/merge-requests/create" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "namespace": "myorg",
    "repository": "myrepo",
    "title": "WIP: Refactor auth module",
    "sourceBranch": "feature/auth-refactor",
    "targetBranch": "develop",
    "draft": true
  }'
```

---

### UpdateMergeRequest

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 제목 수정 | title=새 제목 | 수정된 MR 반환 |
| MR 닫기 | state=closed | CLOSED 상태 MR 반환 |
| 닫힌 MR 재오픈 | state=open (CLOSED MR) | OPEN 상태로 복귀 |
| Draft 해제 (publish) | draft=false (DRAFT MR) | OPEN 상태 MR 반환 |
| MERGED MR 수정 시도 | state=closed (MERGED MR) | 409 Conflict |

**curl 예시 - Draft 해제**

```bash
curl -X PUT "http://localhost:8080/v1/merge-requests/550e8400-e29b-41d4-a716-446655440000/42" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "myorg",
    "repository": "myrepo",
    "draft": false
  }'
```

---

### MergeMergeRequest

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 기본 Merge | mergeMethod=MERGE | MERGED 상태 MR 반환 |
| Squash Merge (GitHub) | mergeMethod=SQUASH | 커밋 하나로 압축 후 머지 |
| Rebase Merge (GitHub) | mergeMethod=REBASE | 히스토리 재배치 후 머지 |
| Squash (Bitbucket) | mergeMethod=SQUASH | 501 Not Implemented |
| 충돌 있는 MR 머지 | mergeable=false | 422 Unprocessable |
| 이미 MERGED된 MR | MERGED 상태 MR | 409 Conflict |
| 소스 브랜치 자동 삭제 | deleteSourceBranch=true | 머지 후 소스 브랜치 삭제 확인 |

**curl 예시 - Squash Merge**

```bash
curl -X POST "http://localhost:8080/v1/merge-requests/merge" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "namespace": "myorg",
    "repository": "myrepo",
    "number": 42,
    "mergeMethod": "SQUASH",
    "commitMessage": "feat: Add login feature (#42)",
    "deleteSourceBranch": true
  }'
```

---

### GetMergeRequestDiff

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 변경파일 목록 조회 | number=42 | 파일별 additions/deletions/patch 반환 |
| 변경 없는 MR | 빈 커밋 MR | 빈 files 배열 반환 |

**curl 예시**

```bash
curl "http://localhost:8080/v1/merge-requests/550e8400-e29b-41d4-a716-446655440000/42/diff?namespace=myorg&repository=myrepo"
```

---

### ListReviews / SubmitReview

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 리뷰 목록 조회 (GitHub) | number=42 | 리뷰 목록 반환 |
| 리뷰 목록 조회 (Bitbucket) | number=42 | 빈 배열 반환 (에러 없음) |
| APPROVED 리뷰 제출 | state=APPROVED | 리뷰 생성 완료 |
| CHANGES_REQUESTED (Bitbucket) | state=CHANGES_REQUESTED | 댓글로 대체 처리 |

**curl 예시 - 리뷰 승인**

```bash
curl -X POST "http://localhost:8080/v1/merge-requests/550e8400-e29b-41d4-a716-446655440000/42/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "myorg",
    "repository": "myrepo",
    "state": "APPROVED",
    "body": "LGTM! 코드가 깔끔합니다."
  }'
```

---

### ListComments / CreateComment / UpdateComment / DeleteComment

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 댓글 목록 조회 | number=42 | 댓글 목록 반환 |
| 일반 댓글 생성 | body="좋은 작업입니다" | 댓글 생성 완료 |
| 인라인 댓글 생성 (GitHub) | body, path=src/main.go, line=42 | 해당 라인에 인라인 댓글 생성 |
| 인라인 댓글 생성 (Bitbucket) | body, path=src/main.go, line=42 | path/line 무시, 일반 댓글로 생성 |
| 댓글 수정 | commentId=123, body=수정내용 | 수정된 댓글 반환 |
| 댓글 삭제 | commentId=123 | 204 No Content |
| 존재하지 않는 댓글 삭제 | commentId=9999 | 404 Not Found |

**curl 예시 - 인라인 댓글 생성**

```bash
curl -X POST "http://localhost:8080/v1/merge-requests/550e8400-e29b-41d4-a716-446655440000/42/comments" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "myorg",
    "repository": "myrepo",
    "body": "이 부분은 null 체크가 필요합니다.",
    "path": "src/main/java/Service.java",
    "line": 87
  }'
```

**curl 예시 - 댓글 삭제**

```bash
curl -X DELETE "http://localhost:8080/v1/merge-requests/550e8400-e29b-41d4-a716-446655440000/42/comments/123?namespace=myorg&repository=myrepo"
```

---

## 에지 케이스

| 케이스 | 입력 | 기대 동작 |
|--------|------|-----------|
| 크로스 Provider MR 생성 불가 | GitHub 연결로 GitLab 저장소 MR 생성 | Provider 불일치로 에러 반환 |
| Draft→OPEN 전환 (GitLab) | draft=false, GitLab 연결 | 타이틀에서 "Draft: " 접두사 자동 제거 확인 |
| 머지 충돌 발생 MR | 소스/타겟 브랜치 충돌 | mergeable=false 반환, MergeMergeRequest 시 422 반환 |
| Bitbucket SQUASH 머지 시도 | mergeMethod=SQUASH, Bitbucket 연결 | 501 Not Implemented 반환 |
| 빈 제목으로 MR 생성 | title="" | 400 Bad Request |
| number 0 또는 음수 | number=0 | 400 Bad Request |
| CLOSED MR 머지 시도 | CLOSED 상태 MR에 MergeMergeRequest | 409 Conflict 또는 422 반환 |
| 리뷰어 없는 MR APPROVED | 리뷰어 미지정 MR | Provider 정책에 따라 처리 (에러 없음) |
| 대용량 Diff 조회 | 파일 1,000개 변경 MR | 전체 반환 또는 페이지네이션 필요 확인 |
| Bitbucket UpdateComment | go-bitbucket v0.9.88 미만 환경 | 501 Not Implemented (라이브러리 버전 의존) |
