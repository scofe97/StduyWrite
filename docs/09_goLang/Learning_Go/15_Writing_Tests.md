# Chapter 15: Writing Tests - 면접정리

## 핵심 개념 상세 설명

### 1. Go 테스트의 기본 철학

Go는 테스트를 일급 시민으로 취급합니다. 별도의 테스트 프레임워크를 설치할 필요 없이 표준 라이브러리의 testing 패키지와 go test 명령으로 모든 테스트를 수행할 수 있습니다. 테스트 파일은 _test.go 접미사를 사용하며, 같은 패키지에 위치하여 unexported 함수와 변수에도 접근할 수 있습니다. 이는 화이트박스 테스트를 자연스럽게 지원합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Go Test File Structure                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   project/                                                      │
│   ├── calculator.go          ← Source file                     │
│   ├── calculator_test.go     ← Test file (same package)        │
│   └── testdata/              ← Test data directory (special)   │
│       ├── input1.txt                                           │
│       └── expected1.txt                                        │
│                                                                 │
│   calculator.go                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ package calculator                                       │   │
│   │                                                          │   │
│   │ func Add(a, b int) int { return a + b }                  │   │
│   │ func subtract(a, b int) int { return a - b }  // unexport│   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   calculator_test.go                                            │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ package calculator  // Same package → access unexported  │   │
│   │                                                          │   │
│   │ func TestAdd(t *testing.T) { ... }                       │   │
│   │ func Test_subtract(t *testing.T) { ... }  // Can test!   │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ⚠️ testdata/ is a special directory name                     │
│      - Ignored by go build                                      │
│      - Accessible via relative path in tests                    │
└─────────────────────────────────────────────────────────────────┘
```

### 2. 테스트 함수의 구조와 규칙

테스트 함수는 세 가지 규칙을 따릅니다. 함수명은 Test로 시작해야 합니다. *testing.T를 유일한 매개변수로 받습니다. 반환값이 없습니다.

```go
// 기본 테스트 함수 구조
func TestFunctionName(t *testing.T) {
    // 준비 (Arrange)
    input := "test input"
    expected := "expected output"

    // 실행 (Act)
    result := FunctionUnderTest(input)

    // 검증 (Assert)
    if result != expected {
        t.Errorf("got %s, want %s", result, expected)
    }
}
```

unexported 함수를 테스트할 때는 함수명 앞에 언더스코어를 붙이는 관례가 있습니다. Test_functionName 형식입니다. 메서드 테스트는 TestTypeName_MethodName 형식을 사용합니다.

### 3. Error vs Fatal: 테스트 실패 보고

testing.T는 테스트 실패를 보고하는 여러 메서드를 제공합니다. Error와 Errorf는 실패를 기록하지만 테스트를 계속합니다. Fatal과 Fatalf는 실패를 기록하고 테스트를 즉시 종료합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Error vs Fatal                               │
├───────────────────────────────┬─────────────────────────────────┤
│         Error/Errorf          │         Fatal/Fatalf            │
├───────────────────────────────┼─────────────────────────────────┤
│                               │                                 │
│ t.Error("message")            │ t.Fatal("message")              │
│ t.Errorf("format", args...)   │ t.Fatalf("format", args...)     │
│                               │                                 │
│ ✓ Records failure             │ ✓ Records failure               │
│ ✓ Continues execution         │ ✗ Stops test immediately        │
│                               │                                 │
├───────────────────────────────┼─────────────────────────────────┤
│ Use when:                     │ Use when:                       │
│ • Multiple independent checks │ • Setup failure                 │
│ • Want to see all failures    │ • Further checks meaningless    │
│ • Validating multiple fields  │ • nil pointer would crash       │
│                               │                                 │
│ Example:                      │ Example:                        │
│ if user.Name == "" {          │ config, err := LoadConfig()     │
│   t.Error("name empty")       │ if err != nil {                 │
│ }                             │   t.Fatal("can't load config")  │
│ if user.Age < 0 {             │ }                               │
│   t.Error("age negative")     │ // config is now safe to use    │
│ }                             │                                 │
└───────────────────────────────┴─────────────────────────────────┘
```

