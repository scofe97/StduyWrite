# 05. Event-Driven PoC (Redpanda 전용)

## 개요

Redpanda에서만 사용 가능한 고유 기능을 실습한다. Kafka로 대체할 수 없는 WASM Data Transforms, Redpanda Connect(구 Benthos), Iceberg Topics 3가지 기능이 대상이다.

> **범용 EDA 패턴은 [`poc/02_Architecture/01-event-driven/`](../../../../02_Architecture/01-event-driven/)로 이동했다.** (14개 챕터)
> **이론 문서**: `runners-high/docs/02_Architecture/03_EventDriven/` (17개 챕터)

## 왜 이 챕터들이 여기에 있는가?

아래 3개 챕터는 Redpanda 전용 기능으로, Kafka에서는 사용할 수 없다. 따라서 범용 EDA 아키텍처 패턴과 분리하여 Redpanda 학습 프로젝트에서 관리한다.

| 기능 | Redpanda | Kafka | 비고 |
|------|----------|-------|------|
| WASM Data Transforms | O | X | 브로커 내부 WebAssembly 변환 |
| Redpanda Connect | O | X | YAML 기반 선언적 파이프라인 (구 Benthos) |
| Iceberg Topics | O | X | 토픽 → Iceberg 테이블 자동 저장 |

## 기술 스택

| 기술 | 버전 | 용도 |
|------|------|------|
| **Redpanda** | v25.3.6 | 메시지 브로커 |
| **Redpanda Connect** | 4.x | 선언적 파이프라인 |
| **WASM** | - | 브로커 내 변환 |
| **Testcontainers** | 1.20.x | 통합 테스트 |
| **Docker Compose** | v2 | 로컬 인프라 |

## 챕터 목록

| # | 문서 | 설명 | 상태 |
|---|------|------|------|
| 01 | [01-wasm-transforms.md](./01-wasm-transforms.md) | 브로커 내부 WebAssembly 변환 — Rust로 PII 마스킹 함수 작성 및 배포 | 완료 |
| ~~02~~ | ~~02-connect-pipeline~~ | 삭제됨 → [07-connectors/](../07-connectors/) 참조 | 이동 |
| 03 | [03-iceberg-topics.md](./03-iceberg-topics.md) | 토픽 → Iceberg 테이블 자동 저장, MinIO + Spark 쿼리 | 완료 |

## 학습 순서 (권장)

1. **선행 학습**: 범용 EDA 패턴을 먼저 학습한 후 진행을 권장한다.
   [`poc/02_Architecture/01-event-driven/`](../../../../02_Architecture/01-event-driven/) 참조

2. **Redpanda 전용 기능**:
   - 01-wasm-transforms (브로커 내 변환) → 03-iceberg-topics (스트림 데이터 레이크)
   - 02-connect-pipeline은 `07-connectors/`에서 상세 학습

## 각 챕터 상세

### 01-wasm-transforms (WASM 데이터 변환)

Redpanda 브로커 내부에서 WebAssembly 코드를 실행하여 메시지를 변환한다. 프로듀서는 원본 데이터를 발행하지만 컨슈머는 마스킹된 데이터를 수신하는 구조다.

- Rust로 PII 데이터 마스킹 함수 작성
- WASM으로 컴파일하여 Redpanda에 `rpk`로 배포
- 무상태(stateless) 변환: WASM 함수는 메시지당 한 번만 실행

### ~~02-connect-pipeline~~ (삭제 → 07-connectors/)

Redpanda Connect 파이프라인 내용은 [07-connectors/](../07-connectors/)로 이동했다.

### 03-iceberg-topics (Iceberg Topics)

스트림 데이터를 Apache Iceberg 테이블로 자동 저장한다. Redpanda가 토픽 데이터를 Iceberg 포맷으로 S3/HDFS에 기록하며, 시간 기반 파티셔닝과 스키마 진화를 자동 처리한다.

- Iceberg Topic 생성 및 설정
- MinIO(S3 호환 저장소)에 데이터 저장
- Apache Spark로 Iceberg 테이블 쿼리

## 관련 폴더

- [02-fundamentals](../02-fundamentals/) — Redpanda 개념 기초 (WASM 개요는 05-core-features 참조)
- [03-spring-boot-integration](../03-spring-boot-integration/) — Spring Boot 연계 패턴
- [04-advanced-patterns](../04-advanced-patterns/) — 모니터링, 보안, 운영
- [07-connectors](../07-connectors/) — 02-connect-pipeline 상세 구현 (Redpanda Connect)
- [poc/02_Architecture/01-event-driven/](../../../../02_Architecture/01-event-driven/) — 범용 EDA 패턴 14개 챕터
