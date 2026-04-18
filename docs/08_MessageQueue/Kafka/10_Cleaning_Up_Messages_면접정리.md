# Chapter 10: 메시지 정리 (Cleaning Up Messages) - 면접 심화 정리

---

## 1. Log Retention: 시간과 크기 기반 데이터 정리

### 1.1 Retention의 기본 원리

Kafka에서 Log Retention은 데이터 보존 기간 또는 저장 용량을 기준으로 오래된 세그먼트를 삭제하는 메커니즘입니다. 이 메커니즘을 정확히 이해하려면 먼저 Kafka가 데이터를 어떻게 저장하는지 알아야 합니다.

Kafka의 파티션은 여러 개의 세그먼트 파일로 구성됩니다. 각 세그먼트는 `.log`, `.index`, `.timeindex` 파일의 집합이며, Kafka는 항상 가장 최신 세그먼트(Active Segment)에만 새 메시지를 추가합니다. Retention 정책은 이 Active Segment를 제외한 나머지 세그먼트들을 대상으로 적용됩니다.

```
파티션 디렉토리 구조
├── 00000000000000000000.log        # 세그먼트 1 (삭제 대상 검토)
├── 00000000000000000000.index
├── 00000000000000000000.timeindex
├── 00000000000000052000.log        # 세그먼트 2 (삭제 대상 검토)
├── 00000000000000052000.index
├── 00000000000000052000.timeindex
└── 00000000000000104000.log        # Active 세그먼트 (삭제 불가)
    ...
```

Retention 검사는 `log.retention.check.interval.ms`(기본값 5분)마다 실행되며, 세그먼트의 가장 최신 메시지 타임스탬프가 `retention.ms`를 초과했거나, 파티션 전체 크기가 `retention.bytes`를 초과한 경우 해당 세그먼트가 삭제 대상이 됩니다.

중요한 점은 Retention이 메시지 단위가 아니라 세그먼트 단위로 동작한다는 것입니다. 세그먼트 내의 가장 최신 메시지가 기준이 되므로, 세그먼트 크기나 롤링 주기에 따라 실제 삭제 시점이 달라질 수 있습니다.

### 1.2 규정 준수를 위한 정확한 삭제 시점 계산

GDPR이나 금융 규정처럼 데이터 보존 기간이 법적으로 정해진 경우, 정확한 삭제 시점을 보장해야 합니다. 이를 위해서는 다음 공식을 이해해야 합니다.

```
최대 보존 기간 = segment.ms + retention.ms + log.retention.check.interval.ms
```

예를 들어, 7일 이내에 모든 데이터를 삭제해야 한다면:

```
segment.ms        = 86,400,000 (1일)
retention.ms      = 515,700,000 (약 5일 23시간 55분)
check.interval    = 300,000 (5분)
─────────────────────────────────────────────────
합계              ≈ 604,800,000 (7일)
```

이 설정에서 메시지의 생명주기는 다음과 같습니다. 메시지가 생성되면 현재 Active 세그먼트에 저장됩니다. 1일 후 새로운 세그먼트가 생성되고 기존 세그먼트는 비활성화됩니다. 약 5일 23시간 55분이 지나면 해당 세그먼트가 삭제 대상으로 표시됩니다. 다음 체크 주기(최대 5분 후)에 실제로 삭제됩니다. 따라서 메시지 생성부터 삭제까지 최대 7일이 소요됩니다.

### 1.3 Offset Retention과 Consumer Group 관리

메시지 Retention과 별개로, Consumer Group의 오프셋도 정리 대상입니다. `offsets.retention.minutes`(기본값 7일)이 지나면 비활성 Consumer Group의 커밋된 오프셋이 삭제됩니다. 비활성이란 그룹 내 어떤 Consumer도 연결되어 있지 않고 커밋도 발생하지 않는 상태를 의미합니다.

