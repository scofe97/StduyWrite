---
title: Kubernetes 딥다이브 로드맵 — 섹션별 키워드 원문
tags: [moc, kubernetes, roadmap, keywords]
status: reference
related:
  - README.md
updated: 2026-06-25
---

# Kubernetes 딥다이브 로드맵 — 섹션별 키워드 원문

---

> "Deployment 를 작성할 줄 아는 개발자" 에서 "Pod 가 왜 뜨고, 왜 죽고, 왜 통신되고, 왜 배포가 멈추는지 설명할 수 있는 개발자" 로 가는 것이 목표입니다. 이 문서는 제공받은 Kubernetes 딥다이브 로드맵 원문을 **섹션별로 빠짐없이** 옮긴 기록입니다. 폴더·챕터 매핑과 갭은 [README.md](README.md) 가 맡고, 이 문서는 "각 섹션이 원래 무엇을 다루라고 했는가" 의 SSOT 입니다.

## 1. Kubernetes 딥다이브 전체 지도

깊게 판다면 아래 순서가 좋습니다.

```text
1. Kubernetes Architecture
2. Control Plane
3. Node Components
4. Pod Lifecycle
5. Workload Resources
6. Deployment / ReplicaSet
7. Scheduling
8. Service Discovery
9. Kubernetes Networking
10. Ingress / Gateway API
11. ConfigMap / Secret
12. Volume / PV / PVC / StorageClass
13. Resource Requests / Limits
14. Probe / Health Check
15. Rolling Update / Rollback
16. Autoscaling
17. RBAC / ServiceAccount
18. Security Context / Pod Security
19. NetworkPolicy
20. Admission Controller / Webhook
21. CRD / Custom Controller / Operator
22. Observability
23. Troubleshooting
24. Production 운영 패턴
```

한 문장으로 줄이면: 사용자는 원하는 상태를 API Server 에 선언하고, Control Plane 은 현재 상태와 원하는 상태를 비교하며, Scheduler 는 Pod 를 Node 에 배치하고, kubelet 은 컨테이너 런타임을 통해 Pod 를 실행하며, Service 와 CNI 는 네트워크를 이어주고, Controller 는 계속 상태를 맞춥니다.

## 2. Spring / Kubernetes 대응

| Spring | Kubernetes |
|--------|-----------|
| BeanDefinition | Manifest / Resource Spec |
| ApplicationContext | Cluster State / API Server |
| Bean 생성 | Pod 생성 |
| Bean Lifecycle | Pod Lifecycle |
| BeanPostProcessor | Admission Controller / Mutating Webhook |
| AOP Proxy / Weaving | Sidecar Injection / Admission Webhook |
| AutoConfiguration | Operator / Controller 자동 조정 |
| DispatcherServlet | API Server |
| @Transactional 상태 관리 | Controller Reconciliation |
| Actuator Health | Liveness / Readiness Probe |

Spring 이 객체의 생명주기를 관리한다면 Kubernetes 는 워크로드의 생명주기를 관리합니다.

## 3. 1단계: Kubernetes Architecture

반드시 알아야 할 것:

```text
Cluster
Control Plane
Worker Node
API Server
etcd
Scheduler
Controller Manager
Cloud Controller Manager
kubelet
kube-proxy
Container Runtime
CRI
CNI
CSI
```

핵심 질문: kubectl apply 를 하면 요청은 어디로 가는가 / YAML 은 어디에 저장되는가 / Scheduler 는 언제 개입하는가 / kubelet 은 무엇을 보고 Pod 를 실행하는가 / Pod 상태는 누가 API Server 에 보고하는가 / Controller 는 무엇을 계속 감시하는가.

내부 흐름: kubectl apply → API Server → Admission 단계 → etcd 저장 → Controller 감지 → ReplicaSet/Pod 생성 요청 → Scheduler 가 Node 결정 → kubelet 이 Pod 실행 → Container Runtime 이 Container 생성 → kubelet 이 상태 보고. 핵심은 Kubernetes 가 명령형 실행기가 아니라 선언형 상태 조정 시스템이라는 점입니다.

## 4. 2단계: Control Plane

- **API Server**: 모든 요청의 관문 · 인증/인가 · Admission 처리 · 리소스 검증 · etcd 와 통신 · watch API 제공
- **etcd**: 클러스터 상태 저장소 · 모든 리소스의 원천 데이터 · 백업/복구에서 가장 중요
- **Scheduler**: Node 미정 Pod 감지 · 조건에 맞는 Node 후보 계산 · 점수화 후 Node 선택
- **Controller Manager**: 원하는 상태와 현재 상태 비교 · Deployment·ReplicaSet·Node·Job 관리 · reconciliation 수행

