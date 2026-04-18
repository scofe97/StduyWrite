# GitHub API 레퍼런스

## 개요

GitHub REST API v3(api.github.com)을 사용한다. GitHub Enterprise Server도 `base_url` 파라미터로 지원한다. Go 클라이언트 라이브러리는 `github.com/google/go-github/v57`을 사용한다.

---

## 인증

### Personal Access Token (PAT)

```bash
# Bearer Token 방식
Authorization: Bearer ghp_xxxxxxxxxxxxxxxxxxxx

# 또는 token 방식
Authorization: token ghp_xxxxxxxxxxxxxxxxxxxx
```

### 필요 권한 (Scopes)

| Scope | 설명 | 필요 기능 |
|-------|------|----------|
| `repo` | 저장소 전체 접근 | CRUD, Branch, Contents |
| `read:org` | 조직 정보 읽기 | 조직 저장소 목록 |
| `delete_repo` | 저장소 삭제 | Repository 삭제 |

### Rate Limit

| 유형 | 제한 |
|------|------|
| 인증 요청 | 5,000 req/hour |
| 비인증 요청 | 60 req/hour |
| Secondary | burst 방지 추가 제한 |

```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
X-RateLimit-Reset: 1372700873
```

### GitHub Enterprise

```go
// base_url 지정 시 Enterprise 클라이언트 사용
config := &GitHubConfig{
    Token:   "ghp_xxx",
    BaseURL: "https://github.company.com/api/v3",
}
// NewEnterpriseClient(baseURL, uploadURL, httpClient) 호출
```

---

## 저장소 API

### 저장소 목록 조회

```
GET /user/repos              # 인증된 사용자의 저장소
GET /orgs/{org}/repos        # 조직의 저장소
GET /users/{username}/repos  # 특정 사용자의 저장소
```

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| type | string | `all`, `owner`, `member` (기본: `owner`) |
| sort | string | `created`, `updated`, `pushed`, `full_name` |
| per_page | int | 최대 100, 기본 30 |
| page | int | 페이지 번호 |

### 저장소 상세 조회

```
GET /repos/{owner}/{repo}
```

### 저장소 생성

```
POST /user/repos         # 사용자 저장소
POST /orgs/{org}/repos   # 조직 저장소
```

```json
{
  "name": "hello-world",
  "description": "My first repository",
  "private": true,
  "auto_init": true
}
```

| 필드 | 타입 | 필수 | 설명 |
|-----|------|------|------|
| name | string | O | 저장소 이름 |
| description | string | X | 설명 |
| private | boolean | X | 비공개 여부 (기본: false) |
| auto_init | boolean | X | README 자동 생성 |

### 저장소 삭제

```
DELETE /repos/{owner}/{repo}
```

`delete_repo` 권한이 있는 토큰 필요.

---

## 브랜치 API

### 브랜치 목록 조회

```
GET /repos/{owner}/{repo}/branches
```

| 파라미터 | 설명 |
|---------|------|
| protected | 보호 브랜치만 조회 |
| per_page | 최대 100 |

### 브랜치 생성 (Git Reference API)

```
POST /repos/{owner}/{repo}/git/refs
```

```json
{
  "ref": "refs/heads/feature-branch",
  "sha": "c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc"
}
```

### 브랜치 삭제

```
DELETE /repos/{owner}/{repo}/git/refs/heads/{branch}
```

---

## PR API

### PR 목록 조회

```
GET /repos/{owner}/{repo}/pulls
```

| 파라미터 | 설명 |
|---------|------|
| state | `open`, `closed`, `all` (기본: open) |
| head | `{owner}:{branch}` |
| base | 타겟 브랜치 |
| per_page | 최대 100 |

### PR 생성

```
POST /repos/{owner}/{repo}/pulls
```

```json
{
  "title": "PR 제목",
  "body": "PR 설명",
  "head": "feature-branch",
  "base": "main",
  "draft": false
}
```

