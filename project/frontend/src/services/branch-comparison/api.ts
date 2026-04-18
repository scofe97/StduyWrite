import apiClient from "@/api/client"
import type {
  BranchComparison,
  CommitInfo,
  MergedBranchInfo,
  StaleBranchInfo,
  CleanupResult,
  CommitsDiffData,
  CompareBranchesParams,
  ListCommitsDiffParams,
  ListMergedBranchesParams,
  ListStaleBranchesParams,
  CleanupBranchesParams,
} from "./types"

const BASE_PATH = "/v1/branches"

// =============================================================================
// Branch Comparison (GET)
// =============================================================================

export async function compareBranches(
  params: CompareBranchesParams
): Promise<BranchComparison> {
  const { connectionId, namespace, repository, base, compare } = params
  const response = await apiClient.get<BranchComparison>(
    `${BASE_PATH}/${connectionId}/compare`,
    { params: { namespace, repository, base, compare } }
  )
  return response.data
}

export async function listCommitsDiff(
  params: ListCommitsDiffParams
): Promise<{ commits: CommitInfo[]; totalCount: number }> {
  const { connectionId, namespace, repository, base, compare, page = 1, perPage = 30 } = params
  const response = await apiClient.get<CommitsDiffData>(
    `${BASE_PATH}/${connectionId}/compare/commits`,
    { params: { namespace, repository, base, compare, page, perPage } }
  )
  return response.data
}

export async function listMergedBranches(
  params: ListMergedBranchesParams
): Promise<MergedBranchInfo[]> {
  const { connectionId, namespace, repository, base = "main" } = params
  const response = await apiClient.get<{ branches: MergedBranchInfo[] }>(
    `${BASE_PATH}/${connectionId}/merged`,
    { params: { namespace, repository, base } }
  )
  return response.data.branches
}

export async function listStaleBranches(
  params: ListStaleBranchesParams
): Promise<StaleBranchInfo[]> {
  const { connectionId, namespace, repository, staleDays = 30 } = params
  const response = await apiClient.get<{ branches: StaleBranchInfo[] }>(
    `${BASE_PATH}/${connectionId}/stale`,
    { params: { namespace, repository, staleDays } }
  )
  return response.data.branches
}

// =============================================================================
// Branch Comparison (POST)
// =============================================================================

export async function compareBranchesPost(
  params: CompareBranchesParams
): Promise<BranchComparison> {
  const response = await apiClient.post<BranchComparison>(`${BASE_PATH}/compare`, params)
  return response.data
}

export async function listCommitsDiffPost(
  params: ListCommitsDiffParams
): Promise<{ commits: CommitInfo[]; totalCount: number }> {
  const response = await apiClient.post<CommitsDiffData>(`${BASE_PATH}/compare/commits`, params)
  return response.data
}

export async function listMergedBranchesPost(
  params: ListMergedBranchesParams
): Promise<MergedBranchInfo[]> {
  const response = await apiClient.post<{ branches: MergedBranchInfo[] }>(`${BASE_PATH}/merged`, params)
  return response.data.branches
}

export async function listStaleBranchesPost(
  params: ListStaleBranchesParams
): Promise<StaleBranchInfo[]> {
  const response = await apiClient.post<{ branches: StaleBranchInfo[] }>(`${BASE_PATH}/stale`, params)
  return response.data.branches
}

// =============================================================================
// Branch Cleanup
// =============================================================================

export async function cleanupBranches(
  params: CleanupBranchesParams
): Promise<CleanupResult> {
  const response = await apiClient.post<CleanupResult>(`${BASE_PATH}/cleanup`, params)
  return response.data
}

// =============================================================================
// Export
// =============================================================================

export const branchComparisonApi = {
  compare: compareBranches,
  comparePost: compareBranchesPost,
  listCommitsDiff,
  listCommitsDiffPost,
  listMergedBranches,
  listMergedBranchesPost,
  listStaleBranches,
  listStaleBranchesPost,
  cleanup: cleanupBranches,
}
