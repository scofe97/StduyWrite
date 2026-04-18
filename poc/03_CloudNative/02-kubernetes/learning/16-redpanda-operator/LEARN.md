# Ch16: Redpanda Operator로 Kafka 호환 클러스터 관리하기

> 📌 **핵심 요약**
>
> Redpanda는 Apache Kafka와 프로토콜 호환되면서도 JVM 없이 C++로 구현된 이벤트 스트리밍 플랫폼이다. ZooKeeper/KRaft 대신 내장 Raft 합의 알고리즘을 사용하고, Schema Registry와 HTTP Proxy(Pandaproxy)를 단일 바이너리에 포함하여 운영 복잡도를 크게 줄인다. Redpanda Operator는 Kubernetes에서 Redpanda 클러스터를 선언적으로 관리하며, Helm 차트와 조합하여 브로커, Console(웹 UI), Schema Registry를 한 번에 배포한다. Strimzi Kafka Operator와 비교하면 리소스 사용량이 적고 운영 구성 요소가 단순하지만, Kafka 생태계의 일부 고급 기능(Kafka Streams, ksqlDB)은 직접 지원하지 않는다. minikube 환경에서는 단일 브로커 + 제한된 메모리로도 학습 및 테스트가 가능하다.

---

## 🎯 학습 목표

이번 챕터를 마치면 다음을 할 수 있다:

1. Redpanda가 Kafka와 호환되면서 어떤 아키텍처적 차이를 가지는지 설명할 수 있다.
2. Redpanda Operator의 CRD(Redpanda, Topic 등)와 동작 원리를 이해할 수 있다.
3. Helm + Operator 조합으로 Redpanda 클러스터를 Kubernetes에 배포할 수 있다.
4. Strimzi Kafka Operator와 Redpanda Operator를 아키텍처, 리소스, 운영 측면에서 비교할 수 있다.
5. Redpanda Console(웹 UI)과 Schema Registry 내장의 장점을 설명할 수 있다.
6. minikube 환경에서 리소스 제약을 고려한 Redpanda 배포 전략을 수립할 수 있다.

---

## 📖 본문

### 1. Redpanda 소개: 왜 또 다른 스트리밍 플랫폼인가

Apache Kafka는 분산 이벤트 스트리밍의 사실상 표준이지만, 10년 이상의 역사를 가진 JVM 기반 시스템이다. Kafka를 운영하면서 반복적으로 등장하는 불만 사항은 다음과 같다:

- **JVM 튜닝 부담**: GC(Garbage Collection) 튜닝, Heap 크기 설정, G1GC vs ZGC 선택 등 Java 메모리 관리에 대한 전문 지식 필요.
- **ZooKeeper 의존성**: Kafka 3.x까지 ZooKeeper가 필수였고, KRaft 전환 중이지만 아직 마이그레이션 과정이 복잡.
- **다중 컴포넌트**: Kafka 브로커 + ZooKeeper/KRaft + Schema Registry + Kafka Connect + REST Proxy를 각각 배포하고 관리해야 함.
- **리소스 사용량**: JVM 기반이므로 브로커당 최소 1~2GB Heap + OS 페이지 캐시 메모리 필요.

Redpanda는 이러한 문제를 해결하기 위해 처음부터 C++로 재설계된 Kafka 호환 스트리밍 플랫폼이다. Vectorized(현 Redpanda Data)가 2020년에 출시했으며, Kafka 프로토콜을 완벽히 구현하여 기존 Kafka 클라이언트, Kafka Connect, MirrorMaker2를 코드 변경 없이 사용할 수 있다.

#### 1.1 Redpanda의 핵심 아키텍처

Redpanda의 설계 철학은 "단일 바이너리, 최소 의존성"이다. 핵심 특징은 다음과 같다:

**C++ + Seastar 프레임워크**:

Redpanda는 ScyllaDB에서 검증된 Seastar 비동기 프레임워크 위에 구축되었다. Seastar는 CPU 코어당 하나의 스레드를 할당하는 Thread-per-Core 모델을 사용한다. 이 모델에서 각 코어는 독립적으로 동작하며, 코어 간 공유 상태가 없으므로 락(lock)이 불필요하다. 이로 인해 다음과 같은 이점이 있다:

- **예측 가능한 레이턴시**: GC 일시 정지(Stop-the-World)가 없으므로 꼬리 지연(tail latency)이 안정적이다. Kafka에서 간헐적으로 발생하는 수백ms~수초의 GC 일시 정지가 Redpanda에는 없다.
- **높은 CPU 효율**: 락 경합(lock contention)이 없으므로 CPU 코어 수에 비례하여 처리량이 선형적으로 증가한다.
- **낮은 메모리 사용량**: JVM Heap이 필요 없으므로 같은 하드웨어에서 더 많은 메모리를 OS 페이지 캐시에 할당할 수 있다. 페이지 캐시는 디스크 I/O 성능에 직접적으로 영향을 미친다.

