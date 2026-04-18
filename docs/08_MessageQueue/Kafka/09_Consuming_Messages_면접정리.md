# Chapter 9: Consuming Messages - 면접 및 실무 가이드

> Consumer의 메시지 소비 과정과 Consumer Group 메커니즘을 면접과 실무 관점에서 상세히 정리한 문서입니다.

---

## 1. Fetch 기반 메시지 소비

### 1.1 Push vs Pull 모델

**면접 답변 예시:**

> "Kafka Consumer는 Pull(Fetch) 기반 모델을 사용합니다. 브로커가 메시지를 Consumer에게 밀어넣는(Push) 것이 아니라, Consumer가 브로커에게 '이 파티션의 이 오프셋부터 데이터를 달라'고 요청합니다.
>
> Pull 모델의 장점은 Consumer가 자신의 처리 속도에 맞게 데이터를 가져갈 수 있다는 것입니다. 처리가 느린 Consumer는 천천히 가져가고, 빠른 Consumer는 빠르게 가져갑니다. Push 모델에서는 브로커가 Consumer의 상태를 모르기 때문에 과부하가 발생할 수 있습니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Push 모델 (RabbitMQ 등)                                    │
│                                                             │
│  Broker ──push──▶ Consumer 1 (처리 빠름) ✓                  │
│  Broker ──push──▶ Consumer 2 (처리 느림) ⚠️ 과부하          │
│  Broker ──push──▶ Consumer 3 (장애 상태) ✗ 메시지 손실      │
│                                                             │
│  • 브로커가 전송 속도 결정                                   │
│  • Consumer 상태 파악 어려움                                 │
│  • 백프레셔 구현 복잡                                        │
├─────────────────────────────────────────────────────────────┤
│  Pull 모델 (Kafka)                                          │
│                                                             │
│  Consumer 1 ──Fetch(빠름)──▶ Broker ──Response──▶ Consumer 1│
│  Consumer 2 ──Fetch(느림)──▶ Broker ──Response──▶ Consumer 2│
│  Consumer 3 ──(요청 없음)─── Broker                         │
│                                                             │
│  • Consumer가 자신의 속도로 요청                             │
│  • 자연스러운 백프레셔                                       │
│  • 브로커 구현 단순화                                        │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Fetch Request 상세

**면접 질문: "Consumer의 Fetch 요청은 어떻게 동작하나요?"**

> "Consumer가 Fetch 요청을 보낼 때 파티션과 시작 오프셋을 지정합니다. 브로커는 해당 오프셋부터 데이터를 읽어 응답합니다. 이때 여러 설정이 동작에 영향을 줍니다.
>
> `fetch.min.bytes`는 최소 반환 바이트를 지정합니다. 데이터가 이 값보다 적으면 브로커는 `fetch.max.wait.ms`까지 대기합니다.
>
> 이 두 설정의 조합으로 '롱 폴링(Long Polling)' 효과를 구현합니다. 새 메시지가 없어도 연결을 유지하다가 메시지가 도착하면 즉시 응답하여 지연 시간을 줄입니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Fetch Request 처리 흐름                                     │
│                                                             │
│  Consumer                 Broker                            │
│     │                        │                              │
│     │──FetchRequest──────────▶│                              │
│     │   {                    │                              │
│     │     topic: "orders",   │                              │
│     │     partition: 0,      │                              │
│     │     offset: 1000,      │                              │
│     │     max_bytes: 1MB     │                              │
│     │   }                    │                              │
│     │                        │                              │
│     │                        │──▶ Page Cache / Disk 조회    │
│     │                        │                              │
│     │                        │──▶ 데이터 있음?              │
│     │                        │    │                         │
│     │                        │    ├─ Yes: 즉시 응답         │
│     │                        │    │                         │
│     │                        │    └─ No (또는 min.bytes 미달)│
│     │                        │        │                     │
│     │                        │        ▼                     │
│     │                        │    Purgatory에서 대기        │
│     │                        │    (max.wait.ms까지)         │
│     │                        │        │                     │
│     │                        │        ▼                     │
│     │◀──FetchResponse────────│    조건 충족 시 응답         │
│     │   {                    │                              │
│     │     records: [...],    │                              │
│     │     highWatermark: 1050│                              │
│     │   }                    │                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Fetch 관련 설정

