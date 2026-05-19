---
title: 05_messaging/spring — TPS message-lib 코드 디테일
tags: [moc, spring, kafka, spring-kafka]
status: final
related:
  - ../README.md
  - ../../12_spring/README.md
updated: 2026-05-14
---

# 05_messaging/spring — TPS message-lib 코드 디테일

> 상위 [`05_messaging/`](../)이 일반 개념을 다룬다면, 이 폴더는 TPS `message-lib` 모듈의 실제 클래스가 어떻게 구성됐는지를 코드 레벨로 정리한다. 상위 문서 말미의 "TPS 적용 사례" 박스가 1~3줄 요약이라면, 여기 문서는 그 박스의 풀 버전이다.

## 학습 흐름

발행 측(01-01·02), 소비 측(02-01), 에러 흐름(03-01·02·03·04·05), 추적(04-01), 운영 고급(05-01·02·03), config 디렉토리 종합(06-01) 순서로 읽는다.

각 문서는 코드 클래스 하나(또는 짝지어진 클래스 묶음)를 출발점으로 잡고, 왜 그렇게 짜였는지·다른 선택지는 무엇이었는지를 정리한다.

> 본 README 의 순서는 *카테고리별 순차 학습* 동선이다. 각 문서 끝에 적힌 "다음 학습 단계" 는 *주제 측면 cross-link* 라서 카테고리 순서와 다를 수 있다. 둘 중 어느 쪽으로 읽어도 일관성을 유지하도록 1차 소스/요약 관계를 본문에 명시했다.

> 넘버링 규칙(2026-05-15 분할): 첫 두 자리는 카테고리(01 publisher / 02 consumer / 03 error / 04 tracing / 05 ops / 06 config), 뒤 두 자리는 카테고리 내 순서. 이전엔 모두 `01-XX`로 묶여 있어 카테고리 식별이 불가능했다.

## 문서 인덱스

### 01. Publisher

- [01-01.CloudEventsHeaderInterceptor](01-01.CloudEventsHeaderInterceptor.md) — Envelope 공통 헤더 자동 부착, ProducerInterceptor의 역할 분담 (현재 `CorrelationIdRecordInterceptor`로 이전됨)
- [01-02.TopicConfig와 파티션 설계](01-02.TopicConfig와%20파티션%20설계.md) — 토픽 정의·파티션 수가 소비 병렬성과 어떻게 연결되는지

### 02. Consumer

- [02-01.Avro Consumer 수신 패턴](02-01.Avro%20Consumer%20수신%20패턴.md) — 앱 내부 Avro vs 외부 JSON, 토픽 분리 원칙

### 03. Error / DLT

- [03-01.Spring Kafka DLT와 Producer Config](03-01.Spring%20Kafka%20DLT와%20Producer%20Config.md) — `DefaultErrorHandler + DeadLetterPublishingRecoverer` 흐름과 `KafkaProducerConfig`의 위치
- [03-02.DlqConsumer](03-02.DlqConsumer.md) — DLQ 끝단 소비자 (현재 코드에서는 미존재. 발행만 처리됨)
- [03-03.Kafka 예외 처리 통합](03-03.Kafka%20예외%20처리%20통합.md) — `KafkaErrorConfig`를 축으로 Producer outbox 상태머신·Consumer 두 겹 방어선·세 가지 재시도 패턴·DLQ 끝단 운영을 한 장에 모은 통합 가이드
- [03-04.KafkaErrorConfig DLT 헤더 폭증 사고](03-04.KafkaErrorConfig%20DLT%20헤더%20폭증%20사고.md) — 06-01 §4의 KafkaErrorConfig 부분을 *라인 단위*로 풀고 그 위에서 발생한 무한 루프 사고(2026-05-14, `RecordTooLargeException`)를 시간순 재구성
- [03-05.Backoff 전략 비교와 선택](03-05.Backoff%20전략%20비교와%20선택.md) — Fixed vs Exponential vs WithMaxRetries 곡선 비교, jitter와 thundering herd, `@RetryableTopic` 백오프가 글로벌 백오프와 다른 인스턴스인 이유

### 04. Tracing

- [04-01.trace-id와 traceparent](04-01.trace-id와%20traceparent.md) — `trace-id`(MDC 운영용)와 `traceparent`(W3C Trace Context 표준)의 차이

### 05. Ops

