import {
  GitPullRequestIcon,
  GitMergeIcon,
  GitPullRequestClosedIcon,
  GitPullRequestDraftIcon,
} from "@primer/octicons-react"

import { Badge } from "@/components/ui/badge"
import type { MergeRequestStatus } from "@/services/merge-request/types"

interface PullRequestStatusBadgeProps {
  status: MergeRequestStatus
  isDraft?: boolean
}

const statusConfig: Record<
  MergeRequestStatus,
  { label: string; icon: React.ElementType; variant: "default" | "secondary" | "destructive" | "outline" }
> = {
  OPEN: {
    label: "Open",
    icon: GitPullRequestIcon,
    variant: "default",
  },
  MERGED: {
    label: "Merged",
    icon: GitMergeIcon,
    variant: "secondary",
  },
  CLOSED: {
    label: "Closed",
    icon: GitPullRequestClosedIcon,
    variant: "destructive",
  },
  DRAFT: {
    label: "Draft",
    icon: GitPullRequestDraftIcon,
    variant: "outline",
  },
}

export function PullRequestStatusBadge({
  status,
  isDraft,
}: PullRequestStatusBadgeProps) {
  // If it's a draft, override the status display
  const effectiveStatus = isDraft && status === "OPEN" ? "DRAFT" : status
  const config = statusConfig[effectiveStatus]
  const Icon = config.icon

  return (
    <Badge variant={config.variant} className="gap-1">
      <Icon size={12} />
      {config.label}
    </Badge>
  )
}
