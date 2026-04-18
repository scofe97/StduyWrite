#!/bin/bash
# 복제 토픽 생성

TOPIC=replication-test
BOOTSTRAP=kafka1:9092

kafka-topics --delete --topic $TOPIC --bootstrap-server $BOOTSTRAP 2>/dev/null
sleep 2

kafka-topics --create \
    --topic $TOPIC \
    --partitions 3 \
    --replication-factor 3 \
    --config min.insync.replicas=2 \
    --bootstrap-server $BOOTSTRAP

kafka-topics --describe --topic $TOPIC --bootstrap-server $BOOTSTRAP
