---
title: 05_messaging MOC
tags: [moc, messaging, kafka]
status: final
related: []
updated: 2026-05-09
---

# 05_messaging — 이벤트 기반 메시징

> Kafka·Redpanda·Avro·Schema Registry 같은 메시징 구현 기술과 EDA 적용 문서를 모은 영역. 분산 시스템의 일반 이론(CAP, Saga 보상 트랜잭션의 구조 일반론)은 `04_distributed/`로, 여기는 도구 레벨의 구체적 선택(예: Producer idempotent 옵션 튜닝, Confluent wire format)을 다룬다.

## 학습 흐름

01 EDA & 통합 → 02 메시지 모델·계약 → 03 토픽 설계 → 04 브로커 아키텍처 → 05 일관성 패턴 → 06 스트림 처리 → 07 CQRS·이벤트 소싱 → (심화) [09_advanced](09_advanced/)

각 그룹은 "왜 필요한가"부터 시작해 구체적인 구현 패턴까지 점진적으로 내려간다. 처음 읽을 때는 그룹별 첫 문서(01-01, 02-01, 03-01 …)만 따라가도 전체 골격이 잡힌다.

## 주제별 인덱스

### 01 EDA & 통합

- [01-01.EDA 기초](01-01.EDA%20기초.md) — 전통 동기 아키텍처의 한계와 이벤트 기반 사고로의 전환
- [01-02.EDA 기반 요청응답 통합](01-02.EDA%20기반%20요청응답%20통합.md) — 비동기 토픽 위에 요청-응답 의미를 얹는 6가지 구조
- [01-03.202 Accepted + Polling 패턴](01-03.202%20Accepted%20+%20Polling%20패턴.md) — 오래 걸리는 작업을 동기 API 인터페이스로 노출하는 표준 패턴

### 02 메시지 모델·계약

- [02-01.EIP Message Pattern](02-01.EIP%20Message%20Pattern.md) — Command/Document/Event 분류와 의도 표현
- [02-02.Schema Registry](02-02.Schema%20Registry.md) — 메시지 계약을 인프라 수준에서 강제하는 중앙 저장소
- [02-03.Avro](02-03.Avro.md) — 스키마 분리 바이너리 직렬화와 Confluent wire format
- [02-04.EventEnvelope 적용](02-04.EventEnvelope%20적용.md) — 메타데이터 표준화와 CloudEvents
- [02-05.Avro 직렬화 예외처리 전략](02-05.Avro%20직렬화%20예외처리%20전략.md) — 정합성이 깨지는 두 시점과 대응
- [02-06.Avro 스키마 진화 패턴](02-06.Avro%20스키마%20진화%20패턴.md) — 호환성 모드와 배포 순서, 필드 변경 안전 규칙

### 03 토픽 설계

- [03-01.토픽 디자인](03-01.토픽%20디자인.md) — 명명 규칙, 파티션 수, 키 선택의 트레이드오프
- [03-02.토픽 파이프라인](03-02.토픽%20파이프라인.md) — 다단계 처리에서 토픽을 단계 사이의 인터페이스로 쓰기
- [03-03.AsyncAPI 명세](03-03.AsyncAPI%20명세.md) — 토픽 계약을 코드 외부에 명세로 고정하기
- [03-04.한 토픽 다수 message 형태](03-04.한%20토픽%20다수%20message%20형태.md) — RecordNameStrategy로 한 토픽에 별개 Avro record 공존시키기

### 04 브로커 아키텍처

- [04-01.메시지 큐 아키텍처](04-01.메시지%20큐%20아키텍처.md) — 분산 커밋 로그라는 구조의 의미
- [04-02.리더 선출](04-02.리더%20선출.md) — Raft 합의 프로토콜의 3가지 역할
- [04-03.Consumer Group](04-03.Consumer%20Group.md) — 발행·소비 기본 구조와 그룹 프로토콜
- [04-04.리밸런스 프로토콜](04-04.리밸런스%20프로토콜.md) — Stop-the-World 트리거와 점진적 리밸런스
- [04-05.Redpanda 아키텍처](04-05.Redpanda%20아키텍처.md) — 단일 바이너리·Raft per partition·thread-per-core
- [04-06.Redpanda Console 인증](04-06.Redpanda%20Console%20인증.md) — 무료 라이선스에서 게이트를 세우는 4가지 옵션
- [04-07.Kafka·Redpanda SASL 인증](04-07.Kafka·Redpanda%20SASL%20인증.md) — 메시지 큐 본체(브로커)에 SASL/ACL/TLS로 인증·인가를 다는 표준 경로
- [04-08.Exactly-once 의미론과 Consumer Idempotency](04-08.Exactly-once%20의미론과%20Consumer%20Idempotency.md) — Kafka EOS의 실제 범위와 DB가 끼면 깨지는 이유, Inbox 멱등 테이블 패턴
- [04-10.Kafka 공통 정책 스타터 패턴](04-10.Kafka%20공통%20정책%20스타터%20패턴.md) — 조직 차원에서 retry·DLT·로그·메트릭 정책을 starter로 묶어 강제·권고를 구분하는 거버넌스 패턴. EnvironmentPostProcessor와 AutoConfiguration 두 경로 활용

