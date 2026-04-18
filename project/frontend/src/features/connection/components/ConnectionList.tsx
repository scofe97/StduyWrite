import { PlugIcon } from "@primer/octicons-react"
import { Plus } from "lucide-react"

import { Button } from "@/components/ui/button"
import { ConnectionCard } from "./ConnectionCard"
import { EmptyState, LoadingState } from "@/components/common"
import { useActiveConnections } from "@/services/connection/hooks"
import { useRepositoriesByConnection } from "@/services/repository/hooks"
import type { Connection } from "@/services/connection/types"

function ConnectionCardWithCount({ connection }: { connection: Connection }) {
  const { data: repositories } = useRepositoriesByConnection(connection.id)
  return (
    <ConnectionCard
      connection={connection}
      repositoryCount={repositories?.length || 0}
    />
  )
}

export function ConnectionList() {
  const { data: connections, isLoading, error } = useActiveConnections()

  if (isLoading) {
    return <LoadingState variant="card" count={3} />
  }

  if (error) {
    return (
      <EmptyState
        icon={<PlugIcon size={48} />}
        title="Failed to load connections"
        description={error.message}
        action={
          <Button onClick={() => window.location.reload()}>
            Try again
          </Button>
        }
      />
    )
  }

  if (!connections || connections.length === 0) {
    return (
      <EmptyState
        icon={<PlugIcon size={48} />}
        title="No connections yet"
        description="Connect to a Git provider to start managing your repositories"
        action={
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Add Connection
          </Button>
        }
      />
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {connections.map((connection) => (
        <ConnectionCardWithCount key={connection.id} connection={connection} />
      ))}
    </div>
  )
}
