import { Badge } from "@/components/ui/badge"
import type { ConnectionStatus } from "@/services/connection/types"

interface ConnectionStatusBadgeProps {
  status: ConnectionStatus
}

const statusConfig: Record<ConnectionStatus, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
  ACTIVE: { label: "Active", variant: "default" },
  INACTIVE: { label: "Inactive", variant: "secondary" },
  ERROR: { label: "Error", variant: "destructive" },
}

export function ConnectionStatusBadge({ status }: ConnectionStatusBadgeProps) {
  const config = statusConfig[status]

  return (
    <Badge variant={config.variant} className="gap-1">
      <span
        className={`h-2 w-2 rounded-full ${
          status === "ACTIVE"
            ? "bg-green-500"
            : status === "ERROR"
              ? "bg-red-500"
              : "bg-gray-400"
        }`}
      />
      {config.label}
    </Badge>
  )
}
