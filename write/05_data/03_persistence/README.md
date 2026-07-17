---
title: 05_data/03_persistence — 애플리케이션 영속성
tags: [moc, persistence, jdbc, jpa, mybatis, querydsl, spring]
status: draft
related:
  - ../README.md
  - ../roadmap.md
  - ../02_relational/README.md
updated: 2026-07-15
---

# 03_persistence — 애플리케이션 영속성
---
> Spring 애플리케이션이 관계형 DB와 연결되는 계층을 JDBC부터 JPA·MyBatis·QueryDSL까지 한 흐름으로 다룹니다. 추상화가 높아질수록 SQL·트랜잭션·인덱스의 원리를 대신하지 않으므로, 관계형 DB 기초를 먼저 익히는 것이 좋습니다.

## 읽는 순서

1. [jdbc/](./jdbc/README.md)에서 DataSource·커넥션 풀·JdbcTemplate·예외 추상화를 익힙니다.
2. [jpa/](./jpa/README.md)에서 영속성 컨텍스트·매핑·Spring Data JPA·트랜잭션·락을 연결합니다.
3. [querydsl/](./querydsl/README.md)에서 동적 조회·프로젝션·페이징·복잡한 쿼리 조립을 확장합니다.

## 하위 묶음

| 경로 | 범위 |
|---|---|
| [jdbc/](./jdbc/README.md) | JDBC 표준, 커넥션 풀, JdbcTemplate, 드라이버 관측 |
| [jpa/](./jpa/README.md) | JPA·Spring Data JPA·MyBatis·트랜잭션·락 |
| [querydsl/](./querydsl/README.md) | 타입 안전 쿼리, 동적 조건, 프로젝션, 페이징, 실무 통합 |

## 관련 문서

- [02_relational](../02_relational/README.md) — SQL·인덱스·MVCC·엔진 관점의 기반
- [06_operations](../06_operations/README.md) — 개발·테스트 환경에서 DB 의존성을 다루는 방법
