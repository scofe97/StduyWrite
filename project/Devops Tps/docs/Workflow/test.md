# Workflow E2E 테스트 시나리오

서버 주소: `localhost:8083` (REST gateway)
Redpanda Connect webhook 엔드포인트: `localhost:8090`

---

## 사전 준비

```bash
# 서버 실행 확인
curl -s -X POST http://localhost:8083/v1/workflows/list -d '{}' | jq .

# Redpanda Connect 실행 확인
curl -s http://localhost:8090/health || echo "Connect 미실행"

# Kafka 토픽 확인
rpk topic list
# git-events, cicd-results 토픽이 있어야 한다

# 파이프라인 사전 등록 (워크플로우 스텝에서 참조)
PIPELINE_ID=$(curl -s -X POST http://localhost:8083/v1/pipelines/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "backend-build",
    "repository": "my-org/backend",
    "branch_pattern": "main",
    "ci_config": {"jenkins": {"url": "http://localhost:8080", "username": "admin", "api_token": "11abc"}},
    "jenkins_job_name": "backend-build"
  }' | jq -r '.pipeline.id')
echo "PIPELINE_ID: $PIPELINE_ID"
```

---

## TC-W1: 워크플로우 생성

### 정상: mr_merged 트리거 워크플로우 등록

```bash
curl -X POST http://localhost:8083/v1/workflows/create \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"backend-deploy-on-merge\",
    \"trigger_event\": \"mr_merged\",
    \"filter\": {
      \"repository\": \"my-org/backend\",
      \"branch\": \"main\"
    },
    \"steps\": [
      {\"name\": \"build\", \"type\": \"cicd_build\", \"pipeline_id\": \"$PIPELINE_ID\"}
    ]
  }"
```

**기대 응답**:

```json
{
  "workflow": {
    "id": "...",
    "name": "backend-deploy-on-merge",
    "trigger_event": "mr_merged",
    "filter": {"repository": "my-org/backend", "branch": "main"},
    "steps": [{"name": "build", "type": "cicd_build", "pipeline_id": "..."}]
  }
}
```

### 정상: push 트리거 + 다중 스텝

```bash
DEPLOY_PIPELINE_ID="..."   # 별도 배포 파이프라인 ID

curl -X POST http://localhost:8083/v1/workflows/create \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"build-and-deploy\",
    \"trigger_event\": \"push\",
    \"filter\": {\"repository\": \"my-org/backend\", \"branch\": \"develop\"},
    \"steps\": [
      {\"name\": \"build\",  \"type\": \"cicd_build\", \"pipeline_id\": \"$PIPELINE_ID\"},
      {\"name\": \"deploy\", \"type\": \"cicd_build\", \"pipeline_id\": \"$DEPLOY_PIPELINE_ID\"}
    ]
  }"
```

**기대 동작**: 2개 스텝이 순차적으로 실행된다. build 스텝 완료 후 deploy 스텝이 시작된다.

---

## TC-W2: 워크플로우 목록 조회

```bash
# 전체 조회
curl -s -X POST http://localhost:8083/v1/workflows/list \
  -H "Content-Type: application/json" \
  -d '{}' | jq .

# 저장소 필터
curl -s -X POST http://localhost:8083/v1/workflows/list \
  -H "Content-Type: application/json" \
  -d '{"repository": "my-org/backend"}' | jq .
```

---

## TC-W3: E2E — Webhook → 워크플로우 자동 실행

이 시나리오는 전체 파이프라인을 검증하는 핵심 E2E 테스트다.

### 3-1: GitLab MR merge webhook 시뮬레이션

```bash
WORKFLOW_ID="..."   # TC-W1에서 생성한 워크플로우 ID

# Redpanda Connect webhook 엔드포인트로 GitLab MR merge 이벤트 전송
curl -X POST http://localhost:8090/webhook \
  -H "Content-Type: application/json" \
  -H "X-Gitlab-Event: Merge Request Hook" \
  -d '{
    "object_kind": "merge_request",
    "project": {
      "path_with_namespace": "my-org/backend"
    },
    "object_attributes": {
      "state": "merged",
      "target_branch": "main",
      "last_commit": {
        "id": "abc123def456"
      }
    }
  }'
```

**기대 동작**:
1. Redpanda Connect가 이벤트를 `git-events` 토픽에 발행한다.
2. git-provider 컨슈머가 이벤트를 소비하고 워크플로우를 매칭한다.
3. Execution이 생성된다.

### 3-2: 실행 상태 폴링

```bash
# 워크플로우의 실행 이력 조회
curl -X POST http://localhost:8083/v1/executions/list \
  -H "Content-Type: application/json" \
  -d "{\"workflow_id\": \"$WORKFLOW_ID\", \"limit\": 5}" | jq .
```

**기대 응답** (webhook 수신 직후):

