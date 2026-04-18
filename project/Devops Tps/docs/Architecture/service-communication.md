# 서비스 간 통신

## 전체 서비스 통신 다이어그램

```mermaid
graph TD
    FE["Frontend (React)"]
    TPS["TPS-API<br/>Spring Boot :8080"]
    GP["Git-Provider<br/>Go :50051 gRPC"]
    GPR["Git-Provider<br/>REST Gateway :8080"]
    GH["GitHub API"]
    GL["GitLab API"]
    BB["Bitbucket API"]
    KAFKA["Kafka / Redpanda"]
    JENKINS["Jenkins"]
    RC["Redpanda Connect<br/>(Webhook 수신)"]

    FE -->|REST| TPS
    TPS -->|gRPC| GP
    GP --- GPR
    GPR -->|REST| GH
    GPR -->|REST| GL
    GPR -->|REST| BB
    TPS -->|Produce| KAFKA
    KAFKA -->|Consume| TPS
    GP -->|Produce/Consume| KAFKA
    RC -->|Webhook 이벤트| KAFKA
    KAFKA -->|git-events| GP
    GP -->|REST API| JENKINS
    JENKINS -->|Webhook| RC
```

---

## 통신 프로토콜 정리

| 구간 | 프로토콜 | 비고 |
|------|---------|------|
| Frontend → TPS-API | REST (HTTP/1.1) | JSON 응답 |
| TPS-API → Git-Provider | gRPC (HTTP/2) | proto3, :50051 |
| Git-Provider → GitHub/GitLab/Bitbucket | REST (HTTPS) | Provider별 API |
| TPS-API ↔ Kafka | Kafka Protocol | franz-go |
| Git-Provider ↔ Kafka | Kafka Protocol | franz-go |
| Git-Provider → Jenkins | REST (HTTP) | Jenkins Remote API |
| Jenkins → Redpanda Connect | Webhook (HTTP) | POST |
| Redpanda Connect → Kafka | Kafka Protocol | git-events 토픽 |

---

## 주요 흐름 시퀀스 다이어그램

### 1. 저장소 생성 흐름

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant TPS as TPS-API
    participant GP as Git-Provider
    participant VCS as Provider API

    FE->>TPS: POST /api/repositories
    TPS->>TPS: Connection 조회 (DB)
    TPS->>GP: gRPC CreateRepository(req)
    GP->>GP: ProviderConfig type switch
    GP->>VCS: Provider REST API 호출
    VCS-->>GP: Repository Created
    GP-->>TPS: pb.Repository
    TPS->>TPS: DB 저장
    TPS-->>FE: 200 OK + Repository
```

### 2. Webhook → Kafka → Workflow 흐름

```mermaid
sequenceDiagram
    participant VCS as GitHub/GitLab/Bitbucket
    participant RC as Redpanda Connect
    participant KAFKA as Kafka
    participant GP as Git-Provider
    participant TPS as TPS-API

    VCS->>RC: Webhook 이벤트 (push, PR 등)
    RC->>KAFKA: git-events 토픽 Produce
    KAFKA->>GP: git-events 토픽 Consume
    GP->>GP: 이벤트 파싱 및 처리
    GP->>KAFKA: runners-high.git.events Produce
    KAFKA->>TPS: runners-high.git.events Consume
    TPS->>TPS: 워크플로우 트리거 판단
    TPS->>KAFKA: runners-high.workflow.events Produce
```

### 3. CI/CD 파이프라인 트리거 흐름

```mermaid
sequenceDiagram
    participant TPS as TPS-API
    participant KAFKA as Kafka
    participant GP as Git-Provider
    participant JENKINS as Jenkins

    TPS->>KAFKA: cicd.commands Produce
    KAFKA->>GP: cicd.commands Consume
    GP->>JENKINS: REST API - 빌드 트리거
    JENKINS-->>GP: 빌드 ID 반환
    JENKINS->>GP: Webhook (빌드 완료)
    GP->>KAFKA: cicd.events Produce
    KAFKA->>TPS: cicd.events Consume
    TPS->>TPS: 빌드 상태 업데이트
```

---

## Kafka 토픽 라우팅 테이블

| 토픽 | 생산자 | 소비자 | 설명 |
|------|--------|--------|------|
| `runners-high.git.commands` | TPS-API | Git-Provider | Git 작업 명령 |
| `runners-high.git.events` | Git-Provider | TPS-API | Git 이벤트 결과 |
| `runners-high.notifications` | TPS-API | Notification Service | 알림 발송 |
| `runners-high.ticket.events` | TPS-API | TPS-API | 티켓 상태 변경 |
| `runners-high.build.events` | TPS-API | TPS-API | 빌드 상태 변경 |
| `runners-high.deploy.events` | TPS-API | TPS-API | 배포 상태 변경 |
| `runners-high.workflow.events` | TPS-API | TPS-API | 워크플로우 실행 |
| `runners-high.approval.events` | TPS-API | TPS-API | 결재 승인/반려 |
| `git-events` | Redpanda Connect | Git-Provider | Webhook 원시 이벤트 |
| `cicd.commands` | Git-Provider | Git-Provider | CI/CD 명령 |
| `cicd.events` | Git-Provider | Git-Provider | CI/CD 이벤트 |
| `cicd-results` | Git-Provider | TPS-API | CI/CD 최종 결과 |
| `workflow.events` | Git-Provider | TPS-API | 워크플로우 이벤트 |

---

## gRPC 서버 시작 흐름

Git-Provider `main.go`는 두 개의 goroutine으로 서버를 구동한다.

```mermaid
sequenceDiagram
    participant Main as main.go
    participant gRPC as gRPC Server :50051
    participant REST as REST Gateway :8080

    Main->>gRPC: goroutine 1 시작
    gRPC->>gRPC: GitService 등록
    gRPC->>gRPC: BranchService 등록
    gRPC->>gRPC: ContentsService 등록
    gRPC->>gRPC: MergeRequestService 등록
    gRPC->>gRPC: Reflection 활성화
    gRPC->>gRPC: Listen :50051

    Main->>REST: goroutine 2 시작
    REST->>REST: grpc-gateway 프록시 설정
    REST->>REST: Listen :8080

    Note over Main: SIGINT/SIGTERM 수신 시 graceful shutdown
```

---

## Provider Dispatch 패턴

모든 gRPC 서버 메서드는 동일한 구조로 Provider를 선택한다.

```
요청 수신
  └─ 입력 검증
       └─ ProviderConfig type switch
            ├─ *pb.ProviderConfig_Github → createGitHubClient()
            ├─ *pb.ProviderConfig_Gitlab → createGitLabClient()
            └─ *pb.ProviderConfig_Bitbucket → createBitbucketClient()
                  └─ Provider API 호출
                       └─ Proto 메시지 변환
                            └─ 응답 반환
```

이 패턴 덕분에 서버는 stateless를 유지한다. 인증 정보를 요청마다 전달받으므로 서버가 세션을 관리할 필요가 없다. 단점은 매 요청마다 클라이언트를 새로 생성하는 오버헤드가 있다는 점으로, 향후 커넥션 풀 또는 캐싱이 필요할 수 있다.

---

## 관련 문서

- [overview.md](overview.md) - 시스템 아키텍처 전체 개요
- [Provider/api-design.md](../Provider/api-design.md) - ProviderService API 설계
- [Repository/api-design.md](../Repository/api-design.md) - GitService Repository RPC
