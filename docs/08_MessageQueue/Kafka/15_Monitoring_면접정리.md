# Chapter 15: Kafka 모니터링과 알림 - 면접 정리

---

## 1. 인프라스트럭처 메트릭 (Infrastructure Metrics)

### 1.1 개요

Kafka 모니터링의 첫 번째 계층은 인프라스트럭처(하드웨어) 메트릭입니다. 브로커와 클라이언트가 올바르게 동작하더라도 기반 인프라의 리소스가 부족하면 성능 문제가 발생합니다. 디스크, 네트워크, CPU, 메모리의 상태를 지속적으로 모니터링해야 합니다.

**인프라 모니터링 계층**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Metrics                        │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Disk       │  │   Network    │  │   Memory             │   │
│  │   Usage      │  │   Utilization│  │   (Page Cache)       │   │
│  │              │  │              │  │                      │   │
│  │  < 60% 권장  │  │  < 60% 권장  │  │  충분한 여유 필요    │   │
│  │              │  │              │  │                      │   │
│  │  리밸런싱    │  │  브로커 장애 │  │  Page Cache로       │   │
│  │  공간 확보   │  │  시 부하 증가│  │  성능 향상          │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                        CPU Load                           │   │
│  │                                                           │   │
│  │   일시적 스파이크: 정상 (Compaction, 리밸런싱 시)        │   │
│  │   지속적 고부하: 스케일링 필요                           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 권장 임계값

| 메트릭 | 권장 임계값 | 초과 시 의미 | 대응 방안 |
|--------|-------------|--------------|-----------|
| **Disk Usage** | < 60% | 파티션 리밸런싱 공간 부족 | 디스크 추가, 보존 기간 단축 |
| **Network Utilization** | < 60% | 브로커 장애 시 대역폭 부족 | 네트워크 업그레이드, 브로커 추가 |
| **Memory** | 충분한 여유 | Page Cache 감소로 성능 저하 | RAM 추가, JVM Heap 조정 |
| **CPU Load** | 일시적 OK | 지속적 고부하 시 처리 지연 | 브로커 추가, 워크로드 분산 |

### 1.3 60% 임계값의 이유

디스크와 네트워크의 60% 임계값은 **장애 대비 여유 공간**을 확보하기 위함입니다.

**디스크 60% 시나리오**:

```
정상 상태 (3개 브로커, 각 60% 사용):
┌─────────┐  ┌─────────┐  ┌─────────┐
│Broker 1 │  │Broker 2 │  │Broker 3 │
│████░░   │  │████░░   │  │████░░   │
│ 60%     │  │ 60%     │  │ 60%     │
└─────────┘  └─────────┘  └─────────┘

브로커 1 장애 → 리밸런싱 발생:
┌─────────┐  ┌─────────┐  ┌─────────┐
│Broker 1 │  │Broker 2 │  │Broker 3 │
│ OFFLINE │  │██████░░ │  │██████░░ │
│         │  │  90%    │  │  90%    │
└─────────┘  └─────────┘  └─────────┘
             ↑ 파티션 이동으로 증가

만약 80%였다면? → 리밸런싱 중 디스크 Full 위험!
```

**네트워크 60% 시나리오**:

```
정상 상태:
- 각 브로커 네트워크 60% 사용
- 브로커 1 장애 시 클라이언트들이 브로커 2, 3으로 재연결
- 복제 트래픽도 브로커 2, 3에 집중
- 40% 여유 공간이 급증하는 트래픽 흡수
```

### 1.4 추세(Trend) 모니터링의 중요성

단순 스냅샷이 아닌 **시간에 따른 추세**를 확인해야 합니다.

```
정상적인 일시적 스파이크:
┌────────────────────────────────────────────────────┐
│ CPU %                                              │
│ 100│      ▲ Compaction           ▲ Rebalancing    │
│    │      ║                      ║                │
│  80│ ─────╨──────────────────────╨────────────    │
│  60│                                              │
│  40│─────────────────────────────────────────    │
│    └──────────────────────────────────────────── │
│         10:00   11:00   12:00   13:00   14:00     │
└────────────────────────────────────────────────────┘
→ 정상: 피크 후 즉시 정상화

비정상적인 지속적 고부하:
┌────────────────────────────────────────────────────┐
│ CPU %                                              │
│ 100│─────────────────────────────────────────    │
│  80│─────────────────────────────────────────    │
│  60│                                              │
│  40│                                              │
│    └──────────────────────────────────────────── │
│         10:00   11:00   12:00   13:00   14:00     │
└────────────────────────────────────────────────────┘
→ 비정상: 스케일링 필요
```

