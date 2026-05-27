# 02. Fundamentals

## 개요

Redpanda의 핵심 개념과 아키텍처를 다룬다. 로그 스토리지 원리, Kafka 비교, Schema Registry, Tiered Storage부터 토픽 설계, 트랜잭션, Geo-Replication까지 이론적 기반을 제공한다.

> **상세 이론 문서**: `runners-high/docs/08_MessageQueue/RedPanda/`

## 챕터 목록

| # | 문서 | 설명 | 상태 |
|---|------|------|------|
| 01 | [01-overview.md](./01-overview.md) | Redpanda 소개, 탄생 배경, Seastar, 라이선스 | 완료 |
| 02 | [02-kafka-comparison.md](./02-kafka-comparison.md) | Kafka vs Redpanda 상세 비교, 마이그레이션 | 완료 |
| 03 | [03-use-cases.md](./03-use-cases.md) | 프로덕션 사례, 선택 가이드, 면접 답변 | 완료 |
| 04 | [04-architecture.md](./04-architecture.md) | Thread-per-core, Raft 합의, 네트워크 아키텍처 | 완료 |
| 05 | [05-core-features.md](./05-core-features.md) | Pandaproxy, 자동 튜닝, rpk CLI, WASM, Connect | 완료 |
| 06 | [06-consumer-groups.md](./06-consumer-groups.md) | Consumer Group, 리밸런싱, 파티션 할당 전략 | 완료 |
| 07 | [07-schema-registry.md](./07-schema-registry.md) | 스키마 관리, 호환성 모드, Avro/Protobuf | 완료 |
| 08 | [08-avro-deep-dive.md](./08-avro-deep-dive.md) | Avro 포맷 심화: 인코딩, 스키마 진화, Wire Format | 완료 |
| 09 | [09-message-schema-design.md](./09-message-schema-design.md) | CloudEvents, AsyncAPI, 미들웨어별 스키마 제어 | 완료 |
| 10 | [10-topic-design.md](./10-topic-design.md) | 토픽 네이밍, 파티셔닝 전략, 미들웨어별 주소 체계 (거버넌스 요약 → 11 참조) | 완료 |
| 11 | [11-topic-governance-gitops.md](./11-topic-governance-gitops.md) | 토픽 거버넌스 마스터 문서: GitOps, 명명 규칙, 생애주기 정책 | 완료 |
| 12 | [12-log-storage.md](./12-log-storage.md) | 로그 기반 스토리지, 세그먼트, 인덱스, Compaction | 완료 |
| 13 | [13-retention-compaction-strategies.md](./13-retention-compaction-strategies.md) | 보존 정책, Log Compaction, Tombstone, 무기한 보존 | 완료 |
| 14 | [14-tiered-storage.md](./14-tiered-storage.md) | 클라우드 스토리지 오프로드, 비용 최적화 | 완료 |
| 15 | [15-storage-requirements.md](./15-storage-requirements.md) | 스토리지 요구사항, NFS 비호환성, 디스크 구성 | 완료 |
| 16 | [16-transactions.md](./16-transactions.md) | Kafka 트랜잭션 API, Redpanda 호환성, commit/abort 시맨틱스 | 완료 |
| 17 | [17-reference-architecture.md](./17-reference-architecture.md) | 단일/멀티 클러스터, 이벤트 드리븐 MSA, CQRS, CDC, 사이징 | 완료 |
| 18 | [18-microservice-migration-patterns.md](./18-microservice-migration-patterns.md) | 폴리글랏 아키텍처, Strangler Fig 패턴, 비동기 API 전환 | 완료 |
| 19 | [19-geo-replication.md](./19-geo-replication.md) | Geo-Replication, 멀티 클러스터, MirrorMaker 2, Remote Read Replicas | 완료 |
| Appendix | [appendix-event-source-sink.md](./appendix-event-source-sink.md) | Source/Sink 패턴 개요 → 상세는 `07-connectors/` 참조 (리디렉트) | 리디렉트 |

## 학습 순서 (권장)

> **설계 원칙**: "왜 쓰는가" → "어떻게 동작하는가" → "어떻게 설계하는가" → "고급 패턴" 순서로 진행. 각 단계를 끝낸 뒤 다음 단계로 넘어가는 것을 권장하지만, 단계 내 문서는 순서 무관하게 읽어도 된다.

### 1단계: Redpanda가 뭔데? (What & Why)

> 목표: Redpanda의 정체, Kafka와의 차이, 실제 사용처를 파악한다.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ① | 01-overview | Redpanda는 왜 만들었고, 뭐가 다른가? | ★☆☆ |
| ② | 02-kafka-comparison | Kafka 대비 구체적으로 뭐가 좋은가? | ★☆☆ |
| ③ | 03-use-cases | 실무에서 누가, 어디에 쓰는가? | ★☆☆ |

### 2단계: 어떻게 동작하지? (Core Mechanics)

> 목표: 브로커 내부 구조, 핵심 기능, 메시지 소비의 기본 단위를 이해한다.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ④ | 04-architecture | Thread-per-core, Raft 합의가 뭔가? | ★★☆ |
| ⑤ | 05-core-features | rpk CLI, HTTP Proxy, WASM, Connect는 뭔가? | ★☆☆ |
| ⑥ | 06-consumer-groups | Consumer Group과 리밸런싱은 어떻게 동작하는가? | ★★☆ |

