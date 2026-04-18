# RabbitMQ Khepri - 면접 정리

## 핵심 한 줄 정리

> **Khepri는 RabbitMQ 4.0에서 도입된 Raft 기반 메타데이터 저장소로, 기존 Mnesia의 Split-brain 문제를 해결하고 클러스터의 일관성과 복구 안정성을 크게 향상시킵니다.**

---

## 면접 필수 암기

### Q1. Khepri란 무엇인가요?

**답변 (30초):**
> Khepri는 RabbitMQ 4.0(2024년)에 정식 지원된 새로운 메타데이터 저장소입니다. 기존 Mnesia를 대체하며, Quorum Queue와 동일한 **Raft 합의 알고리즘**을 사용합니다. 이를 통해 네트워크 파티션 시 Split-brain 없이 **예측 가능한 동작**을 보장하고, 장애 시 **자동 복구**가 가능합니다. 4.2 버전부터는 기본 저장소가 됩니다.

---

### Q2. 메타데이터 저장소가 저장하는 것은?

**답변:**
> 클러스터 운영에 필요한 **모든 정의 정보**를 저장합니다:
> - Virtual Host 정의
> - Exchange, Queue, Binding 정의
> - 사용자 및 권한
> - 정책(Policies)
> - 런타임 파라미터
> - 클러스터 멤버십 정보
>
> **메시지 데이터는 저장하지 않습니다.** 메시지는 각 큐 타입(Classic, Quorum, Stream)이 별도로 관리합니다.

---

### Q3. Mnesia vs Khepri 차이점은?

**답변:**

| 항목 | Mnesia (기존) | Khepri (신규) |
|------|--------------|---------------|
| **기반** | Erlang 분산 DB | Raft 합의 |
| **일관성** | 최종 일관성 | **강한 일관성** |
| **Split-brain** | 취약 | **방지됨** |
| **파티션 복구** | 수동 개입 필요 | **자동 복구** |
| **동작 예측성** | 낮음 | **높음** |

> 핵심 차이: Mnesia는 "모든 노드가 대등"하여 충돌 가능, Khepri는 "Leader가 결정"하여 충돌 없음.

---

### Q4. Khepri의 Quorum 요구사항은?

**답변:**
> Raft 기반이므로 **과반수 노드가 동작해야** 메타데이터 변경이 가능합니다.
>
> **클러스터 시작 예시 (5노드):**
> 1. 노드 1 시작 → 대기 (Quorum 미달)
> 2. 노드 2 시작 → 대기 (Quorum 미달)
> 3. 노드 3 시작 → **Quorum 달성** → 서비스 시작!
>
> 이것이 의미하는 것: 5노드 클러스터에서 3노드 이상 장애 시 **새 큐 생성, 설정 변경이 불가**합니다. (기존 메시지 처리는 가능)

---

### Q5. 마이그레이션 시 주의사항은?

**답변:**
> 1. **일방향**: Khepri → Mnesia 롤백 **불가**
> 2. **버전 요구**: 모든 노드가 4.0+ 이어야 함
> 3. **3.13 Khepri 미지원**: 3.13에서 Khepri 사용 시 4.0 업그레이드 불가
> 4. **피크 시간 회피**: 마이그레이션 마지막에 짧은 일시 중지 발생
> 5. **사전 백업**: `rabbitmqctl export_definitions` 필수

---

## 깊은 이해를 위한 설명

### 왜 Khepri가 필요했나?

**Mnesia의 근본적 문제: Split-brain**

```
정상 상태:
Node1 ←→ Node2 ←→ Node3
(모든 노드가 동일한 메타데이터)

네트워크 파티션 발생:
[Node1, Node2] ←✗→ [Node3]

Mnesia의 문제:
- 양쪽 파티션이 독립적으로 메타데이터 변경
- 복구 시 어떤 것이 "진짜"인지 모름
- 수동 개입 필요 (rabbitmqctl forget_cluster_node 등)
```

**Khepri의 해결:**
```
네트워크 파티션 발생:
[Node1, Node2] ←✗→ [Node3]

Khepri (Raft):
- Quorum(2/3)이 있는 [Node1, Node2]만 쓰기 가능
- [Node3]은 읽기 전용
- 복구 시 자동으로 [Node3]이 동기화
- Split-brain 발생 자체가 불가능
```

