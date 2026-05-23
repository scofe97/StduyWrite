#!/bin/bash
# 멱등성 Producer 테스트
#
# 멱등성(enable.idempotence=true)의 효과:
# - Producer ID + Sequence Number로 중복 감지
# - 네트워크 장애로 재전송해도 중복 저장 안됨
# - 순서 보장 (Sequence가 연속적이지 않으면 거부)
#
# 이 스크립트는 멱등성 설정 방법과 관련 설정을 보여줍니다.
# 실제 중복 방지 효과는 네트워크 장애 시뮬레이션이 필요합니다.

BOOTSTRAP=kafka1:9092

echo "=========================================="
echo "[1] 멱등성 Producer 설정 확인"
echo "=========================================="

echo "
멱등성 활성화 시 자동 설정되는 값들:
- acks=all (필수)
- retries=Integer.MAX_VALUE (무한 재시도)
- max.in.flight.requests.per.connection ≤ 5

Kafka 3.0+에서는 기본 활성화됨
"

echo "=========================================="
echo "[2] 멱등성 vs 비멱등성 비교 토픽 생성"
echo "=========================================="

TOPIC_IDEMP=idempotent-test
TOPIC_NORMAL=non-idempotent-test

for topic in $TOPIC_IDEMP $TOPIC_NORMAL; do
    if ! kafka-topics --list --bootstrap-server $BOOTSTRAP 2>/dev/null | grep -q "^${topic}$"; then
        kafka-topics --create \
            --topic $topic \
            --partitions 1 \
            --replication-factor 3 \
            --config min.insync.replicas=2 \
            --bootstrap-server $BOOTSTRAP 2>/dev/null
        echo "Created: $topic"
    fi
done

echo ""
echo "=========================================="
echo "[3] 멱등성 Producer로 전송"
echo "=========================================="

echo "enable.idempotence=true 로 10개 메시지 전송..."
for i in $(seq 1 10); do
    echo "key-$((i % 3)):msg-$i"
done | kafka-console-producer \
    --topic $TOPIC_IDEMP \
    --producer-property acks=all \
    --producer-property enable.idempotence=true \
    --property parse.key=true \
    --property key.separator=: \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "=========================================="
echo "[4] 결과 확인"
echo "=========================================="

echo "토픽 오프셋 (메시지 수):"
kafka-get-offsets --topic $TOPIC_IDEMP --bootstrap-server $BOOTSTRAP

echo ""
echo "메시지 내용 (key:value):"
kafka-console-consumer \
    --topic $TOPIC_IDEMP \
    --from-beginning \
    --timeout-ms 10000 \
    --max-messages 15 \
    --group idempotent-test-$$ \
    --property print.key=true \
    --property key.separator=: \
    --bootstrap-server $BOOTSTRAP 2>/dev/null