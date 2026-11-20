---
title: 07_devops/docs/iac — IaC 와 쿠버네티스 매니페스트 관리
tags: [moc, iac, helm, kustomize, official-docs]
status: final
related:
  - ../../README.md
  - ../deployment/README.md
  - ../../../08_cloud/kubernetes/README.md
updated: 2026-11-15
---

# 07_devops/docs/iac — IaC 와 쿠버네티스 매니페스트 관리

---

> 인프라와 배포 설정을 코드로 적어 Git 에 두는 방식(IaC, Infrastructure as Code)을 모으는 자리입니다. 지금은 쿠버네티스 매니페스트를 코드로 다루는 두 도구, Helm 과 Kustomize 를 다룹니다.

## 왜 한 폴더로 묶는가

> Helm 과 Kustomize 는 같은 문제를 다른 방법으로 풉니다. 따로 두면 둘을 비교할 자리가 없습니다.

손으로 `kubectl apply` 를 치거나 YAML 을 환경마다 복사해 고치면 무엇이 언제 바뀌었는지 남지 않고, 개발·운영 환경이 조금씩 어긋납니다. IaC 는 원하는 상태를 파일로 선언하고 Git 으로 검토·이력·재현을 맡기는 방식입니다. 같은 파일로 몇 번을 적용해도 같은 결과가 나와야 합니다.

쿠버네티스에서는 매니페스트(Deployment·Service 같은 리소스를 적은 YAML)가 그 선언입니다. 환경마다 이미지 태그·복제 수·도메인이 달라질 때 두 도구가 다르게 답합니다.

| 도구 | 환경 차이를 다루는 방법 | 결과물 |
|------|------------------------|--------|
| Helm | 템플릿에 빈칸을 두고 `values.yaml` 로 채운다 | 차트(버전이 붙은 패키지)와 릴리스 이력 |
| Kustomize | 공통 base 를 두고 환경별 overlay 에서 patch 로 덮는다 | 템플릿 없는 평범한 YAML |

Terraform 처럼 클라우드 자원(VPC·로드밸런서·DB)을 만드는 도구를 IaC 의 대표로 보는 쪽에서는 Helm·Kustomize 를 구성 관리 도구로 따로 부르기도 합니다. 이 폴더는 둘을 "선언을 코드로 두고 같은 결과를 재현한다"는 같은 원칙으로 묶습니다. 클라우드 자원 쪽 노트가 생기면 이 폴더에 장 번호를 새로 열어 더합니다.



## 문서 목록

> 장 번호가 도구입니다. 01장 Helm 에서 템플릿·values 를 잡은 뒤 02장 Kustomize 를 읽으면 두 길의 차이가 잘 보입니다.

| 번호 | 제목 | 1차 자료 | 한 줄 소개 |
|------|------|----------|-----------|
| 01-01 | [Helm 기초](01-01.Helm%20%EA%B8%B0%EC%B4%88.md) | <https://helm.sh/docs/> | 왜 생짜 매니페스트 대신 Helm 을 쓰는지, 템플릿·values 의 기본을 잡습니다. |
| 01-02 | [Helm 고급](01-02.Helm%20%EA%B3%A0%EA%B8%89.md) | <https://helm.sh/docs/chart_template_guide/> | 재사용 가능한 차트를 어떻게 설계하는지 봅니다. |
| 02-01 | [Kustomize](02-01.Kustomize.md) | <https://kubectl.docs.kubernetes.io/references/kustomize/> | Helm 없이 환경별 차이를 patch 로 선언적으로 관리하는 길을 봅니다. |

각 본문 끝의 `점검 질문` 절에서 개념 설명과 심화 Q&A 를 한 문서로 이어 읽습니다.



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [07_devops MOC](../../README.md) — 대분류 지도와 로드맵 단계별 문서 수
- [deployment/](../deployment/README.md) — 여기서 만든 매니페스트를 클러스터에 어떤 순서와 비율로 내보낼지
- [Application 관리하기](../../../08_cloud/book/argocd-up-and-running/04-01.Application%20%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EC%86%8C%EC%8A%A4%C2%B7%EB%8C%80%EC%83%81%C2%B7Helm%C2%B7Kustomize%20%EC%99%80%20%EC%82%AD%EC%A0%9C%C2%B7finalizer.md) — Argo CD 가 Helm·Kustomize 소스를 렌더하는 방식
- [kubernetes MOC](../../../08_cloud/kubernetes/README.md) — 전체 대주제 지도
