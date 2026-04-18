# Chapter 16: Reflect, Unsafe, and Cgo - 면접정리

## 핵심 개념 상세 설명

### 1. Reflection: 런타임 타입 검사와 조작

Go는 정적 타입 언어이지만, reflect 패키지를 통해 런타임에 타입을 검사하고 값을 조작할 수 있습니다. 이는 컴파일 시점에 타입을 알 수 없는 상황에서 유용합니다. encoding/json의 마샬링/언마샬링, database/sql의 레코드 매핑, fmt 패키지의 타입별 출력 등이 reflection을 사용합니다.

reflection의 핵심은 두 가지 함수입니다. reflect.TypeOf는 타입 정보를 반환하고, reflect.ValueOf는 값 정보를 반환합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Reflection Overview                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   var x int = 42                                                │
│                                                                 │
│   reflect.TypeOf(x)                reflect.ValueOf(x)           │
│         │                                │                      │
│         ▼                                ▼                      │
│   ┌─────────────┐                  ┌─────────────┐              │
│   │ reflect.Type│                  │reflect.Value│              │
│   │             │                  │             │              │
│   │ Name(): "int"                  │ Int(): 42   │              │
│   │ Kind(): Int │                  │ Kind(): Int │              │
│   │ Size(): 8   │                  │ Type(): Type│              │
│   └─────────────┘                  └─────────────┘              │
│                                                                 │
│   When to use:                                                  │
│   • Data marshaling/unmarshaling (JSON, XML, CSV)               │
│   • Database record mapping                                     │
│   • Generic-like behavior before Go 1.18                        │
│   • Framework/library internals                                 │
│                                                                 │
│   ⚠️ Trade-offs:                                               │
│   • 50-75x slower than direct code                              │
│   • No compile-time type checking                               │
│   • Can panic at runtime                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Type과 Kind의 차이

reflection에서 Type과 Kind는 다른 개념입니다. Type은 타입의 이름(예: "MyStruct", "int")이고, Kind는 타입의 기본 분류(예: reflect.Struct, reflect.Int)입니다.

```go
type Person struct {
    Name string
    Age  int
}

p := Person{Name: "Alice", Age: 30}
t := reflect.TypeOf(p)

fmt.Println(t.Name())  // "Person"
fmt.Println(t.Kind())  // reflect.Struct

// 포인터의 경우
pt := reflect.TypeOf(&p)
fmt.Println(pt.Name())  // "" (포인터는 이름 없음)
fmt.Println(pt.Kind())  // reflect.Pointer
fmt.Println(pt.Elem().Name())  // "Person" (가리키는 타입)
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    Type vs Kind                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   type MyInt int                                                │
│   type Person struct { Name string; Age int }                   │
│   type Handler func(string) error                               │
│                                                                 │
│   ┌──────────────┬───────────────┬─────────────────────┐        │
│   │    Value     │    Name()     │      Kind()         │        │
│   ├──────────────┼───────────────┼─────────────────────┤        │
│   │ MyInt(42)    │ "MyInt"       │ reflect.Int         │        │
│   │ Person{}     │ "Person"      │ reflect.Struct      │        │
│   │ Handler(...) │ "Handler"     │ reflect.Func        │        │
│   │ &Person{}    │ ""            │ reflect.Pointer     │        │
│   │ []int{}      │ ""            │ reflect.Slice       │        │
│   │ map[s]int{}  │ ""            │ reflect.Map         │        │
│   └──────────────┴───────────────┴─────────────────────┘        │
│                                                                 │
│   Kind tells you WHAT it is (struct, int, pointer, etc.)        │
│   Name tells you HOW it's defined (custom type name or "")      │
│                                                                 │
│   Elem() - gets the element type for:                           │
│   • Pointer → pointed-to type                                   │
│   • Slice/Array → element type                                  │
│   • Map → value type (use Key() for key type)                   │
│   • Channel → element type                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 3. 값 읽기와 설정

reflect.ValueOf로 얻은 Value에서 실제 값을 읽으려면 Int(), String(), Bool() 등의 메서드를 사용합니다. 값을 설정하려면 세 가지 조건이 필요합니다. 첫째, ValueOf에 포인터를 전달해야 합니다. 둘째, Elem()으로 실제 값에 접근해야 합니다. 셋째, SetInt(), SetString() 등으로 설정합니다.

```go
// 값 읽기
x := 42
v := reflect.ValueOf(x)
fmt.Println(v.Int())  // 42

