# Chapter 7: Types, Methods, and Interfaces - 면접 정리

## 핵심 개념 상세 설명

### 1. Go의 타입 시스템과 사용자 정의 타입

Go의 타입 시스템은 상속 없이 조합(Composition)을 통해 코드 재사용을 장려합니다. 사용자 정의 타입은 `type` 키워드로 선언하며, 구조체 기반이나 primitive 타입 기반으로 만들 수 있습니다.

```
┌────────────────────────────────────────────────────────────────┐
│                 Go 타입 분류                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│     Abstract Type (추상 타입)         Concrete Type (구체 타입) │
│     ─────────────────────────         ──────────────────────── │
│                                                                 │
│     interface                         struct                    │
│     - 동작만 정의 (What)              - 저장 방식 + 메서드 구현 │
│     - 구현 없음                       - What + How              │
│                                                                 │
│     type Reader interface {           type Person struct {      │
│         Read(p []byte) (int, error)       Name string           │
│     }                                     Age  int              │
│                                       }                         │
│                                                                 │
│                                       type Score int (primitive)│
└────────────────────────────────────────────────────────────────┘
```

타입 선언의 핵심 원칙은 같은 underlying type을 공유하지만, 별개의 메서드 집합을 가진 다른 타입을 생성한다는 것입니다. `type HighScore Score`로 선언하면 Score와 HighScore는 다른 타입이며, Score의 메서드는 HighScore에 없습니다.

### 2. 메서드와 Receiver

메서드는 사용자 정의 타입에 동작을 추가합니다. receiver 명세가 func 키워드와 메서드명 사이에 위치합니다. receiver 이름은 타입명의 첫 글자 소문자를 사용하며, `this`나 `self`는 Go에서 비관용적입니다.

```
┌────────────────────────────────────────────────────────────────┐
│              메서드 선언 문법                                   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  func (p Person) String() string {                              │
│       ↑          ↑                                              │
│       │          └── 메서드명                                   │
│       └── receiver (타입명 첫 글자)                             │
│                                                                 │
│  • receiver는 타입명의 첫 글자 소문자 사용 (p, c, s 등)        │
│  • this, self 사용 금지 (비관용적)                              │
│  • 메서드는 패키지 블록 레벨에서만 선언 가능                    │
│  • 같은 타입에서 메서드 오버로딩 불가                           │
└────────────────────────────────────────────────────────────────┘
```

### 3. Pointer Receiver vs Value Receiver

receiver 타입 선택은 Go 개발에서 중요한 결정입니다. Pointer Receiver는 원본을 수정할 수 있고, Value Receiver는 복사본에서 작동합니다.

