# Phase 1: 저장소 도메인 완료 보고서

## 개요

**기간**: Phase 1.1 ~ 1.4
**상태**: 완료
**목표**: Git Provider(GitHub, GitLab, Bitbucket) 통합을 통한 저장소 관리 기능 구현

---

## 구현 완료 현황

| Phase | 기능 | 상태 | API 문서 | 도메인 문서 |
|:-----:|------|:----:|:--------:|:-----------:|
| **1.1** | 코드 탐색 | 완료 | [Contents API](../Contents/api-design.md) | [Contents 도메인](../Contents/usecase-model.md) |
| **1.2** | 브랜치 비교 | 완료 | [Branch API](../Branch/api-design.md) | [Branch 도메인](../Branch/usecase-model.md) |
| **1.3** | 브랜치 정리 | 완료 | [Branch API](../Branch/api-design.md) | - |
| **1.4** | PR/MR | 완료 | [MergeRequest API](../MergeRequest/api-design.md) | - |

---

## Provider 지원 현황

### 전체 기능 매트릭스

| 기능 | GitHub | GitLab | Bitbucket | 비고 |
|------|:------:|:------:|:---------:|------|
| **Phase 1.1: 코드 탐색** ||||
| 파일 트리 조회 | 완료 | 완료 | 완료 | |
| 파일 내용 조회 | 완료 | 완료 | 완료 | |
| README 렌더링 | 완료 | 완료 | 완료 | |
| **Phase 1.2: 브랜치 비교** ||||
| ahead/behind 계산 | 완료 | 완료 | 부분 | Bitbucket: 별도 계산 |
| mergeable 상태 | 완료 | 완료 | 미지원 | Bitbucket: PR 생성 필요 |
| diff stat | 완료 | 완료 | 완료 | |
| 커밋 차이 목록 | 완료 | 완료 | 완료 | |
| **Phase 1.3: 브랜치 정리** ||||
| 머지된 브랜치 목록 | 완료 | 완료 | 완료 | |
| Stale 브랜치 목록 | 완료 | 완료 | 완료 | |
| 브랜치 일괄 삭제 | 완료 | 완료 | 완료 | |
| Dry-run 지원 | 완료 | 완료 | 완료 | |
| **Phase 1.4: PR/MR** ||||
| 목록 조회 | 완료 | 완료 | 완료 | |
| 상세 조회 | 완료 | 완료 | 완료 | |
| 생성 | 완료 | 완료 | 완료 | |
| 머지 | 완료 | 완료 | 완료 | |
| 댓글 CRUD | 완료 | 완료 | 부분 | Bitbucket: 수정/삭제 미지원 |
| 리뷰 | 완료 | 완료 | 부분 | Bitbucket: Approve로 대체 |

**범례**: 완료 = 완전 지원 | 부분 = 부분 지원 | 미지원 = 구현 불가

---

## Phase 1.1: 코드 탐색

### 기능 설명

저장소의 파일 구조를 탐색하고 파일 내용을 조회하는 기능이다.

### API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| `GET` | `/v1/contents/{connectionId}/tree` | 파일 트리 조회 |
| `POST` | `/v1/contents/tree` | 파일 트리 조회 (POST) |
| `GET` | `/v1/contents/{connectionId}/file` | 파일 내용 조회 |
| `POST` | `/v1/contents/file` | 파일 내용 조회 (POST) |

### 도메인 모델

```
TreeEntry                      ContentEntry
├── path: String               ├── path: String
├── type: EntryType            ├── type: ContentType
│   └── BLOB | TREE            │   └── FILE | DIRECTORY | SYMLINK | SUBMODULE
├── sha: String                ├── content: String (Base64)
├── size: Long                 ├── encoding: String
└── mode: String               ├── sha: String
                               └── size: Long
```

### 구현 파일

**Git-Provider (Go)**:
- `api/proto/v1/contents.proto`
- `internal/server/contents_server.go`
- `internal/client/github.go`, `gitlab.go`, `bitbucket.go`

**TPS-API (Java)**:
- `domain/contents/TreeEntry.java`, `ContentEntry.java`
- `application/service/ContentsService.java`
- `adapter/in/web/ContentsController.java`

---

## Phase 1.2: 브랜치 비교

### 기능 설명

두 브랜치 간의 차이를 비교하여 ahead/behind 커밋 수, 머지 가능 여부, 권장 액션을 제공한다.

