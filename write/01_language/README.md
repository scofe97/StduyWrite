---
title: 01_language MOC
tags: [moc, language]
status: final
related: []
updated: 2026-04-19
---

# 01_language
---
> 언어별 문법·관용구·표준 라이브러리·빌드 도구를 모은다. JVM 관련 런타임 지식은 Java 하위 `09_jvm/`에 둔다.

## 하위

- [_writing/](_writing/) — 언어중립 코드 작성·리팩토링 원칙(클린 코드·리팩토링). 언어 폴더보다 앞에 두는 공통 묶음
- [java/](java/) — Java 언어·표준 라이브러리·JVM·빌드
  - `01_Core`, `02_TypeSystem`, `03_Collections`, `04_Lambda`, `05_Concurrency`, `06_Modern`, `07_DesignPatterns`, `08_Testing`, **`09_jvm`** (JVM·GC·바이트코드), `10_IO`, `11_Build`
- [python/](python/) — Python 선택 기준·통합 테스트·자동화 스크립트

## 경계 기준

Spring Boot 설정, Spring Kafka 같이 프레임워크 의존적인 내용은 `spring/` 하위로 따로 둘 예정이다. 이 카테고리는 "언어 레퍼런스에 나오는 내용"에 가까운 최종본만 둔다.

Kotlin·Scala 문서가 5개 이상 쌓이는 시점에 `02_runtime/`을 다시 살려 JVM 공통분을 분리한다. 그 전까지는 "JVM은 Java와 함께"가 실사용 흐름에 맞다.
