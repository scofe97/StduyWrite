---
title: 05_scheduling — 스케줄링
tags: [moc, kubernetes, scheduler, affinity, taint, hpa, pdb]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 05_scheduling — 스케줄링

> 파드를 어느 노드에 둘지, 동시 중단을 얼마나 허용할지, 부하에 따라 어떻게 늘리고 줄일지를 봅니다.



## 문서 목록
> 공식 concepts의 Scheduling, Preemption and Eviction에 대응합니다. 파일 번호(`05-MM`)가 읽기 순서입니다. 각 본문 끝에는 `## N. 점검 질문` 절이 있어, 개념 설명과 심화 Q&A를 한 문서에서 이어 읽습니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 05-01 | [스케줄링과 노드 선택](05-01.%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%EA%B3%BC%20%EB%85%B8%EB%93%9C%20%EC%84%A0%ED%83%9D.md) | kube-scheduler의 Filter·Score와 nodeAffinity·Taint가 어떻게 보완되는지 봅니다. |
| 05-02 | [토폴로지 분산과 중단 정책](05-02.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EB%B6%84%EC%82%B0%EA%B3%BC%20%EC%A4%91%EB%8B%A8%20%EC%A0%95%EC%B1%85.md) | Topology Spread·PodDisruptionBudget·PriorityClass·Eviction이 가용성을 어떻게 만드는지 봅니다. |
| 05-03 | [오토스케일링](05-03.%EC%98%A4%ED%86%A0%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | HPA·VPA·KEDA가 어떻게 역할을 나누는지 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
