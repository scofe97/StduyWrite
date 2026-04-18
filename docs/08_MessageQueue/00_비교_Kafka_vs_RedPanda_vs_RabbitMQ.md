# Kafka vs RedPanda vs RabbitMQ 비교 (2025-2026)

## 1. 개요

이 문서는 세 가지 주요 메시지 브로커의 특성을 비교합니다.

| 항목 | Apache Kafka | RedPanda | RabbitMQ |
|------|-------------|----------|----------|
| **출시** | 2011년 | 2020년 | 2007년 |
| **개발** | Apache Foundation | Redpanda Data | VMware (Broadcom) |
| **언어** | Java/Scala | C++ | Erlang |
| **라이선스** | Apache 2.0 | BSL 1.1 | MPL 2.0 |
| **주요 용도** | 이벤트 스트리밍 | 이벤트 스트리밍 | 메시지 큐 + 스트리밍 |

---

## 2. 아키텍처 비교

### 2.1 핵심 설계 철학

| 시스템 | 설계 철학 |
|--------|----------|
| **Kafka** | 분산 커밋 로그, 높은 처리량, 내구성 우선 |
| **RedPanda** | Kafka 호환 + 단순화된 운영 + 성능 최적화 |
| **RabbitMQ** | 유연한 라우팅, 다중 프로토콜, 전통적 메시징 |

### 2.2 메타데이터 관리

| 시스템 | 방식 | 상태 |
|--------|------|------|
| **Kafka** | KRaft (4.0+) | ZooKeeper 제거됨 |
| **RedPanda** | 내장 Raft | 처음부터 독립적 |
| **RabbitMQ** | Khepri (4.0+) | Mnesia에서 전환 중 |

### 2.3 데이터 복제

| 시스템 | 복제 방식 | 특징 |
|--------|----------|------|
| **Kafka** | ISR (In-Sync Replicas) | Leader가 ISR 관리 |
| **RedPanda** | Raft | Quorum 기반 합의 |
| **RabbitMQ** | Raft (Quorum Queues) | Quorum 기반 합의 |

### 2.4 메시지 전달 모델

```
Kafka / RedPanda:
  Pull 기반 - Consumer가 Broker에서 데이터를 가져감
  → 백프레셔 자연 처리, 배치 처리에 유리

RabbitMQ (Queue):
  Push 기반 - Broker가 Consumer에게 메시지 전달
  → 저지연, Prefetch로 흐름 제어

RabbitMQ (Streams):
  Pull 기반 - Kafka와 유사
```

---

## 3. 성능 비교

### 3.1 처리량 (Throughput)

| 시스템 | 단일 노드 | 클러스터 (3노드) |
|--------|----------|-----------------|
| **Kafka** | 200-400 MB/s | 600+ MB/s |
| **RedPanda** | 300-500 MB/s | 600+ MB/s |
| **RabbitMQ (Queue)** | 30-100 MB/s | 100-200 MB/s |
| **RabbitMQ (Streams)** | 100+ MB/s | 300+ MB/s |

### 3.2 지연시간 (Latency)

| 시스템 | P99 (저부하) | P99 (고부하) |
|--------|-------------|-------------|
| **Kafka** | ~5ms | 10-20ms |
| **RedPanda** | ~2-3ms | 5-10ms |
| **RabbitMQ** | <1ms | 지원 불가 (처리량 한계) |

### 3.3 메시지 처리량 (msg/sec)

| 시스템 | 작은 메시지 (1KB) |
|--------|------------------|
| **Kafka** | 50만 - 100만+ |
| **RedPanda** | 50만 - 100만+ |
| **RabbitMQ (Queue)** | 5만 - 10만 |
| **RabbitMQ (Streams)** | 100만+ |

---

## 4. 기능 비교

### 4.1 메시지 모델

