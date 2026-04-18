# Chapter 12: Concurrency in Go - 면접정리

## 핵심 개념 상세 설명

### 1. Go의 동시성 철학: CSP와 "Share memory by communicating"

Go의 동시성 모델은 Tony Hoare가 1978년에 발표한 CSP(Communicating Sequential Processes) 이론에 기반합니다. 전통적인 스레드 프로그래밍에서는 공유 메모리를 통해 통신하고 락으로 보호하는 방식을 사용하지만, Go는 정반대의 접근법을 취합니다. "Don't communicate by sharing memory; share memory by communicating"이라는 격언이 이를 잘 표현합니다. 채널을 통해 데이터의 소유권을 명시적으로 전달함으로써 동시 접근 문제를 구조적으로 해결합니다. 이 방식은 데이터 레이스를 컴파일 시점에 예방할 수는 없지만, 올바르게 사용하면 런타임에 발생할 가능성을 크게 줄여줍니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Traditional Threading                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐        ┌──────────┐        ┌──────────┐         │
│   │ Thread 1 │        │ Thread 2 │        │ Thread 3 │         │
│   └────┬─────┘        └────┬─────┘        └────┬─────┘         │
│        │                   │                   │                │
│        └───────────────────┼───────────────────┘                │
│                            ▼                                    │
│                   ┌────────────────┐                            │
│                   │ Shared Memory  │◄─── Lock/Mutex             │
│                   │   (危险区域)    │     protection             │
│                   └────────────────┘                            │
│                                                                 │
│   Problem: Lock contention, Deadlocks, Race conditions          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Go's CSP Model                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌───────────┐    chan    ┌───────────┐    chan    ┌────────┐ │
│   │Goroutine 1│───────────▶│Goroutine 2│───────────▶│Goroutine│ │
│   │ (Owner)   │   send     │ (Owner)   │   send     │   3    │ │
│   └───────────┘            └───────────┘            └────────┘ │
│                                                                 │
│   Data ownership is TRANSFERRED through channels                │
│   Only ONE goroutine owns data at any time                      │
│                                                                 │
│   Benefit: No locks needed, Clear ownership, Composable         │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Goroutine: 경량 실행 단위

Goroutine은 Go 런타임이 관리하는 경량 실행 단위입니다. OS 스레드와 달리 goroutine은 약 2KB의 초기 스택으로 시작하며, 필요에 따라 동적으로 늘어나고 줄어듭니다. OS 스레드는 일반적으로 1-8MB의 고정 스택을 가지므로 수천 개를 생성하면 메모리 고갈이 발생하지만, goroutine은 수십만 개까지도 효율적으로 운영할 수 있습니다.

