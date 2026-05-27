# Stage 01: Go 기초

**주제**: Go 언어 기본 문법과 핵심 개념

**목표**: 강타입 시스템, 포인터, 인터페이스, I/O를 이해하고 활용

---

## 학습 목표

- [x] 타입 시스템과 Zero Value 이해
- [x] 포인터 vs 값 전달 차이
- [x] 인터페이스와 리시버 관계
- [ ] I/O 인터페이스 활용 (io.Reader, io.Writer)
- [ ] 버퍼링과 스트리밍 처리

---

## 핵심 개념

### 1. 타입 시스템

Go는 강타입 언어입니다. 같은 기반 타입이라도 다른 타입으로 취급됩니다.

```go
type Status string

var s1 Status = "active"
var s2 string = "active"

// s1 = s2  // 컴파일 에러! 다른 타입
s1 = Status(s2)  // 명시적 형변환 필요
```

### 2. Zero Value

모든 타입에 기본값이 정해져 있습니다 (커스텀 기본값 불가).

| 타입 | Zero Value |
|------|------------|
| `string` | `""` |
| `int` | `0` |
| `bool` | `false` |
| `[]T` (slice) | `nil` |
| `map[K]V` | `nil` |
| `*T` (pointer) | `nil` |
| `struct` | 모든 필드가 각자의 zero value |

**커스텀 기본값이 필요하면 생성자 함수 사용**:
```go
func NewConfig() *Config {
    return &Config{Token: "default"}
}
```

### 3. 포인터 vs 값

#### 포인터를 사용하는 3가지 이유

| 이유 | 값 전달 | 포인터 전달 |
|------|---------|------------|
| 원본 수정 | 복사본만 수정 | 원본 수정 가능 |
| 메모리 효율 | 전체 복사 | 주소만 복사 (8바이트) |
| nil 체크 | 불가능 | `if ptr == nil` 가능 |

#### 메서드 Receiver

```go
// Pointer Receiver - 원본 수정 가능, 대부분 이 방식 사용
func (c *Config) Validate() error { ... }

// Value Receiver - 복사본으로 작업
func (c Config) String() string { ... }
```

**관례**: 한 타입의 모든 메서드는 같은 receiver 타입 사용 (일관성)

### 4. 인터페이스와 리시버의 관계

```go
type Greeter interface {
    Greet() string
}

// 포인터 리시버로 정의
func (p *Person) Greet() string { return "Hello" }

// 규칙: 포인터 리시버 → *T만 인터페이스 구현
var g1 Greeter = &Person{}  // OK: *Person은 Greeter
var g2 Greeter = Person{}   // 컴파일 에러! Person은 Greeter 아님
```

| 리시버 타입 | T가 인터페이스 구현? | *T가 인터페이스 구현? |
|------------|---------------------|----------------------|
| 값 `(c T)` | O | O |
| 포인터 `(c *T)` | X | O |

---

## I/O 심화

### io.Reader와 io.Writer

Go의 I/O는 두 핵심 인터페이스를 중심으로 설계되었습니다.

```go
// 가장 기본적인 인터페이스
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}
```

**핵심 원칙**: 모든 데이터 소스(파일, 네트워크, 메모리)가 동일한 인터페이스 구현

### bytes.Buffer

메모리에서 바이트를 읽고 쓰는 가변 크기 버퍼입니다.

```go
import "bytes"

// 생성 방법
var buf bytes.Buffer                    // 빈 버퍼
buf := bytes.NewBufferString("hello")   // 문자열로 초기화
buf := bytes.NewBuffer([]byte{1, 2, 3}) // 바이트로 초기화

// 쓰기
buf.WriteString("hello")
buf.WriteByte('!')
buf.Write([]byte{1, 2, 3})

// 읽기
data, _ := buf.ReadBytes('\n')   // 구분자까지 읽기
line, _ := buf.ReadString('\n')  // 문자열로 읽기
buf.Read(p)                      // 바이트 슬라이스로 읽기

// 변환
str := buf.String()              // 문자열로
data := buf.Bytes()              // 바이트로
```

### bufio - 버퍼링 I/O

성능 향상을 위한 버퍼링 레이어를 제공합니다.

