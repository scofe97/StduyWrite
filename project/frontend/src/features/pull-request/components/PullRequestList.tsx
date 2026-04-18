import { GitPullRequestIcon } from "@primer/octicons-react"

import { Card, CardContent } from "@/components/ui/card"
import { PullRequestItem } from "./PullRequestItem"
import { EmptyState } from "@/components/common"
import type { MergeRequest } from "@/services/merge-request/types"

interface PullRequestListProps {
  pullRequests: MergeRequest[]
  repositoryId: string
}

export function PullRequestList({ pullRequests, repositoryId }: PullRequestListProps) {
  if (pullRequests.length === 0) {
    return (
      <EmptyState
        icon={<GitPullRequestIcon size={48} />}
        title="No pull requests found"
        description="There are no pull requests matching your filter"
      />
    )
  }

  return (
    <Card>
      <CardContent className="p-0">
        {pullRequests.map((pr) => (
          <PullRequestItem
            key={pr.id}
            pullRequest={pr}
            repositoryId={repositoryId}
          />
        ))}
      </CardContent>
    </Card>
  )
}
