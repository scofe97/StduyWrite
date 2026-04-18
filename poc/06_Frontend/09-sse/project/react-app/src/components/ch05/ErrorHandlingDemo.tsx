import { useSSEWithErrorHandling } from '../../hooks/ch05/useSSEWithErrorHandling';
import type { SSEConnectionState } from '../../hooks/ch05/useSSEWithErrorHandling';

const stateColors: Record<SSEConnectionState, { bg: string; color: string; label: string }> = {
  connecting: { bg: '#fff3e0', color: '#ef6c00', label: '연결 중...' },
  connected: { bg: '#e8f5e9', color: '#2e7d32', label: '연결됨' },
  error: { bg: '#ffebee', color: '#c62828', label: '에러' },
  disconnected: { bg: '#f5f5f5', color: '#616161', label: '연결 안됨' },
  'fallback-polling': { bg: '#e3f2fd', color: '#1565c0', label: 'Polling 모드' },
};

export function ErrorHandlingDemo() {
  const {
    messages,
    connectionState,
    errorInfo,
    connect,
    disconnect,
    clearMessages,
  } = useSSEWithErrorHandling('/events/unreliable', {
    maxRetries: 3,
    baseRetryInterval: 1000,
    heartbeatTimeout: 15000,
    pollingUrl: '/api/polling',
  });

  const stateInfo = stateColors[connectionState];

  return (
    <div>
      {/* 상태 머신 시각화 */}
      <div style={{
        padding: '20px', borderRadius: '8px', marginBottom: '16px',
        background: stateInfo.bg, textAlign: 'center',
      }}>
        <div style={{ fontSize: '24px', fontWeight: 'bold', color: stateInfo.color }}>
          {stateInfo.label}
        </div>
        <div style={{ fontSize: '12px', color: '#999', marginTop: '4px' }}>
          상태: {connectionState}
        </div>
      </div>

      {/* 에러 정보 */}
      {errorInfo && (
        <div style={{
          padding: '16px', background: '#fff3e0', borderLeft: '4px solid #ff9800',
          borderRadius: '4px', marginBottom: '16px',
        }}>
          <strong>에러 정보:</strong>
          <div style={{ marginTop: '8px', fontSize: '14px' }}>
            <div>타입: <code>{errorInfo.type}</code></div>
            <div>메시지: {errorInfo.message}</div>
            <div>재시도 횟수: {errorInfo.retryCount}</div>
            <div>재시도 가능: {errorInfo.canRetry ? 'Yes' : 'No'}</div>
          </div>
        </div>
      )}

      {/* 제어 버튼 */}
      <div style={{ marginBottom: '16px', display: 'flex', gap: '8px' }}>
        <button
          onClick={connect}
          disabled={connectionState === 'connected' || connectionState === 'connecting'}
          style={{ padding: '8px 16px', background: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          SSE 연결
        </button>
        <button
          onClick={disconnect}
          disabled={connectionState === 'disconnected'}
          style={{ padding: '8px 16px', background: '#f44336', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          연결 해제
        </button>
        <button
          onClick={clearMessages}
          style={{ padding: '8px 16px', background: '#9e9e9e', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          메시지 초기화
        </button>
      </div>

      {/* 학습 포인트 */}
      <div style={{ padding: '16px', background: '#e8f5e9', borderRadius: '8px', marginBottom: '16px', borderLeft: '4px solid #4CAF50' }}>
        <strong>학습 포인트:</strong>
        <ol style={{ margin: '8px 0 0 0', paddingLeft: '20px', lineHeight: 1.8 }}>
          <li>연결 상태 머신 (connecting → connected → error → disconnected)</li>
          <li>재시도 카운터 + 지수 백오프 계산</li>
          <li>onerror 핸들러 (readyState 기반 판단 + 재시도 제한)</li>
          <li>heartbeat 타임아웃 감지 로직</li>
          <li>fallback (SSE 실패 → polling 전환)</li>
          <li>에러 UI 상태 관리 (errorInfo: type, message, retryCount, canRetry)</li>
        </ol>
      </div>

      {/* 상태 머신 다이어그램 */}
      <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px', marginBottom: '16px' }}>
        <strong>상태 전이 다이어그램:</strong>
        <pre style={{ fontSize: '12px', margin: '8px 0 0 0', lineHeight: 1.6 }}>
{`disconnected → connecting → connected
                    ↓            ↓
                  error ←────── error
                    ↓
           fallback-polling`}
        </pre>
      </div>

      {/* 메시지 로그 */}
      <div style={{ background: '#1e1e1e', borderRadius: '8px', padding: '16px', maxHeight: '300px', overflowY: 'auto' }}>
        <h3 style={{ color: '#4fc3f7', margin: '0 0 12px 0', fontSize: '14px' }}>
          수신 메시지 ({messages.length})
        </h3>
        {messages.length === 0 ? (
          <div style={{ color: '#666', fontFamily: 'monospace' }}>대기 중...</div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} style={{ color: '#81c784', fontFamily: 'monospace', fontSize: '12px', padding: '4px 0' }}>
              [{msg.timestamp}] #{msg.id}: {msg.data}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
