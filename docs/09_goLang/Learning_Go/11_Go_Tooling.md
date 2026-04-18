# Chapter 11: Go Tooling - 면접 정리

## 핵심 개념 상세 설명

### 1. go run과 go install

go run은 컴파일과 실행을 한 번에 수행합니다. 임시 디렉토리에 바이너리를 생성하고 실행한 후 삭제합니다. 작은 프로그램 테스트나 스크립트처럼 사용할 때 유용합니다.

go install은 도구를 설치할 때 사용합니다. 바이너리가 $GOBIN(기본값 ~/go/bin)에 설치됩니다.

```
┌────────────────────────────────────────────────────────────────┐
│              go install 사용 시 주의사항                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ 올바른 사용 (항상 버전 명시)                                │
│  go install github.com/rakyll/hey@latest                       │
│  go install github.com/rakyll/hey@v0.1.4                       │
│                                                                 │
│  ❌ 잘못된 사용 (예측 불가능한 동작)                            │
│  go install github.com/rakyll/hey                              │
│                                                                 │
│  버전 없이 실행하면:                                            │
│  - go.mod가 있으면 그 버전 사용                                 │
│  - 없으면 에러 발생                                             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 2. 코드 품질 도구 (Linters)

Go 생태계는 다양한 정적 분석 도구를 제공합니다.

```
┌────────────────────────────────────────────────────────────────┐
│              Linter 도입 순서                                   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: go vet                                                │
│  ──────────────                                                 │
│  - 기본 제공, 빠름                                              │
│  - 명확한 버그 탐지                                             │
│  - false positive 거의 없음                                     │
│                                                                 │
│          ↓                                                      │
│                                                                 │
│  Phase 2: staticcheck                                           │
│  ──────────────────                                             │
│  - 정확도 높음                                                  │
│  - go vet보다 더 많은 문제 탐지                                 │
│  - 불필요한 코드, 성능 문제 발견                                │
│                                                                 │
│          ↓                                                      │
│                                                                 │
│  Phase 3: golangci-lint                                         │
│  ──────────────────────                                         │
│  - 50+ 도구 통합                                                │
│  - 팀 표준 정립 후 사용                                         │
│  - .golangci.yml로 설정                                         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

staticcheck가 찾는 문제 예시: 불필요한 fmt.Sprintf, 미사용 에러 값, deprecated API 사용 등.

golangci-lint는 go vet, staticcheck, revive 등 여러 도구를 통합 실행합니다. 섀도잉, 미사용 변수, 내장 식별자 재정의 등을 검사합니다.

### 3. govulncheck - 취약점 검사

govulncheck는 Go 취약점 데이터베이스를 기반으로 보안 취약점을 검사합니다.

```
┌────────────────────────────────────────────────────────────────┐
│              govulncheck 사용                                   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  설치:                                                          │
│  go install golang.org/x/vuln/cmd/govulncheck@latest           │
│                                                                 │
│  소스 코드 검사:                                                │
│  govulncheck ./...                                             │
│                                                                 │
│  바이너리 검사:                                                 │
│  govulncheck -mode binary ./myapp                              │
│                                                                 │
│  출력 예시:                                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Vulnerability #1: GO-2020-0036                          │  │
│  │    Excessive resource consumption in YAML parsing        │  │
│  │  Module: gopkg.in/yaml.v2                                │  │
│  │    Found in: v2.2.7                                      │  │
│  │    Fixed in: v2.2.8                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  해결:                                                          │
│  go get -u=patch gopkg.in/yaml.v2                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 4. go:embed - 파일 임베딩

go:embed 지시자로 파일을 바이너리에 포함시킵니다. 배포 시 단일 바이너리로 모든 리소스를 포함할 수 있습니다.

```
┌────────────────────────────────────────────────────────────────┐
│              go:embed 사용법                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  단일 파일 임베딩:                                              │
│  import _ "embed"  // blank import 필수                         │
│                                                                 │
│  //go:embed passwords.txt                                       │
│  var passwords string  // 또는 []byte                          │
│                                                                 │
│  디렉토리 임베딩:                                               │
│  import "embed"                                                 │
│                                                                 │
│  //go:embed help                                                │
│  var helpInfo embed.FS  // 디렉토리는 embed.FS 필수             │
│                                                                 │
│  숨김 파일 처리:                                                │
│  ─────────────────────────────────────────────────────────     │
│  패턴                     설명                                  │
│  //go:embed dir          숨김 파일 제외                         │
│  //go:embed dir/*        루트의 숨김 파일만 포함                │
│  //go:embed all:dir      모든 숨김 파일 포함                    │
│                                                                 │
│  변수 타입별 제약:                                              │
│  - string, []byte: 단일 파일만                                  │
│  - embed.FS: 여러 파일/디렉토리 가능                            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 5. go generate - 코드 자동 생성

