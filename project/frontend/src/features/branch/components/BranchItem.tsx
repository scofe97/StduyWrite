import { formatDistanceToNow } from "date-fns"
import { GitBranchIcon, ShieldLockIcon, TrashIcon } from "@primer/octicons-react"

import { Button } from "@/components/ui/button"
import { BranchTypeBadge } from "./BranchTypeBadge"
import type { Branch } from "@/services/branch/types"

interface BranchItemProps {
  branch: Branch
  defaultBranch: string
  onCreatePR?: (branchName: string) => void
  onDelete?: (branchId: string) => void
}

export function BranchItem({
  branch,
  defaultBranch,
  onCreatePR,
  onDelete,
}: BranchItemProps) {
  const timeAgo = formatDistanceToNow(new Date(branch.updatedAt), {
    addSuffix: true,
  })

  const isDefault = branch.name === defaultBranch
  const canDelete = !isDefault && !branch.isProtected && branch.status !== "MERGED"

  return (
    <div className="flex items-center justify-between py-3 px-4 border-b last:border-b-0 hover:bg-accent/50">
      <div className="flex items-center gap-3 min-w-0">
        <GitBranchIcon size={16} className="text-muted-foreground shrink-0" />
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-medium truncate">{branch.name}</span>
            {isDefault && (
              <span className="text-xs text-muted-foreground">(default)</span>
            )}
            {branch.isProtected && (
              <span title="Protected branch">
                <ShieldLockIcon
                  size={14}
                  className="text-yellow-500"
                />
              </span>
            )}
          </div>
          <div className="flex items-center gap-3 mt-1">
            <BranchTypeBadge type={branch.branchType} />
            <span className="text-xs text-muted-foreground">
              Updated {timeAgo}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        {!isDefault && branch.status === "ACTIVE" && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => onCreatePR?.(branch.name)}
          >
            New PR
          </Button>
        )}
        {canDelete && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete?.(branch.id)}
            className="text-destructive hover:text-destructive"
          >
            <TrashIcon size={14} />
          </Button>
        )}
      </div>
    </div>
  )
}
