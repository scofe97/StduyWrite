---
title: 04_messaging MOC
tags: [moc, messaging, kafka]
status: final
related: []
updated: 2026-05-23
---

# 04_messaging — 이벤트 기반 메시징

> Kafka·Redpanda·Avro·Schema Registry 같은 메시징 구현 기술과 EDA 적용 문서를 모은 영역. 분산 시스템의 일반 이론(CAP, Saga 보상 트랜잭션의 구조 일반론)은 `05_data/`로, EDA 원칙·결정 기준 같은 *이론*은 [`../03_architecture/04_edd/`](../03_architecture/04_edd/)로 분리돼 있다. 여기는 도구 레벨의 구체적 선택(예: Producer idempotent 옵션 튜닝, Confluent wire format, Spring Kafka concurrency 운영)을 다룬다.

## 학습 흐름

01 메시지 모델·계약 → 02 토픽 설계 → 03 브로커 아키텍처 → 04 일관성 패턴 → 05 스트림 처리 → 06 CQRS·이벤트 소싱 → (심화) [`09_advanced/`](09_advanced/)

각 폴더 안에서는 카테고리 안 첫 두 자리(예: `01-01`, `01-02` …) 순서로 읽으면 *개념 → 코드 디테일 → 운영*의 진행이 자연스럽다. 처음 읽을 때는 각 폴더의 `01` 문서만 따라가도 전체 골격이 잡힌다.

> **EDA 사고 모델·요청-응답 통합 같은 *EDA 도입부*는 이 폴더에서 제외되어 [`../03_architecture/04_edd/05_KafkaApplied/`](../03_architecture/04_edd/05_KafkaApplied/)로 이동했다 (2026-05-23 재구성).** 이론 측 `04_edd`와 한 자리에서 같이 본다.

## 폴더 구조와 인덱스

### 01_MessageContract — 메시지 모델·계약

이벤트의 *형태와 의미*를 어떻게 정의하고 진화시키는가. Envelope/Payload 분리, Avro·Schema Registry, CloudEvents 헤더, trace 메타데이터.

- [01-01.EIP Message Pattern](01_MessageContract/01-01.EIP%20Message%20Pattern.md) — Command/Document/Event 분류와 의도 표현
- [01-02.Schema Registry](01_MessageContract/01-02.Schema%20Registry.md) — 메시지 계약을 인프라 수준에서 강제하는 중앙 저장소
- [01-03.Avro](01_MessageContract/01-03.Avro.md) — 스키마 분리 바이너리 직렬화와 Confluent wire format
- [01-04.EventEnvelope 적용](01_MessageContract/01-04.EventEnvelope%20적용.md) — 메타데이터 표준화와 CloudEvents
- [01-05.Avro 직렬화 예외처리 전략](01_MessageContract/01-05.Avro%20직렬화%20예외처리%20전략.md) — 정합성이 깨지는 두 시점과 대응
- [01-06.Avro 스키마 진화 패턴](01_MessageContract/01-06.Avro%20스키마%20진화%20패턴.md) — 호환성 모드와 배포 순서, 필드 변경 안전 규칙
- [01-07.한 토픽 다수 message 형태](01_MessageContract/01-07.한%20토픽%20다수%20message%20형태.md) — RecordNameStrategy로 한 토픽에 별개 Avro record 공존시키기
- [01-08.Avro Consumer 수신 패턴](01_MessageContract/01-08.Avro%20Consumer%20수신%20패턴.md) — 앱 내부 Avro vs 외부 JSON, 토픽 분리 원칙
- [01-09.CloudEventsHeaderInterceptor](01_MessageContract/01-09.CloudEventsHeaderInterceptor.md) — Envelope 공통 헤더 자동 부착, TPS 코드의 인터셉터 풀버전
- [01-10.trace-id와 traceparent](01_MessageContract/01-10.trace-id와%20traceparent.md) — MDC 운영용 vs W3C Trace Context 표준

### 02_TopicDesign — 토픽 설계

토픽을 단계 사이의 *인터페이스*로 다루는 방식. 명명·파티션·키 선택의 트레이드오프와 명세 도구.

- [02-01.토픽 디자인](02_TopicDesign/02-01.토픽%20디자인.md) — 명명 규칙, 파티션 수, 키 선택의 트레이드오프
- [02-02.토픽 파이프라인](02_TopicDesign/02-02.토픽%20파이프라인.md) — 다단계 처리에서 토픽을 단계 사이의 인터페이스로
- [02-03.AsyncAPI 명세](02_TopicDesign/02-03.AsyncAPI%20명세.md) — 토픽 계약을 코드 외부에 명세로 고정하기
- [02-04.TopicConfig와 파티션 설계](02_TopicDesign/02-04.TopicConfig와%20파티션%20설계.md) — 토픽 정의·파티션 수가 소비 병렬성과 어떻게 연결되는지

