import { Plus } from "lucide-react"

import { Button } from "@/components/ui/button"
import { ConnectionList } from "@/features/connection/components/ConnectionList"

export function ConnectionsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Connections</h1>
          <p className="text-muted-foreground">
            Manage your Git provider connections
          </p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          Add Connection
        </Button>
      </div>
      <ConnectionList />
    </div>
  )
}
