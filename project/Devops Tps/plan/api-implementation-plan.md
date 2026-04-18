# API 구현 계획 - git-provider / tps-api

## 개요

GitHub 스타일 Git Provider 관리 웹 구현을 위한 API 구현 계획

---

## 기능 분류

| 기능 | git-provider (Go) | tps-api (Java) | 비고 |
|------|------------------|----------------|------|
| Provider 관리 | Git Provider 직접 호출 | DB 저장 + git-provider 연동 | |
| Repository CRUD | Git Provider 직접 호출 | DB 저장 + git-provider 연동 | |
| Branch CRUD | Git Provider 직접 호출 | DB 저장 + git-provider 연동 | |
| 파일/트리 조회 | Git Provider 직접 호출 | git-provider 프록시 | |
| Protected Branch | Git Provider 직접 호출 | git-provider 프록시 | |
| Commit 조회 | Git Provider 직접 호출 | git-provider 프록시 | |
| Compare/Diff | Git Provider 직접 호출 | git-provider 프록시 | |
| Merge Request | Git Provider 직접 호출 | DB 저장 + git-provider 연동 | |
| Clone | - | JGit 사용 | git-provider 불필요 |

---

# Part 1: git-provider (Go) 구현 목록

## 현재 구현 완료

| API | 설명 |
|-----|------|
| RegisterProvider | 프로바이더 등록 |
| GetProvider | 프로바이더 조회 |
| ListProviders | 프로바이더 목록 |
| DeleteProvider | 프로바이더 삭제 |
| ListRepositories | 저장소 목록 |
| GetRepository | 저장소 상세 |
| CreateRepository | 저장소 생성 |
| DeleteRepository | 저장소 삭제 |
| ListBranches | 브랜치 목록 |
| GetBranch | 브랜치 상세 |
| CreateBranch | 브랜치 생성 |
| DeleteBranch | 브랜치 삭제 |

---

## 추가 구현 필요

### Phase 1: 파일/트리 조회 (필수)

#### 1.1 GetContents
```
목적: 파일/디렉토리 내용 조회
우선순위: 필수

REST: POST /v1/contents
gRPC: GitService.GetContents()

Provider API:
- GitHub: GET /repos/OWNER/REPO/contents/PATH
- GitLab: GET /projects/ID/repository/files/PATH (파일)
- GitLab: GET /projects/ID/repository/tree (디렉토리)
- Bitbucket: GET /repositories/WORKSPACE/REPO/src/COMMIT/PATH
```

#### 1.2 GetTree
```
목적: 전체 파일 트리 조회
우선순위: 필수

REST: POST /v1/tree
gRPC: GitService.GetTree()

Provider API:
- GitHub: GET /repos/OWNER/REPO/git/trees/SHA?recursive=1
- GitLab: GET /projects/ID/repository/tree?recursive=true
- Bitbucket: GET /repositories/WORKSPACE/REPO/src/COMMIT/?max_depth=10
```

---

### Phase 2: Protected Branch (권장)

#### 2.1 ListProtectedBranches
```
목적: 보호 브랜치 목록 조회
우선순위: 권장

REST: POST /v1/branches/protected/list
gRPC: GitService.ListProtectedBranches()

Provider API:
- GitHub: GET /repos/OWNER/REPO/branches/BRANCH/protection
- GitLab: GET /projects/ID/protected_branches
- Bitbucket: GET /repositories/WORKSPACE/REPO/branch-restrictions
```

#### 2.2 ProtectBranch
```
목적: 브랜치 보호 설정
우선순위: 권장

REST: POST /v1/branches/protect
gRPC: GitService.ProtectBranch()

요청:
- provider: ProviderConfig
- namespace: string
- repository: string
- branch: string
- push_access_level: int32 (30=Developer, 40=Maintainer)
- merge_access_level: int32
- allow_force_push: bool

Provider API:
- GitHub: PUT /repos/OWNER/REPO/branches/BRANCH/protection
- GitLab: POST /projects/ID/protected_branches
- Bitbucket: POST /repositories/WORKSPACE/REPO/branch-restrictions
```

#### 2.3 UnprotectBranch
```
목적: 브랜치 보호 해제
우선순위: 권장

REST: POST /v1/branches/unprotect
gRPC: GitService.UnprotectBranch()

Provider API:
- GitHub: DELETE /repos/OWNER/REPO/branches/BRANCH/protection
- GitLab: DELETE /projects/ID/protected_branches/BRANCH
- Bitbucket: DELETE /repositories/WORKSPACE/REPO/branch-restrictions/ID
```

---

### Phase 3: Commit 조회 (권장)

