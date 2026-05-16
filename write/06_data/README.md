---
title: 06_data MOC
tags: [moc, database, ddia, postgres, querydsl, ops, dump]
status: final
source:
  - https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/
  - https://www.postgresql.org/docs/current/
  - https://mariadb.com/docs/server/clients-and-utilities/backup-restore-and-import-clients/mariadb-dump
  - https://hub.docker.com/_/mariadb
  - https://docs.gitlab.com/development/development_seed_files/
  - https://shopify.engineering/modelling-developer-infrastructure-teams
  - https://phauer.com/2018/local-development-docker-compose-seeding-stubs/
related:
  - ../04_distributed/README.md
  - ../05_messaging/README.md
  - ../01_language/java/spring/README.md
updated: 2026-05-14
---

# 06_data
---
> DB 자체 이론, 데이터 처리 모델(배치·스트림), PostgreSQL 실전, ORM 레벨 영속성을 한 카테고리에 모은다. 분산 환경에서 노드 간 합의·복제·샤딩이 일으키는 문제는 자매 카테고리 [`../04_distributed/`](../04_distributed/) 가 담당하고, Kafka·Redpanda 같은 메시지 도구의 구체 구현은 [`../05_messaging/`](../05_messaging/) 가 다룬다.

## 본 카테고리의 구성

> 29 편의 본문이 세 개의 루트 묶음과 두 개의 하위 폴더로 갈린다. 루트의 01-NN 은 DDIA 1부 기반 이론, 02-NN 은 DDIA 3부 기반 데이터 처리(원래 DDIA 부 번호 3을 그대로 가져와 11-NN 으로 두었으나 독자 흐름이 끊겨 02 로 재번호), 03-NN 은 데이터 운영(덤프·이관·마스킹), `postgres/` 는 제품 특화, `spring/` 은 ORM 영역이다. 번호 규칙은 *이론(01) → 처리 모델(02) → 운영(03)* 으로 추상에서 실무 운영으로 내려간다.

### 01-NN. DDIA 이론 (DB 자체)

> 어떤 DB 제품이든 이 기반 위에서 의사결정이 갈린다. PostgreSQL 실전이나 분산 이론으로 가기 전 공통 어휘를 잡는 자리다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [데이터 모델과 쿼리 언어](01-01.데이터%20모델과%20쿼리%20언어.md) | 관계형·문서·그래프, 임피던스 미스매치, Event Sourcing |
| 01-02 | [저장소와 검색](01-02.저장소와%20검색.md) | B-tree vs LSM-tree, Bloom Filter, 컬럼 저장, 벡터 인덱스 |
| 01-03 | [인코딩과 진화](01-03.인코딩과%20진화.md) | JSON·Protobuf·Avro, 스키마 진화, RPC, 워크플로우 |
| 01-04 | [트랜잭션과 격리 수준](01-04.트랜잭션과%20격리%20수준.md) | ACID, MVCC, 격리 4단계, Serializable 3 구현, 2PC |
| 01-05 | [인덱스 이론](01-05.인덱스%20이론.md) | B+Tree, 복합·커버링·부분·표현식, GIN·GiST·BRIN |
| 01-06 | [NoSQL 비교](01-06.NoSQL%20비교.md) | MongoDB·Redis·Cassandra·Neo4j 모델별 트레이드오프, NewSQL |
| 01-07 | [캐싱 전략](01-07.캐싱%20전략.md) | Cache-Aside·Write-Through·Write-Behind, Stampede·Hot Key |

### 02-NN. 데이터 처리 (배치·스트림)

> 같은 입력을 어디서 누적해 어떻게 파생 결과를 만드는지가 두 처리 모델의 공통 질문이다. 마이크로배치·이벤트 시간·exactly-once 같은 실무 함정이 여기서 갈린다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 02-01 | [배치 처리](02-01.배치%20처리.md) | Unix 도구→MapReduce→Dataflow 엔진, Shuffle, 분산 JOIN, 결정론·멱등성 |
| 02-02 | [스트림 처리](02-02.스트림%20처리.md) | 메시지 브로커 2 갈래, CDC, 이벤트 시간·워터마크, 윈도우, exactly-once |
| 02-03 | [스트리밍 시스템 철학](02-03.스트리밍%20시스템%20철학.md) | 데이터 통합, DB unbundling, write/read path, 람다·카파 |



### 03-NN. 데이터 운영 (덤프·이관·로컬 DB)

> 이론과 처리 모델 위에 운영이 얹힌다. 공유 dev DB 의존을 끊고, 덤프로 시작해 seed·마스킹으로 진화시키는 단계별 정책이다. 03-01 이 *왜 옵션이 그렇게 짜여 있는가*, 03-02 가 *한 번 데이고 나면 절실한 함정과 정책*, 03-03 이 *팀 전체의 운영 모델 선택지* 를 다룬다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 03-01 | [DB덤프와 로컬이관](03-01.DB덤프와%20로컬이관.md) | `mariadb-dump` 옵션 풀이, docker compose entrypoint, 복원 두 방식, 단계별 적용 |
| 03-02 | [DB덤프와 로컬이관 (심화)](03-02.DB덤프와%20로컬이관%20(심화).md) | DEFINER 사고, initdb.d 함정, healthcheck, 대용량 튜닝, 마스킹 정책, 사례 트러블슈팅 5선 |
| 03-03 | [로컬 개발환경 운영 모델](03-03.로컬%20개발환경%20운영%20모델.md) | GitLab seed·Shopify Local/Cloud·Toss mock·Phauer seeding+stub, Cloud Dev / Preview Environment 비교 |



