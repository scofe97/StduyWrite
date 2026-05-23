#!/bin/bash
# Producer 기본 성능 측정 (baseline)

TOPIC=perf-test
BOOTSTRAP=kafka1:9092
RECORDS=${1:-100000}
SIZE=${2:-1000}

kafka-producer-perf-test \
    --topic $TOPIC \
    --num-records $RECORDS \
    --record-size $SIZE \
    --throughput -1 \
    --producer-props bootstrap.servers=$BOOTSTRAP
