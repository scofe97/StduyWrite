#!/bin/bash
# Producer 압축 성능 측정

TOPIC=perf-test
BOOTSTRAP=kafka1:9092
RECORDS=${1:-100000}
SIZE=${2:-1000}
COMPRESSION=${3:-lz4}

kafka-producer-perf-test \
    --topic $TOPIC \
    --num-records $RECORDS \
    --record-size $SIZE \
    --throughput -1 \
    --producer-props \
        bootstrap.servers=$BOOTSTRAP \
        batch.size=100000 \
        linger.ms=10 \
        compression.type=$COMPRESSION
