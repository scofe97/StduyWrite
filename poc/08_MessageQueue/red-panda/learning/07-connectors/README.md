# 07. Connectors

## 개요

Kafka Connect와 Redpanda Connect를 다룬다. 코드 없이 설정만으로 외부 시스템과 데이터를 주고받는 커넥터 패턴을 학습한다.

## 챕터 목록

| # | 문서 | 설명 | 줄수 |
|---|------|------|------|
| 01 | [01-source-sink-patterns.md](./01-source-sink-patterns.md) | Source/Sink 7패턴 이론 (Confluent 기반) | ~830 |
| 02 | [02-redpanda-connect.md](./02-redpanda-connect.md) | Redpanda Connect(구 Benthos) — YAML 선언적 파이프라인, Bloblang, Streams Mode | ~1,730 |
| 03 | [03-spring-boot-impl.md](./03-spring-boot-impl.md) | Spring Boot에서 커넥터 패턴 구현 | ~1,020 |
| 04 | [04-operations.md](./04-operations.md) | 운영: 에러 처리, DLQ, 모니터링 | - |
| 05 | [05-helm-deployment.md](./05-helm-deployment.md) | Helm 기반 커넥터 배포 | - |
| 06 | [06-error-recovery.md](./06-error-recovery.md) | HTTP 에러 분류, 구조화 로깅, 장애 복구 런북 | ~625 |
| 07 | [07-playground-connectors.md](./07-playground-connectors.md) | Playground 커넥터 실무 해설 — Bloblang 문법, 호출 흐름, 에러 전략 | ~800 |

## 학습 순서

```
01 (이론) → 02 (Redpanda Connect) → 03 (Spring Boot 구현) → 04 (운영) → 05 (배포) → 06 (에러 복구) → 07 (Playground 실무)
```

## 선행 학습

- [02-fundamentals](../02-fundamentals/) — Redpanda/Kafka 기초
- [03-spring-boot-integration](../03-spring-boot-integration/) — Spring Kafka 기본 패턴

## 관련 문서

- [05-event-driven-poc](../05-event-driven-poc/) — Redpanda 전용 기능 (WASM, Iceberg)
- 기존 `05/02-connect-pipeline.md`는 이 디렉토리로 통합 후 삭제됨
