# 14. Redpanda 도입 통합 고려사항

## 문서 목적

01~13 문서는 개별 유스케이스와 기술 설계를 다뤘다. 이 문서는 횡단 관점에서 Redpanda 도입 시 조직, 인프라, 운영, 장애 대응을 종합적으로 다룬다. 각 유스케이스 문서의 개별 고려사항을 통합하고, 문서 전체에서 다루지 않았던 영역을 보충한다.

---

## 1. 조직/팀 준비도

### 1.1 기술 전환의 핵심 도전

TPS 팀은 Feign/REST 기반 동기 통신에 익숙하다. Redpanda 도입은 단순한 기술 교체가 아니라 **사고방식의 전환**을 요구한다.

| 관점 | 동기 (현재) | 비동기 (전환 후) |
|------|----------|----------------|
| 디버깅 | 호출 스택 추적 (stack trace) | correlationId로 이벤트 체인 추적 |
| 에러 처리 | try-catch + 즉시 응답 | DLQ + 재처리 + 보상 트랜잭션 |
| 데이터 일관성 | 트랜잭션 (ACID) | 최종 일관성 (eventual consistency) |
| 테스트 | 단위 테스트 + MockMvc | Testcontainers + Consumer 검증 |
| 모니터링 | HTTP 상태 코드 + 응답 시간 | Consumer Lag + 처리율 + DLQ 건수 |

이 전환이 가장 어려운 부분이다. 코드를 바꾸는 것보다 팀의 디버깅/운영 습관을 바꾸는 데 시간이 더 걸린다.

### 1.2 학습 경로

기존 학습 자료를 TPS 도입 순서에 맞춰 단계별로 소화하는 경로다.

**Phase 1 (인프라 구축 전)**:
- `02-fundamentals/07-schema-registry.md` — 호환성 모드, 캐싱, API 이해
- `02-fundamentals/04-consumer-group.md` — Consumer Group 리밸런싱, 오프셋 관리
- `03-spring-boot/02-producer-consumer.md` — Spring Kafka 기본 Producer/Consumer

**Phase 2 (핵심 전환 시)**:
- `03-spring-boot/15-schema-registry-strategy.md` — CI/CD 스키마 등록, 브랜치 전략
- `01-event-driven/09-saga-pattern.md` — Choreography vs Orchestration SAGA
- `01-event-driven/17-idempotency-patterns.md` — 멱등성 패턴 (correlationId + eventType)

**Phase 3 (운영 안정화)**:
- `07-connectors/03-RedpandaConnect.md` — Redpanda Connect 설정, DLQ
- `02-fundamentals/14-reference-architecture.md` — 프로덕션 아키텍처 패턴

### 1.3 점진적 전환 원칙

한번에 전체를 전환하지 않는다. 09 문서의 Phase 1~3 로드맵에 따라, 저위험 유스케이스(감사 이력, 알림)부터 시작하여 팀이 이벤트 기반 운영 경험을 쌓은 후 핵심 브로커(DB-as-Queue)를 전환한다.

---

## 2. 인프라 비용/사이징

### 2.1 Redpanda 클러스터 최소 구성

TPS의 현재 트래픽 규모(업무 시간 기준 분당 수십~수백 건)를 감안한 최소 구성이다.

| 구성 요소 | 최소 사양 | 권장 사양 | 비고 |
|----------|---------|---------|------|
| 브로커 수 | 1 (개발) | 3 (프로덕션) | Raft 합의를 위해 홀수 |
| CPU | 2 cores | 4 cores | Redpanda는 thread-per-core 모델 |
| 메모리 | 2GB | 4GB | 페이지 캐시 + 내부 버퍼 |
| 디스크 | 20GB SSD | 50GB SSD | 토픽 보존 기간에 따라 조정 |
| Schema Registry | 내장 | 내장 | 별도 JVM 프로세스 불필요 |
| Redpanda Connect | 1 인스턴스 | 2 인스턴스 (HA) | 50~100MB 메모리, Go 바이너리 |

Confluent Kafka 대비 Redpanda의 장점은, Schema Registry와 HTTP Proxy가 브로커에 내장되어 별도 ZooKeeper/Schema Registry JVM이 불필요하다는 것이다. 운영 컴포넌트 수가 줄어 관리 부담이 낮다.

### 2.2 기존 인프라 절감 효과

Redpanda 도입으로 기존 인프라 부하가 줄어드는 부분이 있다.

| 제거/감소 항목 | 현재 부하 | 절감 효과 |
|--------------|---------|----------|
| DB 폴링 쿼리 (MessageTaskScheduler) | 분당 30회 | 제거 |
| DB 폴링 쿼리 (PipelineTaskScheduler) | 분당 18회 | 제거 |
| DB 분산 락 하트비트 | 60초마다 갱신 | 제거 (Consumer Group 대체) |
| Jenkins API 폴링 | 10초마다 | 제거 (webhook 대체) |
| Thread.sleep 블로킹 | 스레드 최대 30초 점유 | 제거 (비동기 소비자) |

