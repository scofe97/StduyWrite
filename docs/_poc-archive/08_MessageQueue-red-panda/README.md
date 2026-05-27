# Redpanda 학습 저장소

Kafka 호환 스트리밍 플랫폼 Redpanda의 Helm 배포, Spring Boot 통합, 이벤트 기반 아키텍처 실습

## 학습 목표

- Redpanda 기본 개념과 아키텍처 이해
- Docker/Helm 기반 설치 및 배포
- Spring Boot + Kafka 클라이언트 통합
- SAGA 패턴, DLQ 전략 등 분산 트랜잭션 학습
- **TPS 패턴 모사**: pipeline-api ↔ ppln-logging-api 간 REST 기반 비동기 통신을 Redpanda 메시지큐로 대체하는 PoC

## 빠른 시작

```bash
# 1. Redpanda + Console 실행
cd project
docker-compose up -d
# Console 확인: http://localhost:8080

# 2. Spring Boot 빌드
cd redpanda-spring-boot
./gradlew build

# 3. 애플리케이션 실행 (로컬 프로파일)
./gradlew bootRun --args='--spring.profiles.active=local'

# 4. K8s 클러스터 연결 (dev 프로파일)
./gradlew bootRun --args='--spring.profiles.active=dev'

# 5. 헬스체크
curl http://localhost:8080/api/ch01/health

# 6. 테스트 (Testcontainers)
./gradlew test
```

## 참조 소스

| 자료 | 위치 |
|------|------|
| **Helm 차트** | `/Users/simbohyeon/okestro/tps_manifest/helm-charts/redpanda` (v25.3.1) |
| **이론 문서 (Redpanda)** | `runners-high/docs/08_MessageQueue/RedPanda/` |
| **이론 문서 (Event-Driven)** | `runners-high/docs/02_Architecture/03_EventDriven/` (17개 챕터) |
| **공식 문서** | https://docs.redpanda.com |
| **TPS pipeline-api** | `~/okestro/tps-gitlab2/pipeline-api/` (Jenkins 비동기 실행) |
| **TPS ppln-logging-api** | `~/okestro/tps-gitlab2/ppln-logging-api/` (비동기 메시지 상태 관리) |

## 폴더 구조

```
red-panda/
├── learning/                          # 학습 문서
│   ├── 01-helm-chart/                 # 설치 및 배포 (6 챕터)
│   ├── 02-fundamentals/               # 기본 개념 (9 챕터)
│   ├── 03-spring-boot-integration/    # Spring Boot 연동 (7 챕터)
│   ├── 04-advanced-patterns/          # 고급 패턴 (6 챕터)
│   └── 05-event-driven-poc/           # Redpanda 전용 이벤트 기반 PoC (3 챕터)
├── project/                           # 실습 코드
│   ├── docker-compose.yml             # Redpanda v25.3.6 + Console v3.5.1
│   ├── DEPLOYMENT.md                  # K8s 배포 레퍼런스
│   └── redpanda-spring-boot/          # Spring Boot 프로젝트
└── README.md                          # 이 파일
```

| # | 폴더 | 챕터 수 | 설명 |
|---|------|---------|------|
| 01 | [helm-chart](learning/01-helm-chart/) | 6 | 설치 및 배포 (Docker + Helm 차트 분석) |
| 02 | [fundamentals](learning/02-fundamentals/) | 9 | Redpanda 기본 개념, 아키텍처, Kafka 비교, Schema Registry, Tiered Storage |
| 03 | [spring-boot-integration](learning/03-spring-boot-integration/) | 7 | Spring Boot 연계, SAGA 패턴, TPS 패턴 모사 |
| 04 | [advanced-patterns](learning/04-advanced-patterns/) | 6 | 모니터링, 보안, 운영, OpenTelemetry, 에러 처리, CI/CD |
| 05 | [event-driven-poc](learning/05-event-driven-poc/) | 3 | Redpanda 전용 PoC (WASM, Connect, Iceberg). 범용 EDA 패턴은 `poc/02_Architecture/01-event-driven/`으로 이동 |

## Project (실습 코드)

