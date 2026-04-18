# 19. Geo-Replication과 멀티 클러스터

단일 데이터센터의 경계를 넘어 여러 지역에 걸쳐 Redpanda 클러스터를 운영하는 방법, 그리고 그 복잡성을 어떻게 관리하는지 다룹니다.

---

## 학습 목표

- 멀티 클러스터가 필요한 3가지 이유(DR, 지연 최소화, 데이터 주권) 이해
- MirrorMaker 2 vs Cluster Linking vs Redpanda Remote Read Replicas 비교
- Active-Passive와 Active-Active 토폴로지의 트레이드오프 파악
- RPO/RTO 개념과 비동기 복제의 한계 이해

---

## 1. 왜 멀티 클러스터인가

### 단일 클러스터의 한계

단일 Redpanda 클러스터는 운영이 단순하고 비용이 낮다는 장점이 있습니다. 그러나 서비스가 성장하고 글로벌 사용자를 대상으로 하게 되면, 단일 클러스터는 세 가지 근본적인 문제에 부딪힙니다.

**첫째, 단일 장애점(Single Point of Failure)입니다.** 클러스터가 위치한 데이터센터 자체가 재해(화재, 자연재해, 전력 차단)를 입으면 모든 서비스가 중단됩니다. 브로커를 여러 Availability Zone에 분산해도, 같은 지역(Region) 내의 재난에는 무력합니다.

**둘째, 지리적 지연(Geographic Latency)입니다.** 서울에 위치한 클러스터에서 뉴욕의 사용자가 메시지를 소비할 경우, 물리적 거리에 의한 RTT(왕복 지연)가 150~200ms 이상 발생합니다. 이는 실시간 알림, 금융 거래, 게임과 같이 지연에 민감한 서비스에서 치명적입니다.

**셋째, 데이터 주권(Data Sovereignty)과 규제 제약입니다.** GDPR(유럽), PIPL(중국), PIPA(한국) 등의 데이터 보호법은 특정 개인정보가 해당 국가 또는 지역의 경계를 벗어나지 못하도록 규정합니다. 단일 클러스터로 글로벌 서비스를 운영하면 이 규정을 만족하기 어렵습니다.

### 멀티 클러스터의 필요성 정리

| 동기 | 핵심 문제 | 해결책 |
|------|-----------|--------|
| **재해 복구(DR)** | 데이터센터 장애 시 서비스 중단 | 다른 지역에 복제 클러스터 운영 |
| **지연 최소화** | 먼 거리로 인한 높은 RTT | 사용자와 가까운 곳에 클러스터 배치 |
| **데이터 주권** | 법적 규제로 데이터 이동 제한 | 지역별 클러스터에 데이터 격리 |

### 멀티 클러스터 = 복잡성 증가

멀티 클러스터는 위 문제를 해결하지만, 새로운 복잡성을 만듭니다. 클러스터 간 데이터 일관성 유지, 복제 지연 모니터링, 장애 시 Failover 절차, 운영 비용 증가가 대표적입니다. 따라서 멀티 클러스터 도입은 "필요한가?"를 먼저 검토하고, 단일 클러스터로 해결할 수 없는 요구사항이 명확할 때만 선택해야 합니다.

---

## 2. 복제 방식 비교

클러스터 간 데이터를 복제하는 방법은 크게 세 가지입니다. 각각 설계 철학과 트레이드오프가 다르므로, 요구사항에 맞는 방식을 선택해야 합니다.

### 2.1 MirrorMaker 2 (Kafka 공식)

MirrorMaker 2(MM2)는 Apache Kafka 공식 복제 도구입니다. Kafka Connect 프레임워크 위에 구현되어 있으며, Redpanda는 Kafka API 호환성을 제공하므로 MM2를 그대로 사용할 수 있습니다.

**동작 원리**: MM2는 소스 클러스터의 Consumer 역할을 하며 메시지를 읽어 대상 클러스터의 Producer로 씁니다. 단순하지만 이 과정에서 네트워크를 두 번 거치기 때문에 지연이 발생합니다.

**주요 기능**:
- 토픽 복제: `source.topics` 정규식으로 복제할 토픽 지정
- Consumer Group 오프셋 복제: Failover 시 소비 위치를 이어받을 수 있음
- ACL 복제: 접근 제어 정책 동기화
- 양방향 복제(Active-Active) 지원

**구성 예시** (mm2.properties):

```properties
# 클러스터 별칭 정의
clusters = seoul, tokyo
seoul.bootstrap.servers = seoul-broker:9092
tokyo.bootstrap.servers = tokyo-broker:9092

# 서울 → 도쿄 복제 활성화
seoul->tokyo.enabled = true
seoul->tokyo.topics = orders, payments, user-events

# 복제 인수
replication.factor = 3
tasks.max = 4

# 오프셋 동기화 활성화
seoul->tokyo.sync.group.offsets.enabled = true
sync.group.offsets.interval.seconds = 60
```

