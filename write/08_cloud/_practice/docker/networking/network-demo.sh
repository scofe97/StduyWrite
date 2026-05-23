#!/bin/bash
# Docker 네트워킹 데모 스크립트

set -e

echo "=========================================="
echo "Docker Networking Demo"
echo "=========================================="

# 1. 커스텀 bridge 네트워크 생성
echo ""
echo "[1] Creating custom bridge network..."
docker network create --driver bridge demo-net
docker network ls | grep demo-net

# 2. 첫 번째 컨테이너 실행
echo ""
echo "[2] Starting container 1 (alpine1)..."
docker run -d --name alpine1 --network demo-net alpine sleep 3600
echo "✓ alpine1 started"

# 3. 두 번째 컨테이너 실행
echo ""
echo "[3] Starting container 2 (alpine2)..."
docker run -d --name alpine2 --network demo-net alpine sleep 3600
echo "✓ alpine2 started"

# 4. 네트워크 정보 확인
echo ""
echo "[4] Inspecting network..."
docker network inspect demo-net --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'

# 5. DNS 이름으로 통신 테스트
echo ""
echo "[5] Testing DNS resolution (alpine1 -> alpine2)..."
docker exec alpine1 ping -c 3 alpine2

# 6. IP 주소로 통신 테스트
echo ""
echo "[6] Testing IP connectivity..."
ALPINE2_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' alpine2)
docker exec alpine1 ping -c 3 $ALPINE2_IP

echo ""
echo "[7] Network test complete!"
echo ""
echo "To cleanup, run:"
echo "  docker rm -f alpine1 alpine2"
echo "  docker network rm demo-net"
