# 람다 고급: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. invokedynamic이 람다 성능에 미치는 영향은 무엇인가

### 왜 이 질문이 중요한가
"람다가 익명 클래스보다 빠르다"와 "람다가 느리다"는 주장이 공존한다. invokedynamic의 동작 원리를 이해해야 어떤 상황에서 어떤 성능 특성을 가지는지 정확히 설명할 수 있고, JIT 최적화 대상을 논할 수 있다.

### 답변
`invokedynamic`은 Java 7에서 도입된 JVM 명령어로, 람다는 Java 8에서 이를 활용해 구현된다. 첫 실행 시 bootstrap method인 `LambdaMetafactory.metafactory()`가 호출되어 해당 람다를 구현하는 클래스를 런타임에 생성한다. 이 과정은 한 번만 발생하고 이후 호출에서는 Call Site가 이미 생성된 구현체를 직접 가리킨다.

성능 관점에서 invokedynamic의 핵심 장점은 JVM 구현이 최적화 전략을 자유롭게 선택할 수 있다는 것이다. HotSpot JVM은 상황에 따라 다른 전략을 사용한다. 캡처 변수가 없는 stateless 람다는 싱글턴 인스턴스를 반환해 객체 생성 비용이 0이다. 캡처 변수가 있는 람다는 매 호출마다 새 인스턴스를 생성한다.

```java
// Stateless 람다 — JVM이 싱글턴으로 최적화 가능
Comparator<String> c1 = String::compareTo; // 매번 같은 인스턴스

// 캡처 람다 — 매번 새 인스턴스
String prefix = "Hello";
Predicate<String> p = s -> s.startsWith(prefix); // 매 호출마다 새 인스턴스
```

JIT 컴파일러는 람다 호출을 인라인(inline)할 수 있어 메서드 호출 오버헤드를 제거한다. 이 최적화는 익명 클래스에도 적용되므로 단순 성능 차이는 미미하다. 실질적인 성능 차이는 클래스 로딩 시간에서 나온다. 익명 클래스는 컴파일 시 생성된 .class 파일을 JVM 시작 시 로드하지만, 람다는 처음 실행 시점에 동적 생성하므로 초기 클래스 로딩 비용이 분산된다.

성능 측정 시 항상 JMH(Java Microbenchmark Harness)를 사용해야 한다. JIT 워밍업 없이 측정하면 람다가 느려 보이고, 워밍업 후 측정하면 거의 차이가 없는 경우가 많다.

---

## Q2. 직렬화 가능 람다(Serializable lambda)의 위험성은 무엇인가

### 왜 이 질문이 중요한가
프레임워크(특히 분산 처리 프레임워크 Apache Spark, Flink 등)는 람다를 직렬화해 네트워크로 전송한다. 람다 직렬화의 내부 동작과 위험을 모르면 보안 취약점을 만들거나 미묘한 버그를 유발한다.

### 답변
람다를 직렬화하려면 함수형 인터페이스가 `Serializable`을 함께 구현해야 한다. Java는 이를 위한 캐스트 문법을 제공한다.

```java
Runnable r = (Runnable & Serializable) () -> System.out.println("hello");
```

직렬화된 람다는 `SerializedLambda` 객체로 변환된다. 이 객체에는 람다를 정의한 클래스 이름, 메서드 이름, 메서드 시그니처, 캡처한 변수들이 포함된다. 역직렬화 시 JVM은 이 정보를 토대로 원본 람다를 재구성한다.

첫 번째 위험은 보안이다. Java 역직렬화 취약점의 오랜 역사처럼, 직렬화된 람다도 악의적으로 조작된 바이트스트림을 역직렬화할 때 임의 코드 실행으로 이어질 수 있다. `SerializedLambda`의 `readResolve` 메서드가 클래스 로더와 리플렉션을 사용하기 때문이다.

두 번째 위험은 버전 불일치다. 람다가 정의된 클래스가 변경되면 이전에 직렬화된 람다를 역직렬화할 수 없다. 익명 클래스의 `serialVersionUID`처럼 람다는 암묵적인 버전 관리 메커니즘이 없어 클래스 변경 시 `InvalidClassException`이 발생한다.

```java
// 역직렬화 실패 시나리오
// v1: Runnable r = (Runnable & Serializable) () -> System.out.println("v1");
// v1을 직렬화 후 저장
// v2에서 클래스 변경 → 역직렬화 시 예외 발생 가능

// 직렬화된 람다 내부 확인 방법
Runnable r = (Runnable & Serializable) () -> System.out.println("hello");
Method writeReplace = r.getClass().getDeclaredMethod("writeReplace");
writeReplace.setAccessible(true);
SerializedLambda sl = (SerializedLambda) writeReplace.invoke(r);
System.out.println(sl.getImplClass()); // 구현 클래스 이름
```

세 번째 위험은 캡처 변수다. 람다가 캡처한 외부 객체도 함께 직렬화된다. 이 객체가 직렬화 불가능하면 `NotSerializableException`이 발생하고, 직렬화 가능하더라도 예상보다 훨씬 많은 객체 그래프가 직렬화될 수 있다. 특히 `this`를 암묵적으로 캡처하는 람다(비정적 컨텍스트의 람다)는 해당 클래스 전체를 직렬화한다.