Go 스케줄러는 M:N 스케줄링 모델을 사용합니다. M개의 goroutine을 N개의 OS 스레드에 멀티플렉싱하는 방식입니다. 스케줄러는 세 가지 핵심 구조체를 사용합니다: G(goroutine), M(machine, OS thread), P(processor, 논리적 프로세서). P의 개수는 기본적으로 GOMAXPROCS(CPU 코어 수)와 같으며, 이 값이 동시에 실행 가능한 goroutine의 최대 개수를 결정합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Go Scheduler (GMP Model)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    Global Run Queue                      │   │
│   │  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐      │   │
│   │  │ G │ │ G │ │ G │ │ G │ │ G │ │ G │ │ G │ │ G │ ...  │   │
│   │  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘      │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│   │      P1      │  │      P2      │  │      P3      │         │
│   │ Local Queue  │  │ Local Queue  │  │ Local Queue  │         │
│   │ ┌──┬──┬──┐   │  │ ┌──┬──┬──┐   │  │ ┌──┬──┬──┐   │         │
│   │ │G │G │G │   │  │ │G │G │G │   │  │ │G │G │G │   │         │
│   │ └──┴──┴──┘   │  │ └──┴──┴──┘   │  │ └──┴──┴──┘   │         │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│          │                 │                 │                  │
│          ▼                 ▼                 ▼                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│   │      M1      │  │      M2      │  │      M3      │         │
│   │  (OS Thread) │  │  (OS Thread) │  │  (OS Thread) │         │
│   └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│   Work Stealing: 빈 P가 다른 P의 Local Queue에서 G를 훔쳐옴     │
└─────────────────────────────────────────────────────────────────┘
```

Goroutine의 스케줄링은 협력적(cooperative)입니다. 런타임은 함수 호출 시점, 채널 연산 시점, 시스템 콜 대기 시점 등에서 컨텍스트 스위칭을 수행합니다. 이 때문에 무한 루프만 있는 goroutine은 다른 goroutine을 굶길 수 있습니다. Go 1.14부터는 비동기 선점(asynchronous preemption)이 도입되어 10ms 이상 실행되는 goroutine은 강제로 선점됩니다.

### 3. Channel: 타입 안전한 통신 파이프

Channel은 goroutine 간에 값을 안전하게 주고받는 타입 안전한 큐입니다. 채널은 unbuffered(동기)와 buffered(비동기) 두 종류가 있습니다.

Unbuffered 채널은 송신자와 수신자가 동시에 준비될 때까지 양쪽 모두 블록됩니다. 이는 "랑데부(rendezvous)" 또는 "핸드셰이크" 통신으로, 데이터 전달과 동기화를 동시에 달성합니다. 마치 직접 손에서 손으로 물건을 건네는 것과 같습니다.

Buffered 채널은 지정된 용량만큼의 값을 저장할 수 있습니다. 버퍼가 가득 차지 않으면 송신은 블록되지 않고, 버퍼가 비어있지 않으면 수신은 블록되지 않습니다. 생산자-소비자 패턴에서 속도 차이를 완충하는 데 유용합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Unbuffered Channel                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ch := make(chan int)  // capacity = 0                         │
│                                                                 │
│   Sender                              Receiver                  │
│   ┌──────────┐                        ┌──────────┐              │
│   │ ch <- 42 │ ◄────── BLOCKED ──────▶│ v := <-ch│              │
│   └──────────┘        until both      └──────────┘              │
│                       are ready                                 │
│                                                                 │
│   ════════════════════════════════════════════════              │
│   │          │ SYNCHRONIZATION POINT │          │               │
│   ════════════════════════════════════════════════              │
│                                                                 │
│   특징: 완벽한 동기화, 데이터 전달 = 동기화 지점                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Buffered Channel                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ch := make(chan int, 3)  // capacity = 3                      │
│                                                                 │
│   ┌───────────────────────────────────────┐                     │
│   │  Buffer: [  1  |  2  |  _  ]          │                     │
│   │           ▲           ▲               │                     │
│   │          read        write            │                     │
│   └───────────────────────────────────────┘                     │
│                                                                 │
│   Send blocks when: len(ch) == cap(ch)  (buffer full)           │
│   Recv blocks when: len(ch) == 0        (buffer empty)          │
│                                                                 │
│   특징: 생산/소비 속도 차이 완충, 처리량(throughput) 향상       │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Channel 상태별 동작 테이블

채널의 상태(열림/닫힘/nil)에 따라 송신, 수신, 닫기 연산의 동작이 달라집니다. 이 테이블은 면접에서 자주 출제되므로 정확히 암기해야 합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│              Channel Operation Behavior Matrix                  │
├───────────────┬─────────────────────────────────────────────────┤
│   Operation   │        Channel State                            │
│               ├──────────────┬──────────────┬──────────────────┤
│               │    Open      │   Closed     │      nil         │
├───────────────┼──────────────┼──────────────┼──────────────────┤
│   Send        │  Block until │   PANIC!     │  Block forever   │
│   ch <- v     │  receive     │              │  (deadlock)      │
├───────────────┼──────────────┼──────────────┼──────────────────┤
│   Receive     │  Block until │  Zero value  │  Block forever   │
│   <-ch        │  send        │  immediately │  (deadlock)      │
├───────────────┼──────────────┼──────────────┼──────────────────┤
│   Close       │  Success     │   PANIC!     │   PANIC!         │
│   close(ch)   │              │              │                  │
├───────────────┼──────────────┼──────────────┼──────────────────┤
│   v, ok :=    │  v=value     │  v=zero val  │  Block forever   │
│   <-ch        │  ok=true     │  ok=false    │                  │
└───────────────┴──────────────┴──────────────┴──────────────────┘

Key Points:
• 닫힌 채널에 송신 → panic (복구 불가능)
• 닫힌 채널에서 수신 → zero value 즉시 반환 (ok=false로 구분)
• nil 채널 연산 → 영원히 블록 (select에서 case 비활성화에 활용)
• 채널은 송신 측에서만 닫아야 함 (수신 측에서 닫으면 안 됨)
```

