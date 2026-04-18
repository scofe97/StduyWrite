# 구조 패턴

---

> 구조 패턴(Structural Patterns)은 클래스와 객체를 더 큰 구조로 조합하는 방법을 다룬다. 기존 코드를 수정하지 않고 새로운 기능을 덧붙이거나, 서로 다른 인터페이스를 가진 객체들이 협력할 수 있게 한다.

## 패턴 개요

| 패턴 | 목적 | Spring 활용 |
|------|------|------------|
| Proxy | 대상 접근을 제어 | AOP, `@Transactional`, `@Cacheable` |
| Decorator | 책임을 동적으로 추가 | `InputStream` 래핑, `HandlerInterceptor` |
| Facade | 복잡한 서브시스템을 단순화 | `JdbcTemplate`, `RestTemplate` |
| Adapter | 호환되지 않는 인터페이스를 연결 | `Arrays.asList()`, `HandlerAdapter` |

## Proxy — 프록시 패턴

**프록시 패턴**은 다른 객체에 대한 대리자(surrogate)를 제공하여 그 객체에 대한 접근을 제어한다. 클라이언트는 실제 객체와 프록시를 구분하지 못한다. 접근 제어, 지연 초기화, 로깅, 캐싱 등의 부가 기능을 원본 객체 코드 수정 없이 추가할 수 있다.

```java
interface OrderRepository {
    Optional<Order> findById(Long id);
    void save(Order order);
}

// 실제 구현체
class JpaOrderRepository implements OrderRepository {
    public Optional<Order> findById(Long id) { /* JPA 조회 */ return Optional.empty(); }
    public void save(Order order) { /* JPA 저장 */ }
}

// 프록시: 캐싱 기능을 추가한다 (원본 코드 수정 없음)
class CachingOrderRepository implements OrderRepository {
    private final OrderRepository delegate;
    private final Map<Long, Order> cache = new HashMap<>();

    CachingOrderRepository(OrderRepository delegate) {
        this.delegate = delegate;
    }

    public Optional<Order> findById(Long id) {
        return Optional.ofNullable(
            cache.computeIfAbsent(id, k -> delegate.findById(k).orElse(null))
        );
    }

    public void save(Order order) {
        delegate.save(order);
        cache.put(order.id(), order); // 캐시 업데이트
    }
}
```

### Spring AOP: JDK Dynamic Proxy vs CGLIB

Spring AOP는 `@Transactional`, `@Cacheable` 같은 어노테이션을 처리할 때 프록시를 자동 생성한다. 프록시 생성 방식은 대상 클래스의 특성에 따라 결정된다.

| 구분 | JDK Dynamic Proxy | CGLIB |
|------|-------------------|-------|
| 조건 | 인터페이스가 있을 때 | 인터페이스가 없거나 `proxyTargetClass=true` |
| 생성 방식 | `java.lang.reflect.Proxy` | 바이트코드 조작으로 서브클래스 생성 |
| 제약 | 인터페이스 메서드만 프록시 가능 | `final` 클래스/메서드는 프록시 불가 |
| Spring Boot 기본 | Spring Boot 2+ 기본값은 CGLIB | |

```java
// JDK Dynamic Proxy: 인터페이스가 있을 때
@Service
public class OrderServiceImpl implements OrderService { // 인터페이스 존재 → JDK Proxy 가능
    @Transactional
    public void placeOrder(Order order) { /* ... */ }
}

// CGLIB: 인터페이스 없이 클래스만 있을 때
@Service
public class PaymentService { // 인터페이스 없음 → CGLIB 서브클래스 생성
    @Transactional
    public void pay(Long orderId) { /* ... */ }
}
```

## Decorator — 데코레이터 패턴

**데코레이터 패턴**은 객체에 동적으로 책임을 추가한다. 상속 대신 구성(composition)을 사용하므로, 여러 기능을 조합할 때 클래스 폭발을 막을 수 있다. Java I/O 라이브러리가 이 패턴의 가장 대표적인 사례로, `InputStream`을 감싸는 여러 데코레이터가 연쇄 적용된다.

