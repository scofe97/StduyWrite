# Issue #002: SchemaRegistryStrategyTest 예외 타입 불일치

## 증상

```
java.lang.AssertionError:
Expecting actual throwable to be an instance of:
  java.util.concurrent.ExecutionException
but was:
  org.apache.kafka.common.errors.SerializationException: Error retrieving Avro schema...
```

`SchemaRegistryStrategyTest.자동등록_비활성화_시_미등록_스키마로_전송하면_실패한다()` 테스트에서 `ExecutionException`을 기대했지만, 실제로는 `SerializationException`이 발생.

## 원인

`KafkaAvroSerializer`의 직렬화 시점 문제.

### 예상한 동작 (틀림)

```
template.send() → Future 생성 → 비동기 전송 → Future.get()에서 ExecutionException 래핑
```

테스트는 `Future.get()`이 `ExecutionException`으로 래핑된 예외를 던질 것으로 가정했다.

### 실제 동작

```
template.send() → KafkaAvroSerializer.serialize() 호출 → Schema Registry 조회 실패
→ SerializationException 즉시 발생 (Future.get()까지 도달하지 않음)
```

`KafkaAvroSerializer`는 `send()` 호출 시 **동기적으로** 직렬화를 수행한다. Schema Registry에서 스키마를 조회하는 HTTP 호출도 이 시점에 발생한다. `auto.register.schemas=false` 상태에서 미등록 subject를 조회하면 `RestClientException`이 발생하고, 이것이 `SerializationException`으로 래핑되어 `send()` 자체에서 던져진다.

즉, `Future`가 만들어지기 전에 예외가 발생하므로 `Future.get()`의 `ExecutionException` 래핑이 적용되지 않는다.

### 왜 동기적인가?

Kafka Producer의 `send()` 내부 흐름:

1. **직렬화** (동기) — Key/Value를 바이트로 변환
2. **파티셔닝** (동기) — 대상 파티션 결정
3. **RecordAccumulator에 추가** (동기) — 배치 버퍼에 적재
4. **네트워크 전송** (비동기) — Sender 스레드가 브로커로 전송

직렬화(1단계)에서 실패하면 2~4단계에 도달하지 않으므로, `Future` 자체가 생성되지 않고 예외가 호출 스레드에서 즉시 전파된다.

## 수정

```java
// Before: ExecutionException만 기대
.isInstanceOf(ExecutionException.class)

// After: 두 가지 모두 허용
.isInstanceOfAny(
        ExecutionException.class,
        org.apache.kafka.common.errors.SerializationException.class
)
```

`isInstanceOfAny`로 변경하여, 직렬화 시점에서 동기적으로 던져지는 `SerializationException`과 (혹시 비동기 경로를 타는 경우의) `ExecutionException` 모두 수용한다.

또한 `.hasMessageContaining("not found")` 조건을 제거했다. `SerializationException`의 메시지는 "Error retrieving Avro schema..."로, "not found"는 `rootCause`인 `RestClientException`에만 포함되어 있기 때문이다. `rootCause` 체인에서 `RestClientException` 타입 검증으로 충분하다.

## 핵심 학습 포인트

- Kafka Producer의 `send()`는 "완전히 비동기"가 아니다. 직렬화와 파티셔닝은 **호출 스레드에서 동기적으로** 실행된다.
- Schema Registry 조회도 직렬화 단계에서 발생하므로, Registry 관련 에러는 `Future.get()`이 아닌 `send()` 호출 시점에서 발생할 수 있다.
- 테스트에서 예외 타입을 검증할 때, 동기/비동기 경계를 고려해야 한다.

## 관련

- `SchemaRegistryStrategyTest.java` line 76~97
- Issue #001과 무관 (빈 주입 문제가 아닌 테스트 assertion 문제)
