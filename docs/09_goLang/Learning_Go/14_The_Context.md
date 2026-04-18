# Chapter 14: The Context - 면접정리

## 핵심 개념 상세 설명

### 1. Context의 목적과 Go만의 접근 방식

Go의 context 패키지는 요청 범위의 메타데이터와 취소 신호를 전달하는 표준 메커니즘입니다. 다른 언어에서는 ThreadLocal이나 암묵적 컨텍스트를 사용하지만, Go는 명시적으로 context를 함수의 첫 번째 매개변수로 전달합니다. 이 명시성은 Go의 철학인 "명확함이 암묵적인 것보다 낫다"를 반영합니다.

Context는 두 가지 핵심 역할을 수행합니다. 첫째, 요청 전체 수명 동안 필요한 메타데이터(추적 ID, 인증 토큰 등)를 전달합니다. 둘째, 취소 신호를 전파하여 불필요해진 작업을 빠르게 중단합니다. 클라이언트가 연결을 끊거나 타임아웃이 발생하면 모든 하위 goroutine에 취소가 전파됩니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Context's Two Roles                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     context.Context                             │
│                           │                                     │
│           ┌───────────────┴───────────────┐                     │
│           │                               │                     │
│           ▼                               ▼                     │
│   ┌───────────────────┐         ┌───────────────────┐           │
│   │   Value Passing   │         │   Cancellation    │           │
│   │                   │         │                   │           │
│   │ • Request ID      │         │ • Manual cancel   │           │
│   │ • Auth token      │         │ • Timeout         │           │
│   │ • Trace ID        │         │ • Deadline        │           │
│   │ • User info       │         │ • Parent cancel   │           │
│   └───────────────────┘         └───────────────────┘           │
│                                                                 │
│   Rule: Business data → Explicit parameters                    │
│         Infrastructure metadata → Context values                │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Context의 불변성과 체이닝

Context는 불변(immutable)입니다. 값을 추가하거나 취소 기능을 부여할 때마다 기존 context를 래핑하는 새로운 context가 생성됩니다. 이는 부모-자식 관계의 체인을 형성하며, 취소 신호는 부모에서 자식 방향으로만 전파됩니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Context Chain (Immutable)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   context.Background()                                          │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  WithValue(parent, "traceID", "abc-123")                │   │
│   │  → New context wrapping parent                          │   │
│   └────────────────────────┬────────────────────────────────┘   │
│                            │                                    │
│                            ▼                                    │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  WithTimeout(parent, 30*time.Second)                    │   │
│   │  → New context wrapping previous                        │   │
│   └────────────────────────┬────────────────────────────────┘   │
│                            │                                    │
│                            ▼                                    │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  WithCancel(parent)                                     │   │
│   │  → New context wrapping previous                        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   Value lookup: Walks UP the chain until found                  │
│   Cancellation: Propagates DOWN to all children                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Context 생성 함수들

context 패키지는 여러 생성 함수를 제공합니다. context.Background()는 모든 context 체인의 시작점으로, main 함수나 최상위 요청 처리에서 사용합니다. context.TODO()는 아직 어떤 context를 사용할지 결정하지 못한 개발 중인 코드에서 임시로 사용하며, 프로덕션 코드에는 남아있으면 안 됩니다.

```go
// 루트 context - 프로그램 진입점에서 사용
ctx := context.Background()

// 개발 중 placeholder - 프로덕션에서 사용 금지
ctx := context.TODO()

// 값 추가
ctx = context.WithValue(ctx, key, value)

// 수동 취소 가능
ctx, cancel := context.WithCancel(ctx)
defer cancel()

// 타임아웃 (상대 시간)
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

// 데드라인 (절대 시간)
ctx, cancel := context.WithDeadline(ctx, time.Now().Add(5*time.Second))
defer cancel()
```

### 4. Context Values: 안전한 키 정의 패턴

context.WithValue를 사용할 때 키 충돌을 방지하려면 unexported 타입을 사용해야 합니다. string이나 int 같은 공용 타입을 키로 사용하면 다른 패키지와 충돌할 수 있습니다.

두 가지 패턴이 있습니다. 여러 관련 키가 필요하면 int 기반 타입과 iota를 사용합니다. 단일 키만 필요하면 빈 struct 타입을 사용합니다.

