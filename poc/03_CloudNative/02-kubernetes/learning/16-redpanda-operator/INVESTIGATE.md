# Ch16: Redpanda Operator 점검 질문

> 이 질문들은 Ch16 LEARN.md의 핵심 개념을 점검하기 위한 것이다. 각 질문의 핵심 포인트를 먼저 읽고, 심화 질문으로 이해의 깊이를 확인한다.

---

## Q1: Redpanda가 JVM 없이 C++로 구현된 것이 운영에 어떤 차이를 만드는가?

**질문**: Redpanda는 C++ + Seastar 프레임워크로 구현되었고, Kafka는 JVM(Java) 위에서 동작한다. 이 런타임 차이가 실제 운영 환경에서 어떤 실질적인 차이를 만드는가?

**핵심 포인트**:

- **GC(Garbage Collection) 일시 정지 제거**: JVM 기반 Kafka는 메모리가 가득 차면 GC가 실행되며, 이 시간 동안 모든 요청 처리가 멈추는 Stop-the-World 현상이 발생한다. G1GC를 사용해도 수십~수백ms의 일시 정지가 간헐적으로 발생하며, 이는 꼬리 지연(P99, P99.9 latency)을 악화시킨다. Redpanda는 C++ 네이티브 바이너리이므로 GC 자체가 존재하지 않는다. 메모리 할당과 해제를 Seastar 프레임워크가 코어별로 독립적으로 관리하므로 일시 정지 없이 일관된 레이턴시를 제공한다.

- **Thread-per-Core 모델의 성능 특성**: Seastar는 CPU 코어당 하나의 이벤트 루프 스레드를 할당한다. 각 코어는 자신의 메모리, 네트워크 큐, 디스크 I/O를 독립적으로 관리하며, 코어 간 데이터 공유가 없으므로 락(lock)이 불필요하다. 이는 CPU 코어 수에 비례하여 처리량이 선형으로 증가함을 의미한다. 반면 Kafka는 공유 메모리 기반의 멀티스레드 모델을 사용하므로, 스레드 수가 증가할수록 락 경합(contention)이 발생하여 성능 향상에 한계가 있다.

- **운영자 관점의 차이**: Kafka 운영자는 JVM Heap 크기(-Xms, -Xmx), GC 알고리즘(G1GC, ZGC, Shenandoah), GC 로그 분석, JMX 모니터링에 대한 전문 지식이 필요하다. Redpanda 운영자는 이러한 JVM 튜닝이 불필요하고, `memory.redpanda.memory`와 `reserveMemory` 두 가지 설정만으로 메모리를 관리한다. 이는 운영 진입 장벽을 낮추고 튜닝에 소요되는 시간을 줄여준다.

- **리소스 효율성**: JVM은 Heap 외에도 Metaspace, Code Cache, Thread Stack 등에 추가 메모리를 사용한다. 4GB Heap 설정 시 실제 JVM 프로세스는 5~6GB를 사용한다. Redpanda는 이러한 오버헤드가 없으므로 같은 하드웨어에서 더 많은 메모리를 데이터 캐싱(페이지 캐시)에 활용할 수 있다.

- **트레이드오프**: C++ 구현은 성능 면에서 유리하지만, Kafka의 거대한 Java 생태계(Kafka Streams, ksqlDB, Confluent Platform)를 직접 활용할 수 없다는 단점이 있다. 또한 Redpanda의 코드베이스가 Kafka보다 상대적으로 신생이므로, 엣지 케이스에서의 안정성은 아직 Kafka만큼의 프로덕션 검증을 거치지 못했다.

**심화 질문**: Thread-per-Core 모델에서 특정 코어에 핫 파티션(hot partition)이 집중되면 코어 간 부하 불균형이 발생할 수 있다. Redpanda는 이 문제를 어떻게 해결하는가?

---

## Q2: Strimzi Kafka Operator vs Redpanda Operator: 언제 어떤 것을 선택하는가?

**질문**: Kubernetes에서 이벤트 스트리밍을 구축할 때 Strimzi와 Redpanda Operator 중 어떤 것을 선택해야 하는가? 기술적, 조직적 관점에서 판단 기준은 무엇인가?

