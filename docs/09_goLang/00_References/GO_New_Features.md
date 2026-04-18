# Go 언어 신규 문법 및 기능 (2024-2026)

Go 1.21부터 1.24까지의 주요 변경사항을 정리한 문서입니다.

---

## Go 1.21 (2023.08)

### 1. min, max, clear 내장 함수

Go 1.21에서 세 가지 새로운 내장 함수가 추가되었습니다.

#### min, max 함수

**Before (Go 1.20 이전)**
```go
func min(a, b int) int {
    if a < b {
        return a
    }
    return b
}

func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}

// 사용
smallest := min(3, 5)
largest := max(3, 5)
```

**After (Go 1.21+)**
```go
// 내장 함수로 바로 사용
smallest := min(3, 5)           // 3
largest := max(3, 5)            // 5

// 여러 인자 지원
smallest := min(3, 5, 1, 9, 2)  // 1
largest := max(3, 5, 1, 9, 2)   // 9

// 다양한 타입 지원 (ordered 타입)
minFloat := min(3.14, 2.71)     // 2.71
minStr := min("apple", "banana") // "apple" (사전순)
```

**사용 시나리오**
- 두 값 비교 시 삼항 연산자나 if문 대체
- 여러 값 중 최소/최대값 찾기
- 배열/슬라이스 경계값 계산

**주의사항**
- `ordered` 제약을 만족하는 타입만 사용 가능 (정수, 부동소수점, 문자열)
- 최소 1개 이상의 인자 필요
- NaN이 포함된 부동소수점 비교 시 NaN 전파

#### clear 함수

**Before (Go 1.20 이전)**
```go
// 맵 비우기
for k := range m {
    delete(m, k)
}

// 슬라이스 비우기 (제로값으로)
for i := range s {
    s[i] = 0
}
```

**After (Go 1.21+)**
```go
// 맵 비우기
m := map[string]int{"a": 1, "b": 2}
clear(m)
fmt.Println(len(m)) // 0

// 슬라이스 비우기 (제로값으로 설정, 길이 유지)
s := []int{1, 2, 3, 4, 5}
clear(s)
fmt.Println(s)      // [0 0 0 0 0]
fmt.Println(len(s)) // 5
```

**주의사항**
- 슬라이스의 경우 길이는 유지되고 요소만 제로값으로 변경
- 맵의 경우 모든 키-값 쌍이 삭제됨

---

### 2. maps, slices 패키지 (표준 라이브러리)

제네릭을 활용한 유틸리티 패키지가 표준 라이브러리에 추가되었습니다.

#### slices 패키지

```go
import "slices"

// 정렬
nums := []int{3, 1, 4, 1, 5, 9, 2, 6}
slices.Sort(nums)
fmt.Println(nums) // [1 1 2 3 4 5 6 9]

// 커스텀 정렬
people := []Person{{Name: "Bob", Age: 30}, {Name: "Alice", Age: 25}}
slices.SortFunc(people, func(a, b Person) int {
    return cmp.Compare(a.Age, b.Age)
})

// 이진 검색
idx, found := slices.BinarySearch(nums, 4)

// 비교
slices.Equal([]int{1, 2, 3}, []int{1, 2, 3}) // true

// 역순
slices.Reverse(nums)

// 포함 여부
slices.Contains(nums, 5) // true

// 인덱스 찾기
slices.Index(nums, 5) // 첫 번째 5의 인덱스

// 복제
copied := slices.Clone(nums)

// 압축 (연속 중복 제거)
s := []int{1, 1, 2, 2, 2, 3}
s = slices.Compact(s) // [1, 2, 3]

// 삭제
s = slices.Delete(s, 1, 3) // 인덱스 1~2 삭제

// 삽입
s = slices.Insert(s, 1, 10, 20) // 인덱스 1에 10, 20 삽입
```

#### maps 패키지

