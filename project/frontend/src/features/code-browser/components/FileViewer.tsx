import { FileIcon, CopyIcon } from "@primer/octicons-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Skeleton } from "@/components/ui/skeleton"

interface FileViewerProps {
  path: string
  content: string | null
  isLoading: boolean
  encoding?: string | null
}

function decodeContent(content: string | null, encoding: string | null): string {
  if (!content) return ""

  if (encoding === "base64") {
    try {
      return atob(content)
    } catch {
      return content
    }
  }

  return content
}

export function FileViewer({ path, content, isLoading, encoding }: FileViewerProps) {
  const fileName = path.split("/").pop() || path
  const decodedContent = decodeContent(content, encoding || null)
  const lines = decodedContent.split("\n")

  const handleCopy = () => {
    navigator.clipboard.writeText(decodedContent)
  }

  if (isLoading) {
    return (
      <Card>
        <CardHeader className="flex flex-row items-center justify-between py-3">
          <Skeleton className="h-5 w-40" />
          <Skeleton className="h-8 w-20" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="p-4 space-y-2">
            {Array.from({ length: 10 }).map((_, i) => (
              <Skeleton key={i} className="h-4" style={{ width: `${Math.random() * 50 + 30}%` }} />
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between py-3 px-4 border-b">
        <div className="flex items-center gap-2">
          <FileIcon size={14} className="text-muted-foreground" />
          <span className="text-sm font-medium">{fileName}</span>
          <span className="text-xs text-muted-foreground">
            {lines.length} lines
          </span>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={handleCopy}>
            <CopyIcon size={14} />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[500px]">
          <div className="relative">
            <table className="w-full text-sm font-mono">
              <tbody>
                {lines.map((line, index) => (
                  <tr
                    key={index}
                    className="hover:bg-accent/50 border-b border-border/50"
                  >
                    <td className="px-4 py-0.5 text-right text-muted-foreground select-none w-12 border-r border-border/50">
                      {index + 1}
                    </td>
                    <td className="px-4 py-0.5 whitespace-pre overflow-x-auto">
                      {line || " "}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