### RabbitMQ 4.0+의 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                   RabbitMQ 4.0+ Cluster                      │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    Khepri (Raft)                       │ │
│  │            메타데이터: Exchange, Queue 정의 등          │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │Quorum Queue │  │   Stream    │  │Classic Queue│        │
│  │   (Raft)    │  │   (Raft)    │  │  (단일노드)  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  Raft가 메타데이터와 데이터 복제 모두 담당                   │
└─────────────────────────────────────────────────────────────┘
```

> Quorum Queue, Streams, Khepri 모두 **Raft 기반**입니다. 동일한 합의 알고리즘으로 일관된 동작을 보장합니다.

### 버전별 상태

| 버전 | Khepri 상태 | Mnesia 상태 |
|------|------------|-------------|
| 3.13 | 실험적 (미지원) | 기본값 |
| **4.0** | **정식 지원** | 기본값 |
| **4.2** | **기본값** | 지원 (옵션) |
| 향후 | 유일 | **제거 예정** |

---

## 코드 레벨 이해

### Khepri 활성화

**신규 클러스터:**
```ini
# rabbitmq.conf
metadata_store = khepri
```

**기존 클러스터 마이그레이션:**
```bash
# 1. 정의 백업
rabbitmqctl export_definitions /backup/definitions.json

# 2. Feature flag 활성화
rabbitmqctl enable_feature_flag khepri_db

# 3. 마이그레이션 진행 확인
rabbitmq-diagnostics metadata_store_status

# 4. 검증
rabbitmqctl list_queues
rabbitmqctl list_exchanges
```

### 상태 확인

```bash
# 메타데이터 저장소 상태
rabbitmq-diagnostics metadata_store_status

# 예상 출력:
# Metadata store: khepri
# Raft state: leader
# Members: [rabbit@node1, rabbit@node2, rabbit@node3]
```

---

## 면접 예상 꼬리 질문

### Q. Khepri와 Quorum Queue 둘 다 Raft인데, 관계는?

**답변:**
> **별개의 Raft 그룹**입니다.
> - **Khepri**: 메타데이터(Exchange, Queue 정의 등)를 위한 Raft 그룹
> - **Quorum Queue**: 각 큐의 메시지를 위한 Raft 그룹
>
> 같은 알고리즘을 사용하지만 **독립적으로 동작**합니다. Quorum Queue가 장애나도 Khepri는 정상 동작하고, 반대도 마찬가지입니다.

### Q. Khepri 도입으로 운영이 어떻게 바뀌나요?

**답변:**
> **개선점:**
> - 네트워크 파티션 시 수동 개입 불필요
> - 노드 장애 복구가 자동화
> - 동작이 예측 가능해져 트러블슈팅 용이
>
> **주의점:**
> - 과반수 노드 필요 (홀수 노드 권장)
> - 2노드 클러스터는 1대 장애에도 쓰기 불가
> - 마이그레이션 후 롤백 불가

### Q. 왜 4.0에서 바로 기본값으로 안 했나요?

**답변:**
> **점진적 전환 전략**입니다.
> - 4.0: 정식 지원 시작, 프로덕션 검증 기간
> - 4.2: 충분한 검증 후 기본값으로 전환
>
> 기존 Mnesia 사용자들이 **충분히 테스트하고 마이그레이션 준비**할 시간을 주기 위함입니다.

### Q. Kafka의 KRaft와 비교하면?

**답변:**
> 둘 다 **ZooKeeper/Mnesia 같은 외부 의존성을 제거**하고 **내장 Raft로 전환**한 것입니다.
>
> | | Kafka KRaft | RabbitMQ Khepri |
> |--|------------|-----------------|
> | **ZK 제거** | Kafka 4.0 (2025.03) | RabbitMQ 4.0 (2024) |
> | **대상** | 메타데이터 | 메타데이터 |
> | **기존 방식** | ZooKeeper | Mnesia |
>
> 두 프로젝트 모두 **2024-2025년에 Raft 기반으로 전환**을 완료했다는 점에서 업계 트렌드를 보여줍니다.