---

## 2. 브로커 메트릭 (Broker Metrics)

### 2.1 MBean 명명 규칙

Kafka 메트릭은 **Java MBeans** 형식을 따릅니다. 도메인(domain)과 속성(attributes)으로 구성됩니다.

```
MBean 구조:
domain:type=xxx,name=yyy

예시:
kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions
│            │                   │
│            │                   └─ 메트릭 이름
│            └─ 컴포넌트 타입
└─ 도메인 (kafka.server, kafka.network, kafka.log, kafka.controller)
```

**주요 도메인**:

| 도메인 | 설명 | 주요 메트릭 |
|--------|------|-------------|
| `kafka.server` | 브로커 서버 메트릭 | UnderReplicatedPartitions, PartitionCount |
| `kafka.network` | 네트워크 계층 메트릭 | NetworkProcessorAvgIdlePercent |
| `kafka.log` | 로그/스토리지 메트릭 | LogEndOffset, LogStartOffset |
| `kafka.controller` | 컨트롤러 메트릭 | ActiveController, OfflinePartitions |

### 2.2 Kafka Server 메트릭 (복제 상태)

복제 상태를 나타내는 메트릭은 **데이터 내구성**을 모니터링하는 데 핵심입니다.

**복제 상태 메트릭 관계**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Replication Health Hierarchy                  │
│                                                                  │
│  정상 상태:                                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ UnderReplicatedPartitions = 0                              │  │
│  │ AtMinIsrPartitionCount = 0                                │  │
│  │ UnderMinIsrPartitionCount = 0                             │  │
│  │ OfflineReplicaCount = 0                                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  경고 상태 (UnderReplicated > 0):                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 일부 레플리카가 동기화 지연                                 │  │
│  │                                                           │  │
│  │ 원인:                                                      │  │
│  │ ├─ 브로커 오프라인 (지속적)                                │  │
│  │ ├─ 네트워크 문제 (변동)                                    │  │
│  │ └─ 디스크 I/O 병목 (변동)                                  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  위험 상태 (UnderMinIsr > 0):                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ⚠️ acks=all 쓰기 불가!                                    │  │
│  │                                                           │  │
│  │ 예: min.insync.replicas=2, ISR=1                          │  │
│  │ → Producer가 acks=all로 쓰기 시도하면 NotEnoughReplicas   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  치명적 상태 (OfflineReplica > 0):                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 🚨 해당 파티션 읽기/쓰기 불가                             │  │
│  │                                                           │  │
│  │ 리더와 모든 레플리카가 오프라인                            │  │
│  │ → 즉시 조치 필요                                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**핵심 Server 메트릭**:

| 메트릭 | 설명 | 정상 값 | 알람 조건 |
|--------|------|---------|----------|
| `UnderReplicatedPartitions` | 동기화 지연 레플리카가 있는 파티션 수 | **0** | > 0 지속 시 |
| `AtMinIsrPartitionCount` | 정확히 min.insync.replicas를 충족하는 파티션 수 | 낮을수록 좋음 | 급증 시 |
| `UnderMinIsrPartitionCount` | min.insync.replicas 미달 파티션 수 | **0** | > 0 즉시 |
| `OfflineReplicaCount` | 오프라인 레플리카 수 | **0** | > 0 즉시 |
| `PartitionCount` | 브로커의 총 파티션 수 | 균등 분배 | 불균형 시 |
| `LeaderCount` | 브로커의 리더 파티션 수 | 균등 분배 | 불균형 시 |

### 2.3 Kafka Network 메트릭

**NetworkProcessorAvgIdlePercent**는 브로커의 네트워크 처리 용량을 나타내는 핵심 메트릭입니다.

