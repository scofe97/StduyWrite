---
title: 09_cloud/kubernetes — Kubernetes 실전 운영
tags: [moc, kubernetes, helm, operator, argocd]
status: final
source:
  - ../../../poc/03_CloudNative/02-kubernetes/README.md@8ac9e97
related:
  - ../README.md
  - ../argocd/README.md
  - ../service-mesh/README.md
  - ../../08_devops/README.md
updated: 2026-05-09
---

# 09_cloud/kubernetes
---
> Kubernetes 핵심 개념을 로컬에서 체득하고, Helm·Operator 패턴으로 MySQL·PostgreSQL·Kafka 같은 Stateful 워크로드를 운영하며, ArgoCD로 GitOps를 구현하는 경로까지 한 흐름으로 정리한다.

이 카테고리는 "클러스터 안에서 어떻게 연결되고 노출되는가"까지를 기본 범위로 둔다. Service Mesh처럼 서비스 간 L7 정책, mTLS, 세밀한 트래픽 제어가 본격적으로 필요해지는 지점부터는 별도 `service-mesh` 카테고리로 넘긴다.
ArgoCD는 Kubernetes 흐름 안에서 입문 수준으로 소개하지만, 상세 운영과 App of Apps/ApplicationSet/Image Updater는 별도 `argocd` 카테고리로 분리했다.



## 학습 흐름
> 기반 개념, 플랫폼 도구, 운영 주제를 비슷한 개념끼리 같은 장 번호로 묶어 읽을 수 있도록 재정렬했다.

### Part 1 — 기반 (Ch01~03)
로컬 클러스터를 띄우고, Pod/Deployment/Service 같은 핵심 워크로드와 스토리지 모델을 먼저 체득한다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01 | [로컬 클러스터 구성](./01-01.로컬%20클러스터%20구성.md) | 프로덕션 유사 환경을 어떻게 빠르게 재현하는가? |
| 02 | [핵심 워크로드](./02-01.핵심%20워크로드.md) | Pod·Deployment·Service의 역할 분담은? |
| 03 | [스토리지와 상태](./03-01.스토리지와%20상태.md) | Stateless와 Stateful의 스토리지 전략 차이는? |

### Part 2 — 네트워킹 (Ch04)
Pod 간 통신 모델부터 외부 트래픽 수용까지 네트워크 계층을 한 챕터로 묶는다. 파일 번호 순서대로 읽으면 Linux 기반 → 노드 간 트래픽 → Service → DNS → Ingress 순으로 한 단씩 위로 올라간다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 04-01 | [네트워킹](./04-01.네트워킹.md) | 트래픽은 어떤 계층을 거쳐 흐르는가? |
| 04-02 | [Pod 네트워크와 Linux 기반](./04-02.Pod%20네트워크와%20Linux%20기반.md) | Pause·netns·veth·Pod CIDR·CNI·kube-proxy dataplane은 실제 어떻게 동작하는가? ([인터랙티브 시각화](./04-02-pod-network.html)) |
| 04-03 | [오버레이와 노드 간 트래픽](./04-03.오버레이와%20노드%20간%20트래픽.md) | VXLAN·네이티브 라우팅·BGP·ECMP·MetalLB는 노드 간 Pod 트래픽과 외부 LoadBalancer를 어떻게 만드는가? ([인터랙티브 시각화](./04-03-overlay-bgp.html)) |
| 04-04 | [Service와 EndpointSlice](./04-04.Service와%20EndpointSlice.md) | 변하는 Pod 집합을 어떻게 안정적인 진입점으로 노출하는가? |
| 04-05 | [DNS와 CoreDNS](./04-05.DNS와%20CoreDNS.md) | Service 이름은 어떻게 IP로 해석되는가? |
| 04-06 | [Ingress와 Gateway API](./04-06.Ingress와%20Gateway%20API.md) | 외부 트래픽 라우팅은 어떻게 진화하고, cert-manager는 어떻게 인증서를 자동화하는가? |

