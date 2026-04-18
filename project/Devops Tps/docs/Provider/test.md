# Provider 테스트

## API 테스트 시나리오

| RPC | 시나리오 | 입력 | 기대 결과 |
|-----|---------|------|----------|
| RegisterProvider | GitHub 정상 등록 | 유효한 ghp_ 토큰, name="github-main" | provider_id 반환, status=201 |
| RegisterProvider | GitLab self-hosted 등록 | glpat- 토큰 + base_url | provider_id 반환 |
| RegisterProvider | Bitbucket 등록 | email + app_password + workspace | provider_id 반환 |
| RegisterProvider | 이름 중복 | 이미 등록된 name | ALREADY_EXISTS 에러 |
| RegisterProvider | 빈 토큰 | token="" | INVALID_ARGUMENT 에러 |
| GetProvider | 정상 조회 | 유효한 provider_id | Provider 정보 반환 |
| GetProvider | 존재하지 않는 ID | 없는 UUID | NOT_FOUND 에러 |
| ListProviders | 전체 목록 조회 | project_id | 등록된 목록 반환 |
| ListProviders | 타입 필터 | type="GITHUB" | GitHub만 반환 |
| DeleteProvider | 정상 삭제 | 유효한 provider_id | success=true |
| DeleteProvider | 참조 있는 삭제 | Repository가 연결된 provider_id | FAILED_PRECONDITION 에러 |

---

## curl 예시

### RegisterProvider - GitHub

```bash
# REST Gateway (:8080) 사용
curl -X POST http://localhost:8080/v1/providers \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "github-main",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "provider": {
      "github": {
        "token": "ghp_xxxxxxxxxxxxxxxxxxxx"
      }
    }
  }'

# 응답 예시
{
  "provider_id": "b4434b4d-6a0e-4f57-8d75-e02a824abeb0",
  "name": "github-main",
  "type": "GITHUB",
  "created_at": "2026-02-28T09:00:00Z"
}
```

### RegisterProvider - GitLab Self-hosted

```bash
curl -X POST http://localhost:8080/v1/providers \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "gitlab-company",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "provider": {
      "gitlab": {
        "token": "glpat-xxxxxxxxxxxxxxxxxxxx",
        "base_url": "https://gitlab.company.com"
      }
    }
  }'
```

### RegisterProvider - Bitbucket

```bash
curl -X POST http://localhost:8080/v1/providers \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "bitbucket-workspace",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "provider": {
      "bitbucket": {
        "email": "devops@company.com",
        "api_token": "ATATT3xFfGF0xxxxxxxxxxxxxxxx",
        "workspace": "my-workspace"
      }
    }
  }'
```

### GetProvider

```bash
curl -X GET http://localhost:8080/v1/providers/b4434b4d-6a0e-4f57-8d75-e02a824abeb0 \
  -H 'Content-Type: application/json'

# 응답 예시
{
  "provider_id": "b4434b4d-6a0e-4f57-8d75-e02a824abeb0",
  "name": "github-main",
  "type": "GITHUB",
  "base_url": "https://api.github.com",
  "created_at": "2026-02-28T09:00:00Z"
}
```

### ListProviders

```bash
# 전체 목록
curl -X GET "http://localhost:8080/v1/providers?project_id=550e8400-e29b-41d4-a716-446655440000" \
  -H 'Content-Type: application/json'

# 타입 필터
curl -X GET "http://localhost:8080/v1/providers?project_id=550e8400-e29b-41d4-a716-446655440000&type=GITHUB" \
  -H 'Content-Type: application/json'
```

### DeleteProvider

```bash
curl -X DELETE http://localhost:8080/v1/providers/b4434b4d-6a0e-4f57-8d75-e02a824abeb0 \
  -H 'Content-Type: application/json'

# 응답 예시
{
  "success": true,
  "message": "Provider deleted successfully"
}
```

### grpcurl 예시

```bash
# grpcurl 사용 (gRPC 직접 호출)
grpcurl -plaintext -d '{
  "name": "github-main",
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "provider": {
    "github": {
      "token": "ghp_xxxxxxxxxxxxxxxxxxxx"
    }
  }
}' localhost:50051 provider.ProviderService/RegisterProvider

# 목록 조회
grpcurl -plaintext -d '{
  "project_id": "550e8400-e29b-41d4-a716-446655440000"
}' localhost:50051 provider.ProviderService/ListProviders
```

---

## 에지 케이스

| 케이스 | 입력 | 기대 동작 |
|--------|------|----------|
| 빈 token | `token: ""` | INVALID_ARGUMENT: token is required |
| 잘못된 base_url 형식 | `base_url: "not-a-url"` | INVALID_ARGUMENT: invalid base_url |
| 존재하지 않는 project_id | 없는 UUID | NOT_FOUND: project not found |
| Bitbucket email 누락 | `email: ""` | INVALID_ARGUMENT: email is required |
| Bitbucket api_token 누락 | `api_token: ""` | INVALID_ARGUMENT: api_token is required |
| 삭제 시 Repository 참조 있음 | provider_id가 Connection에 사용 중 | FAILED_PRECONDITION: provider is in use |
| 동일 project 내 name 중복 | 기존과 같은 name | ALREADY_EXISTS |

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

### E2E 시나리오: Provider 등록 후 Repository 생성

```bash
#!/bin/bash
# e2e-provider-repository.sh

BASE_URL="http://localhost:8080"
PROJECT_ID="550e8400-e29b-41d4-a716-446655440000"
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# 1. Provider 등록
PROVIDER_RESP=$(curl -s -X POST "$BASE_URL/v1/providers" \
  -H 'Content-Type: application/json' \
  -d "{
    \"name\": \"e2e-github\",
    \"project_id\": \"$PROJECT_ID\",
    \"provider\": {\"github\": {\"token\": \"$GITHUB_TOKEN\"}}
  }")

PROVIDER_ID=$(echo $PROVIDER_RESP | jq -r '.provider_id')
echo "Provider registered: $PROVIDER_ID"

# 2. Provider 조회 확인
curl -s "$BASE_URL/v1/providers/$PROVIDER_ID" | jq .

# 3. Provider 삭제
curl -s -X DELETE "$BASE_URL/v1/providers/$PROVIDER_ID" | jq .
```

### 스크립트 실행

```bash
chmod +x e2e-provider-repository.sh
./e2e-provider-repository.sh
```
