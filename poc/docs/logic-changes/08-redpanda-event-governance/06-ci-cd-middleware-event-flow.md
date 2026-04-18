# 06. CI/CD 미들웨어 이벤트 플로우 표준 (확정본)

## 1. 시스템 구성 확정
- SCM: GitLab (`TRB305/*` 저장소)
- CI: Jenkins
- Registry: Harbor
- Domain services: `workflow-api`, `pipeline-api`, `scheduler`, `notificator`
- Broker: Redpanda

## 2. 표준 이벤트 플로우 (확정)
1. GitLab webhook 수신 (`pipeline-api`)
2. 빌드 요청 이벤트 발행 (`pipeline-api`)
3. Jenkins build 결과 이벤트 발행 (`jenkins-adapter`)
4. Harbor push/scan 결과 이벤트 발행 (`harbor-adapter`)
5. 배포 요청/완료 이벤트 발행 (`workflow-api`)
6. 결과 알림 이벤트 발행 (`notificator`)

## 3. 확정 토픽 목록 (v1)
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

## 4. 상관관계 규칙 확정
- 동일 릴리즈 흐름은 동일 `correlation_id` 유지 (`rel-YYYYMMDD-NNNNN`)
- 단계 간 원인 연결은 `causation_id=직전 event_id`
- 실패 이벤트 누락 금지

## 5. 실패/보상 규칙 확정
- Build 실패 -> 배포 단계 진입 금지
- Scan 실패(severity high) -> 배포 차단 + failed 이벤트 발행
- Deploy 실패 -> rollback 요청 이벤트 발행 + 알림 이벤트 발행
