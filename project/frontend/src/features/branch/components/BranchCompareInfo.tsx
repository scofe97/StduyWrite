import { ArrowUpIcon, ArrowDownIcon } from "@primer/octicons-react"

interface BranchCompareInfoProps {
  ahead?: number
  behind?: number
  baseBranch?: string
}

export function BranchCompareInfo({
  ahead = 0,
  behind = 0,
  baseBranch = "main",
}: BranchCompareInfoProps) {
  if (ahead === 0 && behind === 0) {
    return (
      <span className="text-xs text-muted-foreground">
        Up to date with {baseBranch}
      </span>
    )
  }

  return (
    <div className="flex items-center gap-2 text-xs">
      {ahead > 0 && (
        <span className="flex items-center gap-1 text-green-600 dark:text-green-400">
          <ArrowUpIcon size={12} />
          {ahead} ahead
        </span>
      )}
      {behind > 0 && (
        <span className="flex items-center gap-1 text-orange-600 dark:text-orange-400">
          <ArrowDownIcon size={12} />
          {behind} behind
        </span>
      )}
      <span className="text-muted-foreground">of {baseBranch}</span>
    </div>
  )
}