```go
import "maps"

m1 := map[string]int{"a": 1, "b": 2}
m2 := map[string]int{"a": 1, "b": 2}

// 비교
maps.Equal(m1, m2) // true

// 복제
copied := maps.Clone(m1)

// 복사 (대상 맵에 추가)
dst := map[string]int{"c": 3}
maps.Copy(dst, m1) // dst = {"a": 1, "b": 2, "c": 3}

// 키 수집
keys := slices.Collect(maps.Keys(m1)) // ["a", "b"]

// 값 수집
values := slices.Collect(maps.Values(m1)) // [1, 2]

// 조건부 삭제
maps.DeleteFunc(m1, func(k string, v int) bool {
    return v > 1
})
```

**사용 시나리오**
- 슬라이스/맵 조작 시 보일러플레이트 코드 제거
- 정렬, 검색, 비교 등 일반적인 연산
- 함수형 스타일 데이터 처리

---

### 3. log/slog (구조화된 로깅)

기존 `log` 패키지를 대체할 수 있는 구조화된 로깅 패키지입니다.

**Before (기존 log 패키지)**
```go
import "log"

log.Printf("user %s logged in from %s", username, ip)
// 출력: 2024/01/15 10:30:45 user john logged in from 192.168.1.1
```

**After (slog 사용)**
```go
import "log/slog"

// 기본 사용
slog.Info("user logged in",
    "username", username,
    "ip", ip,
)
// 출력: 2024/01/15 10:30:45 INFO user logged in username=john ip=192.168.1.1

// 로그 레벨
slog.Debug("debug message")
slog.Info("info message")
slog.Warn("warning message")
slog.Error("error message", "err", err)

// JSON 핸들러 사용
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
logger.Info("user logged in", "username", "john")
// 출력: {"time":"2024-01-15T10:30:45Z","level":"INFO","msg":"user logged in","username":"john"}

// 구조화된 속성 그룹
slog.Info("request completed",
    slog.Group("request",
        slog.String("method", "GET"),
        slog.String("path", "/api/users"),
    ),
    slog.Group("response",
        slog.Int("status", 200),
        slog.Duration("latency", 150*time.Millisecond),
    ),
)

// 로거에 기본 속성 추가
logger := slog.Default().With("service", "api", "version", "1.0")
logger.Info("starting up")

// 로그 레벨 설정
opts := &slog.HandlerOptions{
    Level: slog.LevelDebug,
}
logger := slog.New(slog.NewTextHandler(os.Stdout, opts))

// 커스텀 레벨
const LevelTrace = slog.Level(-8)
slog.Log(context.Background(), LevelTrace, "trace message")
```

**사용 시나리오**
- 로그 집계 시스템 (ELK, Splunk 등)과 통합
- 마이크로서비스 환경에서 추적 가능한 로깅
- 운영 환경 모니터링

**주의사항**
- 키-값 쌍은 짝수 개여야 함
- 고성능이 필요한 경우 `LogAttrs` 메서드 사용 권장

---

### 4. cmp 패키지

비교 연산을 위한 새로운 패키지입니다.

```go
import "cmp"

// Compare 함수 - 비교 결과 반환 (-1, 0, 1)
cmp.Compare(1, 2)   // -1 (a < b)
cmp.Compare(2, 2)   // 0  (a == b)
cmp.Compare(3, 2)   // 1  (a > b)

// Less 함수
cmp.Less(1, 2)      // true
cmp.Less(2, 1)      // false

// Or 함수 - 첫 번째 제로값이 아닌 값 반환
cmp.Or("", "", "default")    // "default"
cmp.Or(0, 0, 42)             // 42
cmp.Or("first", "second")    // "first"

// slices.SortFunc와 함께 사용
type Person struct {
    Name string
    Age  int
}

people := []Person{
    {"Charlie", 30},
    {"Alice", 25},
    {"Bob", 30},
}

// 나이순, 같으면 이름순
slices.SortFunc(people, func(a, b Person) int {
    if c := cmp.Compare(a.Age, b.Age); c != 0 {
        return c
    }
    return cmp.Compare(a.Name, b.Name)
})
```