**내장 Raft 합의 알고리즘**:

Kafka는 메타데이터 관리를 위해 ZooKeeper(외부 분산 시스템)에 의존했고, KRaft(Kafka Raft)로 전환 중이다. Redpanda는 처음부터 자체 Raft 구현을 내장하여 외부 합의 시스템이 불필요하다. 각 파티션마다 독립적인 Raft 그룹이 존재하며, 리더 선출과 로그 복제가 파티션 단위로 이루어진다.

```
Kafka 아키텍처:
  Broker 1 ─┐
  Broker 2 ─┼─ ZooKeeper Ensemble (또는 KRaft Controller)
  Broker 3 ─┘
  + Schema Registry (별도 프로세스)
  + REST Proxy (별도 프로세스)

Redpanda 아키텍처:
  Broker 1 (Raft + Schema Registry + HTTP Proxy 내장)
  Broker 2 (Raft + Schema Registry + HTTP Proxy 내장)
  Broker 3 (Raft + Schema Registry + HTTP Proxy 내장)
  → 외부 의존성 없음
```

**단일 바이너리 (All-in-One)**:

Redpanda는 하나의 바이너리에 다음 기능을 모두 포함한다:

| 기능 | Kafka 생태계 | Redpanda |
|------|-------------|----------|
| 메시지 브로커 | Apache Kafka | 내장 |
| 메타데이터 관리 | ZooKeeper / KRaft | 내장 Raft |
| Schema Registry | Confluent Schema Registry (별도) | 내장 |
| HTTP Proxy (REST API) | Confluent REST Proxy (별도) | Pandaproxy (내장) |
| 웹 관리 UI | Confluent Control Center (유료) | Redpanda Console (무료) |

Schema Registry가 내장되어 있다는 것은 별도의 컨테이너를 배포, 모니터링, 스케일링할 필요가 없다는 의미이다. Kubernetes 환경에서 Pod 수가 줄어들고, 네트워크 홉이 감소하며, 리소스 오버헤드가 줄어든다. Testcontainers를 사용한 통합 테스트에서도 Redpanda 컨테이너 하나만 띄우면 Schema Registry까지 포함되므로 테스트 환경 구성이 단순해진다.

#### 1.2 Kafka와의 호환성

Redpanda는 Kafka 프로토콜(API)을 구현한 것이지, Kafka 코드를 포크한 것이 아니다. 이는 다음을 의미한다:

- **Kafka 클라이언트 호환**: Java, Go, Python, Node.js 등 모든 Kafka 클라이언트 라이브러리를 코드 변경 없이 사용할 수 있다. `bootstrap.servers` 주소만 변경하면 된다.
- **Kafka Connect 호환**: 기존 Kafka Connect 커넥터(Debezium, JDBC Sink 등)를 그대로 사용할 수 있다.
- **MirrorMaker2 호환**: Kafka 클러스터와 Redpanda 클러스터 간 데이터 미러링이 가능하다.
- **제한 사항**: Kafka Streams와 ksqlDB는 Kafka 내부 API에 의존하므로 Redpanda에서 직접 실행할 수 없다. 대안으로 Flink, Spark Structured Streaming 등을 사용한다.

---

### 2. Redpanda Operator 아키텍처

Redpanda Operator는 Kubernetes에서 Redpanda 클러스터를 선언적으로 관리하는 Operator이다. Helm 차트를 기반으로 동작하며, 사용자가 정의한 CR(Custom Resource)에 따라 StatefulSet, Service, ConfigMap을 자동으로 생성하고 관리한다.

#### 2.1 CRD(Custom Resource Definition)

Redpanda Operator는 다음 CRD를 제공한다:

**Redpanda CR**:

클러스터 전체를 정의하는 최상위 리소스이다. 브로커 수, 리소스 제한, 스토리지, 리스너, TLS, Schema Registry, Pandaproxy 설정을 포함한다.

```yaml
apiVersion: cluster.redpanda.com/v1alpha2
kind: Redpanda
metadata:
  name: redpanda-cluster
  namespace: redpanda
spec:
  chartRef: {}
  clusterSpec:
    statefulset:
      replicas: 3
    resources:
      cpu:
        cores: 1
      memory:
        container:
          max: 2Gi
        redpanda:
          memory: 1Gi
          reserveMemory: 200Mi
    storage:
      persistentVolume:
        enabled: true
        size: 10Gi
        storageClass: standard
    listeners:
      kafka:
        port: 9092
        tls:
          enabled: false
      schemaRegistry:
        port: 8081
      admin:
        port: 9644
      http:
        port: 8082
```

이 CR을 `kubectl apply`하면 Redpanda Operator가 다음을 자동 생성한다:

1. **StatefulSet**: 브로커 수만큼 Pod 생성. 각 Pod는 Redpanda 컨테이너를 실행하며, Pod 이름은 `redpanda-cluster-0`, `redpanda-cluster-1`, ... 형태.
2. **Service**: 부트스트랩 Service(ClusterIP)와 브로커별 Headless Service. 부트스트랩 주소는 `redpanda-cluster-kafka-bootstrap.redpanda.svc.cluster.local:9092`.
3. **ConfigMap**: `redpanda.yaml` 설정 파일. 리스너, 시드 서버, 메모리 설정 등이 포함.
4. **PersistentVolumeClaim**: 브로커당 PVC 생성. 데이터 디렉토리(`/var/lib/redpanda/data`)에 마운트.

**Topic CR**:

Redpanda Operator는 Topic CR을 통해 토픽을 선언적으로 관리할 수 있다. Strimzi의 KafkaTopic CR과 유사한 개념이다.

```yaml
apiVersion: cluster.redpanda.com/v1alpha2
kind: Topic
metadata:
  name: my-topic
  namespace: redpanda
spec:
  partitions: 3
  replicationFactor: 3
  additionalConfig:
    retention.ms: "604800000"
    cleanup.policy: "delete"
  kafkaApiSpec:
    brokers:
      - "redpanda-cluster-0.redpanda-cluster.redpanda.svc.cluster.local:9092"
```

#### 2.2 Operator 동작 원리

Redpanda Operator는 Helm 기반 Operator라는 독특한 접근 방식을 취한다. 이는 Operator SDK의 Helm 모드를 활용한 것으로, 동작 흐름은 다음과 같다:

```
사용자 → kubectl apply Redpanda CR
  → Operator Watch 감지
  → Redpanda CR의 spec을 Helm values로 변환
  → Helm 차트 렌더링 (StatefulSet, Service, ConfigMap 등)
  → Kubernetes API에 리소스 생성/업데이트
  → Reconciliation Loop (desired state ↔ actual state 지속 비교)
```

이 방식의 장점은 다음과 같다:

- **Helm 차트 재사용**: 독립적으로 `helm install`로 배포할 수도 있고, Operator를 통해 CR로 관리할 수도 있다. 두 방식이 같은 Helm 차트를 공유한다.
- **업그레이드 간편**: Helm 차트 버전을 올리면 Operator가 자동으로 Rolling Update를 수행한다.
- **커스터마이즈 가능**: `spec.clusterSpec`은 사실상 Helm values 구조와 동일하므로, Helm 차트의 모든 옵션을 CR에서 설정할 수 있다.

#### 2.3 Strimzi vs Redpanda Operator 구성 요소

두 Operator의 구성 요소 차이를 이해하면 운영 복잡도를 비교할 수 있다:

```
Strimzi 구성:
  Cluster Operator (Deployment, 1개)
  Entity Operator (Deployment, Kafka 클러스터당 1개)
    ├── Topic Operator (컨테이너)
    └── User Operator (컨테이너)
  Kafka 브로커 (StatefulSet)
  KRaft 컨트롤러 또는 ZooKeeper (StatefulSet)
  → 최소 5개 Pod (Operator 1 + Entity 1 + Broker 1 + Controller/ZK 1)

Redpanda Operator 구성:
  Redpanda Operator (Deployment, 1개)
  Redpanda 브로커 (StatefulSet, Raft 내장)
  Redpanda Console (Deployment, 선택사항)
  → 최소 2개 Pod (Operator 1 + Broker 1)
```

---

### 3. Helm + Operator 조합 배포

Redpanda는 두 가지 배포 방식을 제공한다. Helm만 사용하는 방식과 Operator + CR 방식이다. 실무에서는 Operator를 먼저 설치한 뒤 Redpanda CR로 클러스터를 관리하는 방식을 권장한다.

#### 3.1 Operator 설치

```bash
# Redpanda Helm 저장소 추가
helm repo add redpanda https://charts.redpanda.com
helm repo update

# Operator 설치 (CRD 포함)
helm install redpanda-operator redpanda/operator \
  --namespace redpanda \
  --create-namespace
```

Operator가 설치되면 다음이 생성된다:

- `redpanda-operator` Deployment (Operator Pod)
- Redpanda CRD (`redpandas.cluster.redpanda.com`)
- Topic CRD (`topics.cluster.redpanda.com`)
- ClusterRole, ClusterRoleBinding (Operator가 리소스를 관리할 권한)

#### 3.2 Redpanda 클러스터 배포 (CR 방식)

```yaml
# redpanda-cluster.yaml
apiVersion: cluster.redpanda.com/v1alpha2
kind: Redpanda
metadata:
  name: redpanda
  namespace: redpanda
spec:
  chartRef: {}
  clusterSpec:
    statefulset:
      replicas: 3
    resources:
      cpu:
        cores: 1
      memory:
        container:
          max: 2560Mi
        redpanda:
          memory: 2Gi
          reserveMemory: 200Mi
    storage:
      persistentVolume:
        enabled: true
        size: 20Gi
    listeners:
      kafka:
        port: 9092
      schemaRegistry:
        port: 8081
        enabled: true
      admin:
        port: 9644
      http:
        port: 8082
        enabled: true
    console:
      enabled: true
    tls:
      enabled: false
```