// 값 설정 (포인터 필수)
v = reflect.ValueOf(&x)
v.Elem().SetInt(100)
fmt.Println(x)  // 100

// 구조체 필드 설정
type Data struct {
    Value int
}
d := Data{Value: 10}
dv := reflect.ValueOf(&d).Elem()
field := dv.FieldByName("Value")
if field.CanSet() {
    field.SetInt(20)
}
fmt.Println(d.Value)  // 20
```

CanSet()은 값이 수정 가능한지 확인합니다. unexported 필드나 비포인터로 전달된 값은 수정할 수 없습니다.

### 4. 구조체 필드와 태그 접근

reflection으로 구조체 필드를 순회하고 struct tag를 읽을 수 있습니다. 이는 JSON, XML, CSV 마샬링 라이브러리의 핵심 기능입니다.

```go
type User struct {
    ID    int    `json:"id" db:"user_id"`
    Name  string `json:"name" db:"user_name"`
    Email string `json:"email,omitempty"`
}

t := reflect.TypeOf(User{})
for i := 0; i < t.NumField(); i++ {
    field := t.Field(i)
    fmt.Printf("Field: %s, Type: %s\n", field.Name, field.Type)
    fmt.Printf("  json tag: %s\n", field.Tag.Get("json"))
    fmt.Printf("  db tag: %s\n", field.Tag.Get("db"))
}
```

### 5. unsafe 패키지: 메모리 직접 조작

unsafe 패키지는 Go의 타입 안전성을 우회하여 메모리를 직접 조작할 수 있게 합니다. 성능이 극도로 중요하거나 시스템 프로그래밍에서 사용됩니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    unsafe Package                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Key Functions:                                                │
│   • unsafe.Sizeof(x)    - Size of x in bytes                    │
│   • unsafe.Alignof(x)   - Alignment requirement                 │
│   • unsafe.Offsetof(x.f) - Offset of field f in struct x        │
│   • unsafe.Pointer      - Generic pointer type                  │
│                                                                 │
│   Memory Layout Example:                                        │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  type BoolInt struct {                                  │   │
│   │      b bool   // 1 byte                                 │   │
│   │      // 7 bytes padding (alignment for int64)           │   │
│   │      i int64  // 8 bytes                                │   │
│   │  }  // Total: 16 bytes                                  │   │
│   │                                                         │   │
│   │  type BoolBoolInt struct {                              │   │
│   │      b1 bool  // 1 byte                                 │   │
│   │      b2 bool  // 1 byte                                 │   │
│   │      // 6 bytes padding                                 │   │
│   │      i int64  // 8 bytes                                │   │
│   │  }  // Total: 16 bytes (same, better packing!)          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   Field ordering affects struct size!                           │
│   Group same-size fields together to minimize padding.          │
└─────────────────────────────────────────────────────────────────┘
```

### 6. unsafe.Pointer를 통한 타입 변환

unsafe.Pointer는 모든 포인터 타입과 uintptr 사이의 변환을 허용합니다. 이를 통해 타입 시스템을 우회하여 바이트 단위로 데이터를 해석할 수 있습니다.

```go
// 바이트 배열을 구조체로 변환 (zero-copy)
type Header struct {
    Magic   uint32
    Version uint16
    Flags   uint16
}

func ParseHeader(data [8]byte) Header {
    return *(*Header)(unsafe.Pointer(&data))
}

// 슬라이스를 다른 타입 슬라이스로 변환
func Int32SliceToBytes(s []int32) []byte {
    header := (*reflect.SliceHeader)(unsafe.Pointer(&s))
    return *(*[]byte)(unsafe.Pointer(&reflect.SliceHeader{
        Data: header.Data,
        Len:  header.Len * 4,
        Cap:  header.Cap * 4,
    }))
}
```

