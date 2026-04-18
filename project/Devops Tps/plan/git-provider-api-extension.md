# Git Provider API 확장 계획

## 개요
GitHub 스타일의 Git Provider 관리 웹 구현을 위한 API 확장 계획

---

## 현재 API 현황

### git-provider (Go) - 구현 완료

| 카테고리 | API | 설명 |
|---------|-----|------|
| Provider | RegisterProvider | 프로바이더 등록 |
| Provider | GetProvider | 프로바이더 조회 |
| Provider | ListProviders | 프로바이더 목록 |
| Provider | DeleteProvider | 프로바이더 삭제 |
| Repository | ListRepositories | 저장소 목록 |
| Repository | GetRepository | 저장소 상세 (clone_url 포함) |
| Repository | CreateRepository | 저장소 생성 |
| Repository | DeleteRepository | 저장소 삭제 |
| Branch | ListBranches | 브랜치 목록 |
| Branch | GetBranch | 브랜치 상세 |
| Branch | CreateBranch | 브랜치 생성 |
| Branch | DeleteBranch | 브랜치 삭제 |

### tps-api (Java) - 구현 완료

| 카테고리 | API | 설명 |
|---------|-----|------|
| Connection | CRUD + activate/deactivate/test | DB 저장 |
| Repository | CRUD + sync | DB 저장 |
| Branch | CRUD + status/commit update | DB 저장 |

---

## 추가 필요 API

### 1. GetContents (필수)
**목적**: 저장소 내 파일/디렉토리 내용 조회

```
REST: POST /v1/contents
gRPC: GitService.GetContents()

요청:
  - provider: ProviderConfig
  - namespace: string (owner/org)
  - repository: string
  - path: string (기본값: "" = root)
  - ref: string (branch/tag/commit, 기본값: default_branch)

응답 (디렉토리):
  - type: DIRECTORY
  - name: string
  - path: string
  - entries: [
      { type: FILE, name: "README.md", path: "README.md", size: 1234, sha: "abc123" },
      { type: DIRECTORY, name: "src", path: "src", sha: "def456" }
    ]

응답 (파일):
  - type: FILE
  - name: string
  - path: string
  - size: int64
  - content: string (base64 인코딩)
  - encoding: "base64"
  - sha: string
```

**각 Provider API 매핑**:

| Provider | API Endpoint |
|----------|--------------|
| GitHub | GET /repos/OWNER/REPO/contents/PATH |
| GitLab (파일) | GET /projects/ID/repository/files/PATH |
| GitLab (디렉토리) | GET /projects/ID/repository/tree |
| Bitbucket | GET /repositories/WORKSPACE/REPO/src/COMMIT/PATH |

---

### 2. GetTree (권장)
**목적**: 전체 파일 트리 한번에 조회 (성능 최적화)

```
REST: POST /v1/tree
gRPC: GitService.GetTree()

요청:
  - provider: ProviderConfig
  - namespace: string
  - repository: string
  - ref: string
  - recursive: bool (기본값: true)

응답:
  - sha: string
  - truncated: bool (100K 이상 파일시 true)
  - entries: [
      { path: "src/main.go", type: "blob", size: 2345, sha: "abc" },
      { path: "src/utils", type: "tree", sha: "def" }
    ]
```

**각 Provider API 매핑**:

| Provider | API Endpoint |
|----------|--------------|
| GitHub | GET /repos/OWNER/REPO/git/trees/SHA?recursive=1 |
| GitLab | GET /projects/ID/repository/tree?recursive=true |
| Bitbucket | GET /repositories/WORKSPACE/REPO/src/COMMIT/?max_depth=10 |

---

### 3. SearchFiles (선택)
**목적**: 파일명/경로로 검색 ("Go to file" 기능)

```
REST: POST /v1/files/search
gRPC: GitService.SearchFiles()

요청:
  - provider: ProviderConfig
  - namespace: string
  - repository: string
  - query: string
  - ref: string (optional)

응답:
  - files: [
      { path: "src/main.go", name: "main.go" },
      { path: "cmd/server/main.go", name: "main.go" }
    ]
```

**구현 방식**: GetTree 결과를 클라이언트 또는 서버에서 필터링

---

## 구현 작업 목록

### Phase 1: Proto 정의 (git-provider)

**파일**: `api/proto/v1/provider.proto`

