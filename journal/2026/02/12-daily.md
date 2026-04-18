# 학습 일지 - 2026-02-12 (수요일)

## 오늘의 목표
- [x] Redpanda 03-spring-boot-integration/01-basic-setup.md 학습
- [x] 01-basic-setup.md 문서 분리 (09, 10, 11 챕터 신규 생성)
- [x] Redpanda 03-spring-boot-integration/02-producer-consumer.md 학습 (Producer/Consumer)

---

## 학습 내용

### 1. Spring Boot + Redpanda 기본 연결 설정 (01-basic-setup.md)

**범위**: 의존성, application.yml 설정 카탈로그(Producer/Consumer/Listener), Configuration 클래스, 연결 아키텍처, 토픽 관리(KafkaAdmin), 프로파일별 설정 전략, Redpanda vs Kafka 차이

#### 핵심 배움

**Spring Kafka의 2계층 커밋 메커니즘**: `enable-auto-commit: false`만 설정하면 Kafka 클라이언트 레벨의 자동 커밋만 비활성화된다. Spring Kafka의 `KafkaMessageListenerContainer`는 기본 `AckMode.BATCH`로 자체 커밋을 수행하므로, 진정한 수동 커밋을 위해서는 `enable-auto-commit: false` + `ack-mode: manual` **두 가지를 반드시 함께** 설정해야 한다.

**Producer 설정의 핵심 축**: 신뢰성(`acks`, `enable.idempotence`, `retries`)과 성능(`batch-size`, `linger.ms`, `compression.type`, `max.in.flight.requests`)은 트레이드오프 관계다. `enable.idempotence=true`로 설정하면 `acks=all`이 강제되고 `max.in.flight.requests`는 최대 5로 제한되며, PID+시퀀스 번호로 중복 전송을 방지한다.

**KafkaAdmin의 토픽 관리**: 애플리케이션 시작 시 `NewTopic` Bean을 탐색하여 자동 생성한다. `modify-topic-configs: true`는 주의가 필요한데, 배포 시점에 retention 변경으로 기존 데이터가 삭제될 수 있다. 파티션 수는 증가만 가능하고 감소/복제 계수 변경은 불가하다.

**Redpanda vs Kafka 설정 차이**: 대부분 동일하지만 핵심 차이 3가지. (1) ZooKeeper 설정 불필요 - Raft 기반 자체 메타데이터 관리, (2) Schema Registry URL이 브로커에 내장 - 별도 서비스 불필요, (3) Testcontainers 시작 속도 2배 빠름 (7-10초 vs 15-20초). 클러스터 구성도 Kafka(6 프로세스) vs Redpanda(3 프로세스)로 단순하다.

**프로파일별 설정 전략**: `application-{profile}.yml`로 환경별 설정을 분리한다. 로컬에서는 `auto.register.schemas: true`, 프로덕션에서는 `false`로 설정하여 CI/CD를 통해서만 스키마 등록을 허용한다.

### 2. Spring Kafka Producer/Consumer 심화 (02-producer-consumer.md)

**범위**: 동기/비동기 전송, 파티션/헤더 전송, 자동 헤더 주입(Interceptor/Wrapper/Micrometer Tracing), 배치 Consumer/Factory, DefaultErrorHandler, @RetryableTopic, 리밸런싱, 토픽 관리 전략

#### 핵심 배움

**동기 전송이 필요한 이유**: 비동기 콜백이 있어도 **콜백 시점에 호출 흐름으로 돌아갈 수 없다**는 것이 핵심. API 응답에 전송 결과를 포함해야 하거나, 메시지 간 순서 의존성이 있거나, 트랜잭션 경계 내에서 전송 성공을 보장해야 할 때 동기 전송을 사용한다.

