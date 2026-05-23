#!/bin/bash
# Docker 보안 스캔 데모 스크립트

set -e

echo "=========================================="
echo "Docker Security Scan Demo"
echo "=========================================="

# 1. Docker Scout quickview
echo ""
echo "[1] Quick security overview (nginx:alpine)..."
docker scout quickview nginx:alpine

echo ""
echo "=========================================="

# 2. CVE 상세 확인
echo ""
echo "[2] Detailed CVE scan..."
docker scout cves nginx:alpine

echo ""
echo "=========================================="

# 3. 베이스 이미지 비교
echo ""
echo "[3] Comparing base images..."
echo "Scanning nginx:latest..."
docker scout quickview nginx:latest

echo ""
echo "Scanning nginx:alpine..."
docker scout quickview nginx:alpine

echo ""
echo "=========================================="
echo "Security scan complete!"
echo ""
echo "Key takeaways:"
echo "  - Alpine-based images are typically smaller and have fewer vulnerabilities"
echo "  - Always use specific version tags (not 'latest')"
echo "  - Regularly update base images to get security patches"
echo ""
echo "For more info: https://docs.docker.com/scout/"
