# Stage 01: Go 기본 문법 학습 정리

## 1. 타입 시스템

### 커스텀 타입
```go
type Status string

var s1 Status = "active"
var s2 string = "active"

// s1 = s2  // 컴파일 에러! 다른 타입
s1 = Status(s2)  // 명시적 형변환 필요
```

**핵심**: Go는 강타입 언어. 같은 기반 타입이라도 다른 타입으로 취급.

---

## 2. Zero Value

모든 타입에 기본값이 정해져 있음 (커스텀 기본값 불가):

| 타입 | Zero Value |
|------|------------|
| `string` | `""` |
| `int` | `0` |
| `bool` | `false` |
| `[]T` (slice) | `nil` |
| `map[K]V` | `nil` |
| `*T` (pointer) | `nil` |
| `struct` | 모든 필드가 각자의 zero value |

**해결책**: 커스텀 기본값이 필요하면 생성자 함수 사용
```go
func NewConfig() *Config {
    return &Config{Token: "default"}
}
```

---

## 3. 포인터 vs 값

### 포인터를 사용하는 3가지 이유

| 이유 | 값 전달 | 포인터 전달 |
|------|---------|------------|
| 원본 수정 | 복사본만 수정 | 원본 수정 가능 |
| 메모리 효율 | 전체 복사 | 주소만 복사 (8바이트) |
| nil 체크 | 불가능 | `if ptr == nil` 가능 |

### T vs *T는 다른 타입!
```go
t1 := TokenCredentials{Token: "abc"}   // 타입: TokenCredentials
t2 := &TokenCredentials{Token: "abc"}  // 타입: *TokenCredentials

fmt.Printf("%T\n", t1)  // main.TokenCredentials
fmt.Printf("%T\n", t2)  // *main.TokenCredentials
```

### 메서드 Receiver
```go
// Pointer Receiver - 원본 수정 가능, 대부분 이 방식 사용
func (c *Config) Validate() error { ... }

// Value Receiver - 복사본으로 작업
func (c Config) String() string { ... }
```

**관례**: 한 타입의 모든 메서드는 같은 receiver 타입 사용 (일관성)

### 값 리시버 vs 포인터 리시버 동작 차이
```go
type Counter struct {
    count int
}

// 값 리시버 - 복사본만 수정 (원본 변경 안 됨!)
func (c Counter) IncrementWrong() {
    c.count++
}

// 포인터 리시버 - 원본 수정
func (c *Counter) Increment() {
    c.count++
}

// 실행 결과
counter := Counter{count: 0}
counter.IncrementWrong()
fmt.Println(counter.count)  // 0 (안 바뀜!)

counter.Increment()
fmt.Println(counter.count)  // 1 (바뀜!)
```

### 인터페이스와 리시버의 관계 (중요!)
```go
type Greeter interface {
    Greet() string
}

// 포인터 리시버로 정의
func (p *Person) Greet() string { return "Hello" }

// 규칙: 포인터 리시버 → *T만 인터페이스 구현
var g1 Greeter = &Person{}  // ✅ *Person은 Greeter
var g2 Greeter = Person{}   // ❌ Person은 Greeter 아님!
```

| 리시버 타입 | T가 인터페이스 구현? | *T가 인터페이스 구현? |
|------------|---------------------|----------------------|
| 값 `(c T)` | ✅ | ✅ |
| 포인터 `(c *T)` | ❌ | ✅ |

**이유**: 값 리터럴 `Person{}`은 주소가 없을 수 있어서 포인터 리시버 메서드 호출 불가

---

## 4. make와 nil

### make가 필요한 타입 (3가지만)
```go
slice := make([]int, 길이, 용량)
m := make(map[string]string)
ch := make(chan int)
```

### nil 상태에서 동작 차이

| 타입 | nil에서 쓰기 |
|------|-------------|
| `map` | panic! |
| `slice` | `append` 사용하면 OK |

```go
var m map[string]string
m["key"] = "value"  // panic!

var s []string
s = append(s, "hello")  // OK - append가 새로 할당해서 반환
```

---

## 5. append 동작

```go
var s []string
s2 := append(s, "hello")

fmt.Println(s)   // []     (원본 그대로)
fmt.Println(s2)  // [hello] (새로 만들어진 slice)
```

**핵심**: `append`는 새로운 slice를 반환. 반드시 `s = append(s, ...)` 형태로 받아야 함.

---

## 6. Sentinel Error

### 왜 사용하는가?
```go
// 매번 새로 생성 - 비교 불가
err1 := errors.New("token required")
err2 := errors.New("token required")
fmt.Println(err1 == err2)  // false!

// 미리 정의 - 비교 가능
var ErrEmptyToken = errors.New("token required")
// 여러 곳에서 ErrEmptyToken 반환
if err == ErrEmptyToken {  // 비교 가능!
    // 처리
}
```

---

## 7. 컴파일 타임 인터페이스 검증

```go
type Validatable interface {
    Validate() error
}

// 컴파일 타임에 인터페이스 구현 확인
var _ Validatable = (*AzureDevopsConfig)(nil)
```

**원리**:
- `(*AzureDevopsConfig)(nil)` - nil이지만 타입 정보는 있음
- 컴파일러가 `Validatable` 인터페이스 메서드 구현 여부 확인
- 구현 안 되어 있으면 컴파일 에러

---

## 실습 파일

- `config.go` - AzureDevOps 설정 구조체, Sentinel Error, 인터페이스 검증
- `main.go` - 테스트 코드

---

## 원본 프로젝트 참조

| 파일 | 학습 내용 |
|------|----------|
| `internal/provider/config.go` | Sentinel Error, 인터페이스 정의 |
| `internal/provider/github.go` | struct, Validate 메서드, Pointer Receiver |
