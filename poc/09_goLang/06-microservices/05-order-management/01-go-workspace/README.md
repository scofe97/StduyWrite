# 01. Go Workspace - 모노레포 설정

## 학습 목표

- Go Workspace 개념 이해
- 멀티 모듈 프로젝트 구성
- 공유 코드 관리

## 핵심 개념

### Go Workspace란?

Go 1.18부터 도입된 기능으로, 여러 모듈을 하나의 작업 공간에서 관리할 수 있습니다.

```
order-management-system/
├── go.work              # 워크스페이스 정의
├── common/              # 공유 코드
│   └── go.mod
├── gateway/
│   └── go.mod
└── orders/
    └── go.mod
```

### 장점

1. `replace` 지시문 없이 로컬 모듈 참조
2. 공유 코드 변경 시 즉시 반영
3. 통합 빌드/테스트 가능

## 실습 과제

### Task 1: 프로젝트 디렉토리 생성

```bash
mkdir -p order-management-system/{common,gateway,orders}
cd order-management-system
```

### Task 2: 각 모듈 초기화

```bash
# common 모듈
cd common
go mod init common
cd ..

# gateway 모듈
cd gateway
go mod init gateway
cd ..

# orders 모듈
cd orders
go mod init orders
cd ..
```

### Task 3: Go Workspace 생성

```bash
go work init ./common ./gateway ./orders
```

생성된 `go.work` 파일:
```go
go 1.22

use (
    ./common
    ./gateway
    ./orders
)
```

### Task 4: 공유 코드 작성

```go
// common/env.go
package common

import "os"

func EnvString(key, fallback string) string {
    if val, ok := os.LookupEnv(key); ok {
        return val
    }
    return fallback
}
```

### Task 5: 다른 모듈에서 사용

```go
// gateway/main.go
package main

import (
    "common"
    "fmt"
)

func main() {
    port := common.EnvString("PORT", "8080")
    fmt.Printf("Gateway will start on port %s\n", port)
}
```

## 테스트 방법

```bash
# gateway에서 실행
cd gateway
go run .
```

## 체크리스트

- [ ] 디렉토리 구조 생성
- [ ] 각 모듈 go.mod 초기화
- [ ] go.work 파일 생성
- [ ] common 모듈에 공유 코드 작성
- [ ] 다른 모듈에서 common 참조 확인

## 다음 단계

→ 02-gateway-http: HTTP Gateway 서버 구현
