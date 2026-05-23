#!/bin/bash
# Consumer 성능 측정

TOPIC=perf-test
BOOTSTRAP=kafka1:9092
MESSAGES=${1:-100000}

kafka-consumer-perf-test \
    --topic $TOPIC \
    --messages $MESSAGES \
    --bootstrap-server $BOOTSTRAP
