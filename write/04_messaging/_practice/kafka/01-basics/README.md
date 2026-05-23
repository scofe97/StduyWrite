# Stage 01: Kafka 기초

Kafka 기본 CLI 명령어와 핵심 개념 학습

## 학습 내용

- Kafka 정의와 핵심 기능 (Publish/Subscribe, Store, Process)
- Kafka 아키텍처 (Broker, Topic, Partition, Consumer Group)
- 주요 CLI 명령어 (kafka-topics, kafka-console-producer, kafka-console-consumer)
- Offset 개념 (Current Offset, Committed Offset, LAG)

## 관련 이론

- [Chapter 1: Introduction to Apache Kafka](../../../docs/08_MessageQueue/Kafka/01_Introduction_to_Apache_Kafka.md)
- [Chapter 2: First Steps with Kafka](../../../docs/08_MessageQueue/Kafka/02_First_Steps_with_Kafka.md)

## 실습 환경

```bash
# Kafka 클러스터 시작
docker-compose up -d

# 토픽 생성
kafka-topics --create \
    --topic products.prices.changelog \
    --partitions 3 \
    --replication-factor 1 \
    --bootstrap-server localhost:9092

# 메시지 생산
kafka-console-producer \
    --topic products.prices.changelog \
    --bootstrap-server localhost:9092

# 메시지 소비
kafka-console-consumer \
    --topic products.prices.changelog \
    --from-beginning \
    --bootstrap-server localhost:9092
```

## 다음 단계

- [02-topics-messages](../02-topics-messages/): 토픽과 메시지 구조 심화
