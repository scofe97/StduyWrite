import apiClient from "@/api/client"
import { USE_MOCK, MOCK_DELAY } from "../mock/config"
import { mockRepositories, delay } from "../mock/data"
import type {
  Repository,
  CreateRepositoryParams,
  UpdateRepositoryParams,
} from "./types"

const BASE_PATH = "/v1/repositories"

// =============================================================================
// Repository CRUD
// =============================================================================

export async function createRepository(
  params: CreateRepositoryParams
): Promise<Repository> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const newRepository: Repository = {
      id: `repo-${Date.now()}`,
      ...params,
      metadata: params.metadata || null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
    mockRepositories.push(newRepository)
    return newRepository
  }
  const response = await apiClient.post<Repository>(BASE_PATH, params)
  return response.data
}

export async function updateRepository(
  params: UpdateRepositoryParams
): Promise<Repository> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const index = mockRepositories.findIndex((r) => r.id === params.id)
    if (index === -1) throw new Error("Repository not found")
    mockRepositories[index] = {
      ...mockRepositories[index],
      ...params,
      updatedAt: new Date().toISOString(),
    }
    return mockRepositories[index]
  }
  const { id, ...updateData } = params
  const response = await apiClient.put<Repository>(
    `${BASE_PATH}/${id}`,
    updateData
  )
  return response.data
}

export async function getRepository(id: string): Promise<Repository> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const repository = mockRepositories.find((r) => r.id === id)
    if (!repository) throw new Error("Repository not found")
    return repository
  }
  const response = await apiClient.get<Repository>(`${BASE_PATH}/${id}`)
  return response.data
}

export async function getRepositoriesByProjectId(
  projectId: string
): Promise<Repository[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return mockRepositories.filter((r) => r.projectId === projectId)
  }
  const response = await apiClient.get<Repository[]>(
    `${BASE_PATH}/project/${projectId}`
  )
  return response.data
}

export async function getRepositoriesByConnectionId(
  connectionId: string
): Promise<Repository[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return mockRepositories.filter((r) => r.connectionId === connectionId)
  }
  const response = await apiClient.get<Repository[]>(
    `${BASE_PATH}/connection/${connectionId}`
  )
  return response.data
}

export async function deleteRepository(id: string): Promise<void> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const index = mockRepositories.findIndex((r) => r.id === id)
    if (index !== -1) mockRepositories.splice(index, 1)
    return
  }
  await apiClient.delete(`${BASE_PATH}/${id}`)
}

export async function syncRepository(id: string): Promise<Repository> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const repository = mockRepositories.find((r) => r.id === id)
    if (!repository) throw new Error("Repository not found")
    repository.updatedAt = new Date().toISOString()
    return repository
  }
  const response = await apiClient.post<Repository>(
    `${BASE_PATH}/${id}/sync`
  )
  return response.data
}

// =============================================================================
// Export
// =============================================================================

export const repositoryApi = {
  create: createRepository,
  update: updateRepository,
  get: getRepository,
  getByProjectId: getRepositoriesByProjectId,
  getByConnectionId: getRepositoriesByConnectionId,
  delete: deleteRepository,
  sync: syncRepository,
}
