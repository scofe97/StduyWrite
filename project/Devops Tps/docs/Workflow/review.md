# Workflow E2E 구현 리뷰

## What: 무엇을 구현했는가

WorkflowService는 Git 이벤트(MR merge, push)를 받아 미리 정의된 스텝 순서대로 CI/CD 파이프라인을 자동 실행하는 오케스트레이터다. Phase 3-C의 핵심 컴포넌트로, webhook 수신부터 Jenkins 빌드 완료까지 전체 E2E 흐름을 이벤트 기반으로 연결한다.

구현 범위:
- `workflow.proto` → `workflow_server.go` (6개 RPC 구현)
- 인메모리 워크플로우 스토어 + 실행 이력 스토어
- Kafka `git-events` 토픽 소비 → 워크플로우 매칭 → 실행 오케스트레이션
- Kafka `cicd-results` 토픽 소비 → 스텝 완료 처리 → 다음 스텝 진행
- Redpanda Connect를 통한 webhook 정규화

---

## How: 어떻게 구현했는가

### Redpanda Connect: Webhook 정규화

다양한 Git 플랫폼(GitHub, GitLab, Bitbucket)의 webhook 페이로드 형식이 제각각이므로, Redpanda Connect가 정규화 레이어 역할을 한다. HTTP 엔드포인트로 webhook을 수신하고, `bloblang` 매핑으로 통일된 형식으로 변환하여 `git-events` 토픽에 발행한다.

```yaml
# redpanda-connect 설정 예시
input:
  http_server:
    address: "0.0.0.0:8090"
    path: /webhook

pipeline:
  processors:
    - bloblang: |
        root.event = match this.object_kind {
          "merge_request" => "mr_merged"
          _ => "push"
        }
        root.repository = this.project.path_with_namespace
        root.branch = this.object_attributes.target_branch
        root.commit_sha = this.object_attributes.last_commit.id

output:
  kafka:
    addresses: ["redpanda:9092"]
    topic: git-events
```

### Kafka 컨슈머: 이벤트 라우팅

`cmd/server/main.go`의 메인 루프가 `git-events` 토픽을 소비하고, 이벤트 타입에 따라 워크플로우 엔진으로 전달한다.

```go
// main.go Kafka 컨슈머 루프
for {
    msg, err := consumer.FetchMessage(ctx)
    var event GitEvent
    json.Unmarshal(msg.Value, &event)

    switch event.Event {
    case "mr_merged", "push":
        workflowEngine.Handle(ctx, event)
    case "build_result":
        cicdService.UpdateBuildStatus(ctx, event)
    }
    consumer.CommitMessages(ctx, msg)
}
```

### 워크플로우 엔진: 매칭 → 실행 → 상태 관리

워크플로우 엔진의 핵심은 이벤트를 받았을 때 매칭 워크플로우를 찾고, Execution을 생성하여 스텝을 순차 실행하는 것이다.

```
Handle(event) 흐름:
1. 모든 워크플로우를 순회하며 trigger_event + filter 매칭
2. 매칭 워크플로우 존재 시 Execution 생성 (status: RUNNING)
3. executeStep(execution, stepIndex=0) 호출
   a. CICDService.TriggerBuild(pipeline_id)
   b. Execution.status = WAITING_FOR_STEP
4. cicd-results 이벤트 수신 시:
   a. 해당 Execution 조회
   b. 스텝 성공 → 다음 스텝 실행 또는 COMPLETED
   c. 스텝 실패 → FAILED 처리
```

### CICD 커맨드 핸들러: Jenkins HTTP 호출

워크플로우 엔진은 CICDService의 `TriggerBuild` RPC를 호출하고, CICDService는 파이프라인의 JenkinsConfig를 사용하여 Jenkins HTTP API를 호출한다.

```
워크플로우 엔진 → CICDService.TriggerBuild → Jenkins POST /{job}/build
```

---

## Why: 왜 이렇게 설계했는가

### 이벤트 기반 아키텍처 — 느슨한 결합

각 컴포넌트(Redpanda Connect, 워크플로우 엔진, CICDService, Jenkins)는 Kafka 토픽을 통해서만 통신한다. Git 플랫폼이 GitLab에서 GitHub으로 바뀌어도 Redpanda Connect 매핑만 수정하면 되고, CI 도구가 Jenkins에서 GitHub Actions로 바뀌어도 CICDService의 내부 구현만 교체하면 된다. 워크플로우 엔진은 어느 쪽도 직접 의존하지 않는다.

### Redpanda Connect 도입 — 정규화 책임 분리

webhook 정규화를 git-provider Go 코드에서 하면 플랫폼별 분기 로직이 코드에 녹아들고 테스트가 어려워진다. Redpanda Connect에 위임하면 설정 파일(YAML)만으로 매핑을 변경할 수 있어 배포 없이 webhook 형식 변경에 대응할 수 있다.

### 오케스트레이터 패턴 — 중앙 실행 제어

코레오그래피(각 서비스가 이벤트를 듣고 자율적으로 반응) 대신 오케스트레이터 패턴을 선택한 이유는 실행 상태를 한 곳에서 추적해야 하기 때문이다. 스텝 실패 시 어느 단계에서 실패했는지, 현재 어느 스텝을 실행 중인지를 워크플로우 엔진이 단일 진실 공급원(Single Source of Truth)으로 관리한다.

### 이벤트 소싱(부분적) — 실행 이력 보존

Execution과 StepExecution을 별도로 저장하는 구조는 부분적 이벤트 소싱 패턴이다. 단순히 "성공/실패" 결과만 저장하는 것이 아니라 각 스텝의 시작·종료 시각, 중간 상태를 모두 보존하여 사후 분석과 디버깅이 가능하다.

---

## 적용 패턴

| 패턴 | 적용 위치 | 설명 |
|------|----------|------|
| **Orchestrator** | 워크플로우 엔진 | 스텝 순서와 상태를 중앙에서 제어 |
| **Event Sourcing (부분)** | Execution/StepExecution | 각 스텝의 전체 이력 보존 |
| **Command** | CICDService.TriggerBuild | 빌드 트리거를 커맨드 객체로 캡슐화 |
| **Observer** | Kafka cicd-results 컨슈머 | 빌드 결과 이벤트 구독 |

---

## E2E 흐름 요약

```
GitLab MR merge
  → webhook (HTTP POST :8090)
  → Redpanda Connect (정규화)
  → git-events Kafka 토픽
  → git-provider Kafka 컨슈머
  → 워크플로우 매칭 (trigger_event=mr_merged, filter 비교)
  → Execution 생성 (RUNNING)
  → CICDService.TriggerBuild (스텝 1)
  → Jenkins POST /job/{name}/build
  → Execution (WAITING_FOR_STEP)
  → Jenkins 빌드 완료
  → cicd-results 토픽 발행
  → 컨슈머 수신 → 스텝 1 success
  → 스텝 2가 있으면 반복, 없으면 COMPLETED
```

---

## 알려진 한계

| 항목 | 현재 상태 | 개선 방향 |
|------|----------|----------|
| 실행 이력 영속성 | 인메모리 (재시작 시 초기화) | PostgreSQL 이관 |
| 스텝 병렬 실행 | 순차 실행만 지원 | DAG 기반 병렬 스텝 |
| Webhook 보안 | 서명 검증 없음 | HMAC 서명 검증 추가 |
| 재시도 정책 | 스텝 실패 시 즉시 FAILED | 지수 백오프 재시도 |
| 실행 취소 | 진행 중 Execution 취소 불가 | CancelExecution RPC 추가 |