### 5. Select 문: 다중 채널 처리

select 문은 여러 채널 연산을 동시에 대기하고, 먼저 준비되는 연산을 실행합니다. switch와 비슷하게 생겼지만, case는 채널 연산이어야 합니다.

중요한 특성으로, 여러 case가 동시에 준비되면 Go 런타임이 의사 난수(pseudo-random)로 하나를 선택합니다. 이는 특정 채널이 다른 채널을 굶기는(starvation) 것을 방지합니다. 따라서 select case의 순서에 의존하는 코드는 버그입니다.

default case가 있으면 모든 채널이 준비되지 않았을 때 즉시 실행되어 논블로킹(non-blocking) 연산이 됩니다.

```go
select {
case v := <-ch1:
    // ch1에서 수신 성공
case ch2 <- x:
    // ch2로 송신 성공
case <-time.After(1 * time.Second):
    // 타임아웃
default:
    // 모든 채널이 준비 안 됨 (논블로킹)
}
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    Select Execution Flow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                      select {                            │   │
│   │                        case ...:                         │   │
│   │                        case ...:                         │   │
│   │                        default:                          │   │
│   │                      }                                   │   │
│   └──────────────────────────┬──────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│              ┌───────────────────────────────┐                  │
│              │  Evaluate all case channels   │                  │
│              │    simultaneously             │                  │
│              └───────────────┬───────────────┘                  │
│                              │                                  │
│              ┌───────────────┴───────────────┐                  │
│              │  How many cases are ready?    │                  │
│              └───────────────┬───────────────┘                  │
│                              │                                  │
│          ┌───────────────────┼───────────────────┐              │
│          ▼                   ▼                   ▼              │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│   │   0 ready   │     │   1 ready   │     │  2+ ready   │       │
│   │             │     │             │     │             │       │
│   │ Has default?│     │ Execute it  │     │  RANDOM     │       │
│   │   Yes→run   │     │             │     │  selection  │       │
│   │   No→block  │     │             │     │             │       │
│   └─────────────┘     └─────────────┘     └─────────────┘       │
│                                                                 │
│   Random selection prevents starvation of any channel           │
└─────────────────────────────────────────────────────────────────┘
```

### 6. for-select 패턴과 종료 처리

for-select 루프는 Go 동시성의 핵심 패턴입니다. 무한 루프에서 select로 여러 채널을 처리하며, 종료 시그널을 받으면 깔끔하게 종료합니다.

```go
func worker(ctx context.Context, jobs <-chan Job, results chan<- Result) {
    for {
        select {
        case <-ctx.Done():
            // 취소 시그널 - 정리 후 종료
            return
        case job, ok := <-jobs:
            if !ok {
                // jobs 채널 닫힘 - 정리 후 종료
                return
            }
            result := process(job)
            select {
            case results <- result:
            case <-ctx.Done():
                return
            }
        }
    }
}
```