깊게 볼 질문: API Server 가 죽으면 기존 Pod 는 죽는가 / etcd 가 손상되면 무엇을 잃는가 / Scheduler 가 멈추면 기존 Pod 는 어떻게 되는가 / Controller Manager 가 멈추면 Replica 복구가 되는가. 기존 Pod 는 Node 에서 계속 돌 수 있지만 Control Plane 이 흔들리면 새로운 결정과 상태 조정이 멈춥니다.

## 5. 3단계: Node Components

반드시 알아야 할 것:

```text
Node
kubelet
container runtime
containerd
CRI-O
kube-proxy
Pod sandbox
pause container
cgroup
namespace
image pull
container log
```

kubelet 역할: PodSpec 수신 · 컨테이너 런타임에 실행 요청 · Probe 수행 · Volume mount · Secret/ConfigMap mount · Pod 상태 보고 · Node 상태 보고.

실무 질문: Pod 가 Pending 이면 Scheduler 문제인가 이미지 문제인가 / Pod 가 ContainerCreating 에서 멈추면 무엇을 봐야 하는가 / Pod 가 Running 인데 Ready 가 아니면 무엇이 문제인가 / Node NotReady 가 되면 그 위 Pod 는 어떻게 되는가.

## 6. 4단계: Pod Lifecycle

반드시 알아야 할 것:

```text
Pod
Container
Init Container
Sidecar Container
Pod Phase
Container State
Restart Policy
PreStop Hook
PostStart Hook
Termination Grace Period
Readiness Gate
```

Pod Phase: Pending · Running · Succeeded · Failed · Unknown. Container State: Waiting · Running · Terminated.

실무 질문: Pod 가 Pending 인 이유 / ImagePullBackOff 는 왜 발생하는가 / CrashLoopBackOff 는 어떤 흐름으로 발생하는가 / OOMKilled 는 Java OOM 과 어떻게 다른가 / Pod 종료 시 Spring Boot graceful shutdown 이 동작하는가.

Spring Boot 연결: SIGTERM 수신 → graceful shutdown 시작 → 새 요청 거부 → 처리 중 요청 마무리 → Kafka consumer 종료 → 종료 시간 안에 프로세스 종료 → Pod 제거. `terminationGracePeriodSeconds` 가 너무 짧으면 애플리케이션이 문을 일찍 닫아야 합니다.

## 7. 5단계: Workload Resources

반드시 알아야 할 것: Pod · ReplicaSet · Deployment · StatefulSet · DaemonSet · Job · CronJob.

| 리소스 | 용도 |
|--------|------|
| Pod | 가장 작은 실행 단위 |
| ReplicaSet | 동일 Pod 개수 유지 |
| Deployment | 무상태 애플리케이션 배포/롤링 업데이트 |
| StatefulSet | 안정적인 이름/스토리지가 필요한 상태ful 앱 |
| DaemonSet | 모든/일부 Node 마다 Pod 하나씩 실행 |
| Job | 끝나는 작업 실행 |
| CronJob | 주기적 Job 실행 |

## 8. 6단계: Deployment / ReplicaSet 딥다이브

알아야 할 것:

```text
Deployment
ReplicaSet
Pod Template
Selector
Revision
RollingUpdate
Recreate
maxSurge
maxUnavailable
rollout status
rollout history
rollout undo
```

내부 흐름: Deployment 생성 → Deployment Controller 가 ReplicaSet 생성 → ReplicaSet Controller 가 Pod 생성 → Scheduler 가 Node 배치 → kubelet 이 Pod 실행.

실무 질문: Deployment selector 를 바꾸면 왜 위험한가 / Pod template 이 바뀌면 왜 새 ReplicaSet 이 생기는가 / maxSurge 와 maxUnavailable 은 배포 중 가용성에 어떤 영향을 주는가 / rollout 이 멈추면 어디서 원인을 봐야 하는가.

자주 보는 장애: ProgressDeadlineExceeded · ImagePullBackOff · CrashLoopBackOff · Readiness probe failed · Insufficient cpu · Insufficient memory · FailedScheduling.

## 9. 7단계: Scheduling

반드시 알아야 할 것:

