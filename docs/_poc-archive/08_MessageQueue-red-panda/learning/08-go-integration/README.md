# 08. Go Integration (franz-go)

Go + Redpanda 통합 학습 경로. 기존 Spring Boot 21챕터를 기반으로, Go(franz-go) 구현에 집중한 13챕터로 구성했다.

## 선행 조건

- `02-fundamentals/` 이론 학습 완료
- `03-spring-boot-integration/` 최소 Ch01-10 완료 (개념 이해)
- Go 기초: `09_goLang PoC 01-03` 수준

## 설계 원칙

1. **이론은 재사용**: 기존 문서 교차참조, 중복 작성 안 함
2. **구현에 집중**: Go/franz-go 코드가 핵심
3. **Spring 대비**: 각 챕터에 매핑 테이블 포함

## 라이브러리 선택

| 라이브러리 | 용도 | 선택 이유 |
|-----------|------|----------|
| **franz-go** | Kafka 클라이언트 | 순수 Go, 트랜잭션 완전 지원, SR 내장 |
| hamba/avro | Avro 직렬화 | 순수 Go, 성능 우수 |
| testcontainers-go | 통합 테스트 | Redpanda 모듈 내장 |
| zerolog | 로깅 | 구조화, 제로 할당 |

## 핵심 매핑 테이블

| Spring Boot | Go (franz-go) | 비고 |
|-------------|---------------|------|
| `@KafkaListener` | `client.PollFetches()` 루프 | 명시적 폴링 |
| `KafkaTemplate.send()` | `client.Produce()` | 직접 호출 |
| `ProducerFactory` | `kgo.NewClient(opts...)` | 함수형 옵션 |
| `@RetryableTopic` | 수동 재시도 루프 + DLQ produce | 내장 추상화 없음 |
| `@Transactional` | `client.BeginTransaction()` | 명시적 트랜잭션 |
| `spring.kafka.*` 프로퍼티 | `kgo.Opt` 함수형 옵션 | 타입 안전 빌더 |
| `concurrency=N` | goroutine 풀 | Go 동시성 모델 |
| Kafka Streams DSL | goroutine + channel 파이프라인 | JVM 전용 대안 |

## 챕터 구성

### Stage 1: 환경 구성

| Ch | 제목 | Spring 대응 | 실습 |
|:--:|------|:-----------:|:----:|
| 01 | [Basic Setup & Health Check](01-basic-setup.md) | Ch01+02 | `ch01` |
| 02 | [Configuration Patterns](02-configuration-patterns.md) | Ch02 | `ch02` |

### Stage 2: Producer & Consumer

| Ch | 제목 | Spring 대응 | 실습 |
|:--:|------|:-----------:|:----:|
| 03 | [Producer Patterns](03-producer-patterns.md) | Ch03 전반 | `ch03` |
| 04 | [Consumer & Manual Commit](04-consumer-manual-commit.md) | Ch03 후반+04 | `ch04` |

### Stage 3: 신뢰성

| Ch | 제목 | Spring 대응 | 실습 |
|:--:|------|:-----------:|:----:|
| 05 | [Error Handling & DLQ](05-error-handling-dlq.md) | Ch05 | `ch05` |
| 06 | [Idempotent Consumer](06-idempotent-consumer.md) | Ch06 | `ch06` |

### Stage 4: 트랜잭션 & SAGA

| Ch | 제목 | Spring 대응 | 실습 |
|:--:|------|:-----------:|:----:|
| 07 | [Transaction Patterns](07-transaction-patterns.md) | Ch07 | `ch07` |
| 08 | [SAGA Choreography](08-saga-choreography.md) | Ch08 | `ch08` |
| 09 | [SAGA Orchestration](09-saga-orchestration.md) | Ch09 | `ch09` |

### Stage 5: 테스트

| Ch | 제목 | Spring 대응 | 실습 |
|:--:|------|:-----------:|:----:|
| 10 | [Testing Strategies](10-testing-strategies.md) | Ch10 | `ch10` |

### Stage 6: 아키텍처 & 스키마

| Ch | 제목 | Spring 대응 | 실습 |
|:--:|------|:-----------:|:----:|
| 11 | [Pipeline & EIP Patterns](11-pipeline-eip-patterns.md) | Ch11+13 | `ch11` |
| 12 | [Schema Registry & Avro](12-schema-registry-avro.md) | Ch15 | `ch12` |

### Stage 7: 프로덕션

| Ch | 제목 | Spring 대응 | 실습 |
|:--:|------|:-----------:|:----:|
| 13 | [Production Patterns](13-production-patterns.md) | Ch17+18 | - |

### 교차참조만 (별도 챕터 없음)

| Spring Ch | 사유 |
|-----------|------|
| Ch12 ReplyingKafkaTemplate | Spring 전용; Go는 Ch11에서 Request-Reply 직접 구현 |
| Ch14 미들웨어 아키텍처 | 언어 무관; `03-spring-boot/14` 참조 |
| Ch16 토픽 생명주기 | 언어 무관; `03-spring-boot/16` 참조 |
| Ch19 프로덕션 사례 | 언어 무관; `03-spring-boot/19` 참조 |
| Ch20 공식 튜토리얼 | Spring 전용 |
| Ch21 Kafka Streams | JVM 전용; Go는 Ch11 파이프라인으로 대체 |

## 실습 프로젝트

`../../project/redpanda-go/` — 챕터별 서브커맨드로 실행.

```bash
cd ../../project && docker compose up -d   # Redpanda 시작
cd redpanda-go && make run-ch01            # 챕터 실행
```

## 구현 순서

| 단계 | 내용 |
|:----:|------|
| 1 | 스켈레톤 (go.mod, Makefile, config) |
| 2 | Ch01-04: Setup + Producer/Consumer |
| 3 | Ch05-06: 에러 처리 + 멱등성 |
| 4 | Ch07-09: 트랜잭션 + SAGA |
| 5 | Ch10-12: 테스트 + 파이프라인 + Avro |
| 6 | Ch13: 프로덕션 패턴 |