```
┌─────────────────────────────────────────────────────────────────┐
│                 for-select Loop Pattern                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  for {                                                   │   │
│   │      select {                                            │   │
│   │      case <-done:           ←── Termination signal       │   │
│   │          cleanup()                                       │   │
│   │          return                                          │   │
│   │      case v := <-input:     ←── Work input               │   │
│   │          result := process(v)                            │   │
│   │          output <- result                                │   │
│   │      }                                                   │   │
│   │  }                                                       │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   Key principles:                                               │
│   1. Always have a termination case (done channel or context)  │
│   2. Check ok value to detect closed input channels            │
│   3. Nested select for cancellable output                      │
│   4. Clean up resources before returning                       │
└─────────────────────────────────────────────────────────────────┘
```

### 7. Context: 취소, 타임아웃, 값 전파

context 패키지는 goroutine 트리에 취소 시그널, 타임아웃, 요청 범위 값을 전파하는 표준 메커니즘입니다. 모든 장기 실행 함수와 I/O 함수의 첫 번째 매개변수로 context.Context를 받는 것이 관례입니다.

```go
// 취소 가능한 context
ctx, cancel := context.WithCancel(context.Background())
defer cancel()  // 항상 cancel 호출 (리소스 누수 방지)

// 타임아웃 context
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// 데드라인 context
deadline := time.Now().Add(10 * time.Second)
ctx, cancel := context.WithDeadline(context.Background(), deadline)
defer cancel()

// 값 전달 (주의: 요청 범위 값만, 옵션 매개변수 대용 X)
ctx = context.WithValue(ctx, requestIDKey, "abc123")
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    Context Hierarchy                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    context.Background()                         │
│                           │                                     │
│                           ▼                                     │
│              ┌─────────────────────────┐                        │
│              │   WithCancel(parent)    │                        │
│              │   WithTimeout(parent)   │                        │
│              │   WithDeadline(parent)  │                        │
│              │   WithValue(parent)     │                        │
│              └────────────┬────────────┘                        │
│                           │                                     │
│           ┌───────────────┼───────────────┐                     │
│           ▼               ▼               ▼                     │
│       ┌───────┐       ┌───────┐       ┌───────┐                 │
│       │ Child │       │ Child │       │ Child │                 │
│       │Context│       │Context│       │Context│                 │
│       └───┬───┘       └───┬───┘       └───────┘                 │
│           │               │                                     │
│           ▼               ▼                                     │
│       ┌───────┐       ┌───────┐                                 │
│       │Grand  │       │Grand  │                                 │
│       │ child │       │ child │                                 │
│       └───────┘       └───────┘                                 │
│                                                                 │
│   Cancellation propagates DOWN the tree                         │
│   Parent cancelled → All descendants cancelled                  │
│   Child cancelled → Parent NOT affected                         │
└─────────────────────────────────────────────────────────────────┘
```

### 8. WaitGroup: Goroutine 완료 대기

sync.WaitGroup은 여러 goroutine의 완료를 기다리는 카운터입니다. Add로 대기할 goroutine 수를 추가하고, Done으로 완료를 알리며, Wait로 모든 완료를 기다립니다.

```go
var wg sync.WaitGroup

for _, item := range items {
    wg.Add(1)
    go func(item Item) {
        defer wg.Done()  // 함수 종료 시 반드시 호출
        process(item)
    }(item)
}

wg.Wait()  // 모든 goroutine 완료 대기
```

중요한 규칙: Add()는 반드시 goroutine 시작 전에 호출해야 합니다. goroutine 내부에서 Add()를 호출하면 Wait()가 0 카운터를 보고 조기 반환할 수 있습니다.

### 9. Mutex: 공유 상태 보호

채널이 적합하지 않은 경우(예: 인메모리 캐시, 카운터), sync.Mutex로 공유 상태를 보호합니다.

```go
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}
```

