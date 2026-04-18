# Redpanda Fundamentals: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Raft vs ZooKeeper — Redpanda가 Raft를 선택한 이유와 실무 성능 차이

### 왜 이 질문이 중요한가

Kafka는 수년간 ZooKeeper 의존성을 떼어내기 위해 KRaft를 개발했고, 4.0에서야 ZooKeeper를 완전히 제거했다. 반면 Redpanda는 첫날부터 Raft를 내장했다. 면접에서는 "왜 ZooKeeper가 문제였는가"와 "Raft가 어떻게 그 문제를 해결하는가"를 연결해서 설명해야 한다. 실무에서는 클러스터 장애 복구 속도와 운영 복잡도 차이가 핵심이다.

### 답변

ZooKeeper의 근본 문제는 **별도 프로세스로 존재하는 메타데이터 관리자**라는 설계에서 비롯된다. Kafka 브로커가 ZooKeeper와 별도로 동작하므로, 두 시스템 사이의 상태 동기화 지연이 필연적으로 발생한다. 브로커 장애 시 Controller Election이 ZooKeeper를 통해 이루어지는데, 이 과정에서 수십 초의 다운타임이 생길 수 있다. 또한 ZooKeeper 자체의 앙상블(3~5대)을 별도로 운영해야 하므로, 인프라 비용과 운영 부담이 두 배로 늘어난다.

Raft는 ZooKeeper가 제공하던 분산 합의 기능을 브로커 프로세스 안으로 가져온다. Redpanda의 모든 노드는 동일한 바이너리를 실행하면서 파티션별로 독립적인 Raft 그룹을 형성한다. Leader 선출이 ZooKeeper 왕복 없이 Raft 그룹 내부에서 완결되므로, 장애 감지 후 새 Leader 선출까지 걸리는 시간이 **수백 ms 이내**로 줄어든다.

```yaml
# redpanda.yaml — Raft 리더 선출 타임아웃 튜닝 예시
redpanda:
  raft_heartbeat_interval_ms: 150   # 기본 150ms
  raft_election_timeout_ms: 1500    # 기본 1500ms
  # ZooKeeper 기반 Kafka는 session.timeout.ms(기본 6000ms)를 써야 했음
```

ZooKeeper 대비 핵심 차이: ZooKeeper는 클러스터 전체 메타데이터를 중앙 저장하지만, Raft는 각 파티션 그룹이 자신의 상태를 독립적으로 관리한다. 이 분산 방식이 노드 수가 늘어날수록 확장성에서 유리하다.

---

## Q2. 파티션 리밸런싱 — Cooperative vs Eager, 리밸런싱 폭풍 방지법

### 왜 이 질문이 중요한가

Consumer 수가 수백 개인 대규모 프로덕션 환경에서 배포 한 번에 전체 Consumer Group이 멈추는 "리밸런싱 폭풍"은 실제로 빈번한 장애 원인이다. 면접에서는 두 프로토콜의 차이를 설명하고, 실무에서 어떻게 이를 방지했는지 시나리오로 답해야 설득력이 있다.

### 답변

**Eager 리밸런싱(기본값)**은 리밸런스 시작 시 Group 내 모든 Consumer가 보유한 파티션을 전부 반납하고, 재할당이 완료될 때까지 소비를 중단한다. Consumer 100개가 파티션 100개를 처리하는 환경에서 Consumer 1개가 재시작되면, 나머지 99개도 모두 멈추는 것이다. 이 전면 중단 시간(Stop-the-World)이 리밸런싱 폭풍의 본질이다.

**Cooperative 리밸런싱(증분 방식)**은 변경이 필요한 파티션만 이동시킨다. Consumer 1개가 재시작되면, 해당 Consumer가 보유하던 파티션만 다른 Consumer에게 넘기고 나머지는 기존 할당을 유지하며 계속 소비한다. 전체 중단이 없다.

```java
// Cooperative 리밸런싱 활성화 (Consumer 설정)
props.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG,
    CooperativeStickyAssignor.class.getName());

// 추가로 세션 타임아웃을 늘려 불필요한 리밸런스 방지
props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "45000");   // 기본 45s
props.put(ConsumerConfig.HEARTBEAT_INTERVAL_MS_CONFIG, "15000"); // 세션의 1/3
props.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, "300000"); // 처리가 느린 경우
```

실무 방지 전략 세 가지: 첫째, `CooperativeStickyAssignor`를 기본 전략으로 채택한다. 둘째, 롤링 배포 시 Consumer 인스턴스를 한 번에 1~2개씩만 교체하여 리밸런싱 빈도를 줄인다. 셋째, `max.poll.records`를 줄여(`500 → 100`) 폴 처리 시간을 `max.poll.interval.ms` 안에 맞춘다. Consumer가 느린 처리 때문에 하트비트를 못 보내면 불필요한 리밸런스가 발생하기 때문이다.

