# 생성 패턴: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 정적 팩토리 메서드와 Factory Method 패턴의 차이는 무엇인가?

### 왜 이 질문이 중요한가

이름이 비슷해서 혼동하기 쉽지만 둘은 전혀 다른 개념이다. 정적 팩토리 메서드는 Effective Java에서 소개한 생성자 대안 관용구이고, Factory Method는 GoF 디자인 패턴이다. 면접에서 "팩토리 패턴을 설명해보세요"라는 질문에 둘을 혼동하면 개념 이해 부족으로 평가된다.

### 답변

**정적 팩토리 메서드**는 클래스의 `static` 메서드로, 생성자 대신 객체를 생성해 반환한다. 패턴이 아니라 관용구(idiom)에 가깝다. 이름을 붙일 수 있고(`of`, `from`, `create`, `getInstance`), 반환 타입을 인터페이스로 숨길 수 있으며, 캐싱이 가능하다.

```java
// 정적 팩토리 메서드: 같은 클래스 안에 있다
public class Money {
    private final long cents;
    private Money(long cents) { this.cents = cents; }

    public static Money of(long cents)    { return new Money(cents); }
    public static Money zero()            { return new Money(0); }
    public static Money fromDollars(double d) { return new Money((long)(d * 100)); }
}
```

**Factory Method 패턴**은 GoF 패턴으로, 객체 생성 책임을 서브클래스에 위임하는 구조다. 추상 클래스나 인터페이스에 팩토리 메서드를 선언하고, 어떤 구체 타입을 생성할지는 서브클래스가 결정한다. 상속 구조와 다형성이 핵심이다.

| 구분 | 정적 팩토리 메서드 | Factory Method 패턴 |
|------|-----------------|---------------------|
| 위치 | 같은 클래스의 `static` 메서드 | 추상 클래스/인터페이스의 인스턴스 메서드 |
| 목적 | 생성자 대안, 명시적 이름 | 생성 타입을 서브클래스에 위임 |
| 상속 | 불필요 | 필수 |
| 예시 | `List.of()`, `Optional.of()` | `AbstractController.createView()` |

---

## Q2. Builder 패턴이 record와 공존하는 방법은 무엇인가?

### 왜 이 질문이 중요한가

Java 16에서 `record`가 정식 도입되면서 "Builder를 쓸 것인가 record를 쓸 것인가"라는 선택이 생겼다. 적재적소에 사용하지 않으면 과설계 또는 불편한 API가 된다. 실무에서 두 가지를 함께 사용하는 패턴을 이해하는 것이 중요하다.

### 답변

`record`와 Builder는 경쟁 관계가 아니라 상호 보완적이다. 선택 기준은 **선택적 필드의 복잡성**과 **가변성 여부**다.

`record`가 적합한 경우는 모든 필드가 필수이고, 조합이 단순하며, 불변성이 자연스럽게 보장되어야 할 때다. DTO, 값 객체, 이벤트 페이로드가 대표적이다.

```java
// record: 모든 필드 필수, 조합 단순
record CreateOrderRequest(String userId, String productId, int quantity) {}
```

Builder가 적합한 경우는 선택적 필드가 많아서 생성자가 과부하되거나, 필드 수가 많아 순서 실수가 생길 수 있을 때다.

```java
// record + 커스텀 Builder 공존 패턴
record HttpRequest(String url, String method, Map<String, String> headers, String body, int timeoutMs) {

    // record의 compact constructor로 기본값 설정
    HttpRequest {
        method    = method    != null ? method    : "GET";
        headers   = headers   != null ? Map.copyOf(headers) : Map.of();
        timeoutMs = timeoutMs > 0     ? timeoutMs : 3000;
    }

    // 정적 팩토리로 Builder 진입점 제공
    static Builder builder(String url) { return new Builder(url); }

    static class Builder {
        private final String url;
        private String method;
        private final Map<String, String> headers = new HashMap<>();
        private String body;
        private int timeoutMs;

        Builder(String url) { this.url = url; }
        Builder method(String m)      { this.method = m; return this; }
        Builder header(String k, String v) { headers.put(k, v); return this; }
        Builder body(String b)        { this.body = b; return this; }
        Builder timeout(int ms)       { this.timeoutMs = ms; return this; }

        HttpRequest build() {
            return new HttpRequest(url, method, headers, body, timeoutMs);
        }
    }
}

// 사용
var req = HttpRequest.builder("https://api.example.com")
        .method("POST")
        .header("Authorization", "Bearer token")
        .body("{}")
        .build();
```

핵심은 `record`로 불변 저장 구조를 정의하고, Builder로 복잡한 생성 과정을 처리하는 역할 분리다. Lombok의 `@Builder`는 이 조합을 자동화하지만, `record`에는 직접 사용이 제한적이므로 위와 같이 수동으로 작성하거나 `@RecordBuilder` 같은 라이브러리를 활용할 수 있다.
