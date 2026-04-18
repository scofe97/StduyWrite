import { useNavigate } from "react-router-dom"
import { formatDistanceToNow } from "date-fns"
import { RepoIcon, GitBranchIcon } from "@primer/octicons-react"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { getProviderIcon, getProviderLabel } from "@/lib/provider-registry"
import type { Repository } from "@/services/repository/types"

interface RepositoryCardProps {
  repository: Repository
}

const strategyLabels: Record<string, string> = {
  GIT_FLOW: "Git Flow",
  GITHUB_FLOW: "GitHub Flow",
  TRUNK_BASED: "Trunk Based",
}

export function RepositoryCard({ repository }: RepositoryCardProps) {
  const navigate = useNavigate()
  const ProviderIcon = getProviderIcon(repository.providerType.toLowerCase())
  const timeAgo = formatDistanceToNow(new Date(repository.updatedAt), {
    addSuffix: true,
  })

  const handleClick = () => {
    navigate(`/repositories/${repository.id}`)
  }

  return (
    <Card
      className="hover:shadow-md transition-shadow cursor-pointer"
      onClick={handleClick}
    >
      <CardContent className="pt-4">
        <div className="space-y-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <RepoIcon size={16} className="text-muted-foreground" />
              <span className="font-semibold hover:text-primary">
                {repository.namespace}/{repository.repositoryName}
              </span>
            </div>
            <Badge variant="outline" className="gap-1">
              <ProviderIcon size={12} />
              {getProviderLabel(repository.providerType.toLowerCase())}
            </Badge>
          </div>

          {repository.name !== `${repository.namespace}/${repository.repositoryName}` && (
            <p className="text-sm text-muted-foreground line-clamp-2">
              {repository.name}
            </p>
          )}

          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <GitBranchIcon size={12} />
              {repository.defaultBranch}
            </span>
            <span className="flex items-center gap-1">
              {strategyLabels[repository.strategyType] || repository.strategyType}
            </span>
            <span>Updated {timeAgo}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