unsafe를 사용한 코드는 약 2-3배 빠를 수 있지만, 엔디안 문제, 메모리 정렬 문제, 가비지 컬렉션 문제가 발생할 수 있습니다.

### 7. cgo: C 코드 통합

cgo는 Go 프로그램에서 C 코드를 호출하거나 Go 함수를 C에서 호출할 수 있게 합니다. 기존 C 라이브러리를 활용하거나 시스템 API에 접근할 때 사용합니다.

```go
package main

/*
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 인라인 C 함수
int add(int a, int b) {
    return a + b;
}
*/
import "C"

import (
    "fmt"
    "unsafe"
)

func main() {
    // C 함수 호출
    sum := C.add(3, 4)
    fmt.Println(sum)  // 7

    // C 표준 라이브러리 호출
    result := C.sqrt(100)
    fmt.Println(result)  // 10

    // C 문자열 사용
    cStr := C.CString("Hello")
    defer C.free(unsafe.Pointer(cStr))
    C.puts(cStr)
}
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    cgo Considerations                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Performance Overhead:                                         │
│   • C function call from Go: ~40ns overhead                     │
│   • About 29x slower than C-to-C call                           │
│   • NOT for performance optimization!                           │
│                                                                 │
│   Restrictions:                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ ✗ Cannot pass Go pointers containing Go pointers to C   │   │
│   │ ✗ C cannot store Go pointers after function returns     │   │
│   │ ✗ Cannot call C variadic functions directly             │   │
│   │ ✗ C unions become byte arrays in Go                     │   │
│   │ ✗ Cannot call C function pointers directly              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   When to use cgo:                                              │
│   ✓ Integrating existing C libraries (OpenSSL, SQLite, etc.)   │
│   ✓ System APIs not available in Go                            │
│   ✓ Hardware access requiring C drivers                        │
│                                                                 │
│   When NOT to use cgo:                                          │
│   ✗ Performance optimization (Go is usually fast enough)       │
│   ✗ When a pure Go alternative exists                          │
│   ✗ Cross-compilation requirements (cgo complicates this)      │
└─────────────────────────────────────────────────────────────────┘
```

### 8. cgo.Handle: Go 포인터 전달

Go의 가비지 컬렉터 때문에 Go 포인터를 C에 직접 전달할 수 없습니다. cgo.Handle을 사용하면 Go 값을 정수 핸들로 변환하여 C에 전달하고, 나중에 다시 Go 값으로 복원할 수 있습니다.

```go
import "runtime/cgo"

type Data struct {
    Message string
    Count   int
}

func main() {
    d := Data{Message: "Hello", Count: 42}

    // Go 값을 핸들로 변환
    handle := cgo.NewHandle(d)
    defer handle.Delete()  // 반드시 삭제!

    // C 함수에 핸들 전달
    C.process(C.uintptr_t(handle))
}

//export callback
func callback(h C.uintptr_t) {
    handle := cgo.Handle(h)
    d := handle.Value().(Data)
    fmt.Println(d.Message, d.Count)
}
```

### 9. Reflection 성능 비용

reflection은 편리하지만 상당한 성능 비용이 있습니다. 동일한 작업을 직접 코드나 제네릭으로 구현하는 것보다 50-75배 느릴 수 있습니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Reflection Performance                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Benchmark Results (filtering 1000 strings):                   │
│                                                                 │
│   FilterReflect    203,962 ns/op   46,616 B/op   2219 allocs    │
│   FilterGeneric      3,920 ns/op   16,384 B/op      1 allocs    │
│   FilterDirect       3,885 ns/op   16,384 B/op      1 allocs    │
│                                                                 │
│   Reflection is ~52x slower!                                    │
│                                                                 │
│   Why reflection is slow:                                       │
│   • Runtime type checking                                       │
│   • Cannot be inlined by compiler                               │
│   • Many small allocations                                      │
│   • No compiler optimizations                                   │
│                                                                 │
│   Decision guide:                                               │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ Q: Can I use generics instead?                          │   │
│   │    Yes → Use generics (fast, type-safe)                 │   │
│   │    No  → Is this at program boundary?                   │   │
│   │          Yes → Reflection OK (JSON, DB, etc.)           │   │
│   │          No  → Reconsider design                        │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 비교표

