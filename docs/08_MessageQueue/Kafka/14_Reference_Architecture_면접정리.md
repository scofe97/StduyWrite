# Chapter 14: Kafka Reference Architecture - 면접 정리

---

## 1. Kafka 운영 환경 구성

### 1.1 전체 아키텍처 개요

Kafka 프로덕션 환경은 브로커만으로 구성되지 않습니다. 실제 운영 환경에서는 다양한 컴포넌트들이 유기적으로 연결되어 전체 데이터 파이프라인을 형성합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Applications Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐               │
│  │ Producers│  │ Consumers│  │ Kafka Streams    │               │
│  └────┬─────┘  └────▲─────┘  │ Applications     │               │
│       │             │        └──────────────────┘               │
└───────┼─────────────┼───────────────────────────────────────────┘
        │             │
┌───────▼─────────────┴───────────────────────────────────────────┐
│                      Kafka Cluster                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────────────────┐  │
│  │Broker 1 │  │Broker 2 │  │Broker 3 │  │ Coordination       │  │
│  │(Leader) │  │(Replica)│  │(Replica)│  │ (KRaft/ZooKeeper)  │  │
│  └─────────┘  └─────────┘  └─────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼─────────────────────────────┐
│                      Integration Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │Kafka Connect │  │Schema        │  │ Stream Processing      │ │
│  │(Source/Sink) │  │Registry      │  │ (ksqlDB, Flink)        │ │
│  └──────────────┘  └──────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼─────────────────────────────┐
│                      Operations Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │Cruise Control│  │ Monitoring   │  │ GUI Tools              │ │
│  │(부하 분산)   │  │ (Prometheus) │  │ (Kafbat UI, Kpow)      │ │
│  └──────────────┘  └──────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**핵심 컴포넌트별 역할**:

| 컴포넌트 | 역할 | 필수 여부 |
|----------|------|-----------|
| **Brokers** | 데이터 저장 및 처리, 클러스터의 핵심 | 필수 |
| **Coordination** | 클러스터 메타데이터 관리 (KRaft 또는 ZK) | 필수 |
| **Kafka Connect** | 외부 시스템(DB, 파일 등)과의 데이터 연동 | 선택 |
| **Schema Registry** | 스키마 버전 관리 및 호환성 검증 | 권장 |
| **Cruise Control** | 브로커 부하 분산 및 자동 재배치 | 권장 |
| **Monitoring** | 클러스터 상태 모니터링 및 알림 | 필수 |

---

## 2. 유용한 도구

### 2.1 kcat (kafkacat)

kcat은 C 기반 librdkafka 라이브러리를 사용하는 경량 CLI 도구입니다. Java 기반 kafka-console-producer/consumer보다 빠른 시작 시간을 제공하며, 개발 및 디버깅 용도로 적합합니다.

**kcat vs kafka-console-* 비교**:

| 특성 | kcat | kafka-console-* |
|------|------|-----------------|
| 언어 | C (librdkafka) | Java |
| 시작 시간 | 빠름 (~100ms) | 느림 (~2s, JVM 로딩) |
| 메모리 사용 | 적음 | 많음 (JVM Heap) |
| 헤더 지원 | O | O |
| 용도 | 개발/테스트 | 개발/테스트 |

**주요 명령어 예시**:

```bash
# Producer 모드: 메시지 생산
kcat -b localhost:9092 -t my-topic -P
> message1
> message2
# Ctrl-D로 종료

# Consumer 모드: 메시지 소비
kcat -b localhost:9092 -t my-topic -C

# Key:Value 형식으로 생산 (-K: key 구분자)
kcat -b localhost:9092 -t my-topic -P -K:
> key1:value1
> key2:value2

# 특정 offset부터 읽기
kcat -b localhost:9092 -t my-topic -C -o beginning  # 처음부터
kcat -b localhost:9092 -t my-topic -C -o end        # 끝부터
kcat -b localhost:9092 -t my-topic -C -o 100        # offset 100부터

# 메타데이터 조회
kcat -b localhost:9092 -L  # 클러스터 정보
kcat -b localhost:9092 -L -t my-topic  # 특정 토픽 정보
```

**주의사항**: kcat은 개발/테스트용 도구입니다. 프로덕션 데이터 쓰기에는 적합하지 않으며, 대량 데이터 처리에는 정식 Producer/Consumer 애플리케이션을 사용해야 합니다.

### 2.2 GUI 도구

Kafka 클러스터를 시각적으로 관리하고 모니터링할 수 있는 다양한 GUI 도구들이 있습니다.

**주요 GUI 도구 분류**:

```
┌─────────────────────────────────────────────────────────────┐
│                      GUI Tools 분류                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Open Source   │    Commercial   │    Cloud Provider       │
├─────────────────┼─────────────────┼─────────────────────────┤
│ Kafbat UI       │ Kpow            │ Confluent Cloud UI      │
│ (구 Provectus)  │ Kadeck          │ Aiven Console           │
│                 │ Conduktor       │ AWS MSK Console         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

**GUI 도구 주요 기능**:

| 기능 | 설명 |
|------|------|
| 토픽 탐색 | 토픽 목록, 파티션 분포, 설정 확인 |
| 메시지 조회 | 실시간 메시지 확인, 검색/필터링 |
| Connect 관리 | Connector 상태, 태스크 모니터링 |
| Schema Registry | 스키마 버전 확인, 호환성 검증 |
| Consumer Group | 그룹 상태, Lag 모니터링 |
| ACL 관리 | 접근 권한 설정 조회 |

**프로덕션 환경 GUI 사용 원칙**:

```
✅ 허용되는 사용:
   ├─ 토픽/메시지 조회 (읽기 전용)
   ├─ Consumer Group Lag 모니터링
   ├─ Connector 상태 확인
   └─ Schema Registry 버전 확인

❌ 금지되는 사용:
   ├─ GUI로 토픽 생성/삭제
   ├─ GUI로 설정 변경
   ├─ GUI로 프로덕션 데이터 수정
   └─ GUI를 주요 모니터링 도구로 사용
```

**권장 사항**: GUI는 모니터링 도구(Prometheus, Grafana)를 **대체할 수 없습니다**. 알람 설정, 이력 추적, 대시보드 등 전문 모니터링 시스템이 필요합니다.

### 2.3 GitOps 기반 리소스 관리

프로덕션 Kafka 환경에서는 모든 리소스(토픽, 사용자, ACL)를 Git 저장소에서 코드로 관리하는 GitOps 방식을 권장합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitOps Workflow                               │
│                                                                  │
│  ┌───────────┐     ┌───────────┐     ┌───────────────────────┐  │
│  │   Git     │────▶│   PR      │────▶│   CI/CD Pipeline      │  │
│  │Repository │     │ Review    │     │                       │  │
│  │           │     │           │     │ ┌───────────────────┐ │  │
│  │ topics.   │     │ ✅ Approve │     │ │ kafka-topics.sh   │ │  │
│  │   yaml    │     │           │     │ │ --create/--alter  │ │  │
│  │ acls.yaml │     │           │     │ └─────────┬─────────┘ │  │
│  │ users.    │     │           │     │           │           │  │
│  │   yaml    │     │           │     └───────────┼───────────┘  │
│  └───────────┘     └───────────┘                 │               │
│                                                   ▼               │
│                                         ┌─────────────────┐      │
│                                         │  Kafka Cluster  │      │
│                                         └─────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

**GitOps 핵심 원칙**:

| 원칙 | 설명 |
|------|------|
| **Git = Source of Truth** | 모든 리소스 정의는 Git에 저장 |
| **수동 생성 금지** | CLI/GUI로 직접 리소스 생성 금지 |
| **PR 기반 변경** | 모든 변경은 Pull Request로 리뷰 |
| **자동화 배포** | CI/CD 파이프라인으로 자동 적용 |
| **변경 이력 추적** | Git 커밋으로 모든 변경 이력 관리 |

**kcctl - Kafka Connect CLI**:

Kafka Connect 리소스도 GitOps로 관리할 수 있습니다.

```bash
# Connector 생성/수정 (선언적)
kcctl apply -f connector-config.json

# Connector 목록 조회
kcctl get connectors

# Connector 상태 확인
kcctl describe connector my-connector

# Connector 삭제
kcctl delete connector my-connector

