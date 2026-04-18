#!/bin/bash
# =============================================================================
# E2E 테스트: GitHub PR 병합 → Workflow → Jenkins 배포
# =============================================================================
#
# 사전 조건: docker compose up -d (모든 서비스 healthy)
#
# 흐름:
#   1. Jenkins에 테스트 Job 생성
#   2. git-provider에 파이프라인 등록
#   3. git-provider에 워크플로우 등록
#   4. GitHub PR 병합 webhook 시뮬레이션 (→ Redpanda Connect)
#   5. 실행 결과 확인
# =============================================================================

set -uo pipefail

# 색상
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

JENKINS_URL="http://localhost:9090"
JENKINS_USER="admin"
JENKINS_PASS="admin"
GIT_PROVIDER_URL="http://localhost:8083"
CONNECT_URL="http://localhost:4195"
# Streams 모드에서는 /{stream_id}/path 형태
GITHUB_WEBHOOK_URL="$CONNECT_URL/github/webhook/github"

step() { echo -e "\n${CYAN}━━━ Step $1: $2 ━━━${NC}"; }
ok()   { echo -e "${GREEN}✓ $1${NC}"; }
fail() { echo -e "${RED}✗ $1${NC}"; exit 1; }
info() { echo -e "${YELLOW}  → $1${NC}"; }

# =============================================================================
# 0. 서비스 헬스체크
# =============================================================================
step 0 "서비스 상태 확인"

check_service() {
    local name=$1 url=$2
    if curl -sf -o /dev/null --max-time 5 "$url"; then
        ok "$name 정상"
    else
        fail "$name 응답 없음 ($url). docker compose up -d 먼저 실행하세요."
    fi
}

check_service_post() {
    local name=$1 url=$2
    if curl -sf -o /dev/null --max-time 5 -X POST -H 'Content-Type: application/json' -d '{}' "$url"; then
        ok "$name 정상"
    else
        fail "$name 응답 없음 ($url). docker compose up -d 먼저 실행하세요."
    fi
}

check_service_post "git-provider" "$GIT_PROVIDER_URL/v1/pipelines/list"
check_service "Jenkins"      "$JENKINS_URL/login"
# Redpanda Connect는 streams 모드에서 /ready 없음 — ping으로 확인
check_service "Redpanda Connect" "$CONNECT_URL/ping"

# =============================================================================
# 1. Jenkins에 테스트 Job 생성 (deploy-prod)
# =============================================================================
step 1 "Jenkins 'deploy-prod' Job 생성"

# Jenkins 쿠키 jar (CSRF crumb + session cookie 필요)
JENKINS_COOKIE=$(mktemp)
JENKINS_CRUMB=$(curl -sf -u "$JENKINS_USER:$JENKINS_PASS" -c "$JENKINS_COOKIE" \
    "$JENKINS_URL/crumbIssuer/api/json" 2>/dev/null \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['crumb'])" 2>/dev/null || echo "")
if [ -n "$JENKINS_CRUMB" ]; then
    info "Jenkins CRUMB 획득 완료"
else
    info "Jenkins CRUMB 없음"
fi

# Job이 이미 있는지 확인
if curl -s -o /dev/null -w "%{http_code}" -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/job/deploy-prod/api/json" 2>/dev/null | grep -q "200"; then
    ok "deploy-prod Job 이미 존재 (스킵)"
else
    JOB_XML='<?xml version="1.0" encoding="UTF-8"?>
<project>
  <description>E2E 테스트용 배포 파이프라인</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>BRANCH</name>
          <defaultValue>main</defaultValue>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>COMMIT_SHA</name>
          <defaultValue></defaultValue>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <builders>
    <hudson.tasks.Shell>
      <command>
echo "========================================="
echo "  Deploying branch: ${BRANCH}"
echo "  Commit: ${COMMIT_SHA}"
echo "========================================="
echo "Step 1/3: Pulling latest code..."
sleep 2
echo "Step 2/3: Building application..."
sleep 2
echo "Step 3/3: Deploying to production..."
sleep 1
echo "========================================="
echo "  Deploy SUCCESS!"
echo "========================================="
      </command>
    </hudson.tasks.Shell>
  </builders>
</project>'

    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
        -u "$JENKINS_USER:$JENKINS_PASS" \
        -b "$JENKINS_COOKIE" \
        -H "Content-Type: application/xml" \
        -H "Jenkins-Crumb: $JENKINS_CRUMB" \
        -d "$JOB_XML" \
        "$JENKINS_URL/createItem?name=deploy-prod")

    if [ "$HTTP_CODE" = "200" ]; then
        ok "deploy-prod Job 생성 완료"
    else
        fail "Jenkins Job 생성 실패 (HTTP $HTTP_CODE)"
    fi