### 4. Table 테스트 패턴

Table 테스트는 Go에서 가장 널리 사용되는 테스트 패턴입니다. 여러 입력-출력 쌍을 구조체 슬라이스로 정의하고 반복하여 테스트합니다. 코드 중복을 제거하고 새 테스트 케이스를 쉽게 추가할 수 있습니다.

```go
func TestCalculate(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        op       string
        expected int
        wantErr  bool
    }{
        {"addition", 2, 3, "+", 5, false},
        {"subtraction", 5, 3, "-", 2, false},
        {"multiplication", 4, 3, "*", 12, false},
        {"division", 10, 2, "/", 5, false},
        {"division by zero", 10, 0, "/", 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Calculate(tt.a, tt.b, tt.op)

            if tt.wantErr {
                if err == nil {
                    t.Error("expected error, got nil")
                }
                return
            }

            if err != nil {
                t.Errorf("unexpected error: %v", err)
                return
            }

            if result != tt.expected {
                t.Errorf("got %d, want %d", result, tt.expected)
            }
        })
    }
}
```

t.Run은 서브테스트를 생성합니다. 각 서브테스트는 독립적으로 실패하고, -run 플래그로 특정 서브테스트만 실행할 수 있습니다.

### 5. Setup과 Teardown

Go는 setUp/tearDown 메서드 대신 여러 가지 설정/정리 메커니즘을 제공합니다.

TestMain은 패키지 레벨의 설정/정리를 위한 함수입니다. 패키지당 하나만 존재할 수 있으며, 모든 테스트 전에 한 번 호출됩니다.

```go
var testDB *sql.DB

func TestMain(m *testing.M) {
    // 모든 테스트 전 설정
    testDB = setupDatabase()

    // 모든 테스트 실행
    exitCode := m.Run()

    // 모든 테스트 후 정리
    testDB.Close()

    os.Exit(exitCode)
}
```

t.Cleanup은 테스트별 정리 함수를 등록합니다. 테스트 완료 후 역순으로 실행됩니다.

```go
func TestWithFile(t *testing.T) {
    f, err := os.Create("temp.txt")
    if err != nil {
        t.Fatal(err)
    }
    t.Cleanup(func() {
        f.Close()
        os.Remove(f.Name())
    })

    // 테스트 로직
}
```

t.TempDir()은 자동으로 정리되는 임시 디렉토리를 생성합니다. t.Setenv()는 테스트 후 자동으로 복원되는 환경 변수를 설정합니다.

### 6. 코드 커버리지

go test -cover는 테스트가 실행한 코드의 비율을 측정합니다. 커버리지 프로파일을 생성하고 HTML 보고서로 시각화할 수 있습니다.

```bash
# 커버리지 측정
go test -cover ./...

# 프로파일 저장
go test -coverprofile=coverage.out ./...

# HTML 보고서 생성
go tool cover -html=coverage.out -o coverage.html
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    Coverage Analysis                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   HTML Report Colors:                                           │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ GREEN  │ Covered by tests                                │   │
│   │ RED    │ Not covered - needs tests                       │   │
│   │ GRAY   │ Not instrumentable (declarations, etc.)         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ⚠️ Important Notes:                                          │
│   • 100% coverage ≠ bug-free code                              │
│   • Coverage measures execution, not correctness               │
│   • Focus on critical paths and edge cases                     │
│   • Untested error paths are common gaps                       │
│                                                                 │
│   Better than high coverage:                                    │
│   • Testing edge cases                                          │
│   • Testing error conditions                                    │
│   • Testing boundary values                                     │
│   • Using fuzzing for unexpected inputs                         │
└─────────────────────────────────────────────────────────────────┘
```

