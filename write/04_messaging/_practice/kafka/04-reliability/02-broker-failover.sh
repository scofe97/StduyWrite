#!/bin/bash
# 브로커 장애 시뮬레이션 및 복구
# 호스트에서 docker stop/start 명령어 실행 필요

TOPIC=replication-test
BOOTSTRAP=kafka1:9092

echo "[1] 현재 상태"
kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP

echo ""
echo "=========================================="
echo "호스트에서 실행: docker stop kafka2"
echo "실행 후 Enter를 누르세요..."
read

echo ""
echo "[2] 1개 브로커 다운 후 상태"
kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP

echo ""
echo "메시지 전송 테스트 (acks=all)..."
echo "test-one-down" | kafka-console-producer --topic $TOPIC --producer-property acks=all --bootstrap-server $BOOTSTRAP 2>/dev/null && echo "OK" || echo "FAILED"

echo ""
echo "=========================================="
echo "호스트에서 실행: docker stop kafka3"
echo "실행 후 Enter를 누르세요..."
read

echo ""
echo "[3] 2개 브로커 다운 후 상태"
kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP 2>/dev/null

echo ""
echo "Under-min-ISR 파티션:"
kafka-topics --describe --under-min-isr-partitions --bootstrap-server $BOOTSTRAP

echo ""
echo "메시지 전송 테스트 (acks=all) - 실패 예상..."
timeout 3 bash -c "echo 'test-two-down' | kafka-console-producer --topic $TOPIC --producer-property acks=all --bootstrap-server $BOOTSTRAP" 2>&1 || echo "FAILED (NOT_ENOUGH_REPLICAS)"

echo ""
echo "=========================================="
echo "호스트에서 실행: docker start kafka2 kafka3"
echo "실행 후 Enter를 누르세요..."
read

sleep 10
echo ""
echo "[4] 복구 후 상태 (Leader 자동 복원 안 됨)"
kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP

echo ""
echo "[5] Preferred Leader Election"
kafka-leader-election --election-type preferred --all-topic-partitions --bootstrap-server $BOOTSTRAP

sleep 3
echo ""
echo "[6] 최종 상태"
kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP
