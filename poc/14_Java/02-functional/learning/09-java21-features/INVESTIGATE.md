# Java 21 주요 기능: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Pattern Matching switch가 기존 if-else 체인을 대체하는 실무 시나리오는 무엇인가

### 왜 이 질문이 중요한가
Pattern Matching for switch(Java 21 정식)는 단순히 문법을 줄이는 것이 아니라 타입 안전한 다형성 표현을 가능하게 한다. 실무 시나리오를 알아야 언제 적용할지 판단하고, 기존 코드의 개선 방향을 제시할 수 있다.

### 답변
Pattern Matching switch가 가장 빛나는 시나리오는 sealed class나 sealed interface의 모든 하위 타입을 처리하는 경우다. 컴파일러가 모든 케이스가 커버되었는지 검사(exhaustiveness check)해주어 새 하위 타입이 추가되면 컴파일 에러로 즉시 알려준다.

```java
// 기존 instanceof 체인 — 타입 안전성 없음, 새 타입 추가 시 런타임까지 모름
String describe(Shape shape) {
    if (shape instanceof Circle c) {
        return "Circle r=" + c.radius();
    } else if (shape instanceof Rectangle r) {
        return "Rect " + r.width() + "x" + r.height();
    } else if (shape instanceof Triangle t) {
        return "Triangle base=" + t.base();
    }
    throw new IllegalArgumentException("Unknown: " + shape);
}

// Pattern Matching switch — exhaustiveness 검사, 간결함
String describe(Shape shape) {
    return switch (shape) {
        case Circle c    -> "Circle r=" + c.radius();
        case Rectangle r -> "Rect " + r.width() + "x" + r.height();
        case Triangle t  -> "Triangle base=" + t.base();
        // sealed interface라면 default 없어도 컴파일 가능
        // 새 하위 타입 추가 시 여기서 컴파일 에러
    };
}
```

두 번째 실무 시나리오는 JSON/API 응답 처리다. 다양한 이벤트 타입이나 메시지 타입을 처리하는 코드에서 기존의 `instanceof` 체인이나 Visitor 패턴을 대체할 수 있다.

세 번째는 guard 패턴을 활용한 조건 분기다. `when` 절로 타입 체크와 값 조건을 한 표현식에 담는다.

```java
String classify(Object obj) {
    return switch (obj) {
        case Integer i when i < 0  -> "negative int";
        case Integer i when i == 0 -> "zero";
        case Integer i             -> "positive int: " + i;
        case String s when s.isEmpty() -> "empty string";
        case String s  -> "string: " + s;
        case null      -> "null";
        default        -> "other: " + obj.getClass().getSimpleName();
    };
}
```

기존 코드에서 `if-else instanceof` 체인이 5개 이상이거나 새 타입 추가 시 여러 곳을 수정해야 한다면 Pattern Matching switch + sealed interface 조합으로 리팩토링할 가치가 있다.

---

## Q2. String Templates 철회(Java 23)의 의미는 무엇인가

### 왜 이 질문이 중요한가
Java 21, 22에서 Preview로 제공되던 String Templates가 Java 23에서 철회(withdrawn)된 것은 드문 일이다. 이 결정의 배경을 이해하면 Java 언어 설계 철학과 Preview 프로세스의 의미를 더 깊이 이해할 수 있다.

### 답변
String Templates(JEP 430, 459)는 `STR."Hello \{name}!"` 형태의 문자열 보간(interpolation)을 도입하려 했다. Python의 f-string, Kotlin의 문자열 템플릿과 유사하지만 Java는 더 야심찬 설계를 추구했다.

Java의 String Templates는 단순 보간을 넘어 템플릿 프로세서(Template Processor)를 교체 가능하게 설계했다. `STR`(단순 보간), `FMT`(형식 지정), `RAW`(미처리 템플릿)를 제공하고 사용자 정의 프로세서도 만들 수 있었다. SQL 인젝션 방지를 위한 `DB."SELECT * FROM users WHERE id = \{id}"`처럼 컨텍스트 인식 이스케이핑을 지원하는 것이 목표였다.

```java
// Java 21-22 Preview (현재는 철회됨)
String name = "World";
String greeting = STR."Hello \{name}!"; // "Hello World!"

// SQL 안전 보간 (목표)
PreparedStatement stmt = DB."SELECT * FROM t WHERE id = \{userId}";
// 내부적으로 파라미터 바인딩으로 처리 — SQL 인젝션 불가
```

철회 이유는 API 설계가 충분히 성숙하지 않았다는 판단 때문이다. OpenJDK 팀은 다음 문제들을 지적했다. 첫째, `StringTemplate` 타입이 API 곳곳에 노출되어 복잡성이 증가했다. 둘째, 대부분의 개발자는 커스텀 프로세서를 만들 필요가 없는데 그 복잡성이 기본 사용을 어렵게 만들었다. 셋째, 단순 보간을 위한 더 간단한 대안을 먼저 탐색할 필요가 있었다.

이 철회가 주는 교훈은 두 가지다. 첫째, Java의 Preview 프로세스가 실제로 기능한다는 증거다. Preview가 단순한 "예고"가 아니라 피드백을 반영해 철회할 수 있는 진짜 실험 단계임을 보여준다. 둘째, 언어 기능은 단순히 다른 언어의 기능을 복사하는 것이 아니라 Java 생태계 전체와의 정합성을 고려해야 한다는 것이다. 향후 더 단순한 형태의 문자열 보간이 별도 JEP로 제안될 가능성이 있다.
