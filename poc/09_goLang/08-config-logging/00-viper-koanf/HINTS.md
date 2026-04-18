# Koanf 힌트

막힐 때만 참고하세요! 스스로 해결하는 것이 학습에 더 효과적입니다.

---

## Phase 1: 기본 파일 로드

<details>
<summary>Task 1.2: Load 함수 구현</summary>

```go
import (
    "github.com/knadh/koanf/v2"
    "github.com/knadh/koanf/parsers/yaml"
    "github.com/knadh/koanf/providers/file"
)

var k = koanf.New(".")

func Load(path string) (*Config, error) {
    // 파일 로드
    if err := k.Load(file.Provider(path), yaml.Parser()); err != nil {
        return nil, fmt.Errorf("failed to load config: %w", err)
    }

    // 구조체로 언마샬링
    var cfg Config
    if err := k.Unmarshal("", &cfg); err != nil {
        return nil, fmt.Errorf("failed to unmarshal config: %w", err)
    }

    return &cfg, nil
}
```
</details>

<details>
<summary>Task 1.3: main.go에서 사용</summary>

```go
func main() {
    cfg, err := config.Load("configs/config.yaml")
    if err != nil {
        log.Fatalf("Failed to load config: %v", err)
    }

    fmt.Printf("Server Port: %d\n", cfg.Server.Port)
    fmt.Printf("Database Host: %s\n", cfg.Database.Host)
    fmt.Printf("Log Level: %s\n", cfg.Log.Level)
}
```
</details>

---

## Phase 2: 환경변수 오버라이드

<details>
<summary>Task 2.1: LoadWithEnv 함수 구현</summary>

```go
import "github.com/knadh/koanf/providers/env"

func LoadWithEnv(path string) (*Config, error) {
    // 1. 파일 먼저 로드
    if err := k.Load(file.Provider(path), yaml.Parser()); err != nil {
        return nil, err
    }

    // 2. 환경변수 로드 (파일 설정을 오버라이드)
    // APP_SERVER_PORT → server.port
    err := k.Load(env.Provider("APP_", ".", func(s string) string {
        return strings.Replace(
            strings.ToLower(strings.TrimPrefix(s, "APP_")),
            "_", ".", -1)
    }), nil)
    if err != nil {
        return nil, err
    }

    var cfg Config
    if err := k.Unmarshal("", &cfg); err != nil {
        return nil, err
    }

    return &cfg, nil
}
```

**환경변수 변환 예시**:
- `APP_SERVER_PORT=9090` → `server.port=9090`
- `APP_DATABASE_HOST=db.example.com` → `database.host=db.example.com`
- `APP_LOG_LEVEL=debug` → `log.level=debug`
</details>

<details>
<summary>환경변수 키 변환이 안 돼요</summary>

**변환 함수 상세**:
```go
func envKeyReplacer(s string) string {
    // 1. APP_ 접두사 제거
    s = strings.TrimPrefix(s, "APP_")
    // 2. 소문자로 변환
    s = strings.ToLower(s)
    // 3. 언더스코어를 점으로 변환
    s = strings.Replace(s, "_", ".", -1)
    return s
}

// APP_SERVER_PORT
// → SERVER_PORT (접두사 제거)
// → server_port (소문자)
// → server.port (점으로 변환)
```

**테스트 방법**:
```bash
# Windows
set APP_SERVER_PORT=9090
go run main.go

# Linux/Mac
APP_SERVER_PORT=9090 go run main.go
```
</details>

---

## Phase 3: 다중 환경 설정

<details>
<summary>Task 3.1: LoadMultiple 함수 구현</summary>

```go
func LoadMultiple(paths ...string) (*Config, error) {
    for _, path := range paths {
        // 파일이 없으면 건너뛰기 (선택적)
        if _, err := os.Stat(path); os.IsNotExist(err) {
            continue
        }

        if err := k.Load(file.Provider(path), yaml.Parser()); err != nil {
            return nil, fmt.Errorf("failed to load %s: %w", path, err)
        }
    }

    var cfg Config
    if err := k.Unmarshal("", &cfg); err != nil {
        return nil, err
    }

    return &cfg, nil
}

// 사용 예:
// cfg, _ := LoadMultiple("configs/config.yaml", "configs/config.dev.yaml")
```
</details>

<details>
<summary>Task 3.2: LoadWithProfile 함수 구현</summary>

