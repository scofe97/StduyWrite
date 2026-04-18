# P5: ProducerInterceptor (자동 헤더 주입) 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | 모든 메시지에 공통 헤더(서비스명, 전송시각, traceId)를 자동 주입 |
| 파일 | `CommonHeaderInterceptor.java`, `OrderConsumer.java`, `application.yml` |
| 테스트 | `ConsumerTest.인터셉터가_자동으로_서비스명과_전송시각_헤더를_주입한다()` |

---

## 용어 정리

### MDC (Mapped Diagnostic Context)

스레드 로컬 저장소에 key-value를 넣어두면, 그 스레드에서 찍는 **모든 로그에 자동으로 포함**되는 메커니즘이다.

**왜 필요한가**: 웹 서버에서 동시에 100명이 요청하면 로그가 뒤섞인다. "이 로그가 어떤 요청의 것인지" 구분하려면 매 로그마다 requestId를 수동으로 넣어야 하는데, MDC를 쓰면 한 번만 설정하면 된다.

```java
// MDC 없이: 매번 수동 전달
log.info("[req-123] 주문 생성 시작");
log.info("[req-123] DB 저장 완료");

// MDC 사용: 한 번 설정하면 자동 포함
MDC.put("traceId", "req-123");
log.info("주문 생성 시작");     // logback 패턴에 %X{traceId} → 자동으로 req-123 출력
log.info("DB 저장 완료");       // 동일
MDC.clear();
```

**동작 원리**: 내부적으로 `ThreadLocal<Map<String, String>>`이다. 같은 스레드 내에서는 어디서든 `MDC.get("traceId")`로 값을 꺼낼 수 있다. 실무에서 Spring Cloud Sleuth(현 Micrometer Tracing)가 HTTP 요청 진입 시 `MDC.put("traceId", 자동생성값)`을 해주므로, 개발자가 직접 넣을 필요 없이 모든 로그에 traceId가 붙는다.

**인터셉터에서 쓴 이유**: HTTP 요청의 traceId를 Kafka 메시지 헤더에 실어 보내면, Consumer 쪽에서도 "이 메시지가 어떤 HTTP 요청에서 시작된 것인지" 추적할 수 있다. 이것이 **분산 추적(Distributed Tracing)**의 핵심이다.

### FQCN (Fully Qualified Class Name)

패키지 경로를 포함한 클래스의 **전체 이름**이다.

```
FQCN:  com.study.redpanda.ch02.interceptor.CommonHeaderInterceptor
       ├── 패키지 경로 ──────────────────────┤  ├── 클래스명 ──┤

단순 클래스명: CommonHeaderInterceptor  (패키지 없음)
```

**왜 FQCN이 필요한가**: Java에서 같은 이름의 클래스가 다른 패키지에 존재할 수 있다. `interceptor.classes: CommonHeaderInterceptor`만 쓰면 어떤 패키지의 클래스인지 알 수 없다. Kafka는 이 문자열을 `Class.forName("com.study.redpanda...")`로 로딩하므로 반드시 FQCN이어야 한다.

**리플렉션 과정**:
1. Kafka 클라이언트가 YAML에서 FQCN 문자열을 읽는다
2. `Class.forName(fqcn)` → 클래스 로딩
3. `clazz.getDeclaredConstructor().newInstance()` → 기본 생성자로 인스턴스 생성
4. `interceptor.configure(configs)` → 설정 전달

이 과정이 Spring과 무관하게 진행되기 때문에 `@Autowired`, `@Value`가 동작하지 않는 것이다.

---

## 왜 이렇게 구현했는가

### ProducerInterceptor가 Spring DI 밖에서 동작하는 이유

Kafka의 `interceptor.classes` 설정은 Kafka 클라이언트 내부에서 **리플렉션**으로 인스턴스를 생성한다 (위 FQCN 섹션 참조). 이 과정은 Spring ApplicationContext와 완전히 분리되어 있다.

- `@Autowired`, `@Value` 등 Spring 어노테이션이 **동작하지 않는다**
- `configure(Map<String, ?> configs)`가 유일한 설정 주입 채널이다
- 생성자 주입이 불가능하다 (기본 생성자만 사용)

### `byte[]` 변환과 `StandardCharsets.UTF_8`

Kafka 헤더의 값 타입은 `byte[]`이다. `String.getBytes()`를 인자 없이 호출하면 JVM의 기본 charset(플랫폼 의존적)을 사용하므로 환경마다 다른 바이트가 들어갈 수 있다. `StandardCharsets.UTF_8`을 명시하면 **어떤 환경에서든 동일한 직렬화를 보장**한다.

