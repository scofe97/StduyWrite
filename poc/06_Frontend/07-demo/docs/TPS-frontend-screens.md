# TPS 프론트엔드 화면 데이터 구조

TPS(Runners-High) 플랫폼의 프론트엔드 화면 및 데이터 구조를 정리한 문서입니다.

---

## 📌 화면 구성 개요

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            TPS 프론트엔드 화면 구조                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  Dashboard  │    │   Project   │    │   Ticket    │    │   Branch    │  │
│  │  (역할별)    │    │   관리      │    │    관리     │    │    관리     │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │ MergeRequest│    │    Build    │    │ Deployment  │    │  Workflow   │  │
│  │    관리     │    │    관리     │    │    관리     │    │   에디터    │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │  Approval   │    │   알림/설정  │    │   관리자    │                     │
│  │    결재     │    │             │    │   페이지    │                     │
│  └─────────────┘    └─────────────┘    └─────────────┘                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. 대시보드 (Dashboard)

### 1.1 역할별 대시보드 뷰

#### 개발자 대시보드

```typescript
interface DeveloperDashboard {
  // 내 브랜치
  myBranches: {
    id: string;
    name: string;
    ahead: number;        // main 대비 앞선 커밋 수
    behind: number;       // main 대비 뒤쳐진 커밋 수
    status: 'READY' | 'NEEDS_REBASE' | 'CONFLICT';
    linkedMR?: string;    // 연결된 MR 번호
    lastCommit: Date;
  }[];

  // 내 MR 목록
  myMergeRequests: {
    id: string;
    number: number;
    title: string;
    status: MergeRequestStatus;
    reviewProgress: {
      approved: number;
      required: number;
    };
    createdAt: Date;
  }[];

  // 리뷰 요청받은 MR
  reviewRequests: {
    id: string;
    number: number;
    title: string;
    author: UserSummary;
    additions: number;
    deletions: number;
    createdAt: Date;
  }[];

  // 최근 빌드
  recentBuilds: {
    id: string;
    buildNumber: number;
    repositoryName: string;
    branch: string;
    status: BuildStatus;
    duration: number;     // 초 단위
    finishedAt: Date;
  }[];
}
```

#### PM/기획자 대시보드

```typescript
interface PMDashboard {
  // 승인 대기 목록 (최우선 표시)
  pendingApprovals: {
    id: string;
    type: 'DEPLOYMENT' | 'RELEASE' | 'MERGE_REQUEST';
    targetName: string;
    description: string;
    requester: UserSummary;
    requestedAt: Date;
    urgency: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  }[];

  // 프로젝트별 현황
  projectStatus: {
    projectId: string;
    projectName: string;
    ticketCounts: {
      inProgress: number;
      testing: number;
      pendingDeploy: number;
    };
    currentProdVersion: string;
  }[];

  // 배포 일정 (캘린더용)
  deploymentSchedule: {
    id: string;
    title: string;
    projectName: string;
    scheduledDate: Date;
    status: 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED';
  }[];
}
```

#### QA 대시보드

```typescript
interface QADashboard {
  // 환경별 현재 버전
  environmentStatus: {
    environmentId: string;
    name: string;           // Development, Staging, Production
    currentVersion: string;
    lastDeployedAt: Date;
    status: 'HEALTHY' | 'DEGRADED' | 'DOWN';
  }[];

  // 테스트 대기 배포
  pendingTests: {
    deploymentId: string;
    projectName: string;
    version: string;
    environment: string;
    deployedAt: Date;
    changes: {
      type: 'FEATURE' | 'BUGFIX' | 'HOTFIX';
      description: string;
      ticketNumber: string;
    }[];
  }[];

  // 최근 변경 사항
  recentChanges: {
    ticketNumber: string;
    title: string;
    type: TicketType;
    status: TicketStatus;
    assignee: UserSummary;
    updatedAt: Date;
  }[];
}
```

---

## 2. 프로젝트 관리 (Project)

### 2.1 프로젝트 목록

```typescript
interface ProjectListItem {
  id: string;
  name: string;
  description: string;
  repositoryCount: number;
  memberCount: number;
  lastActivity: Date;
  status: 'ACTIVE' | 'ARCHIVED';
}

interface ProjectListPage {
  projects: ProjectListItem[];
  pagination: Pagination;
  filters: {
    status?: 'ACTIVE' | 'ARCHIVED';
    search?: string;
  };
}
```

### 2.2 프로젝트 상세

```typescript
interface ProjectDetail {
  id: string;
  name: string;
  description: string;
  createdAt: Date;
  updatedAt: Date;

  // 연결된 외부 서비스
  connections: {
    id: string;
    type: 'GITHUB' | 'GITLAB' | 'BITBUCKET' | 'JENKINS' | 'ARGOCD';
    name: string;
    status: 'CONNECTED' | 'DISCONNECTED' | 'ERROR';
    lastSyncAt: Date;
  }[];

  // 저장소 목록
  repositories: {
    id: string;
    name: string;
    fullName: string;       // owner/repo
    defaultBranch: string;
    branchStrategy: 'GIT_FLOW' | 'GITHUB_FLOW' | 'TRUNK_BASED';
    lastPushAt: Date;
  }[];

  // 환경 설정
  environments: {
    id: string;
    name: string;
    type: 'DEVELOPMENT' | 'STAGING' | 'PRODUCTION';
    url?: string;
    requiresApproval: boolean;
  }[];

  // 팀 멤버
  members: {
    userId: string;
    name: string;
    email: string;
    role: 'OWNER' | 'ADMIN' | 'DEVELOPER' | 'VIEWER';
    avatarUrl?: string;
  }[];
}
```

### 2.3 연결(Connection) 설정

