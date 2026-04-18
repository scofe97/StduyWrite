import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

// 02-react-use-websocket
import { BasicConnection, MessageHistory, WithCallbacks } from './ch02/basic-usage';
import { NullUrlPattern, LoginBasedConnection, DynamicUrlPattern } from './ch02/conditional-connect';

// 03-connection-state
import { ConnectionStateDemo, StateChangeActions, StaleDataIndicator } from './ch03/connection-status';

// 04-reconnection
import { BasicReconnect, CloseCodeBasedReconnect, ManualReconnect } from './ch04/basic-reconnect';
import { ExponentialBackoff, BackoffVisualization } from './ch04/exponential-backoff';

// 05-message-types
import { SnapshotDeltaDemo, VersionedSnapshotDelta, OptimisticUpdate } from './ch05/snapshot-delta';
import { BulkUserRegistrationDemo } from './ch05/bulk-user-registration';

// 섹션별 탭 구성
const sections = [
  {
    title: '02-react-use-websocket',
    tabs: [
      { id: 'basic', label: '기본 연결', component: BasicConnection },
      { id: 'history', label: '메시지 히스토리', component: MessageHistory },
      { id: 'callbacks', label: '콜백 로그', component: WithCallbacks },
      { id: 'null-url', label: 'Null URL 패턴', component: NullUrlPattern },
      { id: 'login', label: '로그인 기반', component: LoginBasedConnection },
      { id: 'dynamic', label: '동적 URL', component: DynamicUrlPattern },
    ],
  },
  {
    title: '03-connection-state',
    tabs: [
      { id: 'conn-state', label: '연결 상태 관리', component: ConnectionStateDemo },
      { id: 'state-history', label: '상태 히스토리', component: StateChangeActions },
      { id: 'stale-data', label: '오래된 데이터', component: StaleDataIndicator },
    ],
  },
  {
    title: '04-reconnection',
    tabs: [
      { id: 'basic-reconnect', label: '기본 재연결', component: BasicReconnect },
      { id: 'closecode-reconnect', label: 'Close Code 기반', component: CloseCodeBasedReconnect },
      { id: 'manual-reconnect', label: '수동 재연결', component: ManualReconnect },
      { id: 'exp-backoff', label: '지수 백오프', component: ExponentialBackoff },
      { id: 'backoff-viz', label: '백오프 시각화', component: BackoffVisualization },
    ],
  },
  {
    title: '05-message-types',
    tabs: [
      { id: 'snapshot-delta', label: 'SNAPSHOT/DELTA', component: SnapshotDeltaDemo },
      { id: 'versioned', label: '버전 기반 동기화', component: VersionedSnapshotDelta },
      { id: 'optimistic', label: '낙관적 업데이트', component: OptimisticUpdate },
      { id: 'bulk-registration', label: '다중 유저 등록', component: BulkUserRegistrationDemo },
    ],
  },
];

// 모든 탭 평탄화 (컴포넌트 찾기용)
const allTabs = sections.flatMap(s => s.tabs);

function App() {
  const [activeTab, setActiveTab] = useState('basic');
  const ActiveComponent = allTabs.find(t => t.id === activeTab)?.component || BasicConnection;

  return (
    <div style={{ fontFamily: 'monospace', padding: '20px', background: '#1e1e1e', color: '#fff', minHeight: '100vh' }}>
      <h1 style={{ color: '#4fc3f7' }}>WebSocket 실습 (React)</h1>

      {/* 섹션별 탭 버튼 */}
      {sections.map(section => (
        <div key={section.title} style={{ marginBottom: '16px' }}>
          <div style={{ color: '#4fc3f7', fontSize: '16px', fontWeight: 'bold', marginBottom: '10px' }}>
            {section.title}
          </div>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {section.tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  padding: '8px 16px',
                  background: activeTab === tab.id ? '#4fc3f7' : '#333',
                  color: activeTab === tab.id ? '#000' : '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      ))}

      {/* 컴포넌트 렌더링 */}
      <div style={{ background: '#2d2d2d', padding: '20px', borderRadius: '8px', marginTop: '20px' }}>
        <ActiveComponent />
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
