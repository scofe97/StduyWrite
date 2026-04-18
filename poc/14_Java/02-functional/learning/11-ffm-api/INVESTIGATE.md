# FFM API (Foreign Function & Memory): Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. JNI 대비 FFM API의 실질적 장점은 무엇인가

### 왜 이 질문이 중요한가
FFM API(Java 22 정식, JEP 454)는 JNI를 대체하는 새로운 네이티브 interop 메커니즘이다. JNI의 문제점을 알아야 FFM이 왜 설계되었는지 이해하고, 네이티브 라이브러리 통합이 필요한 프로젝트에서 올바른 도구를 선택할 수 있다.

### 답변
JNI(Java Native Interface)는 1997년부터 Java가 C/C++ 네이티브 코드를 호출하는 유일한 공식 수단이었다. 그러나 세 가지 근본적인 문제가 있다.

첫째, 개발 복잡성이다. JNI를 사용하려면 Java 코드, C 헤더 파일, C 구현 파일, 빌드 스크립트를 모두 작성해야 한다. 네이티브 메서드 이름 규칙(`Java_com_example_MyClass_myMethod`)이 엄격하고, JVM 타입과 C 타입 간 변환을 수동으로 처리해야 한다.

둘째, 안전성 문제다. JNI를 통해 전달된 잘못된 포인터나 배열 경계 초과는 JVM 크래시를 유발한다. JVM의 가비지 컬렉터가 관리하는 메모리와 네이티브 메모리 간 생명주기 관리가 수동이어서 메모리 누수나 double-free가 발생하기 쉽다.

셋째, 성능 오버헤드다. JNI 호출은 JIT 컴파일러의 인라인 최적화를 방해한다. 또한 Java 힙 객체를 네이티브 코드에 전달하려면 GC가 이동하지 못하도록 핀(pin)해야 하는데, 이는 GC 효율을 떨어뜨린다.

FFM API는 이 세 문제를 모두 해결한다.

```java
// JNI — 복잡한 설정 필요
// 1. Java: native 메서드 선언
// 2. javah로 헤더 생성
// 3. C 구현 작성
// 4. .so/.dll 빌드
// 5. System.loadLibrary()

// FFM API — 순수 Java로 네이티브 함수 직접 호출
import java.lang.foreign.*;
import java.lang.invoke.*;

// C 표준 라이브러리의 strlen 직접 호출
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();

MethodHandle strlen = linker.downcallHandle(
    stdlib.find("strlen").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment str = arena.allocateUtf8String("Hello");
    long len = (long) strlen.invoke(str); // 5
}
```

FFM의 핵심 장점은 순수 Java 코드로 네이티브 함수를 호출할 수 있고, `Arena`를 통한 명시적 메모리 생명주기 관리가 안전하며(`try-with-resources`로 자동 해제), JExtract 도구로 C 헤더에서 Java 바인딩을 자동 생성할 수 있다는 것이다.

---

## Q2. FFM API가 Java 생태계에 미칠 영향은 무엇인가

### 왜 이 질문이 중요한가
FFM API는 단순한 JNI 대체를 넘어 Java 생태계의 네이티브 라이브러리 통합 방식을 근본적으로 바꿀 수 있다. 이 영향을 이해해야 AI/ML, 데이터베이스 드라이버, OS API 통합 분야에서 Java의 역할 변화를 예측할 수 있다.

### 답변
FFM API가 Java 생태계에 미칠 영향은 세 영역에서 크게 나타날 것이다.

첫째, AI/ML 네이티브 라이브러리 통합이다. TensorFlow, PyTorch, ONNX Runtime 같은 ML 프레임워크는 C/C++로 작성된 고성능 코어를 가진다. 현재 Java 바인딩은 대부분 JNI 기반이거나 gRPC/HTTP를 통한 외부 프로세스 호출에 의존한다. FFM API로 순수 Java에서 이 라이브러리들을 직접 호출하면 오버헤드가 크게 줄어든다. Project Panama 팀은 이미 BLAS(선형 대수 라이브러리) 바인딩을 FFM으로 시연했다.

둘째, OS 수준 API 접근이다. 현재 Linux `io_uring`, Windows IOCP 같은 고성능 비동기 IO API는 JVM 내부에서만 사용 가능하고 Java 코드에서 직접 접근할 수 없다. FFM으로 이런 API를 직접 호출하면 JVM이 추상화한 것 이상의 성능을 끌어낼 수 있다. Netty와 같은 고성능 네트워킹 라이브러리가 큰 수혜를 받을 것이다.

셋째, JNI 기반 라이브러리의 점진적 대체다. SQLite JDBC 드라이버, 암호화 라이브러리(OpenSSL 바인딩), 그래픽 라이브러리(LWJGL) 같이 JNI를 사용하는 수많은 라이브러리가 FFM으로 재작성될 것이다. `jextract` 도구가 C 헤더에서 바인딩을 자동 생성하므로 유지보수 비용도 크게 줄어든다.

```java
// jextract로 자동 생성된 바인딩 사용 예시 (개념)
// jextract --target-package org.sqlite sqlite3.h
import org.sqlite.sqlite3_h.*;

try (Arena arena = Arena.ofConfined()) {
    MemorySegment db = arena.allocate(ValueLayout.ADDRESS);
    sqlite3_open(arena.allocateUtf8String("test.db"), db);
    // ...
    sqlite3_close(db.get(ValueLayout.ADDRESS, 0));
}
```

주의할 점은 FFM API가 `--enable-native-access` 모듈 플래그 없이는 경고를 출력한다는 것이다. 이는 의도적인 설계로, 네이티브 메모리 접근이 명시적으로 허용된 코드에서만 사용되도록 강제한다. 이 안전 장치가 JNI에는 없었던 FFM의 차별점이다.
