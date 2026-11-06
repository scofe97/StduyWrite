---
title: 08_cloud/docs/kustomize — Kustomize 공식 문서 정독
tags: [moc, kustomize, official-docs]
status: final
related:
  - ../README.md
  - ../helm/README.md
  - ../../kubernetes/README.md
updated: 2026-11-06
---

# 08_cloud/docs/kustomize — Kustomize 공식 문서 정독

---

> Kustomize 공식 문서를 1차 자료로 삼아 base 와 overlay 로 환경별 차이를 조합하는 방식을 읽는 자리입니다. 노트가 한 편뿐이라 하위 폴더 없이 파일을 바로 둡니다.

## 1차 자료

> 노트 프론트매터 `source` 에 적힌 주소입니다.

- 쿠버네티스 공식 문서의 Kustomize 태스크: <https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/>
- Kustomize 레퍼런스: <https://kubectl.docs.kubernetes.io/references/kustomize/>



## 문서 목록

> Helm 의 템플릿·values 개념을 먼저 알고 읽으면 두 도구가 서로 다른 계층이라는 점이 잘 보입니다.

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [Kustomize](01-01.Kustomize.md) | Helm 없이 환경별 차이를 patch 로 선언적으로 관리하는 길을 봅니다. |



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [docs MOC](../README.md) — 제품별 폴더 규칙과 전체 문서 목록
- [helm/](../helm/README.md) — 템플릿과 values 로 패키징하는 다른 길
- [kubernetes MOC](../../kubernetes/README.md) — 전체 대주제 지도