```text
nodeSelector
nodeAffinity
podAffinity
podAntiAffinity
taints
tolerations
topologySpreadConstraints
resource requests
PriorityClass
preemption
```

실무 질문: 왜 Pod 가 Pending 인가 / Node 자원이 부족한가 / taint 를 toleration 하지 못했는가 / node affinity 조건이 너무 강한가 / PVC 가 특정 zone 에 묶여 있는가.

`kubectl describe pod` Events 에서 볼 것: FailedScheduling · `0/3 nodes are available` · Insufficient cpu · `node(s) had untolerated taint` · volume node affinity conflict.

## 10. 8단계: Service Discovery

Pod IP 는 바뀔 수 있어 Service 가 필요합니다.

반드시 알아야 할 것:

```text
Service
ClusterIP
NodePort
LoadBalancer
ExternalName
EndpointSlice
label selector
kube-proxy
iptables
IPVS
CoreDNS
```

핵심 흐름: Client → Service DNS → ClusterIP → kube-proxy rule → EndpointSlice → 실제 Pod IP.

실무 질문: Service 는 있는데 Endpoint 가 비어 있지는 않은가 / selector 가 Pod label 과 맞는가 / Pod 는 Running 이지만 Ready 가 아니라 Endpoint 에서 제외된 것은 아닌가 / DNS 가 안 풀리는가 연결이 안 되는가.

확인 명령: `kubectl get svc` · `get endpoints` · `get endpointslice` · `get pod --show-labels` · `describe svc <name>`.

## 11. 9단계: Kubernetes Networking

반드시 알아야 할 것:

```text
Pod-to-Pod Network
Pod-to-Service Network
Node-to-Pod Network
Cluster DNS
CNI
kube-proxy
iptables
IPVS
Overlay Network
Underlay Network
NAT
SNAT
DNAT
NetworkPolicy
Ingress
Gateway API
```

기본 원칙: Pod 는 고유 IP 를 가진다 · Pod 간 통신은 NAT 없이 가능해야 한다 · Node 는 Pod 와 통신할 수 있어야 한다 · Service 는 안정적인 가상 IP 를 제공한다.

실무 질문: Pod 안에서 외부 API 호출이 안 되는가 / Service 이름으로 DNS 조회가 안 되는가 / 같은 Namespace 와 다른 Namespace DNS 이름은 무엇이 다른가 / NodePort 와 LoadBalancer 는 어디서 트래픽을 받는가 / NetworkPolicy 때문에 막힌 것은 아닌가.

Spring 개발자 관점: `http://payment-service:8080` 또는 `http://payment-service.default.svc.cluster.local:8080` 이름이 단순 문자열이 아니라 CoreDNS·Service·EndpointSlice·kube-proxy 규칙 위에 서 있습니다.

## 12. 10단계: Ingress / Gateway API

Ingress: Ingress · IngressClass · Ingress Controller · Host-based Routing · Path-based Routing · TLS Termination · Rewrite · Rate Limit.

Gateway API: Gateway · GatewayClass · HTTPRoute · TCPRoute · GRPCRoute · ReferenceGrant.

실무 질문: Ingress 리소스만 만들고 Ingress Controller 가 없는 것은 아닌가 / TLS 인증서는 어디서 관리하는가 / Path rewrite 때문에 Spring context path 와 충돌하지 않는가 / Gateway API 로 역할을 더 명확히 나눌 수 있는가.

## 13. 11단계: ConfigMap / Secret

반드시 알아야 할 것:

```text
ConfigMap
Secret
env
envFrom
volume mount
projected volume
immutable config
rollout restart
External Secrets
Sealed Secrets
```

실무 질문: 설정 변경 시 Pod 가 자동 재시작되는가 / Secret 을 환경 변수로 넣을 것인가 파일로 mount 할 것인가 / Spring Boot application.yml 과 Kubernetes ConfigMap 을 어떻게 나눌 것인가 / 운영 Secret 이 Git 에 평문으로 남아 있지는 않은가.

## 14. 12단계: Storage / PV / PVC

반드시 알아야 할 것:

```text
Volume
emptyDir
hostPath
PersistentVolume
PersistentVolumeClaim
StorageClass
Dynamic Provisioning
AccessMode
ReclaimPolicy
CSI
StatefulSet VolumeClaimTemplate
```

실무 질문: Pod 가 재시작되어도 데이터가 남아야 하는가 / PVC 가 Pending 이면 StorageClass 문제인가 / ReadWriteOnce 와 ReadWriteMany 차이를 이해했는가 / StatefulSet 에서 Pod 이름과 PVC 가 어떻게 연결되는가.

