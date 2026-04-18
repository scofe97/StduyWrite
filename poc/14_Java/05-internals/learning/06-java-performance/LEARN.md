# Java 성능
---
> 성능 문제를 과학적으로 측정하고 개선하는 방법론을 이해한다. 올바른 벤치마크 작성, 메모리/CPU/IO 최적화 기법, 프로파일링 도구 활용, 흔한 성능 안티패턴을 다룬다.

## 1. 성능 측정 방법론

성능 튜닝은 측정 없이 시작하면 안 된다. 직관에 의존한 최적화는 틀린 곳을 고치거나, 이미 JIT 컴파일러가 처리하는 부분에 시간을 낭비하게 만든다. 측정 가능한 목표를 먼저 정의해야 한다:

- warmup 이후 `handleRequest()` 메서드의 평균 실행 시간
- 동시 사용자 10명 기준 end-to-end 지연 시간
- 사용자 1~1000명 증가에 따른 응답 시간 저하 곡선

### 1-1. JMH 벤치마크

`System.currentTimeMillis()`로 직접 측정하면 콜드 스타트 문제가 발생한다. JIT 컴파일은 메서드의 후속 실행이 이전보다 빠르므로, 초기 측정값은 정상 상태를 반영하지 못한다. **JMH(Java Microbenchmark Harness)**는 이런 함정을 피하도록 설계된 공식 마이크로벤치마크 프레임워크다.

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Benchmark)
public class StringBenchmark {

    private String[] words;

    @Setup
    public void setup() {
        words = new String[]{"Hello", "World", "Java", "JVM"};
    }

    @Benchmark
    public String concatenation() {
        String result = "";
        for (String word : words) {
            result += word;
        }
        return result;
    }

    @Benchmark
    public String stringBuilder() {
        var sb = new StringBuilder();
        for (String word : words) {
            sb.append(word);
        }
        return sb.toString();
    }
}
```

JMH의 핵심 개념은 **워밍업(Warmup)**이다. `@Warmup(iterations = 5)` 설정으로 JIT 컴파일이 충분히 이루어진 후의 안정적인 성능을 측정한다. 워밍업 없는 측정은 인터프리터 실행 비용을 포함하여 실제 운영 성능과 크게 다를 수 있다.

### 1-2. 메모리 지연 계층 구조

성능 분석에서 메모리 계층 구조를 이해하는 것이 중요하다. CPU 연산 속도와 메모리 접근 속도의 격차가 성능 병목의 근본 원인인 경우가 많다:

- **레지스터**: 직접 연산, 1 사이클
- **L1 캐시**: ~4 사이클
- **L2 캐시**: ~12 사이클
- **L3 캐시**: ~40 사이클
- **메인 메모리**: ~200 사이클
- **SSD**: ~100,000 사이클

캐시 친화적인 코드는 처리량이 많은 코드에서 가장 큰 성능 차이를 만든다. 64바이트 캐시 라인보다 큰 보폭으로 배열을 순회하면 캐시 미스가 발생하더라도 실제 시간 차이는 16배에 달하지 않는다. 메모리 접근 패턴이 성능에 미치는 영향이 알고리즘 복잡도만큼 중요할 수 있다.

## 2. 메모리 최적화

### 2-1. 객체 생성 최소화

GC 압박을 줄이는 가장 직접적인 방법은 불필요한 객체 생성을 피하는 것이다. 특히 핫 경로(자주 실행되는 코드)에서 임시 객체를 대량 생성하면 Minor GC 빈도가 높아진다:

```java
// 나쁜 예: 루프마다 객체 생성
for (int i = 0; i < 1_000_000; i++) {
    String key = "prefix_" + i;    // StringBuilder + String 생성
    process(key);
}

// 좋은 예: StringBuilder 재사용
var sb = new StringBuilder("prefix_");
int prefixLen = sb.length();
for (int i = 0; i < 1_000_000; i++) {
    sb.setLength(prefixLen);
    sb.append(i);
    process(sb.toString());
}
```

### 2-2. 기본형 사용

`Integer`, `Long` 같은 래퍼 타입은 박싱 비용과 추가 객체 헤더(16바이트) 오버헤드가 있다. 숫자를 대량으로 처리하는 코드에서는 기본형 배열이 래퍼 타입 컬렉션보다 훨씬 메모리 효율적이다:

```java
// 오토박싱 함정
List<Integer> list = new ArrayList<>();
for (int i = 0; i < 100_000; i++) {
    list.add(i);          // int → Integer 박싱
    int val = list.get(i); // Integer → int 언박싱
}

// 기본형 배열 사용
int[] array = new int[100_000];
for (int i = 0; i < array.length; i++) {
    array[i] = i;
}
```

### 2-3. 문자열 최적화

문자열은 Java에서 가장 흔한 메모리 낭비 원인이다. 루프 내 `+` 연산은 컴파일러가 `StringBuilder`로 변환하지만, 루프 외부의 `StringBuilder` 재사용이 더 효율적이다. 같은 내용의 문자열이 반복 생성되면 `String.intern()`으로 상수 풀을 활용하거나, `Map<String, String>` 캐시를 사용한다.

## 3. CPU 최적화

### 3-1. 알고리즘과 자료구조 선택

대부분의 성능 문제는 잘못된 자료구조 선택에서 시작한다. `ArrayList`는 인덱스 접근이 O(1)이지만 중간 삽입/삭제가 O(n)이다. `HashMap`의 평균 접근은 O(1)이지만 해시 충돌이 많으면 O(n)으로 저하된다. 알고리즘 복잡도를 먼저 개선하고, 그 다음에 저수준 최적화를 검토하는 순서가 올바르다.

### 3-2. 캐시 친화적 설계

연속 메모리 접근은 캐시 라인을 효율적으로 사용한다. 2차원 배열을 행 우선(row-major)으로 순회하면 열 우선보다 캐시 히트율이 높다. 객체 배열(`Object[]`)보다 기본형 배열(`int[]`)이 메모리 지역성이 좋아 캐시 효율이 높다.

```java
// 캐시 친화적: 행 우선 순회
for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        matrix[i][j] += 1;   // 연속 메모리 접근
    }
}

