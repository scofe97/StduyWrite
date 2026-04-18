# Ch11: Strimzi Kafka Operator 점검 질문

## Q1: Strimzi의 Cluster/Entity/Topic/User Operator 각각의 역할

**질문**: Strimzi의 4개 Operator(Cluster, Entity, Topic, User)는 각각 어떤 리소스를 관리하며, 어떻게 협력하는가? 왜 하나의 Operator로 통합하지 않았는가?

**핵심 포인트**:

- **Cluster Operator**: Kafka 클러스터 전체 생명주기 관리. Kafka CR을 감시하고 StatefulSet, Service, ConfigMap, PVC를 생성/업데이트/삭제. KafkaConnect, KafkaMirrorMaker2, KafkaBridge CR도 관리. Cluster-scoped이며, 여러 Namespace를 감시할 수 있음(`watchNamespaces` 설정).
- **Entity Operator**: Topic Operator와 User Operator를 단일 Pod에서 실행. Cluster Operator가 Kafka CR을 배포할 때 Entity Operator Deployment도 자동 생성. Namespace-scoped이며, Kafka 클러스터당 1개 Entity Operator Pod 실행.
- **Topic Operator**: KafkaTopic CR을 감시하고 Kafka Admin API(`AdminClient`)로 토픽 생성/수정/삭제. 양방향 동기화 - CR 변경 → Kafka 반영, Kafka 토픽 변경 → CR 상태 업데이트. `kafka-topics.sh`로 직접 토픽을 생성하면 Topic Operator가 이를 감지하고 CR 생성 시도(충돌 가능).
- **User Operator**: KafkaUser CR을 감시하고 사용자 인증(SCRAM-SHA-512, TLS mTLS) 및 ACL(Access Control List) 설정. SCRAM 사용자 생성 시 비밀번호를 Secret으로 저장. ACL은 Kafka 내부 `kafka-acls` 명령으로 설정.
- **분리 이유**: (1) 관심사 분리 - Cluster Operator는 인프라(Pod, Service), Topic/User Operator는 애플리케이션 리소스(토픽, 사용자), (2) 권한 분리 - Cluster Operator는 ClusterRole 필요, Topic/User Operator는 Role만 필요, (3) 스케일링 - Kafka 클러스터 100개가 있어도 Cluster Operator는 1개, Entity Operator는 100개(클러스터당 1개).
- **협력 방식**: Cluster Operator가 Kafka CR의 `spec.entityOperator` 섹션을 읽고 Entity Operator Deployment 생성. Entity Operator는 같은 Namespace의 KafkaTopic/KafkaUser CR만 감시. `labels.strimzi.io/cluster`로 어떤 Kafka 클러스터에 속하는지 판단.

**심화 질문**: Topic Operator를 비활성화하고 `kafka-topics.sh`로 직접 토픽을 관리하면 어떤 문제가 발생하는가? GitOps 워크플로우에서 어떤 장단점이 있는가?

---

## Q2: KRaft 모드와 ZooKeeper 모드의 차이 (Kafka 4.0 방향)

**질문**: Kafka 4.0부터 KRaft가 기본이 되는 이유는 무엇인가? ZooKeeper 모드와 비교하여 KRaft의 기술적 장점과 마이그레이션 과정은 어떻게 되는가?

**핵심 포인트**:

- **ZooKeeper의 한계**: (1) 파티션 수 제한 - ZooKeeper는 메모리에 모든 메타데이터를 저장하므로 약 20만 파티션이 한계. 대규모 멀티테넌시 환경에서 병목, (2) 복잡한 아키텍처 - Kafka와 ZooKeeper 두 시스템을 운영해야 하므로 배포/모니터링/업그레이드가 복잡, (3) 느린 컨트롤러 페일오버 - 컨트롤러 브로커가 죽으면 ZooKeeper Watch로 감지하고 새 컨트롤러 선출하는데 수초 소요. 이 시간 동안 메타데이터 업데이트 불가.
- **KRaft의 장점**: (1) 단일 시스템 - Kafka만 운영하면 되므로 운영 복잡도 50% 감소(Pod 수, 설정 파일, 모니터링 대상 감소), (2) 확장성 - Raft 로그는 디스크 기반이므로 수백만 파티션 지원. LinkedIn은 KRaft로 100만 파티션 테스트 성공, (3) 빠른 페일오버 - Raft 프로토콜은 과반수 투표로 수백ms 내 새 컨트롤러 선출. 메타데이터 업데이트 중단 시간 10배 감소, (4) 일관된 메타데이터 - 컨트롤러가 Raft 로그를 브로커에게 스트리밍으로 전파. ZooKeeper는 브로커가 폴링하므로 지연 발생 가능.
- **메타데이터 저장 방식**: KRaft는 `__cluster_metadata` 내부 토픽에 메타데이터를 저장. 이 토픽은 일반 토픽과 달리 컨트롤러만 쓸 수 있고, 복제 계수는 컨트롤러 수(보통 3)와 동일. Raft 로그는 스냅샷으로 압축되어 디스크 사용량 최소화.
- **컨트롤러 역할**: ZooKeeper 모드는 브로커 중 1개가 컨트롤러 역할 수행. KRaft 모드는 Combined(브로커 + 컨트롤러 통합) 또는 Dedicated(컨트롤러 전용 노드) 선택 가능. Strimzi는 기본적으로 Combined 모드 사용. Dedicated 모드는 대규모 클러스터(100+ 브로커)에서 컨트롤러 부하를 분리하기 위해 사용.
- **마이그레이션**: Kafka 3.3+에서 ZooKeeper → KRaft 마이그레이션 지원. (1) ZooKeeper 모드로 실행 중인 클러스터에 KRaft 컨트롤러 추가, (2) ZooKeeper 메타데이터를 KRaft로 복제, (3) 브로커를 Rolling Update로 KRaft 모드로 전환, (4) ZooKeeper 제거. Strimzi에서는 아직 자동화 안 됨 - 수동 마이그레이션 필요.
- **Kafka 4.0 변경사항**: ZooKeeper 지원 완전 제거, KRaft만 지원. 3.x에서 4.0으로 업그레이드하려면 먼저 KRaft로 마이그레이션 필수.

**심화 질문**: KRaft의 컨트롤러 쿼럼이 과반수를 잃으면(예: 3개 중 2개가 죽음) 클러스터는 어떻게 되는가? 브로커는 계속 메시지를 처리할 수 있는가?

---

## Q3: Kafka listener 타입(internal, route, nodeport, ingress, loadbalancer) 선택 기준

**질문**: Strimzi의 Kafka listener 타입은 언제 어떤 것을 사용해야 하는가? 각 타입의 네트워크 경로와 TLS 설정은 어떻게 다른가?

**핵심 포인트**:

- **internal (ClusterIP)**: Kubernetes 클러스터 내부 Pod만 Kafka에 접근. Service DNS(`my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092`)로 연결. 네트워크 경로: 클라이언트 Pod → ClusterIP Service → 브로커 Pod. 가장 낮은 레이턴시, 외부 접근 불가. 프로덕션에서 마이크로서비스 간 통신에 사용.
- **loadbalancer (LoadBalancer Service)**: 클라우드 로드밸런서(AWS ELB, GCP LB, Azure LB)를 사용하여 외부 접근. Strimzi가 브로커당 LoadBalancer Service 생성(각 브로커에 고정 외부 IP). 클라이언트는 브로커별 IP:9094 포트로 연결. 네트워크 경로: 외부 클라이언트 → Cloud LB → 브로커 Pod. TLS 필수 권장(외부 노출). 프로덕션에서 클러스터 외부 클라이언트(데이터 파이프라인, 외부 서비스) 연결에 사용.
- **nodeport (NodePort Service)**: Kubernetes Node IP:NodePort로 외부 접근. 브로커당 NodePort Service 생성. 네트워크 경로: 외부 클라이언트 → Node IP:30092 → 브로커 Pod. 포트 범위 제한(30000-32767), 프로덕션 비추천. 개발 환경에서 minikube/kind 테스트용으로 사용.
- **route (OpenShift Route)**: OpenShift 전용. Route 리소스로 TLS Passthrough를 통해 외부 접근. 네트워크 경로: 외부 클라이언트 → OpenShift Router → 브로커 Pod. TLS 필수(Route는 TLS Passthrough 사용). Kubernetes에서는 지원 안 됨.
- **ingress (Ingress + TLS Passthrough)**: Nginx Ingress Controller 등에서 TLS Passthrough로 외부 접근. 브로커당 Ingress 리소스 생성. 네트워크 경로: 외부 클라이언트 → Ingress Controller → 브로커 Pod. TLS Passthrough 필수(Kafka는 HTTP가 아니므로 L7 라우팅 불가). Ingress Controller가 TLS Passthrough를 지원해야 함(`--enable-ssl-passthrough`).
- **부트스트랩 vs 브로커별 주소**: 클라이언트는 먼저 부트스트랩 주소(bootstrap Service)로 연결하여 브로커 목록 받아옴. 이후 브로커별 주소로 직접 연결. internal은 단일 Service로 충분하지만, loadbalancer/nodeport/ingress는 브로커당 별도 Service/Ingress 필요(클라이언트가 브로커별 외부 IP를 받아야 하므로).
- **TLS 설정**: `tls: true`로 설정하면 Strimzi가 자동으로 TLS 인증서 생성(Cluster CA). 클라이언트는 Secret에서 CA 인증서를 마운트하여 브로커 검증. mTLS(클라이언트 인증서)도 지원.

