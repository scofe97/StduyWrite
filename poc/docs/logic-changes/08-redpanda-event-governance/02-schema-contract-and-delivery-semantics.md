# 02. 스키마 계약과 전달 보장/멱등성 (확정본)

## 1. 스키마 표준 확정
- 직렬화: Avro
- Registry Subject 예: `prod.cd.workflow.release.deployment.requested.v1-value`
- 호환성: BACKWARD

## 2. 공통 이벤트 Envelope (v1)
필수 필드:
- `event_id` (UUID)
- `event_type`
- `event_version`
- `occurred_at` (UTC ISO-8601)
- `producer_service`
- `trace_id`
- `correlation_id`
- `causation_id`
- `tenant_id`
- `idempotency_key`

## 3. 전달 보장 모델 확정
- Broker -> Consumer: at-least-once
- Consumer는 idempotency 저장소 필수 사용
- 성공 처리 후 commit

## 4. 멱등 키 확정 포맷
- Build: `build:{pipeline_id}:{build_number}`
- Deployment: `deploy:{release_id}:{stage}`
- Scan: `scan:{image_digest}:{scanner}`

## 5. Spring Boot 소비자 처리 순서
1. 헤더/스키마 검증
2. 멱등 키 조회
3. 비즈니스 처리
4. 성공 시 멱등 키 저장 + offset commit
5. 실패 시 오류 분류(transient/permanent)

## 6. 샘플 헤더 (확정)
```json
{
  "event_id": "2f9d901f-a81c-4f44-a6fd-38c2f1456f9f",
  "event_type": "cd.workflow.release.deployment.completed",
  "event_version": "1",
  "occurred_at": "2026-02-18T13:55:00Z",
  "producer_service": "workflow-api",
  "trace_id": "6e8d68db98664de8a1e3f5f9f6dc0f56",
  "correlation_id": "rel-20260218-00017",
  "causation_id": "23f8172c-f8b2-4ed8-aa3f-91e8b4e9ed8a",
  "tenant_id": "TRB305",
  "idempotency_key": "deploy:rel-20260218-00017:prod"
}
```
