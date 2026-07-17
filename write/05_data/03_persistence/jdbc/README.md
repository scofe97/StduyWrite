---
title: 05_data/03_persistence/jdbc — JDBC · JdbcTemplate · 드라이버 관측
tags: [moc, jdbc, jdbc-template, connection-pool, hikari, log4jdbc, otel]
status: final
related:
  - ../README.md
  - ../../README.md
  - ../../roadmap.md
updated: 2026-07-15
---

# 05_data/03_persistence/jdbc — JDBC · JdbcTemplate · 드라이버 관측
---
> JDBC 의 토대 (커넥션 풀·JdbcTemplate) + 드라이버 wrap 로깅의 운영 비용·log4jdbc·OTel 졸업 경로.

## 00번대 — 토대

| # | 문서 |
|---|------|
| 00-01 | [자바 예외와 SQL](00-01.%EC%9E%90%EB%B0%94%20%EC%98%88%EC%99%B8%EC%99%80%20SQL.md) |

## 01번대 — JDBC API · 커넥션 풀

| # | 문서 |
|---|------|
| 01-01 | [커넥션 풀과 DataSource](01-01.%EC%BB%A4%EB%84%A5%EC%85%98%20%ED%92%80%EA%B3%BC%20DataSource.md) — §0 JDBC 표준과 라이프사이클 포함 |
| 01-02 | [JDBC Wrapper 개념과 java.sql.Wrapper](01-02.JDBC%20Wrapper%20%EA%B0%9C%EB%85%90%EA%B3%BC%20java.sql.Wrapper.md) — 넓은 의미(추상화 계층) vs 좁은 의미(`unwrap`), wrapper가 여러 겹 쌓이는 이유 |

## 02번대 — JdbcTemplate

| # | 문서 |
|---|------|
| 02-01 | [JdbcTemplate](02-01.JdbcTemplate.md) |

## 03번대 — 예외 추상화

| # | 문서 |
|---|------|
| 03-01 | [스프링 예외 추상화](03-01.%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%98%88%EC%99%B8%20%EC%B6%94%EC%83%81%ED%99%94.md) |

## 04번대 — 드라이버 관측 (운영 회복 시리즈)

| # | 문서 |
|---|------|
| 04-01 | [JDBC 드라이버 wrap 로깅의 운영 비용](04-01.JDBC%20%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84%20wrap%20%EB%A1%9C%EA%B9%85%EC%9D%98%20%EC%9A%B4%EC%98%81%20%EB%B9%84%EC%9A%A9.md) |
| 04-02 | [log4jdbc 로그 제어 베스트 프랙티스](04-02.log4jdbc%20%EB%A1%9C%EA%B7%B8%20%EC%A0%9C%EC%96%B4%20%EB%B2%A0%EC%8A%A4%ED%8A%B8%20%ED%94%84%EB%9E%99%ED%8B%B0%EC%8A%A4.md) |
| 04-02a | [log4jdbc properties 레퍼런스](04-02a.log4jdbc%20properties%20%EB%A0%88%ED%8D%BC%EB%9F%B0%EC%8A%A4.md) — 공식 20개 옵션 전체 (04-02 §4 6개의 전체판) |
| 04-03 | [OTel JDBC 졸업 경로](04-03.OTel%20JDBC%20%EC%A1%B8%EC%97%85%20%EA%B2%BD%EB%A1%9C.md) |

## 05번대 — 설정 최적화

| # | 문서 |
|---|------|
| 05-01 | [Spring DB · JPA 설정 최적화](05-01.Spring%20DB%20JPA%20%EC%84%A4%EC%A0%95%20%EC%B5%9C%EC%A0%81%ED%99%94.md) |