```bash
kubectl apply -f redpanda-cluster.yaml
```

적용 후 Operator의 Reconciliation Loop가 다음 순서로 리소스를 생성한다:

1. ConfigMap (`redpanda` 설정 파일)
2. StatefulSet (브로커 Pod)
3. Service (부트스트랩 + Headless)
4. PVC (브로커당 영구 볼륨)
5. Console Deployment (웹 UI, `console.enabled: true`일 때)

#### 3.3 Helm만 사용하는 방식 (Operator 없이)

Operator 없이 Helm만으로도 배포할 수 있다. 이 방식은 Operator의 Reconciliation Loop가 없으므로 Day-2 운영(스케일링, 롤링 업데이트)을 수동으로 관리해야 한다.

```bash
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --create-namespace \
  --set statefulset.replicas=3 \
  --set resources.cpu.cores=1 \
  --set resources.memory.container.max=2560Mi \
  --set storage.persistentVolume.enabled=true \
  --set storage.persistentVolume.size=20Gi \
  --set console.enabled=true
```

**언제 Helm만 사용하는가**:

- CI/CD 파이프라인에서 Helm으로 직접 배포하고, GitOps(Argo CD)로 관리할 때.
- Operator의 추가 리소스(Operator Pod, CRD)를 최소화하고 싶을 때.
- 단일 클러스터만 운영하고, 자동 복구가 필수가 아닐 때.

**언제 Operator를 사용하는가**:

- 하나의 Kubernetes 클러스터에 여러 Redpanda 클러스터를 운영할 때.
- Operator의 Reconciliation으로 설정 드리프트를 자동 복구하고 싶을 때.
- Topic CR 등 세밀한 선언적 관리가 필요할 때.

---

### 4. Strimzi Kafka Operator와 비교

Ch11에서 Strimzi Kafka Operator를 다루었다. Redpanda Operator와 비교하면 아키텍처, 리소스, 운영 편의성에서 유의미한 차이가 있다.

#### 4.1 아키텍처 비교

| 항목 | Strimzi (Apache Kafka) | Redpanda Operator |
|------|------------------------|-------------------|
| **언어/런타임** | Java (JVM) | C++ (Seastar) |
| **메타데이터 관리** | ZooKeeper → KRaft 전환 중 | 내장 Raft (처음부터) |
| **Schema Registry** | 별도 배포 (Confluent/Apicurio) | 내장 |
| **REST Proxy** | 별도 배포 (Confluent REST Proxy) | Pandaproxy (내장) |
| **웹 UI** | 별도 (Kafka UI, AKHQ 등) | Redpanda Console (공식) |
| **Operator 구조** | Cluster + Entity(Topic+User) Operator | 단일 Operator |
| **CRD 수** | 10+ (Kafka, KafkaTopic, KafkaUser, KafkaConnect, ...) | 2~3 (Redpanda, Topic) |
| **최소 Pod 수 (1 broker)** | 3~4 (Operator + Entity + Broker + ZK/Controller) | 2 (Operator + Broker) |

#### 4.2 리소스 사용량 비교

Redpanda가 C++ 네이티브 바이너리인 점은 리소스 사용량에 직접적인 영향을 미친다:

**메모리**:

- **Kafka**: JVM Heap(기본 1~4GB) + OS 페이지 캐시. Heap이 클수록 GC 일시 정지 시간도 증가할 수 있다. 프로덕션에서 브로커당 6~8GB 권장.
- **Redpanda**: JVM Heap이 없으므로 전체 메모리를 애플리케이션 로직과 페이지 캐시에 사용한다. `memory.redpanda.memory`로 Redpanda가 사용할 메모리를 명시적으로 설정하고, `reserveMemory`로 OS에 여유 메모리를 남긴다. 프로덕션에서 브로커당 2~4GB로 시작 가능.

**CPU**:

- **Kafka**: JVM은 GC, JIT 컴파일, 스레드 스케줄링에 CPU를 사용한다. CPU 코어 수 증가 시 GC 스레드도 증가하여 오버헤드 발생 가능.
- **Redpanda**: Thread-per-Core 모델로 CPU 코어에 1:1 매핑. 코어 수에 비례하여 처리량이 선형 증가. 코어 간 컨텍스트 스위칭과 락 경합이 없다.

**디스크**:

두 시스템 모두 세그먼트 파일 기반으로 데이터를 저장하므로 디스크 I/O 패턴은 유사하다. Redpanda는 추가로 Tiered Storage(S3, GCS)를 지원하여 로컬 디스크 사용량을 줄일 수 있다.

#### 4.3 운영 편의성 비교

