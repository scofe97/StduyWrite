import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Clock } from 'lucide-react';

interface TriggerNodeData {
  label: string;
  inputType?: string;
  inputValue?: string;
}

function TriggerNode({ data, selected }: NodeProps<TriggerNodeData>) {
  return (
    <div
      className={`
        min-w-[200px] rounded-lg border-2 overflow-hidden
        ${selected ? 'border-purple-500 shadow-lg shadow-purple-500/20' : 'border-gray-700'}
        bg-gradient-to-b from-emerald-900/80 to-emerald-950/90
      `}
    >
      {/* 헤더 */}
      <div className="flex items-center gap-2 px-3 py-2 bg-emerald-800/50 border-b border-gray-700">
        <Clock className="w-4 h-4 text-emerald-400" />
        <span className="text-sm font-medium text-white">{data.label}</span>
      </div>

      {/* 본문 */}
      <div className="p-3 space-y-2">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
          <span className="text-xs text-gray-300">
            Input: <span className="text-white">{data.inputType || 'Text'}</span>
          </span>
        </div>
        {data.inputValue && (
          <div className="text-xs text-gray-400 pl-4">{data.inputValue}</div>
        )}
      </div>

      {/* 출력 라벨 */}
      <div className="px-3 py-2 border-t border-gray-700 text-right">
        <span className="text-xs text-gray-400">Output</span>
        <span className="ml-2 text-purple-400">○</span>
      </div>

      {/* 출력 핸들 */}
      <Handle
        type="source"
        position={Position.Right}
        id="output"
        className="!w-3 !h-3 !bg-purple-500 !border-2 !border-purple-300"
        style={{ right: -6 }}
      />
    </div>
  );
}

export default memo(TriggerNode);

