// =============================================================================
// Enums
// =============================================================================

export type ContentType = "FILE" | "DIRECTORY" | "SYMLINK" | "SUBMODULE"

// =============================================================================
// Contents 기본 타입
// =============================================================================

export interface TreeEntry {
  path: string
  type: ContentType
  sha: string
  size: number | null
  mode: string | null
}

export interface ContentEntry {
  path: string
  type: ContentType
  sha: string
  size: number | null
  content: string | null
  encoding: string | null
  url: string | null
}

// =============================================================================
// API 요청 타입
// =============================================================================

export interface GetTreeParams {
  connectionId: string
  namespace: string
  repository: string
  ref?: string
  recursive?: boolean
}

export interface GetContentsParams {
  connectionId: string
  namespace: string
  repository: string
  path?: string
  ref?: string
}

// =============================================================================
// API 응답 내부 타입
// =============================================================================

export interface TreeData {
  entries: TreeEntry[]
}