**심화 질문**: Kafka 클라이언트가 부트스트랩 주소로 연결한 후 브로커별 주소를 받아오는 과정은 어떻게 되는가? Strimzi는 브로커 Pod의 외부 IP를 어떻게 브로커 설정에 주입하는가?

---

## Q4: KafkaTopic CR로 토픽을 관리하는 것과 kafka-topics.sh의 차이

**질문**: KafkaTopic CR을 사용하는 것과 `kafka-topics.sh`로 직접 토픽을 관리하는 것의 차이는 무엇인가? Topic Operator를 사용할 때의 장단점은 무엇인가?

**핵심 포인트**:

- **선언적 vs 명령형**: KafkaTopic CR은 선언적(desired state). "파티션 3개, 복제 계수 2인 토픽이 존재해야 한다"를 선언하면 Topic Operator가 현재 상태를 desired state로 수렴. `kafka-topics.sh`는 명령형(imperative). "파티션을 3개에서 5개로 증가시켜라"를 직접 실행.
- **GitOps 통합**: KafkaTopic CR은 Git 저장소에 YAML로 관리 가능. Argo CD, Flux로 자동 배포. 토픽 생성/변경 이력이 Git 커밋 로그로 남음. `kafka-topics.sh`는 수동 실행이므로 이력 추적 어려움.
- **멀티 클러스터 관리**: KafkaTopic CR에 `labels.strimzi.io/cluster: my-cluster`를 추가하면 어떤 Kafka 클러스터에 속하는지 명시. 하나의 Namespace에 여러 Kafka 클러스터가 있어도 충돌 없음. `kafka-topics.sh`는 `--bootstrap-server` 주소를 매번 지정해야 하므로 실수 가능성 높음.
- **양방향 동기화 문제**: Topic Operator는 Kafka 토픽 변경을 감지하고 CR 상태를 업데이트하려고 시도. 하지만 `kafka-topics.sh`로 토픽을 생성하면 Topic Operator가 이를 감지하고 CR을 자동 생성하는데, Namespace에 이미 같은 이름의 CR이 있으면 충돌. 따라서 Topic Operator 사용 시 `kafka-topics.sh` 사용 금지 권장.
- **파티션 증가 제약**: Kafka는 파티션 감소를 지원하지 않음(데이터 손실 위험). KafkaTopic CR에서 `partitions: 5` → `partitions: 3`으로 변경하면 Topic Operator가 에러 발생. 파티션 증가만 가능. `kafka-topics.sh --alter --partitions 3`도 마찬가지로 에러.
- **리텐션 정책 변경**: `spec.config.retention.ms`를 변경하면 Topic Operator가 `kafka-configs.sh --alter` 실행. 동적 설정 변경 가능.
- **Topic Operator 비활성화**: `spec.entityOperator.topicOperator: {}`로 비활성화 가능. 이 경우 `kafka-topics.sh`로 직접 관리해야 함. 장점: 유연성(Kafka Admin API 모든 기능 사용 가능), 단점: 선언적 관리 불가, GitOps 통합 어려움.

**심화 질문**: KafkaTopic CR의 `spec.config`에 없는 Kafka 토픽 설정(예: `unclean.leader.election.enable`)을 변경하려면 어떻게 해야 하는가? Topic Operator의 한계는 무엇인가?

---

## Q5: Strimzi에서 Kafka 버전 업그레이드 과정 (Rolling Update)

**질문**: Strimzi로 Kafka 버전을 3.7.0에서 3.8.0으로 업그레이드할 때 어떤 과정을 거치는가? Rolling Update 중 클라이언트 연결이 끊기지 않도록 하는 메커니즘은 무엇인가?

**핵심 포인트**:

- **Kafka CR 변경**: `spec.kafka.version: 3.7.0` → `3.8.0`으로 변경. `kubectl apply`로 업데이트.
- **Cluster Operator 동작**: Cluster Operator가 변경을 감지하고 StatefulSet Rolling Update 시작. Pod를 하나씩 재시작(기본 전략: `RollingUpdate`).
- **Rolling Update 순서**: (1) 브로커 0 종료, (2) 새 이미지(3.8.0)로 브로커 0 시작 → Ready 대기, (3) 브로커 1 종료 → 시작, (4) 브로커 2 종료 → 시작. 한 번에 1개 Pod만 재시작하여 나머지 브로커가 서비스 제공.
- **리더 재선출**: 브로커가 종료되면 해당 브로커가 리더였던 파티션은 ISR(In-Sync Replica) 중 다른 브로커로 리더 재선출. 클라이언트는 메타데이터 업데이트로 새 리더를 발견하고 재연결. 재선출 시간은 수백ms.
- **클라이언트 재연결**: Kafka 클라이언트는 브로커 연결이 끊기면 자동으로 다른 브로커에 재연결. 프로듀서/컨슈머 라이브러리가 내부적으로 처리. 애플리케이션 코드 변경 불필요. 단, 짧은 시간(수백ms) 동안 `NetworkException` 발생 가능하므로 재시도 로직 필요.
- **Graceful Shutdown**: Kafka 브로커는 종료 시 리더십을 다른 브로커로 이전한 후 종료. `controlled.shutdown.enable=true`(기본값)로 설정되어 있으면 리더 파티션을 먼저 다른 브로커로 옮긴 후 종료하므로 가용성 영향 최소화.
- **Inter-broker Protocol Version**: Kafka는 브로커 간 통신 프로토콜 버전을 별도로 관리. 업그레이드 시 먼저 바이너리만 업그레이드하고, 모든 브로커가 3.8.0이 되면 `inter.broker.protocol.version`을 3.8로 변경. Strimzi는 이를 자동화하지 않으므로 수동 설정 필요.
- **클라이언트 호환성**: Kafka 클라이언트는 하위 호환(backward compatible). 3.7.0 클라이언트가 3.8.0 브로커에 연결 가능. 하지만 상위 호환은 보장 안 됨(3.8.0 클라이언트 → 3.7.0 브로커는 일부 기능 미지원 가능).

**심화 질문**: Rolling Update 중 브로커가 재시작될 때 해당 브로커의 리플리카 파티션은 어떻게 되는가? ISR에서 제외되었다가 재시작 후 다시 추가되는가?

---

## Q6: JBOD vs 단일 디스크 스토리지 전략

**질문**: Strimzi에서 Kafka 브로커 스토리지를 JBOD(여러 디스크)로 구성하는 것과 단일 PVC로 구성하는 것의 차이는 무엇인가? JBOD의 장단점과 사용 사례는 무엇인가?

**핵심 포인트**:

- **단일 PVC**: `spec.kafka.storage.type: persistent-claim`으로 설정하면 브로커당 PVC 1개 생성. 모든 파티션 데이터가 이 PVC에 저장. 간단하지만, PVC 크기 제한에 도달하면 확장 어려움(일부 스토리지 클래스는 동적 확장 지원).
- **JBOD (Just a Bunch Of Disks)**: `spec.kafka.storage.type: jbod`로 설정하면 브로커당 PVC 여러 개 생성. 각 PVC를 별도 디스크로 마운트. Kafka는 파티션을 여러 디스크에 분산 저장. 예: JBOD 3개 → 브로커당 PVC 3개 → 파티션 로그를 라운드 로빈으로 분산.
- **JBOD 장점**: (1) 처리량 증가 - 여러 디스크에 병렬 I/O 수행하여 처리량 증가(단일 PVC 대비 2-3배), (2) 디스크 장애 격리 - 디스크 1개가 고장나도 다른 디스크의 파티션은 정상 동작. Kafka는 고장난 디스크의 파티션만 리플리카에서 복구, (3) 동적 확장 - 디스크 추가 시 새 PVC를 JBOD에 추가하고 Kafka 재시작. 기존 데이터 이동 불필요.
- **JBOD 단점**: (1) 운영 복잡도 증가 - PVC 관리가 복잡. 브로커당 PVC 3개 × 브로커 5개 = 15개 PVC, (2) 디스크 불균형 - 파티션이 고르게 분산되지 않으면 일부 디스크만 과부하 가능. Kafka는 디스크 간 리밸런싱 미지원, (3) PVC 삭제 위험 - 실수로 PVC 삭제 시 복구 어려움.
- **Kafka JBOD 동작**: Kafka는 새 파티션 생성 시 로그 디렉토리 중 여유 공간이 가장 많은 디렉토리를 선택. 디스크 1이 80% 사용 중이고 디스크 2가 40% 사용 중이면 디스크 2에 파티션 생성. 하지만 기존 파티션은 이동하지 않음.
- **디스크 장애 처리**: JBOD 중 디스크 1개가 고장나면 해당 디스크의 파티션은 오프라인. Kafka는 이 파티션의 리플리카를 다른 브로커에서 승격. 브로커 재시작 후 고장난 디스크를 교체하고 리플리카 복구 수행.
- **사용 사례**: 대규모 Kafka 클러스터(브로커당 10TB+ 데이터)에서 처리량과 장애 격리가 중요한 경우. 예: LinkedIn, Uber는 브로커당 JBOD 12개 사용. minikube에서는 JBOD 불필요(단일 PVC로 충분).

