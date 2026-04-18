import { useSSEWithRecovery } from '../../hooks/ch04/useSSEWithRecovery';

export function ReconnectionDemo() {
  const {
    events,
    isConnected,
    reconnectCount,
    lastEventId,
    error,
    connect,
    disconnect,
    clearEvents,
  } = useSSEWithRecovery('/events/reconnect');

  return (
    <div>
      {/* 상태 표시 */}
      <div style={{
        display: 'flex', gap: '16px', alignItems: 'center', marginBottom: '16px',
        padding: '16px', background: isConnected ? '#e8f5e9' : '#ffebee', borderRadius: '8px',
      }}>
        <span style={{
          width: '12px', height: '12px', borderRadius: '50%',
          background: isConnected ? '#4CAF50' : '#f44336', display: 'inline-block',
        }} />
        <strong>{isConnected ? '연결됨' : '연결 안됨'}</strong>
        <span style={{ color: '#666' }}>재연결 횟수: {reconnectCount}</span>
        <span style={{ color: '#666' }}>Last-Event-ID: {lastEventId ?? 'none'}</span>
      </div>

      {error && (
        <div style={{ padding: '12px', background: '#fff3e0', borderLeft: '4px solid #ff9800', borderRadius: '4px', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      {/* 제어 버튼 */}
      <div style={{ marginBottom: '16px', display: 'flex', gap: '8px' }}>
        <button
          onClick={connect}
          disabled={isConnected}
          style={{ padding: '8px 16px', background: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          연결
        </button>
        <button
          onClick={disconnect}
          disabled={!isConnected}
          style={{ padding: '8px 16px', background: '#f44336', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          연결 해제
        </button>
        <button
          onClick={clearEvents}
          style={{ padding: '8px 16px', background: '#9e9e9e', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          이벤트 초기화
        </button>
      </div>

      {/* 학습 포인트 */}
      <div style={{ padding: '16px', background: '#e8f5e9', borderRadius: '8px', marginBottom: '16px', borderLeft: '4px solid #4CAF50' }}>
        <strong>학습 포인트:</strong>
        <ol style={{ margin: '8px 0 0 0', paddingLeft: '20px', lineHeight: 1.8 }}>
          <li>EventSourcePolyfill 설정 (headers, heartbeatTimeout, Last-Event-ID)</li>
          <li>Last-Event-ID ref 관리</li>
          <li>onopen에서 reconnectCount 리셋</li>
          <li>커스텀 이벤트 리스너에서 lastEventId 갱신</li>
          <li>onerror에서 수동 재연결 (maxRetries, exponential backoff)</li>
          <li>cleanup 함수 (disconnect + clearTimeout)</li>
        </ol>
      </div>

      {/* 이벤트 로그 */}
      <div style={{ background: '#1e1e1e', borderRadius: '8px', padding: '16px', maxHeight: '300px', overflowY: 'auto' }}>
        <h3 style={{ color: '#4fc3f7', margin: '0 0 12px 0', fontSize: '14px' }}>
          수신 이벤트 ({events.length})
        </h3>
        {events.length === 0 ? (
          <div style={{ color: '#666', fontFamily: 'monospace' }}>대기 중...</div>
        ) : (
          events.map((event, idx) => (
            <div key={idx} style={{ color: '#81c784', fontFamily: 'monospace', fontSize: '12px', padding: '4px 0' }}>
              [{event.timestamp}] id={event.id} seq={event.sequence}: {event.data}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
