# GitLab API 레퍼런스

## 개요

GitLab REST API v4를 사용한다. gitlab.com 및 Self-hosted GitLab 인스턴스를 모두 지원한다. Go 클라이언트 라이브러리는 `github.com/xanzy/go-gitlab`(v115)을 사용한다.

GitLab에서는 저장소를 **Project**라고 부른다. 계층 구조는 User/Group/Subgroup/Project이며, 중첩 그룹을 최대 20단계까지 지원한다.

---

## 인증

### Personal Access Token (PAT)

```bash
# Header 방식 (권장)
PRIVATE-TOKEN: glpat-xxxxxxxxxxxxxxxxxxxx

# 또는 OAuth2 Bearer
Authorization: Bearer glpat-xxxxxxxxxxxxxxxxxxxx
```

### 필요 권한 (Scopes)

| Scope | 설명 | 필요 기능 |
|-------|------|----------|
| `api` | 전체 API 접근 | 모든 기능 |
| `read_api` | 읽기 전용 | Contents, Branch Comparison |
| `read_repository` | 저장소 읽기 | Contents |
| `write_repository` | 저장소 쓰기 | Branch 생성/삭제 |

### Self-hosted GitLab

```go
config := &GitLabConfig{
    Token:   "glpat-xxx",
    BaseURL: "https://gitlab.company.com",
}
// BaseURL이 있으면 /api/v4 를 자동으로 붙여서 사용
```

### Rate Limit

| 유형 | 제한 |
|------|------|
| 인증 요청 | 2,000 req/min |
| 비인증 요청 | 500 req/min |

```
RateLimit-Limit: 2000
RateLimit-Remaining: 1999
RateLimit-Reset: 1609459200
```

---

## 프로젝트(저장소) API

### 프로젝트 식별 방식

GitLab은 프로젝트를 숫자 ID 또는 URL-encoded 경로로 식별한다.

```
# 숫자 ID
GET /projects/123

# URL 인코딩된 경로 (슬래시를 %2F로 인코딩)
GET /projects/group%2Fsubgroup%2Fproject
```

```go
// Go에서 경로 인코딩
func encodeProjectPath(owner, repo string) string {
    path := owner + "/" + repo
    return url.PathEscape(path)  // "group%2Fproject"
}
```

### 프로젝트 목록 조회

```
GET /projects                      # 인증된 사용자의 프로젝트
GET /groups/{id}/projects          # 그룹의 프로젝트
GET /users/{id}/projects           # 특정 사용자의 프로젝트
```

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| owned | boolean | 소유한 프로젝트만 (기본: false) |
| membership | boolean | 멤버인 프로젝트만 |
| visibility | string | `public`, `internal`, `private` |
| per_page | int | 최대 100, 기본 20 |

### 프로젝트 상세 조회

```
GET /projects/{id}
```

### 프로젝트 생성

```
POST /projects
```

```json
{
  "name": "hello-world",
  "namespace_id": 123,
  "description": "My first project",
  "visibility": "private",
  "initialize_with_readme": true
}
```

| 필드 | 타입 | 필수 | 설명 |
|-----|------|------|------|
| name | string | O | 프로젝트 이름 |
| namespace_id | int | X | 그룹 ID (미지정 시 개인 네임스페이스) |
| visibility | string | X | `private`, `internal`, `public` |
| initialize_with_readme | boolean | X | README 자동 생성 |

### 프로젝트 삭제

```
DELETE /projects/{id}
```

---

## 브랜치 API

### 브랜치 목록 조회

```
GET /projects/{id}/repository/branches
```

| 파라미터 | 설명 |
|---------|------|
| search | 브랜치 이름 검색 |
| per_page | 페이지당 결과 수 |

### 브랜치 생성

```
POST /projects/{id}/repository/branches
```

```json
{
  "branch": "feature-branch",
  "ref": "main"
}
```

GitHub와 달리 브랜치명을 직접 지정하고, ref는 브랜치명 또는 커밋 SHA 모두 사용 가능하다.

### 브랜치 삭제

```
DELETE /projects/{id}/repository/branches/{branch}
```

---

## MR API

### MR 목록 조회

```
GET /projects/{id}/merge_requests
```

| 파라미터 | 설명 |
|---------|------|
| state | `opened`, `closed`, `merged`, `all` |
| source_branch | 소스 브랜치 필터 |
| target_branch | 타겟 브랜치 필터 |

### MR 생성

```
POST /projects/{id}/merge_requests
```

```json
{
  "source_branch": "feature-branch",
  "target_branch": "main",
  "title": "MR 제목",
  "description": "MR 설명",
  "remove_source_branch": true
}
```

### MR 머지

```
PUT /projects/{id}/merge_requests/{merge_request_iid}/merge
```

```json
{
  "merge_commit_message": "머지 커밋 메시지",
  "squash": false,
  "should_remove_source_branch": true
}
```

### 승인 (Approvals)

```
POST /projects/{id}/merge_requests/{iid}/approve     # 승인
POST /projects/{id}/merge_requests/{iid}/unapprove   # 승인 취소
GET  /projects/{id}/merge_requests/{iid}/approvals   # 승인 상태
```