**사용 시나리오**
- 정렬 함수에서 비교 로직 작성
- 다중 필드 정렬
- 기본값 처리 (`cmp.Or`)

---

### 5. WASI 지원

WebAssembly System Interface 지원이 추가되었습니다.

```bash
# WASI 타겟으로 빌드
GOOS=wasip1 GOARCH=wasm go build -o main.wasm main.go

# wasmtime으로 실행
wasmtime main.wasm

# wazero로 실행
wazero run main.wasm
```

```go
// WASI 호환 코드
package main

import (
    "fmt"
    "os"
)

func main() {
    // 표준 입출력, 파일 시스템 접근 가능
    fmt.Println("Hello from WASI!")

    // 환경 변수 접근
    fmt.Println(os.Getenv("PATH"))

    // 파일 읽기
    data, _ := os.ReadFile("input.txt")
    fmt.Println(string(data))
}
```

**사용 시나리오**
- 서버리스 환경 (Fastly Compute, Cloudflare Workers)
- 플러그인 시스템
- 크로스 플랫폼 CLI 도구

---

## Go 1.22 (2024.02)

### 1. for range 정수 반복

정수에 대한 range 반복이 가능해졌습니다.

**Before (Go 1.21 이전)**
```go
// 0부터 n-1까지 반복
for i := 0; i < 10; i++ {
    fmt.Println(i)
}

// 또는
for i := range make([]struct{}, 10) {
    fmt.Println(i)
}
```

**After (Go 1.22+)**
```go
// 0부터 n-1까지 반복
for i := range 10 {
    fmt.Println(i) // 0, 1, 2, ..., 9
}

// 실용적인 예시
func repeat(s string, n int) string {
    var result strings.Builder
    for range n {
        result.WriteString(s)
    }
    return result.String()
}

// 인덱스가 필요 없는 경우
for range 5 {
    doSomething()
}
```

**주의사항**
- range의 대상이 정수일 때만 동작
- 음수는 0번 반복 (에러 아님)
- 런타임에 값이 결정되어도 동작

```go
n := -5
for range n {
    fmt.Println("실행 안됨")
}

count := getUserInput()
for range count {
    process()
}
```

---

### 2. for 루프 변수 스코프 변경

루프 변수 캡처 문제가 근본적으로 해결되었습니다.

**Before (Go 1.21 이전) - 버그 발생**
```go
var funcs []func()
for _, v := range []int{1, 2, 3} {
    funcs = append(funcs, func() {
        fmt.Println(v) // 모두 3 출력 (마지막 값)
    })
}
for _, f := range funcs {
    f() // 3, 3, 3
}

// 해결책: 로컬 변수 복사
for _, v := range []int{1, 2, 3} {
    v := v // 새도잉
    funcs = append(funcs, func() {
        fmt.Println(v)
    })
}
```

**After (Go 1.22+) - 자동 해결**
```go
var funcs []func()
for _, v := range []int{1, 2, 3} {
    funcs = append(funcs, func() {
        fmt.Println(v) // 각각 1, 2, 3 출력
    })
}
for _, f := range funcs {
    f() // 1, 2, 3
}

// 고루틴에서도 안전
for _, v := range []int{1, 2, 3} {
    go func() {
        fmt.Println(v) // 각각 올바른 값 출력
    }()
}
```

**영향받는 패턴**
```go
// 채널과 함께 사용
ch := make(chan int, 3)
for i := range 3 {
    go func() {
        ch <- i // Go 1.22+에서는 올바르게 동작
    }()
}

// 테스트 케이스
tests := []struct{name string; input int}{...}
for _, tc := range tests {
    t.Run(tc.name, func(t *testing.T) {
        // tc가 올바르게 캡처됨
    })
}
```

**주의사항**
- Go 1.22 미만 버전과 호환성 필요 시 여전히 로컬 복사 권장
- `go.mod`의 go 버전이 1.22 이상이어야 새 동작 적용

---

### 3. math/rand/v2

개선된 난수 생성 패키지입니다.

