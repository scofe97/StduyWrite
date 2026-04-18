import {
  useQuery,
  useMutation,
  useQueryClient,
  type UseQueryOptions,
  type UseMutationOptions,
} from "@tanstack/react-query"
import { branchApi } from "./api"
import type {
  Branch,
  BranchType,
  BranchStatus,
  CreateBranchParams,
  UpdateBranchParams,
  UpdateBranchStatusParams,
  UpdateBranchCommitParams,
} from "./types"

// =============================================================================
// Query Keys
// =============================================================================

export const branchKeys = {
  all: ["branches"] as const,
  lists: () => [...branchKeys.all, "list"] as const,
  listByRepository: (repositoryId: string) =>
    [...branchKeys.lists(), "repository", repositoryId] as const,
  listByStatus: (repositoryId: string, status: BranchStatus) =>
    [...branchKeys.lists(), "repository", repositoryId, "status", status] as const,
  listByType: (repositoryId: string, type: BranchType) =>
    [...branchKeys.lists(), "repository", repositoryId, "type", type] as const,
  details: () => [...branchKeys.all, "detail"] as const,
  detail: (id: string) => [...branchKeys.details(), id] as const,
}

// =============================================================================
// Queries
// =============================================================================

export function useBranch(
  id: string,
  options?: Omit<UseQueryOptions<Branch, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: branchKeys.detail(id),
    queryFn: () => branchApi.get(id),
    enabled: !!id,
    ...options,
  })
}

export function useBranchesByRepository(
  repositoryId: string,
  options?: Omit<UseQueryOptions<Branch[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: branchKeys.listByRepository(repositoryId),
    queryFn: () => branchApi.getByRepositoryId(repositoryId),
    enabled: !!repositoryId,
    ...options,
  })
}

export function useBranchesByStatus(
  repositoryId: string,
  status: BranchStatus,
  options?: Omit<UseQueryOptions<Branch[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: branchKeys.listByStatus(repositoryId, status),
    queryFn: () => branchApi.getByStatus(repositoryId, status),
    enabled: !!repositoryId,
    ...options,
  })
}

export function useBranchesByType(
  repositoryId: string,
  type: BranchType,
  options?: Omit<UseQueryOptions<Branch[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: branchKeys.listByType(repositoryId, type),
    queryFn: () => branchApi.getByType(repositoryId, type),
    enabled: !!repositoryId,
    ...options,
  })
}

// =============================================================================
// Mutations
// =============================================================================

export function useCreateBranch(
  options?: UseMutationOptions<Branch, Error, CreateBranchParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: branchApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: branchKeys.lists() })
      queryClient.setQueryData(branchKeys.detail(data.id), data)
    },
    ...options,
  })
}

export function useUpdateBranch(
  options?: UseMutationOptions<Branch, Error, UpdateBranchParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: branchApi.update,
    onSuccess: (data, variables) => {
      queryClient.setQueryData(branchKeys.detail(variables.id), data)
      queryClient.invalidateQueries({ queryKey: branchKeys.lists() })
    },
    ...options,
  })
}

export function useDeleteBranch(
  options?: UseMutationOptions<void, Error, string>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: branchApi.delete,
    onSuccess: (_, id) => {
      queryClient.removeQueries({ queryKey: branchKeys.detail(id) })
      queryClient.invalidateQueries({ queryKey: branchKeys.lists() })
    },
    ...options,
  })
}

export function useUpdateBranchStatus(
  options?: UseMutationOptions<Branch, Error, UpdateBranchStatusParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, status }) => branchApi.updateStatus(id, status),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(branchKeys.detail(variables.id), data)
      queryClient.invalidateQueries({ queryKey: branchKeys.lists() })
    },
    ...options,
  })
}

export function useUpdateBranchCommit(
  options?: UseMutationOptions<Branch, Error, UpdateBranchCommitParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, commitSha }) => branchApi.updateCommit(id, commitSha),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(branchKeys.detail(variables.id), data)
      queryClient.invalidateQueries({ queryKey: branchKeys.lists() })
    },
    ...options,
  })
}
