// =============================================================================
// Enums
// =============================================================================

export type ProviderType = "GITHUB" | "GITLAB" | "BITBUCKET"

export type ConnectionStatus = "ACTIVE" | "INACTIVE" | "ERROR"

// =============================================================================
// Connection 기본 타입
// =============================================================================

export interface Connection {
  id: string
  projectId: string
  providerType: ProviderType
  name: string
  baseUrl: string | null
  status: ConnectionStatus
  metadata: Record<string, unknown> | null
  createdAt: string
  updatedAt: string
}

// =============================================================================
// API 요청 타입
// =============================================================================

export interface CreateConnectionParams {
  projectId: string
  providerType: ProviderType
  name: string
  baseUrl?: string
  apiToken: string
  metadata?: Record<string, unknown>
}

export interface UpdateConnectionParams {
  id: string
  name?: string
  baseUrl?: string
  apiToken?: string
  metadata?: Record<string, unknown>
}
