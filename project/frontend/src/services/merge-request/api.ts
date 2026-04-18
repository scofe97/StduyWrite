import apiClient from "@/api/client"
import { USE_MOCK, MOCK_DELAY } from "../mock/config"
import { mockMergeRequests, delay } from "../mock/data"
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
  MergeRequest,
} from "./types"

const BASE_PATH = "/v1/merge-requests"

// =============================================================================
// Helper for Mock
// =============================================================================

function getMockMergeRequestsForRepo(repositoryId: string): MergeRequest[] {
  return mockMergeRequests[repositoryId] || []
}

// =============================================================================
// MergeRequest CRUD
// =============================================================================

export async function listMergeRequests(
  params: ListMergeRequestsParams
): Promise<ListMergeRequestsResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    // Find repository by namespace/repository name (simplified lookup)
    let allMRs: MergeRequest[] = []
    for (const repoId in mockMergeRequests) {
      allMRs = allMRs.concat(mockMergeRequests[repoId])
    }

    // Filter by status if provided
    if (params.status) {
      allMRs = allMRs.filter((mr) => mr.status === params.status)
    }

    // Pagination
    const page = params.page || 1
    const perPage = params.perPage || 20
    const start = (page - 1) * perPage
    const items = allMRs.slice(start, start + perPage)

    return {
      items,
      total: allMRs.length,
      page,
      perPage,
      hasMore: start + perPage < allMRs.length,
    }
  }

  const { connectionId, namespace, repository, status, page = 1, perPage = 20 } = params
  const response = await apiClient.get<ListMergeRequestsResponse>(
    `${BASE_PATH}/${connectionId}/list`,
    { params: { namespace, repository, status, page, perPage } }
  )
  return response.data
}

export async function listMergeRequestsPost(
  params: ListMergeRequestsParams
): Promise<ListMergeRequestsResponse> {
  if (USE_MOCK) {
    return listMergeRequests(params)
  }
  const response = await apiClient.post<ListMergeRequestsResponse>(`${BASE_PATH}/list`, params)
  return response.data
}

export async function getMergeRequest(
  params: GetMergeRequestParams
): Promise<MergeRequestResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    for (const repoId in mockMergeRequests) {
      const mr = mockMergeRequests[repoId].find((m) => m.number === params.number)
      if (mr) {
        return { mergeRequest: mr }
      }
    }
    throw new Error("Merge request not found")
  }

  const { connectionId, namespace, repository, number } = params
  const response = await apiClient.get<MergeRequestResponse>(
    `${BASE_PATH}/${connectionId}/${number}`,
    { params: { namespace, repository } }
  )
  return response.data
}

export async function getMergeRequestPost(
  params: GetMergeRequestParams
): Promise<MergeRequestResponse> {
  if (USE_MOCK) {
    return getMergeRequest(params)
  }
  const response = await apiClient.post<MergeRequestResponse>(`${BASE_PATH}/get`, params)
  return response.data
}

export async function createMergeRequest(
  params: CreateMergeRequestParams
): Promise<MergeRequestResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const newMR: MergeRequest = {
      id: `mr-${Date.now()}`,
      externalId: String(Date.now()),
      number: Math.floor(Math.random() * 1000) + 100,
      title: params.title,
      description: params.description || "",
      status: "OPEN",
      sourceBranch: params.sourceBranch,
      targetBranch: params.targetBranch,
      authorName: "Current User",
      authorEmail: "user@example.com",
      url: "#",
      mergedAt: null,
      closedAt: null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      isDraft: params.isDraft || false,
    }
    // Add to first repo for simplicity
    const firstRepoId = Object.keys(mockMergeRequests)[0] || "repo-1"
    if (!mockMergeRequests[firstRepoId]) {
      mockMergeRequests[firstRepoId] = []
    }
    mockMergeRequests[firstRepoId].push(newMR)
    return { mergeRequest: newMR }
  }
  const response = await apiClient.post<MergeRequestResponse>(`${BASE_PATH}/create`, params)
  return response.data
}

export async function updateMergeRequest(
  params: UpdateMergeRequestParams
): Promise<MergeRequestResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    for (const repoId in mockMergeRequests) {
      const index = mockMergeRequests[repoId].findIndex((m) => m.number === params.number)
      if (index !== -1) {
        mockMergeRequests[repoId][index] = {
          ...mockMergeRequests[repoId][index],
          title: params.title || mockMergeRequests[repoId][index].title,
          description: params.description || mockMergeRequests[repoId][index].description,
          updatedAt: new Date().toISOString(),
        }
        return { mergeRequest: mockMergeRequests[repoId][index] }
      }
    }
    throw new Error("Merge request not found")
  }
  const response = await apiClient.post<MergeRequestResponse>(`${BASE_PATH}/update`, params)
  return response.data
}

