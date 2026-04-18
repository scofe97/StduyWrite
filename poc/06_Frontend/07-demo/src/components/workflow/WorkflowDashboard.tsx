import { useState } from 'react';
import {
  Search,
  Grid3X3,
  List,
  RefreshCw,
  Plus,
  Workflow,
  MoreVertical,
  Clock,
  CheckCircle2,
  XCircle,
} from 'lucide-react';

interface WorkflowItem {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'draft' | 'paused' | 'archived';
  runs: number;
  successRate: number;
  errors: number;
  lastRun: string;
  readers: number;
}

const mockWorkflows: WorkflowItem[] = [
  {
    id: '1',
    name: 'Image to Video Pipeline',
    description: 'Automated pipeline: upload trigger → animator video illustrator',
    status: 'active',
    runs: 10,
    successRate: 10,
    errors: 9,
    lastRun: '1h ago',
    readers: 0,
  },
  {
    id: '2',
    name: 'Blank Canvas',
    description: 'Start from scratch with an empty workflow',
    status: 'draft',
    runs: 0,
    successRate: 0,
    errors: 0,
    lastRun: 'Never',
    readers: 0,
  },
  {
    id: '3',
    name: 'Text to Image Generator',
    description: 'AI-powered text to image generation workflow',
    status: 'active',
    runs: 156,
    successRate: 94,
    errors: 10,
    lastRun: '2m ago',
    readers: 3,
  },
  {
    id: '4',
    name: 'Video Transcription',
    description: 'Automatic video transcription and subtitle generation',
    status: 'paused',
    runs: 42,
    successRate: 88,
    errors: 5,
    lastRun: '2d ago',
    readers: 1,
  },
];

type FilterType = 'all' | 'draft' | 'active' | 'paused' | 'archived';

interface WorkflowDashboardProps {
  onCreateNew?: () => void;
  onSelectWorkflow?: (id: string) => void;
}

export default function WorkflowDashboard({ onCreateNew, onSelectWorkflow }: WorkflowDashboardProps) {
  const [filter, setFilter] = useState<FilterType>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const filteredWorkflows = mockWorkflows.filter((workflow) => {
    const matchesFilter = filter === 'all' || workflow.status === filter;
    const matchesSearch = workflow.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const getStatusBadge = (status: WorkflowItem['status']) => {
    switch (status) {
      case 'active':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            Active
          </span>
        );
      case 'draft':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-purple-500/20 text-purple-400 border border-purple-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />
            Draft
          </span>
        );
      case 'paused':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-yellow-500/20 text-yellow-400 border border-yellow-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-yellow-400" />
            Paused
          </span>
        );
      case 'archived':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-gray-500/20 text-gray-400 border border-gray-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-gray-400" />
            Archived
          </span>
        );
    }
  };

  const filterTabs: { key: FilterType; label: string }[] = [
    { key: 'all', label: '전체' },
    { key: 'draft', label: '초안' },
    { key: 'active', label: '활성' },
    { key: 'paused', label: '일시정지' },
    { key: 'archived', label: '보관함' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* 헤더 */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">내 워크플로우</h1>
          <p className="text-sm text-gray-400">AI 자동화 워크플로우를 생성하고 관리하세요</p>
        </div>
        <button
          onClick={onCreateNew}
          className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
        >
          <Plus className="w-4 h-4" />
          새 워크플로우
        </button>
      </div>

      {/* 검색 */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
        <input
          type="text"
          placeholder="검색..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2.5 bg-gray-900 border border-gray-800 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
        />
      </div>

      {/* 필터 및 정렬 */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-6">
          {/* 필터 탭 */}
          <div className="flex items-center gap-1 bg-gray-900 rounded-lg p-1">
            {filterTabs.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setFilter(tab.key)}
                className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                  filter === tab.key
                    ? 'bg-purple-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* 정렬 */}
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <span>정렬:</span>
            <select className="bg-gray-900 border border-gray-800 rounded px-2 py-1 text-white focus:outline-none focus:border-purple-500">
              <option>수정일</option>
              <option>생성일</option>
              <option>이름</option>
            </select>
            <select className="bg-gray-900 border border-gray-800 rounded px-2 py-1 text-white focus:outline-none focus:border-purple-500">
              <option>최신순</option>
              <option>오래된순</option>
            </select>
          </div>
        </div>

        {/* 뷰 모드 */}
        <div className="flex items-center gap-1 bg-gray-900 rounded-lg p-1">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-1.5 rounded ${viewMode === 'grid' ? 'bg-gray-800 text-white' : 'text-gray-500'}`}
          >
            <Grid3X3 className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`p-1.5 rounded ${viewMode === 'list' ? 'bg-gray-800 text-white' : 'text-gray-500'}`}
          >
            <List className="w-4 h-4" />
          </button>
          <button className="p-1.5 rounded text-gray-500 hover:text-white">
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 워크플로우 카드 그리드 */}
      <div className={`grid gap-4 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'}`}>
        {filteredWorkflows.map((workflow) => (
          <div
            key={workflow.id}
            onClick={() => onSelectWorkflow?.(workflow.id)}
            className="group bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-purple-500/50 transition-all cursor-pointer"
          >
            {/* 카드 헤더 */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
                  <Workflow className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-medium text-white group-hover:text-purple-400 transition-colors">
                    {workflow.name}
                  </h3>
                  <p className="text-xs text-gray-500 line-clamp-1">{workflow.description}</p>
                </div>
              </div>
              <button
                onClick={(e) => e.stopPropagation()}
                className="p-1 text-gray-500 hover:text-white opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <MoreVertical className="w-4 h-4" />
              </button>
            </div>

            {/* 상태 배지 */}
            <div className="mb-4">{getStatusBadge(workflow.status)}</div>

            {/* 통계 */}
            <div className="grid grid-cols-3 gap-2 mb-3">
              <div className="text-center">
                <div className="text-lg font-semibold text-white">{workflow.runs}</div>
                <div className="text-xs text-gray-500">Runs</div>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center gap-1">
                  <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                  <span className="text-lg font-semibold text-emerald-400">{workflow.successRate}%</span>
                </div>
                <div className="text-xs text-gray-500">Success</div>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center gap-1">
                  <XCircle className="w-3 h-3 text-red-400" />
                  <span className="text-lg font-semibold text-red-400">{workflow.errors}</span>
                </div>
                <div className="text-xs text-gray-500">Errors</div>
              </div>
            </div>

            {/* 푸터 */}
            <div className="flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-800">
              <div className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                <span>Last run: {workflow.lastRun}</span>
              </div>
              <span>{workflow.readers} readers</span>
            </div>
          </div>
        ))}
      </div>

      {/* 빈 상태 */}
      {filteredWorkflows.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-gray-500">
          <Workflow className="w-12 h-12 mb-4 opacity-50" />
          <p className="text-lg mb-2">워크플로우가 없습니다</p>
          <p className="text-sm">새 워크플로우를 만들어보세요</p>
        </div>
      )}
    </div>
  );
}