중요한 점은 100% 커버리지가 버그 없음을 보장하지 않는다는 것입니다. 커버리지는 코드가 실행되었음을 보여줄 뿐, 올바르게 동작했는지는 보여주지 않습니다.

### 7. 퍼징 (Fuzzing)

Go 1.18에서 도입된 퍼징은 자동 생성된 랜덤 입력으로 예상치 못한 버그를 발견합니다. 특히 파싱, 역직렬화, 인코딩/디코딩 함수에 유용합니다.

```go
func FuzzParse(f *testing.F) {
    // 시드 데이터 추가 (정상적인 입력 예시)
    f.Add([]byte("valid input"))
    f.Add([]byte("another valid"))

    // 퍼즈 타겟
    f.Fuzz(func(t *testing.T, data []byte) {
        result, err := Parse(data)
        if err != nil {
            return  // 에러는 예상된 동작
        }

        // Round-trip 테스트: 파싱 결과를 다시 직렬화하면 동일해야
        serialized := Serialize(result)
        result2, err := Parse(serialized)
        if err != nil {
            t.Errorf("round-trip failed: %v", err)
        }
        if !reflect.DeepEqual(result, result2) {
            t.Errorf("round-trip mismatch")
        }
    })
}
```

```bash
# 퍼징 실행 (시간 제한 없이 계속 실행)
go test -fuzz=FuzzParse

# 30초 동안만 실행
go test -fuzz=FuzzParse -fuzztime=30s
```

퍼징이 버그를 발견하면 실패한 입력이 testdata/fuzz 디렉토리에 저장되고, 이후 테스트에서 자동으로 재실행됩니다.

### 8. 벤치마크

벤치마크는 코드 성능을 측정합니다. Benchmark로 시작하는 함수와 *testing.B 매개변수를 사용합니다.

```go
var result int  // 컴파일러 최적화 방지

func BenchmarkFibonacci(b *testing.B) {
    for i := 0; i < b.N; i++ {
        result = Fibonacci(20)
    }
}

func BenchmarkFibonacciSizes(b *testing.B) {
    sizes := []int{10, 20, 30}
    for _, n := range sizes {
        b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
            for i := 0; i < b.N; i++ {
                result = Fibonacci(n)
            }
        })
    }
}
```

```bash
# 벤치마크 실행
go test -bench=.

# 메모리 할당 정보 포함
go test -bench=. -benchmem
```

```
┌─────────────────────────────────────────────────────────────────┐
│                 Benchmark Output Explained                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   BenchmarkFibonacci-8   5000   230000 ns/op   1024 B/op  10 allocs/op
│   │                  │   │      │              │           │
│   │                  │   │      │              │           └─ Heap allocations per op
│   │                  │   │      │              └─ Bytes allocated per op
│   │                  │   │      └─ Nanoseconds per operation
│   │                  │   └─ Number of iterations run
│   │                  └─ GOMAXPROCS value
│   └─ Benchmark name
│                                                                 │
│   b.N is automatically adjusted to get stable timing            │
│   More iterations = more accurate measurement                   │
│                                                                 │
│   ⚠️ Prevent Compiler Optimization:                            │
│   • Assign result to package-level variable                     │
│   • Otherwise compiler may eliminate "unused" computation       │
└─────────────────────────────────────────────────────────────────┘
```

### 9. Stub과 Mock 패턴

Go는 인터페이스를 통해 테스트 더블을 쉽게 만들 수 있습니다. Stub은 고정된 응답을 반환하고, Mock은 호출을 검증합니다.

인터페이스 임베딩 방식은 큰 인터페이스의 일부만 구현할 때 유용합니다.

```go
type Repository interface {
    GetUser(id string) (User, error)
    SaveUser(user User) error
    DeleteUser(id string) error
    // ... 더 많은 메서드
}

// 필요한 메서드만 구현하는 Stub
type GetUserStub struct {
    Repository  // 임베딩 - 다른 메서드는 패닉
}

func (s GetUserStub) GetUser(id string) (User, error) {
    return User{ID: id, Name: "Test User"}, nil
}
```

