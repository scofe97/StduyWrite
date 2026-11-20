---
title: 05_data/docs/connection-pool — DB 커넥션 풀 공식 문서 정독 계획
tags: [moc, connection-pool, hikaricp, pgbouncer, official-docs]
status: draft
related:
  - ../README.md
  - ../../03_persistence/jdbc/01-01.커넥션 풀과 DataSource.md
  - ../../../01_language/book/jpf_java-performance/11-01.JDBC 기초 — 드라이버·connection pool·prepared statement.md
updated: 2026-11-09
---

# 05_data/docs/connection-pool — DB 커넥션 풀 공식 문서 정독 계획

---

> 커넥션 풀만 전문으로 다루는 책이 소장본에 없어서, 풀 라이브러리·DB 서버·풀러의 공식 문서와 소스를 1차 자료로 삼아 따로 씁니다. 지금은 노트가 없고, 이 README 가 어떤 편을 어떤 자료로 어떻게 쓸지 정해 둔 계획입니다.

## 왜 공식 문서로 쓰는가

> 풀의 동작은 책 한 장의 일부로만 나오고, 정확한 기본값과 경계 조건은 라이브러리 소스와 DB 매뉴얼에만 있습니다.

소장한 책 PDF 1,796개를 `connection pool`·`hikari`·`maximumPoolSize` 같은 낱말로 훑었습니다. 풀을 한 장 넘게 다루는 책은 한 권도 없었습니다. 가장 많이 걸린 장도 데이터 소스 설정이나 복원력을 다루다가 풀을 몇 문단 언급하는 정도였습니다. 그런데 풀 장애를 가르는 것은 대개 숫자 하나입니다. 예를 들어 HikariCP 의 `maxLifetime` 이 DB 서버의 유휴 종료 시간보다 짧은지, 중간 로드밸런서가 유휴 TCP 흐름을 몇 초 뒤에 끊는지가 그렇습니다. 이런 값은 버전마다 바뀌므로 태그를 고정한 소스와 버전이 박힌 매뉴얼 주소에서 확인해야 믿을 수 있습니다.

범위는 HikariCP 한 제품에 묶지 않습니다. 같은 문제를 DBCP2·Go `database/sql`·R2DBC Pool 은 저마다 다르게 풉니다. DB 서버와 서버 쪽 풀러(PgBouncer·ProxySQL)도 그 위에서 동작을 바꿉니다. 이것들을 나란히 놓아야 "왜 이 설정인가"를 설명할 수 있습니다. 그래서 `docs/` 의 "제품마다 폴더 하나" 규칙 대신, 제품을 가로지르는 주제 폴더 하나로 둡니다.



## 문서 목록 (예정)

> 01 번대는 애플리케이션 안의 풀, 02 번대는 풀 바깥(서버 쪽 풀러·과부하·다른 런타임)입니다. 번호가 읽기 순서입니다.

| 번호 | 제목(가제) | 다룰 것 | 주 1차 자료 |
|------|-----------|---------|------------|
| 01-01 | 풀이 하는 일과 크기 결정 | 연결 하나를 여는 비용, 풀 크기 공식, 한 작업이 연결 둘을 쥘 때의 교착과 `Tn × (Cm − 1) + 1` | HikariCP wiki About-Pool-Sizing |
| [01-02](./01-02.getConnection·HouseKeeper·maxLifetime.md) | [getConnection·HouseKeeper·maxLifetime](./01-02.getConnection·HouseKeeper·maxLifetime.md) | 대여 경로, 연결 검증과 그 생략 구간, 하우스키퍼 주기, 수명 끝 연결 교체 | HikariCP 소스(`HikariPool`·`HikariConfig`, 태그 고정), DBCP2 설정 문서 |
| [01-03](./01-03.wait_timeout·idle%20timeout·TCP%20keepalive.md) | [wait_timeout·idle timeout·TCP keepalive](./01-03.wait_timeout·idle%20timeout·TCP%20keepalive.md) | DB 서버 유휴 종료(`wait_timeout`·`idle_session_timeout`), LB·NAT 유휴 타임아웃, TCP keepalive, `maxLifetime` 을 어디에 맞추나 | MySQL 8.4·MariaDB·PostgreSQL 16 매뉴얼, AWS NLB 문서, 리눅스 tcp(7), RFC 9293 |
| 01-04 | 풀 고갈 진단 | 대기 타임아웃 로그 읽기, 풀 메트릭, 스레드 덤프에서 "연결을 쥔 채 기다리는" 스레드 찾기 | HikariCP 소스·README, Spring Boot 문서 |
| 01-05 | 증상 완화와 근본 해결 | 풀을 늘리는 것과 쿼리·트랜잭션 범위를 줄이는 것의 차이, 쿼리 타임아웃, 관리용 연결 남겨 두기 | HikariCP README, 사례 글 |
| 02-01 | 서버 쪽 풀러 | PgBouncer session/transaction 모드와 그 제약, ProxySQL 다중화, 앱 풀과 서버 풀을 겹칠 때의 크기 계산 | PgBouncer·ProxySQL 공식 문서 |
| 02-02 | 과부하와 연결 폭주 | 재시작·장애 복구 때 연결을 한꺼번에 다시 여는 문제, 연결 생성 속도 제한, 우선순위 입장 제어 | Figma PGKeeper 글, PgBouncer 문서 |
| 02-03 | 다른 런타임의 풀 | Go `database/sql` 의 MaxOpen/MaxIdle/ConnMaxLifetime, R2DBC Pool, Oracle UCP 가 같은 문제를 어떻게 푸나 | pkg.go.dev, r2dbc-pool 저장소, Oracle UCP 문서 |

