# JDK 구조와 바이트코드: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 클래스 로더 위임 모델(Parent Delegation Model)이 보안에 기여하는 방법은 무엇인가?

### 왜 이 질문이 중요한가
클래스 로더 위임 모델은 JVM 보안 아키텍처의 핵심이며, 악의적인 코드가 핵심 Java 클래스를 가로채지 못하도록 막는 첫 번째 방어선이다. 면접에서 "Java 보안"을 물으면 Security Manager와 함께 반드시 등장하는 주제이고, 실무에서 ClassNotFoundException이나 ClassCastException이 발생했을 때 원인을 추적하려면 이 모델을 명확히 이해해야 한다.

### 답변

클래스 로더 위임 모델은 자식 로더가 클래스를 직접 로드하기 전에 반드시 부모 로더에게 먼저 위임하는 구조다. Bootstrap → Extension(Platform) → Application 순으로 계층이 형성되며, 요청은 항상 최상위 Bootstrap 로더까지 올라간 뒤 해당 클래스를 찾지 못하면 하위로 내려온다.

이 구조가 보안에 기여하는 핵심 이유는 **코어 클래스의 선점 로딩**이다. 예를 들어 공격자가 `java.lang.String`이라는 이름의 악의적인 클래스를 classpath에 심더라도, Bootstrap 로더가 이미 rt.jar(또는 Java 9+ 이후 모듈 시스템)에서 진짜 `String`을 먼저 로드했기 때문에 애플리케이션 클래스 로더가 그것을 대체할 수 없다.

```java
// 이 코드는 java.lang 패키지에 클래스를 직접 정의하려 하면 SecurityException 발생
// java.lang.Exploit 같은 이름으로 Bootstrap 영역을 침범할 수 없다
ClassLoader.getSystemClassLoader().loadClass("java.lang.String");
// → Bootstrap이 먼저 로드했으므로 시스템 로더는 캐시된 것을 반환
```

실무적으로 중요한 함정은 **동일 클래스의 다중 로드** 문제다. OSGi나 WAS 환경에서 서로 다른 클래스 로더가 같은 클래스를 각각 로드하면 `ClassCastException: com.example.Foo cannot be cast to com.example.Foo`가 발생한다. 클래스 동일성 판단은 **클래스 이름 + 로드한 클래스 로더**의 조합으로 결정되기 때문이다.

Tomcat이나 Spring Boot의 내장 서버는 위임 모델을 의도적으로 역전(child-first)해 애플리케이션 라이브러리가 서버 라이브러리보다 우선하도록 만든다. 이는 `log4j` 같은 라이브러리의 버전 충돌을 방지하기 위한 의도적 설계이며, 표준 위임 모델의 예외 케이스로 반드시 알아둬야 한다.

---

## Q2. javap로 바이트코드를 분석해야 하는 실무 상황은 어떤 것들이 있는가?

### 왜 이 질문이 중요한가
소스 코드만으로는 JVM이 실제로 무엇을 실행하는지 알 수 없는 경우가 있다. 특히 람다, try-with-resources, String switch 같은 문법 설탕(syntactic sugar)이 어떤 바이트코드로 변환되는지 이해하지 못하면 성능 문제나 디버깅 시 잘못된 방향으로 시간을 낭비할 수 있다. `javap`는 소스 없이 .class 파일만 있을 때도 사용할 수 있어 서드파티 라이브러리 디버깅에도 쓸모 있다.

### 답변

`javap`의 핵심 옵션은 `-c`(바이트코드 출력)와 `-verbose`(상수 풀, 스택 크기 포함 전체 출력)다. 실무에서 가장 자주 쓰이는 상황은 아래와 같다.

**첫 번째 상황: 람다 vs 익명 클래스 비용 비교.** 람다가 `invokedynamic`을 사용한다는 것은 알지만, 실제로 어떻게 동작하는지는 바이트코드를 봐야 확인된다. 다음처럼 분석할 수 있다.

```bash
# 컴파일 후 바이트코드 역어셈블
javac LambdaTest.java
javap -c -verbose LambdaTest.class

# 핵심: invokedynamic 호출 시 LambdaMetafactory가 최초 1회만 실행됨을 확인
# invokedynamic #5, 0 // InvokeDynamic #0:apply:()Ljava/util/function/Function;
```

**두 번째 상황: try-with-resources의 실제 구조 확인.** Java 컴파일러는 try-with-resources를 try-catch-finally로 변환하면서 예외 억제(suppressed exception) 로직도 자동 삽입한다. 억제된 예외가 사라지는 버그를 디버깅할 때 바이트코드를 보면 문제 원인이 명확해진다.

**세 번째 상황: 불필요한 객체 생성 확인.** String 연결을 루프 안에서 할 때 `+` 연산자가 `StringBuilder`로 변환되는지, 아니면 매 반복마다 새 StringBuilder를 생성하는지 바이트코드로 확인할 수 있다.

```bash
# Java 11 이전과 이후의 String 연결 바이트코드가 다름
# Java 9+: invokedynamic + StringConcatFactory (더 최적화됨)
javap -c StringConcatTest.class | grep -A3 "invokedynamic\|StringBuilder"
```

**네 번째 상황: 접근 제어 우회 확인.** 리플렉션이나 직렬화 라이브러리가 private 필드에 접근하는 방식, 또는 내부 클래스에서 outer 클래스의 private 멤버에 접근할 때 컴파일러가 생성하는 `access$000` 합성 메서드 확인에도 유용하다.