**Before (math/rand)**
```go
import "math/rand"

// 시드 설정 필요
rand.Seed(time.Now().UnixNano())

n := rand.Intn(100)
f := rand.Float64()
```

**After (math/rand/v2)**
```go
import "math/rand/v2"

// 시드 설정 불필요 (자동 시드)
n := rand.IntN(100)        // 0 ~ 99
f := rand.Float64()        // 0.0 ~ 1.0

// 새로운 함수들
rand.N(100)                // IntN과 동일, 제네릭
rand.N(time.Hour)          // Duration도 지원!

// 범위 지정 난수 (Uint64N 등)
rand.Uint64N(1000)
rand.Uint32N(1000)

// 새로운 알고리즘 사용 가능
// PCG (기본값, 빠름)
// ChaCha8 (암호학적으로 안전)
src := rand.NewChaCha8([32]byte{...})
rng := rand.New(src)

// 셔플
s := []int{1, 2, 3, 4, 5}
rand.Shuffle(len(s), func(i, j int) {
    s[i], s[j] = s[j], s[i]
})

// 또는 slices 패키지와 함께
// (Go 1.23의 slices.Shuffle 사용)
```

**주요 변경사항**
| math/rand | math/rand/v2 | 설명 |
|-----------|--------------|------|
| `Intn(n)` | `IntN(n)` | 이름 변경 |
| `Int31n(n)` | `Int32N(n)` | 이름 변경 |
| `Int63n(n)` | `Int64N(n)` | 이름 변경 |
| `Seed()` | 자동 | 시드 자동 초기화 |
| - | `N[T](n)` | 제네릭 버전 추가 |

**사용 시나리오**
- 게임 로직
- 테스트 데이터 생성
- 로드 밸런싱

---

### 4. net/http 라우팅 개선

서드파티 라우터 없이도 강력한 라우팅이 가능해졌습니다.

**Before (Go 1.21 이전)**
```go
// 기본 라우터의 한계
http.HandleFunc("/users", usersHandler)
// /users/123 처리 불가, 메서드 구분 불가

// Gorilla Mux 등 서드파티 필요
r := mux.NewRouter()
r.HandleFunc("/users/{id}", getUser).Methods("GET")
```

**After (Go 1.22+)**
```go
mux := http.NewServeMux()

// 메서드 지정
mux.HandleFunc("GET /users", listUsers)
mux.HandleFunc("POST /users", createUser)

// 경로 매개변수
mux.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    fmt.Fprintf(w, "User ID: %s", id)
})

// 와일드카드 (나머지 경로 캡처)
mux.HandleFunc("GET /files/{path...}", func(w http.ResponseWriter, r *http.Request) {
    path := r.PathValue("path")
    // /files/a/b/c -> path = "a/b/c"
})

// 정확한 경로 매칭 (슬래시로 끝남)
mux.HandleFunc("GET /api/", apiHandler)    // /api/로 시작하는 모든 경로
mux.HandleFunc("GET /api/{$}", exactAPI)   // 정확히 /api/만 매칭

// 우선순위: 더 구체적인 패턴이 우선
mux.HandleFunc("GET /users/me", getCurrentUser)     // 우선
mux.HandleFunc("GET /users/{id}", getUser)          // 그 다음

// 호스트 기반 라우팅
mux.HandleFunc("GET api.example.com/", apiHandler)
mux.HandleFunc("GET www.example.com/", webHandler)
```

**실용적인 예시**
```go
func main() {
    mux := http.NewServeMux()

    // RESTful API
    mux.HandleFunc("GET /api/v1/posts", listPosts)
    mux.HandleFunc("POST /api/v1/posts", createPost)
    mux.HandleFunc("GET /api/v1/posts/{id}", getPost)
    mux.HandleFunc("PUT /api/v1/posts/{id}", updatePost)
    mux.HandleFunc("DELETE /api/v1/posts/{id}", deletePost)

    // 중첩 경로
    mux.HandleFunc("GET /api/v1/posts/{postID}/comments", listComments)
    mux.HandleFunc("POST /api/v1/posts/{postID}/comments", createComment)

    http.ListenAndServe(":8080", mux)
}

func getPost(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")

    // 유효성 검사
    postID, err := strconv.Atoi(id)
    if err != nil {
        http.Error(w, "Invalid ID", http.StatusBadRequest)
        return
    }

    // ... 처리 로직
}
```

