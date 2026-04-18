# Chapter 9: Errors - 면접 정리

## 핵심 개념 상세 설명

### 1. Go의 에러 처리 철학

Go는 예외(Exception) 대신 에러 반환 값을 사용합니다. 에러는 함수의 마지막 반환값으로 전달되며, 호출자가 명시적으로 처리해야 합니다.

```
┌────────────────────────────────────────────────────────────────┐
│          예외 방식 vs Go 에러 방식                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Exception 방식 (Java, Python 등)                               │
│  ────────────────────────────────                               │
│  - 에러 발생 시 호출 스택을 거슬러 올라감                       │
│  - catch 없으면 에러 무시 가능                                  │
│  - 코드 경로가 암시적                                           │
│                                                                 │
│  Go Error 방식                                                  │
│  ────────────────                                               │
│  - 에러를 반환값으로 명시적 전달                                │
│  - 에러 무시 시 _ 사용 필요 (의도적 무시 표시)                  │
│  - 코드 경로가 순차적이고 명시적                                │
│                                                                 │
│  result, err := doSomething()                                   │
│  if err != nil {                                                │
│      // error handling (들여쓰기)                               │
│      return err                                                 │
│  }                                                              │
│  // business logic (왼쪽 정렬 = "Golden Path")                  │
│  useResult(result)                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

error는 단순한 인터페이스입니다: `type error interface { Error() string }`. nil은 에러가 없음을 의미하며, 인터페이스의 zero value입니다.

### 2. 에러 생성 방법

에러를 생성하는 두 가지 표준 방법이 있습니다. `errors.New`는 단순한 정적 에러 메시지를, `fmt.Errorf`는 런타임 정보를 포함한 동적 에러 메시지를 생성합니다.

에러 메시지 규칙: 대문자로 시작하지 않고, 구두점이나 개행으로 끝나지 않습니다. 이는 에러 메시지가 래핑되어 결합될 때 자연스럽게 읽히도록 하기 위함입니다.

### 3. Sentinel Error

Sentinel Error는 패키지 레벨에 선언된 특별한 에러 값입니다. 특정 상태에 도달했음을 나타내며, 호출자가 이를 확인하고 특별한 처리를 할 수 있습니다.

```
┌────────────────────────────────────────────────────────────────┐
│              Sentinel Error 사용 판단                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  에러 상황 발생                                                 │
│       │                                                         │
│       ▼                                                         │
│  추가 정보가 필요한가? ──Yes──→ Custom Error Type 사용          │
│       │                                                         │
│      No                                                         │
│       ▼                                                         │
│  특정 상태 도달을 나타내는가? ──No──→ 일반 에러 반환           │
│       │                                                         │
│      Yes                                                        │
│       ▼                                                         │
│  기존 Sentinel이 있는가? ──Yes──→ 기존 Sentinel 재사용          │
│       │                          (예: io.EOF)                   │
│      No                                                         │
│       ▼                                                         │
│  새 Sentinel 정의                                               │
│  var ErrNotFound = errors.New("resource not found")             │
│                                                                 │
│  이름 규칙: Err로 시작 (예외: io.EOF)                           │
│  특징: 읽기 전용으로 취급 (변경 금지)                           │
└────────────────────────────────────────────────────────────────┘
```

### 4. Custom Error Type

추가 정보를 담아야 할 때 Custom Error Type을 구현합니다. Error() 메서드만 구현하면 error 인터페이스를 만족합니다.

```
┌────────────────────────────────────────────────────────────────┐
│         Custom Error Type 주의사항                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ 잘못된 패턴:                                                │
│                                                                 │
│  func GenerateError(flag bool) error {                          │
│      var genErr StatusErr  // 구체 타입으로 선언                │
│      if flag {                                                  │
│          genErr = StatusErr{Status: NotFound}                   │
│      }                                                          │
│      return genErr  // flag=false여도 nil이 아님!               │
│  }                                                              │
│                                                                 │
│  이유:                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  var genErr StatusErr  →  error 인터페이스에 할당       │   │
│  │                                                          │   │
│  │  error interface {                                       │   │
│  │      type: StatusErr  ← non-nil!                        │   │
│  │      value: zero value                                   │   │
│  │  }                                                       │   │
│  │                                                          │   │
│  │  type이 non-nil이면 인터페이스 != nil                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ✅ 올바른 패턴:                                                │
│                                                                 │
│  func GenerateError(flag bool) error {                          │
│      if flag {                                                  │
│          return StatusErr{Status: NotFound}                     │
│      }                                                          │
│      return nil  // 명시적 nil 반환                             │
│  }                                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 5. Error Wrapping

