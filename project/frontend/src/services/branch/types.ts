// =============================================================================
// Enums
// =============================================================================

export type BranchType =
  | "MAIN"
  | "DEVELOP"
  | "FEATURE"
  | "RELEASE"
  | "HOTFIX"
  | "BUGFIX"
  | "OTHER"

export type BranchStatus = "ACTIVE" | "MERGED" | "STALE" | "DELETED"

// =============================================================================
// Branch 기본 타입
// =============================================================================

export interface Branch {
  id: string
  repositoryId: string
  name: string
  branchType: BranchType
  status: BranchStatus
  isProtected: boolean
  commitSha: string | null
  metadata: Record<string, unknown> | null
  createdAt: string
  updatedAt: string
}

// =============================================================================
// API 요청 타입
// =============================================================================

export interface CreateBranchParams {
  repositoryId: string
  name: string
  branchType: BranchType
  sourceBranchName: string
  isProtected?: boolean
  metadata?: Record<string, unknown>
}

export interface UpdateBranchParams {
  id: string
  name?: string
  branchType?: BranchType
  isProtected?: boolean
  metadata?: Record<string, unknown>
}

export interface UpdateBranchStatusParams {
  id: string
  status: BranchStatus
}

export interface UpdateBranchCommitParams {
  id: string
  commitSha: string
}