| 설정 | 기본값 | 설명 | 튜닝 포인트 |
|------|--------|------|-------------|
| `fetch.min.bytes` | 1 | 최소 반환 바이트 | 높이면 처리량↑, 지연↑ |
| `fetch.max.wait.ms` | 500ms | 최대 대기 시간 | 낮추면 지연↓, 요청 수↑ |
| `fetch.max.bytes` | 50MB | 한 요청 최대 바이트 | 메모리 사용량 고려 |
| `max.partition.fetch.bytes` | 1MB | 파티션당 최대 바이트 | 메시지 크기 고려 |
| `max.poll.records` | 500 | poll()당 최대 레코드 수 | 처리 시간에 맞게 조정 |

### 1.4 가까운 레플리카에서 Fetch (KIP-392)

**면접 답변 예시:**

> "Kafka 2.4부터 Consumer는 반드시 리더에서만 읽지 않아도 됩니다. `client.rack` 설정을 통해 Consumer의 위치(데이터센터, AZ)를 지정하면, 같은 랙에 있는 Follower 레플리카에서 읽을 수 있습니다.
>
> 이는 멀티 AZ 환경에서 크로스 AZ 트래픽을 줄이고 네트워크 지연을 감소시킵니다. AWS 같은 클라우드에서는 AZ 간 데이터 전송 비용도 절감됩니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Rack Awareness (KIP-392)                                   │
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────┐         │
│  │   AZ-A (us-east-1a) │    │   AZ-B (us-east-1b) │         │
│  │                     │    │                     │         │
│  │  ┌───────────────┐  │    │  ┌───────────────┐  │         │
│  │  │   Consumer    │  │    │  │    Broker 2   │  │         │
│  │  │ client.rack=  │  │    │  │ broker.rack=  │  │         │
│  │  │   "az-a"      │  │    │  │   "az-b"      │  │         │
│  │  └───────┬───────┘  │    │  │   (Leader)    │  │         │
│  │          │          │    │  └───────────────┘  │         │
│  │          │          │    │                     │         │
│  │  ┌───────▼───────┐  │    │                     │         │
│  │  │    Broker 1   │  │    │                     │         │
│  │  │ broker.rack=  │  │    │                     │         │
│  │  │   "az-a"      │◀─┼────┼── 복제 ──           │         │
│  │  │  (Follower)   │  │    │                     │         │
│  │  └───────────────┘  │    │                     │         │
│  │                     │    │                     │         │
│  │  Consumer는 같은   │    │                     │         │
│  │  AZ의 Follower에서 │    │                     │         │
│  │  읽음 (지연↓, 비용↓)│    │                     │         │
│  └─────────────────────┘    └─────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 오프셋 관리

### 2.1 오프셋의 개념

**면접 답변 예시:**

> "오프셋은 파티션 내 메시지의 고유 식별자입니다. 0부터 시작하여 메시지가 추가될 때마다 1씩 증가합니다. 중요한 점은 메시지가 삭제되어도 다른 메시지의 오프셋은 변하지 않는다는 것입니다. 따라서 오프셋 사이에 갭이 생길 수 있습니다.
>
> Consumer는 '현재 처리 중인 오프셋'을 추적하여 장애 후 재시작해도 이어서 처리할 수 있습니다. 이를 '오프셋 커밋'이라고 합니다."