### 05 일관성 패턴

- [05-01.Choreography Saga](05-01.Choreography%20Saga.md) — 중앙 조정자 없는 자율 협력 워크플로우
- [05-02.Orchestration Saga](05-02.Orchestration%20Saga.md) — 명시적 조정자가 단계를 지시하는 방식
- [05-03.Outbox](05-03.Outbox.md) — DB 트랜잭션과 이벤트 발행의 원자성
- [05-04.Outbox 스케일링](05-04.Outbox%20스케일링.md) — 폴러 베이스라인 측정과 병렬화 전략
- [05-05.Inbox](05-05.Inbox.md) — 소비 측 멱등성과 후속 처리 분리
- [05-06.CDC](05-06.CDC.md) — Debezium 기반 변경 데이터 캡처
- [05-07.Inbox 트랜잭션 오염과 멱등 어댑터](05-07.Inbox%20트랜잭션%20오염과%20멱등%20어댑터.md) — 멱등 INSERT의 트랜잭션 오염과 INSERT IGNORE 어댑터
- [05-08.컨슈머 진입점 트랜잭션 경계와 Inbox의 사정거리](05-08.컨슈머%20진입점%20트랜잭션%20경계와%20Inbox의%20사정거리.md) — 영수증 vs 실행 큐 분리, 외부 호출 멱등성과의 직교 관계

### 06 스트림 처리

- [06-01.Kafka Streams](06-01.Kafka%20Streams.md) — 배치와 다른 스트림 처리의 사고 모델
- [06-02.Kafka Streams Spring Boot](06-02.Kafka%20Streams%20Spring%20Boot.md) — `@EnableKafkaStreams` 통합 디테일

### 07 CQRS·이벤트 소싱

- [07-01.Kafka CQRS](07-01.Kafka%20CQRS.md) — 읽기와 쓰기 모델의 분리
- [07-02.Event Sourcing](07-02.Event%20Sourcing.md) — 상태 대신 이벤트의 시계열을 진실의 출처로

## 실 사용 코드

이 학습 트리의 패턴은 `okestro/tps-gitlab2`의 다음 모듈에서 실제로 동작한다.

- `message-lib`: Outbox 라이브러리, `EventPublisher`, `AvroSerializer` (TPS 공통 의존)
- `executor`: 결과 이벤트 발행 측
- `operator`: 명령 발행·결과 소비 측 (Saga 오케스트레이터 역할)

상세 매핑은 각 문서 말미의 "TPS 적용 사례" 박스 참조. 코드 레벨 풀 해설은 [`spring/`](spring/) 폴더의 대응 문서에 있다.

## 하위 컬렉션

- [`01_Connect/`](01_Connect/) — Redpanda Connect 커넥터 실습
- [`02_DAG/`](02_DAG/) — DAG 워크플로우 엔진 학습
- [`spring/`](spring/) — TPS `message-lib` 코드 디테일

## 심화 자료

→ [`09_advanced/`](09_advanced/) — Outbox 변종 비교, Saga 엔진 비교, 스트림 처리 진화, 스키마 거버넌스

## 경계 기준

분산 시스템의 이론(Saga의 보상 트랜잭션 구조 일반론, CAP)은 `04_distributed/`에 속한다. 여기는 "Kafka Producer idempotent 옵션 튜닝"처럼 도구 레벨에서 구체적인 선택을 다룬다. `05-x` Saga 계열은 이론 측면이 강하면 추후 `04_distributed/`로 일부가 분할될 수 있다.
