# Merge API - 병합 요청 관리

GitLab Merge Request(MR) 관리를 위한 API입니다.

## 목적

TPS 티켓 기반 코드 변경을 시스템 브랜치(dev → stg → prd)로 순차 병합하여 배포 파이프라인을 자동화합니다.

| 핵심 기능 | 설명 |
|----------|------|
| **티켓 기반 MR** | 티켓 번호로 소스 브랜치 자동 매핑 |
| **다중 타겟 지원** | 하나의 요청으로 dev/stg/prd 동시 MR 생성 |
| **충돌 관리** | 충돌 감지 및 Rebase 지원 |
| **Squash Merge** | 커밋 압축 병합으로 히스토리 정리 |

## 시퀀스 다이어그램

### 병합 요청 생성

```mermaid
sequenceDiagram
    participant Workflow as Workflow Engine
    participant Controller as MergeControllerV2
    participant Service as MergeServiceV2
    participant GitLab as GitLab API
    participant DB as TPS DB

    Workflow->>Controller: POST /code_merge/v2/merge_requests
    Note right of Workflow: ticketNo, targetBranchs[]
    Controller->>Service: createMergeRequest(request)
    Service->>DB: ticketNo로 소스 브랜치 조회
    DB-->>Service: sourceBranch
    loop 각 타겟 브랜치별
        Service->>GitLab: POST /api/v4/projects/{id}/merge_requests
        GitLab-->>Service: MR Created
        Service->>DB: MR 이력 저장
    end
    Service-->>Controller: List<MergeRequestResponse>
    Controller-->>Workflow: 201 Created
```

### 병합 승인

```mermaid
sequenceDiagram
    participant Approver
    participant Service as MergeServiceV2
    participant GitLab as GitLab API

    Approver->>Service: approve(request)
    Service->>GitLab: GET /api/v4/projects/{id}/merge_requests/{iid}
    GitLab-->>Service: MR 상세 (hasConflicts)
    alt 충돌 없음
        Service->>GitLab: PUT /merge_requests/{iid}/merge
        GitLab-->>Service: Merged
    else 충돌 있음
        Service-->>Approver: 409 Conflict
    end
```

## 호출하는 GitLab API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/v4/projects/{id}/merge_requests` | 병합 요청 목록 |
| POST | `/api/v4/projects/{id}/merge_requests` | 병합 요청 생성 |
| PUT | `/api/v4/projects/{id}/merge_requests/{iid}/merge` | 병합 승인/실행 |
| DELETE | `/api/v4/projects/{id}/merge_requests/{iid}` | 병합 요청 삭제 |

## 제공하는 외부 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/code_merge/v2/merge_requests` | 병합 요청 목록 조회 |
| POST | `/code_merge/v2/merge_requests` | 병합 요청 생성 |
| POST | `/code_merge/v2/merge_requests/approve` | 병합 승인 |
| POST | `/code_merge/v2/merge_requests/revert` | 병합 취소 |

## Merge Status

| 상태 | 설명 |
|------|------|
| `can_be_merged` | 머지 가능 |
| `cannot_be_merged` | 충돌 있음 |
| `checking` | 확인 중 |
