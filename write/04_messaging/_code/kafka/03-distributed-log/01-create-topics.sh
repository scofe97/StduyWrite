#!/bin/bash
# 분산 로그 실습용 토픽 생성

BOOTSTRAP=kafka1:9092

# 1. 단일 파티션 토픽 (Offset 테스트용)
TOPIC1=offset-test
if ! kafka-topics --list --bootstrap-server $BOOTSTRAP 2>/dev/null | grep -q "^${TOPIC1}$"; then
    kafka-topics --create \
        --topic $TOPIC1 \
        --partitions 1 \
        --replication-factor 1 \
        --bootstrap-server $BOOTSTRAP
    echo "Created: $TOPIC1"
else
    echo "Exists: $TOPIC1"
fi

# 2. 다중 파티션 토픽 (Key 없이 - 순서 문제 확인용)
TOPIC2=multi-partition-no-key
if ! kafka-topics --list --bootstrap-server $BOOTSTRAP 2>/dev/null | grep -q "^${TOPIC2}$"; then
    kafka-topics --create \
        --topic $TOPIC2 \
        --partitions 3 \
        --replication-factor 1 \
        --bootstrap-server $BOOTSTRAP
    echo "Created: $TOPIC2"
else
    echo "Exists: $TOPIC2"
fi

# 3. 다중 파티션 토픽 (Key 사용 - 순서 보장 확인용)
TOPIC3=multi-partition-with-key
if ! kafka-topics --list --bootstrap-server $BOOTSTRAP 2>/dev/null | grep -q "^${TOPIC3}$"; then
    kafka-topics --create \
        --topic $TOPIC3 \
        --partitions 3 \
        --replication-factor 1 \
        --bootstrap-server $BOOTSTRAP
    echo "Created: $TOPIC3"
else
    echo "Exists: $TOPIC3"
fi

# 4. Consumer Group 테스트용 토픽
TOPIC4=consumer-group-test
if ! kafka-topics --list --bootstrap-server $BOOTSTRAP 2>/dev/null | grep -q "^${TOPIC4}$"; then
    kafka-topics --create \
        --topic $TOPIC4 \
        --partitions 3 \
        --replication-factor 1 \
        --bootstrap-server $BOOTSTRAP
    echo "Created: $TOPIC4"
else
    echo "Exists: $TOPIC4"
fi

echo ""
echo "=== 생성된 토픽 목록 ==="
kafka-topics --list --bootstrap-server $BOOTSTRAP | grep -E "offset-test|multi-partition|consumer-group"
