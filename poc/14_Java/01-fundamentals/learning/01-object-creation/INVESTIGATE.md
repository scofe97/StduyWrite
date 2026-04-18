# 객체 생성과 파괴: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 정적 팩토리 vs new vs 빌더, 실무에서 어떤 기준으로 선택하는가?

### 왜 이 질문이 중요한가
객체 생성 방식은 API 사용성, 테스트 용이성, 성능 세 가지를 동시에 결정한다. 면접에서는 단순히 "빌더가 더 좋다"는 답변이 아니라 각 방식의 트레이드오프를 이해하고 있는지를 본다. 실무에서도 잘못된 선택은 나중에 변경하기 어려운 API를 만들어 낸다.

### 답변

`new` 생성자는 가장 단순하지만 두 가지 근본적인 제약이 있다. 첫째, 반환 타입이 반드시 해당 클래스 자신이어야 한다. 둘째, 같은 시그니처를 가진 생성자를 두 개 만들 수 없다. 예를 들어 `new Cache(int capacity)`와 `new Cache(int ttlSeconds)`는 공존할 수 없다.

정적 팩토리 메서드는 이 두 제약을 모두 해결한다. 반환 타입으로 인터페이스나 하위 타입을 반환할 수 있어 구현을 숨길 수 있다. `List.of()`가 `Arrays.ArrayList`를 반환하지만 호출자는 `List`만 알면 되는 것이 대표적인 예다. 또한 의미 있는 이름을 붙일 수 있어 `Optional.empty()`나 `LocalDate.of(2024, 1, 1)` 처럼 의도가 명확해진다. 캐싱도 가능해서 `Boolean.valueOf(true)`는 매번 새 객체를 만들지 않는다.

```java
// 정적 팩토리의 이름 표현력
Duration.ofSeconds(30)       // vs new Duration(30) — 단위가 명확함
Duration.ofMillis(30000)     // 같은 의미를 다른 단위로, 같은 타입 반환

// 하위 타입 반환으로 구현 은닉
public static List<String> newList() {
    return new ArrayList<>();  // 나중에 CopyOnWriteArrayList로 바꿔도 호출자 코드 불변
}
```

빌더는 매개변수가 4개 이상이거나 그 중 일부가 선택적일 때 빛을 발한다. 텔레스코핑 생성자(telescoping constructor) 패턴은 매개변수 순서를 외워야 하고, JavaBeans 패턴은 세터 호출 사이 불완전한 상태가 존재한다. 빌더는 객체가 완전히 구성된 후에야 `build()`로 생성하므로 불변 객체를 자연스럽게 만든다.

```java
// 선택 기준 정리
// 매개변수 1~3개, 필수만 있음 → 정적 팩토리 또는 생성자
// 매개변수 4개 이상, 선택적 있음 → 빌더
// 동일 타입 여러 시그니처 필요 → 정적 팩토리
// 캐싱/하위 타입 반환 필요 → 정적 팩토리
User user = User.builder()
    .name("Alice")
    .email("alice@example.com")
    // age는 선택 — 누락해도 컴파일 통과, build()에서 기본값 적용
    .build();
```

실무 판단 기준을 요약하면, 값 객체(VO)나 DTO처럼 간단한 경우에는 정적 팩토리, 엔티티나 복잡한 설정 객체에는 빌더, 내부 구현을 완전히 숨겨야 하는 라이브러리 API에는 정적 팩토리가 적합하다.

---

## Q2. 싱글톤이 안티패턴이라는 의견에 대해

### 왜 이 질문이 중요한가
"싱글톤 = 디자인 패턴"이라고 배웠지만 실무에서는 "싱글톤 = 안티패턴"으로 취급되는 경우가 많다. 이 괴리를 이해하지 못하면 DI 컨테이너를 쓰면서도 싱글톤을 직접 구현하는 실수를 반복한다. 면접에서는 싱글톤의 문제점과 Spring Bean과의 관계를 함께 물어보는 경우가 많다.

### 답변

싱글톤이 안티패턴으로 불리는 이유는 세 가지다. 첫째, 전역 상태를 만든다. 전역 상태는 프로그램의 어느 부분에서나 접근할 수 있으므로 의존 관계가 코드에 드러나지 않는다. `UserService.getInstance().getUser(id)`를 보면 `UserService`가 무엇에 의존하는지 시그니처만으로 알 수 없다.

둘째, 테스트를 어렵게 만든다. 싱글톤 인스턴스는 테스트 사이에 상태가 공유되어 테스트 순서에 따라 결과가 달라진다. Mock으로 교체하는 것도 까다롭다. `getInstance()`를 직접 호출하는 코드는 런타임에 실제 구현체가 고정되므로 단위 테스트에서 격리할 방법이 없다.

```java
// 안티패턴: 숨겨진 의존성
public class OrderService {
    public void place(Order order) {
        // 의존성이 메서드 내부에 숨어있음 — 테스트 시 교체 불가
        UserService.getInstance().validate(order.getUserId());
        PaymentService.getInstance().charge(order);
    }
}

// 개선: DI로 의존성을 드러냄
public class OrderService {
    private final UserService userService;
    private final PaymentService paymentService;

    public OrderService(UserService userService, PaymentService paymentService) {
        // 의존성이 생성자에 명시됨 — 테스트 시 Mock으로 교체 가능
    }
}
```

셋째, 멀티스레드 환경에서 올바르게 구현하기 어렵다. Double-Checked Locking은 `volatile` 없이는 JMM(Java Memory Model)에 의해 깨질 수 있다. Enum을 이용한 싱글톤이 가장 안전하지만 그렇다면 애초에 DI 컨테이너에 맡기는 것이 더 낫다.

Spring이나 Guice 같은 DI 컨테이너는 기본적으로 Bean을 싱글톤 스코프로 관리한다. 이는 싱글톤의 "인스턴스 하나"라는 이점(메모리 절약, 상태 공유)을 취하면서 전역 접근자(`getInstance()`) 없이 생성자 주입으로 의존성을 관리한다. 결론적으로 싱글톤 패턴 자체가 나쁜 것이 아니라, `getInstance()`를 통한 직접 접근이 문제다. DI 컨테이너가 그 문제를 해결한다.
