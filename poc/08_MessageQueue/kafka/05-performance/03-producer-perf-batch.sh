#!/bin/bash
# Producer 배치 최적화 성능 측정

TOPIC=perf-test
BOOTSTRAP=kafka1:9092
RECORDS=${1:-100000}
SIZE=${2:-1000}
BATCH_SIZE=${3:-100000}
LINGER_MS=${4:-10}

kafka-producer-perf-test \
    --topic $TOPIC \
    --num-records $RECORDS \
    --record-size $SIZE \
    --throughput -1 \
    --producer-props \
        bootstrap.servers=$BOOTSTRAP \
        batch.size=$BATCH_SIZE \
        linger.ms=$LINGER_MS