```
NetworkProcessorAvgIdlePercent 해석:

1.0 ────────────────────────────────── 완전히 유휴 (트래픽 없음)
    │
0.7 ────────────────────────────────── ✅ 정상 (30% 사용)
    │
0.5 ────────────────────────────────── ⚠️ 주의 (50% 사용)
    │
0.3 ────────────────────────────────── 🚨 위험 (70% 사용)
    │
0.0 ────────────────────────────────── 포화 (100% 사용)

< 0.3 = 클러스터가 과부하 상태이거나 곧 과부하될 것
```

**0.3 미만 시 대응**:
1. 즉시: 트래픽 소스 확인 (갑작스러운 Producer 증가?)
2. 단기: 브로커 추가 고려
3. 장기: 파티션 분배 최적화

### 2.4 Kafka Controller 메트릭

Controller 메트릭은 클러스터 전체의 상태를 나타냅니다.

| 메트릭 | 설명 | 정상 값 |
|--------|------|---------|
| `ActiveController` | 현재 컨트롤러 역할 수행 여부 | 클러스터에서 정확히 1개 브로커만 1 |
| `ActiveBrokerCount` | 활성 브로커 수 | 예상 브로커 수와 일치 |
| `FencedBrokerCount` | 비활성(격리된) 브로커 수 | 0 |
| `OfflinePartitions` | 오프라인 파티션 수 | 0 |
| `PreferredReplicaImbalanceCount` | 선호 리더가 아닌 파티션 수 | 낮을수록 좋음 |

**PreferredReplicaImbalanceCount**가 높으면?
→ 선호 리더 선출이 필요합니다. 자동 리더 재선출(`auto.leader.rebalance.enable=true`) 또는 수동으로 `kafka-leader-election.sh`를 실행합니다.

---

## 3. 클라이언트 메트릭 (Client Metrics)

### 3.1 클라이언트 메트릭 도메인

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client Metric Domains                         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ kafka.       │  │ kafka.       │  │ kafka.               │   │
│  │ producer     │  │ consumer     │  │ connect              │   │
│  │              │  │              │  │                      │   │
│  │ record-*     │  │ records-lag  │  │ connector-*          │   │
│  │ request-*    │  │ records-lead │  │ task-*               │   │
│  │ batch-*      │  │ rebalance-*  │  │ source/sink-*        │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ kafka.streams                                             │   │
│  │                                                           │   │
│  │ stream-thread-* / task-* / state-store-*                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 프로듀서 메트릭 (Producer Metrics)

프로듀서 메트릭은 메시지 전송 상태와 성능을 모니터링합니다.

**핵심 프로듀서 메트릭**:

| 메트릭 | 설명 | 정상 상태 | 비정상 시 의미 |
|--------|------|----------|---------------|
| `record-error-rate` | 초당 오류 레코드 수 | **0** | 직렬화 오류, 권한 문제, 토픽 없음 |
| `produce-throttle-time-avg` | 평균 쓰로틀링 지연(ms) | 0에 가까움 | Quota 초과 또는 브로커 과부하 |
| `request-latency-avg` | 평균 요청 지연(ms) | 안정적 | 급증 시 브로커/네트워크 문제 |
| `requests-in-flight` | 대기 중인 요청 수 | 설정값 이하 | 브로커 응답 지연 |
| `batch-size-avg` | 평균 배치 크기 | 적절한 수준 | 너무 작으면 오버헤드 증가 |
| `record-queue-time-avg` | 배치 대기 시간(ms) | linger.ms에 비례 | 너무 길면 지연 증가 |

**record-error-rate > 0 원인 분석**:

```
record-error-rate > 0
├─ SerializationException: Serializer 설정 오류
├─ AuthorizationException: ACL 권한 부족
├─ UnknownTopicOrPartitionException: 토픽 없음 또는 auto.create=false
├─ RecordTooLargeException: max.request.size 초과
└─ TimeoutException: 재시도 소진 (retries, delivery.timeout.ms)
```

### 3.3 컨슈머 메트릭 (Consumer Metrics)

컨슈머 메트릭은 메시지 처리 상태와 Consumer Group 안정성을 모니터링합니다.

**records-lag vs records-lead**:

```
토픽 파티션의 메시지 분포:
┌───────────────────────────────────────────────────────────────┐
│ Offset:  0    100   200   300   400   500   600   700   800   │
│          │     │     │     │     │     │     │     │     │   │
│          ▼     ▼     ▼     ▼     ▼     ▼     ▼     ▼     ▼   │
│ ─────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────────│
│          │                 │                       │           │
│          │                 │                       │           │
│   Log Start              Consumer                Log End       │
│   Offset=100             Offset=400             Offset=800    │
│                                                               │
│          ◀───────────────▶ ◀─────────────────────▶           │
│           records-lead=300   records-lag=400                  │
│          (삭제까지 여유)    (미처리 메시지)                    │
└───────────────────────────────────────────────────────────────┘

⚠️ 위험 상황: records-lead가 낮고 records-lag가 높음
→ 컨슈머가 처리하기 전에 메시지가 삭제될 수 있음!
```

**핵심 컨슈머 메트릭**:

| 메트릭 | 설명 | 정상 상태 | 비정상 시 의미 |
|--------|------|----------|---------------|
| `records-lag` | 미처리 메시지 수 | 0 또는 낮은 값 | 계속 증가하면 처리 병목 |
| `records-lead` | 삭제까지 여유 메시지 수 | 충분히 높음 | 낮으면 데이터 손실 위험 |
| `rebalance-rate-per-hour` | 시간당 리밸런싱 수 | 낮고 안정적 | 높으면 Consumer 불안정 |
| `time-between-poll-max` | 폴링 간 최대 시간(ms) | max.poll.interval.ms 미만 | 초과 시 리밸런싱 발생 |
| `fetch-latency-avg` | 평균 fetch 지연(ms) | 안정적 | 급증 시 브로커 과부하 |
| `commit-latency-avg` | 평균 커밋 지연(ms) | 안정적 | 급증 시 조정자 과부하 |

**records-lag 계속 증가 시 대응**:

```
records-lag 증가 대응 순서:

1. 컨슈머 스케일 아웃
   └─ 파티션 수 ≥ 컨슈머 수 확인 후 컨슈머 추가

2. 처리 로직 최적화
   ├─ 배치 처리 도입
   ├─ 비동기 처리
   └─ 외부 시스템 병목 제거

3. 파티션 수 증가
   └─ 병렬 처리 용량 확대 (주의: 기존 순서 보장 영향)

4. 컨슈머 설정 조정
   ├─ max.poll.records 증가
   └─ fetch.min.bytes / fetch.max.wait.ms 조정
```

### 3.4 Kafka Connect & Streams 메트릭

**Kafka Connect 핵심 메트릭**:

| 메트릭 | 설명 | 정상 값 |
|--------|------|---------|
| `connector-failed-task-count` | 실패한 태스크 수 | **0** |
| `connector-running-task-count` | 실행 중인 태스크 수 | 설정값과 일치 |
| `connector-paused-task-count` | 일시 중지된 태스크 수 | 의도한 경우만 |
| `source-record-poll-rate` | Source Connector 레코드 수집률 | 안정적 |
| `sink-record-send-rate` | Sink Connector 레코드 전송률 | 안정적 |

**Kafka Streams 핵심 메트릭**:

| 메트릭 | 설명 | 정상 값 |
|--------|------|---------|
| `failed-stream-threads` | 실패한 스트림 스레드 수 | **0** |
| `dropped-records-rate` | 삭제된 레코드 비율 | **0** (Critical!) |
| `process-rate` | 초당 처리 레코드 수 | 안정적 |
| `commit-rate` | 초당 커밋 수 | 안정적 |

**dropped-records-rate > 0**은 심각한 상황입니다. 원인:
- 윈도우 경과 후 도착한 late records
- 잘못된 타임스탬프
- 처리 오류

---

## 4. 알림 전략 (Alerting)

### 4.1 메트릭에서 알림까지