```
┌─────────────────────────────────────────────────────────────┐
│  오프셋 개념                                                 │
│                                                             │
│  파티션 로그:                                                │
│  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐        │
│  │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │ 8  │ 9  │        │
│  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘        │
│                           ↑         ↑         ↑              │
│                       Committed  Current    LEO              │
│                       Offset(5)  Position(7)                 │
│                                                             │
│  • Committed Offset: 마지막으로 커밋된 위치 (장애 시 재시작점)│
│  • Current Position: Consumer가 현재 읽고 있는 위치          │
│  • LEO: Log End Offset (다음 메시지가 쓰일 위치)             │
│                                                             │
│  메시지 삭제 후 (3, 4가 삭제됨):                             │
│  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐        │
│  │ 0  │ 1  │ 2  │ X  │ X  │ 5  │ 6  │ 7  │ 8  │ 9  │        │
│  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘        │
│                                                             │
│  • 오프셋 3, 4는 갭이 됨 (다른 오프셋은 변경 없음)           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 오프셋 저장 전략

**면접 질문: "오프셋을 저장하는 방법에는 어떤 것들이 있나요?"**

| 전략 | 저장 위치 | 장점 | 단점 | 사용 사례 |
|------|-----------|------|------|-----------|
| **저장 안 함** | 없음 | 단순 | 재시작 시 처음부터 | 인메모리 캐시 워밍 |
| **로컬 디스크** | 로컬 파일/DB | 빠른 복구 | 수평 확장 어려움 | Kafka Streams 상태 저장소 |
| **외부 시스템** | RDB, NoSQL | Exactly-Once 구현 가능 | 추가 인프라 | Kafka Connect Sink |
| **Kafka 자체** | `__consumer_offsets` | 내장, 편리 | Consumer Group 필수 | 일반적인 Consumer |

### 2.3 `__consumer_offsets` 토픽

**면접 답변 예시:**

> "`__consumer_offsets`은 Kafka가 Consumer Group의 오프셋을 저장하는 내부 토픽입니다. 기본적으로 50개 파티션, 복제 팩터 3으로 구성됩니다.
>
> 키는 `(group_id, topic, partition)` 조합이고, 값은 커밋된 오프셋과 메타데이터입니다. Log Compaction이 적용되어 각 키의 최신 값만 유지됩니다.
>
> Consumer Group의 오프셋은 `hash(group_id) % 50`으로 특정 파티션에 저장됩니다. 해당 파티션의 리더 브로커가 그 Consumer Group의 'Group Coordinator'가 됩니다."

```
┌─────────────────────────────────────────────────────────────┐
│  __consumer_offsets 구조                                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  키: (group_id, topic, partition)                       ││
│  │  값: {                                                  ││
│  │    offset: 12345,                                       ││
│  │    metadata: "client-1",                                ││
│  │    commitTimestamp: 1705000000000,                      ││
│  │    expireTimestamp: -1                                  ││
│  │  }                                                      ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  파티션 할당:                                                │
│  Consumer Group "analytics"                                 │
│    → hash("analytics") % 50 = 17                           │
│    → __consumer_offsets-17 파티션에 저장                    │
│    → 해당 파티션 리더 = Group Coordinator                   │
│                                                             │
│  Log Compaction:                                            │
│  ┌──────────────────────────────────────────────┐           │
│  │ (grp, topicA, 0): 100  ← 삭제됨              │           │
│  │ (grp, topicA, 0): 200  ← 삭제됨              │           │
│  │ (grp, topicA, 0): 300  ← 최신, 유지          │           │
│  └──────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 auto.offset.reset 설정

**면접 질문: "auto.offset.reset의 각 옵션에 대해 설명해주세요."**

| 설정값 | 동작 | 사용 사례 |
|--------|------|-----------|
| `latest` (기본) | 최신 메시지부터 소비 시작 | 실시간 스트리밍 처리 |
| `earliest` | 가장 오래된 메시지부터 소비 | 데이터 재처리, 새 Consumer 추가 |
| `none` | 유효한 오프셋 없으면 예외 발생 | 엄격한 오프셋 관리 필요 시 |

> "이 설정은 Consumer Group에 커밋된 오프셋이 없거나, 커밋된 오프셋이 이미 삭제된 경우에만 적용됩니다. 정상적으로 오프셋이 있으면 해당 위치에서 이어서 소비합니다."

---

## 3. Consumer Group

### 3.1 Consumer Group의 개념

**면접 답변 예시:**

> "Consumer Group은 같은 `group.id`를 가진 Consumer들의 집합입니다. 토픽의 파티션들은 그룹 내 Consumer들에게 분배되어, 각 파티션은 그룹 내 하나의 Consumer만 소비합니다.
>
> 이 구조의 장점은 두 가지입니다. 첫째, 파티션 수만큼 Consumer를 추가하여 수평 확장할 수 있습니다. 둘째, 서로 다른 Consumer Group은 독립적으로 동작하므로, 같은 메시지를 여러 서비스가 각자의 속도로 처리할 수 있습니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Consumer Group 개념                                         │
│                                                             │
│  Topic: orders (3 partitions)                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
│  │   P0    │  │   P1    │  │   P2    │                      │
│  └────┬────┘  └────┬────┘  └────┬────┘                      │
│       │            │            │                           │
│       │            │            │                           │
│  ─────┼────────────┼────────────┼─────────────────────────  │
│       │            │            │                           │
│       ▼            ▼            │                           │
│  ┌─────────────────────────────┐│ Consumer Group: analytics │
│  │ Consumer 1    Consumer 2   ││ (2 consumers)             │
│  │   (P0, P1)       (P2)      ││                           │
│  └─────────────────────────────┘│                           │
│                                 │                           │
│       │            │            ▼                           │
│       ▼            ▼            ▼                           │
│  ┌─────────────────────────────────────┐                    │
│  │         Consumer 3                  │ Consumer Group:    │
│  │         (P0, P1, P2)                │ monitoring         │
│  └─────────────────────────────────────┘ (1 consumer)       │
│                                                             │
│  • analytics 그룹: 2 Consumer가 3 파티션 분배               │
│  • monitoring 그룹: 1 Consumer가 3 파티션 모두 소비         │
│  • 두 그룹은 독립적으로 같은 메시지를 각각 소비              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Group Coordinator와 Group Leader

