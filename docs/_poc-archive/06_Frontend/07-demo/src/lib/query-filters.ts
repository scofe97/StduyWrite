/**
 * TPS Query Filters
 * 
 * API 요청에 사용되는 필터 타입 정의
 */

import type {
  ProjectStatus,
  TicketStatus,
  TicketType,
  TicketPriority,
  BranchType,
  BranchStatus,
  MergeRequestStatus,
  BuildStatus,
  BuildTrigger,
  DeploymentStatus,
  WorkflowStatus,
} from '../types/tps-domain';

// ============================================================================
// 프로젝트 필터
// ============================================================================

export interface ProjectFilters {
  status?: ProjectStatus;
  search?: string;
}

// ============================================================================
// 티켓 필터
// ============================================================================

export interface TicketFilters {
  status?: TicketStatus[];
  type?: TicketType[];
  priority?: TicketPriority[];
  assigneeId?: string;
  reporterId?: string;
  projectId?: string;
  repositoryId?: string;
  search?: string;
  createdFrom?: Date;
  createdTo?: Date;
  dueDateFrom?: Date;
  dueDateTo?: Date;
}

// ============================================================================
// 브랜치 필터
// ============================================================================

export interface BranchFilters {
  type?: BranchType[];
  status?: BranchStatus[];
  search?: string;
  hasLinkedTicket?: boolean;
  hasLinkedMR?: boolean;
}

// ============================================================================
// Merge Request 필터
// ============================================================================

export interface MRFilters {
  status?: MergeRequestStatus[];
  authorId?: string;
  reviewerId?: string;
  assigneeId?: string;
  repositoryId?: string;
  targetBranch?: string;
  search?: string;
  createdFrom?: Date;
  createdTo?: Date;
}

// ============================================================================
// 빌드 필터
// ============================================================================

export interface BuildFilters {
  status?: BuildStatus[];
  repositoryId?: string;
  branch?: string;
  trigger?: BuildTrigger[];
  triggeredById?: string;
  createdFrom?: Date;
  createdTo?: Date;
}

// ============================================================================
// 배포 필터
// ============================================================================

export interface DeploymentFilters {
  environmentId?: string;
  status?: DeploymentStatus[];
  repositoryId?: string;
  requestedById?: string;
  createdFrom?: Date;
  createdTo?: Date;
}

// ============================================================================
// 워크플로우 필터
// ============================================================================

export interface WorkflowFilters {
  status?: WorkflowStatus[];
  repositoryId?: string;
  projectId?: string;
  search?: string;
}

// ============================================================================
// 정렬 옵션
// ============================================================================

export interface SortOption {
  field: string;
  direction: 'ASC' | 'DESC';
}

// ============================================================================
// 페이지네이션 옵션
// ============================================================================

export interface PaginationOptions {
  page?: number;
  size?: number;
  sort?: SortOption[];
}

// ============================================================================
// 통합 필터 타입 (제네릭)
// ============================================================================

export interface ListQueryOptions<TFilters = Record<string, unknown>> {
  filters?: TFilters;
  pagination?: PaginationOptions;
}