### Reflection 메서드 비교

| 메서드 | 대상 | 반환 | 용도 |
|--------|------|------|------|
| TypeOf | 값 | Type | 타입 정보 획득 |
| ValueOf | 값 | Value | 값 정보 획득 |
| Type.Name() | Type | string | 타입 이름 |
| Type.Kind() | Type | Kind | 기본 분류 |
| Type.Elem() | Type | Type | 포인터/슬라이스 요소 타입 |
| Value.Int() | Value | int64 | 정수값 읽기 |
| Value.SetInt() | Value | - | 정수값 설정 |
| Value.Interface() | Value | any | 원래 값으로 복원 |

### unsafe 함수 비교

| 함수 | 용도 | 반환 |
|------|------|------|
| Sizeof(x) | 타입 크기 | uintptr |
| Alignof(x) | 정렬 요구사항 | uintptr |
| Offsetof(x.f) | 필드 오프셋 | uintptr |
| Pointer | 범용 포인터 | unsafe.Pointer |
| Add(ptr, len) | 포인터 연산 | unsafe.Pointer |
| Slice(ptr, len) | 슬라이스 생성 | []T |

### reflect vs unsafe vs cgo 비교

| 특성 | reflect | unsafe | cgo |
|------|---------|--------|-----|
| 타입 안전성 | 런타임 체크 | 없음 | 부분적 |
| 성능 | 느림 (50-75x) | 빠름 | 느림 (40ns/call) |
| 사용 사례 | 마샬링, 프레임워크 | 바이너리, 최적화 | C 통합 |
| 위험성 | 런타임 패닉 | 메모리 손상 | 복잡성 |

---

## 면접 예상 질문 및 모범 답안

### Q1. Go에서 reflection이 무엇이고 언제 사용해야 하나요?

**모범 답안:**

reflection은 런타임에 타입을 검사하고 값을 조작하는 기능입니다. reflect 패키지의 TypeOf와 ValueOf 함수가 핵심입니다. 컴파일 시점에 타입을 알 수 없는 상황에서 사용합니다.

주요 사용 사례는 프로그램 경계에서의 데이터 변환입니다. encoding/json은 임의의 구조체를 JSON으로 변환할 때 reflection을 사용합니다. database/sql은 쿼리 결과를 구조체에 매핑할 때 사용합니다. fmt.Printf는 어떤 타입이든 출력할 수 있도록 reflection을 사용합니다.

단점은 성능과 타입 안전성입니다. reflection은 직접 코드보다 50-75배 느립니다. 또한 컴파일 시점에 타입 오류를 잡을 수 없어 런타임에 패닉이 발생할 수 있습니다.

Go 1.18 이후에는 많은 경우 제네릭이 reflection을 대체할 수 있습니다. 제네릭이 가능하면 제네릭을 사용하고, 외부 데이터와의 경계에서만 reflection을 사용하는 것이 좋습니다.

---

### Q2. reflect.Type의 Name()과 Kind()의 차이점을 설명해주세요.

**모범 답안:**

Name()은 타입의 이름을 반환합니다. 사용자 정의 타입이면 그 이름이, 익명 타입(포인터, 슬라이스, 맵 등)이면 빈 문자열이 반환됩니다.

Kind()는 타입의 기본 분류를 반환합니다. reflect.Int, reflect.Struct, reflect.Pointer 등의 상수입니다. 사용자 정의 타입이든 기본 타입이든 그 근본 종류를 나타냅니다.