```go
func LoadWithProfile(basePath, profile string) (*Config, error) {
    // 1. 기본 설정 파일 로드
    if err := k.Load(file.Provider(basePath), yaml.Parser()); err != nil {
        return nil, err
    }

    // 2. 프로파일 설정 파일 로드 (있으면)
    if profile != "" {
        // config.yaml → config.dev.yaml
        profilePath := strings.Replace(basePath, ".yaml", "."+profile+".yaml", 1)

        // 파일이 있는 경우에만 로드
        if _, err := os.Stat(profilePath); err == nil {
            if err := k.Load(file.Provider(profilePath), yaml.Parser()); err != nil {
                return nil, err
            }
        }
    }

    var cfg Config
    if err := k.Unmarshal("", &cfg); err != nil {
        return nil, err
    }

    return &cfg, nil
}
```
</details>

<details>
<summary>Task 3.3: 환경변수로 프로파일 선택</summary>

```go
// main.go
func main() {
    profile := os.Getenv("APP_PROFILE")

    var cfg *Config
    var err error

    if profile != "" {
        cfg, err = config.LoadWithProfile("configs/config.yaml", profile)
    } else {
        cfg, err = config.LoadWithEnv("configs/config.yaml")
    }

    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Profile: %s\n", profile)
    fmt.Printf("Server Port: %d\n", cfg.Server.Port)
}
```

**테스트**:
```bash
# 기본 설정
go run main.go

# 개발 환경
APP_PROFILE=dev go run main.go

# 프로덕션 환경 (config.prod.yaml 필요)
APP_PROFILE=prod go run main.go
```
</details>

---

## Phase 4: 동적 설정 조회

<details>
<summary>Task 4.1: Get 함수들 구현</summary>

```go
func Get(key string) interface{} {
    return k.Get(key)
}

func GetString(key string) string {
    return k.String(key)
}

func GetInt(key string) int {
    return k.Int(key)
}

func GetBool(key string) bool {
    return k.Bool(key)
}

func GetFloat64(key string) float64 {
    return k.Float64(key)
}

// 사용 예:
// port := config.GetInt("server.port")
// host := config.GetString("database.host")
```
</details>

<details>
<summary>Task 4.3: 기본값 지원</summary>

```go
func GetStringWithDefault(key, defaultValue string) string {
    if k.Exists(key) {
        return k.String(key)
    }
    return defaultValue
}

func GetIntWithDefault(key string, defaultValue int) int {
    if k.Exists(key) {
        return k.Int(key)
    }
    return defaultValue
}

// 또는 k.String() 호출 후 빈 값 체크
func GetStringOrDefault(key, defaultValue string) string {
    val := k.String(key)
    if val == "" {
        return defaultValue
    }
    return val
}
```
</details>

---

## Phase 5: 고급 기능

<details>
<summary>Task 5.1: 설정 검증</summary>

```go
func Validate(cfg *Config) error {
    // 포트 범위 검증
    if cfg.Server.Port < 1 || cfg.Server.Port > 65535 {
        return fmt.Errorf("invalid port: %d (must be 1-65535)", cfg.Server.Port)
    }

    // 필수 필드 검증
    if cfg.Database.Host == "" {
        return errors.New("database.host is required")
    }

    if cfg.Database.Name == "" {
        return errors.New("database.name is required")
    }

    // 로그 레벨 검증
    validLevels := map[string]bool{
        "debug": true, "info": true, "warn": true, "error": true,
    }
    if !validLevels[cfg.Log.Level] {
        return fmt.Errorf("invalid log level: %s", cfg.Log.Level)
    }

    return nil
}

// Load 함수에서 사용:
func Load(path string) (*Config, error) {
    // ... 로드 로직 ...

    if err := Validate(&cfg); err != nil {
        return nil, fmt.Errorf("config validation failed: %w", err)
    }

    return &cfg, nil
}
```
</details>

<details>
<summary>Task 5.3: 설정 덤프</summary>

```go
func Dump(cfg *Config) string {
    // 민감 정보 마스킹
    maskedCfg := *cfg
    if maskedCfg.Database.Password != "" {
        maskedCfg.Database.Password = "***"
    }

    // YAML로 출력
    data, _ := yamlLib.Marshal(maskedCfg)
    return string(data)
}

// 또는 직접 포맷팅
func DumpFormatted(cfg *Config) string {
    return fmt.Sprintf(`
Server:
  Host: %s
  Port: %d

Database:
  Host: %s
  Port: %d
  Name: %s
  User: %s
  Password: ***

Log:
  Level: %s
  Format: %s
`,
        cfg.Server.Host, cfg.Server.Port,
        cfg.Database.Host, cfg.Database.Port, cfg.Database.Name, cfg.Database.User,
        cfg.Log.Level, cfg.Log.Format)
}
```
</details>

---

## Bonus Tasks

<details>
<summary>Bonus 1: JSON 지원</summary>

