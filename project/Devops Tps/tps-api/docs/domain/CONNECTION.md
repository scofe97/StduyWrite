# Connection 도메인

## 목표

**Connection**은 TPS 시스템과 외부 Git Provider(GitHub, GitLab, Bitbucket 등) 간의 **연결 정보를 관리**하는 도메인입니다.

### 핵심 목표

1. **멀티 프로바이더 지원**: 하나의 프로젝트에서 여러 Git Provider를 동시에 사용
2. **인증 정보 관리**: API 토큰, 접속 URL 등 보안 정보의 안전한 저장
3. **연결 상태 추적**: Provider와의 연결 상태를 실시간으로 관리
4. **멀티 인스턴스 지원**: 같은 Provider 타입의 여러 인스턴스 관리 (예: 사내 GitLab, 고객사 GitLab)

---

## 핵심 개념

### Connection이란?

Connection은 **Git Provider에 대한 연결 설정**입니다. 실제 저장소(Repository)가 아닌, 저장소에 접근하기 위한 **인증 및 접속 정보**를 담고 있습니다.

```
┌─────────────────────────────────────────────────────────────┐
│                        Project                               │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Connection  │  │  Connection  │  │  Connection  │       │
│  │   (GitHub)   │  │  (GitLab A)  │  │  (GitLab B)  │       │
│  │              │  │  사내 GitLab │  │  고객사 GitLab│       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         ▼                 ▼                 ▼                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Repository A │  │ Repository B │  │ Repository C │       │
│  │ Repository B │  │ Repository C │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Provider 타입

| Provider | base_url 예시 | 특징 |
|----------|---------------|------|
| **GITHUB** | `https://api.github.com` | GitHub.com 또는 GitHub Enterprise |
| **GITLAB** | `https://gitlab.example.com` | GitLab.com 또는 Self-hosted GitLab |
| **BITBUCKET** | `https://api.bitbucket.org` | Bitbucket Cloud 또는 Server |

---

## 엔티티 구조

### Connection Entity

```java
public class Connection {
    private UUID id;              // 고유 식별자 (UUID v7)
    private UUID projectId;       // 소속 프로젝트
    private ProviderType providerType;  // GITHUB, GITLAB, BITBUCKET
    private String name;          // 연결 이름 (예: "사내 GitLab")
    private String baseUrl;       // API 기본 URL
    private String apiToken;      // 인증 토큰 (암호화 저장)
    private ConnectionStatus status;    // 연결 상태
    private String metadata;      // 추가 설정 (JSON)
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

### 필드 상세

| 필드 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| `id` | UUID | 고유 식별자 | PK, Time-based UUID (v7) |
| `projectId` | UUID | 프로젝트 ID | FK, NOT NULL |
| `providerType` | Enum | Provider 종류 | NOT NULL |
| `name` | String | 표시 이름 | NOT NULL, 프로젝트 내 유일 |
| `baseUrl` | String | API 기본 URL | NOT NULL |
| `apiToken` | String | 인증 토큰 | NOT NULL, 암호화 저장 |
| `status` | Enum | 연결 상태 | NOT NULL, 기본값: PENDING |
| `metadata` | JSON | 추가 메타데이터 | NULLABLE |

### metadata 활용 예시

```json
{
  "organization": "my-org",
  "instanceName": "사내 GitLab 운영",
  "environment": "production",
  "rateLimit": {
    "requestsPerHour": 5000
  }
}
```

---

## 상태 다이어그램

```mermaid
stateDiagram-v2
    [*] --> PENDING: createConnection()

    PENDING --> TESTING: testConnection()
    note right of PENDING: 생성 직후 상태\n아직 검증되지 않음

    TESTING --> ACTIVE: 연결 테스트 성공
    TESTING --> FAILED: 연결 테스트 실패
    note right of TESTING: Git-API(Go)가\n실제 Provider에 요청

    ACTIVE --> INACTIVE: deactivate()
    ACTIVE --> TESTING: 재검증 필요 시
    note right of ACTIVE: 정상 운영 상태\nRepository 등록 가능

    INACTIVE --> ACTIVE: activate()
    note right of INACTIVE: 일시 비활성화\n수동 조작

    FAILED --> TESTING: 재시도
    note right of FAILED: 연결 실패\n토큰 만료 등