### Part 3 — 패키지 관리 (Ch05)
반복되는 매니페스트를 Helm 차트로 묶고 직접 차트를 개발한다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 05-01 | [Helm 기초](./05-01.Helm%20기초.md) | 왜 매니페스트 대신 Helm을 쓰는가? |
| 05-02 | [Helm 고급](./05-02.Helm%20고급.md) | 재사용 가능한 차트를 어떻게 설계하는가? |
| 05-03 | [Kustomize](./05-03.Kustomize.md) | Helm 없이 환경별 차이를 어떻게 선언적으로 관리하는가? |
| 05-04 | [K8s 환경변수와 Spring 설정 주입](./05-04.K8s%20환경변수와%20Spring%20설정%20주입.md) | ConfigMap 환경변수는 Spring YAML에 어떻게 적용되는가? |

### Part 4 — Operator 패턴과 DB·미들웨어 (Ch06)
CRD + Controller로 Day-2 운영을 자동화한다. 개념부터 DB(MySQL·PostgreSQL·Redis), 메시징(Kafka·Redpanda)까지 한 묶음이다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 06-01 | [Operator 패턴](./06-01.Operator%20패턴.md) | CRD와 컨트롤러는 어떻게 연동되는가? |
| 06-02 | [MySQL Operator](./06-02.MySQL%20Operator.md) | MySQL HA를 어떻게 자동화하는가? |
| 06-03 | [PostgreSQL Operator](./06-03.PostgreSQL%20Operator.md) | CloudNativePG의 복제·백업 전략은? |
| 06-04 | [Redis Operator](./06-04.Redis%20Operator.md) | Cluster와 Sentinel은 언제 갈라지는가? |
| 06-05 | [Kafka Operator](./06-05.Kafka%20Operator.md) | Strimzi로 Kafka를 선언적으로 관리하는 법은? |
| 06-06 | [Redpanda Operator](./06-06.Redpanda%20Operator.md) | Strimzi와 Redpanda Operator는 뭐가 다른가? |

### Part 5 — DevTools와 GitOps (Ch07)
Jenkins·SonarQube·ArgoCD를 하나의 흐름으로 묶어 개발 생산성과 배포 자동화를 얻는 단계다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 07-01 | [Jenkins on K8s](./07-01.Jenkins%20on%20K8s.md) | K8s 네이티브 Jenkins는 뭐가 달라지는가? |
| 07-02 | [SonarQube on K8s](./07-02.SonarQube%20on%20K8s.md) | SonarQube 영속성 전략은? |
| 07-03 | [ArgoCD와 GitOps](./07-03.ArgoCD와%20GitOps.md) | Git을 단일 진실 공급원으로 삼는 배포는? |
| 07-04 | [Harbor](./07-04.Harbor.md) | 이미지와 OCI Helm chart를 어디서 통합 관리하는가? |

### Part 6 — 운영 심화 (Ch08)
클러스터 유지보수와 인증, 조회 자동화, 시험 대비를 별도 묶음으로 분리한다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 08-01 | [클러스터 업그레이드와 ETCD 백업·복구](./08-01.클러스터%20업그레이드와%20ETCD%20백업·복구.md) | kubeadm 업그레이드와 etcd 재해 복구는 어떤 절차로 다루는가? |
| 08-02 | [TLS와 API 접근 보안](./08-02.TLS와%20API%20접근%20보안.md) | 컨트롤 플레인 PKI(API 서버·etcd·kubelet)는 어떻게 연결되는가? |
| 08-03 | [JSONPath와 kubectl 고급 조회](./08-03.JSONPath와%20kubectl%20고급%20조회.md) | 반복 조회와 스크립팅에 필요한 출력 제어는 어떻게 하는가? |
| 08-04 | [CKA 대비와 문제 풀이 전략](./08-04.CKA%20대비와%20문제%20풀이%20전략.md) | 시험 범위를 실무 문서와 어떻게 연결해 준비하는가? |

