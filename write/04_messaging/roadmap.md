---
title: Kafka / Redpanda 메시징 딥다이브 로드맵 — 토이프로젝트·키워드 원문
tags: [moc, messaging, kafka, redpanda, roadmap, keywords]
status: reference
related:
  - README.md
updated: 2026-06-25
---

# Kafka / Redpanda 메시징 딥다이브 로드맵 — 토이프로젝트·키워드 원문

---

> Kafka/Redpanda 를 "메시지 보내고 받기" 가 아니라 **이벤트 플랫폼을 운영하는 사람의 관점**으로 본다. 핵심 드러낼 것: 비동기 · Fan-out · 재처리 · 순서 보장 · 내구성 있는 로그 · Lag 관측 · 스키마 계약 · 장애 격리. 이 문서는 제공받은 두 원문(DevOps 관점 토이프로젝트 14종 + 실무형 후보 10종)을 **빠짐없이** 옮긴 기록이고, 폴더 인덱스·학습 흐름은 [README.md](README.md) 가 맡는다.

## 0. 2026년 기준 전제

- Kafka 는 4.x 흐름(4.2.x·4.3.x 릴리즈). 새로 공부하면 ZooKeeper 중심이 아니라 **KRaft 기반 Kafka 4.x 운영 관점** (출처: [Apache Kafka Blog](https://kafka.apache.org/blog)).
- Redpanda 는 Kafka 0.11+ 클라이언트 호환을 유지하지만 일부 지원 범위·예외가 있다. "Kafka API 호환 브로커" 로 보되 운영 전 클라이언트·트랜잭션·ACL·스키마·커넥터 호환성 검증 필요 (출처: [Kafka Compatibility](https://docs.redpanda.com/current/develop/kafka-clients/)).
- Kafka 는 단순 큐가 아니라 이벤트를 발행/구독하고 내구성 있게 저장해 실시간·나중에 다시 처리하는 플랫폼. "시간이 지나도 다시 읽을 수 있는 사건의 기록" 으로 설계할 때 장점이 산다 (출처: [Apache Kafka Intro](https://kafka.apache.org/intro/)).
- 권장 스택: Spring Boot 3.x · Java 21 · Spring Kafka · MariaDB · Redpanda/Kafka · Redpanda Console · Docker Compose · Prometheus · Grafana · OpenTelemetry · Loki.

## 1. 기술 학습 토이프로젝트 14종 (DevOps 관점)

### 1. EventOps Control Plane (가장 추천)

이벤트 플랫폼 관리 포털. 토픽 생성·정책 관리 · 컨슈머 그룹/Lag 조회 · DLT 조회 · 재처리 요청 · 스키마 조회 · 이벤트 발행 테스트 · 운영 이력 저장. 공부: AdminClient · Topic · Partition · Consumer Group · Offset · Lag · Retention · Compaction · DLT · Schema Registry · ACL. 전문가 질문: 이 컨슈머는 왜 밀리는가 / 어떤 토픽 retention 이 위험한가 / DLT 메시지는 누가·언제·왜 재처리했는가 / 토픽을 아무나 만들게 둘 것인가 / 스키마 깨진 이벤트를 어떻게 막는가.

### 2. Outbox / Inbox 신뢰성 실험실

DB 트랜잭션과 Kafka 발행의 불일치를 Outbox 로 해결. 흐름: 주문 생성 → orders 저장 → outbox_event 저장 → outbox poller 가 발행 → consumer 가 inbox_event 로 중복 방지 → 후속 상태 반영. 공부: Dual Write Problem · Transactional Outbox · Inbox Pattern · Idempotent Consumer · Event ID · Manual Ack · Retry · DLT. 핵심 질문: DB 저장 성공·Kafka 발행 실패면 / 발행 성공·앱 죽으면 / consumer 처리 후 offset commit 전 죽으면 / 같은 메시지 두 번 받으면 DB 상태가 깨지나.

### 3. Retry / DLT 운영 시스템

메인 토픽 consume → 처리 실패 → 재시도 토픽 → N회 실패 시 DLT → DLT 조회 → 관리자 수동 재처리 → 이력 저장. Spring Kafka 는 `@RetryableTopic`·`RetryTopicConfiguration` 으로 non-blocking retry/DLT 구성 (출처: [Non-Blocking Retries](https://docs.spring.io/spring-kafka/reference/retrytopic.html)). 공부: Blocking/Non-blocking Retry · Retry Topic · Dead Letter Topic · Backoff · Poison Message · Deserialization Error · Manual Reprocess. 기준표 — 재시도 가능(외부 API timeout·일시 DB lock·네트워크) vs 금지(JSON schema 불일치·필수 필드 누락·비즈니스 검증 실패·존재하지 않는 참조 ID).

### 4. Consumer Lag 관측 대시보드

토픽별 consumer group → partition별 current/end offset → lag 계산 → 추세 저장 → Grafana → 임계치 알림. 공부: Consumer Group · Committed Offset · Log End Offset · Lag · Rebalance · Partition Assignment · Prometheus · Grafana · Alertmanager. 깊은 질문: lag 높음 = 무조건 장애인가 / consumer 처리량이 낮은가 / producer 유입이 늘었나 / 특정 partition 만 밀리나 / key skew 가 있나 / rebalance 가 반복되나.

### 5. Exactly-Once Semantics 실험실

input-topic consume → 비즈니스 처리 → output-topic produce → offset commit 을 Kafka transaction 으로 묶기. Spring Kafka 는 transaction 으로 read→process→write 시퀀스에서 EOS 가능(외부 DB 포함 시 별도 멱등성 필요) (출처: [Exactly Once Semantics](https://docs.spring.io/spring-kafka/reference/kafka/exactly-once.html)). Redpanda 도 Kafka 호환 transaction + idempotent producer 로 EOS 지원 (출처: [Transactions](https://docs.redpanda.com/cloud-data-platform/develop/transactions/)). 공부: Idempotent Producer · Transactional Producer · transactional.id · sendOffsetsToTransaction · read-process-write · EOS · At-least-once · Idempotent DB Write. ⚠️ Kafka 안 EOS 와 DB/API 포함 EOS 는 다름: Kafka→Kafka(Transaction 으로 EOS) / Kafka→DB(event_id unique key 로 멱등) / DB→Kafka(Outbox 필요).

### 6. Kafka / Redpanda 성능 비교 실험실

같은 producer/consumer 코드로 Kafka vs Redpanda 비교(동일 topic/partition/replication/설정). 측정: produce/consume throughput · p95/p99 latency · consumer lag · broker CPU/memory · disk · network I/O · rebalance 시간 · 장애 복구 시간. 공부: Batching · Compression · acks · linger.ms · batch.size · max.in.flight.requests · replication · fsync · page cache · partition count. 중요한 건 "Redpanda 가 빠르다더라" 가 아니라 어떤 workload·partition·메시지 크기·compression·복구에서인가 — 성능 테스트는 숫자가 아니라 조건이 중요하다.

### 7. Schema Registry 기반 이벤트 계약 관리

Avro/JSON Schema 등록 → producer 직렬화 → consumer 역직렬화 → 호환 가능/불가능 변경 차단 → 버전 이력. Redpanda 는 Schema Registry(저장·관리·Authorization·Contexts·Server-Side Schema ID Validation) 제공 (출처: [Schema Registry](https://docs.redpanda.com/current/manage/schema-reg/)). 공부: Avro · JSON Schema · Protobuf · Backward Compatibility · Forward Compatibility · Full Compatibility · Schema Evolution · Contract Testing. 질문: 이 필드 삭제해도 되나 / consumer 가 구버전이면 / null 허용인가 / enum 값 추가 시 깨지나.

### 8. Log Compaction 기반 상태 저장소

user-profile-events 토픽(key=userId, value=상태) → 같은 key 반복 발행 → compaction 활성화 → 최종 상태만 남는지 → consumer 재시작 후 상태 복구. 공부: Log · Offset · Retention · Compaction · Tombstone · Key Design · State Reconstruction · Event Sourcing · CQRS. Queue(소비되면 사라짐) vs Kafka log(재생 가능한 시간 기록) vs Compacted topic(key별 최신 상태 복원 재료).

### 9. CDC 기반 데이터 동기화 파이프라인

MariaDB 변경 → Debezium CDC → Kafka/Redpanda → Consumer → read model DB 갱신. 공부: CDC · Debezium · Binlog · Source/Sink Connector · Outbox Event Router · Read Model · Eventual Consistency. 조심: DB 스키마 변경 시 CDC / 초기 스냅샷 / 중복 이벤트 제거 / 삭제 이벤트 표현 / 대량 변경 시 lag.

### 10. Multi-Tenant Topic & ACL Lab

팀별 namespace 설계 · topic naming rule · producer/consumer 권한 분리 · dev/stg/prod 접근 분리 · ACL · 권한 없는 produce/consume 차단. 공부: SASL · SCRAM · mTLS · ACL · Principal · Topic Naming · Consumer Group Naming · Multi-tenancy · Least Privilege. 토픽 이름도 운영 정책 — `dev.order.events.v1` · `team-order.order-created.v1` 처럼. 규칙 없는 토픽은 쓰레기장이 된다.

### 11. Redpanda Console 기반 운영 실험

Redpanda docker compose + Console + topic 생성/조회 · produce/consume · consumer group 조회 · schema registry · rpk CLI. 공부: rpk · Redpanda Console · Kafka API compatibility · Broker/Topic config · Consumer group · Schema Registry. Redpanda 는 Kafka API 호환을 주지만 운영 도구·내부 아키텍처는 다르다 (출처: [Kafka Compatibility](https://docs.redpanda.com/current/develop/kafka-clients/)). 질문: Kafka client 설정 그대로 쓰나 / Spring Kafka 그대로 붙나 / 트랜잭션 동일한가 / ACL/SASL 차이 / 지표 이름 차이.

### 12. Tiered Storage / 장기 보관 실험

짧은 local retention → object storage offload → 오래된 offset consume → broker disk 관측 → remote read latency. ⚠️ Redpanda Tiered Storage 는 Enterprise license 필요 — 로그 세그먼트를 object storage 로 offload (출처: [Tiered Storage](https://docs.redpanda.com/streaming/current/manage/tiered-storage/)). 공부: Tiered Storage · Object Storage · Segment · Remote Read/Write · Cold Data · Recovery. 토이에선 "문서 분석 + 대체 실험" 으로 잡아도 좋다. 핵심: 로컬 디스크 비용 / 오래된 데이터 재읽기 latency / replay 비용 / object storage 장애 영향.

### 13. Chaos Engineering for Kafka / Redpanda

broker 종료 · consumer 강제 종료 · producer 네트워크 지연 · disk full · 처리 지연 · rebalance 반복 유발. 관찰: leader election 시간 · producer error · rebalance · lag 증가 · duplicate · DLT 증가 · 복구 시간. 공부: Replication Factor · ISR · Leader Election · Rebalance · Session Timeout · Heartbeat · max.poll.interval.ms · Backpressure · Failure Recovery.

### 14. Kafka Streams / 실시간 집계

order-events consume → 분 단위 주문 수·상품별 매출 집계 → 비정상 패턴 탐지 → 결과 topic 발행 → API 조회. 공부: Kafka Streams · KTable · KStream · Windowing · State Store · Changelog Topic · Stream Processing · Exactly Once Processing. Consumer(읽고 처리) vs Streams(상태 있는 계산 그래프). Outbox/Retry/Lag 먼저 잡은 뒤 확장 권장.

## 2. Kafka vs Redpanda 학습 방향

| 구분 | Kafka 중심 | Redpanda 중심 |
|------|-----------|--------------|
| 핵심 가치 | 표준 생태계 이해 | Kafka API 호환 브로커 운영 단순화 |
| 운영 포인트 | KRaft·broker·controller·partition·Connect·Streams | rpk·Console·Kafka compatibility·single-binary |
| 학습 난도 | 생태계 넓어 깊음 | 시작은 가볍지만 호환성 검증 중요 |
| Spring 연동 | Spring Kafka 표준 자료 풍부 | Spring Kafka client 로 대부분 접근 가능하되 검증 |
| 좋은 프로젝트 | Outbox·Retry/DLT·Connect·Streams | 로컬 이벤트 플랫폼·관측·Console·Kafka 대비 실험 |
| 주의점 | 설정·운영 개념 많음 | Kafka 와 100% 동일 가정은 위험 |

기술 학습 TOP5: ① Outbox/Inbox ② Retry/DLT ③ Consumer Lag 관측 ④ Schema Registry 계약 ⑤ Kafka vs Redpanda 성능/장애 비교.

## 3. 실무형 토이프로젝트 10종 ("우리도 겪는 문제")

이론 과시가 아니라 실제 회사가 겪는 문제 관점.

### 1. 주문/결제/재고/배송 이벤트 기반 처리 (가장 정석)

주문 생성 → 결제·재고·쿠폰·알림·배송·정산이 따라옴. REST 동기로 묶으면 하나가 느려도 전체 주문 API 가 무거워진다. Kafka: 주문 API 는 `order.created` 만 발행, 후속 서비스가 각자 consume, 하나가 실패해도 주문 생성은 격리, 실패는 retry/DLT, 로그 replay 로 정산/분석 재구성. 구현: order-api(orders+outbox) · outbox-publisher · payment-consumer · inventory-consumer · notification-consumer · admin-api(이력·DLT 조회·재처리). 강한 포인트: Outbox(dual-write 완화) · Inbox(중복 방지) · 보상 이벤트 · DLT 재처리 API · 주문별 이벤트 타임라인.

### 2. 대량 엑셀/CSV 업로드 비동기 처리

수만 건 업로드를 동기로 하면 timeout·메모리·중간 실패 추적 불가·진행률 미표시. Kafka: file.uploaded → file.parsed → row.validation.requested → row.persist.requested → row.failed → upload.completed. 구현: upload-api(202 Accepted) · parser-worker · validator-consumer · persist-consumer · result-aggregator(진행률) · admin-ui(실패 row 재처리). 장점: timeout 회피 · row 단위 병렬 · 실패 row 만 분리 · consumer 확장 · uploadId key 순서/집계. 고급: max.poll.records · partition key=uploadId/rowGroupId · 실패 유형별 retry · row별 idempotency key · 재시작 복구.

### 3. Jenkins/배포 이벤트 허브

build.started/finished · image.pushed · deploy.requested/approved/started/succeeded/failed · rollback.requested. consumer: history(이력) · notify(Slack) · metric(Grafana) · audit(감사) · ticket(변경관리). 구현: jenkins-webhook-api · deployment-history-consumer · notification-consumer · metrics-consumer · admin-api(배포 타임라인·재배포). 장점: 배포 이벤트 fan-out · Jenkins 와 후속 시스템 분리 · 로그 삭제 후에도 이력 보존 · replay 로 통계 재구성 · 알림 실패가 배포를 막지 않음. 이름: CI/CD Event Hub · Deployment EventOps Platform.

### 4. 결재 완료 후 후속 작업 오케스트레이션

휴가 결재→근태 / 권한 승인→IAM / 배포 승인→Jenkins / 구매 결재→발주 / 변경관리 승인→배포 가능. 동기 호출 시 후속 장애가 결재 장애로 번짐. Kafka: approval.completed → leave.apply/permission.grant/deployment.approved/purchase.order.requested. 구현: approval-api(모든 승인 완료 시 발행) · approval-event-consumer(유형별 분기) · workflow-consumer(Jenkins) · permission-consumer · notification-consumer · admin-api(재처리). 고급: approvalId 기준 순서 보장 · 후속 idempotency key · 반려/취소 이벤트 · 후속 실패 알림.

### 5. 알림 통합 플랫폼

서비스마다 이메일/Slack/카카오/SMS 직접 호출 → 코드 중복·재처리 어려움·rate limit·이력 추적·장애 전파. Kafka: 모든 서비스가 `notification.requested` 만 발행, 알림 플랫폼이 채널별 처리(email/sms/slack/kakao-consumer). 구현: notification-api(템플릿·이력) · notification-router · channel-consumer · retry-dlt. 장점: 비즈니스 API 와 발송 분리 · 채널별 독립 확장 · rate limit · 실패 재처리 · 이력/audit. (Spring Kafka non-blocking retry/DLT 활용, 출처: [Non-Blocking Retries](https://docs.spring.io/spring-kafka/reference/retrytopic.html) · [How the Pattern Works](https://docs.spring.io/spring-kafka/reference/retrytopic/how-the-pattern-works.html)).

### 6. CDC 기반 검색/조회 모델 동기화

운영 DB(MariaDB) ↔ 검색/통계 조회 모델 분리. MariaDB binlog → Debezium → Kafka → read-model-consumer → Elasticsearch/OpenSearch/Redis/read model. 구현: source-service · debezium · read-model-consumer · search-api · admin-api(CDC lag·재색인). 장점: 원본 DB 와 조회 모델 분리 · 변경 이벤트 동기화 · offset 부터 재처리 · read model 재구성 · 검색/통계 부하 분리.

### 7. 실시간 작업 상태 추적 시스템

배치·테스트·배포·데이터 이관·파일 처리의 상태 변화(REQUESTED→VALIDATING→RUNNING→PARTIAL_FAILED→RETRYING→COMPLETED→FAILED→CANCELLED). Kafka: job.requested/started/progressed/failed/retried/completed. consumer: state(현재 상태) · timeline(이력) · notify · metric. 구현: job-api(202·jobId) · worker(진행률 발행) · state-projector · timeline-projector · admin-ui(재시도). 장점: 긴 작업 비동기화 · 상태 이력 보존 · replay 로 상태 복원 · 진행률/실패율 관측 · worker 수평 확장.

### 8. 장애 격리형 외부 API 연동 플랫폼

결제사·문자·인사·ERP·Webhook·공공기관 API 는 느리고 불안정. 트랜잭션 안 직접 호출 시 timeout·전파·재시도 중복. Kafka: external-call.requested → succeeded/failed. 구현: business-api(즉시 응답) · external-call-worker(timeout/retry/backoff) · result-consumer · admin-api(재시도·실패율). 실패 분류 — 재시도 가능(timeout·429·503·네트워크) vs 위험(400·인증 실패·필수 필드 누락·비즈니스 검증).

### 9. 이벤트 기반 감사 로그 / 타임라인 시스템

티켓 생성·승인·워크플로우·배포·권한 변경·삭제를 서비스별 DB 에 따로 남기면 조회·포맷 제각각. Kafka: 각 서비스가 `audit.event` 발행, 감사 전용 consumer 가 append-only 저장. 구현: business-services · audit-consumer · timeline-api(entityId 타임라인) · search-consumer · retention-policy. 고급: traceId/correlationId 전파 · actor/userId/IP/userAgent · before/after diff · 민감정보 마스킹 · append-only.

### 10. Schema Registry 기반 이벤트 계약 검증 플랫폼

producer 가 필드 바꾸면 consumer 가 터짐(amount 타입 변경·status enum 추가·필수 필드 삭제·nullable 정책·version 불명확). Redpanda Schema Registry 는 등록·version 조회·compatibility 설정·serialization format 조회 API 제공 (출처: [Schema Registry API](https://docs.redpanda.com/current/manage/schema-reg/schema-reg-api/)). 구현: schema-registry · producer · consumer · contract-test(backward 가능/불가능) · admin-api(subject/version·diff). 단독보다 주문/결재/배포 이벤트 프로젝트에 얹으면 좋다.

실무형 TOP5: ① 주문/결제/재고/배송 ② Jenkins/배포 이벤트 허브 ③ 대량 업로드 비동기 ④ 결재 후속 오케스트레이션 ⑤ CDC Read Model.

## 4. 최종 추천 조합 — Event-Driven Operations Platform

하나로 묶는 최종 조합. 도메인: 변경관리/배포/결재/작업 실행 시스템.

전체 흐름:

```text
1. 사용자가 배포/작업 실행 요청
2. 결재 승인 완료
3. approval.completed 발행
4. Jenkins 실행 consumer가 배포 Job 요청
5. Jenkins webhook이 build/deploy 이벤트 발행
6. history-consumer가 배포 이력 저장
7. notification-consumer가 Slack 알림
8. metric-consumer가 성공률/소요시간 집계
9. 실패 이벤트는 retry/DLT로 이동
10. 운영자가 DLT 조회·재처리
```

아키텍처:

```text
Spring Boot API (approval-api · deployment-api · admin-api)
MariaDB (approval · deployment_history · outbox_event · inbox_event · dlt_reprocess_history)
Kafka/Redpanda (approval.completed · deployment.{requested,started,succeeded,failed} · notification.requested · *.dlt)
Consumers (jenkins-trigger · deployment-history · notification · metrics · dlt-reprocess)
```

이 조합이 좋은 이유: 결재 완료 후 후속은 비동기화가 필요 · 배포 이벤트는 fan-out · 알림 실패가 배포 실패가 되면 안 됨 · 배포 이력은 Jenkins 로그와 별개 보존 · 실패 이벤트는 재처리 가능 · 운영자는 lag/DLT 를 봐야 함. Kafka 장점이 억지가 아니라 자연스럽다.

MVP 단계:

```text
1단계: order/approval 생성 → DB 저장 → order.created/approval.completed 발행 → consumer 처리 → DB 저장
2단계: Outbox 적용 (트랜잭션 안 orders+outbox_event, poller가 발행·published 처리)
3단계: Inbox 적용 (consumer_group+event_id unique key, 중복 skip, 처리 후 offset commit)
4단계: Retry/DLT (일시 장애 retry, 영구 장애 DLT, 조회/재처리 API)
5단계: 운영 대시보드 (consumer lag·처리량·실패율·DLT 적재량·재처리 성공률·p95)
6단계: Schema Registry (event schema 등록·producer validation·consumer compatibility)
```

## 5. 포트폴리오 문서에 넣을 핵심 질문 10

```text
1. 왜 REST 동기 호출이 아니라 Kafka 이벤트로 분리했는가?
2. DB 저장 성공 후 Kafka 발행 실패는 어떻게 처리했는가?
3. Consumer 중복 수신은 어떻게 막았는가?
4. 메시지 처리 실패는 언제 retry하고 언제 DLT로 보내는가?
5. DLT 메시지는 누가, 어떤 기준으로 재처리하는가?
6. 이벤트 순서가 중요한 경우 key를 어떻게 설계했는가?
7. consumer lag가 증가하면 어떤 운영 판단을 하는가?
8. 스키마 변경으로 consumer가 깨지는 문제는 어떻게 막을 것인가?
9. Jenkins나 외부 API 장애가 전체 시스템에 어떻게 전파되지 않게 했는가?
10. 장애 후 이벤트 replay로 무엇을 복구할 수 있는가?
```

## 6. 깊게 팔 키워드 (압축)

```text
Kafka Core
Topic / Partition / Offset / Consumer Group / Rebalance / Retention / Log Compaction / Replication / ISR / KRaft

Producer
acks / retries / linger.ms / batch.size / compression.type / idempotence / transactional.id

Consumer
enable.auto.commit / manual ack / max.poll.records / max.poll.interval.ms / session.timeout.ms / heartbeat.interval.ms / partition assignment

Reliability
At-most-once / At-least-once / Exactly-once / Idempotent Consumer / Outbox Pattern / Inbox Pattern / Retry Topic / DLT

Operations
Lag Monitoring / Broker Metrics / Topic Config / ACL / SASL/SCRAM / mTLS / Quotas / Backup·Restore / Disaster Recovery

Redpanda
rpk / Redpanda Console / Kafka Compatibility / Schema Registry / Redpanda Metrics / Tiered Storage / Single Binary Architecture

Stream/Integration
Kafka Streams / KTable / KStream / Windowing / State Store / Changelog Topic / CDC / Debezium / Source·Sink Connector
```

## 7. 면접/포트폴리오 설명

> Kafka/Redpanda 를 단순 메시지 큐로 쓰지 않고 이벤트 발행·중복 방지·재시도·DLT·Lag 관측·스키마 계약까지 포함한 EventOps 플랫폼으로 설계했습니다. DB↔Kafka dual-write 는 Outbox 로 완화, Consumer 중복은 Inbox 테이블 + event_id unique key 로 해결. 처리 실패는 예외 유형에 따라 retry 가능 실패와 DLT 행 실패를 분리하고, DLT 메시지는 운영 API 에서 조회·재처리. consumer group offset 과 log end offset 을 비교해 lag 를 계산하고 특정 partition 만 밀리는 key skew 까지 관측했습니다.

"Kafka 써봤습니다" 가 아니라 **"장애가 나도 멈추지 않고, 실패해도 다시 처리할 수 있으며, 시간이 지나도 추적 가능한 이벤트 기반 운영 시스템을 설계해봤다"** 가 된다.

## 출처

- [Apache Kafka Blog](https://kafka.apache.org/blog)
- [Apache Kafka Introduction](https://kafka.apache.org/intro/)
- [Redpanda Kafka Compatibility](https://docs.redpanda.com/current/develop/kafka-clients/)
- [Spring Kafka Non-Blocking Retries](https://docs.spring.io/spring-kafka/reference/retrytopic.html)
- [Spring Kafka Retry Pattern](https://docs.spring.io/spring-kafka/reference/retrytopic/how-the-pattern-works.html)
- [Spring Kafka Exactly Once Semantics](https://docs.spring.io/spring-kafka/reference/kafka/exactly-once.html)
- [Redpanda Transactions](https://docs.redpanda.com/cloud-data-platform/develop/transactions/)
- [Redpanda Schema Registry](https://docs.redpanda.com/current/manage/schema-reg/)
- [Redpanda Schema Registry API](https://docs.redpanda.com/current/manage/schema-reg/schema-reg-api/)
- [Redpanda Tiered Storage](https://docs.redpanda.com/streaming/current/manage/tiered-storage/)
