# 행동 패턴: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 전략 패턴을 람다로 대체할 때 얻는 것과 잃는 것은 무엇인가?

### 왜 이 질문이 중요한가

Java 8 이후 `@FunctionalInterface`로 선언된 전략 인터페이스는 람다로 즉시 구현할 수 있다. "그러면 전략 클래스가 필요 없는 것인가?"라는 의문이 자연스럽게 생기는데, 이에 대한 답은 단순히 "람다가 낫다"가 아니라 상황에 따라 다르다.

### 답변

**람다로 대체할 때 얻는 것**은 크게 세 가지다. 첫째, 보일러플레이트 코드 제거다. 전략마다 별도 클래스 파일이 필요 없어진다. 둘째, 호출 지점에서 의도가 명확해진다. 전략이 짧고 이름이 필요 없을 때 람다가 더 읽기 쉽다. 셋째, 조합이 쉬워진다. `Predicate.and()`, `Function.andThen()` 등 기본 제공 합성 메서드를 바로 쓸 수 있다.

**람다로 대체할 때 잃는 것**도 세 가지다. 첫째, **상태를 가질 수 없다**. 람다는 상태를 갖기 어렵고, 외부 변수를 캡처하면 사실상 effectively final만 허용된다. 복잡한 전략(예: 최근 N건의 이력을 기반으로 결정하는 전략)은 클래스로 만들어야 한다. 둘째, **재사용 단위가 불분명해진다**. 람다는 이름이 없으므로 같은 전략을 여러 곳에서 쓸 때 중복이 생기기 쉽다. 셋째, **테스트 격리가 어렵다**. 클래스 기반 전략은 단독 테스트가 쉽지만, 람다는 컨텍스트와 함께 테스트해야 한다.

```java
// 람다가 적합한 경우: 짧고, 무상태, 일회성
list.sort((a, b) -> a.name().compareTo(b.name())); // 명확하고 간결

// 클래스가 적합한 경우: 상태 있음, 재사용, 복잡한 로직
class PriorityBasedRoutingStrategy implements RoutingStrategy {
    private final Map<String, Integer> priorityMap;
    private final int maxRetries;

    // 상태를 가지며, 다양한 곳에서 재사용된다
    public Route route(Request req) { /* 복잡한 우선순위 로직 */ }
}
```

선택 기준은 **전략이 상태를 가지는가**, **여러 곳에서 재사용되는가**, **독립 테스트가 필요한가**다. 셋 중 하나라도 해당하면 클래스로 만들고, 그렇지 않으면 람다가 낫다.

---

## Q2. Template Method와 Template Callback의 선택 기준은 무엇인가?

### 왜 이 질문이 중요한가

두 패턴은 "고정된 흐름 + 변하는 부분"이라는 동일한 문제를 해결하지만 접근 방식이 다르다. 스프링은 레거시 API에서 Template Method를, 현대 API에서는 Template Callback을 많이 선택했는데, 그 이유를 이해하면 설계 결정 능력을 보여줄 수 있다.

### 답변

**Template Method**는 상속으로 확장한다. 추상 클래스를 상속하여 추상 메서드를 구현하는 방식이므로, 확장 단위가 클래스다. 재사용 가능한 타입 계층이 필요할 때, 즉 "이 추상 클래스를 상속하는 구체 클래스를 여러 개 만들 것"이라는 설계 의도가 있을 때 적합하다.

**Template Callback**은 구성으로 확장한다. 변하는 부분을 콜백 인터페이스(람다)로 주입하므로, 확장 단위가 메서드 호출이다. "매번 다른 로직을 주입하되 공통 흐름은 재사용"할 때, 즉 확장이 타입이 아니라 호출마다 다를 때 적합하다.

```java
// Template Method: 타입 계층이 목적
abstract class DataMigrator {
    public final void migrate() {
        List<Object> data = read();   // 서브클래스마다 다름
        transform(data);              // 서브클래스마다 다름
        write(data);                  // 공통
    }
    protected abstract List<Object> read();
    protected abstract void transform(List<Object> data);
    private void write(List<Object> data) { /* 공통 구현 */ }
}

class CsvToDbMigrator extends DataMigrator { /* CSV 읽기, 변환 구현 */ }
class JsonToDbMigrator extends DataMigrator { /* JSON 읽기, 변환 구현 */ }

// Template Callback: 호출마다 다른 로직 주입
class TransactionTemplate {
    public <T> T execute(TransactionCallback<T> callback) {
        begin();
        try {
            T result = callback.doInTransaction(); // 매번 다른 람다
            commit();
            return result;
        } catch (Exception e) {
            rollback();
            throw e;
        }
    }
}

// 호출마다 다른 콜백
template.execute(() -> orderRepo.save(order));
template.execute(() -> paymentRepo.save(payment));
```

| 선택 기준 | Template Method | Template Callback |
|---------|----------------|-------------------|
| 확장이 재사용 가능한 타입인가? | ✓ 적합 | 불필요 |
| 확장이 호출마다 달라지는가? | 상속으로 처리하기 어렵다 | ✓ 적합 |
| 상태가 필요한가? | 클래스 필드로 관리 | 클로저 캡처 |
| 테스트 편의성 | 서브클래스 단독 테스트 가능 | 람다 인라인으로 간결 |
