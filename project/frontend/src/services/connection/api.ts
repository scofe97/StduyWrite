import apiClient from "@/api/client"
import { USE_MOCK, MOCK_DELAY } from "../mock/config"
import { mockConnections, delay } from "../mock/data"
import type {
  Connection,
  CreateConnectionParams,
  UpdateConnectionParams,
  ProviderType,
} from "./types"

const BASE_PATH = "/v1/connections"

// =============================================================================
// Connection CRUD
// =============================================================================

export async function createConnection(
  params: CreateConnectionParams
): Promise<Connection> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const newConnection: Connection = {
      id: `conn-${Date.now()}`,
      ...params,
      baseUrl: params.baseUrl || null,
      status: "ACTIVE",
      metadata: params.metadata || null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
    mockConnections.push(newConnection)
    return newConnection
  }
  const response = await apiClient.post<Connection>(BASE_PATH, params)
  return response.data
}

export async function updateConnection(
  params: UpdateConnectionParams
): Promise<Connection> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const index = mockConnections.findIndex((c) => c.id === params.id)
    if (index === -1) throw new Error("Connection not found")
    mockConnections[index] = {
      ...mockConnections[index],
      ...params,
      updatedAt: new Date().toISOString(),
    }
    return mockConnections[index]
  }
  const { id, ...updateData } = params
  const response = await apiClient.put<Connection>(
    `${BASE_PATH}/${id}`,
    updateData
  )
  return response.data
}

export async function getConnection(id: string): Promise<Connection> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const connection = mockConnections.find((c) => c.id === id)
    if (!connection) throw new Error("Connection not found")
    return connection
  }
  const response = await apiClient.get<Connection>(`${BASE_PATH}/${id}`)
  return response.data
}

export async function getConnectionsByProjectId(
  projectId: string
): Promise<Connection[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return mockConnections.filter((c) => c.projectId === projectId)
  }
  const response = await apiClient.get<Connection[]>(
    `${BASE_PATH}/project/${projectId}`
  )
  return response.data
}

export async function getConnectionsByProviderType(
  providerType: ProviderType
): Promise<Connection[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return mockConnections.filter((c) => c.providerType === providerType)
  }
  const response = await apiClient.get<Connection[]>(
    `${BASE_PATH}/provider/${providerType}`
  )
  return response.data
}

export async function getActiveConnections(): Promise<Connection[]> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return mockConnections.filter((c) => c.status === "ACTIVE")
  }
  const response = await apiClient.get<Connection[]>(
    `${BASE_PATH}/active`
  )
  return response.data
}

export async function deleteConnection(id: string): Promise<void> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const index = mockConnections.findIndex((c) => c.id === id)
    if (index !== -1) mockConnections.splice(index, 1)
    return
  }
  await apiClient.delete(`${BASE_PATH}/${id}`)
}

export async function activateConnection(id: string): Promise<Connection> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const connection = mockConnections.find((c) => c.id === id)
    if (!connection) throw new Error("Connection not found")
    connection.status = "ACTIVE"
    connection.updatedAt = new Date().toISOString()
    return connection
  }
  const response = await apiClient.post<Connection>(
    `${BASE_PATH}/${id}/activate`
  )
  return response.data
}

export async function deactivateConnection(id: string): Promise<Connection> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    const connection = mockConnections.find((c) => c.id === id)
    if (!connection) throw new Error("Connection not found")
    connection.status = "INACTIVE"
    connection.updatedAt = new Date().toISOString()
    return connection
  }
  const response = await apiClient.post<Connection>(
    `${BASE_PATH}/${id}/deactivate`
  )
  return response.data
}

export async function testConnection(id: string): Promise<boolean> {
  if (USE_MOCK) {
    await delay(MOCK_DELAY)
    return true
  }
  const response = await apiClient.post<boolean>(
    `${BASE_PATH}/${id}/test`
  )
  return response.data
}

// =============================================================================
// Export
// =============================================================================

export const connectionApi = {
  create: createConnection,
  update: updateConnection,
  get: getConnection,
  getByProjectId: getConnectionsByProjectId,
  getByProviderType: getConnectionsByProviderType,
  getActive: getActiveConnections,
  delete: deleteConnection,
  activate: activateConnection,
  deactivate: deactivateConnection,
  test: testConnection,
}