---

## Q3. Tiered Storage 비용 모델 — 로컬 vs 원격, 실무 최적화 전략

### 왜 이 질문이 중요한가

데이터를 오래 보관해야 하는 서비스(금융 감사 로그, 의료 기록, 사용자 행동 로그)에서 스토리지 비용은 Redpanda 도입 결정의 핵심 변수다. "Tiered Storage가 왜 필요한가"보다 "언제 켜야 하고 어떻게 설정해야 비용이 실제로 줄어드는가"를 답할 수 있어야 한다.

### 답변

비용 구조를 먼저 이해해야 한다. NVMe SSD는 GB당 월 약 $0.20이고, AWS S3 Standard는 $0.023으로 약 9배 차이다. 하루 100GB씩 1년 보존 시: NVMe만 사용하면 `36,500GB × $0.20 = $7,300/월`, S3 기반 Tiered Storage + 로컬 7일치만 유지하면 `700GB × $0.20 + 35,800GB × $0.023 ≈ $963/월`이 된다.

```yaml
# redpanda.yaml — Tiered Storage 활성화
redpanda:
  cloud_storage_enabled: true
  cloud_storage_bucket: "my-redpanda-tiered"
  cloud_storage_region: "ap-northeast-2"

# 토픽별 로컬 보존 목표 설정 (7일치만 로컬 유지)
rpk topic alter-config my-topic \
  --set retention.local.target.ms=604800000 \
  --set redpanda.remote.write=true \
  --set redpanda.remote.read=true
```

장기 보존 비용을 더 줄이려면 S3 Intelligent-Tiering이나 Glacier를 활용할 수 있다. 30일 이상 접근 없는 데이터는 S3 Glacier Instant Retrieval($0.004/GB)로 자동 전환되도록 S3 Lifecycle Policy를 설정하면 추가로 80% 절감이 가능하다. 단, Tiered Storage의 읽기 성능은 로컬(Sub-ms) 대비 S3(수십 ms)로 느려지므로, 최근 데이터는 항상 로컬 Hot Tier에 유지해야 SLA를 지킬 수 있다.

---

## Q4. ISR과 데이터 유실 — min.insync.replicas와 acks의 관계

### 왜 이 질문이 중요한가

"데이터를 절대 잃으면 안 된다"는 요구사항은 거의 모든 프로덕션 시스템에 존재한다. 하지만 내구성을 높이면 처리량이 줄고 지연이 늘어난다. 면접에서는 두 설정의 역할을 정확히 구분하고, 실무에서 어떤 트레이드오프로 값을 선택하는지 설명해야 한다.

### 답변

`acks`는 **Producer가 쓰기 성공을 판단하는 기준**이고, `min.insync.replicas`(min.isr)는 **그 기준을 충족하기 위해 최소 몇 개의 레플리카가 동기화 상태여야 하는지**를 정한다. 이 둘은 함께 작동할 때만 의미가 있다.

```
시나리오: replication.factor=3, min.insync.replicas=2, acks=all

정상 상태 (ISR=3): 쓰기 성공 — 2개 이상 복제됨
노드 1개 다운 (ISR=2): 쓰기 성공 — min.isr 충족
노드 2개 다운 (ISR=1): NotEnoughReplicasException — min.isr 미달로 쓰기 거부
```

`acks=all`만 설정하고 `min.isr=1`(기본값)이면, ISR에 Leader만 남아도 쓰기가 성공한다고 응답하고 곧바로 Leader가 다운되면 데이터가 유실된다. `acks=all`의 실제 보장은 `min.isr` 설정에 달려 있다.

```java
// 프로덕션 권장 설정 (내구성 최우선)
props.put(ProducerConfig.ACKS_CONFIG, "all");
props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);

// 브로커 측 설정 (rpk)
rpk topic alter-config critical-topic \
  --set min.insync.replicas=2 \
  --set replication.factor=3
```

처리량 중심 설정은 `acks=1`로 Leader 확인만 기다리고, `min.isr`는 의미를 잃는다. 이 경우 Leader 장애 시 최대 수 ms 분량의 데이터가 유실될 수 있음을 수용하는 것이다. 금융 결제처럼 유실이 허용되지 않는 도메인은 반드시 `acks=all + min.isr=2 + rf=3` 조합을 써야 한다.

---

## Q5. Consumer Group 리밸런싱 — 대규모 환경의 문제와 해결

### 왜 이 질문이 중요한가

