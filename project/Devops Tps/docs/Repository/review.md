# Repository 구현 리뷰

## What - 무엇을 구현했는가

GitService는 GitHub, GitLab, Bitbucket 세 프로바이더의 저장소와 브랜치 CRUD를 통합 인터페이스로 추상화하는 gRPC 서비스다. `git_server.go`(330줄)에 구현되어 있으며, 실제 API 호출은 `internal/client/` 패키지의 세 클라이언트 파일(github.go 1,140줄, gitlab.go 960줄, bitbucket.go 1,248줄)에 위임한다.

| RPC 그룹 | 메서드 | 클라이언트 위임 |
|---------|--------|----------------|
| Repository | ListRepositories, GetRepository, CreateRepository, DeleteRepository | 프로바이더별 client |
| Branch | ListBranches, GetBranch, CreateBranch, DeleteBranch | 프로바이더별 client |

클라이언트는 Provider REST API를 호출하고 결과를 `*pb.Repository`, `*pb.Branch` proto 메시지로 변환한다. 서버 계층에는 별도 변환 함수가 없으며, 변환 책임 전체를 클라이언트 계층이 진다.

---

## How - 어떻게 구현했는가

### 코드 구조

```
git-provider/internal/
├── client/
│   ├── github.go      # GitHubClient (1,140줄)
│   ├── gitlab.go      # GitLabClient (960줄)
│   └── bitbucket.go   # BitbucketClient (1,248줄)
└── server/
    ├── git_server.go       # GitService 구현 (330줄)
    └── client_factory.go   # 3개 팩토리 함수
```

### Provider Dispatch 패턴

`git_server.go`의 모든 RPC 핸들러는 동일한 구조를 따른다. 요청의 `provider` 필드를 type switch로 분기하여 적절한 클라이언트를 생성하고, 클라이언트 메서드를 호출한 뒤 결과를 그대로 반환한다.

```go
func (s *GitServer) CreateRepository(
    ctx context.Context,
    req *pb.CreateRepositoryRequest,
) (*pb.CreateRepositoryResponse, error) {
    switch config := req.Provider.Config.(type) {
    case *pb.ProviderConfig_Github:
        client, err := createGitHubClient(ctx, config.Github)
        if err != nil {
            return nil, status.Errorf(codes.Internal, "...")
        }
        return client.CreateRepository(ctx, req)
    case *pb.ProviderConfig_Gitlab:
        client, err := createGitLabClient(config.Gitlab)
        // ...
    case *pb.ProviderConfig_Bitbucket:
        client, err := createBitbucketClient(config.Bitbucket)
        // ...
    default:
        return nil, status.Error(codes.InvalidArgument, "provider required")
    }
}
```

### 입력 검증

| 필드 | GitHub | GitLab | Bitbucket |
|------|--------|--------|-----------|
| `provider` | 항상 필수 | 항상 필수 | 항상 필수 |
| `namespace` | owner로 필수 | namespace/repo 경로로 결합 | Config의 workspace 사용 |
| `repository` | 필수 | 필수 | 필수 |

`namespace` 처리 방식이 프로바이더마다 다르다. GitHub는 `owner/repo` 분리 체계이므로 서버에서 namespace를 owner로 직접 전달한다. GitLab은 `namespace/repository`를 서버에서 결합하여 URL-encoded path로 변환한다. Bitbucket은 namespace를 사용하지 않고 `ProviderConfig.workspace`에서 가져온다. 이 차이는 서버 계층이 아닌 각 클라이언트 내부에서 흡수된다.

### 프로바이더별 ListRepositories 구현

| Provider | Go 호출 | 비고 |
|----------|--------|------|
| GitHub | `client.Repositories.List(ctx, "", opts)` | 인증 사용자의 모든 저장소 |
| GitLab | `client.Projects.ListProjects(&ListProjectsOptions{Owned: &owned})` | 소유한 프로젝트만 |
| Bitbucket | `client.Repositories.ListForAccount(&RepositoriesOptions{Owner: workspace})` | workspace 기준 |

### 프로바이더별 CreateBranch 구현

세 프로바이더 모두 `ref`(소스 커밋 또는 브랜치명)를 기반으로 새 브랜치를 생성하지만, API 방식이 다르다.

| Provider | API | ref 형식 |
|----------|-----|---------|
| GitHub | Git References API (`POST /git/refs`) | `refs/heads/branch-name` + SHA 필수 |
| GitLab | Branch API (`POST /repository/branches`) | 브랜치명 또는 SHA 모두 가능 |
| Bitbucket | Branch API (`POST /refs/branches`) | 커밋 SHA 40자 필수 |

GitHub와 Bitbucket은 브랜치명 ref 대신 커밋 SHA가 필요하다. 따라서 브랜치명으로 생성하려면 먼저 GetBranch를 호출하여 SHA를 얻어야 한다.

### 응답 변환 구조

클라이언트가 `*pb.Repository`와 `*pb.Branch`를 직접 생성하여 반환한다. MergeRequestService는 내부 타입(MergeRequestInfo)을 거쳐 proto로 변환하는 반면, GitService는 중간 타입 없이 클라이언트가 proto를 바로 생성한다.

