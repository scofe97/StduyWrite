---
title: 08_cloud/kubernetes — Kubernetes 개념 딥다이브
tags: [moc, kubernetes, helm, operator, argocd]
status: final
source:
  - ../../../poc/03_CloudNative/02-kubernetes/README.md@8ac9e97
  - https://kubernetes.io/docs/concepts/
related:
  - roadmap.md
  - ../README.md
  - ../argocd/README.md
  - ../service-mesh/README.md
  - ../book/kubernetes-in-action/README.md
updated: 2026-07-10
---

# 08_cloud/kubernetes

> Kubernetes를 개념 축으로 정리한 딥다이브 노트입니다. 공식 문서(kubernetes.io/docs/concepts)의 대분류를 뼈대로 삼되, 폴더 번호는 "무엇을 먼저 배우는가"라는 학습 흐름을 따릅니다. 워크로드에서 시작해 설정·저장소·네트워크로 넓히고, 스케줄링·내부 구조·보안·확장을 거쳐 Day-2 운영까지 한 지도로 잇습니다.

이 카테고리는 "클러스터 안에서 어떻게 선언되고, 배치되고, 연결되고, 운영되는가"를 기본 범위로 둡니다. Service Mesh처럼 서비스 간 L7 정책·mTLS·세밀한 트래픽 제어가 본격적으로 필요해지는 지점부터는 별도 [`service-mesh`](../service-mesh/README.md) 카테고리로 넘깁니다. ArgoCD는 여기서 입문 수준으로만 소개하고, App of Apps·ApplicationSet·Image Updater 같은 상세 운영은 별도 [`argocd`](../argocd/README.md) 카테고리가 맡습니다.

책 한 권을 저자 순서대로 따라가는 정독본은 [`book/kubernetes-in-action`](../book/kubernetes-in-action/README.md)에 따로 있습니다. 이 개념 노트는 주제로 검색해 펼쳐 보는 참조용이고, 정독본은 저자가 개념을 쌓아 올린 순서를 보존하는 학습용이라 역할이 다릅니다. 개념이 겹치면 서로 링크로만 잇고 통째 병합하지 않습니다.



## 폴더 구조

> 공식 concepts 대분류를 대주제 폴더로 두고, 각 폴더 안에 문서를 채웁니다. 폴더 번호(`NN_`)가 학습 순서이고, 파일 번호(`NN-MM`)가 그 폴더 안의 읽기 순서입니다. 각 폴더의 `README.md`가 그 폴더의 진입 안내(MOC) 역할을 합니다.

폴더를 개념 축으로 나눈 이유는 확장성 때문입니다. 새 주제(예: Admission Webhook 전용편, Probe/Health 전용편)가 생기면 그 개념이 속한 대주제 폴더에 파일 번호만 늘려 넣으면 됩니다. 아직 문서가 없는 공식 대분류는 `_containers/`·`_policies/`처럼 언더스코어 stub으로 남겨, 나중에 문서가 쌓이면 정식 번호 폴더로 승격합니다.

| 폴더 | 공식 concepts | 한 줄 요약 |
|------|--------------|-----------|
| [`00_overview/`](00_overview/README.md) | Overview | 클러스터란 무엇이고 어떻게 띄우는가 — 입문·설치 |
| [`01_workloads/`](01_workloads/README.md) | Workloads | Pod·Deployment·컨트롤러·Job/CronJob/DaemonSet |
| [`02_configuration/`](02_configuration/README.md) | Configuration | ConfigMap·Secret·자원 요청/제한·설정 주입 |
| [`03_storage/`](03_storage/README.md) | Storage | Volume·PV·PVC·StorageClass·상태 관리 |
| [`04_networking/`](04_networking/README.md) | Services·Networking | Pod 통신 → Service → DNS → Ingress/Gateway |
| [`05_scheduling/`](05_scheduling/README.md) | Scheduling·Eviction | 노드 배치·토폴로지 분산·오토스케일링 |
| [`06_architecture/`](06_architecture/README.md) | Cluster Architecture | Control Plane·etcd·API 보안·업그레이드 |
| [`07_security/`](07_security/README.md) | Security | RBAC·ServiceAccount·인증·Admission |
| [`08_extending/`](08_extending/README.md) | Extending Kubernetes | CRD·Operator 패턴·DB/메시징 Operator |
| [`09_operations/`](09_operations/README.md) | Cluster Administration | 관측·트러블슈팅·kubectl 고급·CKA |
| [`10_packaging/`](10_packaging/README.md) | (비공식) | Helm·Kustomize 패키징 도구 |
| [`11_devtools/`](11_devtools/README.md) | (비공식) | K8s 위 CI/CD·GitOps·레지스트리 도구 |
| [`_containers/`](_containers/README.md) | Containers | 이미지·런타임·lifecycle hook (작성 예정) |
| [`_policies/`](_policies/README.md) | Policies | LimitRange·ResourceQuota (작성 예정) |

