# 02. CLI와 환경 변수 (flag & os 패키지)

## 학습 목표
Go의 flag 패키지로 CLI 옵션을 파싱하고, 환경 변수를 다루는 방법을 이해한다.

---

## CLI 구성 요소

```bash
./program command -option value argument
          │       │       │     │
          │       │       │     └─ 인자 (대상)
          │       │       └─ 옵션 값
          │       └─ 옵션/플래그
          └─ 서브커맨드
```

| 요소 | 예시 | 설명 |
|------|------|------|
| 커맨드 | `git commit` | 무엇을 할지 (동사) |
| 옵션/플래그 | `-m "msg"` | 어떻게 할지 (설정) |
| 인자 | `file.txt` | 대상 (파일, 값 등) |

---

## flag 패키지 핵심

### 1. 전역 FlagSet vs NewFlagSet

> **면접 답변**: Go의 flag 패키지는 두 가지 방식으로 사용할 수 있습니다. `flag.String()`처럼 전역 함수를 사용하면 프로그램 전체에서 하나의 플래그 세트를 공유하며, `os.Args[1:]`을 자동으로 파싱합니다. 반면 `flag.NewFlagSet()`은 독립적인 플래그 세트를 생성하여 서브커맨드별로 다른 플래그를 정의할 수 있고, 파싱할 인자 슬라이스를 직접 지정할 수 있습니다.

```go
// 전역 FlagSet - 단순 CLI
pattern := flag.String("pattern", "", "설명")
flag.Parse()

// NewFlagSet - 서브커맨드용
fs := flag.NewFlagSet("list", flag.ExitOnError)
filter := fs.String("filter", "", "설명")
fs.Parse(args)
```

| 방식 | 용도 | 파싱 대상 |
|------|------|----------|
| `flag.String()` | 단일 명령 CLI | `os.Args[1:]` 자동 |
| `fs.String()` | 서브커맨드 CLI | 직접 지정 |

### 2. 플래그 타입

> **면접 답변**: flag 패키지의 `String()`, `Int()`, `Bool()` 함수들은 값이 아닌 포인터를 반환합니다. 이는 `flag.Parse()` 호출 시점에 실제 값이 파싱되어 해당 포인터가 가리키는 메모리에 저장되기 때문입니다. 따라서 값에 접근할 때는 `*name`처럼 역참조가 필요합니다.

```go
// 포인터 반환 - 값 접근 시 * 필요
name := flag.String("name", "default", "설명")
count := flag.Int("count", 1, "설명")
verbose := flag.Bool("v", false, "설명")

flag.Parse()

fmt.Println(*name)   // 포인터이므로 * 사용
fmt.Println(*count)
fmt.Println(*verbose)
```

### 3. flag.Args() - 플래그가 아닌 인자들

> **면접 답변**: `flag.Parse()` 호출 후 `flag.Args()`를 사용하면 플래그로 파싱되지 않은 나머지 인자들을 슬라이스로 얻을 수 있습니다. 예를 들어 `./grep -pattern "ERROR" file.txt`에서 `-pattern "ERROR"`는 플래그로 처리되고, `file.txt`는 `flag.Args()[0]`으로 접근할 수 있습니다.

```bash
./grep -pattern "ERROR" file.txt
       └─ 플래그 ────┘  └─ 인자
```

```go
pattern := flag.String("pattern", "", "")
flag.Parse()

args := flag.Args()  // ["file.txt"]
filename := args[0]
```

---

## 주의: 파싱 순서

> **면접 답변**: Go의 flag 패키지는 POSIX 스타일이 아닌 자체 파싱 규칙을 따릅니다. non-flag 인자(하이픈으로 시작하지 않는 인자)가 나오면 그 이후의 모든 인자는 플래그로 인식하지 않고 파싱을 중단합니다. 따라서 플래그는 반드시 일반 인자보다 앞에 위치해야 합니다.

```bash
# ❌ 잘못된 순서
./envtool get HOME --default localhost
#             └─ non-flag → 이후 파싱 중단

# ✅ 올바른 순서
./envtool get --default localhost HOME
#             └─ 플래그 먼저 ────┘ └─ 인자
```

---

## 주의: args vs fs.Args()

> **면접 답변**: `NewFlagSet`을 사용할 때 흔히 하는 실수가 있습니다. `fs.Parse(args)` 호출 후에는 반드시 `fs.Args()`로 파싱되지 않은 인자에 접근해야 합니다. 원본 `args` 슬라이스를 그대로 사용하면 플래그 이름이나 값이 인자로 잘못 처리될 수 있습니다.