### 03_BrokerArchitecture — 브로커 아키텍처와 Spring Kafka 운영

큐 아키텍처·리더 선출·Consumer Group 같은 *도구 원리*와, Spring Kafka 측 *운영 디테일* (concurrency, Manual Ack, Batch Listener, config 5종)을 함께 둔다.

- [03-01.메시지 큐 아키텍처](03_BrokerArchitecture/03-01.메시지%20큐%20아키텍처.md) — 분산 커밋 로그라는 구조의 의미
- [03-02.리더 선출](03_BrokerArchitecture/03-02.리더%20선출.md) — Raft 합의 프로토콜의 3가지 역할
- [03-03.Consumer Group](03_BrokerArchitecture/03-03.Consumer%20Group.md) — 발행·소비 기본 구조와 그룹 프로토콜
- [03-04.리밸런스 프로토콜](03_BrokerArchitecture/03-04.리밸런스%20프로토콜.md) — Stop-the-World 트리거와 점진적 리밸런스
- [03-05.Redpanda 아키텍처](03_BrokerArchitecture/03-05.Redpanda%20아키텍처.md) — 단일 바이너리·Raft per partition·thread-per-core
- [03-06.Redpanda Console 인증](03_BrokerArchitecture/03-06.Redpanda%20Console%20인증.md) — 무료 라이선스에서 게이트를 세우는 4가지 옵션
- [03-07.Kafka·Redpanda SASL 인증](03_BrokerArchitecture/03-07.Kafka·Redpanda%20SASL%20인증.md) — 브로커 본체에 SASL/ACL/TLS로 인증·인가
- [03-08.Kafka 공통 정책 스타터 패턴](03_BrokerArchitecture/03-08.Kafka%20공통%20정책%20스타터%20패턴.md) — retry·DLT·로그·메트릭 정책을 starter로 묶기
- [03-09.Spring Kafka 운영 고급](03_BrokerArchitecture/03-09.Spring%20Kafka%20운영%20고급.md) — Vertical scaling(`concurrency`), 런타임 컨슈머, blocking vs non-blocking retry
- [03-10.Manual Ack와 Offset Commit 정책](03_BrokerArchitecture/03-10.Manual%20Ack와%20Offset%20Commit%20정책.md) — Auto commit vs Manual ack 결정 기준
- [03-11.Batch Listener와 부분 실패 처리](03_BrokerArchitecture/03-11.Batch%20Listener와%20부분%20실패%20처리.md) — 단건 vs Batch, 부분 실패 패턴 3가지
- [03-12.message-lib config 5개 클래스 종합](03_BrokerArchitecture/03-12.message-lib%20config%205개%20클래스%20종합.md) — config 다섯 클래스의 기동 순서·책임·상호작용
- [03-13.message-lib config 학습 검증](03_BrokerArchitecture/03-13.message-lib%20config%20학습%20검증.md) — config 종합 문서 자체의 학습 검증 노트
- [03-14.message-lib config 운영 이식 가이드](03_BrokerArchitecture/03-14.message-lib%20config%20운영%20이식%20가이드.md) — 다른 프로젝트로 옮길 때의 체크리스트

### 04_ConsistencyPattern — 일관성 패턴·예외 처리

분산 트랜잭션 대안(Saga·Outbox·Inbox·CDC)과, 그 운영을 받쳐주는 *예외 처리 인프라*(DLT·DlqConsumer·Backoff·KafkaErrorConfig 사고 회고)를 한 폴더에 모음.