```go
// 패턴 1: 여러 키가 필요할 때 (int + iota)
type contextKey int

const (
    _ contextKey = iota
    userIDKey
    roleKey
    tenantKey
)

// 패턴 2: 단일 키일 때 (empty struct)
type traceIDKey struct{}

// 값 설정/추출 함수 (캡슐화)
func ContextWithTraceID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, traceIDKey{}, id)
}

func TraceIDFromContext(ctx context.Context) (string, bool) {
    id, ok := ctx.Value(traceIDKey{}).(string)
    return id, ok
}
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    Context Key Patterns                         │
├───────────────────────────────┬─────────────────────────────────┤
│       int + iota Pattern      │     empty struct Pattern        │
├───────────────────────────────┼─────────────────────────────────┤
│                               │                                 │
│  type ctxKey int              │  type traceIDKey struct{}       │
│                               │                                 │
│  const (                      │  // No memory allocation        │
│      _ ctxKey = iota          │  // Unique type = unique key    │
│      userIDKey                │                                 │
│      roleKey                  │  ctx.Value(traceIDKey{})        │
│  )                            │                                 │
│                               │                                 │
│  ctx.Value(userIDKey)         │                                 │
│  ctx.Value(roleKey)           │                                 │
│                               │                                 │
├───────────────────────────────┼─────────────────────────────────┤
│  Use when: Multiple related   │  Use when: Single key needed    │
│  keys in same package         │                                 │
└───────────────────────────────┴─────────────────────────────────┘
```

### 5. 취소(Cancellation) 메커니즘

context.WithCancel은 수동으로 취소할 수 있는 context를 생성합니다. 반환된 cancel 함수를 호출하면 해당 context와 모든 자식 context의 Done() 채널이 닫힙니다. cancel 함수는 반드시 호출해야 합니다. 호출하지 않으면 context가 가비지 컬렉션되지 않아 메모리 누수가 발생합니다.

```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()  // 항상 defer로 호출

go func() {
    for {
        select {
        case <-ctx.Done():
            // 정리 작업 후 종료
            return
        case work := <-workCh:
            // 작업 처리
            process(work)
        }
    }
}()
```

Go 1.20에서 추가된 context.WithCancelCause는 취소 원인을 전달할 수 있습니다. 이는 여러 goroutine 중 어디서 왜 취소되었는지 추적하는 데 유용합니다.

```go
ctx, cancelFunc := context.WithCancelCause(context.Background())
defer cancelFunc(nil)  // 정상 종료 시 nil 전달

// 에러 발생 시 원인 전달
cancelFunc(fmt.Errorf("operation failed: %w", err))

// 취소 원인 확인
if cause := context.Cause(ctx); cause != nil {
    log.Printf("cancelled with cause: %v", cause)
}
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cancellation Propagation                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Main Goroutine                                                │
│        │                                                        │
│        │ ctx, cancel := context.WithCancel(...)                 │
│        │                                                        │
│        ├──────────────────────────────────────┐                 │
│        │                                      │                 │
│        ▼                                      ▼                 │
│   ┌──────────┐                          ┌──────────┐            │
│   │Worker 1  │                          │Worker 2  │            │
│   │          │                          │          │            │
│   │  select {│                          │  select {│            │
│   │  case <- │                          │  case <- │            │
│   │   ctx.   │                          │   ctx.   │            │
│   │   Done():│                          │   Done():│            │
│   │   return │                          │   return │            │
│   │  }       │                          │  }       │            │
│   └──────────┘                          └──────────┘            │
│        │                                      │                 │
│        │◄─────────── cancel() ────────────────┤                 │
│        │                                      │                 │
│        │      Done() channels are closed      │                 │
│        │      All workers exit cleanly        │                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6. 타임아웃과 데드라인

context.WithTimeout은 지정된 시간이 지나면 자동으로 취소되는 context를 생성합니다. context.WithDeadline은 특정 시각에 취소됩니다. 둘 다 내부적으로는 데드라인 기반으로 동작하며, WithTimeout은 현재 시간에 duration을 더해 데드라인을 계산합니다.

중요한 점은 자식 context의 타임아웃이 부모보다 길어도 부모의 타임아웃에 제한된다는 것입니다. 부모가 2초 타임아웃이고 자식이 3초 타임아웃이면, 실제로는 2초 후에 취소됩니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Nested Timeout Behavior                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   parent, _ := context.WithTimeout(ctx, 2*time.Second)          │
│   child, _ := context.WithTimeout(parent, 3*time.Second)        │
│                                                                 │
│   Timeline:                                                     │
│   ──────────────────────────────────────────────────────────►   │
│   0s         1s         2s         3s                           │
│   │          │          │          │                            │
│   │          │          ▼          │                            │
│   │          │   Parent timeout    │                            │
│   │          │   Child ALSO times  │                            │
│   │          │   out (inherited)   │                            │
│   │          │          │          ▼                            │
│   │          │          │   Child's own timeout                 │
│   │          │          │   (never reached)                     │
│                                                                 │
│   Rule: Child deadline cannot exceed parent deadline            │
│                                                                 │
│   ctx.Err() returns:                                            │
│   • context.DeadlineExceeded - timeout/deadline reached         │
│   • context.Canceled - manual cancel() called                   │
└─────────────────────────────────────────────────────────────────┘
```

