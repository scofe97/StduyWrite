# Chapter 10: Modules, Packages, and Imports - 면접 정리

## 핵심 개념 상세 설명

### 1. Repository, Module, Package의 관계

Go 코드는 세 가지 계층으로 조직화됩니다.

```
┌────────────────────────────────────────────────────────────────┐
│          Repository / Module / Package 계층 구조                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Repository (소스 코드 저장소)                                  │
│  └── github.com/user/project                                   │
│                                                                 │
│      Module (버전 관리 단위, go.mod 파일 위치)                  │
│      └── go.mod: module github.com/user/project               │
│                                                                 │
│          Package (컴파일 단위, 디렉토리)                        │
│          ├── package main (cmd/server/)                        │
│          ├── package handler (internal/handler/)               │
│          └── package client (pkg/client/)                      │
│                                                                 │
│  핵심 규칙:                                                     │
│  • 하나의 Repository에 여러 Module 가능 (권장하지 않음)         │
│  • 하나의 Module에 여러 Package 포함                           │
│  • Package 이름은 디렉토리명과 일치해야 함                      │
│  • 대문자로 시작하는 식별자는 exported (public)                 │
│  • 소문자로 시작하는 식별자는 unexported (private)              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 2. go.mod 파일 구조와 Directive

go.mod 파일은 모듈의 루트를 정의하고 의존성을 관리합니다.

```
┌────────────────────────────────────────────────────────────────┐
│               go.mod Directive 설명                             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  module github.com/user/project  // 모듈 경로 선언              │
│                                                                 │
│  go 1.21                         // 최소 Go 버전                │
│                                                                 │
│  require (                       // 의존성 선언                 │
│      github.com/pkg/a v1.2.3                                   │
│      github.com/pkg/b v2.0.0 // indirect  // 간접 의존          │
│  )                                                              │
│                                                                 │
│  replace old/pkg => new/pkg v1.0.0  // 모듈 경로 치환           │
│  replace github.com/fork => ./local // 로컬 경로로 치환         │
│                                                                 │
│  exclude github.com/bad/pkg v1.2.3  // 특정 버전 제외           │
│                                                                 │
│  retract v1.5.0  // 자체 발행 버전 철회 (심각한 버그 등)        │
│                                                                 │
│  indirect 의존성:                                               │
│  - 직접 import하지 않지만 의존성 트리에 필요한 모듈             │
│  - 자동으로 // indirect 주석 추가됨                             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 3. Semantic Versioning과 Go의 특수 규칙

Go는 Semantic Versioning을 따르며, v2 이상에서 특별한 규칙이 적용됩니다.

```
┌────────────────────────────────────────────────────────────────┐
│              Semantic Versioning in Go                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  v1.2.3                                                         │
│  │ │ │                                                          │
│  │ │ └── Patch: 버그 수정                                       │
│  │ └── Minor: 새 기능 (하위 호환)                               │
│  └── Major: Breaking Changes                                    │
│                                                                 │
│  Go 특수 규칙 (Import Compatibility Rule):                      │
│  ─────────────────────────────────────────                      │
│  버전            Module Path               Import               │
│  ──────         ─────────────────────     ─────────            │
│  v0.x, v1.x     github.com/user/pkg       동일                  │
│  v2.0.0+        github.com/user/pkg/v2    다름!                 │
│                                                                 │
│  // v1 사용                                                     │
│  import "github.com/user/pkg"                                   │
│                                                                 │
│  // v2 사용 (완전히 다른 모듈로 취급)                           │
│  import "github.com/user/pkg/v2"                                │
│                                                                 │
│  장점: v1과 v2를 동시에 import 가능 (점진적 마이그레이션)       │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 4. Minimal Version Selection (MVS)

Go의 의존성 해석 알고리즘은 다른 패키지 매니저와 다릅니다.

```
┌────────────────────────────────────────────────────────────────┐
│            Minimal Version Selection                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Your App                                                       │
│    │                                                            │
│    ├──→ Module A (requires C v1.2)                             │
│    │                                                            │
│    └──→ Module B (requires C v1.5)                             │
│                                                                 │
│  선택되는 버전: C v1.5 (요구사항을 만족하는 최소 버전)          │
│                                                                 │
│  비교:                                                          │
│  ──────────────────────────────────────────────────────────    │
│  npm/Maven 등          Go (MVS)                                 │
│  ──────────────────    ──────────────────────────────────      │
│  최신 버전 선택        최소 만족 버전 선택                      │
│  자동 업그레이드       수동 업데이트 필요                       │
│  비재현적 빌드         재현 가능한 빌드                         │
│                                                                 │
│  장점:                                                          │
│  - 빌드 재현성 보장 (같은 go.mod → 같은 결과)                   │
│  - 의도치 않은 업그레이드 방지                                  │
│  - 의존성 변경이 명시적                                         │
│                                                                 │
│  업데이트 명령:                                                 │
│  go get github.com/pkg@v1.5.0     # 특정 버전                   │
│  go get -u ./...                  # 모든 의존성 최신화          │
│  go get -u=patch ./...            # 패치 버전만 업데이트        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 5. internal Package