```typescript
interface ConnectionForm {
  type: 'GITHUB' | 'GITLAB' | 'BITBUCKET' | 'JENKINS' | 'ARGOCD';
  name: string;
  baseUrl?: string;      // Self-hosted인 경우
  credentials: {
    type: 'OAUTH' | 'TOKEN' | 'SSH_KEY';
    // OAuth 콜백 또는 토큰 입력
  };
}

interface ConnectionDetail {
  id: string;
  type: ConnectionType;
  name: string;
  baseUrl: string;
  status: 'CONNECTED' | 'DISCONNECTED' | 'ERROR';
  lastSyncAt: Date;
  
  // 사용 가능한 기능
  capabilities: {
    canListRepositories: boolean;
    canManageBranches: boolean;
    canTriggerBuilds: boolean;
    canDeployments: boolean;
  };
}
```

---

## 3. 티켓 관리 (Ticket)

### 3.1 티켓 상태 (7단계)

```typescript
type TicketStatus =
  | 'BACKLOG'        // 백로그
  | 'TODO'           // 할 일
  | 'IN_PROGRESS'    // 진행 중
  | 'CODE_REVIEW'    // 코드 리뷰
  | 'TESTING'        // 테스트 중
  | 'DONE'           // 완료
  | 'DEPLOYED';      // 배포 완료

type TicketType = 'FEATURE' | 'BUGFIX' | 'HOTFIX' | 'RELEASE' | 'TASK';

type TicketPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
```

### 3.2 티켓 목록 (칸반/테이블)

```typescript
interface TicketListItem {
  id: string;
  ticketNumber: string;   // PROJ-123
  title: string;
  type: TicketType;
  status: TicketStatus;
  priority: TicketPriority;
  assignee?: UserSummary;
  reporter: UserSummary;
  createdAt: Date;
  updatedAt: Date;
  
  // 연결 정보
  linkedBranch?: string;
  linkedMR?: {
    number: number;
    status: MergeRequestStatus;
  };
  linkedBuild?: {
    number: number;
    status: BuildStatus;
  };
}

// 칸반 뷰용
interface KanbanBoard {
  columns: {
    status: TicketStatus;
    label: string;
    tickets: TicketListItem[];
    count: number;
  }[];
}

// 테이블 뷰용
interface TicketTablePage {
  tickets: TicketListItem[];
  pagination: Pagination;
  filters: TicketFilters;
  sorting: {
    field: string;
    direction: 'ASC' | 'DESC';
  };
}
```

### 3.3 티켓 상세

```typescript
interface TicketDetail {
  id: string;
  ticketNumber: string;
  title: string;
  description: string;    // Markdown
  type: TicketType;
  status: TicketStatus;
  priority: TicketPriority;

  // 담당자
  assignee?: UserSummary;
  reporter: UserSummary;

  // 일정
  createdAt: Date;
  updatedAt: Date;
  dueDate?: Date;
  estimatedHours?: number;
  actualHours?: number;

  // 연결된 항목
  linkedItems: {
    branches: {
      id: string;
      name: string;
      status: BranchStatus;
    }[];
    mergeRequests: {
      id: string;
      number: number;
      title: string;
      status: MergeRequestStatus;
    }[];
    builds: {
      id: string;
      number: number;
      status: BuildStatus;
    }[];
    deployments: {
      id: string;
      environment: string;
      version: string;
      status: DeploymentStatus;
    }[];
  };

  // 히스토리
  history: {
    id: string;
    action: 'CREATED' | 'STATUS_CHANGED' | 'ASSIGNED' | 'COMMENTED' | 'LINKED';
    actor: UserSummary;
    timestamp: Date;
    details: Record<string, any>;
  }[];

  // 코멘트
  comments: {
    id: string;
    author: UserSummary;
    content: string;
    createdAt: Date;
    updatedAt?: Date;
  }[];
}
```

### 3.4 티켓 생성/수정 폼

```typescript
interface TicketForm {
  title: string;
  description: string;
  type: TicketType;
  priority: TicketPriority;
  assigneeId?: string;
  repositoryId?: string;
  dueDate?: Date;
  estimatedHours?: number;
  labels?: string[];
}
```

---

## 4. 브랜치 관리 (Branch)

### 4.1 브랜치 목록

```typescript
interface BranchListItem {
  id: string;
  name: string;
  type: 'MAIN' | 'DEVELOP' | 'FEATURE' | 'RELEASE' | 'HOTFIX';
  status: 'ACTIVE' | 'MERGED' | 'DELETED' | 'STALE';
  
  // Git 정보
  lastCommit: {
    sha: string;
    message: string;
    author: string;
    date: Date;
  };
  ahead: number;
  behind: number;

  // 연결 정보
  linkedTicket?: {
    number: string;
    title: string;
  };
  linkedMR?: {
    number: number;
    status: MergeRequestStatus;
  };

  // 보호 상태
  isProtected: boolean;
  requiresPR: boolean;
}

interface BranchListPage {
  branches: BranchListItem[];
  pagination: Pagination;
  filters: {
    type?: BranchType[];
    status?: BranchStatus[];
    search?: string;
  };
}
```

### 4.2 브랜치 생성 폼

```typescript
interface CreateBranchForm {
  name: string;
  type: 'FEATURE' | 'RELEASE' | 'HOTFIX';
  sourceBranch: string;     // 분기 기준 브랜치
  linkedTicketId?: string;  // 연결할 티켓
  autoLinkTicket: boolean;  // 자동으로 티켓 상태 변경
}
```

### 4.3 브랜치 전략 설정

