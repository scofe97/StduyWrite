---
title: 04_messaging MOC
tags: [moc, messaging, kafka]
status: final
related: []
updated: 2026-05-23
---

# 04_messaging — 이벤트 기반 메시징

> Kafka·Redpanda·Avro·Schema Registry 같은 메시징 구현 기술과 EDA 적용 문서를 모은 영역입니다. 분산 시스템의 일반 이론(CAP, Saga 보상 트랜잭션의 구조 일반론)은 `05_data/`로, EDA 원칙·결정 기준 같은 이론은 [`../03_architecture/05_edd/`](../03_architecture/05_edd/)로 분리돼 있습니다. 여기서는 도구 레벨의 구체적 선택(예: Producer idempotent 옵션 튜닝, Confluent wire format, Spring Kafka concurrency 운영)을 다룹니다.

## 학습 흐름

01 커넥터 → 02 메시지 모델·계약 → 03 토픽 설계 → 04 브로커 아키텍처 → 05 일관성 패턴 → 06 스트림 처리 → 07 CQRS·이벤트 소싱 → (심화) [`08_advanced/`](08_advanced/)

각 폴더 안에서는 카테고리 안 첫 두 자리(예: `01-01`, `01-02` …) 순서로 읽으면 개념에서 코드 디테일을 거쳐 운영으로 진행이 자연스럽습니다. 처음 읽을 때는 각 폴더의 `01` 문서만 따라가도 전체 골격이 잡힙니다.

> EDA 사고 모델·요청-응답 통합 같은 EDA 도입부는 이 폴더에서 제외되어 [`../03_architecture/05_edd/`](../03_architecture/05_edd/)로 이동했습니다(2026-05-23 재구성). 이론 측 `05_edd`와 한 자리에서 같이 봅니다.

## 폴더 구조와 인덱스

### 01_Connect — 커넥터와 데이터 통합

외부 시스템과 토픽 사이를 잇는 커넥터를 다룹니다. Redpanda Connect의 개념·문법·실습과 운영 측 에러 핸들링·고가용성을 포함합니다.

- [01-01. SourceSink](01_Connect/01-01.%20SourceSink%20.md) — Source와 Sink의 기본 모델
- [01-02.커넥터가 필요한 이유와 실전 사례](01_Connect/01-02.커넥터가%20필요한%20이유와%20실전%20사례.md) — 직접 구현 대신 커넥터를 쓰는 판단 기준
- [02-01.Redpanda Connect 개념](01_Connect/02-01.Redpanda%20Connect%20개념.md) — 파이프라인 구성 요소
- [02-02.Redpanda Connect 문법](01_Connect/02-02.Redpanda%20Connect%20문법.md) — 설정 DSL과 프로세서
- [02-03. 실습 시나리오](01_Connect/02-03.%20실습%20시나리오.md) — 손으로 따라가는 파이프라인 구성
- [03-01.에러 핸들링과 로그 수집](01_Connect/03-01.에러%20핸들링과%20로그%20수집.md) — 실패 경로 설계
- [03-02.장애 복구와 고가용성](01_Connect/03-02.장애%20복구와%20고가용성.md) — 커넥터 운영의 가용성 확보

### 02_MessageContract — 메시지 모델·계약

이벤트의 형태와 의미를 어떻게 정의하고 진화시키는가를 다룹니다. Envelope/Payload 분리, Avro·Schema Registry, CloudEvents 헤더, trace 메타데이터.

- [01-01.EIP Message Pattern](02_MessageContract/01-01.EIP%20Message%20Pattern.md) — Command/Document/Event 분류와 의도 표현
- [01-02.Schema Registry](02_MessageContract/01-02.Schema%20Registry.md) — 메시지 계약을 인프라 수준에서 강제하는 중앙 저장소
- [01-03.Avro](02_MessageContract/01-03.Avro.md) — 스키마 분리 바이너리 직렬화와 Confluent wire format
- [01-04.EventEnvelope 적용](02_MessageContract/01-04.EventEnvelope%20적용.md) — 메타데이터 표준화와 CloudEvents
- [02-01.Avro 직렬화 예외처리 전략](02_MessageContract/02-01.Avro%20직렬화%20예외처리%20전략.md) — 정합성이 깨지는 두 시점과 대응
- [02-02.Avro 스키마 진화 패턴](02_MessageContract/02-02.Avro%20스키마%20진화%20패턴.md) — 호환성 모드와 배포 순서, 필드 변경 안전 규칙
- [02-03.한 토픽 다수 message 형태](02_MessageContract/02-03.한%20토픽%20다수%20message%20형태.md) — RecordNameStrategy로 한 토픽에 별개 Avro record 공존시키기
- [02-04.Avro Consumer 수신 패턴](02_MessageContract/02-04.Avro%20Consumer%20수신%20패턴.md) — 앱 내부 Avro vs 외부 JSON, 토픽 분리 원칙
- [03-01.CloudEventsHeaderInterceptor](02_MessageContract/03-01.CloudEventsHeaderInterceptor.md) — Envelope 공통 헤더 자동 부착, TPS 코드의 인터셉터 풀버전
- [03-02.trace-id와 traceparent](02_MessageContract/03-02.trace-id와%20traceparent.md) — MDC 운영용 vs W3C Trace Context 표준

