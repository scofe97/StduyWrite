---
title: 09_advanced — 메시징 심화 자료
tags: [moc, advanced, messaging, kafka]
status: final
related:
  - ../README.md
updated: 2026-05-09
---

# 09_advanced — 메시징 심화 자료

> 상위 `05_messaging/`이 "기본 패턴 이해"에 집중한다면, 이 폴더는 그 패턴을 운영 규모로 키울 때 등장하는 **변종·비교·진화**를 다룬다. 본 학습 트리의 정상 흐름을 마쳤거나 TPS 적용 시점에 도달한 독자가 다음 선택을 가늠할 때 읽는 자료다.

## 문서 인덱스

- [09-01.Outbox 변종 비교](09-01.Outbox%20변종%20비교.md) — 폴링 기반·log-based CDC·DB 네이티브 시그널·메시징 native의 트레이드오프, Shopify·Uber·Wix 등 사례
- [09-02.Saga 엔진 비교](09-02.Saga%20엔진%20비교.md) — 손코딩 오케스트레이션 vs Temporal/Cadence/Camunda 8/Conductor/Step Functions, 도입 시그널과 마이그레이션 비용
- [09-03.스트림 처리 진화](09-03.스트림%20처리%20진화.md) — Kafka Streams → Flink/ksqlDB/Materialize/RisingWave, exactly-once 보장 비교
- [09-04.스키마 거버넌스](09-04.스키마%20거버넌스.md) — 호환성 자동화·subject naming·RBAC·contract testing(Pact, Microcks)·데이터 카탈로그

## 사용법

각 문서는 다음 4단 구조를 따른다.

1. **출발점**: 본 학습 트리에서 다룬 기본형 (예: 09-01의 출발점은 `05-03.Outbox`의 폴링 Relay)
2. **변종 비교**: 5개 이상의 대안과 핵심 트레이드오프 매트릭스
3. **외부 사례**: 회사 엔지니어링 블로그, 공식 문서 등 1차 자료 기반 (각 사례마다 출처 URL 표기)
4. **TPS 적용 가능성**: 현재 `okestro/tps-gitlab2` 코드 기준으로 도입 시그널·리스크·이행 단계

## 출처 정책

- 1차 자료 우선: 회사 엔지니어링 블로그, 공식 문서, 학술 논문, 컨퍼런스 발표
- 2차 자료(요약 글, 미디엄 포스트)는 1차 자료 링크와 함께 사용
- 모든 사례는 출처 URL을 인용 라인 또는 footnote로 표기
- AI 생성 추정·일반 통념은 본문에 적지 않음. 확인되지 않은 사실은 "추정", "보고된 바에 따르면" 같이 명시

## 비범위

- 기본 패턴 자체의 설명: 상위 `05_messaging/` 참조
- TPS 코드 디테일: `spring/` 참조
- 일반 분산 시스템 이론(CAP, FLP impossibility 등): `04_distributed/` 참조
