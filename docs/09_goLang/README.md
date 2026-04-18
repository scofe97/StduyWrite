# Go 언어 학습 문서

Go 언어 기초부터 시스템 프로그래밍까지 체계적으로 정리한 학습 자료입니다.

---

## 폴더 구조

```
09_goLang/
├── README.md                    # 이 파일
├── 00_References/               # 책 기반 참고 자료
│   ├── Learning_Go/             # Learning Go 책 정리
│   ├── gRPC_Microservices/      # gRPC Microservices 책 정리
│   ├── GO_GC_Theory.md          # Go GC 이론
│   ├── GO_New_Features.md       # Go 새 기능 정리
│   └── Learning_Go_Reference.md # Learning Go 챕터 매핑
│
└── 11_System_Programming/       # 시스템 프로그래밍
    ├── 01_OS_Fundamentals/      # OS 기초 개념
    ├── 02_System_Calls/         # 시스템 콜
    └── 03_Go_System_Integration/ # Go 시스템 통합
```

---

## 학습 경로

### Go 입문자
```
00_References/Learning_Go: 01 → 02 → 03 → 04 → 05 → 06 → 07
```

### Go 심화
```
00_References/Learning_Go: 08(Generics) → 09(Errors) → 12(Concurrency) → 14(Context)
```

### 시스템 프로그래밍
```
11_System_Programming: 01_OS_Fundamentals → 02_System_Calls → 03_Go_System_Integration
```

### 마이크로서비스
```
00_References/Learning_Go 기초 → 00_References/gRPC_Microservices 전체
```

---

## 관련 실습

- [poc/02-go](../../poc/02-go/): Go 언어 실습 코드
  - `01-fundamentals/`: 기초 문법 실습
  - `02-standard-library/`: 표준 라이브러리 실습
  - `03-concurrency/`: 동시성 실습
  - `04-web/`: 웹 개발 실습
  - `05-cli/`: CLI 개발 실습
  - `06-database/`: 데이터베이스 실습
  - `11-system-programming/`: 시스템 프로그래밍 실습

---

## 폴더별 내용

### 00_References/Learning_Go
Go 언어 핵심 문법과 고급 기능

| 파일 | 내용 | 키워드 |
|------|------|--------|
| 01_Setting_Up_Your_Go_Environment.md | 개발 환경 설정 | go mod, GOPATH |
| 02_Predeclared_Types_and_Declarations.md | 기본 타입, 선언 | int, string, var, const |
| 03_Composite_Types.md | 복합 타입 | array, slice, map, struct |
| 04_Blocks_Shadows_and_Control_Structures.md | 블록, 섀도잉, 제어문 | if, for, switch |
| 05_Functions.md | 함수 | func, defer, closure |
| 06_Pointers.md | 포인터 | *, &, nil |
| 07_Types_Methods_and_Interfaces.md | 타입, 메서드, 인터페이스 | type, interface |
| 08_Generics.md | 제네릭 | type parameters, constraints |
| 09_Errors.md | 에러 처리 | error, panic, recover |
| 10_Modules_Packages_and_Imports.md | 모듈, 패키지 | go mod, import |
| 11_Go_Tooling.md | Go 도구 | go build, test, vet |
| 12_Concurrency_in_Go.md | 동시성 | goroutine, channel, select |
| 13_The_Standard_Library.md | 표준 라이브러리 | fmt, io, net/http |
| 14_The_Context.md | Context | context.Context, timeout |
| 15_Writing_Tests.md | 테스트 | testing, benchmark |
| 16_Reflect_Unsafe_Cgo.md | 리플렉션, unsafe, Cgo | reflect, unsafe, cgo |
| 17_From_TCP_to_HTTP_Network_Programming.md | 네트워크 프로그래밍 | TCP, HTTP, net |
| 18_Order_Management_System_Microservices.md | 주문 관리 시스템 | 마이크로서비스 실습 |

### 00_References/gRPC_Microservices
gRPC 기반 마이크로서비스 개발

| 파일 | 내용 | 키워드 |
|------|------|--------|
| 01_Introduction.md | gRPC 소개 | Protocol Buffers, RPC |
| 02_gRPC_Meets_Microservices.md | gRPC와 마이크로서비스 | 서비스 분리, API 설계 |
| 03_Getting_Up_and_Running.md | gRPC 시작하기 | protoc, grpc-go |
| 04_Microservice_Project_Setup.md | 프로젝트 구조 | 디렉토리 구조, 설정 |
| 05_Interservice_Communication.md | 서비스 간 통신 | Unary, Streaming |
| 06_Resilient_Communication.md | 복원력 있는 통신 | Retry, Circuit Breaker |
| 07_Testing_Microservices.md | 마이크로서비스 테스트 | Unit, Integration |
| 08_Deployment.md | 배포 | Docker, Kubernetes |
| 09_Observability.md | 관측 가능성 | Tracing, Metrics, Logging |

### 11_System_Programming
Go로 배우는 시스템 프로그래밍

| 폴더 | 내용 | 키워드 |
|------|------|--------|
| 01_OS_Fundamentals/ | OS 기초 개념 | 프로세스, 메모리, I/O |
| 02_System_Calls/ | 시스템 콜 | syscall, file descriptors |
| 03_Go_System_Integration/ | Go 시스템 통합 | cgo, unsafe |

---

## 출처

| 출처 | 원본 |
|------|------|
| Learning Go | Learning Go, 2nd Edition - Jon Bodner (O'Reilly) |
| gRPC | gRPC Microservices in Go - Hüseyin Babal (Packt) |

---

## 핵심 개념

### Go 언어 특징
| 특징 | 설명 |
|------|------|
| **정적 타입** | 컴파일 타임 타입 검사 |
| **가비지 컬렉션** | 자동 메모리 관리 |
| **동시성** | goroutine, channel 기반 |
| **단순함** | 25개 키워드, 명확한 문법 |

### gRPC 특징
| 특징 | 설명 |
|------|------|
| **Protocol Buffers** | 효율적인 바이너리 직렬화 |
| **HTTP/2** | 멀티플렉싱, 스트리밍 |
| **코드 생성** | .proto → 클라이언트/서버 코드 |
| **다중 언어** | Go, Java, Python 등 지원 |

---

## 학습 체크리스트

### Go 기초
- [ ] 기본 타입과 선언 이해
- [ ] slice, map, struct 활용
- [ ] 함수, 클로저, defer 사용
- [ ] 인터페이스와 타입 임베딩

### Go 심화
- [ ] goroutine과 channel 이해
- [ ] context를 활용한 취소/타임아웃
- [ ] 제네릭 활용
- [ ] 테스트 작성

### 시스템 프로그래밍
- [ ] OS 기초 개념 이해
- [ ] 시스템 콜 이해
- [ ] Go와 시스템 통합

### gRPC
- [ ] Protocol Buffers 작성
- [ ] Unary/Streaming RPC 구현
- [ ] 에러 처리와 복원력 패턴
- [ ] 배포와 관측 가능성

---

## 참고 자료

### 공식 문서
- [Go Documentation](https://go.dev/doc/)
- [gRPC Documentation](https://grpc.io/docs/)
- [Protocol Buffers](https://protobuf.dev/)

---

*마지막 업데이트: 2026-02-02*