# Connector 일시 중지/재개
kcctl pause connector my-connector
kcctl resume connector my-connector
```

### 2.4 Cruise Control

Cruise Control은 LinkedIn에서 개발한 Kafka 클러스터 부하 분산 도구입니다. 브로커 간 파티션 분포를 자동으로 최적화하고, 브로커 추가/제거 시 데이터를 재배치합니다.

**Cruise Control 아키텍처**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cruise Control Architecture                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Kafka Cluster                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │   │
│  │  │  Broker 1   │  │  Broker 2   │  │  Broker 3   │       │   │
│  │  │             │  │             │  │             │       │   │
│  │  │ Metrics JAR │  │ Metrics JAR │  │ Metrics JAR │       │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │   │
│  │         │                │                │              │   │
│  │         ▼                ▼                ▼              │   │
│  │  ┌──────────────────────────────────────────────┐        │   │
│  │  │         __CruiseControlMetrics Topic         │        │   │
│  │  │         (내부 메트릭 저장)                    │        │   │
│  │  └──────────────────────────────────────────────┘        │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Cruise Control                         │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │   Metrics    │  │   Analyzer   │  │   Executor   │    │   │
│  │  │  Collector   │─▶│  (Goals 기반)│─▶│  (파티션     │    │   │
│  │  │              │  │              │  │   이동 실행) │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  │                             │                             │   │
│  │                             ▼                             │   │
│  │                   ┌─────────────────┐                    │   │
│  │                   │ Cruise Control  │                    │   │
│  │                   │      UI         │                    │   │
│  │                   └─────────────────┘                    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Cruise Control 주요 기능**:

| 기능 | 설명 |
|------|------|
| **부하 모니터링** | CPU, RAM, Disk, Network 사용량 실시간 수집 |
| **부하 분석** | 설정된 목표(Goals) 기반으로 불균형 분석 |
| **파티션 재배치** | 리더/레플리카 파티션 균등 분배 제안 |
| **브로커 추가** | 신규 브로커에 기존 파티션 자동 분산 |
| **브로커 제거** | 제거 전 해당 브로커의 파티션을 다른 브로커로 이동 |
| **자동 복구** | 브로커 장애 감지 시 자동 재배치 |

**Goals (목표) 유형**:

```
Goals 우선순위 (높음 → 낮음):
├─ Hard Goals (필수 충족)
│   ├─ RackAwareGoal: 랙 간 레플리카 분산
│   ├─ ReplicaCapacityGoal: 브로커별 레플리카 수 제한
│   └─ DiskCapacityGoal: 디스크 용량 초과 방지
│
└─ Soft Goals (최선 노력)
    ├─ NetworkInboundCapacityGoal: 네트워크 입력 부하 분산
    ├─ NetworkOutboundCapacityGoal: 네트워크 출력 부하 분산
    ├─ CpuCapacityGoal: CPU 부하 분산
    └─ LeaderBytesInDistributionGoal: 리더 쓰기 부하 분산
```

**주의사항**: 파티션 이동은 네트워크와 디스크 I/O 부하가 높습니다. 반드시 **피크 타임을 피해** 재배치를 실행해야 합니다.

---

## 3. 배포 환경

### 3.1 배포 옵션 비교

Kafka 클러스터는 다양한 환경에 배포할 수 있으며, 각 환경은 고유한 장단점을 가집니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    배포 환경 옵션                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Self-Managed (직접 운영)                                       │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│   │ 자체 HW     │  │  VM/가상화  │  │    Kubernetes           │ │
│   │ (Bare Metal)│  │             │  │    (Strimzi)            │ │
│   └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                  │
│   Managed Services (클라우드 관리형)                             │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│   │  AWS MSK    │  │  Confluent  │  │    Aiven                │ │
│   │             │  │   Cloud     │  │                         │ │
│   └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**배포 환경별 비교**:

| 환경 | 장점 | 단점 | 적합한 케이스 |
|------|------|------|--------------|
| **자체 HW** | 완전한 제어, 예측 가능한 비용 | 하드웨어 관리 필요 | 숙련된 운영팀, 예측 가능한 워크로드 |
| **가상화** | 기존 인프라 활용 | SAN 성능 이슈 가능 | 기존 VM 인프라 활용 |
| **Kubernetes** | 자동화, 선언적 관리 | K8s 운영 역량 필요 | DevOps 문화, 클라우드 네이티브 |
| **Cloud Self-Managed** | 인프라 안정성 | 운영 책임 | 클라우드 인프라 활용 |
| **Managed Service** | 운영 부담 감소 | 비용, 제약사항 | 운영팀 부재, 빠른 시작 |

### 3.2 자체 하드웨어

자체 하드웨어에 Kafka를 배포할 때는 물리적 인프라 관리가 핵심입니다.

**고려사항**:

```
자체 하드웨어 체크리스트:
├─ 장애 대응
│   ├─ 하드웨어 장애 대응 계획 수립
│   ├─ 예비 부품 확보
│   └─ 장애 시 교체 프로세스 정의
│
├─ 확장성
│   ├─ 추가 브로커를 위한 랙 공간 확보
│   ├─ 네트워크 포트 여유 확보
│   └─ 전력/냉각 용량 계획
│
├─ 환경 분리
│   ├─ 개발/테스트/프로덕션 환경 분리
│   └─ 네트워크 세그먼트 분리
│
└─ 물리적 분리
    ├─ 브로커를 서로 다른 랙에 배치
    ├─ 화재 구획 분리 고려
    └─ 멀티 DC 시 지연 시간 < 30ms 유지