**핵심 포인트**:

- **기술 스택 호환성 관점**: Kafka Streams, ksqlDB를 사용하는 프로젝트라면 Strimzi가 유일한 선택이다. Kafka Streams는 Kafka 내부 프로토콜에 의존하여 Redpanda에서 공식 지원하지 않는다. 반면 Kafka Connect, MirrorMaker2, 일반 Kafka 클라이언트만 사용하는 경우라면 Redpanda도 동일한 기능을 제공한다.

- **운영 복잡도 관점**: Strimzi는 Cluster Operator, Entity Operator(Topic + User), Kafka 브로커, ZooKeeper/KRaft 컨트롤러로 구성되어 최소 4~5개 Pod가 필요하다. Redpanda Operator는 Operator Pod + 브로커 Pod으로 최소 2개면 충분하다. Schema Registry와 REST Proxy가 브로커에 내장되어 있으므로 추가 구성 요소가 줄어든다. 운영 인력이 적거나 Kubernetes 경험이 제한적인 팀이라면 Redpanda의 단순한 구성이 유리하다.

- **리소스 효율성 관점**: 클라우드 환경에서 인프라 비용이 중요한 경우, Redpanda의 낮은 메모리/CPU 사용량이 비용 절감으로 이어진다. Kafka 브로커당 6~8GB 메모리 + ZooKeeper 1~2GB가 필요한 반면, Redpanda 브로커당 2~4GB로 유사한 처리량을 달성할 수 있다. 특히 개발/테스트 환경에서 다수의 클러스터를 운영할 때 리소스 차이가 누적된다.

- **커뮤니티와 성숙도 관점**: Strimzi는 CNCF Sandbox 프로젝트로 6년 이상의 역사와 대규모 프로덕션 사례를 보유한다. Red Hat, IBM 등 대기업이 기여하며, Kubernetes Operator 패턴의 모범 사례로 꼽힌다. Redpanda Operator는 상대적으로 신생(2020~)이며, 커뮤니티 규모가 작다. 엔터프라이즈 지원이 중요한 조직이라면 Strimzi의 성숙한 생태계가 안전한 선택이다.

- **마이그레이션 용이성 관점**: 이미 Kafka를 사용 중이라면 Strimzi로의 전환이 더 자연스럽다(같은 Apache Kafka). Redpanda로의 마이그레이션은 MirrorMaker2를 통한 데이터 복제가 필요하며, Kafka 전용 기능(Kafka Streams) 사용 여부를 사전에 확인해야 한다.

**심화 질문**: Strimzi에서 Redpanda로 마이그레이션할 때 MirrorMaker2를 사용하는 것과 카프카 클라이언트의 bootstrap.servers만 변경하는 것의 차이는 무엇인가? 데이터 유실 없이 마이그레이션하려면 어떤 순서로 진행해야 하는가?

---

## Q3: Schema Registry 내장 vs 외부 배포의 트레이드오프

**질문**: Redpanda는 Schema Registry를 브로커에 내장하고, Kafka 생태계는 별도 서비스(Confluent Schema Registry)로 운영한다. 각 방식의 트레이드오프는 무엇이며, 어떤 상황에서 어느 방식이 유리한가?

**핵심 포인트**:

- **내장 방식의 장점**: 배포 단순화(별도 Pod/Service 불필요), 네트워크 홉 감소(로컬 호출), 가용성 자동 보장(브로커가 살아있으면 Registry도 동작), 리소스 오버헤드 감소, Testcontainers에서 단일 컨테이너로 테스트 가능. 특히 소규모~중규모 팀에서 운영 부담을 크게 줄여준다.

- **내장 방식의 단점**: Schema Registry만 독립적으로 스케일링할 수 없다. 스키마 요청이 폭증해도 브로커 전체를 스케일아웃해야 한다. 또한 Schema Registry의 버전을 브로커와 독립적으로 업그레이드할 수 없다. 브로커 버전 업그레이드 시 Schema Registry도 함께 변경된다.