`10_packaging`과 `11_devtools`는 공식 concepts에는 없는 주제입니다. Helm·Kustomize는 매니페스트를 다루는 패키징 도구이고, Jenkins·SonarQube·ArgoCD·Harbor는 K8s 위에 올려 쓰는 CI/CD·GitOps·레지스트리 도구라, 순정 개념과 섞이지 않도록 별도 대주제로 분리했습니다.



## 대주제별 소개

> 위 표가 *어디에 무엇이 있나*를 짚는다면, 이 절은 각 폴더가 *무엇을 왜 다루는가*를 한 단계 풀어 소개합니다. 파일 한 줄 소개는 본문을 읽기 전 "이 문서에서 무엇을 얻는가"를 미리 잡아 줍니다.

### 00_overview — 개요

클러스터를 직접 띄워 보고, 이후 모든 폴더가 딛고 설 실습 토대를 만듭니다.

- **00-01 로컬 클러스터 구성** — minikube·kind·k3d·kubeadm으로 프로덕션 유사 환경을 로컬에서 빠르게 재현해, 뒤 문서의 실습 바닥을 깝니다.

### 01_workloads — 워크로드

애플리케이션을 감싸 실행하는 리소스를 봅니다. 상시 실행되는 워크로드부터 끝나는 배치 작업까지 한 묶음입니다.

- **01-01 핵심 워크로드** — Pod·Deployment·Service가 각각 무엇을 책임지는지, 셋의 역할 분담으로 애플리케이션이 어떻게 굴러가는지 봅니다.
- **01-02 배치 워크로드** — Job·CronJob·DaemonSet·InitContainer·Sidecar가 각각 어떤 의도를 표현하는지, 일회성·주기성·노드별 워크로드를 한 묶음으로 봅니다.

### 02_configuration — 설정

애플리케이션에 설정과 자원 한도를 주입하는 방법을 봅니다.

- **02-01 K8s 환경변수와 Spring 설정 주입** — ConfigMap 환경변수가 Spring `application.yml`에 어떻게 적용되는지, 설정 주입의 두 세계를 잇습니다.
- **02-02 자원 관리** — Requests/Limits와 QoS로 안정성을 어떻게 확보하는지, cgroup이 보는 메모리와 애플리케이션이 보는 메모리의 관계를 봅니다.

### 03_storage — 저장소

파드가 사라져도 데이터를 남기는 스토리지 모델을 봅니다.

- **03-01 스토리지와 상태** — Stateless와 Stateful이 스토리지를 다루는 방식이 어떻게 갈리는지, Volume·PV·PVC로 상태를 어디에 두는지 봅니다.

### 04_networking — 네트워킹

Pod IP는 바뀐다는 전제에서 출발해, 트래픽이 Linux netns부터 외부 진입까지 어떤 계층을 거쳐 흐르는지 한 단씩 올라갑니다. 파일 번호 순서가 곧 추상화 상승 순서입니다.