go generate는 소스 파일의 특별한 주석을 찾아 외부 도구를 실행합니다.

```
┌────────────────────────────────────────────────────────────────┐
│              go generate 워크플로우                             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 소스 파일에 주석 추가:                                      │
│  //go:generate stringer -type=Direction                        │
│                                                                 │
│  2. 명령 실행:                                                  │
│  go generate ./...                                             │
│                                                                 │
│  3. 생성된 파일 확인:                                           │
│  direction_string.go (자동 생성)                               │
│                                                                 │
│  일반적인 사용 사례:                                            │
│  - Protocol Buffers (protoc)                                   │
│  - stringer (iota 상수에 String() 메서드)                      │
│  - mockgen (테스트 목 생성)                                    │
│  - sqlc (SQL에서 Go 코드 생성)                                 │
│                                                                 │
│  Best Practice:                                                 │
│  - 생성된 코드는 버전 관리에 커밋                               │
│  - Makefile에 generate 타깃 추가                               │
│  - CI에서 생성 결과 일치 검증                                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 6. 크로스 컴파일

Go는 GOOS와 GOARCH 환경변수로 다른 플랫폼용 바이너리를 빌드합니다.

```
┌────────────────────────────────────────────────────────────────┐
│              크로스 컴파일                                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  현재 플랫폼 확인:                                              │
│  go env GOOS GOARCH                                            │
│                                                                 │
│  Linux AMD64용 빌드:                                            │
│  GOOS=linux GOARCH=amd64 go build                              │
│                                                                 │
│  Windows AMD64용 빌드:                                          │
│  GOOS=windows GOARCH=amd64 go build                            │
│                                                                 │
│  주요 GOOS/GOARCH 조합:                                         │
│  ─────────────────────────────────────────────────────────     │
│  GOOS        GOARCH      설명                                   │
│  linux       amd64       Linux 64비트 Intel/AMD                 │
│  linux       arm64       Linux ARM64 (AWS Graviton 등)          │
│  darwin      amd64       macOS Intel                            │
│  darwin      arm64       macOS Apple Silicon                    │
│  windows     amd64       Windows 64비트                         │
│                                                                 │
│  장점:                                                          │
│  - CGO 없이 순수 Go면 어디서든 크로스 컴파일                    │
│  - 빌드 머신 하나로 모든 플랫폼 바이너리 생성                   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 7. Build Tags

Build Tags로 조건부 컴파일을 수행합니다.

```
┌────────────────────────────────────────────────────────────────┐
│              Build Tags                                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  파일명 기반:                                                   │
│  mycode_linux.go       # Linux에서만 컴파일                     │
│  mycode_windows.go     # Windows에서만 컴파일                   │
│  mycode_darwin_arm64.go  # macOS ARM64에서만                    │
│                                                                 │
│  Build Tag 기반:                                                │
│  //go:build linux                                               │
│  package mypackage    # Linux에서만 컴파일                      │
│                                                                 │
│  //go:build linux && amd64                                      │
│  package mypackage    # Linux AND AMD64에서만                   │
│                                                                 │
│  //go:build !windows                                            │
│  package mypackage    # Windows 제외                            │
│                                                                 │
│  커스텀 태그:                                                   │
│  //go:build integration                                         │
│  package mytest       # 통합 테스트용                           │
│                                                                 │
│  go test -tags integration ./...  # 커스텀 태그로 실행          │
│                                                                 │
│  특수 태그:                                                     │
│  ignore      빌드에서 제외                                      │
│  integration 통합 테스트용 (관례)                               │
│  unix        Unix 계열 OS                                       │
│  cgo         CGO 활성화 시                                      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 비교표

### Linter 비교

| 도구 | 장점 | 단점 | 권장 시점 |
|------|------|------|----------|
| go vet | 기본 제공, 빠름 | 검사 범위 제한 | 항상 사용 |
| staticcheck | 정확도 높음, false positive 적음 | - | 필수 추가 |
| revive | 스타일 규칙 풍부 | false positive 가능 | 코드 표준화 시 |
| golangci-lint | 50+ 도구 통합 | 설정 복잡 | 팀 표준 정립 후 |

### go:embed 변수 타입별 제약

| 변수 타입 | 파일 개수 | 와일드카드 |
|----------|----------|-----------|
| string | 1개만 | 1개 매칭만 |
| []byte | 1개만 | 1개 매칭만 |
| embed.FS | 여러 개 | 여러 개 매칭 가능 |

---

## 면접 예상 질문 및 모범 답안

### Q1. Go에서 사용하는 주요 코드 품질 도구와 도입 순서를 설명하세요.

**모범 답안:**

Go 코드 품질 도구는 단계적으로 도입하는 것이 좋습니다.

첫 번째로 go vet은 기본 제공되는 도구로 항상 사용해야 합니다. 명확한 버그를 탐지하고 false positive가 거의 없습니다. printf 형식 문자열 오류, 복사 불가능한 값 복사 등을 찾습니다.

두 번째로 staticcheck를 추가합니다. go vet보다 더 많은 문제를 탐지하면서도 정확도가 높습니다. 불필요한 코드, deprecated API 사용, 성능 문제 등을 찾습니다. `staticcheck -explain S1039` 처럼 에러 코드에 대한 설명도 볼 수 있습니다.

세 번째로 팀 표준이 정립되면 golangci-lint를 도입합니다. 50개 이상의 도구를 통합 실행하며, .golangci.yml 파일로 세밀하게 설정할 수 있습니다. 섀도잉, 미사용 변수, 내장 식별자 재정의 등 다양한 문제를 검사합니다.

추가로 govulncheck로 보안 취약점을 검사합니다. Go 취약점 데이터베이스를 기반으로 의존성의 알려진 취약점을 찾고 수정 버전을 안내합니다.

---

### Q2. go:embed의 사용법과 주의사항을 설명하세요.

**모범 답안:**

go:embed는 컴파일 시 파일을 바이너리에 포함시키는 기능입니다.

사용법은 세 가지 형태가 있습니다. 첫째, 단일 파일을 string이나 []byte로 임베딩합니다. `//go:embed config.json` 다음 줄에 `var config string`을 선언합니다. 이때 `import _ "embed"` blank import가 필요합니다.

