# RabbitMQ Quorum Queues - 면접 정리

## 핵심 한 줄 정리

> **Quorum Queue는 Raft 합의 알고리즘 기반의 복제 큐로, 과반수(Quorum) 노드 확인 후 메시지를 커밋하여 고가용성과 데이터 안전성을 보장합니다.**

---

## 면접 필수 암기

### Q1. Quorum Queue란 무엇인가요?

**답변 (30초):**
> Quorum Queue는 RabbitMQ 3.8(2019년)에 도입된 복제 큐 타입입니다. Raft 합의 알고리즘을 사용하여 여러 노드에 메시지를 복제합니다. 메시지는 과반수(Quorum) 노드가 확인해야 커밋되므로, 노드 장애에도 데이터 손실 없이 서비스를 지속할 수 있습니다. 기존 Classic Mirrored Queue의 문제점을 해결하기 위해 도입되었고, RabbitMQ 4.0에서 Mirrored Queue가 제거되면서 고가용성의 표준이 되었습니다.

---

### Q2. Quorum의 의미와 계산 방법은?

**답변:**
> Quorum은 "의사결정에 필요한 최소 인원"을 의미합니다. Raft에서는 **과반수**입니다.
>
> ```
> Quorum = (노드 수 / 2) + 1
> ```
>
> | 노드 수 | Quorum | 허용 장애 |
> |--------|--------|----------|
> | 3 | 2 | 1대 |
> | 5 | 3 | 2대 |
> | 7 | 4 | 3대 |
>
> 따라서 **홀수 노드**가 효율적입니다. 4대나 5대나 허용 장애가 2대로 동일하기 때문입니다.

---

### Q3. Quorum Queue의 동작 원리를 설명해주세요.

**답변:**
> 1. **Leader**가 Producer로부터 메시지 수신
> 2. Leader가 **WAL(Write-Ahead Log)**에 기록
> 3. Leader가 모든 **Follower**에게 복제 명령 전송
> 4. **Quorum(과반수)** Follower가 확인 응답
> 5. Leader가 메시지 **커밋** 후 Producer에게 확인
>
> 이 과정 덕분에 Leader가 장애나도 Follower 중 하나가 새 Leader가 되어 데이터 손실 없이 계속 동작합니다.

---

### Q4. Classic Mirrored Queue 대비 Quorum Queue의 장점은?

**답변:**

| 항목 | Classic Mirrored | Quorum Queue |
|------|-----------------|--------------|
| **합의 방식** | 비동기 복제 | Raft (동기 Quorum) |
| **Split-brain** | 취약 | 방지됨 |
| **복구** | 수동 개입 필요 | 자동 리더 선출 |
| **동기화** | 전체 동기화 필요 | 증분 복제 |
| **성능** | 동기화 시 저하 | 일관된 성능 |

> Classic Mirrored Queue는 "모든 미러에 복제" 방식이라 네트워크 파티션 시 Split-brain이 발생할 수 있었습니다. Quorum Queue는 Raft의 Leader 선출과 Quorum 합의로 이 문제를 원천 해결합니다.

---

### Q5. Quorum Queue를 사용하면 안 되는 경우는?

**답변:**
> 1. **임시 큐**: transient/exclusive 큐는 복제 오버헤드가 불필요
> 2. **극도의 저지연**: Quorum 확인으로 인한 추가 지연 발생
> 3. **매우 긴 백로그**: 500만+ 메시지 시 Streams가 더 효율적
> 4. **대규모 팬아웃**: 수천 Consumer 시 Streams 권장
> 5. **높은 큐 churn**: 큐가 자주 생성/삭제되는 경우

---

## 깊은 이해를 위한 설명

### Raft 알고리즘의 핵심

Raft는 분산 합의 알고리즘으로, 다음 세 가지 역할로 구성됩니다:

1. **Leader**: 모든 쓰기 요청을 처리하고 Follower에 복제
2. **Follower**: Leader의 명령을 따르고 데이터 복제
3. **Candidate**: Leader 선출 시 후보 상태

