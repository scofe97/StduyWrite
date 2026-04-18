# Repository 테스트

## API 테스트 시나리오

| RPC | 시나리오 | 입력 | 기대 결과 |
|-----|---------|------|----------|
| ListRepositories | GitHub 조직 저장소 목록 | 유효한 ghp_ 토큰, namespace="my-org" | repositories 배열 반환 |
| ListRepositories | GitLab 그룹 저장소 목록 | glpat- 토큰 + namespace="dev-team" | repositories 배열 반환 |
| ListRepositories | Bitbucket workspace 목록 | email + api_token + workspace | repositories 배열 반환 |
| ListRepositories | provider 누락 | provider 없음 | INVALID_ARGUMENT 에러 |
| GetRepository | GitHub 단일 조회 | owner + repo 이름 | Repository 반환 |
| GetRepository | 존재하지 않는 저장소 | 없는 repo 이름 | NOT_FOUND 에러 |
| GetRepository | 인증 실패 | 만료된 토큰 | UNAUTHENTICATED 에러 |
| CreateRepository | GitHub Organization 저장소 생성 | 유효한 토큰 + namespace + name | Repository 반환, status=200 |
| CreateRepository | GitLab Subgroup 저장소 생성 | glpat- 토큰 + base_url + namespace | Repository 반환 |
| CreateRepository | Bitbucket 저장소 생성 | email + api_token + workspace + name | Repository 반환 |
| CreateRepository | 이름 중복 | 이미 존재하는 name | ALREADY_EXISTS 에러 |
| CreateRepository | 권한 부족 | read-only 토큰 | PERMISSION_DENIED 에러 |
| DeleteRepository | 정상 삭제 | 유효한 토큰 + namespace + repo | success=true |
| DeleteRepository | delete_repo 스코프 없음 (GitHub) | repo 스코프만 있는 토큰 | PERMISSION_DENIED 에러 |
| DeleteRepository | 존재하지 않는 저장소 | 없는 repo 이름 | NOT_FOUND 에러 |

---

## curl 예시

### ListRepositories - GitHub

```bash
# GitHub - 조직 저장소 목록
curl -X POST http://localhost:8080/v1/repositories/list \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "github": { "token": "ghp_xxxxxxxxxxxxxxxxxxxx" }
    },
    "namespace": "my-organization"
  }'

# 응답 예시
{
  "repositories": [
    {
      "id": "123456789",
      "name": "backend-api",
      "full_name": "my-organization/backend-api",
      "url": "https://github.com/my-organization/backend-api",
      "clone_url": "https://github.com/my-organization/backend-api.git",
      "ssh_url": "git@github.com:my-organization/backend-api.git",
      "default_branch": "main",
      "private": true,
      "namespace": {
        "id": "98765",
        "name": "my-organization",
        "type": "NAMESPACE_TYPE_ORGANIZATION"
      }
    }
  ]
}
```

### ListRepositories - GitLab Self-hosted

```bash
curl -X POST http://localhost:8080/v1/repositories/list \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "gitlab": {
        "token": "glpat-xxxxxxxxxxxxxxxxxxxx",
        "base_url": "https://gitlab.company.com"
      }
    },
    "namespace": "dev-team"
  }'
```

### ListRepositories - Bitbucket

```bash
curl -X POST http://localhost:8080/v1/repositories/list \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "bitbucket": {
        "email": "devops@company.com",
        "api_token": "ATATT3xFfGF0xxxxxxxxxxxxxxxx",
        "workspace": "my-workspace"
      }
    }
  }'
```

---

### GetRepository

```bash
# GitHub
curl -X POST http://localhost:8080/v1/repositories/get \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "github": { "token": "ghp_xxxxxxxxxxxxxxxxxxxx" }
    },
    "namespace": "my-organization",
    "repository": "backend-api"
  }'

# GitLab (Subgroup 경로)
curl -X POST http://localhost:8080/v1/repositories/get \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "gitlab": {
        "token": "glpat-xxxxxxxxxxxxxxxxxxxx",
        "base_url": "https://gitlab.company.com"
      }
    },
    "namespace": "dev-team/backend",
    "repository": "api-gateway"
  }'

# Bitbucket (workspace는 Config에 포함)
curl -X POST http://localhost:8080/v1/repositories/get \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "bitbucket": {
        "email": "devops@company.com",
        "api_token": "ATATT3xFfGF0xxxxxxxxxxxxxxxx",
        "workspace": "my-workspace"
      }
    },
    "repository": "data-pipeline"
  }'

# 응답 예시 (공통)
{
  "repository": {
    "id": "123456789",
    "name": "backend-api",
    "full_name": "my-organization/backend-api",
    "description": "Backend API service",
    "url": "https://github.com/my-organization/backend-api",
    "clone_url": "https://github.com/my-organization/backend-api.git",
    "ssh_url": "git@github.com:my-organization/backend-api.git",
    "default_branch": "main",
    "private": true,
    "namespace": {
      "id": "98765",
      "name": "my-organization",
      "type": "NAMESPACE_TYPE_ORGANIZATION"
    },
    "created_at": "2026-01-15T10:30:00Z"
  }
}
```

