---
title: README
tags: []
status: draft
related: []
updated: 2026-04-19
---

# runners-high / write — 학습 MOC

> 최종본만 모이는 공간이다. 실험은 `poc/`에서, 결과만 여기로 올린다. 하네스는 `~/.claude/skills/writing/references/second-brain-harness.md` 참조.

## 카테고리

| # | 경로 | 범위 |
|---|------|------|
| 01 | [01_language/](01_language/) | Java·Go·TS 등 언어별 문법·관용구·생태계. JVM은 Java 하위 `09_jvm/` |
| 02 | _(예약)_ | Kotlin/Scala 문서가 쌓이면 `02_runtime/`으로 JVM 공통분 분리 예정 |
| 03 | [03_architecture/](03_architecture/) | DDD, Hexagonal, Clean, 설계 원칙·패턴 |
| 04 | [04_distributed/](04_distributed/) | CAP, Consistency, Saga, Outbox 등 분산 이론·패턴 |
| 05 | [05_messaging/](05_messaging/) | Kafka, Redpanda, Avro, Schema Registry, EDA 구현 |
| 06 | [06_data/](06_data/) | DB, CDC, Transaction, Indexing (미래) |
| 07 | [07_observability/](07_observability/) | Logging, Tracing, Metrics, OpenTelemetry |
| 08 | [08_devops/](08_devops/) | CI/CD, Jenkins, Nexus, Sonarqube |
| 09 | [09_cloud/](09_cloud/) | Cloud Native, K8s, Service Mesh (미래) |
| 10 | [10_tools/](10_tools/) | tmux, vim, Claude Code, Git |
| 11 | [11_security/](11_security/) | OAuth/JWT, OWASP, 위협 모델링, Spring Security |
| 99 | [99_ETC/](99_ETC/) | 분류 보류 — 3개월 내 재배치 또는 `_archive`로 |

## Spring 전용 통합 인덱스

Spring 문서는 주제별로 분산 배치되지만 [`01_language/java/spring/README.md`](01_language/java/spring/README.md)가 전 카테고리 집계점 역할을 한다.

## 예약 폴더 (일반 최종본 아님)

- [`_meta/`](_meta/) — 이 저장소 자체 메타 (컨벤션, 워크플로우 가이드)
- `_company/` — 사내 전용 분석. `.gitignore` 등록
- [`_archive/`](_archive/) — 6개월 무갱신·무참조 문서 수납

## 최근 추가된 final 문서

Step D(프론트매터 주입) 이후 스크립트로 자동 채운다.

## 규칙 요약

- 모든 `.md`에 프론트매터 필수(`status`, `updated`, `tags`, `related`)
- 파일명: `{장}-{절}.{제목}.md` (`08-01.EDA 기초.md` 형태)
- 상세: [`_meta/conventions.md`](_meta/conventions.md)