internal 디렉토리는 패키지 캡슐화를 강제합니다.

```
┌────────────────────────────────────────────────────────────────┐
│               internal Package 규칙                             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  project/                                                       │
│  ├── go.mod                                                     │
│  ├── internal/          ← 외부 모듈에서 import 불가!            │
│  │   ├── config/                                               │
│  │   └── database/                                             │
│  ├── pkg/               ← 외부 모듈에서 import 가능             │
│  │   └── client/                                               │
│  └── cmd/                                                       │
│      └── server/                                               │
│                                                                 │
│  // 같은 모듈 내에서 - OK                                       │
│  import "github.com/user/project/internal/config"              │
│                                                                 │
│  // 다른 모듈에서 - 컴파일 에러!                                │
│  import "github.com/user/project/internal/config"              │
│  // cannot import internal package                              │
│                                                                 │
│  사용 시점:                                                     │
│  - 구현 세부사항 숨기기                                         │
│  - API 변경 자유도 확보                                         │
│  - 모듈 내부용 유틸리티                                         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 6. 순환 의존성 (Circular Dependencies)

Go는 순환 의존성을 컴파일 타임에 금지합니다.

```
┌────────────────────────────────────────────────────────────────┐
│            순환 의존성 해결 방법                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  문제 상황:                                                     │
│  Package A ──import──→ Package B ──import──→ Package A (에러!)  │
│                                                                 │
│  해결 방법 1: 패키지 병합                                       │
│  Package A + B → Package AB                                     │
│                                                                 │
│  해결 방법 2: 인터페이스로 분리                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  // package interfaces                                  │    │
│  │  type ServiceA interface { DoSomething() }              │    │
│  │                                                         │    │
│  │  // package a                                           │    │
│  │  type implA struct{}                                    │    │
│  │  func (implA) DoSomething() {}                         │    │
│  │                                                         │    │
│  │  // package b                                           │    │
│  │  import "project/interfaces"                            │    │
│  │  func UseService(s interfaces.ServiceA) {}              │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  해결 방법 3: 공통 패키지 추출                                  │
│  Package A ─┐                                                  │
│             └──→ Package common ←──┘                           │
│  Package B ─┘                                                  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 7. Workspace

Workspace는 여러 모듈을 동시에 개발할 때 사용합니다.

