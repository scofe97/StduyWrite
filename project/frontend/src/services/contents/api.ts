import apiClient from "@/api/client"
import { USE_MOCK, MOCK_DELAY } from "../mock/config"
import { mockTreeEntries, mockFileContents, delay } from "../mock/data"
import type {
  TreeEntry,
  ContentEntry,
  TreeData,
  GetTreeParams,
  GetContentsParams,
} from "./types"

const BASE_PATH = "/v1/repositories"

// =============================================================================
// Contents API (GET)
// =============================================================================

export async function getTree(params: GetTreeParams): Promise<TreeEntry[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    // Return all entries for recursive, or filter by direct children for non-recursive
    if (params.recursive) {
      return mockTreeEntries
    }
    // For non-recursive, return only top-level entries
    return mockTreeEntries.filter((entry) => {
      const parts = entry.path.split("/")
      return parts.length === 1 || (parts.length === 2 && entry.type === "DIRECTORY")
    })
  }

  const { connectionId, namespace, repository, ref, recursive = false } = params

  const response = await apiClient.get<TreeData>(
    `${BASE_PATH}/${connectionId}/tree`,
    { params: { namespace, repository, ref, recursive } }
  )
  return response.data.entries
}

export async function getContents(params: GetContentsParams): Promise<ContentEntry> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const path = params.path || "README.md"
    const content = mockFileContents[path]
    if (content) {
      return content
    }
    // Return a default content for unknown files
    return {
      path,
      type: "FILE",
      sha: "unknown",
      size: 100,
      content: btoa(`// Content of ${path}\n`),
      encoding: "base64",
      url: null,
    }
  }

  const { connectionId, namespace, repository, path = "", ref } = params

  const response = await apiClient.get<ContentEntry>(
    `${BASE_PATH}/${connectionId}/contents`,
    { params: { namespace, repository, path, ref } }
  )
  return response.data
}

// =============================================================================
// Contents API (POST)
// =============================================================================

export async function getTreePost(params: GetTreeParams): Promise<TreeEntry[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    if (params.recursive) {
      return mockTreeEntries
    }
    return mockTreeEntries.filter((entry) => {
      const parts = entry.path.split("/")
      return parts.length === 1 || (parts.length === 2 && entry.type === "DIRECTORY")
    })
  }
  const response = await apiClient.post<TreeData>(`${BASE_PATH}/tree`, params)
  return response.data.entries
}

export async function getContentsPost(params: GetContentsParams): Promise<ContentEntry> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const path = params.path || "README.md"
    const content = mockFileContents[path]
    if (content) {
      return content
    }
    return {
      path,
      type: "FILE",
      sha: "unknown",
      size: 100,
      content: btoa(`// Content of ${path}\n`),
      encoding: "base64",
      url: null,
    }
  }
  const response = await apiClient.post<ContentEntry>(`${BASE_PATH}/contents`, params)
  return response.data
}

// =============================================================================
// Export
// =============================================================================

export const contentsApi = {
  getTree,
  getTreePost,
  getContents,
  getContentsPost,
}