sync.RWMutex는 읽기 작업이 많을 때 유용합니다. 여러 goroutine이 동시에 읽을 수 있지만, 쓰기는 배타적입니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                  Mutex vs RWMutex                               │
├───────────────────────────────┬─────────────────────────────────┤
│          sync.Mutex           │        sync.RWMutex             │
├───────────────────────────────┼─────────────────────────────────┤
│  Lock()   → exclusive access  │  Lock()   → exclusive write     │
│  Unlock() → release           │  Unlock() → release write       │
│                               │  RLock()  → shared read         │
│  Only one goroutine at a time │  RUnlock()→ release read        │
│                               │                                 │
│                               │  Multiple readers OR one writer │
├───────────────────────────────┴─────────────────────────────────┤
│  Use Case: Few reads, many writes                               │
│  Use Case: Many reads, few writes (RWMutex)                     │
│                                                                 │
│  ⚠️ Warning: RWMutex has higher overhead than Mutex             │
│     Only use RWMutex if read >> write                           │
└─────────────────────────────────────────────────────────────────┘
```

### 10. 동시성 패턴들

#### Pattern 1: Nil Channel로 Case 비활성화

nil 채널 연산은 영원히 블록되므로, select에서 특정 case를 동적으로 비활성화하는 데 활용합니다.

```go
func merge(ch1, ch2 <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for ch1 != nil || ch2 != nil {
            select {
            case v, ok := <-ch1:
                if !ok {
                    ch1 = nil  // case 비활성화
                    continue
                }
                out <- v
            case v, ok := <-ch2:
                if !ok {
                    ch2 = nil  // case 비활성화
                    continue
                }
                out <- v
            }
        }
    }()
    return out
}
```

#### Pattern 2: Backpressure (역압)

버퍼드 채널을 사용해 생산자가 소비자보다 빠를 때 속도를 조절합니다.

```go
// 최대 100개의 작업만 대기 가능
jobs := make(chan Job, 100)

// 생산자 - 버퍼 가득 차면 블록
for _, job := range allJobs {
    jobs <- job  // blocks when buffer full
}
close(jobs)

// 소비자
for job := range jobs {
    process(job)
}
```

#### Pattern 3: Timeout 패턴

```go
select {
case result := <-resultCh:
    return result, nil
case <-time.After(5 * time.Second):
    return nil, errors.New("timeout")
}
```

#### Pattern 4: Done Channel 패턴

```go
done := make(chan struct{})

go func() {
    // 작업 수행
    close(done)  // 완료 시그널 (빈 struct는 메모리 0)
}()