```typescript
interface BranchStrategyConfig {
  strategy: 'GIT_FLOW' | 'GITHUB_FLOW' | 'TRUNK_BASED';
  
  // Git Flow 설정
  mainBranch: string;
  developBranch?: string;
  
  // 브랜치 명명 규칙
  namingPatterns: {
    feature: string;    // 예: feature/{ticket}-{description}
    release: string;    // 예: release/v{version}
    hotfix: string;     // 예: hotfix/{ticket}-{description}
  };

  // 보호 규칙
  protectedBranches: {
    pattern: string;
    requiresPullRequest: boolean;
    requiredApprovals: number;
    requiresStatusChecks: boolean;
    statusChecks: string[];
  }[];
}
```

---

## 5. Merge Request 관리

### 5.1 MR 상태

```typescript
type MergeRequestStatus =
  | 'DRAFT'
  | 'OPEN'
  | 'REVIEW_IN_PROGRESS'
  | 'CHANGES_REQUESTED'
  | 'APPROVED'
  | 'MERGED'
  | 'CLOSED';
```

### 5.2 MR 목록

```typescript
interface MergeRequestListItem {
  id: string;
  number: number;
  title: string;
  status: MergeRequestStatus;
  
  // 브랜치 정보
  sourceBranch: string;
  targetBranch: string;
  
  // 작성자
  author: UserSummary;
  
  // 리뷰 상태
  reviewStatus: {
    approved: number;
    pending: number;
    changesRequested: number;
    required: number;
  };

  // 변경 통계
  additions: number;
  deletions: number;
  changedFiles: number;

  // CI 상태
  ciStatus: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED' | 'CANCELLED';

  // 시간
  createdAt: Date;
  updatedAt: Date;

  // 연결된 티켓
  linkedTicket?: {
    number: string;
    title: string;
  };
}
```

### 5.3 MR 상세

```typescript
interface MergeRequestDetail {
  id: string;
  number: number;
  title: string;
  description: string;    // Markdown
  status: MergeRequestStatus;

  // 브랜치
  sourceBranch: string;
  targetBranch: string;
  
  // 병합 가능 여부
  mergeable: boolean;
  mergeableReason?: 'CONFLICTS' | 'CI_FAILED' | 'REVIEW_REQUIRED' | 'BLOCKED';

  // 작성자/담당자
  author: UserSummary;
  assignees: UserSummary[];
  reviewers: {
    user: UserSummary;
    status: 'PENDING' | 'APPROVED' | 'CHANGES_REQUESTED' | 'COMMENTED';
    reviewedAt?: Date;
  }[];

  // 변경 사항
  commits: {
    sha: string;
    message: string;
    author: string;
    date: Date;
  }[];

  changedFiles: {
    filename: string;
    status: 'ADDED' | 'MODIFIED' | 'DELETED' | 'RENAMED';
    additions: number;
    deletions: number;
  }[];

  // CI/CD 상태
  statusChecks: {
    name: string;
    status: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED';
    description?: string;
    url?: string;
  }[];

  // 리뷰 코멘트
  reviews: {
    id: string;
    author: UserSummary;
    body: string;
    state: 'COMMENTED' | 'APPROVED' | 'CHANGES_REQUESTED';
    createdAt: Date;
    lineComments?: {
      path: string;
      line: number;
      body: string;
    }[];
  }[];

  // 일반 코멘트
  comments: {
    id: string;
    author: UserSummary;
    body: string;
    createdAt: Date;
  }[];

  // 연결 정보
  linkedTicket?: TicketSummary;
  linkedBuild?: BuildSummary;

  // 시간
  createdAt: Date;
  updatedAt: Date;
  mergedAt?: Date;
  closedAt?: Date;
}
```

---

## 6. 빌드 관리 (Build)

### 6.1 빌드 상태

```typescript
type BuildStatus =
  | 'PENDING'
  | 'QUEUED'
  | 'RUNNING'
  | 'SUCCESS'
  | 'FAILED'
  | 'CANCELLED';
```

### 6.2 빌드 목록

```typescript
interface BuildListItem {
  id: string;
  buildNumber: number;
  repositoryName: string;
  branch: string;
  
  // 트리거 정보
  trigger: 'PUSH' | 'PULL_REQUEST' | 'MANUAL' | 'SCHEDULED' | 'WORKFLOW';
  triggeredBy: UserSummary;

  // 커밋 정보
  commit: {
    sha: string;
    message: string;
    author: string;
  };

  // 상태
  status: BuildStatus;
  
  // 시간
  startedAt?: Date;
  finishedAt?: Date;
  duration?: number;      // 초 단위

  // 연결 정보
  linkedMR?: number;
  linkedTicket?: string;
}
```

### 6.3 빌드 상세

```typescript
interface BuildDetail {
  id: string;
  buildNumber: number;
  repositoryName: string;
  branch: string;
  status: BuildStatus;

  // 빌드 단계
  steps: {
    id: string;
    name: string;
    status: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED' | 'SKIPPED';
    startedAt?: Date;
    finishedAt?: Date;
    duration?: number;
    logUrl?: string;
  }[];

  // 아티팩트
  artifacts: {
    id: string;
    name: string;
    type: 'DOCKER_IMAGE' | 'JAR' | 'WAR' | 'ZIP' | 'OTHER';
    size: number;
    path: string;
    downloadUrl?: string;
  }[];

  // 테스트 결과
  testResults?: {
    total: number;
    passed: number;
    failed: number;
    skipped: number;
    coverage?: number;
  };

  // 환경 정보
  environment: {
    runner: string;
    nodeVersion?: string;
    javaVersion?: string;
    dockerVersion?: string;
  };

  // 로그
  logs: string;           // 전체 로그 또는 로그 URL

  // 시간
  queuedAt: Date;
  startedAt?: Date;
  finishedAt?: Date;
  duration?: number;
}
```

---

## 7. 배포 관리 (Deployment)

### 7.1 배포 상태