- [05-01.Spring Kafka 운영 고급](05-01.Spring%20Kafka%20운영%20고급.md) — Vertical scaling(`concurrency`), 런타임 동적 컨슈머, blocking vs non-blocking retry 결정 기준, Micrometer trace 전파 (ING 운영 사례 기반)
- [05-02.Manual Ack와 Offset Commit 정책](05-02.Manual%20Ack와%20Offset%20Commit%20정책.md) — Auto commit vs Manual ack의 본질적 차이, Spring Kafka ack-mode 7가지, Manual ack가 의미 있는 두 경우와 자동 ack로 충분한 경우의 결정 기준
- [05-03.Batch Listener와 부분 실패 처리](05-03.Batch%20Listener와%20부분%20실패%20처리.md) — 단건 vs Batch listener 비교, 부분 실패 처리 패턴 3가지(`BatchListenerFailedException` 등), TPS가 batch를 채택하지 않은 이유

### 06. Config 종합

- [06-01.message-lib config 5개 클래스 종합](06-01.message-lib%20config%205개%20클래스%20종합.md) — `KafkaDefaultsEnvironmentPostProcessor`/`KafkaErrorConfig`/`KafkaHeaderMapperConfig`/`KafkaJsonConsumerConfig`/`KafkaRetryTemplateConfig` 다섯 클래스의 기동 순서, 책임, 상호작용을 한 장으로. 2026-04 Redpanda v25.3 운영 주의점 포함

## 상위 문서와의 경계

| 상위 (`05_messaging/`) | 대응 spring/ 문서 |
|---|---|
| [02-04.EventEnvelope 적용](../02-04.EventEnvelope%20적용.md) | [01-01.CloudEventsHeaderInterceptor](01-01.CloudEventsHeaderInterceptor.md) |
| [03-01.토픽 디자인](../03-01.토픽%20디자인.md) | [01-02.TopicConfig와 파티션 설계](01-02.TopicConfig와%20파티션%20설계.md) |
| [02-03.Avro](../02-03.Avro.md) / [02-05.Avro 직렬화 예외처리 전략](../02-05.Avro%20직렬화%20예외처리%20전략.md) | [02-01.Avro Consumer 수신 패턴](02-01.Avro%20Consumer%20수신%20패턴.md) |
| [02-05.Avro 직렬화 예외처리 전략](../02-05.Avro%20직렬화%20예외처리%20전략.md) | [03-01.Spring Kafka DLT와 Producer Config](03-01.Spring%20Kafka%20DLT와%20Producer%20Config.md) / [03-02.DlqConsumer](03-02.DlqConsumer.md) |
| [02-04.EventEnvelope 적용](../02-04.EventEnvelope%20적용.md) | [04-01.trace-id와 traceparent](04-01.trace-id와%20traceparent.md) |
| [04-03.Consumer Group](../04-03.Consumer%20Group.md) | [05-01.Spring Kafka 운영 고급](05-01.Spring%20Kafka%20운영%20고급.md) |
| [02-05.Avro 직렬화 예외처리 전략](../02-05.Avro%20직렬화%20예외처리%20전략.md) + [03-04.한 토픽 다수 message 형태](../03-04.한%20토픽%20다수%20message%20형태.md) | [03-03.Kafka 예외 처리 통합](03-03.Kafka%20예외%20처리%20통합.md) |

원리·왜 필요한가는 상위에서, "현재 message-lib에서 어떻게 구현됐나"는 여기서.

## 코드 베이스 위치

`/Users/simbohyeon/okestro/tps-gitlab2/message-lib/src/main/java/org/okestro/tps/messaging/`

주요 패키지:

- `application/outbox/` — `EventPublisher`, `OutboxPoller`
- `domain/outbox/` — `OutboxEvent`, `OutboxStatus`, `OutboxRetryPolicy`
- `infrastructure/outbox/` — `OutboxAutoConfiguration`, `JpaOutboxEventRepository`, `OutboxMetrics`
- `config/` — `KafkaErrorConfig`, `KafkaJsonConsumerConfig`, `KafkaRetryTemplateConfig`, `KafkaDefaultsEnvironmentPostProcessor`, `KafkaHeaderMapperConfig` (다섯 클래스 종합은 [06-01](06-01.message-lib%20config%205개%20클래스%20종합.md))
- `serialization/` — `AvroSerializer`, `AvroSerializationException`
- `topic/` — `Topics` (enum), `TopicConfig`
- `tracing/` — `MessagingTracingAutoConfiguration`, `CorrelationIdRecordInterceptor`, `CorrelationIdContext`, `TraceContextUtil`
- `property/` — `OutboxProperties`, `TopicProperties`

문서별 본문에서 인용하는 클래스 경로가 위 패키지와 다르거나(예: 옛 `dlq/` 패키지) 클래스 자체가 사라진 경우, 해당 문서 상단의 ⚠️ 박스에 구체적 차이를 명시했다.

## 관련 문서

- [상위 MOC](../README.md)
- [Spring 통합 MOC](../../12_spring/README.md)