**한계**:
- **높은 지연**: Consumer → 네트워크 → Producer 경로로 수십~수백 ms 추가 지연 발생
- **설정 복잡도**: Connect 클러스터, MM2 커넥터, 모니터링을 별도로 구성해야 함
- **별도 인프라 필요**: Kafka Connect 클러스터를 추가로 운영해야 함
- **오프셋 불일치**: 소스와 대상의 오프셋이 달라 Failover 시 수동 계산 필요

### 2.2 Confluent Cluster Linking

Confluent Cluster Linking은 Confluent Platform과 Confluent Cloud 전용 기능입니다. Connect 없이 브로커 내부에서 직접 복제가 이루어지므로 훨씬 낮은 지연을 달성합니다.

**동작 원리**: 소스 브로커가 대상 브로커에 직접 데이터를 전송합니다. 복제된 토픽은 **Mirror Topic**으로 생성되며 읽기 전용입니다.

**핵심 특징**:
- **오프셋 보존**: 소스와 대상의 오프셋이 동일 → Failover 시 오프셋 변환 불필요
- **낮은 지연**: 브로커 내장 복제로 수 초 이내 동기화 가능
- **단방향**: Mirror Topic은 읽기 전용으로 쓰기 불가 (Active-Active는 별도 설정 필요)

**제약**: Confluent Platform 또는 Cloud 전용입니다. 순수 Redpanda 또는 오픈소스 Kafka 환경에서는 사용할 수 없습니다.

### 2.3 Redpanda Remote Read Replicas

Redpanda의 고유한 복제 방식으로, **Tiered Storage를 매개로 데이터를 공유**합니다. 별도의 복제 프로세스 없이, 오브젝트 스토리지(S3, GCS, Azure Blob)를 공유 저장소로 활용하여 읽기 전용 클러스터가 데이터에 접근합니다.

**동작 원리**:

```
Source Cluster ──→ S3/GCS ──→ Read Replica Cluster
   (쓰기)        (공유 저장소)      (읽기 전용)
```

소스 클러스터는 Tiered Storage를 통해 오브젝트 스토리지에 세그먼트를 업로드합니다. Read Replica 클러스터는 같은 오브젝트 스토리지를 마운트하여 Consumer 요청에 응답합니다. 데이터를 추가로 전송하거나 복사하지 않으므로 **네트워크 대역폭을 절약**합니다.

**설정 예시**:

```bash
# 소스 클러스터: Tiered Storage 활성화
rpk cluster config set cloud_storage_enabled true
rpk cluster config set cloud_storage_bucket my-redpanda-bucket
rpk cluster config set cloud_storage_region ap-northeast-2

# Read Replica 클러스터: 동일한 버킷을 Read Replica로 연결
rpk topic create orders \
  --topic-config redpanda.remote.readreplica=my-redpanda-bucket
```

**장점**:
- 추가 복제 없이 읽기 확장 가능
- 네트워크 비용 절감
- 분석/보고 워크로드를 소스 클러스터에 부담 없이 분리

**한계**:
- **읽기 전용**: Read Replica에서는 쓰기 불가
- **실시간성 낮음**: Tiered Storage 업로드 주기(기본 수 분)만큼 지연 발생
- **Consumer Group 상태 미복제**: Failover 시 오프셋을 별도로 관리해야 함

### 2.4 세 방식 비교표

| 항목 | MirrorMaker 2 | Cluster Linking | Remote Read Replicas |
|------|--------------|-----------------|----------------------|
| **복제 지연** | 수십~수백 ms | 수 초 이내 | 수 분 (업로드 주기) |
| **방향성** | 단방향/양방향 | 단방향 | 단방향 (읽기 전용) |
| **오프셋 보존** | 미보존 (변환 필요) | 보존 | 보존 |
| **인프라 요구** | Connect 클러스터 별도 | 없음 (브로커 내장) | 오브젝트 스토리지 |
| **쓰기 가능** | 가능 | 미러만 읽기 전용 | 읽기 전용 |
| **플랫폼** | 범용 (Kafka/Redpanda) | Confluent 전용 | Redpanda 전용 |
| **비용** | Connect 운영 비용 | Confluent 라이선스 | 스토리지 비용만 |

---

## 3. Active-Passive vs Active-Active

두 가지 멀티 클러스터 토폴로지의 트레이드오프를 이해해야 운영 방식을 올바르게 선택할 수 있습니다.

### 3.1 Active-Passive (단방향 복제)

하나의 클러스터(Active)가 모든 쓰기 트래픽을 처리하고, 다른 클러스터(Passive)는 복제본을 유지하며 대기합니다. Passive 클러스터는 읽기 트래픽을 일부 처리하거나, 장애 시 Active로 승격(Failover)됩니다.

