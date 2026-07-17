---
title: 05_data/02_relational — 관계형 데이터베이스
tags: [moc, relational-database, sql, mysql, postgres, index, mvcc]
status: draft
related:
  - ../README.md
  - ../roadmap.md
  - ../01_foundation/README.md
  - ../03_persistence/README.md
updated: 2026-07-15
---

# 02_relational — 관계형 데이터베이스
---
> 관계형 모델을 SQL로 표현하고, 인덱스·MVCC·락 같은 엔진 동작을 해석한 뒤, MySQL과 PostgreSQL의 선택과 운영으로 확장합니다. ORM은 SQL을 없애지 않으므로 이 묶음이 `03_persistence/`의 선행 지식입니다.

## 읽는 순서

1. [sql-mysql/](./sql-mysql/README.md)에서 SQL, 정규화, 인덱스, MVCC와 동시성 제어를 익힙니다.
2. PostgreSQL을 쓴다면 [postgres/](./postgres/README.md)에서 제품 기능·인덱스·성능 관측을 이어서 봅니다.
3. 일반 원리의 근거가 필요하면 [01_foundation/](../01_foundation/README.md)의 데이터 모델·트랜잭션·인덱스 문서로 돌아갑니다.

## 하위 묶음

| 경로 | 범위 |
|---|---|
| [sql-mysql/](./sql-mysql/README.md) | SQL 기본, MySQL·InnoDB, 인덱스, MVCC, 락, 쿼리 최적화 |
| [postgres/](./postgres/README.md) | PostgreSQL의 SQL 확장, JSON·전문 검색·확장, 성능과 적합성 평가 |

## 관련 문서

- [03_persistence](../03_persistence/README.md) — JDBC·JPA·QueryDSL이 관계형 DB를 사용하는 방식
- [01_foundation](../01_foundation/README.md) — 데이터 모델·트랜잭션·복제·샤딩의 일반 이론