에러를 래핑하면 컨텍스트를 추가하면서 원본 에러를 보존할 수 있습니다. `fmt.Errorf`의 `%w` verb를 사용합니다.

```go
return fmt.Errorf("loading config from %s: %w", path, err)
// 결과: "loading config from /etc/app.conf: open /etc/app.conf: no such file"
```

Custom Error에서 Unwrap() 메서드를 구현하면 에러 체인을 형성합니다. Go 1.20부터 `errors.Join`으로 여러 에러를 결합하거나, `Unwrap() []error`로 다중 에러를 반환할 수 있습니다.

내부 구현을 숨기고 싶을 때는 `%v`를 사용하여 래핑하지 않습니다.

### 6. errors.Is와 errors.As

에러 체인에서 특정 에러를 검색할 때 사용합니다.

```
┌────────────────────────────────────────────────────────────────┐
│            errors.Is vs errors.As                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  errors.Is(err, target)                                         │
│  ───────────────────────                                        │
│  - 에러 체인에서 특정 값/인스턴스 검색                          │
│  - Sentinel Error 비교에 주로 사용                              │
│  - 커스텀 Is() 메서드로 비교 로직 정의 가능                     │
│                                                                 │
│  if errors.Is(err, os.ErrNotExist) {                           │
│      fmt.Println("파일이 없습니다")                             │
│  }                                                              │
│                                                                 │
│  errors.As(err, &target)                                        │
│  ───────────────────────                                        │
│  - 에러 체인에서 특정 타입 검색                                 │
│  - 두 번째 인자는 반드시 포인터!                                │
│  - 타입별 처리에 사용                                           │
│                                                                 │
│  var statusErr StatusErr                                        │
│  if errors.As(err, &statusErr) {                               │
│      fmt.Printf("Status: %d\n", statusErr.Status)               │
│  }                                                              │
│                                                                 │
│  에러 트리 순회:                                                │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  wrapped error 1                                       │     │
│  │       └── wrapped error 2                              │     │
│  │              └── original error (target)               │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
│  errors.Is/As는 모든 레벨을 순회하며 검색                       │
└────────────────────────────────────────────────────────────────┘
```

### 7. panic과 recover

panic은 복구 불가능한 상황에서만 사용합니다. 발생 시 현재 함수의 defer를 실행하고, 호출 스택을 거슬러 올라가며 각 함수의 defer를 실행합니다. recover는 defer 안에서만 동작하며, panic을 잡아 정상 흐름으로 전환합니다.

