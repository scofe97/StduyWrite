# 클래스와 인터페이스: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 상속 vs 합성, 실무에서의 판단 기준

### 왜 이 질문이 중요한가
"상속보다 합성을 선호하라"는 원칙은 GoF 이후 수십 년간 반복된 조언이지만, 실무에서 구체적으로 어떤 상황에 어떤 것을 선택해야 하는지 설명하지 못하는 경우가 많다. 면접에서는 이 원칙의 이유와 위반 시 어떤 문제가 생기는지를 사례 중심으로 묻는다.

### 답변

상속의 근본 문제는 캡슐화를 깨뜨린다는 점이다. 하위 클래스는 상위 클래스의 내부 구현에 의존하게 된다. 상위 클래스가 내부 구현을 바꾸면 하위 클래스가 조용히 깨질 수 있다. `HashSet`을 상속해서 원소 추가 횟수를 세는 `InstrumentedHashSet`을 만들면, `addAll()`이 내부적으로 `add()`를 호출한다는 사실에 의존하게 된다. Java 버전이 바뀌어 `addAll()` 구현이 바뀌면 카운팅 로직이 틀어진다.

```java
// 상속 — 상위 클래스 구현에 의존하는 취약한 설계
class InstrumentedHashSet<E> extends HashSet<E> {
    private int addCount = 0;

    @Override public boolean add(E e) { addCount++; return super.add(e); }
    @Override public boolean addAll(Collection<? extends E> c) {
        addCount += c.size(); return super.addAll(c);
        // 문제: HashSet.addAll()이 내부에서 add()를 호출하면
        // addCount가 두 번 증가함
    }
}

// 합성 — 내부 구현 변화에 무관
class InstrumentedSet<E> implements Set<E> {
    private final Set<E> delegate; // 감싸기
    private int addCount = 0;

    @Override public boolean add(E e) { addCount++; return delegate.add(e); }
    @Override public boolean addAll(Collection<? extends E> c) {
        addCount += c.size(); return delegate.addAll(c);
        // delegate의 addAll이 내부에서 add를 호출해도 이 클래스의 add는 호출되지 않음
    }
}
```

상속이 적합한 경우는 두 조건을 모두 만족할 때다. 첫째, is-a 관계가 명확하다(Dog is-a Animal). 둘째, 상위 클래스가 변경될 가능성이 낮거나 내가 제어할 수 있다. 특히 같은 패키지 내에서 상위 클래스의 내부 구현을 알고 설계된 경우, 또는 추상 클래스를 통해 상속을 위해 문서화된 경우에는 상속이 적합하다.

합성이 적합한 경우는 외부 라이브러리 클래스를 확장하거나, 기능을 추가하기 위해 기존 클래스를 재사용하려는 경우다. "has-a" 관계거나 구현 재사용이 목적이라면 합성을 선택한다. 실무에서 `final` 키워드가 붙은 클래스(String, Integer 등)는 상속 자체가 불가능하므로 자연스럽게 합성을 사용하게 된다.

---

## Q2. default 메서드가 다중 상속 문제를 완전히 해결하는가?

### 왜 이 질문이 중요한가
Java 8의 `default` 메서드는 인터페이스에 구현을 추가할 수 있게 했다. 이를 다중 상속으로 오해하거나, 반대로 "다이아몬드 문제를 완전히 해결했다"고 과대평가하는 경우가 있다. 실제 한계와 충돌 해결 규칙을 정확히 이해하는 것이 중요하다.

### 답변

`default` 메서드의 원래 목적은 하위 호환성이다. `Collection`에 `forEach()`, `stream()` 같은 메서드를 추가할 때 기존 모든 구현체를 수정하지 않고 인터페이스만 변경할 수 있게 하기 위해 도입됐다. 다중 상속의 편의를 위한 것이 아니다.

다이아몬드 충돌은 세 가지 우선순위 규칙으로 해결된다. 첫째, 클래스가 인터페이스보다 항상 우선한다. 클래스에서 구현한 메서드가 있으면 인터페이스의 `default`를 이긴다. 둘째, 더 구체적인(하위) 인터페이스가 우선한다. `B extends A`이고 둘 다 같은 시그니처의 `default`를 가지면 `B`의 구현이 선택된다. 셋째, 위 규칙으로도 해결이 안 되면 컴파일 에러가 발생하며 구현 클래스에서 명시적으로 재정의해야 한다.

```java
interface A { default String hello() { return "A"; } }
interface B { default String hello() { return "B"; } }

class C implements A, B {
    // 컴파일 에러 — 명시적 선택 필요
    @Override
    public String hello() {
        return A.super.hello(); // 어떤 인터페이스의 default를 쓸지 명시
    }
}
```

`default` 메서드가 해결하지 못하는 것이 있다. 상태(필드)는 여전히 다중 상속이 불가하다. 인터페이스는 상수(`static final`)만 가질 수 있으므로 인스턴스 변수의 다중 상속은 불가능하다. 또한 `Object`의 메서드(`equals`, `hashCode`, `toString`)는 인터페이스에서 `default`로 재정의할 수 없다. 모든 클래스가 `Object`를 상속하므로 클래스 우선 규칙에 의해 항상 클래스가 이기기 때문이다. 결론적으로 `default` 메서드는 타입 행동의 다중 상속만 제한적으로 허용하며, 완전한 다중 상속 해결책이 아니라 API 진화(evolution)를 위한 도구로 이해하는 것이 정확하다.
