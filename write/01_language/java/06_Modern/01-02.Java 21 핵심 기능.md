# Java 21 핵심 기능

---

> Java 21은 Virtual Threads로 동시성 모델을 혁신하고, 패턴 매칭 관련 기능을 GA로 확정하여 함수형·데이터 지향 프로그래밍의 표현력을 크게 높인 LTS다.

## 기능 분류 개요

Java 21(JDK 21, 2023년 9월)은 총 15개의 JEP를 포함한다. 기능은 안정성에 따라 세 단계로 분류된다.

| 분류 | 설명 | 대표 기능 |
|------|------|----------|
| GA (General Availability) | 정식 기능, 실무 적용 가능 | Virtual Threads, Sequenced Collections, Record Patterns, Pattern Matching for switch |
| Preview | 피드백 수집 중, `--enable-preview` 필요 | String Templates, Unnamed Classes and Instance Main Methods |
| Incubator | 실험적 API, 별도 모듈 | Vector API (6차 Incubator) |

Preview와 Incubator 기능은 다음 릴리스에서 변경될 수 있으므로 프로덕션 코드에 사용하지 않는 것이 원칙이다.

## Sequenced Collections

Java의 컬렉션 계층에는 오랫동안 일관성 부재 문제가 있었다. `List`는 `get(0)`과 `get(list.size() - 1)`로 첫/마지막 요소에 접근하지만, `LinkedHashSet`은 동일한 방법을 제공하지 않았다. **Sequenced Collections**(JEP 431)는 이 문제를 해결하기 위해 세 가지 새 인터페이스를 도입했다.

- `SequencedCollection`: `getFirst()`, `getLast()`, `addFirst()`, `addLast()`, `removeFirst()`, `removeLast()`, `reversed()`
- `SequencedSet`: `SequencedCollection`을 확장하는 Set
- `SequencedMap`: `firstEntry()`, `lastEntry()`, `reversed()`, `sequencedKeySet()`, `sequencedValues()`

```java
// Sequenced Collections 활용
List<String> list = new ArrayList<>(List.of("A", "B", "C"));
System.out.println(list.getFirst()); // A
System.out.println(list.getLast());  // C

List<String> reversed = list.reversed();
System.out.println(reversed.getFirst()); // C

LinkedHashMap<String, Integer> map = new LinkedHashMap<>();
map.put("one", 1);
map.put("two", 2);
map.put("three", 3);

System.out.println(map.firstEntry()); // one=1
System.out.println(map.lastEntry());  // three=3
```

`reversed()`는 뷰(view)를 반환하므로 원본 컬렉션을 변경하지 않는다. 반환된 뷰를 통한 수정은 원본에 반영된다.

## Pattern Matching for switch

**Pattern Matching for switch**(JEP 441)는 Java 21에서 GA가 되었다. 기존 switch는 정수형, 문자열, 열거형만 지원했지만, 이제 임의의 타입에 대한 패턴 매칭을 지원한다.

*가드 패턴(guard pattern)*은 `when` 절을 사용하여 패턴에 추가 조건을 부여한다. 타입 매칭과 값 조건을 한 case에 결합할 수 있다.

```java
// Pattern Matching for switch - 가드 패턴과 null 처리
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double w, double h) implements Shape {}
record Triangle(double base, double height) implements Shape {}

String classify(Shape shape) {
    return switch (shape) {
        case Circle c when c.radius() > 10 -> "Large circle"
        case Circle c -> "Small circle"
        case Rectangle r when r.w() == r.h() -> "Square"
        case Rectangle r -> "Rectangle"
        case Triangle t -> "Triangle"
    };
}

// null 처리: NullPointerException 대신 null case 사용
String describe(Object obj) {
    return switch (obj) {
        case null -> "null value"
        case Integer i -> "Integer: " + i
        case String s -> "String: " + s
        default -> "Other: " + obj.getClass().getSimpleName()
    };
}
```

Sealed class와 함께 사용하면 컴파일러가 모든 서브타입이 처리되었는지 검증한다. `default` 없이도 exhaustiveness가 보장되어 새 서브타입 추가 시 컴파일 오류로 누락을 즉시 발견할 수 있다.

## Record Patterns

**Record Patterns**(JEP 440)는 레코드의 컴포넌트를 패턴 매칭으로 직접 분해(destructuring)한다. `instanceof`나 switch의 case에서 레코드 내부 값을 변수에 바로 바인딩할 수 있다.