```go
// github.go - convertRepository()
func convertRepository(repo *github.Repository) *pb.Repository {
    return &pb.Repository{
        Id:            fmt.Sprintf("%d", repo.GetID()),
        Name:          repo.GetName(),
        FullName:      repo.GetFullName(),
        Url:           repo.GetHTMLURL(),
        CloneUrl:      repo.GetCloneURL(),
        SshUrl:        repo.GetSSHURL(),
        DefaultBranch: repo.GetDefaultBranch(),
        Private:       repo.GetPrivate(),
        Namespace:     convertNamespace(repo.GetOwner()),
    }
}
```

---

## Why - 왜 이렇게 구현했는가

### Adapter 패턴으로 Provider 차이 흡수

세 프로바이더는 인증 방식, API 구조, 응답 포맷이 모두 다르다. 서버 계층에서 이 차이를 직접 다루면 각 RPC 핸들러마다 프로바이더별 조건 분기가 폭발적으로 늘어난다. Adapter 패턴으로 차이를 `internal/client/` 계층에서 흡수하면 서버 계층은 통합 타입만 다루면 된다.

### Stateless 설계로 수평 확장

인증 정보(`ProviderConfig`)를 요청마다 전달받으므로 서버가 세션이나 상태를 관리할 필요가 없다. 모든 인스턴스가 동일하게 처리할 수 있어 수평 확장이 용이하다. 매 요청마다 클라이언트 객체를 생성하는 오버헤드가 단점이며, 향후 Provider+Token 기준 커넥션 풀이 개선 대상이다.

### 클라이언트가 직접 proto 생성

GitService의 클라이언트는 중간 타입 없이 proto를 직접 생성한다. 이는 Repository/Branch 모델이 단순하여 중간 타입이 불필요하기 때문이다. 반면 MergeRequestInfo처럼 복잡한 도메인은 중간 타입을 도입하여 비즈니스 로직을 분리한다.

### 기능 매트릭스

| 기능 | GitHub | GitLab | Bitbucket |
|------|--------|--------|-----------|
| Repository CRUD | 완료 | 완료 | 완료 |
| Branch CRUD | 완료 | 완료 | 완료 |
| Branch Compare | 완료 (1회 호출) | 완료 (2회 호출) | 완료 (diffstat) |
| Stale Branch 탐지 | 완료 | 완료 | 완료 |
| File Tree | 완료 (truncated 지원) | 완료 (페이지네이션) | 완료 (재귀 헬퍼) |
| Enterprise / Self-hosted | GitHub Enterprise 지원 | Self-hosted 지원 | Cloud만 지원 |

### Provider별 특이사항

**GitHub**: REST API가 풍부하고 `go-github` 라이브러리가 잘 정리되어 있어 구현 완성도가 가장 높다. Enterprise Server는 `baseURL` 파라미터로 지원한다.

**GitLab**: `CompareBranches`에서 ahead/behind를 구하기 위해 정방향/역방향 2회 API 호출이 필요하다. 프로젝트 경로에 슬래시가 포함되므로 URL encoding이 필수다.

**Bitbucket**: `go-bitbucket` 라이브러리가 `interface{}` 반환이 많아 런타임 타입 단언 코드가 빈번하다. 브랜치 생성 시 커밋 SHA 40자 전체가 필요하므로, 브랜치명으로 생성하려면 선행 API 호출이 필요하다.

---

## 참고 패턴

| 패턴 | 적용 위치 | 설명 |
|------|----------|------|
| Adapter | `internal/client/` | Provider별 API 차이를 proto로 변환 |
| Factory | `client_factory.go` | ProviderConfig에 따라 적절한 클라이언트 생성 |
| Type Switch | `git_server.go` | oneof 필드로 런타임 다형성 구현 |
| Stateless | 서버 전체 | 요청마다 인증 정보 수신, 서버 상태 없음 |

---

## 개선 가능 사항

1. **페이지네이션 미지원**: `ListRepositories`, `ListBranches`에 page/perPage 파라미터가 없어 대규모 저장소에서 성능 이슈 발생 가능. pagelen 파라미터를 추가하고 cursor 기반 페이지네이션을 구현해야 한다.

2. **에러 세분화 부족**: 현재 대부분의 에러가 `codes.Internal`로 반환된다. 404는 `codes.NotFound`, 403은 `codes.PermissionDenied`, 409는 `codes.AlreadyExists`로 세분화하면 클라이언트 처리가 용이해진다.

3. **Repository와 Branch가 같은 서비스**: GitService가 저장소와 브랜치 두 도메인을 함께 관리한다. 브랜치 관련 RPC를 BranchService로 분리하면 단일 책임 원칙에 부합한다.

4. **커넥션 풀 부재**: 매 요청마다 클라이언트를 생성한다. Provider+Token 조합으로 클라이언트를 캐싱하면 HTTP 연결 재사용으로 성능이 향상된다.

5. **Bitbucket 브랜치 생성**: 브랜치명 기반 생성 시 SHA 조회를 위한 추가 API 호출이 필요하다. 내부적으로 GetBranch를 먼저 호출하여 SHA를 얻는 로직이 클라이언트에 숨겨져 있다.

---

## 관련 문서

- [Repository API 설계](./api-design.md)
- [Repository 유스케이스 모델](./usecase-model.md)
- [Provider 구현 리뷰](../Provider/review.md)
- [GitHub API 레퍼런스](../Provider/GitHub/api-reference.md)
- [GitLab API 레퍼런스](../Provider/GitLab/api-reference.md)
- [Bitbucket API 레퍼런스](../Provider/Bitbucket/api-reference.md)