이 설정을 너무 짧게 하면 장기 유지보수나 버그 수정으로 Consumer가 일시 중단된 후 재시작할 때 문제가 발생합니다. 오프셋이 삭제되어 처음부터 다시 소비하거나, 최신 메시지부터 소비하게 되어 데이터 누락이나 중복 처리가 발생할 수 있습니다.

---

## 2. Log Compaction: 키 기반 최신 상태 유지

### 2.1 Compaction의 핵심 개념과 동작 원리

Log Compaction은 Retention과 전혀 다른 접근 방식으로 데이터를 정리합니다. Retention이 시간이나 크기를 기준으로 전체 세그먼트를 삭제하는 반면, Compaction은 각 키(Key)의 최신 메시지만 유지하고 이전 메시지들을 삭제합니다. 이는 Kafka를 상태 저장소(State Store)로 사용할 때 핵심적인 기능입니다.

Compaction 전후의 데이터 변화를 살펴보면:

```
Compaction 전:
Offset 0: Key=user-1, Value={"name":"Alice", "age":25}
Offset 1: Key=user-2, Value={"name":"Bob", "age":30}
Offset 2: Key=user-1, Value={"name":"Alice", "age":26}  ← user-1 업데이트
Offset 3: Key=user-3, Value={"name":"Charlie", "age":35}
Offset 4: Key=user-1, Value={"name":"Alice", "age":27}  ← user-1 재업데이트

Compaction 후:
Offset 1: Key=user-2, Value={"name":"Bob", "age":30}
Offset 3: Key=user-3, Value={"name":"Charlie", "age":35}
Offset 4: Key=user-1, Value={"name":"Alice", "age":27}  ← 최신 상태만 유지
```

여기서 중요한 두 가지 특성이 있습니다. 첫째, 오프셋 순서는 유지됩니다. 삭제된 오프셋(0, 2)은 건너뛰지만 남은 메시지들의 상대적 순서는 변하지 않습니다. 둘째, Compaction은 Active 세그먼트에는 적용되지 않습니다. 현재 쓰기가 진행 중인 세그먼트는 항상 Compaction 대상에서 제외됩니다.

### 2.2 Log Cleaner의 내부 동작

Compaction을 실행하는 것은 Log Cleaner라는 백그라운드 스레드입니다. Log Cleaner는 다음과 같은 과정으로 동작합니다.

첫째, Offset Map 구축 단계입니다. Dirty 세그먼트(아직 Compaction되지 않은 세그먼트)를 스캔하여 각 키의 최신 오프셋을 메모리에 저장합니다. 이 맵은 `log.cleaner.dedupe.buffer.size`(기본값 128MB) 크기의 버퍼에 저장되며, 키당 약 24바이트를 사용하므로 약 500만 개의 고유 키를 처리할 수 있습니다.

둘째, 세그먼트 재작성 단계입니다. 세그먼트를 처음부터 읽으면서 Offset Map에서 해당 키의 최신 오프셋과 비교합니다. 최신 오프셋과 일치하면 새 세그먼트에 복사하고, 그렇지 않으면 건너뜁니다.

셋째, 세그먼트 교체 단계입니다. 새로 생성된 세그먼트로 기존 세그먼트를 원자적으로 교체합니다. 이 과정은 읽기 요청에 영향을 주지 않도록 설계되어 있습니다.

### 2.3 Compaction 트리거 조건의 이해

Compaction이 실행되는 조건은 두 가지입니다.

첫 번째는 Dirty Ratio 기반 트리거입니다. `min.cleanable.dirty.ratio`(기본값 0.5)는 전체 로그 중 Dirty 세그먼트의 비율이 이 값을 초과하면 Compaction을 시작합니다. 여기서 Dirty 세그먼트란 아직 Compaction이 적용되지 않은 세그먼트를 의미합니다. 이 값을 낮추면 더 자주 Compaction이 실행되어 디스크 사용량은 줄지만 CPU와 I/O 부하가 증가합니다.