| 항목 | Strimzi | Redpanda Operator |
|------|---------|-------------------|
| **배포 복잡도** | 높음 (Operator + ZK/KRaft + 브로커 + 부가 서비스) | 낮음 (Operator + 브로커 = All-in-One) |
| **설정 파일 수** | 많음 (server.properties, zookeeper.properties, ...) | 적음 (redpanda.yaml 1개) |
| **Rolling Update** | Cluster Operator가 StatefulSet 순차 업데이트 | Operator + Helm이 순차 업데이트 |
| **토픽 관리** | KafkaTopic CR (Topic Operator) | Topic CR |
| **사용자 관리** | KafkaUser CR (User Operator) | rpk acl 또는 Kafka ACL API |
| **모니터링** | JMX → Prometheus Exporter 필요 | 네이티브 Prometheus 엔드포인트 (`/metrics`) |
| **GC 튜닝** | 필수 (G1GC, ZGC 선택, Heap 크기) | 불필요 (GC 없음) |
| **커뮤니티/성숙도** | CNCF Sandbox, 6년+, 대규모 프로덕션 사례 다수 | 상대적으로 신생 (2020~), 빠르게 성장 중 |

#### 4.4 선택 가이드

**Strimzi를 선택하는 경우**:

- Kafka Streams, ksqlDB 등 Kafka 네이티브 스트림 처리가 필요할 때.
- Confluent Platform 에코시스템(Schema Registry, Connectors)을 이미 사용하고 있을 때.
- 대규모 프로덕션에서 검증된 안정성이 최우선일 때.
- CNCF 생태계 호환성과 커뮤니티 지원이 중요할 때.

**Redpanda를 선택하는 경우**:

- JVM 튜닝 없이 단순한 운영을 원할 때.
- 리소스 효율성이 중요할 때 (클라우드 비용 절감).
- Schema Registry, REST Proxy를 별도로 배포하고 싶지 않을 때.
- 낮은 꼬리 지연(tail latency)이 중요한 실시간 처리 시스템일 때.
- Kubernetes에서 최소 구성 요소로 이벤트 스트리밍을 시작하고 싶을 때.

---

### 5. Redpanda Console (웹 UI) 배포

Redpanda Console은 Redpanda(및 Kafka) 클러스터를 시각적으로 관리하는 웹 UI이다. Confluent Control Center의 오픈소스 대안이라 할 수 있다.

#### 5.1 Console의 주요 기능

- **토픽 관리**: 토픽 목록, 파티션 상태, 메시지 브라우징(Produce/Consume), 설정 변경.
- **컨슈머 그룹**: 그룹별 오프셋 확인, 랙(lag) 모니터링, 그룹 리셋.
- **Schema Registry**: 스키마 목록, 버전 관리, 호환성 검사 결과 확인.
- **ACL 관리**: 접근 제어 목록 조회 및 편집.
- **브로커 상태**: 브로커별 파티션 분포, 디스크 사용량, 네트워크 I/O.

#### 5.2 Console 배포 방법

Redpanda Helm 차트에서 `console.enabled: true`를 설정하면 Console이 자동 배포된다. 별도의 Helm 차트(`redpanda/console`)로도 설치할 수 있다.

```yaml
# Redpanda CR에 Console 포함
spec:
  clusterSpec:
    console:
      enabled: true
```

또는 독립적으로:

```bash
helm install redpanda-console redpanda/console \
  --namespace redpanda \
  --set console.config.kafka.brokers={"redpanda-0.redpanda.redpanda.svc.cluster.local:9092"} \
  --set console.config.kafka.schemaRegistry.enabled=true \
  --set console.config.kafka.schemaRegistry.urls={"http://redpanda-0.redpanda.redpanda.svc.cluster.local:8081"}
```

#### 5.3 Console 접근

minikube에서 Console에 접근하려면 `kubectl port-forward`를 사용한다:

```bash
# Console Service 확인
kubectl get svc -n redpanda | grep console

# 포트 포워딩
kubectl port-forward svc/redpanda-console -n redpanda 8080:8080

# 브라우저에서 http://localhost:8080 접근
```

Console은 Kafka 호환 클러스터(Strimzi Kafka 포함)에도 연결할 수 있으므로, Kafka UI가 필요한 경우 Redpanda Console을 독립적으로 사용하는 것도 가능하다.

---

### 6. Schema Registry 내장의 장점

Kafka 생태계에서 Schema Registry는 메시지 스키마(Avro, Protobuf, JSON Schema)를 중앙에서 관리하는 서비스이다. 프로듀서와 컨슈머가 스키마 ID로 직렬화/역직렬화하므로, 메시지에 스키마 전체를 포함하지 않아도 되어 메시지 크기가 줄어들고 스키마 진화(evolution)를 제어할 수 있다.

#### 6.1 외부 Schema Registry의 운영 부담

Confluent Schema Registry를 Kafka와 별도로 운영하면 다음 부담이 발생한다:

