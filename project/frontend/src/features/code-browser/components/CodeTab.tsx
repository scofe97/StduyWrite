import { useState, useMemo } from "react"
import { FileDirectoryIcon } from "@primer/octicons-react"

import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { BranchSelector } from "./BranchSelector"
import { FileTree } from "./FileTree"
import { FileViewer } from "./FileViewer"
import { ReadmePreview } from "./ReadmePreview"
import { LoadingState, EmptyState } from "@/components/common"
import { useTree, useContents } from "@/services/contents/hooks"
import { useBranchesByRepository } from "@/services/branch/hooks"
import type { Repository } from "@/services/repository/types"

interface CodeTabProps {
  repository: Repository
}

export function CodeTab({ repository }: CodeTabProps) {
  const [currentBranch, setCurrentBranch] = useState(repository.defaultBranch)
  const [selectedPath, setSelectedPath] = useState<string>("")
  const [selectedType, setSelectedType] = useState<"FILE" | "DIRECTORY">("DIRECTORY")

  const { data: branches, isLoading: branchesLoading } = useBranchesByRepository(
    repository.id
  )

  const { data: treeEntries, isLoading: treeLoading } = useTree({
    connectionId: repository.connectionId,
    namespace: repository.namespace,
    repository: repository.repositoryName,
    ref: currentBranch,
    recursive: true,
  })

  const { data: fileContent, isLoading: fileLoading } = useContents(
    {
      connectionId: repository.connectionId,
      namespace: repository.namespace,
      repository: repository.repositoryName,
      path: selectedPath,
      ref: currentBranch,
    },
    {
      enabled: selectedType === "FILE" && !!selectedPath,
    }
  )

  // Find README file
  const readmePath = useMemo(() => {
    if (!treeEntries) return null
    const readmeEntry = treeEntries.find(
      (entry) =>
        entry.type === "FILE" &&
        entry.path.toLowerCase() === "readme.md"
    )
    return readmeEntry?.path || null
  }, [treeEntries])

  const { data: readmeContent, isLoading: readmeLoading } = useContents(
    {
      connectionId: repository.connectionId,
      namespace: repository.namespace,
      repository: repository.repositoryName,
      path: readmePath || "",
      ref: currentBranch,
    },
    {
      enabled: !!readmePath && !selectedPath,
    }
  )

  const handlePathChange = (path: string, type: "FILE" | "DIRECTORY") => {
    setSelectedPath(path)
    setSelectedType(type)
  }

  const handleBranchChange = (branchName: string) => {
    setCurrentBranch(branchName)
    setSelectedPath("")
    setSelectedType("DIRECTORY")
  }

  if (branchesLoading || treeLoading) {
    return <LoadingState variant="detail" />
  }

  return (
    <div className="space-y-4">
      {/* Branch selector */}
      <div className="flex items-center gap-4">
        <BranchSelector
          branches={branches || []}
          currentBranch={currentBranch}
          onBranchChange={handleBranchChange}
          defaultBranch={repository.defaultBranch}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {/* File tree */}
        <Card className="lg:col-span-1">
          <CardContent className="p-0">
            <ScrollArea className="h-[600px]">
              {treeEntries && treeEntries.length > 0 ? (
                <FileTree
                  entries={treeEntries}
                  currentPath={selectedPath}
                  onPathChange={handlePathChange}
                />
              ) : (
                <EmptyState
                  icon={<FileDirectoryIcon size={32} />}
                  title="No files"
                  description="This repository appears to be empty"
                />
              )}
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Content area */}
        <div className="lg:col-span-3">
          {selectedType === "FILE" && selectedPath ? (
            <FileViewer
              path={selectedPath}
              content={fileContent?.content || null}
              isLoading={fileLoading}
              encoding={fileContent?.encoding}
            />
          ) : (
            <ReadmePreview
              content={readmeContent?.content || null}
              isLoading={readmeLoading}
              encoding={readmeContent?.encoding}
            />
          )}
        </div>
      </div>
    </div>
  )
}
