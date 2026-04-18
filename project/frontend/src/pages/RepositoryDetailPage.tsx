import { useParams, useLocation, useNavigate, Link } from "react-router-dom"
import { CodeIcon, GitBranchIcon, GitPullRequestIcon } from "@primer/octicons-react"

import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { RepositoryHeader } from "@/features/repository/components/RepositoryHeader"
import { LoadingState, EmptyState } from "@/components/common"
import { useRepository } from "@/services/repository/hooks"
import { useBranchesByRepository } from "@/services/branch/hooks"

// Lazy load tab contents
import { CodeTab } from "@/features/code-browser/components/CodeTab"
import { BranchesTab } from "@/features/branch/components/BranchesTab"
import { PullRequestsTab } from "@/features/pull-request/components/PullRequestsTab"

function getActiveTab(pathname: string): string {
  if (pathname.includes("/branches")) return "branches"
  if (pathname.includes("/pulls")) return "pulls"
  return "code"
}

export function RepositoryDetailPage() {
  const { id } = useParams<{ id: string }>()
  const location = useLocation()
  const navigate = useNavigate()

  const { data: repository, isLoading, error } = useRepository(id!)
  const { data: branches } = useBranchesByRepository(id!)

  const activeTab = getActiveTab(location.pathname)

  const handleTabChange = (value: string) => {
    if (value === "code") {
      navigate(`/repositories/${id}`)
    } else {
      navigate(`/repositories/${id}/${value}`)
    }
  }

  if (isLoading) {
    return <LoadingState variant="detail" />
  }

  if (error || !repository) {
    return (
      <EmptyState
        icon={<CodeIcon size={48} />}
        title="Repository not found"
        description={error?.message || "The repository you're looking for doesn't exist"}
        action={
          <Button asChild>
            <Link to="/repositories">Back to Repositories</Link>
          </Button>
        }
      />
    )
  }

  const activeBranchCount = branches?.filter((b) => b.status === "ACTIVE").length || 0

  return (
    <div className="space-y-6">
      <RepositoryHeader repository={repository} />

      <Tabs value={activeTab} onValueChange={handleTabChange}>
        <TabsList>
          <TabsTrigger value="code" className="gap-2">
            <CodeIcon size={14} />
            Code
          </TabsTrigger>
          <TabsTrigger value="branches" className="gap-2">
            <GitBranchIcon size={14} />
            Branches
            {activeBranchCount > 0 && (
              <span className="ml-1 rounded-full bg-muted-foreground/20 px-2 py-0.5 text-xs">
                {activeBranchCount}
              </span>
            )}
          </TabsTrigger>
          <TabsTrigger value="pulls" className="gap-2">
            <GitPullRequestIcon size={14} />
            Pull Requests
          </TabsTrigger>
        </TabsList>

        <TabsContent value="code" className="mt-6">
          <CodeTab repository={repository} />
        </TabsContent>

        <TabsContent value="branches" className="mt-6">
          <BranchesTab repositoryId={repository.id} />
        </TabsContent>

        <TabsContent value="pulls" className="mt-6">
          <PullRequestsTab repository={repository} />
        </TabsContent>
      </Tabs>
    </div>
  )
}