메트릭 수집부터 알림 발생까지의 파이프라인입니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Alerting Pipeline                             │
│                                                                  │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌─────────┐│
│  │  Metrics  │───▶│  Storage  │───▶│   Query   │───▶│ Alert   ││
│  │ Collection│    │ (TSDB)    │    │ & Rules   │    │ Manager ││
│  └───────────┘    └───────────┘    └───────────┘    └─────────┘│
│       │                                  │               │       │
│       ▼                                  ▼               ▼       │
│  JMX Exporter              Prometheus Rules      Alertmanager    │
│  + Prometheus              (임계값, 평활화)       (라우팅, 억제) │
│                                                                  │
│                      ┌─────────────────────────────────────┐    │
│                      │          Visualization              │    │
│                      │          (Grafana)                  │    │
│                      └─────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 평활화(Smoothing)

일시적인 스파이크로 인한 거짓 알림을 방지하기 위해 **평활화**를 적용합니다.

```yaml
# Prometheus Alert Rule 예시

# 나쁜 예: 순간 값 기반 (거짓 양성 많음)
- alert: HighCPUUsage_Bad
  expr: cpu_usage > 80
  # CPU가 잠시라도 80% 초과하면 알림

# 좋은 예: 평활화 적용
- alert: HighCPUUsage_Good
  expr: avg_over_time(cpu_usage[5m]) > 80
  for: 5m
  # 5분 평균이 80% 초과하고, 5분 지속 시에만 알림
```

**평활화 함수 선택**:

| 함수 | 용도 |
|------|------|
| `avg_over_time()` | 평균 값 기반 (일반적 사용) |
| `max_over_time()` | 피크 값 감지 필요 시 |
| `min_over_time()` | 최소값 보장 필요 시 |
| `rate()` | 증가율 기반 (에러 카운터 등) |

### 4.3 Alert Fatigue 방지

**Alert Fatigue**는 과도한 거짓 알림으로 인해 운영자가 알림에 둔감해지는 현상입니다. 양치기 소년 효과와 같습니다.

```
Alert Fatigue 악순환:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  과민한 알림 설정    거짓 양성 증가    알림 무시 습관            │
│       │                   │                │                    │
│       ▼                   ▼                ▼                    │
│  ┌─────────┐        ┌─────────┐       ┌─────────┐              │
│  │ 낮은    │───────▶│ 하루    │──────▶│ 알림을  │              │
│  │ 임계값  │        │ 수십 개 │       │ 무시    │              │
│  │ 설정    │        │ 알림    │       │         │              │
│  └─────────┘        └─────────┘       └─────────┘              │
│                                             │                   │
│                                             ▼                   │
│                                       ┌─────────┐              │
│                                       │ 실제    │              │
│                                       │ 장애    │              │
│                                       │ 놓침    │              │
│                                       └─────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

**Alert Fatigue 방지 원칙**:

| 원칙 | 설명 |
|------|------|
| **평활화 적용** | 초 단위 변동을 분 단위로 평균 |
| **자가 치유 허용** | K8s 자동 재시작, 임시 스파이크에 시간 부여 |
| **보수적 시작** | 낮은 민감도로 시작 후 점진적 조정 |
| **정기 검토** | 임계값 주기적 재평가 |
| **알림 분류** | Critical, Warning, Info 등 심각도 구분 |
| **알림 억제** | 관련 알림 그룹화, 중복 억제 |

### 4.4 알림 품질 향상

좋은 알림은 **행동 가능한(actionable)** 정보를 제공합니다.

```yaml
# 좋은 알림 예시 (Prometheus Alertmanager)
- alert: KafkaUnderReplicatedPartitions
  expr: kafka_server_replicamanager_underreplicatedpartitions > 0
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Kafka has under-replicated partitions"
    description: "{{ $value }} partitions are under-replicated on {{ $labels.instance }}"
    dashboard: "https://grafana.example.com/d/kafka-overview"
    playbook: "https://wiki.example.com/kafka/under-replicated-partitions"
    # 의미 설명 + 대시보드 링크 + 문제 해결 플레이북