<-done  // 완료 대기
```

---

## 비교표

### 채널 vs 뮤텍스 선택 기준

| 상황 | 추천 | 이유 |
|------|------|------|
| 데이터 소유권 전달 | Channel | 명확한 소유권 이전 |
| 작업 분배/파이프라인 | Channel | 자연스러운 생산자-소비자 패턴 |
| 이벤트 알림 | Channel | 블로킹 대기 지원 |
| 공유 캐시/맵 | Mutex | 직접 접근이 더 효율적 |
| 카운터/통계 | Mutex (또는 atomic) | 단순 상태 업데이트 |
| 구조체 필드 보호 | Mutex | 채널 오버헤드 불필요 |

### Unbuffered vs Buffered Channel

| 특성 | Unbuffered | Buffered |
|------|------------|----------|
| 용량 | 0 | 1 이상 |
| 송신 블록 | 수신자 대기까지 | 버퍼 가득 찰 때까지 |
| 수신 블록 | 송신자 대기까지 | 버퍼 빌 때까지 |
| 동기화 | 완벽한 핸드셰이크 | 비동기적 |
| 용도 | 시그널, 랑데부 | 처리량, 버퍼링 |

### Context 생성 함수들

| 함수 | 용도 | 취소 방법 |
|------|------|----------|
| `Background()` | 최상위, main 함수 | - |
| `TODO()` | 미정, 리팩토링 표시 | - |
| `WithCancel()` | 수동 취소 | `cancel()` 호출 |
| `WithTimeout()` | 상대적 타임아웃 | 자동 또는 `cancel()` |
| `WithDeadline()` | 절대적 데드라인 | 자동 또는 `cancel()` |
| `WithValue()` | 값 전달 | 부모 따름 |

---

## 면접 예상 질문 및 모범 답안

### Q1. Goroutine과 OS Thread의 차이점을 설명하고, Go 스케줄러의 동작 방식을 설명해주세요.

**모범 답안:**

Goroutine과 OS Thread는 여러 중요한 차이점이 있습니다.

첫째, 메모리 사용량에서 큰 차이가 있습니다. OS 스레드는 일반적으로 1MB~8MB의 고정 크기 스택을 할당받지만, goroutine은 단 2KB의 초기 스택으로 시작하여 필요에 따라 동적으로 증가하고 감소합니다. 이 덕분에 하나의 프로세스에서 수십만 개의 goroutine을 생성할 수 있습니다.

둘째, 스케줄링 주체가 다릅니다. OS 스레드는 커널이 선점적으로 스케줄링하여 컨텍스트 스위칭 시 커널 모드 전환이 발생합니다. 반면 goroutine은 Go 런타임이 사용자 공간에서 스케줄링하므로 오버헤드가 훨씬 작습니다.

Go 스케줄러는 GMP 모델을 사용합니다. G는 goroutine, M은 machine(OS 스레드), P는 processor(논리적 프로세서)를 나타냅니다. GOMAXPROCS 개수만큼의 P가 있고, 각 P는 하나의 M에 붙어서 실행됩니다. 각 P는 로컬 실행 큐를 가지며, 빈 P는 다른 P의 큐에서 goroutine을 훔쳐오는 work stealing 알고리즘을 사용합니다.

스케줄링 시점은 채널 연산, 시스템 콜 대기, 함수 호출, 가비지 컬렉션 등에서 발생합니다. Go 1.14부터는 10ms 이상 실행되는 goroutine을 강제로 선점하는 비동기 선점 기능도 추가되었습니다.

---

### Q2. 닫힌 채널에서 수신하면 어떤 일이 발생하나요? 이를 어떻게 활용할 수 있나요?

**모범 답안:**

닫힌 채널에서 수신하면 해당 타입의 zero value가 즉시 반환됩니다. 블록 없이 바로 반환되며, 두 값 할당 형태 `v, ok := <-ch`를 사용하면 ok가 false로 설정되어 채널이 닫혔음을 확인할 수 있습니다.

이 특성은 여러 방식으로 활용됩니다.

첫째, 브로드캐스트 시그널로 사용합니다. 채널을 닫으면 그 채널에서 대기 중인 모든 goroutine이 동시에 깨어납니다. done 채널 패턴에서 `close(done)`을 호출하면 여러 워커가 동시에 종료 시그널을 받을 수 있습니다.

둘째, for-range 루프의 종료 조건으로 사용합니다. `for v := range ch`는 채널이 닫힐 때까지 반복하다가 닫히면 자동으로 루프를 종료합니다.

주의할 점은 닫힌 채널에 송신하면 panic이 발생한다는 것입니다. 따라서 채널은 반드시 송신 측에서만 닫아야 하며, 여러 송신자가 있는 경우 별도의 동기화 메커니즘(예: sync.Once)을 사용해야 합니다. nil 채널에서의 수신은 영원히 블록되고, nil 채널을 닫으면 panic이 발생한다는 것도 기억해야 합니다.

---

### Q3. select 문에서 여러 case가 동시에 ready 상태일 때 어떤 일이 발생하나요? 이것이 왜 중요한가요?

**모범 답안:**

여러 case가 동시에 ready 상태이면 Go 런타임이 의사 난수(pseudo-random)로 하나를 선택합니다. case의 작성 순서와 무관하게 무작위로 선택됩니다.

이 설계가 중요한 이유는 공정성(fairness)을 보장하기 때문입니다. 만약 첫 번째 case가 항상 우선된다면, 첫 번째 채널이 지속적으로 데이터를 생성하는 경우 다른 채널들은 영원히 처리되지 않는 기아(starvation) 상태에 빠질 수 있습니다.

실무에서 이로 인해 주의할 점이 있습니다. select case의 순서에 의존하는 코드를 작성하면 안 됩니다. 예를 들어 "done 채널이 항상 먼저 체크된다"고 가정하면 버그입니다. 특정 case를 우선 처리해야 한다면 중첩된 select를 사용하거나 별도의 고루틴에서 처리해야 합니다.

```go
// 잘못된 예: 순서에 의존
select {
case <-done:    // "이게 먼저"라고 가정하면 안 됨
    return
case v := <-ch:
    process(v)
}