// 캐시 비친화적: 열 우선 순회
for (int j = 0; j < cols; j++) {
    for (int i = 0; i < rows; i++) {
        matrix[i][j] += 1;   // 불연속 메모리 접근, 캐시 미스
    }
}
```

## 4. I/O 최적화

### 4-1. 버퍼링

비버퍼 I/O는 읽기/쓰기마다 시스템 콜을 발생시킨다. `BufferedReader`, `BufferedWriter`, `BufferedInputStream`으로 감싸면 내부 버퍼를 통해 시스템 콜 횟수를 대폭 줄인다:

```java
// 비버퍼: 1바이트마다 시스템 콜
try (var reader = new FileReader("large.txt")) { ... }

// 버퍼링: 8KB 단위로 읽어 시스템 콜 최소화
try (var reader = new BufferedReader(new FileReader("large.txt"), 65536)) { ... }
```

### 4-2. NIO와 비동기 I/O

Java NIO의 `FileChannel`과 `ByteBuffer`는 운영체제의 zero-copy 기능을 활용할 수 있다. `transferTo()`/`transferFrom()`은 커널 버퍼를 직접 사용하여 불필요한 사용자 공간 복사를 없앤다. 대량 파일 전송에서 기존 스트림 방식보다 수배 빠를 수 있다.

비동기 I/O(`AsynchronousFileChannel`, `CompletableFuture`)는 I/O 완료를 기다리는 동안 스레드를 차단하지 않아 스레드 풀을 효율적으로 사용한다.

## 5. 프로파일링 도구

프로파일러 없이 "느린 코드"를 찾으려 하면 경험과 추측에 의존하게 된다. 프로파일링으로 실제 핫스팟을 찾는 것이 최적화의 첫 단계다.

| 도구 | 특징 | 사용 시점 |
|---|---|---|
| **JFR(Java Flight Recorder)** | JVM 내장, 오버헤드 1% 미만, 프로덕션 사용 가능 | CPU, 메모리, GC, I/O 종합 분석 |
| **async-profiler** | 네이티브 메모리/CPU 샘플링, 낮은 오버헤드 | CPU 플레임 그래프, 네이티브 코드 분석 |
| **VisualVM** | GUI 기반, JMX 연결 | 개발 환경 힙 덤프, 스레드 분석 |
| **JProfiler** | 상용, 상세한 메모리/CPU 분석 | 깊은 메모리 누수 분석 |

JFR 사용 예시는 다음과 같다:

```bash
# 60초 동안 JFR 기록
java -XX:+FlightRecorder \
     -XX:StartFlightRecording=duration=60s,filename=app.jfr \
     -jar app.jar

# JDK Mission Control로 분석
jmc app.jfr
```

async-profiler는 CPU 사용 시간을 플레임 그래프로 시각화한다. 넓고 평평한 막대가 CPU 시간을 많이 소비하는 메서드를 나타낸다.

## 6. 성능 안티패턴

### 6-1. 이른 최적화(Premature Optimization)

가장 흔한 안티패턴이다. 프로파일링 없이 추측으로 최적화하면 코드만 복잡해지고 실제 병목은 그대로다. "측정 → 분석 → 최적화 → 재측정" 사이클을 반드시 따른다.

### 6-2. 불필요한 동기화

`synchronized`가 필요하지 않은 곳에 남용하면 경합이 발생하여 성능이 저하된다. 반대로, 동기화 비용이 두려워 락을 빼면 데이터 경쟁 버그가 생긴다. 이스케이프 분석으로 JIT 컴파일러가 불필요한 락을 자동 제거하므로, 올바른 동기화를 먼저 작성하고 프로파일링으로 실제 경합이 문제임을 확인한 후에 최적화를 검토한다.

### 6-3. 스트림 남용

람다와 스트림은 가독성이 좋지만, 소량 데이터를 처리하는 핫 경로에서 반복 적용하면 람다 객체 생성 오버헤드가 누적된다. 핫 경로에서 `IntStream.range()`보다 단순 `for` 루프가 더 나은 경우가 있다. 항상 측정으로 판단한다.

### 6-4. 잘못된 컬렉션 선택

읽기가 압도적으로 많은 경우 `CopyOnWriteArrayList`가 `Collections.synchronizedList()`보다 낫다. 순서가 중요없고 빠른 검색이 필요하면 `HashSet`이 `ArrayList`보다 낫다. 자료구조를 바꾸는 것이 알고리즘 수준의 개선이며, 저수준 최적화보다 효과가 크다.

### 6-5. 무분별한 로깅

DEBUG 로그가 프로덕션에서 활성화되거나, 가드 조건 없이 무거운 `toString()`이 항상 실행되면 성능에 큰 영향을 준다:

```java
// 나쁜 예: 로그 레벨과 무관하게 항상 toString() 실행
log.debug("State: " + heavyObject.toString());

// 좋은 예: 레벨 확인 후 실행, 또는 람다 지연 평가
log.debug("State: {}", heavyObject);           // SLF4J 지연 포맷팅
log.debug(() -> "State: " + heavyObject);      // 람다 지연 평가
```
