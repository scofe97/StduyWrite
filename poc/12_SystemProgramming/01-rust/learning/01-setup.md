# 01. Setup & First Program

Rust 개발 환경을 구축하고 첫 프로그램을 작성합니다. Cargo는 Rust의 빌드 시스템이자 패키지 매니저로, 프로젝트 생성부터 의존성 관리, 빌드, 테스트까지 모든 것을 관리합니다. Rustup은 Rust 툴체인 버전 관리 도구입니다.

## 목표

이 챕터를 완료하면 다음을 할 수 있어야 합니다:

- [ ] rustup과 cargo를 설치하고 버전을 확인할 수 있다
- [ ] 새로운 Rust 프로젝트를 cargo로 생성할 수 있다
- [ ] Cargo.toml 파일의 구조와 역할을 설명할 수 있다
- [ ] cargo build, run, test 명령어를 사용할 수 있다
- [ ] cargo check와 cargo build의 차이를 설명할 수 있다
- [ ] REPL(evcxr)을 설치하고 간단한 표현식을 실행할 수 있다

## rustup 설치

## Cargo 프로젝트 구조

## Hello World

## cargo build/run/test

## REPL(evcxr)

## 명령어 요약

| 명령어 | 설명 |
|--------|------|
| `rustup install stable` | 안정 버전 Rust 설치 |
| `rustup update` | Rust 툴체인 업데이트 |
| `cargo --version` | Cargo 버전 확인 |
| `cargo new <project>` | 새 프로젝트 생성 (바이너리) |
| `cargo new --lib <name>` | 새 라이브러리 프로젝트 생성 |
| `cargo build` | 디버그 빌드 (target/debug/) |
| `cargo build --release` | 릴리스 빌드 (최적화, target/release/) |
| `cargo run` | 빌드 후 실행 |
| `cargo check` | 컴파일 검사만 (바이너리 생성 X, 빠름) |
| `cargo test` | 테스트 실행 |
| `cargo install evcxr_repl` | Rust REPL 설치 |
| `evcxr` | REPL 시작 |

## 체크포인트

1. **Cargo.toml의 역할은 무엇인가?**
   - 프로젝트 메타데이터(이름, 버전, edition)와 의존성을 정의하는 매니페스트 파일

2. **cargo check와 cargo build의 차이는?**
   - `check`: 컴파일 에러만 검사, 바이너리 생성 X → 빠름
   - `build`: 실행 파일 생성 → 느림

3. **edition의 의미는?**
   - Rust 언어 버전(2015, 2018, 2021 등), 크레이트마다 독립적으로 설정 가능, 하위 호환성 보장

4. **cargo run은 빌드를 포함하는가?**
   - 예, 변경사항이 있으면 자동으로 빌드 후 실행

5. **target/debug와 target/release의 차이는?**
   - debug: 최적화 X, 디버그 정보 포함, 빠른 컴파일
   - release: 최적화 O, 디버그 정보 최소화, 느린 컴파일, 빠른 실행