```protobuf
// 추가할 메시지 정의
enum ContentType {
  CONTENT_TYPE_UNSPECIFIED = 0;
  CONTENT_TYPE_FILE = 1;
  CONTENT_TYPE_DIRECTORY = 2;
  CONTENT_TYPE_SYMLINK = 3;
  CONTENT_TYPE_SUBMODULE = 4;
}

message ContentEntry {
  ContentType type = 1;
  string name = 2;
  string path = 3;
  int64 size = 4;
  string sha = 5;
}

message GetContentsRequest {
  ProviderConfig provider = 1;
  string namespace = 2;
  string repository = 3;
  string path = 4;
  string ref = 5;
}

message GetContentsResponse {
  ContentType type = 1;
  string name = 2;
  string path = 3;
  int64 size = 4;
  string content = 5;
  string encoding = 6;
  string sha = 7;
  repeated ContentEntry entries = 8;
}

message TreeEntry {
  string path = 1;
  string type = 2;  // "blob" or "tree"
  string sha = 3;
  int64 size = 4;
  string mode = 5;
}

message GetTreeRequest {
  ProviderConfig provider = 1;
  string namespace = 2;
  string repository = 3;
  string ref = 4;
  bool recursive = 5;
}

message GetTreeResponse {
  string sha = 1;
  repeated TreeEntry entries = 2;
  bool truncated = 3;
}

// GitService에 추가
service GitService {
  // 기존 메서드들 ...

  rpc GetContents(GetContentsRequest) returns (GetContentsResponse) {
    option (google.api.http) = {
      post: "/v1/contents"
      body: "*"
    };
  }

  rpc GetTree(GetTreeRequest) returns (GetTreeResponse) {
    option (google.api.http) = {
      post: "/v1/tree"
      body: "*"
    };
  }
}
```

---

### Phase 2: Client 구현 (git-provider)

**파일별 작업**:

#### internal/client/github.go
```go
// 추가할 메서드
func (c *GitHubClient) GetContents(ctx context.Context, owner, repo, path, ref string) (*ContentResult, error)
func (c *GitHubClient) GetTree(ctx context.Context, owner, repo, ref string, recursive bool) (*TreeResult, error)
```

#### internal/client/gitlab.go
```go
// 추가할 메서드
func (c *GitLabClient) GetContents(ctx context.Context, projectID, path, ref string) (*ContentResult, error)
func (c *GitLabClient) GetTree(ctx context.Context, projectID, ref string, recursive bool) (*TreeResult, error)
```

#### internal/client/bitbucket.go
```go
// 추가할 메서드
func (c *BitbucketClient) GetContents(ctx context.Context, workspace, repo, path, ref string) (*ContentResult, error)
func (c *BitbucketClient) GetTree(ctx context.Context, workspace, repo, ref string, recursive bool) (*TreeResult, error)
```

---

### Phase 3: Server 구현 (git-provider)

**파일**: `internal/server/git_server.go`

```go
// 추가할 메서드
func (s *GitServer) GetContents(ctx context.Context, req *pb.GetContentsRequest) (*pb.GetContentsResponse, error) {
    // 1. Provider 타입 판별
    // 2. 해당 Client 생성
    // 3. GetContents 호출
    // 4. 응답 변환
}

func (s *GitServer) GetTree(ctx context.Context, req *pb.GetTreeRequest) (*pb.GetTreeResponse, error) {
    // 1. Provider 타입 판별
    // 2. 해당 Client 생성
    // 3. GetTree 호출
    // 4. 응답 변환
}
```

---

### Phase 4: 테스트

**REST API 테스트**:
```bash
curl -X POST http://localhost:8080/v1/contents \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": { "github": { "token": "ghp_xxx" } },
    "namespace": "octocat",
    "repository": "Hello-World",
    "path": "",
    "ref": "main"
  }'
```

**gRPC 테스트**:
```bash
grpcurl -plaintext -d '{
  "provider": { "github": { "token": "ghp_xxx" } },
  "namespace": "octocat",
  "repository": "Hello-World",
  "path": "src",
  "ref": "main"
}' localhost:50051 gitprovider.v1.GitService/GetContents
```

---

## Provider별 특이사항

### GitHub
- contents API가 디렉토리/파일 모두 처리
- 대용량 파일은 blob API 사용 필요 (100KB 초과)
- Tree API는 SHA 필요 (ref에서 commit, tree SHA 순으로 조회)

### GitLab
- 파일 조회와 디렉토리 조회가 별도 API
- 파일 경로는 URL 인코딩 필요 (슬래시를 %2F로)
- type 판별 로직 필요

### Bitbucket
- src API가 디렉토리/파일 모두 처리
- 페이지네이션 처리 필요
- commit SHA 또는 branch name 사용 가능

---

## 일정 추정

| Phase | 작업 | 예상 시간 |
|-------|-----|----------|
| 1 | Proto 정의 + 코드 생성 | 1시간 |
| 2 | GitHub Client 구현 | 2시간 |
| 2 | GitLab Client 구현 | 2시간 |
| 2 | Bitbucket Client 구현 | 2시간 |
| 3 | Server 메서드 구현 | 1시간 |
| 4 | 테스트 및 디버깅 | 2시간 |
| 합계 | - | 10시간 |

---

## 향후 확장 가능 API

| API | 설명 | 우선순위 |
|-----|------|---------|
| GetCommit | 특정 커밋 상세 정보 | 낮음 |
| ListCommits | 커밋 히스토리 | 중간 |
| GetBlame | 파일 blame 정보 | 낮음 |
| CompareCommits | 커밋 비교 | 낮음 |
| GetReadme | README 자동 조회 | GetContents로 대체 |