1. **별도 배포**: Schema Registry용 Deployment, Service, ConfigMap을 작성하고 관리해야 한다.
2. **별도 모니터링**: Schema Registry의 메트릭(요청 수, 레이턴시, 에러율)을 수집하고 대시보드를 구성해야 한다.
3. **별도 스케일링**: 요청량이 증가하면 Schema Registry Pod를 수평 확장해야 한다.
4. **네트워크 홉**: 프로듀서 → Schema Registry(스키마 조회) → Kafka 브로커(메시지 전송)로 네트워크 홉이 추가된다.
5. **버전 호환성**: Schema Registry와 Kafka 버전 간 호환성을 확인해야 한다.

#### 6.2 Redpanda 내장 Schema Registry

Redpanda의 Schema Registry는 브로커 프로세스에 내장되어 있다. 별도의 프로세스나 컨테이너가 아닌, Redpanda 브로커의 일부로 동작한다.

- **배포**: 추가 설정 없이 `schemaRegistry.port: 8081`만 설정하면 자동 활성화. 별도의 Pod/Service 불필요.
- **스토리지**: 스키마는 `_schemas` 내부 토픽에 저장된다. 브로커의 Raft 복제를 통해 자동으로 복제되므로 별도의 스토리지 설정 불필요.
- **가용성**: 브로커가 살아있으면 Schema Registry도 살아있다. 브로커 3대면 Schema Registry도 3중 가용성.
- **성능**: 로컬 프로세스 호출이므로 네트워크 레이턴시 제로. 별도 TCP 연결 불필요.
- **API 호환**: Confluent Schema Registry REST API와 100% 호환. 기존 Kafka 클라이언트의 `schema.registry.url`만 변경하면 된다.

```bash
# Redpanda Schema Registry 테스트
# 스키마 등록
curl -X POST http://localhost:8081/subjects/my-topic-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{\"type\": \"record\", \"name\": \"User\", \"fields\": [{\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"age\", \"type\": \"int\"}]}"}'

# 스키마 조회
curl http://localhost:8081/subjects/my-topic-value/versions/latest
```

Testcontainers를 활용한 통합 테스트에서도 Redpanda의 장점이 드러난다:

```java
// Kafka + Confluent Schema Registry = 컨테이너 2개 필요
KafkaContainer kafka = new KafkaContainer(...);
GenericContainer<?> schemaRegistry = new GenericContainer<>("confluentinc/cp-schema-registry:7.5.0")
    .dependsOn(kafka)
    .withEnv("SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS", kafka.getBootstrapServers());

// Redpanda = 컨테이너 1개로 Schema Registry 포함
RedpandaContainer redpanda = new RedpandaContainer("redpandadata/redpanda:v24.1.1");
String schemaRegistryUrl = redpanda.getSchemaRegistryAddress(); // 내장!
```

---

### 7. 프로덕션 운영

#### 7.1 토픽 관리

Redpanda에서 토픽을 관리하는 방법은 세 가지이다:

**1. Topic CR (선언적)**:

```yaml
apiVersion: cluster.redpanda.com/v1alpha2
kind: Topic
metadata:
  name: orders
  namespace: redpanda
spec:
  partitions: 6
  replicationFactor: 3
  additionalConfig:
    retention.ms: "604800000"       # 7일
    cleanup.policy: "compact,delete"
    min.insync.replicas: "2"
```

**2. rpk CLI (명령형)**:

`rpk`는 Redpanda 전용 CLI 도구로, `kafka-topics.sh`를 대체한다. 더 직관적인 인터페이스를 제공한다.

```bash
# 토픽 생성
rpk topic create orders -p 6 -r 3

# 토픽 목록
rpk topic list

# 토픽 상세 정보
rpk topic describe orders

# 메시지 생산
echo '{"orderId": "123", "amount": 1000}' | rpk topic produce orders

# 메시지 소비
rpk topic consume orders --offset start
```

**3. Kafka CLI (호환)**:

기존 Kafka CLI도 그대로 사용할 수 있다:

```bash
kafka-topics.sh --bootstrap-server redpanda:9092 --create --topic orders --partitions 6 --replication-factor 3
```

#### 7.2 모니터링

Redpanda는 네이티브 Prometheus 메트릭 엔드포인트를 제공한다. JMX Exporter 없이도 `/metrics` 엔드포인트에서 직접 메트릭을 수집할 수 있다.

```bash
# Prometheus 메트릭 확인
curl http://redpanda-0.redpanda.redpanda.svc.cluster.local:9644/metrics
```

**주요 메트릭**:

| 메트릭 | 설명 |
|--------|------|
| `redpanda_kafka_request_latency_seconds` | Kafka API 요청 레이턴시 |
| `redpanda_kafka_request_bytes_total` | 요청/응답 바이트 수 |
| `redpanda_cluster_topics` | 토픽 수 |
| `redpanda_cluster_partitions` | 파티션 수 |
| `redpanda_storage_disk_total_bytes` | 디스크 전체 용량 |
| `redpanda_storage_disk_free_bytes` | 디스크 여유 용량 |
| `redpanda_raft_leadership_changes` | 리더 변경 횟수 (높으면 불안정) |
| `redpanda_schema_registry_requests_total` | Schema Registry 요청 수 |