- **04-01 네트워킹** — 트래픽이 거치는 계층 전체를 조망해 이후 문서의 지도를 그립니다.
- **04-02 Pod 네트워크와 Linux 기반** — pause·netns·veth·Pod CIDR·CNI·kube-proxy dataplane이 실제로 어떻게 동작하는지 Linux 수준까지 내려가 봅니다. ([인터랙티브 시각화](04_networking/04-02-pod-network.html))
- **04-03 오버레이와 노드 간 트래픽** — VXLAN·네이티브 라우팅·BGP·ECMP·MetalLB가 노드 간 Pod 트래픽과 외부 LoadBalancer를 어떻게 만드는지 봅니다. ([인터랙티브 시각화](04_networking/04-03-overlay-bgp.html))
- **04-04 Service와 EndpointSlice** — 변하는 Pod 집합을 안정적인 진입점으로 노출하는 추상화를 EndpointSlice 단위로 봅니다.
- **04-05 DNS와 CoreDNS** — Service 이름이 어떻게 IP로 해석되는지, CoreDNS가 이름 해석을 어떻게 책임지는지 봅니다.
- **04-06 Ingress와 Gateway API** — 외부 HTTP 트래픽 라우팅이 Ingress에서 Gateway API로 어떻게 진화하고, cert-manager가 인증서를 어떻게 자동화하는지 봅니다.

### 05_scheduling — 스케줄링

파드를 어느 노드에 둘지, 동시 중단을 얼마나 허용할지, 부하에 따라 어떻게 늘리고 줄일지를 봅니다.

- **05-01 스케줄링과 노드 선택** — kube-scheduler의 Filter·Score와 nodeAffinity·Taint가 어떻게 보완되는지 봅니다.
- **05-02 토폴로지 분산과 중단 정책** — Topology Spread·PodDisruptionBudget·PriorityClass·Eviction이 가용성을 어떻게 만드는지 봅니다.
- **05-03 오토스케일링** — HPA·VPA·KEDA가 어떻게 역할을 나누는지 봅니다.

### 06_architecture — 클러스터 내부 구조

Control Plane과 노드가 어떻게 맞물려 돌아가는지, 그 상태를 어떻게 지키고 복구하는지를 봅니다.

- **06-01 클러스터 업그레이드와 ETCD 백업·복구** — kubeadm 업그레이드와 etcd 재해 복구를 어떤 절차로 다루는지, etcd Raft 합의가 일관성을 어떻게 지키는지 봅니다.
- **06-02 TLS와 API 접근 보안** — 컨트롤 플레인 PKI(API 서버·etcd·kubelet 인증서)가 어떻게 연결되는지 봅니다.

### 07_security — 보안

누가 무엇을 할 수 있는지, 권한을 어떻게 좁히는지를 봅니다.

- **07-01 RBAC과 보안** — RBAC·ServiceAccount 토큰·Admission(Webhook/VAP)·NetworkPolicy를 어떻게 묶는지 봅니다.

### 08_extending — 확장

CRD와 Controller로 Kubernetes 위에 우리만의 리소스를 얹어, Stateful 워크로드의 Day-2 운영을 자동화합니다.

- **08-01 Operator 패턴** — CRD와 컨트롤러가 어떻게 연동돼 "원하는 상태"를 코드로 표현하는지 봅니다.
- **08-02 MySQL Operator** — MySQL HA를 어떻게 선언적으로 자동화하는지 봅니다.
- **08-03 PostgreSQL Operator** — CloudNativePG의 복제·백업 전략을 봅니다.
- **08-04 Redis Operator** — Cluster와 Sentinel이 언제 갈라지는지 봅니다.
- **08-05 Kafka Operator** — Strimzi로 Kafka를 선언적으로 관리하는 법을 봅니다.
- **08-06 Redpanda Operator** — Strimzi와 Redpanda Operator의 차이를 봅니다.

### 09_operations — Day-2 운영

클러스터를 안정적으로 굴리기 위한 관측·진단·조회 주제를 모았습니다.

- **09-01 모니터링과 트러블슈팅** — 클러스터 장애를 어떻게 체계적으로 진단하는지 봅니다.
- **09-02 OOMKilled 사례 분석** — 6GB Pod가 반복 OOMKilled되는 실제 사례에서 JVM heap과 cgroup이 보는 메모리가 왜 어긋나는지 추적합니다.
- **09-03 JSONPath와 kubectl 고급 조회** — 반복 조회·스크립팅에 필요한 출력 제어를 익힙니다.
- **09-04 CKA 대비와 문제 풀이 전략** — 시험 범위를 실무 문서와 어떻게 잇는지 봅니다.

### 10_packaging — 패키징 도구

