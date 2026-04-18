// =============================================================================
// Enums
// =============================================================================

export type MergeRequestStatus = "OPEN" | "MERGED" | "CLOSED" | "DRAFT"

export type MergeableState = "MERGEABLE" | "CONFLICTING" | "UNKNOWN"

export type ReviewState = "APPROVED" | "CHANGES_REQUESTED" | "COMMENTED" | "PENDING"

// =============================================================================
// MergeRequest 기본 타입
// =============================================================================

export interface MergeRequest {
  id: string
  externalId: string
  number: number
  title: string
  description: string | null
  status: MergeRequestStatus
  sourceBranch: string
  targetBranch: string
  authorName: string
  authorEmail: string | null
  url: string
  mergedAt: string | null
  closedAt: string | null
  createdAt: string
  updatedAt: string
  isDraft: boolean
}

export interface MergeRequestDetail extends MergeRequest {
  mergeableState: MergeableState
  hasConflicts: boolean
  additions: number
  deletions: number
  changedFiles: number
  commitCount: number
  commentCount: number
}

export interface MergeRequestComment {
  id: string
  body: string
  authorName: string
  authorEmail: string | null
  avatarUrl: string | null
  path: string | null
  line: number | null
  isSystem: boolean
  createdAt: string
  updatedAt: string
}

export interface MergeRequestReview {
  id: string
  authorName: string
  authorEmail: string | null
  avatarUrl: string | null
  state: ReviewState
  body: string | null
  submittedAt: string
}

export interface FileDiff {
  path: string
  oldPath: string | null
  status: "added" | "modified" | "deleted" | "renamed"
  additions: number
  deletions: number
  patch: string | null
}

export interface MergeRequestDiff {
  baseSha: string
  headSha: string
  files: FileDiff[]
  totalAdditions: number
  totalDeletions: number
}

// =============================================================================
// API 요청 타입
// =============================================================================

export interface ListMergeRequestsParams {
  connectionId: string
  namespace: string
  repository: string
  status?: MergeRequestStatus
  page?: number
  perPage?: number
}

export interface GetMergeRequestParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
}

export interface CreateMergeRequestParams {
  connectionId: string
  namespace: string
  repository: string
  title: string
  description?: string
  sourceBranch: string
  targetBranch: string
  draft?: boolean
}

export interface UpdateMergeRequestParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
  title?: string
  description?: string
  state?: "open" | "closed"
  targetBranch?: string
}

export interface MergeMergeRequestParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
  commitTitle?: string
  commitMessage?: string
  mergeMethod?: "merge" | "squash" | "rebase"
  deleteSourceBranch?: boolean
}

export interface ListCommentsParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
}

export interface CreateCommentParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
  body: string
  path?: string
  line?: number
  commitId?: string
}

export interface UpdateCommentParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
  commentId: string
  body: string
}

export interface DeleteCommentParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
  commentId: string
}

export interface ListReviewsParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
}

export interface SubmitReviewParams {
  connectionId: string
  namespace: string
  repository: string
  number: number
  state: ReviewState
  body?: string
}

// =============================================================================
// API 응답 타입
// =============================================================================

export interface ListMergeRequestsResponse {
  mergeRequests: MergeRequest[]
  totalCount: number
}

export interface MergeRequestResponse {
  mergeRequest: MergeRequestDetail
}

export interface MergeResponse {
  mergeRequest: MergeRequest
  mergeSha: string
}

export interface ListCommentsResponse {
  comments: MergeRequestComment[]
}

export interface CommentResponse {
  comment: MergeRequestComment
}

export interface ListReviewsResponse {
  reviews: MergeRequestReview[]
}

export interface ReviewResponse {
  review: MergeRequestReview
}

export interface DiffResponse {
  diff: MergeRequestDiff
}