```

### 3.3 가상화 환경

VM 기반 가상화 환경에서 Kafka를 운영할 때는 스토리지 성능이 핵심 고려사항입니다.

**주의사항**:

| 항목 | 권장사항 |
|------|----------|
| **VM 호스트** | 브로커를 서로 다른 VM 호스트에 분산 |
| **스토리지** | SAN 성능 의심 시 로컬 SSD 권장 |
| **테스트** | 스토리지 시스템 부하 테스트 필수 |
| **Compaction** | 동시 Compaction 시 스토리지 과부하 주의 |

### 3.4 Kubernetes (Strimzi)

Strimzi는 Kubernetes에서 Kafka를 운영하기 위한 Operator 프로젝트입니다. Custom Resource Definition(CRD)을 통해 Kafka 리소스를 선언적으로 관리합니다.

**Strimzi 아키텍처**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Strimzi Architecture                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   Cluster Operator                        │   │
│  │   (Kafka CRD 감시, 클러스터 프로비저닝)                   │   │
│  └─────────────────────────┬────────────────────────────────┘   │
│                            │                                     │
│            ┌───────────────┼───────────────┐                    │
│            │               │               │                    │
│            ▼               ▼               ▼                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Kafka Broker │  │    Topic     │  │    User      │          │
│  │    Pods      │  │  Operator    │  │  Operator    │          │
│  │              │  │ (KafkaTopic  │  │ (KafkaUser   │          │
│  │ ┌──────────┐ │  │  CRD 관리)   │  │  CRD 관리)   │          │
│  │ │ Broker 1 │ │  └──────────────┘  └──────────────┘          │
│  │ │ Broker 2 │ │                                               │
│  │ │ Broker 3 │ │                                               │
│  │ └──────────┘ │                                               │
│  └──────────────┘                                               │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             Additional Components                         │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │Kafka Connect │  │Cruise Control│  │ Mirror Maker │    │   │
│  │  │   Cluster    │  │              │  │     2        │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Strimzi Operator 역할**:

| Operator | 역할 |
|----------|------|
| **Cluster Operator** | Kafka 클러스터 배포 및 관리, StatefulSet 생성 |
| **Topic Operator** | KafkaTopic CRD로 토픽 생성/삭제/설정 관리 |
| **User Operator** | KafkaUser CRD로 사용자/ACL 관리, TLS 인증서 자동 생성 |

**Anti-Affinity 설정** (브로커 분리):

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
spec:
  kafka:
    replicas: 3
    template:
      pod:
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchLabels:
                    strimzi.io/cluster: my-cluster
                topologyKey: kubernetes.io/hostname
```

이 설정은 동일한 클러스터의 브로커 Pod들이 서로 다른 노드에 배치되도록 강제합니다.

### 3.5 Managed Services

클라우드 관리형 Kafka 서비스는 운영 부담을 줄여주지만, 비용과 제약사항을 고려해야 합니다.

**주요 Managed Service 비교**:

| 서비스 | 특징 | 과금 방식 |
|--------|------|----------|
| **AWS MSK** | AWS VPC 네이티브 통합, EBS 스토리지 | 브로커 인스턴스 + 스토리지 |
| **Azure HDInsight** | Azure 생태계 통합 | 노드 시간당 |
| **Confluent Cloud** | 브로커 수 투명, 고급 기능 포함 | 처리량 기반 |
| **Aiven** | 멀티 클라우드, 자체 계정 배포 가능 | 노드당 |

**Managed Service 선택 시 고려사항**:

```
체크리스트:
├─ 비용
│   ├─ 데이터 볼륨 증가 시 비용 증가율
│   ├─ 네트워크 전송 비용 (VPC 피어링, Private Link)
│   └─ 숨겨진 비용 (스토리지, 스냅샷, 백업)
│
├─ 제약사항
│   ├─ 보존 기간 제한
│   ├─ 처리량 제한
│   ├─ 파티션 수 제한
│   └─ 커스텀 설정 가능 여부
│
├─ 네트워크
│   ├─ VNet Peering 지원
│   ├─ Private Link / PrivateLink 지원
│   └─ 멀티 리전 지원
│
└─ 기능
    ├─ KRaft 지원 여부
    ├─ 버전 업그레이드 정책
    └─ 모니터링 통합
```

---

## 4. 하드웨어 요구사항

### 4.1 브로커 (Brokers)

Kafka 브로커는 I/O 집약적 워크로드를 처리합니다. 올바른 하드웨어 선택이 성능의 핵심입니다.

