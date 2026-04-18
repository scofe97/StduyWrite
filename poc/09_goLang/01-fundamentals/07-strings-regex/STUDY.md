# 07. 문자열과 정규식 (Strings & Regex)

## 학습 목표
Go의 문자열 처리와 정규표현식 사용법을 이해한다.

---

## 핵심 개념

### 1. 문자열 기본
- 불변(immutable): 수정 불가
- UTF-8 인코딩
- 바이트 슬라이스로 변환 가능: `[]byte(s)`

### 2. 룬(rune)과 UTF-8
- `rune`: int32, 유니코드 코드포인트
- `len(s)`: 바이트 수
- `utf8.RuneCountInString(s)`: 문자 수
- 문자열 순회: `for i, r := range s`

### 3. strings 패키지
- `Contains`, `HasPrefix`, `HasSuffix`
- `Split`, `Join`
- `ToUpper`, `ToLower`, `TrimSpace`
- `Replace`, `ReplaceAll`
- `Builder`: 효율적 문자열 빌드

### 4. strconv 패키지
- `Atoi`, `Itoa`: 정수 ↔ 문자열
- `ParseInt`, `FormatInt`: 진법 지정
- `ParseFloat`, `FormatFloat`

### 5. 정규표현식 (regexp)
- `regexp.Compile`, `regexp.MustCompile`
- `MatchString`, `FindString`
- `FindAllString`, `ReplaceAllString`
- 캡처 그룹: `FindStringSubmatch`

---

## 실무 패턴

### 패턴 1: 효율적 문자열 연결
```go
var builder strings.Builder
for _, s := range items {
    builder.WriteString(s)
}
result := builder.String()
```

### 패턴 2: 문자열 분리/조합
```go
// 분리
parts := strings.Split("a,b,c", ",")

// 조합
joined := strings.Join(parts, "-")  // "a-b-c"
```

### 패턴 3: 정규식 컴파일 (성능)
```go
// 패키지 수준에서 한 번만 컴파일
var emailRegex = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)

func isValidEmail(email string) bool {
    return emailRegex.MatchString(email)
}
```

---

## 소크라테스 질문

1. Go 문자열이 불변인 이유는 무엇인가요? 이것의 장단점은?

2. `len("한글")`이 6을 반환하는 이유는 무엇인가요?

3. 문자열 연결에서 `+` 연산자 대신 `strings.Builder`를 사용해야 하는 이유는?

4. `regexp.Compile`과 `regexp.MustCompile`의 차이점과 각각의 사용 시점은?

5. 정규식 패턴을 함수 내에서 매번 컴파일하면 왜 성능 문제가 발생하나요?

---

## 실습 과제

### 과제 1: 문자열 처리 함수
주어진 문자열에서 모음(a, e, i, o, u)의 개수를 세는 함수를 작성하세요.

### 과제 2: 정규식 활용
전화번호 형식(010-XXXX-XXXX)을 검증하고, 하이픈 없는 형태로 변환하는 함수를 작성하세요.

---

## 하위 디렉토리
- `regexp/`: 정규표현식 심화 예제

---

## 참고 자료
- [Go Blog - Strings](https://go.dev/blog/strings)
- [Go Package - strings](https://pkg.go.dev/strings)
- [Go Package - regexp](https://pkg.go.dev/regexp)
