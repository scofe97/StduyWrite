# Enum: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. enum 상수별 메서드 구현 vs 전략 패턴, 어떤 상황에서 어떤 것을 사용하는가?

### 왜 이 질문이 중요한가
enum에 추상 메서드를 선언하고 각 상수가 구현하는 패턴은 전략 패턴을 대체할 수 있다. 그러나 이 둘을 혼동해서 쓰면 유지보수하기 어려운 코드가 만들어진다. 언제 enum 자체 구현을, 언제 별도 전략 객체를 써야 하는지 판단 기준이 필요하다.

### 답변

enum 상수별 메서드 구현(constant-specific method implementation)은 enum의 각 상수가 추상 메서드를 서로 다르게 구현하는 패턴이다. 상수와 행동이 항상 함께 다닌다는 것이 핵심이다.

```java
// enum 상수별 구현 — 상수와 행동이 결합됨
enum Operation {
    PLUS("+")  { @Override public double apply(double x, double y) { return x + y; } },
    MINUS("-") { @Override public double apply(double x, double y) { return x - y; } },
    TIMES("*") { @Override public double apply(double x, double y) { return x * y; } },
    DIVIDE("/") { @Override public double apply(double x, double y) { return x / y; } };

    private final String symbol;
    Operation(String symbol) { this.symbol = symbol; }
    public abstract double apply(double x, double y);
}

// 사용 — 타입 안전하고 switch 불필요
double result = Operation.PLUS.apply(3, 4); // 7.0
```

이 패턴이 적합한 경우는 행동이 단순하고(몇 줄 이내), 상수와 행동의 결합이 자연스러우며, 상수 목록이 안정적(자주 추가되지 않음)인 경우다.

반면 전략 패턴이 적합한 경우는 세 가지다. 첫째, 전략이 상태를 가지거나 외부 의존성(서비스, 레포지토리)이 필요할 때다. enum 상수는 정적이므로 Spring Bean을 주입받을 수 없다. 둘째, 전략 구현이 복잡해서 별도 클래스로 분리해야 가독성이 높아질 때다. 각 구현이 100줄을 넘는다면 enum 내부에 넣는 것은 가독성을 해친다. 셋째, 런타임에 전략을 교체하거나 조합해야 할 때다.

```java
// 전략 패턴 — 외부 의존성이 있거나 구현이 복잡할 때
interface DiscountStrategy {
    Money calculate(Order order);
}

@Component
class MemberDiscountStrategy implements DiscountStrategy {
    private final MemberRepository memberRepository; // Spring Bean 주입 가능

    @Override
    public Money calculate(Order order) {
        Member member = memberRepository.findById(order.getMemberId());
        return order.totalPrice().multiply(member.getDiscountRate());
    }
}

enum DiscountType {
    MEMBER, VIP, COUPON;
    // 타입만 정의, 전략은 별도 클래스로 관리
}
```

판단 기준을 하나로 정리하면, "행동 구현이 3줄 이내이고 외부 의존성이 없다면 enum 상수별 구현, 그 외에는 전략 패턴"이다.

---

## Q2. ordinal()을 쓰면 안 되는 이유

### 왜 이 질문이 중요한가
`ordinal()`은 enum 상수의 선언 순서(0부터 시작)를 반환한다. 이를 DB 저장이나 배열 인덱스로 쓰는 코드를 실무에서 자주 발견할 수 있다. 왜 이것이 시한폭탄인지 이해해야 레거시 코드의 버그를 예방할 수 있다.

### 답변

`ordinal()`의 근본 문제는 순서가 의미 있는 값으로 취급될 때 드러난다. 새 상수를 중간에 추가하거나 순서를 재배치하면 기존 값의 `ordinal()`이 달라진다.

```java
// 위험한 패턴 — ordinal을 DB에 저장
enum Priority { LOW, MEDIUM, HIGH }
// DB에 0=LOW, 1=MEDIUM, 2=HIGH 저장

// 나중에 CRITICAL 추가
enum Priority { LOW, MEDIUM, HIGH, CRITICAL } // 괜찮아 보임
// 그런데 순서 변경 시
enum Priority { LOW, MEDIUM, CRITICAL, HIGH } // CRITICAL을 HIGH보다 먼저 두고 싶어서
// 이제 DB의 2는 CRITICAL이고 3은 HIGH — 기존 데이터가 모두 잘못된 의미로 읽힘!
```

올바른 대안은 두 가지다. 첫째, `name()`을 문자열로 저장한다. "LOW", "MEDIUM", "HIGH"를 그대로 저장하면 순서 변경에 영향을 받지 않는다. JPA에서는 `@Enumerated(EnumType.STRING)`이 이에 해당한다. 단점은 상수 이름을 변경하면 기존 데이터와 매핑이 깨진다.

둘째, 명시적 값 필드를 사용한다. `ordinal()`에 의존하지 않고 직접 정의한 값을 저장한다.

```java
// 권장 패턴 — 명시적 코드 필드
enum Priority {
    LOW(1), MEDIUM(2), HIGH(3), CRITICAL(4);

    private final int code;
    Priority(int code) { this.code = code; }
    public int getCode() { return code; }

    public static Priority fromCode(int code) {
        return Arrays.stream(values())
            .filter(p -> p.code == code)
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Unknown code: " + code));
    }
}

// JPA에서 코드 기반 변환
@Convert(converter = PriorityConverter.class)
private Priority priority;
```

이제 상수를 어떤 순서로 선언해도, 새 상수를 어디에 추가해도 DB에 저장된 숫자와의 매핑은 변하지 않는다. `ordinal()`이 유일하게 안전하게 쓸 수 있는 경우는 `EnumSet`과 `EnumMap`의 내부 구현처럼 JDK 자체적으로 최적화 목적으로 사용하는 때뿐이며, 애플리케이션 코드에서 직접 사용하는 것은 피해야 한다.