### 7. HTTP에서의 Context 사용 패턴

HTTP 핸들러에서 context는 req.Context()로 추출합니다. 미들웨어에서 값을 추가하려면 req.WithContext()로 새 request를 생성합니다. 외부 서비스 호출 시에는 http.NewRequestWithContext()로 context를 포함한 요청을 생성합니다.

```go
// 미들웨어에서 context에 값 추가
func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        userID := extractUserID(r)
        ctx := r.Context()
        ctx = ContextWithUserID(ctx, userID)
        r = r.WithContext(ctx)  // 새 request 생성
        next.ServeHTTP(w, r)
    })
}

// 핸들러에서 context 사용
func handleRequest(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    userID, ok := UserIDFromContext(ctx)
    if !ok {
        http.Error(w, "unauthorized", http.StatusUnauthorized)
        return
    }
    // 외부 서비스 호출 시 context 전달
    result, err := callExternalService(ctx, userID)
    // ...
}

// 외부 서비스 호출
func callExternalService(ctx context.Context, userID string) (Result, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", apiURL, nil)
    if err != nil {
        return Result{}, err
    }
    resp, err := client.Do(req)  // context 취소 시 요청도 취소됨
    // ...
}
```

### 8. Context Values vs 명시적 매개변수

context.WithValue를 과도하게 사용하면 함수 시그니처만 보고 필요한 데이터를 알 수 없어 코드 이해가 어려워집니다. 핵심 원칙은 비즈니스 로직에 필요한 데이터는 명시적 매개변수로, 시스템 관리용 메타데이터만 context에 담는 것입니다.

```
┌─────────────────────────────────────────────────────────────────┐
│          Context Values vs Explicit Parameters                  │
├───────────────────────────────┬─────────────────────────────────┤
│     Context Values (OK)       │    Explicit Parameters (OK)     │
├───────────────────────────────┼─────────────────────────────────┤
│                               │                                 │
│ • Trace ID / Request ID       │ • User ID (for business logic)  │
│ • Logging configuration       │ • Order data                    │
│ • Auth token (raw)            │ • Query parameters              │
│ • Tenant ID (multi-tenant)    │ • Function inputs               │
│                               │                                 │
│ Infrastructure / Cross-       │ Business logic dependencies     │
│ cutting concerns              │                                 │
│                               │                                 │
├───────────────────────────────┴─────────────────────────────────┤
│                                                                 │
│ ✗ Bad: func Process(ctx context.Context) error                  │
│        // What does this need? Hidden dependencies!             │
│                                                                 │
│ ✓ Good: func Process(ctx context.Context, order Order) error    │
│         // Clear what the function needs                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9. 장시간 실행 작업에서의 취소 확인

채널 연산이 없는 장시간 실행 코드에서는 주기적으로 context 취소를 확인해야 합니다. 그렇지 않으면 클라이언트가 떠나도 불필요한 계산이 계속됩니다.

```go
func processLargeDataset(ctx context.Context, data []Item) error {
    for i, item := range data {
        // 매 100번째 항목마다 취소 확인
        if i%100 == 0 {
            if err := ctx.Err(); err != nil {
                return err  // 취소됨
            }
        }
        process(item)
    }
    return nil
}