**자동 헤더 주입 3가지 방식**: (1) `ProducerInterceptor` — Kafka 네이티브, Spring DI 불가, 다중 등록 시 쉼표 구분으로 체이닝. (2) `KafkaTemplate` 래퍼 — Spring DI 가능하지만 KafkaTemplate 의존. (3) Micrometer Tracing — 코드 0줄, Spring Boot 자동 설정이 ProducerFactory/ConsumerFactory를 프록시하여 W3C traceparent 헤더를 자동 주입/추출.

**DefaultErrorHandler — Consumer 에러 처리의 표준**: Bean으로 등록하면 `KafkaAutoConfiguration`이 모든 Listener Container에 자동 적용. 구성 요소는 BackOff(재시도 전략) + ConsumerRecordRecoverer(복구 처리). 등록하지 않으면 기본값(10회 재시도, Recoverer 없음)이 적용되므로 프로덕션에서는 반드시 직접 등록해야 한다.

**DefaultErrorHandler vs @RetryableTopic — 둘 다 함께 쓴다**: DefaultErrorHandler는 **전역 기본 정책**(블록킹 재시도), @RetryableTopic은 **핵심 토픽의 논블록킹 재시도**. @DltHandler에서도 실패하면 DefaultErrorHandler가 최후의 안전망으로 동작한다. 순서가 중요한 곳(재고 차감, CDC)은 DefaultErrorHandler, 블록킹이 치명적인 곳(주문/결제, 알림)은 @RetryableTopic.

**미들웨어 장애 시 리밸런싱은 무의미하다**: Consumer가 살아있어도 `poll()` 간격이 `max.poll.interval.ms`(5분)를 초과하면 리밸런싱이 발생한다. 그런데 DB나 외부 API 장애가 원인이면 다른 Consumer로 재배정해도 같은 장애를 겪어 **Rebalance Storm**이 발생한다. 올바른 대응은 Circuit Breaker(빠른 실패)나 Consumer Pause(`KafkaListenerEndpointRegistry.pause()` — poll은 유지하되 레코드를 가져오지 않음).

**auto.create.topics.enable=false가 프로덕션 표준**: Confluent Cloud/Redpanda 모두 기본값 false. 실제 사고: Project44(DLT 자동 생성 → 파티션 1개로 디스크 포화), Wikimedia(retry 토픽 무한 루프). DLT/Retry 토픽은 @RetryableTopic의 `autoCreateTopics`(KafkaAdmin 경유, 브로커 auto.create와 무관) 또는 Factory 패턴으로 일괄 생성. 한국 IT 기업(LINE, 카카오, 배민, 네이버)도 모두 명시적 토픽 관리 채택.

---

## Docs 완료
- **경로**: `poc/08_MessageQueue/red-panda/learning/03-spring-boot-integration/01-basic-setup.md`
  - **핵심 개념**: 2계층 커밋(Kafka 클라이언트 + Spring AckMode), Producer 설정 카탈로그, KafkaAdmin 토픽 관리, Redpanda 설정 차이
- **경로**: `poc/08_MessageQueue/red-panda/learning/03-spring-boot-integration/09-anti-patterns-troubleshooting.md` (신규)
  - **핵심 개념**: auto-commit 혼용 안티패턴, schema 자동등록 위험, 토픽 자동생성 의존, Consumer 리밸런스 메커니즘, session.timeout vs max.poll.interval
- **경로**: `poc/08_MessageQueue/red-panda/learning/03-spring-boot-integration/10-manual-commit-deep-dive.md` (신규)
  - **핵심 개념**: MANUAL vs MANUAL_IMMEDIATE, nack() API, 배치 리스너 수동 커밋, acknowledge() 누락 함정
- **경로**: `poc/08_MessageQueue/red-panda/learning/03-spring-boot-integration/11-production-case-studies.md` (신규)
  - **핵심 개념**: 토스 이중 Producer(acks=0/all), LINE 멀티테넌시 쿼터, 사람인 리밸런스 트러블슈팅
