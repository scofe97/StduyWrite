#!/bin/bash
# Nexus Repository Auto-Setup Script
# REST API를 사용하여 기본 리포지토리를 자동 생성한다.
#
# Usage: ./setup-repos.sh [NEXUS_URL] [ADMIN_PASSWORD]

set -euo pipefail

NEXUS_URL="${1:-http://localhost:8081}"
ADMIN_PASS="${2:-admin123}"
API="${NEXUS_URL}/service/rest/v1"

wait_for_nexus() {
  echo "Nexus 시작 대기 중..."
  local max_attempts=60
  local attempt=0
  while [ $attempt -lt $max_attempts ]; do
    if curl -sf "${NEXUS_URL}/service/rest/v1/status" > /dev/null 2>&1; then
      echo "Nexus 준비 완료"
      return 0
    fi
    attempt=$((attempt + 1))
    sleep 5
  done
  echo "ERROR: Nexus 시작 시간 초과"
  exit 1
}

create_repo() {
  local name="$1"
  local payload="$2"

  echo -n "  ${name}... "
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    -u "admin:${ADMIN_PASS}" \
    -H "Content-Type: application/json" \
    -d "${payload}" \
    "${API}/repositories")

  case $status in
    201) echo "생성 완료" ;;
    400) echo "이미 존재 (skip)" ;;
    *) echo "실패 (HTTP ${status})" ;;
  esac
}

wait_for_nexus

echo ""
echo "=== Maven 리포지토리 ==="
create_repo "maven-releases" '{
  "name": "maven-releases",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true, "writePolicy": "ALLOW_ONCE" },
  "maven": { "versionPolicy": "RELEASE", "layoutPolicy": "STRICT" },
  "format": "maven2",
  "type": "hosted"
}'

create_repo "maven-snapshots" '{
  "name": "maven-snapshots",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true, "writePolicy": "ALLOW" },
  "maven": { "versionPolicy": "SNAPSHOT", "layoutPolicy": "STRICT" },
  "format": "maven2",
  "type": "hosted"
}'

create_repo "maven-central-proxy" '{
  "name": "maven-central-proxy",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true },
  "proxy": { "remoteUrl": "https://repo1.maven.org/maven2/", "contentMaxAge": 1440, "metadataMaxAge": 1440 },
  "negativeCache": { "enabled": true, "timeToLive": 1440 },
  "httpClient": { "blocked": false, "autoBlock": true },
  "format": "maven2",
  "type": "proxy"
}'

create_repo "maven-public" '{
  "name": "maven-public",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true },
  "group": { "memberNames": ["maven-releases", "maven-snapshots", "maven-central-proxy"] },
  "format": "maven2",
  "type": "group"
}'

echo ""
echo "=== npm 리포지토리 ==="
create_repo "npm-hosted" '{
  "name": "npm-hosted",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true, "writePolicy": "ALLOW" },
  "format": "npm",
  "type": "hosted"
}'

create_repo "npm-proxy" '{
  "name": "npm-proxy",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true },
  "proxy": { "remoteUrl": "https://registry.npmjs.org/", "contentMaxAge": 1440, "metadataMaxAge": 1440 },
  "negativeCache": { "enabled": true, "timeToLive": 1440 },
  "httpClient": { "blocked": false, "autoBlock": true },
  "format": "npm",
  "type": "proxy"
}'

create_repo "npm-group" '{
  "name": "npm-group",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true },
  "group": { "memberNames": ["npm-hosted", "npm-proxy"] },
  "format": "npm",
  "type": "group"
}'

echo ""
echo "=== Docker 리포지토리 ==="
create_repo "docker-hosted" '{
  "name": "docker-hosted",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true, "writePolicy": "ALLOW" },
  "docker": { "v1Enabled": false, "forceBasicAuth": true, "httpPort": 8082 },
  "format": "docker",
  "type": "hosted"
}'

create_repo "docker-proxy" '{
  "name": "docker-proxy",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true },
  "proxy": { "remoteUrl": "https://registry-1.docker.io", "contentMaxAge": 1440, "metadataMaxAge": 1440 },
  "negativeCache": { "enabled": true, "timeToLive": 1440 },
  "httpClient": { "blocked": false, "autoBlock": true },
  "docker": { "v1Enabled": false, "forceBasicAuth": true },
  "dockerProxy": { "indexType": "HUB" },
  "format": "docker",
  "type": "proxy"
}'

create_repo "docker-group" '{
  "name": "docker-group",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": true },
  "group": { "memberNames": ["docker-hosted", "docker-proxy"] },
  "docker": { "v1Enabled": false, "forceBasicAuth": true, "httpPort": 8083 },
  "format": "docker",
  "type": "group"
}'

echo ""
echo "=== Raw 리포지토리 ==="
create_repo "raw-hosted" '{
  "name": "raw-hosted",
  "online": true,
  "storage": { "blobStoreName": "default", "strictContentTypeValidation": false, "writePolicy": "ALLOW" },
  "format": "raw",
  "type": "hosted"
}'

echo ""
echo "=== 설정 완료 ==="
echo "Nexus UI: ${NEXUS_URL}"
echo "Maven Public: ${NEXUS_URL}/repository/maven-public/"
echo "npm Group: ${NEXUS_URL}/repository/npm-group/"
echo "Docker Push: localhost:8082"
echo "Docker Pull: localhost:8083"