---

### CreateRepository

```bash
# GitHub - Organization 저장소
curl -X POST http://localhost:8080/v1/repositories \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "github": { "token": "ghp_xxxxxxxxxxxxxxxxxxxx" }
    },
    "namespace": "my-organization",
    "name": "new-service",
    "description": "New microservice repository",
    "private": true
  }'

# GitLab - Subgroup 저장소 (Self-hosted)
curl -X POST http://localhost:8080/v1/repositories \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "gitlab": {
        "token": "glpat-xxxxxxxxxxxxxxxxxxxx",
        "base_url": "https://gitlab.company.com"
      }
    },
    "namespace": "dev-team/backend",
    "name": "api-gateway",
    "description": "API Gateway service",
    "private": true
  }'

# Bitbucket - Workspace 저장소
curl -X POST http://localhost:8080/v1/repositories \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "bitbucket": {
        "email": "devops@company.com",
        "api_token": "ATATT3xFfGF0xxxxxxxxxxxxxxxx",
        "workspace": "my-workspace"
      }
    },
    "name": "data-pipeline",
    "description": "Data processing pipeline",
    "private": true
  }'

# 응답 예시
{
  "repository": {
    "id": "987654321",
    "name": "new-service",
    "full_name": "my-organization/new-service",
    "url": "https://github.com/my-organization/new-service",
    "clone_url": "https://github.com/my-organization/new-service.git",
    "ssh_url": "git@github.com:my-organization/new-service.git",
    "default_branch": "main",
    "private": true,
    "namespace": {
      "id": "98765",
      "name": "my-organization",
      "type": "NAMESPACE_TYPE_ORGANIZATION"
    },
    "created_at": "2026-02-28T09:00:00Z"
  }
}
```

---

### DeleteRepository

```bash
# GitHub (delete_repo 스코프 필요)
curl -X POST http://localhost:8080/v1/repositories/delete \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "github": { "token": "ghp_xxxxxxxxxxxxxxxxxxxx" }
    },
    "namespace": "my-organization",
    "repository": "old-service"
  }'

# GitLab
curl -X POST http://localhost:8080/v1/repositories/delete \
  -H 'Content-Type: application/json' \
  -d '{
    "provider": {
      "gitlab": { "token": "glpat-xxxxxxxxxxxxxxxxxxxx" }
    },
    "namespace": "dev-team",
    "repository": "old-project"
  }'

# 응답 예시
{
  "success": true
}
```

---

### grpcurl 예시

```bash
# ListRepositories
grpcurl -plaintext -d '{
  "provider": {
    "github": { "token": "ghp_xxxxxxxxxxxxxxxxxxxx" }
  },
  "namespace": "my-organization"
}' localhost:50051 provider.GitService/ListRepositories

# CreateRepository
grpcurl -plaintext -d '{
  "provider": {
    "gitlab": {
      "token": "glpat-xxxxxxxxxxxxxxxxxxxx",
      "base_url": "https://gitlab.company.com"
    }
  },
  "namespace": "dev-team/backend",
  "name": "new-service",
  "description": "New service",
  "private": true
}' localhost:50051 provider.GitService/CreateRepository

# DeleteRepository
grpcurl -plaintext -d '{
  "provider": {
    "github": { "token": "ghp_xxxxxxxxxxxxxxxxxxxx" }
  },
  "namespace": "my-organization",
  "repository": "old-service"
}' localhost:50051 provider.GitService/DeleteRepository
```

---

## 에지 케이스

