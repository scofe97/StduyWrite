---
title: 08_cloud/docs/architecture — 클러스터 아키텍처
tags: [moc, kubernetes, official-docs, architecture]
status: final
related:
  - ../README.md
updated: 2026-08-27
---

# 08_cloud/docs/architecture — 클러스터 아키텍처

---

> 노드·컨트롤러·리스·cgroup·가비지 컬렉션처럼 클러스터가 어떻게 짜여 있는지를 다루는 섹션입니다. 대응하는 공식문서는 `/docs/concepts/architecture/` 입니다.

## 문서 목록

> 파일 번호가 읽기 순서입니다. 각 문서는 공식문서 여러 편을 한 주제로 묶어 읽은 결과입니다.

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [노드와 클러스터의 소속 — 겹쳐 보이는 클러스터는 어느 층에서 겹치는가](01-01.%EB%85%B8%EB%93%9C%EC%99%80%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EC%9D%98%20%EC%86%8C%EC%86%8D%20%E2%80%94%20%EA%B2%B9%EC%B3%90%20%EB%B3%B4%EC%9D%B4%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%8A%94%20%EC%96%B4%EB%8A%90%20%EC%B8%B5%EC%97%90%EC%84%9C%20%EA%B2%B9%EC%B9%98%EB%8A%94%EA%B0%80.md) | 노드가 클러스터에 소속되는 경로를 kubelet 자가등록으로 따라가고, 여러 클러스터가 노드를 겹쳐 쓴다는 말이 어느 층의 이야기인지 가릅니다. |



## 아직 안 쓴 주제

> 이 섹션이 앞으로 받을 공식 페이지입니다. 쓰는 순서는 정해 두지 않고 그때 궁금한 것부터 씁니다.

- `Controllers`
- `Leases`
- `About cgroup v2`
- `Garbage Collection`
- `Kubernetes Self-Healing`
- `Cloud Controller Manager`



## 관련 문서

> 이 폴더가 딛고 서는 이웃입니다.

- [docs MOC](../README.md) — 폴더 규칙과 전체 문서 목록
