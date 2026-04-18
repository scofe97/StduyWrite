# CICD 테스트 시나리오

서버 주소: `localhost:8083` (REST gateway), `localhost:9093` (gRPC)

---

## 사전 준비

```bash
# 서버 실행 확인
curl -s http://localhost:8083/v1/pipelines/list -d '{}' | jq .

# Jenkins 실행 확인 (Docker Compose 환경)
curl -s http://localhost:8080/api/json | jq .
```

---

## TC-C1: 파이프라인 생성

### 정상: Jenkins 설정 포함 파이프라인 생성

```bash
curl -X POST http://localhost:8083/v1/pipelines/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "backend-build",
    "repository": "my-org/backend",
    "branch_pattern": "main",
    "stages": [
      {"name": "Build", "command": "go build ./...", "timeout_seconds": 300},
      {"name": "Test",  "command": "go test ./...",  "timeout_seconds": 600}
    ],
    "ci_config": {
      "jenkins": {
        "url": "http://localhost:8080",
        "username": "admin",
        "api_token": "11abc..."
      }
    },
    "jenkins_job_name": "backend-build"
  }'
```

**기대 응답**:

```json
{
  "pipeline": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "backend-build",
    "repository": "my-org/backend",
    "branch_pattern": "main",
    "jenkins_job_name": "backend-build",
    "created_at": "2025-01-01T10:00:00Z"
  }
}
```

### 엣지 케이스: ci_config 누락

```bash
curl -X POST http://localhost:8083/v1/pipelines/create \
  -H "Content-Type: application/json" \
  -d '{"name": "incomplete", "repository": "org/repo", "branch_pattern": "main"}'
```

**기대 응답**: `400 Bad Request` — ci_config 필드 필수

---

## TC-C2: 파이프라인 목록 조회

### 정상: 전체 목록

```bash
curl -X POST http://localhost:8083/v1/pipelines/list \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 정상: 저장소 필터

```bash
curl -X POST http://localhost:8083/v1/pipelines/list \
  -H "Content-Type: application/json" \
  -d '{"repository": "my-org/backend"}'
```

**기대 응답**: `my-org/backend` 저장소의 파이프라인만 반환

---

## TC-C3: 파이프라인 단건 조회

```bash
PIPELINE_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X POST http://localhost:8083/v1/pipelines/get \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$PIPELINE_ID\"}"
```

### 엣지 케이스: 존재하지 않는 ID

```bash
curl -X POST http://localhost:8083/v1/pipelines/get \
  -H "Content-Type: application/json" \
  -d '{"id": "non-existent-id"}'
```

**기대 응답**: `404 Not Found`

---

## TC-C4: 빌드 트리거

### 정상: 기본 브랜치로 빌드

```bash
PIPELINE_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X POST http://localhost:8083/v1/builds/trigger \
  -H "Content-Type: application/json" \
  -d "{\"pipeline_id\": \"$PIPELINE_ID\"}"
```

**기대 응답**:

```json
{
  "build": {
    "id": "...",
    "pipeline_id": "550e8400-...",
    "build_number": 1,
    "status": "BUILD_STATUS_QUEUED",
    "trigger": "manual",
    "branch": "main",
    "started_at": "2025-01-01T10:01:00Z"
  }
}
```

### 정상: 브랜치 오버라이드

```bash
curl -X POST http://localhost:8083/v1/builds/trigger \
  -H "Content-Type: application/json" \
  -d "{
    \"pipeline_id\": \"$PIPELINE_ID\",
    \"branch\": \"feature/new-api\",
    \"commit_sha\": \"abc123\"
  }"
```

### 엣지 케이스: Jenkins 오프라인

Jenkins 서버를 중단한 상태에서 빌드 트리거:

```bash
# Jenkins 중단 후
curl -X POST http://localhost:8083/v1/builds/trigger \
  -H "Content-Type: application/json" \
  -d "{\"pipeline_id\": \"$PIPELINE_ID\"}"