편마다 같은 순서로 씁니다. 먼저 증상을 보이고 그 증상이 어느 층에서 생기는지 짚습니다. 그다음 제품별 해결을 나란히 놓습니다. 설정값을 적을 때는 그 값이 정해진 소스 줄이나 매뉴얼 절을 각주로 달고, 확인한 버전과 날짜를 함께 적습니다.



## 실제 사례

> 원문을 직접 열어 확인한 공개 장애 기록입니다. 각 사례는 위 편 중 하나의 근거 예시로 들어갑니다.

| 사례 | 일어난 일 | 원인과 조치 | 들어갈 편 |
|------|----------|------------|----------|
| [우아한형제들, 2020-02-06](https://techblog.woowahan.com/2663/) | 메시지 플랫폼 요청이 연결 대기 타임아웃으로 실패했습니다 | 한 작업이 바깥 트랜잭션으로 연결 하나를 쥔 채 ID 생성용 연결을 하나 더 요청했고, 풀 10개가 모두 그 상태로 막혔습니다. 풀을 24로 늘리고 시퀀스 optimizer 로 두 번째 연결이 필요한 횟수를 줄였습니다 | 01-01 |
| [Val Town, 2024-12-31](https://blog.val.town/blog/post-mortem-exhausted-host-connection-pool) | 호스트의 DB 연결 풀이 바닥났습니다 | 쿼리끼리 교착해 잠긴 연결이 풀 자리를 계속 차지했고, 풀 쿼리에 타임아웃이 없었습니다. 풀 쿼리에 타임아웃을 두고 풀 상태를 헬스체크에 넣었습니다 | 01-04 |
| [Buttondown, 2026-03-31](https://buttondown.com/blog/incident-0024) | 7분과 13분, 두 번 서비스가 멈췄습니다 | DB 는 멀쩡했지만 서버가 받는 연결 상한에 닿았습니다. 관리 작업용 연결을 남겨 두고, 연결 사용률에 경보를 걸고, 헬스체크가 작은 쿼리를 돌게 했습니다 | 01-05 |
| [Figma PGKeeper, 2026-05-04](https://www.figma.com/blog/pgkeeper-building-the-bouncer-we-needed-for-postgres/) | PgBouncer 앞단이 성장 한계에 닿았습니다 | 단일 스레드라 수직 확장이 막혔고, 과부하 뒤 서툰 복구가 연결을 한꺼번에 다시 만들어 DB 를 또 넘어뜨렸습니다. 우선순위 입장 제어와 연결 생성 속도 제한을 둔 자체 프록시로 바꿨습니다 | 02-02 |

아래 셋은 검색 결과로만 본 후보라, 쓰기 전에 원문을 열어 사실을 확인합니다.

- [AWS NLB TCP 유휴 타임아웃 조정 발표](https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-nlb-tcp-configurable-idle-timeout) — 01-03
- [Expedia 의 NLB 연결 타임아웃 글](https://medium.com/expedia-group-tech/lesson-learned-from-a-nlb-connection-timeout-2c672e59e197) — 01-03
- [Honeycomb 의 RDS 성능 저하 포스트모템](https://honeycomb.io/blog/rds-performance-degradation-postmortem) — 01-04



## 1차 자료

> 확인한 주소와 아직 열지 않은 후보를 나눠 둡니다. 후보는 노트를 쓸 때 직접 열어 버전 고정 주소로 바꿉니다.

### 확인한 주소

- HikariCP 6.2.1: [README](https://github.com/brettwooldridge/HikariCP/blob/HikariCP-6.2.1/README.md), [About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing), [HikariConfig.java](https://github.com/brettwooldridge/HikariCP/blob/HikariCP-6.2.1/src/main/java/com/zaxxer/hikari/HikariConfig.java), [HikariPool.java](https://github.com/brettwooldridge/HikariCP/blob/HikariCP-6.2.1/src/main/java/com/zaxxer/hikari/pool/HikariPool.java), [CHANGES](https://github.com/brettwooldridge/HikariCP/blob/HikariCP-6.2.1/CHANGES)
- Spring Boot 3.5: [SQL Databases](https://docs.spring.io/spring-boot/3.5/reference/data/sql.html), [Application Properties](https://docs.spring.io/spring-boot/3.5/appendix/application-properties/index.html)
- DB 서버 변수: [MySQL 8.4 Server System Variables](https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html), [MariaDB Server System Variables](https://mariadb.com/kb/en/server-system-variables/)

### 확인 전 후보

- 다른 풀: Apache Commons DBCP2 설정 문서, Oracle UCP 개발자 문서, r2dbc-pool 저장소 README, Go 표준 라이브러리 `database/sql`
- DB 서버: PostgreSQL 매뉴얼의 연결·클라이언트 설정 절(`max_connections`·`idle_session_timeout`·`idle_in_transaction_session_timeout`)
- 서버 쪽 풀러: PgBouncer 설정 문서, pgpool-II 문서, ProxySQL 문서
- 네트워크: AWS NLB 유휴 타임아웃 문서, 리눅스 `tcp(7)` 의 keepalive 변수



## 참고할 책 장

> 풀 전문서는 없지만, 풀이 왜 필요한지와 장애 전파를 다루는 장은 있습니다. 노트에서 맥락 링크로만 씁니다.

| 책 | 장 | 쓰임 |
|----|----|------|
| Spring Start Here | 12장 Using data sources in Spring apps | 데이터 소스와 풀의 첫 소개. 정독 노트가 이미 있습니다 |
| Cloud Native Spring in Action | 5장 Persisting and managing data in the cloud | 클라우드에서 DB 연결을 설정하는 맥락 |
| Cloud Native Spring in Action | 8장 Reactive Spring: Resilience and scalability | R2DBC 와 반응형 풀(02-03) |
| Building Microservices 2판 | 12장 Resiliency | 타임아웃·격벽으로 장애 전파 막기(01-05) |
| Software Architecture: The Hard Parts | 6장 Pulling Apart Operational Data | DB 를 나눌 때 연결 관리 비용(02-01) |



## 관련 문서

> 이미 있는 풀 관련 노트입니다. 새 편을 쓰면 겹치는 내용은 이쪽으로 링크하거나 이 폴더로 옮깁니다.

- [docs MOC](../README.md) — 05_data/docs 의 폴더 규칙
- [커넥션 풀과 DataSource](../../03_persistence/jdbc/01-01.커넥션%20풀과%20DataSource.md) — JDBC 관점의 첫 정리. 이관 대상 폴더라 새 편이 나오면 내용을 이 폴더로 합칩니다
- [Spring DB JPA 설정 최적화](../../03_persistence/jdbc/05-01.Spring%20DB%20JPA%20설정%20최적화.md) — HikariCP 설정값 일부. 같은 이유로 이관 대상입니다
- [JDBC 기초 — 드라이버·connection pool·prepared statement](../../../01_language/book/jpf_java-performance/11-01.JDBC%20기초%20—%20드라이버·connection%20pool·prepared%20statement.md) — 성능 관점에서 본 풀
- [데이터 소스와 JdbcTemplate](../../../09_spring/books/spring-start-here/12.데이터%20소스와%20JdbcTemplate.md) — Spring 에서 풀을 처음 붙이는 법