반복되는 매니페스트를 패키지로 묶어 환경별 차이를 선언적으로 관리합니다.

- **10-01 Helm 기초** — 왜 생짜 매니페스트 대신 Helm을 쓰는지, 템플릿·values의 기본을 잡습니다.
- **10-02 Helm 고급** — 재사용 가능한 차트를 어떻게 설계하는지 봅니다.
- **10-03 Kustomize** — Helm 없이 환경별 차이를 patch로 선언적으로 관리하는 길을 봅니다.

### 11_devtools — DevTools와 GitOps

Jenkins·SonarQube·ArgoCD·Harbor를 K8s 위에 올려 개발 생산성과 배포 자동화를 얻습니다. ArgoCD 상세 운영은 별도 [`argocd`](../argocd/README.md) 카테고리로 넘깁니다.

- **11-01 Jenkins on K8s** — K8s 네이티브 Jenkins가 무엇이 달라지는지(동적 Agent 등) 봅니다.
- **11-02 SonarQube on K8s** — SonarQube의 영속성 전략을 봅니다.
- **11-03 ArgoCD와 GitOps** — Git을 단일 진실 공급원으로 삼는 배포 모델을 입문 수준으로 봅니다.
- **11-04 Harbor** — 이미지와 OCI Helm chart를 어디서 통합 관리하는지 봅니다.



## 딥다이브 전체 지도

> 위 절이 *무엇이 어디 있고 무엇을 다루나*를 답한다면, 이 절은 *Kubernetes 본질을 어디까지 깊게 파야 하는가*를 답합니다. 딥다이브 로드맵의 섹션별 키워드 전체는 [roadmap.md](roadmap.md)에 원문 그대로 옮겨 두었습니다. 아래는 그 24개 대주제를 6개 학습 단계로 묶어, 우리 폴더·미작성 갭과 연결한 네비게이션입니다.

한 문장으로 줄이면, 사용자는 원하는 상태를 API Server에 선언하고, Control Plane은 현재 상태와 원하는 상태를 비교하며, Scheduler는 Pod를 Node에 배치하고, kubelet은 컨테이너 런타임을 통해 Pod를 실행하며, Service와 CNI는 네트워크를 이어주고, Controller는 계속 상태를 맞춥니다.

| 단계 | 대주제 묶음 | 진입 폴더 | 갭(미작성) |
|------|-----------|----------|-----------|
| 1 기본 리소스 | Pod·Deployment·Service·ConfigMap·Secret·Namespace | [`01_workloads`](01_workloads/README.md)·[`02_configuration`](02_configuration/README.md)·[`03_storage`](03_storage/README.md) | — |
| 2 운영 배포 | Probe·Requests/Limits·RollingUpdate·HPA·PDB·SecurityContext | [`02_configuration`](02_configuration/README.md)·[`05_scheduling`](05_scheduling/README.md) | Probe/Health 전용편, RollingUpdate/Rollback 전용편 |
| 3 네트워크 | Service·EndpointSlice·CoreDNS·Ingress·Gateway·NetworkPolicy·CNI | [`04_networking`](04_networking/README.md)·[`07_security`](07_security/README.md) | — |
| 4 내부 구조 | API Server·etcd·Scheduler·Controller Manager·kubelet·runtime·kube-proxy | [`06_architecture`](06_architecture/README.md)·[`04_networking`](04_networking/README.md) | Control Plane 흐름 전용편 |
| 5 확장 | Admission Webhook·CRD·Controller·Operator·Finalizer·OwnerReference | [`08_extending`](08_extending/README.md)·[`07_security`](07_security/README.md) | Mini Operator 직접 작성 실습편 |
| 6 운영·장애 | Observability·Troubleshooting·Backup·Upgrade·Security | [`09_operations`](09_operations/README.md)·[`06_architecture`](06_architecture/README.md) | 분산 트레이싱(Tempo/OTel) 전용편 |

각 단계의 핵심 키워드 전체와 심화 실습 후보는 [roadmap.md](roadmap.md)에 정리돼 있습니다. 미작성 갭은 위 표의 "갭" 열에 모았습니다 — Probe/Health·RollingUpdate/Rollback 전용편, Control Plane 흐름 전용편, Mini Operator 실습편, 분산 트레이싱 전용편. 이 갭들은 각각 `01_workloads`·`06_architecture`·`08_extending`·`09_operations`에 파일 번호를 늘려 채웁니다.