```
[정상 운영]

  Producer
     |
     v
+----------+     단방향 복제     +----------+
| Active   | ─────────────────> | Passive  |
| Seoul    |                    | Tokyo    |
+----------+                    +----------+
     ^                               |
     |                         (읽기 전용 또는 대기)
  Consumer
```

**장점**:
- 설계와 운영이 단순함
- 데이터 충돌(Conflict) 없음 — 쓰기가 한 곳에서만 발생
- 일관성 보장 용이

**단점**:
- Passive 클러스터의 컴퓨팅 자원이 낭비됨 (대기 상태)
- Failover 시 다운타임 발생 (수 분 이내가 일반적)
- Active 클러스터에 트래픽이 집중됨

**사용 시나리오**: 재해 복구가 주목적이고, 양쪽 클러스터 모두 쓰기가 필요하지 않은 경우. DR SLA(예: RPO < 5분, RTO < 15분)를 만족하면 충분한 대부분의 서비스.

### 3.2 Active-Active (양방향 복제)

두 클러스터 모두 읽기와 쓰기를 처리합니다. 각 지역의 사용자는 가장 가까운 클러스터를 사용하고, 클러스터 간 데이터는 양방향으로 복제됩니다.

```
[Active-Active 운영]

  Producer(서울)          Producer(도쿄)
       |                       |
       v                       v
+----------+   양방향 복제   +----------+
| Active   | <────────────> | Active   |
| Seoul    |                | Tokyo    |
+----------+                +----------+
       ^                       ^
       |                       |
  Consumer(서울)          Consumer(도쿄)
```

**충돌 해결(Conflict Resolution) 필요**: 같은 키를 가진 메시지가 두 클러스터에서 동시에 쓰여지면, 어느 것이 "정답"인지 결정해야 합니다. 일반적인 전략:

- **Last-Write-Wins (LWW)**: 타임스탬프가 더 늦은 메시지가 승리. 간단하지만 NTP 동기화 오차로 인해 위험.
- **CRDT (Conflict-free Replicated Data Types)**: 수학적으로 충돌 없이 병합 가능한 데이터 구조. 구현 복잡.
- **애플리케이션 레벨 충돌 처리**: Consumer가 중복 메시지를 감지하고 처리. 가장 유연하지만 개발 부담.

**순환 복제 방지**: 서울이 도쿄로 복제하고, 도쿄가 다시 서울로 복제하면 같은 메시지가 무한히 순환합니다. 이를 방지하기 위해 메시지 헤더에 소스 클러스터 정보를 포함합니다.

MirrorMaker 2는 복제된 토픽에 소스 클러스터 접두사를 붙여 순환을 방지합니다:

```
서울 클러스터: orders          (원본)
도쿄 클러스터: seoul.orders    (서울에서 복제된 것)
서울 클러스터: tokyo.orders    (도쿄에서 복제된 것)
```

이 접두사 전략 덕분에 각 클러스터는 상대방에서 복제된 토픽을 원본으로 다시 복제하지 않습니다.

**장점**:
- 두 클러스터 모두 트래픽을 처리 → 자원 효율적
- 한 클러스터 장애 시 다른 클러스터가 즉시 처리 (RTO 거의 0)
- 지역별 사용자에게 낮은 지연 제공

**단점**:
- 충돌 해결 로직 필요 → 개발 복잡도 증가
- 순환 복제 방지 메커니즘 필요
- 일관성 보장 어려움 (최종 일관성만 가능)
- 운영 복잡도가 Active-Passive보다 훨씬 높음

**사용 시나리오**: 글로벌 서비스에서 각 지역 사용자에게 낮은 지연이 필수적이고, 일부 데이터 충돌을 수용할 수 있는 경우. 예: 소셜 미디어, 게임, 실시간 채팅.

---

## 4. 비동기 복제와 RPO/RTO

### RPO와 RTO의 정의

재해 복구 계획의 핵심 지표입니다. 이 두 숫자를 명확히 정의하지 않으면 어떤 복제 방식이 "충분한가"를 판단할 수 없습니다.

- **RPO (Recovery Point Objective)**: 장애 발생 시 허용 가능한 데이터 손실 시간. 예를 들어 RPO = 5분이면, 장애 시 최대 5분치 데이터는 손실되어도 비즈니스적으로 허용 가능하다는 의미입니다.

- **RTO (Recovery Time Objective)**: 장애 발생 후 서비스가 다시 정상화되기까지 허용 가능한 시간. RTO = 30분이면, 30분 이내에 서비스가 재개되어야 한다는 의미입니다.

### 비동기 복제의 본질: RPO > 0

현재 실무에서 사용하는 대부분의 Geo-Replication은 **비동기 복제**입니다. 소스 클러스터가 메시지를 커밋한 후, 복제는 별도의 시간에 이루어집니다. 이 복제 지연(Replication Lag)이 RPO를 결정합니다.

