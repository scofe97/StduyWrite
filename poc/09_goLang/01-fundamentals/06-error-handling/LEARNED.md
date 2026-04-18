# Stage 03: 에러 처리 학습 정리

## 1. Go 에러 처리 기본

### try-catch 없음 - 반환값으로 처리
```go
// Go 스타일
result, err := divide(10, 0)
if err != nil {
    // 에러 처리
}
```

### 에러 반환 함수 패턴
```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil  // 성공 시 에러는 nil
}
```

---

## 2. 에러 생성 방법

### errors.New - 단순 메시지
```go
err := errors.New("something went wrong")
```

### fmt.Errorf - 변수 포함 가능
```go
name := "config.json"
err := fmt.Errorf("file not found: %s", name)
```

---

## 3. Sentinel Error

### 문제: 매번 생성하면 비교 불가
```go
err1 := errors.New("error")
err2 := errors.New("error")
fmt.Println(err1 == err2)  // false! 다른 객체
```

### 해결: 미리 정의 (Sentinel Error)
```go
var ErrEmptyPath = errors.New("path is empty")

func ReadFile(path string) error {
    if path == "" {
        return ErrEmptyPath  // 같은 객체 반환
    }
}

// 호출 측에서 비교 가능
if err == ErrEmptyPath {
    // 처리
}
```

---

## 4. 에러 래핑 (%w)

### 에러 체인 유지
```go
_, err := os.ReadFile(path)
if err != nil {
    return fmt.Errorf("ReadFile failed: %w", err)  // 래핑
}
```

### %w vs %v 차이

| 포맷 | 동작 | errors.Is() |
|------|------|-------------|
| `%w` | 에러 체인 유지 | ✅ 원본 추적 가능 |
| `%v` | 문자열만 변환 | ❌ 연결 끊김 |

```go
original := errors.New("원본")
wrapped1 := fmt.Errorf("래핑: %w", original)
wrapped2 := fmt.Errorf("래핑: %v", original)

errors.Is(wrapped1, original)  // true
errors.Is(wrapped2, original)  // false
```

---

## 5. errors.Is() 사용

래핑된 에러에서 원본 찾기:
```go
err := ReadFile("")  // 내부에서 ErrEmptyPath 반환

// 직접 비교 (래핑 안 된 경우)
if err == ErrEmptyPath { }

// errors.Is (래핑되어도 찾음)
if errors.Is(err, ErrEmptyPath) { }
```

---

## 6. 컴파일 에러 vs 런타임 에러

| 구분 | 컴파일 에러 | 런타임 에러 (panic) |
|------|------------|-------------------|
| 시점 | 빌드 시 | 실행 중 |
| 예시 | `undefined: ReadFile` | `slice bounds out of range` |
| 프로그램 | 시작 안 됨 | 실행 중 터짐 |

---

## 7. go run 멀티 파일

같은 폴더의 여러 .go 파일 실행:
```bash
go run .           # 권장
go run *.go        # 또는 모든 파일 지정
go run main.go     # ❌ main.go만 컴파일
```

---

## 실습 파일

| 파일 | 내용 |
|------|------|
| `errors.go` | Sentinel Error 정의 |
| `reader.go` | ReadFile 함수 (에러 래핑) |
| `main.go` | 테스트 코드 |

---

## 원본 프로젝트 참조

| 파일 | 학습 내용 |
|------|----------|
| `internal/provider/config.go` | Sentinel Error 정의 |
| `internal/client/github.go` | 에러 래핑 패턴 (`%w`) |
