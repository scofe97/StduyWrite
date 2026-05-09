---
title: 05_messaging/spring — TPS message-lib 코드 디테일
tags: [moc, spring, kafka, spring-kafka]
status: final
related:
  - ../README.md
  - ../../01_language/java/spring/README.md
updated: 2026-05-09
---

# 05_messaging/spring — TPS message-lib 코드 디테일

> 상위 [`05_messaging/`](../)이 일반 개념을 다룬다면, 이 폴더는 TPS `message-lib` 모듈의 실제 클래스가 어떻게 구성됐는지를 코드 레벨로 정리한다. 상위 문서 말미의 "TPS 적용 사례" 박스가 1~3줄 요약이라면, 여기 문서는 그 박스의 풀 버전이다.

## 학습 흐름

발행 측(01-01~02) → 소비 측(01-03) → 에러 흐름(01-04~05) → 추적(01-06) → 운영 고급(01-07)

각 문서는 코드 클래스 하나(또는 짝지어진 클래스 묶음)를 출발점으로 잡고, 왜 그렇게 짜였는지·다른 선택지는 무엇이었는지를 정리한다.

## 문서 인덱스

- [01-01.CloudEventsHeaderInterceptor](01-01.CloudEventsHeaderInterceptor.md) — Envelope 공통 헤더 자동 부착, ProducerInterceptor의 역할 분담 (현재 `CorrelationIdRecordInterceptor`로 이전됨)
- [01-02.TopicConfig와 파티션 설계](01-02.TopicConfig와%20파티션%20설계.md) — 토픽 정의·파티션 수가 소비 병렬성과 어떻게 연결되는지
- [01-03.Avro Consumer 수신 패턴](01-03.Avro%20Consumer%20수신%20패턴.md) — 앱 내부 Avro vs 외부 JSON, 토픽 분리 원칙
- [01-04.Spring Kafka DLT와 Producer Config](01-04.Spring%20Kafka%20DLT와%20Producer%20Config.md) — `DefaultErrorHandler + DeadLetterPublishingRecoverer` 흐름과 `KafkaProducerConfig`의 위치
- [01-05.DlqConsumer](01-05.DlqConsumer.md) — DLQ 끝단 소비자 (현재 코드에서는 미존재. 발행만 처리됨)
- [01-06.trace-id와 traceparent](01-06.trace-id와%20traceparent.md) — `trace-id`(MDC 운영용)와 `traceparent`(W3C Trace Context 표준)의 차이
- [01-07.Spring Kafka 운영 고급](01-07.Spring%20Kafka%20운영%20고급.md) — Vertical scaling(`concurrency`), 런타임 동적 컨슈머, blocking vs non-blocking retry 결정 기준, Micrometer trace 전파 (ING 운영 사례 기반)

## 상위 문서와의 경계

| 상위 (`05_messaging/`) | 대응 spring/ 문서 |
|---|---|
| [02-04.EventEnvelope 적용](../02-04.EventEnvelope%20적용.md) | [01-01.CloudEventsHeaderInterceptor](01-01.CloudEventsHeaderInterceptor.md) |
| [03-01.토픽 디자인](../03-01.토픽%20디자인.md) | [01-02.TopicConfig와 파티션 설계](01-02.TopicConfig와%20파티션%20설계.md) |
| [02-03.Avro](../02-03.Avro.md) / [02-05.Avro 직렬화 예외처리 전략](../02-05.Avro%20직렬화%20예외처리%20전략.md) | [01-03.Avro Consumer 수신 패턴](01-03.Avro%20Consumer%20수신%20패턴.md) |
| [02-05.Avro 직렬화 예외처리 전략](../02-05.Avro%20직렬화%20예외처리%20전략.md) | [01-04.Spring Kafka DLT와 Producer Config](01-04.Spring%20Kafka%20DLT와%20Producer%20Config.md) / [01-05.DlqConsumer](01-05.DlqConsumer.md) |
| [02-04.EventEnvelope 적용](../02-04.EventEnvelope%20적용.md) | [01-06.trace-id와 traceparent](01-06.trace-id와%20traceparent.md) |
| [04-03.Consumer Group](../04-03.Consumer%20Group.md) | [01-07.Spring Kafka 운영 고급](01-07.Spring%20Kafka%20운영%20고급.md) |

원리·왜 필요한가는 상위에서, "현재 message-lib에서 어떻게 구현됐나"는 여기서.

## 코드 베이스 위치

`/Users/simbohyeon/okestro/tps-gitlab2/message-lib/src/main/java/org/okestro/tps/messaging/`

주요 패키지:

- `application/outbox/` — `EventPublisher`, `OutboxPoller`
- `domain/outbox/` — `OutboxEvent`, `OutboxStatus`, `OutboxRetryPolicy`
- `infrastructure/outbox/` — `OutboxAutoConfiguration`, `JpaOutboxEventRepository`, `OutboxMetrics`
- `config/` — `KafkaErrorConfig`, `KafkaJsonConsumerConfig`, `KafkaRetryTemplateConfig`, `KafkaDefaultsEnvironmentPostProcessor`
- `serialization/` — `AvroSerializer`, `AvroSerializationException`
- `topic/` — `Topics` (enum), `TopicConfig`
- `tracing/` — `MessagingTracingAutoConfiguration`, `CorrelationIdRecordInterceptor`, `CorrelationIdContext`, `TraceContextUtil`
- `property/` — `OutboxProperties`, `TopicProperties`

문서별 본문에서 인용하는 클래스 경로가 위 패키지와 다르거나(예: 옛 `dlq/` 패키지) 클래스 자체가 사라진 경우, 해당 문서 상단의 ⚠️ 박스에 구체적 차이를 명시했다.

## 관련 문서

- [상위 MOC](../README.md)
- [Spring 통합 MOC](../../01_language/java/spring/README.md)
