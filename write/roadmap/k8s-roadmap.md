---
title: Kubernetes 학습 로드맵
tags: [roadmap, kubernetes, k8s, cloud-native, operations, security, eks, iac]
status: final
source:
  - ../08_cloud/kubernetes/README.md
  - ../08_cloud/book/kubernetes-in-action/README.md
related:
  - README.md
  - os-roadmap.md
  - network-roadmap.md
  - observability-roadmap.md
  - ../08_cloud/kubernetes/README.md
updated: 2026-09-23
---

# Kubernetes 학습 로드맵
---

> 오브젝트를 선언하는 데서 시작해 워크로드·연결·자원으로 넓힌 뒤 클러스터 내부와 확장·운영으로 들어갑니다. 개념이 주인공이고 책은 그 개념을 다루는 자리입니다.

## 학습 순서

> 단계마다 배우는 개념을 묶음으로 갈랐습니다. 자료 위치는 아래 단계별 표가 짚습니다.

![오브젝트 선언에서 클러스터 운영까지 이어지는 Kubernetes 학습 순서](_assets/k8s-roadmap.svg)

| 단계 | 묶음 | 배우는 개념 |
|---|---|---|
| 1 · 오브젝트 | API 모델 | API resource · 매니페스트 · `metadata` · `spec` · `status` · kubectl 기본 조회 |
| 1 · 오브젝트 | Pod 생애주기 | Pod · 컨테이너 그룹화 · 사이드카 · phase · conditions · 컨테이너 상태 · restart 정책 |
| 1 · 오브젝트 | 건강 확인 | liveness probe · readiness probe · startup probe · lifecycle hook · 종료 흐름 |
| 1 · 오브젝트 | 조직화 | namespace · label · label selector · field selector · annotation |
| 1 · 오브젝트 | 설정 주입 | `command` · `args` · 환경변수 · ConfigMap · Secret · Downward API · projected volume |
| 2 · 워크로드 | 무상태 | ReplicaSet · reconciliation · 소유 관계 · Deployment · pod-template-hash |
| 2 · 워크로드 | 갱신과 되돌림 | RollingUpdate · Recreate · `maxSurge` · `maxUnavailable` · pause · rollback · 배포 전략 다섯 |
| 2 · 워크로드 | 상태와 노드 | StatefulSet · ordinal · headless Service · retention · DaemonSet · hostNetwork · hostPort |
| 2 · 워크로드 | 배치 작업 | Job · CronJob · 병렬 · 완료 모드 · work queue · suspend |
| 2 · 워크로드 | 컨테이너 구조 패턴 | init container · sidecar · adapter · ambassador |
| 3 · 연결 | 서비스 추상화 | Service · ClusterIP · 세션 어피니티 · NodePort · LoadBalancer · 트래픽 정책 |
| 3 · 연결 | 엔드포인트와 이름 | Endpoint · EndpointSlice · readiness 연동 · 클러스터 DNS · Service FQDN · 토폴로지 |
| 3 · 연결 | 외부 진입 | Ingress · IngressClass · TLS · Gateway API · HTTPRoute · 필터 · 크로스 네임스페이스 |
| 3 · 연결 | 새 확장 | Gateway API Inference Extension · `InferencePool` · Endpoint Picker |
| 4 · 자원과 저장 | 자원 요구 | requests · limits · QoS · LimitRange · ResourceQuota |
| 4 · 자원과 저장 | 배치와 중단 | taint · toleration · affinity · 토폴로지 분산 · PDB · PriorityClass · eviction |
| 4 · 자원과 저장 | 볼륨 | Volume · emptyDir · hostPath · projected · PV · PVC · StorageClass · 동적 프로비저닝 |
| 4 · 자원과 저장 | 저장 운영 | CSI · access mode · reclaim policy · 리사이즈 · 스냅샷 · ephemeral volume |
| 4 · 자원과 저장 | 확장 | HPA · VPA · Cluster Autoscaler · KEDA · metrics-server · custom metric |
| 5 · 내부 구조 | Control Plane | API Server · etcd · Scheduler · Controller Manager · kubelet |
| 5 · 내부 구조 | 노드 인터페이스 | CRI · CNI · CSI · containerd · 조정 루프 · watch · informer |
| 5 · 내부 구조 | 컨트롤러 | List·Watch · resourceVersion · 410 Gone · level-driven 과 edge-driven · GVK · Scheme · upsert 의미 |
| 5 · 내부 구조 | 감시 부품 | Reflector · DeltaFIFO · Indexer · Lister · SharedInformer · resync · 캐시 웜업 · 페이지네이션 |
| 5 · 내부 구조 | 접근 통제 | authentication · authorization · admission · TLS · PKI · 인증서 수명 |
| 5 · 내부 구조 | 상태 저장소 | etcd quorum · Raft · 백업 · 복구 · 클러스터 업그레이드 |
| 6 · 보안과 확장 | 권한 | RBAC · Role · ClusterRole · RoleBinding · ServiceAccount · SelfSubjectAccessReview · 권한 기반 기능 노출 |
| 6 · 보안과 확장 | API 접근 하드닝 | anonymous 인증 · SA 토큰 자동 마운트 |
| 6 · 보안과 확장 | 실행 권한 | SecurityContext · capability · seccomp · AppArmor · Pod Security Standards 세 등급 · Pod Security Admission |
| 6 · 보안과 확장 | 네트워크 분할 | NetworkPolicy |
| 6 · 보안과 확장 | 비밀과 공급망 | Secret 관리 · 저장 암호화 · KMS provider · 외부 저장소 · SBOM · 이미지 서명 · 공급망 보안 |
| 6 · 보안과 확장 | 클라우드 경계 | IRSA · EKS Pod Identity · EKS 봉투 암호화 · 제어부 로깅 |
| 6 · 보안과 확장 | 위협과 점검 | 위협 모델 · 공격 체인 · 횡적 이동 · CIS Benchmark · kube-bench · KISA 클라우드 취약점 점검 가이드 |
| 6 · 보안과 확장 | 감시와 탐지 | 감사 로그 · audit policy · Falco · Tetragon · 탐지와 강제의 차이 |
| 6 · 보안과 확장 | 확장 지점 | CRD · custom resource · controller · Operator · finalizer · OwnerReference · controller-runtime · status subresource |
| 6 · 보안과 확장 | 정책 | 어드미션 웹훅 · OPA · Gatekeeper · Kyverno · ValidatingAdmissionPolicy |
| 7 · 운영 | 증상 좁히기 | 이벤트 · 로그 · 지표를 한 시간축에 · kubectl 고급 조회 · JSONPath · ephemeral container · `kubectl debug` |
| 7 · 운영 | 자원 장애 | OOMKilled · exit code 137 · CPU throttling · node pressure · eviction |
| 7 · 운영 | 종료와 복구 | SIGTERM · PID 1 · PreStop · `terminationGracePeriodSeconds` · PDB · NodeNotReady · OS 자동 업데이트 |
| 7 · 운영 | 배포 도구 | Helm · Kustomize · GitOps · ArgoCD · App of Apps · ApplicationSet |
| 7 · 운영 | 클러스터를 코드로 | IaC · Immutable Infrastructure · Terraform state · module · 비밀 관리 · IaC 정책 검사 |
| 7 · 운영 | 멀티테넌시 | 멀티테넌시 · 가상 컨트롤 플레인 · 이름 변환과 충돌 회피 · status back-sync |
| 7 · 운영 | 멀티클러스터 | 멀티클러스터 세 모델 · 서비스 메시를 쓸 것인가 · OpenShift |