```go
import (
    "github.com/knadh/koanf/parsers/json"
    "path/filepath"
)

func LoadAuto(path string) (*Config, error) {
    ext := filepath.Ext(path)

    var parser koanf.Parser
    switch ext {
    case ".yaml", ".yml":
        parser = yaml.Parser()
    case ".json":
        parser = json.Parser()
    default:
        return nil, fmt.Errorf("unsupported file format: %s", ext)
    }

    if err := k.Load(file.Provider(path), parser); err != nil {
        return nil, err
    }

    var cfg Config
    k.Unmarshal("", &cfg)
    return &cfg, nil
}
```
</details>

<details>
<summary>Bonus 2: 플래그 연동</summary>

```go
import (
    "flag"
    "github.com/knadh/koanf/providers/basicflag"
)

func LoadWithFlags() (*Config, error) {
    // 플래그 정의
    f := flag.NewFlagSet("config", flag.ContinueOnError)
    f.Int("server.port", 8080, "Server port")
    f.String("database.host", "localhost", "Database host")
    f.String("log.level", "info", "Log level")
    f.Parse(os.Args[1:])

    // 1. 파일 로드
    k.Load(file.Provider("configs/config.yaml"), yaml.Parser())

    // 2. 환경변수 로드
    k.Load(env.Provider("APP_", ".", envKeyReplacer), nil)

    // 3. 플래그 로드 (최우선)
    k.Load(basicflag.Provider(f, "."), nil)

    var cfg Config
    k.Unmarshal("", &cfg)
    return &cfg, nil
}
```

**사용**:
```bash
go run main.go --server.port=7000
# 플래그 값이 파일과 환경변수보다 우선
```
</details>

---

## 일반적인 문제 해결

<details>
<summary>설정이 로드되지 않아요</summary>

**체크리스트**:
1. 파일 경로가 정확한가?
2. YAML 문법이 올바른가?
3. 구조체 태그(`koanf:"..."`)가 YAML 키와 일치하는가?

```go
// 디버깅: 로드된 키 출력
fmt.Println("Loaded keys:", k.Keys())

// 디버깅: 특정 키 값 확인
fmt.Printf("server.port = %v\n", k.Get("server.port"))
```
</details>

<details>
<summary>환경변수가 적용되지 않아요</summary>

**체크리스트**:
1. 환경변수 접두사(`APP_`)가 맞는가?
2. 변환 함수가 올바른가?
3. 환경변수 로드 순서가 파일 로드 후인가?

```go
// 디버깅: 변환 결과 확인
key := "APP_SERVER_PORT"
converted := envKeyReplacer(key)
fmt.Printf("%s → %s\n", key, converted)
// APP_SERVER_PORT → server.port

// 디버깅: 환경변수 확인
for _, e := range os.Environ() {
    if strings.HasPrefix(e, "APP_") {
        fmt.Println(e)
    }
}
```
</details>

<details>
<summary>타입 변환 에러</summary>

```go
// 잘못된 예: YAML에서 문자열인데 Int로 읽으려 함
port := k.Int("server.port")  // YAML: port: "8080" (따옴표!)

// 해결: YAML에서 따옴표 제거
// server:
//   port: 8080  (숫자로 인식)

// 또는 코드에서 변환
portStr := k.String("server.port")
port, _ := strconv.Atoi(portStr)
```
</details>

<details>
<summary>koanf 인스턴스 재사용 문제</summary>

```go
// 문제: 전역 k가 이전 로드 결과를 유지
var k = koanf.New(".")

func Load(path string) (*Config, error) {
    // 두 번째 호출 시 이전 값과 병합됨!
    k.Load(file.Provider(path), yaml.Parser())
}

// 해결: 새 인스턴스 생성 또는 Clear()
func Load(path string) (*Config, error) {
    k = koanf.New(".")  // 새 인스턴스
    // 또는
    // 현재 koanf v2에는 Clear 없음, 새 인스턴스 사용
}
```
</details>

---

## 추가 리소스

**유용한 패턴**:

```go
// 싱글톤 설정 관리
var (
    cfg  *Config
    once sync.Once
)

func GetConfig() *Config {
    once.Do(func() {
        cfg, _ = Load("configs/config.yaml")
    })
    return cfg
}

// 환경별 설정 파일 자동 로드
func LoadByEnvironment() (*Config, error) {
    env := os.Getenv("GO_ENV")
    if env == "" {
        env = "development"
    }

    return LoadWithProfile("configs/config.yaml", env)
}
```

**참고 프로젝트**:
- [koanf examples](https://github.com/knadh/koanf/tree/master/examples)
- [Twelve-Factor App: Config](https://12factor.net/config)

---

**힌트를 너무 많이 봤다면**: 파일을 삭제하고 처음부터 다시 도전해보세요!
