# MergeRequest 구현 리뷰

## What - 무엇을 구현했는가

`mr_server.go` (1,007줄)에 MergeRequestService의 12개 RPC를 구현했다. 4개 서비스 중 가장 크다. MR CRUD 6개, Review 2개, Comment 4개로 구성된다.

| 그룹 | RPC | 설명 |
|------|-----|------|
| MR CRUD | ListMergeRequests | 상태 필터, 페이지네이션 지원 |
| MR CRUD | GetMergeRequest | number로 MR 식별 |
| MR CRUD | CreateMergeRequest | title, source/target branch, draft 지원 |
| MR CRUD | UpdateMergeRequest | title, description, state, target branch 수정 |
| MR CRUD | MergeMergeRequest | merge method, commit message, 소스 브랜치 삭제 |
| MR CRUD | GetMergeRequestDiff | 파일별 additions/deletions/patch |
| Review | ListReviews | Bitbucket은 빈 배열 반환 |
| Review | SubmitReview | APPROVED, CHANGES_REQUESTED, COMMENTED |
| Comment | ListComments | 전체 댓글 목록 |
| Comment | CreateComment | path+line으로 인라인 댓글 (GitHub/GitLab만) |
| Comment | UpdateComment | commentId로 식별하여 수정 |
| Comment | DeleteComment | commentId로 식별하여 삭제 |

---

## How - 어떻게 구현했는가

### 변환 계층

MergeRequestService는 4개 서비스 중 가장 풍부한 변환 함수 세트를 가진다. client 공통 타입에서 proto 메시지로의 변환을 전담하는 함수들이 mr_server.go 내에 존재한다.

```go
// 타입 변환 함수
convertMergeRequest(client.MergeRequestInfo) → pb.MergeRequest     // 필드 15개+
convertUser(client.UserInfo)                 → pb.User             // 5개 필드
convertReview(client.ReviewInfo)             → pb.Review           // 4개 필드
convertComment(client.CommentInfo)           → pb.Comment          // 8개 필드
convertMergeRequestDiff(client.MRDiffInfo)   → pb.MergeRequestDiff // 4개 필드
convertFileDiff(client.FileDiffInfo)         → pb.FileDiff         // 6개 필드

// enum 변환 함수
convertMRStateToString(pb.MergeRequestState) → string
convertStringToMRState(string)               → pb.MergeRequestState
convertMergeMethodToString(pb.MergeMethod)   → string
convertReviewStateToString(pb.ReviewState)   → string
convertStringToReviewState(string)           → pb.ReviewState
```

### Draft MR 처리

Draft는 Provider마다 구현 방식이 달라서 서버에서 변환을 수행한다.

```go
// CreateMergeRequest 내부
switch provider {
case GitHub:
    opts.Draft = req.Draft
case GitLab:
    if req.Draft {
        req.Title = "Draft: " + req.Title
    }
case Bitbucket:
    // Draft 미지원, 무시하고 OPEN으로 생성
}
```

UpdateMergeRequest에서 `draft=false`로 전환할 때는 GitLab의 경우 타이틀에서 `"Draft: "` 접두사를 제거하는 방식으로 처리한다.

### Review 시스템 통합

세 Provider의 리뷰 시스템이 근본적으로 다르다. SubmitReview는 ReviewState에 따라 Provider별로 다른 API를 호출한다.

```go
// SubmitReview 내부 (Bitbucket 예시)
switch req.State {
case APPROVED:
    client.Approve(mrNumber)  // Approve API 직접 호출
default:
    client.CreateComment(body)  // 댓글로 대체
}
```

Bitbucket의 `ListReviews`는 API 자체가 없으므로 항상 빈 슬라이스를 반환하고 에러를 발생시키지 않는다. 클라이언트가 빈 배열을 받아도 정상 처리할 수 있도록 설계했다.

### Comment 시스템

인라인 댓글(path+line)은 GitHub와 GitLab만 지원한다. Bitbucket은 인라인 댓글 요청이 들어오면 path/line 필드를 무시하고 일반 댓글로 대체한다.