두 번째는 시간 기반 강제 트리거입니다. `max.compaction.lag.ms`가 설정된 경우, Dirty Ratio와 관계없이 해당 시간이 지난 메시지가 있으면 Compaction이 강제로 실행됩니다. 이는 트래픽이 적은 토픽에서도 Compaction이 실행되도록 보장합니다.

추가로 `min.compaction.lag.ms`는 최소 보존 기간을 설정합니다. 이 시간이 지나지 않은 메시지는 Compaction 대상에서 제외됩니다. 이는 최근 변경 이력을 보존해야 하는 경우에 유용합니다.

### 2.4 존재하지 않는 오프셋 요청 처리

Compaction으로 중간 오프셋이 삭제된 상태에서 Consumer가 해당 오프셋을 요청하면 어떻게 될까요? Kafka는 요청한 오프셋보다 크거나 같은 가장 작은 유효 오프셋의 메시지를 반환합니다. 예를 들어, 오프셋 0, 2가 삭제된 상태에서 오프셋 0을 요청하면 오프셋 1의 메시지가 반환됩니다.

이 동작은 Consumer가 중단 후 재시작할 때 중요합니다. 마지막으로 커밋한 오프셋이 Compaction으로 삭제되었더라도, Consumer는 자동으로 다음 유효한 메시지부터 처리를 재개할 수 있습니다.

---

## 3. Tombstone: 선택적 데이터 삭제

### 3.1 Tombstone의 개념과 필요성

Tombstone은 null 값을 가진 특수한 메시지입니다. Compaction 토픽에서 특정 키의 데이터를 완전히 삭제하고 싶을 때 사용합니다. 일반 Compaction에서는 각 키의 최신 메시지가 항상 유지되지만, Tombstone을 보내면 해당 키의 모든 데이터가 최종적으로 삭제됩니다.

```
Tombstone 처리 과정:

1. Key=user-1에 대한 Tombstone(Value=null) 발행
2. 첫 번째 Compaction: user-1의 이전 메시지들 삭제, Tombstone은 유지
3. delete.retention.ms(기본값 1일) 경과
4. 두 번째 Compaction: Tombstone 자체도 삭제
5. Key=user-1은 토픽에서 완전히 사라짐
```

Tombstone이 즉시 삭제되지 않고 `delete.retention.ms` 동안 유지되는 이유가 있습니다. Compaction 토픽을 소비하는 Consumer가 삭제 이벤트를 처리할 시간이 필요하기 때문입니다. 예를 들어, Kafka 토픽을 소스로 사용하는 애플리케이션이 있다면, Tombstone을 받아서 자신의 로컬 상태에서도 해당 키를 삭제할 수 있어야 합니다.

### 3.2 Tombstone 실무 활용 패턴

GDPR의 잊힐 권리(Right to be Forgotten) 구현에서 Tombstone은 핵심적인 역할을 합니다. 사용자가 데이터 삭제를 요청하면, 해당 사용자 ID를 키로 하는 모든 토픽에 Tombstone을 발행합니다.

```
사용자 삭제 요청 처리 흐름:

1. 삭제 요청 수신: user-12345 삭제 요청
2. 관련 토픽 식별: user-profiles, user-activities, user-preferences
3. 각 토픽에 Tombstone 발행:
   - user-profiles: Key=user-12345, Value=null
   - user-activities: Key=user-12345, Value=null
   - user-preferences: Key=user-12345, Value=null
4. 하위 시스템들이 Tombstone을 소비하여 자신의 저장소에서도 삭제
5. delete.retention.ms 후 Tombstone 자체 삭제
```

---

## 4. Delete와 Compact의 조합

### 4.1 두 정책의 조합이 필요한 상황

`cleanup.policy=delete,compact`로 두 정책을 함께 적용할 수 있습니다. 이는 다음과 같은 요구사항이 있을 때 유용합니다.

- 각 키의 최신 상태만 유지하면서(Compact)
- 일정 기간이 지난 데이터는 삭제(Delete)

