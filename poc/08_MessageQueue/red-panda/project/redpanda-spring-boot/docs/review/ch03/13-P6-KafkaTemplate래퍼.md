# P6: KafkaTemplate 래퍼 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | 공통 헤더를 자동 추가하는 KafkaTemplate 래퍼 (P5 ProducerInterceptor의 Spring 대안) |
| 파일 | `EnhancedKafkaTemplate.java`, `EnhancedKafkaTemplateTest.java` |
| 테스트 | 2개 (공통 헤더 자동 추가, X-Correlation-Id 래퍼 전용 헤더) |

---

## 왜 이렇게 구현했는가

### P5(ProducerInterceptor)와 P6(KafkaTemplate 래퍼)의 비교

두 방식 모두 "모든 메시지에 공통 헤더를 자동 추가"하는 같은 목적이지만, 동작 레벨이 다르다.

| | P5: ProducerInterceptor | P6: KafkaTemplate 래퍼 |
|---|---|---|
| 레벨 | Kafka 네이티브 (KafkaProducer 내부) | Spring 애플리케이션 |
| 설정 | YAML `interceptor.classes` | `@Component` Bean |
| Spring Bean 주입 | **불가** (Kafka가 직접 인스턴스 생성) | **가능** (Spring 컨텍스트) |
| 조건부 헤더 | 어려움 (설정값만 접근 가능) | 쉬움 (Spring Bean, 환경변수 등 자유 접근) |
| 적용 범위 | KafkaTemplate을 사용하는 **모든** send() | 래퍼를 호출한 곳만 |
| 우회 가능성 | 없음 (KafkaProducer 레벨에서 강제) | 있음 (KafkaTemplate 직접 사용하면 우회) |

### "고정값 헤더만이면 인터셉터와 똑같은 거 아닌가?"

맞다. 고정값(서비스명, 환경 등)만 넣는 경우 결과는 동일하다. **래퍼의 존재 이유는 Spring 컨텍스트가 필요한 동적 헤더**다.

인터셉터는 Kafka가 직접 인스턴스를 생성하므로 Spring 컨텍스트 밖에 있다. `@Autowired`, `@Value`, `SecurityContext` 등이 모두 동작하지 않는다.

```java
// P5 Interceptor — Spring 기능 사용 불가
public class HeaderInterceptor implements ProducerInterceptor<String, Object> {
    @Autowired  // ❌ 동작 안 함 — Spring이 관리하는 객체가 아님
    private UserService userService;

    @Value("${app.service-name}")  // ❌ 동작 안 함
    private String serviceName;
}
```

```java
// P6 래퍼 — Spring 기능 모두 사용 가능
@Component
@RequiredArgsConstructor
public class EnhancedKafkaTemplate {
    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;
    private final UserService userService;           // ✅ Spring Bean 주입

    @Value("${app.service-name}")                    // ✅ 설정값 주입
    private String serviceName;

    public CompletableFuture<SendResult<String, OrderEvent>> send(...) {
        // ✅ SecurityContext에서 현재 사용자 조회
        String userId = SecurityContextHolder.getContext()
                .getAuthentication().getName();
        record.headers().add("X-User-Id", userId.getBytes());

        // ✅ Spring Bean으로 동적 값 조회
        String region = userService.getRegion(userId);
        record.headers().add("X-Region", region.getBytes());
    }
}
```

| 헤더 유형 | 인터셉터 | 래퍼 |
|----------|---------|------|
| 고정값 (서비스명, 환경) | **적합** — 똑같이 가능 | 가능 |
| Spring Bean 필요 (DB 조회, 사용자 정보) | **불가** | **적합** |
| SecurityContext (현재 로그인 사용자) | **불가** | **적합** |
| 우회 방지 (무조건 적용) | **적합** | 불가 |

### 래퍼 패턴의 장점

1. **Spring Bean 주입**: `@Value`, `@Autowired` 등으로 설정값이나 다른 서비스를 주입받을 수 있다
2. **조건부 로직**: if문으로 특정 조건에서만 헤더를 추가하거나, 토픽에 따라 다른 헤더를 넣을 수 있다
3. **테스트 용이**: Mock으로 교체하여 단위 테스트가 쉽다
4. **타입 안전성**: 제네릭 타입이 명확하여 컴파일 타임에 타입 검증이 된다

### 래퍼 패턴의 단점

1. **우회 가능**: 개발자가 KafkaTemplate을 직접 주입받아 사용하면 래퍼를 건너뛴다
2. **강제력 없음**: 인터셉터는 KafkaProducer 레벨에서 무조건 실행되지만, 래퍼는 규약에 의존한다

### 어떤 상황에 어떤 방식을 선택하는가

| 상황 | 권장 방식 | 이유 |
|------|----------|------|
| 모든 메시지에 무조건 적용 (tracing 등) | P5 (Interceptor) | 우회 불가, 누락 방지 |
| Spring Bean이 필요한 동적 헤더 | **P6 (래퍼)** | Bean 주입 가능 |
| 팀 내 규약으로 충분한 경우 | **P6 (래퍼)** | 코드가 직관적 |
| 제로 코드 분산 추적 | Micrometer Tracing | 의존성만 추가하면 자동 |

### 실무에서의 조합

실무에서는 하나만 사용하지 않고 **레이어별로 조합**한다.

```
[Micrometer Tracing]     ← 분산 추적 (traceId, spanId) — 자동
[ProducerInterceptor]    ← 인프라 헤더 (서비스명, 환경) — 강제
[KafkaTemplate 래퍼]     ← 비즈니스 헤더 (correlationId, userId) — 선택적
```

---

## 핵심 학습 포인트

1. **래퍼 = Spring 방식** — Bean 주입, 조건부 로직, 타입 안전성의 장점
2. **인터셉터 = Kafka 방식** — 강제 적용, 우회 불가, 누락 방지의 장점
3. **우회 가능성 인지** — 래퍼는 KafkaTemplate 직접 사용으로 건너뛸 수 있다
4. **레이어별 조합** — Tracing(자동) + Interceptor(강제) + 래퍼(비즈니스) 병행이 실무 패턴
5. **P4 → P5 → P6 진화** — 수동 헤더(P4) → 자동 인터셉터(P5) → Spring 래퍼(P6)

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | **High** | 테스트명 "래퍼 없이 직접 전송"인데 실제로는 `enhancedKafkaTemplate.send()` 호출 — 의도한 비교 케이스 미실행 | 핵심 요구사항 미검증 |
| 2 | **High** | 수신 메시지가 방금 보낸 이벤트인지 미식별 — `correlationId != null`만으로 통과 | 이전/다른 메시지로 latch가 내려가도 통과하는 false-positive |