- **외부 배포 방식의 장점**: Schema Registry를 독립적으로 스케일링할 수 있다. 브로커는 3대이지만 Schema Registry는 5대로 운영하는 것이 가능하다. 또한 Confluent Schema Registry는 다중 데이터센터 복제, 고급 호환성 모드(FULL_TRANSITIVE), Schema 링크 등 고급 기능을 제공한다. 브로커 장애 시에도 Schema Registry 캐시가 동작하여 일시적으로 서비스 가능하다.

- **외부 배포 방식의 단점**: 추가 Pod, Service, ConfigMap, 모니터링 구성이 필요하다. 브로커와 Schema Registry 간 버전 호환성을 확인해야 한다. 네트워크 설정(Service Discovery, TLS)이 복잡해진다. 통합 테스트 시 두 개 이상의 컨테이너를 관리해야 한다.

- **의사 결정 기준**: 스키마 수가 수천 개 미만이고 초당 스키마 조회 요청이 수백 건 미만이면 내장 방식으로 충분하다. 대규모 멀티테넌트 환경에서 수만 개의 스키마를 관리하고, 스키마 요청이 브로커 부하에 영향을 주지 않아야 하는 경우 외부 배포가 유리하다.

**심화 질문**: Redpanda의 내장 Schema Registry는 `_schemas` 내부 토픽에 스키마를 저장한다. 이 토픽이 손상되거나 삭제되면 어떻게 복구하는가? Confluent Schema Registry와 호환성 모드(BACKWARD, FORWARD, FULL)의 동작 차이가 있는가?

---

## Q4: Redpanda의 Raft 합의와 Kafka의 ZooKeeper/KRaft 비교

**질문**: Redpanda는 자체 Raft 구현을 사용하고, Kafka는 ZooKeeper에서 KRaft로 전환 중이다. 두 접근 방식의 메타데이터 관리와 리더 선출은 어떻게 다르며, 실제 장애 시나리오에서 어떤 차이가 발생하는가?

**핵심 포인트**:

- **메타데이터 관리 범위**: Kafka의 ZooKeeper/KRaft는 클러스터 수준의 메타데이터(브로커 목록, 토픽 설정, ACL 등)를 관리한다. 파티션 리더 선출은 컨트롤러(단일 브로커 또는 KRaft 컨트롤러 쿼럼)가 중앙에서 결정한다. Redpanda는 각 파티션마다 독립적인 Raft 그룹을 운영한다. 파티션 10,000개면 Raft 그룹도 10,000개이다. 각 Raft 그룹이 자체적으로 리더를 선출하므로 중앙 컨트롤러의 병목이 없다.

- **리더 선출 속도**: ZooKeeper 모드에서는 컨트롤러 브로커가 죽으면 ZooKeeper Watch로 감지(수백ms)하고 새 컨트롤러를 선출(수초)해야 한다. 이 시간 동안 모든 파티션의 리더 변경이 불가하다. KRaft는 Raft 프로토콜로 수백ms 내 새 컨트롤러를 선출하여 크게 개선되었다. Redpanda는 파티션별 Raft이므로 특정 브로커가 죽어도 해당 브로커가 리더였던 파티션만 리더 재선출이 발생하고, 나머지 파티션은 영향을 받지 않는다.

- **장애 복구 시나리오**: 3대 중 1대가 다운된 경우를 비교한다. Kafka(KRaft): 컨트롤러 쿼럼이 2/3으로 줄어들지만 과반수 유지되어 동작 지속. 다운된 브로커의 리더 파티션은 컨트롤러가 새 리더를 지정. Redpanda: 다운된 브로커가 리더였던 Raft 그룹에서 나머지 2개 복제본이 자체적으로 새 리더를 선출. 파티션별로 독립 복구되므로 복구 시간이 파티션 수에 비례하지 않는다.

- **확장성 한계**: Kafka의 중앙 컨트롤러 모델은 파티션 수가 수십만~수백만 개를 넘어가면 컨트롤러의 메타데이터 처리 부하가 증가한다. KRaft는 이를 디스크 기반 Raft 로그로 개선했지만, 여전히 중앙 지점이 존재한다. Redpanda의 파티션별 Raft는 파티션 수가 늘어나도 각 Raft 그룹이 독립적이므로 확장성 문제가 적다. 다만 Raft 그룹 수가 많아지면 메모리와 네트워크 오버헤드가 증가한다.