**브로커 리소스 구성**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Broker Resource Planning                      │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐│
│  │   Storage   │  │    RAM      │  │   Network   │  │   CPU   ││
│  │   (SSD)     │  │(Page Cache) │  │  (≥1Gbps)   │  │         ││
│  │             │  │             │  │             │  │         ││
│  │ 12x1TB SSD  │  │ 6GB Heap +  │  │ 전용 NIC    │  │ Memory  ││
│  │ > 3x4TB SSD │  │ 나머지는    │  │ 브로커 간   │  │ 기반    ││
│  │             │  │ Page Cache  │  │ < 30ms      │  │ 산정    ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘│
└─────────────────────────────────────────────────────────────────┘
```

#### 스토리지

| 권장사항 | 이유 |
|----------|------|
| **SSD 권장** | Sequential I/O 성능 극대화 |
| **다중 소형 SSD** (12x1TB > 3x4TB) | 병렬 I/O 성능, 장애 시 영향 최소화 |
| **RAID 불필요** | Kafka 자체 복제로 내구성 확보 |
| **RAID 5/6 금지** | 쓰기 성능 저하, 복구 시 오버헤드 |
| **Tiered Storage** (Kafka 3.9+) | 오래된 데이터를 저렴한 스토리지로 이동 |

#### RAM

Kafka에서 RAM은 JVM Heap과 Page Cache로 나뉩니다.

**메모리 구성**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    32GB RAM 브로커 예시                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐                                        │
│  │   Kernel (~1GB)     │                                        │
│  ├─────────────────────┤                                        │
│  │   JVM Heap          │  ← 1GB ~ 6GB (대규모에서도 6GB 충분)   │
│  │   (최대 6GB)        │                                        │
│  ├─────────────────────┤                                        │
│  │                     │                                        │
│  │   Page Cache        │  ← OS가 자동 관리                      │
│  │   (~25GB)           │    Consumer Lag 커버                   │
│  │                     │    GC 없음, 재시작해도 유지            │
│  │                     │                                        │
│  └─────────────────────┘                                        │
└─────────────────────────────────────────────────────────────────┘
```

**Page Cache 산정 공식**:

```
필요 Page Cache = (시간당 데이터량 / 브로커 수) × 허용 Lag 시간

예시:
- 3개 브로커, 시간당 30GB 데이터 생성
- Consumer 최대 2시간 Lag 허용

계산:
- 브로커당 데이터: 30GB / 3 = 10GB/hour
- 필요 Page Cache: 10GB × 2시간 = 20GB
- 총 RAM: 6GB (Heap) + 20GB (Cache) = 26GB
- 권장: 32GB RAM
```

#### 네트워크

| 항목 | 권장 |
|------|------|
| **최소 대역폭** | 1 Gbit/s Ethernet |
| **네트워크 스토리지** | 전용 스토리지 네트워크 필요 |
| **브로커 간 지연** | < 30ms (동일 리전 내) |
| **멀티 리전** | 권장하지 않음 (지연 시간 문제) |

#### CPU

- **Memory-Optimized 인스턴스 권장**: Kafka는 CPU보다 I/O가 병목
- **작은 코어 다수 > 큰 코어 소수**: 병렬 처리에 유리
- RAM 기반으로 산정 (32GB RAM 기준 8코어 정도)

#### 브로커 크기 전략

```
적정 브로커 크기:
├─ 너무 큰 브로커
│   ├─ 장애 시 영향 범위가 큼
│   ├─ 복구 시간 증가
│   └─ 리밸런싱 부담 증가
│
├─ 너무 작은 브로커
│   ├─ JVM 오버헤드 비효율
│   ├─ 관리 복잡성 증가
│   └─ 파티션당 오버헤드 증가
│
└─ 권장 크기
    ├─ RAM: 32GB ~ 64GB
    ├─ Storage: 4TB ~ 12TB
    └─ 브로커 수: 최소 3개, 워크로드에 따라 확장
```

### 4.2 Rack Awareness