```
소스 클러스터 타임라인:
  T=0  메시지 A 커밋
  T=1  메시지 B 커밋
  T=2  메시지 C 커밋  ← 장애 발생
  T=3  [클러스터 다운]

대상 클러스터 타임라인:
  T=0  메시지 A 복제 완료
  T=1  메시지 B 복제 완료
  T=2  메시지 C 복제 미완료  ← 이 메시지 손실

RPO = T=2의 메시지 C (약 0~복제지연 시간만큼의 데이터 손실)
```

비동기 복제를 사용하는 한, RPO = 0은 달성할 수 없습니다. 장애가 복제가 완료되기 전에 발생하면 반드시 일부 데이터가 손실됩니다.

### 동기 복제의 가능성과 비용

RPO = 0을 달성하려면 **동기 복제**가 필요합니다. 메시지가 소스와 대상 클러스터 모두에 커밋된 후에야 Producer에게 ACK를 보내는 방식입니다. 그러나 이는 쓰기 지연이 WAN(광역 네트워크) RTT만큼 증가한다는 의미입니다. 서울-도쿄 간 RTT가 약 30ms라면, 모든 쓰기에 30ms의 추가 지연이 붙습니다. 대부분의 고처리량 스트리밍 서비스에서는 수용하기 어려운 비용입니다.

### RPO/RTO vs 비용/복잡도 트레이드오프

| 목표 | 방식 | 쓰기 지연 영향 | 비용 | 복잡도 |
|------|------|--------------|------|--------|
| RPO = 0 | 동기 복제 | WAN RTT 추가 (크게 증가) | 높음 | 높음 |
| RPO < 수 초 | 비동기 + 낮은 복제 지연 | 없음 | 중간 | 중간 |
| RPO < 수 분 | 비동기 (기본) | 없음 | 낮음 | 낮음 |
| RPO < 1시간 | Remote Read Replicas | 없음 | 매우 낮음 | 낮음 |

### 업계 기준

| 업종 | 일반적 RPO | 일반적 RTO | 비고 |
|------|-----------|-----------|------|
| **금융/결제** | 0 ~ 수 초 | < 1분 | 규제 요구사항 |
| **이커머스** | < 1분 | < 5분 | 주문 손실 = 매출 손실 |
| **미디어/게임** | < 5분 | < 15분 | 일부 손실 허용 |
| **일반 SaaS** | < 15분 | < 30분 | 표준 DR |
| **내부 분석** | < 1시간 | < 2시간 | 배치성, 느슨한 SLA |

이 기준을 먼저 비즈니스 팀과 합의한 후 복제 방식을 선택해야 합니다. 기술 선택이 비즈니스 목표를 주도하는 것이 아니라, 비즈니스 목표가 기술 선택을 결정해야 합니다.

---

## 5. 오프셋 동기화

### 왜 오프셋 동기화가 어려운가

Failover 시 가장 큰 문제 중 하나는 Consumer가 "어디서부터 다시 읽어야 하는가"를 알기 어렵다는 점입니다. 소스와 대상 클러스터에서 같은 메시지가 **다른 오프셋**을 가질 수 있기 때문입니다.

```
소스 클러스터 (서울):
  Offset 0: 메시지 A
  Offset 1: 메시지 B
  Offset 2: 메시지 C
  Offset 3: 메시지 D  ← Consumer가 여기까지 소비함

대상 클러스터 (도쿄):
  Offset 0: 메시지 A
  Offset 1: 메시지 B
  Offset 2: 메시지 C
  (메시지 D는 아직 복제 안 됨)

Failover 후 Consumer가 Offset 3을 커밋하려 하면?
→ 도쿄에는 Offset 3이 없음 → 오류 또는 재처리 시작점 불명확
```

오프셋이 항상 일치하지 않는 이유는 MM2 같은 방식이 내부적으로 레코드를 재생성하기 때문입니다. 소스의 `orders` 토픽 Offset 100이 대상의 `seoul.orders` 토픽 Offset 50일 수 있습니다.

### MirrorMaker 2의 오프셋 변환

MM2는 이 문제를 해결하기 위해 **오프셋 매핑 정보**를 별도의 내부 토픽에 저장합니다.

- `mm2-offsets.{source}.internal`: 소스 오프셋과 대상 오프셋의 매핑 테이블
- `mm2-status.{source}.internal`: 복제 커넥터의 상태 정보
- `mm2-configs.{source}.internal`: 커넥터 설정 정보

Consumer Group Failover 시 `RemoteClusterUtils` API를 사용하여 소스 오프셋을 대상 오프셋으로 변환합니다:

```java
// Failover 시 오프셋 변환 예시
Map<TopicPartition, Long> sourceOffsets = getLastCommittedOffsets("my-consumer-group");

Map<TopicPartition, OffsetAndMetadata> targetOffsets =
    RemoteClusterUtils.translateOffsets(
        adminClient,           // 대상 클러스터 Admin Client
        "seoul",               // 소스 클러스터 별칭
        "my-consumer-group",
        Duration.ofSeconds(30)
    );

consumer.assign(targetOffsets.keySet());
targetOffsets.forEach((tp, om) -> consumer.seek(tp, om.offset()));
```