```go
type MyInt int
type Person struct { Name string }

// MyInt
t := reflect.TypeOf(MyInt(0))
t.Name()  // "MyInt"
t.Kind()  // reflect.Int

// Person
t = reflect.TypeOf(Person{})
t.Name()  // "Person"
t.Kind()  // reflect.Struct

// *Person (포인터)
t = reflect.TypeOf(&Person{})
t.Name()  // "" (익명)
t.Kind()  // reflect.Pointer
t.Elem().Name()  // "Person"
```

Kind()는 어떤 연산이 가능한지 판단할 때 사용합니다. 예를 들어 순회가 필요하면 Kind()가 Slice, Array, Map인지 확인합니다. Name()은 특정 사용자 정의 타입인지 확인할 때 사용합니다.

---

### Q3. reflection으로 값을 설정하려면 왜 포인터가 필요한가요?

**모범 답안:**

Go는 call by value입니다. 함수에 값을 전달하면 복사본이 전달됩니다. reflect.ValueOf(x)를 호출하면 x의 복사본이 만들어지고, 그 복사본의 Value가 반환됩니다. 이 Value를 수정해도 원본 x에는 영향이 없습니다.

원본을 수정하려면 포인터를 전달해야 합니다. reflect.ValueOf(&x)는 x를 가리키는 포인터의 Value를 반환합니다. Elem()을 호출하면 포인터가 가리키는 실제 값의 Value를 얻고, 이를 수정하면 원본이 수정됩니다.

```go
x := 10

// 이렇게 하면 수정 불가
v := reflect.ValueOf(x)
v.SetInt(20)  // panic: reflect.Value.SetInt using unaddressable value

// 포인터로 전달해야 수정 가능
v = reflect.ValueOf(&x)
v.Elem().SetInt(20)
fmt.Println(x)  // 20
```

CanSet() 메서드로 수정 가능한지 확인할 수 있습니다. unexported 필드도 수정할 수 없어서 CanSet()이 false를 반환합니다.

---

### Q4. unsafe 패키지는 언제 사용하고, 어떤 위험이 있나요?

**모범 답안:**

unsafe 패키지는 Go의 타입 안전성과 메모리 안전성을 우회합니다. 바이너리 데이터 처리, 시스템 프로그래밍, 극단적인 성능 최적화에서 사용됩니다.

주요 사용 사례는 세 가지입니다. 첫째, 바이트 배열을 구조체로 zero-copy 변환할 때입니다. 둘째, 구조체의 메모리 레이아웃을 분석하고 최적화할 때입니다. 셋째, C 라이브러리와 상호작용할 때입니다.

위험은 심각합니다. 잘못된 포인터 연산은 메모리 손상을 일으킵니다. 엔디안 문제로 다른 아키텍처에서 잘못된 결과가 나올 수 있습니다. 가비지 컬렉터가 unsafe.Pointer를 추적하지 못해 메모리 누수가 발생할 수 있습니다. 컴파일러가 최적화를 적용하지 못합니다.

unsafe를 사용하기 전에 반드시 벤치마크로 성능 이점을 증명해야 합니다. 약 2배 빠른 정도의 개선이 있을 수 있지만, 대부분의 경우 안전한 코드로 충분합니다. go build -gcflags=-d=checkptr로 unsafe 오용을 검사할 수 있습니다.

---

### Q5. cgo의 성능 오버헤드와 제약사항을 설명해주세요.

**모범 답안:**

cgo 호출은 약 40ns의 오버헤드가 있으며, 이는 C에서 C 함수를 호출하는 것보다 약 29배 느립니다. 따라서 성능 향상을 위해 cgo를 사용하는 것은 거의 항상 잘못된 선택입니다. cgo는 기존 C 라이브러리를 통합할 때만 사용해야 합니다.

