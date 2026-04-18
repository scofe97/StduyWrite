---
title: 05_messaging MOC
tags: [moc, messaging, kafka]
status: final
related: []
updated: 2026-04-19
---

# 05_messaging
---
> Kafka·Redpanda·Avro·Schema Registry 같은 메시징 구현 기술과 EDA 적용 문서를 모은다.

## 경계 기준

분산 시스템의 이론(Saga의 보상 트랜잭션 구조, CAP)은 `04_distributed/`에 속한다. 여기는 "Kafka Producer idempotent 옵션 튜닝"처럼 도구 레벨에서 구체적인 선택을 다룬다.

## 주요 문서 (초기 이관분)

Step C에서 이관한 주요 문서 목록이다. 각 파일에 프론트매터는 Step D에서 주입된다.

- `01-1.EDA 기초.md`
- `05-01.메세지 큐 아키텍쳐.md`, `05-02.리더 선출.md`, `05-03 Consumer Group.md`
- `06-1.Choreography-saga.md`, `06-2.Orchestration-saga.md`, `06-3.Outbox.md`
- `07-1.Kafka Stream.md`, `08-2.Event Sourcing.md`

`06-x` Saga 계열은 이론 측면이 강하면 추후 `04_distributed/`로 일부가 분할될 수 있다.
