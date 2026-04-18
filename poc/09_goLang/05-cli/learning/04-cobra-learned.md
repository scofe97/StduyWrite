# Cobra CLI - LEARNED

## 학습 완료 내용


### 1. 기본 구조

```go
var rootCmd = &cobra.Command{
    Use:   "mycli",
    Short: "CLI 설명",
}

func main() {
    rootCmd.Execute()
}
```

### 2. 서브커맨드 추가

```go
var helloCmd = &cobra.Command{
    Use:   "hello",
    Short: "인사하기",
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println("Hello!")
    },
}

func init() {
    rootCmd.AddCommand(helloCmd)
}
```

### 3. 플래그 종류

| 메서드                                              | 용도      |
| ------------------------------------------------ | ------- |
| `StringVarP(&var, "name", "n", "default", "설명")` | 문자열 플래그 |
| `BoolVarP(&var, "loud", "l", false, "설명")`       | 불리언 플래그 |
| `IntVarP(&var, "count", "c", 0, "설명")`           | 정수 플래그  |

- `VarP` = 변수 바인딩 + 짧은 이름 지원
- `Var` = 짧은 이름 없이

### 4. 필수 플래그

```go
logCmd.Flags().StringVarP(&timeSpent, "time", "t", "", "작업 시간")
logCmd.MarkFlagRequired("time")  // -t 없으면 에러
```

### 5. 위치 인자 검증

```go
var logCmd = &cobra.Command{
    Use:  "log [이슈키]",
    Args: cobra.MinimumNArgs(1),  // 최소 1개 필요
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println(args[0])  // 첫 번째 인자
    },
}
```

**Args 검증기 종류:**
- `cobra.NoArgs` - 인자 없음
- `cobra.MinimumNArgs(n)` - 최소 n개
- `cobra.MaximumNArgs(n)` - 최대 n개
- `cobra.ExactArgs(n)` - 정확히 n개
- `cobra.RangeArgs(m, n)` - m~n개

### 6. PersistentFlags (공유 플래그)

```go
// 모든 서브커맨드에서 사용 가능
rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "상세 출력")

// 해당 명령에서만 사용 가능
helloCmd.Flags().StringVarP(&name, "name", "n", "World", "이름")
```

### 7. PersistentPreRun (공통 전처리)

```go
var rootCmd = &cobra.Command{
    Use: "mycli",
    PersistentPreRun: func(cmd *cobra.Command, args []string) {
        // 모든 서브커맨드 실행 전에 호출됨
        if verbose {
            fmt.Println("[설정 로드 중...]")
        }
    },
}
```

## flag vs cobra 비교

| 항목 | flag 패키지 | cobra |
|------|-------------|-------|
| 서브커맨드 | 수동 switch문 | `AddCommand()` |
| 필수 플래그 | if문으로 검증 | `MarkFlagRequired()` |
| 도움말 | 기본 제공 | 자동 생성 (더 예쁨) |
| 공유 플래그 | 불가능 | `PersistentFlags()` |
| 적합한 경우 | 단순 CLI | 복잡한 CLI (git, docker 스타일) |

## 참고

- [Cobra 공식 문서](https://cobra.dev/)
- [spf13/cobra GitHub](https://github.com/spf13/cobra)
