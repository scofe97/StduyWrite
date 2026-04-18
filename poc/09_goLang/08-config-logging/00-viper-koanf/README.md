# Koanf 설정 관리 학습

## 학습 목표

Koanf를 사용하여 유연한 설정 관리 시스템을 구축하는 방법을 익힙니다.

## Koanf란?

Koanf는 Go를 위한 가볍고 확장 가능한 설정 라이브러리입니다.

**주요 특징**:
- 다중 설정 소스: 파일, 환경변수, 플래그, S3 등
- 다양한 형식: YAML, JSON, TOML, env
- 병합 지원: 여러 소스를 우선순위에 따라 병합
- 타입 안전: 구조체로 언마샬링

**Viper와 비교**:
| 항목 | Koanf | Viper |
|------|-------|-------|
| 의존성 | 최소 | 많음 |
| 병합 방식 | 명시적 | 암묵적 |
| 유연성 | 높음 | 중간 |
| 인기도 | 성장 중 | 높음 |

## 핵심 개념

### 1. Provider

설정을 가져오는 소스:
```go
// 파일에서 로드
file.Provider("config.yaml")

// 환경변수에서 로드
env.Provider("APP_", ".", envKeyReplacer)

// 플래그에서 로드
basicflag.Provider(flagset, ".")
```

### 2. Parser

설정 형식을 파싱:
```go
yaml.Parser()
json.Parser()
toml.Parser()
```

### 3. 우선순위 (나중에 로드한 것이 우선)

```
기본값 → 설정 파일 → 환경별 파일 → 환경변수 → CLI 플래그
```

## 프로젝트 구조

```
24-koanf/
├── main.go              # 엔트리 포인트
├── config/
│   └── config.go        # 설정 로드 로직
├── configs/
│   ├── config.yaml      # 기본 설정
│   └── config.dev.yaml  # 개발 환경 설정
├── go.mod
├── README.md            # 이 파일
├── EXERCISES.md         # 실습 과제
├── HINTS.md             # 힌트
└── LEARNED.md           # 학습 회고
```

## 학습 흐름

### 1단계: 파일에서 로드
- YAML 파일 파싱
- 구조체로 언마샬링
- 기본값 설정

### 2단계: 환경변수 병합
- 환경변수 Provider 사용
- 키 변환 규칙 (APP_SERVER_PORT → server.port)
- 오버라이드 테스트

### 3단계: 다중 환경 지원
- 프로파일별 설정 파일
- 설정 병합 순서
- 환경별 차이점 관리

## 주요 API

### Koanf 인스턴스 생성

```go
import "github.com/knadh/koanf/v2"

// 구분자로 "." 사용
k := koanf.New(".")
```

### 파일 로드

```go
import (
    "github.com/knadh/koanf/providers/file"
    "github.com/knadh/koanf/parsers/yaml"
)

// YAML 파일 로드
if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err != nil {
    log.Fatal(err)
}
```

### 환경변수 로드

```go
import "github.com/knadh/koanf/providers/env"

// APP_ 접두사로 환경변수 로드
err := k.Load(env.Provider("APP_", ".", func(s string) string {
    return strings.Replace(
        strings.ToLower(strings.TrimPrefix(s, "APP_")),
        "_", ".", -1)
}), nil)
```

### 값 읽기

```go
// 직접 읽기
port := k.Int("server.port")
host := k.String("database.host")

// 구조체로 언마샬링
var cfg Config
k.Unmarshal("", &cfg)

// 부분 언마샬링
var serverCfg ServerConfig
k.Unmarshal("server", &serverCfg)
```

## 실행 예시

```bash
# 의존성 설치
go get -u github.com/knadh/koanf/v2
go get -u github.com/knadh/koanf/parsers/yaml
go get -u github.com/knadh/koanf/providers/file
go get -u github.com/knadh/koanf/providers/env

# 기본 실행
go run main.go

# 환경변수로 포트 변경
APP_SERVER_PORT=9090 go run main.go

# 개발 프로파일로 실행
APP_PROFILE=dev go run main.go
```

## 참고 자료

- [Koanf GitHub](https://github.com/knadh/koanf)
- [Koanf Examples](https://github.com/knadh/koanf/tree/master/examples)
- [Go Configuration Best Practices](https://blog.gopheracademy.com/advent-2019/configuration-with-koanf/)

### 연관 모듈
- **23-zerolog**: 로그 레벨 설정에 koanf 활용
- **25-go-chi**: 서버 설정에 koanf 활용
- **28-capstone**: 전체 애플리케이션 설정 관리

## 다음 단계

1. `EXERCISES.md`에서 TODO 체크박스 확인
2. 각 파일의 TODO 주석을 채우며 구현
3. `HINTS.md`는 막힐 때만 참고
4. 완료 후 `LEARNED.md`에 회고 작성

## 디버깅 팁

```bash
# 설정 파일 문법 확인
cat configs/config.yaml | python -c "import yaml,sys; yaml.safe_load(sys.stdin)"

# 환경변수 확인
env | grep APP_

# 설정 덤프
go run main.go 2>&1 | grep -E "Port|Host|Level"
```

## 성공 기준

- [ ] YAML 파일에서 설정 로드
- [ ] 환경변수로 설정 오버라이드
- [ ] 다중 환경(dev/prod) 지원
- [ ] 구조체로 타입 안전하게 사용
- [ ] 동적 키 조회 가능

---

**시작하기**: `EXERCISES.md`를 열고 첫 번째 TODO부터 시작하세요!
