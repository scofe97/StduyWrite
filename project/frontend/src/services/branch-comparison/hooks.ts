import {
  useQuery,
  useMutation,
  type UseQueryOptions,
  type UseMutationOptions,
} from "@tanstack/react-query"
import { branchComparisonApi } from "./api"
import type {
  BranchComparison,
  CommitInfo,
  MergedBranchInfo,
  StaleBranchInfo,
  CleanupResult,
  CompareBranchesParams,
  ListCommitsDiffParams,
  ListMergedBranchesParams,
  ListStaleBranchesParams,
  CleanupBranchesParams,
} from "./types"

// =============================================================================
// Query Keys
// =============================================================================

export const branchComparisonKeys = {
  all: ["branch-comparison"] as const,
  comparisons: () => [...branchComparisonKeys.all, "compare"] as const,
  comparison: (params: CompareBranchesParams) =>
    [...branchComparisonKeys.comparisons(), params] as const,
  commitsDiffs: () => [...branchComparisonKeys.all, "commits-diff"] as const,
  commitsDiff: (params: ListCommitsDiffParams) =>
    [...branchComparisonKeys.commitsDiffs(), params] as const,
  mergedBranches: () => [...branchComparisonKeys.all, "merged"] as const,
  mergedBranchesList: (params: ListMergedBranchesParams) =>
    [...branchComparisonKeys.mergedBranches(), params] as const,
  staleBranches: () => [...branchComparisonKeys.all, "stale"] as const,
  staleBranchesList: (params: ListStaleBranchesParams) =>
    [...branchComparisonKeys.staleBranches(), params] as const,
}

// =============================================================================
// Queries
// =============================================================================

export function useBranchComparison(
  params: CompareBranchesParams,
  options?: Omit<UseQueryOptions<BranchComparison, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: branchComparisonKeys.comparison(params),
    queryFn: () => branchComparisonApi.comparePost(params),
    enabled:
      !!params.connectionId &&
      !!params.namespace &&
      !!params.repository &&
      !!params.base &&
      !!params.compare,
    ...options,
  })
}

export function useCommitsDiff(
  params: ListCommitsDiffParams,
  options?: Omit<
    UseQueryOptions<{ commits: CommitInfo[]; totalCount: number }, Error>,
    "queryKey" | "queryFn"
  >
) {
  return useQuery({
    queryKey: branchComparisonKeys.commitsDiff(params),
    queryFn: () => branchComparisonApi.listCommitsDiffPost(params),
    enabled:
      !!params.connectionId &&
      !!params.namespace &&
      !!params.repository &&
      !!params.base &&
      !!params.compare,
    ...options,
  })
}

export function useMergedBranches(
  params: ListMergedBranchesParams,
  options?: Omit<UseQueryOptions<MergedBranchInfo[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: branchComparisonKeys.mergedBranchesList(params),
    queryFn: () => branchComparisonApi.listMergedBranchesPost(params),
    enabled: !!params.connectionId && !!params.namespace && !!params.repository,
    ...options,
  })
}

export function useStaleBranches(
  params: ListStaleBranchesParams,
  options?: Omit<UseQueryOptions<StaleBranchInfo[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: branchComparisonKeys.staleBranchesList(params),
    queryFn: () => branchComparisonApi.listStaleBranchesPost(params),
    enabled: !!params.connectionId && !!params.namespace && !!params.repository,
    ...options,
  })
}

// =============================================================================
// Mutations
// =============================================================================

export function useCleanupBranches(
  options?: UseMutationOptions<CleanupResult, Error, CleanupBranchesParams>
) {
  return useMutation({
    mutationFn: branchComparisonApi.cleanup,
    ...options,
  })
}