- **일관성 보장**: 두 시스템 모두 Raft 기반이므로 Linearizable 읽기/쓰기를 보장할 수 있다. 하지만 기본 설정에서 Kafka는 `acks=all` + `min.insync.replicas`로, Redpanda는 Raft 과반수 복제로 일관성 수준을 제어한다.

**심화 질문**: Redpanda에서 파티션 수가 10만 개를 넘으면 Raft 그룹 10만 개가 생긴다. 각 Raft 그룹의 하트비트와 선출 메시지가 네트워크에 어떤 부하를 주는가? Kafka KRaft의 중앙 컨트롤러 모델과 비교했을 때 어느 쪽이 대규모 환경에서 유리한가?

---

## Q5: Topic CR로 토픽을 관리할 때 vs rpk/kafka-topics.sh CLI 사용의 차이

**질문**: Redpanda Operator의 Topic CR을 사용하는 것과 rpk 또는 kafka-topics.sh CLI로 직접 토픽을 관리하는 것의 차이는 무엇이며, 어떤 방식을 언제 사용해야 하는가?

**핵심 포인트**:

- **선언적 vs 명령형 관리**: Topic CR은 Kubernetes의 선언적 모델을 따른다. "이 토픽이 이 설정으로 존재해야 한다"를 YAML로 선언하면, Operator가 현재 상태(actual state)를 원하는 상태(desired state)로 수렴시킨다. 토픽이 없으면 생성하고, 설정이 다르면 변경한다. rpk/kafka-topics.sh는 명령형이다. "토픽을 생성하라", "파티션을 5개로 변경하라"를 직접 실행한다.

- **GitOps 워크플로우와의 통합**: Topic CR은 YAML 파일이므로 Git 저장소에 커밋할 수 있다. Argo CD나 Flux가 Git 변경을 감지하여 자동으로 `kubectl apply`를 실행하면, 토픽 생성/변경이 코드 리뷰와 승인 프로세스를 거치게 된다. 누가, 언제, 왜 토픽 설정을 변경했는지 Git 커밋 로그로 추적할 수 있다. rpk CLI는 수동 실행이므로 이력 추적이 어렵고, 실수로 잘못된 토픽을 삭제할 위험이 있다.

- **일관성과 드리프트 방지**: Topic CR이 존재하면 Operator가 주기적으로 Reconciliation을 수행한다. 누군가 rpk으로 토픽 설정을 직접 변경해도, Operator가 CR에 정의된 상태로 되돌린다. 이는 설정 드리프트(drift)를 방지하지만, 반대로 긴급 상황에서 빠르게 설정을 변경하기 어렵게 만들 수 있다.

- **CLI의 유연성**: rpk CLI는 Topic CR이 지원하지 않는 고급 작업을 수행할 수 있다. 예를 들어 파티션 재분배(`rpk cluster partitions move`), 컨슈머 그룹 오프셋 리셋(`rpk group seek`), 브로커 상태 확인(`rpk cluster health`)은 CLI로만 가능하다. 또한 디버깅 시 빠르게 토픽을 생성하거나 메시지를 확인하는 데는 CLI가 더 편리하다.

- **혼용 시 주의사항**: Topic CR과 CLI를 혼용하면 충돌이 발생할 수 있다. CLI로 토픽을 생성한 뒤 같은 이름의 Topic CR을 적용하면, Operator가 기존 토픽의 소유권을 가져가면서 설정을 CR 값으로 덮어쓸 수 있다. 반대로 CR로 관리하던 토픽을 CLI로 삭제하면, Operator가 토픽을 다시 생성한다. 따라서 하나의 토픽은 하나의 방식으로만 관리하는 것이 원칙이다.

