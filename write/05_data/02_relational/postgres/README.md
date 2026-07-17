---
title: 05_data/02_relational/postgres — PostgreSQL 실전
tags: [moc, postgres, postgresql, rdbms, indexing, json, fts, timeseries]
status: final
source:
  - https://www.postgresql.org/docs/current/
  - ../../../docs/04_Database/04_PostgreSQL/
related:
  - ../README.md
  - ../../README.md
  - ../../roadmap.md
  - ../../01_foundation/README.md
  - ../../03_persistence/querydsl/README.md
updated: 2026-07-15
---

# 05_data/02_relational/postgres — PostgreSQL 실전
---
> PostgreSQL 의 본편 기능 10개와 운영 부록 3개를 한 묶음으로 정리한다. RDBMS 기본기·모던 SQL·인덱스·JSON·전문 검색·익스텐션·시계열·지리공간·DB 내장 큐를 다루며, 끝에 최적화 팁·적합성 평가·성능 모니터링이 부록으로 붙는다.

## 왜 이 묶음인가

PostgreSQL 은 단순 RDBMS 를 넘어 JSON 문서·시계열·지리공간·메시지 큐를 한 엔진 안에서 소화한다. 그러다 보니 "이 워크로드도 일단 Postgres 로 가능하다" 의 함정에 빠지기 쉽다. 본 묶음은 각 기능이 어디서 빛나고 어디서 한계에 부딪히는지를 정리해, "PostgreSQL 적합성 평가"(02-02) 를 스스로 내릴 수 있는 어휘를 잡는 데 목적이 있다.

## 학습 순서

> 1장(본편) 10절은 입문 → 모던 SQL → 데이터 타입 확장 → 운영 응용 순서다. 2장(부록) 3절은 묶음을 다 본 뒤 펼친다.

| # | 문서 | 다루는 핵심 | 상태 |
|---|------|-----------|------|
| 01-01 | [시작하기](01-01.%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0.md) | Beyond SQL 위치, Docker, psql 명령, generate_series | ✅ Phase 5 |
| 01-02 | [RDBMS 기본 기능](01-02.RDBMS%20%EA%B8%B0%EB%B3%B8%20%EA%B8%B0%EB%8A%A5.md) | Cluster·Database·Schema, MVCC, 제약조건, EXCLUDE, 트리거·뷰, RLS | ✅ Phase 5 |
| 01-03 | [모던 SQL](01-03.%EB%AA%A8%EB%8D%98%20SQL.md) | CTE(12+ inline), 재귀 CTE, 윈도우 함수, LATERAL, UPSERT, RETURNING | ✅ Phase 5 |
| 01-04 | [인덱스](01-04.%EC%9D%B8%EB%8D%B1%EC%8A%A4.md) | 6 가지 타입, 복합·INCLUDE·부분·표현식, GIN/GiST/BRIN 운영, EXPLAIN | ✅ Phase 5 |
| 01-05 | [JSON 처리](01-05.JSON%20%EC%B2%98%EB%A6%AC.md) | json vs jsonb, 연산자, 갱신, jsonb_ops vs jsonb_path_ops, JSON Path | ✅ Phase 5 |
| 01-06 | [전문 검색](01-06.%EC%A0%84%EB%AC%B8%20%EA%B2%80%EC%83%89.md) | tsvector/tsquery, 저장된 컬럼, ts_rank, ts_headline, 한국어 검색 | ✅ Phase 5 |
| 01-07 | [익스텐션](01-07.%EC%9D%B5%EC%8A%A4%ED%85%90%EC%85%98.md) | pgcrypto, pg_stat_statements, FDW, Postgres 호환 솔루션 | ✅ Phase 5 |
| 01-08 | [시계열 데이터](01-08.%EC%8B%9C%EA%B3%84%EC%97%B4%20%EB%8D%B0%EC%9D%B4%ED%84%B0.md) | Declarative Partitioning, TimescaleDB Hypertable, Continuous Aggregate, BRIN | ✅ Phase 5 |
| 01-09 | [지리공간 데이터](01-09.%EC%A7%80%EB%A6%AC%EA%B3%B5%EA%B0%84%20%EB%8D%B0%EC%9D%B4%ED%84%B0.md) | geometry vs geography, SRID, ST_DWithin, GiST | ✅ Phase 5 |
| 01-10 | [메시지 큐](01-10.%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90.md) | SKIP LOCKED, LISTEN/NOTIFY, pgmq, Outbox 패턴 | ✅ Phase 5 |
| 02-01 | [최적화 팁](02-01.%EC%B5%9C%EC%A0%81%ED%99%94%20%ED%8C%81.md) | EXPLAIN, 인덱스 안 쓰는 5 가지 이유, keyset, PgBouncer | ✅ Phase 5 |
| 02-02 | [적합성 평가](02-02.%EC%A0%81%ED%95%A9%EC%84%B1%20%ED%8F%89%EA%B0%80.md) | "Just Use Postgres", 다른 시스템이 답인 자리, 마이그레이션 | ✅ Phase 5 |
| 02-03 | [성능 모니터링](02-03.%EC%84%B1%EB%8A%A5%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81.md) | pg_stat_*, idle in transaction, Prometheus + Grafana | ✅ Phase 5 |

처음 보는 학습자는 01-01 부터 따라간다. 인덱스 설계 의문으로 진입했다면 [`../01-04.트랜잭션과 격리 수준.md`](../../01_foundation/01-04.트랜잭션과%20격리%20수준.md) 에서 MVCC 부분을 먼저 짚고 01-04 로 오는 흐름을 권한다.

## 경계 — 어디까지 이 묶음인가

본 묶음은 PostgreSQL **제품 특화 주제**다. 격리 수준·MVCC 의 일반 이론은 [`01_foundation/01-04.트랜잭션과 격리 수준.md`](../../01_foundation/01-04.트랜잭션과%20격리%20수준.md) 가 담당한다. 분산 환경의 복제·샤딩(Citus, 논리 복제 위 전략)은 [`05_data/`](../..) 영역이다. JPA·QueryDSL 으로 PostgreSQL 을 다루는 ORM 측면은 [`03_persistence/querydsl/`](../../03_persistence/querydsl/) 으로 간다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| PostgreSQL | 16.x | 16에서 도입된 `\dconfig` 등 명령 가정 |
| 도구 | psql, pgAdmin, DBeaver | 본문 예시는 psql 기준 |
| 익스텐션 | pg_stat_statements, pgcrypto, postgis, timescaledb | 01-07 에서 다룸 |

## 면접 대비 체크리스트 (후속 Phase 에서 채움)

1. B-tree 와 GIN 인덱스가 각각 어떤 워크로드에 유리한가?
2. `jsonb` 컬럼 위에 인덱스를 어떻게 설계해야 검색이 빨라지는가?
3. `SKIP LOCKED` 가 작업 큐 구현에서 왜 핵심인가?
4. `EXPLAIN ANALYZE` 출력에서 `Buffers: shared hit/read` 가 의미하는 것은?
5. PostgreSQL 적합성 평가의 결정 기준 세 가지는?

## 관련 문서

- [`../README.md`](../../README.md) — 05_data 카테고리 진입
- [`../README.md`](../../README.md) — DB 자체 이론
- [`../../03_persistence/querydsl/README.md`](../../03_persistence/querydsl/README.md) — ORM 레벨 영속성
