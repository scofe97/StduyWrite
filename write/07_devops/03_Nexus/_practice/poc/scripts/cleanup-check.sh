#!/bin/bash
# Nexus Cleanup Status Check Script
# 디스크 사용량과 Blob Store 상태를 확인한다.
set -euo pipefail

NEXUS_URL="${1:-http://localhost:8081}"
ADMIN_PASS="${2:-admin123}"

echo "=== Nexus 스토리지 상태 ==="
echo ""

# 1. Docker volume 디스크 사용량
echo "--- Docker Volume ---"
docker system df -v 2>/dev/null | grep nexus || echo "nexus volume 정보 없음"
echo ""

# 2. Blob Store 상태 (REST API)
echo "--- Blob Stores ---"
curl -sf -u "admin:${ADMIN_PASS}" \
  "${NEXUS_URL}/service/rest/v1/blobstores" | \
  python3 -m json.tool 2>/dev/null || echo "Blob Store 조회 실패 (Nexus가 실행 중인지 확인)"
echo ""

# 3. 리포지토리별 컴포넌트 수
echo "--- 리포지토리별 컴포넌트 수 ---"
repos=$(curl -sf -u "admin:${ADMIN_PASS}" "${NEXUS_URL}/service/rest/v1/repositories" | \
  python3 -c "import sys,json; [print(r['name']) for r in json.load(sys.stdin)]" 2>/dev/null)

if [ -n "$repos" ]; then
  while IFS= read -r repo; do
    count=$(curl -sf -u "admin:${ADMIN_PASS}" \
      "${NEXUS_URL}/service/rest/v1/components?repository=${repo}" | \
      python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('items',[])))" 2>/dev/null || echo "?")
    printf "  %-30s %s\n" "${repo}" "${count} components"
  done <<< "$repos"
else
  echo "리포지토리 조회 실패"
fi

echo ""
echo "=== 확인 완료 ==="
