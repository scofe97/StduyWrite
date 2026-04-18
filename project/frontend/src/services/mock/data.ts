import type { Connection, ProviderType, ConnectionStatus } from "../connection/types"
import type { Repository, BranchStrategyType } from "../repository/types"
import type { Branch, BranchType, BranchStatus } from "../branch/types"
import type { TreeEntry, ContentEntry } from "../contents/types"
import type { MergeRequest, MergeRequestStatus } from "../merge-request/types"

// =============================================================================
// Mock Connections
// =============================================================================

export const mockConnections: Connection[] = [
  {
    id: "conn-1",
    projectId: "proj-1",
    providerType: "GITHUB",
    name: "GitHub - Personal",
    baseUrl: "https://api.github.com",
    status: "ACTIVE",
    metadata: null,
    createdAt: "2024-01-15T10:00:00Z",
    updatedAt: "2024-01-20T15:30:00Z",
  },
  {
    id: "conn-2",
    projectId: "proj-1",
    providerType: "GITLAB",
    name: "GitLab - Work",
    baseUrl: "https://gitlab.com/api/v4",
    status: "ACTIVE",
    metadata: null,
    createdAt: "2024-01-10T08:00:00Z",
    updatedAt: "2024-01-18T12:00:00Z",
  },
  {
    id: "conn-3",
    projectId: "proj-1",
    providerType: "BITBUCKET",
    name: "Bitbucket - Archive",
    baseUrl: "https://api.bitbucket.org/2.0",
    status: "INACTIVE",
    metadata: null,
    createdAt: "2023-06-01T09:00:00Z",
    updatedAt: "2023-12-01T10:00:00Z",
  },
]

// =============================================================================
// Mock Repositories
// =============================================================================

export const mockRepositories: Repository[] = [
  {
    id: "repo-1",
    projectId: "proj-1",
    connectionId: "conn-1",
    name: "runners-high/frontend",
    gitUrl: "https://github.com/runners-high/frontend",
    defaultBranch: "main",
    strategyType: "GITHUB_FLOW",
    providerType: "GITHUB",
    namespace: "runners-high",
    repositoryName: "frontend",
    metadata: null,
    createdAt: "2024-01-15T10:00:00Z",
    updatedAt: "2024-01-19T14:30:00Z",
  },
  {
    id: "repo-2",
    projectId: "proj-1",
    connectionId: "conn-1",
    name: "runners-high/backend",
    gitUrl: "https://github.com/runners-high/backend",
    defaultBranch: "main",
    strategyType: "GIT_FLOW",
    providerType: "GITHUB",
    namespace: "runners-high",
    repositoryName: "backend",
    metadata: null,
    createdAt: "2024-01-15T10:00:00Z",
    updatedAt: "2024-01-18T09:00:00Z",
  },
  {
    id: "repo-3",
    projectId: "proj-1",
    connectionId: "conn-1",
    name: "runners-high/shared-libs",
    gitUrl: "https://github.com/runners-high/shared-libs",
    defaultBranch: "main",
    strategyType: "TRUNK_BASED",
    providerType: "GITHUB",
    namespace: "runners-high",
    repositoryName: "shared-libs",
    metadata: null,
    createdAt: "2024-01-10T10:00:00Z",
    updatedAt: "2024-01-17T16:00:00Z",
  },
  {
    id: "repo-4",
    projectId: "proj-1",
    connectionId: "conn-2",
    name: "work/internal-api",
    gitUrl: "https://gitlab.com/work/internal-api",
    defaultBranch: "develop",
    strategyType: "GIT_FLOW",
    providerType: "GITLAB",
    namespace: "work",
    repositoryName: "internal-api",
    metadata: null,
    createdAt: "2024-01-12T10:00:00Z",
    updatedAt: "2024-01-19T11:00:00Z",
  },
  {
    id: "repo-5",
    projectId: "proj-1",
    connectionId: "conn-2",
    name: "work/admin-dashboard",
    gitUrl: "https://gitlab.com/work/admin-dashboard",
    defaultBranch: "main",
    strategyType: "GITHUB_FLOW",
    providerType: "GITLAB",
    namespace: "work",
    repositoryName: "admin-dashboard",
    metadata: null,
    createdAt: "2024-01-08T10:00:00Z",
    updatedAt: "2024-01-16T13:00:00Z",
  },
]

// =============================================================================
// Mock Branches
// =============================================================================

