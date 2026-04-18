import { useSSEWithCleanup } from '../../hooks/ch06/useSSEWithCleanup';

export function ReactIntegrationDemo() {
  const {
    messages,
    isConnected,
    mountCount,
    error,
    connect,
    disconnect,
    clearMessages,
  } = useSSEWithCleanup('/events/cleanup-test');

  return (
    <div>
      {/* Strict Mode 관찰 */}
      <div style={{
        padding: '16px', borderRadius: '8px', marginBottom: '16px',
        background: '#e8eaf6', border: '2px solid #5c6bc0',
      }}>
        <strong>React 18 Strict Mode 관찰:</strong>
        <div style={{ marginTop: '8px', display: 'flex', gap: '24px' }}>
          <div>
            <span style={{ color: '#666' }}>마운트 횟수: </span>
            <strong style={{ color: '#5c6bc0', fontSize: '20px' }}>{mountCount}</strong>
          </div>
          <div>
            <span style={{ color: '#666' }}>연결 상태: </span>
            <strong style={{ color: isConnected ? '#2e7d32' : '#c62828' }}>
              {isConnected ? '연결됨' : '연결 안됨'}
            </strong>
          </div>
        </div>
        <p style={{ fontSize: '12px', color: '#666', marginTop: '8px' }}>
          개발 모드에서 Strict Mode가 활성화되어 있으면 마운트 횟수가 2로 시작합니다.
          이는 mount → unmount → remount 시뮬레이션 때문입니다.
        </p>
      </div>

      {error && (
        <div style={{ padding: '12px', background: '#ffebee', borderLeft: '4px solid #f44336', borderRadius: '4px', marginBottom: '16px' }}>
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
          <li>useRef + AbortController로 연결 관리</li>
          <li>React 18 Strict Mode 대응 (mount/unmount/remount)</li>
          <li>useEffect cleanup에서 AbortController.abort() + EventSource.close()</li>
          <li>useCallback으로 연결/해제 함수 메모이제이션</li>
          <li>isMountedRef로 언마운트 후 상태 업데이트 방지</li>
          <li>의존성 배열 최적화 (불필요한 재연결 방지)</li>
        </ol>
      </div>

      {/* 관찰 포인트 */}
      <div style={{ padding: '16px', background: '#e8f5e9', borderRadius: '8px', marginBottom: '16px', borderLeft: '4px solid #4CAF50' }}>
        <strong>관찰 포인트:</strong>
        <ul style={{ margin: '8px 0 0 0', paddingLeft: '20px', lineHeight: 1.8 }}>
          <li>Strict Mode에서 마운트 횟수가 2인지 확인</li>
          <li>연결 → 다른 페이지 이동 → 돌아왔을 때 좀비 연결이 없는지 확인</li>
          <li>브라우저 DevTools Network 탭에서 EventSource 연결 확인</li>
          <li>콘솔에서 "Can't perform a React state update on an unmounted component" 경고가 없는지 확인</li>
        </ul>
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
