# String: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. String Pool과 GC의 관계

### 왜 이 질문이 중요한가
String Pool은 Java 면접의 단골 주제지만 "리터럴은 Pool에 저장된다"는 단편적 지식만 있는 경우가 많다. Pool이 메모리 어디에 있는지, GC와 어떻게 상호작용하는지, `intern()`의 실제 비용은 얼마인지까지 이해해야 메모리 문제를 진단할 수 있다.

### 답변

Java 7 이전에는 String Pool이 PermGen(Permanent Generation)에 위치했다. PermGen은 고정 크기 영역으로 GC 대상이 아니었기 때문에 `intern()`을 남용하면 `OutOfMemoryError: PermGen space`가 발생했다. Java 7부터 String Pool이 Heap으로 이동했다. 이 변경의 핵심적 의미는 Pool 내의 String도 이제 GC 대상이 된다는 점이다.

구체적으로, String Pool의 엔트리는 WeakReference 방식으로 참조된다. Pool 외부에서 해당 String을 참조하는 곳이 없어지면 GC가 그 엔트리를 수거할 수 있다. 이는 PermGen 시절의 영구 보존과 근본적으로 다르다.

```java
// 리터럴 — 컴파일 타임에 Pool에 등록, 클래스가 언로드될 때까지 유지
String a = "hello"; // Pool 참조
String b = "hello"; // 같은 Pool 참조
System.out.println(a == b); // true

// new — 항상 Heap에 새 객체 생성, Pool 사용 안 함
String c = new String("hello"); // Heap에 별도 객체
System.out.println(a == c); // false

// intern() — c의 내용으로 Pool 탐색, 있으면 Pool 참조 반환
String d = c.intern();
System.out.println(a == d); // true
```

`intern()`의 비용은 두 가지다. 첫째, Pool은 내부적으로 해시 테이블로 구현되므로 조회 비용이 있다. 대규모 문자열을 반복해서 `intern()`하면 해시 충돌과 조회 비용이 누적된다. 둘째, Pool에 추가된 String은 강한 참조가 하나도 없을 때만 GC된다. 의도치 않게 많은 String을 Pool에 넣으면 메모리 압박이 생긴다.

실무에서 `intern()` 명시적 호출은 거의 필요하지 않다. 리터럴이나 상수 표현식은 컴파일러가 자동으로 Pool을 활용하고, 동등성 비교는 `equals()`를 쓰는 것이 원칙이다. `intern()`이 유용한 경우는 대량의 중복 문자열(예: CSV 파싱 시 반복되는 컬럼값)을 메모리 효율적으로 처리해야 할 때 정도다.

---

## Q2. String 연결 연산자의 컴파일러 최적화 한계

### 왜 이 질문이 중요한가
"루프 안에서 `+` 연산자로 String을 연결하지 말라"는 조언은 많이 들었지만 왜 그런지, Java 버전마다 다른지, 실제로 얼마나 느린지 설명하지 못하는 경우가 많다. 또한 Java 9+에서 최적화가 바뀌었는데 이를 모르면 불필요한 최적화를 직접 하게 된다.

### 답변

Java 8까지 `+` 연산자는 컴파일 타임에 `StringBuilder`로 변환됐다. 단순한 `"Hello" + name + "!"` 같은 단일 표현식은 컴파일러가 하나의 `StringBuilder`로 처리해서 효율적이다.

문제는 루프 안에서의 연결이다. 컴파일러는 루프 경계를 넘어서까지 최적화하지 않아 매 반복마다 새 `StringBuilder`가 생성된다.

```java
// Java 8에서 이 코드는
String result = "";
for (String s : list) {
    result += s; // 매번 새 StringBuilder 생성
}

// 대략 이렇게 변환됨 — 각 반복마다 StringBuilder 객체 생성
for (String s : list) {
    result = new StringBuilder(result).append(s).toString();
}

// 올바른 방법
StringBuilder sb = new StringBuilder();
for (String s : list) {
    sb.append(s);
}
String result = sb.toString();

// 또는 Stream API
String result = String.join("", list);
// list.stream().collect(Collectors.joining());
```

Java 9+에서는 `invokedynamic`과 `StringConcatFactory`를 활용한 새로운 최적화가 도입됐다. 컴파일러가 `+` 연산을 `invokedynamic` 명령어로 컴파일하고, JVM이 런타임에 최적의 연결 전략을 선택한다. 이는 JIT 최적화와 결합되어 단순 연결에서는 `StringBuilder`보다 빠를 수도 있다.

그러나 이 최적화도 루프에는 여전히 적용되지 않는다. 루프 안의 `+`는 여전히 매 반복마다 새 연결 작업이 발생한다. 따라서 실무 기준은 명확하다. 단일 표현식 연결은 `+` 사용해도 무방하고, 루프나 조건부 연결이 많은 경우에는 `StringBuilder`나 `String.join()`, `Collectors.joining()`을 사용한다.
