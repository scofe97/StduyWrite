# Ch03 전체 테스트 Codex 교차 리뷰

## 개요

| 항목 | 내용 |
|------|------|
| 리뷰 대상 | Ch03 테스트 13개 (C7/C8 제외 — 별도 리뷰 완료) |
| 리뷰어 | Codex (GPT-5.3) |
| 리뷰 방식 | 2개 배치 병렬 실행 |
| 결과 | High 6건, Medium 6건, Low 2건 |

---

## 배치 구성

| 배치 | 파일 |
|------|------|
| Batch 1 | ProducerTest, ConsumerTest, BatchConsumerTest, ErrorHandlerTest, RetryableTopicTest, IdempotentConsumerTest |
| Batch 2 | IdempotentProducerTest, PartitionRoutingTest, SendToConsumerTest, EnhancedKafkaTemplateTest, PerformanceTuningTest |

---

## High (6건)

### 1. BatchConsumerTest — 배치 의도 미검증

`BatchConsumerTest.java:56`에서 `messageCount=20`을 보내지만, latch를 `1`로 설정하고 `>=1`만 단언하여 **1건만 처리되어도 통과**한다.

**문제**: 배치 Consumer의 핵심 동작(다수 메시지를 한 번에 처리)을 검증하지 못함.

### 2. ConsumerTest — 멀티스레드 공유 필드 경합

`concurrency=3` 환경에서 `lastReceived*` 단일 필드로 검증한다. 리스너가 병렬 처리 중이면 마지막 write가 덮여 **다른 메시지 상태를 읽을 수 있다**.

**문제**: 경쟁 상황에서 false positive/negative 발생 가능.

### 3. EnhancedKafkaTemplateTest — 잘못된 메서드 호출

`EnhancedKafkaTemplateTest.java:85` — 테스트명은 "래퍼 없이 직접 전송"인데, 실제로는 다시 `enhancedKafkaTemplate.send()`를 호출한다.

**문제**: 의도한 비교 케이스가 실행되지 않아 핵심 요구사항 미검증.

### 4. EnhancedKafkaTemplateTest — orderId 단언 누락

`EnhancedKafkaTemplateTest.java:98` — 수신 메시지가 방금 보낸 이벤트인지 식별하지 않는다. `correlationId != null`만으로 통과.

**문제**: 이전/다른 메시지로 latch가 내려가도 통과하는 false-positive 위험.

### 5. SendToConsumerTest — volatile 미적용

`SendToConsumerTest.java:37,83` — `latch`, `last*Event` 필드에 동기화/volatile 보호 없이 리스너 스레드와 테스트 스레드가 공유한다.

**문제**: 가시성 이슈로 간헐 실패 가능 (C7/C8에서 동일 이슈 수정 완료).

### 6. 테스트 격리 부족 (공통)

6개 테스트 모두 `AbstractLocalKafkaTest` 기반인데 토픽/컨슈머 그룹 격리 로직이 없다. 잔여 메시지가 다른 테스트에 영향.

**문제**: 환경 상태에 따라 결과 변동, CI에서 flaky.

---

## Medium (6건)

### 1. ErrorHandlerTest / RetryableTopicTest — DLT null 체크 누락

`getLastDltEvent()` null 체크 없이 바로 `getOrderId()` 호출. 타임아웃 시 assertion 실패 대신 NPE로 깨짐.

### 2. ProducerTest — 비동기 테스트의 동기 실행

`ProducerTest.java:53-57` — 매 전송마다 `future.get()` 즉시 호출로 사실상 동기 테스트. 테스트명/주석과 실제 동작 불일치.

### 3. IdempotentConsumerTest — 핵심 단언 부족

count 위주 검증으로 "정확히 어떤 eventId가 처리/중복되었는지" 보장하지 못함.

### 4. IdempotentProducerTest — acks 검증 약함

주석은 `acks=all` 필수라고 설명하지만 실제로는 `acks` non-null만 확인. 잘못된 설정도 통과 가능.

### 5. PerformanceTuningTest — 타입 불일치

`linger.ms`를 문자열 `"10"`으로 비교. Spring/Kafka 버전에 따라 `Integer`로 들어오면 brittle.

### 6. PartitionRoutingTest — 파티션 하드코딩

파티션 수를 `0..2`로 하드코딩. 토픽 파티션 수 변경 시 로직은 맞아도 테스트 실패.

---

## Low (2건)

### 1. 고정 타임아웃 패턴

6개 이상 테스트에서 `latch.await(30, SECONDS)` 고정 대기. Awaitility 조건 기반 polling 미사용으로 CI 부하 시 flaky 증가.

### 2. IdempotentProducerTest — 미사용 필드

`kafkaTemplate` 필드가 선언만 되고 사용되지 않음. 코드 노이즈.

---

## 공통 관찰

### AbstractLocalKafkaTest와 Testcontainers

Codex가 "Testcontainers 기반이라 했는데 실제로는 local profile"이라고 지적했으나, 실제로 `AbstractLocalKafkaTest`는 **Testcontainers로 Redpanda 컨테이너를 띄우는** 베이스 클래스다. "local"은 외부 클러스터가 아닌 테스트 로컬 컨테이너라는 의미이므로, 이 지적은 컨텍스트 부족에 의한 **오진**이다.

다만 **토픽/그룹 격리 부재**라는 근본 지적은 유효하다. `@DirtiesContext`로 컨텍스트를 매번 재생성하여 완화하고 있지만, 동일 컨텍스트 내 테스트 간 격리는 보장되지 않는다.

### 학습 프로젝트 맥락

이 프로젝트는 **학습 PoC**이므로:
- 프로덕션 수준의 테스트 격리/동시성 안전성을 모두 구현할 필요는 없음
- 다만 이 리뷰를 통해 **실무에서 주의할 패턴을 인지**하는 것이 목적

---

## Claude vs Codex 비교 (전체 테스트 리뷰)

| 포인트 | Claude | Codex |
|--------|--------|-------|
| BatchConsumer 약한 단언 | 미지적 | **High로 지적** |
| ConsumerTest 스레드 안전성 | 지적 | **High로 지적** |
| EnhancedKafkaTemplate 잘못된 메서드 | 미지적 | **High로 지적** |
| SendToConsumer volatile 누락 | 지적 (C7/C8 동일 패턴) | **High로 지적** |
| 테스트 격리 부족 | 지적 | **High로 지적** |
| DLT null 체크 | 미지적 | Medium으로 지적 |
| 비동기 테스트 동기 실행 | 미지적 | Medium으로 지적 |
| AbstractLocalKafkaTest 오진 | 정확히 이해 | **컨텍스트 부족으로 오진** |

---

## 핵심 학습 포인트

1. **volatile/동기화** — 멀티스레드 Consumer 테스트에서 공유 필드는 반드시 volatile 또는 Atomic
2. **단언 강도** — count만 확인하면 "어떤 메시지가 처리되었는지" 보장 불가, ID 기반 검증 필요
3. **테스트 격리** — 고정 group/topic은 잔여 메시지 간섭 위험, 랜덤 suffix 또는 `@DirtiesContext` 활용
4. **Awaitility** — 고정 timeout보다 조건 기반 polling이 CI에서 안정적
5. **교차 검증** — Claude가 놓친 EnhancedKafkaTemplate 버그를 Codex가 발견. 독립 AI 리뷰의 가치 확인
