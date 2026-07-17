---
title: 05_data/03_persistence/jpa — JPA · Spring Data JPA · MyBatis
tags: [moc, jpa, hibernate, spring-data-jpa, mybatis, transaction]
status: final
related:
  - ../README.md
  - ../../README.md
  - ../../roadmap.md
  - ../querydsl/README.md
updated: 2026-07-15
---

# 05_data/03_persistence/jpa — JPA · Spring Data JPA · MyBatis
---
> JPA 기본 (영속성·매핑·연관관계·상속·값 타입) + Spring Data JPA (공통 인터페이스·쿼리 메소드·Auditing·Projection) + 스프링 트랜잭션·락 + MyBatis. QueryDSL 은 [`../querydsl/`](../querydsl/) 가 다룬다.

## 01번대 — 입문

| # | 문서 |
|---|------|
| 01-01 | [ORM 개념](01-01.ORM%20%EA%B0%9C%EB%85%90.md) |
| 01-02 | [JPA 시작과 영속성 컨텍스트](01-02.JPA%20%EC%8B%9C%EC%9E%91%EA%B3%BC%20%EC%98%81%EC%86%8D%EC%84%B1%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8.md) |
| 01-03 | [식별자 전략](01-03.%EC%8B%9D%EB%B3%84%EC%9E%90%20%EC%A0%84%EB%9E%B5.md) |

## 02번대 — 매핑

| # | 문서 |
|---|------|
| 02-01 | [엔티티 맵핑](02-01.%EC%97%94%ED%8B%B0%ED%8B%B0%20%EB%A7%B5%ED%95%91.md) |
| 02-02 | [연관관계 매핑](02-02.%EC%97%B0%EA%B4%80%EA%B4%80%EA%B3%84%20%EB%A7%A4%ED%95%91.md) |
| 02-03 | [상속과 값 타입](02-03.%EC%83%81%EC%86%8D%EA%B3%BC%20%EA%B0%92%20%ED%83%80%EC%9E%85.md) |

## 03번대 — Spring Data JPA

| # | 문서 |
|---|------|
| 03-01 | [Spring Data JPA 공통 인터페이스](03-01.Spring%20Data%20JPA%20%EA%B3%B5%ED%86%B5%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4.md) |
| 03-02 | [쿼리 메소드](03-02.%EC%BF%BC%EB%A6%AC%20%EB%A9%94%EC%86%8C%EB%93%9C.md) |
| 03-03 | [프록시와 N+1](03-03.%ED%94%84%EB%A1%9D%EC%8B%9C%EC%99%80%20N+1.md) |
| 03-04 | [Auditing, 페이징, Projection](03-04.Auditing,%20%ED%8E%98%EC%9D%B4%EC%A7%95,%20Projection.md) |
| 03-05 | [커스텀 리포지토리 패턴](03-05.%EC%BB%A4%EC%8A%A4%ED%85%80%20%EB%A6%AC%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC%20%ED%8C%A8%ED%84%B4.md) — `RepositoryCustom` + `Impl` + fragment composition (QueryDSL 결합 예제 포함) |

## 04번대 — 트랜잭션·JPQL·락

| # | 문서 |
|---|------|
| 04-01 | [스프링 트랜잭션](04-01.%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98.md) |
| 04-01b | [트랜잭션 전파 활용 — 회원과 로그 시나리오](04-01b.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EC%A0%84%ED%8C%8C%20%ED%99%9C%EC%9A%A9.md) |
| 04-02 | [낙관적 비관적 락](04-02.%EB%82%99%EA%B4%80%EC%A0%81%20%EB%B9%84%EA%B4%80%EC%A0%81%20%EB%9D%BD.md) |
| 04-04 | [JPQL](04-04.JPQL.md) |

## 05번대 — 도메인 설계 사례

| # | 문서 |
|---|------|
| 05-01 | [도메인 설계 사례 — 주문 도메인](05-01.%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%84%A4%EA%B3%84%20%EC%82%AC%EB%A1%80.md) |

## 07번대 — 도구 혼용

| # | 문서 |
|---|------|
| 07-01 | [도구 혼용 패턴 — Spring Data JPA + QueryDSL 어댑터 vs 직접 사용](07-01.%EB%8F%84%EA%B5%AC%20%ED%98%BC%EC%9A%A9%20%ED%8C%A8%ED%84%B4.md) |

## 06번대 — MyBatis

| # | 문서 |
|---|------|
| 06-01 | [MyBatis 개요](06-01.MyBatis%20%EA%B0%9C%EC%9A%94.md) |
