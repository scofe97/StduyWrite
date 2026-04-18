---
title: 05_messaging/spring — Spring Kafka·메시징 실습
tags: [moc, spring, kafka, spring-kafka]
status: final
related:
  - ../README.md
  - ../../01_language/java/spring/README.md
updated: 2026-04-19
---

# 05_messaging/spring
---
> Spring Kafka, `@KafkaListener`, Producer Config, CloudEvents 헤더, Avro 직렬화 같은 Spring 메시징 구현 문서를 모은다.

## 경계

- Kafka 자체 원리(파티션, Consumer Group, 리밸런싱)는 [`05_messaging/`](../) 직접 하위
- Saga·Outbox의 이론 측면은 `04_distributed/` 후보
- **Spring이 Kafka와 어떻게 통합되는지** — 여기

## 기존 문서 (이관된 초안)

이 폴더는 이전 `03_SpringPractice/`에서 이름만 바뀌었다. 기존 `0x-` 초안은 `status: draft` 상태로 남아 있으며 정식 번호 부여가 필요하다.

- `0x-01.CloudEventsHeaderInterceptor와 헤더 자동 부착 방식.md`
- `0x-02.DlqConsumer와 DLQ 소비 흐름.md`
- `0x-03.TopicConfig와 파티션 수, 소비 병렬성.md`
- `0x-03.Avro 직렬화와 Consumer 수신 패턴 두 가지.md`
- `0x-0x.Spring Kafka DLT와 Producer Config 분석.md`
- `0x-0x.trace-id와 traceparent.md`

## 관련 문서

- [Spring 통합 MOC](../../01_language/java/spring/README.md)
