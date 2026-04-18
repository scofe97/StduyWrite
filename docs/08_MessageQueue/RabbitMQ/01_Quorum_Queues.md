# RabbitMQ Quorum Queues

## 1. 개요

Quorum Queues는 **RabbitMQ 3.8.0 (2019년 가을)**에 도입된 복제 기반 큐 타입입니다. Raft 합의 알고리즘을 사용하여 고가용성과 데이터 안전성을 제공합니다.

### 도입 배경

기존 Classic Mirrored Queues의 문제점:
- 동기화 중 성능 저하
- 네트워크 파티션 시 예측 불가능한 동작
- Split-brain 문제
- 복잡한 복구 절차

→ **Quorum Queues는 이러한 문제를 Raft 알고리즘으로 해결**

---

## 2. 아키텍처

### Raft 합의 알고리즘

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Leader    │────▶│  Follower   │────▶│  Follower   │
│   (Node 1)  │     │   (Node 2)  │     │   (Node 3)  │
└─────────────┘     └─────────────┘     └─────────────┘
       │
       ▼
  Write-Ahead Log (WAL)
```

### 동작 방식

1. **메시지 수신**: Leader가 Producer로부터 메시지 수신
2. **WAL 기록**: Leader가 Write-Ahead Log에 기록
3. **복제**: Leader가 Follower들에게 복제 명령 전송
4. **Quorum 확인**: 과반수(Quorum) 노드가 확인 응답
5. **Commit**: Leader가 메시지 커밋 후 Producer에게 확인

### Quorum (정족수)

```
Quorum = (Replication Factor / 2) + 1

예시:
- 3 노드: Quorum = 2 (1 노드 장애 허용)
- 5 노드: Quorum = 3 (2 노드 장애 허용)
- 7 노드: Quorum = 4 (3 노드 장애 허용)
```

---

## 3. 주요 특징

### 데이터 안전성
| 특성 | 설명 |
|------|------|
| **복제** | 모든 메시지가 Quorum 노드에 복제 |
| **지속성** | 기본적으로 디스크에 저장 |
| **순서 보장** | FIFO 순서 보장 |

### 고가용성
| 특성 | 설명 |
|------|------|
| **자동 리더 선출** | 리더 장애 시 Raft로 새 리더 선출 |
| **무중단 운영** | Quorum 유지 시 서비스 지속 |
| **롤링 업그레이드** | 순차적 노드 업그레이드 지원 |

---

## 4. 버전별 기능 발전

| 버전 | 추가 기능 |
|------|----------|
| **3.8.0** | Quorum Queues 최초 도입 |
| **3.9.x** | 성능 개선, 메모리 최적화 |
| **3.10.x** | Message TTL 지원, Dead Letter 전략 개선 |
| **4.0** | **우선순위 큐 지원**, Classic Mirrored Queue 제거 |

---

## 5. 사용 방법

### 큐 선언 (AMQP)

```java
Map<String, Object> args = new HashMap<>();
args.put("x-queue-type", "quorum");

channel.queueDeclare(
    "my-quorum-queue",  // 큐 이름
    true,               // durable (반드시 true)
    false,              // exclusive
    false,              // autoDelete
    args                // arguments
);
```

### 정책 기반 설정

```bash
rabbitmqctl set_policy quorum-policy \
    "^quorum\." \
    '{"queue-type": "quorum"}' \
    --apply-to queues
```

### 복제 팩터 설정

```java
args.put("x-quorum-initial-group-size", 5); // 5개 노드에 복제
```

---

## 6. Classic Queue vs Quorum Queue

| 항목 | Classic Queue | Quorum Queue |
|------|--------------|--------------|
| **복제** | 없음 (Mirrored 제거됨) | Raft 기반 자동 복제 |
| **데이터 안전성** | 낮음 | 높음 |
| **성능** | 높음 (단일 노드) | 중간 (복제 오버헤드) |
| **장애 복구** | 수동 | 자동 (리더 선출) |
| **메모리 사용** | 낮음 | 높음 |
| **메시지 TTL** | 지원 | 3.10+ 지원 |
| **우선순위** | 지원 | 4.0+ 지원 |

---

## 7. 언제 사용해야 하는가?

### 적합한 경우
- **데이터 손실이 허용되지 않는 경우**
- 노드 장애에도 서비스 지속이 필요한 경우
- 클러스터 환경에서 운영하는 경우
- 업그레이드/유지보수 중 무중단 운영 필요 시

### 부적합한 경우
- **임시 큐** (transient/exclusive queues)
- **극도로 낮은 지연시간**이 필요한 경우
- **매우 긴 큐 백로그** (500만+ 메시지) → Streams 권장
- **대규모 팬아웃** → Streams 권장
- 높은 큐 churn (큐가 자주 생성/삭제되는 경우)

---

## 8. 모니터링

### 주요 메트릭

```bash
# 큐 상태 확인
rabbitmqctl list_queues name type leader members

# Raft 상태 확인
rabbitmq-diagnostics quorum_queue_status <queue-name>
```

### 관찰할 지표
- **Leader 분포**: 리더가 특정 노드에 집중되지 않도록
- **복제 지연**: Follower 동기화 상태
- **메모리 사용량**: Quorum Queue는 더 많은 메모리 사용
- **디스크 I/O**: WAL 기록으로 인한 디스크 부하

---

## 9. 마이그레이션 (Classic Mirrored → Quorum)

RabbitMQ 4.0에서 Classic Mirrored Queues가 제거되었으므로 마이그레이션 필수:

### 마이그레이션 전략

1. **새 Quorum Queue 생성**
2. **Shovel/Federation으로 메시지 이동**
3. **애플리케이션 연결 전환**
4. **기존 큐 삭제**

```bash
# Shovel 설정 예시
rabbitmqctl set_parameter shovel migrate-to-quorum \
  '{"src-uri": "amqp://", "src-queue": "old-mirrored-queue",
    "dest-uri": "amqp://", "dest-queue": "new-quorum-queue"}'
```

---

## 10. 참고 자료

- [RabbitMQ Quorum Queues 공식 문서](https://www.rabbitmq.com/docs/quorum-queues)
- [Migrating to Quorum Queues (2025)](https://www.rabbitmq.com/blog/2025/07/29/latest-benefits-of-rmq-and-migrating-to-qq-along-the-way)
- [CloudAMQP - RabbitMQ 3.8 Quorum Queues](https://www.cloudamqp.com/blog/rabbitmq-quorum-queues.html)
