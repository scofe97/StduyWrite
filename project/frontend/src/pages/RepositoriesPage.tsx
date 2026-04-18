import { RepositoryList } from "@/features/repository/components/RepositoryList"

export function RepositoriesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Repositories</h1>
        <p className="text-muted-foreground">
          Browse and manage your connected repositories
        </p>
      </div>
      <RepositoryList />
    </div>
  )
}