// 올바른 예: done 우선 체크가 필요하면
for {
    select {
    case <-done:
        return
    default:
    }
    select {
    case <-done:
        return
    case v := <-ch:
        process(v)
    }
}
```

---

### Q4. context 패키지의 목적과 주요 사용 패턴을 설명해주세요.

**모범 답안:**

context 패키지는 goroutine 트리 전체에 취소 시그널, 타임아웃, 요청 범위 데이터를 전파하는 표준 메커니즘입니다. HTTP 핸들러에서 시작된 요청이 여러 goroutine으로 분산될 때, 클라이언트가 연결을 끊으면 모든 관련 goroutine을 효율적으로 정리할 수 있습니다.

주요 사용 패턴은 네 가지입니다.

`context.WithCancel`은 수동 취소가 필요할 때 사용합니다. 반환된 cancel 함수를 호출하면 해당 context와 모든 자식 context가 취소됩니다. 반드시 defer cancel()을 호출하여 리소스 누수를 방지해야 합니다.

`context.WithTimeout`은 상대적 시간 제한을 설정합니다. HTTP 클라이언트 요청에 5초 제한을 거는 경우 등에 사용합니다.

`context.WithDeadline`은 절대적 시간 제한을 설정합니다. 특정 시각까지 완료되어야 하는 배치 작업 등에 사용합니다.

`context.WithValue`는 요청 범위 데이터를 전달합니다. 단, 함수 매개변수를 대체하는 용도로 오용하면 안 됩니다. trace ID, 인증 토큰 등 요청 범위에서 암묵적으로 전파되어야 하는 값에만 사용해야 합니다.

context를 사용하는 함수는 첫 번째 매개변수로 ctx context.Context를 받는 것이 관례이며, select 문에서 `case <-ctx.Done():`을 처리하여 취소에 반응해야 합니다.

---

### Q5. 채널과 뮤텍스 중 언제 어떤 것을 선택해야 하나요?

**모범 답안:**

Go의 격언 "Share memory by communicating"은 가능하면 채널을 선호하라는 의미이지만, 모든 상황에서 채널이 최선은 아닙니다.

채널이 적합한 경우는 다음과 같습니다. 데이터 소유권을 한 goroutine에서 다른 goroutine으로 명시적으로 전달할 때, 작업을 여러 워커에 분배할 때, 파이프라인 패턴으로 데이터를 변환할 때, 이벤트 알림이나 시그널링이 필요할 때 채널을 사용합니다.

뮤텍스가 적합한 경우는 다음과 같습니다. 여러 goroutine이 공유 데이터 구조(맵, 캐시)에 접근해야 할 때, 단순한 카운터나 플래그를 업데이트할 때, 구조체 내부의 상태를 보호할 때 뮤텍스가 더 직관적이고 효율적입니다.

실무적인 판단 기준을 말씀드리면, 데이터가 한 goroutine에서 다른 goroutine으로 "흐른다"면 채널, 여러 goroutine이 같은 데이터를 "공유한다"면 뮤텍스입니다. 또한 sync/atomic 패키지의 원자적 연산은 단순한 카운터나 플래그에 뮤텍스보다 더 가볍습니다.

읽기가 많고 쓰기가 적은 경우 sync.RWMutex를 고려할 수 있지만, RWMutex는 Mutex보다 오버헤드가 크므로 읽기가 압도적으로 많을 때만 이점이 있습니다.

---

### Q6. Goroutine 누수(leak)란 무엇이며 어떻게 방지하나요?

**모범 답안:**

Goroutine 누수는 goroutine이 영원히 블록되어 종료되지 않는 상황입니다. 가비지 컬렉터는 블록된 goroutine을 회수하지 않으므로 메모리가 계속 증가합니다. 장기 실행 서버에서는 심각한 문제를 일으킵니다.

주요 원인과 방지책은 다음과 같습니다.

첫째, 수신자 없는 채널 송신입니다. unbuffered 채널에 보낸 값을 아무도 받지 않으면 송신 goroutine이 영원히 블록됩니다. 방지책은 context 취소나 done 채널로 송신을 취소 가능하게 만드는 것입니다.

```go
// 누수 가능
go func() {
    ch <- result  // 아무도 안 받으면 영원히 블록
}()