```go
func cmdGet(args []string) {
    fs := flag.NewFlagSet("get", flag.ExitOnError)
    defaultVal := fs.String("default", "", "")
    fs.Parse(args)

    remaining := fs.Args()

    // args = ["--default", "localhost", "HOME"]  (원본)
    // remaining = ["HOME"]                        (파싱 후 남은 것)

    key := remaining[0]  // ✅ 올바름
    key := args[0]       // ❌ "--default"가 됨
}
```

---

## 환경 변수

### os.Getenv vs os.LookupEnv

> **면접 답변**: 환경 변수를 읽을 때 `os.Getenv()`는 변수가 없으면 빈 문자열을 반환하므로, 실제로 빈 값이 설정된 것인지 변수가 없는 것인지 구분할 수 없습니다. `os.LookupEnv()`는 값과 함께 존재 여부를 bool로 반환하므로, 환경 변수의 존재 여부를 명확히 확인해야 할 때 사용합니다.

```go
// Getenv: 없으면 빈 문자열
value := os.Getenv("KEY")
// "" → 존재 안 함? 빈 값? 구분 불가

// LookupEnv: 존재 여부 확인 가능
value, exists := os.LookupEnv("KEY")
if !exists {
    // 환경 변수가 없음
}
```

### 환경 변수 전체 조회

```go
envs := os.Environ()  // ["KEY1=value1", "KEY2=value2", ...]

for _, env := range envs {
    parts := strings.SplitN(env, "=", 2)
    key, value := parts[0], parts[1]
}
```

---

## 출력: stdout vs stderr

> **면접 답변**: Unix 철학에서 stdout은 프로그램의 정상적인 출력 결과를, stderr는 에러 메시지나 진행 상황 같은 부가 정보를 출력하는 데 사용합니다. 이렇게 분리하면 파이프나 리다이렉션으로 결과만 파일로 저장하면서 에러는 화면에 표시할 수 있습니다. Go에서는 `fmt.Println()`이 stdout으로, `fmt.Fprintln(os.Stderr, ...)`가 stderr로 출력합니다.

```go
fmt.Println("결과")                    // stdout - 정상 출력
fmt.Fprintln(os.Stderr, "에러!")       // stderr - 에러 출력
```

```bash
./program > output.txt   # stdout만 파일로
./program 2> error.txt   # stderr만 파일로
```

**규칙**: 결과는 stdout, 에러/진행상황은 stderr

---

## 프로그램 종료

> **면접 답변**: `os.Exit()`은 프로그램을 즉시 종료시키며, 종료 코드 0은 성공, 1 이상은 실패를 의미합니다. 주의할 점은 `os.Exit()` 호출 시 defer로 등록된 함수들이 실행되지 않는다는 것입니다. 이는 defer가 함수의 정상적인 반환 시점에 실행되는데, `os.Exit()`은 프로세스를 강제 종료하기 때문입니다. 이 문제를 해결하려면 main에서 직접 Exit을 호출하지 않고, 별도 함수에서 error를 반환하는 패턴을 사용합니다.

```go
os.Exit(0)  // 성공
os.Exit(1)  // 실패

// 주의: os.Exit()은 defer 실행 안 함!
func main() {
    defer cleanup()  // 실행 안 됨!
    os.Exit(1)
}

// 해결: run 패턴
func main() {
    if err := run(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}

func run() error {
    defer cleanup()  // 정상 실행됨
    // ...
    return nil
}
```

---

## 실습 결과

### 01-grep: 전역 FlagSet 사용

```go
pattern := flag.String("pattern", "", "검색 패턴")
showLineNum := flag.Bool("n", false, "줄 번호")
ignoreCase := flag.Bool("i", false, "대소문자 무시")
invert := flag.Bool("v", false, "반전")
flag.Parse()

filename := flag.Args()[0]
```

```bash
./grep -pattern "ERROR" -i -n sample.txt
```

### 02-envtool: NewFlagSet으로 서브커맨드

```go
switch os.Args[1] {
case "list":
    fs := flag.NewFlagSet("list", flag.ExitOnError)
    filter := fs.String("filter", "", "")
    fs.Parse(os.Args[2:])
case "get":
    fs := flag.NewFlagSet("get", flag.ExitOnError)
    defaultVal := fs.String("default", "", "")
    fs.Parse(os.Args[2:])
    key := fs.Args()[0]  // ✅ args가 아닌 fs.Args()
}
```

```bash
./envtool list -filter PATH
./envtool get -default localhost DB_HOST
```

---

## 정리: 언제 무엇을 쓰나?

| 상황 | 선택 |
|------|------|
| 단순 CLI (옵션만) | `flag.String()` + `flag.Parse()` |
| 서브커맨드 필요 | `flag.NewFlagSet()` + switch |
| 복잡한 CLI | Cobra 라이브러리 |

---

## 참고 자료
- [Go Package - flag](https://pkg.go.dev/flag)
- [Go Package - os](https://pkg.go.dev/os)
