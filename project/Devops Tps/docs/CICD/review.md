# CICD 구현 리뷰

## What: 무엇을 구현했는가

CICDService는 Jenkins 파이프라인의 전체 생명주기를 gRPC 인터페이스로 추상화한 서비스다. 파이프라인 CRUD(4개 RPC)와 빌드 관리(4개 RPC)로 구성되며, 외부에서는 Jenkins의 존재를 알 필요 없이 `pipeline_id`와 `build_number`만으로 CI/CD를 제어할 수 있다.

구현 범위:
- `cicd.proto` → `cicd_server.go` (8개 RPC 구현)
- 인메모리 파이프라인 스토어 (`map[string]Pipeline`)
- Jenkins HTTP API 호출 (빌드 트리거, 로그 조회)
- Kafka `cicd-results` 토픽 소비 → 빌드 상태 업데이트

---

## How: 어떻게 구현했는가

### 인메모리 파이프라인 스토어

파이프라인은 외부 DB 없이 Go 맵으로 관리된다. 서버 재시작 시 데이터가 초기화되는 제약이 있지만, Phase 3의 학습 목적에는 충분하다.

```go
// internal/server/cicd_server.go
type CICDServer struct {
    pb.UnimplementedCICDServiceServer
    pipelines map[string]*pb.Pipeline  // id → Pipeline
    builds    map[string][]*pb.Build   // pipeline_id → []Build
    mu        sync.RWMutex
}
```

### Jenkins HTTP API 통합

Jenkins 빌드 트리거는 `CIConfig.oneof`에서 Jenkins 설정을 꺼내 HTTP 클라이언트로 직접 호출한다. CSRF 토큰(crumb) 획득 → 빌드 API 호출 순서를 따른다.

```
TriggerBuild 흐름:
1. 파이프라인 조회 → JenkinsConfig 추출
2. GET /crumbIssuer/api/json → crumb 획득
3. POST /{jenkins_job_name}/build (Authorization: Basic, crumb 헤더)
4. Build 객체 생성 (status: QUEUED)
5. 반환
```

### 이벤트 기반 빌드 상태 업데이트

빌드 상태는 Jenkins가 직접 Kafka `cicd-results` 토픽에 결과를 발행하면, git-provider 메인 루프의 Kafka 컨슈머가 소비하여 인메모리 빌드 상태를 업데이트하는 방식으로 동작한다. 이는 폴링이 아닌 Observer(이벤트 드리븐) 패턴이다.

```
cicd-results 메시지 구조:
{
  "pipeline_id": "...",
  "build_number": 42,
  "status": "SUCCESS",
  "finished_at": "2025-01-01T10:00:00Z",
  "duration_seconds": 120
}
```

---

## Why: 왜 이렇게 설계했는가

### Jenkins 추상화 — 향후 CI 프로바이더 교체 가능

`CIConfig.oneof` 설계의 핵심 이유는 벤더 종속(vendor lock-in) 방지다. 현재는 Jenkins만 지원하지만, proto를 수정하지 않고 `GitHubActionsConfig` 필드를 oneof에 추가하는 것만으로 새 CI 프로바이더를 지원할 수 있다. 서버 측 구현도 switch문 하나로 프로바이더를 분기할 수 있어 기존 Jenkins 코드를 건드리지 않는다.

```go
switch cfg := pipeline.CiConfig.Config.(type) {
case *pb.CIConfig_Jenkins:
    return s.triggerJenkins(ctx, cfg.Jenkins, pipeline.JenkinsJobName, req)
// 향후: case *pb.CIConfig_GithubActions:
}
```

### 이벤트 기반 상태 업데이트 — 폴링 제거

빌드 상태를 폴링으로 가져오면 Jenkins에 불필요한 HTTP 부하가 발생하고 상태 갱신 지연이 생긴다. Kafka를 통한 이벤트 발행 방식은 Jenkins가 완료 시점에 한 번만 이벤트를 보내면 되므로 결합도와 부하 모두 낮아진다.

### 인메모리 스토어 — 단순성 우선

Phase 3 학습 목적에서 외부 DB를 도입하면 Docker Compose 의존성이 늘어나고 디버깅이 복잡해진다. 인메모리 스토어는 배포 복잡도를 낮추는 대신 영속성을 포기한 의도적 트레이드오프다. 실운영 전환 시 `sync.RWMutex` 보호 하에 있는 맵을 Redis나 PostgreSQL로 교체하면 된다.

---

## 적용 패턴

| 패턴 | 적용 위치 | 설명 |
|------|----------|------|
| **Strategy** | `CIConfig.oneof` | CI 프로바이더를 런타임에 교체 가능 |
| **Observer** | Kafka cicd-results 컨슈머 | 빌드 완료 이벤트를 구독하여 상태 갱신 |
| **Facade** | CICDService | Jenkins HTTP API 복잡도를 단순 RPC로 감춤 |

---

## 알려진 한계

| 항목 | 현재 상태 | 개선 방향 |
|------|----------|----------|
| 파이프라인 영속성 | 인메모리 (재시작 시 초기화) | PostgreSQL 또는 Redis 도입 |
| 빌드 로그 스트리밍 | 완료 후 전체 텍스트 반환 | Server-side streaming RPC로 전환 |
| Jenkins crumb 캐싱 | 매 요청마다 crumb 재획득 | 캐싱으로 Jenkins 요청 수 감소 |
| 동시 빌드 제한 | 없음 | 파이프라인당 concurrent build 수 제한 |