- **권장 패턴**: 프로덕션 토픽은 Topic CR로 관리하여 GitOps와 통합한다. 개발/테스트 환경에서 임시 토픽은 rpk CLI로 빠르게 생성/삭제한다. 디버깅이나 운영 작업(오프셋 리셋, 파티션 재분배)은 rpk CLI를 사용한다.

**심화 질문**: Argo CD로 Topic CR을 관리할 때, Argo CD의 sync가 실패하면(예: replicationFactor가 브로커 수보다 큰 경우) 어떻게 복구해야 하는가? Topic CR의 `additionalConfig`에 없는 Kafka 토픽 설정을 변경하려면 어떻게 해야 하는가?

---

## Q6: minikube 환경에서 Redpanda의 리소스 튜닝

**질문**: minikube에서 Redpanda를 실행할 때 `tuning` 옵션(tune_aio_events, tune_clocksource 등)을 비활성화하는 이유는 무엇이며, 프로덕션과 어떤 차이가 있는가?

**핵심 포인트**:

- **Redpanda의 자동 튜닝**: Redpanda는 시작 시 `rpk redpanda tune`을 실행하여 OS 커널 파라미터를 자동으로 최적화하려고 한다. 여기에는 AIO(Asynchronous I/O) 이벤트 수 증가(`fs.aio-max-nr`), 클럭 소스 변경(TSC 사용), 스와프 비활성화(`vm.swappiness=0`), 네트워크 튜닝(`net.core.somaxconn`), IRQ 밸런싱 등이 포함된다. 이 튜닝들은 물리 서버나 전용 VM에서 성능을 극대화하기 위한 것이다.

- **minikube에서 비활성화하는 이유**: minikube는 Docker 컨테이너 또는 경량 VM으로 실행되므로 커널 파라미터 변경 권한이 제한된다. `tune_aio_events: true`로 설정하면 컨테이너 내부에서 `sysctl`을 실행하려다 권한 오류가 발생한다. `tune_clocksource`는 가상 환경에서 TSC 클럭 소스를 사용할 수 없어 실패한다. 따라서 minikube에서는 모든 튜닝을 비활성화하고 기본 OS 설정으로 실행한다.

- **ballast_file_size 설정**: Redpanda는 디스크에 "ballast file"을 생성하여 디스크 공간을 예약한다. 디스크가 가득 찰 위기에 처하면 ballast file을 삭제하여 긴급 여유 공간을 확보한다. minikube에서는 디스크가 제한적이므로 `ballast_file_size: "0"`으로 비활성화하여 디스크 공간을 절약한다. 프로덕션에서는 디스크 크기의 1~5%를 ballast로 설정한다.

- **프로덕션 튜닝과의 차이**: 프로덕션에서는 모든 튜닝을 활성화하고, 추가로 NUMA 노드 인식, CPU 거버너(performance 모드), 디스크 스케줄러(noop/none) 설정을 적용한다. 이러한 튜닝으로 레이턴시가 30~50% 개선될 수 있다. minikube에서는 이러한 튜닝이 불가하므로, 기능 테스트와 학습 목적으로만 사용해야 한다.

- **minikube에서의 성능 기대치**: 튜닝 없이 minikube에서 Redpanda를 실행하면 프로듀서/컨슈머 처리량이 프로덕션 대비 10~30% 수준이다. 이는 가상화 오버헤드, 공유 디스크, 제한된 CPU/메모리 때문이다. 하지만 기능적으로는 프로덕션과 동일하게 동작하므로 토픽 관리, Schema Registry, Console UI 등을 테스트하기에 충분하다.

**심화 질문**: Kubernetes에서 Redpanda Pod에 `privileged: true` 보안 컨텍스트를 부여하면 커널 튜닝이 가능해진다. 이 방식의 보안 리스크는 무엇이며, Pod Security Standards의 어느 레벨에서 허용되는가? (다음 챕터 Ch17 RBAC & Security와 연결)

---

## Q7: Redpanda의 Tiered Storage와 Kubernetes PV 전략

**질문**: Redpanda는 Tiered Storage(S3, GCS)를 지원하여 로컬 디스크 사용량을 줄일 수 있다. Kubernetes 환경에서 이 기능은 어떻게 동작하며, PersistentVolume 전략에 어떤 영향을 미치는가?

