# Devops TPS 프로젝트 문서

git-provider 서비스의 전체 문서 인덱스다. 도메인별로 API 설계, 유스케이스 모델, 구현 리뷰, 테스트 시나리오 4개 문서로 구성된다.

---

## 전체 아키텍처

| 문서 | 설명 |
|------|------|
| [Architecture/overview.md](Architecture/overview.md) | 시스템 아키텍처 전체 개요 |

---

## 도메인별 문서

### Provider (Git 프로바이더 관리)

GitHub, GitLab, Bitbucket 연결 설정을 관리하는 도메인이다.

| 문서 | 설명 |
|------|------|
| [Provider/api-design.md](Provider/api-design.md) | ProviderService RPC 목록 및 요청/응답 |
| [Provider/usecase-model.md](Provider/usecase-model.md) | 유스케이스 + 도메인 모델 |
| [Provider/review.md](Provider/review.md) | 구현 리뷰 (What/How/Why) |
| [Provider/test.md](Provider/test.md) | 테스트 시나리오 |
| [Provider/GitHub/api-reference.md](Provider/GitHub/api-reference.md) | GitHub API 참조 |
| [Provider/GitLab/api-reference.md](Provider/GitLab/api-reference.md) | GitLab API 참조 |
| [Provider/Bitbucket/api-reference.md](Provider/Bitbucket/api-reference.md) | Bitbucket API 참조 |

---

### Repository (저장소 관리)

Git 저장소 CRUD와 정보 조회를 담당하는 도메인이다.

| 문서 | 설명 |
|------|------|
| [Repository/api-design.md](Repository/api-design.md) | RepositoryService RPC 목록 및 요청/응답 |
| [Repository/usecase-model.md](Repository/usecase-model.md) | 유스케이스 + 도메인 모델 |
| [Repository/review.md](Repository/review.md) | 구현 리뷰 (What/How/Why) |
| [Repository/test.md](Repository/test.md) | 테스트 시나리오 |

---

### Branch (브랜치 운영)

브랜치 생성·삭제·보호 규칙 관리와 오래된 브랜치 정리를 담당하는 도메인이다.

| 문서 | 설명 |
|------|------|
| [Branch/api-design.md](Branch/api-design.md) | BranchService RPC 목록 및 요청/응답 |
| [Branch/usecase-model.md](Branch/usecase-model.md) | 유스케이스 + 도메인 모델 |
| [Branch/review.md](Branch/review.md) | 구현 리뷰 (What/How/Why) |
| [Branch/test.md](Branch/test.md) | 테스트 시나리오 |

---

### Contents (코드 브라우징)

저장소 내 파일 트리 탐색과 파일 내용 조회를 담당하는 도메인이다.

| 문서 | 설명 |
|------|------|
| [Contents/api-design.md](Contents/api-design.md) | ContentsService RPC 목록 및 요청/응답 |
| [Contents/usecase-model.md](Contents/usecase-model.md) | 유스케이스 + 도메인 모델 |
| [Contents/review.md](Contents/review.md) | 구현 리뷰 (What/How/Why) |
| [Contents/test.md](Contents/test.md) | 테스트 시나리오 |

---

### MergeRequest (PR/MR 관리)

Pull Request / Merge Request 생성, 조회, 리뷰, 머지를 담당하는 도메인이다.

| 문서 | 설명 |
|------|------|
| [MergeRequest/api-design.md](MergeRequest/api-design.md) | MergeRequestService RPC 목록 및 요청/응답 |
| [MergeRequest/usecase-model.md](MergeRequest/usecase-model.md) | 유스케이스 + 도메인 모델 |
| [MergeRequest/review.md](MergeRequest/review.md) | 구현 리뷰 (What/How/Why) |
| [MergeRequest/test.md](MergeRequest/test.md) | 테스트 시나리오 |

---

### CICD (CI/CD 파이프라인)

Jenkins를 추상화하여 파이프라인 CRUD와 빌드 관리를 담당하는 도메인이다. `cicd.proto`의 8개 RPC로 구성된다.

| 문서 | 설명 |
|------|------|
| [CICD/api-design.md](CICD/api-design.md) | CICDService 8개 RPC 및 요청/응답 |
| [CICD/usecase-model.md](CICD/usecase-model.md) | 유스케이스 + BuildStatus 생애주기 |
| [CICD/review.md](CICD/review.md) | 구현 리뷰 (What/How/Why) |
| [CICD/test.md](CICD/test.md) | 테스트 시나리오 (curl 예시 포함) |
| [CICD/Jenkins/api-reference.md](CICD/Jenkins/api-reference.md) | Jenkins API 통합 참조 (파이프라인/자격증명/폴더/노드) |

---

### Workflow (워크플로우 오케스트레이션)

Git 이벤트를 받아 CI/CD 파이프라인을 자동 실행하는 E2E 오케스트레이터 도메인이다. `workflow.proto`의 6개 RPC로 구성된다.