**면접 질문: "Group Coordinator와 Group Leader의 차이점은?"**

| 역할 | 위치 | 책임 |
|------|------|------|
| **Group Coordinator** | 브로커 | 그룹 멤버십 관리, Heartbeat 수신, 리밸런스 조정 |
| **Group Leader** | Consumer | 파티션 할당 계획 수립, Coordinator에게 할당 결과 제출 |

```
┌─────────────────────────────────────────────────────────────┐
│  Group Coordinator와 Group Leader                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Broker Cluster                        ││
│  │  ┌──────────────────────────────────────────────────┐   ││
│  │  │             Group Coordinator                     │   ││
│  │  │  (브로커 내 실행, __consumer_offsets 파티션 리더) │   ││
│  │  │                                                  │   ││
│  │  │  역할:                                            │   ││
│  │  │  • Consumer 멤버십 관리 (Join/Leave)             │   ││
│  │  │  • Heartbeat 모니터링                             │   ││
│  │  │  • 리밸런스 트리거 및 조정                        │   ││
│  │  │  • 오프셋 커밋 저장                               │   ││
│  │  └──────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                  │
│                          │ JoinGroup Response               │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Consumer Group                        ││
│  │                                                         ││
│  │  ┌────────────────────┐  ┌────────────────────┐         ││
│  │  │   Group Leader     │  │   Member (Follower)│         ││
│  │  │   (Consumer 1)     │  │   (Consumer 2)     │         ││
│  │  │                    │  │                    │         ││
│  │  │ 역할:              │  │ 역할:              │         ││
│  │  │ • 파티션 할당 계산 │  │ • 할당받은 파티션  │         ││
│  │  │   (Assignor 사용)  │  │   에서 소비        │         ││
│  │  │ • SyncGroup으로    │  │                    │         ││
│  │  │   할당 결과 제출   │  │                    │         ││
│  │  └────────────────────┘  └────────────────────┘         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ※ Group Leader는 첫 번째로 JoinGroup한 Consumer가 됨       │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Rebalance Protocol

**면접 답변 예시:**

> "리밸런스는 Consumer Group의 파티션 할당을 재조정하는 과정입니다. 새 Consumer 참여, 기존 Consumer 이탈, 토픽 파티션 수 변경 시 발생합니다.
>
> 과정은 다음과 같습니다:
> 1. 리밸런스가 트리거되면 모든 Consumer가 JoinGroup 요청을 Coordinator에게 보냅니다.
> 2. Coordinator는 첫 번째 Consumer를 Leader로 지정하고, 모든 멤버 정보를 Leader에게 전달합니다.
> 3. Leader가 Assignor를 사용해 파티션 할당을 계산하고, SyncGroup으로 결과를 제출합니다.
> 4. Coordinator가 각 Consumer에게 할당 결과를 전달합니다.
> 5. 모든 Consumer가 할당받은 파티션에서 소비를 시작합니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Rebalance Protocol 시퀀스                                   │
│                                                             │
│  Consumer1  Consumer2  Consumer3(New)  Coordinator          │
│     │          │            │              │                │
│     │          │            │──FindCoordinator──▶           │
│     │          │            │◀──Coordinator Info───         │
│     │          │            │                     │         │
│     │          │            │──JoinGroup──────────▶         │
│     │          │            │              │                │
│     │◀─────────┼────────────┼──Rebalance Signal──│          │
│     │          │◀───────────┼──Rebalance Signal──│          │
│     │          │            │              │                │
│     │──JoinGroup────────────┼──────────────▶                │
│     │          │──JoinGroup─┼──────────────▶                │
│     │          │            │              │                │
│     │          │            │     [Coordinator waits        │
│     │          │            │      for all members]         │
│     │          │            │              │                │
│     │◀─JoinGroupResponse (Leader)─────────│                 │
│     │  (멤버 목록 + 구독 정보)            │                 │
│     │          │◀─JoinGroupResponse (Follower)─             │
│     │          │            │◀─JoinGroupResponse (Follower) │
│     │          │            │              │                │
│     │ [Leader: 파티션 할당 계산]          │                 │
│     │          │            │              │                │
│     │──SyncGroup (할당 계획)──────────────▶                  │
│     │          │──SyncGroup (empty)───────▶                  │
│     │          │            │──SyncGroup (empty)──▶          │
│     │          │            │              │                │
│     │◀─SyncGroupResponse (P0, P1)─────────│                  │
│     │          │◀─SyncGroupResponse (P2)──│                  │
│     │          │            │◀─SyncGroupResponse (P3)─       │
│     │          │            │              │                │
│     │          │            │   [소비 시작] │                │
│     │          │            │              │                │
│  ───┼──Heartbeat────────────┼──────────────▶                │
│     │          │──Heartbeat─┼──────────────▶                │
│     │          │            │──Heartbeat───▶                │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. 파티션 할당 전략

### 4.1 Range Assignor (기본)

**면접 답변 예시:**

> "Range Assignor는 토픽별로 파티션을 Consumer에게 범위로 나누어 할당합니다. 같은 파티션 번호가 같은 Consumer에게 할당되므로, 여러 토픽 간 조인이 필요할 때 유용합니다. 같은 키를 가진 메시지는 같은 파티션 번호에 있을 가능성이 높기 때문입니다.
>
> 단점은 불균등 분배입니다. 파티션 2개, Consumer 2개면 균등하지만, 파티션 3개, Consumer 2개면 한 Consumer가 2개를 담당합니다. 여러 토픽을 구독하면 이 불균등이 누적됩니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Range Assignor                                             │
│                                                             │
│  Topic A (4 partitions): [P0, P1, P2, P3]                   │
│  Topic B (4 partitions): [P0, P1, P2, P3]                   │
│  Consumers: [C0, C1, C2]                                    │
│                                                             │
│  Topic A 할당: 4 / 3 = 1... 나머지 1                         │
│    C0: P0, P1  (1 + 나머지 1개)                             │
│    C1: P2                                                   │
│    C2: P3                                                   │
│                                                             │
│  Topic B 할당: 4 / 3 = 1... 나머지 1                         │
│    C0: P0, P1  (1 + 나머지 1개)                             │
│    C1: P2                                                   │
│    C2: P3                                                   │
│                                                             │
│  최종 결과:                                                  │
│    C0: A-P0, A-P1, B-P0, B-P1  (4개) ← 불균등!              │
│    C1: A-P2, B-P2              (2개)                        │
│    C2: A-P3, B-P3              (2개)                        │
│                                                             │
│  장점: 같은 파티션 번호 = 같은 Consumer (조인에 유리)        │
│  단점: 불균등 분배, 일부 Consumer 과부하                     │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Round Robin Assignor

**면접 답변 예시:**

> "Round Robin Assignor는 모든 파티션을 정렬한 후 Consumer에게 순차적으로 하나씩 분배합니다. Range보다 균등한 분배가 가능하지만, 같은 파티션 번호가 다른 Consumer에게 갈 수 있어 토픽 간 조인에는 적합하지 않습니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Round Robin Assignor                                       │
│                                                             │
│  모든 파티션 정렬: [A-P0, A-P1, A-P2, A-P3, B-P0, B-P1, B-P2, B-P3]
│  Consumers: [C0, C1, C2]                                    │
│                                                             │
│  순차 할당:                                                  │
│    A-P0 → C0                                                │
│    A-P1 → C1                                                │
│    A-P2 → C2                                                │
│    A-P3 → C0                                                │
│    B-P0 → C1                                                │
│    B-P1 → C2                                                │
│    B-P2 → C0                                                │
│    B-P3 → C1                                                │
│                                                             │
│  최종 결과:                                                  │
│    C0: A-P0, A-P3, B-P2        (3개)                        │
│    C1: A-P1, B-P0, B-P3        (3개)  ← 거의 균등!          │
│    C2: A-P2, B-P1              (2개)                        │
│                                                             │
│  장점: Range보다 균등한 분배                                 │
│  단점: 토픽 간 같은 파티션 번호 보장 안 됨                   │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Sticky Assignor

**면접 답변 예시:**

> "Sticky Assignor는 Round Robin처럼 균등 분배하면서, 리밸런스 시 기존 할당을 최대한 유지합니다. Consumer가 추가되거나 제거될 때 변경이 필요한 파티션만 이동시켜 리밸런스 오버헤드를 줄입니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Sticky Assignor - 리밸런스 시 변경 최소화                   │
│                                                             │
│  Before (2 Consumers):                                      │
│    C0: P0, P1, P2                                           │
│    C1: P3, P4, P5                                           │
│                                                             │
│  After C2 Join:                                             │
│                                                             │
│  Range/Round Robin:                                         │
│    C0: P0, P3      ← P1, P2 이동                            │
│    C1: P1, P4      ← P3, P5 이동, P1 받음                   │
│    C2: P2, P5      ← 새로 받음                              │
│    (4개 파티션 이동)                                         │
│                                                             │
│  Sticky:                                                    │
│    C0: P0, P1      ← P2만 이동                              │
│    C1: P3, P4      ← P5만 이동                              │
│    C2: P2, P5      ← 새로 받음                              │
│    (2개 파티션만 이동!)                                      │
│                                                             │
│  장점: 리밸런스 시 상태 재구축 비용 감소                     │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Cooperative Sticky Assignor (권장)

**면접 답변 예시:**

> "기존 Assignor들은 'Eager' 프로토콜을 사용합니다. 리밸런스가 시작되면 모든 Consumer가 모든 파티션을 포기하고, 새 할당을 받을 때까지 소비를 중단합니다. 이는 'Stop-the-World' 현상을 유발합니다.
>
> Cooperative Sticky Assignor는 'Cooperative' 프로토콜을 사용합니다. 리밸런스 시 이동이 필요한 파티션만 포기하고, 나머지 파티션은 계속 소비합니다. 리밸런스가 여러 라운드에 걸쳐 점진적으로 진행되어 다운타임이 크게 줄어듭니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Eager vs Cooperative Protocol                              │
│                                                             │
│  [Eager Protocol - 기존 방식]                               │
│                                                             │
│  Before:  C0(P0,P1,P2)    C1(P3,P4,P5)                      │
│                                                             │
│  Rebalance Start:                                           │
│    C0: 모든 파티션 포기 (P0,P1,P2)  ← 소비 중단             │
│    C1: 모든 파티션 포기 (P3,P4,P5)  ← 소비 중단             │
│    ⚠️ 전체 중단 (Stop-the-World)                            │
│                                                             │
│  After:   C0(P0,P1)   C1(P3,P4)   C2(P2,P5)                 │
│           소비 재개    소비 재개    소비 시작               │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  [Cooperative Protocol - 새 방식]                           │
│                                                             │
│  Before:  C0(P0,P1,P2)    C1(P3,P4,P5)                      │
│                                                             │
│  Rebalance Round 1:                                         │
│    C0: P2만 포기 (P0,P1 계속 소비) ✅                        │
│    C1: P5만 포기 (P3,P4 계속 소비) ✅                        │
│    ✅ 대부분 계속 소비                                       │
│                                                             │
│  Rebalance Round 2:                                         │
│    C2: P2,P5 할당받음                                       │
│                                                             │
│  After:   C0(P0,P1)   C1(P3,P4)   C2(P2,P5)                 │
│           (중단 없음)  (중단 없음)  (새로 시작)             │
└─────────────────────────────────────────────────────────────┘
```