| 기능 | Kafka | RedPanda | RabbitMQ |
|------|-------|----------|----------|
| **Pub/Sub** | ✅ | ✅ | ✅ |
| **Point-to-Point** | 제한적 | 제한적 | ✅ |
| **메시지 보존** | ✅ (기본) | ✅ (기본) | Streams만 |
| **메시지 재생** | ✅ | ✅ | Streams만 |
| **복잡한 라우팅** | ❌ | ❌ | ✅ (Exchange) |
| **우선순위 큐** | ❌ | ❌ | ✅ |
| **메시지 TTL** | ✅ | ✅ | ✅ |
| **Dead Letter** | ❌ | ❌ | ✅ |

### 4.2 프로토콜 지원

| 프로토콜 | Kafka | RedPanda | RabbitMQ |
|---------|-------|----------|----------|
| **Kafka Protocol** | ✅ | ✅ | ❌ |
| **AMQP 0-9-1** | ❌ | ❌ | ✅ |
| **AMQP 1.0** | ❌ | ❌ | ✅ |
| **MQTT** | ❌ | ❌ | ✅ |
| **STOMP** | ❌ | ❌ | ✅ |
| **HTTP/REST** | REST Proxy | Pandaproxy | Management API |

### 4.3 에코시스템

| 기능 | Kafka | RedPanda | RabbitMQ |
|------|-------|----------|----------|
| **Schema Registry** | Confluent (별도) | 내장 | ❌ |
| **Stream Processing** | Kafka Streams | Kafka Streams 호환 | ❌ |
| **Connect** | Kafka Connect | Kafka Connect 호환 | Shovel/Federation |
| **KSQL/ksqlDB** | ✅ | ✅ 호환 | ❌ |

---

## 5. 고가용성 비교

### 5.1 도입 시점

| 시스템 | 기능 | 도입 시점 |
|--------|------|----------|
| **Kafka** | 파티션 복제 | 초기부터 |
| **Kafka** | KRaft | 4.0 (2025.03) |
| **RedPanda** | Raft 복제 | 초기부터 |
| **RabbitMQ** | Quorum Queues | 3.8 (2019) |
| **RabbitMQ** | Streams | 3.9 (2021) |
| **RabbitMQ** | Khepri | 4.0 (2024) |

### 5.2 장애 복구

| 항목 | Kafka | RedPanda | RabbitMQ |
|------|-------|----------|----------|
| **리더 선출** | KRaft/ISR | Raft | Raft |
| **복구 시간** | 빠름 (KRaft) | 빠름 | 빠름 |
| **Split-brain 방지** | ✅ | ✅ | ✅ (Quorum) |
| **롤링 업그레이드** | ✅ | ✅ | ✅ |

---

## 6. 운영 복잡도

### 6.1 설치 및 설정

| 항목 | Kafka | RedPanda | RabbitMQ |
|------|-------|----------|----------|
| **외부 의존성** | 없음 (4.0+) | 없음 | 없음 |
| **바이너리 수** | 1 (KRaft) | 1 | 1 |
| **기본 설정** | 많은 튜닝 필요 | 자동 튜닝 | 중간 |
| **JVM 튜닝** | 필요 | 불필요 | 불필요 |

### 6.2 모니터링

| 항목 | Kafka | RedPanda | RabbitMQ |
|------|-------|----------|----------|
| **메트릭** | JMX | Prometheus | Prometheus |
| **관리 UI** | 별도 (AKHQ 등) | Console | Management UI (내장) |
| **CLI** | kafka-* | rpk | rabbitmqctl |

### 6.3 Kubernetes 운영

| 항목 | Kafka | RedPanda | RabbitMQ |
|------|-------|----------|----------|
| **Operator** | Strimzi | RedPanda Operator | RabbitMQ Operator |
| **성숙도** | 높음 | 중간 | 높음 |
| **Helm** | ✅ | ✅ | ✅ |

---

## 7. 비용 및 라이선스

### 7.1 라이선스 비교

| 시스템 | 라이선스 | 상용 제한 |
|--------|---------|----------|
| **Kafka** | Apache 2.0 | 없음 |
| **RedPanda** | BSL 1.1 | 경쟁 SaaS 서비스 제공 금지 |
| **RabbitMQ** | MPL 2.0 | 없음 |

### 7.2 인프라 비용 (추정)

