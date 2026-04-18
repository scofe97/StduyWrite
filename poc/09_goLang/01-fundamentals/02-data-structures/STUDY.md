# 02. 데이터 구조 (Data Structures)

## 학습 목표
Go의 기본 데이터 구조인 배열, 슬라이스, 맵, 구조체를 이해한다.

---

## 핵심 개념

### 1. 배열 (Array)
- 고정 크기, 타입의 일부 (`[3]int` ≠ `[4]int`)
- 값 타입 (복사됨)
- 실무에서는 거의 사용하지 않음

### 2. 슬라이스 (Slice)
- 동적 크기, 배열의 "뷰"
- 3요소: 포인터, 길이(len), 용량(cap)
- `make([]T, len, cap)`: 슬라이스 생성
- `append()`: 요소 추가 (용량 초과 시 재할당)

### 3. 맵 (Map)
- 키-값 저장소 (해시 테이블)
- `make(map[K]V)`: 맵 생성
- 제로 값은 `nil` (읽기만 가능, 쓰기 시 패닉)
- 키 존재 확인: `val, ok := m[key]`

### 4. 구조체 (Struct)
- 필드들의 집합
- 구조체 임베딩: 상속 대신 조합
- 익명 구조체: 일회성 데이터 구조

---

## 실무 패턴

### 패턴 1: 슬라이스 초기화
```go
// 리터럴
nums := []int{1, 2, 3}

// make로 용량 지정 (성능 최적화)
nums := make([]int, 0, 100)
```

### 패턴 2: 맵 키 존재 확인
```go
if val, ok := userMap[userID]; ok {
    // 존재함
    fmt.Println(val)
}
```

### 패턴 3: 구조체 임베딩
```go
type Person struct {
    Name string
}

type Employee struct {
    Person  // 임베딩
    Company string
}

emp := Employee{Person: Person{Name: "Kim"}, Company: "ABC"}
fmt.Println(emp.Name)  // Person의 필드 직접 접근
```

---

## 소크라테스 질문

1. 배열과 슬라이스의 근본적인 차이는 무엇인가요? 왜 실무에서 배열보다 슬라이스를 선호하나요?

2. `append()`가 새 슬라이스를 반환하는 이유는 무엇인가요? 왜 원본을 수정하지 않나요?

3. 맵의 제로 값이 `nil`인 이유와, 이것이 야기하는 문제는 무엇인가요?

4. 구조체 임베딩은 상속과 어떻게 다른가요? Go가 상속 대신 조합을 선택한 이유는?

5. 슬라이스의 용량(capacity)을 미리 지정하면 왜 성능이 좋아지나요?

---

## 실습 과제

### 과제 1: 슬라이스 조작
슬라이스에서 특정 인덱스의 요소를 삭제하는 함수를 작성하세요.

### 과제 2: 맵 활용
단어 빈도수를 세는 함수를 작성하세요. (입력: 문자열 슬라이스, 출력: 맵)

---

## 참고 자료
- [Go Tour - Moretypes](https://go.dev/tour/moretypes)
- [Go Blog - Slices](https://go.dev/blog/slices-intro)
- [Go Blog - Maps](https://go.dev/blog/maps)
