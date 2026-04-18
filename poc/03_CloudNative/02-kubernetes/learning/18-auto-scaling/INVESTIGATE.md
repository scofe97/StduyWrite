# Ch18. Auto-scaling 점검 질문

## Q1: HPA 스케일 아웃 시 쿨다운 기간의 필요성

**질문**: HPA가 스케일 아웃할 때 "쿨다운 기간(stabilization window)"이 왜 필요하며, 이를 설정하지 않으면 어떤 문제가 발생하는가?

**핵심 포인트**:

- **메트릭 변동성(Flapping)**: 실제 트래픽은 일정하지 않고 짧은 주기로 등락을 반복한다. 예를 들어 1초 동안 CPU 사용률이 80%를 찍었다가 다음 1초에 30%로 떨어질 수 있다. HPA Controller는 기본 15초 주기로 메트릭을 확인하는데, 쿨다운 기간 없이 매 주기마다 즉각 반응하면 Pod를 5개로 늘렸다가 3개로 줄이고 다시 6개로 늘리는 진동(oscillation)이 발생한다. 이는 불필요한 Pod 생성/삭제를 반복하며 오히려 시스템 안정성을 해친다.

- **스케일 업 안정화 창(stabilizationWindowSeconds)**: HPA v2의 `behavior.scaleUp.stabilizationWindowSeconds`는 스케일 업 전에 지정된 시간 동안의 메트릭을 관찰하고, 그 기간 내 계산된 추천 replica 수 중 가장 낮은 값을 채택한다. 기본값은 0초(즉시 반응)이다. 이를 60초로 설정하면 60초간의 메트릭 변화를 종합적으로 판단하므로, 일시적 스파이크에 과도하게 반응하는 것을 방지할 수 있다.

- **스케일 다운 안정화 창**: `behavior.scaleDown.stabilizationWindowSeconds`의 기본값은 300초(5분)이다. 이 5분 동안 메트릭이 안정적으로 낮은 상태를 유지해야 비로소 Pod를 줄인다. 왜 스케일 다운을 보수적으로 하는가? 트래픽이 일시적으로 줄었다가 다시 급증하는 패턴(예: 점심 시간 직후 잠시 줄었다가 오후에 다시 증가)에서, 성급하게 Pod를 줄이면 재확장 시 Cold Start(JVM 워밍업, 캐시 비어있음, DB 커넥션 풀 재생성)로 인해 응답 시간이 급증한다. Pod를 유지하는 비용보다 재생성하는 비용이 더 클 수 있다.

- **정책(Policy) 조합**: `scaleDown.policies`에서 `Percent`와 `Pods` 타입을 조합하여 한 번에 최대 10%씩, 또는 최대 2개씩만 줄이도록 제한할 수 있다. `selectPolicy: Min`으로 설정하면 두 정책 중 더 보수적인(적게 줄이는) 값을 채택한다. 예를 들어 현재 20개 Pod가 있을 때 Percent 10% = 2개, Pods = 3개라면, Min 정책은 2개만 줄인다.

- **실무 권장 설정**: 스케일 업은 빠르게(stabilization 0~60초), 스케일 다운은 느리게(stabilization 300~600초)가 일반적이다. 이유는 "사용자가 느린 것은 참지만, 서비스가 죽는 것은 참지 못한다"는 운영 원칙 때문이다. 불필요한 Pod를 잠시 더 유지하는 비용은 서비스 장애 비용보다 훨씬 작다.

- **진동의 실제 비용**: 진동이 발생하면 단순히 Pod 수가 오르내리는 것 이상의 문제가 생긴다. Pod가 생성될 때마다 컨테이너 이미지 Pull, 애플리케이션 초기화, Readiness Probe 통과까지 시간이 소요되며, 이 기간 동안 Service의 Endpoints가 불안정하여 일부 요청이 실패할 수 있다. 또한 Kubernetes 이벤트 로그가 스케일링 이벤트로 가득 차 실제 문제를 파악하기 어려워진다.

**심화 질문**: 트래픽 패턴이 매우 예측 가능한 서비스(예: 오전 9시~오후 6시 고정 패턴)에서 HPA 쿨다운 대신 KEDA의 Cron 트리거를 사용하는 것이 더 효율적인 경우는 언제인가? 두 접근법의 비용-반응성 트레이드오프를 비교하라.

---

## Q2: VPA와 HPA의 동시 사용 충돌

