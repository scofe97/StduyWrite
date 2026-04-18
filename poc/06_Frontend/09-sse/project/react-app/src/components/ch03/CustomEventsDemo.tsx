import React, { useState } from 'react';
import {
  useCustomEvents,
  useCustomEventsWithAuth,
  NotificationEvent,
  UpdateEvent,
  AlertEvent,
  ConnectionStatus,
} from '../../hooks/ch03/useCustomEvents';

// 상태 배지 컴포넌트
const StatusBadge: React.FC<{ status: ConnectionStatus }> = ({ status }) => {
  const colors: Record<ConnectionStatus, string> = {
    connecting: '#ffc107',
    connected: '#28a745',
    disconnected: '#6c757d',
    error: '#dc3545',
  };
  const labels: Record<ConnectionStatus, string> = {
    connecting: '연결 중...',
    connected: '연결됨',
    disconnected: '연결 끊김',
    error: '오류',
  };

  return (
    <span style={{
      padding: '4px 12px',
      borderRadius: '12px',
      backgroundColor: colors[status],
      color: 'white',
      fontSize: '12px',
      fontWeight: 'bold',
    }}>
      {labels[status]}
    </span>
  );
};

const NotificationCard: React.FC<{ event: NotificationEvent; index: number }> = ({ event, index }) => {
  const colors = { info: '#17a2b8', warning: '#ffc107', error: '#dc3545' };
  return (
    <div style={{
      padding: '12px', marginBottom: '8px',
      borderLeft: `4px solid ${colors[event.type]}`,
      backgroundColor: '#f8f9fa', borderRadius: '4px',
    }}>
      <strong>#{index + 1} [{event.type.toUpperCase()}]</strong> {event.title}
      <p style={{ margin: '4px 0 0 0', color: '#666' }}>{event.message}</p>
    </div>
  );
};

const UpdateCard: React.FC<{ event: UpdateEvent; index: number }> = ({ event, index }) => {
  const actionColors = { created: '#28a745', updated: '#17a2b8', deleted: '#dc3545' };
  return (
    <div style={{
      padding: '12px', marginBottom: '8px',
      borderLeft: `4px solid ${actionColors[event.action]}`,
      backgroundColor: '#f8f9fa', borderRadius: '4px',
    }}>
      <strong>#{index + 1}</strong> {event.resource} -
      <span style={{ color: actionColors[event.action], marginLeft: '4px' }}>{event.action}</span>
      <pre style={{ margin: '4px 0 0 0', fontSize: '12px', overflow: 'auto' }}>
        {JSON.stringify(event.data, null, 2)}
      </pre>
    </div>
  );
};

const AlertCard: React.FC<{ event: AlertEvent; index: number }> = ({ event, index }) => {
  const levelColors = { low: '#6c757d', medium: '#ffc107', high: '#fd7e14', critical: '#dc3545' };
  return (
    <div style={{
      padding: '12px', marginBottom: '8px',
      borderLeft: `4px solid ${levelColors[event.level]}`,
      backgroundColor: event.level === 'critical' ? '#fff5f5' : '#f8f9fa',
      borderRadius: '4px',
    }}>
      <strong>#{index + 1} [{event.level.toUpperCase()}]</strong> {event.source}
      <p style={{ margin: '4px 0 0 0', color: '#666' }}>{event.description}</p>
    </div>
  );
};

