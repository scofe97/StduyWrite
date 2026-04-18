# 15. 제네릭 및 samber/lo 힌트

## 제네릭 기본 문법

### 함수 제네릭

```go
// 단일 타입 파라미터
func Identity[T any](value T) T {
    return value
}

// 사용
result := Identity[int](42)
result := Identity(42)  // 타입 추론

// 다중 타입 파라미터
func Pair[T, U any](first T, second U) (T, U) {
    return first, second
}

p := Pair[string, int]("age", 30)
```

### 타입 제약

```go
import "golang.org/x/exp/constraints"

// Ordered: <, >, <=, >= 가능
func Max[T constraints.Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// comparable: ==, != 가능
func Contains[T comparable](slice []T, item T) bool {
    for _, v := range slice {
        if v == item {
            return true
        }
    }
    return false
}

// 커스텀 제약
type Number interface {
    ~int | ~int64 | ~float64
}

func Sum[T Number](numbers []T) T {
    var sum T
    for _, n := range numbers {
        sum += n
    }
    return sum
}
```

## 제네릭 타입

### 제네릭 구조체

```go
type Stack[T any] struct {
    items []T
}

func NewStack[T any]() *Stack[T] {
    return &Stack[T]{
        items: make([]T, 0),
    }
}

func (s *Stack[T]) Push(item T) {
    s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() (T, bool) {
    if len(s.items) == 0 {
        var zero T
        return zero, false
    }
    index := len(s.items) - 1
    item := s.items[index]
    s.items = s.items[:index]
    return item, true
}
```

### 제네릭 맵

```go
type Cache[K comparable, V any] struct {
    data map[K]V
    mu   sync.RWMutex
}

func NewCache[K comparable, V any]() *Cache[K, V] {
    return &Cache[K, V]{
        data: make(map[K]V),
    }
}

func (c *Cache[K, V]) Set(key K, value V) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.data[key] = value
}

func (c *Cache[K, V]) Get(key K) (V, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    v, ok := c.data[key]
    return v, ok
}
```

## samber/lo 사용법

### Map

```go
import "github.com/samber/lo"

// 기본 변환
numbers := []int{1, 2, 3, 4, 5}
doubled := lo.Map(numbers, func(n int, index int) int {
    return n * 2
})
// [2, 4, 6, 8, 10]

// 타입 변환
intStrings := lo.Map(numbers, func(n int, _ int) string {
    return fmt.Sprintf("%d", n)
})
// ["1", "2", "3", "4", "5"]

// 구조체 변환
type User struct {
    ID   int
    Name string
}

users := []User{{1, "Alice"}, {2, "Bob"}}
names := lo.Map(users, func(u User, _ int) string {
    return u.Name
})
// ["Alice", "Bob"]
```

### Filter

```go
// 조건 필터링
numbers := []int{1, 2, 3, 4, 5, 6}
evens := lo.Filter(numbers, func(n int, _ int) bool {
    return n%2 == 0
})
// [2, 4, 6]

// 구조체 필터링
adults := lo.Filter(users, func(u User, _ int) bool {
    return u.Age >= 18
})
```

### Reduce

```go
// 합계
numbers := []int{1, 2, 3, 4, 5}
sum := lo.Reduce(numbers, func(acc int, n int, _ int) int {
    return acc + n
}, 0)
// 15

// 문자열 조인
words := []string{"hello", "world"}
sentence := lo.Reduce(words, func(acc string, word string, _ int) string {
    if acc == "" {
        return word
    }
    return acc + " " + word
}, "")
// "hello world"

// 맵 생성
users := []User{{1, "Alice"}, {2, "Bob"}}
userMap := lo.Reduce(users, func(acc map[int]string, u User, _ int) map[int]string {
    acc[u.ID] = u.Name
    return acc
}, make(map[int]string))
// map[1:"Alice" 2:"Bob"]
```

### Find

```go
// 첫 번째 매칭 항목
numbers := []int{1, 2, 3, 4, 5}
found, ok := lo.Find(numbers, func(n int) bool {
    return n > 3
})
// found=4, ok=true

// 사용자 검색
user, found := lo.Find(users, func(u User) bool {
    return u.Name == "Alice"
})
```

### Uniq

```go
// 중복 제거
numbers := []int{1, 2, 2, 3, 3, 3, 4}
unique := lo.Uniq(numbers)
// [1, 2, 3, 4]

// 조건부 중복 제거
users := []User{{1, "Alice"}, {2, "Alice"}, {3, "Bob"}}
uniqueByName := lo.UniqBy(users, func(u User) string {
    return u.Name
})
// [{1, "Alice"}, {3, "Bob"}]
```

### GroupBy

