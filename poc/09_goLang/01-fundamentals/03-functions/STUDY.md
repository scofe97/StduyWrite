# 03. 함수 (Functions)

## 학습 목표
Go의 함수 선언, 다중 반환값, 가변 인자, 클로저를 이해한다.

---

## 핵심 개념

### 1. 함수 기본
- `func name(params) returnType { }`
- 파라미터: 이름 뒤에 타입
- 같은 타입 파라미터 축약: `func add(a, b int)`

### 2. 다중 반환값
- 여러 값 동시 반환 가능
- 에러 처리의 관용적 패턴: `result, err`
- 사용하지 않는 반환값: `_` (blank identifier)

### 3. Named Return
- 반환값에 이름 지정
- 함수 내에서 변수처럼 사용
- naked return (이름만으로 반환) - 짧은 함수에서만 권장

### 4. 가변 인자 (Variadic)
- `func sum(nums ...int)`: 0개 이상 인자
- 함수 내에서 슬라이스로 처리
- 슬라이스 전달: `sum(slice...)`

### 5. 클로저 (Closure)
- 함수 밖 변수를 캡처하는 함수
- 익명 함수와 함께 자주 사용
- 상태 유지에 활용

---

## 실무 패턴

### 패턴 1: 에러 반환 패턴
```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}
```

### 패턴 2: 옵션 패턴 (가변 인자 활용)
```go
type Option func(*Config)

func WithTimeout(d time.Duration) Option {
    return func(c *Config) {
        c.Timeout = d
    }
}

func NewClient(opts ...Option) *Client {
    // 기본 설정 후 옵션 적용
}
```

### 패턴 3: 클로저로 카운터 만들기
```go
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}
```

---

## 소크라테스 질문

1. Go가 다중 반환값을 지원하는 이유는 무엇인가요? 튜플이나 구조체 대신 이 방식을 선택한 이유는?

2. Named return은 언제 유용하고, 언제 피해야 하나요?

3. 클로저가 변수를 "캡처"한다는 것은 정확히 무슨 의미인가요? 복사인가요, 참조인가요?

4. 가변 인자 함수에 슬라이스를 전달할 때 `...`을 붙여야 하는 이유는?

5. `func` 타입이 일급 시민(first-class citizen)이라는 것은 무엇을 의미하나요?

---

## 실습 과제

### 과제 1: 고차 함수 작성
슬라이스의 각 요소에 함수를 적용하는 `Map` 함수를 작성하세요.
```go
func Map(slice []int, f func(int) int) []int
```

### 과제 2: 클로저 활용
이전 호출의 결과를 기억하는 피보나치 생성기를 클로저로 작성하세요.

---

## 하위 디렉토리
- `closure/`: 클로저 심화 예제

---

## 참고 자료
- [Go Tour - Functions](https://go.dev/tour/moretypes/24)
- [Effective Go - Functions](https://go.dev/doc/effective_go#functions)
