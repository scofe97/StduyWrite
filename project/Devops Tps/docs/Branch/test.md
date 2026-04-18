# Branch 테스트

## API 테스트 시나리오

### GitService - 브랜치 CRUD

| RPC | 시나리오 | 입력 | 기대 결과 |
|-----|----------|------|-----------|
| ListBranches | 브랜치 목록 조회 | owner, repo | 브랜치 배열 반환 |
| ListBranches | 페이지네이션 | page=2, perPage=10 | 2페이지 브랜치 반환 |
| GetBranch | 존재하는 브랜치 조회 | name=main | 브랜치 상세 반환 |
| GetBranch | 존재하지 않는 브랜치 조회 | name=nonexistent | 404 Not Found |
| CreateBranch | 새 브랜치 생성 | name=feature/test, sha=main | 생성된 브랜치 반환 |
| CreateBranch | 이미 존재하는 브랜치 생성 | name=main | 409 Conflict |
| DeleteBranch | 일반 브랜치 삭제 | name=feature/old | 204 No Content |
| DeleteBranch | 보호된 브랜치 삭제 시도 | name=main | 403 Forbidden |

**curl 예시 - ListBranches**

```bash
curl "http://localhost:8080/v1/git/550e8400-e29b-41d4-a716-446655440000/branches?owner=myorg&repo=myrepo"
```

**curl 예시 - CreateBranch**

```bash
curl -X POST "http://localhost:8080/v1/git/550e8400-e29b-41d4-a716-446655440000/branches" \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "myorg",
    "repo": "myrepo",
    "name": "feature/new-feature",
    "sha": "main"
  }'
```

**curl 예시 - DeleteBranch**

```bash
curl -X DELETE "http://localhost:8080/v1/git/550e8400-e29b-41d4-a716-446655440000/branches/feature/old?owner=myorg&repo=myrepo"
```

---

### BranchService - CompareBranches

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 머지 가능한 브랜치 비교 | base=main, compare=feature/login (ahead=5, behind=0) | suggestedAction=FAST_FORWARD |
| 뒤처진 브랜치 비교 | base=main, compare=feature/old (ahead=3, behind=15) | suggestedAction=REBASE |
| 충돌 있는 브랜치 비교 | base=main, compare=feature/conflict | mergeableState=CONFLICTING, suggestedAction=RESOLVE_CONFLICTS |
| 동기화된 브랜치 비교 | base=main, compare=main-copy (ahead=0, behind=0) | suggestedAction=UP_TO_DATE |
| 양방향 차이 있는 비교 | base=main, compare=feature (ahead=3, behind=5) | suggestedAction=MERGE_BASE |

**curl 예시 - 브랜치 비교**

```bash
# 기본 비교
curl "http://localhost:8080/v1/branches/550e8400-e29b-41d4-a716-446655440000/compare?owner=myorg&repo=myrepo&base=main&compare=feature/login"

# 릴리즈 브랜치와 비교
curl "http://localhost:8080/v1/branches/550e8400-e29b-41d4-a716-446655440000/compare?owner=myorg&repo=myrepo&base=develop&compare=release/v1.0"
```

---

### BranchService - ListCommitsDiff

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 커밋 차이 조회 | base=main, compare=feature/login | 커밋 목록 반환 |
| 페이지네이션 | base=main, compare=feature, page=2, perPage=10 | 2페이지 커밋 반환 |
| 동일 브랜치 비교 | base=main, compare=main | 빈 커밋 배열 반환 |

**curl 예시**

```bash
curl "http://localhost:8080/v1/branches/550e8400-e29b-41d4-a716-446655440000/compare/commits?owner=myorg&repo=myrepo&base=main&compare=feature/login&perPage=50"
```

---

### BranchService - ListMergedBranches

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| main에 머지된 브랜치 목록 | base=main | 머지된 브랜치 배열 반환 |
| develop에 머지된 브랜치 목록 | base=develop | 해당 기준의 머지 목록 반환 |
| 머지된 브랜치가 없는 경우 | base=empty-base | 빈 배열 반환 |

**curl 예시**

```bash
# main에 머지된 브랜치
curl "http://localhost:8080/v1/branches/550e8400-e29b-41d4-a716-446655440000/merged?owner=myorg&repo=myrepo"

# develop에 머지된 브랜치
curl "http://localhost:8080/v1/branches/550e8400-e29b-41d4-a716-446655440000/merged?owner=myorg&repo=myrepo&base=develop"
```

