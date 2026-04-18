# 문자 인코딩: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. UTF-8과 UTF-16의 메모리 효율 차이가 실무에 미치는 영향은 무엇인가?

### 왜 이 질문이 중요한가
Java의 `String`은 내부적으로 UTF-16을 사용했기 때문에 ASCII 문자 하나에도 2바이트를 썼다. 대용량 텍스트를 다루는 서비스(검색 엔진, 로그 처리, 자연어 처리)에서 이 차이는 힙 사용량과 GC 빈도에 직접 영향을 준다. 2026년 현재 Java 9+ Compact Strings가 기본 활성화되어 있으므로, 이 최적화의 조건과 한계를 아는 것이 실무에서 중요하다.

### 답변

UTF-8과 UTF-16의 인코딩 방식 차이는 다음과 같다.

| 문자 범위 | UTF-8 바이트 수 | UTF-16 바이트 수 |
|----------|---------------|----------------|
| ASCII (U+0000~U+007F) | 1 | 2 |
| 라틴 확장, 키릴 등 (U+0080~U+07FF) | 2 | 2 |
| BMP (U+0800~U+FFFF, 한중일 포함) | 3 | 2 |
| 보충 다국어 평면 (U+10000~) | 4 | 4 (서로게이트 쌍) |

**실무 영향 1: 영어 중심 텍스트 처리.** REST API 응답, 로그 메시지, SQL 쿼리처럼 ASCII가 대부분인 경우 UTF-16 저장은 메모리를 2배 낭비한다. 100만 건의 평균 100자 문자열이라면 UTF-8로 100MB, UTF-16으로 200MB다.

**실무 영향 2: 한국어/한자 텍스트.** BMP 범위의 한글(U+AC00~U+D7A3)은 UTF-8에서 3바이트, UTF-16에서 2바이트다. 한국어 전용 서비스에서는 오히려 UTF-16(= Java의 내부 표현)이 더 효율적이다.

**실무 영향 3: 파일/네트워크 I/O.** 디스크와 네트워크는 바이트 단위이므로 Java 내부 표현과 무관하게 인코딩 변환이 발생한다. `Files.readString(path, StandardCharsets.UTF_8)`처럼 명시적으로 인코딩을 지정하지 않으면 플랫폼 기본 인코딩이 사용되어 이식성 문제가 생긴다.

```java
// 인코딩 명시 필수 패턴
String content = Files.readString(Path.of("data.txt"), StandardCharsets.UTF_8);

// 시스템 기본 인코딩 확인
System.out.println(Charset.defaultCharset());  // Java 17+에서는 UTF-8이 기본
// Java 17 이전에는 OS 종속 → Windows에서 EUC-KR이 기본일 수 있음
```

---

## Q2. Java String 내부의 Compact Strings 최적화는 어떻게 동작하는가?

### 왜 이 질문이 중요한가
Java 9에서 도입된 Compact Strings는 대부분의 Java 애플리케이션에서 힙 사용량을 10~15% 줄이는 효과가 있다고 OpenJDK 팀이 보고했다. 이 최적화의 조건과 한계를 알면 String 관련 메모리 최적화를 제대로 분석할 수 있고, 인터뷰에서 "Java String의 내부 구조" 질문에 깊이 있는 답을 줄 수 있다.

### 답변

Java 8까지 `String`은 항상 `char[]`(UTF-16, 문자당 2바이트)를 내부 저장소로 사용했다. Java 9부터 Compact Strings는 `byte[]`와 `coder` 필드로 대체했다.

```java
// Java 9+ String 내부 구조 (OpenJDK 소스 기반)
public final class String {
    private final byte[] value;   // 실제 데이터
    private final byte coder;     // LATIN1 = 0, UTF16 = 1
    // ...
}
```

**동작 원리**: 모든 문자가 Latin-1 범위(U+0000~U+00FF)에 속하면 `coder = LATIN1`으로 1바이트/문자로 저장한다. 하나라도 U+0100 이상이면 `coder = UTF16`으로 2바이트/문자를 사용한다. 한글이 하나라도 포함되면 전체 문자열이 UTF-16으로 저장된다.

```java
// 확인 방법: JOL(Java Object Layout) 라이브러리
String ascii = "Hello";   // 5 bytes (LATIN1)
String korean = "안녕";   // 4 bytes (UTF16)
String mixed = "Hello안녕"; // 전체 UTF16 → 14 bytes

// Java 8 동등 코드: 항상 UTF16
// "Hello" → char[5] = 10 bytes
```

**실무 함의**: 영어, 숫자, 기호로만 구성된 문자열(URL, JSON 키, 변수명, 로그 메시지 대부분)은 메모리가 절반으로 줄어든다. 반면 다국어 혼합 문자열은 효과가 없다.

**한계와 주의점**: Compact Strings는 `String.charAt()` 등의 메서드에서 coder를 검사하는 분기가 추가되므로 이론상 CPU 오버헤드가 생긴다. 그러나 실제 벤치마크에서는 캐시 효율 향상으로 인해 오히려 성능이 좋아지거나 중립적이다. `-XX:-CompactStrings`로 비활성화할 수 있지만 실무에서 비활성화할 이유는 거의 없다.

```bash
# Compact Strings 활성화 상태 확인
java -XX:+PrintFlagsFinal -version | grep CompactStrings
# bool CompactStrings = true {product} {default}
```
