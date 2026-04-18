# Project API - 프로젝트/저장소 관리

GitLab 프로젝트(저장소) 관리를 위한 API입니다.

## 목적

TPS 업무관리코드(bizMngCd)와 GitLab 프로젝트를 매핑하여 소스 코드 저장소를 체계적으로 관리합니다.

| 핵심 기능 | 설명 |
|----------|------|
| **저장소 생성** | 업무별 Git 저장소 자동 생성 및 초기화 |
| **멤버 관리** | 프로젝트별 개발자 권한 부여 |
| **업무코드 매핑** | bizMngCd 기반 프로젝트 식별 및 조회 |
| **가시성 제어** | private/internal/public 접근 수준 설정 |

## 시퀀스 다이어그램

### 프로젝트 생성

```mermaid
sequenceDiagram
    participant Client
    participant Controller as ProjectControllerV2
    participant Service as GitLabProjectServiceV2
    participant GitLab as GitLab API
    participant DB as TPS DB

    Client->>Controller: POST /gitlab/v2/create_project
    Note right of Client: name, groupId, visibility
    Controller->>Service: create(request)
    Service->>GitLab: POST /api/v4/projects
    Note right of Service: namespace_id, default_branch=prd
    GitLab-->>Service: Project Created (id, path)
    Service->>DB: bizMngCd 매핑 저장
    DB-->>Service: 저장 완료
    Service-->>Controller: ProjectResponse
    Controller-->>Client: 201 Created
```

### 프로젝트 멤버 다건 수정

```mermaid
sequenceDiagram
    participant Client
    participant Controller as ProjectControllerV2
    participant Service as GitLabProjectServiceV2
    participant GitLab as GitLab API

    Client->>Controller: POST /gitlab/v2/update_project/users
    Note right of Client: projectId, members[]
    Controller->>Service: updateMembers(request)
    loop 각 멤버별
        alt 새 멤버
            Service->>GitLab: POST /api/v4/projects/{id}/members
        else 기존 멤버
            Service->>GitLab: PUT /api/v4/projects/{id}/members/{userId}
        end
        GitLab-->>Service: Updated
    end
    Service-->>Controller: 수정 완료
    Controller-->>Client: 200 OK
```

### 업무코드별 프로젝트 조회

```mermaid
sequenceDiagram
    participant Client
    participant Controller as ProjectControllerV2
    participant Service as GitLabProjectServiceV2
    participant DB as TPS DB
    participant GitLab as GitLab API

    Client->>Controller: GET /gitlab/v2/taskCd/{taskCd}/projects
    Controller->>Service: getByTaskCd(taskCd)
    Service->>DB: taskCd로 bizMngCd 목록 조회
    DB-->>Service: bizMngCd 목록
    loop 각 bizMngCd별
        Service->>GitLab: GET /api/v4/projects/{id}
        GitLab-->>Service: Project 상세
    end
    Service-->>Controller: List<ProjectResponse>
    Controller-->>Client: 200 OK
```

## 호출하는 GitLab API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/v4/projects` | 전체 프로젝트 조회 |
| GET | `/api/v4/projects/{id}` | 프로젝트 조회 |
| POST | `/api/v4/projects` | 프로젝트 생성 |
| PUT | `/api/v4/projects/{id}` | 프로젝트 수정 |
| DELETE | `/api/v4/projects/{id}` | 프로젝트 삭제 |
| GET | `/api/v4/projects/{id}/users` | 프로젝트 사용자 조회 |
| POST | `/api/v4/projects/{id}/members` | 프로젝트 멤버 추가 |
| PUT | `/api/v4/projects/{id}/members` | 프로젝트 멤버 수정 |
| DELETE | `/api/v4/projects/{id}/members/{userId}` | 프로젝트 멤버 삭제 |

## 제공하는 외부 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/gitlab/v2/select_project` | 프로젝트 페이지네이션 조회 |
| GET | `/gitlab/v2/taskCd/{taskCd}/projects` | 업무코드별 프로젝트 조회 |
| POST | `/gitlab/v2/create_project` | 프로젝트 생성 |
| POST | `/gitlab/v2/update_project` | 프로젝트 수정 |
| POST | `/gitlab/v2/delete_projects` | 프로젝트 삭제 |
| GET | `/gitlab/v2/select_project/{bizMngCd}/user` | 프로젝트 사용자 목록 |
| POST | `/gitlab/v2/create_project/user` | 프로젝트 사용자 추가 |
| POST | `/gitlab/v2/update_project/users` | 프로젝트 사용자 다건 수정 |

## 주요 DTO

### Request

```java
// 프로젝트 생성 요청
public class ProjectCreateRequest {
    String name;
    String path;
    Long namespaceId;       // 그룹 ID
    String visibility;      // private, internal, public
    String description;
    Boolean initializeWithReadme;
    String defaultBranch;
}

// 프로젝트 조회 요청
public class ProjectSearchRequest {
    String taskCd;
    String projectName;
    Integer page;
    Integer perPage;
}

// 프로젝트 멤버 추가
public class ProjectMemberAddRequest {
    Long projectId;
    List<Long> userIds;
    Integer accessLevel;
}

// 프로젝트 멤버 다건 수정
public class ProjectMemberBulkUpdateRequest {
    Long projectId;
    List<MemberUpdate> members;
}
```

### Response

```java
// 프로젝트 조회 응답
public class ProjectResponse {
    Long id;
    String name;
    String path;
    String pathWithNamespace;
    String defaultBranch;
    String visibility;
    String webUrl;
    String sshUrlToRepo;
    String httpUrlToRepo;
    Long namespaceId;
    String namespaceName;
}

// 프로젝트 사용자 응답
public class ProjectUserResponse {
    Long userId;
    String username;
    String name;
    Integer accessLevel;
    String accessLevelName;
}
```

## 프로젝트 Visibility

| 값 | 설명 |
|----|------|
| `private` | 멤버만 접근 가능 |
| `internal` | 로그인 사용자 접근 가능 |
| `public` | 누구나 접근 가능 |

## 참고사항

- 프로젝트는 TPS 업무관리코드(bizMngCd)와 매핑됨
- 프로젝트 생성 시 기본 브랜치는 `prd`로 설정
- 삭제 시 연관된 모든 데이터(브랜치, MR 등)도 함께 삭제됨
- 업무코드(taskCd) 기반으로 프로젝트 그룹핑 가능