```typescript
type DeploymentStatus =
  | 'PENDING'
  | 'PENDING_APPROVAL'
  | 'APPROVED'
  | 'REJECTED'
  | 'IN_PROGRESS'
  | 'SUCCESS'
  | 'FAILED'
  | 'ROLLED_BACK';
```

### 7.2 환경별 현황

```typescript
interface EnvironmentOverview {
  environments: {
    id: string;
    name: string;
    type: 'DEVELOPMENT' | 'STAGING' | 'PRODUCTION';
    url?: string;
    
    // 현재 배포 상태
    current: {
      version: string;
      deployedAt: Date;
      deployedBy: UserSummary;
      buildNumber: number;
    };

    // 대기 중인 배포
    pending?: {
      version: string;
      status: DeploymentStatus;
      requestedBy: UserSummary;
      requestedAt: Date;
    };

    // 건강 상태
    health: 'HEALTHY' | 'DEGRADED' | 'DOWN' | 'UNKNOWN';
  }[];
}
```

### 7.3 배포 상세

```typescript
interface DeploymentDetail {
  id: string;
  environment: {
    id: string;
    name: string;
    type: EnvironmentType;
  };
  version: string;
  status: DeploymentStatus;

  // 빌드 정보
  build: {
    id: string;
    number: number;
    commit: string;
    branch: string;
  };

  // 변경 사항 (이전 버전 대비)
  changes: {
    previousVersion: string;
    commits: {
      sha: string;
      message: string;
      author: string;
    }[];
    tickets: {
      number: string;
      title: string;
      type: TicketType;
    }[];
  };

  // 배포 전략
  strategy: 'ROLLING_UPDATE' | 'BLUE_GREEN' | 'CANARY' | 'RECREATE';

  // 배포 태스크
  tasks: {
    id: string;
    name: string;
    status: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED';
    startedAt?: Date;
    finishedAt?: Date;
    logs?: string;
  }[];

  // 결재 정보 (Production인 경우)
  approval?: {
    id: string;
    status: 'PENDING' | 'APPROVED' | 'REJECTED';
    approvalLines: {
      order: number;
      approverRole: string;
      approver?: UserSummary;
      status: 'PENDING' | 'APPROVED' | 'REJECTED';
      respondedAt?: Date;
      comment?: string;
    }[];
  };

  // 시간
  requestedAt: Date;
  requestedBy: UserSummary;
  startedAt?: Date;
  finishedAt?: Date;

  // 롤백 정보
  rollbackFrom?: {
    deploymentId: string;
    version: string;
  };
}
```

### 7.4 배포 요청 폼

```typescript
interface DeploymentRequestForm {
  environmentId: string;
  buildId: string;
  strategy?: 'ROLLING_UPDATE' | 'BLUE_GREEN' | 'CANARY';
  description?: string;
  
  // 고급 옵션 (개발자용)
  advanced?: {
    envOverrides?: Record<string, string>;
    replicaCount?: number;
    canaryPercentage?: number;
  };
}
```

---

## 8. 워크플로우 에디터 (Workflow)

### 8.0 워크플로우 목록

```typescript
interface WorkflowListItem {
  id: string;
  name: string;
  description: string;
  version: number;
  status: 'DRAFT' | 'ACTIVE' | 'ARCHIVED';
  
  // 통계
  stats: {
    totalExecutions: number;
    successRate: number;
    lastExecutedAt?: Date;
  };
  
  // 메타데이터
  createdAt: Date;
  updatedAt: Date;
  createdBy: UserSummary;
}

interface WorkflowListPage {
  workflows: WorkflowListItem[];
  pagination: Pagination;
  filters: {
    status?: 'DRAFT' | 'ACTIVE' | 'ARCHIVED';
    search?: string;
  };
}
```

**워크플로우 목록 페이지 레이아웃**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  워크플로우 관리                              [+ 새 워크플로우 만들기]        │
├─────────────────────────────────────────────────────────────────────────────┤
│  [전체] [활성] [초안] [보관됨]                          🔍 검색...           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 📋 CI/CD 파이프라인                                      [활성] ⚙️  │   │
│  │ 메인 브랜치 푸시 시 빌드/테스트/배포 자동화                          │   │
│  │ 실행: 125회 | 성공률: 94% | 마지막 실행: 2시간 전                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 📋 Hotfix 배포                                          [활성] ⚙️  │   │
│  │ 긴급 수정 사항 빠른 배포                                             │   │
│  │ 실행: 12회 | 성공률: 100% | 마지막 실행: 3일 전                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 📋 Release 워크플로우                                   [초안] ⚙️  │   │
│  │ 정기 릴리스 프로세스                                                 │   │
│  │ 실행: 0회 | 마지막 수정: 1일 전                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **[+ 새 워크플로우 만들기]** 버튼 클릭 시 → **노드 기반 워크플로우 에디터** 페이지로 이동
> 
> 워크플로우 항목 클릭 시 → **동일한 노드 에디터**에서 수정 모드로 열림

### 8.1 워크플로우 정의

```typescript
interface WorkflowDefinition {
  id: string;
  name: string;
  description: string;
  version: number;
  status: 'DRAFT' | 'ACTIVE' | 'ARCHIVED';

  // React Flow 데이터
  definition: {
    nodes: WorkflowNode[];
    edges: WorkflowEdge[];
    viewport: { x: number; y: number; zoom: number };
  };

  // 트리거 설정
  triggers: {
    type: 'MANUAL' | 'PUSH' | 'PULL_REQUEST' | 'SCHEDULE' | 'WEBHOOK';
    config: Record<string, any>;
  }[];

  // 변수
  variables: {
    name: string;
    type: 'STRING' | 'NUMBER' | 'BOOLEAN' | 'SECRET';
    defaultValue?: any;
    required: boolean;
  }[];

  // 메타데이터
  createdAt: Date;
  updatedAt: Date;
  createdBy: UserSummary;
}
```

