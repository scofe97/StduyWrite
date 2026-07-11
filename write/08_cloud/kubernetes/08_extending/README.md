---
title: 08_extending — 확장
tags: [moc, kubernetes, crd, operator, controller]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 08_extending — 확장

> CRD와 Controller로 Kubernetes 위에 우리만의 리소스를 얹어, Stateful 워크로드의 Day-2 운영을 자동화합니다. 개념부터 MySQL·PostgreSQL·Redis·Kafka·Redpanda Operator까지 한 묶음입니다.



## 문서 목록
> 공식 concepts의 Extending Kubernetes에 대응합니다. 파일 번호(`08-MM`)가 읽기 순서입니다. 각 본문 끝에는 `## N. 점검 질문` 절이 있어, 개념 설명과 심화 Q&A를 한 문서에서 이어 읽습니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 08-01 | [Operator 패턴](08-01.Operator%20%ED%8C%A8%ED%84%B4.md) | CRD와 컨트롤러가 어떻게 연동돼 "원하는 상태"를 코드로 표현하는지 봅니다. |
| 08-02 | [MySQL Operator](08-02.MySQL%20Operator.md) | MySQL HA를 어떻게 선언적으로 자동화하는지 봅니다. |
| 08-03 | [PostgreSQL Operator](08-03.PostgreSQL%20Operator.md) | CloudNativePG의 복제·백업 전략을 봅니다. |
| 08-04 | [Redis Operator](08-04.Redis%20Operator.md) | Cluster와 Sentinel이 언제 갈라지는지 봅니다. |
| 08-05 | [Kafka Operator](08-05.Kafka%20Operator.md) | Strimzi로 Kafka를 선언적으로 관리하는 법을 봅니다. |
| 08-06 | [Redpanda Operator](08-06.Redpanda%20Operator.md) | Strimzi와 Redpanda Operator의 차이를 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
