# 구조 패턴: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Spring AOP가 JDK Dynamic Proxy와 CGLIB을 선택하는 기준은 무엇인가?

### 왜 이 질문이 중요한가

`@Transactional`이 왜 `private` 메서드에는 적용되지 않는지, `final` 클래스에서 AOP가 동작하지 않는 이유는 무엇인지를 이해하려면 프록시 생성 메커니즘을 알아야 한다. 이 질문은 Spring의 동작 원리에 대한 이해 깊이를 가늠하는 대표적인 면접 질문이다.

### 답변

Spring AOP는 런타임에 프록시 객체를 생성하여 부가 기능(트랜잭션, 캐싱 등)을 적용한다. 프록시 생성 방식은 대상 클래스의 특성과 설정에 따라 결정된다.

**JDK Dynamic Proxy**는 `java.lang.reflect.Proxy`를 사용하며, 대상 클래스가 하나 이상의 인터페이스를 구현할 때 사용 가능하다. 인터페이스의 메서드만 프록시할 수 있으므로, 구체 클래스에만 선언된 메서드는 AOP 적용이 안 된다.

**CGLIB**은 바이트코드를 조작하여 대상 클래스의 서브클래스를 런타임에 생성한다. 인터페이스 없이도 동작하지만, `final` 클래스와 `final` 메서드는 서브클래싱이 불가능하므로 프록시를 만들 수 없다. Spring Boot 2.0부터는 인터페이스가 있어도 CGLIB을 기본으로 사용한다(`spring.aop.proxy-target-class=true` 기본값).

```java
// @Transactional이 동작하지 않는 대표적 케이스들

// 1. private 메서드: 프록시는 오버라이드로 동작하므로 private은 불가
@Service
class OrderService {
    @Transactional
    private void internalSave(Order o) { } // 동작 안 함: private 메서드
}

// 2. final 메서드: CGLIB 서브클래스에서 오버라이드 불가
@Service
class PaymentService {
    @Transactional
    public final void pay(Long id) { } // 동작 안 함: final 메서드
}

// 3. 같은 클래스 내부 호출 (self-invocation): 프록시를 거치지 않음
@Service
class InvoiceService {
    public void createInvoice(Order o) {
        processInvoice(o); // 프록시를 우회한 직접 호출 → @Transactional 미적용
    }

    @Transactional
    public void processInvoice(Order o) { }
}
```

| 구분 | JDK Dynamic Proxy | CGLIB |
|------|-------------------|-------|
| 조건 | 인터페이스 필요 | 인터페이스 불필요 |
| 제약 | 인터페이스 메서드만 | `final` 클래스/메서드 불가 |
| Spring Boot 기본 | 미사용 (2.0+) | 기본값 |
| 성능 | 반사(reflection) 사용 | 바이트코드 직접 조작 (더 빠름) |

---

## Q2. Decorator 체이닝의 실무 한계는 무엇인가?

### 왜 이 질문이 중요한가

데코레이터 패턴은 강력하지만, 체이닝이 깊어질수록 디버깅과 유지보수가 어려워진다. 패턴의 장점만큼 실무 제약을 이해하는 것이 성숙한 설계자의 관점이다.

### 답변

데코레이터 체이닝의 실무 한계는 세 가지로 나뉜다.

첫째, **디버깅 어려움**이다. 스택 트레이스에 데코레이터 클래스들이 겹겹이 쌓여 실제 구현체를 찾기 어렵다. Java I/O에서 `BufferedInputStream` 안에 `GZIPInputStream` 안에 `FileInputStream`이 있을 때, 예외 발생 시 어느 계층에서 문제가 생겼는지 파악하는 데 시간이 걸린다.

둘째, **순서 의존성**이다. 데코레이터를 잘못된 순서로 감싸면 동작이 달라진다. 압축 후 암호화와 암호화 후 압축은 결과가 전혀 다른데, 이를 컴파일 타임에 잡아낼 방법이 없다.

```java
// 순서가 중요한데 타입 시스템이 강제하지 못한다
InputStream correct = new GZIPInputStream(new CipherInputStream(base, cipher));
InputStream wrong   = new CipherInputStream(new GZIPInputStream(base), cipher); // 다른 결과
```

셋째, **특정 타입 접근 불가**이다. 데코레이터로 감싼 후에는 내부 구현체의 구체 타입에 접근하기 어렵다. 예를 들어 `BufferedInputStream`으로 감싼 후 내부 스트림이 `FileInputStream`인지 확인하려면 `instanceof`와 언래핑이 필요하다.

실무에서는 데코레이터 깊이를 3층 이내로 유지하고, 체이닝 생성을 팩토리 메서드로 캡슐화하여 잘못된 조합을 방지하는 것이 일반적인 대응책이다.

```java
// 팩토리로 올바른 체이닝 순서를 보장
class StreamFactory {
    static InputStream createSecureCompressedStream(InputStream base, Cipher cipher) {
        // 압축 후 암호화 순서를 강제한다
        return new CipherInputStream(new GZIPInputStream(base), cipher);
    }
}
```