### Checkpoint Connector

MM2에는 `MirrorCheckpointConnector`가 포함되어 있어, 소스 클러스터의 Consumer Group 오프셋을 주기적으로 대상 클러스터의 `{source}.checkpoints.internal` 토픽에 기록합니다. Failover 자동화 시스템이 이 토픽을 구독하여 Consumer Group을 자동으로 재배치할 수 있습니다.

### Redpanda Remote Read Replicas의 접근

Remote Read Replicas는 오브젝트 스토리지를 공유하므로 **오프셋이 그대로 보존**됩니다. 소스 클러스터의 Offset 100은 Read Replica에서도 Offset 100입니다. Failover 시 오프셋 변환이 필요 없어 훨씬 단순합니다. 단, Consumer Group 상태 자체는 복제되지 않으므로 Consumer 재시작 시 `__consumer_offsets` 토픽의 오프셋을 수동으로 설정해야 합니다.

---

## 6. Redpanda Remote Read Replicas 심화

### 아키텍처 전체 그림

```
[Source Cluster - Seoul]           [Object Storage - S3]
┌─────────────────────┐           ┌──────────────┐
│  Broker 1           │           │              │
│  Broker 2  ─────────┼──upload──>│  Segments    │
│  Broker 3           │           │  (S3 Bucket) │
└─────────────────────┘           └──────┬───────┘
  Producer 쓰기                          │
  Consumer 읽기 (실시간)                  │ read
                                         │
                               [Read Replica - Tokyo]
                               ┌─────────────────────┐
                               │  Replica Broker 1   │
                               │  Replica Broker 2   │
                               │  Replica Broker 3   │
                               └─────────────────────┘
                                 Consumer 읽기 (분석/보고)
```

Read Replica 클러스터는 소스 클러스터와 **동일한 S3 버킷을 읽기 전용으로 마운트**합니다. 추가 복제 프로세스나 네트워크 전송이 없습니다. S3 데이터는 이미 내구성이 높으므로, 소스 클러스터가 다운되어도 Read Replica는 S3에 업로드된 데이터까지는 계속 서비스할 수 있습니다.

### 소스 클러스터 설정: Tiered Storage 활성화

```bash
# 클러스터 설정으로 Tiered Storage 활성화
rpk cluster config set cloud_storage_enabled true
rpk cluster config set cloud_storage_bucket redpanda-tiered-storage
rpk cluster config set cloud_storage_region ap-northeast-2
rpk cluster config set cloud_storage_access_key AKIAIOSFODNN7EXAMPLE
rpk cluster config set cloud_storage_secret_key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# 특정 토픽에 Tiered Storage 활성화 (토픽 레벨)
rpk topic create orders \
  --topic-config redpanda.remote.write=true \
  --topic-config redpanda.remote.read=true \
  --topic-config retention.bytes=1073741824  # 로컬 1GB 보존

# 기존 토픽에 적용
rpk topic alter-config orders \
  --set redpanda.remote.write=true
```

### Read Replica 클러스터 설정

```bash
# Read Replica 클러스터에서 동일한 S3 버킷 연결
rpk cluster config set cloud_storage_enabled true
rpk cluster config set cloud_storage_bucket redpanda-tiered-storage  # 소스와 동일
rpk cluster config set cloud_storage_region ap-northeast-2

# Read Replica 토픽 생성 (소스 클러스터의 토픽과 같은 이름)
rpk topic create orders \
  --topic-config redpanda.remote.readreplica=redpanda-tiered-storage

# Read Replica 상태 확인
rpk topic describe orders
# remote.readreplica: redpanda-tiered-storage 가 보여야 함

# Consumer로 읽기 (일반 Kafka Consumer와 동일)
rpk topic consume orders --brokers tokyo-broker:9092
```

### 읽기 지연과 업로드 주기

Read Replica의 신선도(Freshness)는 Tiered Storage 업로드 주기에 달려 있습니다. 소스 클러스터가 세그먼트를 S3에 업로드하는 빈도를 조절할 수 있습니다:

```bash
# 업로드 주기 설정 (기본값: 세그먼트가 닫힐 때)
# 세그먼트 롤링 주기를 짧게 하면 더 자주 업로드됨
rpk topic alter-config orders \
  --set segment.ms=60000  # 1분마다 세그먼트 롤링 → 최대 1분 지연
```

실시간 처리가 필요한 워크로드에는 Read Replica가 적합하지 않습니다. **분석, 보고, 배치 처리, 감사(Audit)** 같이 수 분의 지연을 허용할 수 있는 워크로드에 이상적입니다.

### 비용 최적화 시나리오