## 점검 질문 절 (`## N. 점검 질문`)

> 점검 질문은 별도 문서가 아니라 각 본문 끝의 한 절로 들어 있습니다.

각 본문은 마지막 콘텐츠 절 뒤에 `## N. 점검 질문` 절을 두어, 그 장에서 짚어야 할 심화 Q&A를 개념 설명과 같은 문서에서 이어 읽게 합니다(예: `01_workloads/01-02.배치 워크로드.md`의 `## 8. 점검 질문`). 예전에는 `{제목} 점검.md`를 짝 파일로 분리했지만, 복습할 때 파일을 오가는 비용이 커서 본문 안으로 흡수했습니다. hands-on 실습이 필요하면 각 본문의 `실습 환경` 서술을 GCP K8s 클러스터 위에서 수행합니다. 다만 `00_overview`의 로컬 클러스터 구성, `01_workloads/01-01.핵심 워크로드`, `03_storage/03-01.스토리지와 상태`처럼 원래 점검 질문이 없던 일부 입문 편은 점검 절 없이 본문만 있습니다.



## 실습 환경

> 개인 GCP K8s 클러스터를 기준으로 하되, 본문은 가능한 한 범용 명령으로 유지합니다.

현재 기준 실습은 개인 GCP K8s 클러스터(dev-server 1~3, asia-northeast3-a, kubeadm v1.31.14)에서 수행합니다. 환경이 바뀌어도 본문이 유지되도록 환경 특화 명령은 각 본문의 `실습 환경`·`실습 기록` 서술로 몰아 두고, 개념 본문은 `kubectl`·Helm 범용 명령으로 씁니다. 환경 상세는 `gcp` 스킬 문서에서 관리합니다.



## 예정 주제 — OpenShift / OKD (TBD)

> 순정 Kubernetes 딥다이브를 어느 정도 훑은 다음, 그 위에 기업용 기능을 얹은 *배포판*을 봅니다. 순정 K8s가 "엔진"이라면 OpenShift는 웹 콘솔·인증·이미지 빌드까지 조립한 "완제품"입니다.

- **OpenShift / OKD** — Red Hat이 K8s에 웹 콘솔·OAuth 로그인·이미지 빌드(S2I/BuildConfig)·Route(내장 Ingress 추상화)를 통합한 배포판. 조작 CLI는 `kubectl` 상위호환인 `oc`. **OKD**는 그 무료 오픈소스판(RHEL↔CentOS/Fedora 관계와 같다). 순정 K8s를 아는 사람이 "그래서 순정과 뭐가 다른가"를 Route·S2I·OAuth provider 중심으로 익히는 편입니다. (실환경 예시: 미래에셋 3.0.3 환경이 OKD로 구축돼 `oc get nodes`·웹 콘솔로 운영됩니다.)

경계: Pod·Deployment·Service 같은 순정 K8s 리소스는 이 카테고리 본문이 다룹니다. 여기 예정 범위는 **OpenShift 고유 추상화**(Route·BuildConfig·DeploymentConfig·oc)만입니다. GitOps 배포는 [`argocd`](../argocd/README.md)로 갑니다.



## 관련 문서

> service-mesh·argocd·devops 카테고리로 이어지는 선후 관계와, 같은 책을 정독한 노트를 함께 봅니다.

- [service-mesh MOC](../service-mesh/README.md) — 본 카테고리의 다음 단계. Pod 간 트래픽 제어·mTLS·관측성을 메시 계층에서 해결한다
- [argocd MOC](../argocd/README.md) — ArgoCD 상세 시리즈. AppProject·App of Apps·ApplicationSet·Image Updater 운영을 별도로 다룬다
- [Kubernetes in Action 정독본](../book/kubernetes-in-action/README.md) — 같은 개념을 저자 순서대로 쌓아 올린 책-종속 노트. 개념이 겹치면 이 개념 노트로 링크를 건다
- [devops MOC](../../07_devops/README.md) — CI/CD 파이프라인 자체 설계는 이곳