GitLab은 정식 Review API 대신 Approval API를 제공한다. `SubmitReview(state=APPROVED)`는 `ApproveMergeRequest()`를 호출하고, 그 외는 일반 Note를 생성한다.

---

## 브랜치 비교

```
GET /projects/{id}/repository/compare
```

| 파라미터 | 설명 |
|---------|------|
| from | base 브랜치 |
| to | compare 브랜치 |
| straight | true: from...to, false: merge-base |

GitLab compare API는 `behind_by`를 직접 제공하지 않는다. 따라서 정방향/역방향 2회 호출로 계산한다.

```go
// ahead 계산: head가 base보다 얼마나 앞서 있는가
compareAhead, _ := client.Repositories.Compare(pid, &gitlab.CompareOptions{
    From: gitlab.String(base),
    To:   gitlab.String(head),
})
aheadBy := len(compareAhead.Commits)

// behind 계산: head가 base보다 얼마나 뒤처져 있는가
compareBehind, _ := client.Repositories.Compare(pid, &gitlab.CompareOptions{
    From: gitlab.String(head),
    To:   gitlab.String(base),
})
behindBy := len(compareBehind.Commits)
```

---

## 통합 모델 매핑

### Project → 통합 Repository 모델

| GitLab 필드 | 통합 모델 필드 | 변환 로직 |
|------------|--------------|----------|
| `id` | `id` | `fmt.Sprintf("%d", id)` |
| `name` | `name` | 그대로 |
| `path_with_namespace` | `full_name` | 그대로 |
| `web_url` | `url` | 그대로 |
| `http_url_to_repo` | `clone_url` | 그대로 |
| `ssh_url_to_repo` | `ssh_url` | 그대로 |
| `default_branch` | `default_branch` | 그대로 |
| `visibility` | `private` | `visibility != "public"` |
| `namespace.name` | `namespace.name` | 그대로 |
| `namespace.kind` | `namespace.type` | user→USER, group→GROUP |

### MR 상태 매핑

| GitLab state | 통합 MergeRequestStatus |
|--------------|------------------------|
| `opened` | OPEN |
| `closed` | CLOSED |
| `merged` | MERGED |

### merge_status 매핑

| GitLab merge_status | MergeableState |
|--------------------|----------------|
| `can_be_merged` | MERGEABLE |
| `cannot_be_merged` | CONFLICTING |
| `unchecked`, `checking` | UNKNOWN |

---

## 계층 구조

```
User
├── Project (직접 소유)
└── Group (소속)
    ├── Project
    └── Subgroup (최대 20단계)
        └── Project
```

### Namespace 종류

| kind | 설명 |
|------|------|
| `user` | 개인 사용자 네임스페이스 |
| `group` | 그룹 네임스페이스 |

---

## Go 클라이언트 주요 메서드

```go
// 프로젝트 목록 (소유한 것만)
owned := true
client.Projects.ListProjects(&gitlab.ListProjectsOptions{Owned: &owned})

// 프로젝트 생성
client.Projects.CreateProject(&gitlab.CreateProjectOptions{
    Name:       gitlab.Ptr("name"),
    Visibility: gitlab.Ptr(gitlab.PrivateVisibility),
})

// 브랜치 생성
client.Branches.CreateBranch(projectID, &gitlab.CreateBranchOptions{
    Branch: gitlab.Ptr("new-branch"),
    Ref:    gitlab.Ptr("main"),
})

// MR 생성
client.MergeRequests.CreateMergeRequest(projectID, &gitlab.CreateMergeRequestOptions{
    SourceBranch: gitlab.Ptr("feature"),
    TargetBranch: gitlab.Ptr("main"),
    Title:        gitlab.Ptr("제목"),
})
```

---

## 에러 처리

```json
{
  "message": "404 Project Not Found",
  "error": "Not Found"
}
```

| HTTP Status | GitLab 메시지 | gRPC 코드 |
|-------------|--------------|----------|
| 401 | "401 Unauthorized" | UNAUTHENTICATED |
| 403 | "403 Forbidden" | PERMISSION_DENIED |
| 404 | "404 Project Not Found" | NOT_FOUND |
| 409 | "Branch already exists" | ALREADY_EXISTS |

---

## 알려진 제한사항

1. **Tree API 크기 미제공**: 파일 크기는 별도 API 호출 필요
2. **Merge 가능 여부**: MR 생성 전에는 확인 불가 (UNKNOWN 반환)
3. **behindBy 계산**: 별도 compare API 호출 2회 필요
4. **페이지네이션**: 대부분 API가 100개 제한
5. **프로젝트 경로 인코딩**: 특수문자 및 슬래시 인코딩 필수

---

## 관련 문서

- [GitLab REST API 공식 문서](https://docs.gitlab.com/ee/api/)
- [go-gitlab 라이브러리](https://github.com/xanzy/go-gitlab)
- [Provider/comparison.md](../../repo/provider/comparison.md) - Provider 비교 분석