export async function mergeMergeRequest(
  params: MergeMergeRequestParams
): Promise<MergeResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    for (const repoId in mockMergeRequests) {
      const mr = mockMergeRequests[repoId].find((m) => m.number === params.number)
      if (mr) {
        mr.status = "MERGED"
        mr.mergedAt = new Date().toISOString()
        mr.updatedAt = new Date().toISOString()
        return {
          success: true,
          sha: "merged123abc",
          message: "Merge successful",
        }
      }
    }
    throw new Error("Merge request not found")
  }
  const response = await apiClient.post<MergeResponse>(`${BASE_PATH}/merge`, params)
  return response.data
}

// =============================================================================
// Comments
// =============================================================================

export async function listComments(
  params: ListCommentsParams
): Promise<ListCommentsResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    // Return empty comments for mock
    return { comments: [], total: 0 }
  }

  const { connectionId, namespace, repository, number } = params
  const response = await apiClient.get<ListCommentsResponse>(
    `${BASE_PATH}/${connectionId}/${number}/comments`,
    { params: { namespace, repository } }
  )
  return response.data
}

export async function listCommentsPost(
  params: ListCommentsParams
): Promise<ListCommentsResponse> {
  if (USE_MOCK) {
    return listComments(params)
  }
  const response = await apiClient.post<ListCommentsResponse>(`${BASE_PATH}/comments/list`, params)
  return response.data
}

export async function createComment(
  params: CreateCommentParams
): Promise<CommentResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return {
      comment: {
        id: `comment-${Date.now()}`,
        body: params.body,
        authorName: "Current User",
        authorEmail: "user@example.com",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
    }
  }
  const response = await apiClient.post<CommentResponse>(`${BASE_PATH}/comments/create`, params)
  return response.data
}

export async function updateComment(
  params: UpdateCommentParams
): Promise<CommentResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return {
      comment: {
        id: params.commentId,
        body: params.body,
        authorName: "Current User",
        authorEmail: "user@example.com",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
    }
  }
  const response = await apiClient.post<CommentResponse>(`${BASE_PATH}/comments/update`, params)
  return response.data
}

export async function deleteComment(
  params: DeleteCommentParams
): Promise<void> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return
  }
  await apiClient.post(`${BASE_PATH}/comments/delete`, params)
}

// =============================================================================
// Reviews
// =============================================================================

export async function listReviews(
  params: ListReviewsParams
): Promise<ListReviewsResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    // Return empty reviews for mock
    return { reviews: [], total: 0 }
  }

  const { connectionId, namespace, repository, number } = params
  const response = await apiClient.get<ListReviewsResponse>(
    `${BASE_PATH}/${connectionId}/${number}/reviews`,
    { params: { namespace, repository } }
  )
  return response.data
}

export async function listReviewsPost(
  params: ListReviewsParams
): Promise<ListReviewsResponse> {
  if (USE_MOCK) {
    return listReviews(params)
  }
  const response = await apiClient.post<ListReviewsResponse>(`${BASE_PATH}/reviews/list`, params)
  return response.data
}

export async function submitReview(
  params: SubmitReviewParams
): Promise<ReviewResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return {
      review: {
        id: `review-${Date.now()}`,
        state: params.event,
        body: params.body || "",
        authorName: "Current User",
        authorEmail: "user@example.com",
        createdAt: new Date().toISOString(),
      },
    }
  }
  const response = await apiClient.post<ReviewResponse>(`${BASE_PATH}/reviews/submit`, params)
  return response.data
}

// =============================================================================
// Diff
// =============================================================================

export async function getMergeRequestDiff(
  params: GetMergeRequestParams
): Promise<DiffResponse> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return {
      diff: "diff --git a/src/App.tsx b/src/App.tsx\n@@ -1,5 +1,6 @@\n import React from 'react'\n+import { NewComponent } from './NewComponent'\n",
      files: [
        {
          filename: "src/App.tsx",
          status: "modified",
          additions: 5,
          deletions: 2,
          changes: 7,
        },
      ],
    }
  }

  const { connectionId, namespace, repository, number } = params
  const response = await apiClient.get<DiffResponse>(
    `${BASE_PATH}/${connectionId}/${number}/diff`,
    { params: { namespace, repository } }
  )
  return response.data
}

export async function getMergeRequestDiffPost(
  params: GetMergeRequestParams
): Promise<DiffResponse> {
  if (USE_MOCK) {
    return getMergeRequestDiff(params)
  }
  const response = await apiClient.post<DiffResponse>(`${BASE_PATH}/diff`, params)
  return response.data
}

// =============================================================================
// Export
// =============================================================================

export const mergeRequestApi = {
  list: listMergeRequests,
  listPost: listMergeRequestsPost,
  get: getMergeRequest,
  getPost: getMergeRequestPost,
  create: createMergeRequest,
  update: updateMergeRequest,
  merge: mergeMergeRequest,
  listComments,
  listCommentsPost,
  createComment,
  updateComment,
  deleteComment,
  listReviews,
  listReviewsPost,
  submitReview,
  getDiff: getMergeRequestDiff,
  getDiffPost: getMergeRequestDiffPost,
}
