#!/bin/bash
# 환경 설정 (호스트에서 실행)
# 이후 스크립트는 docker exec -it kafka1 /bin/bash 접속 후 실행

cd "$(dirname "$0")/.."
docker-compose -f docker-compose-multi.yml up -d
sleep 30
docker-compose -f docker-compose-multi.yml ps
echo ""
echo "접속: docker exec -it kafka1 /bin/bash"
echo "실습: cd /labs && ./01-create-replicated-topic.sh"
