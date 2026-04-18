import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Image } from 'lucide-react';

interface ImageGenNodeData {
  label: string;
}

function ImageGenNode({ data, selected }: NodeProps<ImageGenNodeData>) {
  return (
    <div
      className={`
        min-w-[220px] rounded-lg border-2 overflow-hidden
        ${selected ? 'border-purple-500 shadow-lg shadow-purple-500/20' : 'border-gray-700'}
        bg-gradient-to-b from-purple-900/80 to-purple-950/90
      `}
    >
      {/* 헤더 */}
      <div className="flex items-center gap-2 px-3 py-2 bg-purple-800/50 border-b border-gray-700">
        <Image className="w-4 h-4 text-yellow-400" />
        <span className="text-sm font-medium text-yellow-400">{data.label}</span>
      </div>

      {/* 입력 포트들 */}
      <div className="p-3 space-y-3">
        {/* Prompt */}
        <div className="flex items-center gap-2 relative">
          <Handle
            type="target"
            position={Position.Left}
            id="prompt"
            className="!w-3 !h-3 !bg-purple-500 !border-2 !border-purple-300"
            style={{ left: -18, top: '50%' }}
          />
          <span className="text-purple-400">○</span>
          <span className="text-xs text-white">
            Prompt <span className="text-emerald-400">*</span>
          </span>
        </div>

        {/* Negative Prompt */}
        <div className="flex items-center gap-2 relative">
          <Handle
            type="target"
            position={Position.Left}
            id="negative"
            className="!w-3 !h-3 !bg-gray-500 !border-2 !border-gray-400"
            style={{ left: -18, top: '50%' }}
          />
          <span className="text-gray-500">○</span>
          <span className="text-xs text-gray-400">Negative Prompt</span>
        </div>

        {/* Reference Image */}
        <div className="flex items-center gap-2 relative">
          <Handle
            type="target"
            position={Position.Left}
            id="reference"
            className="!w-3 !h-3 !bg-gray-500 !border-2 !border-gray-400"
            style={{ left: -18, top: '50%' }}
          />
          <span className="text-gray-500">○</span>
          <span className="text-xs text-gray-400">Reference Image</span>
        </div>
      </div>

      {/* 출력 */}
      <div className="px-3 py-2 border-t border-gray-700 flex justify-end items-center">
        <span className="text-xs text-gray-300">Generated Image</span>
        <Handle
          type="source"
          position={Position.Right}
          id="output"
          className="!w-3 !h-3 !bg-purple-500 !border-2 !border-purple-300"
          style={{ right: -18 }}
        />
      </div>
    </div>
  );
}

export default memo(ImageGenNode);