### 4.5 할당 전략 비교 요약

| Assignor | 균등 분배 | 조인 지원 | 변경 최소화 | 무중단 리밸런스 |
|----------|-----------|-----------|-------------|-----------------|
| Range | ❌ | ✅ | ❌ | ❌ |
| Round Robin | ✅ | ❌ | ❌ | ❌ |
| Sticky | ✅ | ❌ | ✅ | ❌ |
| **Cooperative Sticky** | ✅ | ❌ | ✅ | ✅ |

```java
// 권장 설정
props.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG,
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

---

## 5. Static Membership

### 5.1 문제: 과도한 리밸런스

**면접 답변 예시:**

> "Kubernetes 환경에서 Rolling Restart를 하면 Pod이 하나씩 재시작됩니다. 기존 방식에서는 Consumer가 종료될 때마다 리밸런스가 발생하고, 재시작될 때도 리밸런스가 발생합니다. 3개 Consumer의 Rolling Restart면 6번의 리밸런스가 발생하여 처리량이 크게 저하됩니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Rolling Restart 시 리밸런스 문제                           │
│                                                             │
│  초기 상태: C1(P0,P1), C2(P2,P3), C3(P4,P5)                 │
│                                                             │
│  1. C1 종료      → Rebalance #1 (2 Consumers)              │
│     C2(P0,P1,P2), C3(P3,P4,P5)                              │
│                                                             │
│  2. C1 재시작    → Rebalance #2 (3 Consumers)              │
│     C1(P0,P1), C2(P2,P3), C3(P4,P5)                         │
│                                                             │
│  3. C2 종료      → Rebalance #3 (2 Consumers)              │
│     C1(P0,P1,P2), C3(P3,P4,P5)                              │
│                                                             │
│  4. C2 재시작    → Rebalance #4 (3 Consumers)              │
│     C1(P0,P1), C2(P2,P3), C3(P4,P5)                         │
│                                                             │
│  5. C3 종료      → Rebalance #5 (2 Consumers)              │
│     C1(P0,P1,P2), C2(P3,P4,P5)                              │
│                                                             │
│  6. C3 재시작    → Rebalance #6 (3 Consumers)              │
│     C1(P0,P1), C2(P2,P3), C3(P4,P5)                         │
│                                                             │
│  총 6번의 리밸런스! 각 리밸런스마다 소비 중단 발생           │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Static Membership 해결책

**면접 답변 예시:**

> "Static Membership은 `group.instance.id`를 설정하여 Consumer에게 고정 ID를 부여합니다. Consumer가 재시작해도 같은 ID로 다시 참여하면, Coordinator는 그 Consumer가 '돌아왔다'고 인식합니다.
>
> `session.timeout.ms` 내에 같은 ID로 재참여하면 리밸런스 없이 기존 파티션 할당을 유지합니다. Rolling Restart 시간이 session timeout보다 짧으면 리밸런스가 전혀 발생하지 않습니다."

```
┌─────────────────────────────────────────────────────────────┐
│  Static Membership                                          │
│                                                             │
│  설정:                                                       │
│  group.instance.id = "consumer-1"  (고정 ID)                │
│  session.timeout.ms = 300000       (5분)                    │
│                                                             │
│  Rolling Restart 시나리오:                                   │
│                                                             │
│  1. C1 (instance.id="c1") 종료                              │
│     → Coordinator: "c1이 빠졌지만 session.timeout까지 기다림"│
│     → 리밸런스 없음!                                         │
│                                                             │
│  2. C1 재시작 (같은 instance.id="c1")                       │
│     → Coordinator: "c1이 돌아왔음, 기존 할당 유지"          │
│     → 리밸런스 없음!                                         │
│                                                             │
│  3. C2, C3도 동일하게 처리                                   │
│     → 총 0번의 리밸런스!                                     │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  주의: session.timeout.ms 내에 재시작해야 함             ││
│  │  Pod 재시작이 5분보다 오래 걸리면 리밸런스 발생          ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Static Membership 설정

