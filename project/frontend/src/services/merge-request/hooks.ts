import {
  useQuery,
  useMutation,
  useQueryClient,
  type UseQueryOptions,
  type UseMutationOptions,
} from "@tanstack/react-query"
import { mergeRequestApi } from "./api"
import type {
  ListMergeRequestsParams,
  ListMergeRequestsResponse,
  GetMergeRequestParams,
  MergeRequestResponse,
  CreateMergeRequestParams,
  UpdateMergeRequestParams,
  MergeMergeRequestParams,
  MergeResponse,
  ListCommentsParams,
  ListCommentsResponse,
  CreateCommentParams,
  CommentResponse,
  UpdateCommentParams,
  DeleteCommentParams,
  ListReviewsParams,
  ListReviewsResponse,
  SubmitReviewParams,
  ReviewResponse,
  DiffResponse,
} from "./types"

// =============================================================================
// Query Keys
// =============================================================================

export const mergeRequestKeys = {
  all: ["merge-requests"] as const,
  lists: () => [...mergeRequestKeys.all, "list"] as const,
  list: (params: ListMergeRequestsParams) => [...mergeRequestKeys.lists(), params] as const,
  details: () => [...mergeRequestKeys.all, "detail"] as const,
  detail: (params: GetMergeRequestParams) => [...mergeRequestKeys.details(), params] as const,
  comments: (params: ListCommentsParams) => [...mergeRequestKeys.all, "comments", params] as const,
  reviews: (params: ListReviewsParams) => [...mergeRequestKeys.all, "reviews", params] as const,
  diff: (params: GetMergeRequestParams) => [...mergeRequestKeys.all, "diff", params] as const,
}

// =============================================================================
// Queries
// =============================================================================

export function useMergeRequests(
  params: ListMergeRequestsParams,
  options?: Omit<UseQueryOptions<ListMergeRequestsResponse, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: mergeRequestKeys.list(params),
    queryFn: () => mergeRequestApi.listPost(params),
    ...options,
  })
}

export function useMergeRequest(
  params: GetMergeRequestParams,
  options?: Omit<UseQueryOptions<MergeRequestResponse, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: mergeRequestKeys.detail(params),
    queryFn: () => mergeRequestApi.getPost(params),
    ...options,
  })
}

export function useMergeRequestDiff(
  params: GetMergeRequestParams,
  options?: Omit<UseQueryOptions<DiffResponse, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: mergeRequestKeys.diff(params),
    queryFn: () => mergeRequestApi.getDiffPost(params),
    ...options,
  })
}

export function useMergeRequestComments(
  params: ListCommentsParams,
  options?: Omit<UseQueryOptions<ListCommentsResponse, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: mergeRequestKeys.comments(params),
    queryFn: () => mergeRequestApi.listCommentsPost(params),
    ...options,
  })
}

export function useMergeRequestReviews(
  params: ListReviewsParams,
  options?: Omit<UseQueryOptions<ListReviewsResponse, Error>, "queryKey" | "queryFn">
) {
  return useQuery({
    queryKey: mergeRequestKeys.reviews(params),
    queryFn: () => mergeRequestApi.listReviewsPost(params),
    ...options,
  })
}

// =============================================================================
// Mutations
// =============================================================================

export function useCreateMergeRequest(
  options?: UseMutationOptions<MergeRequestResponse, Error, CreateMergeRequestParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: mergeRequestApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: mergeRequestKeys.lists() })
    },
    ...options,
  })
}

export function useUpdateMergeRequest(
  options?: UseMutationOptions<MergeRequestResponse, Error, UpdateMergeRequestParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: mergeRequestApi.update,
    onSuccess: (data, variables) => {
      queryClient.setQueryData(
        mergeRequestKeys.detail({
          connectionId: variables.connectionId,
          namespace: variables.namespace,
          repository: variables.repository,
          number: variables.number,
        }),
        data
      )
      queryClient.invalidateQueries({ queryKey: mergeRequestKeys.lists() })
    },
    ...options,
  })
}

export function useMergeMergeRequest(
  options?: UseMutationOptions<MergeResponse, Error, MergeMergeRequestParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: mergeRequestApi.merge,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: mergeRequestKeys.detail({
          connectionId: variables.connectionId,
          namespace: variables.namespace,
          repository: variables.repository,
          number: variables.number,
        }),
      })
      queryClient.invalidateQueries({ queryKey: mergeRequestKeys.lists() })
    },
    ...options,
  })
}

export function useCreateComment(
  options?: UseMutationOptions<CommentResponse, Error, CreateCommentParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: mergeRequestApi.createComment,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: mergeRequestKeys.comments({
          connectionId: variables.connectionId,
          namespace: variables.namespace,
          repository: variables.repository,
          number: variables.number,
        }),
      })
    },
    ...options,
  })
}

export function useUpdateComment(
  options?: UseMutationOptions<CommentResponse, Error, UpdateCommentParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: mergeRequestApi.updateComment,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: mergeRequestKeys.comments({
          connectionId: variables.connectionId,
          namespace: variables.namespace,
          repository: variables.repository,
          number: variables.number,
        }),
      })
    },
    ...options,
  })
}

export function useDeleteComment(
  options?: UseMutationOptions<{ success: boolean }, Error, DeleteCommentParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: mergeRequestApi.deleteComment,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: mergeRequestKeys.comments({
          connectionId: variables.connectionId,
          namespace: variables.namespace,
          repository: variables.repository,
          number: variables.number,
        }),
      })
    },
    ...options,
  })
}

export function useSubmitReview(
  options?: UseMutationOptions<ReviewResponse, Error, SubmitReviewParams>
) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: mergeRequestApi.submitReview,
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: mergeRequestKeys.reviews({
          connectionId: variables.connectionId,
          namespace: variables.namespace,
          repository: variables.repository,
          number: variables.number,
        }),
      })
      queryClient.invalidateQueries({
        queryKey: mergeRequestKeys.detail({
          connectionId: variables.connectionId,
          namespace: variables.namespace,
          repository: variables.repository,
          number: variables.number,
        }),
      })
    },
    ...options,
  })
}
