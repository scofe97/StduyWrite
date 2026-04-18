# Stage 05: Go 디자인 패턴

**완료일**: 2025-01-12

---

## 학습 목표

객체 생성 로직을 분리하고, 확장 가능한 구조를 만드는 패턴 학습

---

## 핵심 개념

### 1. 팩토리 패턴 (Factory Pattern)

**문제**: 객체 생성 시 if-else/switch 체인 발생
```go
// Bad: 새 타입 추가 시 이 함수 수정 필요
func NewProvider(t string) ProviderConfig {
    switch t {
    case "github":
        return &GitHubConfig{}
    case "azure":
        return &AzureDevOpsConfig{}
    // case "bitbucket": ... 계속 추가
    }
    return nil
}
```

**해결**: Registry 패턴으로 분산 등록
```go
// Good: 각 구현체가 자신을 등록
var registry = map[ProviderType]ProviderFactory{}

func Register(t ProviderType, factory ProviderFactory) {
    registry[t] = factory
}

func NewProvider(t ProviderType, opts map[string]string) ProviderConfig {
    if factory, ok := registry[t]; ok {
        return factory(opts)
    }
    return nil
}
```

---

### 2. 일급 함수 (First-Class Function)

Go에서 함수는 값으로 취급됨 → 변수에 저장, map에 저장, 인자로 전달 가능

```go
// 함수 타입 정의
type ProviderFactory func(option map[string]string) ProviderConfig

// map에 함수 저장
var registry = map[ProviderType]ProviderFactory{}

// 함수를 값으로 전달
Register(GitHub, func(opt map[string]string) ProviderConfig {
    return &GitHubConfig{Token: opt["Token"]}
})
```

---

### 3. init() 함수

- `main()` 보다 **먼저** 실행됨
- 같은 패키지의 모든 파일에서 `init()` 실행
- 패키지 초기화, 자동 등록에 활용

```
실행 순서:
1. 패키지 변수 초기화 (var registry = ...)
2. 각 파일의 init() 실행 (github.go, azure.go)
3. main() 실행
```

```go
// github.go
func init() {
    Register(GitHub, func(opt map[string]string) ProviderConfig {
        return &GitHubConfig{Token: opt["Token"]}
    })
}
```

---

### 4. 타입 안전성 확보

string 대신 커스텀 타입 사용 → 컴파일 타임 검증

```go
// Bad: 오타 검출 불가
provider := NewProvider("githud")  // 런타임에야 발견

// Good: 컴파일 에러
type ProviderType string
const GitHub ProviderType = "github"

provider := NewProvider(GitHub)    // 타입 체크됨
```

---

### 5. make vs 리터럴 초기화

| 방법 | nil 여부 | 쓰기 가능 | 용도 |
|------|----------|----------|------|
| `var m map[K]V` | ✅ nil | ❌ panic | nil 체크 필요 시 |
| `make(map[K]V)` | ❌ | ✅ | 빈 map 생성 |
| `map[K]V{}` | ❌ | ✅ | 빈 map 또는 초기값 |
| `make(map[K]V, cap)` | ❌ | ✅ | 용량 지정 (성능) |

```go
// nil map - 쓰기 시 panic!
var m1 map[string]int
m1["key"] = 1  // panic!

// 초기화된 map - 쓰기 가능
m2 := make(map[string]int)
m2["key"] = 1  // OK

// 용량 지정 - 대량 데이터 시 성능 향상
m3 := make(map[string]int, 1000)
```

---

## 파일 구조

```
05-patterns/
├── types.go      # ProviderType, ProviderConfig 인터페이스
├── factory.go    # Registry, Register(), NewProvider()
├── github.go     # GitHubConfig + init() 등록
├── azure.go      # AzureDevOpsConfig + init() 등록
└── main.go       # 테스트
```

---

## 패턴 비교

| 패턴 | 장점 | 단점 |
|------|------|------|
| switch문 | 단순, 한 곳에서 관리 | 새 타입 추가 시 수정 필요 |
| Registry | 확장 용이, 분산 관리 | 런타임 등록, 약간 복잡 |

**선택 기준**:
- 타입이 3개 이하, 변경 적음 → switch
- 타입이 많고, 플러그인 구조 필요 → Registry

---

## 실무 적용

이 패턴은 다음 상황에서 유용:
- **플러그인 시스템**: 새 플러그인 추가 시 기존 코드 수정 불필요
- **드라이버 패턴**: DB 드라이버, 클라우드 프로바이더 등
- **전략 패턴**: 알고리즘 교체 가능한 구조

---

## 다음 단계

- Stage 06: gRPC 기초
