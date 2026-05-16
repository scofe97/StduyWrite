---
title: 09_cloud MOC
tags: [moc, cloud, kubernetes, argocd, service-mesh]
status: final
related:
  - ./kubernetes/README.md
  - ./argocd/README.md
  - ./service-mesh/README.md
  - ./spring/README.md
updated: 2026-04-22
---

# 09_cloud
---
> 인프라 추상화와 오케스트레이션 관점의 지식 저장소. Kubernetes, Service Mesh, Helm, GitOps 같은 "클러스터 내부 구조"를 다룬다.

## 구성

| 서브카테고리 | 범위 | 문서 |
|--------------|------|------|
| [kubernetes/](./kubernetes/README.md) | 로컬 클러스터 운영, Helm·Operator, DB/DevTools 운영, RBAC, 오토스케일링 | 20개 장 |
| [argocd/](./argocd/README.md) | GitOps, Application, AppProject, App of Apps, ApplicationSet, Image Updater, 운영 심화 | 14개 장 |
| [service-mesh/](./service-mesh/README.md) | Linkerd·Istio·Cilium, 사이드카/앰비언트, mTLS, 멀티클러스터 | 26개 장 |
| [spring/](./spring/README.md) | K8s 위에서 도는 Spring 스택 (Cloud Gateway, Config) | 준비 중 |

## 경계 기준

CI/CD 파이프라인 작성 자체는 [`08_devops/`](../08_devops/)로 간다. 반대로 K8s 매니페스트 설계, 네트워크 정책, 서비스 메시 사이드카처럼 "클러스터 내부에서 어떻게 돌아가는가"는 여기다. GitOps 도구 중에서도 ArgoCD는 문서 양과 운영 주제가 커져 별도 `argocd/` 서브카테고리로 분리했다. 메시징 미들웨어(Kafka, Redpanda) 자체는 [`05_messaging/`](../05_messaging/)에 있고, 그것을 K8s 위에 올리는 Operator 패턴 관점은 `kubernetes/06-05` `06-06`에서 다룬다.

## 이관 연혁

과거 `03_Cloud Native/` 아래 Kafka·Redpanda 문서는 내용상 메시징이라 `05_messaging/`로 이관됐다. 2026-04-19에 `poc/03_CloudNative/02-kubernetes`와 `03-service-mesh` 총 92개 학습 문서를 세컨드 브레인 하네스 기준으로 경량 손질하여 각 서브카테고리로 편입했다.