---

### BranchService - ListStaleBranches

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| 기본 30일 기준 비활성 브랜치 | staleDays=30 | 30일 이상 비활성 브랜치 목록 |
| 60일 기준 비활성 브랜치 | staleDays=60 | 60일 이상 비활성 브랜치 목록 |
| 비활성 브랜치 없는 경우 | staleDays=1 (모든 브랜치 최근 커밋) | 빈 배열 반환 |
| 보호된 브랜치 포함 여부 | staleDays=30 | isProtected=true로 포함되어 반환 |

**curl 예시**

```bash
# 기본 30일
curl "http://localhost:8080/v1/branches/550e8400-e29b-41d4-a716-446655440000/stale?owner=myorg&repo=myrepo"

# 60일 기준
curl "http://localhost:8080/v1/branches/550e8400-e29b-41d4-a716-446655440000/stale?owner=myorg&repo=myrepo&staleDays=60"
```

---

### BranchService - CleanupBranches

| 시나리오 | 입력 | 기대 결과 |
|----------|------|-----------|
| dry-run으로 미리보기 | dryRun=true, includeMerged=true | toDelete 목록 채워짐, deleted 빈 배열 |
| 머지된 브랜치 실제 삭제 | dryRun=false, includeMerged=true | deleted 목록 채워짐 |
| stale 브랜치 포함 정리 | dryRun=false, includeStale=true, staleDays=90 | 90일 이상 비활성 브랜치도 삭제 |
| 제외 패턴 적용 | excludePatterns=["release/*", "hotfix/*"] | 해당 패턴 브랜치는 skipped로 분류 |
| 보호된 브랜치 제외 | excludeProtected=true | 보호 브랜치는 skipped로 분류 |

**curl 예시 - dry-run 미리보기**

```bash
curl -X POST "http://localhost:8080/v1/branches/cleanup" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "owner": "myorg",
    "repo": "myrepo",
    "dryRun": true,
    "options": {
      "includeMerged": true,
      "includeStale": true,
      "staleDays": 60
    }
  }'
```

**curl 예시 - 실제 삭제 (제외 패턴 적용)**

```bash
curl -X POST "http://localhost:8080/v1/branches/cleanup" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "owner": "myorg",
    "repo": "myrepo",
    "dryRun": false,
    "options": {
      "includeMerged": true,
      "includeStale": false,
      "baseBranch": "main",
      "excludePatterns": ["release/*", "hotfix/*", "develop"]
    }
  }'
```

**curl 예시 - stale 브랜치만 90일 기준 정리**

```bash
curl -X POST "http://localhost:8080/v1/branches/cleanup" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "owner": "myorg",
    "repo": "myrepo",
    "dryRun": false,
    "options": {
      "includeMerged": false,
      "includeStale": true,
      "staleDays": 90
    }
  }'
```

---

## 에지 케이스

| 케이스 | 입력 | 기대 동작 |
|--------|------|-----------|
| 보호된 브랜치 삭제 시도 | DeleteBranch(name=main) | 403 Forbidden 반환 |
| staleDays=0 으로 ListStaleBranches | staleDays=0 | 모든 브랜치 반환 또는 400 Bad Request |
| 빈 저장소에서 CompareBranches | 커밋이 없는 저장소 | 404 또는 ahead=0, behind=0 반환 |
| 자기 자신과 비교 | base=main, compare=main | 422 Unprocessable (같은 브랜치 비교 불가) |
| 존재하지 않는 브랜치 비교 | compare=nonexistent | 404 Not Found |
| includeMerged=false, includeStale=false | 두 옵션 모두 false | 400 Bad Request (최소 하나는 true 필요) |
| 제외 패턴이 모든 브랜치를 포함 | excludePatterns=["*"] | toDelete 빈 배열, 모든 브랜치 skipped |
| 삭제 중 일부 브랜치 실패 | 혼합된 삭제 결과 | deleted + failed 모두 채워진 응답 반환 |
| 매우 큰 저장소 (브랜치 1000개+) | staleDays=30 | 정상 응답 (성능 저하 가능성 있음) |
| stale 기준 경계값 | daysSinceLastCommit 정확히 30 | staleDays=30 이면 포함 여부 확인 |