export const mockBranches: Record<string, Branch[]> = {
  "repo-1": [
    {
      id: "branch-1",
      repositoryId: "repo-1",
      name: "main",
      branchType: "MAIN",
      status: "ACTIVE",
      isProtected: true,
      commitSha: "abc123def456",
      metadata: null,
      createdAt: "2024-01-15T10:00:00Z",
      updatedAt: "2024-01-19T14:30:00Z",
    },
    {
      id: "branch-2",
      repositoryId: "repo-1",
      name: "develop",
      branchType: "DEVELOP",
      status: "ACTIVE",
      isProtected: true,
      commitSha: "def456ghi789",
      metadata: null,
      createdAt: "2024-01-15T10:00:00Z",
      updatedAt: "2024-01-19T12:00:00Z",
    },
    {
      id: "branch-3",
      repositoryId: "repo-1",
      name: "feature/user-auth",
      branchType: "FEATURE",
      status: "ACTIVE",
      isProtected: false,
      commitSha: "ghi789jkl012",
      metadata: null,
      createdAt: "2024-01-17T09:00:00Z",
      updatedAt: "2024-01-19T10:00:00Z",
    },
    {
      id: "branch-4",
      repositoryId: "repo-1",
      name: "feature/dashboard",
      branchType: "FEATURE",
      status: "ACTIVE",
      isProtected: false,
      commitSha: "jkl012mno345",
      metadata: null,
      createdAt: "2024-01-18T11:00:00Z",
      updatedAt: "2024-01-19T08:00:00Z",
    },
    {
      id: "branch-5",
      repositoryId: "repo-1",
      name: "feature/old-feature",
      branchType: "FEATURE",
      status: "MERGED",
      isProtected: false,
      commitSha: "mno345pqr678",
      metadata: null,
      createdAt: "2024-01-10T10:00:00Z",
      updatedAt: "2024-01-15T14:00:00Z",
    },
    {
      id: "branch-6",
      repositoryId: "repo-1",
      name: "hotfix/security-patch",
      branchType: "HOTFIX",
      status: "MERGED",
      isProtected: false,
      commitSha: "pqr678stu901",
      metadata: null,
      createdAt: "2024-01-16T15:00:00Z",
      updatedAt: "2024-01-16T18:00:00Z",
    },
  ],
  "repo-2": [
    {
      id: "branch-7",
      repositoryId: "repo-2",
      name: "main",
      branchType: "MAIN",
      status: "ACTIVE",
      isProtected: true,
      commitSha: "stu901vwx234",
      metadata: null,
      createdAt: "2024-01-15T10:00:00Z",
      updatedAt: "2024-01-18T09:00:00Z",
    },
    {
      id: "branch-8",
      repositoryId: "repo-2",
      name: "develop",
      branchType: "DEVELOP",
      status: "ACTIVE",
      isProtected: true,
      commitSha: "vwx234yza567",
      metadata: null,
      createdAt: "2024-01-15T10:00:00Z",
      updatedAt: "2024-01-18T08:00:00Z",
    },
  ],
}

// =============================================================================
// Mock Tree Entries
// =============================================================================

export const mockTreeEntries: TreeEntry[] = [
  { path: "src", type: "DIRECTORY", sha: "dir1", size: null, mode: "040000" },
  { path: "src/components", type: "DIRECTORY", sha: "dir2", size: null, mode: "040000" },
  { path: "src/components/Button.tsx", type: "FILE", sha: "file1", size: 1234, mode: "100644" },
  { path: "src/components/Card.tsx", type: "FILE", sha: "file2", size: 2345, mode: "100644" },
  { path: "src/pages", type: "DIRECTORY", sha: "dir3", size: null, mode: "040000" },
  { path: "src/pages/Home.tsx", type: "FILE", sha: "file3", size: 3456, mode: "100644" },
  { path: "src/pages/About.tsx", type: "FILE", sha: "file4", size: 1567, mode: "100644" },
  { path: "src/App.tsx", type: "FILE", sha: "file5", size: 890, mode: "100644" },
  { path: "src/main.tsx", type: "FILE", sha: "file6", size: 456, mode: "100644" },
  { path: "package.json", type: "FILE", sha: "file7", size: 1200, mode: "100644" },
  { path: "README.md", type: "FILE", sha: "file8", size: 2500, mode: "100644" },
  { path: "tsconfig.json", type: "FILE", sha: "file9", size: 650, mode: "100644" },
  { path: ".gitignore", type: "FILE", sha: "file10", size: 200, mode: "100644" },
]

// =============================================================================
// Mock File Contents
// =============================================================================