**주의사항**
- 기존 패턴과 호환됨 (메서드 없는 패턴도 동작)
- 패턴 충돌 시 panic 발생 (서버 시작 시)
- `PathValue`는 해당 요청에서만 유효

---

### 5. slices.Concat

여러 슬라이스를 연결하는 함수가 추가되었습니다.

**Before (Go 1.21 이전)**
```go
// append를 여러 번 호출
result := append(s1, s2...)
result = append(result, s3...)

// 또는 용량 계산 후 복사
total := len(s1) + len(s2) + len(s3)
result := make([]int, 0, total)
result = append(result, s1...)
result = append(result, s2...)
result = append(result, s3...)
```

**After (Go 1.22+)**
```go
import "slices"

s1 := []int{1, 2, 3}
s2 := []int{4, 5}
s3 := []int{6, 7, 8, 9}

// 간단하게 연결
result := slices.Concat(s1, s2, s3)
// [1 2 3 4 5 6 7 8 9]

// nil 슬라이스도 안전하게 처리
var empty []int
result := slices.Concat(s1, empty, s2) // [1 2 3 4 5]

// 단일 슬라이스 복제에도 사용 가능
clone := slices.Concat(original)
```

**내부 최적화**
- 총 길이를 미리 계산하여 단일 할당
- `append`의 여러 번 호출보다 효율적

---

## Go 1.23 (2024.08)

### 1. range over func (이터레이터)

함수를 range로 반복할 수 있는 기능입니다.

**이터레이터 타입**
```go
// 값 없이 반복
type Seq0 func(yield func() bool)

// 단일 값 반복
type Seq[V any] func(yield func(V) bool)

// 키-값 쌍 반복
type Seq2[K, V any] func(yield func(K, V) bool)
```

**기본 사용법**
```go
// 이터레이터 정의
func Backward[E any](s []E) iter.Seq[E] {
    return func(yield func(E) bool) {
        for i := len(s) - 1; i >= 0; i-- {
            if !yield(s[i]) {
                return
            }
        }
    }
}

// 사용
s := []string{"a", "b", "c"}
for v := range Backward(s) {
    fmt.Println(v) // c, b, a
}
```

**표준 라이브러리 이터레이터**
```go
import (
    "maps"
    "slices"
)

// 맵 키/값 순회
m := map[string]int{"a": 1, "b": 2, "c": 3}

for k := range maps.Keys(m) {
    fmt.Println(k)
}

for v := range maps.Values(m) {
    fmt.Println(v)
}

// 슬라이스 역순 순회
s := []int{1, 2, 3, 4, 5}
for i, v := range slices.Backward(s) {
    fmt.Printf("%d: %d\n", i, v) // 4:5, 3:4, 2:3, 1:2, 0:1
}

// 정렬된 순서로 맵 순회
for k, v := range maps.All(m) {
    fmt.Printf("%s: %d\n", k, v)
}

// 슬라이스를 청크로 나누기
for chunk := range slices.Chunk(s, 2) {
    fmt.Println(chunk) // [1,2], [3,4], [5]
}
```

