---
title: 06_data/spring — Spring Data·영속성
tags: [moc, spring, data, jpa]
status: final
source:
  - https://docs.spring.io/spring-boot/docs/3.2.3/reference/htmlsingle/
  - https://docs.spring.io/spring-data/jpa/reference/
  - experience  # 본 저장소 학습 트리 운영 경험에서 분류 도출
related:
  - ../README.md
  - ../../01_language/java/spring/README.md
  - ./querydsl/README.md
updated: 2026-05-16
---

# 06_data/spring
---
> Spring Data JPA, R2DBC, `@Transactional`처럼 Spring의 영속성·트랜잭션 기술을 모은다.

## 경계

- DB 자체 이론(격리 수준, 인덱싱, CDC)은 [`06_data/`](../) 직접 하위
- JPA/Hibernate의 순정 이론(1차 캐시, 지연 로딩)도 [`06_data/`](../)
- **Spring이 JPA를 어떻게 감싸는가** — 여기다. `@Transactional` 전파 동작, JpaRepository 추상화 등

## 완료

- [`querydsl/`](querydsl/README.md) — QueryDSL 6.12 (OpenFeign fork) + Spring Boot 3.2.3 학습 묶음 10개 문서. 표준 9편(입문·셋업·기본 문법·동적 쿼리·프로젝션·페이징 함정·커스텀 리포지토리·테스트/멀티모듈·6.12→7.x 마이그레이션) + 실무 변형 1편(PathBuilder·Embedded ID·상관 서브쿼리·JPQL limit 한계·동적 검색 추상 베이스·nullExpression)

## 예정 주제

- Spring Data JPA Repository 추상화
- `@Transactional` 전파 모드와 격리 수준 조합
- R2DBC와 리액티브 트랜잭션
- Outbox 구현 시 Spring Transaction 활용

## 관련 문서

- [Spring 통합 MOC](../../01_language/java/spring/README.md)