Kafka의 Rack Awareness 기능은 레플리카를 서로 다른 랙/가용 영역에 분산 배치합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Rack Awareness                                │
│                                                                  │
│   Data Center                                                    │
│   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│   │    Rack 1     │  │    Rack 2     │  │    Rack 3     │       │
│   │   (rack.id=1) │  │   (rack.id=2) │  │   (rack.id=3) │       │
│   │               │  │               │  │               │       │
│   │  ┌─────────┐  │  │  ┌─────────┐  │  │  ┌─────────┐  │       │
│   │  │Broker 1 │  │  │  │Broker 2 │  │  │  │Broker 3 │  │       │
│   │  │         │  │  │  │         │  │  │  │         │  │       │
│   │  │ Topic A │  │  │  │ Topic A │  │  │  │ Topic A │  │       │
│   │  │(Leader) │  │  │  │(Replica)│  │  │  │(Replica)│  │       │
│   │  └─────────┘  │  │  └─────────┘  │  │  └─────────┘  │       │
│   └───────────────┘  └───────────────┘  └───────────────┘       │
│                                                                  │
│   → 랙 1 전체 장애 시에도 데이터 가용성 유지                     │
└─────────────────────────────────────────────────────────────────┘
```

**설정 방법**:

```properties
# broker.properties
broker.rack=rack-1
```

**글로벌 운영 전략**:

| 구성 | 권장 여부 | 이유 |
|------|----------|------|
| 단일 리전 내 멀티 AZ | O | 지연 시간 < 30ms 유지 가능 |
| 멀티 리전 단일 클러스터 | X | 지연 시간 > 30ms, 성능 저하 |
| 리전별 독립 클러스터 + MirrorMaker | O | 각 리전 독립 운영, 복제로 데이터 동기화 |

### 4.3 조정 클러스터 (KRaft/ZooKeeper)

Kafka 클러스터의 메타데이터를 관리하는 조정(Coordination) 노드의 요구사항입니다.

**요구사항**:

| 항목 | 권장 |
|------|------|
| **RAM** | 4 ~ 8 GB |
| **CPU** | 중간 수준 |
| **Storage** | SSD (낮은 지연 시간) |
| **네트워크** | 낮은 지연 시간 필수 (특히 ZooKeeper) |
| **노드 수** | 홀수 (3개 또는 5개) |

**장애 허용 수**:

| 노드 수 | 장애 허용 | 쿼럼 |
|--------|----------|------|
| 3 | 1개 | 2개 |
| 5 | 2개 | 3개 |
| 7 | 3개 | 4개 |

---

## 5. Tiered Storage (Kafka 3.9+)

Tiered Storage는 Kafka 3.9에서 GA(General Availability)된 기능으로, 오래된 데이터를 저렴한 원격 스토리지(S3, GCS, Azure Blob 등)로 자동 이동합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tiered Storage Architecture                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Kafka Broker                           │   │
│  │                                                           │   │
│  │   Hot Tier (Local SSD)         Cold Tier (S3/Object)     │   │
│  │  ┌─────────────────────┐     ┌─────────────────────────┐ │   │
│  │  │   최신 세그먼트     │     │   오래된 세그먼트       │ │   │
│  │  │   (Active Segment)  │────▶│   (Remote Storage)      │ │   │
│  │  │                     │     │                         │ │   │
│  │  │   Segment 3 (현재)  │     │   Segment 0            │ │   │
│  │  │   Segment 2         │     │   Segment 1            │ │   │
│  │  └─────────────────────┘     └─────────────────────────┘ │   │
│  │                                         │                │   │
│  │                                         ▼                │   │
│  │                               필요 시 로컬로 fetch       │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│   장점:                                                          │
│   ├─ 무기한 데이터 보존 비용 효율화                              │
│   ├─ 로컬 스토리지 용량 절감                                     │
│   └─ 스케일 아웃 시 데이터 이동 최소화                           │
└─────────────────────────────────────────────────────────────────┘
```

**설정 예시**:

```properties
# broker.properties
remote.log.storage.system.enable=true
remote.log.storage.manager.class.name=org.apache.kafka.tiered.storage.s3.S3RemoteStorageManager
remote.log.storage.manager.class.path=/path/to/s3-storage-manager.jar

# S3 설정
remote.log.storage.s3.bucket=my-kafka-tiered-storage
remote.log.storage.s3.region=us-east-1
```

---

## 면접 예상 질문

### Q1: Kafka 프로덕션 환경에서 GUI 도구 사용 원칙은?

**모범 답변**:

프로덕션 환경에서 GUI 도구는 **읽기 전용**으로만 사용해야 합니다. GUI를 통한 토픽 생성, 설정 변경, 데이터 수정은 금지됩니다.

이유는 다음과 같습니다:

1. **변경 추적 불가**: GUI 변경은 Git 이력에 남지 않아 감사(Audit)가 어렵습니다
2. **자동화 방해**: GitOps 파이프라인과 충돌하여 상태 불일치가 발생합니다
3. **실수 가능성**: 클릭 한 번으로 프로덕션 토픽을 삭제할 수 있습니다

GUI는 모니터링, 디버깅, 메시지 조회 용도로만 사용하고, 모든 리소스 변경은 Git PR을 통해 진행해야 합니다. 또한 GUI는 전문 모니터링 도구(Prometheus, Grafana)를 대체할 수 없으므로, 알람과 대시보드는 별도로 구축해야 합니다.