### 8.2 워크플로우 노드

```typescript
type WorkflowNodeType =
  | 'START'
  | 'END'
  | 'BUILD'
  | 'TEST'
  | 'DEPLOY'
  | 'APPROVAL'
  | 'NOTIFICATION'
  | 'CONDITION'
  | 'PARALLEL'
  | 'DELAY'
  | 'SCRIPT';

interface WorkflowNode {
  id: string;
  type: WorkflowNodeType;
  position: { x: number; y: number };
  data: {
    label: string;
    description?: string;
    config: NodeConfig;      // 노드 타입별 설정
  };
}

interface WorkflowEdge {
  id: string;
  source: string;           // 시작 노드 ID
  target: string;           // 대상 노드 ID
  sourceHandle?: string;    // 조건 분기용
  label?: string;
  data?: {
    condition?: string;     // 조건식
  };
}
```

### 8.3 노드별 설정

```typescript
// 빌드 노드
interface BuildNodeConfig {
  repositoryId: string;
  branch?: string;          // 동적: ${branch}
  buildConfig?: string;     // Dockerfile, pom.xml 등
  environment?: Record<string, string>;
}

// 배포 노드
interface DeployNodeConfig {
  environmentId: string;
  strategy: DeploymentStrategy;
  rollbackOnFailure: boolean;
  healthCheckUrl?: string;
}

// 결재 노드
interface ApprovalNodeConfig {
  approverRoles: string[];
  requiredApprovals: number;
  timeout: number;          // 분 단위
  autoReject: boolean;
}

// 조건 노드
interface ConditionNodeConfig {
  expression: string;       // ${build.status} == 'SUCCESS'
  trueLabel: string;
  falseLabel: string;
}

// 알림 노드
interface NotificationNodeConfig {
  channels: ('EMAIL' | 'SLACK' | 'WEBHOOK')[];
  template: string;
  recipients: string[];
}
```

### 8.4 워크플로우 생성/수정 페이지 (노드 에디터)

워크플로우 생성과 수정 모두 **동일한 노드 기반 에디터**를 사용합니다.