### MDC 기반 traceId 전파

`MDC.get("traceId")`는 현재 스레드의 MDC에서 traceId를 가져온다 (위 MDC 섹션 참조). 실무에서 Spring Cloud Sleuth(현 Micrometer Tracing)가 HTTP 요청 진입 시 MDC에 traceId를 자동 설정하므로, "HTTP 요청 -> Kafka 메시지 -> Consumer 처리"의 전체 흐름을 하나의 traceId로 추적할 수 있다.

**주의**: `onSend()`는 `KafkaProducer.send()`를 호출한 **애플리케이션 스레드**에서 실행된다. 따라서 MDC 값을 읽는 것이 안전하다. 반면 `onAcknowledgement()`는 IO 스레드에서 실행되므로 MDC 값이 없을 수 있다.

### `required = false` 전략

인터셉터가 비활성화된 환경(테스트, 다른 프로필)에서도 Consumer가 깨지지 않아야 한다. `required = true`(기본값)로 설정하면 해당 헤더가 없는 메시지 수신 시 `MessageConversionException`이 발생하여 **Consumer 전체가 중단**된다.

### `application.yml`의 `interceptor.classes`

```yaml
producer:
  properties:
    interceptor.classes: com.study.redpanda.ch02.interceptor.CommonHeaderInterceptor
```

Spring Boot의 `spring.kafka.producer.properties.*` 매핑을 통해 Kafka Producer의 네이티브 설정에 FQCN을 전달한다. 여러 인터셉터를 체이닝할 때는 **쉼표로 구분**하며, 선언 순서대로 실행된다.

---

## 코드 리뷰 결과

| 심각도 | 이슈 | 상태 |
|--------|------|------|
| HIGH | `Instant.now()` 이중 호출 — 헤더 값과 로그 값 불일치 | 수정 완료 |
| MEDIUM | ISO-8601 검증 `.contains("T")`가 느슨함 | 인지 (학습 프로젝트로 수용) |
| MEDIUM | SERVICE_NAME 하드코딩 — `configure()`로 외부 주입 가능 | 인지 (학습 프로젝트로 수용) |
| MEDIUM | Consumer 필드 스레드 안전성 — volatile 미사용 | 인지 (CountDownLatch의 happens-before로 동작) |
| LOW | `onAcknowledgement` 성공 메트릭 없음 | 학습 범위 외 |
| LOW | `required = false` 이유 주석 보강 가능 | 학습 범위 외 |

### 수정한 이슈: Instant.now() 이중 호출

```java
// Before (BAD): 헤더와 로그에 다른 시각
record.headers().add("X-Sent-At", Instant.now().toString().getBytes(...));
log.debug("... X-Sent-At={}", SERVICE_NAME, Instant.now());

// After (GOOD): 변수 추출로 동일한 값 사용
String sentAt = Instant.now().toString();
record.headers().add("X-Sent-At", sentAt.getBytes(...));
log.debug("... X-Sent-At={}", SERVICE_NAME, sentAt);
```

---

## 대안: Spring 방식 vs Kafka 네이티브

| 방식 | Spring `RecordInterceptor` | Kafka `ProducerInterceptor` |
|------|---------------------------|---------------------------|
| DI | Spring Bean (DI 가능) | 리플렉션 생성 (DI 불가) |
| 적용 범위 | Spring KafkaTemplate만 | 모든 Kafka Producer |
| 설정 주입 | `@Value`, `@Autowired` | `configure(Map)` |
| 생명주기 | Spring 관리 | Kafka 클라이언트 관리 |

P6(KafkaTemplate 래퍼)에서 Spring 방식을 다룰 예정이므로, P5에서 Kafka 네이티브 방식을 배우는 것은 적절한 순서이다.

---

## 핵심 학습 포인트

1. **MDC** — `ThreadLocal<Map>` 기반, 한 번 설정하면 모든 로그에 자동 포함, 분산 추적의 기반
2. **FQCN** — 패키지 포함 전체 클래스명, Kafka가 리플렉션으로 인스턴스 생성 시 필요
3. **ProducerInterceptor는 Spring 밖에서 동작** — FQCN + 리플렉션이므로 `@Autowired` 불가, `configure()`로 설정 주입
4. **onSend()는 애플리케이션 스레드** — MDC 접근 안전, onAcknowledgement()는 IO 스레드
5. **byte[] + UTF-8 명시** — 플랫폼 독립적 직렬화 보장
6. **required=false는 방어적 프로그래밍** — 인터셉터 미설정 환경에서 Consumer 보호
7. **interceptor.classes는 FQCN** — 쉼표로 체이닝, 선언 순서대로 실행
