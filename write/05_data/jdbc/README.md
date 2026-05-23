---
title: jdbc — JDBC · JdbcTemplate · 드라이버 관측
tags: [moc, jdbc, jdbc-template, connection-pool, hikari, log4jdbc, otel]
status: final
updated: 2026-05-23
---

# jdbc — JDBC · JdbcTemplate · 드라이버 관측
---
> JDBC 의 토대 (커넥션 풀·JdbcTemplate) + 드라이버 wrap 로깅의 운영 비용·log4jdbc·OTel 졸업 경로.

## 00번대 — 토대

| # | 문서 |
|---|------|
| 00-01 | [자바 예외와 SQL](00-01.자바%20예외와%20SQL.md) |

## 01번대 — JDBC API · 커넥션 풀

| # | 문서 |
|---|------|
| 01-01 | [커넥션 풀과 DataSource](01-01.커넥션%20풀과%20DataSource.md) — §0 JDBC 표준과 라이프사이클 포함 |
| 01-02 | [JDBC Wrapper 개념과 java.sql.Wrapper](01-02.JDBC%20Wrapper%20개념과%20java.sql.Wrapper.md) — 넓은 의미(추상화 계층) vs 좁은 의미(`unwrap`), wrapper가 여러 겹 쌓이는 이유 |

## 02번대 — JdbcTemplate

| # | 문서 |
|---|------|
| 02-01 | [JdbcTemplate](02-01.JdbcTemplate.md) |

## 03번대 — 예외 추상화

| # | 문서 |
|---|------|
| 03-01 | [스프링 예외 추상화](03-01.스프링%20예외%20추상화.md) |

## 04번대 — 드라이버 관측 (운영 회복 시리즈)

| # | 문서 |
|---|------|
| 04-01 | [JDBC 드라이버 wrap 로깅의 운영 비용](04-01.JDBC%20드라이버%20wrap%20로깅의%20운영%20비용.md) |
| 04-02 | [log4jdbc 로그 제어 베스트 프랙티스](04-02.log4jdbc%20로그%20제어%20베스트%20프랙티스.md) |
| 04-03 | [OTel JDBC 졸업 경로](04-03.OTel%20JDBC%20졸업%20경로.md) |

## 05번대 — 설정 최적화

| # | 문서 |
|---|------|
| 05-01 | [Spring DB · JPA 설정 최적화](05-01.Spring%20DB%20JPA%20설정%20최적화.md) |
