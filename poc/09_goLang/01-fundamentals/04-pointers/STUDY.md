# 04. 포인터 (Pointers)

## 학습 목표
Go의 포인터 개념과 값/참조 전달의 차이를 이해한다.

---

## 핵심 개념

### 1. 포인터 기본
- `*T`: T 타입의 포인터
- `&v`: v의 주소 얻기
- `*p`: 포인터가 가리키는 값 접근 (역참조)
- 제로 값: `nil`

### 2. 값 전달 vs 참조 전달
- Go는 항상 값 전달 (pass by value)
- 포인터를 전달하면 주소가 복사됨 (참조 효과)
- 큰 구조체는 포인터로 전달 권장

### 3. new vs make
- `new(T)`: T의 제로 값으로 메모리 할당, 포인터 반환
- `make(T)`: 슬라이스, 맵, 채널 전용, 초기화된 값 반환

### 4. 구조체 포인터
- `(*p).field` → `p.field`로 축약 가능
- 메서드에서 자주 사용

---

## 실무 패턴

### 패턴 1: 값 수정을 위한 포인터 전달
```go
func increment(n *int) {
    *n++
}

num := 5
increment(&num)  // num은 6
```

### 패턴 2: nil 체크
```go
func process(data *Data) error {
    if data == nil {
        return errors.New("data is nil")
    }
    // 처리
}
```

### 패턴 3: 구조체 생성자 패턴
```go
func NewUser(name string) *User {
    return &User{
        Name:      name,
        CreatedAt: time.Now(),
    }
}
```

---

## 소크라테스 질문

1. Go에서 "항상 값 전달"이라고 하는데, 슬라이스나 맵은 왜 참조처럼 동작하나요?

2. 포인터를 사용해야 하는 상황과 값을 사용해야 하는 상황은 각각 언제인가요?

3. `new()`와 `make()`가 분리된 이유는 무엇인가요? 하나로 통합할 수 없나요?

4. Go에 포인터 산술(pointer arithmetic)이 없는 이유는 무엇인가요?

5. 함수에서 로컬 변수의 포인터를 반환해도 안전한 이유는 무엇인가요? (이스케이프 분석)

---

## 실습 과제

### 과제 1: 두 변수 값 교환
포인터를 사용해 두 정수의 값을 교환하는 함수를 작성하세요.
```go
func swap(a, b *int)
```

### 과제 2: 링크드 리스트 노드
포인터를 활용해 간단한 단일 연결 리스트 노드를 정의하고, append 함수를 작성하세요.

---

## 참고 자료
- [Go Tour - Pointers](https://go.dev/tour/moretypes/1)
- [Effective Go - Allocation](https://go.dev/doc/effective_go#allocation_new)