```
[일반적인 문제]
소스 클러스터에 분석 Consumer가 과부하를 줌
→ 실시간 Producer/Consumer에 영향

[Remote Read Replicas 해결책]
소스 클러스터: 실시간 스트리밍 (저지연 중요)
Read Replica 클러스터: 분석/ML 학습 데이터 읽기 (지연 허용)

비용 절감:
- Read Replica는 소형 노드로 구성 가능 (쓰기 부하 없음)
- 소스 클러스터 용량 여유 확보
- S3 비용만 추가 (이미 Tiered Storage 사용 중이라면 거의 무료)
```

---

## 7. 재해 복구 시나리오

### Failover 절차

장애 발생 시 당황하지 않으려면 **Failover 절차를 사전에 문서화하고 훈련**해야 합니다. 일반적인 절차는 다음과 같습니다:

**1단계: 장애 감지**

```bash
# 소스 클러스터 헬스 체크
rpk cluster health --brokers seoul-broker:9092

# 복제 지연 모니터링 (정상: < 1000ms)
rpk topic describe orders --brokers tokyo-broker:9092
# replication_lag 확인

# Consumer Group 지연 확인
rpk group describe my-consumer-group --brokers seoul-broker:9092
```

**2단계: DNS/로드밸런서 전환**

```bash
# AWS Route53 예시: Active 클러스터 레코드 변경
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890 \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "kafka.myservice.com",
        "Type": "CNAME",
        "TTL": 60,
        "ResourceRecords": [{"Value": "tokyo-broker.internal"}]
      }
    }]
  }'
```

**3단계: Consumer Group 오프셋 조정 (MM2 사용 시)**

```bash
# MM2 체크포인트에서 오프셋 읽기
rpk topic consume seoul.checkpoints.internal \
  --brokers tokyo-broker:9092 \
  --offset start

# 수동으로 Consumer Group 오프셋 리셋
rpk group seek my-consumer-group \
  --brokers tokyo-broker:9092 \
  --to-offset orders:0:1234  # 마지막으로 확인된 안전한 오프셋
```

**4단계: 서비스 재개 확인**

```bash
# Failover 후 Consumer가 정상적으로 메시지를 소비하는지 확인
rpk group describe my-consumer-group --brokers tokyo-broker:9092
# LAG 값이 줄어들고 있으면 정상

# 메시지 샘플링으로 데이터 유효성 확인
rpk topic consume orders --brokers tokyo-broker:9092 --num 10
```

**자동 vs 수동 Failover 트레이드오프**:

| 항목 | 자동 Failover | 수동 Failover |
|------|-------------|-------------|
| **RTO** | < 2분 (빠름) | 5~30분 (사람 개입) |
| **리스크** | Split-Brain 가능성 | 낮음 (사람이 판단) |
| **적합 상황** | RTO 요구가 엄격한 경우 | 충분한 복구 시간이 있는 경우 |
| **구현 비용** | 높음 (자동화 필요) | 낮음 (Runbook만 필요) |

### Failback 절차

원래 클러스터(서울)가 복구된 후 다시 돌아오는 절차입니다. Failback을 서두르면 데이터 불일치가 발생할 수 있으므로 신중하게 진행해야 합니다.

**1단계: 원래 클러스터 복구 확인**

```bash
# 서울 클러스터 헬스 체크
rpk cluster health --brokers seoul-broker:9092

# 브로커가 모두 정상인지 확인
rpk brokers list --brokers seoul-broker:9092
```

**2단계: 역방향 복제 (도쿄 → 서울)**

Failover 기간 동안 도쿄에 쌓인 데이터를 서울로 다시 복제합니다. MM2를 역방향으로 설정합니다:

```properties
# mm2-failback.properties
clusters = tokyo, seoul
tokyo.bootstrap.servers = tokyo-broker:9092
seoul.bootstrap.servers = seoul-broker:9092

# 역방향 복제 (Failover 기간 동안 도쿄에 쓰인 데이터)
tokyo->seoul.enabled = true
tokyo->seoul.topics = orders, payments
tokyo->seoul.sync.group.offsets.enabled = true
```

**3단계: 데이터 동기화 확인**

```bash
# 두 클러스터의 최신 오프셋 비교
rpk topic describe orders --brokers seoul-broker:9092
rpk topic describe orders --brokers tokyo-broker:9092
# High watermark가 거의 동일해질 때까지 대기
```

**4단계: 트래픽 전환 및 Split-Brain 방지**

```bash
# Split-Brain 방지: 전환 전 도쿄 클러스터의 쓰기를 먼저 차단
# (Producer에게 Connection Refused 반환)
# 이후 서울 클러스터로 DNS 변경
# 두 클러스터가 동시에 쓰기를 받는 상태를 최대한 짧게 유지
```

