---
title: 04_messaging/docs MOC — 공식 문서·제품 사이트 정독
tags: [moc, messaging, official-docs, flink]
status: draft
related:
  - ../README.md
  - flink/README.md
  - ../../05_data/docs/README.md
updated: 2026-11-18
---

# 04_messaging/docs — 공식 문서·제품 사이트 정독

---

> 메시징·스트림 처리 제품의 공식 문서를 1차 자료로 삼아 한 편씩 쓰는 자리입니다. 주제별로 이미 정리한 노트는 [04_messaging MOC](../README.md)의 번호 폴더에 있습니다.

## 폴더 규칙

> 바로 아래에는 제품마다 폴더를 하나씩 둡니다. 공식 문서를 다시 폈을 때 그 제품의 노트가 어디 있는지 고민하지 않게 하려는 규약입니다.

| 폴더 | 1차 자료 | 묶는 기준 |
|------|----------|----------|
| [flink/](flink/README.md) | Apache Flink 2.3 공식 문서 | 제품 |

이 규약은 [05_data/docs](../../05_data/docs/README.md)와 같습니다.

Flink 를 05_data 가 아니라 여기에 두는 근거는 [05_data MOC](../../05_data/README.md)의 경계 기준입니다. 그 기준은 스트림 처리의 일반 이론을 『Designing Data-Intensive Applications』 12장 정독 노트에 둡니다. 브로커·Kafka Streams·CDC 의 구현은 04_messaging 에 둡니다. Flink 는 스트림 처리를 구현한 제품이므로 Kafka Streams 와 같은 쪽에 놓았습니다.



## 문서 목록

> 각 폴더 README 에 예정 편과 읽는 순서가 있습니다.

| 폴더 | 상태 | 예정 편 |
|------|------|--------|
| [flink/](flink/README.md) | 지도만 있음 | 예정 13편, 쓴 편 없음. `table-sql` 5편, `deployment` 3편, `operations` 5편 |



## 관련 문서

- [04_messaging MOC](../README.md) — 메시징 카테고리 전체 지도
- [Kafka Streams](../06_StreamProcessing/01-01.Kafka%20Streams.md) — Kafka Streams 로 본 스트림 처리 기본 모델
- [05_data/docs](../../05_data/docs/README.md) — 같은 규약을 쓰는 docs 폴더
