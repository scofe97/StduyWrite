# 문자 인코딩

---

> 문자 인코딩은 문자를 컴퓨터가 처리할 수 있는 숫자(바이트)로 변환하는 규칙이다. 인코딩과 디코딩에 서로 다른 방식을 사용하면 한글이 깨지는 현상이 발생하므로, 시스템 경계마다 인코딩을 명시해야 한다.

## 1. 문자 집합의 발전: ASCII에서 Unicode까지

컴퓨터가 처음 등장했을 때 각 제조사가 독자적인 문자 집합을 사용해 시스템 간 호환성이 없었다. 1960년대에 미국 표준화 기관이 **ASCII**를 제정해 이 문제를 해결했다. ASCII는 7비트로 128가지 문자(영문자, 숫자, 특수문자)를 표현한다.

한국에서 컴퓨터 사용이 늘어나며 한글 표현 필요성이 생겼고, 2바이트(16비트)를 사용하는 **EUC-KR**이 등장했다. EUC-KR은 자주 사용하는 한글 2,350자만 포함해 '뷁' 같은 일부 글자를 표현하지 못했고, 마이크로소프트가 이를 확장한 **MS949**를 만들었다.

하나의 문서에서 한국어, 중국어, 일본어를 동시에 표현하려면 단일 문자 집합으로는 불가능하다. 이 문제를 해결하기 위해 전 세계 모든 문자를 하나의 집합으로 표현하는 **Unicode**가 도입됐다.

## 2. UTF-8 vs UTF-16

Unicode를 실제 바이트로 인코딩하는 방식이 UTF-8과 UTF-16이다. 두 방식은 사용 바이트 수와 ASCII 호환성에서 차이가 있다.

| 항목 | UTF-8 | UTF-16 |
|------|-------|--------|
| 인코딩 단위 | 가변 1~4바이트 | 가변 2~4바이트 |
| 영문(ASCII) | 1바이트 | 2바이트 |
| 한글 | 3바이트 | 2바이트 |
| ASCII 호환 | 완전 호환 | 비호환 |
| 웹 표준 | 사실상 표준 (W3C 2008) | Java 내부 표현 |

**UTF-8**은 ASCII와 완전히 호환되고 영문에서 메모리를 1바이트만 사용하므로, 웹 문서의 80%가 영어인 환경에서 절대적으로 유리하다. 현대 웹 개발에서 UTF-8이 사실상 표준인 이유다.

**UTF-16**은 한글, 한자, 일본어를 2바이트로 처리하므로 이 언어가 주를 이루는 환경에서 UTF-8보다 효율적이다. Java가 내부적으로 UTF-16을 사용하는 것은 이 때문이다.

## 3. Java의 내부 문자 표현

Java는 `char`와 `String`을 내부적으로 UTF-16으로 표현한다. `char` 타입이 2바이트인 것도 이 때문이다. 하지만 이 방식은 영문만 있는 문자열에서 메모리를 낭비한다는 단점이 있었다.

Java 9에서 **Compact Strings** 최적화가 도입됐다. `String` 내부에 `byte[]`와 `coder` 필드를 두고, 모든 문자가 Latin-1(1바이트)으로 표현 가능하면 `LATIN1` 인코딩을, 그렇지 않으면 `UTF-16` 인코딩을 선택한다. 영문과 숫자만 있는 문자열에서 메모리 사용이 절반으로 줄어드는 효과가 있다.

```java
// Java 내부에서 char는 UTF-16 코드 유닛
char c = '가'; // 0xAC00 (2바이트)
System.out.println((int) c); // 44032

// String.length()는 char(UTF-16 코드 유닛) 수를 반환
String emoji = "😀"; // U+1F600 (보조 평면, 4바이트 UTF-16)
System.out.println(emoji.length());      // 2 (surrogate pair)
System.out.println(emoji.codePointCount(0, emoji.length())); // 1 (실제 문자 수)
```