주의: 일반 Spring API 서버는 대부분 상태(업로드 파일·임시 파일·로그 파일·세션·캐시)를 Pod 안에 저장하면 안 됩니다 — Pod 가 사라지면 함께 사라집니다.

## 15. 13단계: Resource Requests / Limits

반드시 알아야 할 것:

```text
requests.cpu
requests.memory
limits.cpu
limits.memory
QoS Class
Guaranteed
Burstable
BestEffort
OOMKilled
CPU throttling
cgroup
```

실무 질문: requests 가 없어서 스케줄링이 불안정하지 않은가 / memory limit 이 너무 낮아 OOMKilled 가 나지 않는가 / Java Xmx 가 container memory limit 과 맞는가 / CPU limit 때문에 latency 가 튀지는 않는가.

Java 앱: container memory limit > JVM heap + metaspace + thread stack + direct memory + native memory + margin. `-Xmx` 만 보고 안심하면 안 됩니다 — JVM 은 힙 밖에서도 메모리를 씁니다.

## 16. 14단계: Probe / Health Check

반드시 알아야 할 것:

```text
livenessProbe
readinessProbe
startupProbe
httpGet
tcpSocket
exec
initialDelaySeconds
periodSeconds
timeoutSeconds
failureThreshold
successThreshold
```

| Probe | 의미 |
|-------|------|
| startupProbe | 앱이 처음 뜨는 중인지 확인 |
| readinessProbe | 트래픽 받을 준비가 됐는지 확인 |
| livenessProbe | 살아 있는지 확인, 실패하면 재시작 |

Spring Boot 연결: readiness 는 `/actuator/health/readiness`, liveness 는 `/actuator/health/liveness`.

실무 질문: DB 가 잠깐 느리다고 liveness 가 실패해 Pod 를 죽이고 있지는 않은가 / readiness 와 liveness 를 같은 기준으로 보고 있지는 않은가 / 부팅이 느린 앱에 startupProbe 없이 liveness 를 걸고 있지는 않은가. 가장 흔한 실수는 liveness 를 너무 엄격하게 잡는 것입니다.

## 17. 15단계: Security / RBAC

반드시 알아야 할 것:

```text
Authentication
Authorization
RBAC
Role
RoleBinding
ClusterRole
ClusterRoleBinding
ServiceAccount
Token
SecurityContext
Pod Security
runAsNonRoot
readOnlyRootFilesystem
allowPrivilegeEscalation
capabilities
```

실무 질문: Pod 가 default ServiceAccount 를 그대로 쓰고 있지는 않은가 / ServiceAccount 권한이 과도하지 않은가 / 컨테이너가 root 로 실행되고 있지는 않은가 / hostPath·privileged·hostNetwork 를 남용하고 있지는 않은가. 운영에서는 "잘 뜬다" 보다 "너무 많은 권한으로 뜨지 않는다" 가 중요합니다.

## 18. 16단계: NetworkPolicy

반드시 알아야 할 것:

```text
NetworkPolicy
podSelector
namespaceSelector
ipBlock
ingress
egress
default deny
CNI 지원 여부
```

실무 질문: 기본적으로 모든 Pod 가 서로 통신 가능한 상태인가 / 결제 서비스는 주문 서비스에서만 접근 가능해야 하는가 / DB 접근은 특정 Namespace 에서만 허용해야 하는가 / egress 까지 제한할 것인가.

대표 패턴: default deny all → 필요한 ingress 만 허용 → 필요한 egress 만 허용. 단, NetworkPolicy 는 CNI 플러그인이 지원해야 실제로 동작합니다.

## 19. 17단계: Admission Controller / Webhook

반드시 알아야 할 것:

```text
Admission Controller
MutatingAdmissionWebhook
ValidatingAdmissionWebhook
AdmissionReview
Policy
OPA Gatekeeper
Kyverno
Sidecar Injection
Image Policy
Resource Policy
```

Mutating Webhook: Pod 생성 요청 → Webhook 이 PodSpec 수정 → sidecar 추가 · label/annotation 추가 · securityContext 주입. 예: Istio sidecar injection · OpenTelemetry agent injection · 공통 env/volume 주입.

Validating Webhook: Pod 생성 요청 → 정책 검사 → 조건 위반 시 거부. 예: latest image tag 금지 · resources.requests 필수 · root user 실행 금지 · 특정 registry 만 허용.

