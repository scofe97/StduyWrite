import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import type { MergeRequestStatus } from "@/services/merge-request/types"

interface PullRequestFiltersProps {
  currentStatus: MergeRequestStatus | "all"
  onStatusChange: (status: MergeRequestStatus | "all") => void
  counts?: {
    open: number
    closed: number
    merged: number
  }
}

export function PullRequestFilters({
  currentStatus,
  onStatusChange,
  counts,
}: PullRequestFiltersProps) {
  return (
    <Tabs value={currentStatus} onValueChange={(v) => onStatusChange(v as MergeRequestStatus | "all")}>
      <TabsList>
        <TabsTrigger value="all" className="gap-2">
          All
        </TabsTrigger>
        <TabsTrigger value="OPEN" className="gap-2">
          Open
          {counts?.open !== undefined && counts.open > 0 && (
            <span className="ml-1 rounded-full bg-green-500/20 px-2 py-0.5 text-xs text-green-600 dark:text-green-400">
              {counts.open}
            </span>
          )}
        </TabsTrigger>
        <TabsTrigger value="MERGED" className="gap-2">
          Merged
          {counts?.merged !== undefined && counts.merged > 0 && (
            <span className="ml-1 rounded-full bg-purple-500/20 px-2 py-0.5 text-xs text-purple-600 dark:text-purple-400">
              {counts.merged}
            </span>
          )}
        </TabsTrigger>
        <TabsTrigger value="CLOSED" className="gap-2">
          Closed
          {counts?.closed !== undefined && counts.closed > 0 && (
            <span className="ml-1 rounded-full bg-red-500/20 px-2 py-0.5 text-xs text-red-600 dark:text-red-400">
              {counts.closed}
            </span>
          )}
        </TabsTrigger>
      </TabsList>
    </Tabs>
  )
}
