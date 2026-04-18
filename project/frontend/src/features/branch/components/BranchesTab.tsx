import { useState } from "react"
import { Plus, Search } from "lucide-react"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { BranchList } from "./BranchList"
import { LoadingState } from "@/components/common"
import { useBranchesByRepository, useDeleteBranch } from "@/services/branch/hooks"
import { useRepository } from "@/services/repository/hooks"

interface BranchesTabProps {
  repositoryId: string
}

export function BranchesTab({ repositoryId }: BranchesTabProps) {
  const [searchQuery, setSearchQuery] = useState("")

  const { data: repository } = useRepository(repositoryId)
  const { data: branches, isLoading } = useBranchesByRepository(repositoryId)
  const deleteMutation = useDeleteBranch()

  const handleCreatePR = (branchName: string) => {
    // Navigate to PR creation - would need to integrate with PR creation flow
    console.log("Create PR for branch:", branchName)
  }

  const handleDelete = (branchId: string) => {
    if (confirm("Are you sure you want to delete this branch?")) {
      deleteMutation.mutate(branchId)
    }
  }

  const filteredBranches = branches?.filter((branch) =>
    branch.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  if (isLoading) {
    return <LoadingState variant="list" count={5} />
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Find a branch..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          New Branch
        </Button>
      </div>

      <BranchList
        branches={filteredBranches || []}
        defaultBranch={repository?.defaultBranch || "main"}
        onCreatePR={handleCreatePR}
        onDelete={handleDelete}
      />
    </div>
  )
}