- **경로**: `poc/08_MessageQueue/red-panda/learning/03-spring-boot-integration/02-producer-consumer.md` (대폭 보강)
  - **추가 내용**: 동기/비동기 전송 비교, 파티션/헤더 전송 이유, 자동 헤더 주입(Interceptor/Wrapper/Micrometer Tracing), traceparent W3C 형식, 배치 Factory(YAML vs Factory), 타입 불일치 동작, DefaultErrorHandler 상세(Bean 등록 원리, BackOff, 예외 제외, 실무 비교), 리밸런싱(애플리케이션 지연, 미들웨어 장애 대응), @RetryableTopic 토픽 생성 메커니즘
- **경로**: `poc/08_MessageQueue/red-panda/learning/03-spring-boot-integration/01-basic-setup.md` (보강)
  - **추가 내용**: Listener 설정 상세(ack-mode 7종, concurrency, type), auto.create.topics.enable 실제 사고 사례, DLT/Retry 토픽 관리 4가지 접근법, 한국 IT 기업 사례, NewTopic Bean vs IaC 분리 이유
- **경로**: `poc/08_MessageQueue/red-panda/learning/03-spring-boot-integration/08-transaction-patterns.md` (보강)
  - **추가 내용**: Dual Write Problem, Outbox 패턴 보강, Transactional Inbox 패턴 신규

---

## 추가 작업
- [x] 01-basic-setup.md 문서 분리 (2,317줄 → 1,588줄, 31% 축소)
- [x] 09-anti-patterns-troubleshooting.md 신규 생성 (218줄)
- [x] 10-manual-commit-deep-dive.md 신규 생성 (368줄)
- [x] 11-production-case-studies.md 신규 생성 (176줄)
- [x] README.md 챕터 테이블 + Mermaid 다이어그램 업데이트

---

## 복습 Q&A 결과 (8문제, 3/8)

### 취약 영역 (재학습 필요)
- **acks 값 혼동**: `acks=0`(확인 안 함)과 `acks=1`(리더만)을 혼동. `acks=all`은 "모든 브로커"가 아니라 "모든 ISR"
- **멱등성 메커니즘**: 키 기반이 아니라 PID+시퀀스 번호 기반. 강제 설정도 `acks=all` + `max.in.flight ≤ 5` 두 가지
- **KafkaAdmin 토픽 수정**: `modify-topic-configs`의 위험성, 파티션 감소/복제 계수 변경 불가 → 문서에 수정 방법 추가 완료

### 이해 완료
- BATCH vs MANUAL AckMode 차이 (Spring 자동커밋 vs 개발자 제어)
- 기존 토픽 수정 방법 (설정 변경/파티션 증가/마이그레이션)

---

## 회고
- 잘한 점: 2,317줄짜리 문서를 주제별로 분리하면서 각 섹션의 내용을 재확인했다. 복습 Q&A에서 acks/멱등성 개념이 부정확했던 것을 발견하고 교정했다.
- 잘한 점: 02-producer-consumer.md 학습 중 "왜?"를 계속 파고들었다. 동기 전송이 왜 필요한지, auto.create=true가 왜 위험한지, 미들웨어 장애 시 리밸런싱이 왜 무의미한지 — 단순 암기가 아닌 원리 이해 중심으로 학습했다.
- 잘한 점: 한국 IT 기업 사례(LINE 1,500억건/일, 카카오 CDC, 배민 EDA)를 조사하여 이론과 실무를 연결했다.
- 개선할 점: acks=0/1/all 차이, 멱등성의 PID+시퀀스 메커니즘 등 핵심 개념을 "대충 안다"고 넘기지 말고 정확한 정의를 외워야 한다. 학습 문서 1,000줄 초과 시 주제 분리 기준도 세워야 한다.

## 내일 계획
- 02-producer-consumer.md 복습 Q&A (DefaultErrorHandler, 리밸런싱, 토픽 관리 중심)
- 취약 영역 재복습: acks 3단계, 멱등성 메커니즘, KafkaAdmin 토픽 수정
- 03-saga-choreography.md 또는 04-saga-orchestration.md 학습 진행
