import { useState } from "react"
import { FileIcon, FileDirectoryIcon, ChevronRightIcon, ChevronDownIcon } from "@primer/octicons-react"

import { cn } from "@/lib/utils"
import type { TreeEntry } from "@/services/contents/types"

interface FileTreeItemProps {
  entry: TreeEntry
  depth: number
  isSelected: boolean
  onClick: (entry: TreeEntry) => void
  children?: React.ReactNode
}

const fileTypeIcons: Record<string, { icon: string; color: string }> = {
  ".ts": { icon: "TS", color: "text-blue-500" },
  ".tsx": { icon: "TSX", color: "text-blue-400" },
  ".js": { icon: "JS", color: "text-yellow-500" },
  ".jsx": { icon: "JSX", color: "text-yellow-400" },
  ".json": { icon: "{}", color: "text-yellow-600" },
  ".md": { icon: "MD", color: "text-gray-500" },
  ".css": { icon: "CSS", color: "text-purple-500" },
  ".html": { icon: "HTML", color: "text-orange-500" },
  ".java": { icon: "JV", color: "text-red-500" },
  ".py": { icon: "PY", color: "text-green-500" },
  ".yml": { icon: "YML", color: "text-pink-500" },
  ".yaml": { icon: "YML", color: "text-pink-500" },
}

function getFileExtension(path: string): string {
  const match = path.match(/\.[^.]+$/)
  return match ? match[0].toLowerCase() : ""
}

export function FileTreeItem({
  entry,
  depth,
  isSelected,
  onClick,
  children,
}: FileTreeItemProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const isDirectory = entry.type === "DIRECTORY"
  const fileName = entry.path.split("/").pop() || entry.path
  const extension = getFileExtension(fileName)
  const fileType = fileTypeIcons[extension]

  const handleClick = () => {
    if (isDirectory) {
      setIsExpanded(!isExpanded)
    }
    onClick(entry)
  }

  return (
    <div>
      <button
        className={cn(
          "w-full flex items-center gap-2 px-2 py-1 text-sm hover:bg-accent rounded-sm text-left",
          isSelected && "bg-accent"
        )}
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
        onClick={handleClick}
      >
        {isDirectory ? (
          <>
            {isExpanded ? (
              <ChevronDownIcon size={14} className="text-muted-foreground shrink-0" />
            ) : (
              <ChevronRightIcon size={14} className="text-muted-foreground shrink-0" />
            )}
            <FileDirectoryIcon size={14} className="text-blue-400 shrink-0" />
          </>
        ) : (
          <>
            <span className="w-[14px]" />
            {fileType ? (
              <span className={cn("text-xs font-mono shrink-0", fileType.color)}>
                {fileType.icon}
              </span>
            ) : (
              <FileIcon size={14} className="text-muted-foreground shrink-0" />
            )}
          </>
        )}
        <span className="truncate">{fileName}</span>
      </button>
      {isDirectory && isExpanded && children}
    </div>
  )
}