주요 제약사항은 다섯 가지입니다. Go 포인터를 포함하는 Go 값은 C에 직접 전달할 수 없습니다. cgo.Handle을 사용해야 합니다. C는 Go 포인터를 함수 반환 후 저장할 수 없습니다. C의 가변 인자 함수(printf 등)를 직접 호출할 수 없습니다. C union은 Go에서 바이트 배열로 변환됩니다. C 함수 포인터를 직접 호출할 수 없습니다.

추가로 cgo를 사용하면 크로스 컴파일이 어려워집니다. 대상 플랫폼의 C 컴파일러와 라이브러리가 필요합니다. 빌드 시간도 증가합니다.

가능하면 순수 Go 라이브러리나 Go로 작성된 래퍼를 찾아 사용하는 것이 좋습니다. 예를 들어 SQLite의 경우 mattn/go-sqlite3(cgo)보다 modernc.org/sqlite(순수 Go)를 고려할 수 있습니다.

---

### Q6. reflection 대신 제네릭을 사용해야 하는 경우는 언제인가요?

**모범 답안:**

Go 1.18 이후 제네릭이 도입되면서 많은 reflection 사용 사례를 대체할 수 있게 되었습니다. 핵심 기준은 "컴파일 시점에 타입이 결정되는가?"입니다.

제네릭을 사용해야 하는 경우는 다음과 같습니다. 여러 타입에 대해 동일한 로직을 적용하되, 타입이 컴파일 시점에 알려진 경우입니다. 예를 들어 슬라이스 필터링, 맵 변환, 컨테이너 구현 등입니다.

```go
// 제네릭 (빠름, 타입 안전)
func Filter[T any](s []T, pred func(T) bool) []T {
    var result []T
    for _, v := range s {
        if pred(v) {
            result = append(result, v)
        }
    }
    return result
}
```

reflection을 사용해야 하는 경우는 타입이 런타임에만 결정되는 경우입니다. JSON 언마샬링에서 임의의 구조체를 채우거나, 데이터베이스 결과를 동적으로 매핑하거나, struct tag를 읽어야 하는 경우입니다.

제네릭은 reflection보다 50-75배 빠르고 컴파일 시점에 타입 오류를 잡습니다. 가능하면 제네릭을, 불가능하면 reflection을 사용합니다.

---

## 실무 체크리스트

### Reflection 사용 시
- [ ] 제네릭으로 해결할 수 없는지 먼저 검토했는가?
- [ ] 프로그램 경계(입출력)에서만 사용하는가?
- [ ] Kind()를 확인한 후 적절한 메서드를 호출하는가?
- [ ] 값 설정 시 포인터를 전달하는가?
- [ ] CanSet()으로 수정 가능 여부를 확인하는가?
- [ ] 성능 영향을 벤치마크로 측정했는가?

### unsafe 사용 시
- [ ] 성능 이점을 벤치마크로 증명했는가?
- [ ] 엔디안 처리를 고려했는가?
- [ ] -gcflags=-d=checkptr로 테스트했는가?
- [ ] 메모리 정렬 요구사항을 확인했는가?
- [ ] GC 영향을 고려했는가?

### cgo 사용 시
- [ ] 순수 Go 대안을 먼저 찾아보았는가?
- [ ] 성능이 아닌 통합 목적으로만 사용하는가?
- [ ] cgo.Handle로 Go 포인터를 안전하게 전달하는가?
- [ ] C.free로 C 메모리를 해제하는가?
- [ ] 크로스 컴파일 요구사항을 확인했는가?

---

## 참고 자료

- [reflect 패키지 공식 문서](https://pkg.go.dev/reflect)
- [unsafe 패키지 공식 문서](https://pkg.go.dev/unsafe)
- [cgo 공식 문서](https://go.dev/wiki/cgo)
- [The Laws of Reflection](https://go.dev/blog/laws-of-reflection)
- [cgo is not Go](https://dave.cheney.net/2016/01/18/cgo-is-not-go)
- [CGO Performance in Go 1.21](https://shane.ai/posts/cgo-performance-in-go1.21/)