## 자료 읽기 흐름

> 위 단계를 무엇으로 배우는가입니다. 책과 문서를 한 표에 두고, 자료마다 어느 단계에 쓰이는지와 읽을 범위를 적습니다.

![Kubernetes 자료 읽기 흐름 — 우선순위와 읽을 범위](_assets/k8s-books.svg)

《Kubernetes in Action》 은 클러스터를 띄우는 3장만 빼고 통독하고, 나머지는 표의 `읽을 범위`만 봅니다. 문서는 6단계 보안과 EKS 처럼 소장본에 장이 없거나 규격이 계속 바뀌는 자리를 맡습니다.

| 자료 | 종류 | 읽을 범위 | 우선순위 | 자리 |
|---|:---:|---|:---:|---|
| [Kubernetes in Action](../08_cloud/book/kubernetes-in-action/README.md) | 책 | 1·2 · 4~18장 | 필수 | 1~5단계 |
| [Kubernetes Patterns](../08_cloud/book/kubernetes-patterns/README.md) | 책 | 2~9 · 12·13 · 15~24장 | 추천 | 1~4 · 6단계 |
| [Networking and Kubernetes](../08_cloud/book/networking-and-kubernetes/README.md) | 책 | 4·5장 | 추천 | 3단계 |
| Production Kubernetes | 책 | 3~10 · 12·13장 | 추천 | 4~7단계 |
| Programming Kubernetes | 책 | 1~6 · 9장 | 추천 | 5·6단계 |
| [Container Security](../08_cloud/book/container-security/README.md) | 책 | 1~4 · 8·9 · 13장 | 추천 | 6단계 |
| CKS Study Guide | 책 | 2~7장 | 추천 | 6단계 |
| Kubernetes Best Practices | 책 | 3·4 · 8~12 · 17·18장 | 추천 | 6·7단계 |
| [Kubernetes: Up and Running](../08_cloud/book/kubernetes-up-and-running/README.md) | 책 | 4 · 7 · 14~21장 | 추천 | 1 · 3~7단계 |
| Terraform Up and Running | 책 | 1·3·4·6장 | 추천 | 7단계 |
| Policy as Code | 책 | 4·5 · 7·8 · 11·12 · 14장 | 선택 | 6·7단계 |
| Learning eBPF | 책 | 9장 | 선택 | 6단계 |
| Kubernetes 보안 문서 묶음 | 문서 | [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) · [Security Checklist](https://kubernetes.io/docs/concepts/security/security-checklist/) · [Auditing](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/) · [Encrypting Confidential Data at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) | 추천 | 6단계 |
| [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes) | 문서 | Control Plane · Worker 항목 · 점검 도구 [kube-bench](https://github.com/aquasecurity/kube-bench) | 추천 | 6단계 |
| KISA 클라우드 취약점 점검 가이드 | 문서 | 2024년 6월판 2.26 Docker · 2.27 Master · 2.28 Worker 절 | 선택 | 6단계 |
| 런타임 탐지 문서 | 문서 | [Falco](https://falco.org/docs/) · [Tetragon](https://tetragon.io/docs/) | 선택 | 6단계 |
| [EKS Best Practices for Security](https://docs.aws.amazon.com/eks/latest/best-practices/security.html) | 문서 | 가이드 전편 · [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) · [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html) · [envelope encryption](https://docs.aws.amazon.com/eks/latest/userguide/envelope-encryption.html) · [control plane logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) | 추천 | 6단계 |

**보완 참조** — 단계 표의 노트나 책 칸이 가리키지만 읽기 흐름에는 넣지 않은 장입니다. 그 개념에 닿았을 때만 엽니다.

| 책 | 장 | 받치는 자리 |
|---|---|---|
| Kubernetes Patterns | 10·11 · 14 · 29장 | 2단계 Singleton·Stateless Service · 4단계 Self Awareness · HPA 의 노트 |
| Kubernetes Patterns | 25~28 · 30장 | 6단계 Secret · 저장 암호화 · RBAC · Controller·Operator 의 노트 · 이미지 빌드 |
| Container Security | 6·7 · 14장 | 6단계 공급망 보안 · CIS Benchmark 의 노트 |
| Infrastructure as Code | 11·21장 | 7단계 Immutable Infrastructure · IaC 정책 검사 |
| Operating OpenShift | 2·3장 | 7단계 OpenShift — 설치 방식 · Route · SCC |

KISA 가이드는 API server 비인증 접근 차단, etcd 암호화, kubelet 인증 같은 항목을 진단 기준과 조치 방법으로 적어 CIS Benchmark 와 같은 자리를 채웁니다.



## 클러스터를 쓰는 쪽 · 1~4단계

> 선언한 오브젝트가 어떻게 도는지를 봅니다. 클러스터를 직접 세우지 않아도 성립하는 구간입니다.

### 1단계 · 오브젝트

> 먼저: [OS 로드맵](os-roadmap.md) 3단계 namespace · cgroup v2

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| API resource · 매니페스트 · `metadata` · `spec` · `status` | 필수 | [API와 매니페스트](../08_cloud/book/kubernetes-in-action/04-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20API%EC%99%80%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EB%A7%A4%EB%8B%88%ED%8E%98%EC%8A%A4%ED%8A%B8%20%EA%B5%AC%EC%A1%B0.md) · [Node·Event 필드 실습](../08_cloud/book/kubernetes-in-action/04-02.Node%EC%99%80%20Event%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%ED%95%84%EB%93%9C%20%EC%8B%A4%EC%8A%B5.md) | Kubernetes in Action 4장 |
| Pod · 컨테이너 그룹화 · 사이드카 | 필수 | [Pod 이해](../08_cloud/book/kubernetes-in-action/05-01.Pod%20%EC%9D%B4%ED%95%B4%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B7%B8%EB%A3%B9%ED%99%94%EC%99%80%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4.md) · [멀티 컨테이너·사이드카](../08_cloud/book/kubernetes-in-action/05-03.%EB%A9%80%ED%8B%B0%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7init%C2%B7%EB%84%A4%EC%9D%B4%ED%8B%B0%EB%B8%8C%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%EC%99%80%20%EC%82%AD%EC%A0%9C.md) | Kubernetes in Action 5장 |
| phase · conditions · 컨테이너 상태 · restart 정책 | 필수 | [Pod 상태](../08_cloud/book/kubernetes-in-action/06-01.Pod%20%EC%83%81%ED%83%9C%20%E2%80%94%20phase%C2%B7conditions%C2%B7%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%83%81%ED%83%9C.md) | Kubernetes in Action 6장 |
| liveness · readiness · startup probe | 필수 | [liveness·startup probe](../08_cloud/book/kubernetes-in-action/06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md) · [Health Probe](../08_cloud/book/kubernetes-patterns/04-01.Health%20Probe%20%E2%80%94%20%EC%95%B1%EC%9D%B4%20%EC%9E%90%EA%B8%B0%20%EA%B1%B4%EA%B0%95%EC%9D%84%20%ED%94%8C%EB%9E%AB%ED%8F%BC%EC%97%90%20%EC%95%8C%EB%A6%AC%EA%B8%B0.md) | Kubernetes Patterns 4장 |
| lifecycle hook · 종료 흐름 | 필수 | [lifecycle hook](../08_cloud/book/kubernetes-in-action/06-03.lifecycle%20hook%EA%B3%BC%20Pod%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%A0%84%EC%B2%B4.md) · [Managed Lifecycle](../08_cloud/book/kubernetes-patterns/05-01.Managed%20Lifecycle%20%E2%80%94%20%ED%94%8C%EB%9E%AB%ED%8F%BC%EC%9D%98%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%EC%97%90%20%EB%B0%98%EC%9D%91%ED%95%98%EA%B8%B0.md) | Kubernetes Patterns 5장 |
| namespace · label · label selector | 필수 | [namespace](../08_cloud/book/kubernetes-in-action/07-01.namespace%EB%A1%9C%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%A5%BC%20%EA%B0%80%EC%83%81%20%EB%B6%84%ED%95%A0%ED%95%98%EA%B8%B0.md) · [label·selector](../08_cloud/book/kubernetes-in-action/07-02.label%EA%B3%BC%20label%20selector%EB%A1%9C%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EC%A1%B0%EC%A7%81%ED%95%98%EA%B8%B0.md) | Kubernetes in Action 7장 |
| field selector · annotation | 추천 | [field selector·annotation](../08_cloud/book/kubernetes-in-action/07-03.field%20selector%EC%99%80%20annotation.md) | Kubernetes in Action 7장 |
| `command` · `args` · 환경변수 | 필수 | [command·args](../08_cloud/book/kubernetes-in-action/08-01.command%C2%B7args%EC%99%80%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98.md) · [EnvVar Configuration](../08_cloud/book/kubernetes-patterns/19-01.EnvVar%20Configuration%20%E2%80%94%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98%EB%A1%9C%20%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%99%B8%EB%B6%80%ED%99%94%ED%95%98%EA%B8%B0.md) | Kubernetes Patterns 19장 |
| ConfigMap · Secret · Downward API | 필수 | [ConfigMap](../08_cloud/book/kubernetes-in-action/08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md) · [Secret과 Downward API](../08_cloud/book/kubernetes-in-action/08-03.Secret%EA%B3%BC%20Downward%20API.md) · [Configuration Resource](../08_cloud/book/kubernetes-patterns/20-01.Configuration%20Resource%20%E2%80%94%20ConfigMap%EA%B3%BC%20Secret%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC.md) | Kubernetes Patterns 20~22장 |
| kubectl 기본 조회 | 필수 | | Kubernetes: Up and Running 4장 |
| 컨테이너 격리 — namespace · cgroup | 추천 | [namespace·cgroup 격리](../08_cloud/book/kubernetes-in-action/02-03.%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20cgroup%EC%9C%BC%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC.md) · [OS 로드맵](os-roadmap.md) | Kubernetes in Action 2장 |

### 2단계 · 워크로드

> 먼저: 이 문서 1단계 Pod · label selector · probe

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| ReplicaSet · reconciliation · 소유 관계 | 필수 | [ReplicaSet 기초](../08_cloud/book/kubernetes-in-action/14-01.ReplicaSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7%EC%86%8C%EC%9C%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) · [ReplicaSet 컨트롤러](../08_cloud/book/kubernetes-in-action/14-02.ReplicaSet%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20%E2%80%94%20reconciliation%C2%B7%EC%9E%A5%EC%95%A0%EB%B3%B5%EA%B5%AC%C2%B7%EC%82%AD%EC%A0%9C.md) | Kubernetes in Action 14장 |
| Deployment · pod-template-hash | 필수 | [Deployment 기초](../08_cloud/book/kubernetes-in-action/15-01.Deployment%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7pod-template-hash%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | Kubernetes in Action 15장 |
| RollingUpdate · Recreate · `maxSurge` · `maxUnavailable` | 필수 | [Deployment 업데이트](../08_cloud/book/kubernetes-in-action/15-02.Deployment%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%20%E2%80%94%20Recreate%C2%B7RollingUpdate%C2%B7maxSurge.md) · [Declarative Deployment](../08_cloud/book/kubernetes-patterns/03-01.Declarative%20Deployment%20%E2%80%94%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%C2%B7%EB%A1%A4%EB%B0%B1%EC%9D%84%20%EC%84%A0%EC%96%B8%EC%9C%BC%EB%A1%9C.md) | Kubernetes Patterns 3장 |
| rollout 제어 · pause · rollback · 배포 전략 다섯 | 필수 | [rollout 제어](../08_cloud/book/kubernetes-in-action/15-03.rollout%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%E2%80%94%20pause%C2%B7faulty%C2%B7rollback%C2%B7%EC%A0%84%EB%9E%B5%205%EC%A2%85.md) | Kubernetes in Action 15장 |
| StatefulSet · ordinal · headless Service · retention | 필수 | [StatefulSet 기초](../08_cloud/book/kubernetes-in-action/16-01.StatefulSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20Pets%20vs%20Cattle%C2%B7ordinal%C2%B7headless%20Service.md) · [StatefulSet 동작](../08_cloud/book/kubernetes-in-action/16-02.StatefulSet%20%EB%8F%99%EC%9E%91%20%E2%80%94%20%EB%AF%B8%EC%8B%B1%20%ED%8C%8C%EB%93%9C%C2%B7%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%C2%B7retention.md) · [Stateful Service](../08_cloud/book/kubernetes-patterns/12-01.Stateful%20Service%20%E2%80%94%20StatefulSet%EC%9C%BC%EB%A1%9C%20%EC%83%81%ED%83%9C%EB%A5%BC%20first-class%EB%A1%9C.md) | Kubernetes Patterns 12장 |
| DaemonSet · hostNetwork · hostPort | 필수 | [DaemonSet 기초](../08_cloud/book/kubernetes-in-action/17-01.DaemonSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EB%85%B8%EB%93%9C%EB%A7%88%EB%8B%A4%20%ED%95%98%EB%82%98%C2%B7node%20selector%C2%B7%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8.md) · [노드 에이전트 기능](../08_cloud/book/kubernetes-in-action/17-02.%EB%85%B8%EB%93%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%8A%B9%EC%88%98%20%EA%B8%B0%EB%8A%A5%20%E2%80%94%20privileged%C2%B7hostPath%C2%B7hostNetwork%C2%B7PriorityClass.md) · [Daemon Service](../08_cloud/book/kubernetes-patterns/09-01.Daemon%20Service%20%E2%80%94%20%EB%85%B8%EB%93%9C%EB%A7%88%EB%8B%A4%20%EB%8F%84%EB%8A%94%20%EC%9D%B8%ED%94%84%EB%9D%BC%20Pod.md) | Kubernetes Patterns 9장 |
| Job · CronJob · 병렬 · 완료 모드 · work queue | 추천 | [Job 기초](../08_cloud/book/kubernetes-in-action/18-01.Job%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%8B%A4%ED%96%89%C2%B7%EC%83%81%ED%83%9C%C2%B7suspend%C2%B7%EC%9E%90%EB%8F%99%EC%82%AD%EC%A0%9C.md) ~ [work queue·CronJob](../08_cloud/book/kubernetes-in-action/18-03.work%20queue%C2%B7pod%20%ED%86%B5%EC%8B%A0%C2%B7sidecar%C2%B7CronJob.md) · [Batch Job](../08_cloud/book/kubernetes-patterns/07-01.Batch%20Job%20%E2%80%94%20%EC%9C%A0%ED%95%9C%ED%95%9C%20%EC%9E%91%EC%97%85%EC%9D%84%20%EC%99%84%EB%A3%8C%EA%B9%8C%EC%A7%80%20%EC%95%88%EC%A0%95%EC%A0%81%EC%9C%BC%EB%A1%9C.md) | Kubernetes Patterns 7·8장 |
| init container · sidecar | 추천 | [Init Container](../08_cloud/book/kubernetes-patterns/15-01.Init%20Container%20%E2%80%94%20%EC%B4%88%EA%B8%B0%ED%99%94%EB%A5%BC%20%EC%95%B1%EA%B3%BC%20%EB%B6%84%EB%A6%AC%ED%95%B4%20%EB%B3%84%EB%8F%84%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%EB%A1%9C.md) · [Sidecar](../08_cloud/book/kubernetes-patterns/16-01.Sidecar%20%E2%80%94%20%EA%B8%B0%EC%A1%B4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EB%A5%BC%20%EB%B0%94%EA%BE%B8%EC%A7%80%20%EC%95%8A%EA%B3%A0%20%ED%99%95%EC%9E%A5.md) | Kubernetes Patterns 15·16장 |
| adapter · ambassador | 선택 | [Adapter](../08_cloud/book/kubernetes-patterns/17-01.Adapter%20%E2%80%94%20%EC%9D%B4%EC%A7%88%EC%A0%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84%20%ED%86%B5%EC%9D%BC%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%EB%A1%9C.md) · [Ambassador](../08_cloud/book/kubernetes-patterns/18-01.Ambassador%20%E2%80%94%20%EB%B0%94%EA%B9%A5%EC%84%B8%EC%83%81%EC%9C%BC%EB%A1%9C%EC%9D%98%20smart%20proxy.md) | Kubernetes Patterns 17·18장 |
| Singleton Service · Stateless Service | 선택 | [Singleton Service](../08_cloud/book/kubernetes-patterns/10-01.Singleton%20Service%20%E2%80%94%20%ED%95%9C%20%EB%B2%88%EC%97%90%20%ED%95%98%EB%82%98%EB%A7%8C%20%ED%99%9C%EC%84%B1%EC%9D%B4%EB%90%98%20%EA%B3%A0%EA%B0%80%EC%9A%A9.md) · [Stateless Service](../08_cloud/book/kubernetes-patterns/11-01.Stateless%20Service%20%E2%80%94%20%EB%8F%99%EC%9D%BC%C2%B7%EA%B5%90%EC%B2%B4%20%EA%B0%80%EB%8A%A5%ED%95%9C%20replica%EB%A1%9C%20%EC%88%98%ED%8F%89%20%ED%99%95%EC%9E%A5.md) | Kubernetes Patterns 10·11장 |

### 3단계 · 연결

> 먼저: 이 문서 1단계 label selector · 2단계 Deployment · [네트워크 로드맵](network-roadmap.md) 2단계 NAT · conntrack

> 오브젝트가 트래픽을 받는 방법까지입니다. 패킷이 실제로 어떤 경로로 가는지는 [네트워크 로드맵](network-roadmap.md)이 맡습니다.

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| Service · ClusterIP · 세션 어피니티 | 필수 | [Service 기초](../08_cloud/book/kubernetes-in-action/11-01.Service%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%C2%B7ClusterIP%C2%B7%EC%84%B8%EC%85%98%20%EC%96%B4%ED%94%BC%EB%8B%88%ED%8B%B0.md) · [Service와 EndpointSlice](../08_cloud/kubernetes/04_networking/04-04.Service%EC%99%80%20EndpointSlice.md) | Kubernetes in Action 11장 |
| NodePort · LoadBalancer · 트래픽 정책 | 필수 | [외부 노출](../08_cloud/book/kubernetes-in-action/11-02.%EC%99%B8%EB%B6%80%20%EB%85%B8%EC%B6%9C%20%E2%80%94%20NodePort%C2%B7LoadBalancer%C2%B7%ED%8A%B8%EB%9E%98%ED%94%BD%20%EC%A0%95%EC%B1%85.md) | Kubernetes in Action 11장 |
| Endpoint · EndpointSlice · readiness 연동 · 토폴로지 | 필수 | [엔드포인트·DNS·readiness](../08_cloud/book/kubernetes-in-action/11-03.%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7DNS%C2%B7%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%C2%B7readiness.md) | Networking and Kubernetes 5장 |
| 클러스터 DNS · Service FQDN | 필수 | [DNS와 CoreDNS](../08_cloud/kubernetes/04_networking/04-05.DNS%EC%99%80%20CoreDNS.md) · [Service Discovery](../08_cloud/book/kubernetes-patterns/13-01.Service%20Discovery%20%E2%80%94%20%EA%B3%A0%EC%A0%95%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%EB%A1%9C%20%EB%8F%99%EC%A0%81%20Pod%EB%A5%BC%20%EC%B0%BE%EA%B8%B0.md) | Kubernetes Patterns 13장 |
| Ingress · IngressClass · TLS | 필수 | [Ingress](../08_cloud/book/kubernetes-in-action/12-01.Ingress%EB%A1%9C%20%EC%97%AC%EB%9F%AC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%ED%95%9C%20IP%EC%97%90%20%EB%85%B8%EC%B6%9C%ED%95%98%EA%B8%B0.md) · [Ingress TLS](../08_cloud/book/kubernetes-in-action/12-02.Ingress%20TLS%C2%B7%EC%84%A4%EC%A0%95%C2%B7IngressClass.md) | Kubernetes in Action 12장 |
| Gateway API · HTTPRoute · 필터 | 필수 | [Gateway API](../08_cloud/book/kubernetes-in-action/13-01.Gateway%20API%20%EA%B0%9C%EB%85%90%EA%B3%BC%20Gateway%20%EB%B0%B0%ED%8F%AC.md) · [HTTPRoute](../08_cloud/book/kubernetes-in-action/13-02.HTTPRoute%20%E2%80%94%20%EB%9D%BC%EC%9A%B0%ED%8C%85%EA%B3%BC%20%ED%95%84%ED%84%B0.md) | Kubernetes in Action 13장 |
| 크로스 네임스페이스 · mesh 연동 | 추천 | [크로스 네임스페이스·mesh](../08_cloud/book/kubernetes-in-action/13-03.TLS%C2%B7%EA%B8%B0%ED%83%80%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%C2%B7%ED%81%AC%EB%A1%9C%EC%8A%A4%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7mesh.md) | Kubernetes in Action 13장 |
| Service Discovery — DNS 로 못 하는 일 | 추천 | [DNS 밖의 Service Discovery](../08_cloud/book/kubernetes-up-and-running/07-01.Service%20Discovery%20%E2%80%94%20DNS%EA%B0%80%20%EB%AA%BB%20%ED%95%98%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EB%B0%94%EA%B9%A5%EC%9D%84%20%EC%9E%87%EB%8A%94%20%EB%B2%95.md) | Kubernetes: Up and Running 7장 |
| Gateway API Inference Extension · `InferencePool` | 선택 |  | [Gateway API Inference Extension](https://gateway-api-inference-extension.sigs.k8s.io/) |

### 4단계 · 자원과 저장

> 먼저: 이 문서 1단계 Pod · 2단계 Deployment · StatefulSet · [OS 로드맵](os-roadmap.md) 3단계 `cpu.max` · `memory.max`

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| requests · limits · QoS | 필수 | [Predictable Demands](../08_cloud/book/kubernetes-patterns/02-01.Predictable%20Demands%20%E2%80%94%20%EC%9E%90%EC%9B%90%20%EC%9A%94%EA%B5%AC%EB%A5%BC%20%EC%84%A0%EC%96%B8%ED%95%B4%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EC%97%90%20%EC%95%8C%EB%A6%AC%EA%B8%B0.md) | Kubernetes Patterns 2장 |
| LimitRange · ResourceQuota — 네임스페이스 단위 상한 | 추천 | | [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) · [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/) |
| taint · toleration · affinity · 스케줄러 동작 | 필수 | [스케줄링과 노드 선택](../08_cloud/kubernetes/05_scheduling/05-01.%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%EA%B3%BC%20%EB%85%B8%EB%93%9C%20%EC%84%A0%ED%83%9D.md) · [Automated Placement](../08_cloud/book/kubernetes-patterns/06-01.Automated%20Placement%20%E2%80%94%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EA%B0%80%20Pod%EB%A5%BC%20%EB%85%B8%EB%93%9C%EC%97%90%20%EB%B0%B0%EC%B9%98%ED%95%98%EB%8A%94%20%EB%B2%95.md) | Kubernetes Patterns 6장 |
| 토폴로지 분산 · PodDisruptionBudget | 추천 | [토폴로지 분산과 중단 정책](../08_cloud/kubernetes/05_scheduling/05-02.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EB%B6%84%EC%82%B0%EA%B3%BC%20%EC%A4%91%EB%8B%A8%20%EC%A0%95%EC%B1%85.md) | |
| PriorityClass · preemption · eviction | 추천 | [토폴로지 분산과 중단 정책](../08_cloud/kubernetes/05_scheduling/05-02.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EB%B6%84%EC%82%B0%EA%B3%BC%20%EC%A4%91%EB%8B%A8%20%EC%A0%95%EC%B1%85.md) | |
| Volume · emptyDir · hostPath · projected | 필수 | [볼륨과 emptyDir](../08_cloud/book/kubernetes-in-action/09-01.%EB%B3%BC%EB%A5%A8%20%EC%9D%B4%ED%95%B4%EC%99%80%20emptyDir%EB%A1%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B3%B4%EC%A1%B4%ED%95%98%EA%B8%B0.md) ~ [projected 볼륨](../08_cloud/book/kubernetes-in-action/09-03.ConfigMap%C2%B7Secret%C2%B7Downward%20API%C2%B7projected%20%EB%B3%BC%EB%A5%A8.md) | Kubernetes in Action 9장 |
| PV · PVC · StorageClass · 동적 프로비저닝 | 필수 | [PV·PVC·StorageClass](../08_cloud/book/kubernetes-in-action/10-01.PV%C2%B7PVC%C2%B7StorageClass%EC%99%80%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D.md) · [정적 프로비저닝](../08_cloud/book/kubernetes-in-action/10-02.%EC%A0%95%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D%EA%B3%BC%20node-local%20%EB%B3%BC%EB%A5%A8.md) | Kubernetes in Action 10장 |
| CSI · access mode · reclaim policy · 스냅샷 · ephemeral | 추천 | [PV 관리](../08_cloud/book/kubernetes-in-action/10-03.PV%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20%EB%A6%AC%EC%82%AC%EC%9D%B4%EC%A6%88%C2%B7%EC%8A%A4%EB%83%85%EC%83%B7%C2%B7ephemeral.md) | Production Kubernetes 4장 |
| 외부 저장소 통합 · 복제하지 않는 선택지 | 선택 | [저장소 통합 랩](../08_cloud/book/kubernetes-up-and-running/16-01.Integrating%20Storage%20%E2%80%94%20%EB%B3%B5%EC%A0%9C%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%20%EC%84%A0%ED%83%9D%EC%A7%80%EC%99%80%20MySQL%20%EC%8B%B1%EA%B8%80%ED%84%B4%20%EB%9E%A9.md) | Kubernetes: Up and Running 16장 |
| HPA · VPA · Cluster Autoscaler · KEDA | 추천 | [오토스케일링](../08_cloud/kubernetes/05_scheduling/05-03.%EC%98%A4%ED%86%A0%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) · [Elastic Scale](../08_cloud/book/kubernetes-patterns/29-01.Elastic%20Scale%20%E2%80%94%20%EB%B6%80%ED%95%98%EC%97%90%20%EB%A7%9E%EC%B6%B0%20%EC%84%B8%20%EC%B0%A8%EC%9B%90%EC%9C%BC%EB%A1%9C%20%EC%9E%90%EB%8F%99%20%ED%99%95%EC%9E%A5.md) | Production Kubernetes 13장 |
| Self Awareness — 자기 메타데이터 | 선택 | [Self Awareness](../08_cloud/book/kubernetes-patterns/14-01.Self%20Awareness%20%E2%80%94%20downward%20API%EB%A1%9C%20%EC%9E%90%EA%B8%B0%20%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%96%BB%EA%B8%B0.md) | Kubernetes Patterns 14장 |



## 클러스터를 만들고 지키는 쪽 · 5~7단계

> 오브젝트 뒤에서 무엇이 결정을 내리는지, 그리고 그것이 잘못됐을 때 어디를 보는지입니다.

### 5단계 · 내부 구조

> 먼저: 이 문서 1~4단계 · [네트워크 로드맵](network-roadmap.md) 1단계 TLS 핸드셰이크

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| API Server · etcd · Scheduler · Controller Manager | 필수 | [쿠버네티스 아키텍처](../08_cloud/book/kubernetes-in-action/01-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%20%E2%80%94%20%EA%B8%B0%EC%9B%90%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | Kubernetes in Action 1장 |
| kubelet · CRI · CNI · CSI · containerd | 필수 | [Kubernetes MOC](../08_cloud/kubernetes/README.md) | Production Kubernetes 3~5장 |
| 조정 루프 · watch · informer · client-go | 필수 | | Programming Kubernetes 2·3장 |
| List·Watch 와 resourceVersion · 410 Gone | 필수 | | Programming Kubernetes 3장 |
| level-driven 과 edge-driven 의 차이 | 필수 | | Programming Kubernetes 1장 |
| GVK · Scheme · TypeMeta | 추천 | | Programming Kubernetes 2·3장 |
| Reflector · DeltaFIFO · Indexer · Lister | 추천 | | Programming Kubernetes 3장 |
| SharedInformer 와 resync | 추천 | | Programming Kubernetes 3장 |
| 이벤트 병합과 upsert — 감사 로그가 아니다 | 추천 | | Programming Kubernetes 1장 |
| authentication · authorization · admission | 필수 | [TLS와 API 접근 보안](../08_cloud/kubernetes/06_architecture/06-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | Production Kubernetes 8장 |
| TLS · PKI · 인증서 수명 | 필수 | [TLS와 API 접근 보안](../08_cloud/kubernetes/06_architecture/06-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | |
| etcd quorum · Raft · 백업 · 복구 | 필수 | [업그레이드·etcd 백업](../08_cloud/kubernetes/06_architecture/06-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | |
| 클러스터 업그레이드 | 추천 | [업그레이드·etcd 백업](../08_cloud/kubernetes/06_architecture/06-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | |
| kubectl 뒤의 HTTP — 클라이언트가 감추는 요청 | 선택 | [클라이언트와 HTTP](../08_cloud/book/kubernetes-up-and-running/18-01.Accessing%20Kubernetes%20%E2%80%94%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EA%B0%90%EC%B6%94%EB%8A%94%20HTTP%EC%99%80%20%EC%9B%90%EC%84%9C%20%EC%BD%94%EB%93%9C%20%EC%8B%A4%EC%A6%9D%20%EB%9E%A9.md) | Kubernetes: Up and Running 18장 |

### 6단계 · 보안과 확장

> 먼저: 이 문서 5단계 authentication · authorization · admission · 조정 루프 · [OS 로드맵](os-roadmap.md) 5단계 capability · seccomp

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| RBAC · Role · ClusterRole · RoleBinding · ServiceAccount | 필수 | [RBAC 설계와 운영](../08_cloud/book/kubernetes-up-and-running/14-01.RBAC%20%E2%80%94%20%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B3%A0%20%EC%9A%B4%EC%98%81%ED%95%98%EB%8A%94%20%EB%B2%95.md) · [Access Control](../08_cloud/book/kubernetes-patterns/26-01.Access%20Control%20%E2%80%94%20RBAC%EC%9C%BC%EB%A1%9C%20%EB%88%84%EA%B0%80%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%95%A0%20%EC%88%98%20%EC%9E%88%EB%8A%94%EC%A7%80.md) | Kubernetes: Up and Running 14장 |
| SelfSubjectAccessReview · `kubectl auth can-i` | 추천 |  | Kubernetes: Up and Running 14장 |
| 권한 기반 기능 노출 — 볼 수 없는 기능은 끈다 | 추천 |  | [Authorization](https://kubernetes.io/docs/reference/access-authn-authz/authorization/) |
| API 접근 하드닝 — anonymous 인증 · SA 토큰 자동 마운트 끄기 | 추천 | | CKS Study Guide 3장 |
| SecurityContext · capability · seccomp · 최소 권한 | 필수 | [Process Containment](../08_cloud/book/kubernetes-patterns/23-01.Process%20Containment%20%E2%80%94%20%EC%B5%9C%EC%86%8C%20%EA%B6%8C%ED%95%9C%EC%9C%BC%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EB%A5%BC%20%EA%B0%80%EB%91%90%EA%B8%B0.md) · [시스템 콜·capability](../08_cloud/book/container-security/02-01.Linux%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EA%B6%8C%ED%95%9C%C2%B7capability%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%EC%9D%98%20%EB%B0%94%EB%8B%A5.md) | Kubernetes Patterns 23장 |
| AppArmor 프로파일 · `appArmorProfile` 필드 | 추천 | [컨테이너 격리 강화](../08_cloud/book/container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) · [보안 컨텍스트 랩](../08_cloud/book/kubernetes-up-and-running/19-01.Securing%20Applications%20%E2%80%94%20%EC%A3%BD%EC%9D%80%20%EC%8B%A4%EC%8A%B5%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%99%80%20proc%20%EB%A1%9C%20%EB%8B%A4%EC%8B%9C%20%EC%84%B8%EC%9A%B4%20%EB%9E%A9.md) | CKS Study Guide 4장 |
| Pod Security Admission · PSS 세 등급 — Privileged · Baseline · Restricted | 필수 | [보안 컨텍스트 랩](../08_cloud/book/kubernetes-up-and-running/19-01.Securing%20Applications%20%E2%80%94%20%EC%A3%BD%EC%9D%80%20%EC%8B%A4%EC%8A%B5%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%99%80%20proc%20%EB%A1%9C%20%EB%8B%A4%EC%8B%9C%20%EC%84%B8%EC%9A%B4%20%EB%9E%A9.md) | CKS Study Guide 5장 |
| NetworkPolicy · 네트워크 분할 | 추천 | [NetworkPolicy](../08_cloud/kubernetes/04_networking/04-07.NetworkPolicy.md) · [Network Segmentation](../08_cloud/book/kubernetes-patterns/24-01.Network%20Segmentation%20%E2%80%94%20%ED%86%B5%EC%8B%A0%EC%9D%84%20%ED%95%84%EC%9A%94%ED%95%9C%20%EA%B2%BD%EB%A1%9C%EB%A7%8C%20%EB%82%A8%EA%B8%B0%EA%B8%B0.md) | Kubernetes Patterns 24장 |
| Secret 관리 · 외부 저장소 · 안전한 설정 | 추천 | [Secure Configuration](../08_cloud/book/kubernetes-patterns/25-01.Secure%20Configuration%20%E2%80%94%20%EB%AF%BC%EA%B0%90%ED%95%9C%20%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EB%8B%A4%EB%A3%A8%EA%B8%B0.md) | Production Kubernetes 7장 |
| 저장 암호화 — EncryptionConfiguration · KMS provider | 추천 | [Secure Configuration](../08_cloud/book/kubernetes-patterns/25-01.Secure%20Configuration%20%E2%80%94%20%EB%AF%BC%EA%B0%90%ED%95%9C%20%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EB%8B%A4%EB%A3%A8%EA%B8%B0.md) | Production Kubernetes 7장 |
| 격리 강화 · 경계 파괴 · 런타임 보호 | 추천 | [컨테이너 격리 강화](../08_cloud/book/container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) · [컨테이너 격리 깨뜨리기](../08_cloud/book/container-security/09-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B9%A8%EB%9C%A8%EB%A6%AC%EA%B8%B0%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%AC%B4%EB%84%88%EC%A7%80%EB%8A%94%20%EA%B2%BD%EA%B3%84.md) | Container Security 8·9·13장 |
| EKS 워크로드 신원 — IRSA | 추천 | | Production Kubernetes 10장 |
| EKS Pod Identity | 추천 | | [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html) |
| EKS 봉투 암호화 · 제어부 로깅 | 선택 | | [envelope encryption](https://docs.aws.amazon.com/eks/latest/userguide/envelope-encryption.html) · [control plane logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) |
| 위협 모델 · 공격 체인 · 횡적 이동 | 추천 | [컨테이너 보안 위협](../08_cloud/book/container-security/01-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%20%EC%9C%84%ED%98%91%20%E2%80%94%20%EC%9C%84%ED%98%91%20%EB%AA%A8%EB%8D%B8%EB%B6%80%ED%84%B0%20%EB%B3%B4%EC%95%88%20%EC%9B%90%EC%B9%99%EA%B9%8C%EC%A7%80.md) · [Network Segmentation](../08_cloud/book/kubernetes-patterns/24-01.Network%20Segmentation%20%E2%80%94%20%ED%86%B5%EC%8B%A0%EC%9D%84%20%ED%95%84%EC%9A%94%ED%95%9C%20%EA%B2%BD%EB%A1%9C%EB%A7%8C%20%EB%82%A8%EA%B8%B0%EA%B8%B0.md) | Container Security 1장 |
| CIS Benchmark · kube-bench · KISA 점검 가이드 | 추천 | [OWASP Top 10](../08_cloud/book/container-security/14-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80%20OWASP%20Top%2010%20%E2%80%94%20%EC%9B%B9%20%EB%A6%AC%EC%8A%A4%ED%81%AC%EB%A5%BC%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%8C%80%EC%9D%91%EC%9C%BC%EB%A1%9C%20%EC%9E%87%EB%8B%A4.md) | CKS Study Guide 2장 |
| 감사 로그 — audit policy · 로그 백엔드 | 추천 | | CKS Study Guide 7장 |
| 런타임 탐지 — Falco · Tetragon · 탐지와 강제의 차이 | 추천 | [런타임 보호](../08_cloud/book/container-security/13-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20%EC%A0%95%EC%83%81%EC%9D%84%20%EC%A0%95%EC%9D%98%ED%95%B4%20%EC%9D%B4%EC%83%81%EC%9D%84%20%EC%9E%A1%EB%8B%A4.md) | CKS Study Guide 7장 · Learning eBPF 9장 |
| Discovery API · Unstructured — 동적 리소스 | 추천 | | Programming Kubernetes 3장 |
| CRD · custom resource | 추천 | [StatefulSet과 Operator](../08_cloud/book/kubernetes-in-action/16-03.StatefulSet%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%EC%99%80%20Operator%20%E2%80%94%20partition%C2%B7OnDelete%C2%B7CRD.md) · [어드미션 검증 랩](../08_cloud/book/kubernetes-up-and-running/17-01.Extending%20Kubernetes%20%E2%80%94%20%EC%96%B4%EB%93%9C%EB%AF%B8%EC%85%98%C2%B7%EC%BB%A4%EC%8A%A4%ED%85%80%20%EB%A6%AC%EC%86%8C%EC%8A%A4%EC%99%80%20%EC%9D%B8%EC%A6%9D%EC%84%9C%20%EC%97%86%EB%8A%94%20%EA%B2%80%EC%A6%9D%20%EB%9E%A9.md) | Programming Kubernetes 4장 |
| Controller · Operator · finalizer · OwnerReference | 추천 | [Controller](../08_cloud/book/kubernetes-patterns/27-01.Controller%20%E2%80%94%20Observe-Analyze-Act%EB%A1%9C%20%EC%83%81%ED%83%9C%EB%A5%BC%20%EC%A1%B0%EC%A0%95%ED%95%98%EA%B8%B0.md) · [Operator](../08_cloud/book/kubernetes-patterns/28-01.Operator%20%E2%80%94%20CRD%EB%A1%9C%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%A7%80%EC%8B%9D%EC%9D%84%20%EC%9E%90%EB%8F%99%ED%99%94%ED%95%98%EA%B8%B0.md) | Programming Kubernetes 6장 |
| controller-runtime 으로 감싸기 | 추천 | | Programming Kubernetes 6장 |
| status subresource · 코드 생성 | 선택 | | Programming Kubernetes 5·9장 |
| 어드미션 웹훅 · OPA · Gatekeeper · Kyverno | 추천 | [Gatekeeper 정책](../08_cloud/book/kubernetes-up-and-running/20-01.Policy%20and%20Governance%20%E2%80%94%20Gatekeeper%20%EB%A1%9C%20%EB%A7%8C%EB%93%A4%EA%B8%B0%20%EC%A0%84%EC%97%90%20%EB%A7%89%EA%B3%A0%20%EB%A7%8C%EB%93%A0%20%EB%92%A4%EC%97%90%20%EC%84%B8%EB%8A%94%20%EB%B2%95.md) | Policy as Code 7·8장 |
| ValidatingAdmissionPolicy — 웹훅 없는 CEL 정책 | 선택 | | [Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/) |
| 공급망 보안 · SBOM · 이미지 서명 · 취약점 스캔 | 추천 | [이미지 공급망 보안](../08_cloud/book/container-security/06-02.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md) · [이미지 취약점](../08_cloud/book/container-security/07-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%86%8D%20%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%E2%80%94%20CVE%EB%B6%80%ED%84%B0%20%EC%8A%A4%EC%BA%94%20%EC%9A%B4%EC%98%81%EA%B9%8C%EC%A7%80.md) | CKS Study Guide 6장 · Policy as Code 14장 |
| 클러스터 안에서 이미지 빌드 | 선택 | [Image Builder](../08_cloud/book/kubernetes-patterns/30-01.Image%20Builder%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%97%90%EC%84%9C%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A5%BC%20%EB%B9%8C%EB%93%9C%ED%95%98%EA%B8%B0.md) | Kubernetes Patterns 30장 |

### 7단계 · 운영

> 먼저: 이 문서 4단계 requests · limits · 5단계 Control Plane · [OS 로드맵](os-roadmap.md) 2단계 signal · zombie · PID 1

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 이벤트 · 로그 · 지표를 한 시간축에 | 필수 | [모니터링과 트러블슈팅](../08_cloud/kubernetes/09_operations/09-01.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EA%B3%BC%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.md) | Kubernetes Best Practices 3장 |
| kubectl 고급 조회 · JSONPath | 필수 | [JSONPath 조회](../08_cloud/kubernetes/09_operations/09-03.JSONPath%EC%99%80%20kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | |
| ephemeral container · `kubectl debug` | 추천 | | [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/) |
| OOMKilled · exit code 137 · CPU throttling | 필수 | [OOMKilled 사례 분석](../08_cloud/kubernetes/09_operations/09-02.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) · [OS 로드맵](os-roadmap.md) | |
| SIGTERM · PID 1 · PreStop · `terminationGracePeriodSeconds` | 필수 | [Kubernetes 장애 기록](../troubleshooting/kubernetes/README.md) | |
| node pressure · eviction · NodeNotReady | 추천 | [Kubernetes 장애 기록](../troubleshooting/kubernetes/README.md) | |
| OS 자동 업데이트 — 파이프라인 밖에서 노드를 바꾸는 장치 | 선택 | [진단 개념](../troubleshooting/_concepts/os-%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8-%EB%B0%96%EC%97%90%EC%84%9C-%EB%85%B8%EB%93%9C%EB%A5%BC-%EB%B0%94%EA%BE%B8%EB%8A%94-%EC%9E%A5%EC%B9%98.md) |  |
| Helm · Kustomize | 추천 | [Helm 기초](../08_cloud/kubernetes/10_packaging/10-01.Helm%20%EA%B8%B0%EC%B4%88.md) ~ [Kustomize](../08_cloud/kubernetes/10_packaging/10-03.Kustomize.md) | |
| GitOps · ArgoCD · App of Apps · ApplicationSet | 추천 | [ArgoCD와 GitOps](../08_cloud/kubernetes/11_devtools/11-03.ArgoCD%EC%99%80%20GitOps.md) · [ArgoCD 노트](../08_cloud/argocd/README.md) | Kubernetes Best Practices 18장 |
| IaC 와 Immutable Infrastructure — 고치지 않고 다시 만든다 | 추천 | [IaC 관리](../07_devops/book/fdsd_fundamentals-devops/02-01.How%20to%20Manage%20Your%20Infrastructure%20as%20Code.md) | Terraform Up and Running 1장 · Infrastructure as Code 11장 |
| Terraform state · module · 비밀 관리 | 추천 | | Terraform Up and Running 3·4·6장 |
| IaC 정책 검사 — Security as Code | 선택 |  | Policy as Code 11·12장 · Infrastructure as Code 21장 |
| 멀티테넌시 | 추천 | | Production Kubernetes 12장 |
| 가상 컨트롤 플레인 — tenant 와 host 를 잇는 sync 방향 | 선택 | | Production Kubernetes 12장 |
| 이름 변환과 충돌 회피 · status back-sync | 선택 |  | [vcluster](https://www.vcluster.com/docs) |
| 멀티클러스터 세 모델 | 추천 | [멀티클러스터 세 모델](../08_cloud/book/kubernetes-up-and-running/21-01.Multicluster%20%E2%80%94%20%EB%8A%98%EB%A6%AC%EA%B8%B0%20%EC%A0%84%EC%97%90%20%EA%B0%96%EC%B6%9C%20%EA%B2%83%EA%B3%BC%20%EB%8A%98%EB%A6%B0%20%EB%92%A4%20%EA%B0%88%EB%A6%AC%EB%8A%94%20%EC%84%B8%20%EB%AA%A8%EB%8D%B8.md) | Kubernetes: Up and Running 21장 |
| OpenShift — Route · SCC · 설치 방식 | 선택 | | Operating OpenShift 2·3장 |
| 서비스 메시를 쓸 것인가 | 선택 | [서비스 메시 판단](../08_cloud/book/kubernetes-up-and-running/15-01.Service%20Meshes%20%E2%80%94%20%EC%93%B8%20%EA%B2%83%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EB%A8%BC%EC%A0%80%20%EB%94%B0%EC%A7%84%EB%8B%A4.md) · [네트워크 로드맵](network-roadmap.md) | Kubernetes: Up and Running 15장 |
| 클러스터 안 CI 도구 — Jenkins · SonarQube · Harbor | 선택 | [Jenkins on K8s](../08_cloud/kubernetes/11_devtools/11-01.Jenkins%20on%20K8s.md) · [Harbor](../08_cloud/kubernetes/11_devtools/11-04.Harbor.md) | |
| CKA 대비와 문제 풀이 | 선택 | [CKA 대비](../08_cloud/kubernetes/09_operations/09-04.CKA%20%EB%8C%80%EB%B9%84%EC%99%80%20%EB%AC%B8%EC%A0%9C%20%ED%92%80%EC%9D%B4%20%EC%A0%84%EB%9E%B5.md) | |



## 손으로 확인하는 실습

> 노트 안에 실제로 있는 실습 절만 적습니다.

| 출처 | 단계 | 무엇 |
|---|:---:|---|
| [Node와 Event 오브젝트로 보는 필드 실습](../08_cloud/book/kubernetes-in-action/04-02.Node%EC%99%80%20Event%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%ED%95%84%EB%93%9C%20%EC%8B%A4%EC%8A%B5.md) | 1 | 매니페스트 필드를 실제 오브젝트에서 확인 |
| [네임스페이스와 cgroup으로 보는 컨테이너 격리](../08_cloud/book/kubernetes-in-action/02-03.%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20cgroup%EC%9C%BC%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC.md) | 1 | Pod 안 컨테이너가 무엇을 공유하는지 |
| [Extending Kubernetes](../08_cloud/book/kubernetes-up-and-running/17-01.Extending%20Kubernetes%20%E2%80%94%20%EC%96%B4%EB%93%9C%EB%AF%B8%EC%85%98%C2%B7%EC%BB%A4%EC%8A%A4%ED%85%80%20%EB%A6%AC%EC%86%8C%EC%8A%A4%EC%99%80%20%EC%9D%B8%EC%A6%9D%EC%84%9C%20%EC%97%86%EB%8A%94%20%EA%B2%80%EC%A6%9D%20%EB%9E%A9.md) | 6 | 인증서 없이 어드미션 웹훅 검증 |
| [Policy and Governance](../08_cloud/book/kubernetes-up-and-running/20-01.Policy%20and%20Governance%20%E2%80%94%20Gatekeeper%20%EB%A1%9C%20%EB%A7%8C%EB%93%A4%EA%B8%B0%20%EC%A0%84%EC%97%90%20%EB%A7%89%EA%B3%A0%20%EB%A7%8C%EB%93%A0%20%EB%92%A4%EC%97%90%20%EC%84%B8%EB%8A%94%20%EB%B2%95.md) | 6 | Gatekeeper 로 만들기 전에 막기 |
| [Securing Applications](../08_cloud/book/kubernetes-up-and-running/19-01.Securing%20Applications%20%E2%80%94%20%EC%A3%BD%EC%9D%80%20%EC%8B%A4%EC%8A%B5%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%99%80%20proc%20%EB%A1%9C%20%EB%8B%A4%EC%8B%9C%20%EC%84%B8%EC%9A%B4%20%EB%9E%A9.md) | 6 | `/proc` 로 다시 세운 보안 컨텍스트 랩 |
| [Integrating Storage](../08_cloud/book/kubernetes-up-and-running/16-01.Integrating%20Storage%20%E2%80%94%20%EB%B3%B5%EC%A0%9C%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%20%EC%84%A0%ED%83%9D%EC%A7%80%EC%99%80%20MySQL%20%EC%8B%B1%EA%B8%80%ED%84%B4%20%EB%9E%A9.md) | 4 | MySQL 싱글턴으로 저장소 통합 |
| [OOMKilled 사례 분석](../08_cloud/kubernetes/09_operations/09-02.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) | 7 | cgroup 파일로 OOM 원인 좁히기 |
| [Kubernetes 장애 기록](../troubleshooting/kubernetes/README.md) | 3·7 | 증상에서 원인 역추적 |
| [클라우드 장애 기록](../troubleshooting/cloud/README.md) | 4·7 | 절반만 뜨고 멈춘 배포 |



## 로드맵에 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| 패킷 경로 · CNI 데이터패스 · eBPF · Cilium · CNI 구현체 비교 | [네트워크 로드맵](network-roadmap.md)이 맡습니다 |
| cgroup · namespace 의 커널 구현 | [OS 로드맵](os-roadmap.md) 3단계가 맡습니다 |
| Prometheus · Grafana · OpenTelemetry | [관측 가능성 로드맵](observability-roadmap.md)이 맡습니다 |
| 이미지 빌드 · CI 파이프라인 | `07_devops` 소관입니다. 클러스터 안에서 도는 도구만 7단계에 걸었습니다 |
| Istio 의 트래픽 관리와 mTLS | [네트워크 로드맵](network-roadmap.md) 7단계가 맡습니다. 여기는 "쓸 것인가"까지입니다 |
| VPC · Security Group · 클라우드 네트워크 경계 | [네트워크 로드맵](network-roadmap.md) 5단계가 맡습니다 |
| Kubernetes in Action 3장 | 클러스터를 띄우는 절차입니다. 순서가 아니라 준비 단계입니다 |



## 경계

> 이 문서가 정하는 것과 인접 문서에 넘기는 것입니다.

이 문서는 **오브젝트 축의 개념 순서와 우선순위**를 정합니다. 폴더 경계는 [Kubernetes MOC](../08_cloud/kubernetes/README.md)가 맡습니다.

맞닿는 문서가 셋입니다. 오브젝트가 정상인데 패킷이 안 가는 자리는 [네트워크 로드맵](network-roadmap.md)이, 컨테이너를 만드는 커널 기능은 [OS 로드맵](os-roadmap.md)이, 클러스터에서 지표와 트레이스를 모아 보는 일은 [관측 가능성 로드맵](observability-roadmap.md)이 맡습니다.

**같은 증상을 세 문서가 다른 층에서 봅니다.** OOMKilled는 이 문서 7단계가 `kubectl describe` 로, OS 로드맵 3단계가 cgroup 파일로 다룹니다. Service 실패는 이 문서 3단계가 selector와 EndpointSlice로, 네트워크 로드맵이 4단계의 kube-proxy 규칙과 2단계의 conntrack·MTU로 다룹니다.
