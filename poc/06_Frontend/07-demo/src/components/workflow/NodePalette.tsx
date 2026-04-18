import { DragEvent } from 'react';
import {
  Clock,
  Scissors,
  Image,
  Zap,
  MessageSquare,
  Settings,
  FileOutput,
  Search,
  Edit3,
  Wrench,
  Download,
} from 'lucide-react';

interface NodeTypeItem {
  type: string;
  label: string;
  icon: React.ReactNode;
  category: string;
}

const nodeTypesList: NodeTypeItem[] = [
  // 트리거
  { type: 'trigger', label: '수동 트리거', icon: <Zap className="w-4 h-4" />, category: '트리거' },
  { type: 'trigger', label: '예약 트리거', icon: <Clock className="w-4 h-4" />, category: '트리거' },
  { type: 'trigger', label: '웹훅 트리거', icon: <MessageSquare className="w-4 h-4" />, category: '트리거' },
  { type: 'trigger', label: '이벤트 트리거', icon: <Settings className="w-4 h-4" />, category: '트리거' },

  // 생성기
  { type: 'imageGen', label: '텍스트 생성', icon: <Edit3 className="w-4 h-4" />, category: '생성기' },
  { type: 'imageGen', label: '이미지 생성', icon: <Image className="w-4 h-4" />, category: '생성기' },
  { type: 'imageGen', label: '이미지 변환', icon: <Image className="w-4 h-4" />, category: '생성기' },
  { type: 'imageGen', label: '텍스트 → 비디오', icon: <FileOutput className="w-4 h-4" />, category: '생성기' },
  { type: 'imageGen', label: '이미지 → 비디오', icon: <FileOutput className="w-4 h-4" />, category: '생성기' },
  { type: 'imageGen', label: '텍스트 → 음성', icon: <MessageSquare className="w-4 h-4" />, category: '생성기' },
  { type: 'imageGen', label: '음성 → 텍스트', icon: <MessageSquare className="w-4 h-4" />, category: '생성기' },

  // 분석기
  { type: 'split', label: '분할', icon: <Scissors className="w-4 h-4" />, category: '분석기' },
  { type: 'split', label: '검색', icon: <Search className="w-4 h-4" />, category: '분석기' },

  // 유틸리티
  { type: 'split', label: '변환', icon: <Wrench className="w-4 h-4" />, category: '유틸리티' },

  // 출력
  { type: 'split', label: '저장', icon: <Download className="w-4 h-4" />, category: '출력' },
];

// 카테고리별 그룹핑
const categories = ['트리거', '생성기', '분석기', '편집기', '유틸리티', '출력'];

function NodePalette() {
  const onDragStart = (event: DragEvent<HTMLDivElement>, nodeType: string, label: string) => {
    event.dataTransfer.setData('application/reactflow/type', nodeType);
    event.dataTransfer.setData('application/reactflow/label', label);
    event.dataTransfer.effectAllowed = 'move';
  };

  const getNodesByCategory = (category: string) => {
    return nodeTypesList.filter((node) => node.category === category);
  };

  const getCategoryCount = (category: string) => {
    return nodeTypesList.filter((node) => node.category === category).length;
  };

  return (
    <aside className="w-52 bg-gray-900 border-r border-gray-800 overflow-y-auto">
      {/* 검색창 */}
      <div className="p-3 border-b border-gray-800">
        <div className="relative">
          <Search className="absolute left-2 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="노드 검색..."
            className="w-full pl-8 pr-3 py-1.5 text-xs bg-gray-800 border border-gray-700 rounded text-gray-300 placeholder-gray-500 focus:outline-none focus:border-purple-500"
          />
        </div>
      </div>

      {/* 노드 유형 */}
      <div className="p-2">
        <div className="text-xs text-gray-500 px-2 py-1">노드 유형</div>

        {categories.map((category) => {
          const nodes = getNodesByCategory(category);
          const count = getCategoryCount(category);

          return (
            <div key={category} className="mb-1">
              {/* 카테고리 헤더 */}
              <div className="flex items-center justify-between px-2 py-1.5 text-xs text-gray-400 hover:bg-gray-800 rounded cursor-pointer">
                <div className="flex items-center gap-2">
                  {category === '트리거' && <Zap className="w-3.5 h-3.5 text-yellow-500" />}
                  {category === '생성기' && <Image className="w-3.5 h-3.5 text-purple-500" />}
                  {category === '분석기' && <Search className="w-3.5 h-3.5 text-blue-500" />}
                  {category === '편집기' && <Edit3 className="w-3.5 h-3.5 text-green-500" />}
                  {category === '유틸리티' && <Wrench className="w-3.5 h-3.5 text-orange-500" />}
                  {category === '출력' && <Download className="w-3.5 h-3.5 text-cyan-500" />}
                  <span>{category}</span>
                </div>
                <span className="text-gray-600">{count || ''}</span>
              </div>

              {/* 노드 목록 */}
              <div className="ml-4 space-y-0.5">
                {nodes.map((node, index) => (
                  <div
                    key={`${node.type}-${index}`}
                    draggable
                    onDragStart={(e) => onDragStart(e, node.type, node.label)}
                    className="flex items-center gap-2 px-2 py-1.5 text-xs text-gray-300 hover:bg-purple-900/30 hover:text-white rounded cursor-grab active:cursor-grabbing transition-colors"
                  >
                    <span className="text-gray-500">{node.icon}</span>
                    <span>{node.label}</span>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </aside>
  );
}

export default NodePalette;

