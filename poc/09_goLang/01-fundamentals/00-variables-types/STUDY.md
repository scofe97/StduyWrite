# 00. 변수와 타입 (Variables & Types)

## 학습 목표
Go의 변수 선언 방식과 기본 데이터 타입을 이해한다.

---

## 핵심 개념

### 1. 변수 선언 방식
- `var` 키워드: 명시적 타입 지정 가능
- `:=` 단축 선언: 타입 추론, 함수 내부에서만 사용
- 제로 값(Zero Value): 초기화하지 않은 변수의 기본값

### 2. 기본 데이터 타입
- **정수**: `int`, `int8`, `int16`, `int32`, `int64`, `uint`
- **실수**: `float32`, `float64`
- **문자열**: `string` (불변, UTF-8)
- **불리언**: `bool`
- **바이트/룬**: `byte` (uint8), `rune` (int32)

### 3. 상수와 iota
- `const` 키워드로 선언
- `iota`: 연속적인 정수 상수 생성
- 타입 없는 상수 (untyped constant)

### 4. 타입 변환
- Go는 암시적 타입 변환 없음
- 명시적 변환: `T(v)` 형식

---

## 실무 패턴

### 패턴 1: 여러 변수 동시 선언
```go
var (
    name   string = "Go"
    age    int    = 15
    active bool   = true
)
```

### 패턴 2: iota를 활용한 enum 패턴
```go
const (
    StatusPending = iota  // 0
    StatusActive          // 1
    StatusDone            // 2
)
```

---

## 소크라테스 질문

1. `var x int`와 `x := 0`의 차이점은 무엇인가요? 어떤 상황에서 각각을 사용하나요?

2. Go의 제로 값(Zero Value)은 왜 존재하나요? 이것이 null/nil과 어떻게 다른가요?

3. 왜 Go는 암시적 타입 변환을 허용하지 않을까요? `int` + `float64`가 에러인 이유는?

4. `const`와 `var`의 근본적인 차이는 무엇인가요? 컴파일 타임 vs 런타임의 관점에서 생각해보세요.

5. `iota`는 어떤 문제를 해결하기 위해 만들어졌나요?

---

## 실습 과제

### 과제 1: 타입 실험
다양한 타입의 변수를 선언하고 제로 값을 확인하세요.

### 과제 2: iota 활용
요일(Sunday~Saturday)을 iota로 정의하고, 일요일이 0인 경우와 1인 경우를 각각 구현하세요.

---

## 참고 자료
- [Go Tour - Basics](https://go.dev/tour/basics)
- [Effective Go - Variables](https://go.dev/doc/effective_go#variables)
