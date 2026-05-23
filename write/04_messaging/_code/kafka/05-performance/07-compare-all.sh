#!/bin/bash
# 전체 성능 비교

TOPIC=perf-test
BOOTSTRAP=kafka1:9092
RECORDS=50000
SIZE=1000

echo "Performance Comparison ($RECORDS records, ${SIZE}B each)"
echo "========================================================="
echo ""

echo "[1] Producer Baseline"
kafka-producer-perf-test --topic $TOPIC --num-records $RECORDS --record-size $SIZE \
    --throughput -1 --producer-props bootstrap.servers=$BOOTSTRAP 2>/dev/null | tail -1
sleep 2

echo ""
echo "[2] Producer + Batch (100KB, 10ms)"
kafka-producer-perf-test --topic $TOPIC --num-records $RECORDS --record-size $SIZE \
    --throughput -1 --producer-props bootstrap.servers=$BOOTSTRAP batch.size=100000 linger.ms=10 2>/dev/null | tail -1
sleep 2

echo ""
echo "[3] Producer + Batch + LZ4"
kafka-producer-perf-test --topic $TOPIC --num-records $RECORDS --record-size $SIZE \
    --throughput -1 --producer-props bootstrap.servers=$BOOTSTRAP batch.size=100000 linger.ms=10 compression.type=lz4 2>/dev/null | tail -1
sleep 2

echo ""
echo "[4] Consumer Baseline"
kafka-consumer-perf-test --topic $TOPIC --messages $RECORDS --bootstrap-server $BOOTSTRAP 2>/dev/null | grep -E "^[0-9]|MB.sec"