| Spring | Kubernetes |
|--------|-----------|
| BeanPostProcessor | Mutating Admission Webhook |
| Validation | Validating Admission Webhook |
| AOP 부가기능 삽입 | Sidecar Injection |
| AutoConfiguration | Operator / Controller |
| Proxy 로 감싸기 | PodSpec 수정 또는 sidecar 삽입 |

## 20. 18단계: CRD / Custom Controller / Operator

반드시 알아야 할 것:

```text
CRD
Custom Resource
Controller
Operator
Reconciliation Loop
Informer
Watch
Work Queue
Finalizer
OwnerReference
Garbage Collection
Status Subresource
```

핵심 구조: 사용자가 MyApp 리소스 생성 → API Server 가 MyApp 저장 → Custom Controller 가 MyApp watch → 원하는 상태 확인 → Deployment/Service/ConfigMap 생성 → status 업데이트.

실무 질문: 왜 Kubernetes 는 Controller 패턴을 쓰는가 / 원하는 상태와 현재 상태는 어디에 있는가 / Controller 가 중간에 죽으면 어떻게 복구되는가 / Finalizer 는 언제 필요한가 / Operator 는 단순 자동화 스크립트와 무엇이 다른가. 여기까지 가면 Kubernetes 를 사용하는 사람이 아니라 그 위에 플랫폼을 만드는 사람에 가까워집니다.

## 21. 19단계: Observability

반드시 알아야 할 것:

```text
kubectl logs
kubectl describe
kubectl events
metrics-server
Prometheus
Grafana
Loki
Tempo
OpenTelemetry
kube-state-metrics
node-exporter
cAdvisor
Alertmanager
```

봐야 할 지표: Pod restart count · Pod ready status · CPU usage · CPU throttling · Memory usage · OOMKilled count · Network RX/TX · PVC usage · Node condition · Deployment available replicas · HPA scaling event · API Server latency · etcd latency.

Spring Boot 기준: HTTP request latency · JVM memory · GC pause · Thread count · HikariCP connection usage · Kafka consumer lag · Error rate · Readiness state.

실무 질문: Pod 가 재시작된 이유를 알 수 있는가 / 장애 시 이벤트·로그·메트릭·트레이스를 연결할 수 있는가 / Deployment rollout 실패를 Alert 로 받을 수 있는가 / OOMKilled 와 애플리케이션 예외를 구분할 수 있는가.

## 22. 20단계: Troubleshooting

자주 보는 상태:

```text
Pending
ContainerCreating
ImagePullBackOff
ErrImagePull
CrashLoopBackOff
RunContainerError
CreateContainerConfigError
OOMKilled
Evicted
Terminating
NodeNotReady
```

기본 루틴: `kubectl get pod -o wide` · `describe pod <pod>` · `logs <pod>` · `logs <pod> --previous` · `get events --sort-by=.lastTimestamp` · `describe node <node>` · `get svc,endpoints,endpointslice` · `top pod` · `top node`.

| 증상 | 의심 지점 |
|------|----------|
| Pending | 스케줄링 실패, 자원 부족, taint, PVC |
| ImagePullBackOff | 이미지 이름, 태그, registry 인증 |
| CrashLoopBackOff | 앱 부팅 실패, 설정 오류, 의존 서비스 장애 |
| Running but NotReady | readiness probe 실패 |
| OOMKilled | memory limit 부족, JVM 설정 문제 |
| Service 연결 실패 | selector, endpoint, DNS, NetworkPolicy |
| Ingress 404 | host/path rule, ingress class, backend service |
| Terminating 지연 | finalizer, preStop, grace period |

## 23. Spring Boot 개발자 기준 Kubernetes 체크리스트

```text
Deployment
Service
ConfigMap
Secret
Ingress or Gateway
Readiness Probe
Liveness Probe
Startup Probe
Resource Requests
Resource Limits
Graceful Shutdown
terminationGracePeriodSeconds
Rolling Update Strategy
HPA
PodDisruptionBudget
SecurityContext
ServiceAccount
NetworkPolicy
Actuator Health
Prometheus Metrics
Structured Logging
Trace ID
```

## 24. 추천 프로젝트

