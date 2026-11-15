---
title: 08_cloud MOC
tags: [moc, cloud, kubernetes, argocd, service-mesh]
status: final
related:
  - ./kubernetes/README.md
  - ./docs/README.md
  - ./book/networking-and-kubernetes/README.md
  - ./book/container-security/README.md
  - ./book/learning-coredns/README.md
  - ./book/argocd-up-and-running/README.md
  - ./book/cilium-up-and-running/README.md
  - ./book/cks-study-guide/README.md
  - ./book/production-kubernetes/README.md
updated: 2026-11-14
---

# 08_cloud

> 인프라 추상화와 오케스트레이션 관점에서 Kubernetes, Service Mesh, Helm, GitOps 등 클러스터 내부 구조와 IaaS(오픈스택)를 다룹니다.



## 경계 기준

Kubernetes 를 어떤 순서로 읽을지는 [k8s-keywords.md](k8s-keywords.md) 가 정합니다. 네트워크 데이터패스는 [`network-keywords.md`](../02_os/network-keywords.md) 가 따로 다룹니다.

CI/CD 파이프라인 작성 자체는 [`07_devops/`](../07_devops/)로 갑니다. 반대로 K8s 매니페스트 설계, 네트워크 정책, 서비스 메시 사이드카처럼 "클러스터 내부에서 어떻게 돌아가는가"는 여기서 다룹니다.

GitOps 도구 중에서도 ArgoCD는 문서 양과 운영 주제가 커서 [`book/argocd-up-and-running/`](./book/argocd-up-and-running/README.md)에서 따로 다룹니다. 메시징 미들웨어(Kafka, Redpanda) 자체는 [`04_messaging/`](../04_messaging/)에 있고, 그것을 K8s 위에 올리는 Operator 패턴 관점은 [`book/kubernetes-patterns/28-01.Operator`](./book/kubernetes-patterns/28-01.Operator%20%E2%80%94%20CRD%EB%A1%9C%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%A7%80%EC%8B%9D%EC%9D%84%20%EC%9E%90%EB%8F%99%ED%99%94%ED%95%98%EA%B8%B0.md)에서 다룹니다.

층으로 보면 `openstack/` <!-- 링크 끊김(2026-08): ./openstack/README.md -->(IaaS)이 인프라를 만드는 아래층이고, `kubernetes/`·`service-mesh/`는 그 위에서 컨테이너를 굴리는 층입니다. 오픈스택은 컨테이너가 딛고 선 바닥이라, 서비스 내부 딥다이브가 아니라 개발자가 바닥을 조망하는 개요 범위로 둡니다.



## 키워드

### k8s-keywords.md

키워드 파일: [k8s-keywords.md](k8s-keywords.md)

| 묶음 | 다룬 문서 | 빈 필수 키워드 |
|---|---|---|
| 1단계 · 오브젝트 | 26편 | kubectl 기본 조회 |
| 2단계 · 워크로드 | 24편 | — |
| 3단계 · 연결 | 12편 | — |
| 4단계 · 자원과 저장 | 14편 | — |
| 5단계 · 내부 구조 | 6편 | 조정 루프 · watch · informer · client-go · List·Watch 와 resourceVersion · 410 Gone · level-driven 과 edge-driven 의 차이 |
| 6단계 · 보안과 확장 | 23편 | — |
| 7단계 · 운영 | 7편 | 노드 추가·제거 — cordon · drain · PDB 와의 맞물림 |



## 하위 폴더·문서 목록

| 서브카테고리 | 범위 | 문서 |
|--------------|------|------|
| [kubernetes/](./kubernetes/README.md) | 데브툴스 운영(Jenkins·SonarQube·ArgoCD·Harbor) | 11_devtools (4편) |
| [docs/](./docs/README.md) | 공식 문서·제품 사이트 정독 — 제품(kubernetes·cncf-certification·helm·kustomize·argo-rollouts)마다 폴더를 두고 궁금한 주제만 한 편씩 | 16편 |
| [book/networking-and-kubernetes/](./book/networking-and-kubernetes/README.md) | 《Networking and Kubernetes》 정독 — OSI/TCP-IP, Linux 네트워킹, 컨테이너·K8s 네트워킹, Service 추상화, AWS/GCP/Azure | 정독 노트 27편 + 용어집·결정 치트시트 |
| [book/container-security/](./book/container-security/README.md) | 《Container Security》(Liz Rice, 1판) 정독 — 위협 모델, syscall·capability·cgroup·namespace가 세우는 격리 경계, 이미지·공급망 보안, 취약점 스캐닝, 샌드박싱과 격리 파괴 | 정독 노트 17편 (본문 14/14 + 부록 완독) |
| [book/learning-coredns/](./book/learning-coredns/README.md) | 《Learning CoreDNS》(Belamaric·Liu) 정독 — 컨테이너 환경의 서비스 디스커버리를 떠받치는 DNS 서버 편. Corefile·플러그인 체인, 존 데이터, 쿠버네티스 연동, 완전 재귀를 포기한 교환 | 정독 노트 1편 / 9장 |
| [book/argocd-up-and-running/](./book/argocd-up-and-running/README.md) | 《Argo CD: Up and Running》(Block·Hernandez) 정독 — 클러스터 위에 놓이는 GitOps·CD 계층. 설치와 Application·동기화, 인증과 멀티테넌시, 보안, 대규모 배포, 확장, CI 연동, 운영 | 정독 노트 16편 / 14장 |
| [book/cilium-up-and-running/](./book/cilium-up-and-running/README.md) | 《Cilium: Up and Running》(Vibert·Nikolic·Laverack) 정독 — eBPF 데이터패스로 CNI·서비스 부하 분산·정책·관측을 맡는 Cilium 의 설계와 구성 요소 | 정독 노트 24편 / 16장 |
| [book/cks-study-guide/](./book/cks-study-guide/README.md) | 《Certified Kubernetes Security Specialist (CKS) Study Guide》(Muschko, 1판) 정독 — CKS 시험 여섯 도메인 순서로 클러스터 설정·API 접근·호스트·Pod·공급망·런타임 하드닝 절차를 다룸 | 정독 노트 10편 / 7장 |
| [book/production-kubernetes/](./book/production-kubernetes/README.md) | 《Production Kubernetes》(Rosso 외) 정독 — 클러스터 배포 모델, etcd 토폴로지, 머신 부트스트랩, 무중단 업그레이드 등 프로덕션 플랫폼 구축과 운영 라이프사이클 | 정독 노트 1편 / 16장 |