**질문**: VPA와 HPA를 동시에 사용하면 충돌이 발생하는가? 발생한다면 어떤 메커니즘 때문이며, 어떻게 해결하는가?

**핵심 포인트**:

- **충돌이 발생하는 조건**: VPA와 HPA가 **같은 메트릭(CPU, 메모리)**을 기준으로 동작할 때 충돌한다. CPU 사용률이 높아지면 HPA는 "Pod를 더 만들자"고 판단하고, VPA는 "Pod에 CPU를 더 주자"고 판단한다. HPA가 Pod를 늘리면 평균 CPU 사용률이 떨어지고, VPA가 CPU requests를 올리면 사용률 계산 기준이 바뀐다. 두 컨트롤러가 서로의 판단을 무효화하면서 진동이 발생한다.

- **VPA의 Pod 재시작 문제**: VPA가 리소스를 조정하려면 Pod를 퇴거(evict)시키고 새 requests/limits로 재생성해야 한다 (In-Place Resource Resize가 지원되지 않는 경우). Pod 재시작 중 트래픽이 나머지 Pod에 집중되어 CPU가 더 올라가고, HPA가 추가 스케일 아웃을 트리거하는 연쇄 반응이 일어날 수 있다. 최악의 경우 HPA가 maxReplicas까지 확장하고, 트래픽이 분산되면 다시 줄이는 비효율적인 사이클이 반복된다.

- **해결 전략 1 - 메트릭 분리**: HPA는 Custom Metrics(RPS, 큐 길이, 레이턴시 등 비즈니스 메트릭)로 동작시키고, VPA는 CPU/메모리 기반으로 동작시킨다. HPA가 CPU를 보지 않으므로 VPA의 리소스 조정과 충돌하지 않는다. 이 방식이 가장 깔끔하지만, Prometheus Adapter 등 Custom Metrics 인프라가 필요하다.

- **해결 전략 2 - VPA Off 모드**: VPA를 `updateMode: "Off"`로 설정하여 추천값만 계산하고, 실제 적용은 운영자가 수동으로 한다. 주기적으로(예: 주 1회) VPA 추천값을 확인하고, Deployment의 requests/limits를 수동으로 업데이트한다. 이 방식이 가장 안전하며, 대부분의 프로덕션 환경에서 권장된다.

- **해결 전략 3 - 컨테이너 분리**: 멀티컨테이너 Pod에서 HPA는 메인 컨테이너의 메트릭을, VPA는 사이드카 컨테이너(로그 수집기, 프록시 등)의 리소스를 관리하도록 분리한다. 사이드카의 리소스 변경으로 Pod가 재시작되더라도, HPA의 메트릭 판단에는 영향을 주지 않는다.

- **Kubernetes 1.27+ In-Place Resource Resize**: 이 기능이 GA가 되면 VPA가 Pod를 재시작하지 않고도 리소스를 변경할 수 있게 된다. 재시작으로 인한 연쇄 반응은 사라지지만, HPA와 VPA가 같은 메트릭을 보고 동시에 반응하는 근본적인 충돌은 여전히 남는다.

**심화 질문**: Google의 Multidimensional Pod Autoscaler(MPA)는 HPA와 VPA를 통합하여 수평/수직 스케일링을 동시에 수행한다. MPA가 두 스케일링 방향을 어떻게 조율하며, 오픈소스 Kubernetes에서 유사한 기능을 구현하려면 어떤 접근이 필요한가?

---

## Q3: KEDA가 HPA 위에서 동작하는 구조

**질문**: KEDA는 자체 스케일링 엔진을 가지고 있는가, 아니면 기존 HPA를 활용하는가? KEDA의 내부 동작 구조를 설명하라.

**핵심 포인트**:

- **KEDA는 HPA를 생성하고 관리한다**: KEDA는 자체 스케일링 엔진이 아니라, Kubernetes 네이티브 HPA 위에서 동작하는 "메타 스케일러"다. 사용자가 `ScaledObject`를 생성하면, KEDA Operator가 자동으로 해당 Deployment에 대한 HPA를 생성한다. 즉, ScaledObject → KEDA Operator → HPA → Deployment 순서로 스케일링이 전달된다. 이는 Kubernetes의 기존 오토스케일링 메커니즘을 재사용하므로, 안정성과 호환성이 보장된다.

