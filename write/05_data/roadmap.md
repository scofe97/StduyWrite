---
title: 05_data 통합 학습 로드맵 — Spring 백엔드 관점
tags: [roadmap, data, database, spring, sql, jpa, querydsl]
status: draft
source:
  - ./README.md
  - ./01_foundation/README.md
  - ./02_relational/README.md
  - ./03_persistence/README.md
related:
  - ./README.md
  - ../04_messaging/README.md
  - ../09_spring/README.md
updated: 2026-07-15
---

# 05_data 통합 학습 로드맵
---
> 이 로드맵은 Spring 백엔드가 데이터를 모델링하고, 관계형 DB에 저장하며, ORM으로 조회하고, 운영 문제를 해결하는 흐름을 기준으로 합니다. DDIA·Redis·배치 처리는 이 흐름 위에서 확장합니다.

## 1. 데이터 모델과 SQL

[데이터 모델과 쿼리 언어](./01_foundation/01-01.데이터%20모델과%20쿼리%20언어.md)로 관계형·문서·그래프 모델의 차이를 먼저 잡습니다. 이어 [sql-mysql/](./02_relational/sql-mysql/README.md)의 SQL, 정규화, 조인, 인덱스를 읽어 애플리케이션 코드가 실제로 만드는 쿼리를 해석할 수 있게 합니다.

완료 기준은 테이블 구조와 조회 패턴을 보고 정규화·인덱스·조인 방식의 선택 이유를 설명하는 것입니다.

## 2. JDBC에서 JPA·QueryDSL까지

[JDBC](./03_persistence/jdbc/README.md)의 DataSource·커넥션 풀·JdbcTemplate을 먼저 읽고, [JPA](./03_persistence/jpa/README.md)의 영속성 컨텍스트·매핑·Spring Data JPA로 올라갑니다. 동적 검색·DTO 조회·복잡한 페이징은 마지막에 [QueryDSL](./03_persistence/querydsl/README.md)로 확장합니다.

완료 기준은 단순 CRUD에는 어느 계층을 쓰고, 복잡한 조회·벌크 연산·직접 SQL에는 어떤 도구를 선택할지 근거와 함께 말하는 것입니다.

## 3. 트랜잭션과 동시성

[트랜잭션과 격리 수준](./01_foundation/01-04.트랜잭션과%20격리%20수준.md), [InnoDB MVCC](./02_relational/sql-mysql/04-01.InnoDB%20MVCC.md), [동시성제어와 락](./02_relational/sql-mysql/04-02.동시성제어와%20락.md), [스프링 트랜잭션](./03_persistence/jpa/04-01.스프링%20트랜잭션.md) 순서로 같은 문제를 DB·프레임워크 두 계층에서 봅니다.

완료 기준은 격리 수준, 낙관·비관 락, 전파 옵션을 서로 다른 문제로 구분하고, 재고·결제처럼 충돌이 가능한 유스케이스의 선택을 설명하는 것입니다.

## 4. 제품 운영과 개발 환경

로컬 이관, 임베디드 DB, 테스트 트랜잭션은 [06_operations/](./06_operations/README.md)에서 다룹니다.

완료 기준은 느린 쿼리를 `EXPLAIN`으로 확인할 지점과, 로컬·테스트 환경이 운영 DB에 의존하지 않게 만드는 방법을 설명하는 것입니다.

## 5. 분산 데이터와 데이터 통합 심화

복제·샤딩·일관성·합의는 [01_foundation/](./01_foundation/README.md)의 02번대를, 배치·스트림·데이터 통합은 03번대와 [DDIA 2판 정독](./book/designing-data-intensive-applications/README.md)에서 확장합니다. Kafka·Redpanda·Outbox·CDC의 구체 구현은 [04_messaging](../04_messaging/README.md)에서 이어서 봅니다.

완료 기준은 단일 DB의 트랜잭션 문제와 분산 시스템의 복제·일관성 문제를 구분하고, 메시지 브로커가 필요한 이유를 데이터 흐름 관점에서 설명하는 것입니다.

## 관련 문서

- [05_data MOC](./README.md) — 폴더 경계와 전체 자료의 진입점
- [04_messaging](../04_messaging/README.md) — 메시지 브로커·CDC·스트림 구현
- [09_spring](../09_spring/README.md) — Spring 프레임워크 전반
