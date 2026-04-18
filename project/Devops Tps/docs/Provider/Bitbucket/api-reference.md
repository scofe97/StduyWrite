# Bitbucket API 레퍼런스

## 개요

Bitbucket Cloud REST API 2.0을 사용한다. Bitbucket은 GitHub/GitLab과 달리 **Workspace** 기반 구조를 사용하며, 모든 저장소 작업에 Workspace가 필수다. Go 클라이언트 라이브러리는 `github.com/ktrysmt/go-bitbucket`(v0.9.88)을 사용한다.

현재 구현은 Bitbucket Cloud만 지원한다. Bitbucket Server(Data Center)는 별도 API(`/rest/api/1.0/`)를 사용하므로 지원하지 않는다.

---

## 인증

### App Password (권장)

```bash
# Basic Auth (email:app_password를 base64 인코딩)
Authorization: Basic base64(email@example.com:app_password)

# curl 사용 시
curl -u "email@example.com:app_password" https://api.bitbucket.org/2.0/...
```

### App Password 생성

1. Bitbucket → Personal settings → App passwords → Create app password
2. 필요 권한: `Repositories: Read/Write`, `Account: Read`

### Rate Limit

| 유형 | 제한 |
|------|------|
| 인증 요청 | 1,000 req/hour |
| 워크스페이스 공유 | 전체 워크스페이스 합산 |

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
```

---

## 계층 구조

Bitbucket은 GitHub/GitLab과 다른 계층 구조를 사용한다.

```
Workspace (필수)
├── Repository (직접)
└── Project (선택적 그룹핑)
    └── Repository
```

GitHub/GitLab과 비교:
```
GitHub:     owner/repo
GitLab:     group/subgroup/project
Bitbucket:  workspace/repo  (workspace 필수)
```

---

## 저장소 API

### 저장소 목록 조회

```
GET /2.0/repositories/{workspace}    # workspace의 저장소
GET /2.0/repositories                # 인증된 사용자의 전체 저장소
```

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| workspace | string | Workspace slug 또는 UUID |
| role | string | `admin`, `contributor`, `member`, `owner` |
| q | string | 필터 쿼리 (예: `name ~ "test"`) |
| pagelen | int | 최대 100, 기본 10 |

### 저장소 상세 조회

```
GET /2.0/repositories/{workspace}/{repo_slug}
```

### 저장소 생성

```
POST /2.0/repositories/{workspace}/{repo_slug}
```

```json
{
  "scm": "git",
  "is_private": true,
  "description": "My repository",
  "mainbranch": {
    "type": "branch",
    "name": "main"
  }
}
```

| 필드 | 타입 | 필수 | 설명 |
|-----|------|------|------|
| scm | string | X | `git` (기본값) |
| is_private | boolean | X | 비공개 여부 (기본: true) |
| description | string | X | 설명 |
| mainbranch.name | string | X | 기본 브랜치명 |
| project.key | string | X | 프로젝트 키 (그룹핑용, 선택) |

### 저장소 삭제

```
DELETE /2.0/repositories/{workspace}/{repo_slug}
```

---

## 브랜치 API

### 브랜치 목록 조회

```
GET /2.0/repositories/{workspace}/{repo_slug}/refs/branches
```

### 브랜치 생성

```
POST /2.0/repositories/{workspace}/{repo_slug}/refs/branches
```

```json
{
  "name": "feature-branch",
  "target": {
    "hash": "c5b97d5ae6c19d5c5df71a34c7fbeeda2479ccbc"
  }
}
```

Bitbucket은 브랜치 생성 시 커밋 SHA 전체 40자가 필요하다. GitHub처럼 브랜치명을 ref로 사용하는 방식과 다르다.

### 브랜치 삭제

```
DELETE /2.0/repositories/{workspace}/{repo_slug}/refs/branches/{name}
```

---

## PR API

### PR 목록 조회

```
GET /2.0/repositories/{workspace}/{repo_slug}/pullrequests
```

| 파라미터 | 설명 |
|---------|------|
| state | `OPEN`, `MERGED`, `DECLINED`, `SUPERSEDED` |
| pagelen | 최대 50, 기본 10 |

### PR 생성

```
POST /2.0/repositories/{workspace}/{repo_slug}/pullrequests
```

```json
{
  "title": "PR 제목",
  "description": "PR 설명",
  "source": {
    "branch": { "name": "feature-branch" }
  },
  "destination": {
    "branch": { "name": "main" }
  },
  "close_source_branch": true
}
```

### PR 머지

```
POST /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{id}/merge
```

```json
{
  "message": "머지 커밋 메시지",
  "close_source_branch": true,
  "merge_strategy": "merge_commit"
}
```

| merge_strategy | 설명 |
|----------------|------|
| `merge_commit` | 머지 커밋 생성 (기본) |
| `squash` | 스쿼시 머지 |
| `fast_forward` | Fast-forward 머지 |

GitHub/GitLab과 달리 `rebase` 머지는 지원하지 않는다.

### PR 거절

```
POST /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{id}/decline
```

### 승인

```
POST   /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{id}/approve    # 승인
DELETE /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{id}/approve    # 승인 취소
```

Bitbucket은 정식 Review API가 없다. Approve/Unapprove만 지원하며, `REQUEST_CHANGES`에 해당하는 기능이 없다.

---

## 브랜치 비교

Bitbucket은 직접적인 compare API가 없다. 커밋 목록 조회로 계산해야 한다.

```
GET /2.0/repositories/{workspace}/{repo_slug}/commits/{revision}?include={head}&exclude={base}
```

```go
// ahead 계산: head에만 있는 커밋
aheadURL := fmt.Sprintf(".../commits/%s?exclude=%s", head, base)
aheadCommits, _ := fetchAllCommits(ctx, aheadURL)

