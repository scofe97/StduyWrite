# 04. Advanced Patterns

## 개요

Redpanda 프로덕션 운영에 필요한 고급 패턴을 다룬다. 인프라 수준의 모니터링·보안·운영부터 애플리케이션 수준의 분산 추적(OTel), DLQ 고급 패턴, CI/CD 자동화까지 포함한다.

> Schema Registry, Tiered Storage, 스토리지 요구사항은 기본 개념으로 이동 → [02-fundamentals](../02-fundamentals/)

## 챕터 목록

| # | 문서 | 설명 | 상태 |
|---|------|------|------|
| 01 | [01-monitoring.md](./01-monitoring.md) | Prometheus 메트릭 수집, Grafana 대시보드, 브로커 지표 해석 | 완료 |
| 02 | [02-security.md](./02-security.md) | TLS 설정, SASL 인증, ACL 권한 제어 | 완료 |
| 03 | [03-operations.md](./03-operations.md) | 운영 명령어, DR(재해 복구), 트러블슈팅 가이드 | 완료 |
| 04 | [04-opentelemetry.md](./04-opentelemetry.md) | 분산 추적, OTel Collector 설정, Spring Boot 연계 | 완료 |
| 05 | [05-error-handling.md](./05-error-handling.md) | DLQ 고급 패턴, Redpanda Connect 에러 처리, 특수 케이스 대응 | 완료 |
| 06 | [06-cicd-integration.md](./06-cicd-integration.md) | Jenkins/GitLab CI 파이프라인, Testcontainers, GitOps 적용 | 완료 |

## 학습 순서 (권장)

1. **가시성 확보** (운영 전 먼저 보는 것을 만들어야 한다)
   - 01-monitoring → 04-opentelemetry

2. **보안과 운영** (프로덕션 기준 충족)
   - 02-security → 03-operations

3. **에러 처리와 자동화** (장애 대응과 배포 파이프라인)
   - 05-error-handling → 06-cicd-integration

## 관련 폴더

- [02-fundamentals](../02-fundamentals/) — 이론 기반 (토픽 설계, 트랜잭션, Geo-Replication)
- [03-spring-boot-integration](../03-spring-boot-integration/) — 애플리케이션 수준 DLQ 기본 패턴은 `03/06-dlq-strategy` 참조
- [05-event-driven-poc](../05-event-driven-poc/) — Redpanda 전용 기능 PoC

## 폴더 간 교차 참조

| 이 폴더 | 관련 문서 | 관계 |
|---------|----------|------|
| 01-monitoring | 04-opentelemetry | 인프라 메트릭(Prometheus) vs 애플리케이션 추적(OTel) — 상호 보완적 |
| 05-error-handling | 03-spring-boot-integration/06-dlq-strategy | 고급 DLQ 패턴 vs 기본 DLQ 구현 — 심화/기초 관계 |
| 06-cicd-integration | 02-fundamentals/20-topic-governance-gitops | CI/CD 파이프라인 실습 vs 토픽 거버넌스 GitOps 이론 |
