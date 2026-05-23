#!/bin/bash
# Nexus Backup Script
# Docker volume 기반 백업
set -euo pipefail

BACKUP_DIR="${1:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="nexus"

mkdir -p "${BACKUP_DIR}"

echo "=== Nexus 백업 시작: ${TIMESTAMP} ==="

# 1. DB Export Task 트리거 (REST API)
echo "DB Export Task 실행..."
curl -sf -u admin:admin123 \
  -X POST "http://localhost:8081/service/rest/v1/tasks/run" \
  -H "Content-Type: application/json" \
  -d '{"id":"db.backup"}' || echo "DB Export Task를 수동으로 실행하세요"

sleep 5

# 2. Volume 데이터 백업
echo "Volume 데이터 백업 중..."
docker run --rm \
  -v nexus-data:/source:ro \
  -v "$(cd "${BACKUP_DIR}" && pwd)":/backup \
  alpine tar czf "/backup/nexus-data-${TIMESTAMP}.tar.gz" -C /source .

echo "백업 완료: ${BACKUP_DIR}/nexus-data-${TIMESTAMP}.tar.gz"
echo "크기: $(du -h "${BACKUP_DIR}/nexus-data-${TIMESTAMP}.tar.gz" | cut -f1)"

# 3. 오래된 백업 정리 (30일 이상)
echo "30일 이상 된 백업 정리..."
find "${BACKUP_DIR}" -name "nexus-data-*.tar.gz" -mtime +30 -delete 2>/dev/null || true

echo "=== 백업 완료 ==="
