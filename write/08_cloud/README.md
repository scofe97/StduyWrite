---
title: 08_cloud MOC
tags: [moc, cloud, kubernetes, argocd, service-mesh]
status: final
related:
  - ./kubernetes/README.md
  - ./argocd/README.md
  - ./service-mesh/README.md
updated: 2026-05-23
---

# 08_cloud
---
> 인프라 추상화와 오케스트레이션 관점의 지식 저장소. Kubernetes, Service Mesh, Helm, GitOps 같은 "클러스터 내부 구조"를 다룬다. 여기에 더해, 그 클러스터가 딛고 선 아래층인 IaaS(오픈스택)까지 조망 범위에 둔다.

## 구성

| 서브카테고리 | 범위 | 문서 |
|--------------|------|------|
| [kubernetes/](./kubernetes/README.md) | 로컬 클러스터 운영, Helm·Operator, DB/DevTools 운영, RBAC, 오토스케일링 | 20개 장 |
| [argocd/](./argocd/README.md) | GitOps, Application, AppProject, App of Apps, ApplicationSet, Image Updater, 운영 심화 | 14개 장 |
| [service-mesh/](./service-mesh/README.md) | Linkerd·Istio·Cilium, 사이드카/앰비언트, mTLS, 멀티클러스터 | 26개 장 |
| [openstack/](./openstack/README.md) | IaaS 개요, AWS 서비스 대응, 오픈스택↔Kubernetes 층 관계(CMP 바닥 인프라) | 1개 장 |

## 예정 주제 — Spring Cloud 스택 (TBD)

> 옛 `spring/` 서브폴더 placeholder를 본 README로 흡수 (2026-05-23). 작성 분량이 커지면 그 시점에 별도 `spring/` 서브폴더 신설.

- Spring Cloud Gateway — 라우팅·필터·Circuit Breaker 통합
- Spring Cloud Config — 중앙 설정 저장소
- Spring Cloud Stream (Kafka·RabbitMQ 추상화) — 단, 메시징 도메인 측면은 [`../04_messaging/`](../04_messaging/) 확인
- K8s 친화적 설정 — `application-k8s.yml`, probes, graceful shutdown

경계: K8s 매니페스트·Helm 차트 설계는 [`kubernetes/`](./kubernetes/README.md). Service Mesh 개념도 [`service-mesh/`](./service-mesh/README.md). *Spring 애플리케이션이 이들 위에서 돌 때 필요한 Spring 스택*만 위의 예정 주제 범위.

## 경계 기준

CI/CD 파이프라인 작성 자체는 [`07_devops/`](../07_devops/)로 간다. 반대로 K8s 매니페스트 설계, 네트워크 정책, 서비스 메시 사이드카처럼 "클러스터 내부에서 어떻게 돌아가는가"는 여기다. GitOps 도구 중에서도 ArgoCD는 문서 양과 운영 주제가 커져 별도 `argocd/` 서브카테고리로 분리했다. 메시징 미들웨어(Kafka, Redpanda) 자체는 [`04_messaging/`](../04_messaging/)에 있고, 그것을 K8s 위에 올리는 Operator 패턴 관점은 `kubernetes/03-09` `06-06`에서 다룬다.

층으로 보면 [`openstack/`](./openstack/README.md)(IaaS)이 인프라를 *만드는* 아래층이고, `kubernetes/`·`service-mesh/`는 그 위에서 컨테이너를 *굴리는* 층이다. 오픈스택은 회사 CMP·컨테이너가 딛고 선 바닥이라, 서비스 내부 딥다이브가 아니라 개발자가 바닥을 조망하는 개요 범위로 둔다.

## 이관 연혁

과거 `03_Cloud Native/` 아래 Kafka·Redpanda 문서는 내용상 메시징이라 `04_messaging/`로 이관됐다. 2026-04-19에 `poc/03_CloudNative/02-kubernetes`와 `03-service-mesh` 총 92개 학습 문서를 세컨드 브레인 하네스 기준으로 경량 손질하여 각 서브카테고리로 편입했다.
