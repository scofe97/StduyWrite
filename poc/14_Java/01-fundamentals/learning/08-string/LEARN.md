# String 클래스
---
> String은 Java에서 가장 자주 쓰이는 불변 클래스다. 불변성의 의미와 String Pool의 동작 원리를 이해하면 `==` 비교 함정을 피하고, StringBuilder를 언제 직접 써야 하는지 판단할 수 있다.

## 1. String의 구조와 불변성

String은 기본형이 아닌 참조형 클래스다. 내부적으로 문자 배열을 `private final`로 보관하며, 한 번 생성된 이후 값을 바꿀 수 없다:

```java
public final class String {
    private final byte[] value; // Java 9 이후 (이전은 char[])

    public String concat(String str) { ... }
    public int length() { ... }
}
```

Java가 `"hello"`처럼 쌍따옴표 리터럴을 허용하는 이유는 언어 차원에서 자동 변환을 지원하기 때문이다. 문자열이 워낙 자주 쓰이므로 특별 대우를 받는다.

불변성의 실질적 의미는 값 변경 메서드가 항상 새 객체를 반환한다는 것이다:

```java
String str1 = "hello";
str1.concat(" java");             // 반환값을 무시하면 아무 효과 없음
System.out.println(str1);         // "hello" — 원본 그대로

String str2 = str1.concat(" java");
System.out.println(str2);         // "hello java" — 새 객체
```

## 2. String Pool과 `==` vs `equals()`

String 리터럴을 사용하면 JVM은 **String Pool**이라는 힙 내 특별 영역에서 동일한 문자열을 재사용한다. `new String()`으로 생성하면 Pool을 거치지 않고 독립된 인스턴스가 만들어진다:

```java
String str1 = new String("hello");
String str2 = new String("hello");
System.out.println(str1 == str2);     // false — 다른 인스턴스
System.out.println(str1.equals(str2)); // true  — 값이 같음

String str3 = "hello";
String str4 = "hello";
System.out.println(str3 == str4);     // true  — Pool에서 같은 인스턴스 재사용
System.out.println(str3.equals(str4)); // true  — 값도 같음
```

`==`는 참조(주소) 동일성을 비교하고, `equals()`는 값 동등성을 비교한다. 문자열 비교에서 `==`를 쓰면 리터럴인지 `new`로 생성했는지에 따라 결과가 달라지므로, **항상 `equals()`를 사용하는 것이 원칙**이다.

String Pool 덕분에 동일 리터럴이 반복 사용되어도 메모리를 절약할 수 있다. 이것이 가능한 이유는 String이 불변이기 때문이다. 가변이었다면 한 참조자가 값을 바꿀 때 같은 인스턴스를 공유하는 다른 참조자가 영향을 받아 Pool 재사용이 불가능했을 것이다.

## 3. StringBuilder vs StringBuffer

String이 불변이기 때문에 `+` 연산은 매번 새 객체를 만든다. 짧은 연결은 큰 문제가 되지 않지만, 반복문 안에서 누적하면 불필요한 객체가 폭발적으로 생성된다:

```java
String result = "";
for (int i = 0; i < 100_000; i++) {
    result += "Hello Java "; // 매 반복마다 새 String 생성
}
```

이 문제를 해결하는 것이 **StringBuilder**다. 내부 버퍼를 직접 수정하므로 중간 객체가 생기지 않는다:

```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 100_000; i++) {
    sb.append("Hello Java ");
}
String result = sb.toString();
```

StringBuilder와 StringBuffer의 차이는 스레드 안전성 하나다:

| 클래스 | 스레드 안전 | 성능 | 사용 상황 |
|--------|------------|------|----------|
| `StringBuilder` | X | 빠름 | 단일 스레드 (일반적) |
| `StringBuffer` | O | 느림 | 멀티스레드 공유 필요 시 |

대부분의 문자열 조작은 단일 스레드에서 이루어지므로 `StringBuilder`가 기본 선택이다. `StringBuffer`는 명시적으로 멀티스레드 공유가 필요한 경우에만 사용한다.

StringBuilder는 메서드 체이닝을 지원한다. 각 메서드가 `this`를 반환하기 때문이다:

```java
String result = new StringBuilder()
        .append("A")
        .append("B")
        .insert(1, "X")
        .delete(1, 2)
        .reverse()
        .toString();
```

## 4. Text Block

