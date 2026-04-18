# T1: Producer 전송 검증 테스트 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | CompletableFuture 결과를 동기적으로 검증하여 브로커 실제 저장 확인 |
| 파일 | `ProducerTest.java` |
| 테스트 | 전송 후 RecordMetadata(토픽, 파티션, offset) 검증 |
| 리뷰 결과 | APPROVE — HIGH 이슈 없음 |

---

## 왜 이렇게 구현했는가

### SendResult의 두 핵심 객체

`KafkaTemplate.send()`가 반환하는 `CompletableFuture<SendResult<K, V>>`가 완료되면 `SendResult` 객체를 얻는다. 이 객체는 두 핵심 정보를 담는다:

```java
SendResult<String, OrderEvent> result = future.get();

RecordMetadata metadata  = result.getRecordMetadata();  // 브로커 저장 결과
ProducerRecord<String, OrderEvent> record = result.getProducerRecord();  // 원본 메시지
```

| 객체 | 출처 | 담긴 정보 |
|------|------|---------|
| `RecordMetadata` | 브로커 ACK에서 추출 | 실제 저장된 토픽, 파티션 번호, offset, timestamp |
| `ProducerRecord` | Producer가 생성한 원본 | key, value, headers, 의도한 토픽/파티션 |

`RecordMetadata`의 값은 **브로커가 실제로 저장한 결과**이므로, 이것을 검증하면 "전송 성공 + 브로커 저장"까지 확인된다. `ProducerRecord`만 확인하면 "메시지를 만들었다"는 것만 알 수 있고 실제 전송 여부는 모른다.

### CompletableFuture.get()으로 비동기→동기 변환

프로덕션 코드에서 `send()`는 비동기로 동작해야 스루풋이 높다. 하지만 테스트에서는 검증 전에 전송이 완료되어 있어야 한다.

```java
// 테스트에서만 허용: future.get()으로 동기 대기
SendResult<String, OrderEvent> result = future.get(5, TimeUnit.SECONDS);
assertThat(result.getRecordMetadata().topic()).isEqualTo("orders");
```

`get()`은 완료될 때까지 현재 스레드를 블로킹한다. 타임아웃을 지정하지 않으면 브로커 문제 시 테스트가 무한 대기하므로 `get(timeout, unit)` 형태가 권장된다.

| 상황 | 권장 방식 | 이유 |
|------|----------|------|
| 프로덕션 코드 | `whenComplete()` 콜백 | 논블로킹, 스루풋 유지 |
| **테스트 코드** (현재) | `future.get(timeout, unit)` | 검증 전 완료 보장 |

### RecordMetadata로 토픽, 파티션, offset 검증

```java
RecordMetadata metadata = result.getRecordMetadata();

assertThat(metadata.topic()).isEqualTo("orders");
assertThat(metadata.partition()).isGreaterThanOrEqualTo(0);
assertThat(metadata.offset()).isGreaterThanOrEqualTo(0);
```

세 값의 의미:

- **topic**: 의도한 토픽에 실제로 저장됐는지 확인. 설정 오류 (토픽명 오타 등)를 잡는다.
- **partition**: 어느 파티션에 저장됐는지. orderId key 기반이므로 같은 key는 항상 같은 파티션이다. 파티셔너 동작을 검증할 수 있다.
- **offset**: 단조 증가하는 파티션 내 위치. 0 이상이면 브로커에 정상 기록된 것이다.

offset을 정확한 값으로 단언하지 않는 이유: 다른 테스트가 같은 토픽에 먼저 메시지를 보냈을 수 있어 offset 값이 테스트 실행 순서에 따라 달라진다. `isGreaterThanOrEqualTo(0)` 형태로 "유효한 offset"만 검증하는 것이 안정적이다.

### @DirtiesContext로 테스트 격리하는 이유

```java
@DirtiesContext
class ProducerTest extends AbstractKafkaTest {
    ...
}
```

`@DirtiesContext`는 테스트 클래스 실행 후 Spring ApplicationContext를 파기하고 다음 테스트를 위해 새로 생성하도록 지시한다.

Kafka 통합 테스트에서 격리가 필요한 이유:

1. **Consumer의 상태 오염**: 한 테스트에서 생성된 Consumer Group의 offset이 다음 테스트에 영향을 줄 수 있다.
2. **KafkaListenerContainerFactory 재사용**: 이전 테스트의 리스너가 살아있으면 다음 테스트가 받아야 할 메시지를 가로챌 수 있다.
3. **Testcontainers와의 조합**: `@DynamicPropertySource`로 설정된 브로커 주소가 컨텍스트마다 고정되므로, 컨텍스트가 재사용되면 잘못된 설정이 유지될 수 있다.

비용: 컨텍스트 재생성은 수 초가 걸리므로 꼭 필요한 테스트에만 적용한다.

---

## 핵심 학습 포인트

1. **SendResult = RecordMetadata + ProducerRecord** — 브로커 저장 결과와 원본 메시지 분리
2. **RecordMetadata = 브로커 ACK의 증거** — 토픽, 파티션, offset으로 실제 저장 검증
3. **future.get()은 테스트 전용** — 비동기를 동기로 변환, 프로덕션에서는 whenComplete 사용
4. **offset은 `>= 0`으로 검증** — 정확한 값 단언은 테스트 순서 의존성으로 불안정
5. **@DirtiesContext = 테스트 격리** — Kafka 통합 테스트에서 Consumer 상태 오염 방지
6. **타임아웃 지정 필수** — `get(5, TimeUnit.SECONDS)` 형태로 무한 대기 방지