```

**기대 동작**: Build 객체 생성 (status: FAILURE, 연결 실패 메시지 포함)

### 엣지 케이스: 동시 트리거 (Concurrent)

```bash
# 동시에 3개 빌드 트리거
for i in 1 2 3; do
  curl -X POST http://localhost:8083/v1/builds/trigger \
    -H "Content-Type: application/json" \
    -d "{\"pipeline_id\": \"$PIPELINE_ID\"}" &
done
wait
```

**기대 동작**: 3개 빌드 모두 독립적으로 생성 (build_number 각각 상이)

---

## TC-C5: 빌드 조회

```bash
curl -X POST http://localhost:8083/v1/builds/get \
  -H "Content-Type: application/json" \
  -d "{
    \"pipeline_id\": \"$PIPELINE_ID\",
    \"build_number\": 1
  }"
```

---

## TC-C6: 빌드 이력 조회

```bash
# 최근 5개
curl -X POST http://localhost:8083/v1/builds/list \
  -H "Content-Type: application/json" \
  -d "{
    \"pipeline_id\": \"$PIPELINE_ID\",
    \"limit\": 5
  }"
```

---

## TC-C7: 빌드 로그 조회

```bash
curl -X POST http://localhost:8083/v1/builds/log \
  -H "Content-Type: application/json" \
  -d "{
    \"pipeline_id\": \"$PIPELINE_ID\",
    \"build_number\": 1
  }"
```

**기대 응답**:

```json
{
  "log": "Started by user admin\n[Pipeline] Start of Pipeline\n[Build] go build ./...\n...\nFinished: SUCCESS"
}
```

### 엣지 케이스: 실행 중 로그 조회

빌드가 RUNNING 상태일 때 로그 조회:

```bash
# 빌드 트리거 직후 즉시 로그 조회
curl -X POST http://localhost:8083/v1/builds/log \
  -H "Content-Type: application/json" \
  -d "{\"pipeline_id\": \"$PIPELINE_ID\", \"build_number\": 1}"
```

**기대 동작**: 현재까지 출력된 로그 반환 (불완전할 수 있음)

### 엣지 케이스: 빌드 타임아웃

`timeout_seconds`를 매우 짧게 설정 후 장시간 명령어 실행:

```bash
# stage timeout: 5초, command: sleep 60
curl -X POST http://localhost:8083/v1/builds/trigger -d '...'
# 5초 후 빌드 상태 확인
curl -X POST http://localhost:8083/v1/builds/get -d "{...}"
```

**기대 동작**: status: ABORTED, 타임아웃 메시지가 로그에 포함

---

## TC-C8: 파이프라인 삭제

```bash
curl -X POST http://localhost:8083/v1/pipelines/delete \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$PIPELINE_ID\"}"
```

**기대 응답**: `{"success": true}`

삭제 후 조회 시 `404` 반환 확인:

```bash
curl -X POST http://localhost:8083/v1/pipelines/get \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$PIPELINE_ID\"}"
```

---

## 시나리오 요약

| TC | RPC | 시나리오 | 기대 결과 |
|----|-----|----------|----------|
| C1 | CreatePipeline | 정상 생성 | 파이프라인 UUID 반환 |
| C1-E | CreatePipeline | ci_config 누락 | 400 Bad Request |
| C2 | ListPipelines | 전체 / 저장소 필터 | 목록 반환 |
| C3 | GetPipeline | 정상 조회 | 파이프라인 반환 |
| C3-E | GetPipeline | ID 미존재 | 404 Not Found |
| C4 | TriggerBuild | 정상 트리거 | QUEUED 빌드 반환 |
| C4-E1 | TriggerBuild | Jenkins 오프라인 | FAILURE 빌드 반환 |
| C4-E2 | TriggerBuild | 동시 트리거 3개 | 3개 빌드 독립 생성 |
| C5 | GetBuild | 빌드 조회 | 빌드 상태 반환 |
| C6 | ListBuilds | 이력 조회 | 최근 N개 반환 |
| C7 | GetBuildLog | 로그 조회 | 콘솔 로그 반환 |
| C7-E | GetBuildLog | 타임아웃 빌드 | ABORTED + 타임아웃 로그 |
| C8 | DeletePipeline | 삭제 후 재조회 | success:true, 재조회 404 |