### API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| `GET` | `/v1/branches/{connectionId}/compare` | 브랜치 비교 |
| `GET` | `/v1/branches/{connectionId}/compare/commits` | 커밋 차이 목록 |
| `GET` | `/v1/branches/{connectionId}/merged` | 머지된 브랜치 목록 |
| `GET` | `/v1/branches/{connectionId}/stale` | Stale 브랜치 목록 |

### 도메인 모델

```
BranchComparison
├── baseBranch: String
├── compareBranch: String
├── aheadBy: Integer
├── behindBy: Integer
├── mergeableState: MergeableState
│   └── MERGEABLE | CONFLICTING | UNKNOWN
├── mergeStatus: String
├── suggestedAction: SuggestedAction
│   └── CREATE_MR | REBASE | MERGE_BASE | RESOLVE_CONFLICTS | UP_TO_DATE
└── diffStat: DiffStat
    ├── additions: Integer
    ├── deletions: Integer
    └── changedFiles: Integer
```

### 권장 액션 로직

| 조건 | 권장 액션 | 설명 |
|------|----------|------|
| ahead=0, behind=0 | `UP_TO_DATE` | 브랜치가 동일함 |
| ahead>0, behind=0 | `CREATE_MR` | PR/MR 생성 권장 |
| ahead>0, behind>0, mergeable | `CREATE_MR` | 머지 가능, PR 생성 |
| ahead>0, behind>0, !mergeable | `RESOLVE_CONFLICTS` | 충돌 해결 필요 |
| ahead=0, behind>0 | `MERGE_BASE` | 베이스 브랜치 머지 |

---

## Phase 1.3: 브랜치 정리

### 기능 설명

머지 완료된 브랜치와 오래된(Stale) 브랜치를 정리하는 기능이다.

### API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| `POST` | `/v1/branches/cleanup` | 브랜치 정리 (dry-run 지원) |

### 요청 옵션

```yaml
CleanupOptions:
  dryRun: boolean           # 시뮬레이션 모드 (기본: true)
  includeMerged: boolean    # 머지된 브랜치 포함
  includeStale: boolean     # Stale 브랜치 포함
  staleDays: integer        # 비활성 기준 일수 (기본: 30)
  excludePatterns:          # 제외 패턴
    - "main"
    - "master"
    - "develop"
    - "release/*"
    - "hotfix/*"
```

---

## Phase 1.4: PR/MR 관리

### 기능 설명

Pull Request(GitHub, Bitbucket) / Merge Request(GitLab)를 생성하고 관리하는 기능이다.

### API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| `GET` | `/v1/merge-requests/{connectionId}/list` | MR 목록 조회 |
| `GET` | `/v1/merge-requests/{connectionId}/{number}` | MR 상세 조회 |
| `POST` | `/v1/merge-requests/list` | MR 목록 조회 (POST) |
| `POST` | `/v1/merge-requests/get` | MR 상세 조회 (POST) |
| `POST` | `/v1/merge-requests/create` | MR 생성 |
| `POST` | `/v1/merge-requests/merge` | MR 머지 |

### Provider별 용어 매핑

| TPS 통합 | GitHub | GitLab | Bitbucket |
|----------|--------|--------|-----------|
| MergeRequest | Pull Request | Merge Request | Pull Request |
| number | number | iid | id |
| 댓글 | Issue Comments | Notes | Comments |
| 리뷰 | Reviews | Approvals | Approve/Unapprove |

### Bitbucket 제한 사항

| 기능 | 지원 | 비고 |
|------|:----:|------|
| 인라인 댓글 | 미지원 | path, line 파라미터 미지원 |
| 댓글 수정 | 미지원 | go-bitbucket 라이브러리 미지원 |
| 댓글 삭제 | 미지원 | go-bitbucket 라이브러리 미지원 |
| 정식 리뷰 | 미지원 | Approve/Unapprove로 대체 |

---

## 향후 계획 (Phase 2+)

| Phase | 모듈 | 상태 | 주요 기능 |
|:-----:|------|:----:|----------|
| **2** | 파이프라인 | 스펙 작성됨 | Jenkins/GitHub Actions/GitLab CI 연동 |
| **3** | 컨테이너 | 예정 | Docker 관리, Registry 연동 |
| **4** | Kubernetes | 예정 | 클러스터 연결, GitOps 배포 |
| **5** | VM | 예정 | libvirt/KVM 기반 (선택적) |

---

## 관련 문서

- [overview.md](overview.md) - 시스템 아키텍처 개요
- [service-communication.md](service-communication.md) - 서비스 간 통신
- [Repository/review.md](../Repository/review.md) - GitService 구현 리뷰
- [Provider/review.md](../Provider/review.md) - Provider 클라이언트 리뷰