```
┌────────────────────────────────────────────────────────────────┐
│           Receiver 선택 결정 트리                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  메서드가 receiver를 수정하는가?                                │
│           │                                                     │
│          Yes ──────────────→ Pointer Receiver (*T)              │
│           │                                                     │
│          No                                                     │
│           ▼                                                     │
│  nil 처리가 필요한가?                                           │
│           │                                                     │
│          Yes ──────────────→ Pointer Receiver (*T)              │
│           │                                                     │
│          No                                                     │
│           ▼                                                     │
│  타입에 이미 Pointer Receiver 메서드가 있는가?                  │
│           │                                                     │
│          Yes ──────────────→ Pointer Receiver (일관성)          │
│           │                                                     │
│          No ───────────────→ Value Receiver (T)                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

Method Set 규칙도 중요합니다. Value 인스턴스는 Value Receiver 메서드만 Method Set에 포함하고, Pointer 인스턴스는 Value와 Pointer Receiver 메서드 모두 포함합니다. 이 규칙은 인터페이스 구현 판단에 영향을 줍니다.

### 4. Go 인터페이스와 암시적 구현

Go의 인터페이스는 암시적으로 구현됩니다. Java와 달리 `implements` 키워드가 없습니다. 타입이 인터페이스의 모든 메서드를 구현하면 자동으로 해당 인터페이스를 구현한 것으로 간주됩니다.

```
┌────────────────────────────────────────────────────────────────┐
│           인터페이스 구현 방식 비교                             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Duck Typing (Python/Ruby)       Explicit Interface (Java)     │
│  ─────────────────────────       ─────────────────────────     │
│  런타임에 메서드 존재 확인       implements 명시               │
│  유연하지만 타입 안전성 낮음     타입 안전하지만 결합도 높음   │
│                                                                 │
│                    Go Implicit Interface                        │
│                    ─────────────────────                        │
│                    메서드 집합 일치 시 자동 구현                │
│                    타입 안전 + 느슨한 결합                      │
│                                                                 │
│  // Provider 측 - 인터페이스 모름                               │
│  type LogicProvider struct {}                                   │
│  func (lp LogicProvider) Process(data string) string           │
│                                                                 │
│  // Client 측 - 필요한 인터페이스 정의                          │
│  type Logic interface { Process(data string) string }           │
│                                                                 │
│  c := Client{L: LogicProvider{}}  // 자동으로 구현됨            │
└────────────────────────────────────────────────────────────────┘
```

이 방식의 장점은 Provider와 Client가 서로를 몰라도 연결된다는 것입니다. 테스트 시 mock 객체 생성이 쉽고, 코드 결합도가 낮아집니다.

### 5. Embedding을 통한 조합

Go는 상속 대신 Embedding을 통한 조합을 사용합니다. Embedded 필드의 멤버는 외부 타입으로 승격(Promotion)됩니다.

```
┌────────────────────────────────────────────────────────────────┐
│              Embedding과 Promotion                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  type Employee struct {                                         │
│      Name string                                                │
│      ID   string                                                │
│  }                                                              │
│  func (e Employee) Description() string { ... }                 │
│                                                                 │
│  type Manager struct {                                          │
│      Employee         // Embedded (이름 없음)                   │
│      Reports []Employee                                         │
│  }                                                              │
│                                                                 │
│  m := Manager{Employee: Employee{Name: "Bob", ID: "123"}}       │
│                                                                 │
│  m.ID              ──→ "123"         (필드 승격)                │
│  m.Description()   ──→ "Bob (123)"   (메서드 승격)              │
│  m.Employee.Name   ──→ "Bob"         (명시적 접근도 가능)       │
│                                                                 │
│  ⚠️ 중요: Embedding ≠ 상속                                      │
│  var e Employee = m           // 컴파일 에러!                   │
│  var e Employee = m.Employee  // OK                             │
└────────────────────────────────────────────────────────────────┘
```

Embedding은 상속이 아닙니다. Manager는 Employee 타입이 아니며, Employee 타입 변수에 Manager를 직접 할당할 수 없습니다. 또한 동적 디스패치가 없어서 Inner의 메서드 내에서 Outer의 메서드를 호출하지 않습니다.

### 6. 인터페이스와 nil의 관계

인터페이스 변수는 내부적으로 두 개의 포인터를 가집니다: 타입 정보를 가리키는 포인터와 실제 값을 가리키는 포인터. 인터페이스가 nil이 되려면 type과 value 모두 nil이어야 합니다.

```
┌────────────────────────────────────────────────────────────────┐
│            인터페이스 내부 구조와 nil                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Interface Variable                                             │
│  ┌─────────────────┐                                           │
│  │ type pointer  ─────→ 타입 정보 (*Counter)                   │
│  │ value pointer ─────→ 실제 값 (nil 또는 주소)                │
│  └─────────────────┘                                           │
│                                                                 │
│  var pointerCounter *Counter           // nil                   │
│  var incrementer Incrementer           // nil (type=nil, val=nil)│
│  incrementer = pointerCounter          // non-nil! (type≠nil)   │
│                                                                 │
│  fmt.Println(incrementer == nil)       // false!                │
│                                                                 │
│  인터페이스가 nil 포인터를 담으면, 인터페이스 자체는 non-nil   │
└────────────────────────────────────────────────────────────────┘
```

### 7. Type Assertion과 Type Switch

인터페이스에서 구체적인 타입을 추출할 때 Type Assertion을 사용합니다. 안전한 사용을 위해 comma ok idiom을 권장합니다.

```go
// 위험: 실패 시 panic
value := i.(MyType)

