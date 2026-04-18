import { useMemo } from "react"

import { FileTreeItem } from "./FileTreeItem"
import type { TreeEntry } from "@/services/contents/types"

interface FileTreeProps {
  entries: TreeEntry[]
  currentPath: string
  onPathChange: (path: string, type: "FILE" | "DIRECTORY") => void
}

interface TreeNode {
  entry: TreeEntry
  children: TreeNode[]
}

function buildTree(entries: TreeEntry[]): TreeNode[] {
  // Sort entries: directories first, then files
  const sortedEntries = [...entries].sort((a, b) => {
    if (a.type === "DIRECTORY" && b.type !== "DIRECTORY") return -1
    if (a.type !== "DIRECTORY" && b.type === "DIRECTORY") return 1
    return a.path.localeCompare(b.path)
  })

  // Group by top-level path
  const rootNodes: TreeNode[] = []
  const pathMap = new Map<string, TreeNode>()

  for (const entry of sortedEntries) {
    const parts = entry.path.split("/")
    const isRootLevel = parts.length === 1

    const node: TreeNode = {
      entry,
      children: [],
    }
    pathMap.set(entry.path, node)

    if (isRootLevel) {
      rootNodes.push(node)
    } else {
      // Find parent
      const parentPath = parts.slice(0, -1).join("/")
      const parent = pathMap.get(parentPath)
      if (parent) {
        parent.children.push(node)
      } else {
        // Parent not found, add to root
        rootNodes.push(node)
      }
    }
  }

  return rootNodes
}

function TreeNodeComponent({
  node,
  depth,
  currentPath,
  onPathChange,
}: {
  node: TreeNode
  depth: number
  currentPath: string
  onPathChange: (path: string, type: "FILE" | "DIRECTORY") => void
}) {
  const isSelected = currentPath === node.entry.path

  return (
    <FileTreeItem
      entry={node.entry}
      depth={depth}
      isSelected={isSelected}
      onClick={(entry) => {
        onPathChange(entry.path, entry.type as "FILE" | "DIRECTORY")
      }}
    >
      {node.children.map((child) => (
        <TreeNodeComponent
          key={child.entry.path}
          node={child}
          depth={depth + 1}
          currentPath={currentPath}
          onPathChange={onPathChange}
        />
      ))}
    </FileTreeItem>
  )
}

export function FileTree({ entries, currentPath, onPathChange }: FileTreeProps) {
  const tree = useMemo(() => buildTree(entries), [entries])

  if (entries.length === 0) {
    return (
      <div className="p-4 text-sm text-muted-foreground text-center">
        No files found
      </div>
    )
  }

  return (
    <div className="py-2">
      {tree.map((node) => (
        <TreeNodeComponent
          key={node.entry.path}
          node={node}
          depth={0}
          currentPath={currentPath}
          onPathChange={onPathChange}
        />
      ))}
    </div>
  )
}
