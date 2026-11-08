---
title: 08_cloud/docs MOC — 공식 문서·제품 사이트 정독
tags: [moc, cloud, official-docs, kubernetes, helm, kustomize, argo-rollouts]
status: final
related:
  - ../README.md
  - kubernetes/README.md
  - helm/README.md
  - kustomize/README.md
  - argo-rollouts/README.md
updated: 2026-11-08
---

# 08_cloud/docs — 공식 문서·제품 사이트 정독

---

> 공식 문서나 제품 사이트를 1차 자료로 삼아 궁금한 주제만 한 편씩 파고드는 자리입니다. 전체 개념을 순서대로 훑는 일은 [book/](../book/)의 정독 노트와 [kubernetes/](../kubernetes/README.md)의 주제별 노트가 맡습니다.

## 폴더 규칙

> 바로 아래에는 제품(사이트)마다 폴더를 하나씩 둡니다. 공식 문서를 다시 폈을 때 그 제품의 노트가 어디 있는지 고민하지 않게 하려는 규약입니다.

| 폴더 | 1차 자료 |
|------|----------|
| [kubernetes/](kubernetes/README.md) | kubernetes.io 공식 문서 |
| [helm/](helm/README.md) | helm.sh 공식 문서 |
| [kustomize/](kustomize/README.md) | Kustomize 공식 문서 (kubectl.docs.kubernetes.io) |
| [argo-rollouts/](argo-rollouts/README.md) | Argo Rollouts 공식 문서 (argo-rollouts.readthedocs.io) |

제품 안의 하위 폴더 규칙은 그 제품의 README 가 정합니다. 예를 들어 `kubernetes/` 는 사이트의 섹션 슬러그를 그대로 폴더 이름으로 쓰고, `helm/` 과 `kustomize/` 는 노트가 적어 폴더를 나누지 않고 파일을 바로 둡니다. 새 제품을 다루게 되면 그 제품 폴더를 만들고 이 표에 한 줄을 더합니다.



## 문서 목록

> 제품별 현재 문서입니다. 각 제품 README 에 그 제품의 읽기 순서가 있습니다.

| 제품 | 폴더 | 번호 | 제목 |
|------|------|------|------|
| kubernetes | architecture | 01-01 | [노드와 클러스터의 소속](kubernetes/architecture/01-01.%EB%85%B8%EB%93%9C%EC%99%80%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EC%9D%98%20%EC%86%8C%EC%86%8D%20%E2%80%94%20%EA%B2%B9%EC%B3%90%20%EB%B3%B4%EC%9D%B4%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%8A%94%20%EC%96%B4%EB%8A%90%20%EC%B8%B5%EC%97%90%EC%84%9C%20%EA%B2%B9%EC%B9%98%EB%8A%94%EA%B0%80.md) |
| kubernetes | cluster-administration | 01-01 | [자원 모니터링 파이프라인](kubernetes/cluster-administration/01-01.%EC%9E%90%EC%9B%90%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%E2%80%94%20kubelet%EC%9D%B4%20%EC%9E%AC%EB%8A%94%20%EA%B2%83%EA%B3%BC%20kubectl%20top%EC%9D%B4%20%EC%9D%BD%EB%8A%94%20%EA%B2%83.md) |
| kubernetes | scheduling-eviction | 01-01 | [노드 압박 축출과 디스크 관리](kubernetes/scheduling-eviction/01-01.%EB%85%B8%EB%93%9C%20%EC%95%95%EB%B0%95%20%EC%B6%95%EC%B6%9C%EA%B3%BC%20%EB%94%94%EC%8A%A4%ED%81%AC%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20DiskPressure%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%B3%B4%EA%B3%A0%20%EC%BC%9C%EC%A7%80%EB%8A%94%EA%B0%80.md) |
| helm | (바로 아래) | 01-01 | [Helm 기초](helm/01-01.Helm%20%EA%B8%B0%EC%B4%88.md) |
| helm | (바로 아래) | 01-02 | [Helm 고급](helm/01-02.Helm%20%EA%B3%A0%EA%B8%89.md) |
| kustomize | (바로 아래) | 01-01 | [Kustomize](kustomize/01-01.Kustomize.md) |
| argo-rollouts | (바로 아래) | 01-01 | [Argo Rollouts와 배포 전략](argo-rollouts/01-01.Argo%20Rollouts%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5.md) |
| argo-rollouts | (바로 아래) | 01-02 | [Argo Rollouts와 배포 전략 실습](argo-rollouts/01-02.Argo%20Rollouts%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%EC%8B%A4%EC%8A%B5.md) |



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [08_cloud MOC](../README.md) — 대분류 지도
- [kubernetes/](../kubernetes/README.md) — 주제별 학습 노트. 공식 문서 정독과 겹치는 주제는 서로 링크로 잇습니다
- [book/](../book/) — 책 정독 노트. 전체 개념의 뼈대는 이쪽에서 잡습니다