#### 3.1 ListCommits
```
목적: 커밋 히스토리 조회
우선순위: 권장

REST: POST /v1/commits/list
gRPC: GitService.ListCommits()

요청:
- provider: ProviderConfig
- namespace: string
- repository: string
- ref: string (branch/tag)
- path: string (optional, 특정 파일의 커밋만)
- page: int32
- per_page: int32

응답:
- commits: []Commit
  - sha: string
  - message: string
  - author_name: string
  - author_email: string
  - authored_date: string
  - committer_name: string
  - committer_email: string
  - committed_date: string
  - parent_ids: []string

Provider API:
- GitHub: GET /repos/OWNER/REPO/commits
- GitLab: GET /projects/ID/repository/commits
- Bitbucket: GET /repositories/WORKSPACE/REPO/commits
```

#### 3.2 GetCommit
```
목적: 특정 커밋 상세 조회
우선순위: 선택

REST: POST /v1/commits/get
gRPC: GitService.GetCommit()

Provider API:
- GitHub: GET /repos/OWNER/REPO/commits/SHA
- GitLab: GET /projects/ID/repository/commits/SHA
- Bitbucket: GET /repositories/WORKSPACE/REPO/commit/SHA
```

---

### Phase 4: Compare/Diff (권장)

#### 4.1 Compare
```
목적: 두 브랜치/커밋 비교
우선순위: 권장

REST: POST /v1/compare
gRPC: GitService.Compare()

요청:
- provider: ProviderConfig
- namespace: string
- repository: string
- base: string (기준 브랜치/커밋)
- head: string (비교 대상 브랜치/커밋)

응답:
- commits: []Commit (차이 커밋 목록)
- files: []DiffFile
  - path: string
  - old_path: string
  - status: string (added/modified/deleted/renamed)
  - additions: int32
  - deletions: int32
- total_commits: int32
- ahead_by: int32
- behind_by: int32

Provider API:
- GitHub: GET /repos/OWNER/REPO/compare/BASE...HEAD
- GitLab: GET /projects/ID/repository/compare?from=BASE&to=HEAD
- Bitbucket: GET /repositories/WORKSPACE/REPO/diff/BASE..HEAD
```

#### 4.2 GetCommitDiff
```
목적: 특정 커밋의 diff 조회
우선순위: 선택

REST: POST /v1/commits/diff
gRPC: GitService.GetCommitDiff()

Provider API:
- GitHub: GET /repos/OWNER/REPO/commits/SHA (Accept: application/vnd.github.diff)
- GitLab: GET /projects/ID/repository/commits/SHA/diff
- Bitbucket: GET /repositories/WORKSPACE/REPO/diff/SHA
```

---

### Phase 5: Merge Request (선택)

#### 5.1 ListMergeRequests
```
목적: MR/PR 목록 조회
우선순위: 선택

REST: POST /v1/merge-requests/list
gRPC: GitService.ListMergeRequests()

Provider API:
- GitHub: GET /repos/OWNER/REPO/pulls
- GitLab: GET /projects/ID/merge_requests
- Bitbucket: GET /repositories/WORKSPACE/REPO/pullrequests
```

#### 5.2 GetMergeRequest
```
목적: MR/PR 상세 조회
우선순위: 선택

REST: POST /v1/merge-requests/get
gRPC: GitService.GetMergeRequest()
```

#### 5.3 CreateMergeRequest
```
목적: MR/PR 생성
우선순위: 선택

REST: POST /v1/merge-requests
gRPC: GitService.CreateMergeRequest()

요청:
- provider: ProviderConfig
- namespace: string
- repository: string
- title: string
- description: string
- source_branch: string
- target_branch: string
- squash: bool
- remove_source_branch: bool
```

#### 5.4 MergeMergeRequest
```
목적: MR/PR 머지 실행
우선순위: 선택

REST: POST /v1/merge-requests/merge
gRPC: GitService.MergeMergeRequest()
```

#### 5.5 CloseMergeRequest
```
목적: MR/PR 닫기
우선순위: 선택

REST: POST /v1/merge-requests/close
gRPC: GitService.CloseMergeRequest()
```

---

## git-provider Proto 추가 정의