```java
// Static Membership 설정
props.put(ConsumerConfig.GROUP_INSTANCE_ID_CONFIG, "consumer-1");
props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, 300000);  // 5분
```

**Kubernetes에서 활용:**

```yaml
# StatefulSet 사용 시
env:
  - name: GROUP_INSTANCE_ID
    valueFrom:
      fieldRef:
        fieldPath: metadata.name  # Pod 이름 = consumer-0, consumer-1, ...
```

---

## 6. 면접 핵심 질문과 답변

### Q1: "Consumer Group에서 리밸런스는 언제 발생하나요?"

**모범 답변:**

> "리밸런스는 다음 상황에서 발생합니다:
>
> 1. **새 Consumer 참여**: 그룹에 새 멤버가 JoinGroup 요청
> 2. **Consumer 이탈**: session.timeout 초과 또는 명시적 LeaveGroup
> 3. **Consumer 장애**: Heartbeat 중단 감지
> 4. **토픽 파티션 수 변경**: 구독 중인 토픽의 파티션 추가/삭제
> 5. **구독 변경**: Consumer가 구독 토픽 목록 변경
>
> Static Membership을 사용하면 짧은 재시작에 대한 리밸런스를 방지할 수 있습니다."

### Q2: "Cooperative Sticky Assignor의 장점은?"

