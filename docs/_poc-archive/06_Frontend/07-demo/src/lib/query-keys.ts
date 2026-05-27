/**
 * TPS Query Key Factory
 * 
 * TanStack Query v5용 Query Key Factory 패턴 구현
 * @see https://tanstack.com/query/latest/docs/react/guides/query-keys
 */

import type {
  ProjectFilters,
  TicketFilters,
  BranchFilters,
  MRFilters,
  BuildFilters,
  DeploymentFilters,
  WorkflowFilters,
} from './query-filters';

// ============================================================================
// Query Key Factory
// ============================================================================

export const queryKeys = {
  // -------------------------------------------------------------------------
  // 대시보드
  // -------------------------------------------------------------------------
  dashboard: {
    all: ['dashboard'] as const,
    byRole: (role: string) => [...queryKeys.dashboard.all, role] as const,
    developer: () => [...queryKeys.dashboard.all, 'developer'] as const,
    pm: () => [...queryKeys.dashboard.all, 'pm'] as const,
    qa: () => [...queryKeys.dashboard.all, 'qa'] as const,
    admin: () => [...queryKeys.dashboard.all, 'admin'] as const,
  },

  // -------------------------------------------------------------------------
  // 프로젝트
  // -------------------------------------------------------------------------
  projects: {
    all: ['projects'] as const,
    lists: () => [...queryKeys.projects.all, 'list'] as const,
    list: (filters?: ProjectFilters) => 
      [...queryKeys.projects.lists(), filters ?? {}] as const,
    details: () => [...queryKeys.projects.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.projects.details(), id] as const,
    connections: (projectId: string) => 
      [...queryKeys.projects.detail(projectId), 'connections'] as const,
    repositories: (projectId: string) => 
      [...queryKeys.projects.detail(projectId), 'repositories'] as const,
    environments: (projectId: string) => 
      [...queryKeys.projects.detail(projectId), 'environments'] as const,
    members: (projectId: string) => 
      [...queryKeys.projects.detail(projectId), 'members'] as const,
  },

  // -------------------------------------------------------------------------
  // 티켓
  // -------------------------------------------------------------------------
  tickets: {
    all: ['tickets'] as const,
    lists: () => [...queryKeys.tickets.all, 'list'] as const,
    list: (filters?: TicketFilters) => 
      [...queryKeys.tickets.lists(), filters ?? {}] as const,
    kanban: (projectId: string) => 
      [...queryKeys.tickets.all, 'kanban', projectId] as const,
    details: () => [...queryKeys.tickets.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.tickets.details(), id] as const,
    history: (ticketId: string) => 
      [...queryKeys.tickets.detail(ticketId), 'history'] as const,
    comments: (ticketId: string) => 
      [...queryKeys.tickets.detail(ticketId), 'comments'] as const,
    linkedItems: (ticketId: string) => 
      [...queryKeys.tickets.detail(ticketId), 'linkedItems'] as const,
  },

  // -------------------------------------------------------------------------
  // 저장소
  // -------------------------------------------------------------------------
  repositories: {
    all: ['repositories'] as const,
    lists: () => [...queryKeys.repositories.all, 'list'] as const,
    list: (projectId: string) => 
      [...queryKeys.repositories.lists(), projectId] as const,
    details: () => [...queryKeys.repositories.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.repositories.details(), id] as const,
    branchStrategy: (repoId: string) => 
      [...queryKeys.repositories.detail(repoId), 'branchStrategy'] as const,
  },

  // -------------------------------------------------------------------------
  // 브랜치
  // -------------------------------------------------------------------------
  branches: {
    all: ['branches'] as const,
    byRepo: (repoId: string) => [...queryKeys.branches.all, repoId] as const,
    lists: (repoId: string) => 
      [...queryKeys.branches.byRepo(repoId), 'list'] as const,
    list: (repoId: string, filters?: BranchFilters) => 
      [...queryKeys.branches.lists(repoId), filters ?? {}] as const,
    details: (repoId: string) => 
      [...queryKeys.branches.byRepo(repoId), 'detail'] as const,
    detail: (repoId: string, branchName: string) => 
      [...queryKeys.branches.details(repoId), branchName] as const,
  },

  // -------------------------------------------------------------------------
  // Merge Request
  // -------------------------------------------------------------------------
  mergeRequests: {
    all: ['mergeRequests'] as const,
    lists: () => [...queryKeys.mergeRequests.all, 'list'] as const,
    list: (filters?: MRFilters) => 
      [...queryKeys.mergeRequests.lists(), filters ?? {}] as const,
    details: () => [...queryKeys.mergeRequests.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.mergeRequests.details(), id] as const,
    reviews: (mrId: string) => 
      [...queryKeys.mergeRequests.detail(mrId), 'reviews'] as const,
    commits: (mrId: string) => 
      [...queryKeys.mergeRequests.detail(mrId), 'commits'] as const,
    changedFiles: (mrId: string) => 
      [...queryKeys.mergeRequests.detail(mrId), 'changedFiles'] as const,
    statusChecks: (mrId: string) => 
      [...queryKeys.mergeRequests.detail(mrId), 'statusChecks'] as const,
  },

  // -------------------------------------------------------------------------
  // 빌드
  // -------------------------------------------------------------------------
  builds: {
    all: ['builds'] as const,
    lists: () => [...queryKeys.builds.all, 'list'] as const,
    list: (filters?: BuildFilters) => 
      [...queryKeys.builds.lists(), filters ?? {}] as const,
    details: () => [...queryKeys.builds.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.builds.details(), id] as const,
    logs: (buildId: string) => 
      [...queryKeys.builds.detail(buildId), 'logs'] as const,
    steps: (buildId: string) => 
      [...queryKeys.builds.detail(buildId), 'steps'] as const,
    artifacts: (buildId: string) => 
      [...queryKeys.builds.detail(buildId), 'artifacts'] as const,
    testResults: (buildId: string) => 
      [...queryKeys.builds.detail(buildId), 'testResults'] as const,
  },

  // -------------------------------------------------------------------------
  // 환경 & 배포
  // -------------------------------------------------------------------------
  environments: {
    all: ['environments'] as const,
    lists: () => [...queryKeys.environments.all, 'list'] as const,
    list: (projectId: string) => 
      [...queryKeys.environments.lists(), projectId] as const,
    overview: (projectId: string) => 
      [...queryKeys.environments.all, 'overview', projectId] as const,
    details: () => [...queryKeys.environments.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.environments.details(), id] as const,
  },

  deployments: {
    all: ['deployments'] as const,
    lists: () => [...queryKeys.deployments.all, 'list'] as const,
    list: (filters?: DeploymentFilters) => 
      [...queryKeys.deployments.lists(), filters ?? {}] as const,
    byEnvironment: (envId: string) => 
      [...queryKeys.deployments.all, 'byEnv', envId] as const,
    details: () => [...queryKeys.deployments.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.deployments.details(), id] as const,
    tasks: (deploymentId: string) => 
      [...queryKeys.deployments.detail(deploymentId), 'tasks'] as const,
    changes: (deploymentId: string) => 
      [...queryKeys.deployments.detail(deploymentId), 'changes'] as const,
  },

  // -------------------------------------------------------------------------
  // 워크플로우
  // -------------------------------------------------------------------------
  workflows: {
    all: ['workflows'] as const,
    lists: () => [...queryKeys.workflows.all, 'list'] as const,
    list: (filters?: WorkflowFilters) => 
      [...queryKeys.workflows.lists(), filters ?? {}] as const,
    details: () => [...queryKeys.workflows.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.workflows.details(), id] as const,
    definition: (workflowId: string) => 
      [...queryKeys.workflows.detail(workflowId), 'definition'] as const,
    executions: (workflowId: string) => 
      [...queryKeys.workflows.detail(workflowId), 'executions'] as const,
    execution: (workflowId: string, executionId: string) => 
      [...queryKeys.workflows.executions(workflowId), executionId] as const,
  },

  // -------------------------------------------------------------------------
  // 결재
  // -------------------------------------------------------------------------
  approvals: {
    all: ['approvals'] as const,
    pending: () => [...queryKeys.approvals.all, 'pending'] as const,
    myPending: () => [...queryKeys.approvals.pending(), 'mine'] as const,
    lists: () => [...queryKeys.approvals.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) => 
      [...queryKeys.approvals.lists(), filters ?? {}] as const,
    details: () => [...queryKeys.approvals.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.approvals.details(), id] as const,
    history: (approvalId: string) => 
      [...queryKeys.approvals.detail(approvalId), 'history'] as const,
  },

  // -------------------------------------------------------------------------
  // 알림
  // -------------------------------------------------------------------------
  notifications: {
    all: ['notifications'] as const,
    lists: () => [...queryKeys.notifications.all, 'list'] as const,
    list: (filters?: { read?: boolean }) => 
      [...queryKeys.notifications.lists(), filters ?? {}] as const,
    unreadCount: () => [...queryKeys.notifications.all, 'unreadCount'] as const,
    settings: () => [...queryKeys.notifications.all, 'settings'] as const,
  },

  // -------------------------------------------------------------------------
  // 사용자
  // -------------------------------------------------------------------------
  users: {
    all: ['users'] as const,
    current: () => [...queryKeys.users.all, 'current'] as const,
    profile: () => [...queryKeys.users.all, 'profile'] as const,
    lists: () => [...queryKeys.users.all, 'list'] as const,
    list: (filters?: { search?: string; role?: string }) => 
      [...queryKeys.users.lists(), filters ?? {}] as const,
    details: () => [...queryKeys.users.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.users.details(), id] as const,
  },
} as const;