```protobuf
// ========== Phase 1: 파일/트리 ==========
// (기존 계획 참조)

// ========== Phase 2: Protected Branch ==========
message ProtectBranchRequest {
  ProviderConfig provider = 1;
  string namespace = 2;
  string repository = 3;
  string branch = 4;
  int32 push_access_level = 5;
  int32 merge_access_level = 6;
  bool allow_force_push = 7;
}

message ProtectBranchResponse {
  string name = 1;
  bool protected = 2;
}

message UnprotectBranchRequest {
  ProviderConfig provider = 1;
  string namespace = 2;
  string repository = 3;
  string branch = 4;
}

// ========== Phase 3: Commit ==========
message ListCommitsRequest {
  ProviderConfig provider = 1;
  string namespace = 2;
  string repository = 3;
  string ref = 4;
  string path = 5;
  int32 page = 6;
  int32 per_page = 7;
}

message ListCommitsResponse {
  repeated Commit commits = 1;
  int32 total_count = 2;
}

message Commit {
  string sha = 1;
  string message = 2;
  string author_name = 3;
  string author_email = 4;
  string authored_date = 5;
  string committer_name = 6;
  string committer_email = 7;
  string committed_date = 8;
  repeated string parent_ids = 9;
  string web_url = 10;
}

// ========== Phase 4: Compare ==========
message CompareRequest {
  ProviderConfig provider = 1;
  string namespace = 2;
  string repository = 3;
  string base = 4;
  string head = 5;
}

message CompareResponse {
  repeated Commit commits = 1;
  repeated DiffFile files = 2;
  int32 total_commits = 3;
  int32 ahead_by = 4;
  int32 behind_by = 5;
}

message DiffFile {
  string path = 1;
  string old_path = 2;
  string status = 3;  // added, modified, deleted, renamed
  int32 additions = 4;
  int32 deletions = 5;
}

// ========== Phase 5: Merge Request ==========
message MergeRequest {
  int64 id = 1;
  int64 iid = 2;
  string title = 3;
  string description = 4;
  string state = 5;  // opened, closed, merged
  string source_branch = 6;
  string target_branch = 7;
  string merge_status = 8;
  bool has_conflicts = 9;
  string web_url = 10;
  string author_name = 11;
  string created_at = 12;
  string merged_at = 13;
}

message CreateMergeRequestRequest {
  ProviderConfig provider = 1;
  string namespace = 2;
  string repository = 3;
  string title = 4;
  string description = 5;
  string source_branch = 6;
  string target_branch = 7;
  bool squash = 8;
  bool remove_source_branch = 9;
}

// Service 추가
service GitService {
  // Phase 1
  rpc GetContents(GetContentsRequest) returns (GetContentsResponse);
  rpc GetTree(GetTreeRequest) returns (GetTreeResponse);

  // Phase 2
  rpc ProtectBranch(ProtectBranchRequest) returns (ProtectBranchResponse);
  rpc UnprotectBranch(UnprotectBranchRequest) returns (google.protobuf.Empty);

  // Phase 3
  rpc ListCommits(ListCommitsRequest) returns (ListCommitsResponse);
  rpc GetCommit(GetCommitRequest) returns (Commit);

  // Phase 4
  rpc Compare(CompareRequest) returns (CompareResponse);

  // Phase 5
  rpc ListMergeRequests(ListMergeRequestsRequest) returns (ListMergeRequestsResponse);
  rpc GetMergeRequest(GetMergeRequestRequest) returns (MergeRequest);
  rpc CreateMergeRequest(CreateMergeRequestRequest) returns (MergeRequest);
  rpc MergeMergeRequest(MergeMergeRequestRequest) returns (MergeRequest);
  rpc CloseMergeRequest(CloseMergeRequestRequest) returns (MergeRequest);
}
```

---

# Part 2: tps-api (Java) 구현 목록

## 현재 구현 완료

| 도메인 | API | 상태 |
|--------|-----|------|
| Connection | CRUD + activate/deactivate/test | DB만 |
| Repository | CRUD + sync | DB만 |
| Branch | CRUD + status/commit update | DB만 |

---

## 추가 구현 필요

### Phase 1: git-provider 연동

#### 1.1 gRPC Client 설정
```
목적: git-provider gRPC 서버 연동
우선순위: 필수

작업:
1. Proto 파일 복사 (git-provider/api/proto/v1/)
2. build.gradle에 gRPC 의존성 추가
3. GrpcClientConfig 작성
4. GitProviderClient 서비스 작성
```

#### 1.2 Connection Test 구현
```
목적: 실제 Git Provider 연결 테스트
우선순위: 필수

현재: 시뮬레이션
변경: git-provider의 ListRepositories 호출로 검증
```

#### 1.3 Repository Sync 구현
```
목적: Git Provider에서 브랜치 정보 동기화
우선순위: 필수

현재: 상태만 변경
변경: git-provider의 ListBranches 호출 후 DB 동기화
```

---

### Phase 2: 파일 조회 API

#### 2.1 GetContents Proxy
```
목적: 파일/디렉토리 내용 조회 프록시
우선순위: 필수

Endpoint: GET /v1/repositories/{id}/contents
Query: path, ref

동작:
1. Repository ID로 Connection 정보 조회
2. git-provider GetContents 호출
3. 결과 반환
```

#### 2.2 GetTree Proxy
```
목적: 전체 트리 조회 프록시
우선순위: 필수

Endpoint: GET /v1/repositories/{id}/tree
Query: ref, recursive

동작:
1. Repository ID로 Connection 정보 조회
2. git-provider GetTree 호출
3. 결과 반환
```

---

### Phase 3: Commit/Compare API

