import apiClient from "@/api/client"
import { USE_MOCK, MOCK_DELAY } from "../mock/config"
import { mockBranches, delay } from "../mock/data"
import type {
  Branch,
  BranchType,
  BranchStatus,
  CreateBranchParams,
  UpdateBranchParams,
} from "./types"

const BASE_PATH = "/v1/branches"

// =============================================================================
// Branch CRUD
// =============================================================================

export async function createBranch(params: CreateBranchParams): Promise<Branch> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const newBranch: Branch = {
      id: `branch-${Date.now()}`,
      repositoryId: params.repositoryId,
      name: params.name,
      branchType: params.branchType || "FEATURE",
      status: "ACTIVE",
      isProtected: params.isProtected || false,
      commitSha: params.commitSha || "abc123",
      metadata: params.metadata || null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
    if (!mockBranches[params.repositoryId]) {
      mockBranches[params.repositoryId] = []
    }
    mockBranches[params.repositoryId].push(newBranch)
    return newBranch
  }
  const response = await apiClient.post<Branch>(BASE_PATH, params)
  return response.data
}

export async function updateBranch(params: UpdateBranchParams): Promise<Branch> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    for (const repoId in mockBranches) {
      const index = mockBranches[repoId].findIndex((b) => b.id === params.id)
      if (index !== -1) {
        mockBranches[repoId][index] = {
          ...mockBranches[repoId][index],
          ...params,
          updatedAt: new Date().toISOString(),
        }
        return mockBranches[repoId][index]
      }
    }
    throw new Error("Branch not found")
  }
  const { id, ...updateData } = params
  const response = await apiClient.put<Branch>(
    `${BASE_PATH}/${id}`,
    updateData
  )
  return response.data
}

export async function getBranch(id: string): Promise<Branch> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    for (const repoId in mockBranches) {
      const branch = mockBranches[repoId].find((b) => b.id === id)
      if (branch) return branch
    }
    throw new Error("Branch not found")
  }
  const response = await apiClient.get<Branch>(`${BASE_PATH}/${id}`)
  return response.data
}

export async function getBranchesByRepositoryId(
  repositoryId: string
): Promise<Branch[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return mockBranches[repositoryId] || []
  }
  const response = await apiClient.get<Branch[]>(
    `${BASE_PATH}/repository/${repositoryId}`
  )
  return response.data
}

export async function getBranchesByStatus(
  repositoryId: string,
  status: BranchStatus
): Promise<Branch[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const branches = mockBranches[repositoryId] || []
    return branches.filter((b) => b.status === status)
  }
  const response = await apiClient.get<Branch[]>(
    `${BASE_PATH}/repository/${repositoryId}/status/${status}`
  )
  return response.data
}

export async function getBranchesByType(
  repositoryId: string,
  type: BranchType
): Promise<Branch[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const branches = mockBranches[repositoryId] || []
    return branches.filter((b) => b.branchType === type)
  }
  const response = await apiClient.get<Branch[]>(
    `${BASE_PATH}/repository/${repositoryId}/type/${type}`
  )
  return response.data
}

export async function deleteBranch(id: string): Promise<void> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    for (const repoId in mockBranches) {
      const index = mockBranches[repoId].findIndex((b) => b.id === id)
      if (index !== -1) {
        mockBranches[repoId].splice(index, 1)
        return
      }
    }
    return
  }
  await apiClient.delete(`${BASE_PATH}/${id}`)
}

export async function updateBranchStatus(
  id: string,
  status: BranchStatus
): Promise<Branch> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    for (const repoId in mockBranches) {
      const branch = mockBranches[repoId].find((b) => b.id === id)
      if (branch) {
        branch.status = status
        branch.updatedAt = new Date().toISOString()
        return branch
      }
    }
    throw new Error("Branch not found")
  }
  const response = await apiClient.patch<Branch>(
    `${BASE_PATH}/${id}/status`,
    { status }
  )
  return response.data
}

export async function updateBranchCommit(
  id: string,
  commitSha: string
): Promise<Branch> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    for (const repoId in mockBranches) {
      const branch = mockBranches[repoId].find((b) => b.id === id)
      if (branch) {
        branch.commitSha = commitSha
        branch.updatedAt = new Date().toISOString()
        return branch
      }
    }
    throw new Error("Branch not found")
  }
  const response = await apiClient.patch<Branch>(
    `${BASE_PATH}/${id}/commit`,
    { commitSha }
  )
  return response.data
}

// =============================================================================
// Export
// =============================================================================

export const branchApi = {
  create: createBranch,
  update: updateBranch,
  get: getBranch,
  getByRepositoryId: getBranchesByRepositoryId,
  getByStatus: getBranchesByStatus,
  getByType: getBranchesByType,
  delete: deleteBranch,
  updateStatus: updateBranchStatus,
  updateCommit: updateBranchCommit,
}
