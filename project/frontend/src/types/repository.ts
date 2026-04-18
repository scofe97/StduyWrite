export type ProviderType = "github" | "gitlab" | "bitbucket"

export type OwnerType = "user" | "organization" | "project"

export interface RepositoryOwner {
  type: OwnerType
  name: string
  avatarUrl?: string
}

export interface Repository {
  id: string
  name: string
  fullName: string
  description: string | null
  provider: ProviderType
  owner: RepositoryOwner
  private: boolean
  stars: number
  forks: number
  language: string | null
  updatedAt: string
  url: string
  defaultBranch: string
}

// Backward compatibility alias
export type Provider = ProviderType
