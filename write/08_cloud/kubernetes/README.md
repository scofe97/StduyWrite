---
title: 08_cloud/kubernetes — Kubernetes 실전 운영
tags: [moc, kubernetes, helm, operator, argocd]
status: final
source:
  - ../../../poc/03_CloudNative/02-kubernetes/README.md@8ac9e97
related:
  - roadmap.md
  - ../README.md
  - ../argocd/README.md
  - ../service-mesh/README.md
  - ../../07_devops/README.md
updated: 2026-06-25
---

# 08_cloud/kubernetes

> Kubernetes 핵심 개념을 로컬에서 체득하고, Helm·Operator 패턴으로 MySQL·PostgreSQL·Kafka 같은 Stateful 워크로드를 운영하며, ArgoCD로 GitOps를 구현하는 경로까지 한 흐름으로 정리한다.

이 카테고리는 "클러스터 안에서 어떻게 연결되고 노출되는가"까지를 기본 범위로 둔다. Service Mesh처럼 서비스 간 L7 정책, mTLS, 세밀한 트래픽 제어가 본격적으로 필요해지는 지점부터는 별도 `service-mesh` 카테고리로 넘긴다.
ArgoCD는 Kubernetes 흐름 안에서 입문 수준으로 소개하지만, 상세 운영과 App of Apps/ApplicationSet/Image Updater는 별도 `argocd` 카테고리로 분리했다.



## 폴더 구조와 학습 흐름
> 기반 개념, 네트워킹, 플랫폼 도구, 운영 주제를 비슷한 개념끼리 묶어 다섯 개 폴더로 나눴다. 폴더 안의 파일 번호(`NN-MM`)가 곧 학습 순서다. 각 폴더의 `README.md` 가 그 폴더의 진입 안내(MOC) 역할을 한다.

| 폴더 | 묶은 장 | 한 줄 요약 |
|------|---------|-----------|
| [`01_foundation/`](01_foundation/README.md) | Ch01~03 | 로컬 클러스터·핵심 워크로드·스토리지 — 기반 개념 |
| [`02_networking/`](02_networking/README.md) | Ch04 | Pod 통신부터 외부 트래픽 진입까지 네트워크 계층 |
| [`03_platform/`](03_platform/README.md) | Ch05~06 | Helm·Kustomize 패키징 + Operator로 DB·미들웨어 운영 |
| [`04_devtools/`](04_devtools/README.md) | Ch07 | Jenkins·SonarQube·ArgoCD·Harbor — CI/CD·GitOps 도구 |
| [`05_operations/`](05_operations/README.md) | Ch08~10 | 클러스터 유지보수·스케줄링·관측·보안 등 Day-2 운영 |

폴더는 Jenkins 학습 묶음(`07_devops/02_Jenkins`)과 같은 모델을 따른다. 단일 챕터가 한 폴더를 이루지 않도록 인접한 운영 주제(Ch08~10)는 `05_operations` 로, 패키징과 Operator(Ch05~06)는 `03_platform` 으로 합쳤다.

### 01_foundation — 기반 (Ch01~03)
로컬 클러스터를 띄우고, Pod/Deployment/Service 같은 핵심 워크로드와 스토리지 모델을 먼저 체득한다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01 | [로컬 클러스터 구성](01_foundation/01-01.%EB%A1%9C%EC%BB%AC%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EA%B5%AC%EC%84%B1.md) | 프로덕션 유사 환경을 어떻게 빠르게 재현하는가? |
| 02 | [핵심 워크로드](01_foundation/01-02.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md) | Pod·Deployment·Service의 역할 분담은? |
| 03 | [스토리지와 상태](01_foundation/01-03.%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80%EC%99%80%20%EC%83%81%ED%83%9C.md) | Stateless와 Stateful의 스토리지 전략 차이는? |

