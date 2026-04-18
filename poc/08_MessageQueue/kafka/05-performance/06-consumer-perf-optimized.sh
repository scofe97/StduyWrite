#!/bin/bash
# Consumer 최적화 성능 측정

TOPIC=perf-test
BOOTSTRAP=kafka1:9092
MESSAGES=${1:-100000}

# consumer.properties 생성
cat > /tmp/consumer.properties << EOF
fetch.min.bytes=1000000
fetch.max.wait.ms=500
EOF

kafka-consumer-perf-test \
    --topic $TOPIC \
    --messages $MESSAGES \
    --consumer.config /tmp/consumer.properties \
    --bootstrap-server $BOOTSTRAP

rm -f /tmp/consumer.properties