// ============================================================================
// Mutation Key Factory (선택적)
// ============================================================================

export const mutationKeys = {
  tickets: {
    create: ['tickets', 'create'] as const,
    update: (id: string) => ['tickets', 'update', id] as const,
    delete: (id: string) => ['tickets', 'delete', id] as const,
    changeStatus: (id: string) => ['tickets', 'changeStatus', id] as const,
  },

  branches: {
    create: ['branches', 'create'] as const,
    delete: (repoId: string, name: string) => 
      ['branches', 'delete', repoId, name] as const,
  },

  mergeRequests: {
    create: ['mergeRequests', 'create'] as const,
    update: (id: string) => ['mergeRequests', 'update', id] as const,
    merge: (id: string) => ['mergeRequests', 'merge', id] as const,
    close: (id: string) => ['mergeRequests', 'close', id] as const,
    addReview: (id: string) => ['mergeRequests', 'addReview', id] as const,
  },

  builds: {
    trigger: ['builds', 'trigger'] as const,
    cancel: (id: string) => ['builds', 'cancel', id] as const,
    retry: (id: string) => ['builds', 'retry', id] as const,
  },

  deployments: {
    request: ['deployments', 'request'] as const,
    cancel: (id: string) => ['deployments', 'cancel', id] as const,
    rollback: (id: string) => ['deployments', 'rollback', id] as const,
  },

  workflows: {
    create: ['workflows', 'create'] as const,
    update: (id: string) => ['workflows', 'update', id] as const,
    delete: (id: string) => ['workflows', 'delete', id] as const,
    execute: (id: string) => ['workflows', 'execute', id] as const,
    cancelExecution: (executionId: string) => 
      ['workflows', 'cancelExecution', executionId] as const,
  },

  approvals: {
    approve: (id: string) => ['approvals', 'approve', id] as const,
    reject: (id: string) => ['approvals', 'reject', id] as const,
  },

  notifications: {
    markAsRead: (id: string) => ['notifications', 'markAsRead', id] as const,
    markAllAsRead: ['notifications', 'markAllAsRead'] as const,
    updateSettings: ['notifications', 'updateSettings'] as const,
  },
} as const;

// ============================================================================
// Type Exports
// ============================================================================

export type QueryKeys = typeof queryKeys;
export type MutationKeys = typeof mutationKeys;