| 워크로드 | Kafka | RedPanda | RabbitMQ |
|---------|-------|----------|----------|
| **100MB/s** | 3-5 노드 | 3 노드 | 5-10 노드 |
| **500MB/s** | 6-9 노드 | 3-5 노드 | 지원 어려움 |

### 7.3 관리형 서비스

| 시스템 | 서비스 |
|--------|--------|
| **Kafka** | Confluent Cloud, AWS MSK, Azure Event Hubs |
| **RedPanda** | Redpanda Cloud |
| **RabbitMQ** | CloudAMQP, AWS Amazon MQ |

---

## 8. 사용 사례별 추천

### 8.1 추천 매트릭스

| 사용 사례 | 1순위 | 2순위 | 비고 |
|---------|-------|-------|------|
| **대용량 이벤트 스트리밍** | Kafka | RedPanda | 처리량 우선 |
| **실시간 분석 파이프라인** | Kafka | RedPanda | 에코시스템 |
| **마이크로서비스 통신** | RabbitMQ | Kafka | 라우팅 유연성 |
| **작업 큐 (Task Queue)** | RabbitMQ | - | Push 모델 |
| **IoT 메시징** | RabbitMQ | - | MQTT 지원 |
| **Kafka 대체 (비용 절감)** | RedPanda | - | 적은 노드 |
| **Kafka 대체 (단순 운영)** | RedPanda | - | 자동 튜닝 |
| **로그 수집** | Kafka | RedPanda | 보존 + 재처리 |
| **이벤트 소싱** | Kafka | RedPanda | 영구 저장 |
| **CDC (Change Data Capture)** | Kafka | RedPanda | Debezium 연동 |

### 8.2 결정 플로우차트

```
┌─────────────────────────────────────────────────────────────┐
│                    선택 가이드                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 복잡한 라우팅이 필요한가?                                │
│     └─ YES → RabbitMQ                                       │
│     └─ NO → 2번으로                                         │
│                                                             │
│  2. 메시지 재처리/장기 보존이 핵심인가?                       │
│     └─ YES → Kafka 또는 RedPanda                            │
│     └─ NO → 3번으로                                         │
│                                                             │
│  3. MQTT/AMQP 프로토콜이 필요한가?                           │
│     └─ YES → RabbitMQ                                       │
│     └─ NO → 4번으로                                         │
│                                                             │
│  4. 기존 Kafka 인프라/경험이 있는가?                         │
│     └─ YES → Kafka (또는 RedPanda로 마이그레이션)            │
│     └─ NO → 5번으로                                         │
│                                                             │
│  5. 운영 단순화가 우선인가?                                  │
│     └─ YES → RedPanda                                       │
│     └─ NO → Kafka (에코시스템 풍부)                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. 마이그레이션 고려사항

### 9.1 Kafka → RedPanda

```
난이도: 낮음

장점:
- Kafka 클라이언트 그대로 사용
- 토픽 구조 호환
- 설정 대부분 호환

주의:
- 일부 고급 설정 차이
- Kafka Streams 상태 저장소 마이그레이션
```

### 9.2 RabbitMQ → Kafka/RedPanda

```
난이도: 높음

필요 작업:
- 아키텍처 재설계 (Push → Pull)
- Exchange/Binding 로직 → 토픽 구조로 변환
- 클라이언트 코드 전면 수정
- Dead Letter, Priority 등 대안 구현
```

### 9.3 Kafka (ZooKeeper) → Kafka (KRaft)

```
난이도: 중간

경로:
1. Kafka 3.9로 업그레이드 (브릿지 버전)
2. KRaft 마이그레이션 실행
3. Kafka 4.0으로 업그레이드