// 방지
go func() {
    select {
    case ch <- result:
    case <-ctx.Done():
    }
}()
```

둘째, 닫히지 않는 채널에서의 수신입니다. for-range로 채널을 소비하는데 생산자가 채널을 닫지 않으면 영원히 대기합니다. 방지책은 생산자가 완료 시 반드시 채널을 닫는 것입니다.

셋째, WaitGroup 불일치입니다. Add한 수만큼 Done을 호출하지 않으면 Wait가 영원히 블록됩니다. 방지책은 defer wg.Done()을 사용하고, panic 발생 시에도 Done이 호출되도록 하는 것입니다.

테스트에서는 goleak 라이브러리를 사용해 goroutine 누수를 감지할 수 있습니다.

---

## 실무 체크리스트

### Goroutine 시작 시
- [ ] 종료 조건이 명확한가? (context, done 채널, 채널 close)
- [ ] panic 발생 시 recover 처리가 필요한가?
- [ ] WaitGroup 사용 시 Add()를 goroutine 시작 전에 호출했는가?
- [ ] defer wg.Done() 사용으로 완료 보장하는가?

### Channel 사용 시
- [ ] 닫아야 하는 채널은 송신 측에서만 닫는가?
- [ ] 닫힌 채널 수신 시 ok 값으로 확인하는가?
- [ ] nil 채널 할당이 의도적인가?
- [ ] 버퍼 크기가 적절한가? (0이면 동기화, 양수면 처리량)

### Context 사용 시
- [ ] cancel 함수를 defer로 호출하는가?
- [ ] 장기 실행 작업에서 ctx.Done()을 체크하는가?
- [ ] WithValue는 요청 범위 데이터에만 사용하는가?
- [ ] Background vs TODO를 올바르게 구분하는가?

### 동시성 안전성
- [ ] 공유 상태 접근이 뮤텍스로 보호되는가?
- [ ] defer mu.Unlock()으로 잠금 해제 보장하는가?
- [ ] 읽기 위주 접근에 RWMutex가 필요한가?
- [ ] -race 플래그로 테스트하는가?

---

## 참고 자료

- [Go Concurrency Patterns](https://go.dev/blog/pipelines)
- [Advanced Go Concurrency Patterns](https://go.dev/blog/io2013-talk-concurrency)
- [Share Memory By Communicating](https://go.dev/blog/codelab-share)
- [Go Memory Model](https://go.dev/ref/mem)
- [context 패키지 공식 문서](https://pkg.go.dev/context)
- [sync 패키지 공식 문서](https://pkg.go.dev/sync)