함수 필드 프록시 방식은 더 유연합니다. 각 테스트 케이스에서 다른 동작을 정의할 수 있습니다.

```go
type RepositoryStub struct {
    GetUserFunc   func(id string) (User, error)
    SaveUserFunc  func(user User) error
    DeleteUserFunc func(id string) error
}

func (s RepositoryStub) GetUser(id string) (User, error) {
    return s.GetUserFunc(id)
}

// 테스트에서 사용
func TestService(t *testing.T) {
    stub := RepositoryStub{
        GetUserFunc: func(id string) (User, error) {
            return User{ID: id, Name: "Test"}, nil
        },
    }
    service := NewService(stub)
    // ...
}
```

### 10. httptest 패키지

httptest는 HTTP 클라이언트와 서버를 테스트하기 위한 도구를 제공합니다. httptest.NewServer는 실제 HTTP 서버를 시작하여 통합 테스트를 가능하게 합니다.

```go
func TestAPIClient(t *testing.T) {
    // 테스트용 서버 생성
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // 요청 검증
        if r.URL.Path != "/api/users/123" {
            t.Errorf("unexpected path: %s", r.URL.Path)
        }

        // 응답 반환
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"id":"123","name":"Test"}`))
    }))
    defer server.Close()

    // 테스트 대상에 서버 URL 주입
    client := NewAPIClient(server.URL)
    user, err := client.GetUser("123")
    if err != nil {
        t.Fatal(err)
    }
    if user.Name != "Test" {
        t.Errorf("unexpected name: %s", user.Name)
    }
}
```

### 11. 데이터 레이스 탐지

-race 플래그는 데이터 레이스를 탐지합니다. 여러 goroutine이 동기화 없이 같은 메모리에 접근하면 경고합니다.

```bash
# 테스트에서 레이스 탐지
go test -race ./...

# 빌드 시 레이스 탐지기 포함
go build -race
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    Data Race Detection                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Race Condition Example:                                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ var counter int                                          │   │
│   │                                                          │   │
│   │ go func() { counter++ }()  ──┐                           │   │
│   │ go func() { counter++ }()  ──┼── DATA RACE!              │   │
│   │ go func() { counter++ }()  ──┘                           │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   Output with -race:                                            │
│   WARNING: DATA RACE                                            │
│   Write at 0x00c000... by goroutine X                          │
│   Previous write at 0x00c000... by goroutine Y                 │
│                                                                 │
│   ⚠️ Notes:                                                    │
│   • -race slows execution ~10x                                  │
│   • Use in CI/CD but maybe not in every local test             │
│   • Detects actual races, not potential ones                    │
│   • May miss races that don't occur during test run             │
└─────────────────────────────────────────────────────────────────┘
```

-race는 실행 속도를 약 10배 느리게 하므로, CI/CD 파이프라인에서 실행하고 로컬에서는 가끔 실행하는 것이 일반적입니다.

### 12. 병렬 테스트

t.Parallel()은 테스트를 병렬로 실행합니다. 독립적인 테스트들의 실행 시간을 줄일 수 있습니다.

```go
func TestA(t *testing.T) {
    t.Parallel()  // 첫 줄에 호출
    // 테스트 로직
}

