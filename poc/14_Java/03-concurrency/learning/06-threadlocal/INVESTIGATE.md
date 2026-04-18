# ThreadLocal: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 스레드 풀 환경에서 ThreadLocal 메모리 누수 원인과 방지는 무엇인가

### 왜 이 질문이 중요한가
ThreadLocal은 Spring의 트랜잭션 컨텍스트, 보안 컨텍스트, MDC 로깅 등 광범위하게 사용된다. 스레드 풀과 함께 사용할 때의 메모리 누수 메커니즘을 모르면 장기 운영 시 OOM이나 데이터 오염이 발생한다.

### 답변
`ThreadLocal`의 값은 `Thread` 객체 내부의 `ThreadLocalMap`에 저장된다. 일반 스레드(`new Thread(...)`)는 작업 완료 후 GC되면서 `ThreadLocalMap`도 함께 회수된다. 문제는 스레드 풀이다.

스레드 풀의 스레드는 작업이 끝나도 종료되지 않고 재사용된다. 작업 완료 후 `ThreadLocal.remove()`를 호출하지 않으면 이전 작업의 값이 다음 작업에서도 남아 있다. 이는 두 가지 문제를 만든다.

첫째는 데이터 오염이다. 다음 요청을 처리하는 스레드가 이전 요청의 사용자 ID나 트랜잭션 컨텍스트를 가져와 잘못된 동작을 할 수 있다.

둘째는 메모리 누수다. `ThreadLocalMap`의 키는 `ThreadLocal` 인스턴스에 대한 `WeakReference`다. `ThreadLocal` 변수가 GC되어 키가 null이 되어도 값(value)은 강한 참조로 남아 있다. 이 "stale entry"들이 스레드가 살아 있는 한 계속 메모리를 차지한다. 큰 객체(Connection, Session, 대용량 Map)가 값으로 저장되어 있으면 심각한 메모리 누수가 된다.

```java
// 잘못된 패턴 — remove() 없음
public class UserContextHolder {
    private static final ThreadLocal<UserContext> context = new ThreadLocal<>();

    public static void set(UserContext ctx) { context.set(ctx); }
    public static UserContext get() { return context.get(); }
    // remove() 없음 — 스레드 풀에서 누수!
}

// 올바른 패턴 — try-finally로 반드시 제거
public void handleRequest(HttpServletRequest request) {
    UserContext ctx = extractContext(request);
    UserContextHolder.set(ctx);
    try {
        processRequest(request);
    } finally {
        UserContextHolder.remove(); // 반드시 제거
    }
}
```

Spring의 `RequestContextHolder`, `SecurityContextHolder`는 `OncePerRequestFilter`나 인터셉터에서 요청 후 자동으로 `remove()`를 호출하도록 설계되어 있다. 커스텀 ThreadLocal을 만들 때도 이 패턴을 따라야 한다.

---

## Q2. ScopedValue가 ThreadLocal을 대체하는 이유는 무엇인가

### 왜 이 질문이 중요한가
Java 21에서 Preview로 도입되고 Java 23에서 두 번째 Preview 중인 `ScopedValue`는 Virtual Thread 시대의 ThreadLocal 대안으로 설계되었다. 차이를 이해해야 Virtual Thread 기반 애플리케이션에서 올바른 컨텍스트 전파 방법을 선택할 수 있다.

### 답변
`ScopedValue`는 `ThreadLocal`의 세 가지 근본 문제를 해결하기 위해 설계되었다.

첫째, 불변성이다. `ThreadLocal`은 언제든지 `set()`으로 값을 변경할 수 있어 코드 어디서든 컨텍스트가 변경될 수 있다. `ScopedValue`는 바인딩된 스코프 내에서 불변이다. `ScopedValue.where(sv, value).run(() -> { ... })` 블록 안에서 값은 변경되지 않는다.

```java
// ScopedValue 사용 패턴 (Java 21+ Preview)
static final ScopedValue<UserContext> USER = ScopedValue.newInstance();

// 스코프 내에서만 값 접근 가능
ScopedValue.where(USER, new UserContext("alice"))
    .run(() -> {
        process(); // USER.get() 가능
    });
// 스코프 밖에서는 USER.get() → NoSuchElementException

void process() {
    UserContext ctx = USER.get(); // 불변값 읽기
}
```

둘째, 자동 범위 관리다. `ThreadLocal`은 `remove()`를 명시적으로 호출해야 하지만, `ScopedValue`는 스코프(`run()` 또는 `call()` 블록)가 끝나면 자동으로 이전 값(또는 없음 상태)으로 복원된다. 메모리 누수가 구조적으로 불가능하다.

셋째, Virtual Thread와의 호환성이다. Virtual Thread는 수백만 개가 동시에 존재할 수 있다. `ThreadLocal`은 각 Virtual Thread마다 독립적인 `ThreadLocalMap`을 생성하므로 메모리 비용이 크다. `ScopedValue`는 상속(inheritance) 시에도 값을 복사하지 않고 공유 읽기를 허용해 메모리 효율이 높다.

`StructuredTaskScope`와 조합하면 부모 스코프의 값이 자식 태스크로 자동 전파된다.

```java
ScopedValue.where(USER, userContext).run(() -> {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        Future<Result> f1 = scope.fork(() -> taskA()); // USER.get() 접근 가능
        Future<Result> f2 = scope.fork(() -> taskB()); // USER.get() 접근 가능
        scope.join().throwIfFailed();
    }
});
```

`ScopedValue`는 아직 Preview 상태(Java 23 기준)이므로 프로덕션 사용에 주의가 필요하다. 하지만 Virtual Thread를 본격적으로 사용하는 Java 21+ 환경에서는 ThreadLocal의 명확한 후계자로 설계되었다.
