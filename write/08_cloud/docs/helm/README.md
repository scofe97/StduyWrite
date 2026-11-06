---
title: 08_cloud/docs/helm — Helm 공식 문서 정독
tags: [moc, helm, official-docs]
status: final
related:
  - ../README.md
  - ../kustomize/README.md
  - ../../kubernetes/README.md
updated: 2026-11-06
---

# 08_cloud/docs/helm — Helm 공식 문서 정독

---

> helm.sh 의 공식 문서를 1차 자료로 삼아 Helm 의 차트·values·릴리스를 한 편씩 읽는 자리입니다. 노트가 두 편뿐이라 하위 폴더 없이 파일을 바로 둡니다.

## 1차 자료

> 노트 프론트매터 `source` 에 적힌 주소입니다.

- Helm 공식 문서: <https://helm.sh/docs/> — 기초 편의 근거
- 차트 템플릿 가이드: <https://helm.sh/docs/chart_template_guide/> — 고급 편의 근거



## 문서 목록

> 파일 번호가 읽기 순서입니다. 기초 편에서 릴리스 흐름을 잡은 뒤 고급 편에서 차트를 직접 설계합니다.

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [Helm 기초](01-01.Helm%20%EA%B8%B0%EC%B4%88.md) | 왜 생짜 매니페스트 대신 Helm 을 쓰는지, 템플릿·values 의 기본을 잡습니다. |
| 01-02 | [Helm 고급](01-02.Helm%20%EA%B3%A0%EA%B8%89.md) | 재사용 가능한 차트를 어떻게 설계하는지 봅니다. |

각 본문 끝의 `점검 질문` 절에서 개념 설명과 심화 Q&A 를 한 문서로 이어 읽습니다.



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [docs MOC](../README.md) — 제품별 폴더 규칙과 전체 문서 목록
- [kustomize/](../kustomize/README.md) — Helm 없이 환경별 차이를 patch 로 관리하는 다른 길
- [kubernetes MOC](../../kubernetes/README.md) — 전체 대주제 지도