- **이벤트 소스 → External Metrics API**: KEDA Metrics Server는 이벤트 소스(Kafka, RabbitMQ, SQS 등)에서 메트릭을 가져와 Kubernetes External Metrics API(`external.metrics.k8s.io`)로 노출한다. KEDA가 생성한 HPA는 이 External Metrics API에서 메트릭을 조회한다. 기존 HPA + Prometheus Adapter 조합과 비교하면, KEDA는 Prometheus를 거치지 않고 이벤트 소스에서 직접 메트릭을 가져오므로 중간 단계가 줄어들고 설정이 간단하다.

- **0↔1 스케일링은 KEDA가 직접 처리**: HPA는 `minReplicas`를 0으로 설정할 수 없다. KEDA의 핵심 차별점은 이 제한을 우회하는 것이다. replica가 0일 때 이벤트가 감지되면, KEDA Operator가 직접 Deployment의 replica를 0→1로 설정한다. 이후 1→N 스케일링은 KEDA가 생성한 HPA가 담당한다. 반대로 N→0 스케일 다운 시에도 HPA가 N→1로 줄이고, KEDA Operator가 `cooldownPeriod` 경과 후 1→0으로 최종 축소한다.

- **ScaledObject vs ScaledJob**: `ScaledObject`는 Deployment/StatefulSet에 대한 장기 실행 워크로드 스케일링에, `ScaledJob`은 Kubernetes Job에 대한 배치 처리 스케일링에 사용한다. ScaledJob은 이벤트 수에 비례하여 Job을 생성하고, 처리 완료 후 Job이 자동으로 종료된다. 예를 들어 SQS 큐에 100개 메시지가 있으면 10개의 Job을 생성하여 병렬 처리한다.

- **Fallback 메커니즘**: KEDA는 이벤트 소스에 장애가 발생했을 때(예: Kafka 브로커 다운으로 Lag 조회 실패) `fallback` 설정으로 안전장치를 제공한다. `failureThreshold` 횟수만큼 연속 실패하면 `replicas` 값으로 고정한다. 이벤트 소스 장애로 replica가 0이 되어 서비스가 중단되는 것을 방지한다.

**심화 질문**: KEDA를 이미 HPA가 설정된 Deployment에 적용하면 어떻게 되는가? 기존 HPA와 KEDA가 생성하는 HPA가 충돌하는가? KEDA의 `transfer` 전략은 기존 HPA를 어떻게 인수하는가?

---

## Q4: Cluster Autoscaler의 노드 축소 시 Pod 퇴거 과정

**질문**: Cluster Autoscaler가 노드를 제거할 때, 해당 노드에 실행 중인 Pod는 어떤 과정을 거쳐 다른 노드로 이동하는가?

**핵심 포인트**:

- **축소 후보 선정**: CA는 10분간(`--scale-down-unneeded-time`) 리소스 사용률이 50% 미만(`--scale-down-utilization-threshold`)인 노드를 축소 후보로 선정한다. 여기서 "사용률"은 실제 사용량이 아니라 **requests의 합계**를 기준으로 한다. 노드의 requests 합계 / 노드의 Allocatable 리소스가 50% 미만이면 대상이 된다. 이는 중요한 차이점인데, 실제 CPU 사용량이 80%이더라도 requests 합계가 40%이면 축소 대상이 될 수 있다.

- **이동 가능성 검증**: CA는 후보 노드의 모든 Pod가 다른 노드로 재배치 가능한지 시뮬레이션한다. `kube-scheduler`의 로직을 복제하여, 각 Pod가 다른 노드에 배치될 수 있는지(리소스 여유, Node Selector, Affinity, Taints/Tolerations, PDB 준수) 확인한다. 하나라도 이동 불가능한 Pod가 있으면 해당 노드는 축소하지 않는다.

- **이동 불가 Pod의 조건**: (1) PodDisruptionBudget(PDB)을 위반하는 경우 — PDB의 `minAvailable` 미만으로 떨어짐. (2) Controller가 관리하지 않는 단독 Pod — `kubectl run`으로 만든 Pod, Deployment/StatefulSet에 속하지 않는 Pod. 이 Pod는 재생성할 주체가 없으므로 삭제하면 영구 소실된다. (3) 로컬 스토리지를 사용하는 Pod — `emptyDir` 제외, `hostPath`나 `local` PV 사용 시. (4) `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"` 어노테이션이 있는 Pod. (5) `kube-system` 네임스페이스의 Pod 중 Controller가 관리하지 않는 경우.