```go
// 그룹화
users := []User{
    {1, "Alice", 25},
    {2, "Bob", 25},
    {3, "Charlie", 30},
}

grouped := lo.GroupBy(users, func(u User) int {
    return u.Age
})
// map[25:[{Alice,25}, {Bob,25}] 30:[{Charlie,30}]]
```

### Chunk

```go
// 청크 분할
numbers := []int{1, 2, 3, 4, 5, 6, 7, 8}
chunks := lo.Chunk(numbers, 3)
// [[1,2,3], [4,5,6], [7,8]]
```

### Flatten

```go
// 중첩 배열 평탄화
nested := [][]int{{1, 2}, {3, 4}, {5}}
flat := lo.Flatten(nested)
// [1, 2, 3, 4, 5]
```

### Keys / Values

```go
// 맵에서 키 추출
m := map[string]int{"a": 1, "b": 2, "c": 3}
keys := lo.Keys(m)
// ["a", "b", "c"] (순서 보장 안됨)

// 맵에서 값 추출
values := lo.Values(m)
// [1, 2, 3] (순서 보장 안됨)
```

### Partition

```go
// 조건에 따라 분할
numbers := []int{1, 2, 3, 4, 5, 6}
evens, odds := lo.Partition(numbers, func(n int) bool {
    return n%2 == 0
})
// evens=[2,4,6], odds=[1,3,5]
```

## 복합 파이프라인

### 체이닝

```go
type Product struct {
    Name    string
    Price   float64
    InStock bool
}

products := []Product{
    {"A", 100, true},
    {"B", 200, false},
    {"C", 150, true},
    {"D", 50, true},
}

// 1. 재고 있는 것만
// 2. 가격에 세금 추가
// 3. 총합 계산
total := lo.Reduce(
    lo.Map(
        lo.Filter(products, func(p Product) bool {
            return p.InStock
        }),
        func(p Product, _ int) float64 {
            return p.Price * 1.1 // 10% 세금
        },
    ),
    func(acc float64, price float64, _ int) float64 {
        return acc + price
    },
    0.0,
)
```

### 가독성 개선

```go
// 단계별 변수 사용
inStock := lo.Filter(products, func(p Product) bool {
    return p.InStock
})

withTax := lo.Map(inStock, func(p Product, _ int) float64 {
    return p.Price * 1.1
})

total := lo.Reduce(withTax, func(acc float64, price float64, _ int) float64 {
    return acc + price
}, 0.0)
```

## 고급 제네릭 패턴

### Option 타입

```go
type Option[T any] struct {
    value *T
}

func Some[T any](value T) Option[T] {
    return Option[T]{value: &value}
}

func None[T any]() Option[T] {
    return Option[T]{value: nil}
}

func (o Option[T]) IsSome() bool {
    return o.value != nil
}

func (o Option[T]) Unwrap() T {
    if o.value == nil {
        panic("called Unwrap on None")
    }
    return *o.value
}

func (o Option[T]) UnwrapOr(defaultValue T) T {
    if o.value == nil {
        return defaultValue
    }
    return *o.value
}
```

### Result 타입

```go
type Result[T any] struct {
    value T
    err   error
}

func Ok[T any](value T) Result[T] {
    return Result[T]{value: value, err: nil}
}

func Err[T any](err error) Result[T] {
    var zero T
    return Result[T]{value: zero, err: err}
}

func (r Result[T]) IsOk() bool {
    return r.err == nil
}

func (r Result[T]) IsErr() bool {
    return r.err != nil
}

func (r Result[T]) Unwrap() (T, error) {
    return r.value, r.err
}
```

## 성능 고려사항

### 제네릭 vs 인터페이스

```go
// 제네릭: 타입별로 코드 생성 (성능 우수)
func GenericMax[T constraints.Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// 인터페이스: 동적 디스패치 (유연성 우수)
type Comparable interface {
    CompareTo(other Comparable) int
}

func InterfaceMax(a, b Comparable) Comparable {
    if a.CompareTo(b) > 0 {
        return a
    }
    return b
}
```

### 메모리 할당 최소화

```go
// Bad: 매번 새 슬라이스 할당
func AppendBad[T any](slice []T, item T) []T {
    result := make([]T, len(slice)+1)
    copy(result, slice)
    result[len(slice)] = item
    return result
}

// Good: 용량 미리 할당
func AppendGood[T any](slice []T, items ...T) []T {
    result := make([]T, 0, len(slice)+len(items))
    result = append(result, slice...)
    result = append(result, items...)
    return result
}
```

## 일반적인 실수

1. **제로값 처리**: 제네릭에서 `var zero T`로 제로값 반환
2. **타입 추론 실패**: 명시적 타입 파라미터 필요한 경우
3. **제약 누락**: `comparable` 없이 `==` 사용 시 컴파일 에러
4. **불필요한 제네릭**: 단순한 경우 인터페이스가 더 나을 수 있음
