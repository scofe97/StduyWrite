import {
  useQuery,
  useMutation,
  useQueryClient,
  type UseQueryOptions,
  type UseMutationOptions,
} from "@tanstack/react-query"
import { repositoryApi } from "./api"
import type {
  Repository,
  CreateRepositoryParams,
  UpdateRepositoryParams,
} from "./types"

// =============================================================================
// Query Keys
// =============================================================================

export const repositoryKeys = {
  all: ["repositories"] as const,
  lists: () => [...repositoryKeys.all, "list"] as const,
  listByProject: (projectId: string) =>
    [...repositoryKeys.lists(), "project", projectId] as const,
  listByConnection: (connectionId: string) =>
    [...repositoryKeys.lists(), "connection", connectionId] as const,
  details: () => [...repositoryKeys.all, "detail"] as const,
  detail: (id: string) => [...repositoryKeys.details(), id] as const,
}

// =============================================================================
// Queries
// =============================================================================

export function useRepository(
  id: string,
  options?: Omit<UseQueryOptions<Repository, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: repositoryKeys.detail(id),
    queryFn: () => repositoryApi.get(id),
    enabled: !!id,
    ...options,
  })
}

export function useRepositoriesByProject(
  projectId: string,
  options?: Omit<UseQueryOptions<Repository[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: repositoryKeys.listByProject(projectId),
    queryFn: () => repositoryApi.getByProjectId(projectId),
    enabled: !!projectId,
    ...options,
  })
}

export function useRepositoriesByConnection(
  connectionId: string,
  options?: Omit<UseQueryOptions<Repository[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: repositoryKeys.listByConnection(connectionId),
    queryFn: () => repositoryApi.getByConnectionId(connectionId),
    enabled: !!connectionId,
    ...options,
  })
}

// =============================================================================
// Mutations
// =============================================================================

export function useCreateRepository(
  options?: UseMutationOptions<Repository, Error, CreateRepositoryParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: repositoryApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: repositoryKeys.lists() })
      queryClient.setQueryData(repositoryKeys.detail(data.id), data)
    },
    ...options,
  })
}

export function useUpdateRepository(
  options?: UseMutationOptions<Repository, Error, UpdateRepositoryParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: repositoryApi.update,
    onSuccess: (data, variables) => {
      queryClient.setQueryData(repositoryKeys.detail(variables.id), data)
      queryClient.invalidateQueries({ queryKey: repositoryKeys.lists() })
    },
    ...options,
  })
}

export function useDeleteRepository(
  options?: UseMutationOptions<void, Error, string>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: repositoryApi.delete,
    onSuccess: (_, id) => {
      queryClient.removeQueries({ queryKey: repositoryKeys.detail(id) })
      queryClient.invalidateQueries({ queryKey: repositoryKeys.lists() })
    },
    ...options,
  })
}

export function useSyncRepository(
  options?: UseMutationOptions<Repository, Error, string>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: repositoryApi.sync,
    onSuccess: (data, id) => {
      queryClient.setQueryData(repositoryKeys.detail(id), data)
      queryClient.invalidateQueries({ queryKey: repositoryKeys.lists() })
    },
    ...options,
  })
}