### 03_TopicDesign — 토픽 설계

토픽을 단계 사이의 인터페이스로 다루는 방식입니다. 명명·파티션·키 선택의 트레이드오프와 명세 도구.

- [01-01.토픽 디자인](03_TopicDesign/01-01.토픽%20디자인.md) — 명명 규칙, 파티션 수, 키 선택의 트레이드오프
- [01-02.토픽 파이프라인](03_TopicDesign/01-02.토픽%20파이프라인.md) — 다단계 처리에서 토픽을 단계 사이의 인터페이스로
- [01-03.AsyncAPI 명세](03_TopicDesign/01-03.AsyncAPI%20명세.md) — 토픽 계약을 코드 외부에 명세로 고정하기
- [01-04.TopicConfig와 파티션 설계](03_TopicDesign/01-04.TopicConfig와%20파티션%20설계.md) — 토픽 정의·파티션 수가 소비 병렬성과 어떻게 연결되는지

### 04_BrokerArchitecture — 브로커 아키텍처와 Spring Kafka 운영

큐 아키텍처·리더 선출·Consumer Group 같은 도구 원리와, Spring Kafka 측 운영 디테일(concurrency, Manual Ack, Batch Listener, config 5종)을 함께 둡니다.

- [01-01.메시지 큐 아키텍처](04_BrokerArchitecture/01-01.메시지%20큐%20아키텍처.md) — 분산 커밋 로그라는 구조의 의미
- [01-02.리더 선출](04_BrokerArchitecture/01-02.리더%20선출.md) — Raft 합의 프로토콜의 3가지 역할
- [01-03.Consumer Group](04_BrokerArchitecture/01-03.Consumer%20Group.md) — 발행·소비 기본 구조와 그룹 프로토콜
- [01-04.리밸런스 프로토콜](04_BrokerArchitecture/01-04.리밸런스%20프로토콜.md) — Stop-the-World 트리거와 점진적 리밸런스 ([시각화](04_BrokerArchitecture/01-04-rebalance.html))
- [01-05.오프셋 커밋 API](04_BrokerArchitecture/01-05.오프셋%20커밋%20API.md) — commitSync·commitAsync·지정 offset 커밋과 중복·유실 방향성 ([시각화](04_BrokerArchitecture/01-05-offset-commit.html))
- [01-06.Consumer poll 루프와 종료](04_BrokerArchitecture/01-06.Consumer%20poll%20루프와%20종료.md) — poll 루프·1 consumer per thread·seek·wakeup 종료
- [01-07.Consumer 설정 심화](04_BrokerArchitecture/01-07.Consumer%20설정%20심화.md) — fetch 크기·타임아웃·client.rack·오프셋 보존
- [02-01.Redpanda 아키텍처](04_BrokerArchitecture/02-01.Redpanda%20아키텍처.md) — 단일 바이너리·Raft per partition·thread-per-core
- [02-02.Redpanda Console 인증](04_BrokerArchitecture/02-02.Redpanda%20Console%20인증.md) — 무료 라이선스에서 게이트를 세우는 4가지 옵션
- [02-03.Kafka·Redpanda SASL 인증](04_BrokerArchitecture/02-03.Kafka·Redpanda%20SASL%20인증.md) — 브로커 본체에 SASL/ACL/TLS로 인증·인가
- [03-01.Kafka 공통 정책 스타터 패턴](04_BrokerArchitecture/03-01.Kafka%20공통%20정책%20스타터%20패턴.md) — retry·DLT·로그·메트릭 정책을 starter로 묶기
- [03-02.Spring Kafka 운영 고급](04_BrokerArchitecture/03-02.Spring%20Kafka%20운영%20고급.md) — Vertical scaling(`concurrency`), 런타임 컨슈머, blocking vs non-blocking retry
- [03-03.Manual Ack와 Offset Commit 정책](04_BrokerArchitecture/03-03.Manual%20Ack와%20Offset%20Commit%20정책.md) — Auto commit vs Manual ack 결정 기준
- [03-04.Batch Listener와 부분 실패 처리](04_BrokerArchitecture/03-04.Batch%20Listener와%20부분%20실패%20처리.md) — 단건 vs Batch, 부분 실패 패턴 3가지
- [03-05.다중 직렬화 컨슈머 구성 3방식](04_BrokerArchitecture/03-05.다중%20직렬화%20컨슈머%20구성%203방식.md) — 한 앱에서 Avro·JSON 동시 소비: 빈 정의 / 어노테이션 오버라이드 / 설정 런타임 생성
- [04-01.message-lib config 5개 클래스 종합](04_BrokerArchitecture/04-01.message-lib%20config%205개%20클래스%20종합.md) — config 다섯 클래스의 기동 순서·책임·상호작용
- [04-02.message-lib config 학습 검증](04_BrokerArchitecture/04-02.message-lib%20config%20학습%20검증.md) — config 종합 문서 자체의 학습 검증 노트
- [04-03.message-lib config 운영 이식 가이드](04_BrokerArchitecture/04-03.message-lib%20config%20운영%20이식%20가이드.md) — 다른 프로젝트로 옮길 때의 체크리스트
- [05-01.Producer 아키텍처](04_BrokerArchitecture/05-01.Producer%20아키텍처.md) — send-path 파이프라인과 ProducerRecord·RecordMetadata 해부
- [05-02.Producer 생성과 전송 모드](04_BrokerArchitecture/05-02.Producer%20생성과%20전송%20모드.md) — 3 필수 설정과 fire-and-forget·동기·비동기 전송, retriable 오류 구분
- [05-03.Producer 파티셔너](04_BrokerArchitecture/05-03.Producer%20파티셔너.md) — key 기반 매핑·sticky(2.4+)·사용자 정의 파티셔너, Consumer 할당과의 구분
- [05-04.Quota와 Throttling](04_BrokerArchitecture/05-04.Quota와%20Throttling.md) — produce·consume·request quota, 동적 설정과 throttling 동작
- [06-01.AdminClient 기초와 토픽 관리](04_BrokerArchitecture/06-01.AdminClient%20기초와%20토픽%20관리.md) — 비동기·결과적 일관성 설계, 생명주기, 토픽 list·describe·create·delete
- [06-02.AdminClient 설정·컨슈머그룹·클러스터](04_BrokerArchitecture/06-02.AdminClient%20설정·컨슈머그룹·클러스터.md) — 설정 describe·수정, 컨슈머 그룹 offset·lag·reset, 클러스터 메타데이터
- [06-03.AdminClient 고급 작업과 테스트](04_BrokerArchitecture/06-03.AdminClient%20고급%20작업과%20테스트.md) — 파티션 추가·레코드 삭제·리더 선출·replica 재배치·MockAdminClient
- [07-01.신뢰성 검증과 모니터링](04_BrokerArchitecture/07-01.신뢰성%20검증과%20모니터링.md) — Kafka 4대 보장, VerifiableProducer/Consumer·Trogdor·Burrow·JMX 3계층 검증