func TestB(t *testing.T) {
    t.Parallel()
    // 테스트 로직
}
```

Table 테스트에서 병렬 실행 시 주의할 점이 있습니다. Go 1.21 이하에서는 루프 변수를 섀도잉해야 합니다.

```go
for _, tt := range tests {
    tt := tt  // Go 1.21 이하에서 필수!
    t.Run(tt.name, func(t *testing.T) {
        t.Parallel()
        // tt 사용
    })
}
```

Go 1.22부터는 루프 변수가 각 반복마다 새로 생성되므로 섀도잉이 불필요합니다.

---

## 비교표

### 테스트 메서드 비교

| 메서드 | 동작 | 사용 시점 |
|--------|------|----------|
| Error | 실패 기록, 계속 | 독립적 검증 여러 개 |
| Errorf | Error + 포맷팅 | 상세 메시지 |
| Fatal | 실패, 즉시 종료 | 이후 검증 무의미 |
| Fatalf | Fatal + 포맷팅 | 설정 실패 등 |
| Skip | 테스트 건너뛰기 | 조건부 실행 |
| Log | 출력 (-v 필요) | 디버그 정보 |

### 설정/정리 메커니즘 비교

| 기능 | 범위 | 자동 정리 | 용도 |
|------|------|----------|------|
| TestMain | 패키지 | 직접 구현 | DB 연결, 서버 시작 |
| t.Cleanup | 테스트 | 자동 | 파일, 리소스 정리 |
| t.TempDir | 테스트 | 자동 | 임시 디렉토리 |
| t.Setenv | 테스트 | 자동 복원 | 환경 변수 |

### 테스트 유형별 명령어

| 유형 | 함수 접두사 | 실행 명령어 |
|------|------------|------------|
| 단위 테스트 | Test | go test |
| 벤치마크 | Benchmark | go test -bench=. |
| 퍼징 | Fuzz | go test -fuzz=FuzzXxx |
| 예제 | Example | go test (자동) |

---

## 면접 예상 질문 및 모범 답안

### Q1. Go에서 Table 테스트 패턴이 무엇이고 왜 유용한가요?

**모범 답안:**

Table 테스트는 여러 테스트 케이스를 구조체 슬라이스로 정의하고 반복하여 실행하는 패턴입니다. 각 구조체는 입력, 기대 출력, 테스트 이름 등을 포함합니다.

```go
tests := []struct {
    name     string
    input    int
    expected int
}{
    {"positive", 5, 25},
    {"zero", 0, 0},
    {"negative", -3, 9},
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        result := Square(tt.input)
        if result != tt.expected {
            t.Errorf("got %d, want %d", result, tt.expected)
        }
    })
}
```

장점은 세 가지입니다. 첫째, 새 테스트 케이스를 추가하기 쉽습니다. 슬라이스에 항목만 추가하면 됩니다. 둘째, 테스트 로직 중복이 없습니다. 검증 코드가 한 번만 작성됩니다. 셋째, t.Run을 사용하면 각 케이스가 서브테스트가 되어 -run 플래그로 특정 케이스만 실행하거나 개별 실패를 확인할 수 있습니다.

단점은 복잡한 테스트 케이스에서 구조체가 커질 수 있다는 것입니다. 이 경우 관련 케이스를 별도 테스트로 분리하거나 헬퍼 함수를 사용합니다.

---

### Q2. t.Error와 t.Fatal의 차이점은 무엇이고, 각각 언제 사용해야 하나요?

**모범 답안:**

t.Error는 실패를 기록하지만 테스트를 계속 실행합니다. t.Fatal은 실패를 기록하고 테스트를 즉시 종료합니다.

t.Error를 사용해야 하는 경우는 여러 독립적인 조건을 검증할 때입니다. 예를 들어 구조체의 여러 필드를 검증하는 경우, 하나가 실패해도 나머지 필드를 계속 검증하면 모든 문제를 한 번에 파악할 수 있습니다.

```go
if user.Name == "" {
    t.Error("name is empty")
}
if user.Email == "" {
    t.Error("email is empty")
}
// 두 실패 모두 보고됨
```

t.Fatal을 사용해야 하는 경우는 이후 검증이 무의미하거나 패닉이 발생할 수 있을 때입니다. 예를 들어 설정 로드에 실패하면 이후 테스트가 nil 포인터 역참조로 패닉을 일으킬 수 있습니다.

```go
config, err := LoadConfig()
if err != nil {
    t.Fatal("cannot load config:", err)
}
// config가 nil이면 아래 코드가 패닉
value := config.Get("key")
```

원칙은 "더 많은 정보를 보여줄 수 있으면 Error, 계속할 의미가 없으면 Fatal"입니다.

---

### Q3. 코드 커버리지 100%가 왜 충분하지 않은가요? 더 나은 테스트 전략은 무엇인가요?

**모범 답안:**

코드 커버리지는 코드가 실행되었는지만 측정합니다. 올바르게 동작하는지는 측정하지 않습니다. 모든 라인을 실행해도 잘못된 결과를 검증하지 않으면 버그가 있을 수 있습니다.

예를 들어 정렬 함수를 테스트할 때 모든 코드 경로를 실행해도 결과가 정렬되었는지 확인하지 않으면 커버리지는 100%이지만 테스트는 무의미합니다.

더 나은 테스트 전략은 다음과 같습니다.

첫째, 경계값 테스트입니다. 빈 입력, 단일 요소, 최대/최소값, 경계 조건을 테스트합니다.

둘째, 에러 경로 테스트입니다. 에러가 발생하는 경우도 테스트하여 에러 처리가 올바른지 확인합니다.

셋째, 퍼징입니다. 자동 생성된 랜덤 입력으로 예상치 못한 버그를 발견합니다.

넷째, 속성 기반 테스트입니다. 결과가 만족해야 할 속성을 검증합니다. 정렬 결과는 정렬되어 있어야 하고, 원본과 같은 요소를 포함해야 합니다.

핵심은 커버리지를 목표로 삼지 않고, 중요한 동작과 엣지 케이스를 테스트하는 것입니다.

---

### Q4. Go의 퍼징(Fuzzing)은 무엇이고 어떤 종류의 버그를 발견하는 데 유용한가요?

**모범 답안:**

퍼징은 자동으로 생성된 랜덤 입력으로 함수를 반복 테스트하는 기법입니다. Go 1.18에서 표준 라이브러리에 추가되었습니다. 개발자가 예상하지 못한 입력 조합에서 발생하는 버그를 발견하는 데 유용합니다.

특히 유용한 경우는 파싱 함수, JSON/XML 역직렬화, 인코딩/디코딩, 문자열 처리 등입니다. 이런 함수들은 다양한 입력을 받을 수 있고, 특정 패턴에서만 실패하는 버그가 있을 수 있습니다.

```go
func FuzzJSON(f *testing.F) {
    f.Add([]byte(`{"name":"test"}`))  // 시드

    f.Fuzz(func(t *testing.T, data []byte) {
        var result map[string]any
        if err := json.Unmarshal(data, &result); err != nil {
            return  // 파싱 에러는 예상됨
        }

        // 다시 마샬링하면 같아야 함
        marshaled, err := json.Marshal(result)
        if err != nil {
            t.Error("marshal failed after successful unmarshal")
        }
        // ...
    })
}
```

퍼징이 발견하는 버그 유형은 패닉, 무한 루프, 메모리 오버플로우, 잘못된 경계 조건 처리 등입니다. 특히 round-trip 테스트(파싱 후 직렬화하면 동일해야 함)와 함께 사용하면 데이터 손실 버그도 발견할 수 있습니다.

---

### Q5. httptest 패키지를 사용하여 HTTP 클라이언트를 어떻게 테스트하나요?

**모범 답안:**

httptest.NewServer는 실제 HTTP 서버를 로컬에서 시작합니다. 테스트 대상 클라이언트가 이 서버에 요청을 보내고, 서버의 핸들러에서 요청을 검증하고 미리 정의된 응답을 반환합니다.

```go
func TestAPIClient(t *testing.T) {
    // 가짜 서버 생성
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // 요청 검증
        if r.Method != "GET" {
            t.Errorf("expected GET, got %s", r.Method)
        }
        if r.Header.Get("Authorization") == "" {
            w.WriteHeader(http.StatusUnauthorized)
            return
        }

        // 응답 반환
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
    }))
    defer server.Close()

    // 클라이언트에 테스트 서버 URL 주입
    client := NewClient(server.URL)
    result, err := client.Fetch()
    // 결과 검증
}
```

이 접근의 장점은 실제 HTTP 통신을 테스트하면서도 외부 서비스에 의존하지 않는다는 것입니다. 타임아웃, 재시도, 에러 처리 등 실제 네트워크 동작을 테스트할 수 있습니다.

테스트할 서비스가 내 코드라면 httptest.NewRecorder를 사용하여 HTTP 핸들러를 직접 테스트할 수도 있습니다.

---

### Q6. -race 플래그는 무엇을 탐지하고, 언제 사용해야 하나요?

**모범 답안:**

-race 플래그는 Go의 데이터 레이스 탐지기를 활성화합니다. 데이터 레이스는 두 개 이상의 goroutine이 동시에 같은 메모리에 접근하고, 그 중 하나 이상이 쓰기 작업일 때 발생합니다.

```go
var counter int