| 문서 | 설명 |
|------|------|
| [Workflow/api-design.md](Workflow/api-design.md) | WorkflowService 6개 RPC 및 E2E 아키텍처 다이어그램 |
| [Workflow/usecase-model.md](Workflow/usecase-model.md) | 유스케이스 + ExecutionStatus 생애주기 |
| [Workflow/review.md](Workflow/review.md) | E2E 구현 리뷰 (webhook → Kafka → Jenkins → 결과) |
| [Workflow/test.md](Workflow/test.md) | E2E 테스트 시나리오 (webhook 시뮬레이션 포함) |

---

## 컨벤션

| 문서 | 설명 |
|------|------|
| [Conventions/java21-coding-standards.md](Conventions/java21-coding-standards.md) | Java 21 코딩 표준 |

---

## TPS 프로젝트 분석

기존 TPS 시스템의 API를 분석하여 git-provider 설계에 참조한 문서들이다.

### GitLab API 분석

| 문서 | 설명 |
|------|------|
| [TPS/tech/gitlab/01-user-api.md](TPS/tech/gitlab/01-user-api.md) | GitLab 사용자 API |
| [TPS/tech/gitlab/02-group-api.md](TPS/tech/gitlab/02-group-api.md) | GitLab 그룹 API |
| [TPS/tech/gitlab/03-project-api.md](TPS/tech/gitlab/03-project-api.md) | GitLab 프로젝트 API |
| [TPS/tech/gitlab/04-branch-api.md](TPS/tech/gitlab/04-branch-api.md) | GitLab 브랜치 API |
| [TPS/tech/gitlab/05-merge-api.md](TPS/tech/gitlab/05-merge-api.md) | GitLab MR API |
| [TPS/tech/gitlab/06-repository-api.md](TPS/tech/gitlab/06-repository-api.md) | GitLab 저장소 API |
| [TPS/tech/gitlab/07-changes-api.md](TPS/tech/gitlab/07-changes-api.md) | GitLab 변경 내역 API |
| [TPS/tech/gitlab/08-clone-api.md](TPS/tech/gitlab/08-clone-api.md) | GitLab Clone API |

### Pipeline API 분석

| 문서 | 설명 |
|------|------|
| [TPS/tech/pipeline-api/01-user-api.md](TPS/tech/pipeline-api/01-user-api.md) | Pipeline 사용자 API |
| [TPS/tech/pipeline-api/02-group-api.md](TPS/tech/pipeline-api/02-group-api.md) | Pipeline 그룹 API |
| [TPS/tech/pipeline-api/03-project-api.md](TPS/tech/pipeline-api/03-project-api.md) | Pipeline 프로젝트 API |
| [TPS/tech/pipeline-api/04-branch-api.md](TPS/tech/pipeline-api/04-branch-api.md) | Pipeline 브랜치 API |
| [TPS/tech/pipeline-api/05-merge-api.md](TPS/tech/pipeline-api/05-merge-api.md) | Pipeline MR API |
| [TPS/tech/pipeline-api/06-repository-api.md](TPS/tech/pipeline-api/06-repository-api.md) | Pipeline 저장소 API |
| [TPS/tech/pipeline-api/07-changes-api.md](TPS/tech/pipeline-api/07-changes-api.md) | Pipeline 변경 내역 API |
| [TPS/tech/pipeline-api/08-clone-api.md](TPS/tech/pipeline-api/08-clone-api.md) | Pipeline Clone API |

### Jenkins API 분석

Jenkins API는 [CICD/Jenkins/api-reference.md](CICD/Jenkins/api-reference.md)로 통합되었다. 원본 분석 문서는 아래에서 확인할 수 있다.

| 문서 | 설명 |
|------|------|
| [TPS/tech/jenkins/01-pipeline-api.md](TPS/tech/jenkins/01-pipeline-api.md) | Jenkins 파이프라인 API 원본 |
| [TPS/tech/jenkins/02-credential-api.md](TPS/tech/jenkins/02-credential-api.md) | Jenkins 자격증명 API 원본 |
| [TPS/tech/jenkins/03-folder-api.md](TPS/tech/jenkins/03-folder-api.md) | Jenkins 폴더 API 원본 |
| [TPS/tech/jenkins/04-node-api.md](TPS/tech/jenkins/04-node-api.md) | Jenkins 노드 API 원본 |

---

## 문서 구조 패턴

각 도메인 문서는 동일한 4개 파일로 구성된다.

| 파일 | 내용 | 주요 섹션 |
|------|------|----------|
| `api-design.md` | proto 메시지 타입, RPC 목록, 요청/응답 테이블 | 메시지 타입, RPC별 상세, Mermaid 시퀀스 다이어그램 |
| `usecase-model.md` | 액터, 유스케이스, 상태 다이어그램, 도메인 모델 | 유스케이스 흐름, stateDiagram-v2 |
| `review.md` | What/How/Why 구조의 구현 리뷰 | 코드 스니펫, 설계 근거, 패턴, 한계 |
| `test.md` | curl/grpcurl 기반 테스트 시나리오 | 정상 케이스, 엣지 케이스, 요약 테이블 |