### 05_ConsistencyPattern — 일관성 패턴·예외 처리

분산 트랜잭션 대안(Saga·Outbox·Inbox·CDC)과, 그 운영을 받쳐주는 예외 처리 인프라(DLT·DlqConsumer·Backoff·KafkaErrorConfig 사고 회고)를 한 폴더에 모읍니다.

- [01-01.Choreography Saga](05_ConsistencyPattern/01-01.Choreography%20Saga.md) — 중앙 조정자 없는 자율 협력 워크플로우
- [01-02.Orchestration Saga](05_ConsistencyPattern/01-02.Orchestration%20Saga.md) — 명시적 조정자가 단계를 지시하는 방식
- [02-01.Outbox](05_ConsistencyPattern/02-01.Outbox.md) — DB 트랜잭션과 이벤트 발행의 원자성
- [02-02.Outbox 스케일링](05_ConsistencyPattern/02-02.Outbox%20스케일링.md) — 폴러 베이스라인 측정과 병렬화
- [03-01.Inbox](05_ConsistencyPattern/03-01.Inbox.md) — 소비 측 멱등성과 후속 처리 분리
- [03-02.Inbox 트랜잭션 오염과 멱등 어댑터](05_ConsistencyPattern/03-02.Inbox%20트랜잭션%20오염과%20멱등%20어댑터.md) — 멱등 INSERT의 트랜잭션 오염
- [03-03.컨슈머 진입점 트랜잭션 경계와 Inbox의 사정거리](05_ConsistencyPattern/03-03.컨슈머%20진입점%20트랜잭션%20경계와%20Inbox의%20사정거리.md) — 영수증 vs 실행 큐 분리
- [03-04.Exactly-once 의미론과 Consumer Idempotency](05_ConsistencyPattern/03-04.Exactly-once%20의미론과%20Consumer%20Idempotency.md) — Kafka EOS의 실제 범위와 DB가 끼면 깨지는 이유
- [04-01.CDC](05_ConsistencyPattern/04-01.CDC.md) — Debezium 기반 변경 데이터 캡처
- [05-01.Spring Kafka DLT와 Producer Config](05_ConsistencyPattern/05-01.Spring%20Kafka%20DLT와%20Producer%20Config.md) — `DefaultErrorHandler + DeadLetterPublishingRecoverer` 흐름
- [05-02.DlqConsumer](05_ConsistencyPattern/05-02.DlqConsumer.md) — DLQ 끝단 소비자
- [05-03.Kafka 예외 처리 통합](05_ConsistencyPattern/05-03.Kafka%20예외%20처리%20통합.md) — `KafkaErrorConfig`를 축으로 한 통합 가이드
- [05-04.KafkaErrorConfig DLT 헤더 폭증 사고](05_ConsistencyPattern/05-04.KafkaErrorConfig%20DLT%20헤더%20폭증%20사고.md) — 2026-05-14 무한 루프 사고 회고
- [05-05.Backoff 전략 비교와 선택](05_ConsistencyPattern/05-05.Backoff%20전략%20비교와%20선택.md) — Fixed/Exponential/WithMaxRetries 곡선과 jitter

