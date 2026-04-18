# Cobra CLI 프레임워크 학습

## 학습 목표

Cobra를 사용하여 kubectl, helm 스타일의 전문적인 CLI 도구 개발 방법을 익힙니다.

## Cobra란?

Cobra는 Go로 작성된 강력한 CLI 애플리케이션 프레임워크입니다.

**주요 사용처**:
- kubectl (Kubernetes CLI)
- helm (Kubernetes 패키지 매니저)
- gh (GitHub CLI)
- Hugo (정적 사이트 생성기)

## 핵심 개념

### 1. Commands

```
app
├── list        (서브커맨드)
│   ├── --all   (플래그)
│   └── --type  (플래그)
├── create      (서브커맨드)
└── version     (서브커맨드)
```

### 2. Flags

**Local Flag**: 특정 커맨드에만 적용
```go
cmd.Flags().StringP("name", "n", "", "resource name")
```

**Persistent Flag**: 해당 커맨드 + 모든 하위 커맨드에 적용
```go
cmd.PersistentFlags().BoolP("verbose", "v", false, "verbose output")
```

### 3. Command 구조

```go
var cmdExample = &cobra.Command{
    Use:   "example [flags]",
    Short: "짧은 설명",
    Long:  `긴 설명...`,
    Run: func(cmd *cobra.Command, args []string) {
        // 실행 로직
    },
}
```

## 프로젝트 구조

```
10-cobra-cli/
├── main.go              # 엔트리 포인트
├── cmd/
│   ├── root.go          # 루트 커맨드
│   ├── list.go          # list 서브커맨드
│   └── version.go       # version 서브커맨드
├── go.mod
├── README.md            # 이 파일
├── EXERCISES.md         # 실습 과제
├── HINTS.md             # 힌트
└── LEARNED.md           # 학습 회고
```

## 학습 흐름

### 1단계: 기본 구조 이해
- `cmd/root.go`: 루트 커맨드 정의
- `cmd/version.go`: 간단한 서브커맨드
- `main.go`: 엔트리 포인트

### 2단계: 플래그 활용
- Local vs Persistent Flags
- String, Bool, Int 타입 플래그
- Required vs Optional

### 3단계: Viper 연동 (선택)
- 설정 파일 읽기 (.yaml, .json)
- 환경 변수 바인딩
- 우선순위: CLI Flag > 환경변수 > 설정파일 > 기본값

## 주요 API

### Command 생성

```go
cmd := &cobra.Command{
    Use:   "list",
    Short: "List resources",
    RunE: func(cmd *cobra.Command, args []string) error {
        // error 반환 가능
        return nil
    },
}
```

### Flag 추가

```go
// String flag with shorthand
cmd.Flags().StringP("output", "o", "table", "output format")

// Required flag
cmd.MarkFlagRequired("name")

// Persistent flag (루트 커맨드에서)
rootCmd.PersistentFlags().Bool("verbose", false, "verbose output")
```

### 서브커맨드 등록

```go
rootCmd.AddCommand(listCmd)
rootCmd.AddCommand(versionCmd)
```

## 실행 예시

```bash
# 빌드
go build -o mycli

# 루트 커맨드 (도움말)
./mycli

# 서브커맨드
./mycli list --all
./mycli list --type=pod
./mycli version

# Persistent flag
./mycli --verbose list
```

## 참고 자료

- [Cobra 공식 문서](https://github.com/spf13/cobra)
- [Cobra User Guide](https://github.com/spf13/cobra/blob/main/site/content/user_guide.md)
- [Viper (설정 관리)](https://github.com/spf13/viper)
- [Effective Go - Package Names](https://go.dev/doc/effective_go#package-names)

### 📚 Learning Go, 2nd Edition 참조
- **05_Functions.md**: 함수 정의, 가변 인자, 다중 반환값 → Cobra의 RunE 함수 작성에 활용
- **10_Modules_Packages_and_Imports.md**: 패키지 구조화 → cmd/ 디렉토리 구성에 활용
- **09_Errors.md**: 에러 처리 패턴 → CLI 에러 처리에 활용

## 다음 단계

1. `EXERCISES.md`에서 TODO 체크박스 확인
2. 각 파일의 TODO 주석을 채우며 구현
3. `HINTS.md`는 막힐 때만 참고
4. 완료 후 `LEARNED.md`에 회고 작성

## 디버깅 팁

```bash
# 커맨드 트리 확인
go run main.go --help

# 플래그 확인
go run main.go list --help

# 빌드 & 실행
go build -o mycli && ./mycli list --all
```

## 테스트 명령어

```bash
# 루트 커맨드 (도움말 출력되어야 함)
go run main.go

# Version 커맨드
go run main.go version

# List 커맨드 (플래그 없이)
go run main.go list

# List 커맨드 (플래그와 함께)
go run main.go list --all
go run main.go list --type=deployment

# Persistent flag 테스트
go run main.go --verbose list
```

## 성공 기준

- [ ] 모든 커맨드가 정상 동작
- [ ] 플래그가 올바르게 파싱됨
- [ ] 도움말이 명확하게 출력됨
- [ ] 에러 처리가 적절함
- [ ] 코드가 읽기 쉽고 구조적임

---

**시작하기**: `EXERCISES.md`를 열고 첫 번째 TODO부터 시작하세요!
