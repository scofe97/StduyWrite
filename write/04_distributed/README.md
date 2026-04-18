---
title: 04_distributed MOC
tags: [moc, distributed]
status: final
related: []
updated: 2026-04-19
---

# 04_distributed
---
> 분산 시스템 이론과 패턴을 모은다. CAP, Consistency 모델, Saga, Outbox, Inbox 같은 구조적 해법.

## 경계 기준

`03_architecture/`는 "한 시스템 안의 설계 원칙"을 다룬다. 반면 여기는 "여러 노드·서비스가 엮일 때 생기는 문제"를 다룬다. Saga의 이론적 구조(보상 트랜잭션, 실패 복구)는 이 카테고리지만, Kafka로 Saga를 실제 구현하는 문서는 `05_messaging/`으로 간다.

## 초기 상태

Step C 시점에서는 비어 있다. `05_messaging/06-1.Choreography-saga.md` 같은 기존 문서 중 이론 측면이 강한 것은 차후 분할하면서 옮긴다.
