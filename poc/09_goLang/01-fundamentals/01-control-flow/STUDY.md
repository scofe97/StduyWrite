# 01. 제어 흐름 (Control Flow)

## 학습 목표
Go의 조건문, 반복문, switch 문법을 이해하고 활용한다.

---

## 핵심 개념

### 1. if/else 조건문
- 괄호 없이 조건 작성
- 조건문 앞에 짧은 문장 실행 가능 (if 스코프)
- else if 체이닝

### 2. switch 문
- **표현식 switch**: 값 기반 분기
- **타입 switch**: 인터페이스 타입 확인
- `fallthrough`: 다음 case로 강제 진행
- 조건 없는 switch (= if-else 체인 대체)

### 3. for 루프 (Go의 유일한 반복문)
- **전통적 for**: `for i := 0; i < n; i++`
- **while 스타일**: `for condition {}`
- **무한 루프**: `for {}`
- **range**: 컬렉션 순회

### 4. 루프 제어
- `break`: 루프 탈출
- `continue`: 다음 반복으로
- 레이블 break/continue: 중첩 루프 제어

---

## 실무 패턴

### 패턴 1: if 문에서 변수 선언
```go
if err := doSomething(); err != nil {
    return err
}
// err은 이 스코프에서 사라짐
```

### 패턴 2: range로 맵 순회
```go
for key, value := range myMap {
    fmt.Printf("%s: %v\n", key, value)
}
```

### 패턴 3: 조건 없는 switch
```go
switch {
case score >= 90:
    grade = "A"
case score >= 80:
    grade = "B"
default:
    grade = "C"
}
```

---

## 소크라테스 질문

1. Go에서 `while` 키워드가 없는 이유는 무엇일까요? `for`만으로 충분한 이유는?

2. `if err := ...; err != nil` 패턴이 왜 Go에서 관용적인가요? 스코프 관점에서 생각해보세요.

3. switch의 `fallthrough`는 언제 유용한가요? 왜 Go는 기본적으로 break가 적용되나요?

4. `range`로 슬라이스를 순회할 때 `for i, v := range slice`에서 v를 수정하면 원본이 바뀔까요?

5. 레이블 break가 필요한 상황은 어떤 경우인가요?

---

## 실습 과제

### 과제 1: FizzBuzz 구현
1부터 100까지 숫자를 출력하되:
- 3의 배수: "Fizz"
- 5의 배수: "Buzz"
- 15의 배수: "FizzBuzz"

### 과제 2: 구구단 출력
중첩 for문으로 2~9단 구구단을 출력하세요.

---

## 참고 자료
- [Go Tour - Flow Control](https://go.dev/tour/flowcontrol)
- [Effective Go - Control Structures](https://go.dev/doc/effective_go#control-structures)
