---
title: 06_data MOC
tags: [moc, database]
status: final
related: []
updated: 2026-04-19
---

# 06_data
---
> DB 스키마 설계, 인덱싱, 트랜잭션 격리 수준, CDC 파이프라인을 다룰 예정.

## 초기 상태

Step C 시점에서는 비어 있다. 문서가 5개 이상 쌓이면 하위 폴더(`postgres/`, `mysql/`, `cdc/`)로 분할을 검토한다.

## 경계 기준

Outbox 패턴의 DB 쪽 구현(폴링 쿼리, 인덱스 전략)은 여기 대상이다. 반면 Outbox의 메시징 통합·파이프라인은 `05_messaging/`으로 간다.
