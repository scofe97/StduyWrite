#!/bin/bash
# Under-replicated 파티션 모니터링

BOOTSTRAP=kafka1:9092

echo "Under-replicated partitions:"
kafka-topics --describe --under-replicated-partitions --bootstrap-server $BOOTSTRAP

echo ""
echo "Under-min-ISR partitions:"
kafka-topics --describe --under-min-isr-partitions --bootstrap-server $BOOTSTRAP
