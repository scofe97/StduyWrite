#!/bin/bash
# Key 기반 파티셔닝 데모
# - Key 없이 전송: 순서 보장 안됨
# - Key로 전송: 같은 Key는 같은 파티션으로 → 순서 보장

BOOTSTRAP=kafka1:9092

echo "=========================================="
echo "[1] Key 없이 메시지 전송 (순서 깨짐 확인)"
echo "=========================================="

TOPIC_NO_KEY=multi-partition-no-key
kafka-topics --delete --topic $TOPIC_NO_KEY --bootstrap-server $BOOTSTRAP 2>/dev/null
sleep 2
kafka-topics --create --topic $TOPIC_NO_KEY --partitions 3 --replication-factor 1 --bootstrap-server $BOOTSTRAP 2>/dev/null

echo "전송 순서: coffee-1, cola-1, coffee-2, cola-2, coffee-3"
echo "coffee-1
cola-1
coffee-2
cola-2
coffee-3" | kafka-console-producer \
    --topic $TOPIC_NO_KEY \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

sleep 1
echo ""
echo "소비 결과 (순서가 다를 수 있음):"
kafka-console-consumer \
    --topic $TOPIC_NO_KEY \
    --from-beginning \
    --timeout-ms 5000 \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[2] Key로 메시지 전송 (순서 보장 확인)"
echo "=========================================="

TOPIC_WITH_KEY=multi-partition-with-key
kafka-topics --delete --topic $TOPIC_WITH_KEY --bootstrap-server $BOOTSTRAP 2>/dev/null
sleep 2
kafka-topics --create --topic $TOPIC_WITH_KEY --partitions 3 --replication-factor 1 --bootstrap-server $BOOTSTRAP 2>/dev/null

echo "전송 순서: coffee:1, cola:1, coffee:2, cola:2, coffee:3"
echo "coffee:1
cola:1
coffee:2
cola:2
coffee:3" | kafka-console-producer \
    --topic $TOPIC_WITH_KEY \
    --property parse.key=true \
    --property key.separator=: \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

sleep 1
echo ""
echo "소비 결과 (같은 Key끼리 순서 보장):"
kafka-console-consumer \
    --topic $TOPIC_WITH_KEY \
    --from-beginning \
    --timeout-ms 5000 \
    --property print.key=true \
    --property key.separator=: \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[3] 파티션별 메시지 분포 확인"
echo "=========================================="

echo ""
echo "각 파티션의 메시지:"
for p in 0 1 2; do
    echo "--- Partition $p ---"
    kafka-console-consumer \
        --topic $TOPIC_WITH_KEY \
        --partition $p \
        --offset earliest \
        --timeout-ms 3000 \
        --property print.key=true \
        --property key.separator=: \
        --bootstrap-server $BOOTSTRAP 2>/dev/null
done

echo ""
echo "=========================================="
echo "결론: 같은 Key = 같은 파티션 = 순서 보장"
echo "=========================================="