// 또는 context.Cause() 사용 (Go 1.20+)
func computeExpensive(ctx context.Context) (Result, error) {
    for {
        if err := context.Cause(ctx); err != nil {
            return partialResult, err
        }
        // 계산 수행
    }
}
```

### 10. GUID/Trace ID 전파 패턴

분산 시스템에서 요청 추적을 위해 GUID(Trace ID)를 context에 저장하고 전파하는 것은 좋은 사례입니다. 이 값은 비즈니스 로직에 직접 필요하지 않지만, 로깅과 모니터링에 필수적입니다.

```go
package tracker

type traceIDKey struct{}

func ContextWithTraceID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, traceIDKey{}, id)
}

func TraceIDFromContext(ctx context.Context) (string, bool) {
    id, ok := ctx.Value(traceIDKey{}).(string)
    return id, ok
}

// 미들웨어: 들어오는 요청에서 추출 또는 생성
func TraceMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := r.Header.Get("X-Trace-ID")
        if id == "" {
            id = uuid.New().String()
        }
        ctx := ContextWithTraceID(r.Context(), id)
        r = r.WithContext(ctx)
        next.ServeHTTP(w, r)
    })
}

// 나가는 요청에 Trace ID 추가
func PropagateTraceID(req *http.Request) *http.Request {
    if id, ok := TraceIDFromContext(req.Context()); ok {
        req.Header.Set("X-Trace-ID", id)
    }
    return req
}
```

---

## 비교표

### Context 생성 함수 비교

| 함수 | 용도 | 취소 방법 | 반환값 |
|------|------|----------|--------|
| Background() | 루트 context | - | context.Context |
| TODO() | 개발 중 placeholder | - | context.Context |
| WithValue() | 값 추가 | 부모 따름 | context.Context |
| WithCancel() | 수동 취소 | cancel() | ctx, cancel |
| WithCancelCause() | 원인 추적 취소 | cancel(err) | ctx, cancel |
| WithTimeout() | 상대 시간 취소 | 자동/cancel() | ctx, cancel |
| WithDeadline() | 절대 시간 취소 | 자동/cancel() | ctx, cancel |

### Context.Err() 반환값

| 값 | 의미 | 발생 조건 |
|----|------|----------|
| nil | 취소되지 않음 | Done() 열려있음 |
| context.Canceled | 수동 취소 | cancel() 호출됨 |
| context.DeadlineExceeded | 시간 초과 | 타임아웃/데드라인 도달 |

### Context Methods

| 메서드 | 반환 타입 | 설명 |
|--------|----------|------|
| Done() | <-chan struct{} | 취소 시 닫히는 채널 |
| Err() | error | 취소 원인 (nil/Canceled/DeadlineExceeded) |
| Deadline() | (time.Time, bool) | 설정된 데드라인, 설정 여부 |
| Value(key) | any | 저장된 값 (없으면 nil) |

---

## 면접 예상 질문 및 모범 답안

### Q1. Go에서 context를 함수의 첫 번째 매개변수로 전달하는 이유는 무엇인가요? 다른 언어의 접근 방식과 어떻게 다른가요?

**모범 답안:**

Go는 명시적인 context 전달을 선호합니다. 다른 언어에서는 ThreadLocal, AsyncLocal, implicit context 같은 암묵적 메커니즘을 사용하지만, Go는 함수 시그니처에 context를 명시합니다.

이 접근 방식의 장점은 세 가지입니다. 첫째, 함수가 어떤 컨텍스트 정보에 접근하는지 명확히 보입니다. 둘째, goroutine 간 컨텍스트 전파가 명시적이어서 추적하기 쉽습니다. 셋째, 테스트에서 쉽게 모킹하거나 조작할 수 있습니다.

단점으로는 많은 함수에 context 매개변수를 추가해야 해서 코드가 다소 장황해질 수 있습니다. 그러나 Go 커뮤니티는 이 트레이드오프가 명확성과 추적성 면에서 가치가 있다고 판단합니다.

관례적으로 context는 항상 첫 번째 매개변수이며, 변수명은 ctx를 사용합니다. 이 일관성 덕분에 코드 리뷰에서 context 누락을 쉽게 발견할 수 있습니다.

---

### Q2. context.WithCancel의 cancel 함수를 반드시 호출해야 하는 이유는 무엇인가요?

**모범 답안:**

cancel 함수를 호출하지 않으면 리소스 누수가 발생합니다. WithCancel, WithTimeout, WithDeadline은 내부적으로 타이머와 채널을 생성하며, 이 리소스들은 cancel 호출이나 부모 context 취소 전까지 해제되지 않습니다.

특히 WithTimeout이나 WithDeadline의 경우, 작업이 타임아웃 전에 완료되더라도 cancel을 호출해야 타이머 리소스가 즉시 해제됩니다. 호출하지 않으면 타임아웃까지 타이머가 유지됩니다.

올바른 패턴은 context 생성 직후 defer cancel()을 호출하는 것입니다.

```go
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()  // 함수 종료 시 반드시 호출됨