### postgres/ — PostgreSQL 실전

> PostgreSQL 의 본편 기능 10 개와 운영 부록 3 개를 한 묶음으로 정리한다. 격리 수준·MVCC 의 일반 이론은 01-04 가 담당하고, 본 폴더는 PostgreSQL 만의 *구체 동작* 에 집중한다. [`postgres/README.md`](postgres/README.md) 가 진입.

### spring/querydsl/ — ORM 영속성

> Spring Boot 3.2 + QueryDSL 6.12 (OpenFeign fork) 기반 ORM 학습 묶음 11 편(표준 9 + 실무 변형 1 + 락·동시성 1). [`spring/querydsl/README.md`](spring/querydsl/README.md) 가 진입.

## 학습 순서

> 어디서 시작할지가 모호하면 다음 흐름을 권한다.

1. DB 의 공통 어휘부터 잡고 싶으면 → **01-01** 부터 순서대로.
2. 트랜잭션·락·MVCC 의문에서 출발했다면 → **01-04** 를 먼저 펼친 뒤 01-02·01-05 로.
3. PostgreSQL 운영 환경에 바로 부딪혔다면 → [`postgres/01-01.시작하기.md`](postgres/01-01.시작하기.md) 부터.
4. ORM 의 N+1·페이징·페치 조인 함정에 부딪혔다면 → [`spring/querydsl/01-06.페이징과 fetch join 함정.md`](spring/querydsl/01-06.페이징과%20fetch%20join%20함정.md) 부터 골라 읽고 필요할 때 fundamentals 로.
5. 데이터 통합·CDC·이벤트 로그 발상은 → **02-03** 부터.
6. 공유 dev DB 의존을 끊고 로컬로 옮기는 작업에 부딪혔다면 → **03-01** 부터(함정·정책은 03-02 심화, 운영 모델은 03-03).

각 본문 끝에 면접 체크리스트가 함께 있어 자기 점검 도구로 쓸 수 있다.

## 경계 기준

`06_data/` 는 DB 자체와 그 위 ORM 까지 다룬다. 같은 데이터 처리라도 **분산 환경의 합의·복제·샤딩 이론** 은 [`../04_distributed/`](../04_distributed/) 자리다. **메시징 도구(Kafka·Redpanda) 의 구체 구현** 은 [`../05_messaging/`](../05_messaging/) 으로 간다. 두 카테고리와 경계가 모호한 주제(예: Outbox 패턴) 는 "DB 쪽 폴링·인덱스 전략" 은 여기, "메시지 발행 통합" 은 [`../05_messaging/`](../05_messaging/) 으로 분할한다.

ORM 레벨의 락(JPA `@Lock`, QueryDSL `setLockMode`)은 [`spring/querydsl/02-05.락과 동시성 제어.md`](spring/querydsl/02-05.락과%20동시성%20제어.md) 가 다루며, 그 상위 추상인 격리 수준은 [`01-04.트랜잭션과 격리 수준.md`](01-04.트랜잭션과%20격리%20수준.md) 가 다룬다.

같은 도메인이라도 *이론* 은 01-NN, *처리 모델* 은 02-NN, *운영(덤프·이관·마스킹)* 은 03-NN 으로 분리한다. 예를 들어 CDC 의 *발상·이벤트 시간* 은 02-02 가 다루고, *개발자 PC 에 운영 데이터를 안전하게 가져오는 방법* 은 03-01 이 다룬다.

## 사전 지식

> 이 카테고리는 다음을 안다고 가정한다.

1. SQL `SELECT/INSERT/UPDATE/DELETE` 와 `JOIN`/`GROUP BY` 기본 문법.
2. 트랜잭션이 무엇인지 한 문장으로 답할 수 있다(모르면 01-04 가 시작점).
3. Spring Data JPA 의 `@Transactional` 또는 비슷한 ORM 추상을 한 번이라도 써 봤다.
4. Kafka 같은 메시지 큐를 한 번이라도 써 봤다(02-NN 묶음에 한정).

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| 출처 | DDIA 1st ed. | Martin Kleppmann, 2017 (01-NN, 02-NN 의 골격) |
| PostgreSQL | 16~17 | `postgres/` 본문은 16+ 가정 |
| Spring Boot | 3.2.3 | `spring/querydsl/` Jakarta 네임스페이스 |
| QueryDSL | 6.12 (OpenFeign fork) | 원조 `com.querydsl` 은 archived |
| Hibernate | 6.4.x | Spring Boot 3.2 기본 |

## 관련 문서

- [`../04_distributed/README.md`](../04_distributed/README.md) — 분산 환경의 합의·복제·샤딩
- [`../05_messaging/README.md`](../05_messaging/README.md) — Kafka·Redpanda 같은 메시지 도구
- [`../01_language/java/spring/README.md`](../01_language/java/spring/README.md) — Spring 카테고리 전체 진입
