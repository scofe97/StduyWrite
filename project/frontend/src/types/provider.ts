import type { ProviderType } from "./repository"

export type AuthType = "token" | "oauth" | "app"

export type ConnectionStatus = "connected" | "disconnected" | "error"

export interface ProviderConnection {
  id: string
  type: ProviderType | string
  name: string
  baseUrl: string
  authType: AuthType
  status: ConnectionStatus
  createdAt: string
  repositoryCount?: number
}

export interface ProviderMeta {
  type: string
  label: string
  color: string
  defaultBaseUrl: string
  supportedAuthTypes: AuthType[]
}