MariaDB의 폴링 쿼리 부하가 크게 줄어, DB 리소스를 비즈니스 쿼리에 집중할 수 있다.

### 2.3 Docker Compose 최소 구성

```yaml
services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:latest
    command:
      - redpanda start
      - --smp 2
      - --memory 2G
      - --advertise-kafka-addr redpanda:9092
    ports:
      - "9092:9092"    # Kafka API
      - "18081:8081"   # Schema Registry
      - "18082:8082"   # HTTP Proxy
      - "9644:9644"    # Admin API

  redpanda-connect:
    image: docker.redpanda.com/redpandadata/connect:latest
    ports:
      - "4195:4195"
    volumes:
      - ./connect:/connect
    depends_on:
      - redpanda

  redpanda-console:
    image: docker.redpanda.com/redpandadata/console:latest
    ports:
      - "8080:8080"
    environment:
      KAFKA_BROKERS: redpanda:9092
      KAFKA_SCHEMAREGISTRY_ENABLED: "true"
      KAFKA_SCHEMAREGISTRY_URLS: http://redpanda:8081
    depends_on:
      - redpanda
```

3개 컨테이너(브로커 + Connect + Console)로 전체 인프라가 구성된다.

---

## 3. 모니터링 체계

### 3.1 핵심 모니터링 지표

| 지표 | 측정 방법 | 임계값 | 알림 대상 |
|------|---------|--------|----------|
| **Consumer Lag** | `rpk group describe` / Prometheus | > 1,000 | 운영팀 |
| **DLQ 메시지 수** | DLQ 토픽 Consumer | > 0 | 개발팀 |
| **처리율 (msg/sec)** | Consumer 메트릭 | 급격한 변화 | 모니터링 대시보드 |
| **Producer 에러율** | Producer 메트릭 | > 0.1% | 개발팀 |
| **Schema Registry 가용성** | HTTP health check | 응답 없음 | 인프라팀 |
| **Redpanda Connect 상태** | `/ready` 엔드포인트 | 비정상 | 인프라팀 |

### 3.2 Grafana 대시보드 구성

TPS의 기존 Spring Actuator + Prometheus 인프라에 Kafka 메트릭을 추가한다.

**패널 1: 전체 현황**
- 토픽별 메시지 처리량 (produce/consume)
- Consumer Group별 Lag 추이
- DLQ 메시지 누적 건수

**패널 2: 유스케이스별 상세**
- `tps.async-message.*`: 비동기 메시지 전달 지연 (produce→consume 시간 차)
- `tps.audit.ticket-history`: 감사 이력 처리 성공/실패 비율
- `tps.pipeline.status-changed`: Jenkins 이벤트 수신 건수

**패널 3: Redpanda Connect**
- webhook 수신 건수 (도구별)
- 변환 성공/실패 건수
- DLQ 라우팅 건수

### 3.3 Spring Kafka 메트릭 연동

```yaml
# application.yml
management:
  metrics:
    tags:
      application: ${spring.application.name}
  endpoints:
    web:
      exposure:
        include: health, prometheus, info

spring:
  kafka:
    listener:
      observation-enabled: true  # Spring Kafka 3.0+ Micrometer 연동
```

`observation-enabled: true`로 설정하면, Spring Kafka의 Producer/Consumer 메트릭이 Micrometer를 통해 Prometheus에 자동 노출된다.

---

## 4. 기존 시스템 공존 전략

### 4.1 Feature Flag 기반 전환

유스케이스별로 Feign↔토픽을 Feature Flag로 제어한다. 문제 발생 시 플래그만 끄면 즉시 Feign으로 롤백할 수 있다.

```yaml
# application.yml
tps:
  eda:
    audit-history:
      enabled: true       # true: 토픽 발행, false: Feign 호출
    async-message:
      enabled: false      # Phase 2에서 전환
    pipeline-status:
      enabled: false      # Phase 2에서 전환
```

```java
@Service
public class AuditHistoryPublisher {
    @Value("${tps.eda.audit-history.enabled:false}")
    private boolean edaEnabled;

    public void publish(TcktHstryEvent event) {
        if (edaEnabled) {
            kafkaTemplate.send("tps.audit.ticket-history", event.getTcktNo(), event);
        } else {
            tcktLogFeignClient.recordTcktHstry(event.toRequest());  // 기존 Feign
        }
    }
}
```

### 4.2 이중 운영 기간 전략