### 3단계: 스키마와 메시지 설계 (Schema & Message)

> 목표: 메시지 형식을 정의하고 스키마를 관리하는 방법을 익힌다. 스키마 관련 3개 문서를 연속으로 학습.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ⑦ | 07-schema-registry | 스키마 레지스트리가 왜 필요하고 어떻게 쓰는가? | ★★☆ |
| ⑧ | 08-avro-deep-dive | Avro 인코딩, 타입 시스템, 스키마 진화는 어떻게 동작하는가? _(선택)_ | ★★★ |
| ⑨ | 09-message-schema-design | CloudEvents, AsyncAPI로 메시지 구조를 어떻게 표준화하는가? | ★★☆ |

> ⑦→⑧ 흐름: 스키마 레지스트리 개념 → Avro 포맷 심화. ⑧을 건너뛰고 ⑨로 가도 무방.

### 4단계: 토픽 설계와 거버넌스 (Topic Design)

> 목표: 토픽 네이밍/파티셔닝 전략을 세우고, GitOps 기반 거버넌스를 이해한다. 토픽 관련 2개 문서를 연속 학습.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ⑩ | 10-topic-design | 토픽 이름, 파티션 수, 키 전략을 어떻게 정하는가? | ★★☆ |
| ⑪ | 11-topic-governance-gitops | 토픽 생애주기를 GitOps로 어떻게 관리하는가? | ★★☆ |

> ⑩→⑪ 흐름: 토픽을 어떻게 설계하는가 → 설계한 토픽을 조직에서 어떻게 관리하는가.

### 5단계: 스토리지 심화 (Storage Deep Dive)

> 목표: 데이터 저장 원리, 보존/압축 정책, 클라우드 오프로드를 이해한다. 스토리지 관련 4개 문서를 연속 학습.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ⑫ | 12-log-storage | 로그 세그먼트, 인덱스, Compaction은 어떻게 동작하는가? | ★★★ |
| ⑬ | 13-retention-compaction-strategies | 데이터를 얼마나 보관하고 어떻게 정리하는가? | ★★☆ |
| ⑭ | 14-tiered-storage | 오래된 데이터를 클라우드로 자동 이동하려면? | ★★☆ |
| ⑮ | 15-storage-requirements | 디스크 타입, 용량 산정, NFS 비호환 주의사항은? | ★★☆ |

> ⑫→⑬ 흐름: 로그가 어떻게 저장되는가 → 저장된 로그를 어떻게 정리하는가. ⑬→⑭ 흐름: 로컬 보존 정책 → 클라우드 오프로드 전략.

### 6단계: 고급 시맨틱스 (Advanced Patterns)

> 목표: 트랜잭션, 스트림 처리, 아키텍처 패턴을 익힌다. 5단계까지 완료 후 진입.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ⑯ | 16-transactions | Exactly-once와 CTP 패턴은 어떻게 구현하는가? | ★★★ |
| ⑰ | 17-reference-architecture | CQRS, CDC, 이벤트 드리븐 MSA 아키텍처는 어떻게 구성하는가? | ★★★ |
| ⑱ | 18-microservice-migration-patterns | 모놀리스에서 MSA로 어떻게 전환하는가? | ★★★ |
| ⑲ | 19-geo-replication | 멀티 리전 복제와 DR을 어떻게 구성하는가? | ★★★ |

> ⑰→⑱ 흐름: MSA 레퍼런스 아키텍처 → MSA 전환 패턴. ⑱→⑲ 흐름: 단일 클러스터 MSA → 멀티 리전 확장.
> **참고**: 스트림 처리(구 17번)는 [09-kafka-streams/](../09-kafka-streams/)로 분리되었다.

### 제외

| 문서 | 사유 |
|------|------|
| appendix-event-source-sink | 리디렉트 stub → `07-connectors/` 참조 |

## 관련 폴더

- [03-spring-boot-integration](../03-spring-boot-integration/) — Spring Boot 연계 구현 실습
- [04-advanced-patterns](../04-advanced-patterns/) — 모니터링, 보안, 운영, CI/CD
- [05-event-driven-poc](../05-event-driven-poc/) — Redpanda 전용 기능 PoC (WASM, Iceberg)
- [07-connectors](../07-connectors/) — 17-event-source-sink의 Source/Sink 패턴 상세 구현
- [09-kafka-streams](../09-kafka-streams/) — Kafka Streams 이론 + Event Design (구 17-stream-processing 이동)

## 문서 분리 이력

- **11-topic-governance-gitops.md** (신규): 10-topic-design의 거버넌스 섹션을 분리한 마스터 문서. 토픽 생명주기 전략과 GitOps 적용 방법을 상세히 다룬다.
- **08-avro-deep-dive.md** (신규): 07-schema-registry에서 Avro 관련 내용을 분리한 심화 문서.
- **appendix-event-source-sink.md**: Source/Sink 구현 상세 내용은 `07-connectors/`로 이동. 이 파일은 개념 요약과 링크만 유지.
- **17-stream-processing.md** → `09-kafka-streams/01-stream-processing.md`로 분리. Kafka Streams 이론과 Event Design 코스를 통합하여 독립 디렉토리로 관리.