```go
import "bufio"

// Reader 래핑
reader := bufio.NewReader(file)
reader := bufio.NewReaderSize(file, 64*1024)  // 64KB 버퍼

// 한 줄 읽기
line, err := reader.ReadString('\n')

// Scanner - 토큰 단위 읽기
scanner := bufio.NewScanner(file)
for scanner.Scan() {
    fmt.Println(scanner.Text())
}

// Writer 래핑
writer := bufio.NewWriter(file)
writer.WriteString("hello")
writer.Flush()  // 반드시 Flush 호출!
```

#### Scanner 분리 함수

```go
scanner := bufio.NewScanner(reader)

// 내장 분리 함수
scanner.Split(bufio.ScanLines)  // 줄 단위 (기본값)
scanner.Split(bufio.ScanWords)  // 단어 단위
scanner.Split(bufio.ScanBytes)  // 바이트 단위
scanner.Split(bufio.ScanRunes)  // 룬 단위 (UTF-8)
```

### strings.Reader

문자열을 io.Reader로 변환합니다.

```go
import "strings"

reader := strings.NewReader("hello world")

// io.Reader 인터페이스 구현
data := make([]byte, 5)
n, _ := reader.Read(data)  // n=5, data="hello"
```

### os.File 조작

```go
import "os"

// 파일 열기
file, err := os.Open("input.txt")           // 읽기 전용
file, err := os.Create("output.txt")        // 쓰기 전용 (생성/덮어쓰기)
file, err := os.OpenFile("log.txt",         // 세밀한 제어
    os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
defer file.Close()

// 읽기
data, err := io.ReadAll(file)               // 전체 읽기
n, err := file.Read(buf)                    // 버퍼로 읽기

// 쓰기
n, err := file.Write([]byte("hello"))
n, err := file.WriteString("world")
```

### io 유틸리티 함수

```go
import "io"

// 복사
io.Copy(dst, src)                // src → dst 전체 복사
io.CopyN(dst, src, n)            // n 바이트만 복사
io.CopyBuffer(dst, src, buf)     // 제공된 버퍼 사용

// 전체 읽기
data, err := io.ReadAll(reader)  // 끝까지 읽기

// 조합
reader := io.MultiReader(r1, r2, r3)  // 여러 Reader 연결
writer := io.MultiWriter(w1, w2)      // 여러 Writer에 동시 쓰기
reader := io.TeeReader(r, w)          // 읽으면서 동시에 쓰기
```

### io.Pipe

고루틴 간 동기식 파이프를 생성합니다.

```go
import "io"

reader, writer := io.Pipe()

// 쓰기 고루틴
go func() {
    defer writer.Close()
    writer.Write([]byte("hello"))
}()

// 읽기 (메인 또는 다른 고루틴)
data, _ := io.ReadAll(reader)
```

**사용 사례**: 스트리밍 처리, 생산자-소비자 패턴

### 실용 예제: 파일 복사

```go
func CopyFile(src, dst string) error {
    srcFile, err := os.Open(src)
    if err != nil {
        return err
    }
    defer srcFile.Close()

    dstFile, err := os.Create(dst)
    if err != nil {
        return err
    }
    defer dstFile.Close()

    _, err = io.Copy(dstFile, srcFile)
    return err
}
```

### 실용 예제: 라인 처리

```go
func ProcessLines(r io.Reader) error {
    scanner := bufio.NewScanner(r)
    for scanner.Scan() {
        line := scanner.Text()
        // 각 라인 처리
        fmt.Println(line)
    }
    return scanner.Err()
}
```

---

## 파일 구조

```
01-basics/
├── config.go    # 설정 구조체, Sentinel Error
├── main.go      # 테스트 코드
├── types.go     # 커스텀 타입
├── LEARNED.md   # 학습 회고
└── README.md    # 학습 가이드 (현재 파일)
```

---

## 참조 자료

- [Effective Go](https://go.dev/doc/effective_go)
- [Go io 패키지](https://pkg.go.dev/io)
- [Go bufio 패키지](https://pkg.go.dev/bufio)

### Learning Go, 2nd Edition 참조
- **05_Functions.md**: 포인터 vs 값 전달
- **07_Types_Methods_and_Interfaces.md**: 타입, 메서드, 인터페이스
- **13_The_Standard_Library.md**: io, bytes, strings 패키지

---

## 다음 단계

- **Stage 02: Interfaces** - 인터페이스 심화
- **Stage 03: Errors** - 에러 처리 패턴
