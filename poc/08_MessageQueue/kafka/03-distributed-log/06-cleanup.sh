#!/bin/bash
# 실습 토픽 및 Consumer Group 정리

BOOTSTRAP=kafka1:9092

echo "=========================================="
echo "실습 토픽 삭제"
echo "=========================================="

TOPICS=(
    "offset-test"
    "multi-partition-no-key"
    "multi-partition-with-key"
    "consumer-group-test"
    "replication-demo"
)

for topic in "${TOPICS[@]}"; do
    kafka-topics --delete --topic $topic --bootstrap-server $BOOTSTRAP 2>/dev/null
    echo "Deleted: $topic"
done

echo ""
echo "=========================================="
echo "Consumer Group 삭제"
echo "=========================================="

GROUPS=(
    "offset-test-group"
    "analytics-group"
    "monitoring-group"
)

for group in "${GROUPS[@]}"; do
    kafka-consumer-groups --delete --group $group --bootstrap-server $BOOTSTRAP 2>/dev/null
    echo "Deleted: $group"
done

echo ""
echo "=========================================="
echo "정리 완료"
echo "=========================================="
