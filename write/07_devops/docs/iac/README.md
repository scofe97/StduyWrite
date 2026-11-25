---
title: 07_devops/docs/iac — IaC 와 쿠버네티스 매니페스트 관리
tags: [moc, iac, helm, kustomize, official-docs]
status: final
related:
  - ../../README.md
  - ../../../_archive/08_cloud/kubernetes/README.md
updated: 2026-11-25
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

Terraform 처럼 클라우드 자원(VPC·로드밸런서·DB)을 만드는 도구를 IaC 의 대표로 보는 쪽에서는 Helm·Kustomize 를 구성 관리 도구로 따로 부르기도 합니다. 이 폴더는 둘을 "선언을 코드로 두고 같은 결과를 재현한다"는 같은 원칙으로 묶습니다. 클라우드 자원 쪽 노트가 생기면 이 폴더에 도구 이름으로 편을 더합니다.



## 문서 목록

> 편 이름이 도구입니다. Helm 주제별 일곱 편으로 템플릿·values 를 잡은 뒤 Kustomize 를 읽으면 두 길의 차이가 잘 보입니다.

| 문서 | 1차 자료 | 한 줄 소개 |
|------|----------|-----------|
| [Helm 릴리스 운영](Helm%20%EB%A6%B4%EB%A6%AC%EC%8A%A4%20%EC%9A%B4%EC%98%81.md) | <https://helm.sh/docs/> | Helm 릴리스와 리비전이 클러스터에 남는 모양을 이해하고, 배포가 막히거나 충돌할 때 원인을 찾아 풀 수 있습니다. |
| [Helm values와 렌더 검증](Helm%20values%EC%99%80%20%EB%A0%8C%EB%8D%94%20%EA%B2%80%EC%A6%9D.md) | <https://helm.sh/docs/chart_template_guide/values_files/> | 차트에 값을 넣는 규칙을 알아야 최종 값을 예측할 수 있고, 예측한 값을 배포 전에 렌더로 확인할 수 있습니다. |
| [Helm 차트 작성](Helm%20%EC%B0%A8%ED%8A%B8%20%EC%9E%91%EC%84%B1.md) | <https://helm.sh/docs/chart_template_guide/> | 차트 폴더 구성부터 템플릿 언어, 헬퍼 재사용, ConfigMap 변경에 따른 파드 롤링, 변경 검증 순서까지 다룹니다. |
| [Helm 템플릿 값 검증](Helm%20%ED%85%9C%ED%94%8C%EB%A6%BF%20%EA%B0%92%20%EA%B2%80%EC%A6%9D.md) | <https://helm.sh/docs/howto/charts_tips_and_tricks/> | 잘못된 값을 렌더 단계에서 막는 `required`·`fail`, 헬퍼에 값을 여럿 넘기는 `dict`, 차트 파일을 읽는 `.Files` 의 동작과 함정을 다룹니다. |
| [Helm 렌더 테스트](Helm%20%EB%A0%8C%EB%8D%94%20%ED%85%8C%EC%8A%A4%ED%8A%B8.md) | <https://helm.sh/docs/helm/helm_template/> | 클러스터 없이 `helm template` 출력을 단언해 의도치 않은 매니페스트 변경을 막고, `helm lint`·`helm-unittest` 의 역할을 비교합니다. |
| [Helm Hook](Helm%20Hook.md) | <https://helm.sh/docs/topics/charts_hooks/> | 배포 작업의 순서 의존성을 Helm Hook 으로 제어하고 장애 상황에서 안전하게 복구하는 역량을 갖춥니다. |
| [Helm 차트 의존성과 저장소](Helm%20%EC%B0%A8%ED%8A%B8%20%EC%9D%98%EC%A1%B4%EC%84%B1%EA%B3%BC%20%EC%A0%80%EC%9E%A5%EC%86%8C.md) | <https://helm.sh/docs/topics/charts/> | 원격 저장소 관리와 폐쇄망 차트 반입, OCI 배포 및 서브차트 의존성 제어 전 과정을 다룹니다. |
| [Kustomize](Kustomize.md) | <https://kubectl.docs.kubernetes.io/references/kustomize/> | Helm 없이 환경별 차이를 patch 로 선언적으로 관리하는 길을 봅니다. |

각 본문 끝의 `면접 질문` 과 `정답` 절로 스스로 점검합니다.



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [07_devops MOC](../../README.md) — 대분류 지도와 로드맵 단계별 문서 수
- [Blue/Green 무중단 전환과 아키텍처 결정 기록](../../book/aic_ai-infra-claude/05-02.Blue-Green%20%EB%AC%B4%EC%A4%91%EB%8B%A8%20%EC%A0%84%ED%99%98%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B2%B0%EC%A0%95%20%EA%B8%B0%EB%A1%9D.md) · [점진적 배포 Canary와 claude-context](../../book/aic_ai-infra-claude/06-02.%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%20Canary%EC%99%80%20claude-context.md) — 여기서 만든 매니페스트를 클러스터에 어떤 순서와 비율로 내보낼지
- [Application 관리하기](../../book/argocd-up-and-running/04-01.Application%20%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EC%86%8C%EC%8A%A4%C2%B7%EB%8C%80%EC%83%81%C2%B7Helm%C2%B7Kustomize%20%EC%99%80%20%EC%82%AD%EC%A0%9C%C2%B7finalizer.md) — Argo CD 가 Helm·Kustomize 소스를 렌더하는 방식
- [kubernetes MOC](../../../_archive/08_cloud/kubernetes/README.md) — 전체 대주제 지도