```
┌────────────────────────────────────────────────────────────────┐
│             panic/recover 사용 지침                             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  상황                          권장 조치                        │
│  ─────────────────────────     ────────────────────────────    │
│  프로그래밍 에러               panic 허용 (코드 수정 필요)      │
│  (범위 초과, nil 역참조 등)                                     │
│                                                                 │
│  리소스 부족                   recover → 로깅 → os.Exit(1)     │
│  (메모리, 디스크)                                               │
│                                                                 │
│  라이브러리 경계               recover로 panic → error 변환    │
│                                (panic이 API 밖으로 나가면 안됨) │
│                                                                 │
│  일반 에러 상황                error 반환 사용                  │
│  (파일 없음, 네트워크 실패 등)                                  │
│                                                                 │
│  recover 패턴:                                                  │
│                                                                 │
│  func PublicAPIFunction() (result Result, err error) {          │
│      defer func() {                                             │
│          if v := recover(); v != nil {                         │
│              err = fmt.Errorf("internal error: %v", v)          │
│          }                                                      │
│      }()                                                        │
│      return internalLogic()                                     │
│  }                                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 8. defer로 에러 래핑

Named return value와 defer를 조합하면 중복된 에러 래핑 코드를 줄일 수 있습니다.

```go
func DoSomeThings(val1 int, val2 string) (_ string, err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("in DoSomeThings: %w", err)
        }
    }()

    val3, err := doThing1(val1)
    if err != nil {
        return "", err
    }
    // ... 모든 에러가 자동으로 래핑됨
}
```

---

## 비교표

### 에러 처리 방식 비교

| 특징 | Exception (Java 등) | Go Error |
|------|-------------------|----------|
| 에러 전파 | 암시적 (throw/catch) | 명시적 (반환값) |
| 코드 흐름 | 점프 (try-catch 블록) | 순차적 |
| 무시 가능성 | catch 없이 가능 | _ 변수 사용 필요 |
| 성능 | try-catch 오버헤드 | 없음 |

### Sentinel Error vs Custom Error

| 특성 | Sentinel Error | Custom Error |
|------|---------------|--------------|
| 선언 | 패키지 레벨 var | type 정의 |
| 정보량 | 고정 메시지 | 추가 필드 가능 |
| 비교 방법 | errors.Is | errors.As |
| 사용 시점 | 특정 상태 표시 | 추가 컨텍스트 필요 시 |

### errors.Is vs errors.As

| 함수 | 검색 대상 | 사용 예 |
|------|----------|---------|
| errors.Is | 특정 값/인스턴스 | Sentinel Error 비교 |
| errors.As | 특정 타입 | Custom Error 타입 추출 |

### %w vs %v 에러 포맷팅

| 형식 | 동작 | 사용 시점 |
|------|------|----------|
| %w | 에러 래핑 (Unwrap 가능) | 원본 에러 보존 필요 |
| %v | 문자열 변환 (래핑 안 함) | 내부 구현 숨기기 |

---

## 면접 예상 질문 및 모범 답안

### Q1. Go가 예외 대신 에러 반환값을 사용하는 이유와 장단점을 설명하세요.

**모범 답안:**

Go가 에러 반환값을 사용하는 이유는 명시성과 단순성입니다.

장점으로 첫째, 코드 경로가 명시적입니다. 예외는 어디서 발생해서 어디로 전파되는지 추적하기 어렵지만, Go는 에러가 반환값으로 전달되어 흐름이 순차적입니다. 둘째, 에러 무시가 의도적입니다. 예외는 catch 없이 무시되지만, Go는 `_`를 사용해야 해서 코드 리뷰 시 발견하기 쉽습니다. 셋째, 성능 오버헤드가 없습니다. try-catch는 런타임 비용이 있지만, 에러 반환은 일반 반환과 동일합니다.

단점으로 첫째, `if err != nil` 패턴이 반복되어 코드가 장황해 보일 수 있습니다. 둘째, 에러를 무시하고 싶을 때도 반드시 처리해야 합니다. 셋째, 호출 스택 정보가 기본적으로 포함되지 않아 별도로 래핑하거나 서드파티 라이브러리를 사용해야 합니다.

Go의 관용적 스타일은 에러 처리 코드를 들여쓰기하고, 정상 로직은 왼쪽에 정렬하는 "Golden Path" 패턴입니다. 이렇게 하면 코드 의도가 명확해집니다.

---

### Q2. Custom Error Type에서 nil을 반환할 때 주의할 점을 설명하세요.

**모범 답안:**

Go에서 인터페이스는 type과 value 두 개의 포인터로 구성됩니다. 인터페이스가 nil이 되려면 둘 다 nil이어야 합니다.

문제 상황은 Custom Error Type 변수를 선언하고, 조건에 따라 값을 할당한 후 반환할 때 발생합니다.

```go
var genErr StatusErr  // 구체 타입으로 선언
if flag {
    genErr = StatusErr{Status: NotFound}
}
return genErr  // flag=false여도 nil이 아님!
```

genErr이 error 인터페이스로 반환될 때, type 포인터는 StatusErr를 가리키고 value만 zero value입니다. type이 non-nil이므로 인터페이스 자체는 nil이 아닙니다.

해결 방법은 두 가지입니다. 첫째, 명시적으로 nil을 반환합니다: `return nil`. 둘째, 변수를 error 타입으로 선언합니다: `var genErr error`.

권장하는 방식은 첫 번째입니다. 에러가 없을 때 `return nil`을 명시적으로 작성하면 의도가 명확하고 실수를 방지합니다.

---

### Q3. errors.Is와 errors.As의 차이점과 각각의 사용 시나리오를 설명하세요.

**모범 답안:**

errors.Is와 errors.As는 에러 체인에서 특정 에러를 검색하는 함수입니다.

errors.Is는 특정 에러 인스턴스나 값을 찾습니다. Sentinel Error와 비교할 때 주로 사용합니다. 에러 체인을 순회하며 `==` 비교를 수행합니다.

```go
if errors.Is(err, os.ErrNotExist) {
    // 파일이 없는 경우 처리
}
```

커스텀 Is() 메서드를 구현하면 비교 로직을 정의할 수 있습니다. 예를 들어 ResourceErr에서 Resource 필드만 비교하거나 Code 필드만 비교하도록 할 수 있습니다.

errors.As는 특정 에러 타입을 찾습니다. Custom Error에서 추가 정보를 추출할 때 사용합니다. 두 번째 인자는 반드시 포인터여야 합니다.

```go
var statusErr StatusErr
if errors.As(err, &statusErr) {
    fmt.Printf("Status: %d\n", statusErr.Status)
}
```

인터페이스 타입으로도 사용 가능합니다. `var coder interface { CodeVals() []int }` 형태로 선언하고 errors.As에 전달하면, 해당 메서드를 구현한 에러를 찾습니다.

---

### Q4. Error Wrapping이 필요한 이유와 %w 대신 %v를 사용해야 하는 경우를 설명하세요.

**모범 답안:**

Error Wrapping은 에러에 컨텍스트를 추가하면서 원본 에러를 보존합니다.

필요한 이유는 세 가지입니다. 첫째, 에러 발생 위치와 상황을 파악할 수 있습니다. "in fileChecker: open file.txt: no such file"처럼 호출 스택을 추적합니다. 둘째, errors.Is와 errors.As로 원본 에러를 검색할 수 있습니다. 래핑된 에러에서도 os.ErrNotExist를 찾을 수 있습니다. 셋째, 여러 계층을 거치면서 각 계층이 관련 정보를 추가할 수 있습니다.

%v를 사용해야 하는 경우는 내부 구현을 숨기고 싶을 때입니다. 예를 들어 라이브러리가 내부적으로 사용하는 저수준 에러를 노출하고 싶지 않을 때, `fmt.Errorf("failed to initialize: %v", err)`로 문자열만 포함시킵니다. 이렇게 하면 호출자가 errors.Is로 내부 에러를 검색할 수 없습니다.

또한 에러 체인이 너무 길어지면 메모리와 성능에 영향을 줄 수 있으므로, 필요하지 않은 경우 %v로 체인을 끊습니다.

---

### Q5. panic과 recover의 적절한 사용 시나리오와 주의점을 설명하세요.

**모범 답안:**

panic은 복구 불가능한 상황에서만 사용합니다.

적절한 사용 시나리오는 세 가지입니다. 첫째, 프로그래밍 에러입니다. 배열 범위 초과, nil 포인터 역참조 등은 코드 버그이므로 panic이 적절합니다. 둘째, 초기화 실패입니다. 필수 설정 파일이 없거나 데이터베이스 연결이 안 될 때 프로그램 시작 단계에서 panic을 사용할 수 있습니다. 셋째, 불가능한 상황입니다. switch의 default 케이스가 절대 발생하지 않아야 할 때 panic으로 표시합니다.

recover 사용 시나리오는 주로 라이브러리 경계입니다. 라이브러리 내부에서 panic이 발생해도 호출자에게는 error로 반환해야 합니다. 공개 API 함수에서 defer와 recover로 panic을 잡아 error로 변환합니다.

주의점으로, recover는 반드시 defer 함수 안에서만 동작합니다. Go 1.21부터 panic(nil) 호출 시 *runtime.PanicNilError가 발생합니다. 또한 recover 후에도 goroutine은 정상 종료되지만, 다른 goroutine에서 발생한 panic은 recover할 수 없습니다.

---

### Q6. defer를 사용한 에러 래핑 패턴의 장점과 구현 방법을 설명하세요.

**모범 답안:**

defer를 사용한 에러 래핑은 Named return value와 결합하여 중복 코드를 줄입니다.

기존 패턴에서는 각 에러 체크마다 동일한 래핑 코드가 반복됩니다:
```go
if err != nil {
    return "", fmt.Errorf("in DoSomething: %w", err)
}
```

defer 패턴을 사용하면 함수 시작 부분에서 한 번만 정의합니다:
```go
func DoSomething(val int) (_ string, err error) {
    defer func() {
        if err != nil {
            err = fmt.Errorf("in DoSomething: %w", err)
        }
    }()
    // 이후 에러는 return "", err 만 하면 됨
}
```

핵심은 Named return value(`err error`)입니다. defer 클로저가 외부 함수의 err 변수에 접근할 수 있어, 함수가 에러를 반환할 때 자동으로 래핑됩니다.

장점은 세 가지입니다. 첫째, 코드 중복이 줄어듭니다. 둘째, 래핑 로직을 한 곳에서 관리할 수 있습니다. 셋째, 새 에러 체크를 추가할 때 래핑을 잊을 위험이 없습니다.

주의점으로, 첫 번째 반환값도 blank identifier(`_`)로 named return해야 컴파일러가 정상 동작합니다.

---

## 실무 체크리스트

### 에러 생성
- [ ] errors.New 또는 fmt.Errorf 사용
- [ ] 에러 메시지: 소문자 시작, 구두점 없음
- [ ] 런타임 정보 필요 시 fmt.Errorf 사용

### Sentinel Error
- [ ] 패키지 레벨에 var Err... 선언
- [ ] 읽기 전용으로 취급
- [ ] errors.Is로 검사

### Custom Error
- [ ] Error() 메서드 구현
- [ ] 반환 시 error 타입 사용 (구체 타입 아님)
- [ ] 에러 없을 때 명시적 return nil
- [ ] 래핑 필요 시 Unwrap() 구현

### Error Wrapping
- [ ] 컨텍스트 추가 시 %w 사용
- [ ] 내부 구현 숨길 때 %v 사용
- [ ] 여러 에러 결합 시 errors.Join 사용

### 에러 검사
- [ ] Sentinel 비교: errors.Is 사용
- [ ] 타입 추출: errors.As 사용 (포인터 전달!)
- [ ] == 대신 errors.Is 권장 (래핑된 에러 대응)

### panic/recover
- [ ] panic은 복구 불가능한 상황에만 사용
- [ ] 라이브러리 경계에서 recover로 error 변환
- [ ] recover는 defer 안에서만 동작

---

## 참고 자료

- [Go Blog - Error handling and Go](https://go.dev/blog/error-handling-and-go)
- [Go Blog - Working with Errors in Go 1.13](https://go.dev/blog/go1.13-errors)
- [Dave Cheney - Don't Just Check Errors, Handle Them Gracefully](https://dave.cheney.net/2016/04/27/dont-just-check-errors-handle-them-gracefully)
- [Effective Go - Errors](https://go.dev/doc/effective_go#errors)
- [cockroachdb/errors](https://github.com/cockroachdb/errors) - Stack trace 지원