#### 3.1 ListCommits Proxy
```
목적: 커밋 히스토리 조회
우선순위: 권장

Endpoint: GET /v1/repositories/{id}/commits
Query: ref, path, page, perPage
```

#### 3.2 Compare Proxy
```
목적: 브랜치 비교
우선순위: 권장

Endpoint: GET /v1/repositories/{id}/compare
Query: base, head
```

---

### Phase 4: Merge Request 관리

#### 4.1 MergeRequest 도메인 추가
```java
// 도메인
public class MergeRequest {
    UUID id;
    UUID repositoryId;
    Long providerMrId;      // Git Provider의 MR ID
    Long providerMrIid;     // 프로젝트 내 MR 번호
    String title;
    String description;
    String sourceBranch;
    String targetBranch;
    MergeRequestStatus status;  // OPEN, MERGED, CLOSED
    String mergeStatus;     // can_be_merged, cannot_be_merged
    boolean hasConflicts;
    String webUrl;
    LocalDateTime createdAt;
    LocalDateTime mergedAt;
}

// 상태
public enum MergeRequestStatus {
    OPEN, MERGED, CLOSED
}
```

#### 4.2 MergeRequest API
```
Endpoint: /v1/merge-requests

POST /v1/merge-requests
  - 생성 (git-provider 호출 + DB 저장)

GET /v1/merge-requests/{id}
  - 조회

GET /v1/merge-requests/repository/{repositoryId}
  - 저장소별 목록

POST /v1/merge-requests/{id}/merge
  - 머지 실행 (git-provider 호출)

POST /v1/merge-requests/{id}/close
  - 닫기 (git-provider 호출)
```

---

### Phase 5: Clone 기능 (선택)

#### 5.1 JGit 기반 Clone
```
목적: 로컬 스토리지에 저장소 클론
우선순위: 선택 (배포 시스템 연동용)

Endpoint: POST /v1/repositories/{id}/clone
Body:
  - branch: string
  - cloneType: ssh | https

동작:
1. Connection에서 인증 정보 조회
2. JGit으로 클론 실행
3. 로컬 경로 반환
```

---

## tps-api 아키텍처

```
┌─────────────────────────────────────────────────┐
│   Controller Layer (REST API)                   │
│   ├─ ConnectionController                       │
│   ├─ RepositoryController                       │
│   ├─ BranchController                           │
│   ├─ ContentsController (신규)                  │
│   ├─ CommitController (신규)                    │
│   └─ MergeRequestController (신규)              │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│   Application Layer (Use Cases)                 │
│   ├─ ConnectionUseCase                          │
│   ├─ RepositoryUseCase                          │
│   ├─ BranchUseCase                              │
│   ├─ ContentsUseCase (신규)                     │
│   ├─ CommitUseCase (신규)                       │
│   └─ MergeRequestUseCase (신규)                 │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│   Port Layer (Interfaces)                       │
│   ├─ ConnectionPort                             │
│   ├─ RepositoryPort                             │
│   ├─ BranchPort                                 │
│   ├─ MergeRequestPort (신규)                    │
│   └─ GitProviderPort (신규) ─────────┐          │
└─────────────────┬────────────────────│──────────┘
                  │                    │
┌─────────────────▼──────────┐ ┌───────▼──────────┐
│   Adapter-Out (Persistence)│ │  Adapter-Out     │
│   ├─ ConnectionAdapter     │ │  (gRPC Client)   │
│   ├─ RepositoryAdapter     │ │                  │
│   ├─ BranchAdapter         │ │  GitProvider     │
│   └─ MergeRequestAdapter   │ │  GrpcClient      │
│       (신규)               │ │  (신규)          │
└────────────────────────────┘ └──────────────────┘
              │                        │
              ▼                        ▼
        PostgreSQL               git-provider
                                (Go gRPC Server)
```

---

## 구현 우선순위 요약

### MVP (필수)
1. git-provider: GetContents, GetTree
2. tps-api: gRPC Client 설정, Contents/Tree Proxy

### v1.1 (권장)
3. git-provider: Protected Branch, ListCommits, Compare
4. tps-api: Commit/Compare Proxy

### v1.2 (선택)
5. git-provider: Merge Request CRUD
6. tps-api: MergeRequest 도메인 + API

### v2.0 (향후)
7. tps-api: Clone 기능 (JGit)
8. User/Group 관리 (필요시)

---

## 일정 추정

| Phase | 작업 | git-provider | tps-api |
|-------|-----|-------------|---------|
| 1 | 파일/트리 조회 | 6시간 | 4시간 |
| 2 | Protected Branch | 4시간 | - |
| 3 | Commit/Compare | 4시간 | 2시간 |
| 4 | Merge Request | 6시간 | 6시간 |
| 5 | Clone | - | 4시간 |
| 합계 | | 20시간 | 16시간 |
