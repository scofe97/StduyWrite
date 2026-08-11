---
title: 05_data/01_foundation — 데이터 시스템 기초
tags: [moc, ddia, theory, distributed]
status: final
related:
  - ../README.md
  - ../roadmap.md
updated: 2026-07-15
---

# 05_data/01_foundation — 데이터 시스템 기초
---
> Martin Kleppmann 의 *Designing Data-Intensive Applications* 1·2·3부 17편 + Write-Ahead Log 패턴 1편. 어떤 DB 제품이든 이 기반 위에서 의사결정이 갈린다.

## 01번대 — DDIA 1부 (DB 자체)

> 데이터 모델·저장·인코딩·트랜잭션·인덱스·NoSQL·캐싱.

| # | 문서 |
|---|------|
| 01-01 | [데이터 모델과 쿼리 언어](01-01.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%BF%BC%EB%A6%AC%20%EC%96%B8%EC%96%B4.md) |
| 01-02 | [저장소와 검색](01-02.%EC%A0%80%EC%9E%A5%EC%86%8C%EC%99%80%20%EA%B2%80%EC%83%89.md) |
| 01-03 | [인코딩과 진화](01-03.%EC%9D%B8%EC%BD%94%EB%94%A9%EA%B3%BC%20%EC%A7%84%ED%99%94.md) |
| 01-04 | [트랜잭션과 격리 수준](01-04.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EA%B3%BC%20%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80.md) |
| 01-05 | [인덱스 이론](01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) |
| 01-06 | [NoSQL 비교](01-06.NoSQL%20%EB%B9%84%EA%B5%90.md) |
| 01-07 | [캐싱 전략](01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) |

## 02번대 — DDIA 2부 (분산)

> 시스템 아키텍처·복제·샤딩·분산 문제·합의·철학.

| # | 문서 |
|---|------|
| 02-01 | [시스템 아키텍처 트레이드오프](02-01.%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%98%A4%ED%94%84.md) |
| 02-02 | [시스템 아키텍처 트레이드오프 부록](02-02.%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%98%A4%ED%94%84%20%EB%B6%80%EB%A1%9D.md) |
| 02-03 | [복제](02-03.%EB%B3%B5%EC%A0%9C.md) |
| 02-04 | [샤딩](02-04.%EC%83%A4%EB%94%A9.md) |
| 02-05 | [분산 시스템의 문제점](02-05.%EB%B6%84%EC%82%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90.md) |
| 02-06 | [일관성과 합의](02-06.%EC%9D%BC%EA%B4%80%EC%84%B1%EA%B3%BC%20%ED%95%A9%EC%9D%98.md) |
| 02-07 | [철학적 고찰](02-07.%EC%B2%A0%ED%95%99%EC%A0%81%20%EA%B3%A0%EC%B0%B0.md) |

## 03번대 — DDIA 3부 (처리) + WAL

> 배치·스트림 처리, WAL 패턴.

| # | 문서 |
|---|------|
| 03-01 | [배치 처리](03-01.%EB%B0%B0%EC%B9%98%20%EC%B2%98%EB%A6%AC.md) |
| 03-02 | [스트림 처리](03-02.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC.md) |
| 03-03 | [스트리밍 시스템 철학](03-03.%EC%8A%A4%ED%8A%B8%EB%A6%AC%EB%B0%8D%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%B2%A0%ED%95%99.md) |
| 03-04 | [WAL 패턴](03-04.WAL%20%ED%8C%A8%ED%84%B4.md) |

## 2판 정독은 별도 폴더

> 위 18편은 1판 기준 요약입니다. 2판은 장 번호와 구성이 달라 책 단위 정독 폴더로 분리했습니다.

같은 책의 2판을 장별로 정독한 노트는 [`book/designing-data-intensive-applications/`](../book/designing-data-intensive-applications/README.md)에 있습니다. 판본이 다르면 장 번호가 어긋나 한 폴더에서 섞으면 어느 판의 몇 장인지 추적이 끊기므로, 1판 요약(이 폴더)과 2판 정독(책 폴더)을 나눠 둡니다.
