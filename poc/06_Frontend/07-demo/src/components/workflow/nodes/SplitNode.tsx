import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Scissors } from 'lucide-react';

interface SplitNodeData {
  label: string;
}

function SplitNode({ data, selected }: NodeProps<SplitNodeData>) {
  return (
    <div
      className={`
        min-w-[180px] rounded-lg border-2 overflow-hidden
        ${selected ? 'border-purple-500 shadow-lg shadow-purple-500/20' : 'border-gray-700'}
        bg-gradient-to-b from-gray-800/90 to-gray-900/95
      `}
    >
      {/* 입력 핸들 */}
      <Handle
        type="target"
        position={Position.Left}
        id="input"
        className="!w-3 !h-3 !bg-purple-500 !border-2 !border-purple-300"
        style={{ left: -6 }}
      />

      {/* 헤더 */}
      <div className="flex items-center gap-2 px-3 py-2 bg-gray-700/50 border-b border-gray-600">
        <Scissors className="w-4 h-4 text-gray-300" />
        <span className="text-sm font-medium text-white">{data.label}</span>
      </div>

      {/* 본문 */}
      <div className="p-3 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-purple-400">○</span>
          <span className="text-xs text-gray-300">
            Input <span className="text-emerald-400">*</span>
          </span>
        </div>
      </div>

      {/* 출력 라벨 */}
      <div className="px-3 py-2 border-t border-gray-700 text-right">
        <span className="text-xs text-gray-400">Parts</span>
        <span className="ml-2 text-purple-400">○</span>
      </div>

      {/* 출력 핸들 */}
      <Handle
        type="source"
        position={Position.Right}
        id="parts"
        className="!w-3 !h-3 !bg-purple-500 !border-2 !border-purple-300"
        style={{ right: -6 }}
      />
    </div>
  );
}

export default memo(SplitNode);

