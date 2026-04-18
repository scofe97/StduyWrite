# 실행자 프레임워크: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 스레드 풀 크기 결정 공식: CPU-bound vs IO-bound 작업

### 왜 이 질문이 중요한가
스레드 풀 크기를 잘못 설정하면 CPU 코어가 놀거나(under-utilization) 컨텍스트 스위칭 비용이 폭발한다(over-subscription). 인터뷰에서 단골 질문이고 실무에서 성능 튜닝의 첫 번째 체크포인트다.

### 답변
Brian Goetz의 공식이 출발점이다: `스레드 수 = CPU 코어 수 × (1 + 대기 시간 / 서비스 시간)`. 여기서 대기 시간은 IO 대기, 락 대기 등 스레드가 블록되는 시간이고 서비스 시간은 실제 CPU를 사용하는 시간이다.

CPU-bound 작업(암호화, 이미지 처리, 수학 연산)은 대기 시간이 거의 0이므로 공식이 `코어 수 × 1 = 코어 수`로 수렴한다. 코어 수보다 스레드를 더 만들면 컨텍스트 스위칭 비용만 추가된다. 실무에서는 `코어 수` 또는 `코어 수 + 1`을 사용한다. +1은 GC나 OS 인터럽트로 한 스레드가 잠깐 대기할 때 다른 스레드가 CPU를 채우기 위함이다.

```java
int cores = Runtime.getRuntime().availableProcessors();
// CPU-bound
ExecutorService cpuPool = Executors.newFixedThreadPool(cores);
// IO-bound (대기 시간이 서비스 시간의 9배인 경우)
ExecutorService ioPool = Executors.newFixedThreadPool(cores * 10);
```

IO-bound 작업(DB 쿼리, HTTP 호출, 파일 읽기)은 대기 시간이 서비스 시간보다 수십~수백 배 길다. DB 응답 10ms, CPU 처리 1ms라면 `코어 수 × (1 + 10/1) = 코어 수 × 11`이 된다. 다만 이 공식은 이론값이고 실제 최적값은 부하 테스트로 결정해야 한다.

`Executors.newCachedThreadPool()`은 IO-bound 작업에 자주 쓰이지만 위험하다. 스레드 수 상한이 없어 요청 급증 시 수천 개의 스레드가 생성되어 OOM이나 컨텍스트 스위칭 폭발이 발생한다. 운영 환경에서는 반드시 상한을 설정한 `ThreadPoolExecutor`를 직접 생성해야 한다.

```java
// 운영 환경 권장 패턴
ExecutorService executor = new ThreadPoolExecutor(
    corePoolSize,    // 최소 유지 스레드
    maxPoolSize,     // 최대 스레드
    60L, TimeUnit.SECONDS,  // 유휴 스레드 종료 시간
    new LinkedBlockingQueue<>(queueCapacity),  // 큐 크기 제한 필수
    new ThreadPoolExecutor.CallerRunsPolicy()  // 거부 정책: 호출 스레드가 직접 실행
);
```

---

## Q2. CompletableFuture 에러 처리 전략은 어떻게 설계하는가

### 왜 이 질문이 중요한가
`CompletableFuture`의 에러 처리는 동기 코드의 try-catch와 다른 패턴을 사용한다. 에러 처리를 잘못하면 예외가 조용히 삼켜지거나 전체 파이프라인이 복구 불가능한 상태가 된다.

### 답변
`CompletableFuture`의 에러 처리는 세 가지 주요 메서드로 구성된다.

`exceptionally(fn)`은 예외가 발생했을 때 기본값이나 대체 결과를 반환한다. 예외를 복구하는 용도다.

```java
CompletableFuture<String> result = fetchData(id)
    .exceptionally(ex -> {
        log.warn("Fetch failed for {}: {}", id, ex.getMessage());
        return "DEFAULT_VALUE"; // 폴백 값
    });
```

`handle(fn)`은 성공과 실패 모두를 처리한다. `(result, exception)` 두 인수를 받아 항상 실행된다. 성공 시 exception은 null, 실패 시 result는 null이다.

```java
CompletableFuture<Response> result = callApi()
    .handle((data, ex) -> {
        if (ex != null) {
            return Response.error(ex.getMessage());
        }
        return Response.success(data);
    });
```

`whenComplete(action)`은 handle과 유사하지만 반환값을 변환하지 않고 부수 효과(로깅, 메트릭)만 수행한다.

파이프라인 에러 전파에서 주의할 점이 있다. `exceptionally`나 `handle`이 없는 중간 단계에서 예외가 발생하면, 이후 `thenApply`, `thenCompose` 등은 모두 건너뛰고 예외가 전파된다. 최종 `get()`에서 `ExecutionException`으로 감싸져 던져진다.

```java
// 예외가 발생하면 map과 filter는 실행되지 않음
CompletableFuture<Result> pipeline = step1()
    .thenApply(this::transform)    // step1 실패 시 건너뜀
    .thenCompose(this::step2)      // 건너뜀
    .exceptionally(ex -> fallback()); // 여기서 복구

// 여러 CompletableFuture 조합 시 에러 처리
CompletableFuture<Void> all = CompletableFuture.allOf(cf1, cf2, cf3)
    .whenComplete((v, ex) -> {
        if (ex != null) {
            // cf1, cf2, cf3 중 하나라도 실패하면 여기 도달
            // 어떤 것이 실패했는지는 각 future를 개별 확인
            Stream.of(cf1, cf2, cf3)
                .filter(CompletableFuture::isCompletedExceptionally)
                .forEach(cf -> cf.exceptionally(e -> { log.error(e); return null; }));
        }
    });
```

`CompletableFuture.get()`을 호출하지 않고 파이프라인을 구성만 하면 예외가 조용히 삼켜진다. 비동기 파이프라인의 끝에는 반드시 에러 핸들러를 붙이거나 `get()`을 통해 예외를 수면 위로 올려야 한다.
