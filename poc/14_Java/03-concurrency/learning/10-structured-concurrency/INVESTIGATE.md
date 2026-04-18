# 구조적 동시성: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 비구조적 CompletableFuture 조합의 문제점은 무엇인가

### 왜 이 질문이 중요한가
`CompletableFuture` 체이닝은 강력하지만 여러 태스크를 조합할 때 생명주기 관리, 에러 전파, 취소 전파가 암묵적이어서 버그가 숨어든다. 이 문제를 구체적으로 설명할 수 있어야 Structured Concurrency의 필요성을 납득할 수 있다.

### 답변
비구조적 동시성의 핵심 문제는 태스크의 생명주기가 코드 구조와 일치하지 않는다는 것이다. 세 가지 구체적 문제가 있다.

첫째, 에러 전파의 불투명함이다. 여러 `CompletableFuture`를 조합할 때 한 태스크가 실패해도 다른 태스크가 계속 실행된다. `allOf`로 모두 기다리면 한 실패가 다른 성공한 결과를 가릴 수 있고, 어떤 태스크가 실패했는지 파악하는 코드가 복잡해진다.

```java
// 어떤 태스크가 실패했는지 파악하기 어려움
CompletableFuture<User> userFuture = fetchUser(userId);
CompletableFuture<Order> orderFuture = fetchOrders(userId);
CompletableFuture<Address> addrFuture = fetchAddress(userId);

CompletableFuture<Void> all = CompletableFuture.allOf(userFuture, orderFuture, addrFuture);
all.get(); // 예외 발생 시 어느 future가 실패했는지 all.get()만으로는 모름

// 개별 확인 코드 필요
if (userFuture.isCompletedExceptionally()) { ... }
if (orderFuture.isCompletedExceptionally()) { ... }
```

둘째, 취소 전파의 누락이다. 호출자가 결과를 더 이상 필요 없어져 취소를 요청해도, 이미 실행 중인 서브태스크들은 계속 실행된다. `CompletableFuture.cancel(true)`는 dependent future들에 취소를 전파하지 않는다.

```java
CompletableFuture<Result> result = fetchA()
    .thenCombine(fetchB(), this::merge);

result.cancel(true); // fetchA()와 fetchB()는 취소되지 않고 계속 실행됨
```

셋째, 태스크 누수다. 메서드가 반환되어도 백그라운드 태스크가 계속 실행될 수 있다. 예외가 발생해 메서드가 일찍 종료되면 시작된 태스크들의 정리가 보장되지 않는다. 이는 리소스 누수(DB 연결, 네트워크 소켓)로 이어질 수 있다.

---

## Q2. StructuredTaskScope가 프로덕션에서 사용 가능한가 (Preview 상태)

### 왜 이 질문이 중요한가
`StructuredTaskScope`는 Java 21에서 첫 Preview로 등장해 Java 23까지 Preview 상태가 지속되고 있다. Preview API를 언제 프로덕션에 채택할지 판단하는 기준을 갖는 것은 실무 의사결정 능력이다.

### 답변
`StructuredTaskScope`는 Java 21(JEP 428), 22(JEP 462), 23(JEP 480)을 거쳐 현재도 Preview 상태다. API 자체는 상당히 안정되었지만 "Preview"라는 표시는 공식 호환성 보장이 없다는 의미다. 다음 버전에서 API가 변경될 수 있다.

기본 사용 패턴은 다음과 같다.

```java
// ShutdownOnFailure: 하나라도 실패하면 나머지 취소
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<User>    userTask  = scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> ordersTask = scope.fork(() -> fetchOrders(id));

    scope.join()           // 모든 태스크 완료 또는 하나 실패까지 대기
         .throwIfFailed(); // 실패한 태스크의 예외를 여기서 던짐

    // 여기 도달하면 모두 성공
    return new Dashboard(userTask.get(), ordersTask.get());
}
// 스코프 닫힐 때 아직 실행 중인 태스크 자동 취소 — 태스크 누수 없음

// ShutdownOnSuccess: 하나라도 성공하면 나머지 취소 (첫 번째 성공 결과 반환)
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> callServiceA());
    scope.fork(() -> callServiceB()); // A보다 빠르면 이 결과 사용
    scope.join();
    return scope.result(); // 첫 성공 결과
}
```

프로덕션 채택 판단 기준을 세 가지로 정리한다.

첫째, 팀의 Java 버전 업그레이드 주기다. 매 LTS(21, 25)에서만 업그레이드한다면 Preview API 변경을 맞추기 어렵다. Java 25 LTS(2025년 9월 예정)에서 정식 API로 확정될 가능성이 높으므로 그때까지 대기하는 전략도 합리적이다.

둘째, Preview 컴파일 플래그 수용 여부다. `--enable-preview` 컴파일 옵션이 필요하고 런타임에도 `--enable-preview`를 JVM에 전달해야 한다. CI/CD 파이프라인과 컨테이너 이미지에 이 설정을 추가하는 운영 비용을 감수할 수 있는지 판단해야 한다.

셋째, 대안의 비교다. 현재 `CompletableFuture`로 구현된 코드가 충분히 작동하고 유지보수 가능하다면 마이그레이션 비용이 이득보다 클 수 있다. 신규 서비스이거나 비구조적 동시성의 버그가 실제로 발생하고 있다면 Preview 채택을 고려할 가치가 있다.