- [04-01.Choreography Saga](04_ConsistencyPattern/04-01.Choreography%20Saga.md) — 중앙 조정자 없는 자율 협력 워크플로우
- [04-02.Orchestration Saga](04_ConsistencyPattern/04-02.Orchestration%20Saga.md) — 명시적 조정자가 단계를 지시하는 방식
- [04-03.Outbox](04_ConsistencyPattern/04-03.Outbox.md) — DB 트랜잭션과 이벤트 발행의 원자성
- [04-04.Outbox 스케일링](04_ConsistencyPattern/04-04.Outbox%20스케일링.md) — 폴러 베이스라인 측정과 병렬화
- [04-05.Inbox](04_ConsistencyPattern/04-05.Inbox.md) — 소비 측 멱등성과 후속 처리 분리
- [04-06.CDC](04_ConsistencyPattern/04-06.CDC.md) — Debezium 기반 변경 데이터 캡처
- [04-07.Inbox 트랜잭션 오염과 멱등 어댑터](04_ConsistencyPattern/04-07.Inbox%20트랜잭션%20오염과%20멱등%20어댑터.md) — 멱등 INSERT의 트랜잭션 오염
- [04-08.컨슈머 진입점 트랜잭션 경계와 Inbox의 사정거리](04_ConsistencyPattern/04-08.컨슈머%20진입점%20트랜잭션%20경계와%20Inbox의%20사정거리.md) — 영수증 vs 실행 큐 분리
- [04-09.Exactly-once 의미론과 Consumer Idempotency](04_ConsistencyPattern/04-09.Exactly-once%20의미론과%20Consumer%20Idempotency.md) — Kafka EOS의 실제 범위와 DB가 끼면 깨지는 이유
- [04-10.Spring Kafka DLT와 Producer Config](04_ConsistencyPattern/04-10.Spring%20Kafka%20DLT와%20Producer%20Config.md) — `DefaultErrorHandler + DeadLetterPublishingRecoverer` 흐름
- [04-11.DlqConsumer](04_ConsistencyPattern/04-11.DlqConsumer.md) — DLQ 끝단 소비자
- [04-12.Kafka 예외 처리 통합](04_ConsistencyPattern/04-12.Kafka%20예외%20처리%20통합.md) — `KafkaErrorConfig`를 축으로 한 통합 가이드
- [04-13.KafkaErrorConfig DLT 헤더 폭증 사고](04_ConsistencyPattern/04-13.KafkaErrorConfig%20DLT%20헤더%20폭증%20사고.md) — 2026-05-14 무한 루프 사고 회고
- [04-14.Backoff 전략 비교와 선택](04_ConsistencyPattern/04-14.Backoff%20전략%20비교와%20선택.md) — Fixed/Exponential/WithMaxRetries 곡선과 jitter

### 05_StreamProcessing — 스트림 처리

- [05-01.Kafka Streams](05_StreamProcessing/05-01.Kafka%20Streams.md) — 배치와 다른 스트림 처리의 사고 모델
- [05-02.Kafka Streams Spring Boot](05_StreamProcessing/05-02.Kafka%20Streams%20Spring%20Boot.md) — `@EnableKafkaStreams` 통합 디테일

### 06_CQRS_EventSourcing — CQRS와 이벤트 소싱

- [06-01.Kafka CQRS](06_CQRS_EventSourcing/06-01.Kafka%20CQRS.md) — 읽기와 쓰기 모델의 분리
- [06-02.Event Sourcing](06_CQRS_EventSourcing/06-02.Event%20Sourcing.md) — 상태 대신 이벤트의 시계열을 진실의 출처로

## 실 사용 코드

이 학습 트리의 패턴은 `okestro/tps-gitlab2`의 다음 모듈에서 실제로 동작한다.

- `message-lib`: Outbox 라이브러리, `EventPublisher`, `AvroSerializer` (TPS 공통 의존)
- `executor`: 결과 이벤트 발행 측
- `operator`: 명령 발행·결과 소비 측 (Saga 오케스트레이터 역할)

상세 매핑은 각 문서 말미의 "TPS 적용 사례" 박스 참조. message-lib 코드 디테일은 본 폴더 안에 *주제별로* 흡수돼 있다 (옛 `spring/` 서브폴더는 2026-05-23 해체 — 자세한 매핑은 [`spring/README.md`](spring/README.md)).

## 하위 컬렉션

- [`01_Connect/`](01_Connect/) — Redpanda Connect 커넥터 실습
- [`08_workflow/`](08_workflow/) — Temporal 기반 Workflow 오케스트레이션과 EDA+CDC+Temporal 통합 아키텍처
- [`09_advanced/`](09_advanced/) — Outbox 변종 비교, Saga 엔진 비교, 스트림 처리 진화, 스키마 거버넌스

## 경계 기준 (2026-05-23 재정의)

| 영역 | 다루는 것 |
|------|----------|
| 본 폴더 (`04_messaging/`) | Kafka·Redpanda·Avro 도구 레벨 선택과 Spring Kafka 운영. EDA·DDD를 도구로 *적용*할 때의 패턴 |
| [`../03_architecture/04_edd/`](../03_architecture/04_edd/) | EDA 이론·원칙·결정 기준 (Why 토폴로지·단일 작성자·CQRS 모델). EDA의 *적용* 측은 `04_edd/05_KafkaApplied/`에 같이 둠 |
| `05_data/` | 분산 시스템 일반 이론 (CAP, Saga 보상 트랜잭션 구조 일반론) |

> 2026-05-23 변경 요약: spring/ 서브폴더(기술 출처 축) 해체 → 6개 주제 폴더로 재배치. EDA 도입부 3개는 03_architecture/04_edd/05_KafkaApplied/로 이동해 이론과 한 자리에서 본다.