**심화 질문**: JBOD에서 디스크 1개가 고장났을 때 Kafka가 자동으로 리플리카를 복구하는 과정은 무엇인가? 데이터 손실 없이 복구 가능한가?

---

## Q7: minikube에서 Kafka 1 broker로 운영할 때의 한계

**질문**: minikube에서 Kafka를 1 broker로 운영할 때 어떤 기능이 제한되는가? 프로덕션 환경으로 전환할 때 주의할 점은 무엇인가?

**핵심 포인트**:

- **복제 없음**: 1 broker이므로 `replication.factor: 1`로 설정해야 함. 파티션 리플리카가 없으므로 브로커가 죽으면 데이터 손실. 프로덕션에서는 최소 3 broker + replication factor 3 필수.
- **고가용성 미지원**: 브로커 재시작 시 모든 파티션이 오프라인. 클라이언트는 브로커가 복구될 때까지 연결 불가(수초~수분). 프로덕션에서는 Rolling Update로 브로커를 하나씩 재시작하여 가용성 유지.
- **파티션 리더 재선출 불가**: 1 broker이므로 모든 파티션의 리더가 브로커 0. 리더가 죽으면 ISR에서 새 리더를 선출해야 하는데, 리플리카가 없으므로 재선출 불가. 브로커가 재시작될 때까지 대기.
- **처리량 제한**: 단일 브로커의 네트워크/디스크 처리량이 한계. 예: 브로커 CPU 500m + 메모리 1Gi → 초당 1만 메시지 정도 처리 가능. 프로덕션에서는 3 broker로 부하 분산하여 초당 10만+ 메시지 처리.
- **파티션 분산 불가**: 토픽의 모든 파티션이 브로커 0에 집중. 파티션을 여러 브로커에 분산하여 부하 분산하는 Kafka의 핵심 기능 미사용. 프로덕션에서는 파티션 수를 브로커 수의 배수로 설정(예: 3 broker → 파티션 6개 → 브로커당 2개).
- **Consumer Group 리밸런싱 제한**: 컨슈머 그룹의 리밸런싱(파티션 재할당)을 테스트할 수 없음. 1 broker이므로 파티션 이동이 의미 없음. 프로덕션에서는 컨슈머가 증가하면 파티션을 여러 컨슈머에 분산.
- **Ephemeral Storage 데이터 손실**: minikube에서 `storage.type: ephemeral` 사용 시 Pod 재시작 시 데이터 손실. 프로덕션에서는 `persistent-claim` + 10GB+ PVC 필수. 백업/복구 전략도 필요(Kafka MirrorMaker, Velero).
- **프로덕션 전환 체크리스트**: (1) 브로커 3+ 증가, (2) replication.factor 3 설정, (3) min.insync.replicas 2 설정, (4) persistent-claim 스토리지, (5) 리소스 증가(2000m CPU, 4Gi 메모리), (6) TLS 활성화(listener tls: true), (7) SCRAM 인증 + ACL, (8) 메트릭 수집(JMX Exporter + Prometheus), (9) 백업 전략(MirrorMaker2로 DR 클러스터에 미러링).

**심화 질문**: minikube에서 1 broker로 개발한 애플리케이션을 프로덕션 3 broker 환경으로 배포할 때, 파티션 수를 1에서 3으로 증가시키면 컨슈머 그룹에 어떤 영향이 있는가? 리밸런싱이 발생하는가?