- **퇴거 실행 과정**: 축소가 결정되면 CA는 노드를 `cordon` 상태로 전환하여 새 Pod가 배치되지 않도록 한다(Unschedulable로 마킹). 그 다음 `drain`을 실행하여 해당 노드의 모든 Pod에 SIGTERM을 전송한다. Pod는 `terminationGracePeriodSeconds` 내에 정상 종료해야 하며, 그 시간이 지나면 SIGKILL로 강제 종료된다. Pod가 종료되면 ReplicaSet/Deployment Controller가 다른 노드에 새 Pod를 생성한다. 모든 Pod가 종료된 후 CA가 클라우드 API를 호출하여 노드 인스턴스를 삭제한다.

- **Graceful Shutdown 고려**: 처리 중인 요청이 유실되지 않으려면, 애플리케이션이 SIGTERM을 수신했을 때 (1) 새 요청 수신을 중단하고, (2) 진행 중인 요청을 완료한 후, (3) 종료해야 한다. `preStop` 훅에서 `sleep 5`를 추가하여 Service Endpoints에서 Pod IP가 제거되는 시간을 확보하는 패턴이 일반적이다. 이 5초 동안 kube-proxy가 iptables/IPVS 규칙을 업데이트하여 새 트래픽이 해당 Pod로 가지 않도록 한다.

- **스케일 다운 안전 장치**: `--scale-down-delay-after-add`는 새 노드가 추가된 직후 축소를 방지한다 (기본 10분). 노드가 추가되자마자 다시 제거되는 진동을 방지한다. `--scale-down-delay-after-delete`는 노드 삭제 직후 추가 삭제를 방지한다 (기본 scan-interval과 동일). `--max-graceful-termination-sec`는 Pod 종료 대기 최대 시간을 설정한다 (기본 600초).

**심화 질문**: Spot/Preemptible 인스턴스로 구성된 Node Group에서 클라우드 제공자가 인스턴스를 강제 회수(preemption)할 때와, CA가 자발적으로 노드를 축소할 때의 Pod 퇴거 과정에는 어떤 차이가 있는가? AWS Node Termination Handler의 역할은 무엇인가?

---

## Q5: CPU 사용률 기반 HPA의 한계와 Custom Metrics

**질문**: CPU 사용률 기반 HPA가 적합하지 않은 워크로드 유형은 무엇이며, 이를 대체하는 Custom Metrics를 선택하는 기준은 무엇인가?

**핵심 포인트**:

- **I/O 바운드 워크로드**: 데이터베이스 쿼리, 외부 API 호출, 파일 시스템 읽기/쓰기가 주요 작업인 서비스는 CPU 사용률이 낮지만 처리 지연이 발생한다. 예를 들어 외부 결제 API 호출에 2초가 걸리는 동안 스레드는 대기 상태이고 CPU는 거의 사용하지 않는다. HPA는 "CPU가 낮으니 스케일 아웃 불필요"라고 판단하지만, 동시 요청이 늘면 스레드 풀이 고갈되어 응답 시간이 급증한다.

- **메시지 큐 컨슈머**: Kafka, RabbitMQ 컨슈머는 메시지 처리 자체보다 메시지 대기(polling)에 더 많은 시간을 쓴다. CPU 사용률은 5~10%인데 Consumer Lag은 수만 건이 쌓일 수 있다. 이 경우 Consumer Lag(처리하지 못한 메시지 수)이 HPA 메트릭으로 적합하다. Kafka의 경우 파티션당 Lag을 기준으로 스케일링하면, 컨슈머 수가 파티션 수를 넘지 않도록 자연스럽게 제한된다.

- **메모리 기반 워크로드의 함정**: 캐시 서버, ML 추론 서비스처럼 메모리 사용량이 핵심인 워크로드에서 CPU 메트릭은 의미가 없다. 그러나 메모리 기반 HPA도 한계가 있다. 메모리는 CPU와 달리 "해제"가 느리다. JVM의 가비지 컬렉션은 즉시 메모리를 OS에 반환하지 않으므로, 트래픽이 줄어도 메모리 사용률은 여전히 높아 HPA가 스케일 다운하지 않는다. Go 언어의 메모리 해제도 유사하게 지연될 수 있다.