Consumer 수십 개 수준에서는 리밸런싱이 눈에 띄지 않지만, 수백 개 규모로 늘어나면 리밸런싱 한 번에 수 분간 메시지 처리가 중단되는 사태가 발생한다. 이를 경험하지 않은 면접관도 "대규모 Consumer Group에서 고려해야 할 것이 무엇인가"를 자주 묻는다.

### 답변

대규모 Consumer Group에서 리밸런싱이 느린 이유는 두 가지다. 첫째, Group Coordinator가 모든 Consumer의 JoinGroup 요청을 기다린 뒤 한 번에 파티션을 재분배하는데, Consumer 수가 많을수록 이 대기 시간이 `rebalance.timeout.ms`(기본 300초)까지 늘어난다. 둘째, 모든 Consumer가 기존 파티션을 반납하고 재할당받는 동안 전체 그룹이 소비를 멈춘다(Eager 방식의 경우).

```
Consumer 200개, 파티션 200개 환경에서 Eager 리밸런싱:
- JoinGroup 수집 대기: 최대 45초 (session.timeout.ms)
- 파티션 재할당 계산 및 배포: 수 초
- 총 중단 시간: 수십 초 ~ 수 분
```

해결책은 세 방향이다. 첫째, `CooperativeStickyAssignor`로 전환하여 변경된 파티션만 이동시킨다. 둘째, Consumer Group을 여러 개로 분리한다 — 200개 Consumer를 하나의 그룹으로 묶는 대신, 4개 그룹 × 50개 Consumer로 나누면 리밸런싱 영향 범위가 1/4로 줄어든다. 셋째, `group.instance.id`를 설정하여 Static Membership을 활성화한다.

```java
// Static Membership — Consumer 재시작 시 리밸런싱 없이 기존 파티션 복귀
props.put(ConsumerConfig.GROUP_INSTANCE_ID_CONFIG, "consumer-pod-" + podId);
// session.timeout.ms 안에 복귀하면 리밸런싱이 트리거되지 않음
props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "60000");
```

Static Membership은 Kubernetes 환경에서 Pod 이름을 `group.instance.id`로 사용하는 패턴이 특히 효과적이다. 롤링 배포 시 이전 Pod가 종료되고 새 Pod가 같은 이름으로 뜨면, Group Coordinator가 동일한 Consumer가 돌아온 것으로 인식하여 리밸런싱을 건너뛴다.

---

## Q6. Thread-per-Core 모델 — 왜 Redpanda의 성능이 Kafka보다 예측 가능한가

### 왜 이 질문이 중요한가

Redpanda가 Kafka보다 처리량이 높다는 벤치마크 결과를 자주 접하는데, 면접에서 "왜 그런가"를 묻는다면 단순히 "C++이라서"라는 답은 부족하다. Thread-per-Core 모델이 구체적으로 어떻게 컨텍스트 스위치와 Lock 경쟁을 제거하는지 설명해야 한다.

### 답변

전통적인 Thread Pool 모델(Kafka)은 여러 스레드가 공유 자원(큐, 캐시, 소켓 버퍼)에 접근할 때 Lock으로 동기화한다. CPU 코어가 32개인 서버에서 스레드 수백 개가 Lock을 두고 경쟁하면, 실제 CPU 사용률이 높아도 상당 시간을 Lock 대기와 컨텍스트 스위치에 소비한다. GC가 발생하면 모든 스레드가 잠시 멈추는 Stop-the-World도 지연 스파이크의 주요 원인이다.

Redpanda의 Thread-per-Core(Seastar 프레임워크)는 코어 하나에 스레드 하나를 고정 배치하고, 각 스레드가 자신만의 데이터를 담당한다. 코어 0은 파티션 0~7, 코어 1은 파티션 8~15 식으로 데이터가 나뉘면, 코어 사이에 공유 자원이 없으므로 Lock이 필요 없다. 코어 간 통신은 메시지 패싱(Seastar future/promise)으로 이루어진다.

```
Kafka (Thread Pool):
  64 threads → 공유 파티션 큐 → Lock 경쟁 → 컨텍스트 스위치
  처리량: 코어 수 증가 대비 선형 미만 증가

Redpanda (Thread-per-Core):
  32 cores → 32 threads → Lock-free → 코어별 독립 처리
  처리량: 코어 수에 비례하여 선형 증가
```

실무 영향으로는, Redpanda는 p99 지연시간 변동폭이 Kafka보다 작다. JVM GC로 인한 수백 ms 스파이크가 없고, Lock 경쟁으로 인한 지연 폭발도 없기 때문이다. 지연시간 SLA가 엄격한 실시간 처리(결제, 게임 이벤트)에서 이 예측 가능성이 의사결정의 근거가 된다.
