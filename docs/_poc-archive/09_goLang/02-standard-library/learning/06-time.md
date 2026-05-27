# 10. 시간과 로깅 (Time & Logging)

## 학습 목표
Go의 시간 처리와 로깅 방법을 이해한다.

---

## 핵심 개념

### 1. time 패키지 기본
- `time.Now()`: 현재 시간
- `time.Time`: 시간 타입
- `time.Duration`: 기간 타입
- `time.Sleep()`: 일시 정지

### 2. 시간 생성
- `time.Date()`: 특정 시간 생성
- `time.Parse()`: 문자열 → 시간
- 레이아웃: Go의 특이한 포맷 (`2006-01-02 15:04:05`)

### 3. 시간 연산
- `Add()`, `Sub()`: 더하기/빼기
- `Before()`, `After()`, `Equal()`: 비교
- `Truncate()`, `Round()`: 절삭/반올림

### 4. 표준 로깅 (log)
- `log.Print`, `log.Printf`, `log.Println`
- `log.Fatal`: 로그 후 os.Exit(1)
- `log.Panic`: 로그 후 panic
- `log.SetPrefix`, `log.SetFlags`

### 5. 구조화 로깅 (logrus 등)
- 필드 기반 로깅
- 로그 레벨 (Debug, Info, Warn, Error)
- JSON 포맷 출력

---

## 실무 패턴

### 패턴 1: 시간 포맷팅
```go
// Go의 레퍼런스 시간: 2006-01-02 15:04:05
t := time.Now()
fmt.Println(t.Format("2006-01-02"))          // 2024-01-15
fmt.Println(t.Format("15:04:05"))            // 14:30:45
fmt.Println(t.Format(time.RFC3339))          // ISO 8601
```

### 패턴 2: 시간 파싱
```go
layout := "2006-01-02"
t, err := time.Parse(layout, "2024-01-15")
if err != nil {
    log.Fatal(err)
}
```

### 패턴 3: 로깅 설정
```go
log.SetPrefix("[MyApp] ")
log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

log.Println("서버 시작")
// [MyApp] 2024/01/15 14:30:45 main.go:10: 서버 시작
```

---

## 소크라테스 질문

1. Go의 시간 포맷이 왜 `2006-01-02 15:04:05`인가요? 이 특이한 숫자의 의미는?

2. `time.Duration`과 `time.Time`의 차이점은 무엇인가요?

3. 타임존 처리에서 주의해야 할 점은 무엇인가요? `time.Local` vs `time.UTC`

4. `log.Fatal`과 `log.Panic`의 차이점과 각각의 사용 시점은?

5. 구조화 로깅이 일반 텍스트 로깅보다 좋은 이유는 무엇인가요?

---

## 실습 과제

### 과제 1: 시간 차이 계산
두 날짜 사이의 일수를 계산하는 함수를 작성하세요.

### 과제 2: 로그 래퍼
로그 레벨(Debug, Info, Error)을 지원하는 간단한 로거를 작성하세요.

---

## 참고 자료
- [Go Package - time](https://pkg.go.dev/time)
- [Go Package - log](https://pkg.go.dev/log)
- [logrus](https://github.com/sirupsen/logrus)
