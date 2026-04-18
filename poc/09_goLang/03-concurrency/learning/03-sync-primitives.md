# sync 패키지 학습

동시성 제어를 위한 sync 패키지의 프리미티브를 학습합니다.

---

## 학습 목표

- Mutex로 상호 배제
- RWMutex로 읽기/쓰기 분리
- Once로 단일 실행 보장
- Cond로 조건 대기

---

## 1. Mutex (상호 배제)

### 문제: Race Condition
```go
var counter int

// 여러 goroutine이 동시에 접근하면 결과가 예측 불가
func increment() {
    counter++  // 읽기 → 증가 → 쓰기가 원자적이지 않음
}
```

### 해결: sync.Mutex
```go
var (
    counter int
    mu      sync.Mutex
)

func increment() {
    mu.Lock()
    defer mu.Unlock()
    counter++
}
```

### 주의사항
- Lock 후 반드시 Unlock (defer 권장)
- 같은 goroutine에서 두 번 Lock하면 데드락
- 가능하면 채널 사용 우선 고려

---

## 2. RWMutex (읽기/쓰기 분리)

### 특징
- 여러 읽기는 동시 허용
- 쓰기는 단독 실행

```go
var (
    data map[string]string
    mu   sync.RWMutex
)

// 읽기 (여러 goroutine 동시 가능)
func get(key string) string {
    mu.RLock()
    defer mu.RUnlock()
    return data[key]
}

// 쓰기 (단독 실행)
func set(key, value string) {
    mu.Lock()
    defer mu.Unlock()
    data[key] = value
}
```

### 사용 시점
- 읽기가 쓰기보다 훨씬 많을 때
- 캐시, 설정 저장소 등

---

## 3. Once (단일 실행)

### 용도
초기화를 딱 한 번만 실행해야 할 때 사용합니다.

```go
var (
    instance *Database
    once     sync.Once
)

func GetDB() *Database {
    once.Do(func() {
        instance = &Database{}
        instance.Connect()
    })
    return instance
}
```

### 특징
- 여러 goroutine이 동시 호출해도 함수는 한 번만 실행
- 첫 실행이 완료될 때까지 다른 goroutine은 대기
- 싱글톤 패턴 구현에 적합

---

## 4. Cond (조건 변수)

### 용도
특정 조건이 만족될 때까지 대기합니다.

```go
var (
    queue []int
    cond  = sync.NewCond(&sync.Mutex{})
)

// 생산자
func produce(item int) {
    cond.L.Lock()
    queue = append(queue, item)
    cond.Signal()  // 대기 중인 하나를 깨움
    cond.L.Unlock()
}

// 소비자
func consume() int {
    cond.L.Lock()
    for len(queue) == 0 {
        cond.Wait()  // 조건 만족할 때까지 대기
    }
    item := queue[0]
    queue = queue[1:]
    cond.L.Unlock()
    return item
}
```

### 메서드
- `Wait()`: 조건 만족할 때까지 대기 (Lock 해제 후 재획득)
- `Signal()`: 대기 중인 goroutine 하나 깨움
- `Broadcast()`: 대기 중인 모든 goroutine 깨움

---

## 5. Pool (객체 재사용)

### 용도
자주 생성/삭제되는 객체를 재사용하여 GC 부담을 줄입니다.

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func process() {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)
    }()

    buf.WriteString("data")
    // 처리...
}
```

---

## 선택 가이드

| 상황 | 선택 |
|------|------|
| 데이터 전달 | 채널 (우선) |
| 공유 상태 보호 | Mutex |
| 읽기 >> 쓰기 | RWMutex |
| 단일 초기화 | Once |
| 조건 대기 | Cond 또는 채널 |
| 객체 재사용 | Pool |

---

## 과제

### 과제 1: Mutex
`practices/01-mutex/main.go`에서 카운터의 race condition을 해결하세요.

### 과제 2: RWMutex
`practices/02-rwmutex/main.go`에서 캐시를 동시성 안전하게 구현하세요.

### 과제 3: Once
`practices/03-once/main.go`에서 싱글톤 패턴을 구현하세요.

### 과제 4: Cond
`practices/04-cond/main.go`에서 생산자-소비자 패턴을 구현하세요.

---

## 참조 자료

- **Learning Go, 2nd Edition**: 12_Concurrency_in_Go.md - sync 섹션
- **Go by Example**: Mutexes
