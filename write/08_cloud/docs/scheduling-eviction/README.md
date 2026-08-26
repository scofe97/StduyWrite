---
title: 08_cloud/docs/scheduling-eviction — 스케줄링과 축출
tags: [moc, kubernetes, official-docs, scheduling-eviction]
status: final
related:
  - ../README.md
updated: 2026-08-27
---

# 08_cloud/docs/scheduling-eviction — 스케줄링과 축출

---

> 파드를 어디에 놓을지와 언제 내보낼지를 다루는 섹션입니다. 대응하는 공식문서는 `/docs/concepts/scheduling-eviction/` 입니다.

## 문서 목록

> 파일 번호가 읽기 순서입니다. 각 문서는 공식문서 여러 편을 한 주제로 묶어 읽은 결과입니다.

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [노드 압박 축출과 디스크 관리 — DiskPressure는 무엇을 보고 켜지는가](01-01.%EB%85%B8%EB%93%9C%20%EC%95%95%EB%B0%95%20%EC%B6%95%EC%B6%9C%EA%B3%BC%20%EB%94%94%EC%8A%A4%ED%81%AC%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20DiskPressure%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%B3%B4%EA%B3%A0%20%EC%BC%9C%EC%A7%80%EB%8A%94%EA%B0%80.md) | kubelet 이 자원 신호를 재고 노드 컨디션을 달고 자원을 회수한 뒤 파드를 고르는 다섯 단을 따라갑니다. 디스크 관리가 여기 붙습니다. |



## 아직 안 쓴 주제

> 이 섹션이 앞으로 받을 공식 페이지입니다. 쓰는 순서는 정해 두지 않고 그때 궁금한 것부터 씁니다.

- `Kubernetes Scheduler`
- `Assigning Pods to Nodes`
- `Taints and Tolerations`
- `Pod Topology Spread Constraints`
- `Pod Priority and Preemption`
- `API-initiated Eviction`



## 관련 문서

> 이 폴더가 딛고 서는 이웃입니다.

- [docs MOC](../README.md) — 폴더 규칙과 전체 문서 목록