주의:
- 마이그레이션 후 롤백 불가
- 2025년 11월까지 ZK 보안 패치 지원
```

---

## 10. 2025-2026 트렌드

### 10.1 각 시스템의 방향

| 시스템 | 트렌드 |
|--------|--------|
| **Kafka** | KRaft 완성, Tiered Storage 강화, 클라우드 네이티브 |
| **RedPanda** | 기능 확장, 엔터프라이즈 기능, 클라우드 서비스 |
| **RabbitMQ** | Khepri 기본화, Streams 성숙화, 4.x 안정화 |

### 10.2 시장 현황

```
Kafka: 업계 표준, 가장 큰 에코시스템
RedPanda: 빠르게 성장, Kafka 대안으로 자리잡는 중
RabbitMQ: 전통적 메시징에서 여전히 강세, 스트리밍 기능 강화 중
```

---

## 11. 메시지 브로커 vs 이벤트 브로커

### 11.1 분류

| 유형 | 특징 | 대표 제품 |
|------|------|----------|
| **메시지 브로커** | 처리 후 메시지 삭제 | RabbitMQ, Redis Queue |
| **이벤트 브로커** | 메시지 보존, 재처리 가능 | Kafka, RedPanda, Kinesis |

### 11.2 핵심 차이

```
메시지 브로커 (RabbitMQ):
  - Smart Broker / Dumb Consumer
  - Broker가 메시지 관리 담당
  - 메시지 처리 후 즉시 삭제
  - 메모리 기반 (빠르지만 유실 위험)

이벤트 브로커 (Kafka/RedPanda):
  - Dumb Broker / Smart Consumer
  - Consumer가 Offset 관리
  - 메시지 보존 (TTL까지)
  - 디스크 기반 (안전, 재처리 가능)
```

### 11.3 관계

- 메시지 브로커는 이벤트 브로커 역할을 **할 수 없음**
- 이벤트 브로커는 메시지 브로커 역할을 **할 수 있음**
- Kafka/RedPanda는 두 역할 모두 수행 가능

---

## 12. 동기 vs 비동기 통신

### 12.1 비교

| 방식 | 설명 | 비유 |
|------|------|------|
| **동기** | 보내는 순간 받아야 함 | 무전기 |
| **비동기** | 나중에 받아도 됨 | 택배함/이메일 |

### 12.2 메시지 큐 장점

| 장점 | 설명 |
|------|------|
| **디커플링** | Producer/Consumer 독립적 |
| **유연성** | 수신자 추가/삭제 자유로움 |
| **안정성** | 메시지 유실 방지 |
| **확장성** | 수평적 확장 용이 |

---

## 13. 관련 문서

### 13.1 MessageQueue 루트 문서
- `01_Cache_vs_MQ_사용시점.md` - Cache와 MQ 선택 기준
- `02_대기열시스템_Redis_vs_Kafka.md` - 대기열에서 Redis vs Kafka
- `03_메시지브로커_vs_이벤트브로커.md` - 브로커 유형 상세 비교
- `04_메시지큐_기초개념.md` - MQ 기초 개념
- `05_채팅시스템_디자인_MQ활용.md` - 실제 시스템 설계 예시

### 13.2 하위 폴더 문서
- `Kafka/` - Apache Kafka 상세 문서 (18개 챕터)
- `RabbitMQ/` - RabbitMQ 상세 문서 (Quorum Queues, Streams, Khepri 등)
- `RedPanda/` - RedPanda 상세 문서 (아키텍처, 성능 벤치마크)
- `Redis/` - Redis 메시지 큐 상세 문서 (Streams, Pub/Sub, List, Sorted Set, 고가용성)

---

## 14. 참고 자료

### Kafka
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka 4.0 KRaft - InfoQ](https://www.infoq.com/news/2025/04/kafka-4-kraft-architecture/)
- [Confluent Blog](https://www.confluent.io/blog/)

### RedPanda
- [RedPanda Documentation](https://docs.redpanda.com/)
- [RedPanda vs Kafka Benchmark](https://www.redpanda.com/blog/redpanda-vs-kafka-performance-benchmark)
- [Independent Analysis](https://jack-vanlightly.com/blog/2023/5/15/kafka-vs-redpanda-performance-do-the-claims-add-up)

### RabbitMQ
- [RabbitMQ Documentation](https://www.rabbitmq.com/docs)
- [Quorum Queues](https://www.rabbitmq.com/docs/quorum-queues)
- [RabbitMQ Streams Overview](https://blog.rabbitmq.com/posts/2021/07/rabbitmq-streams-overview/)
- [Khepri Roadmap](https://www.rabbitmq.com/blog/2025/09/01/6-khepri-default)