### 02_networking — 네트워킹 (Ch04)
Pod 간 통신 모델부터 외부 트래픽 수용까지 네트워크 계층을 한 챕터로 묶는다. 파일 번호 순서대로 읽으면 Linux 기반 → 노드 간 트래픽 → Service → DNS → Ingress 순으로 한 단씩 위로 올라간다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 02-01 | [네트워킹](02_networking/02-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) | 트래픽은 어떤 계층을 거쳐 흐르는가? |
| 02-02 | [Pod 네트워크와 Linux 기반](02_networking/02-02.Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20Linux%20%EA%B8%B0%EB%B0%98.md) | Pause·netns·veth·Pod CIDR·CNI·kube-proxy dataplane은 실제 어떻게 동작하는가? ([인터랙티브 시각화](02_networking/02-02-pod-network.html)) |
| 02-03 | [오버레이와 노드 간 트래픽](02_networking/02-03.%EC%98%A4%EB%B2%84%EB%A0%88%EC%9D%B4%EC%99%80%20%EB%85%B8%EB%93%9C%20%EA%B0%84%20%ED%8A%B8%EB%9E%98%ED%94%BD.md) | VXLAN·네이티브 라우팅·BGP·ECMP·MetalLB는 노드 간 Pod 트래픽과 외부 LoadBalancer를 어떻게 만드는가? ([인터랙티브 시각화](02_networking/02-03-overlay-bgp.html)) |
| 02-04 | [Service와 EndpointSlice](02_networking/02-04.Service%EC%99%80%20EndpointSlice.md) | 변하는 Pod 집합을 어떻게 안정적인 진입점으로 노출하는가? |
| 02-05 | [DNS와 CoreDNS](02_networking/02-05.DNS%EC%99%80%20CoreDNS.md) | Service 이름은 어떻게 IP로 해석되는가? |
| 02-06 | [Ingress와 Gateway API](02_networking/02-06.Ingress%EC%99%80%20Gateway%20API.md) | 외부 트래픽 라우팅은 어떻게 진화하고, cert-manager는 어떻게 인증서를 자동화하는가? |

### 03_platform — 패키지 관리와 Operator (Ch05~06)
반복되는 매니페스트를 Helm 차트로 묶고 직접 차트를 개발한다. 이어서 CRD + Controller(Operator)로 DB·미들웨어의 Day-2 운영을 자동화한다. 두 주제는 "선언적으로 워크로드를 다룬다" 는 공통 축으로 한 폴더에 묶었다.

**패키지 관리 (Ch05)**

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 03-01 | [Helm 기초](03_platform/03-01.Helm%20%EA%B8%B0%EC%B4%88.md) | 왜 매니페스트 대신 Helm을 쓰는가? |
| 03-02 | [Helm 고급](03_platform/03-02.Helm%20%EA%B3%A0%EA%B8%89.md) | 재사용 가능한 차트를 어떻게 설계하는가? |
| 03-03 | [Kustomize](03_platform/03-03.Kustomize.md) | Helm 없이 환경별 차이를 어떻게 선언적으로 관리하는가? |
| 03-04 | [K8s 환경변수와 Spring 설정 주입](03_platform/03-04.K8s%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98%EC%99%80%20Spring%20%EC%84%A4%EC%A0%95%20%EC%A3%BC%EC%9E%85.md) | ConfigMap 환경변수는 Spring YAML에 어떻게 적용되는가? |

**Operator 패턴과 DB·미들웨어 (Ch06)**
개념부터 DB(MySQL·PostgreSQL·Redis), 메시징(Kafka·Redpanda)까지 한 묶음이다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 03-05 | [Operator 패턴](03_platform/03-05.Operator%20%ED%8C%A8%ED%84%B4.md) | CRD와 컨트롤러는 어떻게 연동되는가? |
| 03-06 | [MySQL Operator](03_platform/03-06.MySQL%20Operator.md) | MySQL HA를 어떻게 자동화하는가? |
| 03-07 | [PostgreSQL Operator](03_platform/03-07.PostgreSQL%20Operator.md) | CloudNativePG의 복제·백업 전략은? |
| 03-08 | [Redis Operator](03_platform/03-08.Redis%20Operator.md) | Cluster와 Sentinel은 언제 갈라지는가? |
| 03-09 | [Kafka Operator](03_platform/03-09.Kafka%20Operator.md) | Strimzi로 Kafka를 선언적으로 관리하는 법은? |
| 03-10 | [Redpanda Operator](03_platform/03-10.Redpanda%20Operator.md) | Strimzi와 Redpanda Operator는 뭐가 다른가? |