*중첩 분해(nested deconstruction)*는 레코드 안의 레코드를 한 번의 패턴으로 분해한다. 복잡한 데이터 구조를 탐색하는 코드를 간결하게 만든다.

```java
// Record Patterns - 중첩 분해
record Point(double x, double y) {}
record Line(Point start, Point end) {}
record ColoredLine(Line line, String color) {}

void printLineInfo(Object obj) {
    if (obj instanceof ColoredLine(Line(Point(var x1, var y1), Point(var x2, var y2)), var color)) {
        System.out.printf(
                "%s line from (%.1f, %.1f) to (%.1f, %.1f)%n"
                , color, x1, y1, x2, y2
        );
    }
}

// 제네릭 레코드 패턴
record Box<T>(T value) {}

void processBox(Box<?> box) {
    switch (box) {
        case Box<Integer>(var i) -> System.out.println("Integer box: " + i);
        case Box<String>(var s) -> System.out.println("String box: " + s);
        default -> System.out.println("Other box");
    }
}
```

## String Templates (Preview)

**String Templates**(JEP 430, Preview)는 문자열 보간을 안전하게 처리하는 메커니즘이다. 단순한 문자열 연결이 아니라 *템플릿 프로세서*가 개입하여 값을 처리한다. 이로써 SQL 인젝션 같은 보안 취약점을 템플릿 수준에서 차단할 수 있다.

`STR` 프로세서는 표현식을 문자열로 변환하고, `FMT` 프로세서는 `printf` 스타일 포맷을 지원한다. `--enable-preview` 플래그가 필요하며, Java 23에서 설계 재검토로 철회되었으므로 최종 형태는 달라질 수 있다.

```java
// String Templates (Java 21 Preview - 참고용)
// 실행 시 --enable-preview 필요
String name = "World";
int count = 42;

String message = STR."Hello, \{name}! Count: \{count}";
// Hello, World! Count: 42

String formatted = FMT."Value: %5.2f\{Math.PI}";
// Value:  3.14
```

## Unnamed Patterns and Variables

**Unnamed Patterns and Variables**(JEP 443, Preview)는 사용하지 않는 변수를 `_`(언더스코어)로 표시한다. 패턴 매칭에서 특정 컴포넌트가 필요 없을 때 이름 없이 처리할 수 있다.

```java
// Unnamed Patterns and Variables
record Point(int x, int y, int z) {}

// z 좌표는 필요 없을 때
if (point instanceof Point(var x, var y, _)) {
    System.out.println("2D: " + x + ", " + y);
}

// try-catch에서 예외 변수 미사용
try {
    riskyOperation();
} catch (Exception _) {
    System.out.println("Operation failed");
}

// 향상된 for 루프에서 인덱스 미사용
for (var _ : list) {
    count++;
}
```

`_`를 사용하면 컴파일러에게 "이 변수는 의도적으로 무시한다"는 신호를 준다. Java 22에서 GA로 확정되었다.

## Key Encapsulation Mechanism API

**KEM API**(JEP 452)는 공개 키 암호화를 기반으로 대칭 키를 안전하게 교환하는 알고리즘을 위한 표준 인터페이스다. 기존 `KeyAgreement` API로는 표현하기 어려웠던 KEM 알고리즘(예: CRYSTALS-Kyber)을 `javax.crypto.KEM` 클래스로 통일된 방식으로 사용할 수 있다.

양자 컴퓨팅 내성 암호화(Post-Quantum Cryptography) 알고리즘 지원을 위한 기반으로, 직접 사용 빈도는 낮지만 보안 라이브러리와 TLS 구현에서 중요한 역할을 한다.

```java
// KEM API 사용 예시
KEM kem = KEM.getInstance("DHKEM(X25519, HKDF-SHA256)");
KeyPairGenerator gen = KeyPairGenerator.getInstance("X25519");
KeyPair recipientKeyPair = gen.generateKeyPair();

// 발신자: 캡슐화
KEM.Encapsulator encapsulator = kem.newEncapsulator(recipientKeyPair.getPublic());
KEM.Encapsulated encapsulated = encapsulator.encapsulate();
SecretKey sharedKey = encapsulated.key();
byte[] encapsulation = encapsulated.encapsulation();

// 수신자: 복원
KEM.Decapsulator decapsulator = kem.newDecapsulator(recipientKeyPair.getPrivate());
SecretKey recoveredKey = decapsulator.decapsulate(encapsulation);
```