```

### 상태별 설명

| 상태 | 설명 | 허용 작업 |
|------|------|-----------|
| **PENDING** | 생성 직후, 아직 테스트되지 않음 | 테스트, 수정, 삭제 |
| **TESTING** | 연결 테스트 진행 중 | 대기 |
| **ACTIVE** | 정상 연결, 사용 가능 | 저장소 등록, 비활성화, 삭제 |
| **INACTIVE** | 수동으로 비활성화됨 | 활성화, 삭제 |
| **FAILED** | 연결 실패 (토큰 만료, 네트워크 오류 등) | 재시도, 수정, 삭제 |

---

## API 상세

### 1. 연결 생성

**`POST /v1/connections`**

새로운 Git Provider 연결을 생성합니다. 생성 후 상태는 `PENDING`입니다.

#### 목적
- 프로젝트에 새로운 Git Provider 연결 추가
- 여러 Provider 또는 동일 Provider의 다중 인스턴스 관리

#### 요청

```json
{
  "projectId": "550e8400-e29b-41d4-a716-446655440000",
  "providerType": "GITLAB",
  "name": "사내 GitLab",
  "baseUrl": "https://gitlab.company.com/api/v4",
  "apiToken": "glpat-xxxxxxxxxxxxxxxxxxxx",
  "metadata": "{\"organization\": \"devops-team\"}"
}
```

#### 응답

```json
{
  "success": true,
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "projectId": "550e8400-e29b-41d4-a716-446655440000",
    "providerType": "GITLAB",
    "name": "사내 GitLab",
    "baseUrl": "https://gitlab.company.com/api/v4",
    "status": "PENDING",
    "createdAt": "2025-01-05T10:00:00"
  }
}
```

#### 사용 시나리오
- 프로젝트 초기 설정 시 Git Provider 연결
- 기존 프로젝트에 새로운 Git 인스턴스 추가

---

### 2. 연결 테스트

**`POST /v1/connections/{id}/test`**

Git Provider에 실제로 연결하여 토큰 유효성을 검증합니다.

#### 목적
- API 토큰의 유효성 확인
- Provider 접속 가능 여부 확인
- 권한 범위(scope) 확인

#### 처리 흐름

```mermaid
sequenceDiagram
    participant Client
    participant TPS as TPS-API (Java)
    participant Kafka
    participant GitAPI as Git-API (Go)
    participant Provider as Git Provider

    Client->>TPS: POST /connections/{id}/test
    TPS->>TPS: status = TESTING
    TPS->>Kafka: TEST_CONNECTION 메시지 발행
    TPS-->>Client: 202 Accepted

    Kafka->>GitAPI: 메시지 수신
    GitAPI->>Provider: GET /user (토큰 검증)

    alt 성공
        Provider-->>GitAPI: 200 OK + User Info
        GitAPI->>Kafka: TEST_RESULT (success=true)
        Kafka->>TPS: 결과 수신
        TPS->>TPS: status = ACTIVE
    else 실패
        Provider-->>GitAPI: 401 Unauthorized
        GitAPI->>Kafka: TEST_RESULT (success=false)
        Kafka->>TPS: 결과 수신
        TPS->>TPS: status = FAILED
    end
