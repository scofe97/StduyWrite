import { useNavigate } from "react-router-dom"
import { ChevronRight, Settings } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ConnectionStatusBadge } from "./ConnectionStatusBadge"
import { getProviderIcon, getProviderLabel, getProviderColor } from "@/lib/provider-registry"
import type { Connection } from "@/services/connection/types"

interface ConnectionCardProps {
  connection: Connection
  repositoryCount?: number
}

export function ConnectionCard({ connection, repositoryCount = 0 }: ConnectionCardProps) {
  const navigate = useNavigate()
  const ProviderIcon = getProviderIcon(connection.providerType.toLowerCase())
  const providerColor = getProviderColor(connection.providerType.toLowerCase())

  const handleManage = () => {
    navigate(`/repositories?connectionId=${connection.id}`)
  }

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <div className="flex items-center gap-3">
          <div
            className="flex h-10 w-10 items-center justify-center rounded-lg text-white"
            style={{ backgroundColor: providerColor }}
          >
            <ProviderIcon size={20} />
          </div>
          <div>
            <CardTitle className="text-base font-semibold">
              {connection.name}
            </CardTitle>
            <p className="text-xs text-muted-foreground">
              {getProviderLabel(connection.providerType.toLowerCase())}
            </p>
          </div>
        </div>
        <ConnectionStatusBadge status={connection.status} />
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">
            <span className="font-medium text-foreground">{repositoryCount}</span>{" "}
            {repositoryCount === 1 ? "repository" : "repositories"}
          </div>
          <div className="flex gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate(`/settings/connections/${connection.id}`)}
            >
              <Settings className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleManage}
              className="gap-1"
            >
              Manage
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
