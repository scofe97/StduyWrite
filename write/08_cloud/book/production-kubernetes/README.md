---
title: Production Kubernetes — 정독 인덱스
tags: [moc, study-index, book, kubernetes, k8s, production-kubernetes, platform-engineering]
status: draft
source:
  - 《Production Kubernetes: Building Successful Application Platforms》(Josh Rosso, Rich Lander, Alex Brand, John Harris, O'Reilly, 2021, ISBN 978-1492092308)
  - 장별 PDF 폴더 — GoogleDrive/내 드라이브/book/Production Kubernetes/ (16개 장)
related:
  - ../kubernetes-in-action/README.md
  - ../kubernetes-up-and-running/README.md
  - ../networking-and-kubernetes/README.md
  - ../cks-study-guide/README.md
  - ../../kubernetes/README.md
updated: 2026-11-09
---

# Production Kubernetes — 정독 인덱스

---

> 이 폴더는 『Production Kubernetes』(Josh Rosso 외, O'Reilly)를 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 프로덕션 플랫폼을 꾸릴 때의 결정을 장별로 정리합니다.

## 플랫폼 관점과 형제 정독본과의 차이

> 쿠버네티스를 소비하는 사용자를 넘어, 운영 플랫폼을 직접 조립하고 지탱하는 플랫폼 팀의 아키텍처 결정을 다룹니다.

『Production Kubernetes』는 단순한 오브젝트 사용법을 넘어 플랫폼 엔지니어링 팀의 설계 결정을 다룹니다. 클러스터 배포 모델부터 런타임, 스토리지, 네트워킹, 비밀 데이터 관리까지 운영 관점을 유지합니다. 나아가 어드미션 제어, 관측 가능성, 멀티테넌시, 공급망 보안, 플랫폼 추상화를 체계적으로 다룹니다.

형제 정독본과 다루는 층위가 다릅니다. [Kubernetes in Action](../kubernetes-in-action/README.md)은 개별 오브젝트를 입문자 관점에서 바닥부터 쌓습니다. [Kubernetes: Up and Running](../kubernetes-up-and-running/README.md)은 운영자의 최소 조작 경로에 집중합니다. [Networking and Kubernetes](../networking-and-kubernetes/README.md)는 패킷 수준의 네트워크 계층을 수직 심화합니다. [CKS Study Guide](../cks-study-guide/README.md)는 시험 실기 기준의 공격 표면 하드닝을 다룹니다. 반면 이 정독본은 **운영 플랫폼을 직접 꾸리는 쪽의 아키텍처 결정과 트레이드오프**를 중심에 둡니다.



## 목차 구성

> 원서 16개 장의 도입부와 본문에서 다루는 핵심 주제를 한국어로 정리한 목차입니다.

| 번호 | 장 제목(영문) | 한 줄 소개(한국어) |
|------|---------------|-------------------|
| 1 | A Path to Production | 프로덕션 환경에서 쿠버네티스 기반 플랫폼을 성공적으로 안착시키기 위한 핵심 설계 여정을 개관합니다. |
| 2 | Deployment Models | 관리형 서비스 활용과 자체 자동화 배포의 득실을 비교하고 클러스터 프로비저닝 모델을 선택합니다. |
| 3 | Container Runtime | Linux cgroup·네임스페이스와 CRI를 바탕으로 kubelet과 협력하는 컨테이너 런타임의 동작 방식을 다룹니다. |
| 4 | Container Storage | 데이터 영속성이 필요한 상태 저장 워크로드를 지원하기 위해 CSI 스토리지 플러그인 아키텍처를 분석합니다. |
| 5 | Pod Networking | 파드 간 고유 주소 할당과 라우팅을 구현하는 소프트웨어 정의 네트워크(SDN)와 CNI 구조를 살펴봅니다. |
| 6 | Service Routing | 동서(East-West) 서비스 통신과 남북(North-South) 외부 노출을 처리하는 Service·Ingress·메시 계층을 구성합니다. |
| 7 | Secret Management | 자격 증명과 암호화 키를 etcd 저장부터 런타임 주입·교체(rotation)까지 안전하게 다루는 정책을 세웁니다. |
| 8 | Admission Control | API 서버 인입 요청을 etcd 영속화 전에 가로채 정책을 강제하고 변이하는 어드미션 제어기를 구축합니다. |
| 9 | Observability | 플랫폼과 워크로드의 실행 상태를 파악하기 위해 로깅·메트릭·분산 추적 파이프라인을 체계화합니다. |
| 10 | Identity | 사용자와 워크로드의 신원을 안전하게 입증하기 위해 인증(Authentication) 체계와 OIDC 토큰을 연동합니다. |
| 11 | Building Platform Services | 사내 시스템 연동과 플랫폼 기능 확장을 위해 CRD와 Operator 패턴으로 커스텀 플랫폼 서비스를 만듭니다. |
| 12 | Multitenancy | 여러 팀과 워크로드가 클러스터 자원을 안전하게 공유하도록 소프트·하드 멀티테넌시 격리 경계를 설계합니다. |
| 13 | Autoscaling | 워크로드 부하 변동에 대응하여 HPA·VPA와 클러스터 오토스케일러로 컴퓨팅 자원을 자동 조절합니다. |
| 14 | Application Considerations | 플랫폼 위 애플리케이션이 프로브·정상 종료·수명주기를 준수하여 쿠버네티스에 맞게 동작하도록 조율합니다. |
| 15 | Software Supply Chain | 코드 작성부터 이미지 빌드·취약점 검사·서명·GitOps 배포까지 이어지는 소프트웨어 공급망을 구성합니다. |
| 16 | Platform Abstractions | 개발자에게 불필요한 인프라 복잡성을 숨기고 셀프서비스 진입로를 제공하는 플랫폼 추상화를 설계합니다. |



## 작성 현황

> 2장 노트가 있고 나머지 장은 예정입니다.

| 편 | 대상 장 | 상태 |
|----|---------|------|
| 01-01 (1장 A Path to Production) | A Path to Production | 예정 |
| [02-01](./02-01.Deployment%20Models%20%E2%80%94%20%EB%B0%B0%ED%8F%AC%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%9D%B8%ED%94%84%EB%9D%BC%20%EA%B5%AC%EC%B6%95.md) | Deployment Models | 완료 · 정독 |
| 03-01 (3장 Container Runtime) | Container Runtime | 예정 |
| 04-01 (4장 Container Storage) | Container Storage | 예정 |
| 05-01 (5장 Pod Networking) | Pod Networking | 예정 |
| 06-01 (6장 Service Routing) | Service Routing | 예정 |
| 07-01 (7장 Secret Management) | Secret Management | 예정 |
| 08-01 (8장 Admission Control) | Admission Control | 예정 |
| 09-01 (9장 Observability) | Observability | 예정 |
| 10-01 (10장 Identity) | Identity | 예정 |
| 11-01 (11장 Building Platform Services) | Building Platform Services | 예정 |
| 12-01 (12장 Multitenancy) | Multitenancy | 예정 |
| 13-01 (13장 Autoscaling) | Autoscaling | 예정 |
| 14-01 (14장 Application Considerations) | Application Considerations | 예정 |
| 15-01 (15장 Software Supply Chain) | Software Supply Chain | 예정 |
| 16-01 (16장 Platform Abstractions) | Platform Abstractions | 예정 |



## 번호 체계

> 파일명은 NN-MM.제목.md 형식을 따르며, 두 자리 장 번호와 장 내 편 순번을 조합합니다.

파일명은 `NN-MM.제목.md` 형식을 씁니다. 앞의 두 자리 숫자 `NN`은 원서의 장 번호이고, 뒤의 두 자리 숫자 `MM`은 한 장 안에서 주제가 길어질 때 나눈 편 순번입니다. 한 장의 내용이 길어져 800줄을 넘길 것으로 판단되면 `02-01`, `02-02`처럼 편 번호를 나누어 독립된 호흡으로 정리합니다.



## 형제 정독본과의 관계

> 겹치는 개념은 각 분야의 정본 문서로 위임하고, 이 정독본에는 플랫폼 설계와 운영 결정만 남깁니다.

- **Kubernetes in Action(KIA)**: 기본 오브젝트 명세와 kubeconfig 파일 자체의 구조·생성은 [KIA 03-01](../kubernetes-in-action/03-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0.md)이 정본입니다. 본 정독본은 인프라와 결합된 클러스터 배포 모델과 플랫폼 구성을 다룹니다.
- **Kubernetes: Up and Running(KUAR)**: 운영자의 최소 조작 경로와 앱 수명주기 관리는 [KUAR](../kubernetes-up-and-running/README.md)이 정본입니다. 본 정독본은 관리형 서비스 활용과 자체 자동화 배포의 구축 판단을 다룹니다.
- **Networking and Kubernetes(N&K)**: Linux 커널 네트워크 스택과 패킷 캡슐화 원리는 [N&K](../networking-and-kubernetes/README.md)가 정본입니다. 본 정독본은 CNI 플러그인 선정과 SDN 토폴로지 설계 등 플랫폼 아키텍처 관점을 다룹니다.
- **CKS Study Guide(CKS)**: CKS 시험 실기 기준의 공격 표면 하드닝 절차는 [CKS](../cks-study-guide/README.md)가 정본입니다. 본 정독본은 조직 단위의 멀티테넌시 격리와 공급망 보안 설계를 다룹니다.



## 관련 문서

> 같은 book/ 영역의 형제 정독본과 참조 인덱스 문서입니다.

- [Kubernetes in Action 정독 인덱스](../kubernetes-in-action/README.md) — 오브젝트를 바닥부터 쌓는 입문·레퍼런스 정독본
- [Kubernetes: Up and Running 정독 인덱스](../kubernetes-up-and-running/README.md) — 운영자의 최소 조작 경로를 다루는 실전서
- [Networking and Kubernetes 정독 인덱스](../networking-and-kubernetes/README.md) — 네트워크 계층 수직 심화 정독본
- [CKS Study Guide 정독 인덱스](../cks-study-guide/README.md) — 클러스터 보안 하드닝 실기 정독본
- [08_cloud/kubernetes 개념 노트 인덱스](../../kubernetes/README.md) — 쿠버네티스 개념 축 통합 인덱스
