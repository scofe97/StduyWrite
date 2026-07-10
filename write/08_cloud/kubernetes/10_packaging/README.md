---
title: 10_packaging — 패키징 도구
tags: [moc, kubernetes, helm, kustomize]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 10_packaging — 패키징 도구

> 반복되는 매니페스트를 패키지로 묶어 환경별 차이를 선언적으로 관리합니다. Helm 템플릿과 Kustomize patch가 두 갈래입니다.



## 문서 목록
> 공식 concepts에는 없는 비공식 주제입니다 — 매니페스트를 다루는 패키징 도구를 모았습니다. 파일 번호(`10-MM`)가 읽기 순서입니다. 각 본문에는 같은 번호의 `점검.md`가 짝을 이룹니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 10-01 | [Helm 기초](10-01.Helm%20%EA%B8%B0%EC%B4%88.md) | 왜 생짜 매니페스트 대신 Helm을 쓰는지, 템플릿·values의 기본을 잡습니다. |
| 10-02 | [Helm 고급](10-02.Helm%20%EA%B3%A0%EA%B8%89.md) | 재사용 가능한 차트를 어떻게 설계하는지 봅니다. |
| 10-03 | [Kustomize](10-03.Kustomize.md) | Helm 없이 환경별 차이를 patch로 선언적으로 관리하는 길을 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