```

#### 응답

```json
{
  "success": true,
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "TESTING",
    "message": "연결 테스트가 시작되었습니다. 잠시 후 상태를 확인해주세요."
  }
}
```

#### 사용 시나리오
- 연결 생성 직후 유효성 검증
- 토큰 갱신 후 재검증
- 정기적인 연결 상태 확인

---

### 3. 연결 조회

**`GET /v1/connections/{id}`**

특정 연결의 상세 정보를 조회합니다.

#### 목적
- 연결 상태 확인
- 설정 정보 조회 (토큰 제외)

#### 응답

```json
{
  "success": true,
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "projectId": "550e8400-e29b-41d4-a716-446655440000",
    "providerType": "GITLAB",
    "name": "사내 GitLab",
    "baseUrl": "https://gitlab.company.com/api/v4",
    "status": "ACTIVE",
    "metadata": "{\"organization\": \"devops-team\"}",
    "createdAt": "2025-01-05T10:00:00",
    "updatedAt": "2025-01-05T10:05:00"
  }
}
```

> **주의**: `apiToken`은 보안상 응답에 포함되지 않습니다.

---

### 4. 프로젝트별 연결 목록

**`GET /v1/connections/project/{projectId}`**

프로젝트에 등록된 모든 연결을 조회합니다.

#### 목적
- 프로젝트 설정 화면에서 연결 목록 표시
- 저장소 등록 시 사용 가능한 연결 목록 조회

#### 응답

```json
{
  "success": true,
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "providerType": "GITLAB",
      "name": "사내 GitLab",
      "status": "ACTIVE"
    },
    {
      "id": "223e4567-e89b-12d3-a456-426614174001",
      "providerType": "GITHUB",
      "name": "GitHub Enterprise",
      "status": "ACTIVE"
    }
  ]
}
```

---

### 5. Provider 타입별 연결 목록

**`GET /v1/connections/provider/{providerType}`**

특정 Provider 타입의 모든 연결을 조회합니다.

#### 목적
- 시스템 관리자가 특정 Provider 연결 현황 파악
- Provider 장애 시 영향받는 연결 확인

#### 사용 예시
```
GET /v1/connections/provider/GITLAB
```

---

### 6. 활성 연결 목록

**`GET /v1/connections/active`**

`ACTIVE` 상태인 모든 연결을 조회합니다.

#### 목적
- 저장소 등록 시 선택 가능한 연결만 표시
- 시스템 헬스 체크

---

### 7. 연결 수정

**`PUT /v1/connections/{id}`**

연결 정보를 수정합니다.

#### 목적
- API 토큰 갱신
- 연결 이름 변경
- 메타데이터 업데이트

#### 요청

```json
{
  "name": "사내 GitLab (운영)",
  "apiToken": "glpat-newtoken",
  "metadata": "{\"organization\": \"platform-team\"}"
}
```

> **주의**: 토큰 변경 후에는 `testConnection()`을 호출하여 재검증이 필요합니다.

---

### 8. 연결 활성화/비활성화

**`POST /v1/connections/{id}/activate`**
**`POST /v1/connections/{id}/deactivate`**

연결을 수동으로 활성화하거나 비활성화합니다.

#### 목적
- 임시 점검 시 연결 비활성화
- 비활성 연결 재활성화

#### 비활성화 시 동작
- 해당 Connection으로 등록된 Repository의 동기화 중단
- 새로운 Repository 등록 불가

---

### 9. 연결 삭제

**`DELETE /v1/connections/{id}`**

연결을 삭제합니다.

#### 목적
- 더 이상 사용하지 않는 연결 제거
- 프로젝트 정리

#### 주의사항
- **CASCADE 삭제**: 해당 Connection으로 등록된 모든 Repository도 함께 삭제됩니다.
- 삭제 전 영향받는 Repository 목록을 확인하세요.

```mermaid
flowchart LR
    A[Connection 삭제] --> B[Repository 1 삭제]
    A --> C[Repository 2 삭제]
    B --> D[Branch 1-1 삭제]
    B --> E[Branch 1-2 삭제]
    C --> F[Branch 2-1 삭제]
```

---

## 다른 도메인과의 관계

### Connection → Repository

```
Connection (1) ────────── (N) Repository
     │                          │
     │ provides                 │
     │                          │
     └── baseUrl + apiToken ────┘
         으로 저장소 접근
```

- 하나의 Connection에 여러 Repository를 등록할 수 있음
- Repository는 Connection의 인증 정보를 사용하여 Git 작업 수행

### Connection과 Project

```
Project (1) ────────── (N) Connection
     │                       │
     │ has                   │
     │                       │
     └── 프로젝트별로 ────────┘
         연결 관리
```

- 프로젝트는 여러 Connection을 가질 수 있음
- 같은 Provider 타입의 Connection도 여러 개 가능 (멀티 인스턴스)

---

## 사용 시나리오

### 시나리오 1: 프로젝트 초기 설정

```
1. 프로젝트 생성
2. GitHub Connection 생성 (회사 공식 GitHub)
3. GitLab Connection 생성 (사내 GitLab)
4. 각 Connection 테스트 → ACTIVE 상태 확인
5. 각 Connection에 저장소 등록
```

### 시나리오 2: 토큰 만료 대응

```
1. Connection 상태가 FAILED로 변경됨 (Git-API가 감지)
2. 관리자에게 알림 발송
3. 새로운 토큰 발급
4. PUT /connections/{id} 로 토큰 갱신
5. POST /connections/{id}/test 로 재검증
6. 상태가 ACTIVE로 복구됨
```

### 시나리오 3: 멀티 인스턴스 관리

```
회사 A: GitLab (https://gitlab.company-a.com)
회사 B: GitLab (https://gitlab.company-b.com)
회사 C: GitHub Enterprise (https://github.company-c.com)

→ 3개의 Connection 생성, 각각 다른 baseUrl과 apiToken
→ 프로젝트에서 3개의 Provider 동시 사용 가능
```

---

## 보안 고려사항

### API 토큰 보안

1. **암호화 저장**: `apiToken`은 DB에 암호화되어 저장
2. **응답 제외**: API 응답에 `apiToken` 포함하지 않음
3. **최소 권한 원칙**: 필요한 scope만 가진 토큰 사용 권장

### 권장 토큰 Scope

| Provider | 필요 Scope |
|----------|-----------|
| GitHub | `repo`, `read:org` |
| GitLab | `api`, `read_repository` |
| Bitbucket | `repository`, `pullrequest` |

---

## 관련 문서

- [Repository 도메인](./REPOSITORY.md)
- [Branch 도메인](./BRANCH.md)
- [아키텍처 개요](../ARCHITECTURE.md)