**Leader 선출 과정:**
```
1. Leader의 heartbeat가 timeout 동안 없음
2. Follower가 Candidate로 전환
3. 자신에게 투표하고 다른 노드에 투표 요청
4. 과반수 투표 받으면 새 Leader
5. 새 Leader가 heartbeat 전송 시작
```

이 메커니즘 덕분에 Leader 장애 시 **자동으로** 새 Leader가 선출됩니다.

### WAL(Write-Ahead Log)의 역할

```
메시지 수신 → WAL 기록 → 메모리 반영 → 응답

장애 복구 시:
WAL 재생 → 메모리 상태 복원
```

> WAL은 "먼저 기록하고 나중에 처리"하는 패턴입니다. 장애가 발생해도 WAL을 재생하면 상태를 복구할 수 있어 데이터 안전성을 보장합니다.

### 언제 Quorum Queue를 선택해야 하나?

**반드시 사용해야 하는 경우:**
- 결제, 주문 등 **데이터 손실이 치명적**인 시스템
- **무중단 운영**이 필수인 서비스
- **클러스터 환경**에서 노드 장애 대비

**Classic Queue로 충분한 경우:**
- 개발/테스트 환경
- 캐시성 데이터 (손실 허용)
- 단일 노드 운영

---

## 코드 레벨 이해

### Quorum Queue 선언

```java
Map<String, Object> args = new HashMap<>();
args.put("x-queue-type", "quorum");  // 핵심!
args.put("x-quorum-initial-group-size", 3);  // 복제 노드 수

channel.queueDeclare(
    "orders-queue",
    true,   // durable (필수 true)
    false,  // exclusive (필수 false)
    false,  // autoDelete (필수 false)
    args
);
```

> Quorum Queue는 반드시 `durable=true`여야 합니다. 복제의 의미가 데이터 보존이기 때문입니다.

### 정책으로 일괄 적용

```bash
# "quorum-" 접두사 큐를 모두 Quorum Queue로
rabbitmqctl set_policy quorum-policy \
    "^quorum-.*" \
    '{"queue-type": "quorum"}' \
    --apply-to queues
```

---

## 면접 예상 꼬리 질문

### Q. Quorum Queue에서 네트워크 파티션이 발생하면?

**답변:**
> Quorum이 유지되는 파티션만 쓰기를 처리합니다. 예를 들어 5노드에서 2-3으로 분리되면, 3노드 파티션만 동작합니다. 2노드 파티션의 클라이언트는 쓰기 실패를 받습니다. 네트워크 복구 후 2노드가 다시 합류하면 자동으로 동기화됩니다.

### Q. Quorum Queue의 성능 오버헤드는?

**답변:**
> Classic Queue 대비 약 **10-20% 처리량 감소**가 일반적입니다. 이는 Quorum 확인을 기다리는 시간 때문입니다. 하지만 Classic Mirrored Queue의 동기화 시 발생하던 **급격한 성능 저하는 없습니다**. 일관된 성능을 유지합니다.

### Q. RabbitMQ 4.0에서 고가용성을 어떻게 구성하나요?

**답변:**
> RabbitMQ 4.0에서 Classic Mirrored Queue가 제거되었으므로, **Quorum Queue가 유일한 고가용성 옵션**입니다. 최소 3노드 클러스터를 구성하고, 중요한 큐는 모두 `x-queue-type: quorum`으로 선언합니다. 메타데이터 고가용성은 새로운 **Khepri** 저장소가 담당합니다.

### Q. Kafka의 ISR과 RabbitMQ Quorum Queue의 차이는?

**답변:**
> **Kafka ISR**: Leader가 "동기화된 복제본 목록"을 관리합니다. 지연된 복제본은 ISR에서 제외되고, `min.insync.replicas` 설정으로 최소 복제 수를 지정합니다.
>
> **Quorum Queue**: Raft 합의로 **항상 과반수 확인**이 필요합니다. 동적으로 복제본을 제외하지 않습니다.
>
> Quorum Queue가 더 **엄격한 일관성**을 보장하지만, Kafka ISR이 **더 유연한 성능 조절**을 허용합니다.
