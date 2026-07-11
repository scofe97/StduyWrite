---
title: 03_storage — 저장소
tags: [moc, kubernetes, volume, pv, pvc, storageclass]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 03_storage — 저장소

> 파드가 사라져도 데이터를 남기는 스토리지 모델을 봅니다. Stateless와 Stateful이 저장소를 다루는 방식이 어떻게 갈리는지가 출발점입니다.



## 문서 목록
> 공식 concepts의 Storage에 대응합니다. 파일 번호(`03-MM`)가 읽기 순서입니다. 각 본문 끝에는 `## N. 점검 질문` 절이 있어, 개념 설명과 심화 Q&A를 한 문서에서 이어 읽습니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 03-01 | [스토리지와 상태](03-01.%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80%EC%99%80%20%EC%83%81%ED%83%9C.md) | Volume·PV·PVC로 상태를 어디에 두는지, Stateless와 Stateful의 스토리지 전략 차이를 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
