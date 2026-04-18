import { useState, useCallback, useRef, useEffect } from 'react';
import { EventSourcePolyfill } from 'event-source-polyfill';
import { useEventSource, ReadyState } from '../../hooks/ch02/useEventSource';
import type { ReadyStateType } from '../../hooks/ch02/useEventSource';

// ============================================
// 타입 정의
// ============================================

interface BasicMessage {
  count: number;
  time: string;
  type: string;
}

interface LogEntry {
  id: number;
  time: string;
  type: 'info' | 'message' | 'open' | 'error' | 'custom';
  eventType?: string;
  content: string;
}

// ============================================
// 스타일
// ============================================

const styles = {
  card: {
    background: 'white',
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '20px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  cardTitle: {
    color: '#444',
    marginBottom: '15px',
    paddingBottom: '10px',
    borderBottom: '1px solid #eee',
    fontSize: '18px',
  },
  button: {
    padding: '10px 20px',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '14px',
    marginRight: '10px',
    marginBottom: '10px',
  },
  primaryButton: { background: '#4CAF50', color: 'white' },
  dangerButton: { background: '#f44336', color: 'white' },
  secondaryButton: { background: '#2196F3', color: 'white' },
  stateDisplay: {
    fontSize: '24px',
    fontWeight: 'bold' as const,
    padding: '20px',
    textAlign: 'center' as const,
    borderRadius: '5px',
    margin: '15px 0',
  },
  logContainer: {
    background: '#1e1e1e',
    borderRadius: '5px',
    padding: '15px',
    maxHeight: '200px',
    overflowY: 'auto' as const,
    fontFamily: 'Consolas, monospace',
    fontSize: '12px',
  },
  codeBlock: {
    background: '#263238',
    color: '#eeffff',
    padding: '15px',
    borderRadius: '5px',
    fontSize: '12px',
    overflow: 'auto' as const,
    margin: '10px 0',
  },
  tipBox: {
    background: '#fff8e1',
    borderLeft: '4px solid #ffc107',
    padding: '15px',
    margin: '15px 0',
    borderRadius: '0 5px 5px 0',
  },
  input: {
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '5px',
    fontSize: '14px',
    width: '100%',
    marginBottom: '10px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
  },
};

const stateColors: Record<number, { bg: string; color: string }> = {
  0: { bg: '#fff3e0', color: '#ef6c00' },
  1: { bg: '#e8f5e9', color: '#2e7d32' },
  2: { bg: '#ffebee', color: '#c62828' },
};

const stateLabels: Record<number, string> = {
  0: 'CONNECTING (0)',
  1: 'OPEN (1)',
  2: 'CLOSED (2)',
};

// ============================================
// 1. 기본 EventSource 데모
// ============================================

