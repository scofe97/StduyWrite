---
title: 05_data MOC
tags: [moc, database, ddia, postgres, querydsl, distributed, ops, jdbc, jpa, redis, sql]
source:
  - https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/
related:
  - ../04_messaging/README.md
  - ../11_spring/README.md
status: final
updated: 2026-05-23
---

# 05_data
---
> DB 자체 이론, 분산 시스템 (DDIA 2부), 데이터 처리 모델 (배치·스트림), 데이터 운영 (덤프·이관·테스트), JDBC 드라이버·JdbcTemplate, JPA·MyBatis 영속성, SQL 기초·인덱스·MVCC·동시성, Redis, PostgreSQL, QueryDSL 을 한 카테고리에 모은다. Kafka·Redpanda 같은 메시지 도구의 구체 구현은 [`../04_messaging/`](../04_messaging/) 가 다룬다.

## 8 개 서브폴더 구조

> 본 카테고리는 *이론 → 운영 → 도구별* 의 흐름으로 8 묶음으로 갈린다.

| 폴더 | 범위 | 진입 |
|------|------|------|
| [theory/](theory/) | DDIA 1·2·3부 18편 + WAL 패턴 | [README](theory/README.md) |
| [ops/](ops/) | DB 덤프·로컬 이관·테스트 인프라 5편 | [README](ops/README.md) |
| [sql/](sql/) | SQL 기초·MySQL·InnoDB·MVCC·동시성 10편 | [README](sql/README.md) |
| [jdbc/](jdbc/) | 커넥션 풀·JdbcTemplate·드라이버 wrap 로깅 5편 | [README](jdbc/README.md) |
| [jpa/](jpa/) | JPA·Spring Data JPA·트랜잭션·락·MyBatis 15편 | [README](jpa/README.md) |
| [redis/](redis/) | Redis 자료구조·세션·캐시·리더보드·Pub Sub·백업 7편 | [README](redis/README.md) |
| [postgres/](postgres/) | PostgreSQL 실전 14편 | [README](postgres/README.md) |
| [querydsl/](querydsl/) | QueryDSL 영속성 17편 | [README](querydsl/README.md) |

## 학습 순서

> 어디서 시작할지가 모호하면 다음 흐름을 권한다.

1. 공통 어휘부터 — [theory/01-01](theory/01-01.데이터%20모델과%20쿼리%20언어.md) 부터 순서대로.
2. 트랜잭션·MVCC 의문에서 — [theory/01-04](theory/01-04.트랜잭션과%20격리%20수준.md) → [sql/04-01.InnoDB MVCC](sql/04-01.InnoDB%20MVCC.md) → [sql/04-02.동시성제어와 락](sql/04-02.동시성제어와%20락.md).
3. 분산 환경의 합의·복제·샤딩 이론 — [theory/02-01](theory/02-01.시스템%20아키텍처%20트레이드오프.md) 부터.
4. PostgreSQL 운영 부딪힘 — [postgres/](postgres/) 진입.
5. JPA 의 N+1·페이징·페치 조인 — [jpa/03-03.프록시와 N+1](jpa/03-03.프록시와%20N+1.md) 또는 [querydsl/](querydsl/).
6. 데이터 통합·CDC·이벤트 로그 — [theory/03-03.스트리밍 시스템 철학](theory/03-03.스트리밍%20시스템%20철학.md).
7. 로컬 DB 의존을 끊는 작업 — [ops/01-01](ops/01-01.DB%20덤프와%20로컬%20이관.md) 부터.
8. JDBC 로깅 폭주 대응 — [jdbc/04-01](jdbc/04-01.JDBC%20드라이버%20wrap%20로깅의%20운영%20비용.md) 부터.

## 경계 기준

> 같은 도메인이라도 이론·구현·운영 영역으로 분리한다.

- **이론** — `theory/` (DDIA 기반 공통 어휘).
- **SQL · DB 엔진** — `sql/` (MySQL·InnoDB 중심), `postgres/` (PostgreSQL 특화).
- **드라이버 계층** — `jdbc/` (커넥션 풀·JdbcTemplate·관측).
- **ORM** — `jpa/` (Spring Data JPA), `querydsl/` (타입 안전 쿼리).
- **운영** — `ops/` (덤프·테스트·로컬 환경).
- **외부 시스템** — `redis/` (인메모리 캐시·세션).
- **메시징** — [`../04_messaging/`](../04_messaging/) (Kafka·Redpanda·Outbox 구현).

ORM 레벨의 락 (JPA `@Lock`, QueryDSL `setLockMode`) 은 [jpa/04-02.낙관적 비관적 락](jpa/04-02.낙관적%20비관적%20락.md) 과 [querydsl/02-05.락과 동시성 제어](querydsl/02-05.락과%20동시성%20제어.md) 가 다루며, 격리 수준의 일반 이론은 [theory/01-04](theory/01-04.트랜잭션과%20격리%20수준.md) 가 다룬다.

## 사전 지식

> 이 카테고리는 다음을 안다고 가정한다.

1. SQL `SELECT/INSERT/UPDATE/DELETE` 와 `JOIN`/`GROUP BY` 기본 문법.
2. 트랜잭션이 무엇인지 한 문장으로 답할 수 있다 (모르면 [theory/01-04](theory/01-04.트랜잭션과%20격리%20수준.md) 가 시작점).
3. Spring Data JPA 의 `@Transactional` 또는 비슷한 ORM 추상을 한 번이라도 써 봤다.
4. Kafka 같은 메시지 큐를 한 번이라도 써 봤다 (theory 의 02-NN, 03-NN 묶음에 한정).

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| 출처 | DDIA 1st ed. | Martin Kleppmann, 2017 (theory 의 골격) |
| PostgreSQL | 16~17 | `postgres/` 본문은 16+ 가정 |
| Spring Boot | 3.2.3 | `jpa/`, `querydsl/` Jakarta 네임스페이스 |
| QueryDSL | 6.12 (OpenFeign fork) | 원조 `com.querydsl` 은 archived |
| Hibernate | 6.4.x | Spring Boot 3.2 기본 |
| MySQL | 8.0+ | `sql/` 본문 가정 |
| Redis | 7.x | `redis/` 본문 가정 |

## 관련 문서

- [`../04_messaging/README.md`](../04_messaging/README.md) — Kafka·Redpanda 같은 메시지 도구
- [`../11_spring/README.md`](../11_spring/README.md) — Spring 카테고리 전체 진입
