import { Plus } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useActiveConnections } from "@/services/connection/hooks"
import { ConnectionStatusBadge } from "@/features/connection/components/ConnectionStatusBadge"
import { getProviderIcon, getProviderLabel, getProviderColor } from "@/lib/provider-registry"
import { LoadingState } from "@/components/common"

export function ProvidersSettings() {
  const { data: connections, isLoading } = useActiveConnections()

  if (isLoading) {
    return <LoadingState variant="list" count={3} />
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Connected Providers</CardTitle>
            <CardDescription>
              Manage your Git provider connections.
            </CardDescription>
          </div>
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Add Provider
          </Button>
        </CardHeader>
        <CardContent>
          {connections && connections.length > 0 ? (
            <div className="space-y-4">
              {connections.map((connection) => {
                const ProviderIcon = getProviderIcon(connection.providerType.toLowerCase())
                const providerColor = getProviderColor(connection.providerType.toLowerCase())

                return (
                  <div
                    key={connection.id}
                    className="flex items-center justify-between py-3 border-b last:border-b-0"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className="flex h-10 w-10 items-center justify-center rounded-lg text-white"
                        style={{ backgroundColor: providerColor }}
                      >
                        <ProviderIcon size={20} />
                      </div>
                      <div>
                        <p className="font-medium">{connection.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {getProviderLabel(connection.providerType.toLowerCase())}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <ConnectionStatusBadge status={connection.status} />
                      <Button variant="outline" size="sm">
                        Configure
                      </Button>
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <p className="text-center text-muted-foreground py-8">
              No providers connected yet. Add a provider to get started.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