---

### Q2: Cruise Control의 역할과 사용 시 주의사항은?

**모범 답변**:

Cruise Control은 LinkedIn에서 개발한 Kafka 클러스터 부하 분산 도구입니다.

**주요 기능**:
- **부하 모니터링**: 브로커별 CPU, RAM, Disk, Network 사용량 수집
- **부하 분석**: 설정된 Goals 기반으로 불균형 분석 및 재배치 제안
- **자동 재배치**: 브로커 추가/제거 시 파티션 자동 분산
- **자동 복구**: 브로커 장애 감지 시 자동 재배치

**주의사항**:
1. **피크 타임 피하기**: 파티션 이동은 네트워크와 디스크 I/O 부하가 높으므로, 트래픽이 적은 시간에 실행해야 합니다
2. **점진적 실행**: 대량 재배치는 한 번에 하지 않고 단계적으로 진행합니다
3. **모니터링 연계**: 재배치 중 클러스터 상태를 실시간 모니터링해야 합니다
4. **Goals 튜닝**: 기본 Goals는 범용적이므로, 워크로드 특성에 맞게 조정이 필요합니다

---

### Q3: Kafka 브로커의 RAM 구성과 Page Cache의 역할은?

**모범 답변**:

Kafka 브로커의 RAM은 **JVM Heap**과 **Page Cache** 두 영역으로 나뉩니다.

**JVM Heap**:
- 크기: 1GB ~ 6GB (대규모 클러스터에서도 6GB 이상 불필요)
- 역할: 메타데이터 관리, 요청 처리
- 주의: Heap을 크게 잡으면 GC 시간이 길어져 오히려 성능 저하

**Page Cache**:
- 크기: 나머지 RAM 전체 (32GB 브로커에서 약 25GB)
- 역할: 최근 읽고 쓴 데이터를 OS 레벨에서 캐싱
- 장점:
  - OS가 자동 관리하므로 GC 없음
  - 브로커 재시작해도 캐시 유지
  - 여러 Consumer가 캐시 공유

**Page Cache 산정**:
Consumer Lag 허용 시간을 기준으로 계산합니다. 예를 들어 시간당 30GB 데이터, 3개 브로커, 2시간 Lag 허용 시:
- 브로커당: 30GB / 3 = 10GB/hour
- 필요 Page Cache: 10GB × 2시간 = 20GB

---

### Q4: Strimzi에서 브로커를 서로 다른 노드에 배치하려면?

**모범 답변**:

Strimzi에서 브로커 Pod를 서로 다른 Kubernetes 노드에 배치하려면 **Pod Anti-Affinity**를 설정합니다.

```yaml
spec:
  kafka:
    replicas: 3
    template:
      pod:
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchLabels:
                    strimzi.io/cluster: my-cluster
                topologyKey: kubernetes.io/hostname
```

**설명**:
- `requiredDuringSchedulingIgnoredDuringExecution`: 스케줄링 시 반드시 충족 (Hard constraint)
- `labelSelector`: 같은 클러스터의 다른 브로커 Pod 식별
- `topologyKey: kubernetes.io/hostname`: 노드 단위로 분리

**고급 설정**:
- 가용 영역(AZ) 분리: `topologyKey: topology.kubernetes.io/zone`
- 랙 분리: `topologyKey: topology.kubernetes.io/rack`

이 설정으로 단일 노드 장애 시에도 클러스터 가용성을 유지할 수 있습니다.

---

### Q5: Managed Kafka 서비스 선택 시 고려사항은?

**모범 답변**:

Managed Kafka 서비스 선택 시 다음 항목을 평가해야 합니다:

**비용**:
- 데이터 볼륨 증가 시 비용 증가율 확인 (선형 vs 지수적)
- 네트워크 전송 비용 (VPC 피어링, Private Link)
- 숨겨진 비용: 스토리지, 스냅샷, 백업, 지원 비용

**제약사항**:
- 보존 기간 제한 (무기한 보존 가능 여부)
- 처리량/파티션 수 제한
- 커스텀 설정 가능 범위 (min.insync.replicas 등)
- Kafka 버전 업그레이드 정책

**네트워크**:
- VNet Peering / Private Link 지원
- 멀티 리전 복제 지원 (MirrorMaker)
- 온프레미스 연결 옵션

**기능**:
- KRaft 지원 여부
- Schema Registry, Connect 포함 여부
- 모니터링/알람 통합

Self-managed 대비 운영 부담은 줄지만, 워크로드가 커지면 비용이 급증할 수 있습니다. 따라서 현재 워크로드뿐 아니라 향후 성장을 고려한 비용 분석이 필요합니다.

