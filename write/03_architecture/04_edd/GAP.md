---
title: 04_edd — SSOT 커버리지 갭
tags: [meta, event-driven, coverage]
status: draft
related:
  - ./README.md
  - ../../../docs/02_Architecture/03_EventDriven/
  - ../../04_messaging/README.md
updated: 2026-05-23
---

# 04_edd — SSOT 커버리지 갭
---
> `docs/02_Architecture/03_EventDriven/` 17편 ↔ 본 시리즈 매핑. 본 시리즈는 **이론·원칙** 측만 다루고, **구현 디테일** 은 `write/04_messaging/` 에 위임한다.

## SSOT ↔ 본 시리즈 매핑

| SSOT (docs/03_EventDriven) | 본 시리즈 | 04_messaging 위임 | 상태 |
|---------------------------|----------|-------------------|------|
| 01_이벤트_기반_마이크로서비스_필요성 | 01-01 이벤트 기반 아키텍처 (흡수) | — | final |
| 02_이벤트_기반_마이크로서비스_기초 | 01-02 토폴로지와 단일 작성자 원칙 | ../../04_messaging/03_TopicDesign/01-01.토픽 디자인.md | final |
| 03_통신과_데이터_계약 | 01-03 데이터 계약과 스키마 설계 원칙 | 02-02.Schema Registry, 02-06.Avro 스키마 진화 패턴 | final |
| 04_기존_시스템과의_통합 | 01-04 기존 시스템 통합 — Data Liberation 과 CDC | 05-03.Outbox, 05-06.CDC | final |
| 05_이벤트_기반_처리_기초 | (본 시리즈 별도 챕터 없음 — 01-02 와 02-03 에 흡수) | 06-01.Kafka Streams | — |
| 06_결정적_스트림_처리 | 02-03 결정적 스트림 처리 — 워터마크와 스트림 타임 | 06-01.Kafka Streams | final |
| 07_상태_기반_스트리밍 | 02-04 상태 기반 스트리밍 | 06-02.Kafka Streams Spring Boot | final |
| 08_마이크로서비스_워크플로우_구축 | 03-02 Choreography vs Orchestration | 05-01.Choreography Saga, 05-02.Orchestration Saga | final |
| 09_FaaS_기반_마이크로서비스 | (본 시리즈 범위 밖 — 향후 08_cloud 후보) | — | 보류 |
| 10_기본_프로듀서_컨슈머_마이크로서비스 | (본 시리즈 범위 밖 — 구현은 04_messaging) | 04_messaging 전반 | 보류 |
| 11_헤비웨이트_프레임워크_마이크로서비스 | (본 시리즈 범위 밖 — 프레임워크 선택은 04_messaging/06-01) | 06-01.Kafka Streams | 보류 |
| 12_라이트웨이트_프레임워크_마이크로서비스 | (본 시리즈 범위 밖 — 동일) | 06-02.Kafka Streams Spring Boot | 보류 |
| 13_이벤트_기반과_요청-응답_마이크로서비스_통합 | 03-03 요청-응답과 이벤트 통합 | 01-02.EDA 기반 요청응답 통합, 01-03.202 Accepted + Polling 패턴 | final |
| 14_지원_도구 | 04-01 지원 도구 — 스키마 레지스트리·할당량·오프셋 관리 | 02-02.Schema Registry | final |
| 15_이벤트_기반_마이크로서비스_테스팅 | 04-02 이벤트 기반 마이크로서비스 테스팅 | — | final |
| 16_이벤트_기반_마이크로서비스_배포 | 04-03 이벤트 기반 마이크로서비스 배포 패턴 | — | final |
| 17_결론 | (본 시리즈 별도 챕터 불필요) | — | — |
| (DDD 측) 11_Dealing_with_Events_and_Their_Evolution | 02-05 이벤트 진화 다루기 | 02-06.Avro 스키마 진화 패턴 | final |
| (DDD 측) 12_Orchestrating_Complexity | 03-02 Choreography vs Orchestration (공통) | 05-02.Orchestration Saga | final |

## 범위 외 (보류) 결정 근거

- SSOT 09~12 는 **실행 환경·런타임 선택** 영역이라 `write/03_architecture/04_edd/` 의 "아키텍처 원칙" 범위를 벗어남. 향후 `write/08_cloud/`(FaaS) 또는 `write/04_messaging/` 의 프레임워크 선택 섹션에서 다룬다.
- SSOT 17 결론은 책 전체 요약이라 별도 챕터로 박제할 학습 가치가 낮다.

## 작성 우선순위 (다음 세션 이후)

1. 01-03 데이터 계약과 스키마 설계 원칙 (시리즈 전체의 기반)
2. 01-02 토폴로지와 단일 작성자 원칙
3. 01-04 Data Liberation 과 CDC
4. 03-02 Choreography vs Orchestration (DDD 측 04-02 와 함께)
5. 02-05 이벤트 진화 다루기
6. 02-03 결정적 스트림 처리
7. 02-04 상태 기반 스트리밍
8. 03-03 요청-응답과 이벤트 통합
9. 04-01 지원 도구
10. 04-02 테스팅 / 04-03 배포 패턴