// behind 계산: base에만 있는 커밋
behindURL := fmt.Sprintf(".../commits/%s?exclude=%s", base, head)
behindCommits, _ := fetchAllCommits(ctx, behindURL)

// diff stat
GET /2.0/repositories/{workspace}/{repo_slug}/diffstat/{base}..{head}
```

Mergeable 상태는 PR 생성 전에 확인할 수 없어 항상 UNKNOWN을 반환한다.

---

## 통합 모델 매핑

### Repository → 통합 모델

| Bitbucket 필드 | 통합 모델 필드 | 변환 로직 |
|---------------|--------------|----------|
| `uuid` | `id` | 그대로 |
| `name` | `name` | 그대로 |
| `full_name` | `full_name` | 그대로 |
| `links.html.href` | `url` | 그대로 |
| `links.clone[https]` | `clone_url` | clone 배열에서 https 찾기 |
| `links.clone[ssh]` | `ssh_url` | clone 배열에서 ssh 찾기 |
| `mainbranch.name` | `default_branch` | 그대로 |
| `is_private` | `private` | 그대로 |
| `workspace.slug` | `namespace.name` | 그대로 |
| `"workspace"` | `namespace.type` | 항상 WORKSPACE |

### PR 상태 매핑

| Bitbucket state | 통합 MergeRequestStatus |
|-----------------|------------------------|
| `OPEN` | OPEN |
| `MERGED` | MERGED |
| `DECLINED`, `SUPERSEDED` | CLOSED |

---

## 페이지네이션

Bitbucket은 GitHub/GitLab과 달리 `next` URL 방식을 사용한다. 페이지 번호가 아닌 cursor 기반이다.

```json
{
  "values": [...],
  "pagelen": 10,
  "size": 50,
  "next": "https://api.bitbucket.org/2.0/repositories/ws/repo/refs/branches?page=2"
}
```

```go
// 구현 패턴
for {
    result, _ := fetchPage(url)
    allItems = append(allItems, result.Values...)
    if result.Next == "" {
        break
    }
    url = result.Next  // 다음 페이지 URL 사용
}
```

---

## Links 구조

Bitbucket은 URL을 `links` 객체에 중첩해서 제공한다. Go에서는 `interface{}` 타입 단언이 필요하다.

```go
func extractCloneURL(links map[string]interface{}, protocol string) string {
    if cloneLinks, ok := links["clone"].([]interface{}); ok {
        for _, link := range cloneLinks {
            if linkMap, ok := link.(map[string]interface{}); ok {
                if name, _ := linkMap["name"].(string); name == protocol {
                    href, _ := linkMap["href"].(string)
                    return href
                }
            }
        }
    }
    return ""
}
```

---

## Go 클라이언트 주요 메서드

```go
// 클라이언트 생성
client, _ := bitbucket.NewBasicAuth("email@example.com", "app_password")

// 저장소 목록
repos, _ := client.Repositories.ListForAccount(&bitbucket.RepositoriesOptions{
    Owner: "workspace-slug",
})

// 저장소 생성
repo, _ := client.Repositories.Repository.Create(&bitbucket.RepositoryOptions{
    Owner:       "workspace-slug",
    RepoSlug:    "new-repo",
    IsPrivate:   "true",
    Description: "Description",
})

// 브랜치 생성
branch, _ := client.Repositories.Repository.CreateBranch(&bitbucket.RepositoryBranchCreationOptions{
    Owner:    "workspace-slug",
    RepoSlug: "repo-slug",
    Name:     "new-branch",
    Target:   bitbucket.RepositoryBranchTarget{Hash: "commit-sha"},
})
```

---

## 에러 처리

```json
{
  "type": "error",
  "error": {
    "message": "Repository not found",
    "detail": "..."
  }
}
```

| HTTP Status | Bitbucket 메시지 | gRPC 코드 |
|-------------|-----------------|----------|
| 401 | "Unauthorized" | UNAUTHENTICATED |
| 403 | "Forbidden" | PERMISSION_DENIED |
| 404 | "Repository not found" | NOT_FOUND |
| 400 | "Bad Request" | INVALID_ARGUMENT |

---

## 알려진 제한사항

1. **Compare API 부재**: 커밋 목록으로 직접 계산 필요 → API 호출 2회
2. **Mergeable 상태 불가**: PR 생성 전에는 확인 불가 (UNKNOWN 반환)
3. **Draft PR 미지원**: Bitbucket API에 draft 개념이 없음
4. **인라인 댓글 미지원**: path/line 파라미터 미지원
5. **댓글 수정/삭제**: go-bitbucket 라이브러리 미지원
6. **Raw 파일 내용**: base64 인코딩이 없어 직접 인코딩 필요
7. **Rate Limit 공유**: 워크스페이스 내 모든 사용자 합산
8. **타입 안전성 부족**: 라이브러리가 `interface{}` 반환이 많아 런타임 타입 단언 필요

---

## 관련 문서

- [Bitbucket Cloud REST API 공식 문서](https://developer.atlassian.com/cloud/bitbucket/rest/)
- [go-bitbucket 라이브러리](https://github.com/ktrysmt/go-bitbucket)
- [Provider/comparison.md](../../repo/provider/comparison.md) - Provider 비교 분석