### Part 7 — 스케줄링과 배치 (Ch09)
어디에 둘지(Affinity·Taint), 동시 중단을 얼마나 허용할지(PDB·PriorityClass), 그리고 일회성·주기성·노드별 워크로드를 한 묶음으로 본다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 09-01 | [스케줄링과 노드 선택](./09-01.스케줄링과%20노드%20선택.md) | kube-scheduler의 Filter·Score와 nodeAffinity·Taint는 어떻게 보완되는가? |
| 09-02 | [토폴로지 분산과 중단 정책](./09-02.토폴로지%20분산과%20중단%20정책.md) | Topology Spread·PodDisruptionBudget·PriorityClass·Eviction은 가용성을 어떻게 만드는가? |
| 09-03 | [배치 워크로드](./09-03.배치%20워크로드.md) | Job·CronJob·DaemonSet·InitContainer·Sidecar는 각각 어떤 의도를 표현하는가? |

### Part 8 — 운영·관측·보안 (Ch10)
안정적으로 운영하기 위한 관측성, 보안, 자원 관리, 스케일링을 한 묶음으로 읽는다. 자원 관리(10-03)가 오토스케일링(10-04)의 입력이 되는 인과 순서로 정렬했다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 10-01 | [모니터링과 트러블슈팅](./10-01.모니터링과%20트러블슈팅.md) | 클러스터 장애를 어떻게 체계적으로 진단하는가? |
| 10-02 | [RBAC과 보안](./10-02.RBAC과%20보안.md) | RBAC·ServiceAccount 토큰·Admission(Webhook/VAP)·NetworkPolicy를 어떻게 묶는가? |
| 10-03 | [자원 관리](./10-03.자원%20관리.md) | Requests/Limits와 QoS로 안정성을 어떻게 확보하는가? |
| 10-04 | [오토스케일링](./10-04.오토스케일링.md) | HPA·VPA·KEDA는 어떻게 역할을 나누는가? |
| 10-05 | [OOMKilled 사례 분석](./10-05.OOMKilled%20사례%20분석.md) | 6GB Pod가 반복 OOMKilled — JVM heap과 cgroup이 보는 메모리는 왜 어긋나는가? (Endowus 사례) |



## 심화 탐구 (deepdive/)
> 각 장에는 같은 번호 체계를 따르는 점검 문서가 짝을 이룬다.

각 장에는 `deepdive/{장}-{절}.{제목} 점검.md` 형식의 심화 문서가 짝을 이룬다. 본 카테고리의 원본 INVESTIGATE는 점검 질문 위주였기 때문에 현재 k8s deepdive는 전부 `점검.md`다. hands-on 실습이 필요한 경우 각 LEARN의 `실습 환경` 서술과 deepdive 상단 `실습 환경` 섹션을 조합해 GCP K8s 클러스터 위에서 수행한다.



## 실습 환경
> 개인 GCP K8s 클러스터를 기준으로 하되, 본문은 가능한 한 범용 명령으로 유지한다.

현재 기준 실습은 개인 GCP K8s 클러스터(dev-server 1~3, asia-northeast3-a, kubeadm v1.31.14)에서 수행한다. 환경이 바뀌어도 본문이 유지되도록 각 심화 문서 상단 `## 실습 환경` 섹션에만 환경 특화 명령을 두고, 본문은 `kubectl`·Helm 범용 명령으로 쓴다. 환경 상세는 [`gcp` 스킬 문서](../../../../.claude/skills/gcp/SKILL.md)에서 관리한다.



## 관련 문서
> service-mesh와 devops 카테고리로 이어지는 선후 관계를 함께 본다.

- [service-mesh MOC](../service-mesh/README.md) — 본 카테고리의 다음 단계. Pod 간 트래픽 제어·mTLS·관측성을 메시 계층에서 해결한다
- [argocd MOC](../argocd/README.md) — ArgoCD 상세 시리즈. AppProject, App of Apps, ApplicationSet, Image Updater 운영을 별도로 다룬다
- [devops MOC](../../08_devops/README.md) — CI/CD 파이프라인 자체 설계는 이곳
