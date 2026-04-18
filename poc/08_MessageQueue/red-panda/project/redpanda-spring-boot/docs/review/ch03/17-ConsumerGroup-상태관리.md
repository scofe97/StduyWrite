# Consumer Group 상태(State) 관리

## 개요

Kafka/Redpanda 콘솔에서 Consumer Group 목록을 조회하면 각 그룹의 **상태(State)**가 표시된다. 테스트 환경에서 대부분 EMPTY로 보이는 이유와 각 상태의 의미를 정리한다.

---

## Consumer Group 상태 Lifecycle

```
[그룹 생성] → PreparingRebalance → CompletingRebalance → Stable
                                                           ↓
                                                    [Consumer 종료]
                                                           ↓
                                                         Empty
                                                           ↓
                                              [offsets.retention 초과]
                                                           ↓
                                                         Dead
```

| 상태 | 의미 | 발생 시점 |
|------|------|----------|
| **Stable** | 파티션 할당 완료, 정상 소비 중 | Consumer가 연결되어 메시지를 처리하는 중 |
| **PreparingRebalance** | 리밸런싱 시작, 기존 멤버에게 소비 중단 요청 | Consumer 추가/제거/장애 감지 시 |
| **CompletingRebalance** | 파티션 재할당 진행 중 | Group Coordinator가 새 할당 계획 배포 중 |
| **Empty** | 그룹 메타데이터는 존재하지만 멤버 0명 | Consumer가 모두 종료된 후 |
| **Dead** | 그룹 메타데이터까지 삭제됨 | `offsets.retention.minutes` 초과 후 자동 삭제 |
| **Unknown** | 상태를 알 수 없음 | 브로커 간 동기화 지연 등 예외 상황 |

---

## 테스트 환경에서 대부분 EMPTY인 이유

### 프로젝트 상황

Ch03 프로젝트에 **11개 `@KafkaListener`**가 있고, 각각 별도 consumer group을 등록한다:

```
pause-test-group, circuit-test-group, order-consumer-group,
batch-consumer-group, error-handler-group, retry-test-group,
sendto-test-group, idempotent-test-group, ...
```

### 실행 흐름

```
1. @SpringBootTest 시작
   → Spring Context 기동
   → 11개 @KafkaListener 빈 생성
   → 11개 consumer group 브로커에 등록
   → 각 그룹 Stable 상태

2. 테스트 실행
   → 해당 리스너만 메시지 처리
   → 나머지는 Stable이지만 idle

3. @DirtiesContext → Spring Context 파괴
   → 모든 consumer 연결 해제
   → 브로커에 group 메타데이터는 잔류
   → 멤버 0명 → 전부 EMPTY
```

### 핵심

**EMPTY = 그룹이 존재하지만 현재 연결된 consumer가 없는 상태**. 테스트가 끝나면 consumer가 모두 종료되므로 당연히 EMPTY가 된다. 그룹 메타데이터(offset 정보 포함)는 `offsets.retention.minutes`(기본 7일) 동안 유지된다.

---

## 실무에서의 의미

### EMPTY가 정상인 경우

- **테스트 환경**: 테스트 종료 후 consumer 미실행
- **배포 중 Rolling Restart**: 구 인스턴스 종료 → 신 인스턴스 기동 사이의 짧은 공백
- **배치 Consumer**: 스케줄에 따라 실행/종료 반복하는 consumer

### EMPTY가 문제인 경우

- **프로덕션 상시 운영 Consumer**: 항상 떠 있어야 하는 consumer가 EMPTY → consumer가 죽은 것
- **모니터링 알림 대상**: EMPTY 상태가 N분 이상 지속되면 알림 발송

### 모니터링 명령어

```bash
# Consumer Group 목록 및 상태 조회
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group <group-name>

# Redpanda (rpk)
rpk group list
rpk group describe <group-name>
```

### 상태별 대응

| 상태 | 프로덕션 대응 |
|------|-------------|
| Stable | 정상 — 모니터링만 |
| PreparingRebalance | 주시 — 장시간 지속 시 consumer 문제 조사 |
| CompletingRebalance | 주시 — 대규모 리밸런싱은 처리 지연 유발 |
| Empty | **알림** — 상시 운영 consumer가 Empty면 즉시 확인 |
| Dead | 정리 완료 — 필요 시 consumer 재기동 |

---

## C7(Consumer Pause)과의 관계

C7에서 학습한 `pause()`는 Consumer Group 상태를 **Stable로 유지**하면서 메시지 fetch만 중단하는 패턴이다.

| 동작 | Group 상태 | 파티션 소유권 |
|------|-----------|-------------|
| 정상 소비 | Stable | 유지 |
| `pause()` | **Stable** | **유지** |
| `stop()` | Empty (멤버 이탈) | 반납 → 리밸런싱 |
| Consumer 장애 | PreparingRebalance → Empty | 반납 → 리밸런싱 |

이것이 인프라 장애 시 `pause()`가 `stop()`보다 유리한 이유다. Group 상태가 Stable을 유지하므로 리밸런싱이 발생하지 않는다.