예를 들어, 고객 정보를 저장하는 토픽에서 30일간 활동이 없는 고객 데이터를 삭제하되, 활동 중인 고객은 항상 최신 상태를 유지해야 하는 경우입니다.

```
설정 예시:
cleanup.policy=delete,compact
retention.ms=2592000000 (30일)
min.cleanable.dirty.ratio=0.5

동작 방식:
1. Compaction: 각 고객의 최신 상태만 유지
2. Retention: 30일 이상 된 세그먼트 삭제
3. 결과: 30일 내 업데이트된 고객의 최신 상태만 토픽에 존재
```

### 4.2 주의사항

두 정책을 함께 사용할 때 몇 가지 주의점이 있습니다. Retention은 세그먼트 단위로 동작하므로, 오래된 키라도 같은 세그먼트에 최근 키가 있으면 함께 보존됩니다. 또한 Compaction이 먼저 실행되고 Retention이 그 다음에 적용되므로, 예상보다 일찍 데이터가 삭제될 수 있습니다.

---

## 5. 면접 핵심 질문과 모범 답변

### Q1. Log Retention과 Log Compaction의 차이점은 무엇인가요?

**모범 답변**: Log Retention과 Log Compaction은 데이터 정리의 기준이 근본적으로 다릅니다. Retention은 시간이나 크기를 기준으로 오래된 세그먼트 전체를 삭제합니다. 예를 들어, 7일이 지난 데이터는 키에 상관없이 모두 삭제됩니다. 반면 Compaction은 메시지의 키를 기준으로 각 키의 최신 값만 유지하고 이전 값들을 삭제합니다. 시간이 아무리 지나도 최신 상태는 보존됩니다.

사용 사례를 보면, Retention은 이벤트 로그나 센서 데이터처럼 시간이 지나면 가치가 떨어지는 데이터에 적합합니다. Compaction은 사용자 프로필이나 상품 가격처럼 현재 상태가 중요하고 변경 이력 전체가 필요하지 않은 데이터에 적합합니다.

### Q2. Compaction이 실행되는 조건과 그 조건들의 의미를 설명해주세요.

**모범 답변**: Compaction은 크게 두 가지 조건에 의해 트리거됩니다.

첫째는 Dirty Ratio 기반입니다. `min.cleanable.dirty.ratio`는 전체 로그 중 아직 Compaction되지 않은 Dirty 세그먼트의 비율 임계값입니다. 기본값 0.5는 절반 이상이 Dirty일 때 Compaction을 시작한다는 의미입니다. 이 값이 낮으면 더 자주 Compaction이 실행되어 디스크를 효율적으로 사용하지만 CPU 부하가 증가합니다.

둘째는 `max.compaction.lag.ms` 기반입니다. 이 값이 설정되면 해당 시간이 지난 메시지가 존재할 때 Dirty Ratio와 관계없이 강제로 Compaction이 실행됩니다. 이는 트래픽이 적은 토픽에서도 Compaction이 보장되도록 합니다.

추가로 `min.compaction.lag.ms`는 최소 보존 기간으로, 이 시간 내의 메시지는 Compaction 대상에서 제외되어 최근 변경 이력을 보존할 수 있습니다.

### Q3. Tombstone이란 무엇이며, 왜 즉시 삭제되지 않나요?

**모범 답변**: Tombstone은 null 값을 가진 메시지로, Compaction 토픽에서 특정 키의 데이터를 완전히 삭제하기 위해 사용됩니다. 일반 Compaction에서는 각 키의 최신 메시지가 항상 유지되지만, Tombstone을 발행하면 해당 키가 최종적으로 토픽에서 완전히 사라집니다.

