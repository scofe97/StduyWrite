---
title: 07_security — 보안
tags: [moc, kubernetes, rbac, serviceaccount, admission, networkpolicy]
status: final
related:
  - ../README.md
  - ../04_networking/README.md
updated: 2026-07-12
---

# 07_security — 보안

> 누가 무엇을 할 수 있는지, 권한을 어떻게 좁히는지를 봅니다. RBAC·ServiceAccount·Admission·Pod Security를 클러스터 보안 경계로 묶고, NetworkPolicy는 보안 관점에서 Cilium·클러스터 하드닝으로 이어 봅니다.



## 문서 목록
> 공식 concepts의 Security에 대응합니다. 파일 번호(`07-MM`)가 읽기 순서입니다. 각 본문 끝에는 `## N. 점검 질문` 절이 있어, 개념 설명과 심화 Q&A를 한 문서에서 이어 읽습니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 07-01 | [RBAC과 보안](07-01.RBAC%EA%B3%BC%20%EB%B3%B4%EC%95%88.md) | RBAC·ServiceAccount·Admission·Pod Security를 묶고, NetworkPolicy를 클러스터 하드닝·Cilium L7 확장 관점에서 조망합니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
- [NetworkPolicy 정본](../04_networking/04-07.NetworkPolicy.md) — 표준 NetworkPolicy의 selector·ingress/egress 격리·additive 허용 계산을 이 문서가 전담합니다.
- [04_networking MOC](../04_networking/README.md) — Service·DNS·NetworkPolicy·dual-stack·토폴로지 라우팅의 학습 순서를 봅니다.
