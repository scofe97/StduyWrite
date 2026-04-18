# Closure Exercise - LEARNED

## 학습 내용

### 클로저 기본

```go
func makeCounter() func() int {
    count := 0  // 자유 변수 (클로저가 캡처)

    return func() int {
        count++       // 외부 변수 count 참조
        return count
    }
}
```

### 핵심 개념

1. **클로저**: 함수 + 함수가 참조하는 외부 변수의 조합
2. **자유 변수**: 클로저가 캡처하는 외부 스코프의 변수
3. **상태 유지**: 반환된 함수는 자유 변수의 상태를 유지

### 실행 결과

```go
counter := makeCounter()
counter()  // 1
counter()  // 2
counter()  // 3
```

### 사용 사례

- 상태를 가진 함수 생성
- 팩토리 패턴
- 콜백에서 컨텍스트 유지

## 참고

- Go는 클로저에서 변수를 **참조**로 캡처 (복사 아님)
