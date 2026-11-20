---
title: 07_devops/docs/deployment — 배포 전략과 점진 배포
tags: [moc, deployment, progressive-delivery, argo-rollouts, argocd, gitops, official-docs]
status: final
related:
  - ../../README.md
  - ../iac/README.md
  - ../../book/argocd-up-and-running/README.md
  - ../../devops-keywords.md
updated: 2026-11-21
---

# 07_devops/docs/deployment — 배포 전략과 점진 배포

---

> 새 버전을 클러스터에 어떻게 내보낼지 다루는 자리입니다. 지금은 Argo Rollouts 공식 문서로 Blue-Green·Canary 를 읽은 두 편과, GitOps 와 ArgoCD 를 입문 수준으로 정리한 한 편이 있습니다.

## 다루는 범위

> 특정 도구가 아니라 "배포를 얼마나 조금씩, 무엇을 보고 진행하는가"가 이 폴더의 주제입니다.

| 질문 | 예 | 지금 자리 |
|------|----|----------|
| 쿠버네티스 기본 교체는 어디까지 하는가 | Deployment 의 RollingUpdate 에 트래픽 분리·자동 검증이 없다는 한계 | 01-01 의 출발점 |
| 두 벌을 두고 한 번에 전환하는가 | Blue-Green | 01-01·01-02 |
| 트래픽을 비율로 옮기며 판정하는가 | Canary, AnalysisTemplate 로 지표 판정 | 01-01·01-02 |
| Git 의 선언을 클러스터에 맞추는 일은 누가 하는가 | GitOps, Argo CD 의 sync | [ArgoCD와 GitOps](ArgoCD%C2%B7GitOps.md) · [Argo CD 정독 노트](../../book/argocd-up-and-running/README.md) |

한 번에 바꿀지, 두 벌을 두고 전환할지, 트래픽을 조금씩 옮기며 지표로 판정할지가 이 폴더가 고르는 문제입니다. Argo CD 는 Git 과 클러스터를 맞추는 일만 맡습니다. 트래픽을 나눠 내보내는 점진 배포는 Rollouts 같은 도구에 맡깁니다. 그래서 Argo CD 자체는 책 정독 노트가 맡고, 이 폴더는 배포 전략 쪽을 모읍니다. Argo CD 공식 문서를 따로 읽게 되면 sync wave·hook 처럼 배포 순서를 정하는 주제를 여기에 장 번호를 새로 열어 더합니다.



## 1차 자료

> 공식 문서 주소입니다. 두 노트의 프론트매터 `source` 에는 옛 주소가 적혀 있습니다.

- Argo Rollouts 공식 문서: <https://argo-rollouts.readthedocs.io/> — 01장 두 편의 1차 자료

두 노트는 2026-04-25 에 쓴 옛 정리를 옮겨 온 것이고, 옮기면서 `source` 주소와 본문을 공식 문서와 다시 대조하지 않았습니다. 버전에 따라 바뀌는 값은 읽을 때 현재 문서에서 확인합니다.



## 문서 목록

> 파일 번호가 읽기 순서입니다. 본문에서 개념을 세운 뒤 실습으로 클러스터에 적용합니다.

번호 없는 편은 따로 골라 읽는 단독 편입니다.

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [Argo Rollouts와 배포 전략](01-01.Argo%20Rollouts%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5.md) | Deployment 교체만으로는 부족한 이유와, Blue-Green·Canary·AnalysisTemplate 이 어떤 리소스를 만드는지 봅니다. |
| 01-02 | [Argo Rollouts와 배포 전략 실습](01-02.Argo%20Rollouts%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%EC%8B%A4%EC%8A%B5.md) | 컨트롤러를 설치하고 Canary, AnalysisTemplate, Blue-Green 을 차례로 적용합니다. |
| — | [ArgoCD와 GitOps](ArgoCD%C2%B7GitOps.md) | Git 을 단일 진실 공급원으로 삼는 배포 모델을 입문 수준으로 봅니다. 2026-11-21 에 08_cloud 의 11_devtools(옛 11-03)에서 옮겼습니다. |



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [07_devops MOC](../../README.md) — 대분류 지도와 로드맵 단계별 문서 수
- [iac/](../iac/README.md) — 내보낼 매니페스트를 Helm·Kustomize 로 코드화하는 앞 단계
- [GitOps 다음 걸음](../../book/argocd-up-and-running/14-01.GitOps%20%EB%8B%A4%EC%9D%8C%20%EA%B1%B8%EC%9D%8C%20%E2%80%94%20%EC%A0%80%EC%9E%A5%EC%86%8C%20%EA%B5%AC%EC%A1%B0%C2%B7Rendered%20Manifests%C2%B7%EC%8A%B9%EA%B2%A9.md#argo-rollouts-%EC%99%80-%EC%A0%90%EC%A7%84-%EB%B0%B0%ED%8F%AC) — Argo CD 가 점진 배포를 직접 하지 않고 Rollouts 같은 도구에 맡긴다는 책의 서술
- [Application 여럿을 순서대로](../../book/argocd-up-and-running/10-01.Application%20%EC%97%AC%EB%9F%BF%EC%9D%84%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%E2%80%94%20%ED%97%AC%EC%8A%A4%20%EC%B2%B4%ED%81%AC%C2%B7App-of-Apps%20sync%20wave%C2%B7Progressive%20Sync.md) — ApplicationSet 의 Progressive Sync 는 트래픽을 나누는 점진 배포와 다른 기능입니다
- [DevOps 로드맵](../../devops-keywords.md) — 6단계 점진 배포에서 이 폴더가 놓인 자리
