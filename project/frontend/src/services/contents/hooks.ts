import { useQuery, type UseQueryOptions } from "@tanstack/react-query"
import { contentsApi } from "./api"
import type { TreeEntry, ContentEntry, GetTreeParams, GetContentsParams } from "./types"

// =============================================================================
// Query Keys
// =============================================================================

export const contentsKeys = {
  all: ["contents"] as const,
  trees: () => [...contentsKeys.all, "tree"] as const,
  tree: (params: GetTreeParams) => [...contentsKeys.trees(), params] as const,
  files: () => [...contentsKeys.all, "file"] as const,
  file: (params: GetContentsParams) => [...contentsKeys.files(), params] as const,
}

// =============================================================================
// Queries
// =============================================================================

export function useTree(
  params: GetTreeParams,
  options?: Omit<UseQueryOptions<TreeEntry[], Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: contentsKeys.tree(params),
    queryFn: () => contentsApi.getTreePost(params),
    enabled: !!params.connectionId && !!params.namespace && !!params.repository,
    ...options,
  })
}

export function useContents(
  params: GetContentsParams,
  options?: Omit<UseQueryOptions<ContentEntry, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: contentsKeys.file(params),
    queryFn: () => contentsApi.getContentsPost(params),
    enabled: !!params.connectionId && !!params.namespace && !!params.repository,
    ...options,
  })
}

export function useFileContent(
  params: GetContentsParams,
  options?: Omit<UseQueryOptions<ContentEntry, Error>, "queryKey" | "queryFn">
) {
  return useContents(params, options)
}
