# 04. 재시도, DLQ, 리플레이 Runbook (확정본)

## 1. 재시도 정책 확정
- max attempts: 5
- backoff: 5s -> 30s -> 2m -> 10m -> 30m
- transient 오류만 재시도

transient 예:
- timeout
- temporary network failure
- downstream 5xx

permanent 예:
- schema validation error
- required field missing
- invalid state transition

## 2. 토픽 확정 규칙
- 원본 예: `prod.cd.workflow.release.deployment.requested.v1`
- 재시도 예: `prod.cd.workflow.release.deployment.requested.v1.retry.1` ~ `.retry.5`
- DLQ 예: `prod.cd.workflow.release.deployment.requested.v1.dlq`

예:
- `prod.cd.workflow.release.deployment.requested.v1.dlq`
- `prod.ci.jenkins.build.completed.v1.retry.2`

## 3. DLQ 알람 임계치
- 5분 DLQ rate > 0.5%: warning
- 5분 DLQ rate > 2.0%: critical
- retry 평균 체류시간 > 10m: warning

## 4. 리플레이 절차 확정
1. incident 티켓 생성
2. 범위 확정(topic/partition/offset/time window)
3. dry-run (최소 100건 샘플)
4. 멱등키 충돌 검증
5. 제한 배치(예: 500건)로 재처리
6. 결과 리포트(성공/실패/잔여 건수)

## 5. 운영 책임자
- 1차 대응: 플랫폼 운영
- 데이터 검증: 도메인 서비스 오너
- 최종 승인: 배포 책임자