```
┌────────────────────────────────────────────────────────────────┐
│                 Go Workspace                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  사용 시나리오:                                                 │
│  - 여러 모듈 동시 개발                                          │
│  - 로컬에서 의존성 수정 테스트                                  │
│  - 모노레포 개발                                                │
│                                                                 │
│  go.work 파일:                                                  │
│  ┌──────────────────────────────────┐                          │
│  │  go 1.21                         │                          │
│  │                                  │                          │
│  │  use (                           │                          │
│  │      ./main-app                  │                          │
│  │      ./module-a                  │                          │
│  │      ./module-b                  │                          │
│  │  )                               │                          │
│  │                                  │                          │
│  │  replace github.com/external =>  │                          │
│  │      ./local-fork                │                          │
│  └──────────────────────────────────┘                          │
│                                                                 │
│  명령어:                                                        │
│  go work init ./main-app ./module-a  # 초기화                   │
│  go work use ./module-b              # 모듈 추가                │
│  go work sync                        # 동기화                   │
│                                                                 │
│  주의: go.work는 .gitignore에 추가 (로컬 개발용)               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 8. Module Proxy와 go.sum

Go는 Module Proxy를 통해 의존성을 캐싱하고 보안을 강화합니다.

```
┌────────────────────────────────────────────────────────────────┐
│          Module Proxy와 Checksum                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  go get 요청 흐름:                                              │
│                                                                 │
│  Developer ──→ go command ──→ Proxy (proxy.golang.org)         │
│                                  │                              │
│                     캐시에 있음? ├──Yes──→ 캐시 반환            │
│                                  │                              │
│                                 No                              │
│                                  │                              │
│                                  ▼                              │
│                           GitHub/GitLab ──→ Proxy 캐시          │
│                                                                 │
│  GOPROXY 설정:                                                  │
│  GOPROXY=https://proxy.golang.org,direct  # 기본값              │
│  GOPRIVATE=github.com/mycompany/*         # 프라이빗 제외       │
│                                                                 │
│  go.sum 파일:                                                   │
│  - 모듈의 cryptographic checksum 저장                           │
│  - 빌드 재현성 보장                                             │
│  - 공급망 공격 방지                                             │
│                                                                 │
│  github.com/pkg v1.0.0 h1:abc123...=                           │
│  github.com/pkg v1.0.0/go.mod h1:def456...=                    │
│                                                                 │
│  검증: go mod verify                                            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 비교표

### go.mod Directive 비교

| Directive | 용도 | 예시 |
|-----------|------|------|
| module | 모듈 경로 선언 | `module github.com/user/project` |
| go | 최소 Go 버전 | `go 1.21` |
| require | 의존성 선언 | `require github.com/pkg v1.0.0` |
| replace | 모듈 경로 치환 | `replace old => new v1.0.0` |
| exclude | 특정 버전 제외 | `exclude github.com/pkg v1.2.3` |
| retract | 자체 버전 철회 | `retract v1.5.0` |

### 프로젝트 구조별 패턴

| 규모 | 구조 | 특징 |
|------|------|------|
| 작은 프로젝트 | 루트에 main.go | 단일 패키지 |
| 중간 프로젝트 | cmd/ + internal/ | 캡슐화 적용 |
| 대규모 프로젝트 | cmd/ + internal/ + pkg/ | 공개 API 분리 |

### MVS vs 다른 패키지 매니저

| 특성 | npm/Maven | Go (MVS) |
|------|-----------|----------|
| 버전 선택 | 최신 버전 | 최소 만족 버전 |
| 빌드 재현성 | 낮음 | 높음 |
| 자동 업그레이드 | 있음 | 없음 |
| lock 파일 | 필요 | go.sum (checksum만) |

---

## 면접 예상 질문 및 모범 답안

### Q1. Go에서 Repository, Module, Package의 차이점과 관계를 설명하세요.

**모범 답안:**

세 개념은 계층적 관계를 형성합니다.

Repository는 Git 같은 버전 관리 시스템에 저장된 소스 코드 저장소입니다. `github.com/user/project`가 예입니다.

Module은 함께 버전 관리되는 Go 패키지들의 집합입니다. go.mod 파일이 있는 디렉토리가 모듈의 루트이며, 모듈 경로가 고유 식별자가 됩니다. 하나의 Repository에 여러 Module이 있을 수 있지만, 보통 하나의 Repository에 하나의 Module을 권장합니다.

Package는 컴파일의 기본 단위로, 같은 디렉토리에 있는 Go 소스 파일들의 집합입니다. 패키지 이름은 디렉토리명과 일치해야 하며, main 패키지가 실행 파일을 생성합니다.

핵심 규칙으로 대문자로 시작하는 식별자는 exported(public)이고, 소문자는 unexported(private)입니다. 이 규칙이 접근 제어의 유일한 메커니즘입니다.

---

### Q2. Minimal Version Selection(MVS)이 무엇이고, 다른 패키지 매니저와 어떻게 다른가요?

**모범 답안:**

MVS는 Go의 의존성 해석 알고리즘으로, 모든 요구사항을 만족하는 최소 버전을 선택합니다.

예를 들어 앱이 A와 B를 의존하고, A가 C v1.2를, B가 C v1.5를 요구하면, Go는 C v1.5를 선택합니다. npm이나 Maven은 C의 최신 버전(예: v1.8)을 선택할 수 있습니다.

MVS의 장점은 세 가지입니다. 첫째, 빌드 재현성이 보장됩니다. 같은 go.mod 파일이면 어디서든 같은 버전이 선택됩니다. 둘째, 의도치 않은 업그레이드가 방지됩니다. 의존성 변경이 명시적입니다. 셋째, lock 파일이 필요 없습니다. go.sum은 checksum만 저장합니다.

단점은 보안 패치나 버그 수정을 받으려면 수동으로 `go get -u`를 실행해야 한다는 것입니다. 정기적인 의존성 업데이트와 취약점 검사가 필요합니다.

---

### Q3. internal 패키지의 역할과 사용 시나리오를 설명하세요.

**모범 답안:**

internal 패키지는 Go에서 모듈 내부 캡슐화를 강제하는 메커니즘입니다.

internal 디렉토리 하위의 패키지는 같은 모듈 내에서만 import할 수 있습니다. 외부 모듈에서 import하려고 하면 컴파일 에러가 발생합니다.

사용 시나리오는 세 가지입니다. 첫째, 구현 세부사항을 숨길 때입니다. 외부에 노출하고 싶지 않은 유틸리티나 헬퍼를 internal에 넣습니다. 둘째, API 변경 자유도를 확보할 때입니다. internal 패키지는 Breaking Change 없이 자유롭게 수정할 수 있습니다. 셋째, 레이어 분리를 강제할 때입니다. 예를 들어 `internal/domain`, `internal/infrastructure`로 분리하면 외부에서 직접 접근을 막을 수 있습니다.

반면 pkg 디렉토리는 관례적으로 외부에 공개하는 라이브러리를 넣습니다. internal과 pkg를 조합하면 명확한 API 경계를 만들 수 있습니다.

---

### Q4. Go에서 v2 이상의 모듈을 어떻게 관리하고, 왜 이런 규칙이 있나요?

**모범 답안:**

Go는 Import Compatibility Rule을 적용합니다. v2.0.0 이상의 메이저 버전은 모듈 경로에 버전을 포함해야 합니다.

v0.x.x와 v1.x.x는 `github.com/user/pkg`로 import합니다. v2.0.0부터는 `github.com/user/pkg/v2`로 import합니다. 이는 완전히 다른 모듈로 취급됩니다.

이 규칙의 이유는 점진적 마이그레이션을 가능하게 하기 위함입니다. v1과 v2를 동시에 import할 수 있어서, 코드베이스를 한 번에 마이그레이션하지 않아도 됩니다. 또한 의존성 충돌 없이 다른 라이브러리들이 다른 메이저 버전을 사용할 수 있습니다.

v2로 전환하려면 두 가지 작업이 필요합니다. 첫째, go.mod의 module 경로에 /v2를 추가합니다. 둘째, git tag v2.0.0을 생성합니다. 내부 import 경로도 모두 /v2로 변경해야 합니다.

---

### Q5. 순환 의존성이 발생했을 때 해결 방법을 설명하세요.

**모범 답안:**

Go는 순환 의존성을 컴파일 타임에 금지합니다. 해결 방법은 세 가지입니다.

첫째, 패키지를 병합합니다. 두 패키지가 서로 의존한다면, 실제로는 하나의 개념일 수 있습니다. 하나의 패키지로 합치는 것이 가장 단순한 해결책입니다.

둘째, 인터페이스로 의존성을 역전합니다. 공통 인터페이스 패키지를 만들고, 각 패키지는 구현체만 제공합니다. 의존하는 쪽은 인터페이스만 알면 됩니다. 이는 Dependency Inversion Principle의 적용입니다.

셋째, 공통 코드를 제3의 패키지로 추출합니다. 두 패키지가 공유하는 타입이나 함수를 별도 패키지로 분리하고, 두 패키지 모두 이 공통 패키지를 import합니다.

설계 단계에서 순환 의존성을 방지하는 것이 가장 좋습니다. 패키지 경계를 명확히 하고, 상위 레이어가 하위 레이어만 의존하도록 설계합니다.

---

### Q6. go.sum 파일의 역할과 Module Proxy의 동작 방식을 설명하세요.

**모범 답안:**

go.sum 파일은 모듈의 cryptographic checksum을 저장합니다. 각 모듈 버전에 대해 zip 파일과 go.mod 파일의 해시값이 기록됩니다.

역할은 세 가지입니다. 첫째, 빌드 재현성을 보장합니다. 같은 checksum이면 같은 소스 코드입니다. 둘째, 공급망 공격을 방지합니다. 모듈이 변조되면 checksum이 일치하지 않아 감지됩니다. 셋째, sum.golang.org에서 전역 checksum 데이터베이스와 비교합니다.

Module Proxy(proxy.golang.org)는 중간 캐시 역할을 합니다. go get 실행 시 먼저 Proxy에 요청하고, Proxy가 캐시에 없으면 원본 저장소에서 가져와 캐시합니다.

장점으로 속도가 빨라지고, 원본 저장소가 삭제되어도 Proxy에 캐시가 남습니다. GOPRIVATE 환경변수로 프라이빗 모듈은 Proxy를 우회하도록 설정합니다.

---

## 실무 체크리스트

### 모듈 초기화
- [ ] go mod init으로 모듈 생성
- [ ] 모듈 경로는 저장소 URL과 일치하게 설정
- [ ] go mod tidy로 의존성 정리

### 패키지 설계
- [ ] 패키지 이름은 디렉토리명과 일치
- [ ] util, common, base 같은 일반적 이름 피하기
- [ ] internal로 구현 세부사항 캡슐화

### 버전 관리
- [ ] Semantic Versioning 준수
- [ ] v2 이상은 모듈 경로에 /vN 포함
- [ ] retract로 문제 있는 버전 철회

### 의존성 관리
- [ ] go get으로 명시적 업데이트
- [ ] govulncheck로 취약점 검사
- [ ] go mod graph로 의존성 분석

### CI/CD
- [ ] GOPROXY 설정 확인
- [ ] GOPRIVATE으로 프라이빗 모듈 설정
- [ ] go mod verify로 checksum 검증

---

## 주요 명령어 요약

| 명령어 | 용도 |
|--------|------|
| `go mod init` | 새 모듈 초기화 |
| `go mod tidy` | 의존성 정리 |
| `go mod download` | 의존성 다운로드 |
| `go mod verify` | checksum 검증 |
| `go mod graph` | 의존성 그래프 |
| `go mod why pkg` | 의존성 이유 확인 |
| `go get pkg@version` | 특정 버전 가져오기 |
| `go get -u ./...` | 모든 의존성 최신화 |
| `go work init` | 워크스페이스 초기화 |

---

## 참고 자료

- [Go Modules Reference](https://go.dev/ref/mod)
- [pkg.go.dev](https://pkg.go.dev/) - Go 패키지 문서
- [Semantic Versioning](https://semver.org/)
- [Go Module Mirror and Checksum Database](https://proxy.golang.org/)
