import { RepoIcon, GitBranchIcon, GitPullRequestIcon } from "@primer/octicons-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface RepositoryStatsProps {
  repositoryCount: number
  branchCount?: number
  pullRequestCount?: number
}

export function RepositoryStats({
  repositoryCount,
  branchCount = 0,
  pullRequestCount = 0,
}: RepositoryStatsProps) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Repositories</CardTitle>
          <RepoIcon size={16} className="text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{repositoryCount}</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Active Branches</CardTitle>
          <GitBranchIcon size={16} className="text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{branchCount}</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Open PRs</CardTitle>
          <GitPullRequestIcon size={16} className="text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{pullRequestCount}</div>
        </CardContent>
      </Card>
    </div>
  )
}
