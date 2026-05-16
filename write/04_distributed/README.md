---
title: 04_distributed MOC
tags: [moc, distributed, ddia, replication, sharding, consensus]
status: final
source:
  - https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/
  - ../../docs/04_Database/02_분산시스템/
related:
  - ../06_data/README.md
  - ../05_messaging/README.md
updated: 2026-05-07
---

# 04_distributed
---
> 분산 시스템 이론과 패턴을 모은다. CAP, Consistency 모델, 복제·샤딩·합의·Saga·Outbox 같은 구조적 해법이 자리다.

## 경계 기준

`03_architecture/` 는 "한 시스템 안의 설계 원칙" 을 다룬다. 본 카테고리는 "여러 노드·서비스가 엮일 때 생기는 문제" 가 출발점이다. Saga 의 이론적 구조(보상 트랜잭션, 실패 복구) 는 여기지만, Kafka 로 Saga 를 실제 구현하는 문서는 [`../05_messaging/`](../05_messaging/) 으로 간다. DB 자체 이론(격리 수준·인덱스) 은 [`../06_data/fundamentals/`](../06_data/fundamentals/) 가 자리고, 분산 트랜잭션의 코디네이터·복제 토폴로지가 주제일 때 본 카테고리에 들어온다.

## 학습 순서

> DDIA 2부(Distributed Data) 를 1장에 통째로 풀어 둔다. 시스템 트레이드오프 → 복제 → 샤딩 → 분산 시스템의 문제점 → 일관성과 합의 → 철학적 정리 순서다.

| # | 문서 | 다루는 핵심 | 상태 |
|---|------|-----------|------|
| 01-01 | [시스템 아키텍처 트레이드오프](01-01.시스템%20아키텍처%20트레이드오프.md) | OLTP·OLAP, 클라우드·셀프호스팅, 분산 vs 단일, 마이크로서비스, GDPR | ✅ Phase 3 |
| 01-02 | [시스템 아키텍처 트레이드오프 부록](01-02.시스템%20아키텍처%20트레이드오프%20부록.md) | 응답시간·처리량·백분위수, Fault·Failure, 확장성, 유지보수성 | ✅ Phase 3 |
| 01-03 | [복제](01-03.복제.md) | 단일/다중 리더, 리더리스, 복제 지연, 충돌 해결, Quorum | ✅ Phase 3 |
| 01-04 | [샤딩](01-04.샤딩.md) | 키 범위·해시·일관된 해싱, 핫스팟, 리밸런싱, 라우팅 | ✅ Phase 3 |
| 01-05 | [분산 시스템의 문제점](01-05.분산%20시스템의%20문제점.md) | 부분 실패, 비동기 네트워크, 시계, 펜싱 토큰, 시스템 모델 | ✅ Phase 3 |
| 01-06 | [일관성과 합의](01-06.일관성과%20합의.md) | 선형성, 인과·순차 일관성, 논리 클럭, Raft·Paxos, ZooKeeper·etcd | ✅ Phase 3 |
| 01-07 | [철학적 고찰](01-07.철학적%20고찰.md) | 예측 분석의 편향, 자동 결정 책임, 프라이버시, 데이터의 양면성 | ✅ Phase 3 |

처음 보는 학습자는 01-01 부터 따라간다. 운영에서 Kafka 의 ISR·리더 선출 로 진입했다면 01-03(복제) 와 01-06(일관성과 합의) 를 먼저 펼치는 흐름도 가능하다.

## 현재 상태

Phase 3 에서 7편 모두 채워졌다. DDIA Part II(Distributed Data) 가 본 카테고리의 첫 콘텐츠로 자리 잡았다. 향후 Saga·Outbox 같은 분산 패턴, Kubernetes·Service Mesh 같은 운영 인프라가 추가될 예정이다.

## 사전 지식

> 본 묶음은 다음을 안다고 가정한다.

1. 단일 DB 의 트랜잭션·격리 수준이 무엇인지 안다 ([`../06_data/fundamentals/01-04.트랜잭션과 격리 수준.md`](../06_data/fundamentals/01-04.트랜잭션과%20격리%20수준.md)).
2. CAP 정리를 한 문장으로 들어 본 적이 있다.
3. Kafka 또는 다른 메시지 큐를 한 번이라도 써 봤다.

## 면접 대비 체크리스트 (후속 Phase 에서 채움)

1. CAP 정리에서 P 가 사실상 강제되는 이유는?
2. 단일 리더와 다중 리더 복제의 트레이드오프를 한 시나리오로 설명할 수 있는가?
3. Quorum (`w + r > n`) 공식이 보장하는 것과 보장하지 않는 것은?
4. 2PC 와 Raft 가 풀려는 문제와 결과적 보장 차이는?
5. 비잔틴 결함이 일반 분산 시스템 가정에서 보통 제외되는 이유는?

## 관련 문서

- [`../06_data/fundamentals/01-04.트랜잭션과 격리 수준.md`](../06_data/fundamentals/01-04.트랜잭션과%20격리%20수준.md) — 단일 DB 트랜잭션, 본 카테고리 진입 전 어휘
- [`../05_messaging/README.md`](../05_messaging/README.md) — Kafka·Redpanda 구현
- [`../03_architecture/README.md`](../03_architecture/README.md) — 단일 시스템 설계 원칙
