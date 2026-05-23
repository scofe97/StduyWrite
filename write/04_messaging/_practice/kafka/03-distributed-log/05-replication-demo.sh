#!/bin/bash
# 복제(Replication) 실습
# - 복제 토픽 생성
# - Leader/Follower/ISR 확인
# - 복제 팩터 제약 확인

BOOTSTRAP=kafka1:9092

echo "=========================================="
echo "[1] 복제 토픽 생성 (RF=3)"
echo "=========================================="

TOPIC=replication-demo
kafka-topics --delete --topic $TOPIC --bootstrap-server $BOOTSTRAP 2>/dev/null
sleep 2

kafka-topics --create \
    --topic $TOPIC \
    --partitions 3 \
    --replication-factor 3 \
    --bootstrap-server $BOOTSTRAP

echo ""
echo "=========================================="
echo "[2] 복제 상태 확인 (메시지 전송 전후 비교)"
echo "=========================================="

echo "--- 전송 전 상태 ---"
kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP

echo ""
echo "3개 메시지 전송 (acks=all)..."
echo "test-message-1
test-message-2
test-message-3" | kafka-console-producer \
    --topic $TOPIC \
    --producer-property acks=all \
    --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "--- 전송 후 상태 ---"
kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP

echo ""
echo "해석:"
echo "- Leader: 해당 파티션의 읽기/쓰기 담당"
echo "- Replicas: 복제본 위치 (브로커 ID)"
echo "- Isr: 동기화 완료된 복제본 (acks=all은 ISR 전체 확인 후 응답)"

echo ""
echo "=========================================="
echo "[3] 브로커별 로그 파일로 복제 확인"
echo "=========================================="

echo "메시지가 저장된 파티션 확인:"
PARTITION=$(kafka-get-offsets --topic $TOPIC --bootstrap-server $BOOTSTRAP 2>/dev/null | grep -v ":0$" | head -1 | cut -d: -f2)
echo "→ Partition $PARTITION 에 메시지 존재"

echo ""
echo "현재 브로커(kafka1)의 로그 파일:"
ls -la /var/lib/kafka/data/${TOPIC}-${PARTITION}/*.log 2>/dev/null

echo ""
echo "※ 호스트에서 3개 브로커 비교 (복제 확인):"
echo "  docker exec kafka1 ls -la /var/lib/kafka/data/${TOPIC}-${PARTITION}/*.log"
echo "  docker exec kafka2 ls -la /var/lib/kafka/data/${TOPIC}-${PARTITION}/*.log"
echo "  docker exec kafka3 ls -la /var/lib/kafka/data/${TOPIC}-${PARTITION}/*.log"

echo ""
echo "=========================================="
echo "[4] 복제 팩터 제약 테스트"
echo "=========================================="

echo "브로커 3개에서 RF=4 생성 시도..."
kafka-topics --create \
    --topic rf-test-fail \
    --partitions 1 \
    --replication-factor 4 \
    --bootstrap-server $BOOTSTRAP 2>&1 || echo "(예상된 에러)"

echo ""
echo "=========================================="
echo "[5] Leader 분포 확인"
echo "=========================================="

echo "파티션별 Leader 분포:"
kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP 2>/dev/null \
    | grep -E "Partition:" \
    | awk '{print "Partition " $4 " → Leader: Broker " $6}'