fi

# =============================================================================
# 2. git-provider에 파이프라인 등록
# =============================================================================
step 2 "파이프라인 등록 (deploy-prod → Jenkins)"

PIPELINE_RESP=$(curl -sf -X POST "$GIT_PROVIDER_URL/v1/pipelines/create" \
    -H 'Content-Type: application/json' \
    -d '{
        "name": "deploy-prod",
        "repository": "team/app",
        "branch_pattern": "main",
        "jenkins_job_name": "deploy-prod",
        "ci_config": {
            "jenkins": {
                "url": "http://jenkins:8080",
                "username": "admin",
                "api_token": "admin"
            }
        }
    }')

PIPELINE_ID=$(echo "$PIPELINE_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['pipeline']['id'])" 2>/dev/null || echo "")
if [ -n "$PIPELINE_ID" ]; then
    ok "파이프라인 등록: $PIPELINE_ID"
else
    fail "파이프라인 등록 실패: $PIPELINE_RESP"
fi

# =============================================================================
# 3. 워크플로우 등록 (PR 병합 → deploy 파이프라인 실행)
# =============================================================================
step 3 "워크플로우 등록 (mr_merged → deploy)"

WORKFLOW_RESP=$(curl -sf -X POST "$GIT_PROVIDER_URL/v1/workflows/create" \
    -H 'Content-Type: application/json' \
    -d "{
        \"name\": \"deploy-on-merge\",
        \"trigger_event\": \"mr_merged\",
        \"filter\": {
            \"repository\": \"team/app\",
            \"branch\": \"main\"
        },
        \"steps\": [
            {
                \"name\": \"deploy\",
                \"type\": \"cicd_build\",
                \"pipeline_id\": \"$PIPELINE_ID\"
            }
        ]
    }")

WORKFLOW_ID=$(echo "$WORKFLOW_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['workflow']['id'])" 2>/dev/null || echo "")
if [ -n "$WORKFLOW_ID" ]; then
    ok "워크플로우 등록: $WORKFLOW_ID"
else
    fail "워크플로우 등록 실패: $WORKFLOW_RESP"
fi

# =============================================================================
# 4. GitHub PR 병합 시뮬레이션 (Redpanda Connect webhook)
# =============================================================================
step 4 "GitHub PR 병합 webhook 시뮬레이션"

WEBHOOK_CODE=$(curl -sf -o /dev/null -w "%{http_code}" \
    -X POST "$GITHUB_WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -H 'X-GitHub-Event: pull_request' \
    -d '{
        "action": "closed",
        "pull_request": {
            "merged": true,
            "base": {"ref": "main"},
            "merge_commit_sha": "abc123def456",
            "merged_by": {"login": "dev1"}
        },
        "repository": {
            "full_name": "team/app"
        }
    }')

if [ "$WEBHOOK_CODE" = "200" ]; then
    ok "Webhook 전송 성공 (HTTP $WEBHOOK_CODE)"
else
    fail "Webhook 전송 실패 (HTTP $WEBHOOK_CODE)"
fi

# =============================================================================
# 5. 결과 확인 (폴링)
# =============================================================================
step 5 "실행 결과 확인 (최대 90초 대기)"

info "워크플로우가 이벤트를 처리하고 Jenkins 빌드가 완료될 때까지 대기..."

for i in $(seq 1 18); do
    sleep 5

    # exec-1이 생성되었는지 확인
    EXEC_RESP=$(curl -sf -X POST "$GIT_PROVIDER_URL/v1/executions/get" \
        -H 'Content-Type: application/json' \
        -d '{"execution_id": "exec-1"}' 2>/dev/null || echo '{"error":"not found"}')

    STATUS=$(echo "$EXEC_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('execution',{}).get('status',''))" 2>/dev/null || echo "")

    case "$STATUS" in
        "EXECUTION_STATUS_COMPLETED"|"3")
            echo ""
            ok "워크플로우 실행 완료!"
            echo ""
            info "Execution 상세:"
            echo "$EXEC_RESP" | python3 -m json.tool 2>/dev/null || echo "$EXEC_RESP"
            echo ""
            echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${GREEN}  E2E 테스트 성공!${NC}"
            echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            exit 0
            ;;
        "EXECUTION_STATUS_FAILED"|"4")
            echo ""
            fail "워크플로우 실행 실패: $EXEC_RESP"
            ;;
        *)
            printf "  [%2d/18] 대기중... (status: %s)\r" "$i" "$STATUS"
            ;;
    esac
done

echo ""
fail "타임아웃: 90초 내에 워크플로우가 완료되지 않음. 로그를 확인하세요: docker compose logs git-provider"
