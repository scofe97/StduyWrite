# 가상 머신 실행 서브시스템: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. invokedynamic이 람다와 문자열 연결에 사용되는 이유는 무엇인가?

### 왜 이 질문이 중요한가
`invokedynamic`은 Java 7에서 도입된 이후 람다(Java 8), 문자열 연결 최적화(Java 9), 레코드·패턴 매칭(Java 16+)까지 Java 언어 진화의 핵심 기반이 됐다. 이것을 이해하면 "람다는 왜 익명 클래스보다 빠른가?", "Java 21의 패턴 매칭은 어떻게 동작하는가?" 같은 질문에 일관된 답을 줄 수 있다. invokedynamic을 모르면 JVM 최적화에 대한 이해가 피상적 수준에 머문다.

### 답변

기존 invoke 명령어(`invokevirtual`, `invokeinterface`, `invokespecial`, `invokestatic`)는 모두 컴파일 타임에 호출 대상이 고정된다. 반면 `invokedynamic`은 **호출 사이트(call site)의 첫 실행 시점에 부트스트랩 메서드를 통해 실제 호출 대상을 동적으로 연결**하며, 이후 연결된 메서드 핸들을 캐시해 재사용한다.

람다의 경우 컴파일러는 람다 본문을 합성 정적 메서드로 추출하고, 호출 사이트에 `invokedynamic`을 삽입한다. 부트스트랩 메서드는 `LambdaMetafactory.metafactory()`이며, **최초 1회 실행 시 바이트코드를 동적 생성**해 함수형 인터페이스 구현 클래스를 만든다. 이후 같은 호출 사이트에서는 이 클래스를 재사용한다.

```java
// 소스 코드
Function<String, Integer> f = s -> s.length();

// 바이트코드 (javap -c)
// invokedynamic #5, 0  // InvokeDynamic #0:apply:()Ljava/util/function/Function;

// 익명 클래스와의 차이: 익명 클래스는 컴파일 타임에 .class 파일을 생성하지만
// 람다는 런타임에 LambdaMetafactory가 필요에 따라 생성 → 클래스파일 수 감소
```

문자열 연결(Java 9+)도 같은 원리다. `"Hello " + name + "!"` 같은 코드가 `StringConcatFactory.makeConcatWithConstants()`를 부트스트랩으로 사용하는 `invokedynamic`으로 컴파일된다. JVM은 런타임에 최적의 연결 전략(StringBuilder, MethodHandle, intrinsic 등)을 선택할 수 있어 Java 8의 고정된 StringBuilder 방식보다 유연하게 최적화된다.

핵심 통찰은 **invokedynamic이 "언제 연결할지"를 컴파일러에서 런타임으로 미룬다**는 점이다. 이로써 JVM은 실행 환경에 따라 가장 효율적인 구현을 선택할 수 있고, 언어 설계자는 JVM 명세를 바꾸지 않고도 새 기능을 추가할 수 있다.

---

## Q2. 가상 디스패치(virtual dispatch)의 성능 비용과 JIT 최적화는 어떻게 이루어지는가?

### 왜 이 질문이 중요한가
"인터페이스가 abstract 클래스보다 느리다"거나 "final 메서드가 빠르다"는 말을 들어봤을 것이다. 이 주장의 진위와 실제 성능 영향을 이해하려면 가상 디스패치의 메커니즘과 JIT가 이를 어떻게 제거하는지 알아야 한다. 고성능 서비스에서 핫패스(hot path) 최적화를 결정할 때 이 지식이 직접 활용된다.

### 답변

가상 디스패치는 메서드 호출 시 수신자 객체의 실제 타입을 보고 vtable(가상 메서드 테이블)에서 올바른 구현을 찾는 과정이다. `invokevirtual`은 vtable 오프셋으로 구현을 찾고, `invokeinterface`는 itable(인터페이스 테이블)을 추가로 탐색하므로 이론상 `invokeinterface`가 약간 더 비싸다.

그러나 현실에서 JIT(특히 C2 컴파일러)는 **인라인 캐시(inline cache)**와 **추측적 인라이닝(speculative inlining)**으로 이 비용을 거의 없앤다.

```
호출 사이트에서 실제로 오는 타입이 단일 타입(monomorphic)인 경우
→ JIT가 직접 호출(direct call)로 최적화 (vtable 조회 생략)
→ 더 나아가 메서드 본문을 호출 사이트에 인라이닝

두 가지 타입(bimorphic)인 경우
→ if-else 체크 + 각각 인라이닝

세 가지 이상(megamorphic)인 경우
→ 최적화 포기, vtable/itable 경유
```

실무 영향: 성능에 민감한 코드에서 `List<Animal>`에 `Dog`와 `Cat`과 `Fish`가 섞여 있으면 `animal.sound()` 호출이 megamorphic이 된다. 이때 타입별로 분리된 컬렉션으로 처리하면 각 호출 사이트가 monomorphic으로 최적화된다.

```java
// megamorphic → 최적화 어려움
for (Animal a : mixedList) a.sound();

// monomorphic × 3 → 각각 인라이닝 가능
for (Dog d : dogs) d.sound();
for (Cat c : cats) c.sound();
for (Fish f : fishes) f.sound();
```

`final` 키워드는 JIT에게 "이 메서드는 오버라이드되지 않는다"는 힌트를 주지만, JIT는 클래스 계층 분석(CHA, Class Hierarchy Analysis)을 통해 `final`이 없어도 실제로 오버라이드된 서브클래스가 로드되지 않았다면 동일하게 최적화한다. 나중에 서브클래스가 로드되면 역최적화(deoptimization)가 발생한다.
