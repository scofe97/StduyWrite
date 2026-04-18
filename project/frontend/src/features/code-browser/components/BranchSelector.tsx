import { useState } from "react"
import { GitBranchIcon, CheckIcon } from "@primer/octicons-react"
import { ChevronsUpDown } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Badge } from "@/components/ui/badge"
import type { Branch } from "@/services/branch/types"

interface BranchSelectorProps {
  branches: Branch[]
  currentBranch: string
  onBranchChange: (branchName: string) => void
  defaultBranch?: string
}

const branchTypeColors: Record<string, string> = {
  MAIN: "bg-purple-500",
  DEVELOP: "bg-blue-500",
  FEATURE: "bg-green-500",
  RELEASE: "bg-orange-500",
  HOTFIX: "bg-red-500",
  BUGFIX: "bg-yellow-500",
  OTHER: "bg-gray-500",
}

export function BranchSelector({
  branches,
  currentBranch,
  onBranchChange,
  defaultBranch,
}: BranchSelectorProps) {
  const [open, setOpen] = useState(false)
  const [search, setSearch] = useState("")

  const filteredBranches = branches.filter((branch) =>
    branch.name.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[200px] justify-between"
        >
          <span className="flex items-center gap-2 truncate">
            <GitBranchIcon size={14} />
            <span className="truncate">{currentBranch}</span>
          </span>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[300px] p-0" align="start">
        <Command>
          <CommandInput
            placeholder="Find a branch..."
            value={search}
            onValueChange={setSearch}
          />
          <CommandList>
            <CommandEmpty>No branch found.</CommandEmpty>
            <CommandGroup heading="Branches">
              {filteredBranches.map((branch) => (
                <CommandItem
                  key={branch.id}
                  value={branch.name}
                  onSelect={() => {
                    onBranchChange(branch.name)
                    setOpen(false)
                  }}
                  className="flex items-center justify-between"
                >
                  <span className="flex items-center gap-2 truncate">
                    <span
                      className={`h-2 w-2 rounded-full ${
                        branchTypeColors[branch.branchType] || branchTypeColors.OTHER
                      }`}
                    />
                    <span className="truncate">{branch.name}</span>
                  </span>
                  <span className="flex items-center gap-2">
                    {branch.name === defaultBranch && (
                      <Badge variant="outline" className="text-xs">
                        default
                      </Badge>
                    )}
                    {currentBranch === branch.name && (
                      <CheckIcon size={14} className="text-primary" />
                    )}
                  </span>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
