---
title: 06_data/spring — Spring Data·영속성
tags: [moc, spring, data, jpa]
status: final
related:
  - ../README.md
  - ../../01_language/java/spring/README.md
updated: 2026-04-19
---

# 06_data/spring
---
> Spring Data JPA, R2DBC, `@Transactional`처럼 Spring의 영속성·트랜잭션 기술을 모은다.

## 경계

- DB 자체 이론(격리 수준, 인덱싱, CDC)은 [`06_data/`](../) 직접 하위
- JPA/Hibernate의 순정 이론(1차 캐시, 지연 로딩)도 [`06_data/`](../)
- **Spring이 JPA를 어떻게 감싸는가** — 여기다. `@Transactional` 전파 동작, JpaRepository 추상화 등

## 예정 주제

- Spring Data JPA Repository 추상화
- `@Transactional` 전파 모드와 격리 수준 조합
- R2DBC와 리액티브 트랜잭션
- Outbox 구현 시 Spring Transaction 활용

## 관련 문서

- [Spring 통합 MOC](../../01_language/java/spring/README.md)