Java 15에서 정식 도입된 **Text Block(`"""`)**은 여러 줄 문자열을 가독성 있게 선언하는 방법이다. 특히 JSON, SQL, HTML처럼 들여쓰기와 줄바꿈이 중요한 문자열에 유용하다:

```java
// 기존 방식
String json = "{\n" +
              "  \"name\": \"John\",\n" +
              "  \"age\": 30\n" +
              "}";

// Text Block
String json = """
        {
          "name": "John",
          "age": 30
        }
        """;
```

Text Block의 들여쓰기 기준은 닫는 `"""`의 위치다. 닫는 따옴표 앞 공백만큼 각 줄의 앞부분이 제거된다. 따라서 닫는 `"""`를 소스 들여쓰기와 같은 열에 두면 의도한 문자열만 남는다.

## 5. String 주요 메서드

자주 쓰이는 메서드를 카테고리별로 정리하면 다음과 같다. 외우기보다 카테고리를 기억해 두고 필요할 때 찾는 방식이 실용적이다:

```java
String str = "Hello World";

// 정보 조회
str.length();           // 11
str.isEmpty();          // false
str.isBlank();          // false (Java 11, 공백 포함 검사)
str.charAt(0);          // 'H'

// 비교
str.equals("hello world");              // false (대소문자 구분)
str.equalsIgnoreCase("hello world");    // true
str.startsWith("Hello");                // true
str.endsWith("World");                  // true
str.contains("lo W");                   // true

// 검색
str.indexOf("o");       // 4 (첫 번째 위치)
str.lastIndexOf("o");   // 7 (마지막 위치)

// 변환
str.substring(6);                       // "World"
str.substring(0, 5);                    // "Hello"
str.replace("World", "Java");           // "Hello Java"
str.toLowerCase();                      // "hello world"
str.toUpperCase();                      // "HELLO WORLD"
str.strip();                            // 앞뒤 공백 제거 (Java 11, trim()의 유니코드 대응 버전)

// 분리/조합
String[] parts = str.split(" ");        // ["Hello", "World"]
String.join("-", "2024", "01", "01");   // "2024-01-01"

// 변환 유틸
String.valueOf(123);                    // "123"
str.toCharArray();                      // char[]
```

## 6. `String.format()` vs `formatted()`

문자열 템플릿을 만들 때 전통적으로 `String.format()`을 사용했다. Java 15부터는 인스턴스 메서드인 `formatted()`를 사용할 수 있어 코드가 더 간결해진다:

```java
// 전통적 방식
String msg1 = String.format("Name: %s, Age: %d", "Alice", 30);

// Java 15+ 방식
String msg2 = "Name: %s, Age: %d".formatted("Alice", 30);
```

두 방식은 동작이 동일하다. 단순한 포맷팅에는 `formatted()`가 더 읽기 좋고, 포맷 문자열을 상수로 분리해 재사용할 경우에는 `String.format()`이 적합하다.

## 7. 문자열 연결의 컴파일러 최적화

Java 컴파일러는 컴파일 시점에 알 수 있는 문자열 상수를 미리 연결한다:

```java
// 소스 코드
String s = "Hello, " + "World!";

// 컴파일 후 (상수 폴딩)
String s = "Hello, World!";
```

변수를 포함한 연결은 `StringBuilder`로 변환한다:

```java
// 소스 코드
String result = str1 + str2;

// Java 8 이하 컴파일 후
String result = new StringBuilder().append(str1).append(str2).toString();
```

Java 9부터는 `StringConcatFactory`를 사용하는 invokedynamic 방식으로 전환됐다. JIT 컴파일러가 런타임에 최적의 연결 전략을 선택하므로 이전보다 성능이 향상됐다.

그러나 컴파일러 최적화가 효과를 발휘하지 못하는 상황이 있다. 반복문 안에서의 연결이 대표적이다:

```java
// 컴파일러 최적화 후에도 반복마다 StringBuilder가 새로 생성됨
for (int i = 0; i < 100_000; i++) {
    result = new StringBuilder().append(result).append("Hello Java ").toString();
}

// StringBuilder를 루프 밖으로 꺼내야 진짜 최적화
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 100_000; i++) {
    sb.append("Hello Java ");
}
String result = sb.toString();
```

StringBuilder를 직접 사용해야 하는 상황은 네 가지다:

- 반복문에서 문자열을 반복 누적할 때
- 조건에 따라 동적으로 문자열을 조합할 때
- 특정 위치의 부분 문자열을 변경해야 할 때
- 매우 긴 대용량 문자열을 처리할 때