09 문서 Phase 2에서 DB-as-Queue와 Redpanda를 이중 운영할 때의 상세 전략이다.

**전환 순서**:

```
1단계: Consumer를 토픽에서 읽도록 전환 (Feign 소비자 유지)
2단계: Producer를 토픽으로 전환 (이중 쓰기: Feign + 토픽)
3단계: Feign 트래픽이 0인 것을 확인
4단계: Feign 호출 제거, Feature Flag off
```

Consumer를 먼저 전환하는 이유는, Producer가 이중 쓰기를 시작하면 토픽 Consumer가 즉시 처리할 수 있어야 하기 때문이다. Consumer가 준비되지 않은 상태에서 토픽에 메시지를 넣으면 Lag만 쌓인다.

### 4.3 멱등성 보장

이중 운영 기간에 동일 메시지가 Feign과 토픽 양쪽에서 처리될 수 있다. `(correlationId, eventType)` 복합 키로 중복을 방지한다.

```java
// ProcessedEvent 테이블 활용 (기존 Redpanda PoC 패턴)
@Query(value = """
    INSERT INTO processed_event (correlation_id, event_type, processed_at)
    SELECT :correlationId, :eventType, NOW()
    WHERE NOT EXISTS (
        SELECT 1 FROM processed_event
        WHERE correlation_id = :correlationId AND event_type = :eventType
    )""", nativeQuery = true)
int tryAcquire(@Param("correlationId") String correlationId,
               @Param("eventType") String eventType);
```

`tryAcquire`가 1을 반환하면 처리, 0을 반환하면 중복으로 스킵한다. INSERT...WHERE NOT EXISTS 패턴은 예외 없이 0/1을 반환하므로 Hibernate 세션 오염이 발생하지 않는다.

### 4.4 롤백 전략

토픽 기반 처리에서 문제가 발생했을 때의 롤백 절차다.

```
1. Feature Flag off → Feign 호출 복구
2. Consumer 중지 (토픽 메시지 누적은 보존)
3. 문제 원인 분석 및 수정
4. Consumer 재시작 → 누적 메시지 재처리 (멱등성으로 안전)
5. Feature Flag on → 토픽 전환 재개
```

토픽 메시지는 보존 기간 내에 언제든 재처리할 수 있으므로, 롤백해도 데이터가 유실되지 않는다.

---

## 5. 장애 대응

### 5.1 Redpanda 클러스터 장애

| 장애 유형 | 영향 | 대응 |
|----------|------|------|
| 단일 브로커 다운 | 리더 파티션 재선출, 일시적 지연 | 자동 복구 (Raft 프로토콜) |
| 과반수 브로커 다운 | 쓰기 불가, 읽기 가능 (ISR 상태 의존) | Circuit Breaker → Feign 폴백 |
| 전체 클러스터 다운 | 모든 produce/consume 중단 | Feature Flag → Feign 전체 복구 |

**Circuit Breaker 패턴**:

```java
@Service
public class ResilientEventPublisher {
    private final CircuitBreaker circuitBreaker;

    public void publish(String topic, String key, Object event) {
        try {
            circuitBreaker.run(
                () -> kafkaTemplate.send(topic, key, event).get(5, TimeUnit.SECONDS),
                throwable -> fallbackToFeign(event)  // Feign 폴백
            );
        } catch (Exception e) {
            fallbackToFeign(event);
        }
    }
}
```

Redpanda가 응답하지 않으면 Circuit Breaker가 열리고, 자동으로 Feign 호출로 폴백한다. Redpanda가 복구되면 Circuit Breaker가 닫히고 토픽 발행을 재개한다.

### 5.2 Consumer 장애

| 장애 유형 | 증상 | 대응 |
|----------|------|------|
| Consumer 프로세스 다운 | Lag 증가, 모니터링 알림 | Consumer Group 리밸런싱 (자동) |
| Consumer 처리 지연 | Lag 점진 증가 | 파티션 수 증가 + Consumer 인스턴스 추가 |
| 역직렬화 실패 | 특정 메시지에서 반복 실패 | DLQ 라우팅 후 수동 분석 |

Consumer가 다운되면 같은 Consumer Group의 다른 인스턴스가 파티션을 인계받는다. 단일 인스턴스인 경우 재시작 전까지 Lag이 쌓이지만, 메시지는 토픽에 보존되므로 재시작 후 누적분을 처리한다.

### 5.3 메시지 신뢰성 설정

프로덕션에서 메시지 유실을 방지하기 위한 설정이다.