export const mockFileContents: Record<string, ContentEntry> = {
  "README.md": {
    path: "README.md",
    type: "FILE",
    sha: "file8",
    size: 2500,
    content: btoa(`# Runners High Frontend

A modern repository management UI built with React and TypeScript.

## Features

- Multi-provider support (GitHub, GitLab, Bitbucket)
- Repository browsing and management
- Branch management with Git Flow support
- Pull Request tracking

## Getting Started

\`\`\`bash
yarn install
yarn dev
\`\`\`

## Tech Stack

- React 18
- TypeScript
- Vite
- TailwindCSS
- shadcn/ui
- React Query
`),
    encoding: "base64",
    url: null,
  },
  "package.json": {
    path: "package.json",
    type: "FILE",
    sha: "file7",
    size: 1200,
    content: btoa(`{
  "name": "runners-high-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}`),
    encoding: "base64",
    url: null,
  },
  "src/App.tsx": {
    path: "src/App.tsx",
    type: "FILE",
    sha: "file5",
    size: 890,
    content: btoa(`import { BrowserRouter, Routes, Route } from "react-router-dom"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
`),
    encoding: "base64",
    url: null,
  },
}

// =============================================================================
// Mock Merge Requests
// =============================================================================

export const mockMergeRequests: Record<string, MergeRequest[]> = {
  "repo-1": [
    {
      id: "mr-1",
      externalId: "123",
      number: 42,
      title: "feat: Add user authentication flow",
      description: "Implements OAuth2 login with GitHub and Google providers",
      status: "OPEN",
      sourceBranch: "feature/user-auth",
      targetBranch: "develop",
      authorName: "John Doe",
      authorEmail: "john@example.com",
      url: "https://github.com/runners-high/frontend/pull/42",
      mergedAt: null,
      closedAt: null,
      createdAt: "2024-01-17T09:00:00Z",
      updatedAt: "2024-01-19T10:00:00Z",
      isDraft: false,
    },
    {
      id: "mr-2",
      externalId: "124",
      number: 43,
      title: "feat: Dashboard redesign",
      description: "Complete redesign of the main dashboard",
      status: "OPEN",
      sourceBranch: "feature/dashboard",
      targetBranch: "develop",
      authorName: "Jane Smith",
      authorEmail: "jane@example.com",
      url: "https://github.com/runners-high/frontend/pull/43",
      mergedAt: null,
      closedAt: null,
      createdAt: "2024-01-18T11:00:00Z",
      updatedAt: "2024-01-19T08:00:00Z",
      isDraft: true,
    },
    {
      id: "mr-3",
      externalId: "120",
      number: 40,
      title: "fix: Security vulnerability in auth module",
      description: "Patches CVE-2024-1234",
      status: "MERGED",
      sourceBranch: "hotfix/security-patch",
      targetBranch: "main",
      authorName: "Security Bot",
      authorEmail: "security@example.com",
      url: "https://github.com/runners-high/frontend/pull/40",
      mergedAt: "2024-01-16T18:00:00Z",
      closedAt: null,
      createdAt: "2024-01-16T15:00:00Z",
      updatedAt: "2024-01-16T18:00:00Z",
      isDraft: false,
    },
    {
      id: "mr-4",
      externalId: "118",
      number: 38,
      title: "feat: Old feature implementation",
      description: "This feature was superseded",
      status: "CLOSED",
      sourceBranch: "feature/old-feature",
      targetBranch: "develop",
      authorName: "Old Developer",
      authorEmail: "old@example.com",
      url: "https://github.com/runners-high/frontend/pull/38",
      mergedAt: null,
      closedAt: "2024-01-15T14:00:00Z",
      createdAt: "2024-01-10T10:00:00Z",
      updatedAt: "2024-01-15T14:00:00Z",
      isDraft: false,
    },
  ],
  "repo-2": [
    {
      id: "mr-5",
      externalId: "50",
      number: 15,
      title: "feat: API rate limiting",
      description: "Adds rate limiting to all API endpoints",
      status: "OPEN",
      sourceBranch: "feature/rate-limit",
      targetBranch: "develop",
      authorName: "Backend Dev",
      authorEmail: "backend@example.com",
      url: "https://github.com/runners-high/backend/pull/15",
      mergedAt: null,
      closedAt: null,
      createdAt: "2024-01-18T10:00:00Z",
      updatedAt: "2024-01-19T09:00:00Z",
      isDraft: false,
    },
  ],
}

// =============================================================================
// Helper Functions
// =============================================================================

export function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}