- **Custom Metrics 선택 기준**: 가장 좋은 메트릭은 "사용자 경험과 직접 연결되는 메트릭"이다. (1) **RPS(Requests Per Second)**: 웹 서비스에서 Pod당 처리할 수 있는 최대 RPS를 기준으로 스케일링. 부하 테스트로 Pod당 최대 RPS를 측정한 뒤, 그 80%를 임계값으로 설정한다. (2) **응답 시간(Latency P95/P99)**: SLA를 기준으로 P99 응답 시간이 500ms를 초과하면 스케일 아웃. 단, 외부 의존성(DB 지연)으로 인한 레이턴시 증가에는 스케일 아웃이 도움이 되지 않는다. (3) **큐 길이(Queue Length/Consumer Lag)**: 메시지 처리 워크로드에서 밀린 메시지 수 기준. (4) **동시 연결 수(Active Connections)**: WebSocket 서버 등에서 Pod당 동시 연결 수 기준.

- **다중 메트릭 HPA의 판단 로직**: 여러 메트릭을 동시에 HPA에 설정하면(예: CPU 50% AND RPS 1000), HPA는 각 메트릭에 대해 필요한 replica 수를 독립적으로 계산한 뒤 **가장 큰 값**을 채택한다. 즉, CPU는 3개면 충분하고 RPS는 7개가 필요하면 7개가 된다. 이는 "어떤 메트릭이든 과부하면 스케일 아웃"하는 안전한 전략이다.

**심화 질문**: External Metrics(클라우드 서비스 메트릭, 예: SQS Queue Length)와 Custom Metrics(클러스터 내부 Prometheus 메트릭)의 차이는 무엇인가? HPA에서 Object 타입 메트릭(특정 Kubernetes 오브젝트에 연결된 메트릭)은 어떤 시나리오에서 사용하는가?

---

## Q6: KEDA의 0→1 스케일링 지연과 Cold Start 문제

**질문**: KEDA가 replica를 0에서 1로 올리는 동안 발생하는 지연(Cold Start)은 어떻게 해결하는가?

**핵심 포인트**:

- **0→1 지연의 구성 요소**: KEDA가 이벤트를 감지하는 시간(`pollingInterval` 주기, 기본 30초) → KEDA Operator가 Deployment replica를 0→1로 변경 → `kube-scheduler`가 적절한 노드를 선택 → 컨테이너 이미지를 Pull (ImagePullPolicy에 따라 수초~수분) → 컨테이너가 시작되고 애플리케이션이 초기화(JVM 워밍업, DB 커넥션 풀 생성, 캐시 로딩) → Readiness Probe가 통과할 때까지 전체 지연이 발생한다. 최소 수십 초에서, 이미지 크기가 크거나 초기화가 오래 걸리는 경우 수 분까지 소요될 수 있다.

- **해결 전략 1 - minReplicaCount=1**: 완전한 0 스케일링 대신 최소 1개를 유지한다. 비용은 약간 증가하지만 Cold Start를 완전히 제거한다. 대기 중인 1개 Pod가 첫 요청을 즉시 처리하고, 부하가 증가하면 HPA가 1→N으로 확장한다. 비용 민감하지 않은 서비스, SLA가 엄격한 서비스에 적합하다.

- **해결 전략 2 - 이미지 최적화**: 컨테이너 이미지를 최소화(Alpine, distroless, scratch)하여 Pull 시간을 줄인다. 예를 들어 JDK 이미지(~300MB)를 JRE 이미지(~100MB)로 바꾸면 Pull 시간이 1/3로 줄어든다. 자주 사용하는 이미지는 노드에 미리 캐시(DaemonSet으로 pre-pull)하거나, `imagePullPolicy: IfNotPresent`로 설정하여 이미 캐시된 이미지를 재사용한다.

- **해결 전략 3 - 빠른 초기화 설계**: 애플리케이션 시작 시간을 최소화한다. Spring Boot의 `lazy-init=true`(빈 지연 초기화), GraalVM Native Image(밀리초 단위 시작), 데이터베이스 커넥션 풀의 `minimum-idle=0`(시작 시 커넥션 생성 생략) 등으로 초기화 비용을 줄인다. Go, Rust 같은 네이티브 컴파일 언어는 시작 시간이 밀리초 단위이므로 Cold Start 문제가 거의 없다.

- **해결 전략 4 - pollingInterval 최소화**: KEDA의 이벤트 감지 주기를 줄여(기본 30초 → 5~10초) 반응 시간을 단축한다. 단, 이벤트 소스에 대한 폴링 부하가 증가할 수 있으므로 이벤트 소스의 API Rate Limit을 확인해야 한다. Kafka의 경우 Consumer Group 오프셋 조회가 가벼운 작업이므로 5초도 문제없지만, AWS SQS는 API 호출 비용이 발생할 수 있다.

