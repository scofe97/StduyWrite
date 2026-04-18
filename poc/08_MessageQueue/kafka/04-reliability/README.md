# Kafka Reliability 실습

## 관련 이론

- [Chapter 5: Reliability](../../../docs/08_MessageQueue/Kafka/05_Reliability.md)

## 시작

```bash
docker exec -it kafka1 /bin/bash
cd /labs/04-reliability
```

## 실습 순서

| 스크립트 | 설명 |
|---------|------|
| `01-create-replicated-topic.sh` | 복제 토픽 생성 (RF=3, min.insync=2) |
| `02-broker-failover.sh` | 브로커 장애/복구/Leader Election |
| `03-ack-comparison.sh` | ACK 성능 비교 |
| `04-under-replicated.sh` | 파티션 모니터링 |
| `05-idempotent-producer.sh` | 멱등성 Producer |
| `06-cleanup.sh` | 정리 |

## 핵심 명령어

```bash
# 토픽 상태
kafka-topics --describe --topic TOPIC --bootstrap-server kafka1:9092

# Under-replicated 확인
kafka-topics --describe --under-replicated-partitions --bootstrap-server kafka1:9092

# Leader Election
kafka-leader-election --election-type preferred --all-topic-partitions --bootstrap-server kafka1:9092
```
