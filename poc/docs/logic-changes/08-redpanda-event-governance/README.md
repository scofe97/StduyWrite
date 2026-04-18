# Redpanda 이벤트 거버넌스 가이드 (확정본 v1)

대상 시스템: TRB305 (workflow-api, pipeline-api, scheduler, common-api, notificator) + GitLab + Jenkins + Harbor
환경: `dev`, `stg`, `prod`

## 문서 구성
1. [01-event-boundary-and-topic-design.md](01-event-boundary-and-topic-design.md)
2. [02-schema-contract-and-delivery-semantics.md](02-schema-contract-and-delivery-semantics.md)
3. [03-outbox-and-spring-transaction.md](03-outbox-and-spring-transaction.md)
4. [04-retry-dlq-replay-runbook.md](04-retry-dlq-replay-runbook.md)
5. [05-orchestration-observability-security.md](05-orchestration-observability-security.md)
6. [06-ci-cd-middleware-event-flow.md](06-ci-cd-middleware-event-flow.md)

## 확정 전제
- 이벤트 버전 정책: `v1` 시작, breaking 변경 시 `v2` 토픽 분리
- 직렬화: Avro + Schema Registry
- 전달 모델: at-least-once + idempotent consumer
- 배포 오케스트레이터: `workflow-api`
- 빌드 트리거 소스: GitLab webhook

## 10개 핵심 개념 매핑
- 1 이벤트 경계 -> 01
- 2 토픽/파티션 키 -> 01
- 3 스키마 계약/호환성 -> 02
- 4 전달 보장/멱등성 -> 02
- 5 Outbox 패턴 -> 03
- 6 재시도/백오프/DLQ -> 04
- 7 오케스트레이션 vs 코레오그래피 -> 05
- 8 관측성/추적 ID -> 05
- 9 보안/권한/멀티테넌시 -> 05
- 10 재처리/리플레이 -> 04
