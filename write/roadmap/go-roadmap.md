---
title: Go 학습 로드맵
tags: [roadmap, go, concurrency, testing, cloud-native]
status: final
related:
  - README.md
  - os-roadmap.md
  - network-roadmap.md
updated: 2026-09-12
---

# Go 학습 로드맵
---

> 문법을 빠르게 통과한 뒤 값 의미론, 인터페이스, 동시성, 테스트, 성능, 네트워크 서비스 순서로 학습합니다.

![문법에서 네트워크 서비스까지 이어지는 Go 학습 순서](_assets/go-roadmap.svg)

## 학습 순서

> 같은 자료의 밀접한 주제는 한 행에 묶고, 자료가 달라지는 지점에서 행을 나눴습니다.

| 단계 | 우선순위 | 주제 | 키워드 | 학습 문서 | 완료 기준 |
|---|:---:|---|---|---|---|
| 1. 문법 | 필수 | 선수지식 · 기본 문법 | variable·constant<br>`if`·`for`·`switch`<br>function·multiple return·`defer` | [A Tour of Go](https://go.dev/tour/) · Learning Go 2판 1~6장 | 작은 프로그램을 패키지와 함수로 나눠 작성합니다. |
| 1. 문법 | 필수 | 핵심 · 컬렉션·값 의미론 | array·slice·capacity·append<br>map·struct·pointer<br>copy·zero value | Learning Go 2판 1~6장 · [Language Specification](https://go.dev/ref/spec) | 배열·슬라이스·구조체를 넘길 때 무엇이 복사되고 공유되는지 설명합니다. |
| 2. 타입 설계 | 필수 | 핵심 · 메서드·인터페이스 | receiver·method set·embedding<br>implicit implementation<br>type assertion·type switch | Learning Go 2판 7~9장 | 인터페이스를 사용하는 패키지에 두고 작은 계약으로 설계합니다. |
| 2. 타입 설계 | 필수 | 실습 · 에러·제네릭 | error value·wrapping<br>`errors.Is/As`·sentinel<br>type parameter·constraint | Learning Go 2판 8~9장 · [Go blog](https://go.dev/blog/) | 실패 맥락을 보존하는 에러 체인과 필요한 범위의 제네릭을 작성합니다. |
| 3. 관용구·도구 | 필수 | 핵심 · Go 관용구 | package boundary·naming<br>composition·interface placement<br>receiver choice | [Effective Go](https://go.dev/doc/effective_go) · [Code Review Comments](https://go.dev/wiki/CodeReviewComments) | Java식 상속과 예외 중심 설계를 Go의 조합과 에러 값으로 바꿉니다. |
| 3. 관용구·도구 | 필수 | 실습 · 모듈·도구 체인 | module·MVS·workspace<br>`gofmt`·`go vet`·staticcheck | Learning Go 2판 10·11·13·14장 · [Go tutorials](https://go.dev/doc/tutorial/) | 모듈 의존성을 설명하고 표준 도구로 빌드·검사합니다. |
| 3. 관용구·도구 | 추천 | 진단 · 흔한 실수 | slice aliasing·interface nil<br>goroutine leak·loop variable<br>context misuse | 100 Go Mistakes · [100go.co](https://100go.co/) | 코드 리뷰에서 소유권, nil, 누수 위험을 재현하고 고칩니다. |
| 4. 동시성 | 필수 | 선수지식 · 고루틴·동기화 | goroutine·`GOMAXPROCS`·scheduler<br>mutex·condition variable<br>WaitGroup·semaphore | Learn Concurrent Programming with Go 1~7장 | 공유 상태를 보호하고 고루틴의 종료 조건을 명시합니다. |
| 4. 동시성 | 필수 | 핵심 · 채널·취소 | channel·buffered channel·`select`<br>pipeline·fan-in/fan-out<br>context·cancellation·errgroup | Learning Go 2판 12장 · Learn Concurrent Programming with Go 8~10장 | 작업 실패와 취소가 모든 고루틴에 전파되는 파이프라인을 만듭니다. |
| 4. 동시성 | 추천 | 진단 · 메모리 모델 | happens-before·race·atomic<br>`sync.Once`·`atomic.Value`<br>deadlock | [The Go Memory Model](https://go.dev/ref/mem) · Learn Concurrent Programming with Go 11~12장 | 동기화가 보장하는 가시성을 설명하고 `go test -race`로 경합을 찾습니다. |
| 5. 테스트·성능 | 필수 | 실습 · 테스트 | table-driven test·test double·coverage<br>benchmark·fuzzing·golden file | [Learn Go with Tests](https://quii.gitbook.io/learn-go-with-tests) · Learning Go 2판 15장 | 행위 경계를 표 주도 테스트로 검증하고 퍼징·벤치마크 대상을 고릅니다. |
| 5. 테스트·성능 | 추천 | 진단 · 프로파일·런타임 | pprof·trace·CPU/heap profile<br>allocation·GC·`GOGC/GOMEMLIMIT`<br>escape analysis | [Go diagnostics](https://go.dev/doc/diagnostics) · Learning Go 2판 16장 · [OS 로드맵](os-roadmap.md) | 추측 대신 프로파일로 CPU·메모리 병목을 확인합니다. |
| 6. 서비스 | 필수 | 실습 · 네트워크·HTTP | address resolution·TCP/UDP<br>`net`·`net/http`·routing<br>client/server timeout·`log/slog` | Network Programming with Go 1~9장 · [네트워크 로드맵](network-roadmap.md) | timeout과 취소가 있는 HTTP 클라이언트·서버를 작성하고 연결 문제의 층을 구분합니다. |
| 6. 서비스 | 추천 | 실습·진단 · 클라우드 네이티브 | resilience·loose coupling<br>graceful shutdown·configuration<br>observability·OpenTelemetry·security | Cloud Native Go 2판 4~13장 | 종료·관측·복원력 경계를 갖춘 서비스를 배포 가능한 형태로 구성합니다. |



## 책 읽기 흐름

> 단계 표에 연결된 책을 처음 읽는 시점과 집중할 범위를 표시합니다.

![Go 책 읽기 흐름](_assets/go-books.svg)
