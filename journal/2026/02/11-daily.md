# 학습 일지 - 2026-02-11 (화요일)

## 오늘의 목표
- [x] Redpanda 02-architecture.md 학습
- [x] Redpanda 04-schema-registry.md 학습

---

## 학습 내용

### 1. Redpanda Architecture (02-architecture.md)

**범위**: 전체 아키텍처 개요, Thread-per-Core, Raft 합의, 스토리지, 네트워크

#### 핵심 배움

**단일 바이너리 아키텍처**: Kafka가 Broker + ZooKeeper/KRaft + Schema Registry + REST Proxy를 별도 프로세스로 운영하는 것과 달리, Redpanda는 단일 C++ 바이너리(`/usr/bin/redpanda`)에 모든 기능을 통합했다. "단일"의 의미는 노드 수가 아니라 **노드 하나에서 실행하는 프로세스 수가 1개**라는 뜻이다. 설정 파일 1개, 모니터링 대상 1개, 버전 호환성 매트릭스 불필요.

**Thread-per-Core (Seastar 기반)**: 각 CPU 코어가 독립적인 Shard로 동작한다. 코어 간 공유 메모리가 없으므로 Lock이 필요 없고, 이것이 Kafka(JVM Thread Pool + Shared Memory)와 근본적으로 다른 점이다. 핵심 메커니즘:
- Future/Promise 기반 비동기 프로그래밍
- Cooperative Scheduling (OS 스케줄러에 의존하지 않음)
- 코어별 전용 I/O Scheduler (O_DIRECT + io_uring)
- 결과: GC Pause 없이 P99.9 지연시간이 수 ms 수준으로 예측 가능

**Raft 합의 프로토콜**: Kafka의 ISR(In-Sync Replica)이 동적 목록 기반인 반면, Redpanda는 Raft의 정적 Quorum 규칙을 사용한다. **파티션 = Raft 그룹**이라는 1:1 매핑이 핵심. 각 파티션이 독립적인 Raft 그룹으로 Leader Election과 복제를 수행하므로, 하나의 파티션 장애가 다른 파티션에 전파되지 않는다.

**네트워크 분리**: 외부 API(Kafka:9092, HTTP Proxy:8082, Schema Registry:8081, Admin:9644)와 내부 RPC(:33145)가 물리적으로 분리되어 보안과 성능을 동시에 확보한다.

### 2. Schema Registry (04-schema-registry.md)

**범위**: SR 필요성, Redpanda 내장 SR, Avro/Protobuf/JSON Schema 비교, API, 호환성 모드, Wire Format, Spring Boot 연동, 개발 워크플로우, 프로덕션 운영

#### 핵심 배움

**Schema Registry의 존재 이유**: 메시지 큐는 바이트 배열만 저장하고 내용을 검증하지 않는다. Schema Registry는 Producer/Consumer 간 암묵적 계약을 **인프라 수준에서 강제**하여, 스키마에 맞지 않는 메시지를 Serializer 단계에서 즉시 차단한다. 오류가 런타임(새벽 3시 프로덕션)이 아니라 전송 전에 드러나는 것이 핵심 가치.

**Wire Format**: `[0x00 Magic Byte][Schema ID 4bytes][Avro/Protobuf 바이너리]`. 모든 메시지에 Schema ID가 포함되어, Consumer가 이 ID로 Schema Registry에서 스키마를 조회한다. 클라이언트 라이브러리(KafkaAvroSerializer/Deserializer)가 프로세스 힙 메모리에 자동 캐싱하므로 매 메시지마다 네트워크 호출은 발생하지 않는다.

**호환성 모드와 배포 순서의 관계**:
- BACKWARD: 새 Consumer가 옛 데이터를 읽을 수 있음 → **Consumer 먼저 배포**
- FORWARD: 옛 Consumer가 새 데이터를 읽을 수 있음 → **Producer 먼저 배포**
- FULL: 양방향 호환 → **배포 순서 무관** (가장 안전하지만 모든 필드 변경에 기본값 필수)
- Transitive: 직전 버전뿐 아니라 **모든 이전 버전**과 호환 검증

**FULL 호환의 핵심 원리 = "기본값이 열쇠"**: 추가하려면 기본값 필수(옛 데이터에서 채울 수 있어야), 삭제하려면 기본값 필수(옛 Consumer가 채울 수 있어야). 기본값 없는 필수 필드는 추가도 삭제도 불가하므로 v1 설계가 중요하다.

**개발 워크플로우**: 로컬에서는 `auto.register.schemas=true`로 앱이 자동 등록, 프로덕션에서는 `false`로 설정하고 CI/CD 파이프라인만 등록. `.avsc` 파일과 코드를 동시에 개발하되, 파이프라인이 호환성 검증 → 스키마 등록 → 앱 배포 순서를 강제한다.

**캐싱 주체**: 캐싱을 하는 것은 JVM이나 Spring Boot가 아니라 **Confluent 클라이언트 라이브러리**(KafkaAvroSerializer/Deserializer)이다. 라이브러리 내부 Map에 스키마를 저장하며, 이는 Java뿐 아니라 Python, Go 등 모든 SR 클라이언트에서 동일하게 동작한다.

---

## Docs 완료
- **경로**: `poc/08_MessageQueue/red-panda/learning/02-fundamentals/02-architecture.md`
  - **핵심 개념**: 단일 바이너리, Thread-per-Core(Seastar), Raft 합의, 파티션=Raft 그룹
- **경로**: `poc/08_MessageQueue/red-panda/learning/02-fundamentals/04-schema-registry.md`
  - **핵심 개념**: Wire Format, 호환성 모드-배포 순서 관계, FULL 호환의 기본값 원리, 개발 워크플로우(로컬 auto vs 프로덕션 CI/CD)

---

## 추가 작업
- [x] 04-schema-registry.md 캐시 설명 상충 수정 ("어디에 존재하는가" + "캐싱의 주체" → 하나로 통합)
- [x] 04-schema-registry.md FORWARD/FULL 호환 섹션에 구체적 예시 및 원리 추가 (사용자 편집)
- [x] 04-schema-registry.md 개발 워크플로우 섹션(9절) 신규 추가 (사용자 편집)
- [x] 10-message-schema-design.md 신규 작성 (CloudEvents, AsyncAPI, 미들웨어별 스키마 제어)
- [x] 11-topic-design.md 신규 작성 (토픽 네이밍, 파티셔닝, 미들웨어별 주소 체계)

---

## 회고
- 잘한 점: 02-architecture에서 Kafka와의 차이를 구조적으로 비교하면서 읽어서, 단순 "Redpanda가 빠르다"가 아니라 **왜 빠른지(Thread-per-Core, O_DIRECT, GC 없음)**를 설명할 수 있게 되었다. 04-schema-registry에서 호환성 모드를 배포 순서와 연결지어 이해한 것이 실무적으로 가장 유용했다.
- 개선할 점: Schema Registry 학습 중 캐시 설명이 상충되는 것을 발견하여 수정했다. 문서 작성 시 하나의 개념을 여러 곳에서 다룰 때 관점(위치 vs 주체)을 명확히 구분해야 한다.

## 내일 계획
- 새로 작성한 10-message-schema-design.md, 11-topic-design.md 리뷰
- Redpanda 학습 다음 챕터 진행 (03-kafka-comparison 또는 05-core-features)
