#!/bin/bash
# Offset 관리 실습
# - Offset 확인
# - 부분 소비 후 LAG 확인
# - Offset 리셋

BOOTSTRAP=kafka1:9092
TOPIC=offset-test
GROUP=offset-test-group

echo "=========================================="
echo "[1] 토픽 준비 및 메시지 전송"
echo "=========================================="

kafka-topics --delete --topic $TOPIC --bootstrap-server $BOOTSTRAP 2>/dev/null
sleep 2
kafka-topics --create --topic $TOPIC --partitions 1 --replication-factor 1 --bootstrap-server $BOOTSTRAP 2>/dev/null

echo "10개 메시지 전송..."
for i in $(seq 0 9); do
    echo "message-$i"
done | kafka-console-producer --topic $TOPIC --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[2] 5개만 소비 후 중단"
echo "=========================================="

echo "5개 메시지 소비:"
kafka-console-consumer \
    --topic $TOPIC \
    --group $GROUP \
    --from-beginning \
    --max-messages 5 \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[3] Consumer Group 상태 확인 (LAG 확인)"
echo "=========================================="

kafka-consumer-groups --describe --group $GROUP --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "해석:"
echo "- CURRENT-OFFSET: 다음에 읽을 위치"
echo "- LOG-END-OFFSET: 전체 메시지 수"
echo "- LAG: 아직 읽지 않은 메시지 수"

echo ""
echo "=========================================="
echo "[4] 나머지 5개 소비"
echo "=========================================="

echo "남은 메시지 소비:"
kafka-console-consumer \
    --topic $TOPIC \
    --group $GROUP \
    --max-messages 5 \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "Consumer Group 상태 (LAG=0):"
kafka-consumer-groups --describe --group $GROUP --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[5] Offset 리셋 (처음으로)"
echo "=========================================="

echo "Offset을 처음으로 리셋..."
kafka-consumer-groups --reset-offsets \
    --group $GROUP \
    --topic $TOPIC \
    --to-earliest \
    --execute \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "리셋 후 상태 (LAG=10):"
kafka-consumer-groups --describe --group $GROUP --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[6] Offset 리셋 옵션들"
echo "=========================================="

echo "
# 처음부터
--to-earliest

# 최신부터 (새 메시지만)
--to-latest

# 특정 위치로
--to-offset 5

# 특정 시간 기준
--to-datetime 2024-01-15T00:00:00.000

# N개 앞으로 (현재-N)
--shift-by -3
"

echo "=========================================="
echo "결론: Offset으로 Consumer의 읽기 위치 제어"
echo "=========================================="
