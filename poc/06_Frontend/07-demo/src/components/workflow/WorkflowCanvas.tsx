import { useCallback, useRef, DragEvent } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
  Connection,
  addEdge,
  useNodesState,
  useEdgesState,
  BackgroundVariant,
  ReactFlowProvider,
  useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { nodeTypes } from './nodes';
import NodePalette from './NodePalette';

// 초기 노드 (이미지와 유사한 구조)
const initialNodes: Node[] = [
  {
    id: 'trigger-1',
    type: 'trigger',
    position: { x: 100, y: 200 },
    data: {
      label: '예약 트리거',
      inputType: 'Text',
      inputValue: '신발이 치즈',
    },
  },
  {
    id: 'split-1',
    type: 'split',
    position: { x: 400, y: 200 },
    data: {
      label: '분할',
    },
  },
  {
    id: 'imagegen-1',
    type: 'imageGen',
    position: { x: 700, y: 100 },
    data: {
      label: '이미지 생성',
    },
  },
  {
    id: 'imagegen-2',
    type: 'imageGen',
    position: { x: 700, y: 350 },
    data: {
      label: '이미지 생성',
    },
  },
];

// 초기 엣지
const initialEdges: Edge[] = [
  {
    id: 'e-trigger-split',
    source: 'trigger-1',
    target: 'split-1',
    sourceHandle: 'output',
    targetHandle: 'input',
    animated: true,
    style: { stroke: '#a855f7', strokeWidth: 2, strokeDasharray: '5,5' },
  },
  {
    id: 'e-split-img1',
    source: 'split-1',
    target: 'imagegen-1',
    sourceHandle: 'parts',
    targetHandle: 'prompt',
    animated: true,
    style: { stroke: '#a855f7', strokeWidth: 2, strokeDasharray: '5,5' },
  },
  {
    id: 'e-split-img2',
    source: 'split-1',
    target: 'imagegen-2',
    sourceHandle: 'parts',
    targetHandle: 'prompt',
    animated: true,
    style: { stroke: '#a855f7', strokeWidth: 2, strokeDasharray: '5,5' },
  },
];

let nodeId = 10;

function Flow() {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const { screenToFlowPosition } = useReactFlow();
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // 새로운 연결
  const onConnect = useCallback(
    (connection: Connection) => {
      setEdges((eds) =>
        addEdge(
          {
            ...connection,
            animated: true,
            style: { stroke: '#a855f7', strokeWidth: 2, strokeDasharray: '5,5' },
          },
          eds
        )
      );
    },
    [setEdges]
  );

  // 드래그 오버
  const onDragOver = useCallback((event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  // 드롭 처리
  const onDrop = useCallback(
    (event: DragEvent<HTMLDivElement>) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow/type');
      const label = event.dataTransfer.getData('application/reactflow/label');

      if (!type) return;

      const position = screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode: Node = {
        id: `${type}-${nodeId++}`,
        type,
        position,
        data: {
          label: label || `${type} 노드`,
          inputType: type === 'trigger' ? 'Text' : undefined,
        },
      };

      setNodes((nds) => [...nds, newNode]);
    },
    [screenToFlowPosition, setNodes]
  );

  return (
    <div className="flex h-full bg-gray-950">
      {/* 사이드바 */}
      <NodePalette />

      {/* 캔버스 */}
      <div ref={reactFlowWrapper} className="flex-1 relative">
        {/* 상단 헤더 */}
        <div className="absolute top-0 left-0 right-0 z-10 flex items-center gap-2 px-4 py-2 bg-gray-900/80 backdrop-blur border-b border-gray-800">
          <div className="flex items-center gap-2">
            <span className="text-purple-400">⚙</span>
            <span className="text-sm text-white font-medium">Image to Video Pipeline</span>
          </div>
          <span className="text-xs text-yellow-500">저장 안됨</span>
        </div>

        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onDragOver={onDragOver}
          onDrop={onDrop}
          nodeTypes={nodeTypes}
          fitView
          className="bg-gray-950"
          defaultEdgeOptions={{
            animated: true,
            style: { stroke: '#a855f7', strokeWidth: 2, strokeDasharray: '5,5' },
          }}
        >
          {/* 배경 그리드 */}
          <Background
            variant={BackgroundVariant.Dots}
            gap={20}
            size={1}
            color="#374151"
          />

          {/* 줌/이동 컨트롤 */}
          <Controls
            className="!bg-gray-800 !border-gray-700 !rounded-lg"
            showInteractive={false}
          />

          {/* 미니맵 */}
          <MiniMap
            nodeStrokeColor="#a855f7"
            nodeColor="#1f2937"
            nodeBorderRadius={8}
            maskColor="rgba(0, 0, 0, 0.8)"
            className="!bg-gray-900 !border-gray-700"
          />
        </ReactFlow>
      </div>
    </div>
  );
}

// ReactFlowProvider로 감싸기
export default function WorkflowCanvas() {
  return (
    <ReactFlowProvider>
      <Flow />
    </ReactFlowProvider>
  );
}

