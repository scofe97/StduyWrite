import { useState, useMemo } from "react"
import { Plus, Search } from "lucide-react"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { PullRequestFilters } from "./PullRequestFilters"
import { PullRequestList } from "./PullRequestList"
import { LoadingState } from "@/components/common"
import { useMergeRequests } from "@/services/merge-request/hooks"
import type { Repository } from "@/services/repository/types"
import type { MergeRequestStatus } from "@/services/merge-request/types"

interface PullRequestsTabProps {
  repository: Repository
}

export function PullRequestsTab({ repository }: PullRequestsTabProps) {
  const [statusFilter, setStatusFilter] = useState<MergeRequestStatus | "all">("all")
  const [searchQuery, setSearchQuery] = useState("")

  const { data, isLoading } = useMergeRequests({
    connectionId: repository.connectionId,
    namespace: repository.namespace,
    repository: repository.repositoryName,
    status: statusFilter !== "all" ? statusFilter : undefined,
  })

  const filteredPRs = useMemo(() => {
    if (!data?.mergeRequests) return []

    if (!searchQuery) return data.mergeRequests

    const query = searchQuery.toLowerCase()
    return data.mergeRequests.filter(
      (pr) =>
        pr.title.toLowerCase().includes(query) ||
        pr.authorName.toLowerCase().includes(query) ||
        pr.sourceBranch.toLowerCase().includes(query) ||
        pr.targetBranch.toLowerCase().includes(query) ||
        pr.number.toString().includes(query)
    )
  }, [data?.mergeRequests, searchQuery])

  // Calculate counts for filters
  const counts = useMemo(() => {
    if (!data?.mergeRequests) return { open: 0, closed: 0, merged: 0 }

    return {
      open: data.mergeRequests.filter((pr) => pr.status === "OPEN").length,
      closed: data.mergeRequests.filter((pr) => pr.status === "CLOSED").length,
      merged: data.mergeRequests.filter((pr) => pr.status === "MERGED").length,
    }
  }, [data?.mergeRequests])

  if (isLoading) {
    return <LoadingState variant="list" count={5} />
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <PullRequestFilters
          currentStatus={statusFilter}
          onStatusChange={setStatusFilter}
          counts={counts}
        />
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          New Pull Request
        </Button>
      </div>

      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Search pull requests..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-9"
        />
      </div>

      <PullRequestList
        pullRequests={filteredPRs}
        repositoryId={repository.id}
      />
    </div>
  )
}
