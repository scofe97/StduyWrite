/**
 * TPS (Runners-High) 도메인 타입 정의
 * 
 * 이 파일은 TPS 플랫폼의 핵심 도메인 모델을 TypeScript 인터페이스로 정의합니다.
 */

// ============================================================================
// 공통 타입
// ============================================================================

/** 사용자 요약 정보 */
export interface UserSummary {
  id: string;
  name: string;
  email: string;
  avatarUrl?: string;
}

/** 사용자 상세 프로필 */
export interface UserProfile extends UserSummary {
  role: UserRole;
  department?: string;
  settings: UserSettings;
}

export type UserRole = 'ADMIN' | 'DEVELOPER' | 'QA' | 'PM' | 'VIEWER';

export interface UserSettings {
  language: 'ko' | 'en';
  theme: 'light' | 'dark' | 'system';
  useTechnicalTerms: boolean;
}

/** 페이지네이션 */
export interface Pagination {
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

/** 페이지네이션 응답 */
export interface PaginatedResponse<T> {
  content: T[];
  pagination: Pagination;
}

/** API 응답 래퍼 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  timestamp: Date;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string>;
}

// ============================================================================
// 프로젝트 도메인
// ============================================================================

export interface Project {
  id: string;
  name: string;
  description: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ProjectListItem extends Project {
  repositoryCount: number;
  memberCount: number;
  lastActivity: Date;
  status: ProjectStatus;
}

export type ProjectStatus = 'ACTIVE' | 'ARCHIVED';

export interface ProjectDetail extends Project {
  connections: ConnectionSummary[];
  repositories: RepositorySummary[];
  environments: EnvironmentSummary[];
  members: ProjectMember[];
}

export interface ProjectMember {
  userId: string;
  name: string;
  email: string;
  role: ProjectMemberRole;
  avatarUrl?: string;
}

export type ProjectMemberRole = 'OWNER' | 'ADMIN' | 'DEVELOPER' | 'VIEWER';

// ============================================================================
// 연결(Connection) 도메인
// ============================================================================

export type ConnectionType = 
  | 'GITHUB' 
  | 'GITLAB' 
  | 'BITBUCKET' 
  | 'JENKINS' 
  | 'ARGOCD';

export type ConnectionStatus = 'CONNECTED' | 'DISCONNECTED' | 'ERROR';

export interface ConnectionSummary {
  id: string;
  type: ConnectionType;
  name: string;
  status: ConnectionStatus;
  lastSyncAt: Date;
}

export interface ConnectionDetail extends ConnectionSummary {
  baseUrl: string;
  capabilities: ConnectionCapabilities;
}

export interface ConnectionCapabilities {
  canListRepositories: boolean;
  canManageBranches: boolean;
  canTriggerBuilds: boolean;
  canDeployments: boolean;
}

export interface ConnectionForm {
  type: ConnectionType;
  name: string;
  baseUrl?: string;
  credentials: CredentialInput;
}

export interface CredentialInput {
  type: 'OAUTH' | 'TOKEN' | 'SSH_KEY';
  token?: string;
  privateKey?: string;
}

// ============================================================================
// 저장소(Repository) 도메인
// ============================================================================

export interface RepositorySummary {
  id: string;
  name: string;
  fullName: string;
  defaultBranch: string;
  branchStrategy: BranchStrategy;
  lastPushAt: Date;
}

export type BranchStrategy = 'GIT_FLOW' | 'GITHUB_FLOW' | 'TRUNK_BASED';

export interface RepositoryDetail extends RepositorySummary {
  description?: string;
  url: string;
  connectionId: string;
  branchCount: number;
  openMRCount: number;
  lastBuild?: BuildSummary;
}

export interface BranchStrategyConfig {
  strategy: BranchStrategy;
  mainBranch: string;
  developBranch?: string;
  namingPatterns: BranchNamingPatterns;
  protectedBranches: ProtectedBranchRule[];
}

export interface BranchNamingPatterns {
  feature: string;
  release: string;
  hotfix: string;
}

export interface ProtectedBranchRule {
  pattern: string;
  requiresPullRequest: boolean;
  requiredApprovals: number;
  requiresStatusChecks: boolean;
  statusChecks: string[];
}

// ============================================================================
// 티켓(Ticket) 도메인
// ============================================================================

/** 티켓 7단계 상태 */
export type TicketStatus =
  | 'BACKLOG'
  | 'TODO'
  | 'IN_PROGRESS'
  | 'CODE_REVIEW'
  | 'TESTING'
  | 'DONE'
  | 'DEPLOYED';

export type TicketType = 'FEATURE' | 'BUGFIX' | 'HOTFIX' | 'RELEASE' | 'TASK';

export type TicketPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface TicketSummary {
  id: string;
  ticketNumber: string;
  title: string;
  type: TicketType;
  status: TicketStatus;
  priority: TicketPriority;
}

export interface TicketListItem extends TicketSummary {
  assignee?: UserSummary;
  reporter: UserSummary;
  createdAt: Date;
  updatedAt: Date;
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

export interface TicketDetail extends TicketListItem {
  description: string;
  dueDate?: Date;
  estimatedHours?: number;
  actualHours?: number;
  linkedItems: TicketLinkedItems;
  history: TicketHistoryItem[];
  comments: TicketComment[];
}

export interface TicketLinkedItems {
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
}

export interface TicketHistoryItem {
  id: string;
  action: TicketAction;
  actor: UserSummary;
  timestamp: Date;
  details: Record<string, unknown>;
}

export type TicketAction = 
  | 'CREATED' 
  | 'STATUS_CHANGED' 
  | 'ASSIGNED' 
  | 'COMMENTED' 
  | 'LINKED';

export interface TicketComment {
  id: string;
  author: UserSummary;
  content: string;
  createdAt: Date;
  updatedAt?: Date;
}

export interface TicketForm {
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

export interface TicketFilters {
  status?: TicketStatus[];
  type?: TicketType[];
  priority?: TicketPriority[];
  assigneeId?: string;
  reporterId?: string;
  projectId?: string;
  search?: string;
}

/** 칸반 보드 */
export interface KanbanBoard {
  columns: KanbanColumn[];
}

export interface KanbanColumn {
  status: TicketStatus;
  label: string;
  tickets: TicketListItem[];
  count: number;
}

// ============================================================================
// 브랜치(Branch) 도메인
// ============================================================================

export type BranchType = 'MAIN' | 'DEVELOP' | 'FEATURE' | 'RELEASE' | 'HOTFIX';

export type BranchStatus = 'ACTIVE' | 'MERGED' | 'DELETED' | 'STALE';

export interface BranchSummary {
  id: string;
  name: string;
  type: BranchType;
  status: BranchStatus;
}

export interface BranchListItem extends BranchSummary {
  lastCommit: CommitInfo;
  ahead: number;
  behind: number;
  linkedTicket?: {
    number: string;
    title: string;
  };
  linkedMR?: {
    number: number;
    status: MergeRequestStatus;
  };
  isProtected: boolean;
  requiresPR: boolean;
}

export interface CommitInfo {
  sha: string;
  message: string;
  author: string;
  date: Date;
}

export interface CreateBranchForm {
  name: string;
  type: 'FEATURE' | 'RELEASE' | 'HOTFIX';
  sourceBranch: string;
  linkedTicketId?: string;
  autoLinkTicket: boolean;
}

export interface BranchFilters {
  type?: BranchType[];
  status?: BranchStatus[];
  search?: string;
}

// ============================================================================
// Merge Request 도메인
// ============================================================================

export type MergeRequestStatus =
  | 'DRAFT'
  | 'OPEN'
  | 'REVIEW_IN_PROGRESS'
  | 'CHANGES_REQUESTED'
  | 'APPROVED'
  | 'MERGED'
  | 'CLOSED';

export interface MergeRequestSummary {
  id: string;
  number: number;
  title: string;
  status: MergeRequestStatus;
}

export interface MergeRequestListItem extends MergeRequestSummary {
  sourceBranch: string;
  targetBranch: string;
  author: UserSummary;
  reviewStatus: ReviewProgress;
  additions: number;
  deletions: number;
  changedFiles: number;
  ciStatus: CIStatus;
  createdAt: Date;
  updatedAt: Date;
  linkedTicket?: TicketSummary;
}

export interface ReviewProgress {
  approved: number;
  pending: number;
  changesRequested: number;
  required: number;
}

export type CIStatus = 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED' | 'CANCELLED';

export interface MergeRequestDetail extends MergeRequestListItem {
  description: string;
  mergeable: boolean;
  mergeableReason?: MergeBlockReason;
  assignees: UserSummary[];
  reviewers: ReviewerStatus[];
  commits: CommitInfo[];
  changedFilesList: ChangedFile[];
  statusChecks: StatusCheck[];
  reviews: Review[];
  comments: MRComment[];
  linkedBuild?: BuildSummary;
  mergedAt?: Date;
  closedAt?: Date;
}

export type MergeBlockReason = 
  | 'CONFLICTS' 
  | 'CI_FAILED' 
  | 'REVIEW_REQUIRED' 
  | 'BLOCKED';

export interface ReviewerStatus {
  user: UserSummary;
  status: 'PENDING' | 'APPROVED' | 'CHANGES_REQUESTED' | 'COMMENTED';
  reviewedAt?: Date;
}

export interface ChangedFile {
  filename: string;
  status: 'ADDED' | 'MODIFIED' | 'DELETED' | 'RENAMED';
  additions: number;
  deletions: number;
}

export interface StatusCheck {
  name: string;
  status: CIStatus;
  description?: string;
  url?: string;
}

export interface Review {
  id: string;
  author: UserSummary;
  body: string;
  state: 'COMMENTED' | 'APPROVED' | 'CHANGES_REQUESTED';
  createdAt: Date;
  lineComments?: LineComment[];
}

export interface LineComment {
  path: string;
  line: number;
  body: string;
}

export interface MRComment {
  id: string;
  author: UserSummary;
  body: string;
  createdAt: Date;
}

export interface MRFilters {
  status?: MergeRequestStatus[];
  authorId?: string;
  reviewerId?: string;
  repositoryId?: string;
  search?: string;
}

// ============================================================================
// 빌드(Build) 도메인
// ============================================================================

export type BuildStatus =
  | 'PENDING'
  | 'QUEUED'
  | 'RUNNING'
  | 'SUCCESS'
  | 'FAILED'
  | 'CANCELLED';

export type BuildTrigger = 
  | 'PUSH' 
  | 'PULL_REQUEST' 
  | 'MANUAL' 
  | 'SCHEDULED' 
  | 'WORKFLOW';

export interface BuildSummary {
  id: string;
  buildNumber: number;
  status: BuildStatus;
}

export interface BuildListItem extends BuildSummary {
  repositoryName: string;
  branch: string;
  trigger: BuildTrigger;
  triggeredBy: UserSummary;
  commit: CommitInfo;
  startedAt?: Date;
  finishedAt?: Date;
  duration?: number;
  linkedMR?: number;
  linkedTicket?: string;
}

export interface BuildDetail extends BuildListItem {
  steps: BuildStep[];
  artifacts: BuildArtifact[];
  testResults?: TestResults;
  environment: BuildEnvironment;
  logs: string;
  queuedAt: Date;
}

export interface BuildStep {
  id: string;
  name: string;
  status: BuildStepStatus;
  startedAt?: Date;
  finishedAt?: Date;
  duration?: number;
  logUrl?: string;
}

export type BuildStepStatus = 
  | 'PENDING' 
  | 'RUNNING' 
  | 'SUCCESS' 
  | 'FAILED' 
  | 'SKIPPED';

export interface BuildArtifact {
  id: string;
  name: string;
  type: ArtifactType;
  size: number;
  path: string;
  downloadUrl?: string;
}

export type ArtifactType = 'DOCKER_IMAGE' | 'JAR' | 'WAR' | 'ZIP' | 'OTHER';

export interface TestResults {
  total: number;
  passed: number;
  failed: number;
  skipped: number;
  coverage?: number;
}

export interface BuildEnvironment {
  runner: string;
  nodeVersion?: string;
  javaVersion?: string;
  dockerVersion?: string;
}

export interface BuildFilters {
  status?: BuildStatus[];
  repositoryId?: string;
  branch?: string;
  trigger?: BuildTrigger[];
}

// ============================================================================
// 배포(Deployment) 도메인
// ============================================================================

export type DeploymentStatus =
  | 'PENDING'
  | 'PENDING_APPROVAL'
  | 'APPROVED'
  | 'REJECTED'
  | 'IN_PROGRESS'
  | 'SUCCESS'
  | 'FAILED'
  | 'ROLLED_BACK';

export type EnvironmentType = 'DEVELOPMENT' | 'STAGING' | 'PRODUCTION';

export type DeploymentStrategy = 
  | 'ROLLING_UPDATE' 
  | 'BLUE_GREEN' 
  | 'CANARY' 
  | 'RECREATE';

export type HealthStatus = 'HEALTHY' | 'DEGRADED' | 'DOWN' | 'UNKNOWN';

export interface EnvironmentSummary {
  id: string;
  name: string;
  type: EnvironmentType;
  url?: string;
  requiresApproval: boolean;
}

export interface EnvironmentOverviewItem extends EnvironmentSummary {
  current: {
    version: string;
    deployedAt: Date;
    deployedBy: UserSummary;
    buildNumber: number;
  };
  pending?: {
    version: string;
    status: DeploymentStatus;
    requestedBy: UserSummary;
    requestedAt: Date;
  };
  health: HealthStatus;
}

export interface DeploymentListItem {
  id: string;
  environment: EnvironmentSummary;
  version: string;
  status: DeploymentStatus;
  build: BuildSummary;
  requestedBy: UserSummary;
  requestedAt: Date;
  startedAt?: Date;
  finishedAt?: Date;
}

export interface DeploymentDetail extends DeploymentListItem {
  changes: DeploymentChanges;
  strategy: DeploymentStrategy;
  tasks: DeploymentTask[];
  approval?: ApprovalInfo;
  rollbackFrom?: {
    deploymentId: string;
    version: string;
  };
}

export interface DeploymentChanges {
  previousVersion: string;
  commits: CommitInfo[];
  tickets: TicketSummary[];
}

export interface DeploymentTask {
  id: string;
  name: string;
  status: BuildStepStatus;
  startedAt?: Date;
  finishedAt?: Date;
  logs?: string;
}

export interface ApprovalInfo {
  id: string;
  status: ApprovalStatus;
  approvalLines: ApprovalLineItem[];
}

export interface DeploymentRequestForm {
  environmentId: string;
  buildId: string;
  strategy?: DeploymentStrategy;
  description?: string;
  advanced?: {
    envOverrides?: Record<string, string>;
    replicaCount?: number;
    canaryPercentage?: number;
  };
}

export interface DeploymentFilters {
  environmentId?: string;
  status?: DeploymentStatus[];
  repositoryId?: string;
}

// ============================================================================
// 워크플로우(Workflow) 도메인
// ============================================================================

export type WorkflowStatus = 'DRAFT' | 'ACTIVE' | 'ARCHIVED';

export type WorkflowNodeType =
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

export type TriggerType = 
  | 'MANUAL' 
  | 'PUSH' 
  | 'PULL_REQUEST' 
  | 'SCHEDULE' 
  | 'WEBHOOK';

export interface WorkflowSummary {
  id: string;
  name: string;
  status: WorkflowStatus;
}

export interface WorkflowListItem extends WorkflowSummary {
  description: string;
  version: number;
  triggers: TriggerType[];
  lastExecutedAt?: Date;
  createdBy: UserSummary;
  createdAt: Date;
  updatedAt: Date;
}

export interface WorkflowDefinition extends WorkflowListItem {
  definition: WorkflowGraph;
  variables: WorkflowVariable[];
}

export interface WorkflowGraph {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  viewport: {
    x: number;
    y: number;
    zoom: number;
  };
}

export interface WorkflowNode {
  id: string;
  type: WorkflowNodeType;
  position: { x: number; y: number };
  data: {
    label: string;
    description?: string;
    config: NodeConfig;
  };
}

export type NodeConfig = 
  | BuildNodeConfig 
  | DeployNodeConfig 
  | ApprovalNodeConfig 
  | ConditionNodeConfig 
  | NotificationNodeConfig
  | Record<string, unknown>;

export interface BuildNodeConfig {
  repositoryId: string;
  branch?: string;
  buildConfig?: string;
  environment?: Record<string, string>;
}

export interface DeployNodeConfig {
  environmentId: string;
  strategy: DeploymentStrategy;
  rollbackOnFailure: boolean;
  healthCheckUrl?: string;
}

export interface ApprovalNodeConfig {
  approverRoles: string[];
  requiredApprovals: number;
  timeout: number;
  autoReject: boolean;
}

export interface ConditionNodeConfig {
  expression: string;
  trueLabel: string;
  falseLabel: string;
}

export interface NotificationNodeConfig {
  channels: ('EMAIL' | 'SLACK' | 'WEBHOOK')[];
  template: string;
  recipients: string[];
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string;
  label?: string;
  data?: {
    condition?: string;
  };
}

export interface WorkflowVariable {
  name: string;
  type: 'STRING' | 'NUMBER' | 'BOOLEAN' | 'SECRET';
  defaultValue?: unknown;
  required: boolean;
}

export interface WorkflowTrigger {
  type: TriggerType;
  config: Record<string, unknown>;
}

// 워크플로우 실행
export type WorkflowExecutionStatus = 
  | 'RUNNING' 
  | 'SUCCESS' 
  | 'FAILED' 
  | 'CANCELLED' 
  | 'WAITING';

export type NodeExecutionStatus = 
  | 'PENDING' 
  | 'RUNNING' 
  | 'SUCCESS' 
  | 'FAILED' 
  | 'SKIPPED' 
  | 'WAITING';

export interface WorkflowExecution {
  id: string;
  workflowId: string;
  workflowName: string;
  status: WorkflowExecutionStatus;
  trigger: {
    type: TriggerType;
    source?: string;
    triggeredBy?: UserSummary;
  };
  nodeStates: NodeExecutionState[];
  variables: Record<string, unknown>;
  startedAt: Date;
  finishedAt?: Date;
  duration?: number;
}

export interface NodeExecutionState {
  nodeId: string;
  nodeName: string;
  status: NodeExecutionStatus;
  startedAt?: Date;
  finishedAt?: Date;
  output?: Record<string, unknown>;
  error?: string;
}

export interface WorkflowFilters {
  status?: WorkflowStatus[];
  repositoryId?: string;
  search?: string;
}

// ============================================================================
// 결재(Approval) 도메인
// ============================================================================

export type ApprovalStatus =
  | 'PENDING'
  | 'IN_PROGRESS'
  | 'APPROVED'
  | 'REJECTED'
  | 'CANCELLED'
  | 'EXPIRED';

export type ApprovalTargetType =
  | 'DEPLOYMENT'
  | 'MERGE_REQUEST'
  | 'RELEASE'
  | 'TICKET';

export type ApprovalUrgency = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface ApprovalListItem {
  id: string;
  targetType: ApprovalTargetType;
  targetId: string;
  targetTitle: string;
  targetDescription: string;
  status: ApprovalStatus;
  urgency: ApprovalUrgency;
  requester: UserSummary;
  requestedAt: Date;
  progress: {
    current: number;
    total: number;
    myTurn: boolean;
  };
  dueAt?: Date;
  isOverdue: boolean;
}

export interface ApprovalDetail extends ApprovalListItem {
  target: unknown; // DeploymentDetail | MergeRequestDetail | etc.
  approvalLines: ApprovalLine[];
  comments: ApprovalComment[];
  history: ApprovalHistoryItem[];
  completedAt?: Date;
}

export interface ApprovalLine {
  order: number;
  approverRole: string;
  approvers: ApproverStatus[];
  requiredApprovals: number;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
}

export interface ApproverStatus {
  user: UserSummary;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  respondedAt?: Date;
  comment?: string;
}

export interface ApprovalLineItem {
  order: number;
  approverRole: string;
  approver?: UserSummary;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  respondedAt?: Date;
  comment?: string;
}

export interface ApprovalComment {
  id: string;
  author: UserSummary;
  content: string;
  createdAt: Date;
}

export interface ApprovalHistoryItem {
  action: ApprovalAction;
  actor: UserSummary;
  timestamp: Date;
  details?: string;
}

export type ApprovalAction = 
  | 'CREATED' 
  | 'APPROVED' 
  | 'REJECTED' 
  | 'COMMENTED' 
  | 'ESCALATED';

export interface ApprovalActionForm {
  action: 'APPROVE' | 'REJECT';
  comment?: string;
}

// ============================================================================
// 알림(Notification) 도메인
// ============================================================================

export type NotificationType =
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

export interface NotificationItem {
  id: string;
  type: NotificationType;
  title: string;
  body: string;
  read: boolean;
  createdAt: Date;
  resource?: NotificationResource;
  actions?: NotificationAction[];
}

export interface NotificationResource {
  type: 'TICKET' | 'MR' | 'BUILD' | 'DEPLOYMENT' | 'APPROVAL';
  id: string;
  url: string;
}

export interface NotificationAction {
  label: string;
  action: string;
  primary?: boolean;
}

export interface NotificationSettings {
  channels: NotificationChannels;
  events: NotificationEventSettings;
  quietHours: QuietHoursSettings;
}

export interface NotificationChannels {
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
}

export type NotificationEventSettings = {
  [K in NotificationType]: {
    email: boolean;
    push: boolean;
    slack: boolean;
  };
};

export interface QuietHoursSettings {
  enabled: boolean;
  start: string;
  end: string;
  timezone: string;
  excludeWeekends: boolean;
  excludeUrgent: boolean;
}

// ============================================================================
// 대시보드 도메인
// ============================================================================

export interface DeveloperDashboard {
  myBranches: DeveloperBranchItem[];
  myMergeRequests: MergeRequestListItem[];
  reviewRequests: ReviewRequestItem[];
  recentBuilds: BuildListItem[];
}

export interface DeveloperBranchItem {
  id: string;
  name: string;
  ahead: number;
  behind: number;
  status: 'READY' | 'NEEDS_REBASE' | 'CONFLICT';
  linkedMR?: string;
  lastCommit: Date;
}

export interface ReviewRequestItem {
  id: string;
  number: number;
  title: string;
  author: UserSummary;
  additions: number;
  deletions: number;
  createdAt: Date;
}

export interface PMDashboard {
  pendingApprovals: PendingApprovalItem[];
  projectStatus: ProjectStatusItem[];
  deploymentSchedule: ScheduledDeployment[];
}

export interface PendingApprovalItem {
  id: string;
  type: ApprovalTargetType;
  targetName: string;
  description: string;
  requester: UserSummary;
  requestedAt: Date;
  urgency: ApprovalUrgency;
}

export interface ProjectStatusItem {
  projectId: string;
  projectName: string;
  ticketCounts: {
    inProgress: number;
    testing: number;
    pendingDeploy: number;
  };
  currentProdVersion: string;
}

export interface ScheduledDeployment {
  id: string;
  title: string;
  projectName: string;
  scheduledDate: Date;
  status: 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED';
}

export interface QADashboard {
  environmentStatus: EnvironmentStatusItem[];
  pendingTests: PendingTestItem[];
  recentChanges: RecentChangeItem[];
}

export interface EnvironmentStatusItem {
  environmentId: string;
  name: string;
  currentVersion: string;
  lastDeployedAt: Date;
  status: HealthStatus;
}

export interface PendingTestItem {
  deploymentId: string;
  projectName: string;
  version: string;
  environment: string;
  deployedAt: Date;
  changes: {
    type: TicketType;
    description: string;
    ticketNumber: string;
  }[];
}

export interface RecentChangeItem {
  ticketNumber: string;
  title: string;
  type: TicketType;
  status: TicketStatus;
  assignee: UserSummary;
  updatedAt: Date;
}

