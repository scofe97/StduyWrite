import { useState } from 'react'
import { WorkflowCanvas } from './components/workflow'
import WorkflowDashboard from './components/workflow/WorkflowDashboard'
import Layout from './components/workflow/Layout'

type View = 'dashboard' | 'editor'

function App() {
  const [currentView, setCurrentView] = useState<View>('dashboard')
  const [, setSelectedWorkflowId] = useState<string | null>(null)

  const handleCreateNew = () => {
    setSelectedWorkflowId(null)
    setCurrentView('editor')
  }

  const handleSelectWorkflow = (id: string) => {
    setSelectedWorkflowId(id)
    setCurrentView('editor')
  }

  const handleBackToDashboard = () => {
    setCurrentView('dashboard')
  }

  return (
    <Layout activeMenu="workflow">
      {currentView === 'dashboard' ? (
        <WorkflowDashboard
          onCreateNew={handleCreateNew}
          onSelectWorkflow={handleSelectWorkflow}
        />
      ) : (
        <div className="relative h-[calc(100vh-56px)]">
          {/* 뒤로가기 버튼 */}
          <button
            onClick={handleBackToDashboard}
            className="absolute top-4 left-56 z-20 flex items-center gap-2 px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white rounded-lg text-sm transition-colors"
          >
            ← 대시보드
          </button>
          <WorkflowCanvas />
        </div>
      )}
    </Layout>
  )
}

export default App