## 4. Charset 클래스

Java에서 인코딩 방식은 `java.nio.charset.Charset` 클래스로 표현한다. 자주 사용하는 Charset은 `StandardCharsets` 상수로 제공한다.

```java
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

// 표준 상수 사용 (권장)
Charset utf8 = StandardCharsets.UTF_8;
Charset utf16 = StandardCharsets.UTF_16;

// 이름으로 조회 (대소문자 무관)
Charset ms949 = Charset.forName("MS949");
Charset euckr = Charset.forName("EUC-KR");

// 시스템 기본 인코딩 조회 (환경마다 다를 수 있어 주의)
Charset defaultCharset = Charset.defaultCharset();
System.out.println(defaultCharset); // 보통 UTF-8

// 문자열 → 바이트 변환
byte[] bytes = "안녕".getBytes(StandardCharsets.UTF_8); // 6바이트 (한글 1자 = 3바이트)
String str = new String(bytes, StandardCharsets.UTF_8);
```

## 5. InputStreamReader / OutputStreamWriter 인코딩 지정

파일이나 네트워크 스트림에서 텍스트를 읽고 쓸 때 **반드시 인코딩을 명시**해야 한다. 명시하지 않으면 JVM의 기본 인코딩을 사용하는데, 이 값은 실행 환경(OS, JVM 옵션)에 따라 달라져 예측할 수 없는 버그의 원인이 된다.

```java
// 인코딩 명시 (권장)
try (BufferedReader reader = new BufferedReader(
        new InputStreamReader(
            new FileInputStream("data.txt")
            , StandardCharsets.UTF_8))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
}

// 인코딩 명시 (쓰기)
try (BufferedWriter writer = new BufferedWriter(
        new OutputStreamWriter(
            new FileOutputStream("output.txt")
            , StandardCharsets.UTF_8))) {
    writer.write("안녕하세요");
}
```

Java 11부터는 `Files` API에서 인코딩을 직접 지정할 수 있어 더 간결하다:

```java
// Java 11+
Path path = Path.of("data.txt");
String content = Files.readString(path, StandardCharsets.UTF_8);
Files.writeString(path, "안녕", StandardCharsets.UTF_8);
```

## 6. 한글 깨짐의 원인과 해결

한글 깨짐 문제는 대부분 인코딩과 디코딩에 다른 방식을 사용할 때 발생한다. 원인을 파악하면 해결책이 명확하다.

가장 흔한 시나리오는 다음 세 가지다:

- UTF-8로 저장한 파일을 EUC-KR로 읽을 때: UTF-8의 3바이트 한글 코드가 EUC-KR 해석 테이블과 맞지 않아 물음표나 이상한 문자가 출력된다
- MS949로 저장한 파일을 UTF-8로 읽을 때: 동일한 이유로 깨진다
- URL에서 한글을 퍼센트 인코딩 없이 전달할 때: URL은 ASCII만 지원하므로 한글을 UTF-8 바이트로 변환 후 각 바이트 앞에 `%`를 붙이는 **퍼센트 인코딩**이 필요하다

```java
import java.net.URLEncoder;
import java.net.URLDecoder;

// '안녕' → UTF-8 3바이트 × 2자 = %EC%95%88%EB%85%95
String encoded = URLEncoder.encode("안녕", StandardCharsets.UTF_8);
System.out.println(encoded); // %EC%95%88%EB%85%95

String decoded = URLDecoder.decode(encoded, StandardCharsets.UTF_8);
System.out.println(decoded); // 안녕
```

인코딩 문제를 예방하는 가장 확실한 방법은 **시스템 전체에서 UTF-8을 일관되게 사용**하는 것이다. 데이터베이스 커넥션, HTTP 헤더, 파일 입출력 모두 명시적으로 UTF-8을 지정하면 인코딩 관련 버그의 대부분을 사전에 차단할 수 있다.
