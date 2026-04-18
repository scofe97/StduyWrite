#!/bin/bash
# Docker 볼륨 데모 스크립트

set -e

echo "=========================================="
echo "Docker Volume Demo"
echo "=========================================="

# 1. Named volume 생성
echo ""
echo "[1] Creating named volume..."
docker volume create demo-volume
docker volume ls | grep demo-volume
echo "✓ Volume created"

# 2. 볼륨에 데이터 쓰기
echo ""
echo "[2] Writing data to volume..."
docker run --rm -v demo-volume:/data alpine sh -c "echo 'Hello from container 1' > /data/test.txt"
docker run --rm -v demo-volume:/data alpine sh -c "echo 'Timestamp: $(date)' >> /data/test.txt"
echo "✓ Data written"

# 3. 데이터 읽기
echo ""
echo "[3] Reading data from volume..."
docker run --rm -v demo-volume:/data alpine cat /data/test.txt

# 4. 컨테이너 생성 및 삭제 후 데이터 영속성 확인
echo ""
echo "[4] Testing data persistence..."
docker run -d --name temp-container -v demo-volume:/data alpine sleep 10
echo "✓ Container created with volume"

echo ""
echo "[5] Stopping and removing container..."
docker rm -f temp-container
echo "✓ Container removed"

echo ""
echo "[6] Verifying data still exists..."
docker run --rm -v demo-volume:/data alpine cat /data/test.txt
echo "✓ Data persisted after container removal!"

# 7. 볼륨 정보 확인
echo ""
echo "[7] Volume details:"
docker volume inspect demo-volume

echo ""
echo "[8] Volume demo complete!"
echo ""
echo "To cleanup, run:"
echo "  docker volume rm demo-volume"