**커스텀 이터레이터 예시**
```go
// 파일의 각 줄을 순회
func Lines(filename string) iter.Seq2[int, string] {
    return func(yield func(int, string) bool) {
        f, err := os.Open(filename)
        if err != nil {
            return
        }
        defer f.Close()

        scanner := bufio.NewScanner(f)
        lineNum := 1
        for scanner.Scan() {
            if !yield(lineNum, scanner.Text()) {
                return
            }
            lineNum++
        }
    }
}

// 사용
for num, line := range Lines("data.txt") {
    fmt.Printf("%d: %s\n", num, line)
}

// 피보나치 수열
func Fibonacci(max int) iter.Seq[int] {
    return func(yield func(int) bool) {
        a, b := 0, 1
        for a <= max {
            if !yield(a) {
                return
            }
            a, b = b, a+b
        }
    }
}

for n := range Fibonacci(100) {
    fmt.Println(n) // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
}

// 트리 순회
type Node struct {
    Value int
    Left  *Node
    Right *Node
}

func (n *Node) InOrder() iter.Seq[int] {
    return func(yield func(int) bool) {
        var traverse func(*Node) bool
        traverse = func(node *Node) bool {
            if node == nil {
                return true
            }
            return traverse(node.Left) &&
                   yield(node.Value) &&
                   traverse(node.Right)
        }
        traverse(n)
    }
}
```

**이터레이터 조합**
```go
// 필터링
func Filter[V any](seq iter.Seq[V], pred func(V) bool) iter.Seq[V] {
    return func(yield func(V) bool) {
        for v := range seq {
            if pred(v) {
                if !yield(v) {
                    return
                }
            }
        }
    }
}

// 변환
func Map[V, U any](seq iter.Seq[V], f func(V) U) iter.Seq[U] {
    return func(yield func(U) bool) {
        for v := range seq {
            if !yield(f(v)) {
                return
            }
        }
    }
}

// 사용
nums := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

// 짝수만 필터링하고 제곱
for n := range Map(Filter(slices.Values(nums),
    func(n int) bool { return n%2 == 0 }),
    func(n int) int { return n * n }) {
    fmt.Println(n) // 4, 16, 36, 64, 100
}
```

**이터레이터를 슬라이스로 수집**
```go
// slices.Collect 사용
result := slices.Collect(Fibonacci(50))
fmt.Println(result) // [0 1 1 2 3 5 8 13 21 34]

// maps.Collect 사용
keys := slices.Collect(maps.Keys(m))
```

**주의사항**
- `yield`가 `false`를 반환하면 즉시 종료해야 함 (break 처리)
- 이터레이터 내에서 panic 발생 시 적절한 cleanup 필요
- 한 번만 순회 가능 (재사용 불가, 매번 새로 생성)

---

### 2. unique 패키지 (인터닝)

문자열 및 값의 인터닝을 위한 새 패키지입니다.

**개념**
- 동일한 값에 대해 단일 인스턴스만 유지
- 메모리 절약 및 빠른 비교 (포인터 비교)

```go
import "unique"

// Handle 생성
h1 := unique.Make("hello")
h2 := unique.Make("hello")
h3 := unique.Make("world")

// 포인터 비교로 동등성 확인 (빠름)
fmt.Println(h1 == h2) // true
fmt.Println(h1 == h3) // false

// 원본 값 가져오기
fmt.Println(h1.Value()) // "hello"

// 비교 가능한 모든 타입 지원
type Point struct {
    X, Y int
}
p1 := unique.Make(Point{1, 2})
p2 := unique.Make(Point{1, 2})
fmt.Println(p1 == p2) // true
```

**사용 시나리오**
```go
// 대량의 중복 문자열 처리
type User struct {
    ID      int
    Country unique.Handle[string]  // 국가명은 중복이 많음
    City    unique.Handle[string]
}

// 100만 명의 사용자 중 대부분이 같은 국가
users := make([]User, 1000000)
for i := range users {
    users[i] = User{
        ID:      i,
        Country: unique.Make(getCountry()), // 인터닝
        City:    unique.Make(getCity()),
    }
}

// 빠른 비교
func sameCountry(a, b User) bool {
    return a.Country == b.Country // 포인터 비교
}
```

**주의사항**
- Handle은 비교 가능하지만 직접 출력 불가 (Value() 사용)
- GC가 자동으로 사용되지 않는 값 정리
- 모든 비교 가능(comparable) 타입 지원

---

### 3. Timer/Ticker 변경

Go 1.23에서 타이머 동작이 개선되었습니다.

**변경사항**
- `Stop()`이 채널을 비움 (드레인 불필요)
- `Reset()`이 채널을 비움
- GC가 더 이상 사용되지 않는 타이머를 자동 정리