// 작업 수행
```

cancel을 여러 번 호출해도 안전합니다. 첫 번째 호출 이후의 호출은 무시됩니다. 따라서 defer로 호출하면서 특정 조건에서 조기에 호출하는 것도 가능합니다.

---

### Q3. context.WithValue를 사용할 때 왜 unexported 타입을 키로 사용해야 하나요? 어떤 패턴들이 있나요?

**모범 답안:**

string이나 int 같은 공용 타입을 키로 사용하면 다른 패키지와 충돌할 수 있습니다. 예를 들어 두 패키지가 모두 "userID"라는 문자열 키를 사용하면 서로의 값을 덮어쓰게 됩니다.

unexported 타입은 해당 패키지 내에서만 접근 가능하므로 다른 패키지와 충돌할 수 없습니다. Go의 타입 시스템이 키 고유성을 보장합니다.

두 가지 패턴이 있습니다. 첫째, 여러 관련 키가 필요하면 int 기반 타입과 iota를 사용합니다.

```go
type contextKey int
const (
    _ contextKey = iota
    userIDKey
    roleKey
)
```

둘째, 단일 키만 필요하면 빈 struct를 사용합니다. 빈 struct는 메모리를 차지하지 않으며, 타입 자체가 고유한 키가 됩니다.

```go
type traceIDKey struct{}
ctx.Value(traceIDKey{})
```

추가로 값 설정/추출 함수를 제공하여 캡슐화하는 것이 좋습니다. ContextWithX와 XFromContext 네이밍 컨벤션을 따릅니다.

---

### Q4. 부모 context에 2초 타임아웃이 있고, 자식 context에 5초 타임아웃을 설정하면 어떻게 되나요?

**모범 답안:**

자식 context의 타임아웃은 부모의 타임아웃을 초과할 수 없습니다. 이 경우 자식은 부모의 2초 타임아웃에 제한됩니다.

```go
parent, cancel := context.WithTimeout(ctx, 2*time.Second)
defer cancel()
child, cancel2 := context.WithTimeout(parent, 5*time.Second)
defer cancel2()

<-child.Done()  // 2초 후 취소됨 (5초 아님)
```

이는 context의 계층 구조 설계 때문입니다. 자식은 부모로부터 취소를 상속받으며, 부모가 취소되면 모든 자식도 즉시 취소됩니다. 자식이 더 긴 타임아웃을 설정해도 부모의 제한을 벗어날 수 없습니다.

이 동작은 안전성을 위한 것입니다. 상위 레벨에서 설정한 타임아웃을 하위 레벨에서 임의로 연장할 수 없어야 시스템 전체의 시간 제한을 신뢰할 수 있습니다.

Deadline() 메서드로 실제 데드라인을 확인할 수 있습니다. 자식 context에서 호출하면 부모와 자식 중 더 이른 데드라인이 반환됩니다.

---

### Q5. context.Value를 과도하게 사용하면 왜 문제가 되나요? 어떤 데이터를 context에 넣어야 하나요?

**모범 답안:**

context.Value를 과도하게 사용하면 함수의 의존성이 숨겨집니다. 함수 시그니처만 보고는 어떤 데이터가 필요한지 알 수 없어 코드 이해와 테스트가 어려워집니다.

잘못된 사용 예시는 비즈니스 로직에 필요한 데이터를 context에 숨기는 것입니다.

```go
// 나쁜 예: 의존성이 숨겨짐
func ProcessOrder(ctx context.Context) error {
    order := ctx.Value(orderKey).(Order)  // 어떤 데이터가 필요한지 모름
    // ...
}

