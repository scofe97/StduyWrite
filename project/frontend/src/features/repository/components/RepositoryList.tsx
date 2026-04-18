import { useState, useMemo } from "react"
import { useSearchParams } from "react-router-dom"
import { RepoIcon } from "@primer/octicons-react"
import { Search } from "lucide-react"

import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { RepositoryCard } from "./RepositoryCard"
import { EmptyState, LoadingState } from "@/components/common"
import { useActiveConnections } from "@/services/connection/hooks"
import { useRepositoriesByConnection } from "@/services/repository/hooks"

export function RepositoryList() {
  const [searchParams] = useSearchParams()
  const connectionIdParam = searchParams.get("connectionId")

  const [searchQuery, setSearchQuery] = useState("")
  const [selectedConnectionId, setSelectedConnectionId] = useState<string>(
    connectionIdParam || "all"
  )

  const { data: connections, isLoading: connectionsLoading } = useActiveConnections()

  // Get repositories for selected connection or all
  const { data: repositories, isLoading: reposLoading } = useRepositoriesByConnection(
    selectedConnectionId !== "all" ? selectedConnectionId : "",
    { enabled: selectedConnectionId !== "all" }
  )

  const filteredRepositories = useMemo(() => {
    if (!repositories) return []

    if (!searchQuery) return repositories

    const query = searchQuery.toLowerCase()
    return repositories.filter(
      (repo) =>
        repo.name.toLowerCase().includes(query) ||
        repo.namespace.toLowerCase().includes(query) ||
        repo.repositoryName.toLowerCase().includes(query)
    )
  }, [repositories, searchQuery])

  const isLoading = connectionsLoading || reposLoading

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search repositories..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select
          value={selectedConnectionId}
          onValueChange={setSelectedConnectionId}
        >
          <SelectTrigger className="w-full sm:w-[200px]">
            <SelectValue placeholder="Select provider" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Providers</SelectItem>
            {connections?.map((connection) => (
              <SelectItem key={connection.id} value={connection.id}>
                {connection.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {isLoading ? (
        <LoadingState variant="list" count={5} />
      ) : selectedConnectionId === "all" ? (
        <EmptyState
          icon={<RepoIcon size={48} />}
          title="Select a provider"
          description="Choose a connection from the dropdown to view its repositories"
        />
      ) : filteredRepositories.length === 0 ? (
        <EmptyState
          icon={<RepoIcon size={48} />}
          title="No repositories found"
          description={
            searchQuery
              ? "Try adjusting your search query"
              : "No repositories registered for this connection"
          }
        />
      ) : (
        <div className="space-y-3">
          {filteredRepositories.map((repository) => (
            <RepositoryCard key={repository.id} repository={repository} />
          ))}
        </div>
      )}
    </div>
  )
}
