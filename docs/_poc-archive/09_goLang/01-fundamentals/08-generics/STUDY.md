# 11. 제네릭 (Generics)

## 학습 목표
Go 1.18에서 도입된 제네릭의 개념과 활용법을 이해한다.

---

## 핵심 개념

### 1. 타입 파라미터 (Type Parameters)
- `[T any]`: 모든 타입 허용
- `[T comparable]`: 비교 가능한 타입
- `[T constraints.Ordered]`: 정렬 가능한 타입

### 2. 타입 제약 (Type Constraints)
- 인터페이스로 제약 정의
- `~int`: int 기반 타입 포함
- `int | string`: 유니온 타입

### 3. 제네릭 함수
```go
func Min[T constraints.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}
```

### 4. 제네릭 구조체
```go
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T) {
    s.items = append(s.items, item)
}
```

### 5. 타입 추론
- 함수 호출 시 타입 생략 가능
- `Min(1, 2)` → `Min[int](1, 2)`

---

## 실무 패턴

### 패턴 1: 제네릭 슬라이스 함수
```go
func Filter[T any](slice []T, f func(T) bool) []T {
    result := make([]T, 0)
    for _, v := range slice {
        if f(v) {
            result = append(result, v)
        }
    }
    return result
}
```

### 패턴 2: 제네릭 맵 함수
```go
func Map[T, U any](slice []T, f func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = f(v)
    }
    return result
}
```

### 패턴 3: 커스텀 제약
```go
type Number interface {
    ~int | ~int64 | ~float64
}

func Sum[T Number](nums []T) T {
    var sum T
    for _, n := range nums {
        sum += n
    }
    return sum
}
```

---

## 소크라테스 질문

1. Go에 제네릭이 왜 늦게(1.18) 도입되었나요? 그 전에는 어떻게 해결했나요?

2. `any`와 `interface{}`의 차이점은 무엇인가요?

3. 제약에서 `int`와 `~int`의 차이점은 무엇인가요? 왜 `~`가 필요한가요?

4. 제네릭을 사용하면 안 되는 상황은 언제인가요? 과도한 사용의 문제점은?

5. `comparable` 제약의 의미와 필요성은 무엇인가요?

---

## 실습 과제

### 과제 1: 제네릭 스택
Push, Pop, Peek, IsEmpty 메서드를 가진 제네릭 스택을 구현하세요.

### 과제 2: 제네릭 Reduce
슬라이스를 단일 값으로 줄이는 `Reduce` 함수를 작성하세요.
```go
func Reduce[T, U any](slice []T, initial U, f func(U, T) U) U
```

---

## 참고 자료
- [Go Tour - Generics](https://go.dev/tour/generics)
- [Go Blog - Intro to Generics](https://go.dev/blog/intro-generics)
- [Go Package - constraints](https://pkg.go.dev/golang.org/x/exp/constraints)
