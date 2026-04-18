# 01. 이벤트 경계와 토픽/파티션 키 설계 (확정본)

## 1. 경계(Bounded Context) 확정
- `scm` 도메인: GitLab webhook/merge request
- `ci` 도메인: Jenkins build/test
- `registry` 도메인: Harbor push/scan
- `cd` 도메인: 배포 오케스트레이션(workflow-api)

이벤트 공개 주체:
- `pipeline-api`: CI/CD 파이프라인 상태 이벤트
- `workflow-api`: 릴리즈/배포 상태 이벤트
- `scheduler`: 예약 실행 트리거 이벤트
- `notificator`: 알림 송신 결과 이벤트

## 2. 토픽 네이밍 확정 규칙
포맷: `{env}.{domain}.{context}.{entity}.{event}.v{major}`

확정 예시:
- `prod.scm.gitlab.webhook.received.v1`
- `prod.ci.jenkins.build.requested.v1`
- `prod.ci.jenkins.build.completed.v1`
- `prod.ci.jenkins.build.failed.v1`
- `prod.registry.harbor.image.pushed.v1`
- `prod.registry.harbor.scan.completed.v1`
- `prod.cd.workflow.release.deployment.requested.v1`
- `prod.cd.workflow.release.deployment.completed.v1`
- `prod.cd.workflow.release.deployment.failed.v1`
- `prod.notify.notificator.message.sent.v1`

## 3. 파티션 키 확정
- 빌드/배포 흐름: `pipeline_id`
- merge request 중심 흐름: `merge_request_id`
- 이미지 흐름: `image_digest`
- 배포 단위 흐름: `release_id`

우선순위:
1. `release_id`
2. `pipeline_id`
3. `merge_request_id`
4. `image_digest`

## 4. 파티션 수 가이드 (v1)
- `*.build.*`: 12 partitions
- `*.deployment.*`: 12 partitions
- `*.scan.*`: 6 partitions
- `*.notify.*`: 3 partitions

운영 규칙:
- 파티션 증설 시 consumer group re-balance 리스크를 배포 계획에 포함
- 파티션 축소는 금지(새 토픽으로 마이그레이션)
