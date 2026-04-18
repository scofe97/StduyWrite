import { GitBranchIcon } from "@primer/octicons-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BranchItem } from "./BranchItem"
import { EmptyState } from "@/components/common"
import type { Branch } from "@/services/branch/types"

interface BranchListProps {
  branches: Branch[]
  defaultBranch: string
  onCreatePR?: (branchName: string) => void
  onDelete?: (branchId: string) => void
}

export function BranchList({
  branches,
  defaultBranch,
  onCreatePR,
  onDelete,
}: BranchListProps) {
  // Separate branches by status
  const activeBranches = branches.filter((b) => b.status === "ACTIVE")
  const mergedBranches = branches.filter((b) => b.status === "MERGED")
  const staleBranches = branches.filter((b) => b.status === "STALE")

  // Sort: default branch first, then by type priority, then alphabetically
  const typePriority: Record<string, number> = {
    MAIN: 0,
    DEVELOP: 1,
    RELEASE: 2,
    HOTFIX: 3,
    FEATURE: 4,
    BUGFIX: 5,
    OTHER: 6,
  }

  const sortBranches = (branchList: Branch[]) => {
    return [...branchList].sort((a, b) => {
      // Default branch first
      if (a.name === defaultBranch) return -1
      if (b.name === defaultBranch) return 1

      // Then by type priority
      const priorityDiff =
        (typePriority[a.branchType] || 6) - (typePriority[b.branchType] || 6)
      if (priorityDiff !== 0) return priorityDiff

      // Then alphabetically
      return a.name.localeCompare(b.name)
    })
  }

  if (branches.length === 0) {
    return (
      <EmptyState
        icon={<GitBranchIcon size={48} />}
        title="No branches found"
        description="This repository doesn't have any tracked branches yet"
      />
    )
  }

  return (
    <div className="space-y-4">
      {/* Active branches */}
      {activeBranches.length > 0 && (
        <Card>
          <CardHeader className="py-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-green-500" />
              Active ({activeBranches.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            {sortBranches(activeBranches).map((branch) => (
              <BranchItem
                key={branch.id}
                branch={branch}
                defaultBranch={defaultBranch}
                onCreatePR={onCreatePR}
                onDelete={onDelete}
              />
            ))}
          </CardContent>
        </Card>
      )}

      {/* Merged branches */}
      {mergedBranches.length > 0 && (
        <Card>
          <CardHeader className="py-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-purple-500" />
              Merged ({mergedBranches.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            {sortBranches(mergedBranches).map((branch) => (
              <BranchItem
                key={branch.id}
                branch={branch}
                defaultBranch={defaultBranch}
                onDelete={onDelete}
              />
            ))}
          </CardContent>
        </Card>
      )}

      {/* Stale branches */}
      {staleBranches.length > 0 && (
        <Card>
          <CardHeader className="py-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-gray-500" />
              Stale ({staleBranches.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            {sortBranches(staleBranches).map((branch) => (
              <BranchItem
                key={branch.id}
                branch={branch}
                defaultBranch={defaultBranch}
                onDelete={onDelete}
              />
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
