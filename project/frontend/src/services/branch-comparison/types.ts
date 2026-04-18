// =============================================================================
// Enums
// =============================================================================

export type MergeableState = "MERGEABLE" | "CONFLICTING" | "UNKNOWN"

export type SuggestedAction =
  | "CREATE_MR"
  | "REBASE"
  | "MERGE_BASE"
  | "RESOLVE_CONFLICTS"
  | "UP_TO_DATE"

// =============================================================================
// Branch Comparison 타입
// =============================================================================

export interface BranchComparison {
  baseBranch: string
  compareBranch: string
  aheadBy: number
  behindBy: number
  mergeableState: MergeableState
  mergeStatus: string
  suggestedAction: SuggestedAction
  diffStat: DiffStat
}

export interface DiffStat {
  additions: number
  deletions: number
  changedFiles: number
}

export interface CommitInfo {
  sha: string
  message: string
  authorName: string
  authorEmail: string
  authoredAt: string
  committedAt: string
}

export interface MergedBranchInfo {
  name: string
  mergedAt: string | null
  mergedBy: string | null
  lastCommit: string
  isProtected: boolean
}

export interface StaleBranchInfo {
  name: string
  lastCommitAt: string
  lastCommitSha: string
  lastCommitAuthor: string
  staleDays: number
  isProtected: boolean
}

export interface CleanupResult {
  deleted: string[]
  skipped: CleanupSkipped[]
  dryRun: boolean
  totalDeleted: number
  totalSkipped: number
}

export interface CleanupSkipped {
  branch: string
  reason: string
}

// =============================================================================
// API 요청 타입
// =============================================================================

export interface CompareBranchesParams {
  connectionId: string
  namespace: string
  repository: string
  base: string
  compare: string
}

export interface ListCommitsDiffParams {
  connectionId: string
  namespace: string
  repository: string
  base: string
  compare: string
  page?: number
  perPage?: number
}

export interface ListMergedBranchesParams {
  connectionId: string
  namespace: string
  repository: string
  base?: string
}

export interface ListStaleBranchesParams {
  connectionId: string
  namespace: string
  repository: string
  staleDays?: number
}

export interface CleanupBranchesParams {
  connectionId: string
  namespace: string
  repository: string
  dryRun?: boolean
  excludePatterns?: string[]
  staleDays?: number
  includeMerged?: boolean
  includeStale?: boolean
}

// =============================================================================
// API 응답 내부 타입
// =============================================================================

export interface CommitsDiffData {
  commits: CommitInfo[]
  totalCount: number
}

export interface BranchesData {
  branches: MergedBranchInfo[] | StaleBranchInfo[]
}
