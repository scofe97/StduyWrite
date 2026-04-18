# Kafka Learning PoC

Kafka 핵심 개념과 CLI 명령어 실습

## Progress Tracker

### Stage 01: Kafka 기본 CLI ✅ (완료)
- [x] 환경 구성 (Docker Compose)
- [x] 토픽 생성 (`kafka-topics`)
- [x] 메시지 생산 (`kafka-console-producer`)
- [x] 메시지 소비 (`kafka-console-consumer`)
- [x] Consumer Group 이해

**학습 내용**: 토픽, 파티션, 오프셋, Producer/Consumer, Consumer Group

### Stage 02: Topics and Messages ✅ (완료)
- [x] 멀티 파티션 토픽 생성
- [x] Key와 파티션 관계 실험
- [x] 메시지 타입 4가지 (States, Deltas, Events, Commands)
- [x] Leader, Replicas, ISR 개념

**학습 내용**: Key 기반 파티션 분배, 순서 보장 원리, 메시지 타입 선택 기준

### Stage 03: Kafka as Distributed Log ✅ (완료)
- [x] Offset 관리 (__consumer_offsets)
- [x] At-Least-Once vs At-Most-Once
- [x] 멱등성 (Idempotency) 개념
- [x] Consumer Group 리밸런싱
- [x] Sticky Partitioner

**학습 내용**: Offset 커밋 전략, 전달 보장, 리밸런싱 동작, Sticky Partitioner

### Stage 04: Reliability ✅ (완료)
- [x] ACK 전략 (acks=0, 1, all)
- [x] Replication Factor와 min.insync.replicas
- [x] 전달 보장 (At-Most-Once, At-Least-Once, Exactly-Once)
- [x] 멱등성 Producer (enable.idempotence)
- [x] Kafka 트랜잭션 개념
- [x] Leader-Follower 복제와 장애 복구
- [x] Preferred Leader Election

**학습 내용**: ACK, 복제 설정, 멱등성, 트랜잭션, 장애 복구, Leader 선출

### Stage 05: Performance ✅ (완료)
- [x] Throughput vs Latency 개념
- [x] Producer 배치 설정 (batch.size, linger.ms)
- [x] Compression (lz4, zstd, snappy)
- [x] Consumer 튜닝 (fetch.min.bytes, max.poll.records)
- [x] Kafka가 빠른 이유 (Sequential I/O, Zero-Copy, Page Cache)
- [x] OS 레벨 최적화 이해

**학습 내용**: 성능 튜닝, Long Polling, session.timeout.ms vs max.poll.interval.ms, 면접 대비

### Stage 06: Kafka Connect (예정)
- [ ] Source Connector
- [ ] Sink Connector
- [ ] Schema Registry

---

## Quick Start

### 단일 브로커 (학습용)
```bash
# 1. Kafka 시작
docker-compose up -d

# 2. 컨테이너 접속
docker exec -it kafka_learn /bin/bash

# 3. 토픽 생성
kafka-topics --create \
    --topic test-topic \
    --partitions 1 \
    --replication-factor 1 \
    --bootstrap-server localhost:9092
```

### 멀티 브로커 (복제 실습용)
```bash
# 1. 멀티 브로커 시작 (3개 브로커)
docker-compose -f docker-compose-multi.yml up -d

# 2. 컨테이너 접속
docker exec -it kafka1 /bin/bash

# 3. 복제 토픽 생성
kafka-topics --create \
    --topic replication-test \
    --partitions 3 \
    --replication-factor 3 \
    --bootstrap-server kafka1:9092
```

---

## Directory Structure

```
kafka-messaging/
├── docker-compose.yml        # Kafka 단일 브로커 (KRaft 모드)
├── docker-compose-multi.yml  # Kafka 3개 브로커 (복제 실습용)
├── README.md                 # 이 파일
├── 01-basics/
│   └── LEARNED.md            # CLI 명령어 정리
├── 02-topics-messages/
│   └── LEARNED.md            # Key, 파티션, 메시지 타입
├── 03-distributed-log/
│   └── LEARNED.md            # Offset, 전달 보장, 리밸런싱
├── 04-reliability/
│   └── LEARNED.md            # ACK, 복제, 트랜잭션, 장애 복구
└── 05-performance/
    └── LEARNED.md            # 성능 튜닝, Zero-Copy, Page Cache
```

---

## Reference

- [Confluent Kafka Docker](https://hub.docker.com/r/confluentinc/cp-kafka)
- [Kafka CLI 문서](https://kafka.apache.org/documentation/#quickstart)
- [Apache Kafka - Producer Configs](https://kafka.apache.org/documentation/#producerconfigs)
- [Confluent - Kafka Transactions](https://www.confluent.io/blog/transactions-apache-kafka/)
