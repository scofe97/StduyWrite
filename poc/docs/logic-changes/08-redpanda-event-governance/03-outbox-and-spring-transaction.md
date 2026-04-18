# 03. Outbox 패턴과 Spring 트랜잭션 정합성 (확정본)

## 1. 적용 대상 서비스
- `workflow-api`
- `pipeline-api`
- `scheduler`
- `notificator`

## 2. Outbox 테이블 확정 스키마
- `outbox_event_id` (PK)
- `aggregate_type`
- `aggregate_id`
- `topic_name`
- `partition_key`
- `event_type`
- `event_payload`
- `event_headers`
- `publish_status` (`NEW`, `PUBLISHED`, `FAILED`)
- `retry_count`
- `created_at`, `published_at`

## 3. 트랜잭션 확정 규칙
- 비즈니스 데이터 변경 + outbox insert는 단일 `@Transactional`
- Redpanda 발행은 relay가 비동기 처리
- relay 실패 시 status=`FAILED`, 재시도 큐 등록

## 4. Relay 운영값 (v1)
- poll interval: 1s
- batch size: 200
- publish timeout: 3s
- max retry: 5

## 5. 장애 시나리오 대응
- DB commit 성공 / publish 실패: outbox 재시도 가능
- publish 성공 / 상태 업데이트 실패: event_id 기반 중복 차단
- 장기 실패: DLQ로 이동 후 수동 재처리
