import type { ProviderType } from "../connection/types"

// =============================================================================
// Enums
// =============================================================================

export type BranchStrategyType = "GIT_FLOW" | "GITHUB_FLOW" | "TRUNK_BASED"

// =============================================================================
// Repository 기본 타입
// =============================================================================

export interface Repository {
  id: string
  projectId: string
  connectionId: string
  name: string
  gitUrl: string
  defaultBranch: string
  strategyType: BranchStrategyType
  providerType: ProviderType
  namespace: string
  repositoryName: string
  metadata: Record<string, unknown> | null
  createdAt: string
  updatedAt: string
}

// =============================================================================
// API 요청 타입
// =============================================================================

export interface CreateRepositoryParams {
  projectId: string
  connectionId: string
  name: string
  gitUrl: string
  defaultBranch?: string
  strategyType?: BranchStrategyType
  metadata?: Record<string, unknown>
}

export interface UpdateRepositoryParams {
  id: string
  name?: string
  defaultBranch?: string
  strategyType?: BranchStrategyType
  metadata?: Record<string, unknown>
}