**Split-Brain 방지 전략**:
- 전환 순서: 새 클러스터 활성화 → 구 클러스터 비활성화 (Overlap 최소화)
- Producer에 짧은 읽기 전용 기간 적용 (수 초)
- DNS TTL을 미리 낮춰 전환 속도 향상 (평소 300초 → 전환 전날 60초로 변경)

### DR 테스트 (Game Day)

**DR 계획은 테스트하지 않으면 존재하지 않는 것과 같습니다.** 실제 장애가 발생했을 때 처음 Failover를 시도하면 반드시 예상치 못한 문제가 발생합니다. 정기적인 DR 훈련이 필수적인 이유입니다.

**Game Day 시나리오 예시**:

```
시나리오 1: 소스 클러스터 단일 브로커 장애
  - 한 브로커를 강제 종료
  - RF=3이므로 서비스 지속 가능한지 확인
  - 복제 지연이 증가하는지 모니터링

시나리오 2: 소스 클러스터 전체 장애
  - 소스 클러스터 네트워크 차단
  - Failover 절차 실행
  - RTO 측정: 실제로 몇 분이 걸리는가?
  - 데이터 손실 확인: 실제 RPO는?

시나리오 3: 복제 지연 급증
  - 네트워크 대역폭 제한 시뮬레이션
  - Consumer가 대상 클러스터로 자동 전환하는지 확인
```

**DR 준비 상태 체크리스트**:

```
□ 복제 지연 모니터링 알람 설정 (임계값: > 60초)
□ Failover Runbook 문서화 및 최신화
□ Consumer Group 오프셋 변환 도구 준비
□ DNS TTL 값 확인 (60초 이하 권장)
□ 대상 클러스터의 용량이 전체 트래픽을 처리할 수 있는지 확인
□ 최근 3개월 내 DR 훈련 실시 여부
□ Failover 후 데이터 검증 스크립트 준비
□ Split-Brain 방지 절차 팀 공유
□ PagerDuty/OpsGenie 등 알람 대상 클러스터 설정
```

---

## 8. 모니터링과 운영 지표

### 핵심 모니터링 지표

멀티 클러스터 환경에서는 단일 클러스터보다 더 많은 지표를 추적해야 합니다. 복제 파이프라인 전체가 정상인지 지속적으로 관찰해야 하기 때문입니다.

**복제 지연 (Replication Lag)**

복제 지연은 소스 클러스터의 최신 오프셋과 대상 클러스터가 복제 완료한 오프셋의 차이입니다. 이 값이 곧 현재의 RPO 근사치가 됩니다. 복제 지연이 허용 RPO를 초과하면 즉시 알람이 울려야 합니다.

```bash
# rpk로 복제 지연 확인 (MM2 Consumer Group 기준)
rpk group describe mirrormaker2-consumer-group \
  --brokers tokyo-broker:9092

# 출력 예시:
# TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
# orders          0          9850            9870            20   ← 20개 메시지 지연
# orders          1          9900            9900            0
# payments        0          5100            5103            3

# 메시지 수 대신 시간으로 변환하려면:
# LAG(메시지) × 평균 메시지 간격(ms) = 복제 지연(ms)
```

**체크해야 할 Prometheus 메트릭**:

| 메트릭 | 설명 | 임계값 예시 |
|--------|------|------------|
| `redpanda_kafka_consumer_group_lag` | Consumer Group 오프셋 지연 | > 10,000 메시지 |
| `redpanda_storage_log_segments_active` | 활성 세그먼트 수 | 이상 급증 시 |
| `redpanda_cloud_storage_upload_lag_ms` | Tiered Storage 업로드 지연 | > 60,000 ms |
| `redpanda_rpc_latency_seconds_p99` | 내부 RPC 지연 P99 | > 100 ms |

**MirrorMaker 2 전용 메트릭**:

```bash
# Kafka Connect REST API로 MM2 커넥터 상태 확인
curl http://connect-cluster:8083/connectors/seoul-to-tokyo/status | jq .

# 예상 출력:
# {
#   "name": "seoul-to-tokyo",
#   "connector": { "state": "RUNNING" },
#   "tasks": [{ "id": 0, "state": "RUNNING" }]
# }

# 복제 처리량 확인
curl http://connect-cluster:8083/connectors/seoul-to-tokyo/offsets | jq .
```

### 알람 설계 원칙

멀티 클러스터 알람은 **계층적으로** 설계해야 합니다. 모든 경고를 동일한 심각도로 처리하면 알람 피로(Alert Fatigue)가 발생하여 실제 장애를 놓칩니다.

```
P1 (즉시 대응): 복제 지연 > RPO 임계값
  → 담당자 전화 호출, 15분 내 대응

P2 (1시간 내 대응): 복제 지연 > RPO의 50%
  → 슬랙 알람, 다음 근무 시간 내 대응

P3 (다음 날 대응): MM2 커넥터 재시작 횟수 > 3회/일
  → 이메일 보고서, 주간 회의에서 검토
```

### 용량 계획 (Capacity Planning)

