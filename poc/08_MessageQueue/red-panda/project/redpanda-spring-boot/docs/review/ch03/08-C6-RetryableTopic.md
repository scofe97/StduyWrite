# C6: @RetryableTopic 논블록킹 재시도 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | 재시도 토픽 기반 논블록킹 재시도로 원본 토픽 처리를 차단하지 않는 에러 핸들링 |
| 파일 | `RetryableConsumer.java`, `RetryableTopicTest.java`, `KafkaTopicConfig.java` |
| 테스트 | 2개 (재시도 소진 후 DLT 전송, 정상 처리 시 재시도 미발생) |

---

## 왜 이렇게 구현했는가

### C5(DefaultErrorHandler)와 C6(@RetryableTopic)의 핵심 차이

두 방식 모두 "재시도 후 DLT 전송"이라는 결과는 같지만, **재시도가 일어나는 위치**가 다르다.

| | C5: DefaultErrorHandler | C6: @RetryableTopic |
|---|---|---|
| 재시도 위치 | Consumer 메모리 (in-memory) | 별도 재시도 토픽 |
| 파티션 블록킹 | O — 재시도 중 다른 메시지 대기 | X — 원본 토픽 계속 처리 |
| 토픽 메시지 수 | 원본 1건 + DLT 1건 | 원본 1건 + retry-0 1건 + retry-1 1건 + DLT 1건 |
| DLT 수신 방식 | 별도 `@KafkaListener(topics = "...-dlt")` | 같은 클래스의 `@DltHandler` |
| 설정 방식 | `@Bean DefaultErrorHandler` | `@RetryableTopic` 어노테이션 |
| 토픽 생성 | 수동 (NewTopic 빈) | `autoCreateTopics = "true"`로 자동 |

### 논블록킹이 중요한 이유

C5의 블록킹 재시도에서는 재시도 중 해당 파티션의 **다른 정상 메시지도 처리되지 못한다.** 파티션에 1만 건이 쌓여 있고 첫 번째 메시지가 3회 재시도(1초 x 2)를 한다면, 나머지 9,999건은 최소 2초를 대기한다.

C6은 실패 메시지를 retry 토픽으로 보내고 즉시 다음 메시지를 처리하므로, 정상 메시지의 처리량에 영향이 없다.

### @RetryableTopic이 생성하는 토픽 구조

```
chapter2.retryable-test              ← 원본
chapter2.retryable-test-retry-0      ← 1초 후 재시도 (자동 생성)
chapter2.retryable-test-retry-1      ← 2초 후 재시도 (자동 생성)
chapter2.retryable-test-dlt          ← 최종 DLT (자동 생성)
```

`topicSuffixingStrategy = SUFFIX_WITH_INDEX_VALUE`로 `-retry-0`, `-retry-1` 형태를 사용한다. 다른 전략으로 `SUFFIX_WITH_DELAY_VALUE`를 쓰면 `-retry-1000`, `-retry-2000`처럼 지연시간이 접미사가 된다.

### @DltHandler의 에러 헤더 활용

Spring Kafka는 DLT 전송 시 에러 정보를 메시지 헤더에 자동 포함한다. 별도 설정 없이 `@Header`로 추출 가능하다.

| 헤더 | 내용 |
|------|------|
| `kafka_dlt-exception-fqcn` | 예외 클래스명 |
| `kafka_dlt-exception-message` | 에러 메시지 |
| `KafkaHeaders.ORIGINAL_TOPIC` | 원본 토픽 |
| `KafkaHeaders.ORIGINAL_OFFSET` | 원본 offset |

운영에서는 이 헤더를 추출해 DB에 저장하면 모니터링/재처리가 가능하다.

### 자동 생성 토픽의 파티션 설정

`@RetryableTopic`으로 자동 생성되는 retry/DLT 토픽의 기본 파티션 수는 **1**이다. 변경 방법은 3가지가 있다.

**방법 1: 어노테이션 개별 설정**

```java
@RetryableTopic(
    autoCreateTopics = "true",
    numPartitions = "3",           // 기본값 1 → 3으로 변경
    replicationFactor = "1"
)
```

모든 재시도/DLT 토픽에 동일하게 적용된다. 토픽별로 다른 파티션 수가 필요하면 `autoCreateTopics = "false"`로 끄고 NewTopic 빈으로 수동 등록한다.

**방법 2: RetryTopicConfiguration 빈 (글로벌 기본값)**

어노테이션 대신 빈으로 정의하면 앱 전체의 기본값으로 동작한다.

```java
@Bean
public RetryTopicConfiguration retryTopicConfiguration(KafkaTemplate<String, ?> template) {
    return RetryTopicConfigurationBuilder
            .newInstance()
            .fixedBackOff(1000)
            .maxAttempts(3)
            .autoCreateTopicsWith(3, (short) 1)  // 파티션 3, 리플리카 1
            .create(template);
}
```

`@RetryableTopic` 어노테이션과 병행 시, 어노테이션이 개별 오버라이드가 된다.

**방법 3: 브로커 기본값 변경**

Redpanda/Kafka 브로커의 `num.partitions` 설정을 변경하면, 파티션 수를 지정하지 않은 모든 자동 생성 토픽에 적용된다.

```bash
rpk cluster config set default_topic_partitions 3
```

| 방식 | 범위 | 적합한 경우 |
|------|------|------------|
| 어노테이션 `numPartitions` | 개별 리스너 | 리스너별 세밀 제어 |
| `RetryTopicConfiguration` 빈 | Spring 앱 전체 | 앱 내 일관된 기본값 |
| 브로커 `num.partitions` | 브로커 전체 | 인프라 레벨에서 일괄 설정 |

### 어떤 상황에 어떤 방식을 선택하는가

| 상황 | 권장 방식 | 이유 |
|------|----------|------|
| 짧은 재시도 (1-2회), 순서 보장 필요 | C5 (DefaultErrorHandler) | 파티션 내 순서가 유지됨 |
| 긴 재시도, 처리량 우선 | **C6 (@RetryableTopic)** | 원본 토픽 블록 없음 |
| 외부 서비스 장애 (수 초~수 분 대기) | C6 + exponential backoff | 대기 중 다른 메시지 계속 처리 |

---

## 핵심 학습 포인트

1. **논블록킹 재시도** — 실패 메시지를 별도 토픽으로 이동, 원본 토픽 처리 계속 진행
2. **@DltHandler** — 같은 클래스 내에서 자동 연결, 별도 @KafkaListener 불필요
3. **에러 헤더 자동 포함** — 예외 클래스, 메시지, 원본 토픽/offset이 DLT 메시지 헤더에 포함
4. **토픽 자동 생성** — retry/DLT 토픽을 `autoCreateTopics = "true"`로 자동 관리
5. **C5와의 트레이드오프** — 블록킹(순서 보장) vs 논블록킹(처리량), 상황에 따라 선택

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | Medium | `getLastDltEvent()` null 체크 없이 바로 `getOrderId()` 호출 | 타임아웃 시 assertion 실패 대신 NPE로 깨져 원인 파악 어려움 |
