#!/bin/bash
# 토픽 정리

BOOTSTRAP=kafka1:9092

kafka-topics --delete --topic replication-test --bootstrap-server $BOOTSTRAP 2>/dev/null
kafka-topics --delete --topic idempotent-test --bootstrap-server $BOOTSTRAP 2>/dev/null

echo "Topics deleted."
echo "To stop cluster (on host): docker-compose -f docker-compose-multi.yml down"
