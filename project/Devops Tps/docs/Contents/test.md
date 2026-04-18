# Contents 테스트

## API 테스트 시나리오

### GetTree - 파일 트리 조회

| RPC | 시나리오 | 입력 | 기대 결과 |
|-----|----------|------|-----------|
| GetTree | 루트 트리 조회 | owner, repo (ref 없음) | 기본 브랜치 루트 항목 반환 |
| GetTree | 특정 브랜치 트리 조회 | ref=develop | develop 브랜치의 트리 반환 |
| GetTree | 하위 경로 트리 조회 | path=src/main/java | 해당 경로의 항목만 반환 |
| GetTree | 재귀 조회 | recursive=true | 모든 하위 항목 반환 |
| GetTree | 특정 커밋 SHA 기준 | ref=abc1234567 | 해당 커밋 시점의 트리 반환 |
| GetTree | 존재하지 않는 브랜치 | ref=nonexistent | 404 Not Found |
| GetTree | 빈 저장소 | 커밋 없는 저장소 | 404 또는 빈 entries 배열 |

**curl 예시 - 루트 트리 조회**

```bash
curl "http://localhost:8080/v1/contents/550e8400-e29b-41d4-a716-446655440000/tree?owner=myorg&repo=myrepo"
```

**curl 예시 - 특정 브랜치 하위 경로 조회**

```bash
curl "http://localhost:8080/v1/contents/550e8400-e29b-41d4-a716-446655440000/tree?owner=myorg&repo=myrepo&ref=develop&path=src/main"
```

**curl 예시 - 재귀 전체 조회**

```bash
curl "http://localhost:8080/v1/contents/550e8400-e29b-41d4-a716-446655440000/tree?owner=myorg&repo=myrepo&recursive=true"
```

**curl 예시 - POST 방식**

```bash
curl -X POST "http://localhost:8080/v1/contents/tree" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "owner": "myorg",
    "repo": "myrepo",
    "ref": "main",
    "path": "src/main/java",
    "recursive": false
  }'
```

---

### GetContents - 파일/디렉토리 내용 조회

| RPC | 시나리오 | 입력 | 기대 결과 |
|-----|----------|------|-----------|
| GetContents | 텍스트 파일 조회 | path=README.md | type=FILE, base64 content 반환 |
| GetContents | 특정 브랜치 파일 조회 | path=src/main.go, ref=develop | 해당 브랜치 파일 내용 반환 |
| GetContents | 디렉토리 조회 | path=src/ | type=DIR, entries 배열 반환 |
| GetContents | 존재하지 않는 파일 | path=missing.txt | 404 Not Found |
| GetContents | 특정 커밋 기준 파일 | path=config.yaml, ref=abc1234 | 해당 커밋 시점 파일 내용 반환 |
| GetContents | 심볼릭 링크 | path=link-file | type=SYMLINK 반환 |

**curl 예시 - 파일 내용 조회**

```bash
# GET 방식
curl "http://localhost:8080/v1/contents/550e8400-e29b-41d4-a716-446655440000/file?owner=myorg&repo=myrepo&path=README.md"

# 특정 브랜치 파일
curl "http://localhost:8080/v1/contents/550e8400-e29b-41d4-a716-446655440000/file?owner=myorg&repo=myrepo&path=src/main.go&ref=develop"
```

**curl 예시 - POST 방식**

```bash
curl -X POST "http://localhost:8080/v1/contents/file" \
  -H "Content-Type: application/json" \
  -d '{
    "connectionId": "550e8400-e29b-41d4-a716-446655440000",
    "owner": "myorg",
    "repo": "myrepo",
    "path": "pom.xml",
    "ref": "release/v1.0"
  }'
```

---

### GetReadme - README 자동 탐지

| RPC | 시나리오 | 입력 | 기대 결과 |
|-----|----------|------|-----------|
| GetReadme | README.md 존재 | 루트에 README.md 있음 | README.md 내용 반환 |
| GetReadme | README.rst 존재 (md 없음) | 루트에 README.rst만 있음 | README.rst 내용 반환 |
| GetReadme | 특정 브랜치 README | ref=feature/docs | 해당 브랜치의 README 반환 |
| GetReadme | README 없음 | README 파일 없는 저장소 | 404 Not Found |
| GetReadme | 빈 저장소 | 커밋 없는 저장소 | 404 Not Found |

**curl 예시 - README 조회**

```bash
curl "http://localhost:8080/v1/contents/550e8400-e29b-41d4-a716-446655440000/readme?owner=myorg&repo=myrepo"
```

---

## 에지 케이스

| 케이스 | 입력 | 기대 동작 |
|--------|------|-----------|
| 빈 저장소 트리 조회 | 커밋이 없는 저장소의 GetTree | 404 Not Found 또는 빈 entries 반환 |
| 바이너리 파일 조회 | path=image.png (PNG 파일) | Base64 인코딩된 바이너리 내용 반환 (타입 구분 없이 동일 처리) |
| 대용량 파일 조회 (1MB 초과) | path=large-dataset.csv (5MB 파일) | content 필드가 비거나 생략될 수 있음, size 필드는 정확히 반환 |
| 중첩 디렉토리 조회 | path=a/b/c/d/e (깊은 중첩) | 해당 경로 항목 정상 반환 |
| 루트 경로 파라미터 없음 | path="" 또는 path 생략 | 루트 디렉토리 항목 반환 |
| 경로 앞뒤 슬래시 | path=/src/ vs path=src | 동일 결과 반환 (정규화 처리) |
| 재귀 조회 대용량 저장소 | recursive=true, 파일 10만 개 이상 | truncated=true 반환 (GitHub) 또는 전체 수집 (GitLab/Bitbucket, 느릴 수 있음) |
| 존재하지 않는 커밋 SHA | ref=0000000000000000000 | 404 Not Found |
| 숨김 파일 조회 | path=.gitignore | 정상적으로 파일 내용 반환 |
| 빈 파일 조회 | path=empty.txt (0 bytes) | size=0, content="" (빈 base64) 반환 |
