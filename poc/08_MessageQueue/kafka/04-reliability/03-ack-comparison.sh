#!/bin/bash
# ACK 전략별 성능 비교
# Usage: ./03-ack-comparison.sh [MESSAGE_COUNT]

TOPIC=replication-test
BOOTSTRAP=kafka1:9092
COUNT=${1:-1000}

# 메시지 생성
for i in $(seq 1 $COUNT); do echo "msg-$i"; done > /tmp/messages.txt

# 워밍업
head -100 /tmp/messages.txt | kafka-console-producer \
    --topic $TOPIC --producer-property acks=1 --bootstrap-server $BOOTSTRAP 2>/dev/null
sleep 2

# acks=all
START_ALL=$(date +%s%3N)
cat /tmp/messages.txt | kafka-console-producer \
    --topic $TOPIC \
    --producer-property acks=all \
    --producer-property linger.ms=0 \
    --producer-property batch.size=1 \
    --bootstrap-server $BOOTSTRAP 2>/dev/null
END_ALL=$(date +%s%3N)
TIME_ALL=$((END_ALL - START_ALL))
sleep 1

# acks=1
START_1=$(date +%s%3N)
cat /tmp/messages.txt | kafka-console-producer \
    --topic $TOPIC \
    --producer-property acks=1 \
    --producer-property linger.ms=0 \
    --producer-property batch.size=1 \
    --bootstrap-server $BOOTSTRAP 2>/dev/null
END_1=$(date +%s%3N)
TIME_1=$((END_1 - START_1))
sleep 1

# acks=0
START_0=$(date +%s%3N)
cat /tmp/messages.txt | kafka-console-producer \
    --topic $TOPIC \
    --producer-property acks=0 \
    --producer-property linger.ms=0 \
    --producer-property batch.size=1 \
    --bootstrap-server $BOOTSTRAP 2>/dev/null
END_0=$(date +%s%3N)
TIME_0=$((END_0 - START_0))

rm -f /tmp/messages.txt

echo "ACK Performance ($COUNT msgs)"
echo "=============================="
echo "acks=all : ${TIME_ALL}ms"
echo "acks=1   : ${TIME_1}ms"
echo "acks=0   : ${TIME_0}ms"