```java
// Java I/O 데코레이터 체이닝
InputStream raw       = new FileInputStream("data.txt");
InputStream buffered  = new BufferedInputStream(raw);     // 버퍼링 추가
InputStream counted   = new CountingInputStream(buffered); // 바이트 카운팅 추가

// 커스텀 데코레이터 구현
interface TextProcessor {
    String process(String text);
}

record PlainProcessor() implements TextProcessor {
    public String process(String text) { return text; }
}

// 추상 데코레이터: 공통 위임 코드를 담는다
abstract class TextProcessorDecorator implements TextProcessor {
    protected final TextProcessor wrapped;
    TextProcessorDecorator(TextProcessor wrapped) { this.wrapped = wrapped; }
}

class TrimDecorator extends TextProcessorDecorator {
    TrimDecorator(TextProcessor wrapped) { super(wrapped); }
    public String process(String text) { return wrapped.process(text).trim(); }
}

class UpperCaseDecorator extends TextProcessorDecorator {
    UpperCaseDecorator(TextProcessor wrapped) { super(wrapped); }
    public String process(String text) { return wrapped.process(text).toUpperCase(); }
}

// 사용: trim → uppercase 순으로 적용
TextProcessor processor = new UpperCaseDecorator(
        new TrimDecorator(new PlainProcessor())
);
String result = processor.process("  hello world  "); // "HELLO WORLD"
```

### Proxy vs Decorator 비교

두 패턴은 구조가 동일하지만 **의도**가 다르다. 프록시는 원본 객체에 대한 접근을 제어하는 것이 목적이고, 데코레이터는 원본 객체의 동작을 확장하는 것이 목적이다.

| 관점 | Proxy | Decorator |
|------|-------|-----------|
| 의도 | 접근 제어 (보안, 캐싱, 지연) | 기능 확장 (동적 책임 추가) |
| 대상 인지 | 프록시가 대상을 직접 생성하거나 참조 보관 | 외부에서 주입받는다 |
| 체이닝 | 일반적으로 단층 | 여러 겹 중첩이 일반적 |
| Spring 예시 | `@Transactional` 프록시 | `HandlerInterceptor` 체인 |

## Facade — 퍼사드 패턴

**퍼사드 패턴**은 복잡한 서브시스템에 대한 단순화된 인터페이스를 제공한다. 클라이언트는 퍼사드만 알면 되므로 서브시스템의 복잡성에서 격리된다. `JdbcTemplate`이 커넥션 획득, 스테이트먼트 준비, 예외 변환, 리소스 해제라는 복잡한 절차를 단일 메서드 호출로 숨기는 것이 대표적이다.

```java
// 서브시스템들: 각각 복잡한 API를 가진다
class VideoEncoder { String encode(String file) { return "encoded:" + file; } }
class AudioMixer   { String mix(String file)    { return "mixed:" + file; } }
class Transcoder   { String transcode(String v, String a) { return v + "+" + a; } }

// 퍼사드: 복잡한 처리 과정을 단일 메서드로 감춘다
class VideoProcessingFacade {
    private final VideoEncoder encoder   = new VideoEncoder();
    private final AudioMixer   mixer     = new AudioMixer();
    private final Transcoder   transcoder = new Transcoder();

    public String process(String videoFile) {
        String encodedVideo = encoder.encode(videoFile);
        String mixedAudio   = mixer.mix(videoFile);
        return transcoder.transcode(encodedVideo, mixedAudio);
    }
}

// 클라이언트: 내부 구현 모름
var facade = new VideoProcessingFacade();
String result = facade.process("movie.mp4");
```

## Adapter — 어댑터 패턴

**어댑터 패턴**은 호환되지 않는 인터페이스를 가진 클래스들이 함께 동작할 수 있게 한다. 기존 코드를 수정하지 않고 새로운 인터페이스에 맞게 감싸는 방식으로, 레거시 코드 통합이나 서드파티 라이브러리 교체 시 자주 사용된다.

```java
// 기존 레거시 결제 API (변경 불가)
class LegacyPaymentGateway {
    public boolean processPayment(double amount, String cardNumber) {
        System.out.println("Legacy: processing " + amount);
        return true;
    }
}

// 새 시스템이 기대하는 인터페이스
interface PaymentProcessor {
    PaymentResult pay(PaymentRequest request);
}

record PaymentRequest(long amountCents, String maskedCard) {}
record PaymentResult(boolean success, String transactionId) {}

// 어댑터: 레거시 API를 새 인터페이스에 맞게 변환
class LegacyPaymentAdapter implements PaymentProcessor {
    private final LegacyPaymentGateway legacy;

    LegacyPaymentAdapter(LegacyPaymentGateway legacy) {
        this.legacy = legacy;
    }

    public PaymentResult pay(PaymentRequest request) {
        double amount = request.amountCents() / 100.0;
        boolean ok = legacy.processPayment(amount, request.maskedCard());
        return new PaymentResult(ok, ok ? "TXN-" + System.currentTimeMillis() : null);
    }
}
```
