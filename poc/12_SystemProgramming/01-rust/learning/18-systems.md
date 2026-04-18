# 18. 시스템 프로그래밍

Rust는 zero-cost abstractions와 메모리 안전성으로 시스템 프로그래밍에 이상적입니다. 커스텀 메모리 할당기로 low-level 제어를, TCP 서버로 네트워크 프로토콜 구현을, Wasm 타겟으로 웹 환경 배포를 수행합니다. perf와 flamegraph로 성능을 프로파일링하여 병목을 제거합니다.

## 목표
- [ ] GlobalAlloc 트레이트로 커스텀 메모리 할당기 구현
- [ ] std::net으로 TCP 에코 서버 구현
- [ ] 바이너리 프로토콜 파싱
- [ ] wasm-pack으로 Wasm 타겟 빌드
- [ ] perf와 flamegraph로 성능 프로파일링
- [ ] Rust가 시스템 프로그래밍에 적합한 이유 설명

## 1. 커스텀 메모리 할당기(GlobalAlloc)

## 2. TCP 서버 구현

## 3. 프로토콜 파싱

## 4. Wasm 컴파일(wasm-pack)

## 5. 성능 프로파일링

## 명령어 요약
| 개념 | 설명 |
|------|------|
| `GlobalAlloc` | 커스텀 메모리 할당기 트레이트 |
| `#[global_allocator]` | 전역 할당기 지정 |
| `std::net::TcpListener` | TCP 서버 생성 |
| `std::net::TcpStream` | TCP 연결 |
| `wasm-pack build` | Wasm 빌드 |
| `cargo flamegraph` | flamegraph 생성 |
| `perf record` | 성능 데이터 수집 |

## 체크포인트
- Rust가 시스템 프로그래밍에 적합한 이유는?
- zero-cost abstractions란 무엇인가?
- Wasm에서 GC가 불필요한 이유는?
- GlobalAlloc 구현 시 주의할 점은?
- TCP와 UDP의 선택 기준은?
- 프로토콜 파싱에서 endianness란?
- flamegraph를 읽는 방법은?
- Rust의 시스템 프로그래밍 vs C/C++의 트레이드오프는?
