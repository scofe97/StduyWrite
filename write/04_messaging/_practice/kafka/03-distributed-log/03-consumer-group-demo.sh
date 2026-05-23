#!/bin/bash
# Consumer Group 데모
# - 같은 Group: 파티션을 나눠서 소비 (부하 분산)
# - 다른 Group: 독립적으로 모든 데이터 소비

BOOTSTRAP=kafka1:9092
TOPIC=consumer-group-test

echo "=========================================="
echo "[1] 테스트 데이터 준비"
echo "=========================================="

kafka-topics --delete --topic $TOPIC --bootstrap-server $BOOTSTRAP 2>/dev/null
sleep 2
kafka-topics --create --topic $TOPIC --partitions 3 --replication-factor 1 --bootstrap-server $BOOTSTRAP 2>/dev/null

echo "9개 메시지 전송 (3개 Key × 3개씩)..."
for key in order-A order-B order-C; do
    for i in 1 2 3; do
        echo "$key:event-$i"
    done
done | kafka-console-producer \
    --topic $TOPIC \
    --property parse.key=true \
    --property key.separator=: \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo "전송 완료"

echo ""
echo "=========================================="
echo "[2] 같은 Group - 파티션별 메시지 분포"
echo "=========================================="

echo "--- Partition 0 ---"
kafka-console-consumer --topic $TOPIC --partition 0 --offset earliest --timeout-ms 3000 \
    --property print.key=true --property key.separator=: --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "--- Partition 1 ---"
kafka-console-consumer --topic $TOPIC --partition 1 --offset earliest --timeout-ms 3000 \
    --property print.key=true --property key.separator=: --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "--- Partition 2 ---"
kafka-console-consumer --topic $TOPIC --partition 2 --offset earliest --timeout-ms 3000 \
    --property print.key=true --property key.separator=: --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[3] 다른 Group은 독립적으로 전체 소비"
echo "=========================================="

GROUP1=analytics-group
GROUP2=monitoring-group

echo "--- Group: $GROUP1 ---"
kafka-console-consumer \
    --topic $TOPIC \
    --group $GROUP1 \
    --from-beginning \
    --timeout-ms 10000 \
    --max-messages 9 \
    --property print.key=true \
    --property key.separator=: \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "--- Group: $GROUP2 ---"
kafka-console-consumer \
    --topic $TOPIC \
    --group $GROUP2 \
    --from-beginning \
    --timeout-ms 10000 \
    --max-messages 9 \
    --property print.key=true \
    --property key.separator=: \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[4] 두 Group의 Offset 비교"
echo "=========================================="

echo "--- $GROUP1 ---"
kafka-consumer-groups --describe --group $GROUP1 --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "--- $GROUP2 ---"
kafka-consumer-groups --describe --group $GROUP2 --bootstrap-server $BOOTSTRAP 2>/dev/null
