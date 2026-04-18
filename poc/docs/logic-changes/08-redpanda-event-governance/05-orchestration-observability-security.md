# 05. 오케스트레이션, 관측성, 보안/권한 (확정본)

## 1. 오케스트레이션 확정
중앙 오케스트레이터: `workflow-api`

역할:
- GitLab -> Jenkins -> Harbor -> Deploy 흐름 상태머신 관리
- 단계별 timeout/compensation 처리
- 실패 이벤트 표준 발행

## 2. 관측성 확정 필드
필수 로그 필드:
- `event_type`, `topic`, `partition`, `offset`
- `trace_id`, `correlation_id`, `causation_id`
- `producer_service`, `consumer_service`, `result`

필수 메트릭:
- `consumer_lag`
- `event_retry_total`
- `event_dlq_total`
- `schema_validation_failure_total`
- `event_end_to_end_latency_ms`

## 3. 보안/권한 확정
서비스 계정 분리:
- `svc-workflow-api`
- `svc-pipeline-api`
- `svc-scheduler`
- `svc-notificator`
- `svc-jenkins-adapter`
- `svc-gitlab-adapter`
- `svc-harbor-adapter`

규칙:
- producer/consumer ACL 최소 권한
- topic wildcard 권한 금지 (`prod.*` 전체 권한 금지)
- payload에 secret/token/password 금지
- `tenant_id=TRB305` 기본 강제
