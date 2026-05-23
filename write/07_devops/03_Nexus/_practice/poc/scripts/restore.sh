#!/bin/bash
# Nexus Restore Script
set -euo pipefail

BACKUP_FILE="${1:?Usage: ./restore.sh <backup-file.tar.gz>}"
CONTAINER_NAME="nexus"

if [ ! -f "${BACKUP_FILE}" ]; then
  echo "ERROR: 백업 파일을 찾을 수 없습니다: ${BACKUP_FILE}"
  exit 1
fi

echo "=== Nexus 복구 시작 ==="
echo "백업 파일: ${BACKUP_FILE}"
echo ""
read -p "경고: 기존 데이터가 덮어씌워집니다. 계속하시겠습니까? (y/N) " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
  echo "복구 취소"
  exit 0
fi

# 1. Nexus 컨테이너 중지
echo "Nexus 중지..."
docker compose stop nexus

# 2. Volume 데이터 복구
echo "데이터 복구 중..."
docker run --rm \
  -v nexus-data:/target \
  -v "$(cd "$(dirname "${BACKUP_FILE}")" && pwd)":/backup \
  alpine sh -c "rm -rf /target/* && tar xzf /backup/$(basename "${BACKUP_FILE}") -C /target"

# 3. Nexus 재시작
echo "Nexus 재시작..."
docker compose up -d nexus

echo ""
echo "=== 복구 완료 ==="
echo "Nexus 시작까지 1-2분 소요됩니다."
echo "상태 확인: curl -f http://localhost:8081/service/rest/v1/status"