Prometheus ServiceMonitor 또는 PodMonitor를 생성하여 kube-prometheus-stack과 통합한다:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: redpanda-metrics
  namespace: redpanda
  labels:
    release: kube-prometheus
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: redpanda
  endpoints:
    - port: admin
      path: /public_metrics
      interval: 30s
```

Kafka에서는 JMX → Prometheus JMX Exporter → Prometheus 경로를 거쳐야 메트릭을 수집할 수 있다. Strimzi에서는 `spec.kafka.metricsConfig`로 JMX Exporter를 설정한다. Redpanda는 이 중간 단계가 불필요하므로 모니터링 구성이 단순하다.

#### 7.3 스케일링

**수평 스케일링 (브로커 추가/제거)**:

```yaml
# Redpanda CR에서 replicas 변경
spec:
  clusterSpec:
    statefulset:
      replicas: 5  # 3 → 5
```

`kubectl apply`하면 Operator가 StatefulSet의 replicas를 변경하고, 새 브로커 Pod가 생성된다. 기존 파티션은 자동으로 새 브로커에 재분배되지 않는다. 파티션 재분배는 수동으로 수행해야 한다:

```bash
# rpk으로 파티션 재분배
rpk cluster partitions move --from 0,1,2 --to 0,1,2,3,4

# 또는 Redpanda Console에서 시각적으로 재분배
```

**수직 스케일링 (리소스 변경)**:

```yaml
spec:
  clusterSpec:
    resources:
      cpu:
        cores: 2      # 1 → 2
      memory:
        container:
          max: 4Gi     # 2560Mi → 4Gi
        redpanda:
          memory: 3Gi  # 2Gi → 3Gi
```

리소스 변경 시 Operator가 Rolling Update를 수행하여 한 번에 한 브로커씩 재시작한다. 복제 계수가 2 이상이면 데이터 손실 없이 업데이트된다.

---

### 8. minikube 환경에서의 리소스 전략

minikube는 단일 노드 Kubernetes이므로 리소스가 제한적이다. Redpanda를 minikube에서 실행하려면 다음 전략을 사용한다.

#### 8.1 최소 구성

```yaml
apiVersion: cluster.redpanda.com/v1alpha2
kind: Redpanda
metadata:
  name: redpanda
  namespace: redpanda
spec:
  chartRef: {}
  clusterSpec:
    statefulset:
      replicas: 1                    # 단일 브로커
    resources:
      cpu:
        cores: 1                     # 1 코어
      memory:
        container:
          max: 1536Mi                # 컨테이너 전체 1.5GB
        redpanda:
          memory: 1Gi                # Redpanda에 1GB 할당
          reserveMemory: 200Mi       # OS에 200MB 예약
    storage:
      persistentVolume:
        enabled: true
        size: 5Gi                    # 최소 디스크
        storageClass: standard       # minikube 기본
    listeners:
      kafka:
        port: 9092
      schemaRegistry:
        port: 8081
        enabled: true
      admin:
        port: 9644
      http:
        port: 8082
        enabled: true
    console:
      enabled: true
    tuning:
      tune_aio_events: false         # minikube에서 AIO 튜닝 비활성화
      tune_clocksource: false
      tune_swappiness: false
      ballast_file_size: "0"
```

#### 8.2 minikube 시작 설정

```bash
# Redpanda를 위한 minikube 설정 (최소)
minikube start \
  --cpus=4 \
  --memory=6144 \
  --disk-size=30g \
  --driver=docker

# 또는 기존 minikube에서 리소스 확인
minikube status
kubectl top nodes
```

Redpanda 단일 브로커 + Console을 실행하면 약 2~2.5GB 메모리를 사용한다. minikube에 다른 워크로드(Prometheus, Grafana 등)도 함께 실행하려면 6~8GB 메모리를 할당해야 한다.

#### 8.3 단일 브로커의 한계

| 항목 | 단일 브로커 | 3 브로커 (프로덕션) |
|------|------------|-------------------|
| **복제 계수** | 최대 1 (데이터 손실 위험) | 최대 3 (고가용성) |
| **파티션 분산** | 모든 파티션이 1개 브로커에 집중 | 파티션이 브로커에 분산 |
| **장애 복구** | 브로커 다운 = 전체 서비스 중단 | 1~2대 다운해도 서비스 유지 |
| **Raft 합의** | 리더 선출 없음 (자기 자신) | 3노드 Raft 합의 동작 |
| **용도** | 개발, 학습, 테스트 | 프로덕션 |

#### 8.4 minikube에서의 접근 방법

```bash
# Kafka 부트스트랩 주소 (Port Forward)
kubectl port-forward svc/redpanda -n redpanda 9092:9092 &

