# 04_Database POC - 학습 가이드

> DDIA, JUP 등 3권 기반 이론 문서 36개를 14개 챕터로 재구성한 학습 경로

## 학습 구조

각 챕터는 두 개의 문서로 구성된다:
- **LEARN.md**: 핵심 정리 — 이론 요약, 다이어그램, 코드 예시, 비교 테이블
- **INVESTIGATE.md**: 심화 탐구 — 면접 대비 + 실무 시나리오 중심 Q&A (챕터당 3-5개)

## 실습 환경

| 구분 | 도구 | 용도 |
|------|------|------|
| **실습 코드** | Docker + docker-compose | 로컬에서 바로 실행 가능한 환경 |
| **아키텍처 학습** | Kubernetes Operator | 프로덕션 배포 패턴 이해 |

Ch.13-14 클러스터링 챕터에서 Docker compose 기반 실습 + K8s Operator 설명을 병행한다.

---

## Part 1: DB 기본개념

DDIA(Designing Data-Intensive Applications) 기반 데이터베이스 핵심 이론을 다룬다.

| # | 챕터 | 핵심 주제 | 참조 docs |
|---|------|----------|----------|
| 01 | [데이터 모델과 쿼리 언어](learning/01-데이터모델과쿼리언어/) | 관계형/문서/그래프 모델, 선언적 쿼리, 임피던스 불일치 | 01_기본개념/01 |
| 02 | [저장소와 검색](learning/02-저장소와검색/) | LSM-tree, B-tree, Hash Index, WAL, Bloom Filter | 01_기본개념/02, 05 |
| 03 | [인코딩과 스키마 진화](learning/03-인코딩과스키마진화/) | Protobuf/Avro, 스키마 진화, 호환성 | 01_기본개념/03 |
| 04 | [트랜잭션](learning/04-트랜잭션/) | ACID, MVCC, 격리 수준, 2PC | 01_기본개념/04 |
| 05 | [NoSQL과 캐싱](learning/05-NoSQL과캐싱/) | CAP, NoSQL 4유형, 캐싱 패턴, Redis | 01_기본개념/06, 07 |

## Part 2: PostgreSQL 실전

JUP(Just Use Postgres) 기반 PostgreSQL 실무 활용법을 다룬다.

| # | 챕터 | 핵심 주제 | 참조 docs |
|---|------|----------|----------|
| 06 | [PostgreSQL 시작하기](learning/06-PostgreSQL시작하기/) | Docker 설치, 객체 계층, 스키마, 제약조건 | 04_PG/01, 02 |
| 07 | [모던 SQL](learning/07-모던SQL/) | CTE, 윈도우 함수, LATERAL JOIN | 04_PG/03 |
| 08 | [인덱스 실전](learning/08-인덱스실전/) | B-tree, GIN, GiST, BRIN, EXPLAIN ANALYZE | 04_PG/04 |
| 09 | [JSON과 전문 검색](learning/09-JSON과전문검색/) | JSONB, tsvector/tsquery, 랭킹 | 04_PG/05, 06 |
| 10 | [익스텐션 생태계](learning/10-익스텐션생태계/) | pgvector, PostGIS, pg_stat_statements | 04_PG/07 |
| 11 | [쿼리 최적화와 모니터링](learning/11-쿼리최적화와모니터링/) | EXPLAIN ANALYZE, pg_stat_*, 설정 튜닝 | 04_PG/A, B, C |

## Part 3: DB 클러스터링

분산 시스템 이론 + PostgreSQL/MariaDB 클러스터링 실전을 다룬다.

| # | 챕터 | 핵심 주제 | 참조 docs |
|---|------|----------|----------|
| 12 | [복제와 샤딩 이론](learning/12-복제와샤딩이론/) | 복제 전략 3종, 샤딩, 합의(Raft/Paxos) | 02_분산시스템/02, 03, 05 |
| 13 | [PostgreSQL 클러스터링](learning/13-PostgreSQL클러스터링/) | Streaming/Logical Replication, Patroni+etcd, Citus, pgpool-II | 신규 작성 |
| 14 | [MariaDB 클러스터링](learning/14-MariaDB클러스터링/) | Galera Cluster, MaxScale, Semi-sync, Group Replication | 신규 작성 |

### 클러스터링 환경별 구성

| 항목 | Docker (실습용) | Kubernetes (학습용) |
|------|----------------|-------------------|
| PostgreSQL HA | Patroni + etcd 컨테이너 | CloudNativePG / Zalando Operator |
| PostgreSQL 분산 | Citus 컨테이너 | Citus Operator |
| MariaDB HA | Galera 3-node compose | mariadb-operator |
| 프록시 | pgpool-II / MaxScale | Service + Ingress |
| 모니터링 | Prometheus + Grafana compose | kube-prometheus-stack |

---

## 학습 순서 가이드

**입문자 경로** (Part 1 → Part 2 순서):
```
Ch.01 → Ch.02 → Ch.04 → Ch.06 → Ch.07 → Ch.08 → Ch.11
```

**전체 경로** (Part 1 → Part 2 → Part 3):
```
Ch.01~05 → Ch.06~11 → Ch.12~14
```

**클러스터링만** (Part 3 직행, Part 1-2 선행 가정):
```
Ch.12 → Ch.13 → Ch.14
```

---

## 관련 이론 문서

- [docs/04_Database](../../docs/04_Database/) — 원본 이론 문서 36개
  - `01_기본개념/` — DDIA 기반 7개
  - `02_분산시스템/` — DDIA 분산 파트 7개
  - `04_PostgreSQL/` — JUP 기반 13개