#### 페이지 레이아웃

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  워크플로우 에디터                                    [저장] [테스트 실행]    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐  ┌───────────────────────────────────────────────────┐   │
│  │  노드 팔레트  │  │                                                   │   │
│  │              │  │              React Flow 캔버스                     │   │
│  │  ▸ 트리거    │  │                                                   │   │
│  │    • Manual  │  │       ┌─────┐      ┌─────┐      ┌─────┐          │   │
│  │    • Push    │  │       │START│ ───▸ │BUILD│ ───▸ │TEST │          │   │
│  │    • PR      │  │       └─────┘      └─────┘      └─────┘          │   │
│  │              │  │                                    │              │   │
│  │  ▸ 빌드/테스트│  │                                    ▼              │   │
│  │    • Build   │  │                              ┌─────────┐          │   │
│  │    • Test    │  │                              │CONDITION│          │   │
│  │              │  │                              └─────────┘          │   │
│  │  ▸ 배포      │  │                              ↙         ↘         │   │
│  │    • Deploy  │  │                        ┌──────┐    ┌──────┐      │   │
│  │    • Rollback│  │                        │DEPLOY│    │NOTIFY│      │   │
│  │              │  │                        │Staging│   │ Fail │      │   │
│  │  ▸ 결재/알림  │  │                        └──────┘    └──────┘      │   │
│  │    • Approval│  │                            │                      │   │
│  │    • Notify  │  │                            ▼                      │   │
│  │              │  │                       ┌────────┐                  │   │
│  │  ▸ 제어 흐름  │  │                       │APPROVAL│                  │   │
│  │    • Condition│ │                       └────────┘                  │   │
│  │    • Parallel│  │                            │                      │   │
│  │    • Delay   │  │                            ▼                      │   │
│  │              │  │                       ┌──────┐                    │   │
│  │              │  │                       │DEPLOY│                    │   │
│  │              │  │                       │ Prod │                    │   │
│  │              │  │                       └──────┘                    │   │
│  │              │  │                            │                      │   │
│  │              │  │                            ▼                      │   │
│  │              │  │                        ┌───┐                      │   │
│  │              │  │                        │END│                      │   │
│  │              │  │                        └───┘                      │   │
│  └──────────────┘  └───────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  속성 패널 (선택된 노드)                                              │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ 노드: DEPLOY (Staging)                                        │ │   │
│  │  │ ─────────────────────────────────────────────────────────────  │ │   │
│  │  │ 환경:      [Staging ▼]                                        │ │   │
│  │  │ 전략:      [Rolling Update ▼]                                 │ │   │
│  │  │ 롤백 조건:  [실패 시 자동 롤백 ☑]                               │ │   │
│  │  │ Health Check: [https://staging.example.com/health]            │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 워크플로우 생성 폼 (기본 정보)

```typescript
interface WorkflowCreateForm {
  // 기본 정보 (생성 시 입력)
  name: string;
  description?: string;
  projectId: string;
  
  // 초기 노드 (기본 START/END 노드로 시작)
  initialDefinition: {
    nodes: WorkflowNode[];  // [START, END] 기본 제공
    edges: WorkflowEdge[];  // START → END 연결
    viewport: { x: number; y: number; zoom: number };
  };
}
```

#### 워크플로우 에디터 상태

```typescript
interface WorkflowEditorState {
  // 워크플로우 기본 정보
  id?: string;                    // 수정 시에만 존재
  name: string;
  description: string;
  isNew: boolean;                 // 생성 vs 수정 구분
  
  // React Flow 상태
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  viewport: { x: number; y: number; zoom: number };
  
  // 편집 상태
  selectedNodeId: string | null;
  isDirty: boolean;               // 변경사항 있음
  
  // 유효성 검사
  validationErrors: {
    nodeId: string;
    field: string;
    message: string;
  }[];
  
  // 노드 팔레트 상태
  paletteCollapsed: Record<string, boolean>;
}
```

#### 노드 드래그 앤 드롭 인터랙션

```typescript
interface NodeDragDropHandler {
  // 팔레트에서 캔버스로 드래그
  onDragStart: (nodeType: WorkflowNodeType) => void;
  onDragOver: (event: DragEvent) => void;
  onDrop: (event: DragEvent, position: { x: number; y: number }) => void;
  
  // 새 노드 생성 (드롭 시)
  createNode: (type: WorkflowNodeType, position: { x: number; y: number }) => WorkflowNode;
}

// 노드 생성 시 기본 설정
const defaultNodeConfigs: Record<WorkflowNodeType, Partial<NodeConfig>> = {
  START: { label: '시작' },
  END: { label: '종료' },
  BUILD: { 
    label: '빌드',
    repositoryId: '',
    branch: '${branch}',
  },
  TEST: { 
    label: '테스트',
    testType: 'UNIT',
  },
  DEPLOY: { 
    label: '배포',
    environmentId: '',
    strategy: 'ROLLING_UPDATE',
    rollbackOnFailure: true,
  },
  APPROVAL: { 
    label: '결재',
    approverRoles: [],
    requiredApprovals: 1,
    timeout: 1440,  // 24시간
  },
  NOTIFICATION: { 
    label: '알림',
    channels: ['SLACK'],
    template: 'default',
  },
  CONDITION: { 
    label: '조건',
    expression: '',
    trueLabel: 'Yes',
    falseLabel: 'No',
  },
  PARALLEL: { 
    label: '병렬',
    branches: 2,
  },
  DELAY: { 
    label: '대기',
    duration: 300,  // 5분
  },
  SCRIPT: { 
    label: '스크립트',
    script: '',
    language: 'bash',
  },
};
```

#### 에디터 액션

```typescript
interface WorkflowEditorActions {
  // 노드 조작
  addNode: (node: WorkflowNode) => void;
  updateNode: (nodeId: string, data: Partial<WorkflowNode['data']>) => void;
  deleteNode: (nodeId: string) => void;
  
  // 엣지 조작
  addEdge: (edge: WorkflowEdge) => void;
  updateEdge: (edgeId: string, data: Partial<WorkflowEdge>) => void;
  deleteEdge: (edgeId: string) => void;
  
  // 선택
  selectNode: (nodeId: string | null) => void;
  
  // 저장
  saveWorkflow: () => Promise<void>;
  saveDraft: () => Promise<void>;
  
  // 유효성 검사
  validate: () => ValidationResult;
  
  // 테스트 실행
  testRun: () => Promise<void>;
  
  // 실행 취소/재실행
  undo: () => void;
  redo: () => void;
  
  // 뷰포트 조작
  fitView: () => void;
  zoomIn: () => void;
  zoomOut: () => void;
}
```

#### 노드 팔레트 컴포넌트

```typescript
interface NodePaletteCategory {
  id: string;
  label: string;
  icon: string;
  nodes: {
    type: WorkflowNodeType;
    label: string;
    icon: string;
    description: string;
  }[];
}

const nodePaletteCategories: NodePaletteCategory[] = [
  {
    id: 'trigger',
    label: '트리거',
    icon: 'play',
    nodes: [
      { type: 'START', label: '시작', icon: 'play-circle', description: '워크플로우 시작점' },
    ],
  },
  {
    id: 'build-test',
    label: '빌드/테스트',
    icon: 'package',
    nodes: [
      { type: 'BUILD', label: '빌드', icon: 'box', description: '애플리케이션 빌드' },
      { type: 'TEST', label: '테스트', icon: 'check-square', description: '테스트 실행' },
    ],
  },
  {
    id: 'deploy',
    label: '배포',
    icon: 'upload-cloud',
    nodes: [
      { type: 'DEPLOY', label: '배포', icon: 'server', description: '환경에 배포' },
    ],
  },
  {
    id: 'approval-notify',
    label: '결재/알림',
    icon: 'bell',
    nodes: [
      { type: 'APPROVAL', label: '결재', icon: 'user-check', description: '결재 요청' },
      { type: 'NOTIFICATION', label: '알림', icon: 'bell', description: '알림 전송' },
    ],
  },
  {
    id: 'control-flow',
    label: '제어 흐름',
    icon: 'git-branch',
    nodes: [
      { type: 'CONDITION', label: '조건', icon: 'git-branch', description: '조건 분기' },
      { type: 'PARALLEL', label: '병렬', icon: 'layers', description: '병렬 실행' },
      { type: 'DELAY', label: '대기', icon: 'clock', description: '지연 시간' },
      { type: 'SCRIPT', label: '스크립트', icon: 'code', description: '커스텀 스크립트' },
    ],
  },
  {
    id: 'end',
    label: '종료',
    icon: 'stop-circle',
    nodes: [
      { type: 'END', label: '종료', icon: 'stop-circle', description: '워크플로우 종료' },
    ],
  },
];
```

### 8.5 워크플로우 실행

```typescript
interface WorkflowExecution {
  id: string;
  workflowId: string;
  workflowName: string;
  status: 'RUNNING' | 'SUCCESS' | 'FAILED' | 'CANCELLED' | 'WAITING';

  // 트리거 정보
  trigger: {
    type: TriggerType;
    source?: string;        // 브랜치, PR 번호 등
    triggeredBy?: UserSummary;
  };

  // 노드 상태
  nodeStates: {
    nodeId: string;
    nodeName: string;
    status: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED' | 'SKIPPED' | 'WAITING';
    startedAt?: Date;
    finishedAt?: Date;
    output?: Record<string, any>;
    error?: string;
  }[];

  // 변수 값
  variables: Record<string, any>;

  // 시간
  startedAt: Date;
  finishedAt?: Date;
  duration?: number;
}
```

---

## 9. 결재 관리 (Approval)

### 9.1 결재 상태

```typescript
type ApprovalStatus =
  | 'PENDING'
  | 'IN_PROGRESS'
  | 'APPROVED'
  | 'REJECTED'
  | 'CANCELLED'
  | 'EXPIRED';

type ApprovalTargetType =
  | 'DEPLOYMENT'
  | 'MERGE_REQUEST'
  | 'RELEASE'
  | 'TICKET';
```

### 9.2 결재 목록 (내가 처리해야 할)

```typescript
interface ApprovalListItem {
  id: string;
  targetType: ApprovalTargetType;
  targetId: string;
  targetTitle: string;
  targetDescription: string;
  
  status: ApprovalStatus;
  urgency: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

  requester: UserSummary;
  requestedAt: Date;

  // 결재 진행 상황
  progress: {
    current: number;      // 현재 단계
    total: number;        // 전체 단계
    myTurn: boolean;      // 내 차례인지
  };

  // 마감
  dueAt?: Date;
  isOverdue: boolean;
}
```

### 9.3 결재 상세

```typescript
interface ApprovalDetail {
  id: string;
  targetType: ApprovalTargetType;
  targetId: string;
  status: ApprovalStatus;

  // 대상 정보 (타입에 따라 다름)
  target: DeploymentDetail | MergeRequestDetail | ReleaseDetail | TicketDetail;

  // 결재선
  approvalLines: {
    order: number;
    approverRole: string;
    approvers: {
      user: UserSummary;
      status: 'PENDING' | 'APPROVED' | 'REJECTED';
      respondedAt?: Date;
      comment?: string;
    }[];
    requiredApprovals: number;
    status: 'PENDING' | 'APPROVED' | 'REJECTED';
  }[];

  // 코멘트
  comments: {
    id: string;
    author: UserSummary;
    content: string;
    createdAt: Date;
  }[];

  // 히스토리
  history: {
    action: 'CREATED' | 'APPROVED' | 'REJECTED' | 'COMMENTED' | 'ESCALATED';
    actor: UserSummary;
    timestamp: Date;
    details?: string;
  }[];

  // 시간
  requestedAt: Date;
  dueAt?: Date;
  completedAt?: Date;
}
```

### 9.4 결재 처리 폼

```typescript
interface ApprovalActionForm {
  action: 'APPROVE' | 'REJECT';
  comment?: string;
}
```

---

## 10. 알림 및 설정

### 10.1 알림 목록

```typescript
interface NotificationItem {
  id: string;
  type: NotificationType;
  title: string;
  body: string;
  read: boolean;
  createdAt: Date;

  // 관련 리소스
  resource?: {
    type: 'TICKET' | 'MR' | 'BUILD' | 'DEPLOYMENT' | 'APPROVAL';
    id: string;
    url: string;
  };

  // 액션
  actions?: {
    label: string;
    action: string;
    primary?: boolean;
  }[];
}

type NotificationType =
  | 'APPROVAL_REQUESTED'
  | 'APPROVAL_COMPLETED'
  | 'BUILD_FAILED'
  | 'BUILD_SUCCESS'
  | 'DEPLOYMENT_COMPLETED'
  | 'DEPLOYMENT_FAILED'
  | 'REVIEW_REQUESTED'
  | 'REVIEW_COMMENT'
  | 'MENTION'
  | 'TICKET_ASSIGNED';
```

### 10.2 알림 설정

```typescript
interface NotificationSettings {
  // 채널별 설정
  channels: {
    email: {
      enabled: boolean;
      address: string;
    };
    push: {
      enabled: boolean;
      devices: string[];
    };
    slack: {
      enabled: boolean;
      channel: string;
    };
  };

  // 이벤트별 설정
  events: {
    [K in NotificationType]: {
      email: boolean;
      push: boolean;
      slack: boolean;
    };
  };

  // 방해 금지
  quietHours: {
    enabled: boolean;
    start: string;        // HH:mm
    end: string;          // HH:mm
    timezone: string;
    excludeWeekends: boolean;
    excludeUrgent: boolean;  // 긴급 알림은 항상 전송
  };
}
```

---

## 11. 공통 타입 정의

### 11.1 사용자 정보

```typescript
interface UserSummary {
  id: string;
  name: string;
  email: string;
  avatarUrl?: string;
}

interface UserProfile extends UserSummary {
  role: 'ADMIN' | 'DEVELOPER' | 'QA' | 'PM' | 'VIEWER';
  department?: string;
  settings: {
    language: 'ko' | 'en';
    theme: 'light' | 'dark' | 'system';
    useTechnicalTerms: boolean;
  };
}
```

### 11.2 페이지네이션

```typescript
interface Pagination {
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

interface PaginatedResponse<T> {
  content: T[];
  pagination: Pagination;
}
```

### 11.3 API 응답

```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, string>;
  };
  timestamp: Date;
}
```

---

## 12. 화면별 API 엔드포인트

| 화면 | 메서드 | 엔드포인트 | 설명 |
|-----|--------|-----------|------|
| **대시보드** | GET | `/api/dashboard/{role}` | 역할별 대시보드 데이터 |
| **프로젝트** | GET | `/api/projects` | 프로젝트 목록 |
| | GET | `/api/projects/{id}` | 프로젝트 상세 |
| | POST | `/api/projects` | 프로젝트 생성 |
| **티켓** | GET | `/api/tickets` | 티켓 목록 |
| | GET | `/api/tickets/{id}` | 티켓 상세 |
| | POST | `/api/tickets` | 티켓 생성 |
| | PATCH | `/api/tickets/{id}/status` | 상태 변경 |
| **브랜치** | GET | `/api/repositories/{repoId}/branches` | 브랜치 목록 |
| | POST | `/api/repositories/{repoId}/branches` | 브랜치 생성 |
| **MR** | GET | `/api/merge-requests` | MR 목록 |
| | GET | `/api/merge-requests/{id}` | MR 상세 |
| | POST | `/api/merge-requests` | MR 생성 |
| | POST | `/api/merge-requests/{id}/merge` | 병합 |
| **빌드** | GET | `/api/builds` | 빌드 목록 |
| | GET | `/api/builds/{id}` | 빌드 상세 |
| | POST | `/api/builds` | 빌드 트리거 |
| | GET | `/api/builds/{id}/logs` | 로그 조회 |
| **배포** | GET | `/api/environments` | 환경 목록 |
| | GET | `/api/deployments` | 배포 목록 |
| | POST | `/api/deployments` | 배포 요청 |
| | POST | `/api/deployments/{id}/rollback` | 롤백 |
| **워크플로우** | GET | `/api/workflows` | 워크플로우 목록 |
| | GET | `/api/workflows/{id}` | 워크플로우 상세 |
| | POST | `/api/workflows` | 워크플로우 생성 (노드 에디터) |
| | PUT | `/api/workflows/{id}` | 워크플로우 수정 (노드 에디터) |
| | DELETE | `/api/workflows/{id}` | 워크플로우 삭제 |
| | POST | `/api/workflows/{id}/execute` | 실행 |
| | POST | `/api/workflows/{id}/test-run` | 테스트 실행 |
| | WS | `/ws/workflow-executions/{id}` | 실시간 상태 |
| **결재** | GET | `/api/approvals/pending` | 대기 목록 |
| | GET | `/api/approvals/{id}` | 결재 상세 |
| | POST | `/api/approvals/{id}/approve` | 승인 |
| | POST | `/api/approvals/{id}/reject` | 거절 |

---

## 13. React Query 키 팩토리

```typescript
// Query Key Factory 패턴
export const queryKeys = {
  // 대시보드
  dashboard: {
    all: ['dashboard'] as const,
    byRole: (role: string) => [...queryKeys.dashboard.all, role] as const,
  },

  // 프로젝트
  projects: {
    all: ['projects'] as const,
    lists: () => [...queryKeys.projects.all, 'list'] as const,
    list: (filters: ProjectFilters) => [...queryKeys.projects.lists(), filters] as const,
    details: () => [...queryKeys.projects.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.projects.details(), id] as const,
  },

  // 티켓
  tickets: {
    all: ['tickets'] as const,
    lists: () => [...queryKeys.tickets.all, 'list'] as const,
    list: (filters: TicketFilters) => [...queryKeys.tickets.lists(), filters] as const,
    kanban: (projectId: string) => [...queryKeys.tickets.all, 'kanban', projectId] as const,
    details: () => [...queryKeys.tickets.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.tickets.details(), id] as const,
  },

  // 브랜치
  branches: {
    all: ['branches'] as const,
    byRepo: (repoId: string) => [...queryKeys.branches.all, repoId] as const,
    list: (repoId: string, filters: BranchFilters) => 
      [...queryKeys.branches.byRepo(repoId), 'list', filters] as const,
  },

  // MR
  mergeRequests: {
    all: ['mergeRequests'] as const,
    lists: () => [...queryKeys.mergeRequests.all, 'list'] as const,
    list: (filters: MRFilters) => [...queryKeys.mergeRequests.lists(), filters] as const,
    details: () => [...queryKeys.mergeRequests.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.mergeRequests.details(), id] as const,
  },

  // 빌드
  builds: {
    all: ['builds'] as const,
    lists: () => [...queryKeys.builds.all, 'list'] as const,
    list: (filters: BuildFilters) => [...queryKeys.builds.lists(), filters] as const,
    details: () => [...queryKeys.builds.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.builds.details(), id] as const,
    logs: (id: string) => [...queryKeys.builds.detail(id), 'logs'] as const,
  },

  // 배포
  deployments: {
    all: ['deployments'] as const,
    environments: () => [...queryKeys.deployments.all, 'environments'] as const,
    lists: () => [...queryKeys.deployments.all, 'list'] as const,
    list: (filters: DeploymentFilters) => [...queryKeys.deployments.lists(), filters] as const,
    details: () => [...queryKeys.deployments.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.deployments.details(), id] as const,
  },

  // 워크플로우
  workflows: {
    all: ['workflows'] as const,
    lists: () => [...queryKeys.workflows.all, 'list'] as const,
    list: (filters: WorkflowFilters) => [...queryKeys.workflows.lists(), filters] as const,
    details: () => [...queryKeys.workflows.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.workflows.details(), id] as const,
    executions: (id: string) => [...queryKeys.workflows.detail(id), 'executions'] as const,
  },

  // 결재
  approvals: {
    all: ['approvals'] as const,
    pending: () => [...queryKeys.approvals.all, 'pending'] as const,
    details: () => [...queryKeys.approvals.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.approvals.details(), id] as const,
  },
} as const;
```

---

## 관련 문서

- [사용자 경험 가이드](../../docs/TPS/features/user-experience.md)
- [사용자 흐름 다이어그램](../../docs/TPS/summary/user-flows.md)
- [도메인 모델](../../docs/TPS/design/domain-models/README.md)
- [프론트엔드 기술 스택](../../docs/TPS/tech/frontend/README.md)