- **해결 전략 5 - Knative Serving 또는 KEDA HTTP Add-on**: HTTP 트래픽 기반이라면 Knative Serving의 Activator 또는 KEDA HTTP Add-on의 Interceptor가 0 replica 상태에서 들어오는 요청을 버퍼링하고, Pod가 Ready 상태가 되면 전달한다. 요청이 유실되지 않지만 첫 요청의 응답 시간이 길어진다 (Cold Start 시간만큼). 후속 요청은 이미 Pod가 실행 중이므로 정상 응답 시간이다.

**심화 질문**: Kubernetes의 "Ready-made Pods" 개념(사전에 Pod를 생성해두고 유휴 상태로 대기시키는 방식)은 Cold Start를 어떻게 해결하는가? OpenFaaS의 "idle function" 패턴과 KEDA의 0 스케일링 접근법은 어떻게 다른가?

---

## Q7: HPA의 스케일링 공식과 메트릭 집계 방식

**질문**: HPA가 "현재 3개 Pod, 평균 CPU 80%, 목표 50%"일 때 5개로 스케일 아웃하는 공식의 세부 동작을 설명하라. 개별 Pod의 CPU가 불균형할 때는 어떻게 계산되는가?

**핵심 포인트**:

- **기본 공식**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`. 여기서 `currentMetricValue`는 모든 Pod의 평균값이다. 3개 Pod가 각각 CPU 90%, 70%, 80%를 사용하면 평균은 80%이므로, `ceil[3 × (80/50)] = ceil[4.8] = 5`가 된다.

- **불균형 시나리오**: Pod A가 CPU 150%, Pod B가 30%, Pod C가 60%라면 평균은 80%이다. 이 평균값을 기준으로 5개로 스케일 아웃한다. 그러나 실제로는 Pod A가 과부하 상태이고 다른 Pod는 여유가 있다. HPA는 이런 불균형을 감지하지 못하고 단순 평균만 본다. 이 문제를 해결하려면 Pod의 리소스를 균등하게 분배하는 로드밸런서 설정이 필요하다.

- **Not Ready Pod 처리**: Ready 상태가 아닌 Pod(시작 중, 실패 중)는 메트릭 계산에서 제외된다. 단, `--horizontal-pod-autoscaler-initial-readiness-delay`(기본 30초) 이내의 새 Pod는 아직 메트릭이 없어도 Ready로 간주한다. 이는 새 Pod가 워밍업 중일 때 HPA가 "메트릭 없음 → 과부하"로 오판하여 추가 스케일 아웃하는 것을 방지한다.

- **Tolerance 범위**: HPA는 현재 비율이 목표의 ±10%(기본 `--horizontal-pod-autoscaler-tolerance=0.1`) 이내이면 스케일링을 수행하지 않는다. 즉, 목표 50%에서 실제 45~55%이면 변경하지 않는다. 이 허용 범위가 작은 수준의 메트릭 변동에 대한 진동을 방지한다.

- **다중 메트릭 판단**: 여러 메트릭이 설정되면 각각에 대해 desiredReplicas를 독립적으로 계산한 뒤, **최댓값**을 채택한다. CPU가 3개를 요구하고 메모리가 5개를 요구하면 5개가 된다. 이는 어느 하나의 메트릭이라도 과부하이면 스케일 아웃하는 안전한 전략이다.

- **Missing Metrics 처리**: 일부 Pod에서 메트릭이 수집되지 않으면(metrics-server 지연, Pod 네트워크 문제), HPA는 해당 Pod를 제외하고 나머지 Pod의 평균으로 계산한다. 단, 누락된 Pod의 비율이 높으면 HPA가 스케일링을 보류하고 이벤트에 경고를 기록한다. `kubectl describe hpa`에서 "unable to fetch metrics" 같은 메시지가 나타나면 metrics-server의 상태를 확인해야 한다.

**심화 질문**: HPA Controller의 `--horizontal-pod-autoscaler-sync-period`(기본 15초)를 5초로 줄이면 반응 속도가 빨라지지만, kube-apiserver에 대한 메트릭 조회 부하가 증가한다. 대규모 클러스터(수천 개 HPA)에서 이 주기를 조정할 때의 트레이드오프는 무엇인가?
