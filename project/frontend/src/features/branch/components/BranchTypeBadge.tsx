import { Badge } from "@/components/ui/badge"
import type { BranchType } from "@/services/branch/types"

interface BranchTypeBadgeProps {
  type: BranchType
}

const branchTypeConfig: Record<BranchType, { label: string; color: string }> = {
  MAIN: { label: "Main", color: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200" },
  DEVELOP: { label: "Develop", color: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200" },
  FEATURE: { label: "Feature", color: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200" },
  RELEASE: { label: "Release", color: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200" },
  HOTFIX: { label: "Hotfix", color: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200" },
  BUGFIX: { label: "Bugfix", color: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200" },
  OTHER: { label: "Other", color: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200" },
}

export function BranchTypeBadge({ type }: BranchTypeBadgeProps) {
  const config = branchTypeConfig[type] || branchTypeConfig.OTHER

  return (
    <Badge variant="outline" className={config.color}>
      {config.label}
    </Badge>
  )
}