```yaml
spring:
  kafka:
    producer:
      acks: all                    # 모든 ISR 복제본 확인
      retries: 3                   # 일시적 실패 재시도
      properties:
        enable.idempotence: true   # PID+시퀀스로 중복 방지
        max.in.flight.requests.per.connection: 5  # 멱등성 모드 제한
    consumer:
      enable-auto-commit: false    # 수동 커밋 (처리 완료 후)
      auto-offset-reset: earliest  # 신규 Consumer는 처음부터 읽기
```

`acks=all` + `enable.idempotence=true`는 Producer 측에서 at-least-once 전달을 보장한다. Consumer 측에서 `enable-auto-commit=false`로 처리 완료 후에만 오프셋을 커밋하면, 메시지 유실 없이 at-least-once 처리가 완성된다.

### 5.4 순서 보장 검증

파티션 키가 일관되게 설정되었는지 주기적으로 검증해야 한다. 같은 엔티티의 이벤트가 다른 파티션으로 라우팅되면 순서가 역전될 수 있다.

```bash
# rpk으로 파티션별 메시지 키 분포 확인
rpk topic consume tps.workflow.ticket --num 100 -f '%k %p\n' | sort | uniq -c | sort -rn
```

동일한 `tcktNo` 키가 여러 파티션에 분산되어 있으면 파티셔닝 로직에 문제가 있는 것이다.

---

## 6. 성공 기준 및 KPI

### 6.1 Phase별 완료 기준

| Phase | 기간 | 성공 기준 |
|-------|------|----------|
| Phase 1 | 1~2주 | 감사 유실률 0%, 알림 재시도 동작, Consumer Lag 모니터링 정상 |
| Phase 2 | 3~4주 | 비동기 메시지 지연 <100ms, DB 폴링 쿼리 0회/분, MessageService 비활성화 |
| Phase 3 | 5~8주 | SAGA 보상 트랜잭션 동작, Thread.sleep 코드 완전 제거 |

### 6.2 정량적 KPI

| KPI | 현재 값 | 목표 값 | 측정 방법 |
|-----|--------|--------|----------|
| 비동기 메시지 전달 지연 | 최대 20초 | <100ms | produce→consume 타임스탬프 차이 |
| 감사 이력 유실률 | Feign 실패율 의존 | 0% | DLQ 건수 / 전체 건수 |
| DB 폴링 쿼리 | 48회/분 | 0회/분 | Slow query log 또는 Prometheus |
| Feign 클라이언트 수 | 43개 | 30개 이하 | 코드 grep 카운트 |
| MessageService 코드 | 834줄 | 0줄 (제거) | 파일 존재 여부 |
| 장애 복구 시간 (RTO) | 수동 forceAcquire | 자동 리밸런싱 <30초 | Consumer Group 상태 모니터링 |

### 6.3 go/no-go 기준

각 Phase 전환 전에 확인해야 할 사항이다.

**Phase 1 → Phase 2 전환 조건**:
- [ ] Consumer Lag 모니터링 대시보드 운영 중
- [ ] DLQ 알림 파이프라인 동작 확인
- [ ] 감사 이력 토픽: 장애 주입 테스트 통과 (Feign 차단 시 토픽으로 정상 전달)
- [ ] 팀 전원 Kafka Consumer 로그 분석 경험 1회 이상

**Phase 2 → Phase 3 전환 조건**:
- [ ] DB-as-Queue 트래픽 0% 확인 (최소 1주 관찰)
- [ ] MessageService 비활성화 후 부작용 없음 확인
- [ ] 이중 운영 기간 멱등성 검증 완료 (중복 처리 0건)

---

## 7. 기존 문서 참조 매핑

이 문서의 각 고려사항이 기존 01~13 문서의 어느 영역과 연결되는지 정리한다.

| 고려사항 | 관련 문서 | 보충 내용 |
|---------|----------|----------|
| 학습 경로 (1.2) | 전체 | 기존 학습 자료를 TPS 도입 Phase에 매핑 |
| 인프라 사이징 (2) | 09 Phase 1 | 09의 "인프라 구축"을 구체적 스펙으로 |
| 모니터링 (3) | 09 Phase 1, 13 운영 | 09/13에서 언급한 모니터링을 대시보드 수준으로 |
| Feature Flag (4.1) | 09 Phase 2 | 09의 이중 운영 전략을 코드 수준으로 |
| 멱등성 (4.3) | 08 UC-1, 03 SAGA | 기존 PoC(Redpanda Spring Boot) 패턴 적용 |
| 클러스터 장애 (5.1) | 해당 없음 | 완전 신규 — 기존 문서에서 미다룸 |
| Consumer 장애 (5.2) | 해당 없음 | 완전 신규 |
| 메시지 신뢰성 (5.3) | 12 호환성 정책 | 12의 스키마 정책과 함께 프로덕션 설정 |
| 성공 기준 (6) | 09 검증 기준 | 09의 검증 기준을 정량적 KPI로 확장 |