둘째, 디렉토리나 여러 파일을 embed.FS 타입으로 임베딩합니다. `//go:embed static/*` 다음에 `var staticFiles embed.FS`를 선언합니다. embed.FS는 io/fs.FS 인터페이스를 구현하므로 http.FileServer 등과 호환됩니다.

셋째, 숨김 파일 처리에 주의해야 합니다. 기본적으로 숨김 파일은 제외됩니다. `//go:embed all:dir` 패턴으로 모든 숨김 파일을 포함시킬 수 있습니다.

주의사항으로 string과 []byte 변수는 단일 파일만 임베딩 가능합니다. 와일드카드가 여러 파일을 매칭하면 컴파일 에러가 발생합니다. 또한 임베딩은 컴파일 시점에 수행되므로, 런타임에 파일을 변경해도 반영되지 않습니다.

---

### Q3. go generate의 동작 원리와 일반적인 사용 사례를 설명하세요.

**모범 답안:**

go generate는 소스 파일의 `//go:generate` 주석을 찾아 지정된 명령을 실행합니다. 빌드 과정과 분리되어 있어 명시적으로 `go generate ./...`를 실행해야 합니다.

일반적인 사용 사례는 네 가지입니다. 첫째, Protocol Buffers로 .proto 파일에서 Go 코드를 생성합니다. `//go:generate protoc --go_out=. person.proto` 형태로 사용합니다.

둘째, stringer로 iota 상수에 String() 메서드를 생성합니다. `//go:generate stringer -type=Direction`을 선언하면 direction_string.go 파일이 생성되어 Direction 값을 문자열로 변환할 수 있습니다.

셋째, mockgen으로 인터페이스의 mock 구현을 생성합니다. 테스트 코드 작성에 유용합니다.

넷째, sqlc로 SQL 쿼리에서 타입 안전한 Go 코드를 생성합니다.

Best Practice로 생성된 코드는 버전 관리에 커밋해야 합니다. Makefile에 generate 타깃을 추가하고, CI에서 생성 결과가 커밋된 내용과 일치하는지 검증합니다.

---

### Q4. Go의 크로스 컴파일 방법과 Build Tags의 역할을 설명하세요.

**모범 답안:**

크로스 컴파일은 GOOS와 GOARCH 환경변수로 수행합니다. 예를 들어 Mac에서 `GOOS=linux GOARCH=amd64 go build`를 실행하면 Linux용 바이너리가 생성됩니다.

Go의 크로스 컴파일이 쉬운 이유는 순수 Go 코드는 런타임이 필요 없고, 표준 라이브러리가 모든 플랫폼을 지원하기 때문입니다. CGO를 사용하면 대상 플랫폼의 C 컴파일러가 필요해서 복잡해집니다.

Build Tags는 조건부 컴파일을 위한 메커니즘입니다. 파일명 기반(`mycode_linux.go`)과 주석 기반(`//go:build linux`) 두 가지 방법이 있습니다.