function BasicDemo() {
  const { data, readyState, isConnected, close, connect } = useEventSource<BasicMessage>(
    '/events/basic',
    { autoConnect: false }
  );

  return (
    <div style={styles.card}>
      <h2 style={styles.cardTitle}>1. readyState 모니터링 (useEventSource 훅)</h2>
      <div>
        <button
          style={{ ...styles.button, ...styles.primaryButton }}
          onClick={connect}
          disabled={isConnected}
        >
          연결
        </button>
        <button
          style={{ ...styles.button, ...styles.dangerButton }}
          onClick={close}
          disabled={!isConnected}
        >
          종료
        </button>
      </div>
      <div
        style={{
          ...styles.stateDisplay,
          background: stateColors[readyState].bg,
          color: stateColors[readyState].color,
        }}
      >
        {stateLabels[readyState]}
      </div>
      {data && (
        <div style={{ padding: '10px', background: '#f5f5f5', borderRadius: '5px' }}>
          <strong>마지막 수신 데이터:</strong>
          <pre style={{ margin: '5px 0 0 0' }}>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
      <pre style={styles.codeBlock}>
{`// useEventSource 훅 사용법
const { data, isConnected, close, connect } = useEventSource<MyType>('/events/basic');`}
      </pre>
    </div>
  );
}

// ============================================
// 2. 커스텀 헤더 테스트
// ============================================

function AuthHeaderDemo() {
  const [token, setToken] = useState('my-jwt-token-123');
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [readyState, setReadyState] = useState<ReadyStateType>(ReadyState.CLOSED);
  const logIdRef = useRef(0);
  const esRef = useRef<EventSourcePolyfill | null>(null);

  const addLog = useCallback((type: LogEntry['type'], content: string) => {
    const entry: LogEntry = {
      id: ++logIdRef.current,
      time: new Date().toLocaleTimeString(),
      type,
      content,
    };
    setLogs((prev) => [...prev.slice(-50), entry]);
  }, []);

  const connect = useCallback(() => {
    if (esRef.current) esRef.current.close();
    setLogs([]);
    addLog('info', `토큰: ${token}`);

    const es = new EventSourcePolyfill('/events/auth', {
      headers: {
        Authorization: `Bearer ${token}`,
        'X-Custom-Header': 'custom-value',
      },
      heartbeatTimeout: 45000,
    });

    esRef.current = es;
    setReadyState(ReadyState.CONNECTING);

    es.onopen = () => {
      setReadyState(ReadyState.OPEN);
      addLog('open', '연결 성공! (헤더가 서버로 전송됨)');
    };
    es.onmessage = (event: any) => {
      addLog('message', event.data.substring(0, 50));
    };
    es.onerror = () => {
      setReadyState(es.readyState as ReadyStateType);
      addLog('error', `에러! readyState: ${es.readyState}`);
    };
  }, [token, addLog]);

  const disconnect = useCallback(() => {
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
      setReadyState(ReadyState.CLOSED);
      addLog('info', '연결 종료');
    }
  }, [addLog]);

  useEffect(() => {
    return () => { esRef.current?.close(); };
  }, []);

  const getLogColor = (type: LogEntry['type']) => {
    switch (type) {
      case 'open': return '#81c784';
      case 'message': return '#4fc3f7';
      case 'error': return '#ef5350';
      default: return '#ccc';
    }
  };

  return (
    <div style={{ ...styles.card, border: '2px solid #2196F3' }}>
      <h2 style={{ ...styles.cardTitle, color: '#1565c0' }}>
        2. 커스텀 헤더 (event-source-polyfill)
      </h2>
      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>JWT 토큰:</label>
        <input
          type="text"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          style={styles.input}
          placeholder="JWT 토큰 입력"
        />
      </div>
      <div>
        <button style={{ ...styles.button, ...styles.secondaryButton }} onClick={connect}>
          커스텀 헤더로 연결
        </button>
        <button style={{ ...styles.button, ...styles.dangerButton }} onClick={disconnect}>
          종료
        </button>
      </div>
      <div
        style={{
          ...styles.stateDisplay,
          background: stateColors[readyState].bg,
          color: stateColors[readyState].color,
          fontSize: '18px',
          padding: '10px',
        }}
      >
        {stateLabels[readyState]}
      </div>
      <div style={styles.logContainer}>
        {logs.length === 0 ? (
          <div style={{ color: '#ccc' }}>로그가 여기에 표시됩니다.</div>
        ) : (
          logs.map((log) => (
            <div key={log.id} style={{ color: getLogColor(log.type), padding: '3px 0' }}>
              [{log.time}] {log.type.toUpperCase()}: {log.content}
            </div>
          ))
        )}
      </div>
      <div style={styles.tipBox}>
        <strong>기본 EventSource vs event-source-polyfill:</strong><br />
        EventSourcePolyfill은 Authorization 헤더와 heartbeatTimeout을 지원합니다.
      </div>
    </div>
  );
}

// ============================================
// 3. 핵심 실습: event: 필드와 이벤트 라우팅
// ============================================

function MultiTypeDemo() {
  const [onmessageLogs, setOnmessageLogs] = useState<LogEntry[]>([]);
  const [customEventLogs, setCustomEventLogs] = useState<LogEntry[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const logIdRef = useRef(0);
  const esRef = useRef<EventSourcePolyfill | null>(null);

  const addOnmessageLog = useCallback((content: string) => {
    setOnmessageLogs((prev) => [...prev.slice(-20), {
      id: ++logIdRef.current, time: new Date().toLocaleTimeString(), type: 'message' as const, content,
    }]);
  }, []);

  const addCustomEventLog = useCallback((eventType: string, content: string) => {
    setCustomEventLogs((prev) => [...prev.slice(-20), {
      id: ++logIdRef.current, time: new Date().toLocaleTimeString(), type: 'custom' as const, eventType, content,
    }]);
  }, []);

  const handleConnect = useCallback(() => {
    if (esRef.current) esRef.current.close();
    setOnmessageLogs([]);
    setCustomEventLogs([]);

    const es = new EventSourcePolyfill('/events/multi', { heartbeatTimeout: 45000 });
    esRef.current = es;

    es.onopen = () => { setIsConnected(true); };
    es.onmessage = (event: any) => {
      try {
        const data = JSON.parse(event.data);
        addOnmessageLog(`msg: "${data.msg}" (${data.time})`);
      } catch { addOnmessageLog(event.data); }
    };

    es.addEventListener('notification', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        addCustomEventLog('notification', `${data.title} - ${data.body}`);
      } catch { addCustomEventLog('notification', event.data); }
    });

    es.addEventListener('heartbeat', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        addCustomEventLog('heartbeat', `status: ${data.status}`);
      } catch { addCustomEventLog('heartbeat', event.data); }
    });

    es.addEventListener('user-action', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        addCustomEventLog('user-action', `${data.action} by ${data.userId}`);
      } catch { addCustomEventLog('user-action', event.data); }
    });

    es.onerror = () => {
      if (es.readyState === ReadyState.CONNECTING) {
        addOnmessageLog('재연결 시도 중...');
      } else { setIsConnected(false); }
    };
  }, [addOnmessageLog, addCustomEventLog]);

  const handleDisconnect = useCallback(() => {
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
      setIsConnected(false);
    }
  }, []);

  useEffect(() => {
    return () => { esRef.current?.close(); };
  }, []);

  const getEventColor = (eventType?: string) => {
    switch (eventType) {
      case 'notification': return '#ffb74d';
      case 'heartbeat': return '#81c784';
      case 'user-action': return '#4fc3f7';
      default: return '#ccc';
    }
  };

  return (
    <div style={{ ...styles.card, border: '2px solid #4CAF50' }}>
      <h2 style={{ ...styles.cardTitle, color: '#2e7d32' }}>3. event: 필드와 이벤트 라우팅</h2>
      <div>
        <button style={{ ...styles.button, ...styles.primaryButton }} onClick={handleConnect} disabled={isConnected}>
          연결 (다양한 이벤트)
        </button>
        <button style={{ ...styles.button, ...styles.dangerButton }} onClick={handleDisconnect} disabled={!isConnected}>
          종료
        </button>
        <span style={{ marginLeft: '10px', color: isConnected ? '#2e7d32' : '#c62828' }}>
          {isConnected ? '● 연결됨' : '○ 연결 안됨'}
        </span>
      </div>
      <div style={{ ...styles.grid, marginTop: '15px' }}>
        <div style={{ background: '#e3f2fd', padding: '15px', borderRadius: '5px' }}>
          <h3 style={{ color: '#1565c0', marginBottom: '10px' }}>onmessage (기본 메시지)</h3>
          <div style={{ ...styles.logContainer, background: '#0d47a1' }}>
            {onmessageLogs.length === 0 ? (
              <div style={{ color: '#ccc' }}>대기 중...</div>
            ) : (
              onmessageLogs.map((log) => (
                <div key={log.id} style={{ color: '#4fc3f7', padding: '3px 0' }}>
                  [{log.time}] {log.content}
                </div>
              ))
            )}
          </div>
        </div>
        <div style={{ background: '#fff3e0', padding: '15px', borderRadius: '5px' }}>
          <h3 style={{ color: '#e65100', marginBottom: '10px' }}>addEventListener (커스텀)</h3>
          <div style={{ ...styles.logContainer, background: '#e65100' }}>
            {customEventLogs.length === 0 ? (
              <div style={{ color: '#ccc' }}>대기 중...</div>
            ) : (
              customEventLogs.map((log) => (
                <div key={log.id} style={{ color: getEventColor(log.eventType), padding: '3px 0' }}>
                  [{log.time}] [{log.eventType}] {log.content}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
      <div style={{ ...styles.tipBox, marginTop: '15px' }}>
        <strong>관찰 포인트:</strong><br />
        1. 기본 메시지는 왼쪽(onmessage)에만 표시<br />
        2. notification, heartbeat, user-action은 오른쪽(addEventListener)에만 표시
      </div>
    </div>
  );
}

// ============================================
// 메인 컴포넌트
// ============================================

export function EventSourceDemo() {
  return (
    <div>
      <BasicDemo />
      <AuthHeaderDemo />
      <MultiTypeDemo />
    </div>
  );
}