**모범 답변:**

> "Cooperative Sticky Assignor는 두 가지 핵심 장점이 있습니다.
>
> 첫째, 'Cooperative' 프로토콜로 리밸런스 중에도 변경되지 않는 파티션은 계속 소비합니다. Eager 프로토콜처럼 모든 Consumer가 멈추는 'Stop-the-World' 현상이 없습니다.
>
> 둘째, 'Sticky' 특성으로 기존 할당을 최대한 유지합니다. 파티션 이동을 최소화하여 상태 재구축 비용을 줄입니다.
>
> 프로덕션 환경에서는 Cooperative Sticky Assignor 사용을 권장합니다."

### Q3: "Consumer Lag는 무엇이고 왜 중요한가요?"

**모범 답변:**

> "Consumer Lag는 `LEO - Committed Offset`으로, 아직 처리되지 않은 메시지 수입니다.
>
> Lag가 증가하면 Consumer가 Producer 속도를 따라잡지 못한다는 신호입니다. 이는 처리 지연으로 이어지고, 오래된 메시지가 retention으로 삭제되면 데이터 유실이 발생할 수 있습니다.
>
> Lag 모니터링은 Consumer 헬스 체크의 핵심입니다. Lag가 증가하면 Consumer 수 확장, 처리 로직 최적화, 파티션 수 증가 등의 조치가 필요합니다."

