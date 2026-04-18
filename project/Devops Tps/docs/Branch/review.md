# Branch 구현 리뷰

## What - 무엇을 구현했는가

`branch_server.go` (540줄)에 BranchService의 5개 RPC를 구현했다. GitService의 기본 CRUD(ListBranches, GetBranch, CreateBranch, DeleteBranch)와 달리, 여기서는 브랜치 간 관계와 상태를 분석하는 고수준 기능을 제공한다.

| RPC | 구현 핵심 |
|-----|-----------|
| CompareBranches | ahead/behind 계산, MergeableState·SuggestedAction 결정 |
| ListCommitsDiff | 브랜치 간 커밋 차이 목록 (페이지네이션) |
| ListMergedBranches | 기준 브랜치에 머지된 브랜치 수집 |
| ListStaleBranches | stale_days 기준으로 비활성 브랜치 필터링 |
| CleanupBranches | 머지+stale 브랜치 일괄 삭제, dry-run 지원 |

---

## How - 어떻게 구현했는가

### 변환 계층 (2단계 변환)

BranchService는 GitService와 달리 2단계 변환 구조를 사용한다. Provider API 응답을 `internal/client/` 공통 타입으로 먼저 변환하고, 그 다음 proto 메시지로 변환한다. 이 구조 덕분에 Provider별 차이를 client 계층에서 완전히 흡수하고, server 계층은 공통 타입만 다루면 된다.

```
Provider API 응답
    ↓ client 계층
internal/client 공통 타입 (BranchComparison, MergedBranchInfo 등)
    ↓ server 계층 변환 함수
proto 메시지 (pb.BranchComparison, pb.MergedBranchInfo 등)
```

**변환 함수 목록**

```go
convertBranchComparison(*client.BranchComparison) → *pb.BranchComparison
convertCommitInfoList([]*client.CommitInfo) → []*pb.CommitInfo
convertMergedBranchInfoList([]*client.MergedBranchInfo) → []*pb.MergedBranchInfo
convertStaleBranchInfoList([]*client.StaleBranchInfo) → []*pb.StaleBranchInfo
```

### Provider별 ahead/behind 계산

가장 복잡한 부분은 CompareBranches의 ahead/behind 계산이다. GitHub는 단일 API로 양방향 비교가 가능하지만, GitLab과 Bitbucket은 서버에서 보정이 필요하다.

| Provider | ahead 계산 | behind 계산 | API 호출 횟수 |
|----------|-----------|-------------|--------------|
| GitHub | `Repositories.CompareCommits()` 직접 | 동일 응답 | 1회 |
| GitLab | `Repositories.Compare(base→compare)` | `Repositories.Compare(compare→base)` 역방향 | 2회 |
| Bitbucket | 커밋 목록으로 직접 계산 | 역방향 커밋으로 계산 | 2회 이상 |

### ListStaleBranches 구현

`stale_days` 파라미터(기본값 30)보다 오래된 브랜치를 반환한다. Provider별로 구현 방식이 다르다.

- **GitHub**: 모든 브랜치를 순회하며 마지막 커밋 날짜 체크
- **GitLab**: 브랜치 API에 `stale_days` 파라미터를 직접 전달하여 서버 측 필터링
- **Bitbucket**: 모든 브랜치를 순회하며 `calculateDaysSince()`로 경과 일수 계산

`calculateDaysSince()` 함수는 초기에 항상 0을 반환하는 버그가 있었다. ISO 8601 형식의 날짜 문자열을 파싱하지 않고 비교했기 때문이다. `time.Parse(time.RFC3339)`로 올바르게 파싱하여 수정되었다.

### CleanupBranches 실행 흐름

```
1. ListMergedBranches → 머지된 브랜치 수집
2. ListStaleBranches → 비활성 브랜치 수집
3. 두 목록 합산 (중복 제거)
4. exclude_patterns 적용 (main, develop, release/* 등 보호)
5. dry_run 확인 → false이면 각 브랜치에 DeleteBranch 호출
6. 결과 집계 (삭제 성공/실패/스킵 수)
```

### 패턴 매칭 (isExcluded)

`isExcluded()` 함수는 간단한 와일드카드(`*`)를 지원한다. 정규식은 지원하지 않는다.

- `main` → 정확 일치
- `release/*` → `release/` 접두사 매칭
- `*-hotfix` → `-hotfix` 접미사 매칭

---

## Why - 왜 이렇게 구현했는가

### 2단계 변환을 선택한 이유

GitService는 proto 메시지를 직접 반환하는 단순 구조를 사용한다. 반면 BranchService는 중간 공통 타입을 거치는 2단계 구조를 사용한다. BranchService의 기능이 Provider마다 다르게 동작하기 때문이다. ahead/behind 계산처럼 GitHub는 단일 API로 가능하지만 GitLab은 2회 호출이 필요한 경우, 이 복잡성을 client 계층에서 캡슐화하고 server 계층에는 통일된 인터페이스를 제공하기 위해 2단계 변환을 선택했다.

### dry-run 기본값을 true로 설정한 이유

CleanupBranches는 복구 불가능한 삭제 작업이다. 실수로 `dryRun=false`를 보내 중요한 브랜치를 삭제하는 것을 방지하기 위해 기본값을 `true`로 설정했다. 사용자는 먼저 dry-run으로 삭제 대상을 확인하고, 명시적으로 `dryRun=false`를 지정해야만 실제 삭제가 진행된다.

### 와일드카드만 지원하는 이유

정규식 패턴을 지원하면 더 강력하지만, 일반적인 브랜치 보호 패턴(release/*, hotfix/*)은 간단한 와일드카드로 충분히 표현 가능하다. 정규식은 잘못 작성할 경우 보호해야 할 브랜치가 삭제되는 위험이 있어, 단순하고 이해하기 쉬운 와일드카드만 지원한다.

---

## 참고 패턴

| 패턴 | 적용 위치 | 설명 |
|------|-----------|------|
| 2단계 변환 | `branch_server.go` | Provider API → 공통 타입 → proto 메시지 |
| Dry-run 패턴 | `CleanupBranches` | 실제 작업 전 미리보기 제공 |
| 역방향 비교 보정 | `CompareBranches` GitLab/Bitbucket | 단방향 API로 양방향 비교 구현 |
| glob 패턴 매칭 | `isExcluded()` | 와일드카드(*) 기반 브랜치 보호 |
| RFC3339 파싱 | `calculateDaysSince()` | ISO 8601 날짜 올바른 파싱 |

---

## 개선 가능 사항

1. **대규모 저장소 성능**: ListStaleBranches가 모든 브랜치를 순회하므로 브랜치가 수백 개인 저장소에서 성능 저하가 발생할 수 있다. 커서 기반 페이지네이션으로 개선이 필요하다.
2. **CleanupBranches 병렬화**: 현재 순차적으로 브랜치를 삭제하는데, goroutine 풀을 사용하면 대규모 삭제 작업의 속도를 개선할 수 있다.
3. **정규식 패턴 지원**: 현재 와일드카드만 지원하므로 `feature/[A-Z]+-*` 같은 복잡한 패턴은 매칭이 불가능하다.