대상 클러스터는 Failover 시 소스 클러스터의 전체 트래픽을 감당해야 합니다. 그러나 평소에는 소스 트래픽의 복제본만 받으므로 낮은 부하로 운영됩니다. 이 간극을 미리 계획해야 합니다.

```
소스 클러스터: 10Gbps 쓰기 처리량, 30Gbps 읽기 처리량
대상 클러스터 (Active-Passive 평시): 10Gbps 복제 수신 + 5Gbps 읽기 (분석)
대상 클러스터 (Failover 시 필요): 10Gbps 쓰기 + 30Gbps 읽기

→ 대상 클러스터는 소스와 동일한 용량으로 구성해야 Failover 가능
→ 비용 절감을 위해 Auto Scaling 또는 Burst 용량 확보 필요
```

---

## 9. 실전 패턴: 멀티 클러스터 설계 결정 가이드

### 결정 트리

다음 질문들을 순서대로 답하면 어떤 방식을 선택해야 하는지 좁혀집니다.

```
Q1. 목적이 무엇인가?
  ├── 재해 복구만 → Q2
  ├── 지연 최소화 + DR → Q3
  └── 분석 워크로드 분리 → Remote Read Replicas

Q2. RPO 요구사항은?
  ├── RPO < 1분 → MirrorMaker 2 + 낮은 복제 지연 설정
  └── RPO < 1시간 → Remote Read Replicas

Q3. 양방향 쓰기가 필요한가?
  ├── 예 → Active-Active + MirrorMaker 2 (충돌 해결 전략 필수)
  └── 아니오 → Active-Passive + MirrorMaker 2 또는 Cluster Linking

Q4. Confluent Platform을 사용하는가?
  ├── 예 → Cluster Linking 우선 검토 (낮은 지연, 오프셋 보존)
  └── 아니오 → MirrorMaker 2 또는 Remote Read Replicas
```

### 패턴 A: DR 전용 (가장 일반적)

소규모~중규모 서비스에서 재해 복구를 목적으로 멀티 클러스터를 도입하는 가장 흔한 패턴입니다.

```
구성: Active-Passive
복제: MirrorMaker 2 (단방향)
목표: RPO < 5분, RTO < 15분
비용: 대상 클러스터를 소형으로 구성하고 Failover 시 Auto Scaling
```

```bash
# 최소 설정으로 시작하는 DR 클러스터
# 소스: 3노드 8코어 32GB
# 대상: 3노드 4코어 16GB (평시 복제만 받음)
# Failover 시: 노드 업그레이드 또는 수평 확장
```

### 패턴 B: 글로벌 서비스 지연 최소화

글로벌 사용자를 대상으로 지연을 최소화하는 패턴입니다. 각 지역 사용자는 가장 가까운 클러스터를 사용합니다.

```
구성: Active-Active (지역별)
복제: MirrorMaker 2 (양방향)
핵심 과제: 충돌 해결, 순환 복제 방지
예시: 서울(한국/일본 사용자) ↔ 싱가포르(동남아 사용자) ↔ 프랑크푸르트(유럽 사용자)
```

각 클러스터는 해당 지역 사용자의 데이터만 쓰도록 애플리케이션 레벨에서 라우팅합니다. 다른 지역 데이터는 읽기만 하도록 설계하면 충돌을 최소화할 수 있습니다.

### 패턴 C: 분석/운영 분리

운영 클러스터에서 분석 워크로드를 분리하는 패턴입니다. Redpanda 고유의 Remote Read Replicas가 가장 적합합니다.

```
구성: 소스(운영) + Read Replica(분석)
복제: Remote Read Replicas
장점: 운영 클러스터에 부하 없음, 분석 클러스터 독립 스케일
사용 예: Spark, Flink, dbt가 Read Replica에서 데이터 읽기
```

```bash
# 분석 팀이 Read Replica에서 Kafka Consumer로 읽기
# bootstrap.servers=tokyo-replica:9092  ← Read Replica 엔드포인트
# 나머지 설정은 일반 Consumer와 동일
kafka-console-consumer.sh \
  --bootstrap-server tokyo-replica:9092 \
  --topic orders \
  --from-beginning
```

---

## 참고 자료

- **Confluent**: [Geo-Replication Pattern](https://docs.confluent.io/platform/current/multi-dc-deployments/replicator/index.html)
- **Redpanda 공식 문서**: [Remote Read Replicas](https://docs.redpanda.com/current/manage/remote-read-replicas/)
- **Redpanda 공식 문서**: [Tiered Storage](https://docs.redpanda.com/current/manage/tiered-storage/)
- **Apache Kafka**: [MirrorMaker 2 공식 문서](https://kafka.apache.org/documentation/#georeplication)
- **기존 문서**: `07-tiered-storage.md` — Tiered Storage 설정 상세
- **기존 문서**: `14-reference-architecture.md` — 멀티 클러스터 아키텍처 개요
