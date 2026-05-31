---
title: 01_language/_writing MOC
tags: [moc, clean-code, refactoring, code-quality]
status: final
related:
  - ../README.md
  - ../java/03_DesignPatterns/README.md
updated: 2026-05-31
---

# 01_language/_writing — 코드 작성·리팩토링

> 특정 언어에 종속되지 않는 *코드 작성·리팩토링 원칙*을 모은다. 네이밍·함수·주석 같은 줄 단위 미시 규칙(클린 코드)과, 그 좋은 코드에 도달하는 리팩토링 절차·규칙이다. Java·Python처럼 언어 폴더(java/·python/)와 형제로 두되, 언어 무관 공통이라 `_` prefix로 맨 앞에 둔다.

## 하위

- [01-01.클린 코드 원칙](01-01.클린%20코드%20원칙.md) — 네이밍·함수·주석·예외·CQS·디미터·테스트 등 줄 단위 미시 규칙 (좋은 코드의 *기준*)
- 02-01.리팩토링 절차와 규칙 — *작성 예정*: Five Lines of Code 기반 리팩토링 규칙·절차 (그 기준에 *도달하는 법*)

## 경계 기준

여기는 *언어중립* 코드 작성·리팩토링 원칙만 둔다. 언어에 종속된 코드 스타일은 각 언어 폴더에 둔다 — 일급객체·Optional/Stream 활용 같은 Java 코드 스타일은 [`../java/03_DesignPatterns/02-01`](../java/03_DesignPatterns/02-01.일급객체%20사상과%20Java%20코드%20스타일.md), 함수형 패턴이 Spring 인프라와 만나는 함정은 [`../java/03_DesignPatterns/02-03`](../java/03_DesignPatterns/02-03.함수형%20패턴%20도입의%20함정과%20경계%20설계.md)에 있다.

클래스·모듈 단위 거시 *설계* 원칙(SOLID·계층·의존성)은 코드 작성이 아니라 설계라, [`../java/03_DesignPatterns/01-01.SOLID 원칙`](../java/03_DesignPatterns/01-01.SOLID%20원칙.md)과 [`03_architecture/`](../../03_architecture/)가 맡는다. *도메인 모델* 차원의 리팩토링도 [`03_architecture/04_ddd/03-01`](../../03_architecture/04_ddd/03-01.리팩토링%20원칙%20—%20행동하기%20전에%20이해하기.md)에 별도로 있다. 이 폴더는 그보다 작은 *함수·줄 단위*의 작성·개선에 집중한다.
