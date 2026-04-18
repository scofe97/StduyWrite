# Stage 02: 인터페이스와 다형성 학습 정리

## 1. 인터페이스 기본

### 암시적 구현 (Duck Typing)
```go
type Credentials interface {
    ApplyAuth(req *http.Request)
    GetAuthType() string
}

// implements 키워드 없이 메서드만 구현하면 자동으로 인터페이스 충족
type TokenCredentials struct { Token string }

func (c *TokenCredentials) ApplyAuth(req *http.Request) { ... }
func (c *TokenCredentials) GetAuthType() string { ... }
```

**핵심**: "오리처럼 걷고 꽥꽥거리면 오리다" - 메서드 시그니처만 맞으면 인터페이스 구현

---

## 2. 다형성 활용

### 여러 타입을 하나의 인터페이스로 처리
```go
// 서로 다른 구현체를 하나의 슬라이스에
configs := []ProviderConfig{
    &GitHubConfig{Token: "ghp_xxx"},
    &AzureDevOpsConfig{Organization: "org", Project: "prj", PAT: "pat"},
}

// 동일한 방식으로 처리
for _, cfg := range configs {
    fmt.Printf("Provider: %s, Auth: %s\n",
        cfg.GetType(),
        cfg.GetCredentials().GetAuthType())
}
```

### 인터페이스를 파라미터로 받는 함수
```go
func PrintAuthInfo(c Credentials) {
    fmt.Println(c.GetAuthType())  // 어떤 구현체든 동작
}

PrintAuthInfo(&TokenCredentials{Token: "abc"})   // bearer_token
PrintAuthInfo(&BasicCredentials{User: "u", Pass: "p"})  // basic_auth
```

---

## 3. 포인터 리시버와 인터페이스

### 포인터 리시버로 정의하면 *T만 인터페이스 구현
```go
func (c *TokenCredentials) GetAuthType() string { ... }

// 인터페이스에 할당 시
var c1 Credentials = &TokenCredentials{}  // ✅ *TokenCredentials는 OK
var c2 Credentials = TokenCredentials{}   // ❌ TokenCredentials는 불가!
```

| 리시버 타입 | T 구현? | *T 구현? |
|------------|--------|---------|
| 값 `(c T)` | ✅ | ✅ |
| 포인터 `(c *T)` | ❌ | ✅ |

---

## 4. 빈 인터페이스 (interface{})

```go
var anything interface{}

anything = 42                              // int
anything = "hello"                         // string
anything = TokenCredentials{Token: "abc"}  // struct

fmt.Printf("%T\n", anything)  // 타입 출력
```

**용도**: 어떤 타입이든 받아야 할 때 (예: `fmt.Println`의 인자)

---

## 5. 컴파일 타임 인터페이스 검증

```go
var _ ProviderConfig = (*AzureDevOpsConfig)(nil)
```

- 인터페이스 구현 누락 시 컴파일 에러 발생
- 런타임 에러 방지

---

## 6. 인터페이스 설계 원칙

### 작은 인터페이스가 좋다
```go
// ✅ 좋음: 작고 명확
type Credentials interface {
    ApplyAuth(req *http.Request)
    GetAuthType() string
}

// ❌ 나쁨: 너무 큰 인터페이스
type Everything interface {
    Method1()
    Method2()
    Method3()
    // ... 10개 이상
}
```

**Go 격언**: "The bigger the interface, the weaker the abstraction"

---

## 실습 파일

| 파일 | 내용 |
|------|------|
| `credentials.go` | Credentials 인터페이스, Token/Basic 구현 |
| `config.go` | ProviderConfig 인터페이스, ProviderType |
| `github.go` | GitHubConfig 구현 |
| `azure.go` | AzureDevOpsConfig 구현 |
| `main.go` | 다형성 테스트 |

---

## 원본 프로젝트 참조

| 파일 | 학습 내용 |
|------|----------|
| `internal/provider/config.go` | ProviderConfig 인터페이스 정의 |
| `internal/provider/credentials.go` | Credentials 인터페이스 + 구현들 |
| `internal/provider/github.go` | 인터페이스 구현 예시 |