// 안전: comma ok 사용
value, ok := i.(MyType)
if !ok {
    // 에러 처리
}
```

Type Switch는 여러 타입을 검사할 때 사용합니다. Optional Interface 체크나 제한된 타입 집합 처리에 유용합니다.

### 8. Accept Interfaces, Return Structs 원칙

함수는 인터페이스를 받고 구조체를 반환해야 합니다. 이 원칙을 따르면 새 메서드나 필드 추가 시 기존 코드에 영향이 없습니다.

```
┌────────────────────────────────────────────────────────────────┐
│        Accept Interfaces, Return Structs                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  // 좋은 패턴                                                   │
│  func NewService(logger Logger, store DataStore) *Service {     │
│      return &Service{logger: logger, store: store}              │
│  }                                                              │
│                                                                 │
│  // 나쁜 패턴                                                   │
│  func NewService(logger Logger, store DataStore) ServiceInterface {│
│      // 인터페이스 반환 - 확장성 제한                           │
│  }                                                              │
│                                                                 │
│  반환 타입        새 메서드/필드 추가 시                        │
│  ──────────────   ────────────────────────────                  │
│  Concrete(struct) 기존 코드 영향 없음 (Minor release)           │
│  Interface        모든 구현체 수정 필요 (Major release)         │
└────────────────────────────────────────────────────────────────┘
```

### 9. Dependency Injection 패턴

Go에서 DI는 인터페이스와 조합을 통해 구현됩니다. 클라이언트가 필요한 인터페이스를 정의하고, main에서 구체적 구현을 조립합니다.

```
┌────────────────────────────────────────────────────────────────┐
│              Dependency Injection 구조                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  main (유일하게 구체 타입을 아는 곳)                            │
│    │                                                            │
│    ├──→ LoggerAdapter (Logger 인터페이스 구현)                  │
│    ├──→ SimpleDataStore (DataStore 인터페이스 구현)             │
│    ├──→ SimpleLogic (Logic 인터페이스 구현)                     │
│    └──→ Controller                                              │
│                                                                 │
│  SimpleLogic                     Controller                     │
│  ┌────────────────┐             ┌────────────────┐             │
│  │ l: Logger      │             │ l: Logger      │             │
│  │ ds: DataStore  │             │ logic: Logic   │             │
│  └────────────────┘             └────────────────┘             │
│         ↑                              ↑                        │
│  인터페이스에 의존 (구체 타입 모름)                             │
│                                                                 │
│  장점:                                                          │
│  - 테스트 용이 (mock 쉽게 주입)                                 │
│  - 느슨한 결합                                                  │
│  - 구현 교체 용이                                               │
└────────────────────────────────────────────────────────────────┘
```

---

## 비교표

### Pointer Receiver vs Value Receiver

| 특성 | Pointer Receiver | Value Receiver |
|------|-----------------|----------------|
| 원본 수정 | 가능 | 불가 (복사본 수정) |
| nil에서 호출 | 가능 (내부에서 처리) | panic 발생 |
| Method Set | Value + Pointer 인스턴스 모두 포함 | Value 인스턴스만 포함 |
| 사용 시점 | 상태 변경, nil 처리 필요 시 | 읽기 전용, 불변 데이터 |

### 상속 vs Embedding

| 특성 | 상속 (Java 등) | Embedding (Go) |
|------|---------------|----------------|
| 관계 | is-a | has-a |
| 부모 타입 할당 | 가능 | 불가 (명시적 접근 필요) |
| 동적 디스패치 | 지원 | 미지원 |
| 메서드 오버라이딩 | 지원 | 섀도잉만 가능 |
| 다중 상속/Embedding | 언어마다 다름 | 지원 |

### 인터페이스 구현 방식

| 방식 | 언어 | 특징 |
|------|------|------|
| Duck Typing | Python, Ruby | 런타임 검사, 유연하지만 불안전 |
| Explicit Interface | Java, C# | 컴파일타임 검사, 결합도 높음 |
| Implicit Interface | Go | 컴파일타임 검사, 느슨한 결합 |

---

## 면접 예상 질문 및 모범 답안

### Q1. Go에서 Pointer Receiver와 Value Receiver를 선택하는 기준을 설명하세요.

**모범 답안:**

Pointer Receiver와 Value Receiver 선택은 세 가지 기준으로 판단합니다.

첫째, 메서드가 receiver를 수정해야 하면 반드시 Pointer Receiver를 사용합니다. Value Receiver는 복사본에서 작동하므로 원본을 수정할 수 없습니다.

둘째, nil 처리가 필요하면 Pointer Receiver를 사용합니다. Value Receiver에서 nil 인스턴스로 메서드를 호출하면 panic이 발생하지만, Pointer Receiver는 메서드 내부에서 nil을 체크하고 처리할 수 있습니다. 이진 트리 같은 재귀 구조에서 유용합니다.

셋째, 일관성을 위해 타입에 이미 Pointer Receiver 메서드가 있다면 다른 메서드도 Pointer Receiver로 통일합니다.

Method Set 규칙도 중요합니다. Value 인스턴스는 Value Receiver 메서드만, Pointer 인스턴스는 두 종류 모두 Method Set에 포함합니다. 따라서 인터페이스가 Pointer Receiver 메서드를 요구하면, Value 인스턴스는 해당 인터페이스를 구현할 수 없습니다.

---

### Q2. Go 인터페이스의 암시적 구현이 Java의 명시적 구현보다 어떤 장점이 있나요?

**모범 답안:**

Go의 암시적 인터페이스 구현은 세 가지 주요 장점이 있습니다.

첫째, 느슨한 결합입니다. Provider가 Client의 인터페이스를 알 필요가 없습니다. Provider는 메서드만 구현하고, Client가 필요한 인터페이스를 정의합니다. 둘이 서로를 몰라도 연결됩니다.

둘째, 테스트 용이성입니다. mock 객체를 쉽게 만들 수 있습니다. 테스트 코드에서 필요한 메서드만 가진 인터페이스를 정의하고, 그에 맞는 mock 구조체를 만들면 됩니다. Java처럼 implements 선언 없이도 자동으로 인터페이스를 구현합니다.

셋째, 작은 인터페이스 장려입니다. Go 표준 라이브러리의 io.Reader, io.Writer는 메서드 하나만 가집니다. 암시적 구현 덕분에 작은 인터페이스를 조합해서 사용하기 쉽습니다. Java에서는 작은 인터페이스마다 implements를 선언해야 해서 번거롭습니다.

단점은 컴파일 타임에 인터페이스 구현 여부를 명시적으로 확인하기 어렵다는 것입니다. 이를 위해 `var _ Interface = (*Type)(nil)` 패턴으로 컴파일 타임 검증을 추가하기도 합니다.

---

### Q3. Go의 Embedding은 상속과 어떻게 다른가요?

**모범 답안:**

Go의 Embedding은 상속과 근본적으로 다릅니다.

첫째, 관계가 다릅니다. 상속은 is-a 관계이고, Embedding은 has-a 관계입니다. Manager가 Employee를 embed해도 Manager는 Employee 타입이 아닙니다. `var e Employee = manager`는 컴파일 에러입니다. `manager.Employee`로 명시적으로 접근해야 합니다.

둘째, 동적 디스패치가 없습니다. 상속에서는 자식 클래스가 부모 메서드를 오버라이드하면, 부모 메서드 내에서 호출되는 메서드도 자식 버전으로 바뀝니다. Go Embedding에서는 Inner의 메서드 내에서 호출되는 메서드는 항상 Inner의 것입니다. Outer가 같은 이름의 메서드를 가져도 Inner 메서드에서는 호출되지 않습니다.

셋째, 다중 Embedding이 가능합니다. Go에서는 여러 타입을 동시에 embed할 수 있습니다. 이름 충돌 시에는 외부 타입의 필드가 우선하며, 내부 필드는 명시적 접근으로 사용합니다.

Embedding의 장점은 코드 재사용과 조합이 명확하다는 것입니다. 타입 계층 없이도 필요한 기능을 가져와 사용할 수 있습니다.

---

### Q4. "Accept Interfaces, Return Structs" 원칙이 왜 중요한가요?

**모범 답안:**

이 원칙은 API의 유연성과 호환성을 위한 것입니다.

인터페이스를 파라미터로 받으면 호출자가 다양한 구현을 전달할 수 있습니다. 테스트 시 mock 객체를 쉽게 주입할 수 있고, 프로덕션에서 구현을 교체하기도 쉽습니다.

구조체를 반환하면 API 진화가 자유롭습니다. 구조체에 새 필드나 메서드를 추가해도 기존 호출자 코드는 영향받지 않습니다. Minor 버전 업데이트로 충분합니다. 반면 인터페이스를 반환하면 새 메서드 추가 시 모든 구현체가 그 메서드를 구현해야 합니다. 이는 Breaking Change로 Major 버전 업데이트가 필요합니다.

예외적으로 Decorator 패턴에서는 인터페이스를 받아 인터페이스를 반환합니다. io.Reader를 받아 gzip으로 감싸 다시 io.Reader로 반환하는 것이 예입니다. 하지만 이런 경우도 자체적으로 새 인터페이스를 정의하지 않고 기존 표준 인터페이스를 사용합니다.

---

### Q5. Go에서 인터페이스 변수에 nil 포인터를 할당하면 왜 non-nil이 되나요?

**모범 답안:**

Go 인터페이스의 내부 구조 때문입니다.

인터페이스 변수는 두 개의 포인터로 구성됩니다: 타입 정보를 가리키는 포인터와 실제 값을 가리키는 포인터. 인터페이스가 nil이 되려면 두 포인터 모두 nil이어야 합니다.

```go
var counter *Counter       // nil 포인터
var inc Incrementer        // nil 인터페이스 (type=nil, value=nil)
inc = counter              // type=*Counter, value=nil
fmt.Println(inc == nil)    // false!
```

counter가 nil이라도 inc에 할당하면 타입 정보(*Counter)가 설정됩니다. value 포인터는 nil이지만 type 포인터는 non-nil이므로 인터페이스 자체는 non-nil입니다.

이로 인해 흔히 발생하는 버그가 있습니다. 에러를 반환할 때 nil 포인터를 직접 반환하면 인터페이스가 non-nil이 될 수 있습니다.

```go
func getError() error {
    var err *MyError = nil
    return err          // non-nil error 반환!
}
```

해결 방법은 인터페이스 타입의 nil을 직접 반환하는 것입니다: `return nil`.

---

### Q6. iota를 사용할 때 주의할 점과 적절한 사용 시나리오를 설명하세요.

**모범 답안:**

iota는 열거형 상수를 선언할 때 사용하지만, 사용 시나리오를 잘 구분해야 합니다.

iota를 사용해야 하는 경우는 값 자체가 중요하지 않고 구분만 필요할 때입니다. 예를 들어 내부 상태 머신의 상태값이나 외부에 노출되지 않는 플래그 등입니다.

iota를 피해야 하는 경우가 더 중요합니다. 첫째, 외부 스펙이 값을 정의한 경우입니다. HTTP 상태 코드나 프로토콜 버전 등은 명시적 값을 사용해야 합니다. 둘째, 데이터베이스에 저장되는 값입니다. 나중에 상수 순서를 변경하면 기존 데이터와 불일치가 발생합니다. 셋째, API로 노출되는 값입니다. 클라이언트와 서버 간 불일치 위험이 있습니다.

iota 사용 시 zero value 처리도 고려해야 합니다. Go에서 int의 zero value는 0이므로, 초기화되지 않은 변수가 첫 번째 상수와 같아질 수 있습니다. 이를 방지하려면 첫 번째 값을 무효 상태로 버립니다: `_ = iota`로 0을 건너뛰고 유효한 값은 1부터 시작하게 합니다.

---

## 실무 체크리스트

### 메서드 설계
- [ ] receiver 이름은 타입 첫 글자 소문자 사용 (this, self 사용 안 함)
- [ ] 상태 변경 메서드는 Pointer Receiver 사용
- [ ] 타입의 모든 메서드는 일관된 receiver 타입 사용
- [ ] nil에서 호출될 가능성 있으면 Pointer Receiver + nil 체크

### 인터페이스 설계
- [ ] 인터페이스는 가능한 작게 유지 (1-3개 메서드)
- [ ] 클라이언트 측에서 인터페이스 정의 (Accept Interfaces)
- [ ] 함수는 구조체 반환 (Return Structs)
- [ ] `var _ Interface = (*Type)(nil)`로 컴파일 타임 구현 검증

### Embedding 사용
- [ ] 상속처럼 사용하지 않음 (is-a 관계 아님)
- [ ] 이름 충돌 시 명시적 접근 필요
- [ ] 동적 디스패치 기대하지 않음

### Type Assertion
- [ ] 항상 comma ok idiom 사용
- [ ] panic 가능한 단일 반환 형태 피하기
- [ ] Type Switch에서 복수 타입 케이스는 any 타입임을 인지

### DI 패턴
- [ ] 비즈니스 로직은 인터페이스에 의존
- [ ] main에서만 구체 타입 조립
- [ ] 함수 어댑터로 간단한 의존성 주입

---

## 참고 자료

- [Effective Go - Interfaces](https://go.dev/doc/effective_go#interfaces)
- [Go Blog - The Laws of Reflection](https://go.dev/blog/laws-of-reflection)
- [Preemptive Interface Anti-Pattern in Go](https://medium.com/@cep21/preemptive-interface-anti-pattern-in-go-54c18ac0668a)
- [Google Wire - Compile-time Dependency Injection](https://github.com/google/wire)
