# Ch09 실습 #5: Kafka 트랜잭션 (CTP)

## 목적

Consume-Transform-Produce(CTP) 패턴이 SAGA Orchestrator에서 어떻게 동작하는지 이해하고, DB+Kafka 트랜잭션의 원자성 한계를 학습한다.

## 핵심 발견: TripKafkaConfig에 이미 CTP가 구현되어 있다

실습 #2에서 만든 TripKafkaConfig에 CTP의 모든 요소가 이미 포함되어 있다:

| 설정 | 빈 | 역할 |
|------|-----|------|
| `transactional.id prefix` | ch04ProducerFactory | Kafka 트랜잭션 활성화 |
| `enable.idempotence=true` | ch04ProducerFactory | PID+시퀀스로 중복 방지 |
| `KafkaTransactionManager` | ch04KafkaTransactionManager | 리스너에서 자동 TX 시작/커밋 |
| `isolation.level=read_committed` | ch04ConsumerFactory | abort된 메시지 필터링 |
| `AckMode.MANUAL` + TX Manager | ch04KafkaListenerContainerFactory | 오프셋을 TX에 포함 |

실습 #5의 본질은 "새 코드 작성"이 아니라 "이미 구성된 CTP가 어떻게 동작하는지 이해"하는 것이다.

---

## CTP 패턴 동작 원리

```
@KafkaListener 메서드 호출 시:
  1. KafkaTransactionManager가 Kafka TX 시작 (beginTransaction)
  2. 메시지 수신 (consume)
  3. 비즈니스 로직 실행 + DB 업데이트 (transform)
  4. kafkaTemplate.send() — 같은 TX에 포함 (produce)
  5. 정상 반환 → TX 커밋 (오프셋 + 발행 메시지)
  6. 예외 발생 → TX abort (오프셋 미커밋 + 메시지 미전달)
```

### 우리 Orchestrator에서의 CTP

```
onFlightBooked() 호출 시:
  beginTransaction()
    ├── FlightBooked 메시지 소비 (오프셋 기록)
    ├── SagaState DB 업데이트 (IN_PROGRESS)
    ├── BookHotelCommand Kafka 발행
    └── commitTransaction() ← 오프셋 + 메시지가 원자적으로 커밋
```

만약 `kafkaTemplate.send()` 후 커밋 전에 Orchestrator가 죽으면:
- Kafka TX가 abort됨
- 오프셋이 커밋되지 않음 → FlightBooked가 다시 수신됨
- BookHotelCommand가 `read_committed` Consumer에게 보이지 않음

---

## DB + Kafka 트랜잭션의 간극

### 문제: 두 트랜잭션은 독립적이다

```
@Transactional (Spring/JPA)        Kafka TX
  │                                  │
  ├── SagaState UPDATE               │
  ├── DB COMMIT ─────────────────── ✅│
  │                                  ├── kafkaTemplate.send()
  │                                  ├── KAFKA COMMIT ──── ❌ (실패!)
  │                                  │
  └── DB는 이미 커밋됨               └── Kafka는 abort
```

**결과**: DB에는 `IN_PROGRESS`로 기록됐지만, `BookHotelCommand`는 전달되지 않음. SAGA가 영원히 멈춤.

### 해결 방법 3단계

| 방식 | DB+Kafka 원자성 | 복잡도 | 적합 상황 |
|------|----------------|--------|----------|
| Kafka TX만 (CTP) | Kafka 내부만 보장 | 낮음 | Kafka-to-Kafka 변환 |
| DB TX + Kafka TX 체이닝 | 대부분 안전, 간극 존재 | 중간 | **현재 구현 (대부분의 SAGA)** |
| Transactional Outbox | 완벽한 원자성 | 높음 | 금융, 결제 등 크리티컬 |

현재 구현은 2번(체이닝)이다. 간극이 존재하지만, 실습 #6의 타임아웃 + 장애 복구 스케줄러가 이 간극을 보완한다. stalled SAGA를 감지하여 재전송하므로, 영원히 멈추는 것을 방지한다.

---

## 통합 테스트

`TripSagaIntegrationTest`로 CTP 동작을 End-to-End 검증한다:

| 테스트 | 시나리오 | 기대 결과 |
|--------|---------|----------|
| 정상 플로우 | ICN→NRT + Tokyo Hotel | COMPLETED, FLT-xxx, HTL-xxx |
| Step 1 실패 | departure="FAIL" | FAILED, 보상 없음 |
| Step 2 실패 + 보상 | hotelName="FAIL" | COMPENSATED, 항공 취소됨 |

테스트 인프라:
- **Redpanda**: Testcontainers (`v25.3.6`) — Schema Registry 내장
- **PostgreSQL**: Testcontainers JDBC URL (`jdbc:tc:postgresql:16:///saga`)
- **Awaitility**: 비동기 플로우 완료 대기 (최대 30초, 1초 간격 폴링)

---

## 생성된 파일

| 파일 | 역할 |
|------|------|
| `src/test/resources/application-test.yml` | 테스트 프로파일 설정 |
| `src/test/java/com/study/redpanda/ch04/TripSagaIntegrationTest.java` | 통합 테스트 3개 |

---

## 빌드 결과

`./gradlew compileTestJava` → **BUILD SUCCESSFUL**
