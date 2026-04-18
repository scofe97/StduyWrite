import {
  useQuery,
  useMutation,
  useQueryClient,
  type UseQueryOptions,
  type UseMutationOptions,
} from "@tanstack/react-query"
import { connectionApi } from "./api"
import type {
  Connection,
  CreateConnectionParams,
  UpdateConnectionParams,
  ProviderType,
} from "./types"

// =============================================================================
// Query Keys
// =============================================================================

export const connectionKeys = {
  all: ["connections"] as const,
  lists: () => [...connectionKeys.all, "list"] as const,
  listByProject: (projectId: string) =>
    [...connectionKeys.lists(), "project", projectId] as const,
  listByProvider: (providerType: ProviderType) =>
    [...connectionKeys.lists(), "provider", providerType] as const,
  listActive: () => [...connectionKeys.lists(), "active"] as const,
  details: () => [...connectionKeys.all, "detail"] as const,
  detail: (id: string) => [...connectionKeys.details(), id] as const,
}

// =============================================================================
// Queries
// =============================================================================

export function useConnection(
  id: string,
  options?: Omit<UseQueryOptions<Connection, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: connectionKeys.detail(id),
    queryFn: () => connectionApi.get(id),
    enabled: !!id,
    ...options,
  })
}

export function useConnectionsByProject(
  projectId: string,
  options?: Omit<UseQueryOptions<Connection[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: connectionKeys.listByProject(projectId),
    queryFn: () => connectionApi.getByProjectId(projectId),
    enabled: !!projectId,
    ...options,
  })
}

export function useConnectionsByProvider(
  providerType: ProviderType,
  options?: Omit<UseQueryOptions<Connection[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: connectionKeys.listByProvider(providerType),
    queryFn: () => connectionApi.getByProviderType(providerType),
    ...options,
  })
}

export function useActiveConnections(
  options?: Omit<UseQueryOptions<Connection[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: connectionKeys.listActive(),
    queryFn: () => connectionApi.getActive(),
    ...options,
  })
}

// =============================================================================
// Mutations
// =============================================================================

export function useCreateConnection(
  options?: UseMutationOptions<Connection, Error, CreateConnectionParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: connectionApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: connectionKeys.lists() })
      queryClient.setQueryData(connectionKeys.detail(data.id), data)
    },
    ...options,
  })
}

export function useUpdateConnection(
  options?: UseMutationOptions<Connection, Error, UpdateConnectionParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: connectionApi.update,
    onSuccess: (data, variables) => {
      queryClient.setQueryData(connectionKeys.detail(variables.id), data)
      queryClient.invalidateQueries({ queryKey: connectionKeys.lists() })
    },
    ...options,
  })
}

export function useDeleteConnection(
  options?: UseMutationOptions<void, Error, string>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: connectionApi.delete,
    onSuccess: (_, id) => {
      queryClient.removeQueries({ queryKey: connectionKeys.detail(id) })
      queryClient.invalidateQueries({ queryKey: connectionKeys.lists() })
    },
    ...options,
  })
}

export function useActivateConnection(
  options?: UseMutationOptions<Connection, Error, string>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: connectionApi.activate,
    onSuccess: (data, id) => {
      queryClient.setQueryData(connectionKeys.detail(id), data)
      queryClient.invalidateQueries({ queryKey: connectionKeys.lists() })
    },
    ...options,
  })
}

export function useDeactivateConnection(
  options?: UseMutationOptions<Connection, Error, string>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: connectionApi.deactivate,
    onSuccess: (data, id) => {
      queryClient.setQueryData(connectionKeys.detail(id), data)
      queryClient.invalidateQueries({ queryKey: connectionKeys.lists() })
    },
    ...options,
  })
}

export function useTestConnection(
  options?: UseMutationOptions<boolean, Error, string>
) {
  return useMutation({
    mutationFn: connectionApi.test,
    ...options,
  })
}
