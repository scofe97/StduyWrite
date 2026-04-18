# 16. CLI 도구 개발

Rust는 크로스 플랫폼 바이너리 배포와 빠른 실행 속도로 CLI 도구 개발에 적합합니다. clap으로 인자 파싱, serde로 구성 파일 처리, std::fs로 파일 I/O를 수행하며, 통합 테스트와 릴리즈 빌드로 프로덕션 품질을 보장합니다. cargo install로 간편하게 배포할 수 있습니다.

## 목표
- [ ] clap derive API로 CLI 인자 파싱 구조 설계
- [ ] serde로 JSON/TOML 파일 읽기/쓰기
- [ ] std::fs로 파일 I/O 처리
- [ ] anyhow/thiserror로 에러 처리 통합
- [ ] 통합 테스트(tests/ 디렉토리) 작성
- [ ] 릴리즈 빌드 및 크로스 컴파일
- [ ] cargo install로 배포

## 1. clap으로 인자 파싱

## 2. serde로 직렬화/역직렬화

## 3. 파일 I/O(std::fs)

## 4. 에러 처리 통합

## 5. 테스트 작성

## 6. 크로스 컴파일

## 명령어 요약
| 개념 | 설명 |
|------|------|
| `clap::Parser` | derive 매크로로 CLI 구조 정의 |
| `serde::Deserialize` | JSON/TOML → Rust 구조체 |
| `std::fs::read_to_string` | 파일 읽기 |
| `std::fs::write` | 파일 쓰기 |
| `anyhow::Result` | 범용 에러 타입 |
| `thiserror::Error` | 커스텀 에러 타입 derive |
| `cargo build --release` | 최적화 빌드 |
| `cargo install --path .` | 로컬 바이너리 설치 |

## 체크포인트
- clap의 derive API vs builder API의 트레이드오프는?
- serde의 동작 원리(proc macro)는 무엇인가?
- anyhow vs thiserror를 선택하는 기준은?
- cargo install로 배포하는 방법은?
- 통합 테스트와 단위 테스트의 차이는?
- 릴리즈 빌드에서 최적화 수준 조정 방법은?
- 크로스 컴파일 시 target triple이란?
