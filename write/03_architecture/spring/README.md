---
title: 03_architecture/spring — Spring 설계 철학
tags: [moc, spring, architecture, ioc, aop]
status: final
related:
  - ../../01_language/java/spring/README.md
updated: 2026-04-19
---

# 03_architecture/spring
---
> Spring의 **설계 철학** 관점. "왜 IoC인가", "AOP는 어떤 설계 문제를 푸는가" 같은 주제만 다룬다.

## 경계

Spring Framework의 구현 디테일(Bean Lifecycle, ApplicationContext API)은 [`01_language/java/spring/01_core/`](../../01_language/java/spring/01_core/)에 속한다. 여기는 "IoC는 Dependency Inversion Principle의 구현", "AOP는 Decorator 패턴의 프레임워크화" 처럼 아키텍처 원칙과의 연결을 다룬다.

문서량이 3개 이하면 이 폴더 없이 `03_architecture/` 직접 하위에 놓아도 된다. 5개 이상이 되면 별도 폴더 유지가 맞다.

## 예정 주제

- `01_ioc-as-design-pattern.md` — IoC를 GoF·DIP 관점으로 해석
- `02_aop-as-decorator.md` — AOP가 해결하는 횡단 관심사 문제
- `03_convention-over-configuration.md` — Spring Boot의 철학

## 관련 문서

- [Spring 통합 MOC](../../01_language/java/spring/README.md) — 전 카테고리 Spring 문서 집계점
