---
title: 08_cloud/docs/argo-rollouts — Argo Rollouts 공식 문서 정독
tags: [moc, argo-rollouts, official-docs]
status: final
related:
  - ../README.md
  - ../../book/argocd-up-and-running/README.md
  - ../../../landscape/devops-keywords.md
updated: 2026-11-08
---

# 08_cloud/docs/argo-rollouts — Argo Rollouts 공식 문서 정독

---

> Argo Rollouts 공식 문서를 1차 자료로 삼아 Blue-Green·Canary 배포와 AnalysisTemplate 을 읽는 자리입니다. 노트가 두 편뿐이라 하위 폴더 없이 파일을 바로 둡니다.

## 1차 자료

> 공식 문서 주소입니다. 두 노트의 프론트매터 `source` 에는 옛 주소가 적혀 있습니다.

- Argo Rollouts 공식 문서: <https://argo-rollouts.readthedocs.io/> — 두 편의 1차 자료

두 노트는 2026-04-25 에 쓴 옛 정리를 옮겨 온 것이고, 옮기면서 `source` 주소와 본문을 공식 문서와 다시 대조하지 않았습니다. 버전에 따라 바뀌는 값은 읽을 때 현재 문서에서 확인합니다.



## 문서 목록

> 파일 번호가 읽기 순서입니다. 본문에서 개념을 세운 뒤 실습으로 클러스터에 적용합니다.

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [Argo Rollouts와 배포 전략](01-01.Argo%20Rollouts%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5.md) | Deployment 교체만으로는 부족한 이유와, Blue-Green·Canary·AnalysisTemplate 이 어떤 리소스를 만드는지 봅니다. |
| 01-02 | [Argo Rollouts와 배포 전략 실습](01-02.Argo%20Rollouts%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%EC%8B%A4%EC%8A%B5.md) | 컨트롤러를 설치하고 Canary, AnalysisTemplate, Blue-Green 을 차례로 적용합니다. |



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [docs MOC](../README.md) — 제품별 폴더 규칙과 전체 문서 목록
- [GitOps 다음 걸음](../../book/argocd-up-and-running/14-01.GitOps%20%EB%8B%A4%EC%9D%8C%20%EA%B1%B8%EC%9D%8C%20%E2%80%94%20%EC%A0%80%EC%9E%A5%EC%86%8C%20%EA%B5%AC%EC%A1%B0%C2%B7Rendered%20Manifests%C2%B7%EC%8A%B9%EA%B2%A9.md#argo-rollouts-%EC%99%80-%EC%A0%90%EC%A7%84-%EB%B0%B0%ED%8F%AC) — Argo CD 가 점진 배포를 직접 하지 않고 Rollouts 같은 도구에 맡긴다는 책의 서술
- [Application 여럿을 순서대로](../../book/argocd-up-and-running/10-01.Application%20%EC%97%AC%EB%9F%BF%EC%9D%84%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%E2%80%94%20%ED%97%AC%EC%8A%A4%20%EC%B2%B4%ED%81%AC%C2%B7App-of-Apps%20sync%20wave%C2%B7Progressive%20Sync.md) — ApplicationSet 의 Progressive Sync 는 트래픽을 나누는 점진 배포와 다른 기능입니다
- [DevOps 로드맵](../../../landscape/devops-keywords.md) — 6단계 점진 배포에서 이 폴더가 놓인 자리