### PR 머지

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge
```

```json
{
  "commit_title": "머지 커밋 제목",
  "merge_method": "merge"
}
```

| merge_method | 설명 |
|-------------|------|
| `merge` | 머지 커밋 생성 |
| `squash` | 스쿼시 머지 |
| `rebase` | 리베이스 머지 |

### 리뷰

```
POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
```

```json
{
  "event": "APPROVE",
  "body": "LGTM"
}
```

---

## 브랜치 비교

```
GET /repos/{owner}/{repo}/compare/{base}...{head}
```

**응답 매핑**

| GitHub 필드 | 통합 필드 |
|-------------|---------|
| `ahead_by` | `aheadBy` |
| `behind_by` | `behindBy` |
| `mergeable_state` | `mergeableState` |
| `files[].additions` 합계 | `diffStat.additions` |

**mergeable_state 매핑**

| GitHub 값 | MergeableState |
|-----------|----------------|
| `clean`, `has_hooks`, `unstable` | MERGEABLE |
| `dirty`, `blocked` | CONFLICTING |
| `unknown` | UNKNOWN |

---

## 통합 모델 매핑

### Repository → 통합 모델

| GitHub 필드 | 통합 모델 필드 | 변환 로직 |
|------------|--------------|----------|
| `id` | `id` | `fmt.Sprintf("%d", id)` |
| `name` | `name` | 그대로 |
| `full_name` | `full_name` | 그대로 |
| `html_url` | `url` | 그대로 |
| `clone_url` | `clone_url` | 그대로 |
| `ssh_url` | `ssh_url` | 그대로 |
| `default_branch` | `default_branch` | 그대로 |
| `private` | `private` | 그대로 |
| `owner.login` | `namespace.name` | 그대로 |
| `owner.type` | `namespace.type` | User→USER, Organization→ORGANIZATION |

### Branch → 통합 모델

| GitHub 필드 | 통합 모델 필드 | 변환 로직 |
|------------|--------------|----------|
| `name` | `name` | 그대로 |
| `commit.sha` | `sha` | 그대로 |
| `protected` | `protected` | 그대로 |

---

## Go 클라이언트 주요 메서드

```go
// 저장소 목록
client.Repositories.List(ctx, "", &github.RepositoryListOptions{})

// 저장소 생성
client.Repositories.Create(ctx, "", &github.Repository{Name: github.Ptr("name")})

// 브랜치 생성 (ref 방식)
client.Git.CreateRef(ctx, owner, repo, &github.Reference{
    Ref:    github.Ptr("refs/heads/new-branch"),
    Object: &github.GitObject{SHA: github.Ptr("sha")},
})

// 브랜치 삭제
client.Git.DeleteRef(ctx, owner, repo, "refs/heads/branch-name")

// 브랜치 비교
client.Repositories.CompareCommits(ctx, owner, repo, "main...feature", nil)
```

---

## 에러 처리

| HTTP Status | GitHub 메시지 | gRPC 코드 |
|-------------|--------------|----------|
| 401 | "Bad credentials" | UNAUTHENTICATED |
| 403 | "rate limit exceeded" | RESOURCE_EXHAUSTED |
| 404 | "Not Found" | NOT_FOUND |
| 409 | "Git Repository is empty" | FAILED_PRECONDITION |
| 422 | "Reference does not exist" | NOT_FOUND |

---

## 알려진 제한사항

1. **트리 조회**: recursive=true 시 최대 100,000 엔트리
2. **파일 크기**: Contents API로 1MB 이상 파일 조회 불가 (Blob API 필요)
3. **비교 제한**: 250개 이상 커밋 차이 시 truncated
4. **Secondary Rate Limit**: 짧은 시간 내 많은 요청 시 추가 제한

---

## 관련 문서

- [GitHub REST API 공식 문서](https://docs.github.com/en/rest)
- [go-github 라이브러리](https://github.com/google/go-github)
- [Provider/comparison.md](../../repo/provider/comparison.md) - Provider 비교 분석
