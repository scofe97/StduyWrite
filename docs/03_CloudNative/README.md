# CloudNative 학습 문서

컨테이너, 오케스트레이션, GitOps, Service Mesh를 다루는 클라우드 네이티브 기술 학습 자료입니다.

---

## 학습 경로

```
Docker (기초) → Kubernetes (오케스트레이션) → ArgoCD (배포) → Service Mesh (네트워킹)
```

| 순서 | 주제 | 선행 지식 |
|------|------|----------|
| 1 | Docker | Linux 기초 |
| 2 | Kubernetes | Docker 컨테이너 |
| 3 | ArgoCD | Kubernetes, Git |
| 4 | Linkerd / Service Mesh | Kubernetes 네트워킹 |

---

## 폴더 구조

```
CloudNative/
├── README.md
├── 01_Docker/           # 컨테이너 기초 (17개 문서)
├── 02_Kubernetes/       # CKA 시험 대비 (23개 문서)
├── 03_ArgoCD/           # GitOps & CI/CD (14개 문서)
└── 04_Linkerd/          # Service Mesh (8개 문서)
```

**총 문서 수**: 62개

---

## 섹션별 내용

### 01_Docker (17개 문서)

컨테이너 기술의 기초부터 실무 활용까지 다룹니다.

| 문서 | 주요 내용 |
|------|----------|
| 01~05 | 컨테이너 개요, Docker 설치, 아키텍처 |
| 06~08 | 이미지, 컨테이너 관리, 앱 컨테이너화 |
| 09~11 | Compose, AI/Wasm 통합 |
| 12~14 | Swarm, 네트워킹 |
| 15~17 | 볼륨, 보안, 다음 단계 |

**출처**: Docker Deep Dive

---

### 02_Kubernetes (23개 문서)

CKA(Certified Kubernetes Administrator) 시험 준비를 위한 핵심 개념입니다.

| 문서 | 주요 내용 |
|------|----------|
| 01~03 | 시험 정보, K8s 개요, 클러스터 상호작용 |
| 04~08 | 설치, etcd 백업, 인증/인가, CRD, Helm |
| 09~13 | Pod, ConfigMap, Deployment, Scaling, 리소스 관리 |
| 14~16 | 스케줄링, 볼륨, PV |
| 17~20 | 서비스, Ingress, Gateway API, 네트워크 정책 |
| 21~22 | 트러블슈팅 (앱/클러스터) |
| Appendix | 연습 문제 정답 |

**출처**: CKA Study Guide

---

### 03_ArgoCD (14개 문서)

GitOps 기반 지속적 배포를 위한 ArgoCD 활용법입니다.

| 문서 | 주요 내용 |
|------|----------|
| 01~03 | 소개, 설치, 상호작용 |
| 04~06 | 애플리케이션 관리, 동기화, 인증/인가 |
| 07~09 | 클러스터 관리, 멀티테넌시, 보안 |
| 10~14 | 대규모 운영, 확장, CI 통합, 운영화, 향후 고려사항 |

**출처**: Argo CD Up and Running (O'Reilly)

---

### 04_Linkerd (8개 문서)

경량 Service Mesh 솔루션 Linkerd의 핵심 기능입니다.

| 문서 | 주요 내용 |
|------|----------|
| 01~02 | Service Mesh 개념, Linkerd 소개 |
| 03~04 | 배포, 워크로드 추가 |
| 05~06 | Ingress 통합, CLI |
| 07~08 | mTLS/인증서, 정책 관리 |

**출처**: Linkerd Up and Running (O'Reilly)

> **실습**: [poc/03_CloudNative/03-service-mesh/](../../poc/03_CloudNative/03-service-mesh/) 참조 — Linkerd + Istio + Cilium 비교, Ambient Mesh, Gateway API 등 2026년 기준 20챕터 학습 프로젝트

---

## 관련 학습 자료

| 주제 | 경로 |
|------|------|
| CI/CD 패턴 | `../CICD Pattern/` |
| Observability | `../Observability/` |
| DevOps 기초 | `../Fundamentals of DevOps and Software Delivery/` |

---

## 참고 링크

- [Docker 공식 문서](https://docs.docker.com/)
- [Kubernetes 공식 문서](https://kubernetes.io/docs/)
- [ArgoCD 공식 문서](https://argo-cd.readthedocs.io/)
- [Linkerd 공식 문서](https://linkerd.io/docs/)
- [Istio 공식 문서](https://istio.io/latest/docs/)
- [Cilium 공식 문서](https://docs.cilium.io/)
- [Gateway API](https://gateway-api.sigs.k8s.io/)
