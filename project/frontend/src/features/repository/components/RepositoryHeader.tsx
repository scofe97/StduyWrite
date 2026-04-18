import { Link } from "react-router-dom"
import { formatDistanceToNow } from "date-fns"
import {
  RepoIcon,
  LinkExternalIcon,
  SyncIcon,
} from "@primer/octicons-react"
import { ChevronRight } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { getProviderIcon, getProviderLabel } from "@/lib/provider-registry"
import { useSyncRepository } from "@/services/repository/hooks"
import type { Repository } from "@/services/repository/types"

interface RepositoryHeaderProps {
  repository: Repository
}

const strategyLabels: Record<string, string> = {
  GIT_FLOW: "Git Flow",
  GITHUB_FLOW: "GitHub Flow",
  TRUNK_BASED: "Trunk Based",
}

export function RepositoryHeader({ repository }: RepositoryHeaderProps) {
  const ProviderIcon = getProviderIcon(repository.providerType.toLowerCase())
  const syncMutation = useSyncRepository()

  const timeAgo = formatDistanceToNow(new Date(repository.updatedAt), {
    addSuffix: true,
  })

  const handleSync = () => {
    syncMutation.mutate(repository.id)
  }

  return (
    <div className="space-y-4">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-1 text-sm text-muted-foreground">
        <Link
          to="/repositories"
          className="hover:text-foreground transition-colors"
        >
          Repositories
        </Link>
        <ChevronRight className="h-4 w-4" />
        <span className="flex items-center gap-1">
          <ProviderIcon size={14} />
          {getProviderLabel(repository.providerType.toLowerCase())}
        </span>
        <ChevronRight className="h-4 w-4" />
        <span>{repository.namespace}</span>
        <ChevronRight className="h-4 w-4" />
        <span className="text-foreground font-medium">
          {repository.repositoryName}
        </span>
      </nav>

      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <RepoIcon size={24} className="text-muted-foreground" />
            <h1 className="text-2xl font-bold">
              {repository.namespace}/{repository.repositoryName}
            </h1>
            <Badge variant="outline">
              {getProviderLabel(repository.providerType.toLowerCase())}
            </Badge>
          </div>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <span>{repository.defaultBranch}</span>
            <span>
              {strategyLabels[repository.strategyType] || repository.strategyType}
            </span>
            <span>Last sync: {timeAgo}</span>
          </div>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleSync}
            disabled={syncMutation.isPending}
            className="gap-2"
          >
            <SyncIcon
              size={14}
              className={syncMutation.isPending ? "animate-spin" : ""}
            />
            Sync
          </Button>
          <Button variant="outline" size="sm" asChild>
            <a
              href={repository.gitUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="gap-2"
            >
              <LinkExternalIcon size={14} />
              Open in {getProviderLabel(repository.providerType.toLowerCase())}
            </a>
          </Button>
        </div>
      </div>

      <Separator />
    </div>
  )
}