### 06_StreamProcessing — 스트림 처리

- [01-01.Kafka Streams](06_StreamProcessing/01-01.Kafka%20Streams.md) — 배치와 다른 스트림 처리의 사고 모델
- [01-02.Kafka Streams Spring Boot](06_StreamProcessing/01-02.Kafka%20Streams%20Spring%20Boot.md) — `@EnableKafkaStreams` 통합 디테일

### 07_CQRS_EventSourcing — CQRS와 이벤트 소싱

- [01-01.Kafka CQRS](07_CQRS_EventSourcing/01-01.Kafka%20CQRS.md) — 읽기와 쓰기 모델의 분리
- [01-02.Event Sourcing](07_CQRS_EventSourcing/01-02.Event%20Sourcing.md) — 상태 대신 이벤트의 시계열을 진실의 출처로

## 실 사용 코드

이 학습 트리의 패턴은 `okestro/tps-gitlab2`의 다음 모듈에서 실제로 동작합니다.

- `message-lib`: Outbox 라이브러리, `EventPublisher`, `AvroSerializer` (TPS 공통 의존)
- `executor`: 결과 이벤트 발행 측
- `operator`: 명령 발행·결과 소비 측 (Saga 오케스트레이터 역할)

상세 매핑은 각 문서 말미의 "TPS 적용 사례" 박스를 참조합니다. message-lib 코드 디테일은 본 폴더 안에 주제별로 흡수돼 있습니다(옛 `spring/` 서브폴더는 2026-05-23 해체 후 삭제 — 04_BrokerArchitecture·05_ConsistencyPattern·02_MessageContract 등으로 흩어짐).

## 하위 컬렉션

- [`08_advanced/`](08_advanced/) — 메시징 심화. `01_variants/`(Outbox·Saga·스트림·스키마 변종 비교)와 `02_workflow/`(Temporal 워크플로우 깊이) 두 갈래

## 경계 기준 (2026-05-23 재정의)

| 영역 | 다루는 것 |
|------|----------|
| 본 폴더 (`04_messaging/`) | Kafka·Redpanda·Avro 도구 레벨 선택과 Spring Kafka 운영. EDA·DDD를 도구로 적용할 때의 패턴 |
| [`../03_architecture/05_edd/`](../03_architecture/05_edd/) | EDA 이론·원칙·결정 기준 (Why 토폴로지·단일 작성자·CQRS 모델). EDA의 적용 측은 `05_edd/`에 같이 둠 |
| `05_data/` | 분산 시스템 일반 이론 (CAP, Saga 보상 트랜잭션 구조 일반론) |

> 2026-05-23 변경 요약: `01_MessageContract`와 `01_Connect`가 둘 다 `01` prefix로 충돌해 `01_Connect`를 빼고 나머지 카테고리를 한 칸씩 밀어 prefix 유일성을 확보했습니다(02_MessageContract … 07_CQRS_EventSourcing). 옛 `08_workflow`와 `09_advanced`는 둘 다 심화 성격이라 `08_advanced/` 한 폴더로 흡수했습니다(`01_variants/`, `02_workflow/` 두 갈래). 단행본 실습 폴더 명명은 `_code/`에서 `_practice/`로 통일했습니다.