**Before (Go 1.22 이전)**
```go
timer := time.NewTimer(5 * time.Second)

// Stop 후 채널 드레인 필요
if !timer.Stop() {
    select {
    case <-timer.C:
    default:
    }
}

// Reset 전에도 드레인 필요
if !timer.Stop() {
    select {
    case <-timer.C:
    default:
    }
}
timer.Reset(10 * time.Second)
```

**After (Go 1.23+)**
```go
timer := time.NewTimer(5 * time.Second)

// Stop이 자동으로 채널을 비움
timer.Stop()

// Reset도 자동으로 채널을 비움
timer.Reset(10 * time.Second)

// 더 이상 드레인 패턴 불필요!
```

**Ticker도 동일**
```go
ticker := time.NewTicker(1 * time.Second)

// 안전하게 Stop
ticker.Stop()

// 안전하게 Reset
ticker.Reset(2 * time.Second)
```

**GODEBUG로 이전 동작 유지**
```bash
GODEBUG=asynctimerchan=1 go run main.go
```

**주의사항**
- 새 동작은 `go.mod`의 go 버전이 1.23+ 일 때만 적용
- 기존 코드의 드레인 패턴은 해가 되지 않음 (호환성)
- 멀티 고루틴에서 타이머 공유 시 주의 필요

---

### 4. 기타 변경사항

#### structs 패키지 (Go 1.23)
```go
import "structs"

// 레이아웃 최적화 힌트
type Data struct {
    _ structs.HostLayout // 호스트 메모리 레이아웃 사용
    A int32
    B int64
    C int32
}
```

#### slices 패키지 추가 함수
```go
// Repeat - 슬라이스 반복
s := slices.Repeat([]int{1, 2}, 3)
// [1, 2, 1, 2, 1, 2]

// Chunk - 청크로 분할 (이터레이터)
for chunk := range slices.Chunk([]int{1,2,3,4,5}, 2) {
    fmt.Println(chunk)
}
// [1 2]
// [3 4]
// [5]

// Sorted - 이터레이터를 정렬된 슬라이스로
sorted := slices.Sorted(maps.Keys(m))

// SortedFunc - 커스텀 정렬
sorted := slices.SortedFunc(maps.Keys(m), strings.Compare)

// SortedStableFunc - 안정 정렬
sorted := slices.SortedStableFunc(seq, cmp)
```

#### os.CopyFS (Go 1.23)
```go
import (
    "embed"
    "os"
)

//go:embed templates/*
var templates embed.FS

func main() {
    // 임베디드 파일 시스템을 실제 디렉토리로 복사
    err := os.CopyFS("./output", templates)
    if err != nil {
        log.Fatal(err)
    }
}
```

---

## Go 1.24 (2025.02) - 예정된 변경사항

Go 1.24는 2025년 2월 출시 예정이며, 다음 기능들이 포함될 예정입니다.

### 1. 제네릭 타입 별칭 (Generic Type Aliases)

```go
// 타입 별칭에 타입 매개변수 사용 가능
type Set[T comparable] = map[T]struct{}

// 사용
var s Set[string]
s = make(Set[string])
s["hello"] = struct{}{}

// 기존 타입 정의와 차이
type MySet[T comparable] map[T]struct{}  // 새 타입
type Set[T comparable] = map[T]struct{}  // 별칭 (= 사용)
```

### 2. 약한 참조 (Weak Pointers)

```go
import "weak"

// 약한 포인터 생성
p := new(int)
*p = 42
w := weak.Make(p)

// 값 접근 (GC되었으면 nil)
if strong := w.Value(); strong != nil {
    fmt.Println(*strong)
}

// 캐시 구현 예시
type Cache[K comparable, V any] struct {
    mu    sync.Mutex
    items map[K]weak.Pointer[V]
}

func (c *Cache[K, V]) Get(key K) *V {
    c.mu.Lock()
    defer c.mu.Unlock()

    if wp, ok := c.items[key]; ok {
        return wp.Value() // GC되었으면 nil
    }
    return nil
}
```