// 좋은 예: 의존성이 명시적
func ProcessOrder(ctx context.Context, order Order) error {
    // ...
}
```

context.Value에 적합한 데이터는 시스템 관리용 메타데이터입니다. 요청 추적 ID(Trace ID), 인증 토큰, 로깅 설정, 멀티테넌트 환경의 테넌트 ID 등이 해당합니다. 이런 데이터는 비즈니스 로직에 직접 사용되지 않지만 인프라 레이어에서 필요합니다.

기준은 "이 데이터가 없어도 비즈니스 로직이 동작하는가?"입니다. 로깅에만 필요한 Trace ID는 context에 적합하고, 주문 처리에 필수인 주문 ID는 명시적 매개변수로 전달해야 합니다.

---

### Q6. HTTP 서버에서 context가 자동으로 취소되는 경우는 언제인가요? 이를 어떻게 활용해야 하나요?

**모범 답안:**

Go의 net/http 패키지에서 클라이언트가 연결을 끊으면 req.Context()로 얻은 context가 자동으로 취소됩니다. 이를 통해 불필요해진 작업을 빠르게 중단할 수 있습니다.

활용하려면 핸들러에서 시작하는 모든 goroutine과 외부 서비스 호출에 context를 전달해야 합니다.

```go
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // 데이터베이스 쿼리에 context 전달
    result, err := db.QueryContext(ctx, query)
    if err != nil {
        if ctx.Err() == context.Canceled {
            return  // 클라이언트가 떠남, 응답 불필요
        }
        // 실제 에러 처리
    }

    // 외부 API 호출에 context 전달
    req, _ := http.NewRequestWithContext(ctx, "GET", apiURL, nil)
    resp, err := client.Do(req)
    // ...
}
```

이 패턴의 이점은 클라이언트가 떠나면 데이터베이스 쿼리, 외부 API 호출, 백그라운드 계산이 모두 중단되어 서버 리소스를 절약하는 것입니다. 특히 느린 응답이나 클라이언트 타임아웃 상황에서 효과적입니다.

---

## 실무 체크리스트

### Context 기본 사용
- [ ] context는 함수의 첫 번째 매개변수로 전달하는가?
- [ ] Background()를 루트 context로 사용하는가?
- [ ] TODO()가 프로덕션 코드에 남아있지 않은가?

### 취소 처리
- [ ] cancel 함수를 defer로 호출하는가?
- [ ] select에서 ctx.Done()을 확인하는가?
- [ ] 장시간 작업에서 주기적으로 취소를 확인하는가?
- [ ] WithCancelCause로 취소 원인을 추적하는가?

### 값 전달
- [ ] unexported 타입을 키로 사용하는가?
- [ ] ContextWith*/FromContext 함수로 캡슐화하는가?
- [ ] 비즈니스 데이터는 명시적 매개변수로 전달하는가?
- [ ] context에는 메타데이터만 저장하는가?

### HTTP 패턴
- [ ] req.Context()로 context를 추출하는가?
- [ ] req.WithContext()로 새 request를 생성하는가?
- [ ] NewRequestWithContext()로 외부 요청을 생성하는가?
- [ ] 클라이언트 연결 종료 시 작업을 중단하는가?

### 타임아웃
- [ ] 외부 호출에 적절한 타임아웃을 설정하는가?
- [ ] 자식 타임아웃이 부모보다 짧은지 확인하는가?
- [ ] Deadline()으로 남은 시간을 확인하는가?
- [ ] Err()로 취소/타임아웃을 구분하는가?

---

## 참고 자료

- [context 패키지 공식 문서](https://pkg.go.dev/context)
- [Go Blog: Context and Structs](https://go.dev/blog/context-and-structs)
- [Go Blog: Contexts and struct](https://go.dev/blog/context-is-for-cancellation)
- [Go Concurrency Patterns: Context](https://go.dev/blog/context)
- [Standard library HTTP package](https://pkg.go.dev/net/http)