Bitbucket의 UpdateComment와 DeleteComment는 go-bitbucket 라이브러리 v0.9.88부터 `PullRequests.UpdateComment()`와 `PullRequests.DeleteComment()` 메서드가 추가되어 구현이 완료되었다. 이전 버전에서는 미구현 상태로 에러를 반환했다.

### 서비스 등록 버그 수정

MergeRequestService는 구현이 완료되어 있었지만 `cmd/server/main.go`에서 등록되지 않아 404가 반환되는 버그가 있었다. 다음 코드를 추가하여 수정했다.

```go
mrServer := server.NewMergeRequestServer()
pb.RegisterMergeRequestServiceServer(grpcServer, mrServer)
pb.RegisterMergeRequestServiceHandlerFromEndpoint(ctx, mux, grpcEndpoint, opts)
```

---

## Why - 왜 이렇게 구현했는가

### 서비스가 가장 큰 이유

MR은 단순 CRUD가 아닌 협업 워크플로우 전체를 담는다. 리뷰 시스템과 댓글 시스템이 MR과 강하게 결합되어 있고, Provider별 차이도 가장 크다. GitHub의 Review 이벤트 방식, GitLab의 Approval 방식, Bitbucket의 단순 Approve 방식을 통합 인터페이스로 추상화하는 코드가 필연적으로 많아진다.

### Bitbucket ListReviews를 에러 없이 빈 배열로 반환하는 이유

Bitbucket에 정식 Review API가 없다는 것은 기능 부재이지 오류가 아니다. 에러를 반환하면 클라이언트가 Bitbucket 연결에서는 리뷰 탭 자체를 표시하지 못하게 된다. 빈 배열을 반환하면 클라이언트가 "리뷰 없음"으로 처리할 수 있어, Provider에 관계없이 동일한 UI 흐름을 유지할 수 있다.

### enum 변환 함수를 별도로 분리한 이유

MR 상태(OPEN/CLOSED/MERGED/DRAFT)와 ReviewState(APPROVED/CHANGES_REQUESTED 등)는 Provider마다 문자열 표현이 다르다. GitHub는 `"open"/"closed"`, GitLab은 `"opened"/"closed"`, Bitbucket은 `"OPEN"/"DECLINED"`처럼 제각각이다. enum 변환 함수를 한 곳에 모아두면 새 Provider 추가 시 변환 로직을 한 곳만 수정하면 된다.

---

## 참고 패턴

| 패턴 | 적용 위치 | 설명 |
|------|-----------|------|
| Provider별 Draft 변환 | CreateMergeRequest | GitHub 필드, GitLab 타이틀 접두사, Bitbucket 무시 |
| Graceful degradation | ListReviews (Bitbucket) | 미지원 기능은 에러 대신 빈 배열 반환 |
| Fallback to comment | SubmitReview | CHANGES_REQUESTED 미지원 시 댓글로 대체 |
| enum 변환 함수 집중화 | mr_server.go 하단 | 상태 문자열 ↔ proto enum 양방향 변환 |
| 풍부한 변환 계층 | convertMergeRequest 등 | 6개 타입, 10개 enum 변환 함수 |

---

## 개선 가능 사항

1. **MR 이벤트 히스토리**: 상태 변경 이력을 조회하는 타임라인 API가 있으면 MR 진행 상황 추적이 용이하다.
2. **CI/CD 상태 연동**: MR의 파이프라인 빌드 결과(pass/fail)를 GetMergeRequest 응답에 함께 반환하면 UI에서 머지 가능 여부를 더 정확하게 판단할 수 있다.
3. **리뷰어 자동 할당**: CODEOWNERS 파일 기반으로 변경 파일에 맞는 리뷰어를 자동 추천하는 기능이 있으면 리뷰 요청 과정이 단순해진다.
4. **Batch 댓글**: 여러 인라인 댓글을 하나의 리뷰로 묶어서 제출하는 API (GitHub의 Pull Request Review 방식)가 있으면 리뷰 알림 수를 줄일 수 있다.
5. **Webhook 연동**: MR 상태 변경 시 외부 알림을 보내는 기능은 향후 WebhookService와 연계하여 구현할 예정이다.
