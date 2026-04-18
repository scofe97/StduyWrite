import { BookIcon } from "@primer/octicons-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

interface ReadmePreviewProps {
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

export function ReadmePreview({ content, isLoading, encoding }: ReadmePreviewProps) {
  const decodedContent = decodeContent(content, encoding || null)

  if (isLoading) {
    return (
      <Card>
        <CardHeader className="flex flex-row items-center gap-2 py-3">
          <BookIcon size={14} />
          <Skeleton className="h-5 w-24" />
        </CardHeader>
        <CardContent className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-4" style={{ width: `${Math.random() * 40 + 40}%` }} />
          ))}
        </CardContent>
      </Card>
    )
  }

  if (!content) {
    return null
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center gap-2 py-3 border-b">
        <BookIcon size={14} className="text-muted-foreground" />
        <CardTitle className="text-sm font-medium">README.md</CardTitle>
      </CardHeader>
      <CardContent className="pt-4">
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <pre className="whitespace-pre-wrap font-sans text-sm">
            {decodedContent}
          </pre>
        </div>
      </CardContent>
    </Card>
  )
}