```

**알림에 포함할 정보**:

| 항목 | 설명 |
|------|------|
| **의미 설명** | 이 알림이 왜 중요한지 |
| **현재 값** | 메트릭의 현재 값 |
| **대시보드 링크** | 관련 Grafana 대시보드 |
| **플레이북 링크** | 문제 해결 가이드 |
| **자동 조치** | 가능한 경우 자동 조치 트리거 |

---

## 5. 배포 환경별 모니터링 고려사항

### 5.1 환경별 모니터링 포인트

배포 환경에 따라 모니터링해야 할 추가 메트릭이 다릅니다.

```
┌─────────────────────────────────────────────────────────────────┐
│              Deployment-Specific Monitoring                      │
│                                                                  │
│  자체 하드웨어 ────────────────────────────────────────────────│
│  │  ├─ 디스크 SMART 상태, 배드 섹터                            │
│  │  ├─ 네트워크 인터페이스 에러                                 │
│  │  ├─ CPU 온도, 팬 속도                                       │
│  │  └─ 전원 공급 장치 상태                                      │
│                                                                  │
│  가상 머신 ────────────────────────────────────────────────────│
│  │  ├─ ⚠️ CPU Steal Time (st) - 다른 VM에 빼앗긴 CPU 시간     │
│  │  ├─ I/O Wait - 스토리지 지연                                │
│  │  ├─ 메모리 스와핑                                           │
│  │  └─ 하이퍼바이저 리소스 경합                                 │
│                                                                  │
│  퍼블릭 클라우드 ──────────────────────────────────────────────│
│  │  ├─ 인스턴스 상태 체크                                      │
│  │  ├─ 네트워크 지연 (cross-AZ, cross-region)                  │
│  │  ├─ EBS/Cloud Disk IOPS 제한                               │
│  │  └─ 오토스케일링 이벤트                                     │
│                                                                  │
│  Kubernetes ───────────────────────────────────────────────────│
│  │  ├─ ⚠️ Pod 상태 (Pending, CrashLoopBackOff)                │
│  │  ├─ 노드 리소스 (CPU, Memory, Disk Pressure)               │
│  │  ├─ PVC 상태 및 용량                                        │
│  │  └─ JMX Exporter Sidecar 상태                              │
│                                                                  │
│  관리형 서비스 ────────────────────────────────────────────────│
│  │  ├─ 처리량 제한 도달 여부                                   │
│  │  ├─ 컨슈머 지연                                             │
│  │  ├─ ⚠️ SLA 준수 여부                                       │
│  │  └─ 비용 모니터링                                           │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 VM 환경의 CPU Steal Time

**CPU Steal Time(st)**은 하이퍼바이저가 해당 VM에서 다른 VM으로 CPU 시간을 빼앗은 비율입니다.

```
top 명령어 출력:
%Cpu(s):  5.0 us,  2.0 sy,  0.0 ni, 90.0 id,  0.0 wa,  0.0 hi,  0.0 si,  3.0 st
                                                                          ↑
                                                                       Steal Time

st > 5%: 하이퍼바이저 리소스 경합 → VM 이동 또는 전용 호스트 고려
```

### 5.3 Kubernetes 환경의 JMX 메트릭 수집

Kubernetes에서 Kafka 메트릭을 수집하려면 **JMX Exporter Sidecar** 또는 **Agent** 방식을 사용합니다.

```yaml
# Strimzi Kafka CRD with JMX Exporter
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
spec:
  kafka:
    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
```

---

## 면접 예상 질문

### Q1: Kafka에서 가장 중요한 브로커 메트릭은 무엇인가요?

**모범 답변**:

가장 중요한 브로커 메트릭은 **`UnderReplicatedPartitions`**입니다.

이 메트릭은 ISR(In-Sync Replicas)에 포함되지 못한 레플리카가 있는 파티션 수를 나타냅니다. 정상 상태에서는 **0**이어야 합니다.

**0이 아닐 때 해석**:
- **지속적으로 > 0**: 특정 브로커가 오프라인이거나 심각한 문제 발생
- **변동이 잦음**: 네트워크 문제, 디스크 I/O 병목, 리소스 부족

**영향**:
- 데이터 내구성 저하 (레플리카 동기화 실패)
- 브로커 장애 시 데이터 손실 위험 증가
- `acks=all` 설정 시 쓰기 지연 발생 가능

**대응**:
1. 어떤 브로커에서 문제인지 확인 (`kafka-topics.sh --describe`)
2. 해당 브로커의 리소스(디스크, 네트워크, CPU) 점검
3. 브로커 로그 분석
4. 필요시 파티션 재배치

---

### Q2: Consumer Lag가 계속 증가하면 어떻게 대응하나요?

**모범 답변**:

Consumer Lag가 지속적으로 증가하면 컨슈머의 처리 속도가 Producer의 생산 속도를 따라가지 못하는 것입니다.

**대응 순서**:

1. **컨슈머 스케일 아웃**:
   - 현재 파티션 수 확인 (컨슈머 수 ≤ 파티션 수)
   - 파티션 수가 충분하면 컨슈머 인스턴스 추가
   - 파티션 수가 부족하면 먼저 파티션 증가 고려

2. **처리 로직 최적화**:
   - 배치 처리 도입 (여러 메시지를 한 번에 처리)
   - 비동기 처리 (외부 시스템 호출을 비동기로)
   - 외부 시스템 병목 제거 (DB 쿼리 최적화 등)

3. **컨슈머 설정 조정**:
   - `max.poll.records` 증가 (한 번에 더 많이 가져오기)
   - `fetch.min.bytes`, `fetch.max.wait.ms` 조정

4. **파티션 수 증가**:
   - 병렬 처리 용량 확대
   - 주의: 순서 보장 범위 변경

5. **처리 불필요 메시지 필터링**:
   - Consumer에서 필터링 대신 Kafka Streams로 전처리 고려

**추가로 확인할 것**:
- `records-lead` 값: 낮으면 메시지가 삭제되기 전에 처리하지 못할 위험

---

### Q3: Alert Fatigue란 무엇이며 어떻게 방지하나요?

**모범 답변**:

**Alert Fatigue**는 과도한 알림(특히 거짓 양성)으로 인해 운영자가 알림에 둔감해지는 현상입니다. 양치기 소년 효과와 유사합니다.

**문제점**:
- 실제 중요한 알림을 무시하게 됨
- 장애 대응 시간 증가
- 운영팀 번아웃

**방지 전략**:

1. **평활화(Smoothing) 적용**:
   - 순간 값 대신 시간 평균 사용
   - 예: `avg_over_time(cpu_usage[5m]) > 80`

2. **자가 치유 허용 시간**:
   - Kubernetes Pod 재시작 등 자동 복구에 시간 부여
   - 예: `for: 5m` (5분 지속 시에만 알림)

3. **보수적 시작**:
   - 초기에는 높은 임계값으로 시작
   - 점진적으로 조정하며 적정 수준 탐색

4. **정기 검토**:
   - 월간/분기별 알림 임계값 재평가
   - 거짓 양성 비율 분석

5. **알림 분류 및 억제**:
   - Critical, Warning, Info 등 심각도 구분
   - 관련 알림 그룹화 (한 장애에 수십 개 알림 방지)

6. **알림 품질 향상**:
   - 의미 설명, 대시보드 링크, 플레이북 포함
   - 행동 가능한(actionable) 알림만 발송

---

### Q4: NetworkProcessorAvgIdlePercent가 0.3 미만이면 어떤 의미인가요?

**모범 답변**:

**`NetworkProcessorAvgIdlePercent`**는 브로커의 네트워크 처리 스레드가 유휴 상태인 비율입니다. 1.0은 완전히 유휴, 0.0은 완전히 포화 상태입니다.

**0.3 미만의 의미**:
- 네트워크 스레드가 70% 이상 사용 중
- 클러스터가 **과부하 상태**이거나 **곧 과부하될 것**
- 요청 처리 지연 발생 가능

**즉각 조치**:
1. 트래픽 소스 확인 (갑작스러운 Producer 증가?)
2. 비정상적인 클라이언트 확인 (재시도 폭주?)
3. 불필요한 트래픽 차단

**단기 조치**:
1. 브로커 추가 고려
2. 네트워크 스레드 수 증가 (`num.network.threads`)

**장기 조치**:
1. 파티션 분배 최적화 (Cruise Control)
2. 클라이언트 배치 최적화 (batch.size, linger.ms)
3. 압축 활용으로 네트워크 부하 감소

---

### Q5: VM 환경에서 Kafka 모니터링 시 특별히 주의할 점은?

**모범 답변**:

VM 환경에서 Kafka를 운영할 때는 **리소스 경합**과 **I/O 성능**을 특별히 모니터링해야 합니다.

**주요 모니터링 포인트**:

1. **CPU Steal Time (st)**:
   - 하이퍼바이저가 다른 VM에 CPU를 할당한 시간
   - `top` 명령의 `st` 값 확인
   - 5% 이상이면 경합 발생, VM 이동 또는 전용 호스트 고려

2. **I/O Wait**:
   - 프로세스가 I/O 완료를 기다리는 시간
   - SAN/NAS 스토리지 지연 확인
   - 높으면 로컬 SSD 전환 고려

3. **메모리 스와핑**:
   - 스왑 사용 시 Page Cache 효과 저하
   - Kafka는 Page Cache에 크게 의존하므로 스왑 최소화 필수

4. **하이퍼바이저 오버커밋**:
   - CPU, 메모리 오버커밋 비율 확인
   - Kafka 브로커는 전용 리소스 권장

**권장 사항**:
- 가능하면 Kafka 브로커 VM에 전용 리소스 할당
- SAN 성능이 의심되면 로컬 SSD 사용
- VM 호스트 간 브로커 분산 배치

---

### Q6: records-lag와 records-lead의 차이점과 모니터링 의의는?

**모범 답변**:

두 메트릭은 컨슈머의 처리 위치를 다른 관점에서 보여줍니다.

**records-lag**:
- 정의: 컨슈머가 아직 처리하지 못한 메시지 수
- 계산: Log End Offset - Consumer Offset
- 의미: 처리 지연 정도
- 정상: 0 또는 낮은 값
- 모니터링: 계속 증가하면 처리 병목

**records-lead**:
- 정의: 컨슈머 오프셋과 로그 시작 오프셋 사이의 메시지 수
- 계산: Consumer Offset - Log Start Offset
- 의미: 삭제되기 전까지 여유 공간
- 정상: 충분히 높음
- 모니터링: 낮으면 데이터 손실 위험

**위험 시나리오**:
```
records-lead가 낮고 + records-lag가 높음
= 컨슈머가 처리하기 전에 메시지가 삭제될 수 있음!
```

**대응**:
1. 보존 기간(retention.ms) 연장
2. 컨슈머 처리 속도 개선
3. 알람 설정: records-lead < 임계값

---

## 실무 체크리스트

### 인프라 메트릭

- [ ] 디스크 사용률 < 60% 유지
- [ ] 네트워크 사용률 < 60% 유지
- [ ] CPU 지속적 고부하 모니터링
- [ ] 메모리 여유 공간 (Page Cache) 확보

### 브로커 메트릭

- [ ] UnderReplicatedPartitions = 0 확인
- [ ] UnderMinIsrPartitionCount = 0 확인
- [ ] NetworkProcessorAvgIdlePercent > 0.3 확인
- [ ] ActiveController가 정확히 1개인지 확인
- [ ] PartitionCount, LeaderCount 균등 분배 확인

### 클라이언트 메트릭

- [ ] Producer record-error-rate = 0 확인
- [ ] Consumer records-lag 추세 모니터링
- [ ] Consumer records-lead 충분한지 확인
- [ ] rebalance-rate-per-hour 안정적인지 확인
- [ ] Connect connector-failed-task-count = 0 확인

### 알림 설정

- [ ] 평활화 적용 (avg_over_time, for 절)
- [ ] 알림에 대시보드/플레이북 링크 포함
- [ ] 심각도 분류 (Critical, Warning, Info)
- [ ] 정기적인 임계값 검토 프로세스

### 환경별 추가 모니터링

- [ ] VM: CPU Steal Time, I/O Wait
- [ ] Cloud: 네트워크 지연, IOPS 제한
- [ ] K8s: Pod 상태, 노드 리소스
- [ ] Managed: SLA 준수, 비용

---

## 참고 자료

- [Kafka Monitoring Documentation](https://kafka.apache.org/documentation/#monitoring)
- [Prometheus JMX Exporter](https://github.com/prometheus/jmx_exporter)
- [Strimzi Kafka Dashboards](https://github.com/strimzi/strimzi-kafka-operator/tree/main/examples/metrics)
- [Grafana Kafka Dashboards](https://grafana.com/grafana/dashboards/)
- [Kafka at LinkedIn - Monitoring](https://www.confluent.io/blog/kafka-monitoring-guide/)