### 3. 파이널라이저 개선

```go
import "runtime"

// 새로운 AddCleanup 함수
type Resource struct {
    handle uintptr
}

func NewResource() *Resource {
    r := &Resource{handle: allocate()}
    runtime.AddCleanup(r, func(handle uintptr) {
        release(handle)
    }, r.handle)
    return r
}
```

### 4. testing/synctest 패키지

시간 관련 테스트를 위한 새 패키지입니다.

```go
import "testing/synctest"

func TestTimeout(t *testing.T) {
    synctest.Run(func() {
        timer := time.NewTimer(5 * time.Second)

        // 시간을 즉시 앞으로 이동
        synctest.Wait()  // 모든 고루틴이 블록될 때까지 대기

        select {
        case <-timer.C:
            // 실제로 5초 기다리지 않고 타이머 완료
        default:
            t.Fatal("timer should have fired")
        }
    })
}
```

### 5. 디렉토리 제한 빌드

```bash
# 특정 디렉토리 외부 파일 참조 금지
go build -godebug=dirmod=1 ./...
```

### 6. omitzero 태그 (encoding/json)

```go
type Config struct {
    Name    string `json:"name"`
    Count   int    `json:"count,omitzero"`   // 0이면 생략
    Enabled bool   `json:"enabled,omitzero"` // false면 생략
}

// 기존 omitempty와 차이
// omitempty: 제로값이면 생략 (문자열 "", 숫자 0, bool false 등)
// omitzero: 타입의 IsZero() 메서드로 판단

type Time struct {
    time.Time
}

func (t Time) IsZero() bool {
    return t.Time.IsZero()
}

type Event struct {
    Time Time `json:"time,omitzero"` // IsZero()가 true면 생략
}
```

### 7. crypto 패키지 개선

```go
// FIPS 140-3 모드 지원
import "crypto/fips"

func init() {
    fips.Enable() // FIPS 모드 활성화
}

// 새로운 ML-KEM (포스트 양자 암호)
import "crypto/mlkem"

// 키 생성
pub, priv := mlkem.GenerateKey768()

// 캡슐화 (송신자)
ciphertext, sharedSecret := mlkem.Encapsulate768(pub)

// 복호화 (수신자)
sharedSecret := mlkem.Decapsulate768(priv, ciphertext)
```

**주의사항**
- Go 1.24는 아직 출시되지 않았으며, 기능이 변경될 수 있음
- 베타/RC 버전으로 미리 테스트 가능: `go install golang.org/dl/go1.24beta1@latest`

---

## 마이그레이션 가이드

### Go 1.21로 업그레이드
```go
// go.mod
go 1.21

// 변경 사항
// 1. 커스텀 min/max 함수 제거 (내장 함수 사용)
// 2. slices, maps 패키지 활용
// 3. log -> log/slog 마이그레이션 고려
```

### Go 1.22로 업그레이드
```go
// go.mod
go 1.22

// 변경 사항
// 1. 루프 변수 새도잉 코드 제거 가능
// 2. math/rand -> math/rand/v2 마이그레이션
// 3. 서드파티 라우터 대신 표준 라이브러리 사용 고려
```

### Go 1.23으로 업그레이드
```go
// go.mod
go 1.23

// 변경 사항
// 1. 이터레이터 패턴 도입 검토
// 2. 타이머 드레인 코드 제거 가능
// 3. unique 패키지로 메모리 최적화
```

---

## 참고 자료

- [Go 1.21 Release Notes](https://go.dev/doc/go1.21)
- [Go 1.22 Release Notes](https://go.dev/doc/go1.22)
- [Go 1.23 Release Notes](https://go.dev/doc/go1.23)
- [Go 1.24 Release Notes](https://go.dev/doc/go1.24) (예정)
- [Go Wiki: Range Over Function Types](https://go.dev/wiki/RangefuncExperiment)
- [The Go Blog](https://go.dev/blog/)