// 기본 커스텀 이벤트 데모
export const BasicCustomEventsDemo: React.FC = () => {
  const {
    status, error, notifications, updates, alerts, connect, disconnect, clearEvents,
  } = useCustomEvents('/events/custom', { autoConnect: false });

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '20px' }}>
      <h2>기본 커스텀 이벤트 데모</h2>
      <p style={{ color: '#666' }}>
        event-source-polyfill을 사용한 커스텀 이벤트 수신 (notification, update, alert)
      </p>
      <div style={{ marginBottom: '16px' }}>
        <StatusBadge status={status} />
        {error && <span style={{ color: 'red', marginLeft: '12px' }}>{error}</span>}
      </div>
      <div style={{ marginBottom: '16px' }}>
        <button onClick={connect} disabled={status === 'connected' || status === 'connecting'} style={{ marginRight: '8px', padding: '8px 16px' }}>연결</button>
        <button onClick={disconnect} disabled={status === 'disconnected'} style={{ marginRight: '8px', padding: '8px 16px' }}>연결 해제</button>
        <button onClick={clearEvents} style={{ padding: '8px 16px' }}>이벤트 초기화</button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
        <div>
          <h3>Notifications ({notifications.length})</h3>
          <div style={{ maxHeight: '300px', overflow: 'auto' }}>
            {notifications.map((event, idx) => <NotificationCard key={idx} event={event} index={idx} />)}
          </div>
        </div>
        <div>
          <h3>Updates ({updates.length})</h3>
          <div style={{ maxHeight: '300px', overflow: 'auto' }}>
            {updates.map((event, idx) => <UpdateCard key={idx} event={event} index={idx} />)}
          </div>
        </div>
        <div>
          <h3>Alerts ({alerts.length})</h3>
          <div style={{ maxHeight: '300px', overflow: 'auto' }}>
            {alerts.map((event, idx) => <AlertCard key={idx} event={event} index={idx} />)}
          </div>
        </div>
      </div>
    </div>
  );
};

// 인증 커스텀 이벤트 데모
export const AuthCustomEventsDemo: React.FC = () => {
  const [token, setToken] = useState<string | null>(null);
  const [tokenInput, setTokenInput] = useState('my-secret-token');

  const {
    status, error, notifications, updates, alerts, connect, disconnect, clearEvents, isAuthenticated,
  } = useCustomEventsWithAuth('/events/custom-auth', token);

  const handleLogin = () => setToken(tokenInput);
  const handleLogout = () => { setToken(null); disconnect(); };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '20px' }}>
      <h2>인증 헤더를 사용한 커스텀 이벤트 데모</h2>
      <div style={{ marginBottom: '16px', padding: '12px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
        <strong>인증 상태:</strong> {isAuthenticated ? '로그인됨' : '로그아웃'}
      </div>
      {!isAuthenticated && (
        <div style={{ marginBottom: '16px' }}>
          <input type="text" value={tokenInput} onChange={(e) => setTokenInput(e.target.value)} placeholder="토큰 입력" style={{ padding: '8px', width: '200px', marginRight: '8px' }} />
          <button onClick={handleLogin} style={{ padding: '8px 16px' }}>로그인</button>
        </div>
      )}
      {isAuthenticated && (
        <>
          <div style={{ marginBottom: '16px' }}>
            <StatusBadge status={status} />
            {error && <span style={{ color: 'red', marginLeft: '12px' }}>{error}</span>}
          </div>
          <div style={{ marginBottom: '16px' }}>
            <button onClick={connect} disabled={status === 'connected' || status === 'connecting'} style={{ marginRight: '8px', padding: '8px 16px' }}>연결</button>
            <button onClick={disconnect} disabled={status === 'disconnected'} style={{ marginRight: '8px', padding: '8px 16px' }}>연결 해제</button>
            <button onClick={clearEvents} style={{ marginRight: '8px', padding: '8px 16px' }}>이벤트 초기화</button>
            <button onClick={handleLogout} style={{ padding: '8px 16px', backgroundColor: '#dc3545', color: 'white', border: 'none' }}>로그아웃</button>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
            <div>
              <h3>Notifications ({notifications.length})</h3>
              <div style={{ maxHeight: '300px', overflow: 'auto' }}>
                {notifications.map((event, idx) => <NotificationCard key={idx} event={event} index={idx} />)}
              </div>
            </div>
            <div>
              <h3>Updates ({updates.length})</h3>
              <div style={{ maxHeight: '300px', overflow: 'auto' }}>
                {updates.map((event, idx) => <UpdateCard key={idx} event={event} index={idx} />)}
              </div>
            </div>
            <div>
              <h3>Alerts ({alerts.length})</h3>
              <div style={{ maxHeight: '300px', overflow: 'auto' }}>
                {alerts.map((event, idx) => <AlertCard key={idx} event={event} index={idx} />)}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
