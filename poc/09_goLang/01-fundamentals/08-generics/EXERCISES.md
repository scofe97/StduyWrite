# 15. 제네릭 및 samber/lo 연습 문제

## Exercise 1: 제네릭 유틸리티 함수

**목표**: 범용 유틸리티 함수 구현

**요구사항**:
```go
// Min 두 값 중 작은 값 반환
func Min[T constraints.Ordered](a, b T) T

// Max 두 값 중 큰 값 반환
func Max[T constraints.Ordered](a, b T) T

// Clamp 값을 범위 내로 제한
func Clamp[T constraints.Ordered](value, min, max T) T

// Contains 슬라이스에 요소가 있는지 확인
func Contains[T comparable](slice []T, item T) bool

// Keys 맵의 모든 키 추출
func Keys[K comparable, V any](m map[K]V) []K

// Values 맵의 모든 값 추출
func Values[K comparable, V any](m map[K]V) []V
```

## Exercise 2: 제네릭 자료구조 - Stack

**목표**: 제네릭 기반 스택 구현

**요구사항**:
```go
type Stack[T any] struct {
    items []T
}

func NewStack[T any]() *Stack[T]
func (s *Stack[T]) Push(item T)
func (s *Stack[T]) Pop() (T, bool)
func (s *Stack[T]) Peek() (T, bool)
func (s *Stack[T]) IsEmpty() bool
func (s *Stack[T]) Size() int
```

**테스트**:
```go
stack := NewStack[int]()
stack.Push(1)
stack.Push(2)
stack.Push(3)
val, _ := stack.Pop() // 3
```

## Exercise 3: 제네릭 자료구조 - Set

**목표**: 중복을 허용하지 않는 Set 구현

**요구사항**:
```go
type Set[T comparable] struct {
    items map[T]struct{}
}

func NewSet[T comparable]() *Set[T]
func (s *Set[T]) Add(item T)
func (s *Set[T]) Remove(item T)
func (s *Set[T]) Contains(item T) bool
func (s *Set[T]) Size() int
func (s *Set[T]) ToSlice() []T
func (s *Set[T]) Union(other *Set[T]) *Set[T]
func (s *Set[T]) Intersection(other *Set[T]) *Set[T]
```

## Exercise 4: samber/lo Map

**목표**: Map을 사용한 데이터 변환

**요구사항**:
```go
// 숫자 슬라이스를 제곱
numbers := []int{1, 2, 3, 4, 5}
squared := lo.Map(numbers, func(n int, _ int) int {
    return n * n
})
// [1, 4, 9, 16, 25]

// 사용자 구조체에서 이름만 추출
users := []User{{Name: "Alice"}, {Name: "Bob"}}
names := lo.Map(users, func(u User, _ int) string {
    return u.Name
})
// ["Alice", "Bob"]
```

## Exercise 5: samber/lo Filter

**목표**: Filter를 사용한 조건부 필터링

**요구사항**:
```go
// 짝수만 필터링
numbers := []int{1, 2, 3, 4, 5, 6}
evens := lo.Filter(numbers, func(n int, _ int) bool {
    return n%2 == 0
})
// [2, 4, 6]

// 성인만 필터링
users := []User{
    {Name: "Alice", Age: 25},
    {Name: "Bob", Age: 17},
}
adults := lo.Filter(users, func(u User, _ int) bool {
    return u.Age >= 18
})
```

## Exercise 6: samber/lo Reduce

**목표**: Reduce를 사용한 집계

**요구사항**:
```go
// 합계 계산
numbers := []int{1, 2, 3, 4, 5}
sum := lo.Reduce(numbers, func(acc int, n int, _ int) int {
    return acc + n
}, 0)
// 15

// 최댓값 찾기
max := lo.Reduce(numbers, func(acc int, n int, _ int) int {
    if n > acc {
        return n
    }
    return acc
}, numbers[0])
```

## Exercise 7: 복합 파이프라인

**목표**: Map, Filter, Reduce 조합

**요구사항**:
```go
// 제품 목록에서:
// 1. 재고가 있는 제품만 필터링
// 2. 가격에 세금 추가 (10%)
// 3. 총 금액 계산

type Product struct {
    Name     string
    Price    float64
    InStock  bool
}

products := []Product{
    {Name: "A", Price: 100, InStock: true},
    {Name: "B", Price: 200, InStock: false},
    {Name: "C", Price: 150, InStock: true},
}

// 파이프라인 구현
```

## Exercise 8: samber/lo 유틸리티

**목표**: 다양한 lo 함수 활용

**요구사항**:
```go
// Uniq: 중복 제거
numbers := []int{1, 2, 2, 3, 3, 3, 4}
unique := lo.Uniq(numbers)

// GroupBy: 그룹화
users := []User{
    {Name: "Alice", Age: 25},
    {Name: "Bob", Age: 25},
    {Name: "Charlie", Age: 30},
}
grouped := lo.GroupBy(users, func(u User) int {
    return u.Age
})

// Chunk: 청크 분할
numbers := []int{1, 2, 3, 4, 5, 6, 7}
chunks := lo.Chunk(numbers, 3)
// [[1,2,3], [4,5,6], [7]]

// Find: 조건 검색
user, found := lo.Find(users, func(u User) bool {
    return u.Name == "Alice"
})
```

## Exercise 9: 커스텀 타입 제약

**목표**: 인터페이스 기반 타입 제약 정의

**요구사항**:
```go
// Number 제약 정의
type Number interface {
    ~int | ~int64 | ~float64
}

// Number 타입만 받는 함수
func Sum[T Number](numbers []T) T {
    var sum T
    for _, n := range numbers {
        sum += n
    }
    return sum
}

// Stringer 제약
type Stringer interface {
    String() string
}

func PrintAll[T Stringer](items []T) {
    for _, item := range items {
        fmt.Println(item.String())
    }
}
```

## Exercise 10: 제네릭 Cache

**목표**: 제네릭 기반 캐시 구현

**요구사항**:
```go
type Cache[K comparable, V any] struct {
    data map[K]V
    mu   sync.RWMutex
}

func NewCache[K comparable, V any]() *Cache[K, V]
func (c *Cache[K, V]) Set(key K, value V)
func (c *Cache[K, V]) Get(key K) (V, bool)
func (c *Cache[K, V]) Delete(key K)
func (c *Cache[K, V]) Has(key K) bool
func (c *Cache[K, V]) Clear()
```

## 보너스 Exercise: 제네릭 Result 타입

**목표**: Rust 스타일 Result<T, E> 구현

**요구사항**:
```go
type Result[T any] struct {
    value T
    err   error
}

func Ok[T any](value T) Result[T]
func Err[T any](err error) Result[T]
func (r Result[T]) IsOk() bool
func (r Result[T]) IsErr() bool
func (r Result[T]) Unwrap() T
func (r Result[T]) UnwrapOr(defaultValue T) T
```

## 성공 기준

- [ ] 제네릭 함수가 다양한 타입에서 동작
- [ ] 제네릭 자료구조가 타입 안전
- [ ] samber/lo를 효과적으로 활용
- [ ] 코드 중복이 감소
- [ ] 타입 제약을 적절히 사용

## 추가 과제

1. 제네릭 Iterator 패턴 구현
2. 제네릭 Builder 패턴
3. Option<T> 모나드 구현
4. Either<L, R> 타입 구현
