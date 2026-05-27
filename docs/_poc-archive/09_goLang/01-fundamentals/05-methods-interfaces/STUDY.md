# 05. 메서드와 인터페이스 (Methods & Interfaces)

## 학습 목표
Go의 메서드 정의와 인터페이스 기반 다형성을 이해한다.

---

## 핵심 개념

### 1. 메서드 정의
- 함수에 리시버(receiver) 추가
- 값 리시버: `func (r Rect) Area() float64`
- 포인터 리시버: `func (r *Rect) Scale(factor float64)`

### 2. 값 리시버 vs 포인터 리시버
- 값 리시버: 복사본에서 동작, 원본 수정 불가
- 포인터 리시버: 원본 수정 가능, 큰 구조체에 효율적
- 일관성 유지: 하나의 타입에서 하나만 사용 권장

### 3. 인터페이스
- 메서드 시그니처의 집합
- 암시적 구현 (implements 키워드 없음)
- 덕 타이핑: "오리처럼 걷고 꽥꽥대면 오리"

### 4. 타입 단언 (Type Assertion)
- `value := i.(T)`: 인터페이스 → 구체 타입
- `value, ok := i.(T)`: 안전한 타입 단언
- 타입 switch: 여러 타입 처리

### 5. 빈 인터페이스 (any)
- `interface{}` 또는 `any`: 모든 타입 수용
- 타입 안전성 감소, 필요 시에만 사용

---

## 실무 패턴

### 패턴 1: 인터페이스 기반 설계
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// 인터페이스 조합
type ReadWriter interface {
    Reader
    Writer
}
```

### 패턴 2: 인터페이스 검증 (컴파일 타임)
```go
// MyStruct가 Reader를 구현하는지 컴파일 시점에 확인
var _ Reader = (*MyStruct)(nil)
```

### 패턴 3: 타입 switch
```go
func describe(i interface{}) {
    switch v := i.(type) {
    case int:
        fmt.Printf("정수: %d\n", v)
    case string:
        fmt.Printf("문자열: %s\n", v)
    default:
        fmt.Printf("알 수 없는 타입: %T\n", v)
    }
}
```

---

## 소크라테스 질문

1. Go의 암시적 인터페이스 구현이 Java의 명시적 implements보다 좋은 점과 나쁜 점은?

2. 언제 값 리시버를 쓰고, 언제 포인터 리시버를 써야 하나요? 둘을 섞어 쓰면 안 되는 이유는?

3. "작은 인터페이스"가 왜 Go에서 권장되나요? (예: io.Reader는 메서드 1개)

4. `interface{}`(any)는 편리하지만 왜 남용하면 안 되나요?

5. 타입 단언과 타입 변환의 차이점은 무엇인가요?

---

## 실습 과제

### 과제 1: 도형 인터페이스
`Shape` 인터페이스(Area, Perimeter)를 정의하고, Rectangle과 Circle 타입으로 구현하세요.

### 과제 2: Stringer 구현
`fmt.Stringer` 인터페이스를 구현해 커스텀 타입의 출력 포맷을 지정하세요.

---

## 참고 자료
- [Go Tour - Methods](https://go.dev/tour/methods)
- [Effective Go - Interfaces](https://go.dev/doc/effective_go#interfaces)