```bash
# Lag 확인 명령어
kafka-consumer-groups.sh --describe --group my-group --bootstrap-server localhost:9092
```

### Q4: "auto.offset.reset의 earliest와 latest 차이는?"

**모범 답변:**

> "이 설정은 Consumer Group에 유효한 오프셋이 없을 때 적용됩니다.
>
> `earliest`는 파티션의 처음부터 소비합니다. 새 Consumer Group이 기존 데이터를 모두 처리해야 할 때 사용합니다. 예를 들어 데이터 재처리나 새 분석 시스템 도입 시 적합합니다.
>
> `latest`는 이후에 들어오는 새 메시지만 소비합니다. 실시간 스트리밍 처리에서 과거 데이터가 불필요할 때 사용합니다.
>
> 주의할 점은, 이미 오프셋이 커밋된 Consumer Group은 이 설정과 무관하게 커밋된 위치에서 이어서 소비합니다."

---

## 7. 실무 적용 체크리스트

### 7.1 Consumer 설정 권장사항

| 설정 | 권장값 | 이유 |
|------|--------|------|
| `partition.assignment.strategy` | CooperativeStickyAssignor | 무중단 리밸런스 |
| `enable.auto.commit` | false | 명시적 오프셋 관리 |
| `max.poll.records` | 처리량에 맞게 조정 | 메모리와 처리 시간 균형 |
| `session.timeout.ms` | 45000 | 장애 감지와 안정성 균형 |
| `heartbeat.interval.ms` | 3000 | session.timeout의 1/3 이하 |
| `max.poll.interval.ms` | 처리 시간에 맞게 | 긴 처리 시 증가 필요 |

### 7.2 Static Membership 적용 조건

- [ ] Kubernetes/Cloud 환경에서 Rolling Restart가 빈번함
- [ ] 리밸런스로 인한 처리량 저하가 문제됨
- [ ] Pod/Instance 재시작이 session.timeout 내에 완료됨
- [ ] Consumer 수가 고정적이거나 변경이 드묾

### 7.3 모니터링 지표

| 지표 | 임계값 | 조치 |
|------|--------|------|
| `records-lag-max` | 증가 추세 | Consumer 확장, 처리 최적화 |
| `records-consumed-rate` | 감소 | 병목 확인, 파티션 증가 |
| `rebalance-latency-avg` | 수 초 이상 | Static Membership 적용 |
| `commit-latency-avg` | 증가 | Coordinator 상태 확인 |

---

## 8. 참고 자료

- [Apache Kafka Documentation - Consumer Configs](https://kafka.apache.org/documentation/#consumerconfigs)
- [KIP-392: Fetch from the closest replica](https://cwiki.apache.org/confluence/display/KAFKA/KIP-392)
- [KIP-345: Static Membership](https://cwiki.apache.org/confluence/display/KAFKA/KIP-345)
- [KIP-848: The Next Generation Consumer Rebalance Protocol](https://cwiki.apache.org/confluence/display/KAFKA/KIP-848)
- [Confluent - Consumer Group Protocol](https://docs.confluent.io/platform/current/clients/consumer.html)