주석 기반은 더 유연합니다. `//go:build linux && amd64`로 AND 조건을, `//go:build linux || darwin`으로 OR 조건을, `//go:build !windows`로 NOT 조건을 표현합니다.

커스텀 태그도 가능합니다. `//go:build integration`을 선언하고 `go test -tags integration ./...`으로 실행하면 통합 테스트 파일만 포함됩니다. 이렇게 단위 테스트와 통합 테스트를 분리할 수 있습니다.

---

### Q5. govulncheck의 역할과 취약점 발견 시 대응 방법을 설명하세요.

**모범 답안:**

govulncheck는 Go 공식 취약점 데이터베이스를 기반으로 프로젝트의 보안 취약점을 검사합니다.

두 가지 모드가 있습니다. 소스 코드 검사(`govulncheck ./...`)는 의존성과 실제 호출 경로를 분석합니다. 바이너리 검사(`govulncheck -mode binary ./myapp`)는 빌드된 바이너리에 포함된 취약한 코드를 찾습니다.

출력에는 취약점 ID, 설명, 영향받는 모듈과 버전, 수정된 버전, 그리고 실제로 취약한 함수를 호출하는 코드 경로가 포함됩니다.

대응 방법은 먼저 취약점의 심각도와 실제 영향을 평가합니다. 해당 코드 경로를 실제로 사용하지 않으면 위험이 낮을 수 있습니다. 수정이 필요하면 `go get -u=patch 패키지`로 패치 버전으로 업데이트하거나, 메이저 버전 업그레이드가 필요할 수 있습니다.

CI/CD 파이프라인에 govulncheck를 포함시켜 취약점이 발견되면 빌드가 실패하도록 설정하는 것이 권장됩니다.

---

### Q6. Go 프로젝트의 Makefile과 CI/CD 파이프라인 구성을 설명하세요.

**모범 답안:**

Makefile은 반복적인 작업을 자동화합니다. 일반적인 타깃 구성은 다음과 같습니다.

lint 타깃에서 go vet, staticcheck, golangci-lint를 순서대로 실행합니다. vuln 타깃에서 govulncheck를 실행합니다. test 타깃에서 `go test -race ./...`로 race detector와 함께 테스트합니다. generate 타깃에서 `go generate ./...`를 실행합니다. build 타깃은 generate에 의존하고 바이너리를 빌드합니다.

CI/CD 파이프라인(예: GitHub Actions)에서는 코드 체크아웃, Go 설정, go mod verify로 의존성 검증, golangci-lint 실행, govulncheck 실행, 테스트 실행, 빌드 순서로 진행합니다.

Pre-commit hook으로 커밋 전에 go fmt, go vet, staticcheck를 자동 실행하면 CI 실패를 미리 방지할 수 있습니다.

중요한 점은 도구 버전을 명시하는 것입니다. go install 시 @latest 대신 특정 버전을 지정하면 재현 가능한 빌드가 됩니다.

---

## 실무 체크리스트

### 기본 도구
- [ ] go run으로 빠른 테스트 실행
- [ ] go install로 도구 설치 (@latest 또는 버전 명시)
- [ ] goimports로 import 자동 정리

### 코드 품질
- [ ] go vet 기본 검사 (필수)
- [ ] staticcheck 정적 분석 (권장)
- [ ] golangci-lint 종합 검사 (팀 표준화 후)
- [ ] govulncheck 취약점 검사 (보안 필수)

### 고급 기능
- [ ] go:embed로 파일 임베딩 (배포 단순화)
- [ ] go:generate로 코드 생성 (버전 관리에 커밋)
- [ ] 크로스 컴파일로 다중 플랫폼 지원
- [ ] Build Tags로 조건부 컴파일

### CI/CD 통합
- [ ] Makefile에 lint, test, build 타깃
- [ ] Pre-commit hook 설정
- [ ] CI에서 취약점 검사 자동화

---

## 주요 명령어 요약

| 명령어 | 용도 |
|--------|------|
| `go run file.go` | 빌드 후 즉시 실행 |
| `go install pkg@latest` | 도구 설치 |
| `go vet ./...` | 기본 정적 분석 |
| `staticcheck ./...` | 고급 정적 분석 |
| `golangci-lint run` | 종합 lint |
| `govulncheck ./...` | 취약점 검사 |
| `go generate ./...` | 코드 생성 실행 |
| `GOOS=linux go build` | 크로스 컴파일 |
| `go build -tags tag` | 커스텀 태그 빌드 |
| `go version -m binary` | 빌드 정보 확인 |

---

## 참고 자료

- [staticcheck](https://staticcheck.io/)
- [golangci-lint](https://golangci-lint.run/)
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [Go Embed](https://pkg.go.dev/embed)
- [Go Generate](https://go.dev/blog/generate)