### 04_devtools — DevTools와 GitOps (Ch07)
Jenkins·SonarQube·ArgoCD를 하나의 흐름으로 묶어 개발 생산성과 배포 자동화를 얻는 단계다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 04-01 | [Jenkins on K8s](04_devtools/04-01.Jenkins%20on%20K8s.md) | K8s 네이티브 Jenkins는 뭐가 달라지는가? |
| 04-02 | [SonarQube on K8s](04_devtools/04-02.SonarQube%20on%20K8s.md) | SonarQube 영속성 전략은? |
| 04-03 | [ArgoCD와 GitOps](04_devtools/04-03.ArgoCD%EC%99%80%20GitOps.md) | Git을 단일 진실 공급원으로 삼는 배포는? |
| 04-04 | [Harbor](04_devtools/04-04.Harbor.md) | 이미지와 OCI Helm chart를 어디서 통합 관리하는가? |

### 05_operations — 운영 심화·스케줄링·관측 (Ch08~10)
클러스터를 안정적으로 굴리기 위한 Day-2 운영 주제를 한 폴더에 모았다. 유지보수·인증(Ch08), 워크로드를 어디에 어떻게 둘지(Ch09), 그리고 관측·보안·자원·스케일링(Ch10)이 차례로 이어진다.

**운영 심화 (Ch08) — 클러스터 유지보수와 인증, 조회 자동화, 시험 대비**

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 05-01 | [클러스터 업그레이드와 ETCD 백업·복구](05_operations/05-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | kubeadm 업그레이드와 etcd 재해 복구는 어떤 절차로 다루는가? |
| 05-02 | [TLS와 API 접근 보안](05_operations/05-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | 컨트롤 플레인 PKI(API 서버·etcd·kubelet)는 어떻게 연결되는가? |
| 05-03 | [JSONPath와 kubectl 고급 조회](05_operations/05-03.JSONPath%EC%99%80%20kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | 반복 조회와 스크립팅에 필요한 출력 제어는 어떻게 하는가? |
| 05-04 | [CKA 대비와 문제 풀이 전략](05_operations/05-04.CKA%20%EB%8C%80%EB%B9%84%EC%99%80%20%EB%AC%B8%EC%A0%9C%20%ED%92%80%EC%9D%B4%20%EC%A0%84%EB%9E%B5.md) | 시험 범위를 실무 문서와 어떻게 연결해 준비하는가? |

**스케줄링과 배치 (Ch09)**
어디에 둘지(Affinity·Taint), 동시 중단을 얼마나 허용할지(PDB·PriorityClass), 그리고 일회성·주기성·노드별 워크로드를 한 묶음으로 본다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 05-05 | [스케줄링과 노드 선택](05_operations/05-05.%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%EA%B3%BC%20%EB%85%B8%EB%93%9C%20%EC%84%A0%ED%83%9D.md) | kube-scheduler의 Filter·Score와 nodeAffinity·Taint는 어떻게 보완되는가? |
| 05-06 | [토폴로지 분산과 중단 정책](05_operations/05-06.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EB%B6%84%EC%82%B0%EA%B3%BC%20%EC%A4%91%EB%8B%A8%20%EC%A0%95%EC%B1%85.md) | Topology Spread·PodDisruptionBudget·PriorityClass·Eviction은 가용성을 어떻게 만드는가? |
| 05-07 | [배치 워크로드](05_operations/05-07.%EB%B0%B0%EC%B9%98%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md) | Job·CronJob·DaemonSet·InitContainer·Sidecar는 각각 어떤 의도를 표현하는가? |

**관측·보안·자원·스케일링 (Ch10)**
관측성, 보안, 자원 관리, 스케일링을 한 묶음으로 읽는다. 자원 관리(05-10)가 오토스케일링(05-11)의 입력이 되는 인과 순서로 정렬했다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 05-08 | [모니터링과 트러블슈팅](05_operations/05-08.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EA%B3%BC%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.md) | 클러스터 장애를 어떻게 체계적으로 진단하는가? |
| 05-09 | [RBAC과 보안](05_operations/05-09.RBAC%EA%B3%BC%20%EB%B3%B4%EC%95%88.md) | RBAC·ServiceAccount 토큰·Admission(Webhook/VAP)·NetworkPolicy를 어떻게 묶는가? |
| 05-10 | [자원 관리](05_operations/05-10.%EC%9E%90%EC%9B%90%20%EA%B4%80%EB%A6%AC.md) | Requests/Limits와 QoS로 안정성을 어떻게 확보하는가? |
| 05-11 | [오토스케일링](05_operations/05-11.%EC%98%A4%ED%86%A0%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | HPA·VPA·KEDA는 어떻게 역할을 나누는가? |
| 05-12 | [OOMKilled 사례 분석](05_operations/05-12.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) | 6GB Pod가 반복 OOMKilled — JVM heap과 cgroup이 보는 메모리는 왜 어긋나는가? (Endowus 사례) |



## 대주제·소주제·챕터 소개

> 위의 폴더 표가 *어디에 무엇이 있나*를 짚는다면, 이 절은 각 폴더(대주제)와 그 안의 그룹(소주제)이 *무엇을 왜 다루는가*를 한 단계 더 풀어 소개한다. 챕터 한 줄 소개는 본문을 읽기 전 "이 문서에서 무엇을 얻는가"를 미리 잡아 준다.

### 01_foundation — 기반 (대주제)

클러스터를 직접 띄우고, 워크로드와 스토리지라는 두 기둥을 손으로 만져 본다. 이후 모든 폴더가 이 위에 쌓이므로, 여기서 Pod·Deployment·Service·PV의 기본 감각을 먼저 잡는다.

- **01-01 로컬 클러스터 구성** — 프로덕션 유사 환경을 로컬에서 빠르게 재현해, 뒤 챕터의 실습 토대를 만든다.
- **01-02 핵심 워크로드** — Pod·Deployment·Service가 각각 무엇을 책임지는지, 셋의 역할 분담으로 애플리케이션이 어떻게 굴러가는지 본다.
- **01-03 스토리지와 상태** — Stateless와 Stateful이 스토리지를 다루는 방식이 어떻게 갈리는지, Volume·PV·PVC로 상태를 어디에 두는지 본다.

### 02_networking — 네트워킹 (대주제)

Pod IP는 바뀐다는 전제에서 출발해, 트래픽이 Linux netns부터 외부 진입까지 어떤 계층을 거쳐 흐르는지 한 단씩 위로 올라간다. 파일 번호 순서가 곧 추상화 상승 순서다.

- **02-01 네트워킹** — 트래픽이 거치는 계층 전체를 조망해 이후 챕터의 지도를 그린다.
- **02-02 Pod 네트워크와 Linux 기반** — pause·netns·veth·Pod CIDR·CNI·kube-proxy dataplane이 실제로 어떻게 동작하는지 Linux 수준까지 내려가 본다.
- **02-03 오버레이와 노드 간 트래픽** — VXLAN·네이티브 라우팅·BGP·ECMP·MetalLB가 노드 간 Pod 트래픽과 외부 LoadBalancer를 어떻게 만드는지 본다.
- **02-04 Service와 EndpointSlice** — 변하는 Pod 집합을 안정적인 진입점으로 노출하는 추상화를 EndpointSlice 단위로 본다.
- **02-05 DNS와 CoreDNS** — Service 이름이 어떻게 IP로 해석되는지, CoreDNS가 이름 해석을 어떻게 책임지는지 본다.
- **02-06 Ingress와 Gateway API** — 외부 HTTP 트래픽 라우팅이 Ingress에서 Gateway API로 어떻게 진화하고, cert-manager가 인증서를 어떻게 자동화하는지 본다.

### 03_platform — 패키징과 Operator (대주제)

"선언적으로 워크로드를 다룬다"는 한 축으로 두 소주제를 묶었다. 반복되는 매니페스트를 패키지로 묶는 일과, CRD+Controller로 운영 자체를 자동화하는 일이다.

**소주제 ① 패키지 관리 (03-01~03-04)** — 매니페스트 중복을 Helm·Kustomize로 걷어내고, 설정 주입을 Spring 앱과 잇는다.

- **03-01 Helm 기초** — 왜 생짜 매니페스트 대신 Helm을 쓰는지, 템플릿·values의 기본을 잡는다.
- **03-02 Helm 고급** — 재사용 가능한 차트를 어떻게 설계하는지 본다.
- **03-03 Kustomize** — Helm 없이 환경별 차이를 patch로 선언적으로 관리하는 길을 본다.
- **03-04 K8s 환경변수와 Spring 설정 주입** — ConfigMap 환경변수가 Spring `application.yml`에 어떻게 적용되는지, 설정 주입의 두 세계를 잇는다.

**소주제 ② Operator 패턴과 DB·미들웨어 (03-05~03-10)** — 개념부터 MySQL·PostgreSQL·Redis·Kafka·Redpanda까지, Stateful 워크로드의 Day-2 운영을 Operator로 자동화한다.

- **03-05 Operator 패턴** — CRD와 컨트롤러가 어떻게 연동돼 "원하는 상태"를 코드로 표현하는지 본다.
- **03-06 MySQL Operator** — MySQL HA를 어떻게 선언적으로 자동화하는지 본다.
- **03-07 PostgreSQL Operator** — CloudNativePG의 복제·백업 전략을 본다.
- **03-08 Redis Operator** — Cluster와 Sentinel이 언제 갈라지는지 본다.
- **03-09 Kafka Operator** — Strimzi로 Kafka를 선언적으로 관리하는 법을 본다.
- **03-10 Redpanda Operator** — Strimzi와 Redpanda Operator의 차이를 본다.

### 04_devtools — DevTools와 GitOps (대주제)

Jenkins·SonarQube·ArgoCD·Harbor를 한 흐름으로 묶어 개발 생산성과 배포 자동화를 K8s 위에서 얻는다. ArgoCD 상세 운영은 별도 `argocd` 카테고리로 넘긴다.

- **04-01 Jenkins on K8s** — K8s 네이티브 Jenkins가 무엇이 달라지는지(동적 Agent 등) 본다.
- **04-02 SonarQube on K8s** — SonarQube의 영속성 전략을 본다.
- **04-03 ArgoCD와 GitOps** — Git을 단일 진실 공급원으로 삼는 배포 모델을 입문 수준으로 본다.
- **04-04 Harbor** — 이미지와 OCI Helm chart를 어디서 통합 관리하는지 본다.

### 05_operations — Day-2 운영 (대주제)

클러스터를 안정적으로 굴리기 위한 운영 주제를 세 소주제로 모았다. 유지보수·인증, 워크로드 배치, 관측·보안·자원·스케일링 순으로 이어진다.

**소주제 ① 유지보수·인증·조회·시험 (05-01~05-04)**

- **05-01 클러스터 업그레이드와 ETCD 백업·복구** — kubeadm 업그레이드와 etcd 재해 복구를 어떤 절차로 다루는지 본다.
- **05-02 TLS와 API 접근 보안** — 컨트롤 플레인 PKI(API 서버·etcd·kubelet)가 어떻게 연결되는지 본다.
- **05-03 JSONPath와 kubectl 고급 조회** — 반복 조회·스크립팅에 필요한 출력 제어를 익힌다.
- **05-04 CKA 대비와 문제 풀이 전략** — 시험 범위를 실무 문서와 어떻게 잇는지 본다.

**소주제 ② 스케줄링과 배치 (05-05~05-07)** — 어디에 둘지, 동시 중단을 얼마나 허용할지, 일회성·주기성·노드별 워크로드를 한 묶음으로 본다.

- **05-05 스케줄링과 노드 선택** — kube-scheduler의 Filter·Score와 nodeAffinity·Taint가 어떻게 보완되는지 본다.
- **05-06 토폴로지 분산과 중단 정책** — Topology Spread·PodDisruptionBudget·PriorityClass·Eviction이 가용성을 어떻게 만드는지 본다.
- **05-07 배치 워크로드** — Job·CronJob·DaemonSet·InitContainer·Sidecar가 각각 어떤 의도를 표현하는지 본다.

**소주제 ③ 관측·보안·자원·스케일링 (05-08~05-12)** — 자원 관리가 오토스케일링의 입력이 되는 인과 순서로 정렬했다.

- **05-08 모니터링과 트러블슈팅** — 클러스터 장애를 어떻게 체계적으로 진단하는지 본다.
- **05-09 RBAC과 보안** — RBAC·ServiceAccount 토큰·Admission(Webhook/VAP)·NetworkPolicy를 어떻게 묶는지 본다.
- **05-10 자원 관리** — Requests/Limits와 QoS로 안정성을 어떻게 확보하는지 본다.
- **05-11 오토스케일링** — HPA·VPA·KEDA가 어떻게 역할을 나누는지 본다.
- **05-12 OOMKilled 사례 분석** — 6GB Pod가 반복 OOMKilled되는 실제 사례에서 JVM heap과 cgroup이 보는 메모리가 왜 어긋나는지 추적한다.



## Kubernetes 딥다이브 전체 지도

> 위 두 절이 *무엇이 어디 있고 무엇을 다루나*를 답한다면, 이 절은 *Kubernetes 본질을 어디까지 깊게 파야 하는가*를 답한다. 딥다이브 로드맵의 **섹션별 키워드 전체**는 [roadmap.md](roadmap.md)에 원문 그대로 옮겨 두었다. 아래는 그 24개 대주제를 6개 학습 단계로 묶어, 우리 보유 챕터·미작성 갭과 연결한 네비게이션이다.

한 문장으로 줄이면, 사용자는 원하는 상태를 API Server에 선언하고, Control Plane은 현재 상태와 원하는 상태를 비교하며, Scheduler는 Pod를 Node에 배치하고, kubelet은 컨테이너 런타임을 통해 Pod를 실행하며, Service와 CNI는 네트워크를 이어주고, Controller는 계속 상태를 맞춘다.

| 단계 | 대주제 묶음 | 진입 챕터 | 갭(미작성) |
|------|-----------|----------|-----------|
| 1 기본 리소스 | Pod·Deployment·Service·ConfigMap·Secret·Namespace | [01-01](01_foundation/01-01.%EB%A1%9C%EC%BB%AC%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EA%B5%AC%EC%84%B1.md)·[01-02](01_foundation/01-02.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md)·[01-03](01_foundation/01-03.%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80%EC%99%80%20%EC%83%81%ED%83%9C.md), [03-04](03_platform/03-04.K8s%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98%EC%99%80%20Spring%20%EC%84%A4%EC%A0%95%20%EC%A3%BC%EC%9E%85.md) | — |
| 2 운영 배포 | Probe·Requests/Limits·RollingUpdate·HPA·PDB·SecurityContext | [05-10](05_operations/05-10.%EC%9E%90%EC%9B%90%20%EA%B4%80%EB%A6%AC.md)·[05-11](05_operations/05-11.%EC%98%A4%ED%86%A0%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md)·[05-06](05_operations/05-06.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EB%B6%84%EC%82%B0%EA%B3%BC%20%EC%A4%91%EB%8B%A8%20%EC%A0%95%EC%B1%85.md), [05-12](05_operations/05-12.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) | Probe/Health 전용편, RollingUpdate/Rollback 전용편 |
| 3 네트워크 | Service·EndpointSlice·CoreDNS·Ingress·Gateway·NetworkPolicy·CNI | [02-01](02_networking/02-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md)~[02-06](02_networking/02-06.Ingress%EC%99%80%20Gateway%20API.md), [05-09](05_operations/05-09.RBAC%EA%B3%BC%20%EB%B3%B4%EC%95%88.md) | — |
| 4 내부 구조 | API Server·etcd·Scheduler·Controller Manager·kubelet·runtime·kube-proxy | [02-02](02_networking/02-02.Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20Linux%20%EA%B8%B0%EB%B0%98.md)·[02-03](02_networking/02-03.%EC%98%A4%EB%B2%84%EB%A0%88%EC%9D%B4%EC%99%80%20%EB%85%B8%EB%93%9C%20%EA%B0%84%20%ED%8A%B8%EB%9E%98%ED%94%BD.md), [05-01](05_operations/05-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md)·[05-02](05_operations/05-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md), [05-05](05_operations/05-05.%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%EA%B3%BC%20%EB%85%B8%EB%93%9C%20%EC%84%A0%ED%83%9D.md) | Control Plane(API Server·etcd·Scheduler·CM) 흐름 전용편 |
| 5 확장 | Admission Webhook·CRD·Controller·Operator·Finalizer·OwnerReference | [03-05](03_platform/03-05.Operator%20%ED%8C%A8%ED%84%B4.md)~[03-10](03_platform/03-10.Redpanda%20Operator.md), [05-09](05_operations/05-09.RBAC%EA%B3%BC%20%EB%B3%B4%EC%95%88.md) | Custom Controller/Operator 직접 작성(Mini Operator) 실습편 |
| 6 운영·장애 | Observability·Events·Logs·Metrics·Tracing·Troubleshooting·Backup·Upgrade·Security | [05-08](05_operations/05-08.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EA%B3%BC%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.md), [05-12](05_operations/05-12.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md), [05-01](05_operations/05-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | 분산 트레이싱(Tempo/OTel) 전용편 |

각 단계의 핵심 키워드 전체와 단계별 요약·심화 실습 후보 5종은 [roadmap.md](roadmap.md)에 정리돼 있다. 우리 자료의 미작성 갭은 위 표의 "갭" 열에 모았다 — Probe/Health·RollingUpdate/Rollback 전용편, Control Plane 흐름 전용편, Mini Operator 실습편, 분산 트레이싱 전용편.



## 점검 문서 (`* 점검.md`)
> 각 본문에는 같은 번호 체계를 따르는 점검 문서가 짝을 이룬다.

각 본문 옆에는 `{장}-{절}.{제목} 점검.md` 형식의 점검 문서가 같은 폴더에 함께 놓인다(예: `01_foundation/01-01.로컬 클러스터 구성.md` ↔ `01_foundation/01-01.로컬 클러스터 구성 점검.md`). 예전에는 `deepdive/` 한 폴더에 모았으나, 폴더링 과정에서 본문과 짝이 한눈에 보이도록 같은 토픽 폴더로 옮겼다. 본 카테고리의 원본 INVESTIGATE는 점검 질문 위주였기 때문에 점검 문서는 전부 `점검.md`다. hands-on 실습이 필요한 경우 각 본문의 `실습 환경` 서술과 점검 문서 상단 `실습 환경` 섹션을 조합해 GCP K8s 클러스터 위에서 수행한다.



## 실습 환경
> 개인 GCP K8s 클러스터를 기준으로 하되, 본문은 가능한 한 범용 명령으로 유지한다.

현재 기준 실습은 개인 GCP K8s 클러스터(dev-server 1~3, asia-northeast3-a, kubeadm v1.31.14)에서 수행한다. 환경이 바뀌어도 본문이 유지되도록 각 점검 문서 상단 `## 실습 환경` 섹션에만 환경 특화 명령을 두고, 본문은 `kubectl`·Helm 범용 명령으로 쓴다. 환경 상세는 [`gcp` 스킬 문서](../../../../.claude/skills/gcp/SKILL.md)에서 관리한다.



## 관련 문서
> service-mesh와 devops 카테고리로 이어지는 선후 관계를 함께 본다.

- [service-mesh MOC](../service-mesh/README.md) — 본 카테고리의 다음 단계. Pod 간 트래픽 제어·mTLS·관측성을 메시 계층에서 해결한다
- [argocd MOC](../argocd/README.md) — ArgoCD 상세 시리즈. AppProject, App of Apps, ApplicationSet, Image Updater 운영을 별도로 다룬다
- [devops MOC](../../07_devops/README.md) — CI/CD 파이프라인 자체 설계는 이곳