**핵심 포인트**:

- **Tiered Storage의 동작 원리**: Redpanda의 Tiered Storage는 로컬 디스크의 세그먼트 파일을 객체 스토리지(S3, GCS, Azure Blob)에 비동기적으로 업로드한다. 최근 데이터(hot data)는 로컬 디스크에 유지하고, 오래된 데이터(cold data)는 객체 스토리지에만 보관한다. 컨슈머가 오래된 데이터를 요청하면 객체 스토리지에서 다운로드하여 서빙한다. 이 방식은 Kafka의 Confluent Tiered Storage나 Apache Kafka KIP-405와 유사하다.

- **PV 크기 절감 효과**: Tiered Storage가 없으면 retention 기간(예: 7일) 동안의 모든 데이터를 로컬 PV에 저장해야 한다. 일일 100GB 유입 시 최소 700GB PV가 필요하다. Tiered Storage를 활성화하면 로컬에는 최근 몇 시간~하루치만 보관하고 나머지는 S3에 저장하므로, PV를 100~200GB로 줄일 수 있다. Kubernetes 환경에서 PV는 IOPS에 비례하여 비용이 증가하므로(AWS gp3, GCP pd-ssd), PV 크기 절감은 직접적인 비용 절감으로 이어진다.

- **Kubernetes에서의 설정**: Redpanda CR에서 Tiered Storage를 활성화하려면 `cloud_storage_enabled: true`와 버킷 정보를 설정한다. S3 접근을 위한 IAM 자격 증명은 Kubernetes Secret으로 관리하거나, EKS에서는 IRSA(IAM Roles for Service Accounts)를 사용하여 Pod에 IAM 역할을 직접 부여할 수 있다. IRSA 방식이 Secret에 액세스 키를 저장하는 것보다 보안적으로 우수하다.

- **복구 시나리오**: 브로커의 PV가 손상되더라도 Tiered Storage에 데이터가 보존되어 있으므로, 새 PV를 할당하고 브로커를 재시작하면 객체 스토리지에서 데이터를 복구할 수 있다. 이는 PV 기반 복구보다 안정적이며, 특히 클라우드 환경에서 AZ(Availability Zone) 장애 시 다른 AZ에서 브로커를 재시작하는 DR(Disaster Recovery) 시나리오에 유용하다.

- **minikube에서의 한계**: minikube에서는 S3 호환 객체 스토리지가 없으므로 Tiered Storage를 테스트하려면 MinIO를 로컬에 배포해야 한다. MinIO는 S3 호환 API를 제공하므로 Redpanda의 Tiered Storage를 테스트하기에 적합하지만, 프로덕션 성능을 반영하지는 않는다.

- **Kafka와의 비교**: Apache Kafka도 KIP-405(Tiered Storage)를 통해 유사한 기능을 도입했으나, Kafka의 Tiered Storage는 상대적으로 최근에 GA가 되었고 Confluent Platform에서 더 성숙하게 지원된다. Redpanda는 초기부터 Shadow Indexing이라는 이름으로 Tiered Storage를 지원해 왔으며, 오픈소스 버전에서도 제한 없이 사용할 수 있다.

- **데이터 일관성**: Tiered Storage에 업로드된 세그먼트는 불변(immutable)이다. 로컬 세그먼트가 클로즈(close)된 후에만 업로드되므로, 업로드 중 데이터 손상 가능성이 낮다. 다만 객체 스토리지와 로컬 디스크 간 메타데이터 동기화가 중요하며, Redpanda는 이를 `archival_metadata` 내부 토픽으로 관리한다.

**심화 질문**: Tiered Storage에서 객체 스토리지의 데이터를 읽는 컨슈머의 레이턴시는 로컬 디스크 대비 어떻게 달라지는가? 실시간 처리와 배치 처리에서 Tiered Storage의 적용 전략은 어떻게 다른가?



---

> **[이관 완료]** write/09_cloud/kubernetes/06-06.Redpanda Operator.md · deepdive/06-06.Redpanda Operator 점검.md (2026-04-19)
