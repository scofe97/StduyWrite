import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function WorkflowsPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Workflows</h1>
      <Card>
        <CardHeader>
          <CardTitle>Coming Soon</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Workflow management will be available in the next update.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
