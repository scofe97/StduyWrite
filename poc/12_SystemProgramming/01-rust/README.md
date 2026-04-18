# Rust 시스템 프로그래밍 학습

Java/Spring Boot 백엔드 개발자가 CS 기초 실력 강화를 위해 Rust를 학습합니다.
메모리 모델, 소유권, 타입 시스템을 깊이 이해하여 어떤 언어/시스템을 다루더라도 탄탄한 기초를 갖추는 것이 목표입니다.

---

## 학습 목표

1. 소유권/빌림/라이프타임의 원리를 설명하고 컴파일 에러를 해결할 수 있다
2. idiomatic Rust 코드를 작성할 수 있다 (enum, trait, Result/Option)
3. 멀티스레드/비동기 프로그램을 안전하게 작성할 수 있다
4. CLI 도구, Web API, 시스템 프로그래밍 프로젝트를 완성할 수 있다

---

## 학습 리소스

| 리소스 | 용도 | 비용 |
|--------|------|------|
| [The Rust Book](https://doc.rust-lang.org/book/) | 메인 교재 | 무료 |
| [Rustlings](https://github.com/rust-lang/rustlings) | 연습 문제 (Phase 1~2) | 무료 |
| [Rust by Example](https://doc.rust-lang.org/rust-by-example/) | 예제 참조 | 무료 |
| [Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/) | 소유권 심화 | 무료 |
| [Tokio Tutorial](https://tokio.rs/tokio/tutorial) | 비동기 (Ch14) | 무료 |

---

## 커리큘럼

### Phase 1: 기초 — "Java와 다른 세계" (3~4주)

| 순서 | 파일 | 주제 | Java 대비 차이점 |
|------|------|------|-----------------|
| 01 | [01-setup](./learning/01-setup.md) | Setup & First Program | Maven/Gradle → Cargo |
| 02 | [02-variables-types](./learning/02-variables-types.md) | 변수, 타입, 함수 | 모든 것이 불변 기본 |
| 03 | [03-ownership](./learning/03-ownership.md) | 소유권(Ownership) | **GC 없음** — 가장 큰 차이 |
| 04 | [04-borrowing](./learning/04-borrowing.md) | 참조와 빌림(Borrowing) | 참조 ≠ Java 참조 |
| 05 | [05-lifetimes](./learning/05-lifetimes.md) | 라이프타임(Lifetimes) | Java에 없는 개념 |

### Phase 2: 언어 핵심 — "Rust다운 코드 작성" (3~4주)

| 순서 | 파일 | 주제 | Java 대비 차이점 |
|------|------|------|-----------------|
| 06 | [06-structs-enums](./learning/06-structs-enums.md) | 구조체와 열거형 | enum이 데이터를 가짐 (ADT) |
| 07 | [07-traits](./learning/07-traits.md) | 트레이트(Traits) | interface + 더 강력 |
| 08 | [08-generics](./learning/08-generics.md) | 제네릭과 타입 시스템 | 타입 소거 없음 (단형화) |
| 09 | [09-error-handling](./learning/09-error-handling.md) | 에러 처리 | try-catch 없음 |
| 10 | [10-collections-iterators](./learning/10-collections-iterators.md) | 컬렉션과 이터레이터 | Stream API와 유사하지만 지연 |

### Phase 3: 고급 — "성능과 동시성" (4~5주)

| 순서 | 파일 | 주제 | Java 대비 차이점 |
|------|------|------|-----------------|
| 11 | [11-closures](./learning/11-closures.md) | 클로저와 함수형 패턴 | 3가지 클로저 트레이트 구분 |
| 12 | [12-smart-pointers](./learning/12-smart-pointers.md) | 스마트 포인터 | GC 대신 직접 선택 |
| 13 | [13-concurrency](./learning/13-concurrency.md) | 동시성(Concurrency) | 컴파일 타임 데이터 레이스 방지 |
| 14 | [14-async](./learning/14-async.md) | 비동기(Async/Await) | CompletableFuture보다 저수준 |
| 15 | [15-unsafe-ffi](./learning/15-unsafe-ffi.md) | unsafe와 FFI | JNI보다 직접적 |

### Phase 4: 실전 — "프로젝트로 증명" (3~4주)

| 순서 | 파일 | 주제 | 연계 |
|------|------|------|------|
| 16 | [16-cli-tool](./learning/16-cli-tool.md) | CLI 도구 개발 | clap, serde, 파일 I/O |
| 17 | [17-web-api](./learning/17-web-api.md) | Web API (Axum) | Spring Boot 대비 비교 |
| 18 | [18-systems](./learning/18-systems.md) | 시스템 프로그래밍 | 메모리 할당기, 네트워크, Wasm |

---

## 예상 소요 기간

| Phase | 기간 | 난이도 |
|-------|------|--------|
| Phase 1 (기초) | 3~4주 | 높음 (소유권 장벽) |
| Phase 2 (핵심) | 3~4주 | 중간 |
| Phase 3 (고급) | 4~5주 | 높음 |
| Phase 4 (실전) | 3~4주 | 중간 |
| **합계** | **약 3~4개월** | |

---

## 진행 상태

### Phase 1: 기초
- [ ] 01-setup: Setup & First Program
- [ ] 02-variables-types: 변수, 타입, 함수
- [ ] 03-ownership: 소유권
- [ ] 04-borrowing: 참조와 빌림
- [ ] 05-lifetimes: 라이프타임

### Phase 2: 언어 핵심
- [ ] 06-structs-enums: 구조체와 열거형
- [ ] 07-traits: 트레이트
- [ ] 08-generics: 제네릭과 타입 시스템
- [ ] 09-error-handling: 에러 처리
- [ ] 10-collections-iterators: 컬렉션과 이터레이터

### Phase 3: 고급
- [ ] 11-closures: 클로저와 함수형 패턴
- [ ] 12-smart-pointers: 스마트 포인터
- [ ] 13-concurrency: 동시성
- [ ] 14-async: 비동기
- [ ] 15-unsafe-ffi: unsafe와 FFI

### Phase 4: 실전
- [ ] 16-cli-tool: CLI 도구 개발
- [ ] 17-web-api: Web API (Axum)
- [ ] 18-systems: 시스템 프로그래밍