# Schema Registry
kubectl port-forward svc/redpanda -n redpanda 8081:8081 &

# Console (웹 UI)
kubectl port-forward svc/redpanda-console -n redpanda 8080:8080 &

# rpk CLI로 클러스터 상태 확인
kubectl exec -it redpanda-0 -n redpanda -- rpk cluster info
kubectl exec -it redpanda-0 -n redpanda -- rpk topic list
```

---

### 9. Strimzi에서 Redpanda로 마이그레이션

기존에 Strimzi로 Kafka를 운영하고 있다면, Redpanda로 마이그레이션하는 방법은 다음과 같다.

#### 9.1 마이그레이션 전략

Redpanda는 Kafka 프로토콜을 구현하므로, MirrorMaker2를 사용한 온라인 마이그레이션이 가능하다:

```
기존 Kafka 클러스터 (Strimzi)
  ↓ MirrorMaker2 (실시간 복제)
Redpanda 클러스터 (신규)
  ↑
클라이언트 전환 (bootstrap.servers 변경)
```

1. Redpanda 클러스터를 새로 배포한다.
2. MirrorMaker2를 구성하여 Kafka → Redpanda로 토픽과 메시지를 실시간 복제한다.
3. 컨슈머를 먼저 Redpanda로 전환한다 (양쪽에서 읽기 가능).
4. 프로듀서를 Redpanda로 전환한다.
5. 복제 래그가 0이 되면 MirrorMaker2를 중단하고 기존 Kafka 클러스터를 제거한다.

#### 9.2 변경이 필요한 설정

| 항목 | Strimzi (Kafka) | Redpanda | 변경 필요 여부 |
|------|-----------------|----------|----------------|
| `bootstrap.servers` | `kafka-bootstrap:9092` | `redpanda:9092` | ✅ 변경 |
| `schema.registry.url` | `http://schema-registry:8081` | `http://redpanda:8081` | ✅ 변경 |
| Kafka 클라이언트 코드 | 그대로 | 그대로 | ❌ 변경 불필요 |
| Avro/Protobuf 스키마 | 그대로 | 그대로 | ❌ 변경 불필요 |
| Kafka Connect 커넥터 | 그대로 | 그대로 | ❌ 변경 불필요 |

---

### 10. 정리: Redpanda Operator 핵심 명령어

```bash
# === Operator 설치 ===
helm repo add redpanda https://charts.redpanda.com
helm repo update
helm install redpanda-operator redpanda/operator -n redpanda --create-namespace

# === 클러스터 배포 ===
kubectl apply -f redpanda-cluster.yaml

# === 상태 확인 ===
kubectl get redpanda -n redpanda
kubectl get pods -n redpanda
kubectl get svc -n redpanda
kubectl get topics -n redpanda

# === rpk CLI (Pod 내부) ===
kubectl exec -it redpanda-0 -n redpanda -- rpk cluster info
kubectl exec -it redpanda-0 -n redpanda -- rpk topic list
kubectl exec -it redpanda-0 -n redpanda -- rpk topic create my-topic -p 3 -r 1
kubectl exec -it redpanda-0 -n redpanda -- rpk topic describe my-topic
kubectl exec -it redpanda-0 -n redpanda -- rpk cluster health

# === 메시지 송수신 ===
kubectl exec -it redpanda-0 -n redpanda -- rpk topic produce my-topic
kubectl exec -it redpanda-0 -n redpanda -- rpk topic consume my-topic --offset start

# === Schema Registry ===
kubectl exec -it redpanda-0 -n redpanda -- \
  curl http://localhost:8081/subjects

# === 포트 포워딩 ===
kubectl port-forward svc/redpanda -n redpanda 9092:9092       # Kafka
kubectl port-forward svc/redpanda -n redpanda 8081:8081       # Schema Registry
kubectl port-forward svc/redpanda-console -n redpanda 8080:8080 # Console UI

# === 로그 확인 ===
kubectl logs redpanda-0 -n redpanda
kubectl logs -l app.kubernetes.io/name=redpanda-operator -n redpanda

# === 정리 ===
kubectl delete redpanda redpanda -n redpanda
helm uninstall redpanda-operator -n redpanda
```

---

### 참고 자료

- [Redpanda 공식 문서](https://docs.redpanda.com/)
- [Redpanda Operator for Kubernetes](https://docs.redpanda.com/current/deploy/deployment-option/self-hosted/kubernetes/)
- [Redpanda Helm Charts](https://github.com/redpanda-data/helm-charts)
- [Redpanda vs Kafka 벤치마크](https://redpanda.com/blog/kafka-vs-redpanda-performance-benchmark)
- [Strimzi 공식 문서](https://strimzi.io/documentation/) (비교 참조)
- [Ch11: Strimzi Kafka Operator](../11-kafka-operator/LEARN.md) (이전 챕터 참조)