// 데이터 레이스!
go func() { counter++ }()
go func() { counter++ }()
```

탐지기는 테스트나 프로그램 실행 중 발생하는 실제 레이스를 탐지합니다. 특정 실행 경로에서 레이스가 발생하지 않으면 탐지하지 못할 수 있으므로, 충분한 커버리지를 가진 테스트와 함께 사용해야 합니다.

사용 시점에 대해서는, 로컬 개발에서 가끔 실행하고, CI/CD 파이프라인에서는 항상 실행하는 것이 좋습니다. -race는 실행 속도를 약 10배 느리게 하고 메모리를 더 사용하므로 프로덕션 빌드에는 포함하지 않습니다.

발견 시 대응은 sync.Mutex, sync/atomic, 채널 등을 사용하여 동기화를 추가하는 것입니다. 레이스는 간헐적으로 발생하고 재현하기 어려우므로, 발견 즉시 수정해야 합니다.

---

## 실무 체크리스트

### 기본 테스트
- [ ] 테스트 파일은 _test.go 접미사를 사용하는가?
- [ ] 테스트 함수는 Test로 시작하는가?
- [ ] Error와 Fatal을 적절히 구분하는가?
- [ ] 테스트 데이터는 testdata/ 디렉토리에 있는가?

### Table 테스트
- [ ] 반복적인 테스트 케이스에 Table 패턴을 사용하는가?
- [ ] t.Run으로 서브테스트를 생성하는가?
- [ ] 테스트 케이스 이름이 명확한가?
- [ ] 에러 케이스도 테스트하는가?

### Setup/Teardown
- [ ] 패키지 레벨 설정에 TestMain을 사용하는가?
- [ ] 테스트별 정리에 t.Cleanup을 사용하는가?
- [ ] 임시 파일/디렉토리에 t.TempDir을 사용하는가?
- [ ] 환경 변수에 t.Setenv를 사용하는가?

### 고급 테스트
- [ ] 커버리지를 측정하고 분석하는가?
- [ ] 파싱/역직렬화에 퍼징을 사용하는가?
- [ ] 성능 민감 코드에 벤치마크가 있는가?
- [ ] CI에서 -race 플래그를 사용하는가?

### 테스트 더블
- [ ] 외부 의존성에 인터페이스를 사용하는가?
- [ ] Stub/Mock이 테스트 의도를 명확히 표현하는가?
- [ ] HTTP 테스트에 httptest를 사용하는가?

---

## 참고 자료

- [testing 패키지 공식 문서](https://pkg.go.dev/testing)
- [Go Fuzzing 공식 문서](https://go.dev/security/fuzz/)
- [Data Race Detector](https://go.dev/doc/articles/race_detector)
- [go-cmp 라이브러리](https://github.com/google/go-cmp)
- [testify 라이브러리](https://github.com/stretchr/testify)
- [Table Driven Tests](https://go.dev/wiki/TableDrivenTests)
