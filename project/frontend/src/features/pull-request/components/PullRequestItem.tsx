import { Link } from "react-router-dom"
import { formatDistanceToNow } from "date-fns"
import {
  GitPullRequestIcon,
  GitBranchIcon,
} from "@primer/octicons-react"

import { PullRequestStatusBadge } from "./PullRequestStatusBadge"
import type { MergeRequest } from "@/services/merge-request/types"

interface PullRequestItemProps {
  pullRequest: MergeRequest
  repositoryId: string
}

export function PullRequestItem({ pullRequest, repositoryId }: PullRequestItemProps) {
  const timeAgo = formatDistanceToNow(new Date(pullRequest.createdAt), {
    addSuffix: true,
  })

  return (
    <div className="flex items-start gap-3 py-3 px-4 border-b last:border-b-0 hover:bg-accent/50">
      <div className="mt-1">
        <GitPullRequestIcon
          size={16}
          className={
            pullRequest.status === "OPEN"
              ? "text-green-500"
              : pullRequest.status === "MERGED"
                ? "text-purple-500"
                : "text-red-500"
          }
        />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <Link
            to={`/repositories/${repositoryId}/pulls/${pullRequest.number}`}
            className="font-medium hover:text-primary hover:underline"
          >
            {pullRequest.title}
          </Link>
          <PullRequestStatusBadge
            status={pullRequest.status}
            isDraft={pullRequest.isDraft}
          />
        </div>

        <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
          <span>#{pullRequest.number}</span>
          <span>opened {timeAgo}</span>
          <span>by {pullRequest.authorName}</span>
        </div>

        <div className="flex items-center gap-3 mt-2 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <GitBranchIcon size={12} />
            {pullRequest.sourceBranch}
          </span>
          <span>→</span>
          <span className="flex items-center gap-1">
            <GitBranchIcon size={12} />
            {pullRequest.targetBranch}
          </span>
        </div>
      </div>
    </div>
  )
}
