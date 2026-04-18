# Go Learning

Go 언어 학습 프로젝트

## 관련 이론

- [docs/09_goLang](../../docs/09_goLang/): Go 언어 이론 문서
  - `00_References/Learning_Go/`: Learning Go 책 정리
  - `00_References/gRPC_Microservices/`: gRPC 마이크로서비스 책 정리
  - `11_System_Programming/`: 시스템 프로그래밍 이론

---

## 폴더 구조

```
go-learning/
├── 01-fundamentals/          # Go 기초 문법
│   ├── 00-variables-types/
│   ├── 01-control-flow/
│   ├── 02-data-structures/
│   ├── 03-functions/
│   ├── 04-pointers/
│   ├── 05-methods-interfaces/
│   ├── 06-error-handling/
│   ├── 07-strings-regex/
│   └── 08-generics/
│
├── 02-standard-library/      # 표준 라이브러리
│   ├── 00-file-io/
│   ├── 01-json-encoding/
│   ├── 02-time/
│   ├── 03-context/
│   └── 04-testing/
│
├── 03-concurrency/           # 동시성
│   ├── 00-basics/
│   └── 03-worker-pool/
│
├── 04-web/                   # 웹 개발
│   ├── 00-http-server/
│   ├── 01-chi-router/
│   ├── 02-websocket/
│   └── 03-grpc/
│
├── 05-cli/                   # CLI 도구
│   ├── 00-flag/
│   ├── 01-cobra/
│   ├── 02-env/
│   └── 03-makefile/
│
├── 06-database/              # 데이터베이스
│   ├── 00-sql-basics/
│   └── 01-sqlc/
│
├── 07-config-logging/        # 설정 & 로깅
│   ├── 00-viper-koanf/
│   ├── 01-zerolog/
│   └── 02-observability/
│
├── 08-patterns/              # 디자인 패턴
│   ├── 00-fsm/
│   └── 01-others/
│
├── 09-devops/                # DevOps
│   ├── 00-docker-k8s/
│   ├── 01-container-scratch/
│   └── 02-distributed/
│
├── 10-capstone/              # 종합 프로젝트
│
├── projects/                 # 독립 프로젝트
│   ├── jira-worklog/
│   ├── figma-mcp/
│   └── spring-test-server/
│
└── docs/                     # 문서
```

## 각 폴더 구조

```
XX-topic-name/
├── STUDY.md          # 학습할 내용 (개념, 질문)
├── main.go           # 실습 코드 (학습 후 작성)
└── LEARNED.md        # 학습 완료 후 정리 (선택)
```

## 학습 순서

1. **01-fundamentals** - Go 기초 문법 이해
2. **02-standard-library** - 표준 라이브러리 활용
3. **03-concurrency** - 동시성 프로그래밍
4. **04-web** - 웹 서버 개발
5. **05-cli** - CLI 도구 개발
6. **06-database** - 데이터베이스 연동
7. **07-config-logging** - 설정 및 로깅
8. **08-patterns** - 디자인 패턴
9. **09-devops** - DevOps 관련 기술
10. **10-capstone** - 종합 프로젝트