---

### Q6: Kafka 클러스터의 글로벌 운영 전략은?

**모범 답변**:

Kafka 클러스터의 글로벌 운영은 **리전별 독립 클러스터 + MirrorMaker** 방식을 권장합니다.

**멀티 리전 단일 클러스터가 권장되지 않는 이유**:
- 브로커 간 지연 시간 30ms 초과 시 성능 저하
- 리더 선출, ISR 동기화에 지연 발생
- 네트워크 파티션 시 split-brain 위험

**권장 아키텍처**:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   US-East   │         │   EU-West   │         │   AP-Seoul  │
│   Cluster   │◀───────▶│   Cluster   │◀───────▶│   Cluster   │
│             │   MM2   │             │   MM2   │             │
└─────────────┘         └─────────────┘         └─────────────┘
```

**MirrorMaker 2 활용**:
- Active-Active: 양방향 복제, 각 리전이 로컬 Producer/Consumer 처리
- Active-Passive: 단방향 복제, DR(재해 복구) 용도
- Hub-and-Spoke: 중앙 클러스터로 데이터 집계

**설계 원칙**:
1. 각 리전 클러스터는 독립적으로 운영
2. 리전 간 데이터 동기화는 MirrorMaker 2로 비동기 복제
3. 애플리케이션은 가장 가까운 리전 클러스터에 연결
4. 글로벌 분석이 필요한 경우 중앙 분석 클러스터로 집계

---

### Q7: Tiered Storage의 장점과 사용 시나리오는?

**모범 답변**:

Tiered Storage는 Kafka 3.9에서 GA된 기능으로, 오래된 세그먼트를 원격 스토리지(S3, GCS 등)로 자동 이동합니다.

**장점**:
1. **비용 효율화**: 오래된 데이터를 저렴한 Object Storage로 이동
2. **무기한 보존**: 로컬 스토리지 제약 없이 데이터 보존 가능
3. **스케일 아웃 효율화**: 브로커 추가 시 기존 데이터 이동 불필요
4. **복구 시간 단축**: 로컬 스토리지 용량 감소로 브로커 복구 빨라짐

**사용 시나리오**:
- 규정 준수로 수년간 데이터 보존이 필요한 경우
- 과거 데이터 분석이 간헐적으로 필요한 경우
- 스토리지 비용 최적화가 중요한 대용량 환경

**주의사항**:
- Cold Tier 데이터 접근 시 지연 시간 증가
- 원격 스토리지 가용성에 의존
- 네트워크 비용 발생 (데이터 전송)

---

## 실무 체크리스트

### GitOps 리소스 관리

- [ ] 토픽/사용자/ACL 정의를 Git 저장소에 관리
- [ ] CI/CD 파이프라인으로 자동 배포 구성
- [ ] PR 리뷰 프로세스 정립
- [ ] GUI는 읽기 전용으로 제한

### Cruise Control 운영

- [ ] Cruise Control 배포 및 설정
- [ ] Goals 커스터마이징 (워크로드 특성 반영)
- [ ] 재배치 실행 시간대 정의 (피크 타임 제외)
- [ ] 재배치 모니터링 대시보드 구성

### 하드웨어 계획

- [ ] RAM: Consumer Lag 기반 Page Cache 산정
- [ ] Storage: SSD, 다중 디스크 구성
- [ ] Network: 최소 1Gbps, 브로커 간 지연 < 30ms
- [ ] Rack Awareness 설정

### 배포 환경

- [ ] 브로커 물리적 분리 (Anti-Affinity)
- [ ] 개발/테스트/프로덕션 환경 분리
- [ ] Managed Service 선택 시 비용/제약 분석
- [ ] 글로벌 운영 시 리전별 독립 클러스터 + MirrorMaker

### 조정 클러스터

- [ ] KRaft/ZooKeeper 노드 홀수 구성 (3개 또는 5개)
- [ ] 전용 하드웨어/VM 배치
- [ ] 낮은 네트워크 지연 시간 확보

---

## 참고 자료

- [kcat GitHub](https://github.com/edenhill/kcat)
- [Kafbat Kafka UI](https://github.com/kafbat/kafka-ui)
- [kcctl - Kafka Connect CLI](https://github.com/kcctl/kcctl)
- [Cruise Control for Apache Kafka](https://github.com/linkedin/cruise-control)
- [Strimzi Documentation](https://strimzi.io/documentation/)
- [Red Hat AMQ Streams](https://access.redhat.com/products/red-hat-amq-streams)
- [Confluent Cloud](https://www.confluent.io/confluent-cloud/)
- [Aiven for Apache Kafka](https://aiven.io/kafka)
