---
title: 01_language MOC
tags: [moc, language]
status: final
related: []
updated: 2026-11-14
---

# 01_language

> 언어별 문법·관용구·표준 라이브러리·빌드 도구를 모으고 JVM 관련 런타임 지식을 다룹니다.

## 경계 기준

Spring Boot 설정, Spring Kafka 같이 프레임워크 의존적인 내용은 `spring/` 하위로 따로 둘 예정입니다. 이 카테고리는 "언어 레퍼런스에 나오는 내용"에 가까운 최종본만 둡니다.

Kotlin·Scala 문서가 5개 이상 쌓이는 시점에 `02_runtime/`을 다시 살려 JVM 공통분을 분리합니다. 그 전까지는 "JVM은 Java와 함께"가 실사용 흐름에 맞습니다.



## 키워드

### go-keywords.md

키워드 파일: [go-keywords.md](go-keywords.md)

| 묶음 | 다룬 문서 | 빈 필수 키워드 |
|---|---|---|
| 1단계 · 문법 | 17편 | — |
| 2단계 · 타입 설계 | 10편 | — |
| 3단계 · 관용구와 도구 | 23편 | — |
| 4단계 · 동시성 | 5편 | 메모리 공유와 경쟁 상태 · message passing · 채널 프로그래밍 · happens-before · `go test -race` · 채널 소유권 — 닫기는 한 곳에서만 |
| 5단계 · 테스트와 성능 | 5편 | pprof — CPU · heap · block · mutex profile |
| 6단계 · 서비스 | 7편 | — |
| 7단계 · 터미널과 세션 | 0편 | SSH 3계층 — 전송 · 사용자 인증 · 연결 · `pty-req` 와 `window-change` · 세션 채널과 애플리케이션의 경계 · rune 과 grapheme 과 터미널 셀 폭 · 논블로킹 알림과 신호 병합 · 인증과 인가는 다른 문제다 |

### jvm-keywords.md

키워드 파일: [jvm-keywords.md](jvm-keywords.md)

| 묶음 | 다룬 문서 | 빈 필수 키워드 |
|---|---|---|
| 1단계 · 실행 모델 | 7편 | — |
| 2단계 · 클래스 로딩 | 14편 | — |
| 3단계 · 실행 엔진과 컴파일 | 14편 | — |
| 4단계 · 가비지 컬렉션 | 17편 | — |
| 5단계 · 동시성 | 17편 | — |
| 6단계 · 성능 측정과 튜닝 | 23편 | — |
| 7단계 · 장애 진단 | 27편 | — |



## 하위 폴더·문서 목록

- [java/](java/) — Java 언어·표준 라이브러리·JVM·빌드
  - [book/five-lines-of-code/](book/five-lines-of-code/) — 언어중립 코드 작성·리팩토링 원칙(클린 코드·Five Lines of Code)
  - [book/sicp_structure-and-interpretation-of-computer-programs/](book/sicp_structure-and-interpretation-of-computer-programs/) — 언어중립 프로그래밍 원리서(SICP JavaScript판) — 추상화·인터프리터·레지스터 머신·GC
  - `01_Core`, `02_TypeSystem`, `03_Collections`, `04_Lambda`, `05_Concurrency`, `06_Modern`
  - `07_DesignPatterns`, `08_Testing`, **`09_jvm`** (JVM·GC·바이트코드), `10_IO`, `11_Build`
- Go
  - [book/lgo_learning-go/](book/lgo_learning-go/README.md) — Go 문법 정독(Learning Go 2판) — 타입·slice·인터페이스·에러·제네릭·모듈·동시성·테스트
  - [docs/go/](docs/README.md) — Go 표준 라이브러리 공식문서 정독(pkg.go.dev + go1.25.1 소스) — net · net/http
