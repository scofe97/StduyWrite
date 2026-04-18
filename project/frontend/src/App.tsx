import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

import { MainLayout } from "@/components/layout/MainLayout"
import { ConnectionsPage } from "@/pages/ConnectionsPage"
import { RepositoriesPage } from "@/pages/RepositoriesPage"
import { RepositoryDetailPage } from "@/pages/RepositoryDetailPage"
import { CICDPage } from "@/pages/CICDPage"
import { WorkflowsPage } from "@/pages/WorkflowsPage"
import { TicketsPage } from "@/pages/TicketsPage"
import { SettingsPage } from "@/pages/SettingsPage"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate to="/connections" replace />} />
            <Route path="connections" element={<ConnectionsPage />} />
            <Route path="repositories" element={<RepositoriesPage />} />
            <Route path="repositories/:id" element={<RepositoryDetailPage />} />
            <Route path="repositories/:id/code/*" element={<RepositoryDetailPage />} />
            <Route path="repositories/:id/branches" element={<RepositoryDetailPage />} />
            <Route path="repositories/:id/pulls" element={<RepositoryDetailPage />} />
            <Route path="repositories/:id/pulls/:number" element={<RepositoryDetailPage />} />
            <Route path="cicd" element={<CICDPage />} />
            <Route path="workflows" element={<WorkflowsPage />} />
            <Route path="tickets" element={<TicketsPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
