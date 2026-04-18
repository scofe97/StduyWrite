# 05-cli

Go CLI 도구 개발을 학습합니다. flag 패키지부터 Cobra 프레임워크, 환경변수, Makefile까지.

## 구조

```
05-cli/
├── learning/
│   ├── 01-cobra.md
│   ├── 02-env.md
│   ├── 03-makefile.md
│   ├── 04-cobra-learned.md
│   └── 05-makefile-learned.md
├── practice/
│   ├── 01-flag/
│   ├── 02-cobra/
│   ├── 03-env/
│   └── 04-makefile/
└── README.md
```

## 학습 순서

| # | 토픽 | learning | practice |
|---|------|----------|----------|
| 1 | Flag 패키지 | - | 01-flag (go.mod + main.go) |
| 2 | Cobra CLI | 01, 04 | 02-cobra (go.mod + main.go) |
| 3 | 환경변수 & CLI | 02 | 03-env (grep, envtool) |
| 4 | Makefile | 03, 05 | 04-makefile (go.mod + Makefile) |

## 주요 라이브러리

| 토픽 | 라이브러리 | 설치 |
|------|-----------|------|
| Cobra | spf13/cobra | `go get github.com/spf13/cobra` |
| Viper | spf13/viper | `go get github.com/spf13/viper` |