```json
{
  "executions": [
    {
      "id": "exec-uuid",
      "workflow_id": "...",
      "status": "EXECUTION_STATUS_WAITING_FOR_STEP",
      "current_step": 0,
      "branch": "main",
      "commit_sha": "abc123def456",
      "steps": [
        {"name": "build", "status": "running", "started_at": "..."}
      ]
    }
  ]
}
```

### 3-3: 실행 상세 조회 (스텝별 상태)

```bash
EXECUTION_ID="exec-uuid"

curl -X POST http://localhost:8083/v1/executions/get \
  -H "Content-Type: application/json" \
  -d "{\"execution_id\": \"$EXECUTION_ID\"}" | jq .
```

### 3-4: 빌드 결과 확인

Jenkins 빌드 완료 후 빌드 상태 조회:

```bash
curl -X POST http://localhost:8083/v1/builds/get \
  -H "Content-Type: application/json" \
  -d "{\"pipeline_id\": \"$PIPELINE_ID\", \"build_number\": 1}" | jq .
```

**기대 결과**: `status: BUILD_STATUS_SUCCESS`, Execution은 `EXECUTION_STATUS_COMPLETED`

---

## TC-W4: 엣지 케이스

### 4-1: 매칭 워크플로우 없음

필터가 다른 브랜치(`develop`)로 설정된 워크플로우만 있을 때 `main` 브랜치 이벤트 전송:

```bash
curl -X POST http://localhost:8090/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "object_kind": "merge_request",
    "project": {"path_with_namespace": "my-org/backend"},
    "object_attributes": {"state": "merged", "target_branch": "feature/test", "last_commit": {"id": "xyz"}}
  }'
```

**기대 동작**: 이벤트 무시, Execution 생성 없음. `executions/list` 결과 변화 없음.

### 4-2: 스텝 실패 시 Execution FAILED

Jenkins 빌드가 실패하도록 설정된 파이프라인으로 워크플로우 실행:

```bash
# 실패하는 파이프라인으로 워크플로우 생성 후 이벤트 트리거
# ... (webhook 전송)

# 빌드 실패 후 Execution 상태 확인
curl -X POST http://localhost:8083/v1/executions/get \
  -H "Content-Type: application/json" \
  -d "{\"execution_id\": \"$EXECUTION_ID\"}" | jq '.execution.status'
```

**기대 결과**: `"EXECUTION_STATUS_FAILED"`, 실패한 스텝의 `status: "failure"`

### 4-3: Jenkins 연결 불가

Jenkins 서버 중단 상태에서 워크플로우 실행:

**기대 동작**: Execution이 생성되고 CICDService가 빌드 트리거를 시도하지만 실패한다. Execution status는 FAILED, 스텝 status는 failure로 기록된다.

### 4-4: 다중 스텝 순차 실행 검증

2개 스텝 워크플로우에서 각 스텝이 순서대로 실행되는지 확인:

```bash
# 2스텝 워크플로우 이벤트 트리거 후
# 짧은 간격으로 Execution 상태 폴링
for i in {1..10}; do
  curl -s -X POST http://localhost:8083/v1/executions/get \
    -d "{\"execution_id\": \"$EXECUTION_ID\"}" | jq '{status: .execution.status, step: .execution.current_step}'
  sleep 5
done
```

**기대 흐름**:
1. `WAITING_FOR_STEP`, `current_step: 0` (스텝1 빌드 대기)
2. `RUNNING`, `current_step: 1` (스텝2 시작)
3. `WAITING_FOR_STEP`, `current_step: 1` (스텝2 빌드 대기)
4. `COMPLETED` (모든 스텝 완료)

---

## TC-W5: 워크플로우 삭제

```bash
curl -X POST http://localhost:8083/v1/workflows/delete \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$WORKFLOW_ID\"}"
```

삭제 후 동일 이벤트 전송 시 Execution이 생성되지 않아야 한다.

---

## 시나리오 요약

| TC | 항목 | 시나리오 | 기대 결과 |
|----|------|----------|----------|
| W1 | CreateWorkflow | 정상 생성 | 워크플로우 UUID 반환 |
| W1 | CreateWorkflow | 다중 스텝 | 스텝 순서 보존 |
| W2 | ListWorkflows | 저장소 필터 | 해당 저장소 워크플로우만 반환 |
| W3 | E2E | webhook → 실행 → 완료 | COMPLETED, 빌드 SUCCESS |
| W4-1 | 이벤트 라우팅 | 매칭 없음 | Execution 미생성 |
| W4-2 | 스텝 실패 | 빌드 FAILURE | Execution FAILED |
| W4-3 | Jenkins 불가 | 연결 오류 | Execution FAILED |
| W4-4 | 다중 스텝 | 순차 실행 | current_step 0→1, 최종 COMPLETED |
| W5 | DeleteWorkflow | 삭제 후 이벤트 | Execution 미생성 |