```
project/
├── docker-compose.yml          # Redpanda v25.3.6 + Console v3.5.1
├── DEPLOYMENT.md               # K8s 배포 레퍼런스 (폐쇄망 실전 경험)
└── redpanda-spring-boot/       # Spring Boot 프로젝트
    ├── build.gradle
    └── src/
        ├── main/java/com/study/redpanda/
        │   ├── config/             # Kafka 공통 설정
        │   ├── common/event/       # 공통 이벤트 DTO
        │   ├── ch01/               # basic-setup (헬스체크)
        │   ├── ch02/               # producer-consumer (TODO)
        │   ├── ch07/               # middleware-architecture ★TPS 패턴
        │   │   ├── event/          # 이벤트 DTO (완성)
        │   │   ├── model/          # MessageStatus enum (완성)
        │   │   ├── config/         # 토픽 설정 (완성)
        │   │   ├── producer/       # PipelineProducer (TODO)
        │   │   ├── consumer/       # JenkinsWorkerConsumer, LoggingConsumer (TODO)
        │   │   └── service/        # PipelineService, MessageStatusService (TODO)
        │   └── ...
        └── test/
```

### 프로파일 설정

| 프로파일 | bootstrap-servers | 용도 |
|----------|------------------|------|
| `local` (기본) | `localhost:19092` | docker-compose 로컬 개발 |
| `dev` | `10.255.17.176:31092` | K8s 클러스터 연결 |

### TPS 패턴 매핑 (ch07)

| TPS 원본 | PoC 대응 | 변경점 |
|----------|---------|--------|
| `JenkinsFeignClient` (REST) | `PipelineProducer` (Kafka) | REST → 메시지큐 |
| `AsyncMessageFeignClient` (REST) | `LoggingConsumer` (Kafka) | Feign → @KafkaListener |
| `CompletableFuture` + `Thread.sleep(10000)` | 토픽 기반 비동기 | 폴링 → 이벤트 드리븐 |
| `TB_TPS_MS_021` 상태관리 | `MessageStatusService` (인메모리) | DB → 인메모리 (PoC용) |
| `Quartz 스케줄러` 재시도 | `@RetryableTopic` 또는 DLQ | 스케줄러 → 카프카 재시도 |

> **흐름도**: AS-IS(REST+Quartz) vs TO-BE(Redpanda) 비교 다이어그램은 [TPS-FLOW-DIAGRAM.md](TPS-FLOW-DIAGRAM.md) 참고

## Redpanda vs Kafka 요약

| 항목 | Redpanda | Kafka |
|------|----------|-------|
| 언어 | C++ (Seastar) | Java/Scala (JVM) |
| ZooKeeper | 불필요 (내장 Raft) | KRaft/ZK 필요 |
| Schema Registry | 내장 | 별도 Confluent SR |
| HTTP Proxy | 내장 (Pandaproxy) | 별도 REST Proxy |
| 튜닝 | 자동 | 수동 튜닝 필요 |
| 지연시간 | 10x 낮음 (공칭) | 기준 |
| 비용 | 3-6x 효율적 | 기준 |

## 2026 최신 기능 (v25.3+)

- **Shadowing**: 재해 복구용 비동기 오프셋 보존 복제
- **AWS Glue Catalog 통합**: Iceberg 테이블로 토픽 연동
- **Testcontainers 개선**: Kafka 대비 2배 빠른 테스트 시작
- **WASM Data Transforms (GA)**: 브로커 내 데이터 변환 (별도 스트림 프로세서 불필요)
- **Iceberg Topics (GA)**: 토픽을 Iceberg 테이블로 자동 변환
- **Redpanda Connect (GA)**: 300+ 커넥터 기반 선언적 데이터 파이프라인
- **Serverless**: 완전 관리형 서버리스 스트리밍 (AWS/GCP)

## 학습 순서

```
02-fundamentals (개념)
     ↓
01-helm-chart (배포)
     ↓
03-spring-boot-integration (연동 + TPS 패턴 실습)
     ↓
04-advanced-patterns (고급)
     ↓
05-event-driven-poc (이벤트 기반 실습)
```
