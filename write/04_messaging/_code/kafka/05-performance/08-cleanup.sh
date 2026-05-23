#!/bin/bash
# 토픽 정리

BOOTSTRAP=kafka1:9092

kafka-topics --delete --topic perf-test --bootstrap-server $BOOTSTRAP 2>/dev/null

echo "Topics deleted."