| 케이스 | 입력 | 기대 동작 |
|--------|------|----------|
| provider 필드 누락 | `{}` | INVALID_ARGUMENT: provider is required |
| repository 필드 누락 | provider만 있음 | INVALID_ARGUMENT: repository is required |
| GitHub namespace 누락 | GitHub + repository만 있음 | INVALID_ARGUMENT: namespace is required for GitHub |
| 잘못된 base_url (GitLab) | `base_url: "not-a-url"` | INVALID_ARGUMENT: invalid base_url |
| Bitbucket workspace 누락 | email + api_token만 있음 | INVALID_ARGUMENT: workspace is required |
| Bitbucket email 누락 | api_token + workspace만 있음 | INVALID_ARGUMENT: email is required |
| 만료된 토큰 | 만료된 ghp_ 토큰 | UNAUTHENTICATED: token expired |
| 저장소명 중복 | 이미 존재하는 name | ALREADY_EXISTS |
| Provider API 타임아웃 | 느린 네트워크 환경 | INTERNAL: context deadline exceeded |
| 대규모 목록 | 저장소 1,000개 이상인 workspace | 전체 반환 (페이지네이션 미구현으로 성능 주의) |

---

## E2E 테스트

### 테스트 환경 준비

```bash
# git-provider 서버 실행
cd git-provider
make run-server
# gRPC :50051, REST :8080 기동 확인

# 또는 Docker Compose 사용
docker-compose up git-provider
```

### E2E 시나리오: 저장소 생성 → 조회 → 삭제

```bash
#!/bin/bash
# e2e-repository.sh

BASE_URL="http://localhost:8080"
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
ORG="my-organization"
REPO_NAME="e2e-test-$(date +%s)"

echo "=== E2E: Repository CRUD ==="

# 1. 저장소 생성
echo "[1] CreateRepository..."
CREATE_RESP=$(curl -s -X POST "$BASE_URL/v1/repositories" \
  -H 'Content-Type: application/json' \
  -d "{
    \"provider\": {\"github\": {\"token\": \"$GITHUB_TOKEN\"}},
    \"namespace\": \"$ORG\",
    \"name\": \"$REPO_NAME\",
    \"description\": \"E2E test repository\",
    \"private\": true
  }")

echo "$CREATE_RESP" | jq .
REPO_ID=$(echo "$CREATE_RESP" | jq -r '.repository.id')
echo "Created: $REPO_ID"

# 2. 저장소 조회
echo "[2] GetRepository..."
curl -s -X POST "$BASE_URL/v1/repositories/get" \
  -H 'Content-Type: application/json' \
  -d "{
    \"provider\": {\"github\": {\"token\": \"$GITHUB_TOKEN\"}},
    \"namespace\": \"$ORG\",
    \"repository\": \"$REPO_NAME\"
  }" | jq .

# 3. 목록 조회 (생성된 저장소 포함 확인)
echo "[3] ListRepositories..."
curl -s -X POST "$BASE_URL/v1/repositories/list" \
  -H 'Content-Type: application/json' \
  -d "{
    \"provider\": {\"github\": {\"token\": \"$GITHUB_TOKEN\"}},
    \"namespace\": \"$ORG\"
  }" | jq '.repositories | length'

# 4. 저장소 삭제
echo "[4] DeleteRepository..."
curl -s -X POST "$BASE_URL/v1/repositories/delete" \
  -H 'Content-Type: application/json' \
  -d "{
    \"provider\": {\"github\": {\"token\": \"$GITHUB_TOKEN\"}},
    \"namespace\": \"$ORG\",
    \"repository\": \"$REPO_NAME\"
  }" | jq .

echo "=== E2E 완료 ==="
```

### 스크립트 실행

```bash
chmod +x e2e-repository.sh
./e2e-repository.sh
```

### E2E 시나리오: TPS 연동 흐름

```bash
#!/bin/bash
# e2e-tps-repository.sh
# TPS Backend를 통한 전체 흐름 테스트

TPS_URL="http://localhost:8090"
PROJECT_ID="550e8400-e29b-41d4-a716-446655440000"
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# 1. Provider 등록 (git-provider 직접 호출이 아닌 TPS API)
PROVIDER_RESP=$(curl -s -X POST "$TPS_URL/api/connections" \
  -H 'Content-Type: application/json' \
  -d "{
    \"projectId\": \"$PROJECT_ID\",
    \"providerType\": \"GITHUB\",
    \"name\": \"e2e-github\",
    \"token\": \"$GITHUB_TOKEN\"
  }")

CONNECTION_ID=$(echo "$PROVIDER_RESP" | jq -r '.id')
echo "Connection: $CONNECTION_ID"

# 2. TPS를 통한 저장소 생성 (git-provider gRPC 내부 호출)
REPO_RESP=$(curl -s -X POST "$TPS_URL/api/repositories" \
  -H 'Content-Type: application/json' \
  -d "{
    \"projectId\": \"$PROJECT_ID\",
    \"connectionId\": \"$CONNECTION_ID\",
    \"namespace\": \"my-organization\",
    \"name\": \"e2e-service\",
    \"private\": true
  }")

echo "$REPO_RESP" | jq .
```