- **프로젝트 1 — Spring Boot on Kubernetes Production Template**: Deployment · Service · Ingress · ConfigMap · Secret · Probe · Resource requests/limits · Graceful shutdown · SecurityContext · HPA · PDB · Prometheus scraping.
- **프로젝트 2 — Kubernetes Troubleshooting Lab**: ImagePullBackOff · CrashLoopBackOff · Readiness probe failed · OOMKilled · Pending(insufficient cpu) · Service selector mismatch · NetworkPolicy block · Ingress path mismatch · PVC Pending 을 일부러 만들고 (증상→kubectl 결과→원인→해결→재발 방지) 로 정리.
- **프로젝트 3 — Spring Boot + ConfigMap/Secret Reload Lab**: 환경 변수 주입 · ConfigMap volume mount · Secret mount · Pod 재시작 필요 여부 · rollout restart · Spring Cloud Kubernetes 검토.
- **프로젝트 4 — Kubernetes Networking Lab**: Pod-to-Pod · Service DNS · Namespace 간 통신 · Ingress routing · NetworkPolicy default deny · 특정 app 만 DB 접근 허용.
- **프로젝트 5 — Mini Operator**: SpringApp CRD → Controller 가 Deployment·Service·ConfigMap·Ingress·HPA 자동 생성. CRD · Controller · Reconciliation · OwnerReference · Status · Finalizer.

## 25. 딥다이브 학습 순서 (6단계)

1단계 기본 리소스: Pod · Deployment · ReplicaSet · Service · ConfigMap · Secret · Namespace → "Spring Boot 앱을 올리고 내부 Service 로 접근할 수 있다".

2단계 운영 배포: Probe · Resource requests/limits · RollingUpdate · Rollback · HPA · PDB · SecurityContext → "안전하게 배포하고 죽지 않게 운영할 수 있다".

3단계 네트워크: Service · EndpointSlice · CoreDNS · Ingress · Gateway API · NetworkPolicy · CNI → "트래픽 흐름을 설명하고 연결 장애를 추적할 수 있다".

4단계 내부 구조: API Server · etcd · Scheduler · Controller Manager · kubelet · container runtime · kube-proxy → "Pod 생성 전체 흐름을 Control Plane 부터 Node 까지 설명할 수 있다".

5단계 확장: Admission Webhook · CRD · Custom Controller · Operator · Finalizer · OwnerReference → "Kubernetes 위에 우리 팀만의 플랫폼 리소스를 만들 수 있다".

6단계 운영/장애: Observability · Events · Logs · Metrics · Tracing · Troubleshooting · Backup · Upgrade · Security → "장애가 났을 때 감이 아니라 증거로 원인을 좁힐 수 있다".

## 26. 최종 압축 키워드

```text
Kubernetes Architecture
Control Plane
API Server
etcd
Scheduler
Controller Manager
Node
kubelet
container runtime
CRI
CNI
CSI
kube-proxy
Pod
Pod Lifecycle
Init Container
Sidecar Container
Restart Policy
Deployment
ReplicaSet
StatefulSet
DaemonSet
Job
CronJob
Service
ClusterIP
NodePort
LoadBalancer
EndpointSlice
CoreDNS
Ingress
Ingress Controller
Gateway API
ConfigMap
Secret
Volume
PersistentVolume
PersistentVolumeClaim
StorageClass
Resource Requests
Resource Limits
QoS Class
OOMKilled
CPU Throttling
Liveness Probe
Readiness Probe
Startup Probe
Rolling Update
Rollback
HPA
VPA
Cluster Autoscaler
PodDisruptionBudget
nodeSelector
Node Affinity
Pod Affinity
Taints
Tolerations
Topology Spread Constraints
RBAC
ServiceAccount
Role
RoleBinding
ClusterRole
ClusterRoleBinding
SecurityContext
Pod Security
NetworkPolicy
Admission Controller
Mutating Webhook
Validating Webhook
Sidecar Injection
CRD
Custom Resource
Custom Controller
Operator
Reconciliation Loop
Informer
Watch
Finalizer
OwnerReference
Garbage Collection
Helm
Kustomize
kubectl
k9s
Prometheus
Grafana
Loki
OpenTelemetry
kube-state-metrics
Troubleshooting
```

## 출처

- [Overview](https://kubernetes.io/docs/concepts/overview/)
- [Cluster Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)
- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Workloads](https://kubernetes.io/docs/concepts/workloads/)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
- [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Cluster Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/)
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Security](https://kubernetes.io/docs/concepts/security/)
- [NetworkPolicy](https://kubernetes.io/docs/reference/kubernetes-api/networking/network-policy-v1/)