Tombstone이 즉시 삭제되지 않고 `delete.retention.ms`(기본값 1일) 동안 유지되는 이유는 Consumer에게 삭제 이벤트를 전파하기 위해서입니다. Compaction 토픽을 소비하는 애플리케이션은 Tombstone을 받아서 자신의 로컬 저장소에서도 해당 데이터를 삭제해야 합니다. 만약 Tombstone이 즉시 삭제되면, 일시적으로 중단되었던 Consumer는 삭제 이벤트를 놓치게 되어 데이터 불일치가 발생할 수 있습니다.

### Q4. GDPR 준수를 위해 7일 이내 데이터 삭제를 보장하려면 어떻게 설정해야 하나요?

**모범 답변**: 정확한 삭제 시점을 계산하려면 세 가지 설정의 합을 고려해야 합니다.

`segment.ms`는 새 세그먼트가 생성되는 주기입니다. Retention은 세그먼트 단위로 적용되므로, 메시지가 생성된 후 세그먼트가 롤링되어야 삭제 대상이 될 수 있습니다. `retention.ms`는 세그먼트의 최신 메시지가 이 시간을 초과하면 삭제 대상이 됩니다. `log.retention.check.interval.ms`는 삭제 대상 검사 주기입니다.

따라서 7일 이내 삭제를 보장하려면 이 세 값의 합이 7일을 넘지 않아야 합니다. 예를 들어, segment.ms를 1일, retention.ms를 약 5일 23시간 55분, check.interval을 5분으로 설정하면 총합이 7일이 됩니다.

### Q5. Compaction 토픽에서 Consumer가 존재하지 않는 오프셋을 요청하면 어떻게 되나요?

**모범 답변**: Kafka는 요청한 오프셋보다 크거나 같은 가장 작은 유효 오프셋의 메시지를 반환합니다. 예를 들어, 오프셋 0, 2가 Compaction으로 삭제된 상태에서 오프셋 0을 요청하면, Kafka는 오프셋 1의 메시지를 반환합니다.

이 설계는 Consumer의 내결함성을 보장합니다. Consumer가 중단 후 재시작할 때 마지막으로 커밋한 오프셋이 이미 Compaction으로 삭제되었더라도, 자동으로 다음 유효한 메시지부터 처리를 재개할 수 있습니다. 별도의 에러 처리 없이도 정상적으로 동작합니다.

---

## 6. 정리 전략 선택 가이드

| 사용 사례 | 권장 정책 | 핵심 설정 |
|-----------|-----------|-----------|
| 이벤트 스트리밍 | delete | retention.ms=7d |
| 센서 데이터 | delete | retention.ms=30d, retention.bytes 설정 |
| 상태 저장소 | compact | min.cleanable.dirty.ratio=0.3 |
| CDC (변경 데이터 캡처) | compact | delete.retention.ms=1d |
| GDPR 대상 사용자 데이터 | delete,compact | retention.ms + Tombstone 활용 |
| 감사 로그 | delete | retention.ms=365d 이상 |

---

## 7. 실무 체크리스트

- [ ] 법적 데이터 보존 요구사항 확인 (segment.ms + retention.ms + check.interval ≤ 최대 보존 기간)
- [ ] Compaction 토픽은 반드시 키 사용 (null 키 메시지는 거부됨)
- [ ] min.cleanable.dirty.ratio 튜닝 시 스토리지 vs CPU 트레이드오프 고려
- [ ] Tombstone의 delete.retention.ms는 Consumer 처리 시간 고려
- [ ] offsets.retention.minutes는 최소 7일 유지 권장
- [ ] Log Cleaner 지연 및 Dirty Ratio 모니터링 설정
- [ ] delete,compact 조합 시 실제 삭제 시점 테스트

---

## 8. 참고 자료

- [Apache Kafka - Log Compaction](https://kafka.apache.org/documentation/#compaction)
- [Apache Kafka - Log Retention Configuration](https://kafka.apache.org/documentation/#brokerconfigs_log.retention.ms)
- [Confluent - Log Compaction Deep Dive](https://docs.confluent.io/platform/current/kafka/design.html#log-compaction)
