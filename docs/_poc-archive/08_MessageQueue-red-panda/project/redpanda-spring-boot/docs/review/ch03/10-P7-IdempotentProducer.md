# P7: Idempotent Producer 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | 브로커 레벨에서 PID+시퀀스 기반 Producer 중복 전송 방어 |
| 파일 | `application.yml` (설정 추가), `IdempotentProducerTest.java` |
| 테스트 | 2개 (설정 검증, 정상 전송) |

---

## 왜 이렇게 구현했는가

### Idempotent Producer의 동작 원리

`enable.idempotence=true` 설정 시 Producer는 브로커로부터 **PID(Producer ID)**를 할당받고, 각 메시지에 **시퀀스 번호**를 부여한다. 브로커는 (PID, 파티션, 시퀀스) 조합으로 중복을 감지한다.

```
Producer (PID=100)
  메시지1: seq=0 → 브로커 저장 (OK)
  메시지2: seq=1 → 브로커 저장 (OK)
  메시지2: seq=1 → 네트워크 재시도 → 브로커가 중복 감지 → 무시 (ACK 반환)
```

### 필수 조건 3가지

| 설정 | 값 | 이유 |
|------|-----|------|
| `enable.idempotence` | `true` | 멱등성 활성화 |
| `acks` | `all` | 모든 ISR 복제본이 저장 확인해야 시퀀스 추적 가능 |
| `max.in.flight.requests.per.connection` | `≤ 5` | 6 이상이면 순서 역전 가능 → 시퀀스 검증 불가 |

Kafka 3.x에서 `enable.idempotence=true`가 기본값이고 `acks=all`도 강제되지만, **명시적으로 선언**하는 것이 운영 투명성과 학습 목적에 적합하다.

### PID 변경과 한계

| 시나리오 | PID | 중복 방어 |
|---------|-----|----------|
| 네트워크 재시도 (같은 세션) | 동일 | **방어** |
| Producer 재시작 | **변경** | 방어 불가 |
| 다른 Producer 인스턴스 | 다른 PID | 방어 불가 |

PID는 Producer가 브로커에 연결할 때마다 새로 할당된다. 따라서 Producer 재시작 후 같은 메시지를 다시 보내면 브로커는 다른 Producer로 인식하여 중복 저장한다. 이것이 **Consumer 측 dedup(C9)이 필요한 이유**이다.

### 설정만 추가하고 코드 변경 없는 이유

Idempotent Producer는 **KafkaProducer 내부에서 투명하게 동작**한다. 애플리케이션 코드에서 PID나 시퀀스를 직접 다루지 않는다. `KafkaTemplate.send()`는 동일하게 사용하되, 내부적으로 시퀀스 번호가 자동 부여된다.

---

## 핵심 학습 포인트

1. **설정 한 줄** — `enable.idempotence=true`로 네트워크 레벨 중복 방어 (비용 거의 없음)
2. **PID+시퀀스** — 브로커가 (PID, 파티션, 시퀀스)로 중복 감지, 앱 코드 변경 불필요
3. **acks=all 강제** — 멱등성은 모든 ISR 복제본 확인이 전제
4. **max.in.flight ≤ 5** — 6 이상이면 순서 역전으로 시퀀스 검증 불가
5. **PID 재시작 시 변경** — 앱 레벨 중복은 Consumer dedup(C9)으로 보완 필요
6. **P7 + C9 = 완전한 멱등성** — Producer(네트워크) + Consumer(앱) 양쪽 방어가 정석

---

## 실습 중 발견한 포인트

### "enable.idempotence=true인데 왜 토픽에 중복이 쌓이나?"

IdempotentConsumerTest에서 같은 eventId로 `send()`를 2번 호출하면, 토픽에 2건이 모두 저장된다.

이유: **각 `send()` 호출마다 새로운 시퀀스 번호가 부여**되기 때문이다. 브로커는 페이로드(eventId)를 보지 않고 (PID, 파티션, 시퀀스) 조합으로만 중복을 판단한다.

| 상황 | 시퀀스 | 브로커 판단 | 결과 |
|------|--------|-----------|------|
| 네트워크 재시도 (같은 send의 자동 재전송) | 같은 seq | 중복 | 무시 |
| 앱에서 send() 2번 호출 | 다른 seq | 신규 | 둘 다 저장 |

결론: Producer 멱등성은 KafkaProducer 내부의 네트워크 레벨 재시도만 방어한다. 애플리케이션이 의도적으로(또는 재시작으로) `send()`를 2번 호출하는 것은 방어하지 못한다. 이것이 Consumer 측 dedup(C9)이 필요한 근본적인 이유다.

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | Medium | 주석은 `acks=all` 필수라고 설명하지만 실제로는 `acks` non-null만 확인 | 잘못된 설정도 통과 가능 |
| 2 | Medium | "Idempotent Producer 정상 동작" 테스트가 단일 전송 성공만 확인 — 중복 억제(멱등성) 동작 자체 미검증 | 테스트 이름 대비 단언 부족 |
| 3 | Low | `kafkaTemplate` 필드가 선언만 되고 사용되지 않음 | 코드 노이즈 |
